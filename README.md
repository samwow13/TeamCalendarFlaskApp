# Team Calendar - Out of Office Tracker

A Flask web application for teams to track out-of-office time and coordinate schedules.

## Features

- User registration and authentication
- Create, edit, and delete out-of-office events
- Calendar view to see team availability
- Responsive design

## Installation

1. Clone the repository:
   ```
   git clone https://your-repository-url.git
   cd team-calendar
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Configure environment variables (optional):
   Create a `.env` file in the root directory with the following variables:
   ```
   SECRET_KEY=your-secret-key
   DATABASE_URL=sqlite:///app.db
   ```

5. Run the application:
   ```
   python run.py
   ```

6. Access the application at http://localhost:5000

## Project Structure

- `app/` - Main application package
  - `__init__.py` - Application factory
  - `config.py` - Configuration settings
  - `models.py` - Database models
  - `routes.py` - Route handlers
  - `forms.py` - Form definitions
  - `static/` - Static assets (CSS, JS)
  - `templates/` - HTML templates
- `run.py` - Application entry point
- `requirements.txt` - Dependencies

## Development

To run the application in development mode:

```
python run.py
```

This will start the development server with debugging enabled.