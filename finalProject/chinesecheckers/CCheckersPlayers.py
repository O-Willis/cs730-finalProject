import numpy as np
from finalProject.gui import *
from finalProject.chinesecheckers.CCheckersNode import Node
from finalProject.chinesecheckers.CCheckersLogic import *
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

            # highlighted_moves, temp_select = draw_board(display_surface, board, player, highlighted_moves, selected_pit)
            # pg.display.update()
            # if temp_select != -1:
            #     selected_pit = temp_select
            # user_move = -1
            # for event in pg.event.get():
            #
            #     if event.type == pg.MOUSEBUTTONDOWN:
            #         position = pg.mouse.get_pos()
            #         highlighted_moves, temp_select = draw_board(display_surface, board, player, highlighted_moves, selected_pit)
            #         pg.display.update()
            #         # piece, user_move = [int(x) for x in a.split(' ')]
            #         piece = int(piece)
            #         if piece != -1:  # -1 will be the optional termination command
            #             user_move = int(user_move)
            #             if user_move in valid[piece]:
            #                 break
            #             else:
            #                 print("Incorrect input!!")
            #             # if piece < 0 or piece > 6:
            #
            #             # if isMovingPiece(event.pos):
            #
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

            if entered_input is True:
                break

        return [piece, user_move]


class RandPlayer:

    def __init__(self, game):
        self.game = game
        self.threshold = 10

    def play(self, display_surface, board, player):
        player_index = 1 if player == 1 else 0
        p_pieces = board.pieces[player_index]
        valid = self.game.getValidMoves(board, player)
        piece = self.get_valid_piece(valid)  # ensure that the valid array is not empty at index 'piece'
        move_index = np.random.randint(len(valid[piece]))
        while not self.is_better_move(player, board, p_pieces[piece], valid[piece][move_index]):
            piece = self.get_valid_piece(valid)
            move_index = np.random.randint(len(valid[piece]))
        # time.sleep(0.5)
        return [piece, valid[piece][move_index]]

    def get_valid_piece(self, valid):
        cur_piece = np.random.randint(self.game.getActionSize())
        while len(valid[cur_piece]) == 0:
            cur_piece = np.random.randint(self.game.getActionSize())
        return cur_piece

    def is_better_move(self, player, board, current_piece_index, valid_move_index):
        if player == 1:
            cur_piece_score = scorePlayer1[current_piece_index][0]
            valid_move_score = scorePlayer1[valid_move_index][0]
        else:
            cur_piece_score = scorePlayer2[current_piece_index][0]
            valid_move_score = scorePlayer2[valid_move_index][0]
        return valid_move_score >= cur_piece_score


def getPrioritizedPieces(board, player):
    playerInd = 1 if player == 1 else 0
    notPrioritized = []
    prioritizedPieces = []
    for i in range(6):
        playerIndex = board.pieces[playerInd, i]
        if np.isin(playerIndex, board.goal[playerInd]):
            notPrioritized.append(i)
        else:
            prioritizedPieces.append(i)

    prioritizedPieces += notPrioritized
    return prioritizedPieces


class MinMaxPlayer:

    def __init__(self, game):
        self.game = game

    def play(self, display_surface, board, player):
        valids = self.game.getValidMoves(board, 1)
        # TODO IMPLEMENT MCTS HERE

def selection(node, opposing_player):
    result = 1
    while not node.is_terminal():
        is_leaf = node.is_leaf()
        node.visits += is_leaf
        expand(node)
        node = node.best_child()
        if is_leaf:
            node, result = simulate(node, opposing_player)
            break
    backpropagate(node, result)

def expand(node):  # logic to create child nodes
    if not node.is_fully_expanded():
        rand_move = np.random.randint(len(node.untried_moves))
        action = node.untried_moves[rand_move]  # Random selection is here
        board_copy = node.state.duplicate()
        new_state, next_player = node.game.getNextState(board_copy, node.cur_player, action)
        child_node = Node(node.game, new_state, node.cur_player, node, action)
        node.children.append(child_node)
        node.untried_moves.remove(action)

def simulate(node, opposing_player):  # logic to simulate a game from this state
    is_first_move = True
    while not node.game.getGameEnded(node.state, node.cur_player):
        if is_first_move:
            temp_state, temp_player = node.game.getNextState(node.state, node.cur_player, node.action)
            is_first_move = False
        else:
            random_move = node.get_contrained_move()
            temp_state, temp_player = node.game.getNextState(node.state, node.cur_player, random_move)
            child_node = Node(node.game, temp_state, temp_player, node, random_move)
            node.children.append(child_node)
            node = child_node
        action = opposing_player(None, temp_state, temp_player)
        node.state, node.cur_player = node.game.getNextState(temp_state, temp_player, action)
    return node, node.game.getGameEnded(node.state, node.cur_player)

def backpropagate(node, result):  # logic to update node statistics
    while node.parent:
        node.visits += 1
        node.wins += result
        node = node.parent
    node.visits += 1
    node.wins += result
    return node


class MCTSPlayer:

    def __init__(self, game, args):
        self.game = game
        self.args = args
        self.root = None

    def play(self, display_surface, state, player):
        opposing_player = RandPlayer(self.game).play
        # root = createNode(self.game, state, player, None, None)
        root = Node(self.game, state, player, None, None)

        for i in range(self.args.numMCTSSims):  # Iteration for loop
            selection(root, opposing_player)
        return root.best_child().action
