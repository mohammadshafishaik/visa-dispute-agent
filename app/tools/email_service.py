"""Real-time email service using Gmail SMTP"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any
import os


class EmailService:
    """Send real emails using Gmail SMTP"""
    
    def __init__(self):
        # Gmail SMTP settings from environment
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.sender_email = os.getenv("SMTP_EMAIL", "")
        self.sender_password = os.getenv("SMTP_PASSWORD", "")
        
    def send_dispute_decision(
        self,
        to_email: str,
        dispute_id: str,
        customer_name: str,
        decision: str,
        reasoning: str,
        amount: float,
        currency: str = "INR"
    ) -> Dict[str, Any]:
        """Send dispute decision email"""
        
        # Create email content
        email_content = f"""
To: {to_email}
Subject: Dispute Resolution - {dispute_id}

Dear {customer_name},

Your dispute has been processed:

Dispute ID: {dispute_id}
Decision: {decision.upper()}
Amount: {currency} {amount:,.2f}

Reasoning:
{reasoning}

Thank you for using our dispute resolution system.
"""
        
        if not self.sender_email or not self.sender_password or \
           self.sender_email == "your-email@gmail.com":
            # Log email instead of sending
            print("\n" + "="*60)
            print("📧 EMAIL NOTIFICATION (Not sent - SMTP not configured)")
            print("="*60)
            print(email_content)
            print("="*60)
            print("\nTo enable real emails, see EMAIL_SETUP_GUIDE.md")
            print("="*60 + "\n")
            
            return {
                "success": True,
                "message": f"Email logged (SMTP not configured). Would be sent to: {to_email}",
                "email_content": email_content
            }
        
        try:
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = f"Dispute Resolution - {dispute_id}"
            message["From"] = f"Dispute Resolution System <{self.sender_email}>"
            message["To"] = to_email
            
            # Create HTML email body
            html_body = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background: #1a1f36; color: white; padding: 20px; text-align: center; }}
                    .content {{ background: #f9f9f9; padding: 20px; border: 1px solid #ddd; }}
                    .detail {{ margin: 10px 0; padding: 10px; background: white; border-left: 3px solid #0066cc; }}
                    .footer {{ text-align: center; padding: 20px; color: #666; font-size: 12px; }}
                    .decision-box {{ padding: 15px; margin: 15px 0; border-radius: 5px; }}
                    .approved {{ background: #d4edda; border: 2px solid #28a745; color: #155724; }}
                    .rejected {{ background: #f8d7da; border: 2px solid #dc3545; color: #721c24; }}
                    .review {{ background: #fff3cd; border: 2px solid #ffc107; color: #856404; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>Dispute Resolution System</h1>
                        <p>Automated Decision Notification</p>
                    </div>
                    
                    <div class="content">
                        <p>Dear {customer_name},</p>
                        
                        <p>Your dispute has been processed. Please find the details below:</p>
                        
                        <div class="detail">
                            <strong>Dispute ID:</strong> {dispute_id}
                        </div>
                        
                        <div class="detail">
                            <strong>Amount:</strong> {currency} {amount:,.2f}
                        </div>
                        
                        <div class="decision-box {'approved' if decision.lower() == 'accept' else 'rejected' if decision.lower() == 'reject' else 'review'}">
                            <h3>Decision: {decision.upper()}</h3>
                            <p><strong>Reasoning:</strong></p>
                            <p>{reasoning}</p>
                        </div>
                        
                        <p>If you have any questions or concerns, please contact our support team.</p>
                        
                        <p>Thank you for using our dispute resolution system.</p>
                    </div>
                    
                    <div class="footer">
                        <p>This is an automated email. Please do not reply.</p>
                        <p>&copy; 2024 Dispute Resolution System. All rights reserved.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            # Attach HTML body
            html_part = MIMEText(html_body, "html")
            message.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)
            
            return {
                "success": True,
                "message": f"Email sent successfully to {to_email}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


# Global instance
email_service = EmailService()
