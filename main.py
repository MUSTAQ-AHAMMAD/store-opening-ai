"""
Store Opening AI Management System
Entry point - delegates to app.py
"""

from app import app, initialize_db
import os

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
