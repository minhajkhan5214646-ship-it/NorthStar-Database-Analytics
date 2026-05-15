import pandas as pd

vehicles = pd.read_csv("vehicles.csv")
orders = pd.read_csv("orders.csv")
incidents = pd.read_csv("incidents.csv")
hubs = pd.read_csv("hubs.csv")
drivers = pd.read_csv("drivers.csv")
deliveries = pd.read_csv("deliveries.csv")
customers = pd.read_csv("customers.csv")
complaints = pd.read_csv("complaints.csv")
app_events = pd.read_csv("app_events.csv")

print("All datasets loaded for preprocessing.")
# Standardise zone names

def clean_zone_names(column):
    column = column.str.strip().str.title()
    column = column.replace({"Ctr": "Central"})
    return column

vehicles["assigned_zone"] = clean_zone_names(vehicles["assigned_zone"])
orders["pickup_zone"] = clean_zone_names(orders["pickup_zone"])
orders["dropoff_zone"] = clean_zone_names(orders["dropoff_zone"])
hubs["zone"] = clean_zone_names(hubs["zone"])
drivers["base_zone"] = clean_zone_names(drivers["base_zone"])
customers["home_zone"] = clean_zone_names(customers["home_zone"])
app_events["zone_context"] = clean_zone_names(app_events["zone_context"])

print("\nZone names after cleaning:")
print("Vehicles:", vehicles["assigned_zone"].unique())
print("Orders pickup:", orders["pickup_zone"].unique())
print("Orders dropoff:", orders["dropoff_zone"].unique())
print("Drivers:", drivers["base_zone"].unique())
print("Customers:", customers["home_zone"].unique())
print("App Events:", app_events["zone_context"].unique())
# Convert date columns to datetime format

vehicles["commission_date"] = pd.to_datetime(vehicles["commission_date"])
orders["order_created_at"] = pd.to_datetime(orders["order_created_at"])
incidents["reported_at"] = pd.to_datetime(incidents["reported_at"])
deliveries["dispatch_time"] = pd.to_datetime(deliveries["dispatch_time"])
deliveries["delivery_completed_at"] = pd.to_datetime(deliveries["delivery_completed_at"])
customers["signup_date"] = pd.to_datetime(customers["signup_date"])
complaints["created_at"] = pd.to_datetime(complaints["created_at"])
app_events["event_timestamp"] = pd.to_datetime(app_events["event_timestamp"])

print("\nDate columns converted successfully.")
print("\nDate column data types after conversion:")

print("commission_date:", vehicles["commission_date"].dtype)
print("order_created_at:", orders["order_created_at"].dtype)
print("reported_at:", incidents["reported_at"].dtype)
print("dispatch_time:", deliveries["dispatch_time"].dtype)
print("delivery_completed_at:", deliveries["delivery_completed_at"].dtype)
print("signup_date:", customers["signup_date"].dtype)
print("created_at:", complaints["created_at"].dtype)
print("event_timestamp:", app_events["event_timestamp"].dtype)
# Check possible reasons for some missing values

print("\nResolution status where resolved_hours is missing:")
print(incidents[incidents["resolved_hours"].isnull()]["resolution_status"].value_counts())

print("\nDelivery status where delivery_completed_at is missing:")
print(deliveries[deliveries["delivery_completed_at"].isnull()]["delivery_status"].value_counts())

print("\nDelivery status where customer_rating_post_delivery is missing:")
print(deliveries[deliveries["customer_rating_post_delivery"].isnull()]["delivery_status"].value_counts())
# Handle missing values that are safe to fill

vehicles["battery_health_pct"] = vehicles["battery_health_pct"].fillna(
    vehicles["battery_health_pct"].median()
)

orders["booking_channel"] = orders["booking_channel"].fillna("Unknown")

drivers["training_score"] = drivers["training_score"].fillna(
    drivers["training_score"].median()
)

customers["loyalty_score"] = customers["loyalty_score"].fillna(
    customers["loyalty_score"].median()
)

customers["preferred_channel"] = customers["preferred_channel"].fillna("Unknown")

print("\nSafe missing values filled successfully.")
print("\nMissing values after safe cleaning:")

print("\nVehicles:")
print(vehicles.isnull().sum())

print("\nOrders:")
print(orders.isnull().sum())

print("\nDrivers:")
print(drivers.isnull().sum())

print("\nCustomers:")
print(customers.isnull().sum())
# Check remaining missing values before deciding how to handle them

print("\nComplaint status where compensation_amount is missing:")
print(complaints[complaints["compensation_amount"].isnull()]["status"].value_counts())

print("\nComplaint types where compensation_amount is missing:")
print(complaints[complaints["compensation_amount"].isnull()]["complaint_type"].value_counts())

print("\nApp event types where order_id is missing:")
print(app_events[app_events["order_id"].isnull()]["event_type"].value_counts())
# Remaining missing values are kept because they cannot be safely estimated

print("\nRemaining missing values kept after cleaning:")

print("Incidents - resolved_hours:", incidents["resolved_hours"].isnull().sum())
print("Deliveries - delivery_completed_at:", deliveries["delivery_completed_at"].isnull().sum())
print("Deliveries - customer_rating_post_delivery:", deliveries["customer_rating_post_delivery"].isnull().sum())
print("Complaints - compensation_amount:", complaints["compensation_amount"].isnull().sum())
print("App Events - order_id:", app_events["order_id"].isnull().sum())
# Check other important categorical columns

print("\nUnique values in important categorical columns:")

print("\nVehicle types:")
print(vehicles["vehicle_type"].unique())

print("\nMaintenance status:")
print(vehicles["maintenance_status"].unique())

print("\nDelivery status:")
print(deliveries["delivery_status"].unique())

print("\nIncident severity:")
print(incidents["severity"].unique())

print("\nComplaint severity:")
print(complaints["severity"].unique())

print("\nComplaint status:")
print(complaints["status"].unique())

print("\nCustomer account status:")
print(customers["account_status"].unique())
# Check ranges of important numeric columns

print("\nSummary of important numeric columns:")

print("\nVehicles:")
print(vehicles[["battery_health_pct", "odometer_km"]].describe())

print("\nDrivers:")
print(drivers[["years_experience", "training_score", "driver_rating"]].describe())

print("\nCustomers:")
print(customers[["age", "loyalty_score", "app_engagement_score"]].describe())

print("\nDeliveries:")
print(deliveries[[
    "route_distance_km",
    "manual_route_override_count",
    "customer_rating_post_delivery",
    "fuel_or_charge_cost"
]].describe())
# Save cleaned datasets into the cleaned_data folder

vehicles.to_csv("cleaned_data/vehicles_cleaned.csv", index=False)
orders.to_csv("cleaned_data/orders_cleaned.csv", index=False)
incidents.to_csv("cleaned_data/incidents_cleaned.csv", index=False)
hubs.to_csv("cleaned_data/hubs_cleaned.csv", index=False)
drivers.to_csv("cleaned_data/drivers_cleaned.csv", index=False)
deliveries.to_csv("cleaned_data/deliveries_cleaned.csv", index=False)
customers.to_csv("cleaned_data/customers_cleaned.csv", index=False)
complaints.to_csv("cleaned_data/complaints_cleaned.csv", index=False)
app_events.to_csv("cleaned_data/app_events_cleaned.csv", index=False)

print("\nAll cleaned datasets saved successfully.")
# Create delivery duration in hours

deliveries["delivery_duration_hours"] = (
    deliveries["delivery_completed_at"] - deliveries["dispatch_time"]
).dt.total_seconds() / 3600

print("\nDelivery duration column created.")
print(deliveries[["dispatch_time", "delivery_completed_at", "delivery_duration_hours"]].head())
# Check for impossible negative delivery durations

print("\nNumber of negative delivery durations:")
print((deliveries["delivery_duration_hours"] < 0).sum())

print("\nRows with negative delivery durations:")
print(deliveries[deliveries["delivery_duration_hours"] < 0][[
    "delivery_id",
    "dispatch_time",
    "delivery_completed_at",
    "delivery_status",
    "delivery_duration_hours"
]])
# Replace impossible negative durations with missing values

deliveries.loc[
    deliveries["delivery_duration_hours"] < 0,
    "delivery_duration_hours"
] = float("nan")

print("\nNegative delivery durations replaced with missing values.")
print("Remaining negative durations:",
      (deliveries["delivery_duration_hours"] < 0).sum())
print("\nMissing values in delivery_duration_hours after cleaning:")
print(deliveries["delivery_duration_hours"].isnull().sum())
# Save cleaned datasets into the cleaned_data folder

vehicles.to_csv("cleaned_data/vehicles_cleaned.csv", index=False)
orders.to_csv("cleaned_data/orders_cleaned.csv", index=False)
incidents.to_csv("cleaned_data/incidents_cleaned.csv", index=False)
hubs.to_csv("cleaned_data/hubs_cleaned.csv", index=False)
drivers.to_csv("cleaned_data/drivers_cleaned.csv", index=False)
deliveries.to_csv("cleaned_data/deliveries_cleaned.csv", index=False)
customers.to_csv("cleaned_data/customers_cleaned.csv", index=False)
complaints.to_csv("cleaned_data/complaints_cleaned.csv", index=False)
app_events.to_csv("cleaned_data/app_events_cleaned.csv", index=False)

print("\nAll cleaned datasets saved successfully.")