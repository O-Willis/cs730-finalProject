import Arena
from MCTS import MCTS
from chinesecheckers.CCheckersGame import CCheckersGame as Game
from chinesecheckers.CCheckersPlayers import *
# from chinesecheckers.pytorch.NNet import NNetWrapper as Net

import numpy as np
from utils import *

from pygame.constants import *
import pygame
from board import *  # Contains gui elements

Human_Against_AI = True  # TODO Add logic for p v p or p vs AI
game = Game(6)
rp = RandPlayer(game).play
humanPlayer = HumanPlayer(game).play

n1 = 0
# n1 = NNet(game)
# n1.load_checkpoint('./pretrained_models/', 'chinesecheckers_easy.tar')
# args1 = dotdict({'numMCTSSims': 50, 'cpuct':1.0})
# mcts1 = MCTS(game, n1, args1)  # TODO N1 WILL CAUSE PROBLEMS!!
# n1p = lambda x: np.argmax(mcts1.getActionProb(x, temp=0))
n1p = HumanPlayer(game).play


if Human_Against_AI:
    player2 = humanPlayer  # TODO add checking for which AI algorithm to use
else:
    n2p = 0
    # n2 = NNet(game)  TODO add this in after MCTS standalone + NNet Implementation
    # n2.load_checkpoint('./pretrained_models/othello/pytorch/', '8x8_100checkpoints_best.pth.tar')
    # args2 = dotdict({'numMCTSSims': 50, 'cpuct': 1.0})
    # mcts2 = MCTS(g, n2, args2)
    # n2p = lambda x: np.argmax(mcts2.getActionProb(x, temp=0))

    player2 = n2p

arena = Arena.Arena(n1p, player2, game, display=Game.display)

result = arena.playGame(verbose=True)
print(result)
#print(arena.playGames(2, verbose=True))
