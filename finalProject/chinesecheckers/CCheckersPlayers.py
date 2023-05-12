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
        while self.is_better_move(player, board, p_pieces[piece], valid[piece][move_index]):
            piece = self.get_valid_piece(valid)
            move_index = np.random.randint(len(valid[piece]))
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

    def is_better_move(self, player, board, current_piece_index, valid_move_index):
        if player == 1:
            cur_piece_score = board.scorePlayer1[current_piece_index][0]
            valid_move_score = board.scorePlayer1[valid_move_index][0]
        else:
            cur_piece_score = board.scorePlayer2[current_piece_index][0]
            valid_move_score = board.scorePlayer2[valid_move_index][0]
        return valid_move_score <= cur_piece_score
        # is_above_threshold = threshold > self.threshold  # select any move rather than moving up the board
        # # goals = self.game.getPlayerGoals(player)
        # if player == 1:
        #     # is_piece_in_goal = self.piece_in_goal(goals, pieces, piece, player, valid[piece][move_index], 0)
        #     # if not is_piece_in_goal:
        #     #     return True
        #     # if not is_above_threshold:
        #     #     return True
        #     return valid[piece][move_index] <= p_pieces[piece]
        # else:
        #     # is_piece_in_goal = self.piece_in_goal(goals, pieces, piece, player, valid[piece][move_index], 5)
        #     # if not is_piece_in_goal:
        #     #     return True
        #     # if not is_above_threshold:
        #     #     return True
        #     return valid[piece][move_index] >= p_pieces[piece]

class MinMaxPlayer:

    def __init__(self, game):
        self.game = game

    def play(self, display_surface, board, player):
        valids = self.game.getValidMoves(board, 1)
        # TODO IMPLEMENT MCTS HERE


class MCTSPlayer:

    def __init__(self, game, args):
        self.game = game
        self.args = args
        self.root = None


        self.Qsa = {}  # stores Q values for s,a
        self.Nsa = {}  # contains the num of times edge s,a was visited
        self.Ns = {}  # contains num times board s was visited
        self.Ps = {}  # stores policy

        self.Es = {}  # contains the bool for if a game has ended for board s
        self.Vs = {}  # contains the valid moves for board s

    def play(self, display_surface, state, player):
        if self.root is None or state != self.root.state:
            self.root = Node(self.game, state, player)
            self.root.visits += 1

        opposing_player = RandPlayer(self.game).play

        move_len = self.root.get_node_move_len()
        for i in range(self.args.numMCTSSims):  # Iteration for loop
            selected = self.root.selection(move_len, self.root)
            result = self.root.simulate(selected.action, opposing_player)
            self.root = self.root.backpropagate(result)

    def getActionProb(self, canonical, cur_player=-1, temp=1):

        for i in range(self.args.numMCTSSims):  # Iteration for loop
            self.search(canonical, cur_player)  # Select and expand

        s = self.game.stringRepresentation(canonical)
        counts = [self.Nsa[(s, a)] if (s, a) in self.Nsa else 0 for a in range(self.game.getActionSize())]

        if temp == 0:
            best_actions = np.array(np.argwhere(counts == np.max(counts))).flatten()
            best_action = np.random.choice(best_actions)
            probability = [0] * len(counts)
            probability[best_action] = 1
            return probability

        counts = [x ** (1. / temp) for x in counts]
        counts_sum = float(sum(counts))
        probs = [s / counts_sum for x in counts]
        return probs

    def search(self, board, cur_player):
        canonical = self.game.getCanonicalForm(board)
        s = self.game.stringRepresentation(canonical)

        if s not in self.Es:  # Check if state s is not ended
            self.Es[s] = self.game.getGameEnded(board, cur_player)
        if self.Es[s] != 0:  # If getGameEnded returned indication that a player won
            return -self.Es[s]  # Return opposite? FIXME idk whats happening here

        selected = self.select(board, s, cur_player)

        # if s not in self.Ps:  # If state is not in stored policy
        #     # self.Ps[s], v = self.nnet.predict
        #     self.Ps[]
        #     self.Ps[s] = self.predict(canonical)  # Select & Expand
        #     valids = self.game.getValidMoves(board, cur_player)
        #     self.Ps[s] = self.Ps[s] * valids
        #     sum_policy_s = np.sum(self.Ps[s])
        #     if sum_policy_s > 0:
        #         self.Ps[s] /= sum_policy_s  # normalize policy of state s
        #     else:
        #         # if a
        #         self.Ps[s] = self.Ps[s] + valids
        #         self.Ps[s] /= np.sum(self.Ps[s])
        #
        #     self.Vs[s] = valids
        #     self.Ns[s] = 0
        #     exit(0)  #  FIXME!!
        #     return 0

        valids = self.game.getValidMoves(board, cur_player)

        valids = self.Vs[s]
        cur_best = -float('inf')
        best_act = -1

        for a in range(self.game.getActionSize()):
            if valids[a]:
                if (s, a) in self.Qsa:
                    u = self.Qsa[(s, a)] + self.args.cpuct * self.Ps[s][a] * math.sqrt(self.Ns[s]) / (
                            1 + self.Nsa[(s, a)])
                else:
                    from finalProject.MCTS import EPS
                    u = self.args.cpuct * self.Ps[s][a] * math.sqrt(self.Ns[s] + EPS)

                if u > cur_best:
                    cur_best = u
                    best_act = a

        a = best_act
        next_s, next_player = self.game.getNextState(board, cur_player, a)
        next_s = self.game.getCanonicalForm(next_s, next_player)

        v = self.search(next_s, next_player)

        if (s, a) in self.Qsa:
            self.Qsa[(s, a)] = (self.Nsa[(s, a)] * self.Qsa[(s, a)] + v) / (self.Nsa[(s, a)] + 1)
            self.Nsa[(s, a)] += 1

        else:
            self.Qsa[(s, a)] = v
            self.Nsa[(s, a)] = 1

        self.Ns[s] += 1  # This is fine at end of search
        return -v

