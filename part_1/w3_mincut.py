import gzip
import math
import random
from collections import Counter
from time import monotonic


class Graph:
    def __init__(self, adjacency_list):
        self.vertices = {}

        for values in adjacency_list:
            self.vertices[values[0]] = Counter(values[1:])

        self._update_edges()

    def contract(self):
        while len(self.vertices) > 2:
            v1, v2 = random.choice(self.edges)
            self.merge_vertices(v1, v2)

    def merge_vertices(self, v1, v2):
        '''
        Removes 'v2' from the graph, reassigning all its connections to 'v1.'
        'v1' and 'v2' should be connected
        '''
        if (
            v1 not in self.vertices
            or v2 not in self.vertices
            or v1 not in self.vertices[v2]
        ):
            return

        # remove the edge between 'v1' and 'v2' to avoid self loops
        del self.vertices[v2][v1]
        del self.vertices[v1][v2]

        # reassign the connections to 'v1'
        deleted = self.vertices.pop(v2)
        self.vertices[v1].update(deleted)

        # update all the neighboring vertices of the deleted vertex 'v2'
        for neighbor in deleted:
            self.vertices[neighbor][v1] += self.vertices[neighbor].pop(v2)

        self._update_edges()

    def _update_edges(self):
        self.edges = []

        for vertex, destination_counts in self.vertices.items():
            self.edges.extend(
                (vertex, dest)
                for dest in destination_counts.keys()
                for _ in range(destination_counts[dest])
                if vertex < dest
            )


def load_adjacency_list(filename):
    adjacency_list = []

    if filename.endswith('.gz'):
        open_file = gzip.open
    else:
        open_file = open

    with open_file(filename, mode='rt') as fp:
        for row in fp.readlines():
            adjacency_list.append([int(item) for item in row.split()])

    return adjacency_list


def randomized_mincut(adjacency_list, num_iter=None, silent=True):
    n = len(adjacency_list)
    min_cut = n * (n - 1) // 2

    if num_iter is None:
        num_iter = int(n * (n - 1) * math.log(n) / 2)

    for i in range(num_iter):
        t0 = monotonic()

        graph = Graph(adjacency_list)
        graph.contract()

        min_cut = min(len(graph.edges), min_cut)

        if not silent:
            print(
                f'Iteration {i}:\t'
                f'current min_cut {len(graph.edges)}\t'
                f'total min_cut {min_cut}\t'
                f'iteration timing: {monotonic() - t0:.3f} s'
            )

    return min_cut


# Programming Assignment 3
if __name__ == '__main__':
    adjacency_list = load_adjacency_list('assets/kargerMinCut.txt.gz')
    NUM_ITER = 100

    t0 = monotonic()

    min_cut = randomized_mincut(
        adjacency_list,
        num_iter=NUM_ITER,
        silent=False,
    )

    print(f'min_cut after {NUM_ITER} trials: {min_cut}')
    print(f'timing: {monotonic() - t0:.2f} s')
