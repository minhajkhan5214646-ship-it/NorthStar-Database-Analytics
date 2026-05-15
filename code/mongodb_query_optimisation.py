from pymongo import MongoClient, ASCENDING
from urllib.parse import quote_plus

print("MongoDB query optimisation file started.")

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
# 1. Remove old custom indexes for a fair test
# ---------------------------------------------------------

db.deliveries.drop_indexes()
db.complaints.drop_indexes()
db.app_events.drop_indexes()

print("\nOld custom indexes removed. Default _id indexes remain.")


# ---------------------------------------------------------
# 2. Explain query before indexing
# ---------------------------------------------------------

explain_before = db.command(
    "explain",
    {
        "find": "deliveries",
        "filter": {"delivery_status": "Delayed"}
    },
    verbosity="executionStats"
)

print("\nQuery performance BEFORE indexing:")
print("Documents returned:", explain_before["executionStats"]["nReturned"])
print("Documents examined:", explain_before["executionStats"]["totalDocsExamined"])
print("Keys examined:", explain_before["executionStats"]["totalKeysExamined"])
print("Execution time ms:", explain_before["executionStats"]["executionTimeMillis"])


# ---------------------------------------------------------
# 3. Create useful indexes
# ---------------------------------------------------------

db.deliveries.create_index([("delivery_status", ASCENDING)])
db.deliveries.create_index([("order_id", ASCENDING)])
db.deliveries.create_index([("hub_id", ASCENDING)])

db.complaints.create_index([("complaint_type", ASCENDING)])
db.complaints.create_index([("customer_id", ASCENDING)])
db.complaints.create_index([("order_id", ASCENDING)])

db.app_events.create_index([("event_type", ASCENDING)])
db.app_events.create_index([("customer_id", ASCENDING)])
db.app_events.create_index([("event_timestamp", ASCENDING)])

print("\nIndexes created successfully.")


# ---------------------------------------------------------
# 4. Explain same query after indexing
# ---------------------------------------------------------

explain_after = db.command(
    "explain",
    {
        "find": "deliveries",
        "filter": {"delivery_status": "Delayed"}
    },
    verbosity="executionStats"
)

print("\nQuery performance AFTER indexing:")
print("Documents returned:", explain_after["executionStats"]["nReturned"])
print("Documents examined:", explain_after["executionStats"]["totalDocsExamined"])
print("Keys examined:", explain_after["executionStats"]["totalKeysExamined"])
print("Execution time ms:", explain_after["executionStats"]["executionTimeMillis"])


# ---------------------------------------------------------
# 5. Show created indexes
# ---------------------------------------------------------

print("\nIndexes on deliveries collection:")
for index in db.deliveries.list_indexes():
    print(index)

print("\nIndexes on complaints collection:")
for index in db.complaints.list_indexes():
    print(index)

print("\nIndexes on app_events collection:")
for index in db.app_events.list_indexes():
    print(index)


print("\nMongoDB query optimisation completed successfully.")