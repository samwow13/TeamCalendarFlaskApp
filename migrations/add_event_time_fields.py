from datetime import datetime
from app import db
from app.models import Event
from sqlalchemy import text

def upgrade():
    """Add start_time and end_time fields to Event model"""
    # SQLite doesn't support ADD COLUMN with DEFAULT in a single statement,
    # so we'll alter the table directly through SQLAlchemy
    
    # Check if columns already exist to avoid errors
    with db.engine.connect() as conn:
        # Get table information
        result = conn.execute(text("PRAGMA table_info(event)"))
        columns = [row[1] for row in result]
        
        # Add start_time column if it doesn't exist
        if 'start_time' not in columns:
            conn.execute(text("ALTER TABLE event ADD COLUMN start_time VARCHAR(10)"))
        
        # Add end_time column if it doesn't exist
        if 'end_time' not in columns:
            conn.execute(text("ALTER TABLE event ADD COLUMN end_time VARCHAR(10)"))
    
    print("✅ Added start_time and end_time columns to Event table")

def downgrade():
    """This is a database migration downgrade function"""
    # SQLite doesn't support dropping columns, so in a real app we'd need a more complex
    # approach like creating a new table without these columns and copying data
    print("⚠️ SQLite doesn't support dropping columns. Manual intervention required for downgrade.")
