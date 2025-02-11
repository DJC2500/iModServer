import os
from pymongo import MongoClient
from pymongo.errors import OperationFailure


MONGO_URI = os.getenv("MONGO_URI")

# Connect to MongoDB
client = MongoClient(MONGO_URI)

# Define the database
db = client['xChange']  # Replace 'messagingApp' with your DB name

# Schema validation rules
message_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["message_id", "sender", "recipient", "content", "timestamp"],
        "properties": {
            "message_id": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "sender": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "recipient": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "content": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "timestamp": {
                "bsonType": "date",
                "description": "must be a date and is required"
            }
        }
    }
}

# Optional: Insert an example message to verify the schema
message = {
    "message_id": "abc123",
    "sender": "user123",
    "recipient": "user456",
    "content": "Hello, how are you?",
    "timestamp": "2025-02-05T10:00:00Z"
}

# Insert a message document
message_collection = db["Messages"]
result = message_collection.insert_one(message)
print(f"Message inserted with ID: {result.inserted_id}")
