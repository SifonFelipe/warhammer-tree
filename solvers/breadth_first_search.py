"""
Breadth-First Search (BFS) explores all the neighbor nodes at the
present depth prior to moving on to the nodes at the next depth level.
This approach ensures that the first solution found is the one with the
least number of steps from the initial state, making it an optimal search
strategy for unweighted problems.
"""
import warnings
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from solver import Solver
from .utils import Node

class BFS_Solver(Solver):
    """
    Solver implements a tree algorithm to find a solution to any given problem.
    It uses the Problem class to define the problem space and the Node class to
    represent states in the search tree.
    Takes as a solution the first node that reaches a winning state (less weight)
    """
    name = "Breadth-First Search"

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

                self.weights.append(new_node)
