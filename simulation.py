import random 
from pathlib import Path

import pandas as pd

random.seed(42)

agents = ["Agent_A", "Agent_B", "Agents_C"]
records = []

for step in range(200):
  agent = random.choice(agents)
  collusion = step >= 150 and agent in ["Agent_A", "Agent_B"]

  records.append({
    "step": step,
    "agent": agent,
    "communication_count": random.randint(7, 12)
      if collusion else random.randint(1,6),
    "action_delay": round(
      random.uniform(0.1, 0.5)
      if collusion else random.uniform(0.5, 3.0), 2
    ),
    "objective_deviation": round(
      random.uniform(0.6,1.0)
      if collusion else random.uniform(0.0,0.3), 2
    ),
    "collusion_label": int(collusion)
  })
  df = pd.DataFrame(records)

  Path("data").mkdir(exist_ok=True)
  df.to_csv("data/synthetic_interactions.csv", index=False)

  print("Simulation completed successfully!")
  print(df.head())
  print("\nCollusion labels:")
  print(df["collusion_label"].value_counts())