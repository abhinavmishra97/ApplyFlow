import os
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def get_gmail_service():
    """
    Authenticate and return Gmail API service.
    """
    creds = None
    token_file = 'token.json'
    credentials_file = 'credentials.json'
    
    # Load existing token
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    
    # If no valid credentials, authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(credentials_file):
                raise FileNotFoundError(
                    "credentials.json not found. Please download it from Google Cloud Console."
                )
            flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save credentials
        with open(token_file, 'w') as token:
            token.write(creds.to_json())
    
    return build('gmail', 'v1', credentials=creds)

def send_email_via_gmail(to_email, subject, body, resume_path=None):
    """
    Send email using Gmail API.
    Returns (success: bool, error_message: str or None)
    """
    try:
        service = get_gmail_service()
        
        # Create message
        message = MIMEMultipart()
        message['to'] = to_email
        message['subject'] = subject
        
        # Add body
        message.attach(MIMEText(body, 'plain'))
        
        # Attach resume if provided
        if resume_path and os.path.exists(resume_path):
            with open(resume_path, 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename={os.path.basename(resume_path)}'
                )
                message.attach(part)
        
        # Encode message
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
        
        # Send message
        send_message = service.users().messages().send(
            userId='me',
            body={'raw': raw_message}
        ).execute()
        
        return True, None
    
    except HttpError as error:
        return False, f"Gmail API error: {error}"
    except Exception as e:
        return False, f"Error sending email: {str(e)}"

def prepare_email_content(template, company_data):
    """
    Replace placeholders in email template with company data.
    """
    content = template
    
    # Replace placeholders
    replacements = {
        '{company_name}': company_data.get('company_name', ''),
        '{recipient_name}': company_data.get('recipient_name', 'Hiring Manager'),
        '{role}': company_data.get('role', ''),
        '{designation}': company_data.get('designation', ''),
    }
    
    for placeholder, value in replacements.items():
        content = content.replace(placeholder, value)
    
    # Extract subject and body
    lines = content.split('\n')
    subject = ''
    body_lines = []
    
    for i, line in enumerate(lines):
        if line.startswith('Subject:'):
            subject = line.replace('Subject:', '').strip()
        elif i > 0 or not line.startswith('Subject:'):
            body_lines.append(line)
    
    body = '\n'.join(body_lines).strip()
    
    return subject, body
