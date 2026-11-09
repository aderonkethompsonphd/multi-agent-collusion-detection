
import pandas as pd

# Load the external behavioural dataset
df = pd.read_parquet(
    "data/cert/feature_matrix_v1.parquet"
)

# Select behavioural features
features = [
    "total_logon_activity",
    "after_hours_activity",
    "http_activity_count",
    "total_emails",
    "file_activity_count",
    "usb_activity_count"
]

# Display descriptive statistics
print("Behavioural feature statistics:")
print(df[features].describe().round(2))

# Count unique users
print("\nNumber of unique users:")
print(df["user"].nunique())

# Inspect time coverage
print("\nDay column type:")
print(df["day"].dtype)

print("\nFirst five day values:")
print(df["day"].head().to_string(index=False))

# Check missing values in selected features
print("\nMissing values:")
print(df[features].isnull().sum())

# Check for negative values
print("\nNegative values:")
print((df[features] < 0).sum())

print("\nCERT exploratory analysis completed!")
