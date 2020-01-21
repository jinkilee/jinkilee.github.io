
class Config():
	def __init__(self):
		'''
			this configuration follows ALBERT `base`.
		'''
		self.n_embbed = 20 # E. originally 128
		self.n_vocab = 10  # V. originally 32000
		self.n_hidden = 40 # H. originally 768
		self.n_hidden_ff = self.n_hidden * 4 # 4H. originally n_hidden * 4
		self.n_maxseq = 15 # originally 512
		self.dropout_rate = 0.1
		self.eps = 1e-6
		self.n_layers = 6	   # originally 12
		self.n_head = 8		 # originally H/64, originally H/64
		assert self.n_hidden % self.n_head == 0
		self.attention_size = self.n_hidden // self.n_head
