import problems
import solvers

SOLVERS = {
    "BFS": solvers.BFS_Solver,
    "DFS": solvers.DFS_Solver,
    "ASTAR": solvers.AStar_Solver,
}

if __name__ == "__main__":
    possible_scenario = problems.WarhammerState(
        spawn=problems.Position(0, 0),
        position=problems.Position(0, 0),
        xenos=(
            problems.Position(2, 0),
            problems.Position(-2, 0),
            problems.Position(0, 2),
            problems.Position(0, -3)
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

    solver = SOLVERS["BFS"]
    solver = solver(wh_problem)
    solver.run()
    solver.results()
