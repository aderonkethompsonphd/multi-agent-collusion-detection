
import pandas as pd

# Load Experiment 4 results
df = pd.read_csv("results/cert_anomaly_results.csv")

features = [
    "total_logon_activity",
    "after_hours_activity",
    "http_activity_count",
    "total_emails",
    "file_activity_count",
    "usb_activity_count"
]

# Calculate average behaviour by anomaly flag
summary = df.groupby("anomaly_flag")[features].mean()

print("Average behavioural characteristics:")
print(summary.round(2).to_string())

# Count distinct users with flagged activity
flagged = df[df["anomaly_flag"] == 1]

print("\nUsers with at least one flagged observation:")
print(flagged["user"].nunique())

# Find the highest-scoring activity days by selected counts
print("\nFlagged observations with highest file activity:")
print(
    flagged.nlargest(10, "file_activity_count")[
        ["user", "day", "file_activity_count",
         "usb_activity_count", "after_hours_activity"]
    ].to_string(index=False)
)
