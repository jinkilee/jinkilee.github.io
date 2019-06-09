import tensorflow as tf
from setting import BATCH_SIZE, CORPUS_FILENAME
from input_data import read_data, tokenize
from sklearn.model_selection import train_test_split

# read dataset
en, kr = read_data(CORPUS_FILENAME)
en_seq, en_tok, en_wc = tokenize(en)
kr_seq, kr_tok, kr_wc = tokenize(kr)
en_seq_train, en_seq_val, kr_seq_train, kr_seq_val = train_test_split(en_seq, kr_seq, test_size=0.1)

# make tf.dataset
BUFFER_SIZE = len(en_seq_train)
dataset = tf.data.Dataset.from_tensor_slices((en_seq_train, kr_seq_train)).shuffle(BUFFER_SIZE)
dataset = dataset.batch(BATCH_SIZE, drop_remainder=True)

