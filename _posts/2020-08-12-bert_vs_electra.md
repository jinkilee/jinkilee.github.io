---
title: "BERT VS Electra"
date: 2020-08-12 08:26:28 -0400
categories: AI
---

이 글에서는 ELECTRA를 공부해보려고 한다. 목차는 아래와 같다.

- Introduction
- Modeling details
- Benchmark

Introduction
----------------
ELECTRA는 Google에서 발표한 새로운 학습 방법을 이용한 Language Model이다. 이 논문에서 가장 중요한 내용은 아래와 같다.
```
훨씬 적은 수의 파라미터로 훨씬 빠르게 Language Model을 학습할 수 있다.
```
이를 가능케하는 방법을 이 글에서 설명해보려고 한다. 아래의 Modeling details에서 그 내용들을 이야기 하고 Benchmark에서 타 LM모델들과 비교를 한 후 이 글을 마치려고 한다.

Modeling details
-----------------
ELECTRA는 Efficiently Learning an Encoder that Classifies Token Replacements Accurately의 약자다. (길다...) Token Replacements를 정확하게 잘 학습하는 인코더를 효과적으로 학습한다는 뜻이다. 무슨말인가... ELECTRA의 가장 큰 핵심은 Replaced Token Detection인데, 이것에 대해서 알아보도록 하자.

### Masked Language Model and Replaced Token Detection (MLM and RTD)
기존의 BERT에서는 MLM을 이용해서 LM의 성능을 비약적으로 발전시켰다. MLM을 이용한 BERT는 한번 학습하는데 굉장히 많은 HW 리소스와 시간을 소모한다. ELECTRA를 학습할 때 GAN과 같이 Generator와 Discriminator로 나눈다. ELECTRA의 Generator는 BERT의 MLM과 같은 방법으로 학습을 한다. Discriminator를 학습할 때 RTD를 이용한다.

길게 설명할 필요 없이 아래의 예제로 모두 설명할 수 있다. 학습할 때 데이터가 변하는 과정을 설명한 예제이다.
```
inputs = ['the', 'chef', 'cooked', 'the', 'meal']
masked = ['[MASK]', 'chef', '[MASK]', 'the', 'meal']
generated = ['the', 'chef', 'ate', 'the', 'meal']
is_replaced = [0, 0, 1, 0, 0]
```
`inputs`에서 랜덤으로 토큰 몇 개를 선택해서 `masked`를 만든다. `masked`를 이용해서 MLM을 학습하는 것이 ELECTRA의 Generator이다. 그렇게 해서 Generator가 만들어낸 문장이 `generated`인데, 이 문장을 원래의 `inputs`과 비교해서 바뀌었는지(1) 그렇지 않은지(0)을 판단해서 `is_replaced`를 만든다. 즉 원래의 데이터에서 데이터가 바뀌었는지를 토큰마다 판단하게 된다. 각 토큰마다 바뀌었는지를 확인하게 된다는 것은 모든 토큰이 학습에 사용된다는 뜻이다.

ELECTRA의 Discriminator가 모든 토큰을 사용해서 학습을 하게 되는데, 이로 인해서 BERT에 비해 학습속도가 확 줄어들게 된다는 것이 이 논문의 핵심이다. 

BERT에서는 MLM 이후에는 Next Sentence Prediction(NSP)를 했다. NSP에서 모든 토큰이 학습에 직접 사용되지는 않는다. NSP의 입력으로 MLM의 결과값이 들어가지만 직접적으로 하나하나의 토큰을 이용해서 학습을 하는 것은 아니기 때문이다. 즉, BERT에서는 MLM에서 랜덤으로 선택된 15% 만이 학습에 직접적으로 사용된다는 뜻이다.
```
BERT는 MLM → NSP (전체 Token의 15% 만이 학습에 직접적으로 사용됨)
ELECTRA는 MLM → RTD (전체 Token이 모두 학습에 직접적으로 사용됨)
```

논문에서 이 개념을 그림 하나로 잘 설명하고 있다.
그림1

Training details
--------------------
학습시 알아봐야 할 몇가지 디테일이 있다.
- Weight sharing
- Smaller generator

### Weight sharing
말 그대로 학습된 Weight을 share하는 것이다. Generator와 Discriminator가 서로서로 Weight을 공유한다. Generator를 하나의 BERT 구조로 보고 Discriminator를 또 다른 BERT 구조로 봤을 떄 둘이는 서로 같은 구조이기 때문에 Weight을 공유할 수 있다. 

![weight sharing of ELECTRA](../img/electra_structure.png)

그런데 여러번의 실험의 결과 Generator를 Discriminator보다 좀 작은 모델로 만드는 것이 좀 더 성능이 좋게 나왔다고 한다. 이럴 경우 Generator와 Discriminator의 파라미터 개수가 다르기 때문에 완전한 Weight sharing을 할 수 없다. 따라서 부분적으로 할 수 있는 부분만 찾아서 Weight sharing을 하는데, 그 부분이 token embedding과 positional embedding이다. 
```
"...However, we found it to be more efficient to have a small generator, in which case we only share the embeddings (both the token and positional embeddings) of the generator and discriminator...."
```

### Smaller Generator
위에서 언급한데로 ELECTRA에서 Discriminator보다 Generator의 크기를 더 작게 해서 사용한다. 실험 결과 Generator의 사이즈가 Discriminator 사이즈의 1/4에서 1/2 정도 됐을 때 성능이 가장 좋았다고 한다. 이 때, Generator 크기를 작게 하기 위해 레이어 사이즈를 줄이고 다른 파라미터는 같게 뒀다고 한다. 

![smaller generator](../img/small_generator.png)


Benchmark
-------------------
























































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





