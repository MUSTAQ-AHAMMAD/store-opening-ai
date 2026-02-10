"""
AI Service for Intelligent Follow-ups and Predictions
Using OpenAI GPT for smart task management and follow-up recommendations
"""

import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import openai
import logging

# Configure logging
logger = logging.getLogger(__name__)

class AIService:
    """AI service for intelligent task management"""
    
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        if self.api_key:
            openai.api_key = self.api_key
        self.enabled = bool(self.api_key)
    
    def generate_follow_up_message(self, task: Dict, team_member: Dict, context: Dict) -> str:
        """Generate intelligent follow-up message based on task context"""
        if not self.enabled:
            return self._default_follow_up_message(task, team_member)
        
        try:
            days_overdue = context.get('days_overdue', 0)
            priority = task.get('priority', 'medium')
            
            prompt = f"""Generate a professional and empathetic follow-up message for a team member about an overdue task.

Task Details:
- Title: {task.get('title')}
- Priority: {priority}
- Days Overdue: {days_overdue}
- Team Member: {team_member.get('name')}
- Role: {team_member.get('role')}

Context:
- Store Opening Date: {context.get('store_opening_date')}
- Days Until Opening: {context.get('days_until_opening')}
- Overall Progress: {context.get('completion_percentage', 0)}%

Generate a concise, professional message (max 150 words) that:
1. Acknowledges the task is overdue
2. Emphasizes the importance based on priority and opening timeline
3. Offers support if needed
4. Requests a status update

Keep the tone professional but supportive."""

            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant for store opening management."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            logger.error(f"AI service error: {e}")
            return self._default_follow_up_message(task, team_member)
    
    def _default_follow_up_message(self, task: Dict, team_member: Dict) -> str:
        """Default follow-up message when AI is not available"""
        return f"""Hello {team_member.get('name')},

This is a reminder about the following task:

Task: {task.get('title')}
Priority: {task.get('priority', 'medium').upper()}
Status: Overdue

Please provide an update on the progress of this task. If you need any assistance, let us know.

Thank you!"""
    
    def predict_task_risk(self, task: Dict, similar_tasks: List[Dict]) -> Dict:
        """Predict risk level for task completion based on historical data"""
        if not self.enabled or not similar_tasks:
            return self._default_risk_assessment(task)
        
        try:
            # Analyze similar tasks
            completed_on_time = sum(1 for t in similar_tasks if t.get('completed_on_time', False))
            total_similar = len(similar_tasks)
            avg_completion_days = sum(t.get('completion_days', 0) for t in similar_tasks) / total_similar if total_similar > 0 else 0
            
            prompt = f"""Analyze the risk of task completion based on historical data.

Current Task:
- Title: {task.get('title')}
- Priority: {task.get('priority')}
- Due Date: {task.get('due_date')}
- Assigned To: {task.get('assigned_to_name')}

Historical Data from {total_similar} similar tasks:
- Completed on time: {completed_on_time}/{total_similar} ({completed_on_time/total_similar*100 if total_similar > 0 else 0:.1f}%)
- Average completion time: {avg_completion_days:.1f} days

Provide a risk assessment (low/medium/high) and a brief explanation (max 100 words)."""

            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a data analyst specializing in project risk assessment."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.5
            )
            
            ai_response = response.choices[0].message.content.strip()
            
            # Parse risk level
            risk_level = 'medium'
            if 'high risk' in ai_response.lower():
                risk_level = 'high'
            elif 'low risk' in ai_response.lower():
                risk_level = 'low'
            
            return {
                'risk_level': risk_level,
                'explanation': ai_response,
                'success_rate': completed_on_time / total_similar if total_similar > 0 else 0
            }
        
        except Exception as e:
            logger.error(f"AI risk prediction error: {e}")
            return self._default_risk_assessment(task)
    
    def _default_risk_assessment(self, task: Dict) -> Dict:
        """Default risk assessment when AI is not available"""
        priority = task.get('priority', 'medium')
        
        risk_mapping = {
            'critical': 'high',
            'high': 'medium',
            'medium': 'low',
            'low': 'low'
        }
        
        return {
            'risk_level': risk_mapping.get(priority, 'medium'),
            'explanation': f"Risk level based on task priority: {priority}",
            'success_rate': 0.75
        }
    
    def suggest_task_prioritization(self, tasks: List[Dict], store_context: Dict) -> List[Dict]:
        """Suggest optimal task prioritization using AI"""
        if not self.enabled or not tasks:
            return tasks
        
        try:
            days_until_opening = store_context.get('days_until_opening', 30)
            
            # Create task summary
            task_summary = "\n".join([
                f"- {t.get('title')} (Priority: {t.get('priority')}, Due: {t.get('due_date')}, Status: {t.get('status')})"
                for t in tasks[:10]  # Limit to first 10 tasks
            ])
            
            prompt = f"""You are a project manager. Given these tasks for a store opening in {days_until_opening} days, suggest the optimal order to prioritize them.

Tasks:
{task_summary}

Provide a prioritized list with brief reasoning for the top 5 tasks that should be focused on first. Consider:
1. Time sensitivity
2. Dependencies
3. Critical path items
4. Current status

Format: Task Title - Reasoning (one line each)"""

            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert project manager for retail store openings."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            suggestions = response.choices[0].message.content.strip()
            
            # Add AI suggestions to tasks
            for task in tasks:
                task['ai_suggestions'] = suggestions
            
            return tasks
        
        except Exception as e:
            logger.error(f"AI prioritization error: {e}")
            return tasks
    
    def generate_escalation_message(self, task: Dict, recipient: Dict, escalation_level: int, context: Dict) -> str:
        """Generate escalation message for managers"""
        if not self.enabled:
            return self._default_escalation_message(task, recipient, escalation_level, context)
        
        try:
            recipient_role = recipient.get('role', 'Manager')
            assignee_name = context.get('assignee_name', 'Unknown')
            days_overdue = context.get('days_overdue', 0)
            
            prompt = f"""Generate an escalation message for a {recipient_role} about an overdue task.

Task Details:
- Title: {task.get('title')}
- Priority: {task.get('priority')}
- Days Overdue: {days_overdue}
- Assigned To: {assignee_name}
- Escalation Level: {escalation_level}

Store Context:
- Days Until Opening: {context.get('days_until_opening')}
- Overall Progress: {context.get('completion_percentage', 0)}%

Generate a professional escalation message (max 150 words) that:
1. States the urgency clearly
2. Provides task context
3. Requests immediate action
4. Maintains professional tone

Level {escalation_level} means {"critical urgency" if escalation_level >= 2 else "high priority"}."""

            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an AI assistant helping manage critical project escalations."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.6
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            logger.error(f"AI escalation message error: {e}")
            return self._default_escalation_message(task, recipient, escalation_level, context)
    
    def _default_escalation_message(self, task: Dict, recipient: Dict, escalation_level: int, context: Dict) -> str:
        """Default escalation message"""
        urgency = "CRITICAL" if escalation_level >= 2 else "URGENT"
        
        return f"""[{urgency}] Task Escalation

Dear {recipient.get('name')},

This is a level {escalation_level} escalation for an overdue task:

Task: {task.get('title')}
Priority: {task.get('priority', 'unknown').upper()}
Days Overdue: {context.get('days_overdue', 0)}
Assigned To: {context.get('assignee_name', 'Unknown')}

Store Opening: {context.get('days_until_opening', 'N/A')} days remaining

Immediate attention required.

Please contact the team member and ensure task completion ASAP.

Thank you."""

# Global AI service instance
ai_service = None

def get_ai_service():
    """Get or create AI service instance"""
    global ai_service
    if ai_service is None:
        ai_service = AIService()
    return ai_service
