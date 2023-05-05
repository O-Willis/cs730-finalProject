import logging
import math

import numpy as np

EPS = 1e-8

log = logging.getLogger(__name__)

class MCTS():

    def __init__(self, game, nnet, args):
        self.game = game
        self.nnet = nnet
        self.args = args
        self.Qsa = {}  # stores Q values for s,a
        self.Nsa = {}  # contains the num of times edge s,a was visited
        self.Ns = {}  # contains num times board s was visited
        self.Ps = {}  # takes the initial policy of neural net

        self.Es = {}  # contains the bool for if a game has ended for board s
        self.Vs = {}  # contains the valid moves for board s

    def getActionProb(self, canonicalBoard, temp=1):

        for i in range(self.args.numMCTSSims):
            self.search(canonicalBoard)

        s = self.game.stringRepresentation(canonicalBoard)
        counts = [self.Nsa[(s, a)] if (s, a) in self.Nsa else 0 for a in range(self.game.getActionSize())]

        if temp == 0:
            bestActions = np.array(np.argwhere(counts == np.max(counts))).flatten()
            bestAction = np.random.choice(bestActions)
            probability = [0] * len(counts)
            probability[bestAction] = 1
            return probability

        counts = [x ** (1. / temp) for x in counts]
        counts_sum = float(sum(counts))
        probs = [s / counts_sum for x in counts]
        return probs


    def searchh(self, canonicalBoard):

        s = self.game.stringRepresentation(canonicalBoard)

        if s not in self.Es:
            self.Es[s] = self.game.getGameEnded(canonicalBoard, 1)
        if self.Es[s] != 0:
            return -self.Es[s]

        if s not in self.Ps:
            self.Ps[s], v = self.nnet.predict(canonicalBoard)
            valids = self.game.getValidMoves(canonicalBoard, 1)
            self.Ps[s] = self.Ps[s] * valids
            sum_Ps_s = np.sum(self.Ps[s])
            if sum_Ps_s > 0:
                self.Ps[s] /= sum_Ps_s
            else:
                log.error('All valid moves were masked, doing a workaround.')
                self.Ps[s] = self.Ps[s] + valids
                self.Ps[s] /= np.sum(self.Ps[s])

            self.Vs[s] = valids
            self.Vs[s] = 0
            return -v

        valids = self.Vs[s]
        cur_best = -float('inf')  # Set the best to the highest value
        best_act = -1

        for a in range(self.game.getActionSize()):
            if valids[a]:
                if (s, a) in self.Qsa:
                    u = self.Qsa[(s, a)] + self.args.cpuct + self.Ps[s][a] * math.sqrt(self.Ns[s]) / (1 + self.Nsa[(s, a)])
                else:
                    u =  self.args.cpuct + self.Ps[s][a] * math.sqrt(self.Ns[s] + EPS)

                if u > cur_best:
                    cur_best = u
                    best_act = a


        a = best_act
        next_s, next_player = self.game.getNextState(canonicalBoard, 1, a)
        next_s = self.game.getCanonicalForm(next_s, next_player)

        v = self.search(next_s)

        if (s, a) in self.Qsa:
            self.Qsa[(s, a)] = (self.Nsa[(s, a)] * self.Qsa[(s, a)] + v) / (self.Nsa[(s, a)] + 1)
            self.Nsa[(s, a)] += 1

        else:
            self.Qsa[(s, a)] = v
            self.Nsa[(s, a)] = 1

        self.Ns[s] += 1
        return -v

class MCTS_2():

    def __init__(self, game, args):
        self.game = game
        self.args = args
        self.Qsa = {}  # stores Q values for s,a
        self.Nsa = {}  # contains the num of times edge s,a was visited
        self.Ns = {}  # contains num times board s was visited

        self.Es = {}  # contains the bool for if a game has ended for board s
        self.Vs = {}  # contains the valid moves for board s

    def getActionProb(self, canonicalBoard, temp=1):

        for i in range(self.args.numMCTSSims):
            self.search(canonicalBoard)

        s = self.game.stringRepresentation(canonicalBoard)
        counts = [self.Nsa[(s, a)] if (s, a) in self.Nsa else 0 for a in range(self.game.getActionSize())]

        if temp == 0:
            bestActions = np.array(np.argwhere(counts == np.max(counts))).flatten()
            bestAction = np.random.choice(bestActions)
            probability = [0] * len(counts)
            probability[bestAction] = 1
            return probability

        counts = [x ** (1. / temp) for x in counts]
        counts_sum = float(sum(counts))
        probs = [s / counts_sum for x in counts]
        return probs


    def search(self, canonicalBoard):

        s = self.game.stringRepresentation(canonicalBoard)

        if s not in self.Es:
            self.Es[s] = self.game.getGameEnded(canonicalBoard, 1)
        if self.Es[s] != 0:
            return -self.Es[s]

        valids = self.Vs[s]
        cur_best = -float('inf')  # Set the best to the highest value
        best_act = -1

        for a in range(self.game.getActionSize()):
            if valids[a]:
                if (s, a) in self.Qsa:
                    u = self.Qsa[(s, a)] + self.args.cpuct + math.sqrt(self.Ns[s]) / (1 + self.Nsa[(s, a)])
                else:
                    u = self.args.cpuct + math.sqrt(self.Ns[s] + EPS)

                if u > cur_best:
                    cur_best = u
                    best_act = a


        a = best_act
        next_s, next_player = self.game.getNextState(canonicalBoard, 1, a)
        next_s = self.game.getCanonicalForm(next_s, next_player)

        v = self.search(next_s)

        if (s, a) in self.Qsa:
            self.Qsa[(s, a)] = (self.Nsa[(s, a)] * self.Qsa[(s, a)] + v) / (self.Nsa[(s, a)] + 1)
            self.Nsa[(s, a)] += 1

        else:
            self.Qsa[(s, a)] = v
            self.Nsa[(s, a)] = 1

        self.Ns[s] += 1
        return -v





