import sys

import Arena
from MCTS import MCTS
from finalProject.gui_2 import *
from chinesecheckers.CCheckersPlayers import *
from chinesecheckers.CCheckersGame import CCheckersGame as Game
# from chinesecheckers.pytorch.NNet import NNetWrapper as Net

import numpy as np
from utils import *

from pygame.constants import *
import pygame
from gui_2 import *  # Contains gui elements

def failCode(errorCode):
    if errorCode == 0:
        print("ERROR: INVALID INPUT")
        exit(1)
    elif errorCode == 1:
        print(f"NOTICE: input does not match the required -play command format")
        exit(0)

def getPlayers(type):
    humanPlayer = HumanPlayer(game).play
    rp = RandPlayer(game).play
    minimaxPlayer = MinMaxPlayer(game).play
    mctsPlayer = MCTSPlayer(game).play
    player1 = rp
    player2 = rp
    if type == 1:  # default 0 represents AI vs AI
        if 'minimax' in sys.argv:
            player1 = minimaxPlayer  # TODO change this later
            player2 = minimaxPlayer
        elif 'mcts' in sys.argv:
            player1 = mctsPlayer  # TODO change this later
            player2 = mctsPlayer
            n2p = 0
            # n2 = NNet(game)  TODO add this in after MCTS standalone + NNet Implementation
            # n2.load_checkpoint('./pretrained_models/othello/pytorch/', '8x8_100checkpoints_best.pth.tar')
            # args2 = dotdict({'numMCTSSims': 50, 'cpuct': 1.0})
            # mcts2 = MCTS(g, n2, args2)
            # n2p = lambda x: np.argmax(mcts2.getActionProb(x, temp=0))

            # player2 = n2p
    if type == 2:
        player2 = humanPlayer
        if 'minimax' in sys.argv:
            player1 = minimaxPlayer  # TODO change this later
        elif 'mcts' in sys.argv:
            player1 = player1  # TODO change this later
        elif 'rand' in sys.argv:
            player1 = rp  # TODO change this later
        else:
            player1 = humanPlayer

    return player1, player2

print(f"Arguments count: {len(sys.argv)}")
battle_type = 0
if '-play' in sys.argv:
    if len(sys.argv) < 2:
        failCode(0)
    if len(sys.argv) == 2:
        battle_type = 0
    elif len(sys.argv) > 2:
        battle_type = int(sys.argv[2])

game = Game(6)
player1, player2 = getPlayers(battle_type)

n1 = 0
# n1 = NNet(game)
# n1.load_checkpoint('./pretrained_models/', 'chinesecheckers_easy.tar')
# args1 = dotdict({'numMCTSSims': 50, 'cpuct':1.0})
# mcts1 = MCTS(game, n1, args1)  # TODO N1 WILL CAUSE PROBLEMS!!
# n1p = lambda x: np.argmax(mcts1.getActionProb(x, temp=0))

arena = Arena.Arena(player1, player2, game, display=Game.display)

result = arena.playGame(verbose=True)
print(result)
#print(arena.playGames(2, verbose=True))
