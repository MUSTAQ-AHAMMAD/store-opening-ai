from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///store_opening.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
CORS(app)

# Import models
from backend.models.models import Store, TeamMember, Checklist, Task, WhatsAppGroup, ArchivedConversation, FollowUp

# Import routes
from backend.routes import store_routes, team_routes, checklist_routes, whatsapp_routes, analytics_routes

# Register blueprints
app.register_blueprint(store_routes.bp)
app.register_blueprint(team_routes.bp)
app.register_blueprint(checklist_routes.bp)
app.register_blueprint(whatsapp_routes.bp)
app.register_blueprint(analytics_routes.bp)

# Import and initialize scheduler
from backend.services.scheduler import init_scheduler

# Create tables
with app.app_context():
    db.create_all()
    print("Database tables created successfully!")

# Initialize scheduler
scheduler = init_scheduler(app)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'true').lower() == 'true'
    
    try:
        app.run(host='0.0.0.0', port=port, debug=debug)
    except (KeyboardInterrupt, SystemExit):
        if scheduler:
            scheduler.stop()
        print("\nApplication stopped")
