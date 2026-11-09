import pandas as pd
import matplotlib.pyplot as plt

# Load the simulated agent interaction dataset
df = pd.read_csv("data\synthetic_interactions.csv")

# Display the first five observations
print("First five observation:")
print(df.head())

# Display dataset information
print("\nDataset information:")
df.info()

# Count Legiimate and collusive observations
print("\nBehaviour classsification:")
print(df["collusion_label"].value_counts())

# Compare communication frequency
df.boxplot(
  column="communication_count",
  by="collusion_label"
)

plt.title("Agent Communcation Behaviour")
plt.suptitle("")
plt.xlabel(("Collusion Label (0 = Legitimate, 1 = Collusive)"))
plt.ylabel("Communication Count")
plt.tight_layout()
plt.show()