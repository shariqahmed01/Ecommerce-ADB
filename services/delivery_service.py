from app.models.delivery import Delivery

def track_delivery(tracking_number):
    """Track delivery status."""
    delivery = Delivery.get_delivery_by_tracking(tracking_number)
    if not delivery:
        return {"message": "Delivery not found.", "success": False}
    return {"success": True, "delivery": delivery}
