import io
import re
import unicodedata
import numpy as np
import tensorflow as tf

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

def tokenize(sent, min_count=5):
	sent_tokenizer = tf.keras.preprocessing.text.Tokenizer(oov_token='<UNK>', filters='')
	sent_tokenizer.fit_on_texts(sent)
	wc_list = [sent_tokenizer.word_counts[t] for t in dict(sent_tokenizer.word_counts)]

	infreq_words = [k for k, c in sent_tokenizer.word_counts.items() if c < min_count]
	for w in infreq_words:
		del sent_tokenizer.word_index[w]
		del sent_tokenizer.word_docs[w]
		del sent_tokenizer.word_counts[w]

	sequences = sent_tokenizer.texts_to_sequences(sent)
	sequences = tf.keras.preprocessing.sequence.pad_sequences(sequences, padding='post')
	return sequences, sent_tokenizer, wc_list
