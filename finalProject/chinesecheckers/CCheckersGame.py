from __future__ import print_function
import sys
import numpy as np
from finalProject.Game import Game
from finalProject.chinesecheckers.CCheckersLogic import Board
from finalProject.gui_2 import *

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
        self.goals = self.getInitBoard().goal

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
        b.pieces = np.copy(board.pieces)
        legal_moves = b.get_legal_moves(player)
        if len(legal_moves) == 0:
            valids[-1]=1  # TODO not sure what this does!!!
            return np.array(valids)
        return legal_moves

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
        if b.is_game_over(player):  # Player can be represented by either 1 or -1
            return 1
        if b.is_game_over(-player):
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

    ''' Score of Player 1
                      0      goal
                   -1   -1  
                 -2   -2   -2  
               -3   -3   -3  -3  
            -4   -4   -4   -4   -4  
          -5   -5   -5   -5   -5  -5  
            -6   -6   -6   -6   -6  
              -7   -7   -7   -7  
                -9    -9   -9  
                  -12   -12  
                     -16    starting
        '''

    ''' Score of Player 2
                          -16     starting
                       -12   -12  
                     -9   -9   -9  
                   -7   -7   -7  -7  
                -6   -6   -6   -6   -6  
              -5   -5   -5   -5   -5  -5  
                 -4   -4   -4   -4  -4  
                   -3   -3   -3   -3  
                     -2    -2   -2  
                        -1    -1  
                            0     goal 
            '''

    def getScore(self, board, player):
        playerInd = 1 if player == 1 else 0
        score = 0
        b = Board(self.n)
        b.pieces = np.copy(board.pieces)
        for i in range(6):
            if playerInd:
                score += board.scorePlayer1[b.pieces[playerInd, i]][0]
                score -= board.scorePlayer2[b.pieces[playerInd-1, i]][0]
            else:
                score -= board.scorePlayer1[b.pieces[playerInd+1, i]][0]
                score += board.scorePlayer2[b.pieces[playerInd, i]][0]
        return score

    @staticmethod
    def display(display, board, cannonical):
        display_layout(display, cannonical)
        print("----------------------------------------")
        print(str(board), end="")
        print("----------------------------------------")