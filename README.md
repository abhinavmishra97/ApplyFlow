# ApplyFlow - Ethical Job Search Automation

![ApplyFlow](https://img.shields.io/badge/Status-Production%20Ready-success)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

**ApplyFlow** is a professional, ethical job search automation tool that helps you send personalized cold emails to companies while maintaining strict rate limits and anti-spam measures..

## 🌟 Features

- **User Authentication**: Secure account creation and login
- **File Upload**: Upload Excel/CSV files with company data
- **Resume Attachment**: Attach your PDF resume to emails
- **Email Templates**: Customizable templates with placeholders
- **Background Processing**: Emails send via Celery workers, even when offline
- **Ethical Rate Limiting**: 
  - Maximum 4 emails per hour
  - Maximum 25 emails per day
  - Random delays (60-300 seconds) between sends
- **Gmail API Integration**: Reliable email delivery via Gmail
- **Real-time Dashboard**: Track sent, pending, and failed emails
- **Campaign Management**: Create, start, pause, and monitor campaigns

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **Database**: PostgreSQL
- **Task Queue**: Celery + Redis
- **Email**: Gmail API
- **Frontend**: Jinja2 Templates, HTML/CSS/JavaScript
- **Authentication**: Flask-Login

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.8 or higher
- PostgreSQL 12 or higher
- Redis 6 or higher
- Git

## 🚀 Installation & Setup

### 1. Clone the Repository

\`\`\`bash
git clone https://github.com/yourusername/ApplyFlow.git
cd ApplyFlow
\`\`\`

### 2. Create Virtual Environment

\`\`\`bash
# Windows
python -m venv venv
venv\\Scripts\\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
\`\`\`

### 3. Install Dependencies

\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 4. Install PostgreSQL

**Windows:**
1. Download PostgreSQL from [postgresql.org](https://www.postgresql.org/download/windows/)
2. Run the installer and follow the setup wizard
3. Remember the password you set for the `postgres` user
4. Add PostgreSQL to your PATH (usually `C:\\Program Files\\PostgreSQL\\15\\bin`)

**Linux (Ubuntu/Debian):**
\`\`\`bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
\`\`\`

**macOS:**
\`\`\`bash
brew install postgresql
brew services start postgresql
\`\`\`

### 5. Create Database

\`\`\`bash
# Windows (PowerShell)
psql -U postgres

# Linux/Mac
sudo -u postgres psql
\`\`\`

Then in the PostgreSQL prompt:
\`\`\`sql
CREATE DATABASE applyflow;
CREATE USER applyflow_user WITH PASSWORD 'your_password_here';
GRANT ALL PRIVILEGES ON DATABASE applyflow TO applyflow_user;
\\q
\`\`\`

### 6. Install Redis

**Windows:**
1. Download Redis from [github.com/microsoftarchive/redis/releases](https://github.com/microsoftarchive/redis/releases)
2. Extract and run `redis-server.exe`

Or use WSL:
\`\`\`bash
wsl --install
wsl
sudo apt update
sudo apt install redis-server
sudo service redis-server start
\`\`\`

**Linux (Ubuntu/Debian):**
\`\`\`bash
sudo apt update
sudo apt install redis-server
sudo systemctl start redis
sudo systemctl enable redis
\`\`\`

**macOS:**
\`\`\`bash
brew install redis
brew services start redis
\`\`\`

Verify Redis is running:
\`\`\`bash
redis-cli ping
# Should return: PONG
\`\`\`

### 7. Configure Gmail API

#### Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (e.g., "ApplyFlow")
3. Enable the Gmail API:
   - Go to "APIs & Services" > "Library"
   - Search for "Gmail API"
   - Click "Enable"

#### Step 2: Create OAuth 2.0 Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth client ID"
3. Configure consent screen if prompted:
   - User Type: External
   - App name: ApplyFlow
   - User support email: Your email
   - Developer contact: Your email
   - Add scope: `https://www.googleapis.com/auth/gmail.send`
   - Add test users: Your Gmail address
4. Create OAuth client ID:
   - Application type: Desktop app
   - Name: ApplyFlow Desktop
5. Download the JSON file
6. Rename it to `credentials.json` and place it in the project root directory

### 8. Configure Environment Variables

Copy the example environment file:
\`\`\`bash
cp .env.example .env
\`\`\`

Edit `.env` with your settings:
\`\`\`env
SECRET_KEY=your-secret-key-here-change-this-in-production
FLASK_ENV=development

# Update with your PostgreSQL credentials
DATABASE_URL=postgresql://applyflow_user:your_password_here@localhost:5432/applyflow

REDIS_URL=redis://localhost:6379/0

GMAIL_CREDENTIALS_FILE=credentials.json
GMAIL_TOKEN_FILE=token.json

MAX_EMAILS_PER_HOUR=4
MAX_EMAILS_PER_DAY=25
MIN_DELAY_SECONDS=60
MAX_DELAY_SECONDS=300

UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216
\`\`\`

### 9. Initialize Database

\`\`\`bash
python
>>> from app import create_app, db
>>> app = create_app()
>>> with app.app_context():
...     db.create_all()
>>> exit()
\`\`\`

### 10. Authenticate Gmail API (First Time Only)

Run this once to authenticate:
\`\`\`bash
python
>>> from app.utils.email_sender import get_gmail_service
>>> get_gmail_service()
\`\`\`

This will:
1. Open your browser
2. Ask you to log in to your Google account
3. Request permission to send emails
4. Save the token to `token.json`

## 🎯 Running the Application

You need to run **three separate processes**:

### Terminal 1: Flask Web Server

\`\`\`bash
python run.py
\`\`\`

The app will be available at: `http://localhost:5000`

### Terminal 2: Celery Worker

\`\`\`bash
celery -A celery_worker.celery worker --loglevel=info --pool=solo
\`\`\`

Note: On Windows, use `--pool=solo`. On Linux/Mac, you can omit this flag.

### Terminal 3: Redis Server

If not running as a service:
\`\`\`bash
redis-server
\`\`\`

## 📊 Usage Guide

### 1. Create Account
- Navigate to `http://localhost:5000`
- Click "Get Started" or "Register"
- Enter your email and password

### 2. Create Campaign
- Click "New Campaign" from the dashboard
- Fill in campaign details:
  - **Campaign Name**: e.g., "Software Engineer Applications - Jan 2025"
  - **Companies File**: Upload CSV/Excel with columns:
    - `company_name` (required)
    - `email` (required)
    - `name` (optional)
    - `role` (optional)
    - `designation` (optional)
  - **Resume**: Upload your PDF resume (optional)
  - **Email Template**: Customize the template with placeholders:
    - `{company_name}`
    - `{recipient_name}`
    - `{role}`
    - `{designation}`
  - **Schedule Type**: Choose "Auto-send" or "Scheduled"

### 3. Start Campaign
- Click "Create Campaign"
- The system will:
  - Parse and validate your companies file
  - Remove duplicates
  - Create email queue
  - Start sending (if auto-send enabled)

### 4. Monitor Progress
- View real-time statistics on the dashboard
- Check individual campaign details
- See sent, pending, and failed emails
- Pause/resume campaigns as needed

## 📁 CSV/Excel File Format

Example `companies.csv`:
\`\`\`csv
company_name,email,name,role,designation
Google,hr@google.com,John Doe,Software Engineer,Senior Recruiter
Microsoft,careers@microsoft.com,Jane Smith,Full Stack Developer,HR Manager
Amazon,jobs@amazon.com,,,
\`\`\`

## 🔒 Ethical Guidelines

ApplyFlow is designed with ethics in mind:

- **Rate Limiting**: Strict limits prevent spam behavior
- **One Email Per Company**: No duplicate sends
- **Random Delays**: Mimics human behavior
- **Professional Templates**: Encourages personalized, respectful communication
- **Transparent Logging**: All sends are tracked and logged
- **User Responsibility**: Users must ensure compliance with local laws

## 🐛 Troubleshooting

### PostgreSQL Connection Error
\`\`\`
Error: could not connect to server
\`\`\`
**Solution**: Ensure PostgreSQL is running:
\`\`\`bash
# Windows
net start postgresql-x64-15

# Linux
sudo systemctl start postgresql
\`\`\`

### Redis Connection Error
\`\`\`
Error: Error 10061 connecting to localhost:6379
\`\`\`
**Solution**: Start Redis server:
\`\`\`bash
redis-server
\`\`\`

### Gmail API Authentication Error
\`\`\`
Error: credentials.json not found
\`\`\`
**Solution**: Download OAuth credentials from Google Cloud Console and save as `credentials.json`

### Celery Worker Not Processing Tasks
**Solution**: Ensure you're using `--pool=solo` on Windows:
\`\`\`bash
celery -A celery_worker.celery worker --loglevel=info --pool=solo
\`\`\`

## 📝 Project Structure

\`\`\`
ApplyFlow/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── models.py            # Database models
│   ├── forms.py             # WTForms
│   ├── tasks.py             # Celery tasks
│   ├── routes/
│   │   ├── auth.py          # Authentication routes
│   │   └── main.py          # Main app routes
│   ├── utils/
│   │   ├── email_sender.py  # Gmail API integration
│   │   └── file_parser.py   # CSV/Excel parser
│   ├── templates/           # Jinja2 templates
│   └── static/
│       └── css/
│           └── style.css    # Styles
├── uploads/                 # User uploads (auto-created)
├── config.py               # Configuration
├── run.py                  # Flask entry point
├── celery_worker.py        # Celery entry point
├── requirements.txt        # Dependencies
├── .env                    # Environment variables
├── credentials.json        # Gmail OAuth (you create)
└── token.json             # Gmail token (auto-created)
\`\`\`

## 🚀 Deployment

For production deployment:

1. **Update `.env`**:
   - Set `FLASK_ENV=production`
   - Use strong `SECRET_KEY`
   - Use production database URL

2. **Use Production Server**:
   \`\`\`bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 run:app
   \`\`\`

3. **Run Celery as Service** (Linux):
   Create `/etc/systemd/system/celery.service`

4. **Use Nginx as Reverse Proxy**

5. **Enable HTTPS** with Let's Encrypt

## 📄 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## ⚠️ Disclaimer

This tool is designed for legitimate job search purposes only. Users are responsible for:
- Complying with anti-spam laws (CAN-SPAM, GDPR, etc.)
- Obtaining necessary permissions
- Using professional, respectful communication
- Following rate limits and ethical guidelines

Misuse of this tool may result in account suspension or legal consequences.

## 📧 Support

For issues or questions:
- Open an issue on GitHub
- Email: support@applyflow.com (example)

---

**Built with ❤️ for ethical job seekers**
