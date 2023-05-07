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
        self.pieces = [None] * self.n
        for i in range(self.n):
            self.pieces[i] = [0] * self.n
        self.pieces = np.zeros((2, 6), dtype=int)
        self.pieces[0, :] = [0, 1, 2, 3, 4, 5]
        self.pieces[1, :] = 35 - np.array([5, 4, 3, 2, 1, 0])

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
        return b  # In array form for neural network

    def getBoardSize(self):
        return self.n

    def getActionSize(self):
        return 6  # Constant for number of possible moves from 1 pit

    def getNextState(self, board, player, action):
        # For player taking an action on board
        # TODO Need to check if action is valid
        if action == [-1, -1]:
            return (board, -player)
        b = Board(self.n)
        self.pieces = np.copy(board.pieces)
        b.pieces = np.copy(board.pieces)
        piece, move = action
        b.execute_move(player, piece, move)
        return (b, -player)

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
        valids = [0]*self.getActionSize()
        b = Board(self.n)
        b.pieces = np.copy(self.pieces)
        legal_moves = b.get_legal_moves(player)
        if len(legal_moves) == 0:
            valids[-1]=1  # TODO not sure what this does!!!
            return np.array(valids)
        return legal_moves

    def getPlayerPieces(self, board):
        # index = [None] * self.n
        # for i in range(0, self.n):
        #     index[i] = [0] * self.n
        # index = np.zeros((2, 6), dtype=int)
        # counter_p2 = 0
        # counter_p1 = 0
        # for i in range(0, 36):
        #     if board[i] == 1:
        #         index[1, counter_p2] = i
        #         counter_p2 += 1
        #     elif board[i] == -1:
        #         index[0, counter_p1] = i
        #         counter_p1 += 1

        return self.pieces

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
        b.pieces = np.copy(board.pieces)
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
        map = np.zeros((36))
        map[board[0]] = -1
        map[board[1]] = 1
        return map  # Returns the np.array as the player's state

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

    '''
                 0      player 1 goal
               1   2  
             3   4   5  
           6   7   8   9  
        10  11  12  13  14  
      15  16  17  18  19  20  
        21  22  23  24  25  
          26  27  28  29  
            30  31  32  
              33  34  
                35       player 2 goal
    '''

    def getScore(self, board, player):
        playerInd = 1 if player == 1 else 0
        score = 0
        for i in range(6):
            if playerInd:
                score += board.scorePlayer1[self.pieces[playerInd, i]][0]
                score -= board.scorePlayer2[self.pieces[playerInd-1, i]][0]
            else:
                score -= board.scorePlayer1[self.pieces[playerInd+1, i]][0]
                score += board.scorePlayer2[self.pieces[playerInd, i]][0]
        return score

    @staticmethod
    def display(board):
        print("----------------------------------------")
        print(str(board), end="")
        print("----------------------------------------")