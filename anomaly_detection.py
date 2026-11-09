import  pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.metrics import classification_report, confusion_matrix

# Load our synthetic dataset
df  = pd.read_csv("data\synthetic_interactions.csv")
print("Available columns:")
print(df.columns.tolist())

# Select behavioural features
features = [
  "communication_count",
  "action_delay",
  "objective_deviation"
]

x = df[features]

# Train on unsupervised anolamy detection model
model = IsolationForest(
  n_estimators=100,
  contamination=0.1,
  random_state=42
)

model.fit(x)

#Predict anomalies
predictions = model.predict(x)

#Convert prediction to binary labels
# Isolation Forest: -1 = anomaly, 1 = normal
df["predicted_collusion"] = [
  1 if prediction  == -1 else 0
  for prediction in predictions
]

# Evaluate against known simulation labels
print ("Confusion Matrix:")
print(confusion_matrix(
  df["collusion_label"],
  df["predicted_collusion"]
))

print("\nClassification report:")
print(classification_report(
  df["collusion_label"],
  df["predicted_collusion"],
  zero_division=0
))

# Save results
df.to_csv("data/detection_results.csv", index=False)

print("\nDetection results saved successfully!")