import numpy as np
from finalProject.gui import *
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
        self.threshold = 10

    def play(self, display_surface, board, player):
        valid = self.game.getValidMoves(board, player)
        chanceNum = np.random.randint(100)
        piece = self.get_valid_piece(valid)  # ensure that the valid array is not empty at index 'piece'
        moveInd = np.random.randint(len(valid[piece]))
        while not self.is_better_move(valid, chanceNum, player, piece, moveInd):
            piece = self.get_valid_piece(valid)
            moveInd = np.random.randint(len(valid[piece]))
            chanceNum = np.random.randint(100)
        # time.sleep(0.5)
        return [piece, valid[piece][moveInd]]

    # def piece_in_goal(self, goal, pieces, piece, player, move, goal_index):
    #     if (player == -1 and goal_index == 5) and (move == goal[goal_index] or pieces[piece] == goal[goal_index]):
    #         x = 0
    #     if (player == 1 and goal_index == 0) and (move == goal[goal_index] or pieces[piece] == goal[goal_index]):
    #         x = 0
    #     if goal_index == 6:  # If all pieces are in goal state, then return True for win condition
    #         return True
    #     elif move == goal[goal_index]:
    #         return True
    #     elif pieces[piece] == goal[goal_index]:  # If current piece is in goal, skip piece
    #         return False
    #     elif np.isin(goal[goal_index], pieces):  # If piece exists in the desired goal, then check other goal_indexes
    #         return self.piece_in_goal(goal, pieces, piece, player, move, goal_index+player)  # player is either -1 (p2) or +1 (1p)
    #     else:  # otherwise, return false
    #         return False

    def get_valid_piece(self, valid):
        curPiece = np.random.randint(self.game.getActionSize())
        while len(valid[curPiece]) == 0:
            curPiece = np.random.randint(self.game.getActionSize())
        return curPiece

    def is_better_move(self, valid, chanceNum, player, piece, move_index):
        pieces = self.game.getPlayerPieces(player)
        is_above_threshold = chanceNum > self.threshold  # select any move rather than moving up the board
        # goals = self.game.getPlayerGoals(player)
        if player == 1:
            # is_piece_in_goal = self.piece_in_goal(goals, pieces, piece, player, valid[piece][move_index], 0)
            # if not is_piece_in_goal:
            #     return True
            if not is_above_threshold:
                return True
            return valid[piece][move_index] <= pieces[piece]
        else:
            # is_piece_in_goal = self.piece_in_goal(goals, pieces, piece, player, valid[piece][move_index], 5)
            # if not is_piece_in_goal:
            #     return True
            if not is_above_threshold:
                return True
            return valid[piece][move_index] >= pieces[piece]

class MinMaxPlayer:

    def __init__(self, game):
        self.game = game

    def play(self, display_surface, board, player):
        valids = self.game.getValidMoves(board, 1)
        # TODO IMPLEMENT MCTS HERE


class MCTSPlayer:

    def __init__(self, game):
        self.game = game

    def play(self, display_surface, board, player):
        valids = self.game.getValidMoves(board, 1)
        # TODO IMPLEMENT MCTS HERE
