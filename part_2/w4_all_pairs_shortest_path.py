import gzip
import heapq
import math
from collections import defaultdict
from itertools import chain
from time import monotonic

import numpy as np


class DiGraph:
    def __init__(self):
        self.edges = {}
        self.vertices = set()
        self.children = defaultdict(list)

    def _dijkstra_single_source(self, source, vertices_weights, edges_weights):
        seen = set()

        costs = defaultdict(lambda: math.inf)
        costs[source] = 0.

        vertex_priority = []
        heapq.heappush(vertex_priority, (0, source))

        while vertex_priority:
            _, vertex = heapq.heappop(vertex_priority)
            seen.add(vertex)

            for child in self.children[vertex]:
                if child in seen:
                    continue

                new_cost = costs[vertex] + edges_weights[(vertex, child)]

                if costs[child] > new_cost:
                    costs[child] = new_cost
                    heapq.heappush(vertex_priority, (new_cost, child))

        result = {}

        for vertex, weight in costs.items():
            weight += vertices_weights[vertex] - vertices_weights[source]

            result[vertex] = weight

        return result

    def _get_adjacency_matrix(self):
        vertices_id = {v: i for i, v in enumerate(self.vertices)}
        vertices = sorted(vertices_id.keys(), key=vertices_id.get)

        adjacency_matrix = np.full((len(vertices), len(vertices)), np.inf)
        np.fill_diagonal(adjacency_matrix, 0)

        for edge, weight in self.edges.items():
            start, end = edge
            adjacency_matrix[vertices_id[start], vertices_id[end]] = weight

        return vertices, adjacency_matrix

    def _get_vertices_weights(self):
        vertices_weights = defaultdict(int)
        updated = False

        for _ in range(len(self.vertices)):
            updated = False

            for edge, weight in self.edges.items():
                start, end = edge

                pivot_weight = vertices_weights[start] + weight

                if pivot_weight < vertices_weights[end]:
                    vertices_weights[end] = pivot_weight
                    updated = True

        if not updated:
            return vertices_weights

    def add_edge(self, parent_node, child_node, weight):
        edge = (parent_node, child_node)
        if edge in self.edges:
            return

        self.edges[edge] = weight
        self.vertices.add(parent_node)
        self.vertices.add(child_node)
        self.children[parent_node].append(child_node)

    def shortest_path_floyd_warshall(self):
        vertices, path_matrix = self._get_adjacency_matrix()

        for ix in range(len(vertices)):
            path_matrix = np.minimum(
                path_matrix,
                path_matrix[np.newaxis, ix, :]
                + path_matrix[:, ix, np.newaxis],
            )

            if np.any(path_matrix.diagonal() != 0):
                return

        result = {}

        for i, source in enumerate(vertices):
            result[source] = {
                vertices[j]: path_matrix[i, j].item()
                for j in range(len(vertices))
                if not np.isinf(path_matrix[i, j])
            }

        return result

    def shortest_path_johnson(self):
        v_weights = self._get_vertices_weights()
        if v_weights is None:
            return

        e_weights = {
            (u, v): weight + v_weights[u] - v_weights[v]
            for (u, v), weight in self.edges.items()
        }

        result = {
            v: self._dijkstra_single_source(v, v_weights, e_weights)
            for v in self.vertices
        }

        return result


def load_graph(filename):
    graph = DiGraph()

    if filename.endswith('.gz'):
        open_file = gzip.open
    else:
        open_file = open

    with open_file(filename, mode='rt') as fp:
        num_vertices, num_edges = map(int, fp.readline().split())

        for line in fp.readlines():
            tail, head, weight = map(int, line.split())
            graph.add_edge(tail, head, weight)

    assert len(graph.vertices) == num_vertices
    assert len(graph.edges) == num_edges

    return graph


if __name__ == '__main__':
    files = (
        ('g1', 'assets/g1.txt.gz'),
        ('g2', 'assets/g2.txt.gz'),
        ('g3', 'assets/g3.txt.gz'),
    )

    for label, filename in files:
        graph = load_graph(filename)

        t0 = monotonic()
        res1 = graph.shortest_path_floyd_warshall()
        t_fw = monotonic() - t0

        t0 = monotonic()
        res2 = graph.shortest_path_johnson()
        t_j = monotonic() - t0

        assert res1 == res2

        if res1 is None:
            result = 'The graphs has negative-cost cycles'
        else:
            result = int(min(chain(min(p.values()) for p in res1.values())))

        print(f'{label}: {result}')
        print(f'timing Floyd Warshall:\t{t_fw:.3f} s')
        print(f'timing Johnson:\t{t_j:.3f} s')
