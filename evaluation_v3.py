
import pandas as pd
from pathlib import Path
from sklearn.ensemble import IsolationForest
from sklearn.metrics import (
    confusion_matrix,
    classification_report
)

# 1. Load Experiment 3 dataset
df = pd.read_csv("data/synthetic_interactions_v3.csv")

# 2. Select behavioural features
features = [
    "communication_count",
    "action_delay",
    "objective_deviation"
]

# 3. Use early legitimate interactions for training
train_df = df[df["step"] < 300].copy()

# 4. Use later interactions for testing
test_df = df[df["step"] >= 300].copy()

X_train = train_df[features]
X_test = test_df[features]
y_test = test_df["collusion_label"]

# 5. Train Isolation Forest
model = IsolationForest(
    n_estimators=100,
    contamination=0.05,
    random_state=42
)

model.fit(X_train)

# 6. Predict anomalous interactions
predictions = model.predict(X_test)

test_df["predicted_collusion"] = (
    predictions == -1
).astype(int)

# 7. Evaluate the detector
print("Experiment 3: Overlapping Agent Behaviours")

print("\nConfusion Matrix:")
print(confusion_matrix(
    y_test,
    test_df["predicted_collusion"],
    labels=[0, 1]
))

print("\nClassification Report:")
print(classification_report(
    y_test,
    test_df["predicted_collusion"],
    labels=[0, 1],
    zero_division=0
))

# 8. Save evaluation results
Path("results").mkdir(exist_ok=True)

test_df.to_csv(
    "results/evaluation_v3.csv",
    index=False
)

print("\nExperiment 3 evaluation completed!")
