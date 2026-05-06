import pandas as pd
import networkx as nx

from algorithms.dijkstra_algorithm import dijkstra

# Load cleaned dataset
df = pd.read_csv("data/cleaned_supply_chain_data.csv")

# Create graph
G = nx.DiGraph()

# Add edges
for _, row in df.iterrows():

    source = row["Order City"]
    destination = row["Customer City"]
    shipping_time = row["Days for shipping (real)"]

    G.add_edge(
        source,
        destination,
        weight=shipping_time
    )

# Example cities
start_city = "Bikaner"
end_city = "San Jose"

# Run Dijkstra
path, total_distance = dijkstra(
    G,
    start_city,
    end_city
)

# Print results
print("\nSHORTEST PATH RESULT\n")

print(f"Start City: {start_city}")
print(f"End City: {end_city}")

print("\nOptimal Path:")
print(" -> ".join(path))

print(f"\nTotal Shipping Time: {total_distance}")