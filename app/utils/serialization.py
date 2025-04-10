from bson import ObjectId
from datetime import datetime


def convert_to_serializable(data):
    # If it's a list, recursively process each item
    if isinstance(data, list):
        return [convert_to_serializable(item) for item in data]

    # If it's a dict, recursively process each value
    if isinstance(data, dict):
        return {key: convert_to_serializable(value) for key, value in data.items()}

    # Convert ObjectId to string
    if isinstance(data, ObjectId):
        return str(data)

    # Convert datetime to ISO string
    if isinstance(data, datetime):
        return data.isoformat()

    # Leave everything else unchanged
    return data
