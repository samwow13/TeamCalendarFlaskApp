from app import create_app, db

# Import the migration
from migrations.add_event_time_fields import upgrade

# Create the app and run the migration within app context
app = create_app()
with app.app_context():
    print("Starting migration to add event time fields...")
    upgrade()
    print("Migration completed successfully!")
