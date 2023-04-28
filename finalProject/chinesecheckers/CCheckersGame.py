from __future__ import print_function
import sys
sys.path.append('..')
from finalProject.Game import Game
from .CCheckersLogic import Board
import numpy as np

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

    def getStringRepresentation(self):
        board = Board(self.n)
        return str(board)

    def getInitBoard(self):
        '''TODO
            Compact code by using tuples of coordinates -> map to board on print
            As opposed to string layout of board + updating per move
            |
            Hard code/precompute all moves at every pit
                Prune off if piece in pit
                    But also hardcode if piece can jump + prune if not possible
            |
            Results in 12 possible moves being hardcoded per pit
        '''
        b = Board(self.n)
        return np.array(b.pieces)  # In array form for neural network

    def getBoardSize(self):
        return self.n

    def getActionSize(self):
        return 6  # Constant for number of possible moves from 1 pit

    def getNextState(self, board, player, action):
        # For player taking an action on board
        # TODO Need to check if action is valid
        if action == self.n*self.n:
            board.execute_move(player, action)
            return (board, -player)
        b = Board()
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
        return board.get_legal_moves(player)

    def getGameEnded(self, board, player):
        """
        Input:
            board: current board
            player: current player (1 or -1)
        Returns:
            r: 0 if game has not ended. 1 if player won, -1 if player lost,
               small non-zero value for draw.

        """
        b = Board(self.n)
        b.pieces = np.copy(board)
        if b.is_game__over(player):  # Player can be represented by either 1 or -1
            return 1
        if b.is_game__over(-player):
            return -1
        else:
            return 0

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
        playerInd = 0 if player == 1 else 1
        return player*board  # Returns the np.array as the player's state

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
        return []

    def stringRepresentation(self, board):
        """
        Input:
            board: current board
        Returns:
            boardString: a quick conversion of board to a string format.
                         Required by MCTS for hashing.
        """
        return str(board)

    def getScore(self, board, player):
        board = Board(self.n)
        board.pieces = np.copy(board)
        return board.countDiff(player)  # TODO NEED TO IMPLEMENT

    @staticmethod
    def display(board):
        print("----------------------------------------")
        print(str(board))
        print("----------------------------------------")