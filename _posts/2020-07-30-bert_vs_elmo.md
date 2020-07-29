---
title: "BERT VS ELMo"
date: 2020-07-30 08:26:28 -0400
categories: AI
---

이 글에서는 BERT와 ELMo의 차이점에 대해서만 간략하게 짚어보려고 한다. 그 전에 ELMo에 대해서 간략하게 이야기해보고 넘어가자.

ELMo(Embedding from Language Model)
-------------------------
ELMo는 [**allenai**](https://allenai.org/)에서 2018년 2월에 처음 발표된 모델이다.(최종 버전은 5월에 발표됐다.) 이 논문의 원래의 제목은 `Deep contextualized word representations`이다. 기존의 language model과 비교했을 때, 거의 처음으로 contextualized word embedding을 채택한 모델이라고 생각하면 될 것 같다. ELMo의 큰 특징은 아래와 같다.
- Contextualized word embedding
- 다음 단어를 예측하는 방식의 Language Model
- Bi-LSTM 형태로 모델을 구성하여 LSTM이 순방향과 역방향 모두 계산이 된다.

ELMo Example
---------------
ELMo를 `allennlp`라는 패키지를 이용해서 간단하게 실행시켜볼 수 있다.
```python
from allennlp.modules.elmo import Elmo, batch_to_ids

options_file = "https://s3-us-west-2.amazonaws.com/allennlp/models/elmo/2x4096_512_2048cnn_2xhighway/elmo_2x4096_512_2048cnn_2xhighway_options.json"
weight_file = "https://s3-us-west-2.amazonaws.com/allennlp/models/elmo/2x4096_512_2048cnn_2xhighway/elmo_2x4096_512_2048cnn_2xhighway_weights.hdf5"

# Compute two different representation for each token.
# Each representation is a linear weighted combination for the
# 3 layers in ELMo (i.e., charcnn, the outputs of the two BiLSTM))
elmo = Elmo(options_file, weight_file, 2, dropout=0)

# use batch_to_ids to convert sentences to character ids
sentences = [
    ['New', 'yorkers', '.'],
    ['New', 'yorker', '.'],
    ['New', 'commers', '.'],
]
character_ids = batch_to_ids(sentences)

embeddings = elmo(character_ids)
fwd_embeddings, bwd_embeddings = embeddings['elmo_representations']

for s, f, b in zip(sentences, fwd_embeddings, bwd_embeddings):
    print(s)
    print(f.shape, b.shape, (f==b).float().mean())
    print(f.sum(dim=1), b.sum(dim=1))
    print('--------------')
```
위의 코드를 실행하면 아래와 같은 결과를 얻을 수 있다.
```
['New', 'yorkers', '.']
torch.Size([3, 1024]) torch.Size([3, 1024]) tensor(1.)
tensor([ 5.2636, -2.4707,  1.8964], grad_fn=<SumBackward1>) tensor([ 5.2636, -2.4707,  1.8964], grad_fn=<SumBackward1>)
--------------
['New', 'yorker', '.']
torch.Size([3, 1024]) torch.Size([3, 1024]) tensor(1.)
tensor([ 8.3876, -0.5249,  2.8822], grad_fn=<SumBackward1>) tensor([ 8.3876, -0.5249,  2.8822], grad_fn=<SumBackward1>)
--------------
['New', 'commers', '.']
torch.Size([3, 1024]) torch.Size([3, 1024]) tensor(1.)
tensor([10.2149, 30.8928,  1.3071], grad_fn=<SumBackward1>) tensor([10.2149, 30.8928,  1.3071], grad_fn=<SumBackward1>)
--------------
```
주의해서 볼 내용이 `New`라는 단어가 세 문장 모두 들어갔는데, 모두 다른 벡터를 가지고 있다는 것이다.
그나마 `New yorkers`와 `New yorker`는 비슷하니까 벡터(합)가 `5.2636` VS `8.3876` 정도 차이가 나는 것 같다. `New commers`처럼 전혀 다른 뜻에서는 `10.2149`와 같이 전혀 다른 값을 갖게 된다.

BERT VS ELMo: 개요
------------------------
성능을 떠나서 구현적/개념적 차이를 논해보자. 차이가 나는 부분은 아래와 같다.
- 학습방법: Masked Language Model VS Next word prediction
- 구조: Transformer VS Bi-LSTM

BERT VS ELMo: 학습방법
------------------------
BERT에서는 `I like an apple`에서 `an apple` 대신에 `a banana`가 들어갈 수 있는 가능성을 위해 일부는 정답을 바꿔서 일부러 틀리게 하는 학습 전략도 있었다. 하지만 ELMo는 그런 측면에서는 정직하게 다음 단어만을 맞추는 모델이다. 





