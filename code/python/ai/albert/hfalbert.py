import numpy as np
import torch
from config import Config
myconf = Config()

from utils import set_seeds
from transformers.modeling_albert import AlbertModel, AlbertAttention
from transformers.configuration_albert import AlbertConfig

conf = AlbertConfig(
	embedding_size=myconf.n_embed,
	vocab_size=myconf.n_vocab,
	hidden_size=myconf.n_hidden,			# H
	intermediate_size=myconf.n_hidden_ff,	# 4H
	max_position_embeddings=myconf.n_maxseq,
	layer_norm_eps=myconf.eps,
	num_hidden_layers=myconf.n_layers,
	num_attention_heads=myconf.n_head,
)

# make random ALBERT input
np.random.seed(102)
n_batch = 3
inp = np.random.randint(0, conf.vocab_size, (n_batch, 10))
inp[:,0] = 1
inp[:,-3:] = 0
inp = torch.LongTensor(inp)
print(inp)

set_seeds(100)
# make model
#model = AlbertAttention(conf)
model = AlbertModel(conf)
o = model(inp)
out = o[0]
print(out.sum(), out.shape)

