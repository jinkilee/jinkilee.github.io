import tensorflow as tf

class Encoder(tf.keras.Model):
	def __init__(self, vocab_size, embedding_dim, enc_units, batch_sz):
		super(Encoder, self).__init__()
		self.batch_sz = batch_sz
		self.enc_units = enc_units
		self.embedding = tf.keras.layers.Embedding(vocab_size, embedding_dim)
		self.gru = tf.keras.layers.GRU(self.enc_units,
								   return_sequences=True,
								   return_state=True,
								   recurrent_initializer='glorot_uniform')

	def call(self, x, hidden):
		x = self.embedding(x)
		output, state = self.gru(x, initial_state = hidden)
		return output, state

	def initialize_hidden_state(self):
		return tf.zeros((self.batch_sz, self.enc_units))


class BahdanauAttention(tf.keras.Model):
	def __init__(self, units):
		super(BahdanauAttention, self).__init__()
		self.W1 = tf.keras.layers.Dense(units)
		self.W2 = tf.keras.layers.Dense(units)
		self.V = tf.keras.layers.Dense(1)

	def call(self, query, values):
		# hidden shape == (batch_size, hidden size)
		# hidden_with_time_axis shape == (batch_size, 1, hidden size)
		# we are doing this to perform addition to calculate the score
		hidden_with_time_axis = tf.expand_dims(query, 1)

		# score shape == (batch_size, max_length, hidden_size)
		print(self.W1(values).shape)
		print(self.W2(hidden_with_time_axis).shape)
		print((self.W1(values) + self.W2(hidden_with_time_axis)).shape)
		score = self.V(tf.nn.tanh(
			self.W1(values) + self.W2(hidden_with_time_axis)))
		print(score.shape)
		print('---------')

		# attention_weights shape == (batch_size, max_length, 1)
		# we get 1 at the last axis because we are applying score to self.V
		attention_weights = tf.nn.softmax(score, axis=1)
		print(attention_weights.shape)

		# context_vector shape after sum == (batch_size, hidden_size)
		context_vector = attention_weights * values
		print(values.shape)
		print(context_vector.shape)
		context_vector = tf.reduce_sum(context_vector, axis=1)
		print(context_vector.shape)

		return context_vector, attention_weights



