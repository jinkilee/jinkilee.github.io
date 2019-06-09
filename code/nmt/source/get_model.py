import tensorflow as tf
from models import Encoder, Decoder, BahdanauAttention
from setting import BATCH_SIZE, UNITS, EMBEDDING_DIM, ATTENTION_UNITS
from get_data import en_tok, kr_tok

# make encoder
vocab_inp_size = len(en_tok.word_index) + 1
vocab_tar_size = len(kr_tok.word_index) + 1
encoder = Encoder(vocab_inp_size, EMBEDDING_DIM, UNITS, BATCH_SIZE)
decoder = Decoder(vocab_tar_size, EMBEDDING_DIM, UNITS, BATCH_SIZE)
attention_layer = BahdanauAttention(ATTENTION_UNITS)

