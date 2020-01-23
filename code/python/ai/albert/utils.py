import numpy as np
import random
import torch
import os
from functools import reduce

'''
def set_seeds(seed):
    "set random seeds"
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
'''

def get_num_params(model):
	n_params = 0
	for param in model.parameters():
		param_shape = list(param.shape)
		n_params += reduce(lambda x, y: x*y, param_shape)
	return n_params

def set_seeds(seed):
    """ Set all seeds to make results reproducible (deterministic mode).
        When seed is a false-y value or not supplied, disables deterministic mode. """

    if seed:
        torch.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
        np.random.seed(seed)
        random.seed(seed)
        os.environ['PYTHONHASHSEED'] = str(seed)
    else:
        print("Running in non-deterministic mode")

