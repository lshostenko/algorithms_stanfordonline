import gzip
import heapq
from collections import defaultdict


class Graph:
    def __init__(self, max_cost=float('inf')):
        self.neighbours = defaultdict(list)
        self.max_cost = max_cost

    def add_edge(self, v1, v2, weight):
        if (weight, v2) not in self.neighbours[v1]:
            self.neighbours[v1].append((weight, v2))

    def dijkstra_shortest_path(self, source):
        seen = set()

        costs = defaultdict(lambda: self.max_cost)
        costs[source] = 0

        vertex_priority = []
        heapq.heappush(vertex_priority, (0, source))

        while vertex_priority:
            _, node = heapq.heappop(vertex_priority)
            seen.add(node)

            for weight, adj_node in self.neighbours[node]:
                if adj_node in seen:
                    continue

                new_cost = costs[node] + weight

                if costs[adj_node] > new_cost:
                    costs[adj_node] = new_cost
                    heapq.heappush(vertex_priority, (new_cost, adj_node))

        return costs


# Programming Assignment 5
if __name__ == '__main__':
    g = Graph(max_cost=1000000)

    with gzip.open('assets/dijkstraData.txt.gz', mode='rt') as fp:
        for line in fp.readlines():
            items = line.split()
            tail = int(items[0])

            for pair in items[1:]:
                head, weight = map(int, pair.split(','))
                g.add_edge(tail, head, weight)

    START = 1
    DESTINATIONS = [7, 37, 59, 82, 99, 115, 133, 165, 188, 197]
    paths = g.dijkstra_shortest_path(START)

    for v in DESTINATIONS:
        print(f'shortest path [{START} -> {v}]:\t{paths[v]}')
