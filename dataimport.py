from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client.online_clothing_store_dev

# Insert test data into collections
def insert_test_data():
    # Admin Collection
    db.Admin.insert_one({
        "_id": ObjectId("648d0d5c8f8b9b9f9f8b9b90"),
        "name": "Admin User",
        "username": "admin",
        "password": "$2b$12$hashedpassword12345",  # Replace with bcrypt hashed password
        "email": "admin@store.com"
    })

    # Customer Collection
    db.Customer.insert_one({
        "_id": ObjectId("648d0d5c8f8b9b9f9f8b9b91"),
        "name": "John Doe",
        "email": "john@example.com",
        "address": "123 Main St, Springfield",
        "contact": "1234567890",
        "username": "johndoe",
        "password": "$2b$12$hashedpassword12345",  # Replace with bcrypt hashed password
        "cart": [
            {
                "productId": ObjectId("648d0d5c8f8b9b9f9f8b9b92"),
                "quantity": 1
            }
        ]
    })

    # Category Collection
    db.Category.insert_many([
        {"_id": ObjectId("648d0d5c8f8b9b9f9f8b9b93"), "name": "Women"},
        {"_id": ObjectId("648d0d5c8f8b9b9f9f8b9b94"), "name": "Men"},
        {"_id": ObjectId("648d0d5c8f8b9b9f9f8b9b95"), "name": "Kids"}
    ])

    # Subcategory Collection
    db.Subcategory.insert_many([
        {
            "_id": ObjectId("648d0d5c8f8b9b9f9f8b9b96"),
            "categoryId": ObjectId("648d0d5c8f8b9b9f9f8b9b93"),
            "name": "Dresses"
        },
        {
            "_id": ObjectId("648d0d5c8f8b9b9f9f8b9b97"),
            "categoryId": ObjectId("648d0d5c8f8b9b9f9f8b9b94"),
            "name": "Shirts"
        }
    ])

    # Product Collection
    db.Product.insert_many([
        {
            "_id": ObjectId("648d0d5c8f8b9b9f9f8b9b92"),
            "subcategoryId": ObjectId("648d0d5c8f8b9b9f9f8b9b96"),
            "name": "Floral Dress",
            "description": "A beautiful floral dress perfect for summer.",
            "price": 49.99,
            "material": "Cotton",
            "imageUrls": ["https://example.com/images/floral-dress.jpg"],
            "isTrending": True,
            "createdAt": datetime.datetime.utcnow(),
            "updatedAt": datetime.datetime.utcnow()
        },
        {
            "_id": ObjectId("648d0d5c8f8b9b9f9f8b9b98"),
            "subcategoryId": ObjectId("648d0d5c8f8b9b9f9f8b9b97"),
            "name": "Casual Shirt",
            "description": "A classic casual shirt for everyday wear.",
            "price": 29.99,
            "material": "Polyester",
            "imageUrls": ["https://example.com/images/casual-shirt.jpg"],
            "isTrending": False,
            "createdAt": datetime.datetime.utcnow(),
            "updatedAt": datetime.datetime.utcnow()
        }
    ])

    # ProductVariant Collection
    db.ProductVariant.insert_many([
        {
            "_id": ObjectId("648d0d5c8f8b9b9f9f8b9b99"),
            "productId": ObjectId("648d0d5c8f8b9b9f9f8b9b92"),
            "size": "M",
            "color": "Blue",
            "stockQuantity": 20,
            "price": 49.99
        },
        {
            "_id": ObjectId("648d0d5c8f8b9b9f9f8b9b9a"),
            "productId": ObjectId("648d0d5c8f8b9b9f9f8b9b92"),
            "size": "L",
            "color": "Blue",
            "stockQuantity": 10,
            "price": 49.99
        }
    ])

    # Order Collection
    db.Order.insert_one({
        "_id": ObjectId("648d0d5c8f8b9b9f9f8b9b9b"),
        "customerId": ObjectId("648d0d5c8f8b9b9f9f8b9b91"),
        "orderDate": datetime.datetime.utcnow(),
        "items": [
            {
                "productId": ObjectId("648d0d5c8f8b9b9f9f8b9b92"),
                "variantId": ObjectId("648d0d5c8f8b9b9f9f8b9b99"),
                "quantity": 2,
                "price": 49.99
            }
        ],
        "totalAmount": 99.98,
        "status": "pending"
    })

    # Delivery Collection
    db.Delivery.insert_one({
        "_id": ObjectId("648d0d5c8f8b9b9f9f8b9b9c"),
        "orderId": ObjectId("648d0d5c8f8b9b9f9f8b9b9b"),
        "deliveryAddress": "123 Main St, Springfield",
        "deliveryDate": datetime.datetime(2024, 12, 1),
        "trackingNumber": "TRACK123",
        "status": "in transit"
    })

    # Payment Collection
    db.Payment.insert_one({
        "_id": ObjectId("648d0d5c8f8b9b9f9f8b9b9d"),
        "orderId": ObjectId("648d0d5c8f8b9b9f9f8b9b9b"),
        "paymentDate": datetime.datetime.utcnow(),
        "amount": 99.98,
        "method": "credit card",
        "status": "completed"
    })

    # Review Collection
    db.Review.insert_one({
        "_id": ObjectId("648d0d5c8f8b9b9f9f8b9b9e"),
        "productId": ObjectId("648d0d5c8f8b9b9f9f8b9b92"),
        "customerId": ObjectId("648d0d5c8f8b9b9f9f8b9b91"),
        "rating": 5,
        "comment": "Beautiful dress! Perfect fit.",
        "reviewDate": datetime.datetime.utcnow()
    })

    # Employee Collection
    db.Employee.insert_one({
        "_id": ObjectId("648d0d5c8f8b9b9f9f8b9b9f"),
        "name": "Jane Smith",
        "role": "Customer Support",
        "contact": "9876543210",
        "username": "janesmith",
        "password": "$2b$12$hashedpassword12345"  # Replace with bcrypt hashed password
    })

    print("Test data inserted successfully!")

# Run the script
if __name__ == "__main__":
    insert_test_data()
