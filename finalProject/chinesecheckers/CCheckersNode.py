


class Node:

    def __init__(self, board, parent=None):
        self.state = board
        self.parent = parent
        self.children = []
        self.wins = 0
        self.visits = 0

    def expand(self):
        # logic to create child nodes
        pass

    def simulate(self):
        # logic to simulate a game from this state
        pass

    def backpropagate(self, result):
        # logic to update node statistics
        pass

    def is_fully_expanded(self):
        # logic to check if all child nodes have been created
        return len(self.children) == len(self.state.get_legal_moves())

    def best_child(self, c_param=1.4):
        # logic to select the best child node using the UCB1 formula
        pass

    def is_terminal(self):
        return self.state.is_game_over()