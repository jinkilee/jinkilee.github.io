import numpy as np
import torch
from transformers.modeling_albert import AlbertModel, AlbertAttention
from transformers.configuration_albert import AlbertConfig
from utils import set_seeds

set_seeds(100)
conf = AlbertConfig(
	embedding_size=20,
	vocab_size=10,
	hidden_size=40,			# H
	intermediate_size=40*4,	# 4H
	max_position_embeddings=15,
	layer_norm_eps=1e-6,
	num_hidden_layers=6,
	num_attention_heads=8,
)

# make random ALBERT input
np.random.seed(102)
n_batch = 3
inp = np.random.randint(0, conf.vocab_size, (n_batch, 10))
inp[:,0] = 1
inp[:,-3:] = 0
inp = torch.LongTensor(inp)

# make model
#model = AlbertAttention(conf)
model = AlbertModel(conf)
o = model(inp)
out = o[0]
print(out.sum(), out.shape)

