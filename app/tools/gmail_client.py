"""Gmail API client for sending email notifications"""
import base64
import os
from email.mime.text import MIMEText
from typing import Optional
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


SCOPES = ['https://www.googleapis.com/auth/gmail.send']


class GmailClient:
    """Gmail API client for sending emails"""
    
    def __init__(self, credentials_path: Optional[str] = None):
        """Initialize Gmail client with credentials"""
        self.credentials_path = credentials_path or os.getenv('GMAIL_API_CREDENTIALS')
        self.creds = None
        self.service = None
    
    def authenticate(self) -> None:
        """Authenticate with Gmail API"""
        token_path = 'token.json'
        
        # Load existing credentials
        if os.path.exists(token_path):
            self.creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        
        # Refresh or get new credentials
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            elif self.credentials_path and os.path.exists(self.credentials_path):
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES
                )
                self.creds = flow.run_local_server(port=0)
            else:
                raise ValueError(
                    "Gmail credentials not found. Set GMAIL_API_CREDENTIALS environment variable "
                    "or provide credentials_path"
                )
            
            # Save credentials for next run
            with open(token_path, 'w') as token:
                token.write(self.creds.to_json())
        
        # Build service
        self.service = build('gmail', 'v1', credentials=self.creds)
    
    def create_message(
        self,
        to: str,
        subject: str,
        body: str,
        from_email: str = 'me'
    ) -> dict:
        """Create an email message"""
        message = MIMEText(body)
        message['to'] = to
        message['from'] = from_email
        message['subject'] = subject
        
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
        return {'raw': raw_message}
    
    async def send_email(
        self,
        to: str,
        subject: str,
        body: str,
        from_email: str = 'me'
    ) -> dict:
        """Send an email via Gmail API"""
        try:
            # Ensure authenticated
            if not self.service:
                self.authenticate()
            
            # Create message
            message = self.create_message(to, subject, body, from_email)
            
            # Send message
            sent_message = self.service.users().messages().send(
                userId='me',
                body=message
            ).execute()
            
            return {
                'success': True,
                'message_id': sent_message['id'],
                'thread_id': sent_message.get('threadId'),
                'label_ids': sent_message.get('labelIds', [])
            }
            
        except HttpError as error:
            return {
                'success': False,
                'error': str(error),
                'error_code': error.resp.status if hasattr(error, 'resp') else None
            }
        except Exception as error:
            return {
                'success': False,
                'error': str(error)
            }


# Global Gmail client instance
gmail_client = GmailClient()
