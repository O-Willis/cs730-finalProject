import random
import numpy as np
from operator import index
from finalProject.chinesecheckers.CCheckersLogic import *


# Visited node should not be expanded
# Can expand only one node at a time

cacheNodes = {}
base = np.array([[1.0, 40.0, 40.0**2, 40.0**3, 40.0**4, 40.0**5], [40.0**6, 40.0**7, 40.0**8, 40.0**9, 40.0**10, 40.0**11]])
def createNode(game, state, player, parent, action):
    # hash = (id(parent), np.sum(base * state.pieces))
    # hash = (id(parent), tuple(map(tuple, state.pieces)))
    # if hash in cacheNodes:
    #     assert (state.pieces == cacheNodes[hash].state.pieces).all()
    #     return cacheNodes[hash]
    node = Node(game, state, player, parent, action)
    # cacheNodes[hash] = node
    return node

class Node:

    def __init__(self, game, state, player, parent=None, action=None):
        self.game = game
        self.state = state
        # self.state.pieces = np.copy(state.pieces)  # changes when expanding
        self.cur_player = player
        self.action = action  # Action is a tuple (piece, move)
        self.parent = parent
        self.children = []
        moves = state.get_legal_moves(player)

        self.node_move_len = len(moves)
        for i in range(0, len(moves)):
            self.node_move_len += len(moves[i])

        self.untried_moves = []
        p_index = 1 if self.cur_player == 1 else 0
        p_pieces = self.state.pieces[p_index]
        for i in range(0, len(moves)):
            if len(moves[i]) == 0:
                continue
            for action in moves[i]:
                if self.get_better_move(self.cur_player, p_pieces[i], action):
                    self.untried_moves.append((i, action))
        self.wins = 0
        self.visits = 0

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value

    # def __eq__(self, item):
    #     if isinstance(item, Node):
    #         return base * self.state.pieces == base * item.state.pieces
    #     try:
    #         # Accept any int-like thing
    #         return base * self.state.pieces == base * item.state.pieces
    #     except TypeError:
    #         return NotImplemented
    #
    # def __hash__(self):
    #     return base * self.state.pieces

    def best_child(self, c=1.4):
        # logic to select the best child node using the UCB1 formula
        best_child = None
        best_score = -float('inf')
        if self.action is None:
            x = 0
        for child in self.children:
            if child.visits == 0:
                return child
            exploit_term = child.wins / child.visits
            cur_node_visits = max(1, self.visits)  # Makes sure visits is 1 even if its 0
            child_parent_visits = max(1, child.parent.visits)
            explore_term = c * np.sqrt(np.log(child_parent_visits) / cur_node_visits)
            uct_score = exploit_term + explore_term
            if uct_score > best_score:
                best_child = child
                best_score = uct_score
        return best_child

    def is_fully_expanded(self, legal_move_num):  # logic to check if all child nodes have been created
        return len(self.untried_moves) == 0

    def is_terminal(self):  # logic to check if the game is over
        # return True if the game is over, False otherwise
        return self.game.getGameEnded(self.state, self.cur_player)

    def get_node_move_len(self):
        return self.node_move_len

    def get_contrained_move(self):
        player_index = 1 if self.cur_player == 1 else 0
        valid_moves = self.game.getValidMoves(self.state, self.cur_player)
        player_pieces = self.state.pieces[player_index]
        piece = self.get_valid_rand_piece(valid_moves)
        move = np.random.randint(len(valid_moves[piece]))
        while not self.get_better_move(self.cur_player, player_pieces[piece], valid_moves[piece][move]):
            piece = self.get_valid_rand_piece(valid_moves)
            move = np.random.randint(len(valid_moves[piece]))
        return [piece, valid_moves[piece][move]]

    def get_valid_rand_piece(self, valid):
        cur_piece = np.random.randint(self.game.getActionSize())
        while len(valid[cur_piece]) == 0:
            cur_piece = np.random.randint(self.game.getActionSize())
        return cur_piece

    def get_better_move(self, player, current_piece_index, valid_move_index):  # This logic can be refactored BIG TIME
        if player == 1:
            cur_piece_score = scorePlayer1[current_piece_index][0]
            valid_move_score = scorePlayer1[valid_move_index][0]
        else:
            cur_piece_score = scorePlayer2[current_piece_index][0]
            valid_move_score = scorePlayer2[valid_move_index][0]
        return valid_move_score >= cur_piece_score


