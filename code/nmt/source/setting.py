import logging
import logging.config
import tensorflow as tf

TEST = True

# set logging condition
logging.config.fileConfig('/anything/git/jinkilee.github.io/code/nmt/source/logging.conf')
logger = logging.getLogger('nmtLogger')

if TEST:
	# # variables for real model
	CORPUS_FILENAME = '/data/nmt/kor.txt'
	EPOCHS = 200
	BATCH_SIZE = 64
	EMBEDDING_DIM = 64  	# originally 128
	UNITS = 512				# originally 512
	ATTENTION_UNITS = 10
	CHECKPOINT_DIR = '/anything/git/jinkilee.github.io/code/nmt/source/models/'
	MODELPATH = '/anything/git/jinkilee.github.io/code/nmt/source/models/'
else:
	# variables for test model
	CORPUS_FILENAME = '/data/nmt/corpus.txt'
	EPOCHS = 100
	BATCH_SIZE = 128
	EMBEDDING_DIM = 64  	# originally 128
	UNITS = 128				# originally 512
	ATTENTION_UNITS = 10
	CHECKPOINT_DIR = '/data/nmt/models/'
	MODELPATH = '/data/nmt/models/'
PREFIX = 'model-b{}-e{}-u{}-a{}'.format(BATCH_SIZE, EMBEDDING_DIM, UNITS, ATTENTION_UNITS)
