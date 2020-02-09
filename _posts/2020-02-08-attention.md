---
title: "Attention Mechanism"
date: 2020-02-08 08:26:28 -0400
categories: AI
---
From the end of 2018, transformer architecture has cleaned up most of SOTA result on public NLP project such as SQuAD. The main idea of transformer comes from the paper `[**Attention is all you need**](https://arxiv.org/pdf/1706.03762.pdf)`. This actually means "You do not really need to use RNN architecture, but attention". Then what is an Attention?

Basic concept
---------------
To talk about the main of attention mechanism, it is good to take a short look on RNN architecture. Imagine how do we build a classifier model using RNN architecture. 

```python
# https://github.com/jinkilee/multi-class-text-classification-cnn-rnn/blob/master/text_cnn_rnn.py
class TextCNNRNN(object):
	def __init__(self, embedding_mat, non_static, hidden_unit, sequence_length, max_pool_size,
		num_classes, embedding_size, filter_sizes, num_filters, l2_reg_lambda=0.0):

		self.input_x = tf.placeholder(tf.int32, [None, sequence_length], name='input_x')
		self.input_y = tf.placeholder(tf.float32, [None, num_classes], name='input_y')

		# ...
		self._initial_state = lstm_cell.zero_state(self.batch_size, tf.float32)
		outputs, state = tf.contrib.rnn.static_rnn(
			lstm_cell, 
			inputs, 
			initial_state=self._initial_state, 
			sequence_length=self.real_len)

		# Collect the appropriate last words into variable output (dimension = batch x embedding_size)
		output = outputs[0]

		# Build a classifier with `output`
		# ...
```

This is a normal code to run a classifier with a LSTM. Everything is okay, but why have we used the last output only? LSTM is designed to memorize long term sequence. so we just believe it is okay to use the last one only. That is, the last one has compact representation of an entire sequence.

| ![Figure 1](http://jinkilee.github.io/img/attention/1.png) |
|:--:|
| *Figure 1: RNN-like architecture taking only the last output* |

However, is it really okay? I have always doubt that `outputs` other than the last one may have some meaningful representation. LSTM may work on short sequences but the longer sentences are, the less information it can represent. The basic idea of attention is to keep those vectors and make a good use of it.

With an example
---------------
Let's say we want to build a translator(english to korean) To build a translation model, a seq2seq model which contains encoder and decoder was widely used.

// 2.jpg
// encode source sentence and decode it to target sentence
| ![Figure 2](http://jinkilee.github.io/img/attention/2.png) |
|:--:|
| *Figure 2: Translation with seq2seq model* |

Let's see one translation example.
- eng: I like an apple
- kor: 나는(I)  사과를(apple)  좋아한다.(like)

For those of you who cannot speak Korean, I put english word next to korean word. If you see the two sentences, you can easily find that corresponding words does not come in order. In english, verb comes next to subject, while verb comes at the end of a sentence in korean. 

- eng: I like an apple
- kor: 나는(I)  사과를(apple)  좋아한다.(like)

Therefore, when you train seq2seq model, you should make your model to consider this out-of-order characteristic. To do it, you can use attention architecture. you can have your model pay an `ATTENTION` to part. That is, when your model process `like`, it does not need to see subject(I) or object(apple). With sample principle, you do not need to see `나는(I)` or `좋아한다(like)` when you focus on `an apple`.

How attention is calculated
---------------
Now we know what attention is, so let's see how it is calculated with code.

```python
import tensorflow as tf
import numpy as np

# GRU class
def gru(units):
    # If you have a GPU, we recommend using CuDNNGRU(provides a 3x speedup than GRU)
    # the code automatically does that.
    if tf.test.is_gpu_available():
        return tf.keras.layers.CuDNNGRU(units, 
                                        return_sequences=True, 
                                        return_state=True, 
                                        recurrent_initializer='glorot_uniform')
    else:
        return tf.keras.layers.GRU(units, 
                                   return_sequences=True, 
                                   return_state=True, 
                                   recurrent_activation='sigmoid', 
                                   recurrent_initializer='glorot_uniform')

# define setting
vocab_size = 10
embedding_dim = 20
units = 40

# make inputs
x = np.expand_dims(np.random.randint(0, vocab_size, (5)), axis=0)

# passing encoder
embedding = tf.keras.layers.Embedding(vocab_size, embedding_dim)
x = embedding(x)
gru_cell = gru(units)
output, state = gru_cell(x)

# passing decoder
W1 = tf.keras.layers.Dense(units)
W2 = tf.keras.layers.Dense(units)
V = tf.keras.layers.Dense(1)

hidden_with_time_axis = tf.expand_dims(state, 1)
score = V(tf.nn.tanh(W1(output) + W2(hidden_with_time_axis)))

# attention_weights shape == (batch_size, max_length, 1)
attention_weights = tf.nn.softmax(score, axis=1)
attention_weights
```

The above code block will output the following.
```
<tf.Tensor: shape=(1, 5, 1), dtype=float32, numpy=
array([[[0.20362999],
        [0.2018812 ],
        [0.1988714 ],
        [0.19788313],
        [0.19773428]]], dtype=float32)>
```

Key method to convert GRU's `output` and `state` is just several feed forward networks such as `W1`, `W2`, and `V` followed by `tf.nn.tanh` activation. It is not technically hard one. It is also good to note that `output` and `state` were used for calculating attention.

Our context vector is just weighted multiplication of `attention_weights` and `output`.
```
context_vector = attention_weights * enc_output
context_vector = tf.reduce_sum(context_vector, axis=1)
<tf.Tensor: shape=(1, 40), dtype=float32, numpy=
array([[ 0.00450457, -0.000479  ,  0.01776177, -0.00874093, -0.00549831,
        -0.00403002, -0.00280772,  0.01280778, -0.00150356,  0.01241918,
        -0.01647402, -0.00602317,  0.00513975,  0.00845177, -0.01333129,
         0.00751389,  0.00228994,  0.01548713, -0.00374114,  0.00115751,
        -0.00692876,  0.00238407, -0.00133134,  0.01229093,  0.01858362,
        -0.00297811, -0.0060442 ,  0.00627679,  0.00151788,  0.01066009,
        -0.02028783,  0.01406133, -0.02786346,  0.01104608,  0.01019504,
         0.00855909, -0.0151533 , -0.00260982,  0.02325839,  0.00457436]],
      dtype=float32)>
```

With `context_vector` we can iteratively generate(decode) next word from `<start>`. And loss is calculated word by word during training. Note that in the evaluation, the decoder will iterate until `<end>` comes out. 
```python
loss = 0

# training pseudo code
for word in ['I','like','an','apple']:
    # some codes with context_vector
    # ...

    # predicted word
    pred = predict_word(context_vector, ..)

    # calculate loss
    loss += loss_fn(pred, word)

# evaluation pseudo code
for word in ['I','like','an','apple']:
    # some codes with context_vector
    # ...

    # predicted word
    pred = predict_word(context_vector, ..)

    # break if `<end>` comes out
    if pred == '<end>':
        break
```

Attention after training
---------------
After attention is trained, we can see that our attention network can pay more attention to specific part given one input data. Because our network was not fully trained due to limited time, translation does not work very well, so I prepared well-trained attention network for positive/negative sentence classification to see how attention network work.

| ![Figure 5](http://jinkilee.github.io/img/attention/5.png) |
|:--:|
| *Figure 5: Highlited attention with real input sentences* |

The above model pay more attention to positive part of given sentence. 

Attention with one sentence(Self-Attention)
----------------
So far, we have talked about attention with two sentences. However, we can also train attention network with one sentence.

Rather than training a new model, I loaded a pretrained `BertModel` model from `[**huggingface/transformer**}`(https://github.com/huggingface/transformers).

| ![Figure 6](http://jinkilee.github.io/img/attention/6.png) |
|:--:|
| *Figure 6: Self-attention result from BERT* |

word | 1st | 2nd | 3rd | 4th | 5th
--- | --- | --- | --- | --- | --- |
i | [SEP] | apple | [SEP] | [CLS] | i
like | [CLS] | like | [SEP] | [SEP] | like
an | [CLS] | i | [SEP] | [SEP] | you
apple | [CLS] | [SEP] | [SEP] | like | like
[SEP] | [SEP] | i | [SEP] | banana | like
you | apple | i | [SEP] | [CLS] | [SEP]
like | [CLS] | like | like | [SEP] | [SEP]
a | you | [SEP] | [SEP] | i | [CLS]]
banana | [CLS] | like | apple | like | [SEP]
[SEP] | [SEP] | [SEP] | i | banana | [CLS]

Original sentence was `I like an apple [SEP] You like a banana`. As you may guess, top-5 highlights are mostly apple, like, banana.
Paying specific part in one sentence is actually what we always do. We do not always pay equal attention from start to end. Given a sentence `I like an apple`, do we pay attenion to `an`? Not really. We only hear `like` and `apple` maybe. Attention with one sentence is called Self-Attention.

Conclusion
----------------
I would like to summarize my post here
- Attention idea: No only last output like LSTM, but make use of all hidden representation
- How attention is calculated: it can be calculated with only simple feedforward networks.
- Training attention: word by word training and evaluation
- Application: translator, text summarization and many various NLP project. even in Image.
- Attention with one sentence: self-attention

Actually, the self-attention is very important idea in most of BERT-like transformer.(i.e. BERT, RoBERTa, AlBert, ..) I would like to explain self-attention in more detail later.

Reference
----------------
- [**Intuitive Understanding of Attention Mechanism in Deep Learning**](https://towardsdatascience.com/intuitive-understanding-of-attention-mechanism-in-deep-learning-6c9482aecf4f)
- [**Attention mechanism in NLP. From seq2seq + attention to BERT**](https://lovit.github.io/machine%20learning/2019/03/17/attention_in_nlp/)
- [**A Beginner's Guide to Attention Mechanisms and Memory Networks**](https://pathmind.com/wiki/attention-mechanism-memory-network)
- [**Long Short-Term Memory (LSTM) 이해하기**](https://dgkim5360.tistory.com/entry/understanding-long-short-term-memory-lstm-kr)



