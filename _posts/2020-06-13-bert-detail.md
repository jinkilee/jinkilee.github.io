---
title: "BERT Structure with detail"
date: 2020-06-13 08:26:28 -0400
categories: AI
---

이전의 글에서([**BERT Structure(https://github.com/jinkilee/jinkilee.github.io/blob/master/_posts/2020-05-24-bert.md)**]) BERT의 Input에 대해서 Output이 어떻게 나오게 되는지를 살펴봤다. 여러가지 이야기를 했지만 가장 중요한 내용은 하나다.
```
BERT의 Input은 (B, M) shape의 vector이고 Output은 (B, M, E) shape의 vector이다.
```

그런데 사실 BERT의 Input에 아래의 세가지가 더 들어간다. 아래의 내용들이 어떤 블록에 어떻게 들어가는지 알아보자.
- `token_type_ids`
- `head_mask`
- `attention_mask`

### `token_type_ids`
`token_type_ids`는 `sent_a`일경우 0, `sent_b`일 경우 1인 (B, M) shape의 vector이고, `position_ids`는 [0, M-1] 범위의 숫자를 갖는 (B, M) shape의 vector이다. `token_type_ids`와 `position_ids`를 만드는 과정을 파이선 코드로 간단하게 봐보자.

```python
# example data
bos = [1]
eos = [2]
sent_a = [5,5,5,3,0,0,0]	# len(sent_a) == 7
sent_b = [6,6,6,0,0,0,0]	# len(sent_b) == 7

# make inputs
input_ids = bos + sent_a + eos + sent_b + eos	# len(input_ids) == 17
token_type_ids = [0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1]	# len(token_type_ids) == 17
position_ids = [0,1,2,3,4,5,6,7,8,9,10,12,13,14,15,16]	# len(position_ids) == 17

# embedding
inputs_embeds = self.word_embeddings(input_ids)
position_embeddings = self.position_embeddings(position_ids)
token_type_embeddings = self.token_type_embeddings(token_type_ids)
embeddings = inputs_embeds + position_embeddings + token_type_embeddings
```

`token_type_ids`를 통해서 `sent_a`와 `sent_b`를 구분하는 것이다. 그리고 `position_ids`는 마치 attention처럼 강조하고자 하는 부분에 해당하는 embedding을 더해주는 느낌으로 생각하면 된다.  보통 `position_ids`는 0부터 M-1까지의 숫자를 차례대로 체우는 것으로 대신한다. 그런데 여기에서 중요한 것이 있다. 
```
`position_ids`로 인해서 같은 단어도 embedding이 다르게 될 수 있다.
```

그 이유는 embedding을 만들 때 아래와 같이 각각의 embedding을 모두 더해주기 때문이다.
```
# embedding
inputs_embeds = self.word_embeddings(input_ids)
position_embeddings = self.position_embeddings(position_ids)
token_type_embeddings = self.token_type_embeddings(token_type_ids)
embeddings = inputs_embeds + position_embeddings + token_type_embeddings
```

위와 같이 연산을 하면 같은 hello라는 단어여도 앞에 나오는 hello의 embedding과 뒤에 나오는 hello의 embedding이 서로 다른 값이 된다.

# FIXME
`sent_a`와 `sent_b`가 무엇인지는 link에서 나오니 참고하면 된다.


### `head_mask`와 `attention_mask`
`sent_a`와 `sent_b`를 만들 때 각각 padding이 된다. `head_mask`는 padding값일 경우 1, 그렇지 않을 경우 0인 (B, M) shape의 vector이다. `attention_mask`는 attention을 적용할 곳은 1 그렇지 않을 곳은 0이 체워진 (B, M) shape의 vector이다.

`head_mask`와 `attention_mask`는 `BertSelfAttention`에서만 쓰이는데, 아래와 같이 쓰인다.
```python
# `attention_score`를 구하는 과정은 생략했다.
attention_scores = attention_scores + attention_mask
attention_probs = nn.Softmax(dim=-1)(attention_scores)
attention_probs = self.dropout(attention_probs)

if head_mask is not None:
	attention_probs = attention_probs * head_mask

context_layer = torch.matmul(attention_probs, value_layer)
context_layer = context_layer.permute(0, 2, 1, 3).contiguous()
...
```
`attention_scores`에 `attention_mask`를 더해서 
### TBD
input이 더해진다는 것!! 내용 추가하기!!


https://github.com/huggingface/transformers/blob/master/notebooks/02-transformers.ipynb
