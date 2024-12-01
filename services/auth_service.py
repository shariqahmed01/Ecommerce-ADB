from app.models.customer import Customer
from utils.bcrypt_helper import hash_password, check_password
from utils.jwt_helper import generate_token

def register_user(user_data):
    """Register a new user."""
    existing_user = Customer.get_customer_by_email(user_data['email'])
    if existing_user:
        return {"message": "Email already registered.", "success": False}

    user_data['password'] = hash_password(user_data['password'])
    Customer.create_customer(user_data)
    return {"message": "Registration successful.", "success": True}

def login_user(login_data):
    """Log in an existing user."""
    email = login_data.get("email", "")
    password = login_data.get("password", "")
    print(f"Email: {email}, Password: {password}")

    user = Customer.get_customer_by_email(email)
    if not user:
        print("User not found")
        return {"message": "Invalid email or password.", "success": False}

    print(f"User password from DB: {user['password']}")
    if not check_password(password, user['password']):
        print("Password mismatch")
        return {"message": "Invalid email or password.", "success": False}

    token = generate_token(user['_id'])
    return {"message": "Login successful.", "success": True, "token": token}
