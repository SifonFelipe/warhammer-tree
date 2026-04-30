import math
import sys
import os
from dataclasses import dataclass
from collections import defaultdict
from typing import Tuple

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from .utils import Position
from .warhammer_draw import Draw
from problem import Problem

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
UNNECESARY_PRAY_PENALTY = 5

def position_is_in(pos, range_positions):
    """
    Check if a position is in a list of positions (by coordinates).
    Mute from Tuple to Position object
    """

    if isinstance(pos, Position):
        pos = (pos.x, pos.y)

    for position in range_positions:
        if (position.x, position.y) == pos:
            return True

    return False


@dataclass
class GoldPosition:
    """
    A position from which you can shoot multiple xenos,
    with the count of xenos and distance to it.
    """
    position: Position
    xeno_count: int
    distance: int


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

        # Movement: cardinal only (Manhattan step)
        if faith >= move_cost and not is_armed:
            for mov in [
                Position(pos.x + 1, pos.y),
                Position(pos.x - 1, pos.y),
                Position(pos.x, pos.y + 1),
                Position(pos.x, pos.y - 1),
            ]:
                if not position_is_in(mov, xenos):
                    actions.append(("move", mov))

        # Check armed and shoot distance
        if faith >= arm_cost:
            if is_armed:
                actions.append(("arm", False))

                if faith >= shoot_cost:
                    for xeno in xenos:
                        if pos.chebyshev_distance(xeno) <= SHOOT_DISTANCE:
                            actions.append(("shoot", xeno))
            else:
                for xeno in xenos:
                    if pos.chebyshev_distance(xeno) <= SHOOT_DISTANCE:
                        actions.append(("arm", True))
                        break

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

    def gold_positions(self, state):
        """
        Gold positions are positions from which you can kill the most xenos
        with the fewest moves.
        Returns a list of (position, xeno_count) tuples,
        sorted best-first.
        """
        xenos = state.xenos
        position = state.position

        if not xenos:
            return []

        # Map each xeno to the set of positions from which it can be shot
        xeno_ranges = {
            xeno: set(xeno.positions_in_range(SHOOT_DISTANCE))
            for xeno in xenos
        }

        # Score every candidate position: how many xenos can be hit from there?
        position_scores = defaultdict(int)
        for xeno, reachable_positions in xeno_ranges.items():
            for pos in reachable_positions:
                for x in xenos:
                    if pos.get_distance(x) == 0:
                        continue  # Can't stand on a xeno

                pos = (pos.x, pos.y)  # Use tuple for dict key
                position_scores[pos] += 1

        # Sort by score descending
        gold = sorted(position_scores.items(), key=lambda item: item[1], reverse=True)

        # Only return positions where you can hit more than 1 xeno
        gold = [
            GoldPosition(
                position=Position(pos[0], pos[1]),
                xeno_count=count,
                distance=position.distance_to(Position(pos[0], pos[1]))
            )
            for pos, count in gold if count > 1
        ]

        return gold

    def get_heuristic(self, state):
        xenos = state.xenos
        pos = state.position

        if not xenos:
            return 0

        shoot_cost = FAITH_COSTS[SHOOT] * len(xenos)
        min_distance = min(pos.distance_to(x) for x in xenos)
        move_cost = max(0, min_distance - SHOOT_DISTANCE) * FAITH_COSTS[MOVE]
        arm_cost = 0 if state.armed else FAITH_COSTS[ARM]

        min_faith_needed = shoot_cost + move_cost + arm_cost  # negative (costs)

        faith_deficit = min_faith_needed - state.faith  # both negative
        pray_cost = 0
        if faith_deficit < 0:  # Need more faith
            pray_gain = abs(FAITH_COSTS[PRAY])
            prays_needed = math.ceil(abs(faith_deficit) / pray_gain)
            pray_cost = prays_needed

        return shoot_cost + move_cost + arm_cost + pray_cost

    def after_solve(self, nodes):
        """
        After solving, we can show the solution visually
        """
        draw = Draw(nodes)
        ans = str(input("Do you want to see the solution visually? (y/n): ")).lower()
        if ans == "y":
            draw.run()

