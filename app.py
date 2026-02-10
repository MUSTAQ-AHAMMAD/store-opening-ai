from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
cors = CORS()

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///store_opening.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions with app
    db.init_app(app)
    cors.init_app(app)
    
    with app.app_context():
        # Import parts
        from backend import models
        
        # Create tables
        db.create_all()
        print("Database tables created successfully!")
        
        # Import and register blueprints
        from backend.routes.store_routes import bp as store_bp
        from backend.routes.team_routes import bp as team_bp
        from backend.routes.checklist_routes import bp as checklist_bp
        from backend.routes.whatsapp_routes import bp as whatsapp_bp
        from backend.routes.analytics_routes import bp as analytics_bp
        
        app.register_blueprint(store_bp)
        app.register_blueprint(team_bp)
        app.register_blueprint(checklist_bp)
        app.register_blueprint(whatsapp_bp)
        app.register_blueprint(analytics_bp)
    
    return app

if __name__ == '__main__':
    app = create_app()
    
    # Initialize scheduler
    from backend.services.scheduler import init_scheduler
    scheduler = init_scheduler(app)
    
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'true').lower() == 'true'
    
    try:
        app.run(host='0.0.0.0', port=port, debug=debug)
    except (KeyboardInterrupt, SystemExit):
        if scheduler:
            scheduler.stop()
        print("\nApplication stopped")
