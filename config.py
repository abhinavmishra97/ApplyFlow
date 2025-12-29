import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://localhost/applyflow')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Redis & Celery
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    CELERY_BROKER_URL = REDIS_URL
    CELERY_RESULT_BACKEND = REDIS_URL
    
    # Gmail API
    GMAIL_CREDENTIALS_FILE = os.getenv('GMAIL_CREDENTIALS_FILE', 'credentials.json')
    GMAIL_TOKEN_FILE = os.getenv('GMAIL_TOKEN_FILE', 'token.json')
    
    # Rate Limiting
    MAX_EMAILS_PER_HOUR = int(os.getenv('MAX_EMAILS_PER_HOUR', 4))
    MAX_EMAILS_PER_DAY = int(os.getenv('MAX_EMAILS_PER_DAY', 25))
    MIN_DELAY_SECONDS = int(os.getenv('MIN_DELAY_SECONDS', 60))
    MAX_DELAY_SECONDS = int(os.getenv('MAX_DELAY_SECONDS', 300))
    
    # Upload
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16MB
    ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls', 'pdf', 'docx'}
