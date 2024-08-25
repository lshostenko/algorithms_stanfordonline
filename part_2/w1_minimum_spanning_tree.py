import gzip
import heapq
from collections import defaultdict, deque

from scipy.cluster.hierarchy import DisjointSet


class Graph:
    def __init__(self):
        self.edges = {}
        self.vertices = defaultdict(set)

    def __eq__(self, other):
        if not isinstance(other, Graph):
            return False

        return self.edges == other.edges and self.vertices == other.vertices

    def _edge_weight(self, v1, v2):
        if (v1, v2) in self.edges:
            return self.edges[(v1, v2)]

        return self.edges[(v2, v1)]

    def add_edge(self, v1, v2, weight):
        if v1 == v2:
            return

        edge = tuple(sorted([v1, v2]))

        # override if edge is already in the graph
        self.edges[edge] = weight
        self.vertices[v1].add(v2)
        self.vertices[v2].add(v1)

    def calculate_total_weight(self):
        if self.edges:
            return sum(self.edges.values())

        raise ValueError('The graph must contain at least one edge.')

    def is_connected(self):
        seen = set()
        vertex = next(iter(self.vertices.keys()))
        stack = deque([vertex])

        while stack:
            v = stack.pop()

            if v not in seen:
                seen.add(v)
                stack.extend(
                    neighbour for neighbour in self.vertices[v]
                    if neighbour not in seen
                )

        return seen == self.vertices.keys()

    def minimum_spanning_tree_prim(self):
        if not self.is_connected():
            return

        mst = Graph()

        vertex = next(iter(self.vertices.keys()))
        vertex_priority = []

        for neighbour in self.vertices[vertex]:
            weight = self._edge_weight(vertex, neighbour)
            item = (weight, vertex, neighbour)
            heapq.heappush(vertex_priority, item)

        while vertex_priority:
            if len(mst.vertices) == len(self.vertices):
                break

            weight, v1, v2 = heapq.heappop(vertex_priority)

            if v2 not in mst.vertices:
                mst.add_edge(v1, v2, weight)

            for v_next in self.vertices[v2]:
                if v_next in mst.vertices:
                    continue

                w_next = self._edge_weight(v2, v_next)
                heapq.heappush(vertex_priority, (w_next, v2, v_next))

        return mst

    def minimum_spanning_tree_kruskal(self):
        mst = Graph()

        unionfind = DisjointSet(self.vertices.keys())

        for v1, v2 in sorted(self.edges.keys(), key=self.edges.get):
            if not unionfind.connected(v1, v2):
                unionfind.merge(v1, v2)
                mst.add_edge(v1, v2, self.edges[(v1, v2)])

        return mst


# Programming Assignment 1 - Question 3
if __name__ == '__main__':
    graph = Graph()

    with gzip.open('assets/edges.txt.gz', mode='rt') as fp:
        number_of_nodes, number_of_edges = map(int, fp.readline().split())

        for line in fp.readlines():
            v1, v2, weight = map(int, line.split())
            graph.add_edge(v1, v2, weight)

    assert len(graph.vertices) == number_of_nodes
    assert len(graph.edges) == number_of_edges

    mst_prim = graph.minimum_spanning_tree_prim()
    print(mst_prim.calculate_total_weight())

    mst_kruskal = graph.minimum_spanning_tree_kruskal()
    assert mst_kruskal == mst_prim
