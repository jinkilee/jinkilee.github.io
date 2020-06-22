---
title: "BERT Structure with detail"
date: 2020-06-13 08:26:28 -0400
categories: AI
---

이전의 글에서
- [BERT Structure](https://github.com/jinkilee/jinkilee.github.io/blob/master/_posts/2020-05-24-bert.md)
- [BERT Training](https://github.com/jinkilee/jinkilee.github.io/blob/master/_posts/2020-06-18-bert-pretrain.md)

BERT의 Input에 대해서 Output이 어떻게 나오게 되는지 그리고 어떻게 학습되는지를 살펴봤다. 여러가지 이야기를 했지만 가장 중요한 내용은 하나다.
```
- BERT의 Input은 (B, M) shape의 vector이고 Output은 (B, M, E) shape의 vector이다.
- BERT는 `sent_a`와 `sent_b`를 이용해서 MLM과 NSP를 이용해 학습한다.
```

그런데 사실 BERT의 Input에 아래의 세가지가 더 들어간다. 아래의 내용들이 어떤 블록에 어떻게 들어가는지 알아보자.
- `token_type_ids`
- `position_ids`
- `attention_mask`

### `token_type_ids`와 `position_ids`
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
inputs_embeds = self.word_embeddings(input_ids)	# (B,M,E)
position_embeddings = self.position_embeddings(position_ids) # (B,M,E)
token_type_embeddings = self.token_type_embeddings(token_type_ids) # (B,M,E)
embeddings = inputs_embeds + position_embeddings + token_type_embeddings # (B,M,E)
```

`token_type_ids`를 통해서 `sent_a`와 `sent_b`를 구분하는 것이다. 그리고 `position_ids`는 마치 attention처럼 강조하고자 하는 부분에 해당하는 embedding을 더해주는 느낌으로 생각하면 된다.  보통 `position_ids`는 0부터 M-1까지의 숫자를 차례대로 체우는 것으로 대신한다. 그런데 여기에서 중요한 것이 있다. `position_ids`로 인해서 같은 단어도 embedding이 다르게 될 수 있다.

그 이유는 embedding을 만들 때 아래와 같이 각각의 embedding을 모두 더해주기 때문이다.
```
# embedding
inputs_embeds = self.word_embeddings(input_ids)	# (B,M,E)
position_embeddings = self.position_embeddings(position_ids) # (B,M,E)
token_type_embeddings = self.token_type_embeddings(token_type_ids) # (B,M,E)
embeddings = inputs_embeds + position_embeddings + token_type_embeddings # (B,M,E)
```

위와 같이 연산을 하면 같은 hello라는 단어여도 앞에 나오는 hello의 embedding과 뒤에 나오는 hello의 embedding이 서로 다른 값이 된다.

### `attention_mask`
`attention_mask`는 attention을 적용시켜줄 부분에 1, 그렇지 않을 부분에 0으로 표시한다. 위의 예를 이용해서 `attention_mask`를 만들면 아래와 같다.
```python
# padding 자리에 0, 나머지는 1
attention_mask = [1,1,1,1,1,0,0,0,1,1,1,1,0,0,0,0,0]
```

### reference
- https://github.com/huggingface/transformers/blob/master/notebooks/02-transformers.ipynb
