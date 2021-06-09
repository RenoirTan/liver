import sys
from typing import *
from . import script


COMMANDS: Dict[str, Callable] = {
    "resolve": script.show_resolved_colors,
    "generate": script.generate
}


def main(args: List[str]) -> int:
    if len(args) < 2:
        print("No arguments")
        return 0
    COMMANDS[args[1]](*args[2:])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
