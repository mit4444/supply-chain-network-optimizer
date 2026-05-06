import streamlit as st

# Page title
st.title("Supply Chain Network Optimizer")

# Introduction
st.write("""
Welcome to the Supply Chain Network Optimizer.

This project uses graph algorithms to analyze and optimize
real-world supply chain routes using the DataCo dataset.

Algorithms Used:
- Kahn's Algorithm (Topological Sort)
- Dijkstra's Shortest Path Algorithm
""")

# Project overview
st.header("Project Overview")

st.write("""
This application helps visualize how products move through
a supply chain network and finds the fastest shipping routes
between cities.
""")