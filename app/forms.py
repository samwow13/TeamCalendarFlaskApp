from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from wtforms.fields import DateField, TimeField
from .models import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=64)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
            
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already registered. Please use a different one.')

class PasswordResetForm(FlaskForm):
    """Form for resetting password after admin-triggered reset"""
    password = PasswordField('New Password', validators=[DataRequired(), Length(min=8, max=64)])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Set New Password')

class EventForm(FlaskForm):
    event_type = SelectField('Event Type', choices=[
        ('OOO', 'Out of Office (OOO)'),
        ('VA', 'Vacation (VA)'),
        ('SL', 'Sick Leave (SL)'),
        ('PT', 'Personal Time (PT)')
    ], default='OOO')
    start_date = DateField('Start Date', validators=[DataRequired()], format='%Y-%m-%d')
    start_time = TimeField('Start Time', format='%H:%M')
    end_date = DateField('End Date', validators=[DataRequired()], format='%Y-%m-%d')
    end_time = TimeField('End Time', format='%H:%M')
    description = TextAreaField('Description (Optional)', render_kw={'placeholder': 'Enter additional details (optional)'})
    submit = SubmitField('Save Event')
    
    def validate_end_date(self, end_date):
        if self.start_date.data and end_date.data < self.start_date.data:
            raise ValidationError('End date must be after start date.')