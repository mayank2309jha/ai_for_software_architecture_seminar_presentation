import pandas as pd
import matplotlib.pyplot as plt

# Load CSV
df = pd.read_csv("analytics.csv")

# Convert timestamps to relative time (start from 0)
df["arrivalTime"] = df["arrivalTime"] - df["arrivalTime"].min()

# -----------------------------
# 1. Orders over time
# -----------------------------
plt.figure()
df["arrivalTime"].plot(kind="hist", bins=50)
plt.title("Orders Arrival Distribution")
plt.xlabel("Time (ms)")
plt.ylabel("Number of Orders")
plt.savefig("orders_over_time.png")
plt.close()

# -----------------------------
# 2. Latency Distribution
# -----------------------------
plt.figure()
df["latency"].plot(kind="hist", bins=50)
plt.title("Latency Distribution")
plt.xlabel("Latency (ms)")
plt.ylabel("Count")
plt.savefig("latency_distribution.png")
plt.close()

# -----------------------------
# 3. Processing Time Distribution
# -----------------------------
plt.figure()
df["processingTime"].plot(kind="hist", bins=50)
plt.title("Processing Time Distribution")
plt.xlabel("Processing Time (ms)")
plt.ylabel("Count")
plt.savefig("processing_time_distribution.png")
plt.close()

# -----------------------------
# 4. Match vs Stored
# -----------------------------
plt.figure()
df["status"].value_counts().plot(kind="bar")
plt.title("Matched vs Stored Orders")
plt.xlabel("Status")
plt.ylabel("Count")
plt.savefig("match_vs_stored.png")
plt.close()

# -----------------------------
# 5. Orders per Item
# -----------------------------
plt.figure()
df["item"].value_counts().sort_index().plot(kind="bar")
plt.title("Orders per Item (A-J)")
plt.xlabel("Item")
plt.ylabel("Count")
plt.savefig("orders_per_item.png")
plt.close()

# -----------------------------
# 6. Latency Over Time (Trend)
# -----------------------------
plt.figure()
plt.scatter(df["arrivalTime"], df["latency"], s=5)
plt.title("Latency Over Time")
plt.xlabel("Time (ms)")
plt.ylabel("Latency (ms)")
plt.savefig("latency_over_time.png")
plt.close()

# -----------------------------
# 7. Orders Completion Over Time
# -----------------------------
plt.figure()

# Sort by completion time
df_sorted = df.sort_values(by="endProcessTime")

# Convert to relative time
df_sorted["endProcessTime"] = df_sorted["endProcessTime"] - df_sorted["endProcessTime"].min()

# Create cumulative count
df_sorted["completed_orders"] = range(1, len(df_sorted) + 1)

# Plot
plt.plot(df_sorted["endProcessTime"], df_sorted["completed_orders"])

plt.title("Orders Completed Over Time")
plt.xlabel("Time (ms)")
plt.ylabel("Cumulative Completed Orders")

plt.savefig("orders_completion_over_time.png")
plt.close()
print("All graphs generated successfully!")
