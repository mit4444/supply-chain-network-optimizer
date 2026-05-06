from pyvis.network import Network
import streamlit.components.v1 as components
import tempfile
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

        # Display edge weights
        st.write("### Route Breakdown")

        calculated_total = 0

        for i in range(len(path) - 1):
            source = path[i]
            destination = path[i + 1]

            edge_weight = G[source][destination]["weight"]

            calculated_total += edge_weight

            st.write(
                f"{source} → {destination} = {edge_weight} days"
            )

        st.write(f"### Total Shipping Time: {calculated_total} days")

        # -----------------------------
        # ROUTE VISUALIZATION
        # -----------------------------

        st.write("### Route Visualization")

        net = Network(
            height="500px",
            width="100%",
            directed=True
        )

        # Add nodes
        for city in path:
            net.add_node(city, label=city)

        # Add edges
        for i in range(len(path) - 1):

            source = path[i]
            destination = path[i + 1]

            net.add_edge(
                source,
                destination
            )

        # Save graph temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:

            net.save_graph(tmp_file.name)

            html_file = open(tmp_file.name, "r", encoding="utf-8")

            components.html(
                html_file.read(),
                height=550
            )

# ==========================================
# TOPOLOGICAL SORT SECTION
# ==========================================

st.write("---")

st.header("Supply Chain Workflow (Kahn's Algorithm)")

st.write(
    """
This section demonstrates Kahn's Algorithm
(Topological Sorting) to determine the correct
processing order in a supply chain workflow.
"""
)

# Create DAG
workflow_graph = nx.DiGraph()

workflow_graph.add_edges_from([
    ("Supplier", "Warehouse"),
    ("Warehouse", "Distribution Center"),
    ("Distribution Center", "Customer")
])

# Perform topological sort
topological_order = list(nx.topological_sort(workflow_graph))

# Display result
st.write("### Processing Order")

st.write(" → ".join(topological_order))

# ---------------------------------
# VISUALIZE WORKFLOW GRAPH
# ---------------------------------

workflow_net = Network(
    height="400px",
    width="100%",
    directed=True
)

for node in workflow_graph.nodes():
    workflow_net.add_node(node, label=node)

for edge in workflow_graph.edges():
    workflow_net.add_edge(edge[0], edge[1])

with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:

    workflow_net.save_graph(tmp_file.name)

    html_file = open(tmp_file.name, "r", encoding="utf-8")

    components.html(
        html_file.read(),
        height=450
    )