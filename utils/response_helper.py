def success_response(message, data=None):
    """Returns a standardized success response."""
    response = {
        "success": True,
        "message": message,
    }
    if data:
        response["data"] = data
    return response

def error_response(message, code=400):
    """Returns a standardized error response."""
    return {
        "success": False,
        "message": message,
        "code": code
    }
