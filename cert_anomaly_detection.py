
import pandas as pd
from pathlib import Path
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# 1. Load the external dataset
df = pd.read_parquet(
    "data/cert/feature_matrix_v1.parquet"
)

# 2. Select observable behavioural features
features = [
    "total_logon_activity",
    "after_hours_activity",
    "http_activity_count",
    "total_emails",
    "file_activity_count",
    "usb_activity_count"
]

# 3. Sort chronologically
df = df.sort_values(["day", "user"]).copy()

# 4. Separate earlier and later observations
cutoff = df["day"].quantile(0.70)

train_df = df[df["day"] <= cutoff].copy()
test_df = df[df["day"] > cutoff].copy()

# 5. Prepare numerical features
X_train = train_df[features]
X_test = test_df[features]

# 6. Fit the scaler on training data only
scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 7. Train the anomaly detector
model = IsolationForest(
    n_estimators=100,
    contamination=0.05,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train_scaled)

# 8. Predict anomalies on later observations
predictions = model.predict(X_test_scaled)

test_df["anomaly_flag"] = (
    predictions == -1
).astype(int)

# 9. Calculate the anomaly rate
total = len(test_df)
anomalies = int(test_df["anomaly_flag"].sum())
anomaly_rate = 100 * anomalies / total

print("CERT External Dataset Experiment")
print(f"Training observations: {len(train_df)}")
print(f"Testing observations: {total}")
print(f"Anomalies detected: {anomalies}")
print(f"Anomaly rate: {anomaly_rate:.2f}%")

# 10. Inspect flagged observations
print("\nSample anomalous observations:")
print(
    test_df[test_df["anomaly_flag"] == 1][
        ["user", "day"] + features
    ].head(10).to_string(index=False)
)

# 11. Save results
Path("results").mkdir(exist_ok=True)

test_df.to_csv(
    "results/cert_anomaly_results.csv",
    index=False
)

print("\nCERT anomaly detection completed!")
