import random
import numpy as np
from operator import index


# Visited node should not be expanded
# Can expand only one node at a time

class Node:

    def __init__(self, game, state, player, parent=None, action=None):
        self.game = game
        self.state = state  # changes when expanding
        self.cur_player = player
        self.action = action  # Action is a tuple (piece, move)
        self.parent = parent
        self.children = []
        moves = state.get_legal_moves(player)
        self.untried_moves = []
        for i in range(0, len(moves)):
            if len(moves[i]) == 0:
                continue
            for action in moves[i]:
                self.untried_moves.append((i, action))
        self.wins = 0
        self.visits = 0

    def __eq__(self, item):
        if isinstance(item, Node):
            return self.action == item.action and self.cur_player == item.cur_player
        try:
            # Accept any int-like thing
            return self.action == index(item)
        except TypeError:
            return NotImplemented

    def __hash__(self):
        return self.action

    def selection(self, opposing_player, move_len=10):
        move_len = self.get_node_move_len()
        if self.is_terminal():
            return self

        if self.visits == 0:
            self.visits += 1
            self.root, result = self.simulate(opposing_player)
            back_prop_node = self.root.backpropagate(result)
            if back_prop_node is None:
                x = 0
            return back_prop_node
        else:
            if not self.is_fully_expanded(move_len):
                self.expand()
            self = self.best_child()  # otherwise, check best child and traverse in
        # state is the current state (before action), and action is the action made from that state
        return self.selection(opposing_player, move_len)

    def expand(self):  # logic to create child nodes
        rand_move = np.random.randint(len(self.untried_moves))
        action = self.untried_moves[rand_move]  # Random selection is here
        new_state, next_player = self.game.getNextState(self.state, self.cur_player, action)
        child_node = Node(self.game, new_state, self.cur_player, self, action)
        self.children.append(child_node)
        self.untried_moves.remove(action)

    def best_child(self, c=1.4):
        # logic to select the best child node using the UCB1 formula
        best_child = None
        best_score = -float('inf')
        for child in self.children:
            if child.visits == 0:
                exploitation_term = 0
            else:
                exploitation_term = child.wins / child.visits
            exploration_term = c * np.sqrt(np.log(child.parent.visits) / self.visits)
            uct_score = exploitation_term + exploration_term
            if uct_score > best_score:
                best_child = child
                best_score = uct_score
        return best_child

    def simulate(self, opposing_player):  # logic to simulate a game from this state
        is_first_move = True
        while not self.game.getGameEnded(self.state, self.cur_player):
            if is_first_move:
                temp_state, temp_player = self.game.getNextState(self.state, self.cur_player, self.action)
                is_first_move = False
            else:
                random_move = self.get_contrained_move()
                temp_state, temp_player = self.game.getNextState(self.state, self.cur_player, random_move)
                child_node = Node(self.game, temp_state, temp_player, self, random_move)
                self.children.append(child_node)
                self = child_node

            action = opposing_player(None, temp_state, temp_player)
            self.state, self.cur_player = self.game.getNextState(temp_state, temp_player, action)
        return self, self.game.getGameEnded(self.state, self.cur_player)

    def backpropagate(self, result):  # logic to update node statistics
        while self.parent:
            self.visits += 1
            self.wins += result
            self = self.parent
        self.visits += 1
        self.wins += result
        return self

    def is_fully_expanded(self, legal_move_num):  # logic to check if all child nodes have been created
        return len(self.children) == legal_move_num

    def is_terminal(self): # logic to check if the game is over
        # return True if the game is over, False otherwise
        return self.game.getGameEnded(self.state, self.cur_player)

    def get_node_move_len(self):
        node_move_len = 0
        legal_node_moves = self.state.get_legal_moves(self.cur_player)
        for i in range(0, len(legal_node_moves)):
            node_move_len += len(legal_node_moves[i])
        return node_move_len

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
            cur_piece_score = self.state.scorePlayer1[current_piece_index][0]
            valid_move_score = self.state.scorePlayer1[valid_move_index][0]
        else:
            cur_piece_score = self.state.scorePlayer2[current_piece_index][0]
            valid_move_score = self.state.scorePlayer2[valid_move_index][0]
        return valid_move_score >= cur_piece_score


