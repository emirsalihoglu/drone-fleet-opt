# src/utils/graph.py

import math

class Graph:
    """
    Represents a weighted undirected graph for delivery routing.
    """

    def __init__(self):
        # Dictionary: node_id -> list of (neighbor_id, cost)
        self.adjacency_list = {}

    def add_node(self, node_id: int):
        """
        Adds a node to the graph.
        """
        if node_id not in self.adjacency_list:
            self.adjacency_list[node_id] = []

    def add_edge(self, from_node: int, to_node: int, cost: float):
        """
        Adds a bidirectional (undirected) edge with cost between two nodes.
        """
        self.adjacency_list[from_node].append((to_node, cost))
        self.adjacency_list[to_node].append((from_node, cost))

    def get_neighbors(self, node_id: int):
        """
        Returns the list of (neighbor_id, cost) for a given node.
        """
        return self.adjacency_list.get(node_id, [])

    @staticmethod
    def euclidean_distance(pos1: tuple, pos2: tuple) -> float:
        """
        Calculates the Euclidean distance between two coordinate points.
        """
        return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)

    def __repr__(self):
        return f"<Graph nodes={len(self.adjacency_list)}>"