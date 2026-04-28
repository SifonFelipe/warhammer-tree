from abc import ABC, abstractmethod

class Problem(ABC):
    """ Abstract base class for a problem to be solved by a search algorithm. """

    def __init__(self, name, description, initial_state, expected_depth):
        self.name = name
        self.description = description
        self.initial_state = initial_state
        self.expected_depth = expected_depth

    @abstractmethod
    def check_win(self, state):
        """ Return True if the current state is a winning state, False otherwise."""
        raise NotImplementedError("Subclasses should implement this method")

    @abstractmethod
    def get_actions(self, state):
        """ Return a list of possible actions that can be taken from the given state."""
        raise NotImplementedError("Subclasses should implement this method")

    @abstractmethod
    def apply_action(self, state, action):
        """ Return the new state that results from applying the given action to the given state."""
        raise NotImplementedError("Subclasses should implement this method")

    @abstractmethod
    def after_solve(self, nodes):
        """ Perform any necessary actions after the problem has been solved, such as printing the solution path."""
        raise NotImplementedError("Subclasses should implement this method")
