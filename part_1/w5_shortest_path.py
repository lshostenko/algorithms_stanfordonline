import gzip
import heapq
from collections import defaultdict


class Graph:
    def __init__(self, max_cost=float('inf')):
        self.children = defaultdict(list)
        self.max_cost = max_cost

    def add_edge(self, tail, head, weight):
        if (weight, head) not in self.children[tail]:
            self.children[tail].append((weight, head))

    def find_all_shortest_paths(self, start):
        seen = set()

        costs = defaultdict(lambda: self.max_cost)
        costs[start] = 0

        vertex_priority = []
        heapq.heappush(vertex_priority, (0, start))

        while vertex_priority:
            _, node = heapq.heappop(vertex_priority)
            seen.add(node)

            for weight, adj_node in self.children[node]:
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

    start = 1
    destinations = [7, 37, 59, 82, 99, 115, 133, 165, 188, 197]
    paths = g.find_all_shortest_paths(start)

    for v in destinations:
        print(f'shortest path [{start} -> {v}]:\t{paths[v]}')
