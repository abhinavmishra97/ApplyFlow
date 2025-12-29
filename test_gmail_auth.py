"""
Gmail API Authentication Test Script
Run this after setting up credentials.json to authenticate your Gmail account
"""

import os
import sys

def test_gmail_auth():
    print("=" * 50)
    print("Gmail API Authentication Test")
    print("=" * 50)
    print()
    
    # Check if credentials.json exists
    if not os.path.exists('credentials.json'):
        print("❌ ERROR: credentials.json not found!")
        print()
        print("Please download OAuth credentials from Google Cloud Console:")
        print("1. Go to: https://console.cloud.google.com/")
        print("2. Select your project")
        print("3. Go to: APIs & Services > Credentials")
        print("4. Download OAuth 2.0 Client ID JSON")
        print("5. Rename to 'credentials.json' and place in project root")
        print()
        return False
    
    print("✓ credentials.json found")
    print()
    
    # Try to authenticate
    try:
        print("Attempting to authenticate with Gmail API...")
        print("This will open your browser for authorization.")
        print()
        
        from app.utils.email_sender import get_gmail_service
        
        service = get_gmail_service()
        
        print("✓ Gmail API authentication successful!")
        print("✓ token.json has been created")
        print()
        
        # Test getting user profile
        profile = service.users().getProfile(userId='me').execute()
        email = profile.get('emailAddress')
        
        print(f"✓ Authenticated as: {email}")
        print()
        print("=" * 50)
        print("Authentication Complete!")
        print("=" * 50)
        print()
        print("You can now use ApplyFlow to send emails.")
        print()
        return True
        
    except FileNotFoundError as e:
        print(f"❌ ERROR: {e}")
        print()
        print("Make sure credentials.json is in the project root directory.")
        return False
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        print()
        print("Authentication failed. Please check:")
        print("1. credentials.json is valid")
        print("2. Gmail API is enabled in Google Cloud Console")
        print("3. OAuth consent screen is configured")
        print("4. Your email is added as a test user")
        print()
        return False

if __name__ == '__main__':
    success = test_gmail_auth()
    sys.exit(0 if success else 1)
