"""
docstring example
=================
"""

# Builtin / legacy variables
from functools import reduce

# Classes
class Class(object):
# Functions and methods
    def __init__(self, stuff: str):
# Keyword variables
        self.stuff: str = stuff

# Control flow keywords
things = [Class(i) for i in "stuff"]
if True:
    assert things[0].stuff == "s"

# Comments
def main():
    for _ in range(reduce(sum, [5, 5 << 1])):
        print("Hello World")
# Operators
    print(1 << 6 & 43 + 987 - 34)