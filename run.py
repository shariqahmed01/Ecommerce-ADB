import os
from app import create_app

# Get the environment from FLASK_ENV or default to "development"
env = os.getenv("FLASK_ENV", "development")
print(env)

# Create the Flask application
app = create_app(env)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000,debug=True)
