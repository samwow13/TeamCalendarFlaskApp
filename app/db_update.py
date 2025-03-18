from app import db, create_app
from app.models import User
import sqlalchemy as sa
from sqlalchemy.exc import OperationalError


def update_user_table():
    """Add first_name, last_name, and color columns to the user table if they don't exist"""
    app = create_app()
    with app.app_context():
        # Check if columns already exist
        inspector = sa.inspect(db.engine)
        columns = [column['name'] for column in inspector.get_columns('user')]
        
        # Add first_name column if it doesn't exist
        if 'first_name' not in columns:
            try:
                db.session.execute(sa.text('ALTER TABLE user ADD COLUMN first_name VARCHAR(64)'))
                print("Added first_name column to user table")
            except OperationalError as e:
                print(f"Error adding first_name column: {e}")
        
        # Add last_name column if it doesn't exist
        if 'last_name' not in columns:
            try:
                db.session.execute(sa.text('ALTER TABLE user ADD COLUMN last_name VARCHAR(64)'))
                print("Added last_name column to user table")
            except OperationalError as e:
                print(f"Error adding last_name column: {e}")
        
        # Add color column if it doesn't exist
        if 'color' not in columns:
            try:
                db.session.execute(sa.text('ALTER TABLE user ADD COLUMN color VARCHAR(20)'))
                print("Added color column to user table")
            except OperationalError as e:
                print(f"Error adding color column: {e}")
        
        # Set default values for existing users
        try:
            users = User.query.all()
            for user in users:
                if not hasattr(user, 'first_name') or not user.first_name:
                    user.first_name = user.username
                if not hasattr(user, 'last_name') or not user.last_name:
                    user.last_name = ''
                # Assign a color to each user if they don't have one
                if not hasattr(user, 'color') or not user.color:
                    user.color = User.generate_color()
            db.session.commit()
            print("Updated existing users with default first and last names, and assigned colors")
        except Exception as e:
            print(f"Error updating existing users: {e}")
            db.session.rollback()


if __name__ == '__main__':
    update_user_table()
