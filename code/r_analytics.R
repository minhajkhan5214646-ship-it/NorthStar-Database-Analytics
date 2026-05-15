# R Analytics for NorthStar Assignment

# ---------------------------------------------------------
# 1. Load cleaned datasets
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

print("Cleaned datasets loaded successfully for R analytics.")


# ---------------------------------------------------------
# 2. Basic descriptive statistics
# ---------------------------------------------------------

print("Descriptive statistics for delivery duration:")
print(summary(deliveries$delivery_duration_hours))

print("Descriptive statistics for customer rating after delivery:")
print(summary(deliveries$customer_rating_post_delivery))

print("Descriptive statistics for fuel or charge cost:")
print(summary(deliveries$fuel_or_charge_cost))

print("Descriptive statistics for app latency:")
print(summary(app_events$api_latency_ms))
# ---------------------------------------------------------
# 3. Average delivery duration by delivery status
# ---------------------------------------------------------

average_duration_by_status <- aggregate(
  delivery_duration_hours ~ delivery_status,
  data = deliveries,
  FUN = mean,
  na.rm = TRUE
)

average_duration_by_status$delivery_duration_hours <- round(
  average_duration_by_status$delivery_duration_hours,
  2
)

print("Average delivery duration by delivery status:")
print(average_duration_by_status)

# Save R chart
png("charts/r_average_duration_by_status.png", width = 800, height = 500)

barplot(
  average_duration_by_status$delivery_duration_hours,
  names.arg = average_duration_by_status$delivery_status,
  main = "Average Delivery Duration by Delivery Status",
  xlab = "Delivery Status",
  ylab = "Average Delivery Duration Hours"
)

dev.off()
# ---------------------------------------------------------
# 4. Correlation between delivery duration and customer rating
# ---------------------------------------------------------

rating_duration_data <- deliveries[
  !is.na(deliveries$delivery_duration_hours) &
  !is.na(deliveries$customer_rating_post_delivery),
]

correlation_result <- cor.test(
  rating_duration_data$delivery_duration_hours,
  rating_duration_data$customer_rating_post_delivery
)

print("Correlation between delivery duration and customer rating:")
print(correlation_result)

# Save R scatter plot
png("charts/r_duration_vs_customer_rating.png", width = 800, height = 500)

plot(
  rating_duration_data$delivery_duration_hours,
  rating_duration_data$customer_rating_post_delivery,
  main = "Delivery Duration vs Customer Rating",
  xlab = "Delivery Duration Hours",
  ylab = "Customer Rating"
)

dev.off()
# ---------------------------------------------------------
# 5. App latency by success status
# ---------------------------------------------------------

app_events$success_label <- ifelse(
  app_events$success_flag == 1,
  "Success",
  "Failed"
)

average_latency_by_status <- aggregate(
  api_latency_ms ~ success_label,
  data = app_events,
  FUN = mean
)

average_latency_by_status$api_latency_ms <- round(
  average_latency_by_status$api_latency_ms,
  2
)

print("Average app latency by success status:")
print(average_latency_by_status)

latency_test <- t.test(
  api_latency_ms ~ success_label,
  data = app_events
)

print("T-test comparing app latency between successful and failed events:")
print(latency_test)

# Save R chart
png("charts/r_app_latency_by_success_status.png", width = 800, height = 500)

barplot(
  average_latency_by_status$api_latency_ms,
  names.arg = average_latency_by_status$success_label,
  main = "Average App Latency by Success Status",
  xlab = "App Event Status",
  ylab = "Average API Latency ms"
)

dev.off()
# ---------------------------------------------------------
# 6. Summary findings from R analytics
# ---------------------------------------------------------

print("Summary Findings from R Analytics:")

print("1. The average delivery duration was 10.32 hours, while the median was 7.91 hours, showing that some long deliveries increased the average.")
print("2. Failed deliveries had the longest average delivery duration, followed by delayed deliveries.")
print("3. On-time deliveries had the shortest average delivery duration.")
print("4. Pearson correlation showed a negative relationship between delivery duration and customer rating, meaning longer deliveries are linked with lower ratings.")
print("5. App latency was very similar between successful and failed app events.")
print("6. The t-test showed that app latency difference between successful and failed app events was not statistically significant.")
print("R analytics completed successfully.")