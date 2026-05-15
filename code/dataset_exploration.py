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

print("All datasets loaded successfully.")
print("\nNumber of rows and columns in each dataset:")

print("Vehicles:", vehicles.shape)
print("Orders:", orders.shape)
print("Incidents:", incidents.shape)
print("Hubs:", hubs.shape)
print("Drivers:", drivers.shape)
print("Deliveries:", deliveries.shape)
print("Customers:", customers.shape)
print("Complaints:", complaints.shape)
print("App Events:", app_events.shape)
print("\nColumn names in each dataset:")

print("\nVehicles columns:")
print(vehicles.columns)

print("\nOrders columns:")
print(orders.columns)

print("\nIncidents columns:")
print(incidents.columns)

print("\nHubs columns:")
print(hubs.columns)

print("\nDrivers columns:")
print(drivers.columns)

print("\nDeliveries columns:")
print(deliveries.columns)

print("\nCustomers columns:")
print(customers.columns)

print("\nComplaints columns:")
print(complaints.columns)

print("\nApp Events columns:")
print(app_events.columns)
print("\nData types in each dataset:")

print("\nVehicles data types:")
print(vehicles.dtypes)

print("\nOrders data types:")
print(orders.dtypes)

print("\nIncidents data types:")
print(incidents.dtypes)

print("\nHubs data types:")
print(hubs.dtypes)

print("\nDrivers data types:")
print(drivers.dtypes)

print("\nDeliveries data types:")
print(deliveries.dtypes)

print("\nCustomers data types:")
print(customers.dtypes)

print("\nComplaints data types:")
print(complaints.dtypes)

print("\nApp Events data types:")
print(app_events.dtypes)
print("\nMissing values in each dataset:")

print("\nVehicles:")
print(vehicles.isnull().sum())

print("\nOrders:")
print(orders.isnull().sum())

print("\nIncidents:")
print(incidents.isnull().sum())

print("\nHubs:")
print(hubs.isnull().sum())

print("\nDrivers:")
print(drivers.isnull().sum())

print("\nDeliveries:")
print(deliveries.isnull().sum())

print("\nCustomers:")
print(customers.isnull().sum())

print("\nComplaints:")
print(complaints.isnull().sum())

print("\nApp Events:")
print(app_events.isnull().sum())
print("\nDuplicate rows in each dataset:")

print("Vehicles:", vehicles.duplicated().sum())
print("Orders:", orders.duplicated().sum())
print("Incidents:", incidents.duplicated().sum())
print("Hubs:", hubs.duplicated().sum())
print("Drivers:", drivers.duplicated().sum())
print("Deliveries:", deliveries.duplicated().sum())
print("Customers:", customers.duplicated().sum())
print("Complaints:", complaints.duplicated().sum())
print("App Events:", app_events.duplicated().sum())
print("\nUnique zone values:")

print("\nVehicles assigned_zone:")
print(vehicles["assigned_zone"].unique())

print("\nOrders pickup_zone:")
print(orders["pickup_zone"].unique())

print("\nOrders dropoff_zone:")
print(orders["dropoff_zone"].unique())

print("\nDrivers base_zone:")
print(drivers["base_zone"].unique())

print("\nCustomers home_zone:")
print(customers["home_zone"].unique())

print("\nApp Events zone_context:")
print(app_events["zone_context"].unique())