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
        b.pieces = np.copy(board)
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
        # if len(board) == 2:  # FIXME randPlayer and Human both use canonical for board!!
        #     b.pieces = np.copy(self.pieces)
        # else:
        #     b.pieces = np.copy(board)
        b.pieces = np.copy(board)
        legal_moves = b.get_legal_moves(player)
        if len(legal_moves) == 0:
            valids[-1]=1  # TODO not sure what this does!!!
            return np.array(valids)
        return legal_moves

    def getPlayerPieces(self, player):
        return np.nonzero(self.pieces[:] == player)

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
        b.pieces = np.copy(board)  # For canonical board
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
        canonical_s = "".join(self.pit_content[pit] for pit in board)
        return canonical_s

    def getScore(self, board, player):
        board = Board(self.n)
        board.pieces = np.copy(board)
        return board.countDiff(player)  # TODO NEED TO IMPLEMENT

    @staticmethod
    def display(display, pieces, cannonical):
        display_layout(display, cannonical)
        lengths = [1, 2, 3, 4, 5, 6]
        out = ""
        index = 0
        reverse_index = 2

        if len(pieces) == 2:
            p1_piece_indexes = pieces[0,:]
            p2_piece_indexes = pieces[1,:]
        else:
            p1_piece_indexes = np.nonzero(pieces[:] == 1)[0]
            p2_piece_indexes = np.nonzero(pieces[:] == -1)[0]
        for r in range(0, 11):
            row_val = r
            linetab = r - 4
            if (r <= 5):
                linetab = 6 - r
            for t in range(0, linetab):
                out += "   "
            if r > 5:
                row_val -= reverse_index
                reverse_index += 2
            for c in range(0, lengths[row_val]):
                isEnd = c == lengths[row_val] - 1
                p2_piece = index == p2_piece_indexes[:]
                p1_piece = index == p1_piece_indexes[:]
                arr1 = np.array([0, 1, 2, 3, 4, 5])
                if np.sum(p2_piece):
                    out += f" 1_{arr1[p2_piece].item()}  "
                elif np.sum(p1_piece):
                    out += f" 2_{arr1[p1_piece].item()}  "
                else:
                    out += "  -   "
                index += 1
                if isEnd:
                    out += "\n"
                    break
        print("----------------------------------------")
        print(out, end="")
        print("----------------------------------------")