from __future__ import print_function
from finalProject.Game import Game
from finalProject.chinesecheckers.CCheckersLogic import *
from finalProject.gui_2 import *


class CCheckersGame(Game):
    pit_content = {
        -1: "2",
        +0: "-",
        +1: "1"
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
        b = Board(self.n)
        return b  # In array form for neural network

    def getBoardSize(self):
        return self.n

    def getActionSize(self):
        return 6  # Constant for number of possible moves from 1 pit

    def getNextState(self, board, player, action):
        # For player taking an action on board
        if action == [-1, -1]:
            return (board, -player)
        b = board.duplicate()
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
        b = board.duplicate()
        legal_moves = b.get_legal_moves(player)
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
        b = board.duplicate()
        if b.is_game_over(player):  # Player can be represented by either 1 or -1
            return 1
        if b.is_game_over(-player):
            return -1
        else:
            return 0

    def getCanonicalForm(self, board):
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

    def stringRepresentation(self, board):
        """
        Input:
            board: current board
        Returns:
            boardString: a quick conversion of board to a string format.
                         Required by MCTS for hashing.
        """
        return board.tostring()

    ''' 
    ========= Score of Player 1 =========
                      0      goal
                   -1  -1  
                 -2  -2  -2  
               -3  -3  -3  -3  
             -4  -4  -4  -4  -4  
           -5  -5  -5  -5  -5  -5  
             -6  -6  -6  -6  -6  
               -7  -7  -7  -7  
                 -9  -9  -9  
                  -12 -12  
                    -16    starting

    ========= Score of Player 2 =========
                    -16     starting
                  -12 -12  
                 -9  -9  -9  
               -7  -7  -7  -7  
             -6  -6  -6  -6  -6  
           -5  -5  -5  -5  -5  -5  
             -4  -4  -4  -4  -4  
               -3  -3  -3  -3  
                 -2  -2  -2  
                   -1  -1  
                      0     goal 
    '''

    def getScore(self, board, player):
        player_index = 1 if player == 1 else 0
        score = 0
        b = board.duplicate()
        for i in range(6):
            if player_index:
                score += scorePlayer1[b.pieces[player_index, i]][0]
                score -= scorePlayer2[b.pieces[player_index-1, i]][0]
            else:
                score -= scorePlayer1[b.pieces[player_index+1, i]][0]
                score += scorePlayer2[b.pieces[player_index, i]][0]
        return score

    @staticmethod
    def display(display, board, cannonical):
        display_layout(display, cannonical)
        print("----------------------------------------")
        print(str(board), end="")
        print("----------------------------------------")