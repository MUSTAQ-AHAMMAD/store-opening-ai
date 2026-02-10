"""
Store Opening AI Management System
Main Flask application
"""

import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from backend.database import db

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///store_opening.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
CORS(app)

# Import models (must be before routes)
from backend.models import models

# Register blueprints/routes
from backend.routes import (
    store_routes, team_routes, checklist_routes, 
    whatsapp_routes, analytics_routes, auth_routes,
    voice_routes, ai_routes, workflow_routes
)

app.register_blueprint(store_routes.bp)
app.register_blueprint(team_routes.bp)
app.register_blueprint(checklist_routes.bp)
app.register_blueprint(whatsapp_routes.bp)
app.register_blueprint(analytics_routes.bp)
app.register_blueprint(auth_routes.bp)
app.register_blueprint(voice_routes.bp)
app.register_blueprint(ai_routes.bp)
app.register_blueprint(workflow_routes.bp)

# Root route
@app.route('/')
def index():
    return {
        'message': 'Store Opening AI API',
        'version': '1.0.0',
        'endpoints': {
            'stores': '/api/stores',
            'team': '/api/team',
            'checklists': '/api/checklists',
            'whatsapp': '/api/whatsapp',
            'analytics': '/api/analytics'
        }
    }

@app.route('/health')
def health():
    return {'status': 'healthy'}

def initialize_db():
    """Initialize database tables and seed default users"""
    with app.app_context():
        db.create_all()
        print("Database tables created successfully")
        
        # Auto-seed default demo users (admin, manager, team_member) if no users exist
        from backend.models.models import User
        if User.query.count() == 0:
            from data.seed_users import seed_admin_user
            seed_admin_user(use_existing_context=True)

if __name__ == '__main__':
    # Initialize database
    initialize_db()
    
    # Run the app
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'true').lower() == 'true'
    
    print(f"\n{'='*50}")
    print(f"Store Opening AI - Backend Server")
    print(f"{'='*50}")
    print(f"Server running on: http://localhost:{port}")
    print(f"Debug mode: {debug}")
    print(f"Database: {app.config['SQLALCHEMY_DATABASE_URI']}")
    print(f"{'='*50}\n")
    
    app.run(host='0.0.0.0', port=port, debug=debug)