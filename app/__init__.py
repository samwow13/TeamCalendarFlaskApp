from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from datetime import datetime
from .config import Config

# Initialize extensions before importing models
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app(config_class=Config):
    """Application factory function to create and configure the Flask app"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions with the app
    db.init_app(app)
    login_manager.init_app(app)
    
    # Register context processor for all templates
    @app.context_processor
    def inject_now():
        """Make the current datetime available to all templates"""
        return {'now': datetime.utcnow()}
    
    # Import and register blueprints
    from .routes import main, auth, events
    from .admin import admin
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(events)
    app.register_blueprint(admin)
    
    # Create database tables
    with app.app_context():
        db.create_all()
        
    return app

# Import models after initializing extensions
from . import models