
import pandas as pd

df = pd.read_csv("results/cert_anomaly_results.csv")

# Select one user
user_id = "AJF0370"
user_data = df[df["user"] == user_id].copy()

# Sort chronologically
user_data["day"] = pd.to_datetime(user_data["day"])
user_data = user_data.sort_values("day")

print("User:", user_id)
print("Total test observations:", len(user_data))
print("Flagged observations:", user_data["anomaly_flag"].sum())

print("\nAverage behaviour:")
print(
    user_data[
        [
            "file_activity_count",
            "usb_activity_count",
            "after_hours_activity"
        ]
    ].mean().round(2)
)

print("\nFirst 10 chronological observations:")
print(
    user_data[
        [
            "day",
            "file_activity_count",
            "usb_activity_count",
            "after_hours_activity",
            "anomaly_flag"
        ]
    ].head(10).to_string(index=False)
)

print("\nLast 10 chronological observations:")
print(
    user_data[
        [
            "day",
            "file_activity_count",
            "usb_activity_count",
            "after_hours_activity",
            "anomaly_flag"
        ]
    ].tail(10).to_string(index=False)
)

