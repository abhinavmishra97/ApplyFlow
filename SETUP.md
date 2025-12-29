# ApplyFlow Setup Guide

## Quick Start Checklist

- [ ] Python 3.8+ installed
- [ ] PostgreSQL installed and running
- [ ] Redis installed and running
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Database created
- [ ] Gmail API credentials configured
- [ ] Environment variables set
- [ ] Database initialized
- [ ] Gmail authenticated

## Detailed Setup Steps

### 1. Install Python Dependencies

\`\`\`bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\\Scripts\\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install packages
pip install -r requirements.txt
\`\`\`

### 2. PostgreSQL Setup

#### Windows Installation

1. Download: https://www.postgresql.org/download/windows/
2. Run installer (remember the postgres password!)
3. Default port: 5432

#### Create Database

\`\`\`bash
# Open psql
psql -U postgres

# In psql prompt:
CREATE DATABASE applyflow;
CREATE USER applyflow_user WITH PASSWORD 'SecurePassword123!';
GRANT ALL PRIVILEGES ON DATABASE applyflow TO applyflow_user;
\\q
\`\`\`

### 3. Redis Setup

#### Windows (WSL Method - Recommended)

\`\`\`bash
# Install WSL if not already installed
wsl --install

# In WSL terminal:
sudo apt update
sudo apt install redis-server
sudo service redis-server start

# Test
redis-cli ping
# Should return: PONG
\`\`\`

#### Windows (Native Method)

1. Download: https://github.com/microsoftarchive/redis/releases
2. Extract and run `redis-server.exe`

### 4. Gmail API Configuration

#### Create Google Cloud Project

1. Go to: https://console.cloud.google.com/
2. Click "New Project"
3. Name: "ApplyFlow"
4. Click "Create"

#### Enable Gmail API

1. Go to "APIs & Services" > "Library"
2. Search: "Gmail API"
3. Click "Enable"

#### Configure OAuth Consent Screen

1. Go to "APIs & Services" > "OAuth consent screen"
2. User Type: **External**
3. Click "Create"
4. Fill in:
   - App name: `ApplyFlow`
   - User support email: Your email
   - Developer contact: Your email
5. Click "Save and Continue"
6. Scopes: Click "Add or Remove Scopes"
   - Search: `gmail.send`
   - Check: `https://www.googleapis.com/auth/gmail.send`
   - Click "Update"
7. Click "Save and Continue"
8. Test users: Add your Gmail address
9. Click "Save and Continue"

#### Create OAuth Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth client ID"
3. Application type: **Desktop app**
4. Name: `ApplyFlow Desktop`
5. Click "Create"
6. Click "Download JSON"
7. Rename file to `credentials.json`
8. Move to project root directory

### 5. Environment Configuration

\`\`\`bash
# Copy example file
cp .env.example .env
\`\`\`

Edit `.env`:
\`\`\`env
SECRET_KEY=generate-random-secret-key-here
FLASK_ENV=development
DATABASE_URL=postgresql://applyflow_user:SecurePassword123!@localhost:5432/applyflow
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

### 6. Initialize Database

\`\`\`bash
python
\`\`\`

\`\`\`python
from app import create_app, db
app = create_app()
with app.app_context():
    db.create_all()
    print("Database tables created successfully!")
exit()
\`\`\`

### 7. Authenticate Gmail

\`\`\`bash
python
\`\`\`

\`\`\`python
from app.utils.email_sender import get_gmail_service
service = get_gmail_service()
print("Gmail authenticated successfully!")
exit()
\`\`\`

This will:
1. Open your browser
2. Ask you to sign in to Google
3. Request permission to send emails
4. Save token to `token.json`

### 8. Run the Application

Open **3 separate terminals**:

#### Terminal 1: Flask Server
\`\`\`bash
cd ApplyFlow
venv\\Scripts\\activate
python run.py
\`\`\`

#### Terminal 2: Celery Worker
\`\`\`bash
cd ApplyFlow
venv\\Scripts\\activate
celery -A celery_worker.celery worker --loglevel=info --pool=solo
\`\`\`

#### Terminal 3: Redis (if not running as service)
\`\`\`bash
redis-server
\`\`\`

### 9. Access the Application

Open browser: http://localhost:5000

## Testing the Setup

### 1. Create Test CSV

Create `test_companies.csv`:
\`\`\`csv
company_name,email,name,role
Test Company,your-test-email@gmail.com,Test Recruiter,Software Engineer
\`\`\`

### 2. Test Workflow

1. Register account
2. Create campaign
3. Upload test CSV
4. Start campaign
5. Check email logs

## Common Issues

### Issue: "psycopg2 not found"
\`\`\`bash
pip install psycopg2-binary
\`\`\`

### Issue: "Redis connection refused"
\`\`\`bash
# Check if Redis is running
redis-cli ping

# If not, start it
redis-server
\`\`\`

### Issue: "credentials.json not found"
- Ensure you downloaded OAuth credentials from Google Cloud Console
- File must be named exactly `credentials.json`
- File must be in project root directory

### Issue: Celery tasks not running
- Ensure Redis is running
- Use `--pool=solo` on Windows
- Check Celery worker logs for errors

## Verification Commands

\`\`\`bash
# Check Python version
python --version

# Check PostgreSQL
psql -U postgres -c "SELECT version();"

# Check Redis
redis-cli ping

# Check virtual environment
pip list

# Check database connection
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); print('DB connected!')"
\`\`\`

## Next Steps

1. ✅ Complete all setup steps
2. ✅ Test with sample CSV
3. ✅ Verify email sending
4. 📖 Read usage guide in README.md
5. 🚀 Start your job search!

## Support

If you encounter issues:
1. Check this guide
2. Review README.md troubleshooting section
3. Check terminal logs for error messages
4. Verify all services are running

---

**Setup Time: ~30-45 minutes**
