import time
import warnings
from abc import ABC, abstractmethod

class Solver(ABC):
    """ Abstract base class for a solver that implements a search algorithm. """

    name = str

    def __init__(self, problem):
        self.problem = problem
        self.initial_node = self.create_node(problem.initial_state)

        self.solved = self.problem.check_win(self.initial_node.state)
        self.weights = [self.initial_node]

        self.nodes_checked = 0
        self.solution_node = None

        self.timer_switch = False
        self.start_time = 0
        self.end_time = 0
        self.elapsed_time = 0

    def switch_timer(self):
        """ Start or stop the timer and return the elapsed time. """
        # If paused or not started, start the timer
        if not self.timer_switch:
            self.timer_switch = True
            self.start_time = time.time()

        self.timer_switch = False
        self.end_time = time.time()
        self.elapsed_time = self.end_time - self.start_time

    def found_solution(self, solution_node, nodes_checked):
        """ Set the solution node and the number of nodes checked. """
        self.solution_node = solution_node
        self.nodes_checked = nodes_checked
        self.switch_timer()

        return solution_node, nodes_checked

    @abstractmethod
    def create_node(self, state, parent=None, action=None):
        """ Create a new node with the given state, parent, and action. """
        raise NotImplementedError("Subclasses should implement this method")

    @abstractmethod
    def run(self):
        """ Run the search algorithm to find a solution to the problem. """
        raise NotImplementedError("Subclasses should implement this method")

    def results(self):
        """
        Print the problem description, initial scenario, and the solution path.
        """
        print(f"Problem: {self.problem.name}")
        print(f"Description: {self.problem.description}")
        print(f"Algorith used to solve: {self.name}\n")
        print("Initial Scenario: ")
        print(self.problem.initial_state.show())

        print(f"\nSolution Found after {self.nodes_checked} Nodes Checked")
        print(f"Elapsed Time: {self.elapsed_time:.4f} seconds\n")

        nodes = self.solution_node.get_path()
        depth = len(nodes) - 1  # Exclude initial node from depth count

        print(f"Solution Depth: {depth}")
        print(f"Expected Depth: {self.problem.expected_depth}\n")

        for node in nodes:
            print(node.show())

        if depth > self.problem.expected_depth:
            warnings.warn(
                f"Solution depth {depth} exceeds expected depth {self.problem.expected_depth}."
            )

        self.problem.after_solve(nodes)

