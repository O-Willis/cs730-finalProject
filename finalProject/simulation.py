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

print(f"Arguments count: {len(sys.argv)}")
battle_type = 0
if '-play' in sys.argv:
    if len(sys.argv) < 2:
        failCode(0)
    elif len(sys.argv) > 2:
        battle_type = int(sys.argv[2])

game = Game(6)
humanPlayer = HumanPlayer(game).play
rp = RandPlayer(game).play
minimaxPlayer = MinMaxPlayer(game).play

args = dotdict({'numMCTSSims': 50, 'cpuct': 1.0})
mcts = MCTSPlayer(game, args).play
#mctsPlayer = lambda x, _: np.argmax(mcts.getActionProb(x, -1, temp=0))
mctsPlayer = mcts

player1 = rp
player2 = rp

if 'human' in sys.argv:  # normally sets player 2 to specified opponent
    player1 = humanPlayer
elif 'minimax' in sys.argv:
    player1 = minimaxPlayer
elif 'mcts' in sys.argv:
    player1 = mctsPlayer
elif 'alpha' in sys.argv:  # TODO add this in after MCTS standalone + NNet Implementation
    x = 0
    # neural = NNet(game)
    # neural.load_checkpoint('./pretrained_models/pytorch/', '100checkpoints_best.pth.tar')
    # mcts1 = MCTS(game, neural, args)

if battle_type == 2:  # default 0 represents AI vs AI
    if 'minimax' in sys.argv:
        player2 = minimaxPlayer
    elif 'mcts' in sys.argv:
        player2 = mctsPlayer
    elif 'alpha' in sys.argv:  # TODO add this in after MCTS standalone + NNet Implementation
        x = 0
        # neural = NNet(game)
        # neural.load_checkpoint('./pretrained_models/pytorch/', '100checkpoints_best.pth.tar')
        # mcts2 = MCTS(game, neural, args)
    else:
        player2 = humanPlayer

arena = Arena.Arena(player1, player2, game, display=Game.display)

result = arena.playGame(verbose=True)
print(result)
#print(arena.playGames(2, verbose=True))
