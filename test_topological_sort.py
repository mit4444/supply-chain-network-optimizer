from algorithms.kahn_topological_sort import kahn_topological_sort

# Supply chain DAG
supply_chain_graph = {

    "Supplier": ["Warehouse"],

    "Warehouse": ["Distribution Center"],

    "Distribution Center": ["Customer"],

    "Customer": []
}

# Run Kahn's Algorithm
result = kahn_topological_sort(supply_chain_graph)

# Print result
print("\nTOPOLOGICAL SORT RESULT\n")

if result:
    print(" -> ".join(result))
else:
    print("Cycle detected. Topological sort not possible.")