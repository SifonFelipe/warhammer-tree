import math
from dataclasses import dataclass, asdict
from typing import Tuple

from draw import Draw

# Actions
MOVE = "move"
SHOOT = "shoot"
ARM = "arm"
PRAY = "pray"

FAITH_COSTS = {
    MOVE: 1,
    SHOOT: 2,
    ARM: 1,
    PRAY: -10
}
SHOOT_DISTANCE = 2
FAITH_MAX = 20  # If faith goes to 0, he loses


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


@dataclass
class Status:
    """
    Map and character data
    """
    spawn: Position
    position: Position
    xenos: Tuple[Position, ...]
    armed: bool = False
    faith: int = 0

    def __post_init__(self):
        self.faith = min(self.faith, FAITH_MAX)

    def show(self):
        xenos_pos = [p.show() for p in self.xenos]
        return f"Position: {self.position.show()}, " \
               f"Xenos: {len(self.xenos)} {xenos_pos}, " \
               f"Armed: {self.armed}, " \
               f"Faith: {self.faith}"


class Node:
    def __init__(self, status: Status, parent=None, action=None):
        self.status = status
        self.parent = parent
        self.action = action

    @property
    def is_head(self):
        """ True if first node """
        return self.parent is None

    def get_path(self):
        """ Get path from head to current node """
        path = []
        node = self

        while node is not None:
            path.append(node)
            node = node.parent

        return list(reversed(path))

    def show_action(self):
        if self.action:
            if isinstance(self.action[1], Position):
                action_target = self.action[1].show()
            else:
                action_target = self.action[1]

            return f"{self.action[0]} {action_target}"

        return "Start"

    def show(self):
        action = self.show_action()
        return f"Status: {self.status.show()}, Action: {action}"


class Environment:
    def __init__(self, status: Position):
        initial_node = self.create_node(status)
        self.weights = [initial_node]

    def possible_actions(self, status):
        """
        Possible actions:
        - (move, Position): move to a position next to actual one
        - (arm, bool): arm or disarm current weapon
        - (shoot, Position): shoot/kill xeno (Position)
        - (pray, amount): pray and recharge faith
        """

        actions = []
        pos = status.position
        xenos = status.xenos
        is_armed = status.armed
        faith = status.faith

        move_cost = FAITH_COSTS[MOVE]
        shoot_cost = FAITH_COSTS[SHOOT]
        arm_cost = FAITH_COSTS[ARM]
        pray_cost = FAITH_COSTS[PRAY]

        # Check for movements
        if faith >= move_cost and not is_armed:
            right = Position(pos.x + 1, pos.y)
            left = Position(pos.x - 1, pos.y)
            up = Position(pos.x, pos.y + 1)
            down = Position(pos.x, pos.y - 1)

            for mov in [right, left, up, down]:
                if mov not in xenos:
                    actions.append(("move", mov))

        # Check armed and shoot distance
        if faith >= arm_cost:
            if is_armed:
                actions.append(("arm", False))

                if faith >= shoot_cost:
                    for xeno in xenos:
                        if pos.get_distance(xeno) <= SHOOT_DISTANCE:
                            actions.append(("shoot", xeno))

            else:
                actions.append(("arm", True))

        # Check faith
        if faith < FAITH_MAX:
            pray_cost = FAITH_COSTS[PRAY]

            to_recharge = min(FAITH_MAX-faith, pray_cost)
            actions.append(("pray", to_recharge))

        return actions

    def check_win(self, status):
        return len(status.xenos) == 0

    def create_node(self, status: Status, parent=None, action=None):
        return Node(status=status, parent=parent, action=action)

    def solve(self, node):
        """
        Solve returns possible branches to the world, status changes
        """
        status = node.status

        actions = self.possible_actions(status)
        faith = status.faith
        xenos = status.xenos
        armed = status.armed
        position = status.position
        spawn = status.spawn

        solved = False
        node_solution = None

        for action in actions:
            type_action = action[0]
            target = action[1]
            cost = FAITH_COSTS[type_action]

            assert faith >= cost, f"You don't have enough faith. ({faith})"
            new_faith = faith - cost

            if type_action == MOVE:
                assert target not in xenos, "There is a xeno where you wanna move"
                assert not armed, "You can't move if you are armed"
                new_status = Status(
                    spawn=spawn,
                    position=target,
                    xenos=xenos,
                    armed=armed,
                    faith=new_faith
                )

            elif type_action == SHOOT:
                assert target in xenos, "You are shooting nothing"
                new_status = Status(
                    spawn=spawn,
                    position=position,
                    xenos=tuple(x for x in xenos if x != target),
                    armed=armed,
                    faith=new_faith
                )

            elif type_action == ARM:
                assert target != armed, "You can't change to same gun"
                new_status = Status(
                    spawn=spawn,
                    position=position,
                    xenos=xenos,
                    armed=target,
                    faith=new_faith
                )

            elif type_action == PRAY:
                new_status = Status(
                    spawn=spawn,
                    position=position,
                    xenos=xenos,
                    armed=armed,
                    faith=new_faith
                )
            else:
                raise ValueError(f"Unknown action type: {type_action}")

            branch = self.create_node(status=new_status, parent=node, action=action)
            self.weights.append(branch)

            if self.check_win(new_status):
                node_solution = branch
                solved = True
                break

        return solved, node_solution

    def run(self):
        nodes_checked = 0
        solved = False
        while not solved:
            actual_node = self.weights.pop(0)
            solved, node_solution = self.solve(actual_node)
            nodes_checked += 1

        print("Nodes checked: ", nodes_checked)
        return node_solution


if __name__ == "__main__":
    possible_scenario = Status(
        spawn=Position(0, 0),
        position=Position(0, 0),
        xenos=(Position(0, 3), Position(0, -2), Position(2, 0), Position(-2, 0)),
        armed=False,
        faith=20
    )
    env = Environment(possible_scenario)
    solution = env.run()

    print("Initial Scenario: ")
    print(possible_scenario.show())

    print("\nSolution Found: ")
    path = solution.get_path()

    for node in path:
        print(node.show())

    visual = str(input("Do you want to see the solution visually? (y/n): ")).lower()
    if visual == "y":
        Draw(path).run()
