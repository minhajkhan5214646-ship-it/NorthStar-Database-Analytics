from pymongo import MongoClient
from urllib.parse import quote_plus

print("MongoDB aggregation file started.")

# Ask password normally
password = input("Enter your MongoDB password: ")
encoded_password = quote_plus(password)

# MongoDB connection
connection_string = f"mongodb+srv://minhajkhan5214646_db_user:{encoded_password}@minhaj.we9e1mr.mongodb.net/?appName=Minhaj"

client = MongoClient(connection_string)

# Select database
db = client["northstar_db"]

# Test connection
client.admin.command("ping")
print("MongoDB Atlas connection successful.")


# ---------------------------------------------------------
# Aggregation 1: Delivery status counts
# ---------------------------------------------------------

pipeline_1 = [
    {
        "$group": {
            "_id": "$delivery_status",
            "total_deliveries": {"$sum": 1}
        }
    },
    {
        "$sort": {"total_deliveries": -1}
    }
]

result_1 = db.deliveries.aggregate(pipeline_1)

print("\nAggregation 1: Delivery status counts")
for item in result_1:
    print(item)


# ---------------------------------------------------------
# Aggregation 2: Complaint count and compensation by complaint type
# ---------------------------------------------------------

pipeline_2 = [
    {
        "$group": {
            "_id": "$complaint_type",
            "total_complaints": {"$sum": 1},
            "average_compensation": {"$avg": "$compensation_amount"},
            "total_compensation": {"$sum": "$compensation_amount"}
        }
    },
    {
        "$project": {
            "_id": 1,
            "total_complaints": 1,
            "average_compensation": {"$round": ["$average_compensation", 2]},
            "total_compensation": {"$round": ["$total_compensation", 2]}
        }
    },
    {
        "$sort": {"total_complaints": -1}
    }
]

result_2 = db.complaints.aggregate(pipeline_2)

print("\nAggregation 2: Complaint count and compensation by complaint type")
for item in result_2:
    print(item)


# ---------------------------------------------------------
# Aggregation 3: Average app latency by event type
# ---------------------------------------------------------

pipeline_3 = [
    {
        "$group": {
            "_id": "$event_type",
            "average_latency_ms": {"$avg": "$api_latency_ms"},
            "total_events": {"$sum": 1}
        }
    },
    {
        "$project": {
            "_id": 1,
            "total_events": 1,
            "average_latency_ms": {"$round": ["$average_latency_ms", 2]}
        }
    },
    {
        "$sort": {"average_latency_ms": -1}
    }
]

result_3 = db.app_events.aggregate(pipeline_3)

print("\nAggregation 3: Average app latency by event type")
for item in result_3:
    print(item)


print("\nMongoDB aggregation queries completed successfully.")