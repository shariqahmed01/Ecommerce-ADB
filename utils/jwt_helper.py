import jwt
import datetime
from flask import current_app

def generate_token(user_id):
    user_id_str = str(user_id)
    if len(user_id_str) < 22:  # Ensure valid length for slicing
        raise ValueError("User ID length is too short for token generation.")
    return user_id_str[:22]  # Adjust slice range


def decode_token(token):
    """Decodes a JWT token."""
    try:
        payload = jwt.decode(token, current_app.config['JWT_SECRET'], algorithms=['HS256'])
        return {"user_id": payload["user_id"], "success": True}
    except jwt.ExpiredSignatureError:
        return {"message": "Token expired.", "success": False}
    except jwt.InvalidTokenError:
        return {"message": "Invalid token.", "success": False}
