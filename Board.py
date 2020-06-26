"""
A game board object

"""

import numpy as np
from CrossPoint import CrossPoint
from typing import List, Union
from Helper import Helper
import copy


class Board:
    '''
    ===============  Attributes  ===============
    size: int
    turn: int
        -1 for black 1 for white
    whiteTimer: Time
        The amount of time is allowed for white
        player before goes into ticker time
    whiteTickerNum: int
        The number of times a n seconds ticker is 
        allowed
    whiteTicker: Time
        The amount of time that is given to the 
        player after regular timer
    blackTimer: Time
        The amount of time is allowed for black
        player before goes into time ticker
    blackTickerNum: int
    blackTicker: Time

    moveSquence: List[Stone]
    currStatePtr: int
        A index of moveSquence to indicate the 
        board state that is required to render

    CurrBoard: List of Lists[CrossPoint]

    groupInfo: Dict[CrossPoint, List]
        A dictionary that records the liberty crosspoints of 
        a head of a group.
    '''

    def __init__(self, size, timeLimit, tickerLimit, tickerNum):
        """
        ==========    Parameters    ==========

        """
        self.size = size
        # Indicates the color of the next player
        self.turn = -1
        self.whiteTimer = timeLimit
        self.blackTimer = timeLimit
        self.whiteTickerNum = tickerNum
        self.blackTickerNum = tickerNum
        self.whiteTicker = tickerLimit
        self.blackTicker = tickerLimit

        self.moveSquence = []
        self.movePtr = -1
        self.currBoard = np.empty([size, size], dtype=CrossPoint)
        for i in range(size):
            for j in range(size):
                self.currBoard[i, j] = CrossPoint(0, [i,j])
        self.pre1Board = None
        self.groupInfo = {}

        self.whiteCaptured = 0
        self.blackCaptured = 0

    def __str__(self):
        result = np.empty([self.size, self.size], dtype=int)
        for i in range(self.size):
            for j in range(self.size):
                result[i, j] = str(self.currBoard[i, j])
        return str(result)


    def placeStone(self, x: int, y: int) -> bool:
        """ Check is the stone placed at (x, y) a legal move.
        Place it if its legal and return true, false otherwise.
        
        """

        # Check is the position (x, y) already been occupied.
        if self.currBoard[x, y].color != 0:
            return False

        # Check whether the intended position is a suicide or a 
        # capture.

        # Get the head of the surrounding crossPoints.
        friends, foes, neutral = Helper.getAdjacents(
            self, x, y)
        tempPre1Board = copy.deepcopy(self.currBoard)

        # Check if any enemy stone is captured by this move
        isThereCaptured = False
        for cp in foes:
            if len(self.groupInfo[cp]) == 1:
                isThereCaptured = True
            else:
                foes.pop(cp)

        # IF true, check for ko. 
        if isThereCaptured:
            captured = []

            # Uncolor all captured stones
            for i in range(self.size):
                for j in range(self.size):
                    if Helper.getHead(self.currBoard[i,j]) in foes:
                        self.currBoard[i,j].color = 0
                        captured.append(self.currBoard[i, j])
            self.currBoard[x, y].color = self.turn

            # Compare currBoard with pre1Board.
            isKo = True
            for i in range(self.size):
                for j in range(self.size):
                    if self.currBoard[i, j].color != \
                        self.pre1Board[i, j].color:
                        isKo = False
                        break
                if not isKo:
                    break

            # IF is ko, color all captured stones back to its original 
            # color then return false.
            if isKo:
                self.currBoard[x, y].color = 0
                for cp in captured:
                    self.currBoard[cp.x, cp.y].color = -1 * self.turn
                print("It is Ko")
                return False
            else:
                for cp in captured:
                    cp.head = None

        # IF false, check for suicide. If its suicide return false.
        else:
            isSuicide = True
            if len(neutral) > 0:
                isSuicide = False
            else:
                for cp in friends:
                    if len(self.groupInfo[cp]) > 1:
                        isSuicide = False
                        break
            if isSuicide:
                print("It is suicide")
                return False

        # To here we are in the situation of either captured some  
        # stones or its not suicide,we need to record all the changes.
        # First by change the turn to next player.
        self.currBoard[x, y].color = self.turn
        self.turn *= -1
        self.groupInfo[self.currBoard[x ,y]] = []

        # Change the head of each cp in friends to the newly placed cp 
        # and remove the cp from groupInfo since its been grouped  
        # with the new cp and update the info in currBoard[x,y]
        for cp in friends:
            cp.head = self.currBoard[x, y]
            self.groupInfo[self.currBoard[x ,y]].extend(
                self.groupInfo[cp])
            self.groupInfo.pop(cp)

        # Add new cp that are considered as liberty to the cp at (x,y)
        for cp in neutral:
            self.groupInfo[self.currBoard[x ,y]].append(cp)
        self.groupInfo[self.currBoard[x ,y]] = \
            list(set(self.groupInfo[self.currBoard[x ,y]]))
        try:
            self.groupInfo[self.currBoard[x ,y]].remove(
                self.currBoard[x,y])
        except ValueError:
            pass
        self.pre1Board = tempPre1Board

        # TODO: consider record the move sequence.
        return True


if __name__ == "__main__":
    boardA = Board(19, 0,0,0)
    print(boardA)

    r = boardA.placeStone(3,4)
    
    print(r)
    print(boardA)











