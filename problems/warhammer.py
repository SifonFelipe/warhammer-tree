from .utils import Position
from .warhammer_draw import Draw
from problem import Problem

import sys
import os
from dataclasses import dataclass, asdict
from typing import Tuple

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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


@dataclass
class WarhammerState:
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


class WarhammerProblem(Problem):
    """
    The problem consists of a Devastator Marine in a xeno-infested planet.
    The goal is to eliminate all xenos while managing the marine's faith and weapon status.
    The marine can move, arm/disarm his weapon, shoot xenos, or pray to recharge faith.
    """

    def get_actions(self, state):
        """
        Possible actions:
        - (move, Position): move to a position next to actual one
        - (arm, bool): arm or disarm current weapon
        - (shoot, Position): shoot/kill xeno (Position)
        - (pray, amount): pray and recharge faith
        """

        actions = []
        pos = state.position
        xenos = state.xenos
        is_armed = state.armed
        faith = state.faith

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

    def check_win(self, state):
        """ Checks if there are no xenos left """
        return len(state.xenos) == 0

    def apply_action(self, state, action):
        """
        Solve returns possible branches to the world, state changes
        """
        faith = state.faith
        xenos = state.xenos
        armed = state.armed
        position = state.position
        spawn = state.spawn

        type_action = action[0]
        target = action[1]
        cost = FAITH_COSTS[type_action]

        assert faith >= cost, f"You don't have enough faith. ({faith})"
        new_faith = faith - cost

        if type_action == MOVE:
            assert target not in xenos, "There is a xeno where you wanna move"
            assert not armed, "You can't move if you are armed"
            new_state = WarhammerState(
                spawn=spawn,
                position=target,
                xenos=xenos,
                armed=armed,
                faith=new_faith
            )

        elif type_action == SHOOT:
            assert target in xenos, "You are shooting nothing"
            new_state = WarhammerState(
                spawn=spawn,
                position=position,
                xenos=tuple(x for x in xenos if x != target),
                armed=armed,
                faith=new_faith
            )

        elif type_action == ARM:
            assert target != armed, "You can't change to same gun"
            new_state = WarhammerState(
                spawn=spawn,
                position=position,
                xenos=xenos,
                armed=target,
                faith=new_faith
            )

        elif type_action == PRAY:
            new_state = WarhammerState(
                spawn=spawn,
                position=position,
                xenos=xenos,
                armed=armed,
                faith=new_faith
            )
        else:
            raise ValueError(f"Unknown action type: {type_action}")

        return new_state

    def after_solve(self, nodes):
        """
        After solving, we can show the solution visually
        """
        draw = Draw(nodes)
        ans = str(input("Do you want to see the solution visually? (y/n): ")).lower()
        if ans == "y":
            draw.run()

