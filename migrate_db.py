import sqlite3
import os

# Path to the database file
db_path = os.path.join('instance', 'app.db')

def add_admin_column():
    """Add is_admin column to the user table if it doesn't exist"""
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if the column already exists
    cursor.execute("PRAGMA table_info(user)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if 'is_admin' not in columns:
        print("Adding 'is_admin' column to user table...")
        cursor.execute("ALTER TABLE user ADD COLUMN is_admin BOOLEAN DEFAULT 0")
        conn.commit()
        print("Column added successfully!")
    else:
        print("Column 'is_admin' already exists.")
    
    # Close connection
    conn.close()

def create_admin_user():
    """Create or update admin user"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if admin user exists
    cursor.execute("SELECT id FROM user WHERE username = 'Admin'")
    admin = cursor.fetchone()
    
    if admin:
        # Update existing admin user
        print("Updating existing Admin user...")
        cursor.execute(
            "UPDATE user SET is_admin = 1, email = 'admin@example.com' WHERE username = 'Admin'"
        )
    else:
        # Create new admin user with password 'password'
        # Generate a simple hash for the password (in production, use better hashing)
        from werkzeug.security import generate_password_hash
        password_hash = generate_password_hash('password')
        
        print("Creating new Admin user...")
        cursor.execute(
            "INSERT INTO user (username, email, password_hash, first_name, last_name, is_admin) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            ('Admin', 'admin@example.com', password_hash, 'System', 'Administrator', 1)
        )
    
    conn.commit()
    print("Admin user configured successfully!")
    print("Username: Admin")
    print("Password: password")
    conn.close()

if __name__ == '__main__':
    print(f"Database path: {os.path.abspath(db_path)}")
    add_admin_column()
    create_admin_user()
