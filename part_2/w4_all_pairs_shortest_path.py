import heapq
import math
from collections import defaultdict

import numpy as np


class DiGraph:
    def __init__(self):
        self.edges = {}
        self.vertices = set()
        self.children = defaultdict(list)

    def _dijkstra_single_source(self, source, vertices_weights):
        seen = set()
        reweighted_edges = {
            (u, v): weight + vertices_weights[u] - vertices_weights[v]
            for (u, v), weight in self.edges.items()
        }
        costs = defaultdict(lambda: math.inf)
        costs[source] = 0

        vertex_priority = []
        heapq.heappush(vertex_priority, (0, source))

        while vertex_priority:
            _, vertex = heapq.heappop(vertex_priority)
            seen.add(vertex)

            for child in self.children[vertex]:
                if child in seen:
                    continue

                new_cost = costs[vertex] + reweighted_edges[(vertex, child)]

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
        raise NotImplementedError
