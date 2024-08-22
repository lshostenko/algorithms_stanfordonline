import gzip
from collections import defaultdict, deque


class Graph:
    def __init__(self):
        self.edges = set()
        self.vertices = set()
        self.children = defaultdict(list)

    def add_edge(self, parent_node, child_node):
        edge = (parent_node, child_node)
        if edge in self.edges:
            return

        self.edges.add(edge)
        self.vertices.add(parent_node)
        self.vertices.add(child_node)
        self.children[parent_node].append(child_node)

    def strongly_connected_components(self):
        g_t = self.transpose()
        ordered_vertices = g_t._order_vertices()
        return self._group_connected_vertices(ordered_vertices)

    def transpose(self):
        transposed = Graph()

        for i, j in self.edges:
            transposed.add_edge(j, i)

        return transposed

    def _dfs_visit(self, vertex, seen, finishing_times, timestep=None):
        if timestep is None:
            if finishing_times:
                timestep = max(finishing_times.values()) + 1
            else:
                timestep = 0

        stack = deque([vertex])

        while stack:
            v = stack[-1]

            if v in seen:
                v = stack.pop()
                if v not in finishing_times:
                    finishing_times[v] = timestep
                    timestep += 1
            else:
                seen.add(v)
                stack.extend(
                    child for child in self.children[v]
                    if child not in seen
                )

        return timestep

    def _group_connected_vertices(self, ordered_vertices):
        result = []
        seen = set()

        for vertex in ordered_vertices:
            if vertex in seen:
                continue

            finishing_times = {}
            self._dfs_visit(vertex, seen, finishing_times)
            result.append(tuple(finishing_times.keys()))

        return result

    def _order_vertices(self):
        timestep = 0
        finishing_times = {}
        seen = set()

        for vertex in self.vertices:
            if vertex in seen:
                continue

            timestep = self._dfs_visit(
                vertex,
                seen,
                finishing_times,
                timestep=timestep,
            )

        ordered_vertices = sorted(
            finishing_times.keys(),
            key=finishing_times.get,
            reverse=True,
        )

        return ordered_vertices


# Programming Assignment 4
if __name__ == '__main__':
    g = Graph()

    with gzip.open('assets/SCC.txt.gz', mode='rt') as fp:
        for line in fp.readlines():
            i, v = line.split()
            i, v = int(i), int(v)
            g.add_edge(i, v)

        res = g.strongly_connected_components()
        lengths = sorted((len(i) for i in res), reverse=True)
        labels = (
            'largest SCC',
            '2nd largest SCC',
            '3rd largest SCC',
            '4th largest SCC',
            '5th largest SCC',
        )

        for label, length in zip(labels, lengths[:5]):
            print(f'{label}:\t{length}')
