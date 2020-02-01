---
title: "BERT VS ALBERT"
date: 2020-01-31 08:26:28 -0400
categories: jekyll update
---
There are so many blogs about BERT that surprised most of NLP people in 2018. As one of people who was surprised, I applied this technique on my company's project right away and got quite good result at that time. However, something I wanted more was its size. BERT was too big. Too big to load and too big to save as well for one single model. Albert is upgrade version of BERT in terms of its size and performance. In this post, I would like to explain how the size of BERT was reduced and also want to explain why it works. 

Actually, there are many blogs that explain the difference of BERT and ALBERT. In my post, I want to focus in terms of `why` more. The major difference between BERT and ALBERT are followings
- Factorized embedding parameterization
- Cross-layer parameter sharing
- Sentence order prediction

Factorized embedding parameterization (How)
---------------
This is a technique to reduce the number of parameters from an embedding layer, which is at the very front of BERT/ALBERT. Let's see how this technique reduce the number of parameters from code.
```python
# Implementation of BERT's embedding layer
class BertEmbeddings(nn.Module):
    """Construct the embeddings from word, position and token_type embeddings.
    """

    def __init__(self, config):
        super().__init__()
        self.word_embeddings = nn.Embedding(config.vocab_size, config.hidden_size, padding_idx=0)
        self.position_embeddings = nn.Embedding(config.max_position_embeddings, config.hidden_size)
        self.token_type_embeddings = nn.Embedding(config.type_vocab_size, config.hidden_size)

        # self.LayerNorm is not snake-cased to stick with TensorFlow model variable name and be able to load
        # any TensorFlow checkpoint file
        self.LayerNorm = BertLayerNorm(config.hidden_size, eps=config.layer_norm_eps)
        self.dropout = nn.Dropout(config.hidden_dropout_prob)

    def forward(self, input_ids=None, token_type_ids=None, position_ids=None, inputs_embeds=None):
		# note that some detail of forward() is omitted for clearance
		input_shape = input_ids.shape
		position_ids = position_ids.unsqueeze(0).expand(input_shape)
		token_type_ids = torch.zeros(input_shape, dtype=torch.long)

		inputs_embeds = self.word_embeddings(input_ids)
        position_embeddings = self.position_embeddings(position_ids)
        token_type_embeddings = self.token_type_embeddings(token_type_ids)

        embeddings = inputs_embeds + position_embeddings + token_type_embeddings
        embeddings = self.LayerNorm(embeddings)
        embeddings = self.dropout(embeddings)
        return embeddings

# Implementation of ALBERT's embedding layer
class AlbertEmbeddings(BertEmbeddings):
    """
    Construct the embeddings from word, position and token_type embeddings.
    """

    def __init__(self, config):
        super().__init__(config)

        self.word_embeddings = nn.Embedding(config.vocab_size, config.embedding_size, padding_idx=0)
        self.position_embeddings = nn.Embedding(config.max_position_embeddings, config.embedding_size)
        self.token_type_embeddings = nn.Embedding(config.type_vocab_size, config.embedding_size)
        self.LayerNorm = torch.nn.LayerNorm(config.embedding_size, eps=config.layer_norm_eps)

	# forward function is overriden from `BertEmbeddings`
```

Let's see the expected number of parameter of both embedding layers
```python
vocab_size = 30000				# vocabulary size
max_position_embeddings = 512	# maximum length of sequence
type_vocab_size = 2				# possible number of sentence segment
embedding_size = 128			# embedding dimension
hidden_size = 1024				# hidden layer size

# number of embedding parameters of BERT
num_context_embed_params = (vocab_size + max_position_embeddings + type_vocab_size) * hidden_size
num_bert_embed_params = num_context_embed_params

# number of embedding parameters of ALBERT
num_context_embed_params = (vocab_size + max_position_embeddings + type_vocab_size) * embedding_size
num_mapping_params = embedding_size * hidden_size
num_albert_embed_params = num_context_embed_params + num_mapping_params
```

Assuming that `hidden_size` of BERT/ALBERT is 1024 and ALBERT's `embedding_size` is 128, `AlbertEmbeddings` has around 7.74 times less parameters than `BertEmbeddings`. This is HOW `AlbertEmbeddings` can have less parameters than `BertEmbeddings`.


Factorized embedding parameterization (Why)
---------------
However, it is okay or safe to just reduce number from 1024 to 128? I think it is impossible or really difficult to *demonstrate* that it is okay or safe to do so. However, at least, I can deliver some possibilities to reduce the number of parameters.

Let's first expand `num_context_embed_params` from BERT and ALBERT
```python
# BERT's num_context_embed_params = (vocab_size + max_position_embeddings + type_vocab_size) * hidden_size
num_vocab_embed_params = vocab_size * hidden_size					# context-independant parameters
num_position_embed_params = max_position_embeddings * hidden_size	# context-dependant parameters
num_type_embed_params = type_vocab_size * hidden_size				# context-dependant parameters
num_context_embed_parmas = num_vocab_embed_params + num_position_embed_params + num_type_embed_params

# ALBERT's num_context_embed_params = (vocab_size + max_position_embeddings + type_vocab_size) * embedding_size
num_vocab_embed_params = vocab_size * embedding_size					# context-independant parameters
num_position_embed_params = max_position_embeddings * embedding_size	# context-dependant parameters
num_type_embed_params = type_vocab_size * embedding_size				# context-dependant parameters
num_context_embed_parmas = num_vocab_embed_params + num_position_embed_params + num_type_embed_params
```

`num_vocab_embed_params` is context-independant parameters, that is, one vocabulary has one fixed representation. However `num_position_embed_params` and `num_type_embed_params` are context-dependant parameters. Normally `vocab_size` is 30000 or above. So, to represent `vocab_size=30000` vocabularies, `hidden_size=1024` size of vectors were created for each vocabulary. However, compared to `vocab_size`, `max_position_embeddings=512` and `type_vocab_size=2` are too small. This means that `max_position_embeddings` and `type_vocab_size` DO NOT need too big vector size. 

Therefore, let's reduce `num_position_embed_params` and `num_type_embed_params` by replacing `hidden_size` with `embedding_size`. And carefully think about `embedding_size=512` size of vector is large enough for representing `vocab_size=30000`. If `embedding_size` is 512, we can represent one vector as [e0, e1, ..., e511]. Just simply assuming that e0 can have 10 different values, [e0, e1, ..., e511] can have 10^512 different vector, which is still much much larger than `vocab_size=30000`.

A little bit long to read my own evidence. so I summarized the above into three.
- embedding parameters consist of context-independant parameters and context-dependant parameters
- context-dependant parameters are unnecessarily large to learn embedding representation. (-> this is why it is okay to reduce)
- Also, even though we reduce `hidden_size` into `embedding_size`, it is still large to learn word embedding representation. (-> this is why it is safe to reduce)


Cross-layer parameter sharing (How)
---------------
A second way to reduce the number of parameter is through cross-layer parameter sharing. We can simply implement example pseudo code like this.
```python
num_layers = 12

# Layer pseudo code
class Layer(nn.Module):
	def __init__(self, config):
		self.some_functions = ..
		...

	def forward(self, input_ids):
		x = self.some_functions(input_ids)
		...
		return x

# BERT style of layer definition
layers = [Layer(conf) for _ in range(num_layers)]

# BERT style of layer forwarding
x = some_values
for layer in layers:
	x = layer(x)	# parameter of `layer` always differ through iteration


# ALBERT style of layer definition
layer = Layer(conf)

# ALBERT style of layer forwarding
x = some_values
for _ in range(num_layers):
	x = layer(x)	# parameter of `layer` always remain same through iteration
```

If you read the above code carefully, it is not difficult to understand how the number of parameters can be reduced across the layers. At ALBERT, only one `Layer` object was created and this one iteratively was used through the iteration, while the `Layer` object was created `num_layers` times at BERT. Normally `num_layers` is 6 to 12. So 1/6-1/12 is the expected ratio of parameter reduction.

Cross-layer parameter sharing (Why)
---------------
Okay, I understand the number of parameters can be reduced with cross-layer parameter sharing. But why is it okay or safe to do so? Actually if you read the original paper of [**ALBERT**](https://arxiv.org/pdf/1909.11942.pdf), you can find the evidence.

```
"We observe that the transitions from layer to layer are much smoother for ALBERT than for BERT. These results show that weight-sharing has an effect on stabilizing network parameters."
```

| ![Figure 1](http://jinkilee.github.io/img/doodle/fig1.png) |
|:--:|
| *Figure 1: Differance between input/output embedding vector(Left:ALBERT, Right:BERT)* |

You can see a smoother plot from ALBERT than BERT. ALBERT looks good. But why? Why smoother embedding distance is better than fluctuating one? Smoother plot means through the `num_layers` difference(L2/cosine distance) between input and output embeddings are consistant and small. Let's see the pseudo code of this. Working example is on my [**github repository**](https://github.com/jinkilee/jinkilee.github.io/tree/master/code/python/ai/ipynb/albert.ipynb)
```python
# BERT's input/output embedding
for i, layer in enumerate(layers):
	out = layer(x)
	print('BERT's L2 difference between inputs and outputs at {}th layer: {:.4f}'.format(i, l2(x, out)))
	x = out

# ALBERT's input/output embedding
for i in range(num_layers):
	out = layer(x)
	print('ALBERT's L2 difference between inputs and outputs at {}th layer: {:.4f}'.format(i, l2(x, out)))
	x = out
```

-- TBD again
-- Having small L2 distance difference means `inputs` and `output` are not very different. But is it something good? It sounds like... even though `inputs` goes through neural network, `output` is similar to `inputs`. In the paper, what the authors said is

```
-- "Very recently, Bai et al. (2019) propose a Deep Equilibrium Model (DQE) for transformer networks and show that DQE can reach an equilibrium point for which the input embedding and the output embedding of a certain layer stay the same. Our observations show that our embeddings are oscillating rather than converging."
```

-- According to the DQE paper, DQE for transformer can reach a point where input/output embeddings are nearly same. We say this point as equilibrium point.

Sentence order prediction(SOP)
---------------
The last thing I want to mention is the SOP. At BERT, Next Sentence Prediction(NSP) was used to build a pre-trained BERT model. After BERT, many researchers suspected if NSP is really effective in learning Language. On the top of my head, compared to predicting masked word, NSP looks too easy, which somehow may lead to over-fitting. This is why NSP is upgraded to SOP. 

While BERT only knows two sentences are in similar relation, ALBERT knows which one comes first. Here I want to throw two questions.
- Can BERT do SOP?
- Can ALBERT do NSP?

Let's check the first question.
```python
import numpy as np
import torch
from pytorch_pretrained_bert import BertTokenizer, BertModel, BertForMaskedLM, BertForNextSentencePrediction

model_nm = 'bert-base-uncased'

# Load pre-trained model tokenizer (vocabulary)
tokenizer = BertTokenizer.from_pretrained(model_nm)

# NSP label should be 0
sent_1 = 'How old are you?'
sent_2 = 'I am 35 years old'

# NSP label should be 0
sent_1 = 'is Obama the president of the US?'
sent_2 = 'No but he was'

# NSP label should be 1
# sent_1 = 'How old are you?'
# sent_2 = 'The Eiffel Tower is in Paris'


# Tokenized input
text = ' '.join(['[CLS]', sent_1, '[SEP]', sent_2, '[SEP]'])
tokenized_text = tokenizer.tokenize(text)

# Convert token to vocabulary indices
indexed_tokens = tokenizer.convert_tokens_to_ids(tokenized_text)
segments_ids = (len(tokenizer.tokenize(sent_1))+2)*[0] + (len(tokenizer.tokenize(sent_2))+1)*[1]

# Convert inputs to PyTorch tensors
tokens_tensor = torch.tensor([indexed_tokens])
segments_tensors = torch.tensor([segments_ids])

# Load pre-trained model (weights)
model = BertForNextSentencePrediction.from_pretrained(model_nm)
model.eval()

output = model(tokens_tensor, segments_tensors)
logits = output[0]
logits
tensor([ 5.5330, -4.8882], grad_fn=<SelectBackward>)
```

And this is the result.
```
# Sentence-pair A (expected answer: 0)
- How old are you?
- I am 35 years old

# Sentence-pair B (expected answer: 1)
- How old are you?
- The Eiffel Tower is in Paris

# Sentence-pair C (expected answer: 0)
- Is Obama the president of the US?
- No but he was
```
| Sentences         | NSP | SOP |
| ----------------- |:---:|:---:|
| Sentence-pair A   |  O  |  X  |
| Sentence-pair B   |  O  |  X  |
| Sentence-pair C   |  O  |  X  |

You can see the jupyter notebook result from [**here**](http://121.161.230.192:9999/notebooks/bert.ipynb)
As you can see, BERT can do NSP(of course) but not SOP.

-- TBD
-- Can ALBERT do NSP?
-- For what I tested so far, SOP was not implemented in Pytorch's ALBERT and Tensorflow's ALBERT SOP could not do neighther NSP nor SOP.










