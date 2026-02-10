# app.py

from flask import Flask

app = Flask(__name__)

def initialize_db():
    # db initialization logic goes here
    pass

if __name__ == '__main__':
    with app.app_context():
        initialize_db()  # Making sure that DB is initialized before importing routes
        from routes import *  # Import routes after DB initialization

app.run()