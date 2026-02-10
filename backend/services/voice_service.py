"""
Voice Calling Service for AI-powered Escalations
Uses Twilio Voice API for automated calling
"""

import os
from typing import Dict, Optional
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Say, Gather
from datetime import datetime
from backend.database import db

class VoiceCallingService:
    """Service for making automated voice calls for escalations"""
    
    def __init__(self):
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.phone_number = os.getenv('TWILIO_PHONE_NUMBER')
        
        if self.account_sid and self.auth_token:
            self.client = Client(self.account_sid, self.auth_token)
            self.enabled = True
        else:
            self.client = None
            self.enabled = False
    
    def make_escalation_call(
        self, 
        recipient_phone: str, 
        recipient_name: str,
        task_title: str, 
        escalation_level: int,
        store_name: str,
        days_overdue: int,
        callback_url: Optional[str] = None
    ) -> Dict:
        """
        Make an automated voice call for task escalation
        
        Args:
            recipient_phone: Phone number to call
            recipient_name: Name of recipient
            task_title: Title of the overdue task
            escalation_level: Escalation level (0-2)
            store_name: Name of the store
            days_overdue: Number of days the task is overdue
            callback_url: URL for handling call responses
        
        Returns:
            Dict with call status and details
        """
        if not self.enabled:
            return {
                'success': False,
                'error': 'Twilio voice service not configured',
                'call_sid': None
            }
        
        try:
            # Generate TwiML for the call
            twiml = self._generate_escalation_twiml(
                recipient_name,
                task_title,
                escalation_level,
                store_name,
                days_overdue
            )
            
            # Make the call
            call = self.client.calls.create(
                to=recipient_phone,
                from_=self.phone_number,
                twiml=twiml,
                status_callback=callback_url if callback_url else None,
                status_callback_event=['completed', 'answered', 'busy', 'no-answer']
            )
            
            return {
                'success': True,
                'call_sid': call.sid,
                'status': call.status,
                'recipient': recipient_phone,
                'timestamp': datetime.utcnow().isoformat()
            }
        
        except Exception as e:
            print(f"Error making escalation call: {e}")
            return {
                'success': False,
                'error': str(e),
                'call_sid': None
            }
    
    def _generate_escalation_twiml(
        self,
        recipient_name: str,
        task_title: str,
        escalation_level: int,
        store_name: str,
        days_overdue: int
    ) -> str:
        """Generate TwiML script for escalation call"""
        response = VoiceResponse()
        
        # Greeting
        greeting = f"Hello {recipient_name}. This is an automated call from the Store Opening AI Management System."
        response.say(greeting, voice='alice', language='en-US')
        
        # Pause
        response.pause(length=1)
        
        # Urgency message based on escalation level
        if escalation_level >= 2:
            urgency = "This is a CRITICAL escalation."
        elif escalation_level == 1:
            urgency = "This is an URGENT escalation."
        else:
            urgency = "This is an important reminder."
        
        response.say(urgency, voice='alice', language='en-US')
        response.pause(length=1)
        
        # Task details
        task_message = f"A task for {store_name} is now {days_overdue} days overdue. "
        task_message += f"The task is: {task_title}. "
        response.say(task_message, voice='alice', language='en-US')
        
        response.pause(length=1)
        
        # Action required
        if escalation_level >= 2:
            action = "Immediate action is required. Please contact your team immediately to resolve this issue."
        else:
            action = "Please review this task and take appropriate action as soon as possible."
        
        response.say(action, voice='alice', language='en-US')
        
        response.pause(length=1)
        
        # Gather response
        gather = Gather(
            num_digits=1,
            action='/api/voice/acknowledgment',
            method='POST',
            timeout=10
        )
        gather.say(
            "Press 1 to acknowledge this escalation, or press 2 to speak with support.",
            voice='alice',
            language='en-US'
        )
        response.append(gather)
        
        # If no response
        response.say(
            "We did not receive your response. Please check your dashboard for details. Goodbye.",
            voice='alice',
            language='en-US'
        )
        
        return str(response)
    
    def make_manager_escalation_call(
        self,
        manager_phone: str,
        manager_name: str,
        team_member_name: str,
        task_title: str,
        store_name: str,
        days_overdue: int
    ) -> Dict:
        """
        Make an escalation call to a manager about a team member's overdue task
        
        Args:
            manager_phone: Manager's phone number
            manager_name: Manager's name
            team_member_name: Name of team member who missed deadline
            task_title: Title of the overdue task
            store_name: Name of the store
            days_overdue: Number of days overdue
        
        Returns:
            Dict with call status
        """
        if not self.enabled:
            return {
                'success': False,
                'error': 'Twilio voice service not configured'
            }
        
        try:
            # Generate manager escalation TwiML
            twiml = self._generate_manager_escalation_twiml(
                manager_name,
                team_member_name,
                task_title,
                store_name,
                days_overdue
            )
            
            call = self.client.calls.create(
                to=manager_phone,
                from_=self.phone_number,
                twiml=twiml
            )
            
            return {
                'success': True,
                'call_sid': call.sid,
                'status': call.status,
                'recipient': manager_phone
            }
        
        except Exception as e:
            print(f"Error making manager escalation call: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _generate_manager_escalation_twiml(
        self,
        manager_name: str,
        team_member_name: str,
        task_title: str,
        store_name: str,
        days_overdue: int
    ) -> str:
        """Generate TwiML for manager escalation"""
        response = VoiceResponse()
        
        # Greeting
        greeting = f"Hello {manager_name}. This is an urgent call from the Store Opening AI Management System."
        response.say(greeting, voice='alice', language='en-US')
        response.pause(length=1)
        
        # Escalation notice
        response.say(
            "This is a manager escalation regarding a critical overdue task.",
            voice='alice',
            language='en-US'
        )
        response.pause(length=1)
        
        # Details
        details = f"Team member {team_member_name} has a task that is {days_overdue} days overdue. "
        details += f"Store: {store_name}. Task: {task_title}. "
        response.say(details, voice='alice', language='en-US')
        
        response.pause(length=1)
        
        # Action required
        response.say(
            "As the manager, please contact the team member immediately and ensure this task is completed today.",
            voice='alice',
            language='en-US'
        )
        
        response.pause(length=1)
        
        # Gather response
        gather = Gather(
            num_digits=1,
            action='/api/voice/manager-acknowledgment',
            method='POST',
            timeout=10
        )
        gather.say(
            "Press 1 to acknowledge this escalation.",
            voice='alice',
            language='en-US'
        )
        response.append(gather)
        
        # Closing
        response.say("Thank you. Please log in to the dashboard for full details.", voice='alice', language='en-US')
        
        return str(response)
    
    def get_call_status(self, call_sid: str) -> Dict:
        """Get the status of a call"""
        if not self.enabled:
            return {'error': 'Service not enabled'}
        
        try:
            call = self.client.calls(call_sid).fetch()
            return {
                'sid': call.sid,
                'status': call.status,
                'duration': call.duration,
                'start_time': call.start_time,
                'end_time': call.end_time,
                'direction': call.direction
            }
        except Exception as e:
            return {'error': str(e)}
    
    def send_follow_up_sms(self, phone: str, message: str) -> Dict:
        """Send an SMS follow-up (fallback when calls fail)"""
        if not self.enabled:
            return {'success': False, 'error': 'Service not enabled'}
        
        try:
            sms = self.client.messages.create(
                body=message,
                from_=self.phone_number,
                to=phone
            )
            
            return {
                'success': True,
                'sid': sms.sid,
                'status': sms.status
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

# Global voice calling service instance
voice_service = None

def get_voice_service():
    """Get or create voice calling service instance"""
    global voice_service
    if voice_service is None:
        voice_service = VoiceCallingService()
    return voice_service
