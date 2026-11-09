import random
from pathlib import Path
import pandas as pd

# Make the simulation reproducible
random.seed(42)

agents = ["Agent_A", "Agent_B", "Agent_C"]
records = []


# Generate 500 agent-to-agent interactions
for step in range(500):

  sender, receiver = random.sample(agents, 2)

  # Introduce a collusion scenario in later steps
  collusion = (
    step >= 350
    and set([sender, receiver])
    == {"Agent_A", "Agent_B"}
  )

  # Some legitimate interactions are also intensive
  intensive = random.random() < 0.20

  if collusion:
    communication_count = random.randint(4, 10)
    action_delay = random.uniform(0.20, 2.0)
    objective_deviation = random.uniform(0.3, 0.8)

  elif intensive:
        communication_count = random.randint(5, 10)
        action_delay = random.uniform(0.2, 1.5)
        objective_deviation = random.uniform(0.1, 0.5)

  else:
        communication_count = random.randint(1, 6)
        action_delay = random.uniform(0.5, 3.0)
        objective_deviation = random.uniform(0.0, 0.3)  

  records.append({
      "step": step,
      "sender": sender,
      "receiver": receiver,
      "communication_count": communication_count,
      "action_delay": round(action_delay, 2),
      "objective_deviation": round(
          objective_deviation, 2
      ),
      "collusion_label": int(collusion)
  })

  # Convert interaction into a dataset
  df = pd.DataFrame(records)

  # Save the synthetic interaction records
  Path("data").mkdir(exist_ok=True)

  df.to_csv(
      "data/synthetic_interactions_v3.csv",
      index=False
  )

print("Experiment 3 simulation completed!")
print("\nFirst five interactons:")
print(df.head())

print("\nBehaviour classification:")
print(df["collusion_label"].value_counts())

print("\nAgent communication pairs:")
print(df.groupby(
    ["sender", "receiver"]
).size())