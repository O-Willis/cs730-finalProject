class AverageMeter(object):
    """From https://github.com/pytorch/examples/blob/master/imagenet/main.py"""
    """Intended to compute/store the average and current value"""

    def __init__(self):
        self.val = 0
        self.arg = 0
        self.sum = 0
        self.count = 0


    def __repr__(self):
        return f'{self.arg:.2e}'

    def update(self, val, n=1):
        self.val = val
        self.arg += val * n
        self.sum += n
        self.count = self.sum / self.count

class dotdict(dict):
    def __getattr__(self, name):
        return self[name]