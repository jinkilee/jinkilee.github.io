
class Config():
	def __init__(self):
		'''This configuration follows ALBERT `base`.

		Args:
			n_embed (:obj:`int`, optional, defaults to 128):
				embedding size
			n_vocab (:obj:`int`, optional, defaults to 32000):
				number of vocabulary in a dictionary
			n_hidden (:obj:`int`, optional, defaults to 768): 
				hidden size
			n_hidden_ff (:obj:`int`, optional, defaults to 4*n_hidden): 
				usually 4*`n_hidden`
			n_maxseq (:obj:`int`, optional, defaults to 512):
				maximum number of sequence in one sentence
			dropout_rate (:obj:`float`, optional, defaults to 0.0): 
				zero-substitution rate (e.g. if 0.0, no substitution)
			eps (:obj:`float`, optional, defaults to 1e-12): 
				epsilon value used for layer normalization
			n_layers (:obj:`int`, optional, defaults to 12): 
				number of layers
			n_head (:obj:`int`, optional, defaults to n_hidden/64): 
				number of heads in multi-head attention
			n_hidden_group (:obj:`int`, optional, defaults to 1): 
				number of groups for the hidden layers, parameters in the same group are shared
			n_tok (:obj:`int`, optional, defaults to 2):
				number of token type
			use_seed ((:obj:`bool`, optional, defaults to False)):
				whether to use torch.manual_seed(10) for deterministic setting
			attention_size (:obj:`int`, optional, defaults to 64):
				attention size
		'''
		self.n_embed = 20 # E. originally 128
		self.n_vocab = 10  # V. originally 32000
		self.n_hidden = 40 # H. originally 768
		self.n_hidden_ff = self.n_hidden * 4 # 4H. originally n_hidden * 4
		self.n_maxseq = 15 # originally 512
		self.dropout_rate = 0.0
		self.eps = 1e-6
		self.n_layers = 6	   # originally 12
		self.n_head = 8		   # originally H/64, originally H/64
		self.n_hidden_group = 1
		self.n_tok = 2
		self.use_seed = True
		assert self.n_hidden % self.n_head == 0
		self.attention_size = self.n_hidden // self.n_head
