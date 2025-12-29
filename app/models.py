from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    campaigns = db.relationship('Campaign', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.email}>'

class Campaign(db.Model):
    __tablename__ = 'campaigns'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    resume_path = db.Column(db.String(500))
    email_template = db.Column(db.Text, nullable=False)
    schedule_type = db.Column(db.String(50), default='auto')  # 'auto' or 'scheduled'
    scheduled_time = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(50), default='draft')  # draft, active, paused, completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    companies = db.relationship('Company', backref='campaign', lazy=True, cascade='all, delete-orphan')
    email_logs = db.relationship('EmailLog', backref='campaign', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Campaign {self.name}>'

class Company(db.Model):
    __tablename__ = 'companies'
    
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaigns.id'), nullable=False)
    company_name = db.Column(db.String(200), nullable=False)
    recipient_email = db.Column(db.String(120), nullable=False)
    recipient_name = db.Column(db.String(200))
    role = db.Column(db.String(200))
    designation = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    email_logs = db.relationship('EmailLog', backref='company', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Company {self.company_name}>'

class EmailLog(db.Model):
    __tablename__ = 'email_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaigns.id'), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(50), default='pending')  # pending, sent, failed, paused
    error_message = db.Column(db.Text)
    sent_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to user
    user = db.relationship('User', backref='email_logs')
    
    def __repr__(self):
        return f'<EmailLog {self.id} - {self.status}>'

class RateLimit(db.Model):
    __tablename__ = 'rate_limits'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    hour_start = db.Column(db.DateTime, nullable=False)
    day_start = db.Column(db.DateTime, nullable=False)
    emails_this_hour = db.Column(db.Integer, default=0)
    emails_today = db.Column(db.Integer, default=0)
    last_email_sent = db.Column(db.DateTime)
    
    # Relationship
    user = db.relationship('User', backref='rate_limit', uselist=False)
    
    def __repr__(self):
        return f'<RateLimit User {self.user_id}>'
