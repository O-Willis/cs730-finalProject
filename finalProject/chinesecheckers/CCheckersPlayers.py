import random
from .CCheckersNode import Node
from .CCheckersLogic import *
from copy import deepcopy


class HumanPlayer:

    def __init__(self, game):
        self.game = game

    def play(self, board, player):
        valid = self.game.getValidMoves(board, player)  # Get valid moves as list
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

            if entered_input is True:
                break

        return [piece, user_move]


class RandPlayer:

    def __init__(self, game):
        self.game = game
        self.threshold = 10

    def play(self, board, player):
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

class MinMaxPlayer:
    def __init__(self, game):
        self.game = game

    def play(self, board, player):
        # calling minimax and waiting action information
        _, pieceToMove, nextIndex = self.minimax(board, player, 2, player, True)
        return [pieceToMove, nextIndex]

    def minimax(self, board, player, maxDepth, playerHeuristic, maxP):
        if maxDepth == 0 or self.game.getGameEnded(board, player) != 0:
            return [self.game.getScore(board, playerHeuristic), None, None]

        if maxP: # maximizing player
            bestValue = float('-inf')
            piece = -1
            index = -1
            valids = self.game.getValidMoves(board, player)

            randomListMax = []
            for i in range(6):
                for j in range(len(valids[i])):
                    originalBoard = deepcopy(board)
                    board, _ = self.game.getNextState(board, player, [i,valids[i][j]])
                    actionValue, _, _ = self.minimax(board, -player, maxDepth - 1, playerHeuristic, False)

                    if actionValue == bestValue:
                        bestValue = actionValue
                        index = valids[i][j]
                        piece = i
                        act = [index, piece, bestValue]
                        randomListMax.append(act)

                    if actionValue > bestValue:
                        randomListMax = []
                        bestValue = actionValue
                        index = valids[i][j]
                        piece = i

                    board = originalBoard

            if len(randomListMax) > 0:
                actionInd = random.randint(0, len(randomListMax)-1)
                return randomListMax[actionInd][2], randomListMax[actionInd][1], randomListMax[actionInd][0]

            return [bestValue, piece, index]

        else: # minimizing player
            piece = -1
            index = -1
            bestValue = float('inf')
            valids = self.game.getValidMoves(board, player)

            randomListMin = []
            for i in range(6):
                for j in range(len(valids[i])):
                    originalBoard = deepcopy(board)
                    board, _ = self.game.getNextState(board, player, [i, valids[i][j]])
                    actionValue, _, _ = self.minimax(board, -player, maxDepth - 1, playerHeuristic, True)

                    if actionValue == bestValue:
                        bestValue = actionValue
                        index = valids[i][j]
                        piece = i
                        act = [index, piece, bestValue]
                        randomListMin.append(act)

                    if actionValue < bestValue:
                        randomListMin = []
                        bestValue = actionValue
                        index = valids[i][j]
                        piece = i

                    board = originalBoard

            if len(randomListMin) > 0:
                actionInd = random.randint(0, len(randomListMin)-1)
                return randomListMin[actionInd][2], randomListMin[actionInd][1], randomListMin[actionInd][0]

            return [bestValue, piece, index]

class AlphaBetaPlayer:
    def __init__(self, game):
        self.game = game

    def play(self, board, player):
        alpha = float('-inf')
        beta = float('inf')
        _, pieceToMove, nextIndex = self.minimax(board, player, 4, player, True, alpha, beta)
        return [pieceToMove, nextIndex]

    def minimax(self, board, player, maxDepth, playerHeuristic, maxP, alpha, beta):
        if maxDepth == 0 or self.game.getGameEnded(board, player) != 0:
            return [self.game.getScore(board, playerHeuristic), None, None]

        if maxP: # maximizing player
            bestValue = float('-inf')
            piece = -1
            index = -1
            valids = self.game.getValidMoves(board, player)

            isDone = False
            for i in range(6):
                for j in range(len(valids[i])):
                    originalBoard = deepcopy(board)
                    board, _ = self.game.getNextState(board, player, [i,valids[i][j]])
                    actionValue, _, _ = self.minimax(board, -player, maxDepth - 1, playerHeuristic, False, alpha, beta)

                    if actionValue > bestValue:
                        bestValue = actionValue
                        alpha = max(alpha, bestValue)
                        index = valids[i][j]
                        piece = i
                        if beta <= alpha:
                            isDone = True
                            break

                    board = originalBoard

                if isDone:
                    break

            return [bestValue, piece, index]

        else: # minimizing player
            piece = -1
            index = -1
            bestValue = float('inf')
            valids = self.game.getValidMoves(board, player)

            isDone = False
            for i in range(6):
                for j in range(len(valids[i])):
                    originalBoard = deepcopy(board)
                    board, _ = self.game.getNextState(board, player, [i, valids[i][j]])
                    actionValue, _, _ = self.minimax(board, -player, maxDepth - 1, playerHeuristic, True, alpha, beta)

                    if actionValue < bestValue:
                        bestValue = actionValue
                        index = valids[i][j]
                        piece = i
                        beta = min(beta, bestValue)
                        if beta <= alpha:
                            isDone = True
                            break

                    board = originalBoard
                if isDone:
                    break

            return [bestValue, piece, index]

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
        action = opposing_player(temp_state, temp_player)
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

    def play(self, state, player):
        opposing_player = RandPlayer(self.game).play
        # root = createNode(self.game, state, player, None, None)
        root = Node(self.game, state, player, None, None)

        for i in range(self.args['numMCTSSims']):  # Iteration for loop
            selection(root, opposing_player)
        return root.best_child().action
