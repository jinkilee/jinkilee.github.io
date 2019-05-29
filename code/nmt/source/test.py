import io
import re
import numpy as np
import unicodedata
import tensorflow as tf
from sklearn.model_selection import train_test_split
from models import Encoder
from models import BahdanauAttention

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
dataset = tf.data.Dataset.from_tensor_slices((en_seq_train, kr_seq_train)).shuffle(BUFFER_SIZE)
dataset = dataset.batch(BATCH_SIZE, drop_remainder=True)


# make encoder
vocab_inp_size = len(en_tok.word_index) + 1
encoder = Encoder(vocab_inp_size, embedding_dim, units, BATCH_SIZE)

# sample input
sample_hidden = encoder.initialize_hidden_state()
print ('Encoder Hidden state shape: (batch size, units) {}'.format(sample_hidden.shape))
#sample_output, sample_hidden = encoder(example_input_batch, sample_hidden)
#print ('Encoder output shape: (batch size, sequence length, units) {}'.format(sample_output.shape))

attention_layer = BahdanauAttention(10)
print(attention_layer)




