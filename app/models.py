from datetime import datetime, timedelta
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, login_manager
import random

@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login"""
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    """User model for authentication and event ownership"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    password_hash = db.Column(db.String(128))
    color = db.Column(db.String(20), nullable=False)  # Store the user's color
    is_admin = db.Column(db.Boolean, default=False)  # Admin flag
    events = db.relationship('Event', backref='author', lazy='dynamic')
    
    def set_password(self, password):
        """Set password hash"""
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        """Check password against stored hash"""
        return check_password_hash(self.password_hash, password)
    
    def get_full_name(self):
        """Return user's full name"""
        return f"{self.first_name} {self.last_name}"
    
    @staticmethod
    def generate_color():
        """Generate a random shade of blue for user events"""
        # Generate a blue shade with some variation
        # Format: hsl(hue, saturation%, lightness%)
        # Using HSL to keep it in blue family (hue ~210) with varying saturation and lightness
        hue = random.randint(200, 220)  # Keep in blue range
        saturation = random.randint(65, 90)  # High saturation for vibrant colors
        lightness = random.randint(40, 70)  # Medium lightness for visibility
        
        return f"hsl({hue}, {saturation}%, {lightness}%)"
    
    def __repr__(self):
        return f'<User {self.username}>'

class Event(db.Model):
    """Event model for calendar events"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Event {self.title}>'
        
    def to_dict(self):
        """Convert event to dictionary for JSON serialization"""
        # Store the original title for reference in the modal
        original_title = self.title
        
        # Create a compact display title with format: "Title - Name"
        display_title = f"{self.title} - {self.author.get_full_name()}"
        
        return {
            'id': self.id,
            'title': display_title,  # Use the compact display title for the calendar
            'original_title': original_title,  # Keep the original title for the modal
            'start': self.start_date.strftime('%Y-%m-%d'),
            'end': (self.end_date + timedelta(days=1)).strftime('%Y-%m-%d'),
            'description': self.description,
            'user_id': self.user_id,  # Use user_id instead of username for ownership checks
            'creator_name': self.author.get_full_name(),
            'backgroundColor': self.author.color,  # Add user's color to the event
            'borderColor': self.author.color,  # Match border color with background
            'is_admin': False  # This will be overridden in JavaScript for admin users
        }