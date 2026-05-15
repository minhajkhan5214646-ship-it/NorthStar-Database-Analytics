from pymongo import MongoClient
from getpass import getpass

# Ask password safely, so it is not saved inside the code
password = getpass("Enter your MongoDB password: ")

connection_string = f"mongodb+srv://minhajkhan5214646_db_user:{password}@minhaj.we9e1mr.mongodb.net/?appName=Minhaj"

client = MongoClient(connection_string)

# Test connection
try:
    client.admin.command("ping")
    print("MongoDB Atlas connection successful.")
except Exception as e:
    print("MongoDB connection failed.")
    print(e)