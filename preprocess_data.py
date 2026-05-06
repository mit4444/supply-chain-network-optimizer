import pandas as pd

# Load dataset
df = pd.read_csv(
    "data/DataCoSupplyChainDataset.csv",
    encoding="latin1"
)

# Select only useful columns
selected_columns = [
    "Order City",
    "Customer City",
    "Order Country",
    "Customer Country",
    "Days for shipping (real)",
    "Sales per customer",
    "Order Item Total",
    "Shipping Mode",
    "Delivery Status"
]

clean_df = df[selected_columns]

# Remove missing values
clean_df = clean_df.dropna()

# Remove duplicate rows
clean_df = clean_df.drop_duplicates()

# Keep only first 5000 rows for performance
clean_df = clean_df.head(5000)

# Save cleaned dataset
clean_df.to_csv("data/cleaned_supply_chain_data.csv", index=False)

# Print summary
print("\nCLEANED DATASET CREATED SUCCESSFULLY\n")

print("Shape:")
print(clean_df.shape)

print("\nFirst 5 rows:\n")
print(clean_df.head())
