from pymongo import MongoClient
from bson.objectid import ObjectId

# MongoDB Configuration
MONGO_URI = "mongodb://localhost:27017/"  # Replace with your MongoDB URI if different
DATABASE_NAME = "online_clothing_store_dev"  # Replace with your database name

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]

# Sample Data
categories = [
    {"_id": ObjectId("648d1c1e8f8b9b9f9f8b9c01"), "name": "Men"},
    {"_id": ObjectId("648d1c1e8f8b9b9f9f8b9c02"), "name": "Women"},
    {"_id": ObjectId("648d1c1e8f8b9b9f9f8b9c03"), "name": "Kids"},
]

subcategories = [
    {"_id": ObjectId("648d1c2e8f8b9b9f9f8b9c01"), "categoryId": ObjectId("648d1c1e8f8b9b9f9f8b9c01"), "name": "Jeans"},
    {"_id": ObjectId("648d1c2e8f8b9b9f9f8b9c02"), "categoryId": ObjectId("648d1c1e8f8b9b9f9f8b9c01"), "name": "Jackets"},
    {"_id": ObjectId("648d1c2e8f8b9b9f9f8b9c03"), "categoryId": ObjectId("648d1c1e8f8b9b9f9f8b9c02"), "name": "Dresses"},
    {"_id": ObjectId("648d1c2e8f8b9b9f9f8b9c04"), "categoryId": ObjectId("648d1c1e8f8b9b9f9f8b9c02"), "name": "Activewear"},
    {"_id": ObjectId("648d1c2e8f8b9b9f9f8b9c05"), "categoryId": ObjectId("648d1c1e8f8b9b9f9f8b9c03"), "name": "Toys"},
]

products = [
    {
        "_id": ObjectId("648d1d3e8f8b9b9f9f8b9c01"),
        "categoryId": ObjectId("648d1c1e8f8b9b9f9f8b9c01"),
        "subcategoryId": ObjectId("648d1c2e8f8b9b9f9f8b9c01"),
        "productVariantId": ObjectId("648d1d4e8f8b9b9f9f8b9c01"),
        "name": "Slim Fit Jeans",
        "description": "Comfortable and stylish slim-fit jeans for men.",
        "imageUrls": [
            "https://example.com/images/slimfit-jeans-1.jpg",
            "https://example.com/images/slimfit-jeans-2.jpg"
        ],
        "isTrending": True
    },
    {
        "_id": ObjectId("648d1d3e8f8b9b9f9f8b9c02"),
        "categoryId": ObjectId("648d1c1e8f8b9b9f9f8b9c02"),
        "subcategoryId": ObjectId("648d1c2e8f8b9b9f9f8b9c03"),
        "productVariantId": ObjectId("648d1d4e8f8b9b9f9f8b9c02"),
        "name": "Evening Gown",
        "description": "Elegant evening gown for special occasions.",
        "imageUrls": [
            "https://example.com/images/evening-gown-1.jpg",
            "https://example.com/images/evening-gown-2.jpg"
        ],
        "isTrending": True
    },
    {
        "_id": ObjectId("648d1d3e8f8b9b9f9f8b9c03"),
        "categoryId": ObjectId("648d1c1e8f8b9b9f9f8b9c03"),
        "subcategoryId": ObjectId("648d1c2e8f8b9b9f9f8b9c05"),
        "productVariantId": ObjectId("648d1d4e8f8b9b9f9f8b9c03"),
        "name": "Educational Toy Set",
        "description": "A fun and educational toy set for kids.",
        "imageUrls": [
            "https://example.com/images/toy-set-1.jpg",
            "https://example.com/images/toy-set-2.jpg"
        ],
        "isTrending": False
    },
]

product_variants = [
    {
        "_id": ObjectId("648d1d4e8f8b9b9f9f8b9c01"),
        "size": "32",
        "color": "Blue",
        "material": "Denim",
        "stockQuantity": 50,
        "price": 40.99
    },
    {
        "_id": ObjectId("648d1d4e8f8b9b9f9f8b9c02"),
        "size": "M",
        "color": "Red",
        "material": "Silk",
        "stockQuantity": 20,
        "price": 120.50
    },
    {
        "_id": ObjectId("648d1d4e8f8b9b9f9f8b9c03"),
        "size": "N/A",
        "color": "Multi",
        "material": "Plastic",
        "stockQuantity": 100,
        "price": 25.00
    },
]

# Insert Data
def insert_data(collection_name, data):
    collection = db[collection_name]
    collection.delete_many({})  # Optional: Clear existing data
    result = collection.insert_many(data)
    print(f"Inserted {len(result.inserted_ids)} documents into {collection_name}.")

# Main Function
if __name__ == "__main__":
    insert_data("Category", categories)
    insert_data("Subcategory", subcategories)
    insert_data("Product", products)
    insert_data("ProductVariant", product_variants)
    print("Data import completed!")
