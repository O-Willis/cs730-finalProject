####################################
# By Oliver Willis & Hasan Polat   #
# Date: 3/30/2023                  #
####################################

import logging
import coloredlogs

from chinesecheckers.CCheckersGame import CCheckersGame as Game
#from chinesecheckers.pytorch.NNet import
from .utils import *

log = logging.getLogger(__name__)
coloredlogs.install(level='INFO')

"""
dotDict allows custom arguments to be inserted into program for NeuralNet
"""
args = dotdict({
    'numIters': 1000,
    'numSelfPlay': 100,
    'tempthreshold': 10,        # Key for tempThreshold before NNet finds value during training
    'updateThreshold': 0.6,     # Reward value for arena training for new neural net if threshold or more games are won
    'maxlenOfQueue': 100000,    #
    'numMCTSSims': 25,          # Used for Monte Carlo Tree Search on num game's moves
    'arenaCompare': 40,         # TODO Understand diff between threshold & arena value
    'cpuct': 1,                 # TODO understand this!!

    'checkpoint': './temp/',
    'load_model': False,
    'load_folder_file': ('/dev/models/8x100x50','best.pth.tar'),
    'numItersForTrainExamplesHistory': 20,

})

def main():
    log.info('Loading %s...', Game.__name__)
    game = Game(6)
    print(game.getStringRepresentation())

    #log.info('Loading %s...', nn.__name__)
    #nnet = nn(curGame)

    # log.info('Loading the Coach...')
    # c = Coach(curGame, nnet, args)
    
    # log.info("Loading 'trainExamples' from file...")
    # c.learn()

    # TODO load NeuralNet of curGame
    # TODO create Coach class w/ params (curGame, nnet, args


if __name__ == "__main__":
    main()