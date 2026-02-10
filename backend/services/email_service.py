"""
Email Service for Store Opening Notifications
Sends emails for store creation, stage transitions, and escalations
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class EmailService:
    """Service for sending email notifications"""
    
    def __init__(self):
        self.smtp_host = os.getenv('SMTP_HOST', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.smtp_user = os.getenv('SMTP_USER')
        self.smtp_password = os.getenv('SMTP_PASSWORD')
        self.from_email = os.getenv('FROM_EMAIL', self.smtp_user)
        self.enabled = bool(self.smtp_user and self.smtp_password)
        
        if not self.enabled:
            logger.warning("Email service not configured. Email notifications will be simulated.")
    
    def send_email(self, to_emails: List[str], subject: str, body: str, html_body: Optional[str] = None) -> Dict:
        """Send an email"""
        if not self.enabled:
            logger.info(f"[SIMULATED] Email to {to_emails}: {subject}")
            return {'success': True, 'simulated': True}
        
        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = self.from_email
            msg['To'] = ', '.join(to_emails)
            msg['Subject'] = subject
            
            # Add text version
            text_part = MIMEText(body, 'plain')
            msg.attach(text_part)
            
            # Add HTML version if provided
            if html_body:
                html_part = MIMEText(html_body, 'html')
                msg.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            
            logger.info(f"Email sent successfully to {to_emails}")
            return {'success': True}
            
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return {'success': False, 'error': str(e)}
    
    def send_store_creation_email(self, store_data: Dict, team_members: List[Dict]) -> Dict:
        """Send email notification when a new store is created"""
        subject = f"🏪 New Store Opening - {store_data['name']}"
        
        team_list = '\n'.join([f"- {m['name']} ({m['role']}) - {m['email']}" for m in team_members if m.get('email')])
        
        body = f"""
New Store Opening Notification

Store Details:
- Name: {store_data['name']}
- Location: {store_data['location']}
- Opening Date: {store_data['opening_date']}
- Status: {store_data['status']}

Team Members:
{team_list}

A WhatsApp group has been created for this store opening project.

The 7-stage workflow process has been initiated:
1. Update nearby store details
2. Complete checklist & send to warehouse
3. Confirm material reached nearby store
4. Confirm material sent to actual store
5. Start installation & update TeamViewer ID
6. Complete final checklist on opening day
7. Store opening complete

Please ensure all stages are completed on time.

Best regards,
Store Opening AI System
        """.strip()
        
        html_body = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 5px; }}
                .content {{ padding: 20px; }}
                .store-info {{ background: #f5f5f5; padding: 15px; border-radius: 5px; margin: 15px 0; }}
                .stage {{ padding: 10px; margin: 5px 0; background: #e8f4f8; border-left: 3px solid #667eea; }}
                .footer {{ margin-top: 20px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🏪 New Store Opening</h1>
            </div>
            <div class="content">
                <h2>{store_data['name']}</h2>
                
                <div class="store-info">
                    <p><strong>Location:</strong> {store_data['location']}</p>
                    <p><strong>Opening Date:</strong> {store_data['opening_date']}</p>
                    <p><strong>Status:</strong> {store_data['status']}</p>
                </div>
                
                <h3>Team Members</h3>
                <ul>
                    {''.join([f"<li>{m['name']} ({m['role']}) - {m['email']}</li>" for m in team_members if m.get('email')])}
                </ul>
                
                <h3>Workflow Process (7 Stages)</h3>
                <div class="stage">1. Update nearby store details</div>
                <div class="stage">2. Complete checklist & send to warehouse</div>
                <div class="stage">3. Confirm material reached nearby store</div>
                <div class="stage">4. Confirm material sent to actual store</div>
                <div class="stage">5. Start installation & update TeamViewer ID</div>
                <div class="stage">6. Complete final checklist on opening day</div>
                <div class="stage">7. Store opening complete</div>
                
                <p style="margin-top: 20px;">
                    A WhatsApp group has been created for this project. All updates will be shared there.
                </p>
            </div>
            <div class="footer">
                <p>This is an automated message from Store Opening AI System</p>
            </div>
        </body>
        </html>
        """
        
        emails = [m['email'] for m in team_members if m.get('email')]
        if not emails:
            return {'success': False, 'error': 'No email addresses found'}
        
        return self.send_email(emails, subject, body, html_body)
    
    def send_stage_transition_email(self, store_data: Dict, stage_data: Dict, team_emails: List[str]) -> Dict:
        """Send email when a workflow stage transitions"""
        subject = f"Stage {stage_data['stage_number']} Update - {store_data['name']}"
        
        status_icon = '✅' if stage_data['status'] == 'completed' else '🚀'
        
        body = f"""
Workflow Stage Update

Store: {store_data['name']}
{status_icon} Stage {stage_data['stage_number']}: {stage_data['stage_name']}
Status: {stage_data['status']}

{stage_data.get('notes', '')}

Opening Date: {store_data['opening_date']}

Please check the WhatsApp group for more details.

Best regards,
Store Opening AI System
        """.strip()
        
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 5px;">
                <h2>{status_icon} Stage Update</h2>
            </div>
            <div style="padding: 20px;">
                <h3>{store_data['name']}</h3>
                <p><strong>Stage {stage_data['stage_number']}:</strong> {stage_data['stage_name']}</p>
                <p><strong>Status:</strong> {stage_data['status']}</p>
                {f"<p><strong>Notes:</strong> {stage_data.get('notes', '')}</p>" if stage_data.get('notes') else ''}
                <p><strong>Opening Date:</strong> {store_data['opening_date']}</p>
            </div>
        </body>
        </html>
        """
        
        if not team_emails:
            return {'success': False, 'error': 'No email addresses provided'}
        
        return self.send_email(team_emails, subject, body, html_body)
    
    def send_escalation_email(self, manager_email: str, store_data: Dict, stage_data: Dict, days_overdue: int) -> Dict:
        """Send escalation email to manager"""
        subject = f"🔴 URGENT: Stage Delay - {store_data['name']}"
        
        body = f"""
URGENT ESCALATION

Store: {store_data['name']}
Location: {store_data['location']}
Opening Date: {store_data['opening_date']}

Delayed Stage:
Stage {stage_data['stage_number']}: {stage_data['stage_name']}
Days Overdue: {days_overdue}
Status: {stage_data['status']}

This stage is significantly overdue and requires immediate attention.
Please contact the assigned team member and ensure completion ASAP.

Store Opening Risk: {'HIGH' if days_overdue > 3 else 'MEDIUM'}

Best regards,
Store Opening AI System
        """.strip()
        
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="background: #dc3545; color: white; padding: 20px; border-radius: 5px;">
                <h2>🔴 URGENT ESCALATION</h2>
            </div>
            <div style="padding: 20px;">
                <h3>{store_data['name']}</h3>
                <p><strong>Location:</strong> {store_data['location']}</p>
                <p><strong>Opening Date:</strong> {store_data['opening_date']}</p>
                
                <div style="background: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0;">
                    <h4 style="margin-top: 0;">Delayed Stage</h4>
                    <p><strong>Stage {stage_data['stage_number']}:</strong> {stage_data['stage_name']}</p>
                    <p><strong>Days Overdue:</strong> <span style="color: #dc3545; font-size: 18px; font-weight: bold;">{days_overdue}</span></p>
                    <p><strong>Status:</strong> {stage_data['status']}</p>
                </div>
                
                <p style="color: #dc3545; font-weight: bold;">
                    Store Opening Risk: {'HIGH' if days_overdue > 3 else 'MEDIUM'}
                </p>
                
                <p>This stage requires immediate attention. Please contact the assigned team member and ensure completion ASAP.</p>
            </div>
        </body>
        </html>
        """
        
        return self.send_email([manager_email], subject, body, html_body)
    
    def send_opening_date_change_email(self, store_data: Dict, old_date: str, new_date: str, team_emails: List[str]) -> Dict:
        """Send email when opening date is changed"""
        subject = f"⚠️ Opening Date Changed - {store_data['name']}"
        
        body = f"""
Opening Date Update

Store: {store_data['name']}

Previous Opening Date: {old_date}
New Opening Date: {new_date}

All workflow stage timelines have been automatically recalculated.

Please review the updated deadlines in the system and plan accordingly.

Best regards,
Store Opening AI System
        """.strip()
        
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="background: #ff9800; color: white; padding: 20px; border-radius: 5px;">
                <h2>⚠️ Opening Date Changed</h2>
            </div>
            <div style="padding: 20px;">
                <h3>{store_data['name']}</h3>
                <div style="background: #f5f5f5; padding: 15px; border-radius: 5px; margin: 15px 0;">
                    <p><strong>Previous Opening Date:</strong> <s>{old_date}</s></p>
                    <p><strong>New Opening Date:</strong> <span style="color: #ff9800; font-weight: bold;">{new_date}</span></p>
                </div>
                <p><strong>⚠️ All workflow stage timelines have been automatically recalculated.</strong></p>
                <p>Please review the updated deadlines in the system and plan accordingly.</p>
            </div>
        </body>
        </html>
        """
        
        if not team_emails:
            return {'success': False, 'error': 'No email addresses provided'}
        
        return self.send_email(team_emails, subject, body, html_body)


# Global email service instance
email_service = None

def get_email_service():
    """Get or create email service instance"""
    global email_service
    if email_service is None:
        email_service = EmailService()
    return email_service
