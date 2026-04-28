"""
Depth first search implementation for solving problems defined
in the 'problems' module.
"""
import random
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from solver import Solver
from .utils import Node

class DFS_Search(Solver):
    """
    Depth-First Search (DFS) explores as far as possible along each branch before backtracking.
    This approach can be more memory-efficient than BFS, as it doesn't need to store all nodes at
    """

    name = "Depth-First Search"

    def create_node(self, state, parent=None, action=None):
        return Node(state=state, parent=parent, action=action)

    def run(self):
        nodes_checked = 0

        self.switch_timer()  # Start timer

        if self.solved:
            return self.found_solution(self.initial_node, nodes_checked)

        while True:
            parent_node = self.weights.pop()  # Pop the last one
            state = parent_node.state
            actions = self.problem.get_actions(state)

            # Shuffle actions to add some randomness to the search
            random.shuffle(actions)

            for action in actions:
                new_state = self.problem.apply_action(state, action)
                new_node = self.create_node(new_state, parent=parent_node, action=action)

                nodes_checked += 1
                if self.problem.check_win(new_state):
                    return self.found_solution(new_node, nodes_checked)

                self.weights.append(new_node)
