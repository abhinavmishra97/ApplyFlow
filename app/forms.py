from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, DateTimeLocalField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from app.models import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use a different email.')

class CampaignForm(FlaskForm):
    name = StringField('Campaign Name', validators=[DataRequired(), Length(max=200)])
    companies_file = FileField('Companies File (CSV/Excel)', 
                               validators=[FileRequired(), FileAllowed(['csv', 'xlsx', 'xls'], 'Only CSV and Excel files allowed!')])
    resume = FileField('Resume (PDF)', 
                      validators=[FileAllowed(['pdf'], 'Only PDF files allowed!')])
    email_template = TextAreaField('Email Template', validators=[DataRequired()], 
                                   default="""Subject: Exploring Opportunities at {company_name}

Dear Hiring Manager,

I hope this email finds you well. I am reaching out to express my interest in potential opportunities at {company_name}.

I am a passionate software engineer with experience in full-stack development, and I am particularly impressed by your company's work and culture. I have attached my resume for your review.

I would be grateful for the opportunity to discuss how my skills and experience could contribute to your team.

Thank you for your time and consideration.

Best regards,
[Your Name]
[Your Contact Information]""")
    schedule_type = SelectField('Schedule Type', 
                               choices=[('auto', 'Auto-send within safe limits'), ('scheduled', 'Schedule for specific time')],
                               default='auto')
    scheduled_time = DateTimeLocalField('Scheduled Time', format='%Y-%m-%dT%H:%M', validators=[])
    submit = SubmitField('Create Campaign')
