from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session, flash
from app.models.customer import Customer

profile_bp = Blueprint('profile', __name__, url_prefix='/profile')

@profile_bp.route('/', methods=['GET'])
def view_profile():
    """Display the user profile."""
    customer_id = session.get('customer_id')
    if not customer_id:
        flash("Please log in to access your profile.", "danger")
        return redirect(url_for('auth.login'))

    customer = Customer.get_customer_by_id(customer_id)
    if not customer:
        flash("Customer not found.", "danger")
        return redirect(url_for('home.index'))

    return render_template('profile/profile.html', customer=customer)

@profile_bp.route('/edit', methods=['POST'])
def edit_profile():
    """Edit the user profile."""
    customer_id = session.get('customer_id')
    if not customer_id:
        return jsonify({"message": "Unauthorized access.", "success": False}), 401

    # Get customer details
    customer = Customer.get_customer_by_id(customer_id)
    if not customer:
        return jsonify({"message": "Customer not found.", "success": False}), 404

    # Get updated data
    updated_data = {
        "name": request.form.get('name'),
        "email": request.form.get('email'),
        "address": request.form.get('address'),
        "contact": request.form.get('contact')
    }

    # Validate email uniqueness (if changed)
    if updated_data['email'] != customer['email']:
        existing_customer = Customer.get_customer_by_email(updated_data['email'])
        if existing_customer:
            flash("Email is already in use.", "danger")
            return redirect(url_for('profile.view_profile'))

    # Update customer details
    Customer.update_customer_by_id(customer_id, updated_data)
    flash("Profile updated successfully.", "success")
    return redirect(url_for('profile.view_profile'))
