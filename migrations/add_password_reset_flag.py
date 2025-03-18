"""Migration script to add password_reset_required column to User model"""
import sys
import os

# Add the parent directory to sys.path so we can import the app package
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

# Import the create_app factory and db
from app import create_app, db
from sqlalchemy import text

def upgrade():
    # Create the app with the app factory
    app = create_app()
    
    # Add the new column to the User table
    with app.app_context():
        # Check if the column exists by running a query
        inspector = db.inspect(db.engine)
        columns = [c['name'] for c in inspector.get_columns('user')]
        
        if 'password_reset_required' not in columns:
            print('Adding password_reset_required column to User table...')
            # Use text() to create an executable SQL expression
            sql = text('ALTER TABLE user ADD COLUMN password_reset_required BOOLEAN DEFAULT FALSE')
            db.session.execute(sql)
            db.session.commit()
            print('Column added successfully.')
        else:
            print('Column already exists, skipping.')

if __name__ == '__main__':
    upgrade()
    print('Migration completed.')
