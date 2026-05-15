import pandas as pd
import matplotlib.pyplot as plt

vehicles = pd.read_csv("cleaned_data/vehicles_cleaned.csv")
orders = pd.read_csv("cleaned_data/orders_cleaned.csv")
incidents = pd.read_csv("cleaned_data/incidents_cleaned.csv")
hubs = pd.read_csv("cleaned_data/hubs_cleaned.csv")
drivers = pd.read_csv("cleaned_data/drivers_cleaned.csv")
deliveries = pd.read_csv("cleaned_data/deliveries_cleaned.csv")
customers = pd.read_csv("cleaned_data/customers_cleaned.csv")
complaints = pd.read_csv("cleaned_data/complaints_cleaned.csv")
app_events = pd.read_csv("cleaned_data/app_events_cleaned.csv")

print("Cleaned datasets loaded successfully for analysis.")
# Chart 1: Number of deliveries by delivery status

delivery_status_counts = deliveries["delivery_status"].value_counts()

print("\nDelivery status counts:")
print(delivery_status_counts)

delivery_status_counts.plot(kind="bar")

plt.title("Number of Deliveries by Delivery Status")
plt.xlabel("Delivery Status")
plt.ylabel("Number of Deliveries")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig("charts/delivery_status_counts.png")
plt.show()
# Chart 2: Number of complaints by complaint type

complaint_type_counts = complaints["complaint_type"].value_counts()

print("\nComplaint type counts:")
print(complaint_type_counts)

complaint_type_counts.plot(kind="bar")

plt.title("Number of Complaints by Complaint Type")
plt.xlabel("Complaint Type")
plt.ylabel("Number of Complaints")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("charts/complaints_by_type.png")
plt.show()
# Chart 3: Delayed and failed deliveries by hub

delivery_hub = deliveries.merge(
    hubs[["hub_id", "hub_name", "zone"]],
    on="hub_id",
    how="left"
)

problem_deliveries = delivery_hub[
    delivery_hub["delivery_status"].isin(["Delayed", "Failed"])
]

problem_by_hub = problem_deliveries["hub_name"].value_counts()

print("\nDelayed and failed deliveries by hub:")
print(problem_by_hub)

plt.figure()
problem_by_hub.plot(kind="bar")

plt.title("Delayed and Failed Deliveries by Hub")
plt.xlabel("Hub")
plt.ylabel("Number of Problem Deliveries")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("charts/problem_deliveries_by_hub.png")
plt.show()
# Chart 4: Average customer rating by delivery status

average_rating_by_status = deliveries.groupby("delivery_status")["customer_rating_post_delivery"].mean()

print("\nAverage customer rating by delivery status:")
print(average_rating_by_status)

plt.figure()
average_rating_by_status.plot(kind="bar")

plt.title("Average Customer Rating by Delivery Status")
plt.xlabel("Delivery Status")
plt.ylabel("Average Customer Rating")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig("charts/average_rating_by_status.png")
plt.show()
# Chart 5: Average manual route overrides by delivery status

average_override_by_status = deliveries.groupby("delivery_status")["manual_route_override_count"].mean()

print("\nAverage manual route overrides by delivery status:")
print(average_override_by_status)

plt.figure()
average_override_by_status.plot(kind="bar")

plt.title("Average Manual Route Overrides by Delivery Status")
plt.xlabel("Delivery Status")
plt.ylabel("Average Number of Route Overrides")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig("charts/average_route_overrides_by_status.png")
plt.show()
# Chart 6: Delivery problem rate by pickup zone

delivery_orders = deliveries.merge(
    orders[["order_id", "pickup_zone"]],
    on="order_id",
    how="left"
)

delivery_orders["problem_delivery"] = delivery_orders["delivery_status"].isin(["Delayed", "Failed"])

problem_rate_by_zone = delivery_orders.groupby("pickup_zone")["problem_delivery"].mean() * 100

problem_rate_by_zone = problem_rate_by_zone.sort_values(ascending=False)

print("\nDelivery problem rate by pickup zone (%):")
print(problem_rate_by_zone)

plt.figure()
problem_rate_by_zone.plot(kind="bar")

plt.title("Delivery Problem Rate by Pickup Zone")
plt.xlabel("Pickup Zone")
plt.ylabel("Problem Delivery Rate (%)")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("charts/problem_rate_by_pickup_zone.png")
plt.show()
# Summary findings from Python analysis

print("\nSummary Findings from Python Analysis:")

print("1. Most deliveries were completed on time, but delayed and failed deliveries still form a noticeable service issue.")
print("2. Delay was the most common complaint type, showing that late service is a major customer concern.")
print("3. Central Core and Midtown Relay recorded the highest number of delayed and failed deliveries.")
print("4. On-time deliveries received much higher customer ratings than delayed and failed deliveries.")
print("5. Delayed and failed deliveries had slightly higher manual route override counts than on-time deliveries.")
print("6. Central pickup zone had the highest delivery problem rate, suggesting uneven service performance across zones.")