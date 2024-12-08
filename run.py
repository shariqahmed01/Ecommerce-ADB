import os
from datetime import datetime

from app import create_app

# Get the environment from FLASK_ENV or default to "development"
env = os.getenv("FLASK_ENV", "development")
print(env)

# Create the Flask application
app = create_app(env)

# Register a custom filter for formatting dates
@app.template_filter('datetimeformat')
def datetimeformat(value):
    if isinstance(value, datetime):
        return value.strftime('%Y-%m-%d %H:%M:%S')
    return value

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000,debug=True)
