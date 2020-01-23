import numpy as np
import torch
from model import AlbertModel
from utils import get_num_params
from config import Config

conf = Config()
np.random.seed(100)
n_batch = 3

# make random input
#inp = np.random.randint(0, conf.n_vocab, (n_batch, 10))
inp = np.random.random((n_batch, 10, conf.n_embed))
inp = torch.FloatTensor(inp)
print(inp.shape, inp.sum())

# define AlbertModel
transformer = AlbertModel(conf)

# output AlbertModel
out, pout = transformer(inp)
print(out.shape, pout.shape)
print(out.sum(), pout.sum())
