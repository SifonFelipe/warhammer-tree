import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from solver import Solver
from .utils import Node

class AStar_Solver(Solver):
    """
    A* Search is a best-first search algorithm that uses a heuristic to estimate the cost of reaching the goal from a given node.
    It combines the actual cost from the start node to the current node with the estimated cost from the current node to the goal.
    This allows it to prioritize nodes that are likely to lead to a solution more quickly.
    """

    name = "A* Search"

    def create_node(self, state, parent=None, action=None):
        return Node(state=state, parent=parent, action=action)

    def run(self):
        nodes_checked = 0

        self.switch_timer()  # Start timer

        if self.solved:
            return self.found_solution(self.initial_node, nodes_checked)

        while True:
            parent_node = self.weights.pop(0)

            state = parent_node.state
            actions = self.problem.get_actions(state)

            for action in actions:
                new_state = self.problem.apply_action(state, action)
                new_node = self.create_node(new_state, parent=parent_node, action=action)

                nodes_checked += 1
                if self.problem.check_win(new_state):
                    return self.found_solution(new_node, nodes_checked)
