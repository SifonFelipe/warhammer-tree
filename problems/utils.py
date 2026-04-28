import math

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_distance(self, position):
        return math.sqrt(
            (self.x - position.x) ** 2
            + (self.y - position.y) ** 2
        )

    def show(self):
        return f"({self.x}, {self.y})"


