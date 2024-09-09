from collections import defaultdict

import numpy as np


class DiGraph:
    def __init__(self):
        self.edges = {}
        self.vertices = set()
        self.children = defaultdict(list)

    def add_edge(self, parent_node, child_node, weight):
        edge = (parent_node, child_node)
        if edge in self.edges:
            return

        self.edges[edge] = weight
        self.vertices.add(parent_node)
        self.vertices.add(child_node)
        self.children[parent_node].append(child_node)

    def get_adjacency_matrix(self):
        vertices_id = {v: i for i, v in enumerate(self.vertices)}
        vertices = sorted(vertices_id.keys(), key=vertices_id.get)

        adjacency_matrix = np.full((len(vertices), len(vertices)), np.inf)
        np.fill_diagonal(adjacency_matrix, 0)

        for edge, weight in self.edges.items():
            start, end = edge
            ix_1, ix_2 = vertices_id[start], vertices_id[end]
            adjacency_matrix[ix_1, ix_2] = weight

        return vertices, adjacency_matrix

    def shortest_path_floyd_warshall(self):
        vertices, shortest_paths = self.get_adjacency_matrix()

        for ix in range(len(vertices)):
            shortest_paths = np.minimum(
                shortest_paths,
                shortest_paths[np.newaxis, ix, :]
                + shortest_paths[:, ix, np.newaxis],
            )

            if np.any(shortest_paths.diagonal() != 0):
                return

        result = {}

        for i, source in enumerate(vertices):
            paths_i = {
                vertices[j]: shortest_paths[i, j].item()
                for j in range(len(vertices))
                if i != j and not np.isinf(shortest_paths[i, j])
            }

            if paths_i:
                result[source] = paths_i

        return result
