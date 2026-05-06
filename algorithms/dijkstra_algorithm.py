import heapq


def dijkstra(graph, start, end):

    # Priority queue
    queue = [(0, start)]

    # Distance dictionary
    distances = {node: float('inf') for node in graph.nodes()}
    distances[start] = 0

    # Previous node tracker
    previous_nodes = {}

    while queue:

        current_distance, current_node = heapq.heappop(queue)

        # Stop if destination reached
        if current_node == end:
            break

        # Explore neighbors
        for neighbor in graph.neighbors(current_node):

            weight = graph[current_node][neighbor]['weight']
            distance = current_distance + weight

            # Shorter path found
            if distance < distances[neighbor]:

                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node

                heapq.heappush(queue, (distance, neighbor))

    # Reconstruct path
    path = []

    current = end

    while current in previous_nodes:
        path.insert(0, current)
        current = previous_nodes[current]

    path.insert(0, start)

    return path, distances[end]