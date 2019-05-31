import io
import re
import os
import time
import numpy as np
import unicodedata
import tensorflow as tf
from sklearn.model_selection import train_test_split
from models import Encoder, Decoder
from models import BahdanauAttention
from absl import logging

# set logging condition
logging.set_verbosity(logging.INFO)
logging.set_verbosity(logging.DEBUG)

BATCH_SIZE = 64
embedding_dim = 256
units = 1024

def unicode_to_ascii(s):
	return ''.join(c for c in unicodedata.normalize('NFD', s)
		if unicodedata.category(c) != 'Mn')

def preprocess_eng(w):
	w = unicode_to_ascii(w.lower().strip())

	# replace substring
	w = re.sub(r"([?.!,¿])", r" \1 ", w)
	w = re.sub(r'[" "]+', " ", w)
	w = re.sub(r"[^a-zA-Z?.!,¿]+", " ", w)
	w = w.rstrip().strip()

	# add start/end tags
	w = '<start> ' + w + ' <end>'
	return w

def preprocess_kor(w):
	# replace substring
	w = re.sub(r'([?.!,¿])', r' \1 ', w)
	w = re.sub(r'[" "]+', ' ', w)
	w = re.sub(r'[^ ㄱ-ㅣ가-힣]+', ' ', w)
	w = w.rstrip().strip()

	# add start/end tags
	w = '<start> ' + w + ' <end>'
	return w

def read_data(filename):
	lines = io.open(filename, encoding='UTF-8').read().strip().split('\n')
	word_pairs = np.array([l.rstrip().split('\t') for l in lines])
	eng = list(map(preprocess_eng, word_pairs[:, 0]))
	kor = list(map(preprocess_kor, word_pairs[:, 1]))
	return eng, kor

def tokenize(sent):
	sent_tokenizer = tf.keras.preprocessing.text.Tokenizer(filters='')
	sent_tokenizer.fit_on_texts(sent)

	sequences = sent_tokenizer.texts_to_sequences(sent)
	sequences = tf.keras.preprocessing.sequence.pad_sequences(sequences, padding='post')
	return sequences, sent_tokenizer

# read dataset
en, kr = read_data('/data/nmt/kor.txt')
en_seq, en_tok = tokenize(en)
kr_seq, kr_tok = tokenize(kr)
en_seq_train, en_seq_val, kr_seq_train, kr_seq_val = train_test_split(en_seq, kr_seq, test_size=0.1)

# make tf.dataset
BUFFER_SIZE = len(en_seq_train)
steps_per_epoch = len(en_seq_train) // BATCH_SIZE
dataset = tf.data.Dataset.from_tensor_slices((en_seq_train, kr_seq_train)).shuffle(BUFFER_SIZE)
dataset = dataset.batch(BATCH_SIZE, drop_remainder=True)

example_input_batch, example_target_batch = next(iter(dataset))
example_input_batch.shape, example_target_batch.shape

# make encoder
vocab_inp_size = len(en_tok.word_index) + 1
vocab_tar_size = len(kr_tok.word_index) + 1
encoder = Encoder(vocab_inp_size, embedding_dim, units, BATCH_SIZE)
decoder = Decoder(vocab_tar_size, embedding_dim, units, BATCH_SIZE)
attention_layer = BahdanauAttention(10)

# sample input
sample_hidden = encoder.initialize_hidden_state()
sample_output, sample_hidden = encoder(example_input_batch, sample_hidden)
sample_decoder_output, _, _ = decoder(tf.random.uniform((64, 1)), sample_hidden, sample_output)
attention_result, attention_weights = attention_layer(sample_hidden, sample_output)
logging.debug('Encoder Hidden state shape: (batch size, units) {}'.format(sample_hidden.shape))
logging.debug('Encoder output shape: (batch size, sequence length, units) {}'.format(sample_output.shape))
logging.debug('Attention result shape: (batch size, units) {}'.format(attention_result.shape))
logging.debug('Attention weights shape: (batch_size, sequence_length, 1) {}'.format(attention_weights.shape))
logging.debug('Decoder output shape: (batch_size, vocab size) {}'.format(sample_decoder_output.shape))

# optimizer
optimizer = tf.keras.optimizers.Adam()
loss_object = tf.keras.losses.SparseCategoricalCrossentropy(
	from_logits=True, reduction='none')

def loss_function(real, pred):
	mask = tf.math.logical_not(tf.math.equal(real, 0))
	loss_ = loss_object(real, pred)
	mask = tf.cast(mask, dtype=loss_.dtype)
	loss_ *= mask

	return tf.reduce_mean(loss_)

@tf.function
def train_step(inp, targ, enc_hidden):
	loss = 0

	with tf.GradientTape() as tape:
		enc_output, enc_hidden = encoder(inp, enc_hidden)
		dec_hidden = enc_hidden
		dec_input = tf.expand_dims([kr_tok.word_index['<start>']] * BATCH_SIZE, 1)

		# Teacher forcing - feeding the target as the next input
		for t in range(1, targ.shape[1]):
			# passing enc_output to the decoder
			predictions, dec_hidden, _ = decoder(dec_input, dec_hidden, enc_output)
			loss += loss_function(targ[:, t], predictions)
			# using teacher forcing
			dec_input = tf.expand_dims(targ[:, t], 1)

	batch_loss = (loss / int(targ.shape[1]))
	variables = encoder.trainable_variables + decoder.trainable_variables
	gradients = tape.gradient(loss, variables)
	optimizer.apply_gradients(zip(gradients, variables))
	return batch_loss

checkpoint_dir = './training_checkpoints'
checkpoint_prefix = os.path.join(checkpoint_dir, "ckpt")
checkpoint = tf.train.Checkpoint(optimizer=optimizer, encoder=encoder, decoder=decoder)

EPOCHS = 100
for epoch in range(EPOCHS):
	start = time.time()

	enc_hidden = encoder.initialize_hidden_state()
	total_loss = 0

	for (batch, (inp, targ)) in enumerate(dataset.take(steps_per_epoch)):
		batch_loss = train_step(inp, targ, enc_hidden)
		total_loss += batch_loss

	# saving (checkpoint) the model every 2 epochs
	if (epoch + 1) % 2 == 0:
		checkpoint.save(file_prefix = checkpoint_prefix)

	#print('Epoch {} Loss {:.4f}'.format(epoch + 1, total_loss / steps_per_epoch))
	logging.info('epoch {} loss {:.4f} -> {:.4f} taken'.format(
		epoch+1, total_loss/steps_per_epoch, time.time()-start))
