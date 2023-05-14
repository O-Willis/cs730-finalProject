import sys

import Arena
from finalProject.gui_2 import *
from chinesecheckers.CCheckersPlayers import *
from chinesecheckers.CCheckersGame import CCheckersGame as Game

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

    if len(sys.argv) == 3:
        battle_type = 2

    elif len(sys.argv) > 2:
        battle_type = int(sys.argv[2])

game = Game(6)
humanPlayer = HumanPlayer(game).play
rp = RandPlayer(game).play
minimaxPlayer = MinMaxPlayer(game).play
alphaPlayer = AlphaBetaPlayer(game).play

# args = dotdict({'numMCTSSims': 10, 'cpuct': 1.0})
args = dotdict({'numMCTSSims': 150})
mcts = MCTSPlayer(game, args).play
#mctsPlayer = lambda x, _: np.argmax(mcts.getActionProb(x, -1, temp=0))
mctsPlayer = mcts

player1 = rp
player2 = rp
is_duplicate = False
if 'human' in sys.argv:  # normally sets player 2 to specified opponent
    player1 = humanPlayer
    if sys.argv.count('human') == 2:
        player2 = humanPlayer
if 'minimax' in sys.argv:
    player1 = minimaxPlayer
    if sys.argv.count('minimax') == 2:
        player2 = minimaxPlayer
elif 'mcts' in sys.argv:
    player1 = mctsPlayer
    if sys.argv.count('mcts') == 2:
        player2 = mctsPlayer
elif 'alpha' in sys.argv:  # TODO add this in after MCTS standalone + NNet Implementation
    player1 = alphaPlayer
    if sys.argv.count('alpha') == 2:
        player2 = alphaPlayer

arena = Arena.Arena(player1, player2, game, display=Game.display)

result = arena.playGame(verbose=True)
print(result)
#print(arena.playGames(2, verbose=True))
