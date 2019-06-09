import os
import time
import tensorflow as tf

from setting import BATCH_SIZE, EPOCHS, CHECKPOINT_DIR, PREFIX, logger
from get_data import dataset, en_seq_train, kr_tok
from get_model import encoder, decoder, attention_layer

DO_SAMPLE_TEST = True

if DO_SAMPLE_TEST:
	example_input_batch, example_target_batch = next(iter(dataset))
	example_input_batch.shape, example_target_batch.shape

	# sample input
	sample_hidden = encoder.initialize_hidden_state()
	sample_output, sample_hidden = encoder(example_input_batch, sample_hidden)
	sample_decoder_output, _, _ = decoder(tf.random.uniform((BATCH_SIZE, 1)), sample_hidden, sample_output)
	attention_result, attention_weights = attention_layer(sample_hidden, sample_output)
	logger.debug('Encoder Hidden state shape: (batch size, units) {}'.format(sample_hidden.shape))
	logger.debug('Encoder output shape: (batch size, sequence length, units) {}'.format(sample_output.shape))
	logger.debug('Attention result shape: (batch size, units) {}'.format(attention_result.shape))
	logger.debug('Attention weights shape: (batch_size, sequence_length, 1) {}'.format(attention_weights.shape))
	logger.debug('Decoder output shape: (batch_size, vocab size) {}'.format(sample_decoder_output.shape))

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
			logger.info(t, predictions, dec_hidden)

	batch_loss = (loss / int(targ.shape[1]))
	variables = encoder.trainable_variables + decoder.trainable_variables
	gradients = tape.gradient(loss, variables)
	optimizer.apply_gradients(zip(gradients, variables))
	return batch_loss

#from get_model import optimizer
# optimizer
# optimizer = tf.keras.optimizers.Adam()

optimizer = tf.keras.optimizers.Adam()
loss_object = tf.keras.losses.SparseCategoricalCrossentropy(
    from_logits=True, reduction='none')

checkpoint_dir = CHECKPOINT_DIR
checkpoint_prefix = os.path.join(checkpoint_dir, PREFIX)
checkpoint = tf.train.Checkpoint(optimizer=optimizer, encoder=encoder, decoder=decoder)

steps_per_epoch = len(en_seq_train) // BATCH_SIZE
for epoch in range(EPOCHS):
	start = time.time()

	enc_hidden = encoder.initialize_hidden_state()
	total_loss = 0

	for (batch, (inp, targ)) in enumerate(dataset.take(steps_per_epoch)):
		batch_loss = train_step(inp, targ, enc_hidden)
		total_loss += batch_loss
		logger.debug('{} {} loss: {}'.format(inp.shape, targ.shape, batch_loss))

	# saving (checkpoint) the model every 2 epochs
	if epoch % 10 == 0:
		checkpoint.save(file_prefix=checkpoint_prefix)

	logger.info('epoch {} loss {:.4f} -> {:.4f} taken'.format(
		epoch+1, total_loss/steps_per_epoch, time.time()-start))
