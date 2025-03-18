from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

# Create the application context
app = create_app()

# Function to create admin user
def create_admin_user():
    """Create the admin user if it doesn't already exist"""
    with app.app_context():
        # Check if admin already exists
        admin = User.query.filter_by(username='Admin').first()
        if admin:
            print('Admin user already exists!')
            return
        
        # Create new admin user
        admin = User(
            username='Admin',
            email='admin@example.com',  # Providing a valid email format
            password=generate_password_hash('password'),
            first_name='System',
            last_name='Administrator',
            is_admin=True  # Setting admin privileges
        )
        
        # Add to database
        db.session.add(admin)
        db.session.commit()
        print('Admin user created successfully!')
        print('Username: Admin')
        print('Password: password')

# Run the function if this script is executed directly
if __name__ == '__main__':
    create_admin_user()
