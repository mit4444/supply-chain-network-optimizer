import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

import streamlit as st
import pandas as pd
import networkx as nx

from algorithms.dijkstra_algorithm import dijkstra

# -----------------------------
# PAGE TITLE
# -----------------------------

st.title("Supply Chain Network Optimizer")

st.write("""
This project uses graph algorithms to analyze and optimize
real-world supply chain routes using the DataCo dataset.
""")

# -----------------------------
# LOAD DATA
# -----------------------------

data_path = os.path.join(
    os.path.dirname(__file__),
    "..",
    "data",
    "cleaned_supply_chain_data.csv"
)

df = pd.read_csv(data_path)

# -----------------------------
# CREATE GRAPH
# -----------------------------

G = nx.DiGraph()

for _, row in df.iterrows():

    source = row["Order City"]
    destination = row["Customer City"]
    shipping_time = row["Days for shipping (real)"]

    G.add_edge(
        source,
        destination,
        weight=shipping_time
    )

# -----------------------------
# ROUTE OPTIMIZER SECTION
# -----------------------------

st.header("Route Optimizer")

# Get unique cities
cities = sorted(list(G.nodes()))

# Dropdowns
start_city = st.selectbox(
    "Select Start City",
    cities
)

end_city = st.selectbox(
    "Select Destination City",
    cities
)

# Button
if st.button("Find Shortest Route"):

    path, total_distance = dijkstra(
        G,
        start_city,
        end_city
    )

    # Handle unreachable paths
    if total_distance == float('inf'):

        st.error("No route found between selected cities.")

    else:

        st.success("Route Found!")

        st.write("### Optimal Path")

        st.write(" → ".join(path))

        st.write(f"### Total Shipping Time: {total_distance}")