import numpy as np

"""

"""

class RandPlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board):
        a = np.random.randint(self.game.getActionSize())
        valids = self.game.getValidMoves(board, 1)
        while valids[a] != 1:
            a = np.random.randint(self.game.getActionSize())
        return a

class HumanCCheckersPlayer():
    def __int__(self, game):
        self.game = game

    def play(self, board):
        valid = self.game.getValidMoves(board, 1)  # Get valid moves as list
        for i in range(len(valid)):  # iterate over moves
            if valid[i]:  # TODO change in accordance to board implementation
                print(int(i/self.game.n), int(i%self.game.n))
        while True:  # While loop for input
            a = input()  # TODO change in accordance to board implementation

            x,y = [int(x) for x in a.split(' ')]
            a = self.game.n * x + y if x != -1 else self.game.n ** 2
            if valid[a]:
                break
            else:
                print('Invalid')

        return a