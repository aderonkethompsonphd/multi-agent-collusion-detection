import pandas as pd
from pathlib import Path
from sklearn.ensemble import IsolationForest 
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
  classification_report,
  confusion_matrix
)  

# 1. Load the synthetic dataset
df = pd.read_csv("data/synthetic_interactions.csv")

# 2. Select the behavioural features
features = [
  "communication_count",
  "action_delay",
  "objective_deviation"
]

# 3. Separate Legitimate and collusive observations
legitimate = df[df["collusion_label"] == 0]
collusive = df[df["collusion_label"] == 1]

# 4. Split legitimate observation into training and testing
train_normal, test_normal = train_test_split(
  legitimate,
  test_size=0.30,
  random_state=42
)

# 5. Create a test set containing both behaviour classes 
test_df = pd.concat(
  [test_normal, collusive],
  ignore_index=True
)

# 6. Prepare the model inputs
x_train = train_normal[features]
x_test = test_df[features]
y_test = test_df["collusion_label"]

# 7. Train on legiimate behaviour only
model = IsolationForest(
  n_estimators=100,
  contamination=0.05,
  random_state=42
)

model.fit(x_train)

# 8. Predict anomalies in the test set
predictions = model.predict(x_test)

# 9. Convert predictions to binary labels
test_df["predicted_collusion"] = (
  predictions == -1
).astype(int)

# 10. Evaluate the model
print("Experiment 2: Legitimate-only training")
print("\nConfusion_matrix:")
print(confusion_matrix(
  y_test,
  test_df["predicted_collusion"],
  labels=[0,1]
))

print("\nClassification Report:")
print(classification_report(
  y_test,
  test_df["predicted_collusion"],
  labels=[0,1],
  zero_division=0
))

# 11. Save the results
Path("results").mkdir(exist_ok=True)

test_df.to_csv(
  "results/evaluation_v2.csv",
  index=False
  )

print('\nExperiment 2 completed successfully!')