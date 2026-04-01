import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ========================
# LOAD & CLEAN
# ========================
KEY_COLS = ["totalTime", "waitingTime", "processingTime"]

ai = pd.read_csv("ai_metrics.csv")
baseline = pd.read_csv("baseline_metrics.csv")

for col in KEY_COLS:
    ai[col] = pd.to_numeric(ai[col], errors="coerce")
    baseline[col] = pd.to_numeric(baseline[col], errors="coerce")

# Only drop rows where our key columns are missing
ai = ai.dropna(subset=KEY_COLS)
baseline = baseline.dropna(subset=KEY_COLS)

print(f"AI rows: {len(ai)}, Baseline rows: {len(baseline)}")

# ========================
# 1. LOG SCALE LINE PLOT
# ========================
fig, ax = plt.subplots(figsize=(10, 5))

ax.plot(range(len(ai)), sorted(ai["totalTime"]),
        label="AI", linewidth=2, color="steelblue")
ax.plot(range(len(baseline)), sorted(
    baseline["totalTime"]), label="Baseline", linewidth=2, color="tomato")

ax.set_yscale("log")
ax.set_title("Total Time Comparison (Log Scale)")
ax.set_xlabel("Task Index")
ax.set_ylabel("Time (log ms)")
ax.legend()
ax.grid(True, which="both", linestyle="--", alpha=0.5)

plt.tight_layout()
plt.savefig("1_log_comparison.png", dpi=150)
plt.close()

# ========================
# 2. DUAL Y-AXIS LINE PLOT (handles scale difference cleanly)
# ========================
fig, ax1 = plt.subplots(figsize=(10, 5))

ax2 = ax1.twinx()

ax1.plot(range(len(ai)), sorted(
    ai["totalTime"]), label="AI Total Time", color="steelblue", linewidth=2)
ax2.plot(range(len(baseline)), sorted(
    baseline["totalTime"]), label="Baseline Total Time", color="tomato", linewidth=2, linestyle="--")

ax1.set_xlabel("Task Index")
ax1.set_ylabel("AI Time (ms)", color="steelblue")
ax2.set_ylabel("Baseline Time (ms)", color="tomato")
ax1.tick_params(axis="y", labelcolor="steelblue")
ax2.tick_params(axis="y", labelcolor="tomato")

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

plt.title("Total Time Comparison (Dual Axis)")
plt.tight_layout()
plt.savefig("2_dual_axis_comparison.png", dpi=150)
plt.close()

# ========================
# 3. SPEEDUP GRAPH
# ========================
min_len = min(len(ai), len(baseline))
ai_sorted = np.array(sorted(ai["totalTime"]))[:min_len]
baseline_sorted = np.array(sorted(baseline["totalTime"]))[:min_len]

speedup = baseline_sorted / ai_sorted

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(speedup, color="green", linewidth=2)
ax.axhline(y=speedup.mean(), color="gray", linestyle="--",
           label=f"Mean speedup: {speedup.mean():.2f}x")
ax.set_title("Speedup Factor (Baseline / AI)")
ax.set_xlabel("Task Index")
ax.set_ylabel("Speedup (x)")
ax.legend()
ax.grid(True, linestyle="--", alpha=0.5)

plt.tight_layout()
plt.savefig("3_speedup.png", dpi=150)
plt.close()

# ========================
# 4. GROUPED BAR CHART (all 3 metrics)
# ========================
fig, ax = plt.subplots(figsize=(9, 5))

metrics = KEY_COLS
ai_means = [ai[c].mean() for c in metrics]
baseline_means = [baseline[c].mean() for c in metrics]

x = np.arange(len(metrics))
width = 0.35

bars1 = ax.bar(x - width/2, ai_means, width, label="AI", color="steelblue")
bars2 = ax.bar(x + width/2, baseline_means, width,
               label="Baseline", color="tomato")

ax.set_title("Average Time Metrics: AI vs Baseline")
ax.set_ylabel("Time (ms)")
ax.set_xticks(x)
ax.set_xticklabels(["Total Time", "Waiting Time", "Processing Time"])
ax.legend()
ax.set_yscale("log")  # log scale because of large value differences
ax.grid(True, which="both", linestyle="--", alpha=0.4)

# Add value labels on bars
for bar in bars1 + bars2:
    h = bar.get_height()
    ax.annotate(f"{h:.0f}", xy=(bar.get_x() + bar.get_width()/2, h),
                xytext=(0, 3), textcoords="offset points", ha="center", fontsize=8)

plt.tight_layout()
plt.savefig("4_avg_comparison.png", dpi=150)
plt.close()

# ========================
# TEXT REPORT
# ========================
avg_ai = ai["totalTime"].mean()
avg_baseline = baseline["totalTime"].mean()
avg_wait_ai = ai["waitingTime"].mean()
avg_wait_baseline = baseline["waitingTime"].mean()
avg_proc_ai = ai["processingTime"].mean()
avg_proc_baseline = baseline["processingTime"].mean()
overall_speedup = avg_baseline / avg_ai

with open("analysis.txt", "w") as f:
    f.write("=== PERFORMANCE COMPARISON ===\n\n")
    f.write(
        f"Average Total Time      — AI: {avg_ai:.2f} ms  |  Baseline: {avg_baseline:.2f} ms\n")
    f.write(
        f"Average Waiting Time    — AI: {avg_wait_ai:.2f} ms  |  Baseline: {avg_wait_baseline:.2f} ms\n")
    f.write(
        f"Average Processing Time — AI: {avg_proc_ai:.2f} ms  |  Baseline: {avg_proc_baseline:.2f} ms\n\n")
    f.write(f"Overall Speedup: {overall_speedup:.2f}x\n\n")
    f.write("=== INTERPRETATION ===\n\n")
    f.write("- Baseline shows linear increase in waiting time (sequential execution).\n")
    f.write("- AI architecture processes tasks in parallel using a worker pool.\n")
    f.write("- Waiting time is bounded in the AI system.\n")
    f.write("- Processing time remains ~constant in both systems.\n")
    f.write(
        f"- Overall speedup of {overall_speedup:.2f}x achieved due to parallelism.\n")

print("✅ FINAL GRAPHS + REPORT GENERATED")
