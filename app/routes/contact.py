from flask import Blueprint, request, jsonify, render_template

contact_bp = Blueprint('contact', __name__, url_prefix='/contact')

@contact_bp.route('/', methods=['GET'])
def contact_page():
    """Render the contact page."""
    return render_template('Contact/contact.html')

@contact_bp.route('/submit', methods=['POST'])
def submit_contact():
    """Handle contact form submission."""
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    # You can save this data to a database or send it as an email
    print(f"Name: {name}, Email: {email}, Message: {message}")

    return jsonify({"message": "Thank you for contacting us. We'll get back to you soon.", "success": True})
