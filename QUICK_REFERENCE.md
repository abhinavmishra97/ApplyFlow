# ApplyFlow - Quick Reference Guide

## 🚀 Quick Start Commands

### Initial Setup (One-time)
```bash
# 1. Run setup script (Windows)
setup.bat

# 2. Edit .env file with your credentials
notepad .env

# 3. Initialize database
python init_db.py

# 4. Test Gmail authentication
python test_gmail_auth.py
```

### Running the Application (Every time)

**Terminal 1: Flask Server**
```bash
venv\Scripts\activate
python run.py
```

**Terminal 2: Celery Worker**
```bash
venv\Scripts\activate
celery -A celery_worker.celery worker --loglevel=info --pool=solo
```

**Terminal 3: Redis (if not running as service)**
```bash
redis-server
```

**Access**: http://localhost:5000

## 📁 File Upload Format

### CSV/Excel Columns
| Column Name | Required | Example |
|-------------|----------|---------|
| company_name | ✅ Yes | Google |
| email | ✅ Yes | hr@google.com |
| name | ❌ No | John Doe |
| role | ❌ No | Software Engineer |
| designation | ❌ No | Senior Recruiter |

### Accepted Variations
- `company` → `company_name`
- `email id` → `email`
- `recipient name` → `name`
- `position` → `role`
- `title` → `designation`

## 📧 Email Template Placeholders

```
{company_name}     → Company name from CSV
{recipient_name}   → Recipient name (or "Hiring Manager")
{role}             → Role from CSV
{designation}      → Designation from CSV
```

## 🔒 Rate Limits

| Limit | Value |
|-------|-------|
| Emails per hour | 4 |
| Emails per day | 25 |
| Min delay between emails | 60 seconds |
| Max delay between emails | 300 seconds |

## 🎯 Campaign Workflow

1. **Create Campaign**
   - Dashboard → New Campaign
   - Enter campaign name
   - Upload companies CSV/Excel
   - Upload resume (optional)
   - Customize email template
   - Choose schedule type

2. **Start Campaign**
   - Auto-send: Starts immediately
   - Scheduled: Starts at specified time

3. **Monitor Progress**
   - View dashboard statistics
   - Check campaign details
   - Review email logs

4. **Manage Campaign**
   - Pause: Temporarily stop sending
   - Resume: Continue sending
   - View: Check status and logs

## 🗄️ Database Commands

### Create Tables
```python
python init_db.py
```

### Reset Database (⚠️ Deletes all data)
```python
from app import create_app, db
app = create_app()
with app.app_context():
    db.drop_all()
    db.create_all()
```

### Check Database
```bash
psql -U postgres -d applyflow
\dt  # List tables
\d users  # Describe users table
```

## 🔧 Troubleshooting

### Flask won't start
```bash
# Check if port 5000 is in use
netstat -ano | findstr :5000

# Kill process if needed
taskkill /PID <PID> /F
```

### Celery not processing tasks
```bash
# Check Redis connection
redis-cli ping

# Check Celery logs for errors
# Ensure using --pool=solo on Windows
```

### Database connection error
```bash
# Check PostgreSQL is running
net start postgresql-x64-15

# Verify DATABASE_URL in .env
```

### Gmail authentication error
```bash
# Re-authenticate
python test_gmail_auth.py

# Delete token.json and re-authenticate
del token.json
python test_gmail_auth.py
```

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Landing page |
| `/auth/register` | GET, POST | User registration |
| `/auth/login` | GET, POST | User login |
| `/auth/logout` | GET | User logout |
| `/dashboard` | GET | User dashboard |
| `/campaign/new` | GET, POST | Create campaign |
| `/campaign/<id>` | GET | Campaign details |
| `/campaign/<id>/start` | POST | Start campaign |
| `/campaign/<id>/pause` | POST | Pause campaign |
| `/api/campaign/<id>/status` | GET | Campaign status (JSON) |

## 🎨 UI Components

### Status Badges
- **draft**: Gray (campaign not started)
- **active**: Green (currently sending)
- **paused**: Orange (temporarily stopped)
- **completed**: Blue (all emails sent)

### Email Status
- **pending**: Yellow (queued, not sent)
- **sent**: Green (successfully sent)
- **failed**: Red (error occurred)

## 📝 Environment Variables

```env
SECRET_KEY=<random-secret-key>
FLASK_ENV=development
DATABASE_URL=postgresql://user:pass@localhost:5432/applyflow
REDIS_URL=redis://localhost:6379/0
GMAIL_CREDENTIALS_FILE=credentials.json
GMAIL_TOKEN_FILE=token.json
MAX_EMAILS_PER_HOUR=4
MAX_EMAILS_PER_DAY=25
MIN_DELAY_SECONDS=60
MAX_DELAY_SECONDS=300
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216
```

## 🔑 Important Files

| File | Purpose |
|------|---------|
| `credentials.json` | Gmail OAuth credentials (download from Google) |
| `token.json` | Gmail access token (auto-generated) |
| `.env` | Environment variables (create from .env.example) |
| `uploads/` | User-uploaded files (auto-created) |

## 🐛 Common Errors

### "credentials.json not found"
→ Download OAuth credentials from Google Cloud Console

### "psycopg2 not found"
→ `pip install psycopg2-binary`

### "Redis connection refused"
→ Start Redis server: `redis-server`

### "Database does not exist"
→ Create database: `psql -U postgres -c "CREATE DATABASE applyflow;"`

### "Celery tasks not running"
→ Ensure Redis is running and use `--pool=solo` on Windows

## 📞 Support Resources

- **README.md**: Comprehensive documentation
- **SETUP.md**: Detailed setup instructions
- **PROJECT_SUMMARY.md**: Architecture and features
- **sample_companies.csv**: Example data file
- **email_template_example.txt**: Example email template

## 🎯 Testing Checklist

- [ ] Register new account
- [ ] Login successfully
- [ ] Upload sample CSV
- [ ] Create campaign
- [ ] Start campaign
- [ ] Check Celery logs for task execution
- [ ] Verify email sent (check Gmail)
- [ ] View campaign statistics
- [ ] Pause campaign
- [ ] Resume campaign

## 💡 Pro Tips

1. **Test with your own email first** before sending to real companies
2. **Customize email templates** to match your experience
3. **Use professional language** in all communications
4. **Monitor Celery logs** to debug email sending issues
5. **Keep credentials.json secure** - never commit to Git
6. **Backup your database** before major changes
7. **Use .env for sensitive data** - never hardcode credentials

## 🚀 Production Deployment

### Before Deploying
- [ ] Set `FLASK_ENV=production`
- [ ] Use strong `SECRET_KEY`
- [ ] Use production database (not SQLite)
- [ ] Enable HTTPS
- [ ] Use Gunicorn/uWSGI instead of Flask dev server
- [ ] Set up proper logging
- [ ] Configure firewall
- [ ] Use environment variables for all secrets

### Recommended Platforms
- **Heroku**: Easy deployment, free tier available
- **Railway**: Modern, simple, free tier
- **DigitalOcean**: VPS, more control
- **AWS**: Scalable, professional

---

**Quick Help**: If stuck, check README.md troubleshooting section or run `python test_gmail_auth.py` to verify Gmail setup.
