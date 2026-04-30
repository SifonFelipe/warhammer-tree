import math
import random
from itertools import product

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_distance(self, other):
        return max(abs(self.x - other.x), abs(self.y - other.y))

    def chebyshev_distance(self, other):
        return max(abs(self.x - other.x), abs(self.y - other.y))

    def positions_in_range(self, distance):
        return [
            Position(self.x + dx, self.y + dy)
            for dx in range(-distance, distance + 1)
            for dy in range(-distance, distance + 1)
            if 0 < max(abs(dx), abs(dy)) <= distance
        ]

    def distance_to(self, other):
        """
        Straight line distance to another position.
        """
        return int(math.sqrt(
            (self.x - other.x) ** 2
            + (self.y - other.y) ** 2
        ))

    def show(self):
        return f"({self.x}, {self.y})"


