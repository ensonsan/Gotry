# find group head
# get adjacent
# combine connected group
from typing import Tuple
from CrossPoint import CrossPoint

class Helper:

	@staticmethod
	def getHead(cp):
		counter = 0
		result = cp
		while result.head is not None:
			result = result.head
			counter += 1
			
		if counter > 2:
			cp.head = result		
		return result

	def getAdjacents(board, x: int, y: int) -> Tuple:
		friends = []
		foes = []
		neutral = []

		try:
			if board.currBoard[x-1, y].color == board.turn:
				friends.append(board.currBoard[x-1, y])
			elif board.currBoard[x-1, y].color == -1 * board.turn:
				foes.append(board.currBoard[x-1, y])
			else:
				neutral.append(board.currBoard[x-1, y])
		except IndexError:
			pass
		try:
			if board.currBoard[x+1, y].color == board.turn:
				friends.append(board.currBoard[x+1, y])
			elif board.currBoard[x+1, y].color == -1 * board.turn:
				foes.append(board.currBoard[x+1, y])
			else:
				neutral.append(board.currBoard[x+1, y])
		except IndexError:
			pass
		try:
			if board.currBoard[x, y-1].color == board.turn:
				friends.append(board.currBoard[x, y-1])
			elif board.currBoard[x, y-1].color == -1 * board.turn:
				foes.append(board.currBoard[x, y-1])
			else:
				neutral.append(board.currBoard[x, y-1])
		except IndexError:
			pass
		try:
			if board.currBoard[x, y+1].color == board.turn:
				friends.append(board.currBoard[x, y+1])
			elif board.currBoard[x, y+1].color == -1 * board.turn:
				foes.append(board.currBoard[x, y+1])
			else:
				neutral.append(board.currBoard[x, y+1])
		except IndexError:
			pass
		return friends, foes, neutral



