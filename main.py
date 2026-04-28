import warnings
import problems

class Node:
    """
    Node class represents a state in the search tree,
    along with its parent and the action taken to reach it.
    """
    def __init__(self, state, parent=None, action=None):
        self.state = state
        self.parent = parent
        self.action = action

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
        return f"State: {self.state.show()}, Action: {action}"


class Solver:
    """
    Solver implements a tree algorithm to find a solution to any given problem.
    It uses the Problem class to define the problem space and the Node class to
    represent states in the search tree.
    Takes as a solution the first node that reaches a winning state (less weight)
    """
    def __init__(self, problem):
        self.problem = problem
        self.initial_node = self.create_node(problem.initial_state)
        self.weights = [self.initial_node]

    def create_node(self, state, parent=None, action=None):
        return Node(state=state, parent=parent, action=action)

    def run(self):
        nodes_checked = 0

        while True:
            parent_node = self.weights.pop(0)
            state = parent_node.state
            actions = self.problem.get_actions(state)

            for action in actions:
                new_state = self.problem.apply_action(state, action)
                new_node = self.create_node(new_state, parent=parent_node, action=action)

                nodes_checked += 1
                if self.problem.check_win(new_state):
                    self.solution_node = new_node
                    self.nodes_checked = nodes_checked
                    return new_node, nodes_checked

                self.weights.append(new_node)

    def results(self):
        """
        Print the problem description, initial scenario, and the solution path.
        """

        print(f"Problem: {self.problem.name}")
        print(f"Description: {self.problem.description}")
        print("Initial Scenario: ")
        print(self.problem.initial_state.show())

        print(f"\nSolution Found after {self.nodes_checked} Nodes Checked")

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


if __name__ == "__main__":
    possible_scenario = problems.WarhammerState(
        spawn=problems.Position(0, 0),
        position=problems.Position(0, 0),
        xenos=(
            problems.Position(0, 3),
            problems.Position(0, -2),
            problems.Position(2, 0),
            problems.Position(-2, 0),
        ),
        armed=False,
        faith=20
    )
    wh_problem = problems.WarhammerProblem(
        name="Warhammer 40k: Purge",
        description="You are a lone Devastator Marine, armed with a powerful"\
                    "Heavy Bolter, tasked with purging xenos",
        initial_state=possible_scenario,
        expected_depth=8
    )

    solver = Solver(wh_problem)
    solver.run()
    solver.results()
