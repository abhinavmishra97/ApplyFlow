from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from app.models import Campaign, Company, EmailLog
from app.forms import CampaignForm
from app.utils.file_parser import parse_companies_file
from app.tasks import start_email_campaign
import os
from datetime import datetime

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')

@bp.route('/dashboard')
@login_required
def dashboard():
    campaigns = Campaign.query.filter_by(user_id=current_user.id).order_by(Campaign.created_at.desc()).all()
    
    # Get statistics
    stats = {
        'total_campaigns': len(campaigns),
        'active_campaigns': len([c for c in campaigns if c.status == 'active']),
        'total_sent': EmailLog.query.filter_by(user_id=current_user.id, status='sent').count(),
        'total_pending': EmailLog.query.filter_by(user_id=current_user.id, status='pending').count(),
        'total_failed': EmailLog.query.filter_by(user_id=current_user.id, status='failed').count(),
    }
    
    return render_template('dashboard.html', campaigns=campaigns, stats=stats)

@bp.route('/campaign/new', methods=['GET', 'POST'])
@login_required
def new_campaign():
    form = CampaignForm()
    
    if form.validate_on_submit():
        # Create campaign
        campaign = Campaign(
            user_id=current_user.id,
            name=form.name.data,
            email_template=form.email_template.data,
            schedule_type=form.schedule_type.data,
            scheduled_time=form.scheduled_time.data if form.schedule_type.data == 'scheduled' else None
        )
        
        # Handle resume upload
        if form.resume.data:
            resume_file = form.resume.data
            filename = secure_filename(f"{current_user.id}_{datetime.utcnow().timestamp()}_{resume_file.filename}")
            resume_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            resume_file.save(resume_path)
            campaign.resume_path = resume_path
        
        db.session.add(campaign)
        db.session.flush()  # Get campaign ID
        
        # Handle companies file upload
        if form.companies_file.data:
            companies_file = form.companies_file.data
            filename = secure_filename(companies_file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            companies_file.save(file_path)
            
            # Parse companies
            companies_data = parse_companies_file(file_path)
            
            if companies_data:
                for company_data in companies_data:
                    company = Company(
                        campaign_id=campaign.id,
                        company_name=company_data.get('company_name', ''),
                        recipient_email=company_data.get('email', ''),
                        recipient_name=company_data.get('name', ''),
                        role=company_data.get('role', ''),
                        designation=company_data.get('designation', '')
                    )
                    db.session.add(company)
                    
                    # Create email log entry
                    email_log = EmailLog(
                        campaign_id=campaign.id,
                        company_id=company.id,
                        user_id=current_user.id,
                        status='pending'
                    )
                    db.session.add(email_log)
                
                flash(f'Campaign created with {len(companies_data)} companies!', 'success')
            else:
                flash('No valid companies found in the file.', 'warning')
            
            # Clean up uploaded file
            os.remove(file_path)
        
        db.session.commit()
        
        # Start campaign if auto-send
        if campaign.schedule_type == 'auto':
            campaign.status = 'active'
            db.session.commit()
            start_email_campaign.delay(campaign.id)
            flash('Campaign started! Emails will be sent within rate limits.', 'info')
        
        return redirect(url_for('main.campaign_detail', campaign_id=campaign.id))
    
    return render_template('campaign/new.html', form=form)

@bp.route('/campaign/<int:campaign_id>')
@login_required
def campaign_detail(campaign_id):
    campaign = Campaign.query.filter_by(id=campaign_id, user_id=current_user.id).first_or_404()
    
    # Get email logs with company info
    email_logs = db.session.query(EmailLog, Company).join(Company).filter(
        EmailLog.campaign_id == campaign_id
    ).order_by(EmailLog.created_at.desc()).all()
    
    # Statistics
    stats = {
        'total': len(email_logs),
        'sent': len([log for log, _ in email_logs if log.status == 'sent']),
        'pending': len([log for log, _ in email_logs if log.status == 'pending']),
        'failed': len([log for log, _ in email_logs if log.status == 'failed']),
    }
    
    return render_template('campaign/detail.html', campaign=campaign, email_logs=email_logs, stats=stats)

@bp.route('/campaign/<int:campaign_id>/start', methods=['POST'])
@login_required
def start_campaign(campaign_id):
    campaign = Campaign.query.filter_by(id=campaign_id, user_id=current_user.id).first_or_404()
    
    if campaign.status == 'draft' or campaign.status == 'paused':
        campaign.status = 'active'
        db.session.commit()
        start_email_campaign.delay(campaign.id)
        flash('Campaign started!', 'success')
    else:
        flash('Campaign is already active or completed.', 'warning')
    
    return redirect(url_for('main.campaign_detail', campaign_id=campaign_id))

@bp.route('/campaign/<int:campaign_id>/pause', methods=['POST'])
@login_required
def pause_campaign(campaign_id):
    campaign = Campaign.query.filter_by(id=campaign_id, user_id=current_user.id).first_or_404()
    
    if campaign.status == 'active':
        campaign.status = 'paused'
        db.session.commit()
        flash('Campaign paused.', 'info')
    else:
        flash('Campaign is not active.', 'warning')
    
    return redirect(url_for('main.campaign_detail', campaign_id=campaign_id))

@bp.route('/api/campaign/<int:campaign_id>/status')
@login_required
def campaign_status_api(campaign_id):
    campaign = Campaign.query.filter_by(id=campaign_id, user_id=current_user.id).first_or_404()
    
    email_logs = EmailLog.query.filter_by(campaign_id=campaign_id).all()
    
    stats = {
        'total': len(email_logs),
        'sent': len([log for log in email_logs if log.status == 'sent']),
        'pending': len([log for log in email_logs if log.status == 'pending']),
        'failed': len([log for log in email_logs if log.status == 'failed']),
        'status': campaign.status
    }
    
    return jsonify(stats)
