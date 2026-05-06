import pandas as pd
import networkx as nx

# Load cleaned dataset
df = pd.read_csv("data/cleaned_supply_chain_data.csv")

# Create directed graph
G = nx.DiGraph()

# Add edges
for _, row in df.iterrows():

    source = row["Order City"]
    destination = row["Customer City"]
    shipping_time = row["Days for shipping (real)"]

    # Add edge with weight
    G.add_edge(
        source,
        destination,
        weight=shipping_time
    )

# Print graph information
print("\nGRAPH CREATED SUCCESSFULLY\n")

print(f"Number of nodes: {G.number_of_nodes()}")
print(f"Number of edges: {G.number_of_edges()}")

print("\nSample edges:\n")

# Print first 10 edges
for edge in list(G.edges(data=True))[:10]:
    print(edge)