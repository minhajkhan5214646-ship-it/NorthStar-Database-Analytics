# SQL in R Analysis for NorthStar Assignment

# ---------------------------------------------------------
# 1. Install and load required packages
# ---------------------------------------------------------

user_library <- Sys.getenv("R_LIBS_USER")
user_library <- path.expand(user_library)

if (user_library == "") {
  user_library <- file.path(Sys.getenv("USERPROFILE"), "R", "win-library")
}

if (!dir.exists(user_library)) {
  dir.create(user_library, recursive = TRUE)
}

.libPaths(c(user_library, .libPaths()))

packages <- c("DBI", "RSQLite")

for (pkg in packages) {
  if (!requireNamespace(pkg, quietly = TRUE)) {
    install.packages(
      pkg,
      lib = user_library,
      repos = "https://cloud.r-project.org",
      dependencies = TRUE
    )
  }
  library(pkg, character.only = TRUE)
}

print("Required R packages loaded successfully.")


# ---------------------------------------------------------
# 2. Load cleaned datasets
# ---------------------------------------------------------

vehicles <- read.csv("cleaned_data/vehicles_cleaned.csv")
orders <- read.csv("cleaned_data/orders_cleaned.csv")
incidents <- read.csv("cleaned_data/incidents_cleaned.csv")
hubs <- read.csv("cleaned_data/hubs_cleaned.csv")
drivers <- read.csv("cleaned_data/drivers_cleaned.csv")
deliveries <- read.csv("cleaned_data/deliveries_cleaned.csv")
customers <- read.csv("cleaned_data/customers_cleaned.csv")
complaints <- read.csv("cleaned_data/complaints_cleaned.csv")
app_events <- read.csv("cleaned_data/app_events_cleaned.csv")

print("Cleaned datasets loaded successfully into R.")


# ---------------------------------------------------------
# 3. Check dataset sizes
# ---------------------------------------------------------

print("Dataset sizes:")

print(paste("Vehicles:", nrow(vehicles), "rows and", ncol(vehicles), "columns"))
print(paste("Orders:", nrow(orders), "rows and", ncol(orders), "columns"))
print(paste("Incidents:", nrow(incidents), "rows and", ncol(incidents), "columns"))
print(paste("Hubs:", nrow(hubs), "rows and", ncol(hubs), "columns"))
print(paste("Drivers:", nrow(drivers), "rows and", ncol(drivers), "columns"))
print(paste("Deliveries:", nrow(deliveries), "rows and", ncol(deliveries), "columns"))
print(paste("Customers:", nrow(customers), "rows and", ncol(customers), "columns"))
print(paste("Complaints:", nrow(complaints), "rows and", ncol(complaints), "columns"))
print(paste("App Events:", nrow(app_events), "rows and", ncol(app_events), "columns"))


# ---------------------------------------------------------
# 4. Create SQLite database connection
# ---------------------------------------------------------

connection <- dbConnect(SQLite(), ":memory:")

print("SQLite database connection created successfully.")


# ---------------------------------------------------------
# 5. Copy datasets into SQLite tables
# ---------------------------------------------------------

dbWriteTable(connection, "vehicles", vehicles, overwrite = TRUE)
dbWriteTable(connection, "orders", orders, overwrite = TRUE)
dbWriteTable(connection, "incidents", incidents, overwrite = TRUE)
dbWriteTable(connection, "hubs", hubs, overwrite = TRUE)
dbWriteTable(connection, "drivers", drivers, overwrite = TRUE)
dbWriteTable(connection, "deliveries", deliveries, overwrite = TRUE)
dbWriteTable(connection, "customers", customers, overwrite = TRUE)
dbWriteTable(connection, "complaints", complaints, overwrite = TRUE)
dbWriteTable(connection, "app_events", app_events, overwrite = TRUE)

print("All datasets copied into SQLite database successfully.")


# ---------------------------------------------------------
# 6. Test SQL query
# ---------------------------------------------------------

query_1 <- "
SELECT delivery_status, COUNT(*) AS total_deliveries
FROM deliveries
GROUP BY delivery_status
ORDER BY total_deliveries DESC;
"

result_1 <- dbGetQuery(connection, query_1)

print("SQL Query 1: Number of deliveries by delivery status")
print(result_1)


# ---------------------------------------------------------
# 7. Close database connection
# ---------------------------------------------------------
# ---------------------------------------------------------
# 7. SQL Query 2: Delivery problem rate by pickup zone
# ---------------------------------------------------------

query_2 <- "
SELECT 
    o.pickup_zone,
    COUNT(d.delivery_id) AS total_deliveries,
    SUM(CASE 
        WHEN d.delivery_status IN ('Delayed', 'Failed') THEN 1 
        ELSE 0 
    END) AS problem_deliveries,
    ROUND(AVG(CASE 
        WHEN d.delivery_status IN ('Delayed', 'Failed') THEN 1.0 
        ELSE 0 
    END) * 100, 2) AS problem_rate_percent
FROM deliveries d
JOIN orders o
ON d.order_id = o.order_id
GROUP BY o.pickup_zone
ORDER BY problem_rate_percent DESC;
"

result_2 <- dbGetQuery(connection, query_2)

print("SQL Query 2: Delivery problem rate by pickup zone")
print(result_2)
# ---------------------------------------------------------
# SQL Query 3: Delayed and failed deliveries by hub
# ---------------------------------------------------------

query_3 <- "
SELECT 
    h.hub_name,
    h.zone,
    COUNT(d.delivery_id) AS problem_deliveries
FROM deliveries d
JOIN hubs h
ON d.hub_id = h.hub_id
WHERE d.delivery_status IN ('Delayed', 'Failed')
GROUP BY h.hub_name, h.zone
ORDER BY problem_deliveries DESC;
"

result_3 <- dbGetQuery(connection, query_3)

print("SQL Query 3: Delayed and failed deliveries by hub")
print(result_3)
# ---------------------------------------------------------
# SQL Query 4: Average rating and delivery duration by status
# ---------------------------------------------------------

query_4 <- "
SELECT 
    delivery_status,
    COUNT(delivery_id) AS total_deliveries,
    ROUND(AVG(customer_rating_post_delivery), 2) AS average_customer_rating,
    ROUND(AVG(delivery_duration_hours), 2) AS average_delivery_duration_hours
FROM deliveries
GROUP BY delivery_status
ORDER BY average_customer_rating DESC;
"

result_4 <- dbGetQuery(connection, query_4)

print("SQL Query 4: Average rating and delivery duration by status")
print(result_4)
# ---------------------------------------------------------
# SQL Query 5: Complaint count and compensation by complaint type
# ---------------------------------------------------------

query_5 <- "
SELECT 
    complaint_type,
    COUNT(complaint_id) AS total_complaints,
    ROUND(AVG(compensation_amount), 2) AS average_compensation,
    ROUND(SUM(compensation_amount), 2) AS total_compensation
FROM complaints
GROUP BY complaint_type
ORDER BY total_complaints DESC;
"

result_5 <- dbGetQuery(connection, query_5)

print("SQL Query 5: Complaint count and compensation by complaint type")
print(result_5)
# ---------------------------------------------------------
# SQL Query 6: Delivery problem rate by service type
# ---------------------------------------------------------

query_6 <- "
SELECT 
    o.service_type,
    COUNT(d.delivery_id) AS total_deliveries,
    SUM(CASE 
        WHEN d.delivery_status IN ('Delayed', 'Failed') THEN 1 
        ELSE 0 
    END) AS problem_deliveries,
    ROUND(AVG(CASE 
        WHEN d.delivery_status IN ('Delayed', 'Failed') THEN 1.0 
        ELSE 0 
    END) * 100, 2) AS problem_rate_percent
FROM deliveries d
JOIN orders o
ON d.order_id = o.order_id
GROUP BY o.service_type
ORDER BY problem_rate_percent DESC;
"

result_6 <- dbGetQuery(connection, query_6)

print("SQL Query 6: Delivery problem rate by service type")
print(result_6)
# ---------------------------------------------------------
# SQL Summary Findings
# ---------------------------------------------------------

print("Summary Findings from SQL in R Analysis:")

print("1. Most deliveries were completed on time, but delayed and failed deliveries still created a noticeable service reliability issue.")
print("2. Central pickup zone recorded the highest delivery problem rate, showing that service quality differs across zones.")
print("3. Central Core and Midtown Relay had the highest number of delayed and failed deliveries among hubs.")
print("4. On-time deliveries had the highest average customer rating and the shortest average delivery duration.")
print("5. Delay was the most common complaint type and also created the highest total compensation cost.")
print("6. Business service deliveries had the highest problem rate among service types.")
dbDisconnect(connection)

print("SQL in R starter analysis completed successfully.")
