import math
from collections import defaultdict


class DiGraph:
    def __init__(self):
        self.edges = defaultdict(math.inf)
        self.vertices = set()
        self.children = defaultdict(list)
        self.parents = defaultdict(list)

    def add_edge(self, parent_node, child_node, weight):
        edge = (parent_node, child_node)
        if edge in self.edges:
            return

        self.edges[edge] = weight
        self.vertices.add(parent_node)
        self.vertices.add(child_node)
        self.children[parent_node].append(child_node)
        self.parents[child_node].append(parent_node)
