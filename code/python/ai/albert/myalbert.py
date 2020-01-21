import torch
import torch.nn as nn
import numpy as np
import math
from functools import reduce
from config import Config
from utils import set_seeds

set_seeds(100)
conf = Config()

def get_num_params(model):
	n_params = 0
	for param in model.parameters():
		param_shape = list(param.shape)
		n_params += reduce(lambda x, y: x*y, param_shape)
	return n_params

class ContextDependentEmbedding(nn.Module):
	def __init__(self, conf, use_positinal_embedding=True):
		super().__init__()
		# context-independent embedding
		self.embedded_word = nn.Embedding(conf.n_vocab, conf.n_embbed)
		
		# FIXME: n_embbed -> n_embed
		self.pos_emb_vector = nn.Embedding(conf.n_maxseq, conf.n_embbed)
		self.use_positinal_embedding = use_positinal_embedding
		self.norm = nn.LayerNorm(conf.n_embbed, eps=conf.eps)
		self.drop = nn.Dropout(conf.dropout_rate)
		
	def forward(self, x):
		n_seq = x.size()[1]
		ci_emb = self.embedded_word(x)
		
		if self.use_positinal_embedding:
			cd_emb = ci_emb + self.pos_emb_vector.weight[:n_seq]
			cd_emb = self.drop(self.norm(cd_emb))
		return cd_emb

class AlbertMultiHeadAttention(nn.Module):
	def __init__(self, conf):
		super().__init__()
		torch.manual_seed(7)
		
		self.query = nn.Linear(conf.n_hidden, conf.n_hidden)
		self.key = nn.Linear(conf.n_hidden, conf.n_hidden)
		self.value = nn.Linear(conf.n_hidden, conf.n_hidden)
		self.attention_size = conf.attention_size
		self.hidden_size = conf.n_hidden
		self.n_head = conf.n_head
		self.softmax = torch.nn.Softmax(dim=-1)
		self.layer_norm = nn.LayerNorm(conf.n_hidden, eps=conf.eps)
		
		#torch.manual_seed(7)
		#self.dense = nn.Linear(conf.n_hidden, conf.n_hidden)
		
		torch.manual_seed(7)
		self.dense = nn.Linear(conf.n_hidden, conf.n_hidden)
		self.attention_head_size = conf.n_hidden // conf.n_head
		
	def split_tensor(self, x):
		x_split = torch.split(x, self.attention_size, dim=2)
		return torch.stack(x_split, dim=-2)
		
	#def merge_tensor(self, x):
	#	s = x.size()[-2]
	#	return torch.cat([x[:,:,i,:] for i in range(s)], dim=-1)
	
	def merge_last_ndims(self, x, n_dims):
		s = x.size()
		return x.view(*s[:-n_dims], -1)
	
	def forward(self, x):
		q = self.query(x)
		k = self.key(x)
		v = self.value(x)
		q, k, v = list(map(lambda x: self.split_tensor(x).transpose(1,2), [q, k, v]))

		score = (q @ k.transpose(-2,-1)) / np.sqrt(self.attention_size)
		prob = self.softmax(score)
		
		# FIXME: why contiguous?
		context = (prob @ v).transpose(1,2).contiguous()
		#w = (
		#	self.dense.weight.t()
		#	.view(self.n_head, self.attention_head_size, self.hidden_size)
		#	.to(context.dtype)
		#)
		#b = self.dense.bias.to(context.dtype)
		#projected_context = torch.einsum("bfnd,ndh->bfh", context, w) + b
		projected_context = self.dense(self.merge_last_ndims(context, 2))
		#print(projected_context.sum())
		
		# do something about `mask`
		hidden = self.layer_norm(x + projected_context)
		return hidden


def gelu_new(x):
	""" Implementation of the gelu activation function currently in Google Bert repo (identical to OpenAI GPT).
		Also see https://arxiv.org/abs/1606.08415
	"""
	return 0.5 * x * (1 + torch.tanh(math.sqrt(2 / math.pi) * (x + 0.044715 * torch.pow(x, 3))))

class AlbertLayer(nn.Module):
	def __init__(self, conf):
		super().__init__()
		self.mhead_attention = AlbertMultiHeadAttention(conf)
		self.n_hidden = conf.n_hidden
		self.n_hidden_ff = conf.n_hidden_ff
		self.feedforward = nn.Linear(conf.n_hidden, conf.n_hidden_ff)
		self.feedforward_out = nn.Linear(conf.n_hidden_ff, conf.n_hidden)
		self.layer_norm = nn.LayerNorm(conf.n_hidden, eps=conf.eps)
		self.act_fn = gelu_new
		
	def forward(self, x):
		x = self.mhead_attention(x)
		x = self.layer_norm(
			self.feedforward_out(self.act_fn(self.feedforward(x))) + x
		)
		return x

class Transformer(nn.Module):
	def __init__(self, conf):
		super().__init__()
		self.linear_to_hidden = nn.Linear(conf.n_embbed, conf.n_hidden)
		self.n_layers = conf.n_layers
		layer = AlbertLayer(conf)
		self.layers = nn.ModuleList([layer for _ in range(self.n_layers)])
		
	def forward(self, x):
		x = self.linear_to_hidden(x)
		for layer in self.layers:
			x = layer(x)

		return x

class AlbertModel(nn.Module):
	def __init__(self, conf):
		super().__init__()
		self.embedding = ContextDependentEmbedding(conf, use_positinal_embedding=True)
		self.encoder = Transformer(conf)
		self.pooler = nn.Linear(conf.n_hidden, conf.n_hidden)
		self.pooler_activation = nn.Tanh()
		
	def forward(self, x):
		x = self.embedding(x)
		x = self.encoder(x)
		x = self.pooler_activation(self.pooler(x))
		return x

# make random ALBERT input
np.random.seed(102)
n_batch = 3
inp = np.random.randint(0, conf.n_vocab, (n_batch, 10))
inp[:,0] = 1
inp[:,-3:] = 0
inp = torch.LongTensor(inp)

# make model
model = AlbertModel(conf)
out = model(inp)
print(out.sum())
