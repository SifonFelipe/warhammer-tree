import math
import random
from itertools import product

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_distance(self, position):
        return abs(self.x - position.x) + abs(self.y - position.y)

    def distance_to(self, other):
        """
        Straight line distance to another position.
        """
        return math.sqrt(
            (self.x - other.x) ** 2
            + (self.y - other.y) ** 2
        )

    def positions_in_range(self, radius):
        """
        Gets the positions that are in range, within a certain radius.
        Yields them in shuffled order.
        """
        # get possible values for x and y in a rectangle around the center, filter out by distance to
        # only use the ones contained by the circle
        x_values = list(range(self.x - radius, self.x + radius + 1))
        y_values = list(range(self.y - radius, self.y + radius + 1))
        coords_combinations = list(product(x_values, y_values))
        random.shuffle(coords_combinations)

        for x, y in coords_combinations:
            position = Position(x, y)
            if position != self and self.distance_to(position) <= radius:
                yield position

    def show(self):
        return f"({self.x}, {self.y})"


