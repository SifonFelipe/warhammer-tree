import copy

class Colors:
    DARK_RED = '\033[31m'
    BRONZE = '\033[33m' # Un color que se asemeja al metal/cobre
    CYAN = '\033[36m'
    GREY = '\033[90m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

class Draw:
    def __init__(self, nodes):
        self.nodes = nodes

    def get_bounds(self):
        all_x = []
        all_y = []

        for node in self.nodes:
            all_x.append(node.status.position.x)
            all_y.append(node.status.position.y)

            for xeno in node.status.xenos:
                all_x.append(xeno.x)
                all_y.append(xeno.y)

        return min(all_x), max(all_x), min(all_y), max(all_y)

    def run(self):
        min_x, max_x, min_y, max_y = self.get_bounds()
        grid_w, grid_h = (max_x - min_x + 3), (max_y - min_y + 1)
        offset_x, offset_y = (-min_x + 1), (-min_y)

        for node in self.nodes:
            print("\033[H\033[J", end="")

            grid = [["." for _ in range(grid_w)] for _ in range(grid_h)]

            pos = node.status.position
            grid[pos.y + offset_y][pos.x + offset_x] = f"{Colors.CYAN}{Colors.BOLD}Ω{Colors.RESET}"

            for xeno in node.status.xenos:
                grid[xeno.y + offset_y][xeno.x + offset_x] = f"{Colors.DARK_RED}X{Colors.RESET}"

            # Interface "Data-Slate" of Mechanicus
            print(f"{Colors.BRONZE}+++ DATA-SLATE: TACTICAL AUSPEX SCAN +++{Colors.RESET}")
            print(f"{Colors.GREY}+---------------------------------------{Colors.RESET}")
            for row in grid:
                print(f"{Colors.GREY}|{Colors.RESET} " + "".join(row) + f" {Colors.GREY}|{Colors.RESET}")

            print(f"{Colors.GREY}+---------------------------------------{Colors.RESET}")

            # System "teletry"
            print(f"{Colors.BRONZE}>>> MACHINE SPIRIT STATUS:{Colors.RESET}")
            print(f" Faith Core   : [{Colors.CYAN}{'█' * (node.status.faith // 2)}"\
                  f"{'░' * (10 - node.status.faith // 2)}{Colors.RESET}] {node.status.faith}%")
            print(f" Weapon Link  : {'[ARMED]' if node.status.armed else '[DISARMED]'}")
            print(f" Last Invoked : {node.show_action()}")
            print(f"{Colors.BRONZE}+++ END OF TRANSMISSION +++{Colors.RESET}")

            _ = input(f"{Colors.GREY}>> Waiting for input...{Colors.RESET}")
