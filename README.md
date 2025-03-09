# Employee Info Flask Application

This is a simple Flask application to store and display employee information.

## Structure

- `main.py`: The main application file.
- `employee.db`: SQLite database file for storing employee information.
- `templates/index.html`: HTML file for rendering the employee form and employee list.
- `static/style.css`: CSS file for styling the application.

## Setup

1. Install the required packages:
   ```bash
   pip install Flask Flask-SQLAlchemy
   ```

2. Run the application:
   ```bash
   python main.py
   ```

3. Open your web browser and go to `http://127.0.0.1:5000/`.

## Usage

- Fill in the form to add a new employee.
- The added employee will be displayed in the list below the form.
```

This code creates a simple web application where you can input employee details (name, position, department) and view them in a list. The SQLite database (`employee.db`) will store this information.