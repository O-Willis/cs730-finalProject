from __future__ import print_function
import sys
sys.path.append('..')

from finalProject.Game import Game
from .CCheckersLogic import *

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
        b = board.duplicate()
        legal_moves = b.get_legal_moves(player)
        return legal_moves

    def getGameEnded(self, board, player):
        b = board.duplicate()
        if b.is_game_over(player):  # Player can be represented by either 1 or -1
            return 1
        if b.is_game_over(-player):
            return -1
        else:
            return 0

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
    def display(board):
        print("----------------------------------------")
        print(str(board), end="")
        print("----------------------------------------")