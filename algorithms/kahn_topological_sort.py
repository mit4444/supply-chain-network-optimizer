from collections import deque


def kahn_topological_sort(graph):

    # Calculate in-degrees
    in_degree = {node: 0 for node in graph}

    for node in graph:
        for neighbor in graph[node]:
            in_degree[neighbor] += 1

    # Queue for nodes with in-degree 0
    queue = deque()

    for node in in_degree:
        if in_degree[node] == 0:
            queue.append(node)

    topological_order = []

    while queue:

        current = queue.popleft()
        topological_order.append(current)

        # Reduce in-degree of neighbors
        for neighbor in graph[current]:

            in_degree[neighbor] -= 1

            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # Detect cycle
    if len(topological_order) != len(graph):
        return None

    return topological_order