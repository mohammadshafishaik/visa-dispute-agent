"""Alternative email service using SendGrid (more reliable than Gmail SMTP)"""
import os
from typing import Dict, Any

# SendGrid is optional - only import if available
try:
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import Mail, Email, To, Content
    SENDGRID_AVAILABLE = True
except ImportError:
    SENDGRID_AVAILABLE = False


class SendGridEmailService:
    """Send emails using SendGrid API (more reliable than SMTP)"""
    
    def __init__(self):
        self.api_key = os.getenv("SENDGRID_API_KEY", "")
        self.sender_email = os.getenv("SMTP_EMAIL", "noreply@dispute-system.com")
        self.enabled = SENDGRID_AVAILABLE and bool(self.api_key)
        
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
        """Send dispute decision email via SendGrid"""
        
        if not self.enabled:
            return {
                "success": False,
                "error": "SendGrid not configured or not available"
            }
        
        try:
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
            
            # Create SendGrid message
            message = Mail(
                from_email=Email(self.sender_email, "Dispute Resolution System"),
                to_emails=To(to_email),
                subject=f"Dispute Resolution - {dispute_id}",
                html_content=Content("text/html", html_body)
            )
            
            # Send email
            sg = SendGridAPIClient(self.api_key)
            response = sg.send(message)
            
            return {
                "success": True,
                "message": f"Email sent successfully to {to_email} via SendGrid",
                "status_code": response.status_code
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


# Global instance
sendgrid_service = SendGridEmailService()
