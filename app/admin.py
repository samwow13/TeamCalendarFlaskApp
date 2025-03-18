from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from werkzeug.security import generate_password_hash
from . import db
from .models import User, Event

# Define admin blueprint
admin = Blueprint('admin', __name__, url_prefix='/admin')

# Admin decorator
def admin_required(f):
    """Decorator to require admin privileges"""
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You need administrator privileges to access this page.', 'danger')
            return redirect(url_for('main.home'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

# Admin routes
@admin.route('/dashboard')
@login_required
@admin_required
def admin_dashboard():
    """Admin dashboard"""
    users = User.query.all()
    events = Event.query.all()
    return render_template('admin/dashboard.html', users=users, events=events)

# User management
@admin.route('/users')
@login_required
@admin_required
def list_users():
    """List all users"""
    users = User.query.all()
    return render_template('admin/users.html', users=users)

# Create new admin user
@admin.route('/users/create_admin', methods=['POST'])
@login_required
@admin_required
def create_admin():
    """Create a new admin user"""
    if request.method == 'POST':
        # Get form data
        username = request.form.get('username')
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validate form data
        if not username or not email or not first_name or not last_name or not password:
            flash('All fields are required.', 'danger')
            return redirect(url_for('admin.list_users'))
        
        # Check if passwords match
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('admin.list_users'))
        
        # Check if username already exists
        existing_username = User.query.filter_by(username=username).first()
        if existing_username:
            flash('Username already exists.', 'danger')
            return redirect(url_for('admin.list_users'))
        
        # Check if email already exists
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash('Email already exists.', 'danger')
            return redirect(url_for('admin.list_users'))
        
        # Create new admin user
        new_admin = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password_hash=generate_password_hash(password),
            color=User.generate_color(),
            is_admin=True  # Set admin privileges
        )
        
        # Add to database
        db.session.add(new_admin)
        db.session.commit()
        
        flash(f'New administrator {first_name} {last_name} created successfully!', 'success')
        return redirect(url_for('admin.list_users'))
    
    return redirect(url_for('admin.list_users'))

# Create new regular user
@admin.route('/users/create_user', methods=['POST'])
@login_required
@admin_required
def create_user():
    """Create a new regular user"""
    if request.method == 'POST':
        # Get form data
        username = request.form.get('username')
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validate form data
        if not username or not email or not first_name or not last_name or not password:
            flash('All fields are required.', 'danger')
            return redirect(url_for('admin.list_users'))
        
        # Check if passwords match
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('admin.list_users'))
        
        # Check if username already exists
        existing_username = User.query.filter_by(username=username).first()
        if existing_username:
            flash('Username already exists.', 'danger')
            return redirect(url_for('admin.list_users'))
        
        # Check if email already exists
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash('Email already exists.', 'danger')
            return redirect(url_for('admin.list_users'))
        
        # Create new regular user
        new_user = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password_hash=generate_password_hash(password),
            color=User.generate_color(),
            is_admin=False  # Not an admin
        )
        
        # Add to database
        db.session.add(new_user)
        db.session.commit()
        
        flash(f'New user {first_name} {last_name} created successfully!', 'success')
        return redirect(url_for('admin.list_users'))
    
    return redirect(url_for('admin.list_users'))

@admin.route('/users/delete/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    """Delete a user and all their events"""
    user = User.query.get_or_404(user_id)
    
    # Don't allow admin to delete themselves
    if user.id == current_user.id:
        flash('You cannot delete your own account.', 'danger')
        return redirect(url_for('admin.list_users'))
    
    # Delete all events by this user
    Event.query.filter_by(user_id=user.id).delete()
    
    # Delete the user
    db.session.delete(user)
    db.session.commit()
    
    flash(f'User {user.get_full_name()} has been deleted.', 'success')
    return redirect(url_for('admin.list_users'))

# Password reset functionality
@admin.route('/users/reset_password/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def reset_user_password(user_id):
    """Reset a user's password and flag for mandatory password change on next login"""
    user = User.query.get_or_404(user_id)
    
    # Don't allow admin to reset their own password this way
    if user.id == current_user.id:
        flash('You cannot reset your own password using this feature.', 'danger')
        return redirect(url_for('admin.list_users'))
    
    # Generate a temporary password
    temp_password = 'TemporaryPassword123'  # Simple temporary password
    
    # Update user record
    user.password_hash = generate_password_hash(temp_password)
    user.password_reset_required = True  # Flag for mandatory password change
    db.session.commit()
    
    flash(f'Password for {user.get_full_name()} has been reset. They will be required to set a new password on next login.', 'success')
    return redirect(url_for('admin.list_users'))

# Event management
@admin.route('/events')
@login_required
@admin_required
def list_events():
    """List all events"""
    events = Event.query.all()
    return render_template('admin/events.html', events=events)

@admin.route('/events/delete/<int:event_id>', methods=['POST'])
@login_required
@admin_required
def delete_event(event_id):
    """Delete an event"""
    event = Event.query.get_or_404(event_id)
    
    # Get the event creator's name before deleting
    event_creator = event.author.get_full_name()
    event_title = event.title
    
    db.session.delete(event)
    db.session.commit()
    
    flash(f'Event "{event_title}" by {event_creator} has been deleted.', 'success')
    return redirect(url_for('admin.list_events'))
