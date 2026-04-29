import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import problems

class Node:
    """
    Node class represents a state in the search tree,
    along with its parent and the action taken to reach it.
    """
    def __init__(self, state, parent=None, action=None, heuristic=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.heuristic = heuristic

    @property
    def is_head(self):
        """ True if first node """
        return self.parent is None

    def get_path(self):
        """ Get path from head to current node """
        solution_path = []
        node = self

        while node is not None:
            solution_path.append(node)
            node = node.parent

        return list(reversed(solution_path))

    def show_action(self):
        """ Return a string representation of the action taken to reach this node. """
        if self.action:
            if isinstance(self.action[1], problems.Position):
                action_target = self.action[1].show()
            else:
                action_target = self.action[1]

            return f"{self.action[0]} {action_target}"

        return "Start"

    def show(self):
        action = self.show_action()
        return f"State: {self.state.show()}, Action: {action}, Heuristic: {self.heuristic}"

