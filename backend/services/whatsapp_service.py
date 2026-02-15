import os
import logging
from datetime import datetime
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

class WhatsAppService:
    """Service for WhatsApp integration using Twilio"""
    
    def __init__(self):
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.whatsapp_number = os.getenv('TWILIO_WHATSAPP_NUMBER', 'whatsapp:+14155238886')
        self.test_mode = os.getenv('TEST_MODE', 'false').lower() == 'true'
        
        # Initialize Twilio client if credentials are available and not in test mode
        if self.account_sid and self.auth_token and not self.test_mode:
            self.client = Client(self.account_sid, self.auth_token)
            logger.info("WhatsApp service initialized with Twilio")
        else:
            self.client = None
            if self.test_mode:
                logger.info("WhatsApp service in TEST MODE - messages will be logged only")
            else:
                logger.warning("Twilio credentials not configured. WhatsApp messaging will be simulated.")
    
    def send_message(self, to_phone, message):
        """Send a WhatsApp message to a phone number"""
        if not to_phone.startswith('whatsapp:'):
            to_phone = f'whatsapp:{to_phone}'
        
        if self.client:
            try:
                message = self.client.messages.create(
                    from_=self.whatsapp_number,
                    body=message,
                    to=to_phone
                )
                return {
                    'success': True,
                    'message_sid': message.sid,
                    'status': message.status
                }
            except Exception as e:
                return {
                    'success': False,
                    'error': str(e)
                }
        else:
            # Test/Simulated mode
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log_msg = f"[TEST MODE] WhatsApp to {to_phone} at {timestamp}"
            logger.info(log_msg)
            logger.info(f"Message: {message[:100]}..." if len(message) > 100 else f"Message: {message}")
            print(f"\n{'='*60}")
            print(f"📱 WhatsApp Message (Test Mode)")
            print(f"{'='*60}")
            print(f"To: {to_phone}")
            print(f"Time: {timestamp}")
            print(f"Message:\n{message}")
            print(f"{'='*60}\n")
            return {
                'success': True,
                'simulated': True,
                'test_mode': self.test_mode,
                'message': 'Message logged successfully (Test Mode)',
                'timestamp': timestamp
            }
    
    def send_message_to_group(self, group, message, team_members):
        """Send a message to all team members in a group"""
        sent_to = 0
        failed = 0
        results = []
        
        for member in team_members:
            if member.is_active and member.phone:
                result = self.send_message(member.phone, message)
                if result.get('success'):
                    sent_to += 1
                else:
                    failed += 1
                results.append({
                    'member': member.name,
                    'phone': member.phone,
                    'result': result
                })
        
        return {
            'sent_to': sent_to,
            'failed': failed,
            'results': results
        }
    
    def send_follow_up(self, task, team_member):
        """Send a follow-up message for a task"""
        message = f"""
🔔 Task Reminder

Task: {task.title}
Priority: {task.priority.upper()}
Due Date: {task.due_date.strftime('%Y-%m-%d %H:%M') if task.due_date else 'Not set'}
Status: {task.status}

{task.description if task.description else ''}

Please update the status once completed.
        """.strip()
        
        return self.send_message(team_member.phone, message)
    
    def send_escalation(self, task, team_member, escalation_level):
        """Send an escalation message for an overdue task"""
        urgency = ['⚠️ Reminder', '🚨 URGENT', '🔴 CRITICAL'][min(escalation_level, 2)]
        
        message = f"""
{urgency} - Overdue Task

Task: {task.title}
Priority: {task.priority.upper()}
Due Date: {task.due_date.strftime('%Y-%m-%d %H:%M') if task.due_date else 'Not set'}
Status: {task.status}

This task is overdue. Please complete it as soon as possible or update the status.

{task.description if task.description else ''}
        """.strip()
        
        return self.send_message(team_member.phone, message)
