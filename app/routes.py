from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.urls import url_parse
from datetime import datetime
import uuid

from . import db
from .models import User, Event
from .forms import LoginForm, RegistrationForm, EventForm

# Define blueprints
main = Blueprint('main', __name__)
auth = Blueprint('auth', __name__, url_prefix='/auth')
events = Blueprint('events', __name__, url_prefix='/events')

# Main routes
@main.route('/')
@main.route('/home')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('main.calendar'))
    return render_template('home.html')

@main.route('/calendar')
@login_required
def calendar():
    return render_template('calendar.html', title='Team Calendar')

# Authentication routes
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.calendar'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password', 'danger')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.calendar')
        return redirect(next_page)
    
    return render_template('login.html', title='Sign In', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.calendar'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        # Generate a unique username based on email and UUID to ensure uniqueness
        # Username is not displayed to users but still required by the system
        email_prefix = form.email.data.split('@')[0]
        unique_id = str(uuid.uuid4())[:8]
        auto_username = f"{email_prefix}_{unique_id}"
        
        user = User(
            username=auto_username, 
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            color=User.generate_color()  # Assign a unique color to the user
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html', title='Register', form=form)

# Event routes
@events.route('/api/events')
@login_required
def get_events():
    events = Event.query.all()
    return jsonify([event.to_dict() for event in events])

@events.route('/new', methods=['GET', 'POST'])
@login_required
def new_event():
    form = EventForm()
    if form.validate_on_submit():
        event = Event(
            title=form.event_type.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            description=form.description.data,
            author=current_user
        )
        db.session.add(event)
        db.session.commit()
        flash('Your event has been created!', 'success')
        return redirect(url_for('main.calendar'))
    
    return render_template('event_form.html', title='New Event', form=form)

@events.route('/edit/<int:event_id>', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.author != current_user:
        flash('You can only edit your own events!', 'danger')
        return redirect(url_for('main.calendar'))
    
    form = EventForm()
    if form.validate_on_submit():
        event.title = form.event_type.data
        event.start_date = form.start_date.data
        event.end_date = form.end_date.data
        event.description = form.description.data
        db.session.commit()
        flash('Your event has been updated!', 'success')
        return redirect(url_for('main.calendar'))
    elif request.method == 'GET':
        form.event_type.data = event.title
        form.start_date.data = event.start_date
        form.end_date.data = event.end_date
        form.description.data = event.description
    
    return render_template('event_form.html', title='Edit Event', form=form)

@events.route('/delete/<int:event_id>', methods=['POST'])
@login_required
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.author != current_user:
        flash('You can only delete your own events!', 'danger')
        return redirect(url_for('main.calendar'))
    
    db.session.delete(event)
    db.session.commit()
    flash('Your event has been deleted!', 'success')
    return redirect(url_for('main.calendar'))