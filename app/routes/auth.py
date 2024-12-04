from flask import Blueprint, request, render_template, redirect, url_for, flash, jsonify, session

from app.models.admin import Admin
from app.models.customer import Customer
from services.auth_service import register_user, login_user
import bcrypt

from utils.bcrypt_helper import check_password

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')



@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Input validation
        if not username or not email or not password or not confirm_password:
            flash("All fields are required.", "danger")
            return render_template('auth/register.html')

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return render_template('auth/register.html')

        # Check if email already exists
        if Customer.get_customer_by_email(email):
            flash("Email is already registered.", "danger")
            return render_template('auth/register.html')

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Save the customer
        Customer.create_customer({
            "username": username,
            "email": email,
            "password": hashed_password
        })

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_data = {
            "email": request.form.get('username', '').strip(),
            "password": request.form.get('password', '').strip()
        }

        # Input validation
        if len(login_data['email']) > 50 or len(login_data['password']) > 50:
            flash("Input exceeds maximum length.", "danger")
            return render_template('auth/login.html')

        # Check if the login is for admin
        admin = Admin.get_admin_by_username(login_data['email'])
        if admin and login_data['password']=="admin":
            # Admin login
            session['admin_id'] = str(admin['_id'])
            session['is_admin'] = True
            flash("Welcome, Admin!", "success")
            return redirect(url_for('admin.dashboard'))

        # Attempt customer login
        response = login_user(login_data)
        if response["success"]:
            # Store customer data in session
            customer = Customer.get_customer_by_email(login_data['email'])
            session['customer_id'] = str(customer['_id'])
            session['customer_name'] = customer['username']
            session['customer_email'] = customer['email']
            session['is_admin'] = False

            flash(response["message"], "success")
            return redirect(url_for('home.index'))
        else:
            flash(response["message"], "danger")

    return render_template('auth/login.html')


@auth_bp.route('/logout', methods=['GET'])
def logout():
    """Log out the user and clear the session."""
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for('auth.login'))
