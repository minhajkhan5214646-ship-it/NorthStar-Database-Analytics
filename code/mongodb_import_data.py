import pandas as pd
import json
from pymongo import MongoClient
from urllib.parse import quote_plus

print("MongoDB import file started.")

password = input("Enter your MongoDB password: ")
encoded_password = quote_plus(password)

connection_string = f"mongodb+srv://minhajkhan5214646_db_user:{encoded_password}@minhaj.we9e1mr.mongodb.net/?appName=Minhaj"

client = MongoClient(connection_string)
db = client["northstar_db"]

client.admin.command("ping")
print("MongoDB Atlas connection successful.")


def import_csv_to_mongodb(file_path, collection_name):
    data = pd.read_csv(file_path)

    # Convert NaN values into proper MongoDB null values
    records = json.loads(data.to_json(orient="records"))

    collection = db[collection_name]

    # Clear old data to avoid duplicates
    collection.delete_many({})

    if records:
        collection.insert_many(records)

    print(f"{collection_name}: {len(records)} records inserted successfully.")


import_csv_to_mongodb("cleaned_data/vehicles_cleaned.csv", "vehicles")
import_csv_to_mongodb("cleaned_data/orders_cleaned.csv", "orders")
import_csv_to_mongodb("cleaned_data/incidents_cleaned.csv", "incidents")
import_csv_to_mongodb("cleaned_data/hubs_cleaned.csv", "hubs")
import_csv_to_mongodb("cleaned_data/drivers_cleaned.csv", "drivers")
import_csv_to_mongodb("cleaned_data/deliveries_cleaned.csv", "deliveries")
import_csv_to_mongodb("cleaned_data/customers_cleaned.csv", "customers")
import_csv_to_mongodb("cleaned_data/complaints_cleaned.csv", "complaints")
import_csv_to_mongodb("cleaned_data/app_events_cleaned.csv", "app_events")

print("All cleaned datasets imported into MongoDB Atlas successfully.")