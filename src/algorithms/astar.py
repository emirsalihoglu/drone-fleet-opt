# src/algorithms/astar.py

import heapq
from src.utils.graph import Graph

class AStar:
    """
    Implements the A* pathfinding algorithm on a weighted graph.
    """

    def __init__(self, graph: Graph, node_positions: dict):
        """
        :param graph: The Graph object containing nodes and weighted edges
        :param node_positions: Dictionary mapping node_id to (x, y) coordinates
        """
        self.graph = graph
        self.positions = node_positions  # Needed for heuristic calculation

    def heuristic(self, current: int, goal: int) -> float:
        """
        Heuristic: Euclidean distance from current to goal
        """
        return self.graph.euclidean_distance(self.positions[current], self.positions[goal])

    def find_path(self, start: int, goal: int) -> tuple:
        """
        Finds the optimal path from start to goal using A*.

        :return: (total_cost, path_list) if path found, else (float('inf'), [])
        """
        open_set = []
        heapq.heappush(open_set, (0, start))

        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}

        while open_set:
            _, current = heapq.heappop(open_set)

            if current == goal:
                return g_score[current], self.reconstruct_path(came_from, current)

            for neighbor, cost in self.graph.get_neighbors(current):
                tentative_g = g_score[current] + cost

                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + self.heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return float('inf'), []

    def reconstruct_path(self, came_from: dict, current: int) -> list:
        """
        Reconstructs the path from the came_from map.
        """
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path