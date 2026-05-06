from pyvis.network import Network
import streamlit.components.v1 as components
import tempfile
import sys
import os

# ==========================================
# PROJECT IMPORT PATH
# ==========================================

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

# ==========================================
# IMPORTS
# ==========================================

import streamlit as st
import pandas as pd
import networkx as nx

from algorithms.dijkstra_algorithm import dijkstra

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Supply Chain Network Optimizer",
    layout="wide"
)

# ==========================================
# LOAD DATA
# ==========================================

data_path = os.path.join(
    os.path.dirname(__file__),
    "..",
    "data",
    "cleaned_supply_chain_data.csv"
)

df = pd.read_csv(data_path)

# ==========================================
# CREATE GRAPH
# ==========================================

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

# ==========================================
# PAGE TITLE
# ==========================================

st.title("Supply Chain Network Optimizer")

st.write("""
This project uses graph algorithms to analyze and optimize
real-world supply chain routes using the DataCo dataset.

Algorithms Used:
- Dijkstra’s Shortest Path Algorithm
- Kahn’s Topological Sort Algorithm
""")

# ==========================================
# DATASET STATISTICS
# ==========================================

st.subheader("Dataset Statistics")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Shipment Records",
    f"{len(df):,}"
)

col2.metric(
    "Cities in Network",
    f"{G.number_of_nodes():,}"
)

col3.metric(
    "Shipping Routes",
    f"{G.number_of_edges():,}"
)

st.write("---")

# ==========================================
# ROUTE OPTIMIZER
# ==========================================

st.header("Route Optimizer")

st.write("""
Select two cities to find the shortest shipping route
using Dijkstra’s Algorithm.
""")

# ------------------------------------------
# CITY SELECTION
# ------------------------------------------

cities = sorted(list(G.nodes()))

col1, col2 = st.columns(2)

with col1:
    start_city = st.selectbox(
        "Select Start City",
        cities
    )

with col2:
    end_city = st.selectbox(
        "Select Destination City",
        cities
    )

# ------------------------------------------
# FIND ROUTE BUTTON
# ------------------------------------------

if st.button("Find Shortest Route"):

    path, total_distance = dijkstra(
        G,
        start_city,
        end_city
    )

    # --------------------------------------
    # NO PATH FOUND
    # --------------------------------------

    if total_distance == float('inf'):

        st.error(
            "No valid shipping route found between selected cities."
        )

    # --------------------------------------
    # PATH FOUND
    # --------------------------------------

    else:

        st.success("Optimal Route Found!")

        # ----------------------------------
        # PATH DISPLAY
        # ----------------------------------

        st.write("### Optimal Path")

        st.write(" → ".join(path))

        # ----------------------------------
        # ROUTE BREAKDOWN
        # ----------------------------------

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

        st.write(
            f"### Total Shipping Time: {calculated_total} days"
        )

        # ----------------------------------
        # ROUTE VISUALIZATION
        # ----------------------------------

        st.write("### Route Visualization")

        net = Network(
            height="500px",
            width="100%",
            directed=True
        )

        # Hierarchical layout
        net.set_options("""
        var options = {
          "layout": {
            "hierarchical": {
              "enabled": true,
              "direction": "LR",
              "sortMethod": "directed"
            }
          },
          "physics": {
            "enabled": false
          }
        }
        """)

        # Add nodes
        for city in path:
            net.add_node(
                city,
                label=city
            )

        # Add edges
        for i in range(len(path) - 1):

            source = path[i]
            destination = path[i + 1]

            edge_weight = G[source][destination]["weight"]

            net.add_edge(
                source,
                destination,
                label=f"{edge_weight} days"
            )

        # Render visualization
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".html"
        ) as tmp_file:

            net.save_graph(tmp_file.name)

            html_file = open(
                tmp_file.name,
                "r",
                encoding="utf-8"
            )

            components.html(
                html_file.read(),
                height=550
            )

# ==========================================
# TOPOLOGICAL SORT SECTION
# ==========================================

st.write("---")

st.header("Supply Chain Dependency Workflow")

st.write("""
This section demonstrates Kahn’s Algorithm
(Topological Sorting) to determine the correct
dependency order of operations in a real-world
supply chain process.
""")

# ==========================================
# CREATE WORKFLOW DAG
# ==========================================

workflow_graph = nx.DiGraph()

workflow_graph.add_edges_from([

    ("Order Received", "Inventory Check"),

    ("Inventory Check", "Supplier Processing"),

    ("Supplier Processing", "Warehouse Packaging"),

    ("Warehouse Packaging", "Regional Distribution"),

    ("Regional Distribution", "Local Delivery Hub"),

    ("Local Delivery Hub", "Customer Delivery"),

    ("Customer Delivery", "Order Completed")
])

# ==========================================
# TOPOLOGICAL SORT
# ==========================================

topological_order = list(
    nx.topological_sort(workflow_graph)
)

st.write("### Processing Order")

st.write(" → ".join(topological_order))

# ==========================================
# WORKFLOW VISUALIZATION
# ==========================================

workflow_net = Network(
    height="400px",
    width="100%",
    directed=True
)

workflow_net.set_options("""
var options = {
  "layout": {
    "hierarchical": {
      "enabled": true,
      "direction": "LR",
      "sortMethod": "directed"
    }
  },
  "physics": {
    "enabled": false
  }
}
""")

# Add workflow nodes
for node in workflow_graph.nodes():

    workflow_net.add_node(
        node,
        label=node
    )

# Add workflow edges
for edge in workflow_graph.edges():

    workflow_net.add_edge(
        edge[0],
        edge[1]
    )

# Render workflow graph
with tempfile.NamedTemporaryFile(
    delete=False,
    suffix=".html"
) as tmp_file:

    workflow_net.save_graph(tmp_file.name)

    html_file = open(
        tmp_file.name,
        "r",
        encoding="utf-8"
    )

    components.html(
        html_file.read(),
        height=450
    )