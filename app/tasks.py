from celery import Celery
from config import Config
import time
import random
from datetime import datetime, timedelta

# Initialize Celery
celery = Celery('applyflow')
celery.config_from_object(Config)

@celery.task(bind=True)
def start_email_campaign(self, campaign_id):
    """
    Background task to send emails for a campaign with rate limiting.
    """
    from app import create_app, db
    from app.models import Campaign, Company, EmailLog, RateLimit
    from app.utils.email_sender import send_email_via_gmail, prepare_email_content
    
    app = create_app()
    
    with app.app_context():
        campaign = Campaign.query.get(campaign_id)
        if not campaign or campaign.status != 'active':
            return
        
        user_id = campaign.user_id
        
        # Get or create rate limit tracker
        rate_limit = RateLimit.query.filter_by(user_id=user_id).first()
        if not rate_limit:
            rate_limit = RateLimit(
                user_id=user_id,
                hour_start=datetime.utcnow(),
                day_start=datetime.utcnow(),
                emails_this_hour=0,
                emails_today=0
            )
            db.session.add(rate_limit)
            db.session.commit()
        
        # Reset counters if needed
        now = datetime.utcnow()
        if now - rate_limit.hour_start >= timedelta(hours=1):
            rate_limit.hour_start = now
            rate_limit.emails_this_hour = 0
        
        if now - rate_limit.day_start >= timedelta(days=1):
            rate_limit.day_start = now
            rate_limit.emails_today = 0
        
        db.session.commit()
        
        # Get pending emails
        pending_logs = EmailLog.query.filter_by(
            campaign_id=campaign_id,
            status='pending'
        ).all()
        
        if not pending_logs:
            campaign.status = 'completed'
            db.session.commit()
            return
        
        # Send emails with rate limiting
        for email_log in pending_logs:
            # Check if campaign is still active
            db.session.refresh(campaign)
            if campaign.status != 'active':
                break
            
            # Check rate limits
            db.session.refresh(rate_limit)
            if rate_limit.emails_this_hour >= Config.MAX_EMAILS_PER_HOUR:
                # Wait until next hour
                wait_time = 3600 - (datetime.utcnow() - rate_limit.hour_start).total_seconds()
                if wait_time > 0:
                    time.sleep(wait_time)
                rate_limit.hour_start = datetime.utcnow()
                rate_limit.emails_this_hour = 0
                db.session.commit()
            
            if rate_limit.emails_today >= Config.MAX_EMAILS_PER_DAY:
                # Pause campaign until tomorrow
                campaign.status = 'paused'
                db.session.commit()
                # Schedule to resume tomorrow
                resume_time = (datetime.utcnow() + timedelta(days=1)).replace(hour=9, minute=0, second=0)
                resume_campaign.apply_async((campaign_id,), eta=resume_time)
                break
            
            # Get company data
            company = Company.query.get(email_log.company_id)
            if not company:
                continue
            
            # Prepare email
            company_data = {
                'company_name': company.company_name,
                'recipient_name': company.recipient_name or 'Hiring Manager',
                'role': company.role or '',
                'designation': company.designation or '',
            }
            
            subject, body = prepare_email_content(campaign.email_template, company_data)
            
            # Send email
            success, error = send_email_via_gmail(
                to_email=company.recipient_email,
                subject=subject,
                body=body,
                resume_path=campaign.resume_path
            )
            
            # Update email log
            if success:
                email_log.status = 'sent'
                email_log.sent_at = datetime.utcnow()
                rate_limit.emails_this_hour += 1
                rate_limit.emails_today += 1
                rate_limit.last_email_sent = datetime.utcnow()
            else:
                email_log.status = 'failed'
                email_log.error_message = error
            
            db.session.commit()
            
            # Random delay between emails (60-300 seconds)
            if success:
                delay = random.randint(Config.MIN_DELAY_SECONDS, Config.MAX_DELAY_SECONDS)
                time.sleep(delay)
        
        # Check if campaign is complete
        remaining = EmailLog.query.filter_by(campaign_id=campaign_id, status='pending').count()
        if remaining == 0:
            campaign.status = 'completed'
            db.session.commit()

@celery.task
def resume_campaign(campaign_id):
    """
    Resume a paused campaign.
    """
    from app import create_app, db
    from app.models import Campaign
    
    app = create_app()
    
    with app.app_context():
        campaign = Campaign.query.get(campaign_id)
        if campaign and campaign.status == 'paused':
            campaign.status = 'active'
            db.session.commit()
            start_email_campaign.delay(campaign_id)
