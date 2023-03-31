import os
import sys
import time
import numpy as np
import tqdm import tqdm  # Shows progress bars for for loops

sys.path.append('../../')
from ...utils import *
from ...NeuralNet import NeuralNet

import torch
import torch.optim as optim

from .CCheckersNNet import CCHeckersNNet as ccnet

args = dotdict({  # Define neural network arguments
    'lr': 0.001,  # learning rate
    'dropout': 0.3,
    'epochs': 10,
    'batch_size': 64,
    'cuda': torch.cuda.is_available(),  # TODO FIGURE OUT THIS!!!
    'num_channels': 512,
})

class NNetWrapper(NeuralNet):
    def __init__(self, game):
        self.nnet = ccnet(game, args)
        self.board = game.getBoardSize()
        self.action_size = game.getActionSize()

        if args.cuda:  # TODO Understand this!!
            self.nnet.cuda()

    def train(self, examples):
        """
        :param examples: list of examples where each example is of form (board, pi, v)
        """
        optimizer = optim.Adam(self.nnet.parameters())  # TODO understand optim from pytorch

        for epoch in range(args.epochs):
            print('EPOCH ::: ' + str(epoch + 1))
            self.nnet.train()
            pi_losses = AverageMeter()
            v_losses = AverageMeter()

            batch_count = int(len(examples) / args.batch_size)

            t = tqdm(range(batch_count), desc="Training Net")
            for _ in t:
                sample_ids = np.random.randint(len(examples), size=args.batch_size)
                boards, pis, vs = list(zip(*[examples[i] for i in sample_ids]))
                boards = torch.FloatTensor(np.array(boards).astype(np.float64))
                target_pis = torch.FloatTensor(np.array(pis))
                target_vs = torch.FloatTensor(np.array(vs).astype(np.float64))

                # predict
                if args.cuda:
                    boards, target_pis, target_vs = \
                        boards.contiguous().cuda(), \
                            target_pis.contiguous().cuda(), \
                            target_vs.contiguous().cuda()

                # Computes the output
                out_pi, out_v = self.nnet(boards)
                l_pi = self.loss_pi(target_pis, out_v)
                l_v = self.loss_v(target_vs, out_v)
                total_loss = l_pi + l_v

                # record loss
                pi_losses.update(l_pi.item(), boards.size(0))
                v_losses.update(l_v.item(), boards.size(0))
                t.set_postfix(Loss_pi=pi_losses, Loss_v=v_losses)

                # compute gradient and do SGD step
                optimizer.zero_grad()
                total_loss.backward()
                optimizer.step()

    def predict(self, board):
        """
        board: np array with board
        """
        # timing
        start = time.time()

        # preparing input