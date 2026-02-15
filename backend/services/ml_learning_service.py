"""
Self-Learning Machine Learning Service
Continuously learns from historical data to improve predictions and recommendations
"""

import os
import json
import pickle
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import numpy as np
from pathlib import Path

logger = logging.getLogger(__name__)

class MLLearningService:
    """Self-learning ML service that improves over time"""
    
    def __init__(self):
        self.model_dir = Path('data/ml_models')
        self.model_dir.mkdir(parents=True, exist_ok=True)
        self.models = {}
        self.learning_enabled = True
        self.min_samples_for_training = 10
        
        # Load existing models
        self._load_models()
        
        logger.info("ML Learning Service initialized")
    
    def _load_models(self):
        """Load pre-trained models from disk"""
        try:
            model_files = {
                'completion_predictor': self.model_dir / 'completion_predictor.pkl',
                'risk_assessor': self.model_dir / 'risk_assessor.pkl',
                'task_duration': self.model_dir / 'task_duration.pkl',
                'success_factors': self.model_dir / 'success_factors.pkl'
            }
            
            for model_name, model_path in model_files.items():
                if model_path.exists():
                    with open(model_path, 'rb') as f:
                        self.models[model_name] = pickle.load(f)
                        logger.info(f"Loaded model: {model_name}")
                else:
                    self.models[model_name] = None
                    logger.info(f"Model not found: {model_name}, will train on first use")
        
        except Exception as e:
            logger.error(f"Error loading models: {e}")
    
    def _save_model(self, model_name: str, model_data: Dict):
        """Save trained model to disk"""
        try:
            model_path = self.model_dir / f'{model_name}.pkl'
            with open(model_path, 'wb') as f:
                pickle.dump(model_data, f)
            logger.info(f"Saved model: {model_name}")
        except Exception as e:
            logger.error(f"Error saving model {model_name}: {e}")
    
    def learn_from_completed_store(self, store_data: Dict, tasks_data: List[Dict]):
        """Learn from a completed store opening to improve future predictions"""
        try:
            # Extract features
            features = self._extract_store_features(store_data, tasks_data)
            
            # Update completion predictor
            self._update_completion_model(features)
            
            # Update risk assessor
            self._update_risk_model(features)
            
            # Update task duration predictor
            self._update_duration_model(tasks_data)
            
            # Analyze success factors
            self._analyze_success_factors(store_data, tasks_data)
            
            logger.info(f"Learned from completed store: {store_data.get('name')}")
            
            return {
                'success': True,
                'store_id': store_data.get('id'),
                'features_extracted': len(features),
                'models_updated': 4
            }
        
        except Exception as e:
            logger.error(f"Error learning from store: {e}")
            return {'success': False, 'error': str(e)}
    
    def _extract_store_features(self, store_data: Dict, tasks_data: List[Dict]) -> Dict:
        """Extract relevant features from store data"""
        total_tasks = len(tasks_data)
        completed_tasks = len([t for t in tasks_data if t.get('status') == 'completed'])
        overdue_tasks = len([t for t in tasks_data if t.get('is_overdue', False)])
        high_priority_tasks = len([t for t in tasks_data if t.get('priority') in ['high', 'critical']])
        
        # Calculate time metrics
        task_durations = []
        for task in tasks_data:
            if task.get('completed_at') and task.get('created_at'):
                duration = (task['completed_at'] - task['created_at']).total_seconds() / 86400  # days
                task_durations.append(duration)
        
        avg_task_duration = np.mean(task_durations) if task_durations else 0
        
        # Calculate team size
        team_members = set()
        for task in tasks_data:
            if task.get('assigned_to'):
                team_members.add(task['assigned_to'])
        
        return {
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'completion_rate': completed_tasks / total_tasks if total_tasks > 0 else 0,
            'overdue_tasks': overdue_tasks,
            'high_priority_tasks': high_priority_tasks,
            'avg_task_duration': avg_task_duration,
            'team_size': len(team_members),
            'was_successful': store_data.get('status') == 'completed',
            'opened_on_time': store_data.get('opened_on_time', False),
            'timestamp': datetime.utcnow()
        }
    
    def _update_completion_model(self, features: Dict):
        """Update the completion prediction model"""
        if self.models['completion_predictor'] is None:
            self.models['completion_predictor'] = {
                'training_data': [],
                'accuracy': 0.0,
                'last_trained': datetime.utcnow()
            }
        
        # Add new data point
        self.models['completion_predictor']['training_data'].append(features)
        
        # Retrain if enough samples
        if len(self.models['completion_predictor']['training_data']) >= self.min_samples_for_training:
            self._train_completion_model()
            self._save_model('completion_predictor', self.models['completion_predictor'])
    
    def _train_completion_model(self):
        """Train the completion prediction model using accumulated data"""
        data = self.models['completion_predictor']['training_data']
        
        # Simple linear regression for demonstration
        # In production, use sklearn or similar ML library
        
        completion_rates = [d['completion_rate'] for d in data]
        success_rates = [1 if d['was_successful'] else 0 for d in data]
        
        if len(set(success_rates)) > 1:  # Need both success and failure cases
            # Calculate correlation
            correlation = np.corrcoef(completion_rates, success_rates)[0, 1]
            
            self.models['completion_predictor']['weights'] = {
                'completion_rate_weight': correlation,
                'baseline_success_rate': np.mean(success_rates)
            }
            
            self.models['completion_predictor']['accuracy'] = abs(correlation)
            self.models['completion_predictor']['last_trained'] = datetime.utcnow()
            
            logger.info(f"Trained completion model - Accuracy: {abs(correlation):.2f}")
    
    def predict_completion_success(self, current_features: Dict) -> Dict:
        """Predict likelihood of successful completion based on current progress"""
        try:
            model = self.models['completion_predictor']
            
            if model is None or 'weights' not in model:
                # Default prediction
                return {
                    'success_probability': 0.75,
                    'confidence': 'low',
                    'message': 'Insufficient historical data for accurate prediction',
                    'model_trained': False
                }
            
            # Use trained model
            completion_rate = current_features.get('completion_rate', 0)
            weights = model['weights']
            
            # Calculate probability
            baseline = weights['baseline_success_rate']
            weight = weights['completion_rate_weight']
            
            probability = baseline + (weight * (completion_rate - 0.5))
            probability = max(0, min(1, probability))  # Clamp to [0, 1]
            
            # Determine confidence based on amount of training data
            training_samples = len(model['training_data'])
            if training_samples < 20:
                confidence = 'low'
            elif training_samples < 50:
                confidence = 'medium'
            else:
                confidence = 'high'
            
            return {
                'success_probability': round(probability, 3),
                'confidence': confidence,
                'model_accuracy': round(model['accuracy'], 3),
                'training_samples': training_samples,
                'message': f'Prediction based on {training_samples} completed stores',
                'model_trained': True,
                'last_trained': model['last_trained'].isoformat()
            }
        
        except Exception as e:
            logger.error(f"Error predicting completion success: {e}")
            return {
                'success_probability': 0.75,
                'confidence': 'low',
                'message': f'Error: {str(e)}',
                'model_trained': False
            }
    
    def _update_risk_model(self, features: Dict):
        """Update risk assessment model"""
        if self.models['risk_assessor'] is None:
            self.models['risk_assessor'] = {
                'risk_factors': [],
                'last_updated': datetime.utcnow()
            }
        
        # Analyze risk factors
        risk_score = 0
        if features['completion_rate'] < 0.5:
            risk_score += 2
        if features['overdue_tasks'] > 5:
            risk_score += 3
        if not features['was_successful']:
            risk_score += 5
        
        self.models['risk_assessor']['risk_factors'].append({
            'features': features,
            'risk_score': risk_score,
            'timestamp': datetime.utcnow()
        })
        
        self._save_model('risk_assessor', self.models['risk_assessor'])
    
    def assess_current_risk(self, current_features: Dict) -> Dict:
        """Assess risk level for current store opening"""
        try:
            model = self.models['risk_assessor']
            
            if model is None or len(model.get('risk_factors', [])) < self.min_samples_for_training:
                # Default risk assessment
                return self._default_risk_assessment(current_features)
            
            # Calculate risk based on historical patterns
            risk_score = 0
            risk_factors = []
            
            # Completion rate risk
            if current_features.get('completion_rate', 0) < 0.5:
                risk_score += 2
                risk_factors.append('Low completion rate (<50%)')
            
            # Overdue tasks risk
            overdue = current_features.get('overdue_tasks', 0)
            if overdue > 5:
                risk_score += 3
                risk_factors.append(f'{overdue} overdue tasks')
            
            # Team capacity risk
            team_size = current_features.get('team_size', 0)
            total_tasks = current_features.get('total_tasks', 0)
            if team_size > 0 and total_tasks / team_size > 10:
                risk_score += 1
                risk_factors.append('High task-to-team ratio')
            
            # Determine risk level
            if risk_score >= 5:
                risk_level = 'high'
            elif risk_score >= 3:
                risk_level = 'medium'
            else:
                risk_level = 'low'
            
            return {
                'risk_level': risk_level,
                'risk_score': risk_score,
                'risk_factors': risk_factors,
                'recommendations': self._generate_risk_recommendations(risk_level, risk_factors),
                'historical_patterns': len(model['risk_factors'])
            }
        
        except Exception as e:
            logger.error(f"Error assessing risk: {e}")
            return self._default_risk_assessment(current_features)
    
    def _default_risk_assessment(self, features: Dict) -> Dict:
        """Default risk assessment when insufficient data"""
        completion_rate = features.get('completion_rate', 0)
        
        if completion_rate > 0.7:
            risk_level = 'low'
        elif completion_rate > 0.4:
            risk_level = 'medium'
        else:
            risk_level = 'high'
        
        return {
            'risk_level': risk_level,
            'risk_score': 0,
            'risk_factors': [],
            'recommendations': ['Continue monitoring progress regularly'],
            'historical_patterns': 0
        }
    
    def _generate_risk_recommendations(self, risk_level: str, risk_factors: List[str]) -> List[str]:
        """Generate actionable recommendations based on risk level"""
        recommendations = []
        
        if risk_level == 'high':
            recommendations.append('🚨 Immediate action required')
            recommendations.append('Schedule emergency team meeting')
            recommendations.append('Consider reallocating resources')
        
        if 'overdue' in ' '.join(risk_factors).lower():
            recommendations.append('Prioritize overdue tasks immediately')
            recommendations.append('Provide additional support to team members')
        
        if 'completion rate' in ' '.join(risk_factors).lower():
            recommendations.append('Analyze blockers preventing task completion')
            recommendations.append('Consider extending deadline if feasible')
        
        if not recommendations:
            recommendations.append('Continue current pace and monitor closely')
        
        return recommendations
    
    def _update_duration_model(self, tasks_data: List[Dict]):
        """Update task duration prediction model"""
        if self.models['task_duration'] is None:
            self.models['task_duration'] = {
                'task_types': {},
                'last_updated': datetime.utcnow()
            }
        
        for task in tasks_data:
            if task.get('completed_at') and task.get('created_at'):
                duration = (task['completed_at'] - task['created_at']).total_seconds() / 86400
                task_type = task.get('title', 'unknown').split()[0].lower()  # First word as type
                
                if task_type not in self.models['task_duration']['task_types']:
                    self.models['task_duration']['task_types'][task_type] = []
                
                self.models['task_duration']['task_types'][task_type].append(duration)
        
        self._save_model('task_duration', self.models['task_duration'])
    
    def predict_task_duration(self, task_title: str, task_priority: str) -> Dict:
        """Predict expected duration for a task"""
        try:
            model = self.models['task_duration']
            
            if model is None:
                return {'expected_days': 3, 'confidence': 'low', 'based_on_samples': 0}
            
            task_type = task_title.split()[0].lower() if task_title else 'unknown'
            
            if task_type in model['task_types'] and model['task_types'][task_type]:
                durations = model['task_types'][task_type]
                avg_duration = np.mean(durations)
                std_duration = np.std(durations)
                
                # Adjust for priority
                priority_multipliers = {
                    'critical': 0.7,  # Critical tasks often get done faster
                    'high': 0.85,
                    'medium': 1.0,
                    'low': 1.3
                }
                
                multiplier = priority_multipliers.get(task_priority, 1.0)
                expected = avg_duration * multiplier
                
                return {
                    'expected_days': round(expected, 1),
                    'confidence': 'high' if len(durations) > 10 else 'medium',
                    'based_on_samples': len(durations),
                    'range': {
                        'min': round(max(1, avg_duration - std_duration), 1),
                        'max': round(avg_duration + std_duration, 1)
                    }
                }
            
            # Default prediction
            return {'expected_days': 3, 'confidence': 'low', 'based_on_samples': 0}
        
        except Exception as e:
            logger.error(f"Error predicting task duration: {e}")
            return {'expected_days': 3, 'confidence': 'low', 'based_on_samples': 0}
    
    def _analyze_success_factors(self, store_data: Dict, tasks_data: List[Dict]):
        """Analyze what factors contribute to successful store openings"""
        if self.models['success_factors'] is None:
            self.models['success_factors'] = {
                'factors': [],
                'patterns': {},
                'last_analyzed': datetime.utcnow()
            }
        
        was_successful = store_data.get('status') == 'completed' and store_data.get('opened_on_time', False)
        
        features = self._extract_store_features(store_data, tasks_data)
        
        self.models['success_factors']['factors'].append({
            'success': was_successful,
            'features': features,
            'timestamp': datetime.utcnow()
        })
        
        # Analyze patterns every 10 new data points
        if len(self.models['success_factors']['factors']) % 10 == 0:
            self._identify_success_patterns()
        
        self._save_model('success_factors', self.models['success_factors'])
    
    def _identify_success_patterns(self):
        """Identify patterns that correlate with success"""
        data = self.models['success_factors']['factors']
        
        if len(data) < 10:
            return
        
        successful = [d for d in data if d['success']]
        unsuccessful = [d for d in data if not d['success']]
        
        if not successful or not unsuccessful:
            return
        
        # Compare averages
        patterns = {}
        
        if successful:
            patterns['successful_stores'] = {
                'avg_completion_rate': np.mean([d['features']['completion_rate'] for d in successful]),
                'avg_team_size': np.mean([d['features']['team_size'] for d in successful]),
                'avg_task_duration': np.mean([d['features']['avg_task_duration'] for d in successful])
            }
        
        if unsuccessful:
            patterns['unsuccessful_stores'] = {
                'avg_completion_rate': np.mean([d['features']['completion_rate'] for d in unsuccessful]),
                'avg_team_size': np.mean([d['features']['team_size'] for d in unsuccessful]),
                'avg_task_duration': np.mean([d['features']['avg_task_duration'] for d in unsuccessful])
            }
        
        self.models['success_factors']['patterns'] = patterns
        logger.info("Updated success patterns based on historical data")
    
    def get_success_insights(self) -> Dict:
        """Get insights about what makes store openings successful"""
        try:
            model = self.models['success_factors']
            
            if model is None or not model.get('patterns'):
                return {
                    'insights': ['Insufficient data for pattern analysis'],
                    'data_points': 0
                }
            
            patterns = model['patterns']
            insights = []
            
            if 'successful_stores' in patterns and 'unsuccessful_stores' in patterns:
                success = patterns['successful_stores']
                failure = patterns['unsuccessful_stores']
                
                # Completion rate insight
                comp_diff = success['avg_completion_rate'] - failure['avg_completion_rate']
                if abs(comp_diff) > 0.1:
                    insights.append(
                        f"✅ Successful stores maintain {success['avg_completion_rate']:.1%} completion rate "
                        f"vs {failure['avg_completion_rate']:.1%} for delayed stores"
                    )
                
                # Team size insight
                team_diff = success['avg_team_size'] - failure['avg_team_size']
                if abs(team_diff) > 1:
                    insights.append(
                        f"👥 Optimal team size appears to be around {success['avg_team_size']:.0f} members"
                    )
                
                # Task duration insight
                duration_diff = success['avg_task_duration'] - failure['avg_task_duration']
                if abs(duration_diff) > 0.5:
                    insights.append(
                        f"⏱️ Successful stores complete tasks in {success['avg_task_duration']:.1f} days on average"
                    )
            
            return {
                'insights': insights if insights else ['Patterns are being analyzed'],
                'data_points': len(model['factors']),
                'last_analyzed': model['last_analyzed'].isoformat()
            }
        
        except Exception as e:
            logger.error(f"Error getting success insights: {e}")
            return {
                'insights': ['Error analyzing patterns'],
                'data_points': 0
            }
    
    def get_model_stats(self) -> Dict:
        """Get statistics about all trained models"""
        stats = {}
        
        for model_name, model in self.models.items():
            if model is None:
                stats[model_name] = {
                    'trained': False,
                    'data_points': 0
                }
            else:
                if model_name == 'completion_predictor':
                    stats[model_name] = {
                        'trained': 'weights' in model,
                        'data_points': len(model.get('training_data', [])),
                        'accuracy': model.get('accuracy', 0)
                    }
                elif model_name == 'risk_assessor':
                    stats[model_name] = {
                        'trained': True,
                        'data_points': len(model.get('risk_factors', []))
                    }
                elif model_name == 'task_duration':
                    task_types = len(model.get('task_types', {}))
                    total_samples = sum(len(v) for v in model.get('task_types', {}).values())
                    stats[model_name] = {
                        'trained': task_types > 0,
                        'task_types': task_types,
                        'total_samples': total_samples
                    }
                elif model_name == 'success_factors':
                    stats[model_name] = {
                        'trained': True,
                        'data_points': len(model.get('factors', [])),
                        'patterns_identified': len(model.get('patterns', {})) > 0
                    }
        
        return stats


# Global ML service instance
ml_service = None

def get_ml_service():
    """Get or create ML learning service instance"""
    global ml_service
    if ml_service is None:
        ml_service = MLLearningService()
    return ml_service
