import pandas as pd
import matplotlib.pyplot as plt

# Load baseline
baseline = pd.read_csv("baseline_metrics.csv")

# Drop only rows where key columns are missing (NOT all columns)
baseline = baseline.dropna(
    subset=["totalTime", "waitingTime", "processingTime"])

# Convert to numeric
baseline["totalTime"] = pd.to_numeric(baseline["totalTime"], errors="coerce")
baseline["waitingTime"] = pd.to_numeric(
    baseline["waitingTime"], errors="coerce")
baseline["processingTime"] = pd.to_numeric(
    baseline["processingTime"], errors="coerce")

# Drop again after coerce (in case any became NaN)
baseline = baseline.dropna(
    subset=["totalTime", "waitingTime", "processingTime"])

print(f"Rows loaded: {len(baseline)}")  # Should be 100

# ========================
# LINE PLOT — Total Time
# ========================
plt.figure()
plt.plot(range(len(baseline)), sorted(
    baseline["totalTime"]), color="steelblue")
plt.title("Baseline Total Time Growth")
plt.xlabel("Task Index")
plt.ylabel("Time (ms)")
plt.tight_layout()
plt.savefig("baseline_line.png")

# ========================
# LINE PLOT — Waiting Time
# ========================
plt.figure()
plt.plot(range(len(baseline)), sorted(baseline["waitingTime"]), color="tomato")
plt.title("Baseline Waiting Time Growth")
plt.xlabel("Task Index")
plt.ylabel("Time (ms)")
plt.tight_layout()
plt.savefig("baseline_waiting_line.png")

# ========================
# BONUS — Processing Time
# ========================
plt.figure()
plt.plot(range(len(baseline)), baseline["processingTime"], color="seagreen")
plt.title("Baseline Processing Time (Constant)")
plt.xlabel("Task Index")
plt.ylabel("Time (ms)")
plt.tight_layout()
plt.savefig("baseline_processing_line.png")

print("✅ Baseline graphs generated")
