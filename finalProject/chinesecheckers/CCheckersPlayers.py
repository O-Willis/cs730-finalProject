import numpy as np
from finalProject.board import *
import pygame as pg
import sys
import time

class HumanPlayer:

    def __init__(self, game):
        self.game = game

    def play(self, display_surface, board, player):
        valid = self.game.getValidMoves(board, player)  # Get valid moves as list
        # pieces = self.game.getNumpyFromCannonical(board)
        for i in range(0, len(valid)):  # iterate over moves
            if valid[i]:
                print(f"{i}:{valid[i]}")
        highlighted_moves = set()
        selected_pit = -1
        entered_input = False
        while True:  # While loop for input

            a = input()

            piece, userMove = [int(x) for x in a.split(' ')]
            piece = int(piece)
            if piece != -1:  # -1 will be the optional termination command
                userMove = int(userMove)
                if userMove in valid[piece]:
                    break
                else:
                    print("Incorrect input!!")
            else:
                break

            # highlighted_moves, temp_select = draw_board(display_surface, pieces, player, highlighted_moves, selected_pit)
            # pg.display.update()
            # if temp_select != -1:
            #     selected_pit = temp_select
            #
            # for event in pg.event.get():
            #
            #     if event.type == pg.MOUSEBUTTONDOWN:
            #         position = pg.mouse.get_pos()
            #         highlighted_moves, temp_select = draw_board(display_surface, board, player, highlighted_moves, selected_pit)
            #         pg.display.update()
            #         # piece, userMove = [int(x) for x in a.split(' ')]
            #         piece = int(piece)
            #         if piece != -1:  # -1 will be the optional termination command
            #             userMove = int(userMove)
            #             if userMove in valid[piece]:
            #                 break
            #             else:
            #                 print("Incorrect input!!")
            #             # if piece < 0 or piece > 6:
            #
            #             # while userMove not in board.get_legal_moves(player_turn)[piece]:
            #             #     print(f"current move: {piece} to {userMove}")
            #             #     piece, userMove = input("That is not a valid piece move! Please retry!: ").split()
            #             #     piece = int(piece)
            #             #     userMove = int(userMove)
            #             #
            #             # if board.execute_move(player_turn, piece, userMove) == True:
            #             #     player_turn = (player_turn % 2) + 1
            #
            #         else:
            #             entered_input = True
            #             break
            #
            # if entered_input is True:
            #     break

        return [piece, userMove]


class RandPlayer:

    def __init__(self, game):
        self.game = game

    def play(self, board):
        a = np.random.randint(self.game.getActionSize())
        valids = self.game.getValidMoves(board, 1)
        while valids[a] != 1:
            a = np.random.randint(self.game.getActionSize())
        return a

class MinMaxPlayer:

    def __int__(self, game):
        self.game = game

    def play(self, board):
        valids = self.game.getValidMoves(board, 1)
        # TODO IMPLEMENT MCTS HERE


class MCTSPlayer:
    def __int__(self, game):
        self.game = game

    def play(self, board):
        valids = self.game.getValidMoves(board, 1)
        # TODO IMPLEMENT MCTS HERE
