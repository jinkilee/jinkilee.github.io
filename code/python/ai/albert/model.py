import torch
import torch.nn as nn
import numpy as np
import math
from config import Config
from utils import set_seeds

set_seeds(100)
conf = Config()

# identical with AlbertEmbedding assuming that it has same forward implementation
class ContextDependentEmbedding(nn.Module):
	'''class implementation for AlbertMultiHeadAttention

	Args:
		conf(Config): object of `Config` class defined at `config.py`

	Example:
		>>> import numpy as np
		>>> import torch
		>>> from model import ContextDependentEmbedding
		>>> from utils import get_num_params
		>>> from config import Config
		>>> conf = Config()
		>>> np.random.seed(100)
		>>> n_batch = 3
		>>> inp = np.random.randint(0, conf.n_vocab, (n_batch, 10))
		>>> inp = torch.LongTensor(inp)
		>>> print(inp)
		tensor([[8, 8, 3, 7, 7, 0, 4, 2, 5, 2],
				[2, 2, 1, 0, 8, 4, 0, 9, 6, 2],
				[4, 1, 5, 3, 4, 4, 3, 7, 1, 1]])
		>>> transformer = ContextDependentEmbedding(conf)
		>>> out = transformer(inp)
		>>> print('number of parameter: {}'.format(get_num_params(transformer)))
		number of parameter: 580
		>>> print('output shape: {}'.format(out.shape))
		output shape: torch.Size([3, 10, 20])
		>>> print(out.sum())
		tensor(-7.5251e-07, grad_fn=<SumBackward0>)
	'''
	def __init__(self, conf, use_positinal_embedding=True):
		super().__init__()
		if conf.use_seed:
			torch.manual_seed(10)

		# context-independent embedding
		# FIXME: n_embed -> n_embed
		self.embedded_word = nn.Embedding(conf.n_vocab, conf.n_embed)
		self.pos_emb_vector = nn.Embedding(conf.n_maxseq, conf.n_embed)
		self.tok_emb_vector = nn.Embedding(conf.n_tok, conf.n_embed)
		self.use_positinal_embedding = use_positinal_embedding
		self.norm = nn.LayerNorm(conf.n_embed, eps=conf.eps)
		self.drop = nn.Dropout(conf.dropout_rate)
		
	def forward(self, x, pos_x=None, tok_x=None):
		n_seq = x.size()[1]
		ci_emb = self.embedded_word(x)

		if pos_x is None:
			pos_x = torch.arange(n_seq, dtype=torch.long)
			pos_x = pos_x.unsqueeze(0).expand(x.shape)

		if tok_x is None:
			tok_x = torch.zeros(x.shape, dtype=torch.long)

		if self.use_positinal_embedding:
			pos_emb = self.pos_emb_vector(pos_x)
			tok_emb = self.tok_emb_vector(tok_x)
			cd_emb = ci_emb + pos_emb + tok_emb
			cd_emb = self.drop(self.norm(cd_emb))
		return cd_emb

# identical with AlbertAttention
class AlbertMultiHeadAttention(nn.Module):
	'''class implementation for AlbertMultiHeadAttention

	Args:
		conf(Config): object of `Config` class defined at `config.py`

	Example:
		>>> import numpy as np
		>>> import torch
		>>> from model import AlbertMultiHeadAttention
		>>> from utils import get_num_params
		>>> from config import Config
		>>> conf = Config()
		>>> np.random.seed(100)
		>>> n_batch = 3
		>>> inp = np.random.random((n_batch, 10, conf.n_hidden))
		>>> inp = torch.FloatTensor(inp)
		>>> print(inp[:,2:4,5:7])
		tensor([[[0.3356, 0.8055],
				 [0.4922, 0.4029]],

				[[0.2013, 0.8774],
				 [0.3597, 0.1592]],

				[[0.2649, 0.3293],
				 [0.0957, 0.7220]]])
		>>> transformer = AlbertMultiHeadAttention(conf)
		>>> out = transformer(inp)
		>>> print('number of parameter: {}'.format(get_num_params(transformer)))
		number of parameter: 6640
		>>> print('output shape: {}'.format(out.shape))
		output shape: torch.Size([3, 10, 40])
		>>> print(out.sum())
		tensor(-1.8835e-05, grad_fn=<SumBackward0>)
	'''
	def __init__(self, conf):
		super().__init__()
		if conf.use_seed:
			torch.manual_seed(10)
		
		self.query = nn.Linear(conf.n_hidden, conf.n_hidden)
		self.key = nn.Linear(conf.n_hidden, conf.n_hidden)
		self.value = nn.Linear(conf.n_hidden, conf.n_hidden)
		self.attention_size = conf.attention_size
		self.hidden_size = conf.n_hidden
		self.n_head = conf.n_head
		self.softmax = torch.nn.Softmax(dim=-1)
		self.layer_norm = nn.LayerNorm(conf.n_hidden, eps=conf.eps)
		
		torch.manual_seed(10)
		self.dense = nn.Linear(conf.n_hidden, conf.n_hidden)
		self.attention_head_size = conf.n_hidden // conf.n_head
		
	def split_tensor(self, x):
		x_split = torch.split(x, self.attention_size, dim=2)
		return torch.stack(x_split, dim=-2)
		
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
		projected_context = self.dense(self.merge_last_ndims(context, 2))
		
		# do something about `mask`
		hidden = self.layer_norm(x + projected_context)
		return hidden


def gelu_new(x):
	""" Implementation of the gelu activation function currently in Google Bert repo (identical to OpenAI GPT).
		Also see https://arxiv.org/abs/1606.08415
	"""
	return 0.5 * x * (1 + torch.tanh(math.sqrt(2 / math.pi) * (x + 0.044715 * torch.pow(x, 3))))

# identical to AlbertLayer
class AlbertLayer(nn.Module):
	'''class implementation for AlbertLayer

	Args:
		conf(Config): object of `Config` class defined at `config.py`

	Example:
		>>> from model import AlbertLayer
		>>> from utils import get_num_params
		>>> from config import Config
		>>> conf = Config()
		>>> np.random.seed(100)
		>>> n_batch = 3
		>>> inp = np.random.random((n_batch, 10, conf.n_hidden))
		>>> inp = torch.FloatTensor(inp)
		>>> print(inp[:,2:4,5:7])
		tensor([[[0.3356, 0.8055],
				 [0.4922, 0.4029]],

				[[0.2013, 0.8774],
				 [0.3597, 0.1592]],

				[[0.2649, 0.3293],
				 [0.0957, 0.7220]]])
		>>> transformer = AlbertLayer(conf)
		>>> out = transformer(inp)
		>>> print('number of parameter: {}'.format(get_num_params(transformer)))
		number of parameter: 19720
		>>> print('output shape: {}'.format(out.shape))
		output shape: torch.Size([3, 10, 40])
		>>> print(out.sum())
		tensor(-2.8610e-06, grad_fn=<SumBackward0>)
	'''
	def __init__(self, conf):
		super().__init__()
		if conf.use_seed:
			torch.manual_seed(10)

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

# identical to AlbertTransformer
class Transformer(nn.Module):
	'''class implementation for Transformer

	Args:
		conf(Config): object of `Config` class defined at `config.py`

	Example:
		>>> import numpy as np
		>>> import torch
		>>> from model import Transformer
		>>> from utils import get_num_params
		>>> from config import Config
		>>> conf = Config()
		>>> np.random.seed(100)
		>>> n_batch = 3
		>>> inp = np.random.random((n_batch, 10, conf.n_embed))
		>>> inp = torch.FloatTensor(inp)
		>>> print(inp[:,2:4,5:7])
		tensor([[[0.5447, 0.7691],
				 [0.9464, 0.6023]],

				[[0.1901, 0.7119],
				 [0.5252, 0.3863]],

				[[0.5240, 0.8063],
				 [0.3297, 0.4935]]])
		>>> transformer = Transformer(conf)
		>>> out = transformer(inp)
		>>> print('number of parameter: {}'.format(get_num_params(transformer)))
		number of parameter: 20560
		>>> print('output shape: {}'.format(out.shape))
		output shape: torch.Size([3, 10, 40])
		>>> print(out.sum())
		tensor(6.4373e-06, grad_fn=<SumBackward0>)
	'''
	def __init__(self, conf):
		super().__init__()
		if conf.use_seed:
			torch.manual_seed(10)

		self.linear_to_hidden = nn.Linear(conf.n_embed, conf.n_hidden)
		self.n_layers = conf.n_layers
		layer = AlbertLayer(conf)
		self.layers = nn.ModuleList([layer for _ in range(self.n_layers)])
		
	def forward(self, x):
		x = self.linear_to_hidden(x)
		for i in range(self.n_layers):
			x = self.layers[0](x)
			print(i, x.shape, x.sum())

		return x

# FIXME: remove torch.manual_seed(10)
# identical to AlbertModel if ContextDenendentEmbedding is skipped
class AlbertModel(nn.Module):
	'''class implementation for AlbertModel

	Args:
		conf(Config): object of `Config` class defined at `config.py`

	Example:
		>>> import numpy as np
		>>> import torch
		>>> from model import AlbertModel
		>>> from utils import get_num_params
		>>> from config import Config
		>>> conf = Config()
		>>> np.random.seed(100)
		>>> n_batch = 3
		>>> inp = np.random.randint(0, conf.n_vocab, (n_batch, 10))
		>>> inp = torch.LongTensor(inp)
		>>> transformer = AlbertModel(conf)
		>>> out, pout = transformer(inp)
		0 torch.Size([3, 10, 40]) tensor(6.3181e-06, grad_fn=<SumBackward0>)
		1 torch.Size([3, 10, 40]) tensor(5.6624e-06, grad_fn=<SumBackward0>)
		2 torch.Size([3, 10, 40]) tensor(-4.0233e-06, grad_fn=<SumBackward0>)
		3 torch.Size([3, 10, 40]) tensor(-4.3474e-06, grad_fn=<SumBackward0>)
		4 torch.Size([3, 10, 40]) tensor(8.5831e-06, grad_fn=<SumBackward0>)
		5 torch.Size([3, 10, 40]) tensor(-9.1195e-06, grad_fn=<SumBackward0>)
		>>> print('number of parameter: {}'.format(get_num_params(transformer)))
		number of parameter: 22780
		>>> print('out, pout shape: {} {}'.format(out.shape, pout.shape))
		out, pout shape: torch.Size([3, 10, 40]) torch.Size([3, 40])
		>>> print('out, pout sum: {} {}'.format(out.sum(), pout.sum()))
		out, pout sum: -9.119510650634766e-06 11.930480003356934
	'''
	def __init__(self, conf):
		super().__init__()
		if conf.use_seed:
			torch.manual_seed(10)

		self.embedding = ContextDependentEmbedding(conf, use_positinal_embedding=True)
		self.encoder = Transformer(conf)
		self.pooler = nn.Linear(conf.n_hidden, conf.n_hidden)
		self.pooler_activation = nn.Tanh()
	

	def io_embedding_distance(self, x):
		dist = nn.CosineSimilarity(dim=1, eps=1e-6)
		emb_x = self.embedding(x)
		old_x = self.encoder.linear_to_hidden(emb_x)
		for i, layer in enumerate(self.encoder.layers):
			new_x = layer(old_x)
			distance = dist(old_x.view(3, -1), new_x.view(3, -1))
			print(distance)
			#print('{} layers: {:.4f}'.format(i, distance))
			old_x = new_x
	
	def forward(self, x):
		x = self.embedding(x)
		seq_output = self.encoder(x)
		pull_output = self.pooler_activation(self.pooler(seq_output[:,0]))
		return seq_output, pull_output






conf = Config()
np.random.seed(100)
n_batch = 3

# make random input
inp = np.random.randint(0, conf.n_vocab, (n_batch, 10))
inp = torch.LongTensor(inp)
#inp = np.random.random((n_batch, 10, conf.n_embed))
#inp = torch.FloatTensor(inp)

# define AlbertModel
transformer = AlbertModel(conf)

# output AlbertModel
#out, pout = transformer(inp)
#print(out.shape, pout.shape)
#print(out.sum(), pout.sum())
transformer.io_embedding_distance(inp)
