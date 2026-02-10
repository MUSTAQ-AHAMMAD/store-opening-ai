import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

class WhatsAppService:
    """Service for WhatsApp integration using Twilio"""
    
    def __init__(self):
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.whatsapp_number = os.getenv('TWILIO_WHATSAPP_NUMBER', 'whatsapp:+14155238886')
        
        # Initialize Twilio client if credentials are available
        if self.account_sid and self.auth_token:
            self.client = Client(self.account_sid, self.auth_token)
        else:
            self.client = None
            print("Warning: Twilio credentials not configured. WhatsApp messaging will be simulated.")
    
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
            # Simulated mode
            print(f"[SIMULATED] WhatsApp message to {to_phone}: {message}")
            return {
                'success': True,
                'simulated': True,
                'message': 'Message simulated (Twilio not configured)'
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
