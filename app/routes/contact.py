from flask import Blueprint, request, jsonify, render_template, flash, redirect, url_for

contact_bp = Blueprint('contact', __name__, url_prefix='/contact')


@contact_bp.route('/', methods=['GET'])
def contact_page():
    """Render the contact page."""
    return render_template('contact/contact.html')


@contact_bp.route('/submit', methods=['POST'])
def submit_contact():
    """Handle contact form submission."""
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    # Log the data (or save it to a database/send an email)
    print(f"Name: {name}, Email: {email}, Message: {message}")

    # Flash a success message
    flash("Thank you for contacting us. We'll get back to you soon.", "success")

    # Redirect back to the contact page
    return redirect(url_for('contact.contact_page'))
