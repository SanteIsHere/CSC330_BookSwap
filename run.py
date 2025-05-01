# Import app initialization function from `app/__init__.py`
from app import create_app

# Initialize the Flask application
app = create_app()


if __name__ == "__main__":
    # Run the application in debug mode
    app.run(debug=True)
