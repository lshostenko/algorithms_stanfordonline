from collections import defaultdict

import numpy as np


class DiGraph:
    def __init__(self):
        self.edges = {}
        self.vertices = set()
        self.children = defaultdict(list)

    def _dijkstra_single_source(self, vertices_weights):
        raise NotImplementedError

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
        raise NotImplementedError

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
            shortest_path = {
                vertices[j]: path_matrix[i, j].item()
                for j in range(len(vertices))
                if i != j and not np.isinf(path_matrix[i, j])
            }

            if shortest_path:
                result[source] = shortest_path

        return result

    def shortest_path_johnson(self):
        raise NotImplementedError
