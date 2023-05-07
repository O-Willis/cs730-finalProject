import numpy as np
from finalProject.gui import *
from finalProject.chinesecheckers.CCheckersNode import Node
import pygame as pg
import sys
import time

class HumanPlayer:

    def __init__(self, game):
        self.game = game

    def play(self, display_surface, board, player):
        valid = self.game.getValidMoves(board, player)  # Get valid moves as list
        # pieces = self.game.getNumpyFromCannonical(board)
        highlighted_moves = set()
        selected_pit = -1
        entered_input = False
        while True:  # While loop for input

            a = input()

            piece, user_move = [int(x) for x in a.split(' ')]
            piece = int(piece)
            if piece != -1:  # -1 will be the optional termination command
                user_move = int(user_move)
                if user_move in valid[piece]:
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

        return [piece, user_move]


class RandPlayer:

    def __init__(self, game):
        self.game = game
        self.threshold = 10

    def play(self, display_surface, board, player):
        player_index = 1 if player == 1 else 0
        p_pieces = board.pieces[player_index]
        valid = self.game.getValidMoves(board, player)
        threshold = np.random.randint(100)
        piece = self.get_valid_piece(valid)  # ensure that the valid array is not empty at index 'piece'
        move_index = np.random.randint(len(valid[piece]))
        while not self.is_better_move(valid, threshold, player, p_pieces, piece, move_index):
            piece = self.get_valid_piece(valid)
            move_index = np.random.randint(len(valid[piece]))
            threshold = np.random.randint(100)
        # time.sleep(0.5)
        return [piece, valid[piece][move_index]]

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
        cur_piece = np.random.randint(self.game.getActionSize())
        while len(valid[cur_piece]) == 0:
            cur_piece = np.random.randint(self.game.getActionSize())
        return cur_piece

    def is_better_move(self, valid, threshold, player, p_pieces, piece, move_index):
        is_above_threshold = threshold > self.threshold  # select any move rather than moving up the board
        # goals = self.game.getPlayerGoals(player)
        if player == 1:
            # is_piece_in_goal = self.piece_in_goal(goals, pieces, piece, player, valid[piece][move_index], 0)
            # if not is_piece_in_goal:
            #     return True
            if not is_above_threshold:
                return True
            return valid[piece][move_index] <= p_pieces[piece]
        else:
            # is_piece_in_goal = self.piece_in_goal(goals, pieces, piece, player, valid[piece][move_index], 5)
            # if not is_piece_in_goal:
            #     return True
            if not is_above_threshold:
                return True
            return valid[piece][move_index] >= p_pieces[piece]

class MinMaxPlayer:

    def __init__(self, game):
        self.game = game

    def play(self, display_surface, board, player):
        valids = self.game.getValidMoves(board, 1)
        # TODO IMPLEMENT MCTS HERE


class MCTSPlayer:

    def __init__(self, game, args):
        self.root = None
        self.game = game
        self.args = args

    def get_action(self, state):
        if self.root is None or state != self.root.state:
            self.root = Node(state)

        for i in range(self.args.numMCTSSims):
            node = self.root
            while not node.is_fully_expanded() and not node.is_terminal():
                node = node.expand()

            if node.is_terminal():
                result = node.reward()
            else:
                child = node.best_child()
                result = child.simulate()
            node.backpropagate(result)

        best_child = self.root.best_child(c_param=0)
        return best_child.action

    def get_legal_moves(self):
        legal_moves = []
        # logic to get all legal moves
        return legal_moves

    def make_move(self, move):
        self.player_turn = 2 if self.player_turn == 1 else 1

    def is_game_over(self):
        # logic to check if the game is over
        # return True if the game is over, False otherwise
        return False  # replace with actual logic

    def play(self, display_surface, board, player):
        valids = self.game.getValidMoves(board, 1)
        # TODO IMPLEMENT MCTS HERE
