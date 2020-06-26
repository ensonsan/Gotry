"""
A CrossPoint object that is need to be place at each intersection
on the board to indicate black , white, or empty.

cp is an abbreviation of CrossPoint.

"""
from typing import List


class CrossPoint:
    """
    =============   Attributes   =============
    color: int
        -1 for black, 1 for white, 0 for neutral.
    head: CrossPoint
        The head of a cp is the representative of a set
        of cps that has the same color and are connected.
        If the head of a cp is None then it is considered
        as the head of the set.
    where: [int x, int y]
        the x y position of the point on a game board.
    
    """
    def __init__(self, color: int, pos: List):
        self.color = color
        self.head = None
        self.x = pos[0]
        self.y = pos[1]

    def __hash__(self):
        return hash((self.x, self.y))

    def __str__(self):
        return str(self.color)




    
