# 🚀 Getting Started with ApplyFlow

Welcome to **ApplyFlow**! This guide will help you get up and running in under an hour.

## 📋 What You'll Need

Before starting, make sure you have:

- [ ] Windows 10/11, macOS, or Linux
- [ ] Python 3.8 or higher
- [ ] A Gmail account
- [ ] 45-60 minutes of setup time

## 🎯 Overview

ApplyFlow helps you automate job search emails ethically. Here's what it does:

1. **Upload** a CSV/Excel file with company contacts
2. **Customize** your email template
3. **Send** emails automatically in the background
4. **Track** progress in real-time
5. **Stay ethical** with built-in rate limits (4/hour, 25/day)

## 🛠️ Step-by-Step Setup

### Step 1: Download & Install Prerequisites (15 minutes)

#### 1.1 Install Python
- **Windows**: Download from [python.org](https://www.python.org/downloads/)
  - ✅ Check "Add Python to PATH" during installation
- **Mac**: `brew install python3`
- **Linux**: `sudo apt install python3 python3-pip`

Verify: `python --version` (should show 3.8+)

#### 1.2 Install PostgreSQL
- **Windows**: Download from [postgresql.org](https://www.postgresql.org/download/windows/)
  - Remember the password you set!
  - Default port: 5432
- **Mac**: `brew install postgresql && brew services start postgresql`
- **Linux**: `sudo apt install postgresql postgresql-contrib`

Verify: `psql --version`

#### 1.3 Install Redis
- **Windows**: Use WSL or download from [GitHub](https://github.com/microsoftarchive/redis/releases)
- **Mac**: `brew install redis && brew services start redis`
- **Linux**: `sudo apt install redis-server`

Verify: `redis-cli ping` (should return "PONG")

### Step 2: Clone & Setup Project (5 minutes)

```bash
# Navigate to your projects folder
cd Desktop

# Clone the repository (or download ZIP)
git clone https://github.com/yourusername/ApplyFlow.git
cd ApplyFlow

# Run setup script (Windows)
setup.bat

# Or manually create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Configure Database (5 minutes)

```bash
# Open PostgreSQL command line
psql -U postgres

# Create database and user
CREATE DATABASE applyflow;
CREATE USER applyflow_user WITH PASSWORD 'YourSecurePassword123!';
GRANT ALL PRIVILEGES ON DATABASE applyflow TO applyflow_user;
\q
```

### Step 4: Configure Gmail API (15 minutes)

This is the most important step!

#### 4.1 Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click **"New Project"**
3. Name: `ApplyFlow`
4. Click **"Create"**

#### 4.2 Enable Gmail API

1. In your project, go to **"APIs & Services"** → **"Library"**
2. Search for **"Gmail API"**
3. Click **"Enable"**

#### 4.3 Configure OAuth Consent Screen

1. Go to **"APIs & Services"** → **"OAuth consent screen"**
2. Choose **"External"** → Click **"Create"**
3. Fill in:
   - **App name**: `ApplyFlow`
   - **User support email**: Your email
   - **Developer contact**: Your email
4. Click **"Save and Continue"**
5. **Scopes**: Click **"Add or Remove Scopes"**
   - Search: `gmail.send`
   - Check: `https://www.googleapis.com/auth/gmail.send`
   - Click **"Update"** → **"Save and Continue"**
6. **Test users**: Add your Gmail address
7. Click **"Save and Continue"** → **"Back to Dashboard"**

#### 4.4 Create OAuth Credentials

1. Go to **"APIs & Services"** → **"Credentials"**
2. Click **"Create Credentials"** → **"OAuth client ID"**
3. Application type: **"Desktop app"**
4. Name: `ApplyFlow Desktop`
5. Click **"Create"**
6. Click **"Download JSON"**
7. **Rename** the file to `credentials.json`
8. **Move** it to your ApplyFlow project folder

### Step 5: Configure Environment (5 minutes)

```bash
# Copy example environment file
cp .env.example .env

# Edit .env file
notepad .env  # Windows
nano .env     # Mac/Linux
```

Update these values in `.env`:

```env
SECRET_KEY=your-random-secret-key-here-change-this
FLASK_ENV=development
DATABASE_URL=postgresql://applyflow_user:YourSecurePassword123!@localhost:5432/applyflow
REDIS_URL=redis://localhost:6379/0
```

### Step 6: Initialize Database (2 minutes)

```bash
python init_db.py
```

You should see:
```
✓ Database tables created successfully!
✓ Created 5 tables:
  - users
  - campaigns
  - companies
  - email_logs
  - rate_limits
```

### Step 7: Authenticate Gmail (3 minutes)

```bash
python test_gmail_auth.py
```

This will:
1. Open your browser
2. Ask you to sign in to Google
3. Request permission to send emails
4. Save authentication token

You should see:
```
✓ Gmail API authentication successful!
✓ Authenticated as: your-email@gmail.com
```

### Step 8: Run the Application (2 minutes)

Open **3 separate terminal windows**:

**Terminal 1: Flask Server**
```bash
cd ApplyFlow
venv\Scripts\activate
python run.py
```

**Terminal 2: Celery Worker**
```bash
cd ApplyFlow
venv\Scripts\activate
celery -A celery_worker.celery worker --loglevel=info --pool=solo
```

**Terminal 3: Redis** (if not running as service)
```bash
redis-server
```

### Step 9: Access the Application

Open your browser: **http://localhost:5000**

You should see the ApplyFlow landing page! 🎉

## 🎓 First Campaign Tutorial (10 minutes)

### 1. Create Account
- Click **"Get Started"**
- Enter your email and password
- Click **"Register"**

### 2. Prepare Test Data

Create a file `test_companies.csv`:
```csv
company_name,email,name,role
Test Company,your-email@gmail.com,Your Name,Software Engineer
```

**Important**: Use your own email for testing!

### 3. Create Campaign
- Click **"New Campaign"**
- Fill in:
  - **Campaign Name**: "Test Campaign"
  - **Companies File**: Upload `test_companies.csv`
  - **Resume**: Upload your PDF resume (optional)
  - **Email Template**: Customize the default template
  - **Schedule Type**: "Auto-send within safe limits"
- Click **"Create Campaign"**

### 4. Monitor Progress
- You'll be redirected to the campaign detail page
- Watch the statistics update in real-time
- Check your email inbox for the test email!

### 5. Verify in Celery Logs
In Terminal 2 (Celery worker), you should see:
```
[INFO] Task app.tasks.start_email_campaign started
[INFO] Sending email to: your-email@gmail.com
[INFO] Email sent successfully!
```

## ✅ Verification Checklist

After setup, verify everything works:

- [ ] Flask server running on http://localhost:5000
- [ ] Celery worker running without errors
- [ ] Redis responding to `redis-cli ping`
- [ ] Can register and login
- [ ] Can create campaign
- [ ] Can upload CSV file
- [ ] Test email received in inbox
- [ ] Campaign statistics updating

## 🐛 Common Issues & Solutions

### "Module not found" error
```bash
# Ensure virtual environment is activated
venv\Scripts\activate
pip install -r requirements.txt
```

### "Database connection error"
```bash
# Check PostgreSQL is running
net start postgresql-x64-15  # Windows
brew services start postgresql  # Mac
sudo service postgresql start  # Linux
```

### "Redis connection refused"
```bash
# Start Redis
redis-server
```

### "credentials.json not found"
- Ensure you downloaded OAuth credentials from Google Cloud Console
- File must be named exactly `credentials.json`
- File must be in project root folder

### Celery tasks not running
```bash
# Windows: Use --pool=solo
celery -A celery_worker.celery worker --loglevel=info --pool=solo

# Check Redis is running
redis-cli ping
```

### Gmail authentication error
```bash
# Delete token and re-authenticate
del token.json  # Windows
rm token.json   # Mac/Linux
python test_gmail_auth.py
```

## 📚 Next Steps

Now that you're set up:

1. **Read the docs**:
   - `README.md` - Full documentation
   - `QUICK_REFERENCE.md` - Common commands
   - `ARCHITECTURE.md` - System design

2. **Customize your templates**:
   - See `email_template_example.txt` for ideas
   - Use placeholders: `{company_name}`, `{recipient_name}`, etc.

3. **Prepare your real data**:
   - Create a CSV with actual company contacts
   - Ensure emails are valid
   - Include company names and roles

4. **Start your job search**:
   - Create a real campaign
   - Monitor progress
   - Track responses

## 💡 Pro Tips

1. **Test first**: Always send test emails to yourself before real campaigns
2. **Personalize**: Customize templates for each industry/role
3. **Monitor logs**: Keep an eye on Celery worker logs
4. **Stay ethical**: Respect the rate limits (4/hour, 25/day)
5. **Track responses**: Keep a spreadsheet of companies that respond
6. **Follow up**: Respond promptly to any replies

## 🎯 Success Metrics

After your first week:
- [ ] Sent 25+ emails
- [ ] Zero spam complaints
- [ ] At least 1 response
- [ ] Campaign running smoothly
- [ ] Comfortable with the workflow

## 📞 Need Help?

If you're stuck:

1. Check `QUICK_REFERENCE.md` for common commands
2. Review `SETUP.md` for detailed setup instructions
3. Check terminal logs for error messages
4. Verify all services are running
5. Try the troubleshooting section in `README.md`

## 🎉 You're Ready!

Congratulations! You've successfully set up ApplyFlow. 

**Remember**: Use this tool responsibly and ethically. Good luck with your job search! 🚀

---

**Setup Time**: ~45-60 minutes  
**Difficulty**: Intermediate  
**Support**: Check README.md for detailed documentation
