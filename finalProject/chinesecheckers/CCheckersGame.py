import sys
import numpy as np
sys.path.append('../..')
from ..Game import Game
from .CCheckersLogic import Board

class CCheckersGame(Game):
    pit_content = {
        -1: "2",
        +0: "-",
        +1:"1"
    }

    @staticmethod
    def getPit(piece):
        return CCheckersGame.pit_content[piece]
    def __init__(self, n):
        self.n = n

    def getinitBoard(self):
        board = Board(self.n)
        return np.array(b.pieces)
        # init = [["1", " ", " ", " ", " ", " "],
        #        ["1", "1", " ", " ", " ", " "],
        #        ["1", "1", "1", " ", " ", " "],
        #        ["-", "-", "-", "-", " ", " "],
        #        ["-", "-", "-", "-", "-", " "],
        #        ["-", "-", "-", "-", "-", "-"],
        #        ["-", "-", "-", "-", "-", " "],
        #        ["-", "-", "-", "-", " ", " "],
        #        ["2", "2", "2", " ", " ", " "],
        #        ["2", "2", " ", " ", " ", " "],
        #        ["2", " ", " ", " ", " ", " "]]

    def getBoardSize(self):
        return (self.n, self.n)  # return tuple

    def getActionSize(self):
        return self.n*self.n + 1

    def getNextState(self, board, player, action):
        # For player taking an action on board
        # TODO Need to check if action is valid
        if action == self.n*self.n:
            return (board, -player)
        b = Board(self.n)
        b.pieces = np.copy(board)
        move = 0  # TODO

    def getValidMoves(self, board, player):
        """
        Input:
            board: current board
            player: current player
        Returns:
            validMoves: a binary vector of length self.getActionSize(), 1 for
                        moves that are valid from the current board and player,
                        0 for invalid moves
        """
        pass

    def getGameEnded(self, board, player):
        """
        Input:
            board: current board
            player: current player (1 or -1)
        Returns:
            r: 0 if game has not ended. 1 if player won, -1 if player lost,
               small non-zero value for draw.

        """
        pass

    def getCanonicalForm(self, board, player):
        """
        Input:
            board: current board
            player: current player (1 or -1)
        Returns:
            canonicalBoard: returns canonical form of board. The canonical form
                            should be independent of player. For e.g. in chess,
                            the canonical form can be chosen to be from the pov
                            of white. When the player is white, we can return
                            board as is. When the player is black, we can invert
                            the colors and return the board.
        """
        pass

    def getSymmetries(self, board, pi):
        """
        Input:
            board: current board
            pi: policy vector of size self.getActionSize()
        Returns:
            symmForms: a list of [(board,pi)] where each tuple is a symmetrical
                       form of the board and the corresponding pi vector. This
                       is used when training the neural network from examples.
        """
        pass

    def stringRepresentation(self, board):
        """
        Input:
            board: current board
        Returns:
            boardString: a quick conversion of board to a string format.
                         Required by MCTS for hashing.
        """
        pass
