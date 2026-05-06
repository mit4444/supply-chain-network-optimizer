import pandas as pd

# Load dataset
df = pd.read_csv("data/DataCoSupplyChainDataset.csv", encoding="latin1")

# Display basic information
print("\nFIRST 5 ROWS:\n")
print(df.head())

print("\nDATASET SHAPE:\n")
print(df.shape)

print("\nCOLUMN NAMES:\n")
print(df.columns.tolist())