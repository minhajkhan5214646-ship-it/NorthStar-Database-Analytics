print("CRUD file started")

from pymongo import MongoClient
from getpass import getpass
from urllib.parse import quote_plus

# Ask password safely
password = getpass("Enter your MongoDB password: ")
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
# 1. CREATE operation: insert a test complaint
# ---------------------------------------------------------

test_complaint = {
    "complaint_id": "TEST001",
    "customer_id": "CUST_TEST",
    "order_id": "ORD_TEST",
    "complaint_type": "Delay",
    "channel": "App",
    "severity": "High",
    "created_at": "2026-05-14",
    "status": "Open",
    "resolution_days": None,
    "compensation_amount": None
}

db.complaints.insert_one(test_complaint)

print("\nCREATE operation completed: test complaint inserted.")


# ---------------------------------------------------------
# 2. READ operation: find high severity complaints
# ---------------------------------------------------------

high_severity_complaints = db.complaints.find(
    {"severity": "High"},
    {
        "_id": 0,
        "complaint_id": 1,
        "complaint_type": 1,
        "severity": 1,
        "status": 1
    }
).limit(5)

print("\nREAD operation completed: high severity complaints found.")

for complaint in high_severity_complaints:
    print(complaint)


# ---------------------------------------------------------
# 3. UPDATE operation: update the test complaint status
# ---------------------------------------------------------

db.complaints.update_one(
    {"complaint_id": "TEST001"},
    {"$set": {"status": "Resolved", "resolution_days": 2}}
)

updated_complaint = db.complaints.find_one(
    {"complaint_id": "TEST001"},
    {"_id": 0}
)

print("\nUPDATE operation completed: test complaint updated.")
print(updated_complaint)


# ---------------------------------------------------------
# 4. DELETE operation: delete the test complaint
# ---------------------------------------------------------

db.complaints.delete_one({"complaint_id": "TEST001"})

deleted_check = db.complaints.find_one(
    {"complaint_id": "TEST001"}
)

print("\nDELETE operation completed: test complaint deleted.")
print("Deleted record check:", deleted_check)


print("\nMongoDB CRUD operations completed successfully.")