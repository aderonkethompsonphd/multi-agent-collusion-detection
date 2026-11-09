
from pathlib import Path
import pandas as pd

# Locate the downloaded dataset
file_path = Path("data/cert/feature_matrix_v1.parquet")

# Check that the file exists
if not file_path.exists():
    raise FileNotFoundError(
        f"Dataset not found: {file_path}"
    )

# Load the dataset
df = pd.read_parquet(file_path)

# Display its dimensions
print("Dataset shape:")
print(df.shape)

# Display column names
print("\nAvailable columns:")
print(df.columns.tolist())

# Display the first five observations
print("\nFirst five observations:")
print(df.head().to_string())

# Examine data types
print("\nData types:")
print(df.dtypes)

# Identify missing values
print("\nMissing values:")
print(df.isnull().sum().to_string())

print("\nDataset inspection completed!")
