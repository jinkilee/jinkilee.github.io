---
title: "Transformer: Attention is all you need"
date: 2020-04-23 08:26:28 -0400
categories: AI
---
Transformer를 이용해서 번역기를 만들어봤다. 회사일과 육아와 이것 저것을 병행하면서 하다보니 2달이나 걸렸다. 어쨌든 아래와 같은 순서로 포스팅을 해보려고 한다.
1. 데이터셋 디테일
2. 데이터 전처리
3. 입력/출력/평가
4. 트랜스포머 구조 step-by-step
5. optimizer/label-encoding
6. 학습 파라미터 및 Multi-GPU 환경
7. 모델 학습 결과


2월 달에 seq2seq 모델과 attention을 이용해서 한국어-영어 번역기를 만들어봤다. (link) 이번에는 한국어-영어 번역기를 트랜스포머 형태로 만들어보려고 한다. 트랜스포머를 이용해서 번역기를 만들 경우 번역 품질이 얼마나 더 좋아지는지 문장으로 그리고 BLEU 스코어를 기준으로 알아보자.

데이터셋 디테일
--------------------
aihub에서 약 160만개 정도의 한국어-영어 번역 데이터셋을 다운받았다. ([**link**](http://www.aihub.or.kr/aidata/87)) 다운로드 받은 데이터는 아래와 같이 다양한 영역으로 구성돼 있다.
```
뉴스 뉴스 텍스트 80만 문장
정부 웹사이트/저널 정부/지자체 홈페이지,간행물 10만 문장
법률 행정 규칙,자치 법규 10만 문장
한국문화 한국 역사,문화 콘텐츠 10만 문장
구어체 자연스러운 구어체 문장 40만 문장
대화체 상황/시나리오 기반 대화 세트 10만 문장
>> 합계 160만 문장
```

엑셀파일로 구성돼 있으며 아래와 같이 한국어-영어 쌍 형태로 구성돼 있다.
```
>>> sent_pairs[0]
['우리 팀 구장은 화장실 때문에 불만들이 많아요.',
 'There are a lot of complaints about our stadium because of the restroom.']
```

데이터 전처리
--------------------
데이터 전처리에는 google에서 연구한 sentencepiece를 이용했다. sentencepiece는 아래의 특징을 가진다.
- 모든 단어 앞에 _ 를 붙인다. 
- 단어 내에서도 빈도를 고려해서 쪼갤 수 있는 단위까지 쪼갠다.

예를 들면 아래와 같다.
```
Jinki likes to eat
STEP1: _Jinki _likes _to _eat → _ 붙이기
STEP2: _J ink i _likes _to _eat → 단어별로 "빈도를 고려해서" 쪼갤 수 있을 때까지 쪼개기
```

STEP2에서 "빈도를 고려한다"는 의미는 예를 들어서 Jinki 안에 있는 ink는 이전에도 많이 쓰였던 단어일 수 있다. 먹물=ink. 그래서 _J와 ink 그리고 마지막 i를 따로 본다.
이렇게 두면 STEP2의 단어에서 원래의 문장으로 쉽게 복호화도 가능하다. 

Jinki는 이름이지 J + ink + i가 아니다. 그렇지만 상관 없다고 보는 것이다. 나머지 부분은 그냥 알고리즘에 맡기는 컨샙이고, 어짜피 Jinki가 많이 나오는 단어가 아니기도 하다. 예를 들어 "문재인"은 한 단어로 인식해서 "_문재인"으로 인식하게 될 수도 있다.

sentencepiece의 장점은 문장의 개수가 늘어나더라도 vocabulary 사이즈가 크게 늘어나지 않는다는 점이다. 빈도가 약한 단어에 대해서는 최대한 작은 단위로 쪼개는 원리이기 때문이다. 가령, 영어로 치면 영어 단어의 개수는 어마어마하게 많지만 알파벳의 개수는 고작 26개이다.


입력/출력/학습/평가
--------------------
데이터 전처리 다음에 다룰 내용은 입력/출력/학습/평가 방법에 대한 내용이다. 우선 학습하는 상황을 가정하고 입력/출력을 따져보려고 한다. 아래의 예제를 봐보자. 아래의 예시에서 이해를 돕기 위해 indexing은 생략했다. 
```
# 학습할 때
src: 내 컴퓨터가 고장났어
trg: my computer is not working

# tokenize
src: 내, 컴퓨터, 가, 고장, 났어
trg: <s>, my, computer, is, not, working, </s>

# 학습 과정
>> STEP1: src과 trg[:-1]을 model의 입력으로 넣어서 trg[1:]에 대한 embedding을 구한다.
src: 내, 컴퓨터, 가, 고장, 났어
trg[:-1]: <s>, my, computer, is, not, working
예를 들어서 위의 예시로 512 사이즈로 embedding을 구하려고 할 때, (6, 512) 사이즈의 embedding을 구하게 된다.
inp/out=(5,)(6,) --model--> emb=(6, 512)

>> STEP2: embedding에 간단하게 classifier를 씌워서 trg[1:]과 하나하나 비교해서 각 단어별로 loss를 구한다.
emb=(6, 512) --classifier--> pred=(6, 32000) VS trg[1:]=(6,)

>> STEP3: 각 단어별로 구한 loss를 평균내서 최종 loss를 구한다.
```

기본적으로 트랜스포머는 결국 embedding을 해주는 모델이다. 따라서 위와 같이 model에 inp/out을 넣었을 때 out에 대한 embedding을 구할 수 있다. model에 inp/out을 동시에 넣은 것처럼 보이지만 실제로는 아래와 같이 encoder와 decoder를 차례로 거친 결과이다.
inp=(5,) --model.encoder--> src_emb/trg=(5, 512)(6,) --model.decoder--> trg_emb(6, 512)

학습 과정은 결국 번역할 문장과 번역될 문장을 트랜스포머 모델에 넣어서 번역될 문장의 embedding을 구한 후, 그것을 classifier에 넣어서 번역된 문장과 비교해서 loss를 구하고 그 loss를 줄여나가는 방식으로 학습하는 모델로 정리할 수 있다.

평가는(evaluate) 다음과 같이 할 수 있다.
```
# 번역할 때
src: 내 컴퓨터가 고장났어
trg: ??

# tokenize
src: 내, 컴퓨터, 가, 고장, 났어

# 번역 과정
>> STEP1: src와 src_mask를 model.encoder에 넣어서 src에 대한 embedding을 구한다. embedding 사이즈를 512로 한다고 가정하고 아래의 예제를 봐보자.
src: 내, 컴퓨터, 가, 고장, 났어
src_mask: 1, 1, 1, 1, 1
src/src_mask=(5,)(5,) --model.encoder--> src_emb=(5, 512)

>> STEP2: src_emb를 이용해서 <s>부터 차근차근 loop를 돌며 다음 단어를 예측해나간다.
0th iteration: src_emb/trg=(5, 512)(1,) --model.decoder--> trg_emb=(6, 512) --classifier--> (6, 32000)
1th iteration: src_emb/trg=(5, 512)(2,) --model.decoder--> trg_emb=(6, 512) --classifier--> (6, 32000)
..
5th iteration: src_emb/trg=(5, 512)(6,) --model.decoder--> trg_emb=(6, 512) --classifier--> (6, 32000)
```

여기서 중요한 것은, 번역할 때는 번역한 문장에 대한 정보가 전혀 없다는 것이다. 따라서 번역할 문장의 embedding을 먼저 구하고, 그 embedding을 이용해서 trg_emb를 구해서 classifier에 넣는다. classifier는 결국 번역된 단어 하나하나를 예측하는 꼴이 된다.

트랜스포머 구조
--------------------
트랜스포머의 구조를 알아보자. 보통 시퀀스를 학습할 때 RNN 계열의 구조를 쓰는 것이 매우 일반화돼 있었으나, 트랜스포머는 RNN 계열의 구조를 사용하지 않는다. 트랜스포머를 처음 소개한 논문의 제목이 `Attention is all you need`인 것을 보면 알 수 있듯이 Attention을 강조한 구조다. 단위 연산만 보면 reshape, 행렬 곱샘, 행렬 잇기/쪼개기, softmax 함수 적용 등등의 단순 연산만으로 이루어진 구조일 뿐인데 그런 연산들이 너무 많아서 구조를 하나하나 보기에는 조금 복잡할 수 있다.
그 복잡한 구조를 아래의 블로그에서 매우 디테일하게 소개하고 있다. 트랜스포머에 대해서 더 자세하게 연구하고자 한다면 아래의 링크를 참고하라.
link

여기에서는 자세한 구조보다도 숲과 나무 중간의 디테일로 설명해보고자 한다. 우선 트랜스포머의 입력과 출력은 아래와 같다.
```
# 입력
src = (B, M1)
trg = (B, M2)

# 출력
out = (B, M2, E)
```

트랜스포머는 크게 Encoder와 Decoder로 구성돼 있다. Encoder와 Decoder에 src와 trg를 넣으려면 먼저 Embedding을 거쳐야 한다. Embedding을 함께 그리면 아래와 같이 트랜스포머의 구조를 그려볼 수 있다. 트랜스포머의 입력은 두 종류인데, `src(=번역할 문장)`과 `trg(=번역된 문장)`이다. encoder의 입력은 `src`만 들어가고 decoder에서는 `encoder의 출력`이 `trg`와 함께 들어가기 때문에 아래와 같은 구조가 된다.
![Figure 1](http://jinkilee.github.io/img/transformer/transformer1.png)
|:--:|
| *Figure 1: Transformer: Encoder/Decoder with Embedding* |

```
# Encoder
입력: (B, M1, E)
출력: (B, M1, E)

# Decoder
입력: (B, M1, E), (B, M2, E)
출력: (B, M2, E)
```

여기에서 Encoder와 Decoder를 조금 더 자세하게 그려보자. Encoder와 Decoder는 각각 6개의 EncoderLayer와 DecoderLayer로 구성돼 있다. (6개는 파라미터 값이므로 변경 가능하다.) 
![Figure 2](http://jinkilee.github.io/img/transformer/transformer2.png)
|:--:|
| *Figure 2: Transformer: Encoder/Decoder with its Layer structure* |

트랜스포머의 꽃! Attention은 EncoderLayer와 DecoderLayer에 들어가 있다. 그 구조는 아래와 같다.

![Figure 3](http://jinkilee.github.io/img/transformer/transformer3.png)
|:--:|
| *Figure 3: Transformer: EncoderLayer/DecoderLayer structure* |

EncoderLayer이든 DecoderLayer이든 입력과 출력의 shape은 같다. 이 레이어들의 역할은 쉽게 생각해서 Attention을 통해 Embedding을 더 강력하게 해준다고 생각하면 된다. 각 레이어에 대해서 조금만 더 설명해보자.
EncoderLayer는 SelfAttention 하나와 FeedForward 레이어로 구성된다. 그에 반에 DecoderLayer는 SelfAttention, EncoderDecoderLayer, FeedForward루 구성된다.

왜 그럴까? EncoderLayer는 `src`만 입력으로 들어가기 때문에 "SELF" Attention이다. 비교할 것이 자기 자신밖에 없다. 반면에 DecoderLayer에는 `EncoderLayer의 출력`과 `trg`가 입력으로 들어간다. `trg`를 이용해서 SelfAttention을 구하고 그 결과와 EncoderLayer의 출력을 이용해서 EncoderDecoderAttention을 구하는 것이다.

트랜스포머의 입력과 출력에 집중하기 위해 여기까지만 설명하려고 한다. 더 자세한 설명은 위에서 소개했던 블로그를 보면 된다.

optimizer/label-encoding
--------------------
학습을 시작하기 전에 마지막으로 고려할 것은 optimizer와 label-encoding이다.

optimizer는 `torch.optim.Optimizer`를 상속받아서 `NoamOpt`라는 custom optimizer를 이용했다. 이 optimizer 내에서 실제로 사용하는 optimizer는 Adam Optimizer이다. Adam Optimizer와 다른 점은 scheduling 기능을 `NoamOpt.step` 함수를 이용해서 구현했다는 것인데, step 함수를 통해서 매번 learning rate을 변화시킬 수 있다. NoamOpt를 이용하면 학습을 진행할 때마다 learning rate이 아래와 같은 추이로 변화하게 된다.
그림

그 다음에 추가해주면 좋은 것은 label-encoding이다.

학습 파라미터 및 Multi-GPU 환경
--------------------
트랜스포머 기반의 모델은 학습이 오래 걸리기 때문에 학습하는 처음에 학습 파라미터도 잘 설정해야하며, 무엇보다도 어느 정도의 하드웨어도 받쳐줘야 한다. 이번에 학습한 트랜스포머의 파라미터는 아래와 같다.
```
src_vocab_size = 50000 # vocab 사이즈
trg_vocab_size = 32000 # vocab 사이즈
d_model = 1024
d_ff = 4096
h = 16
dropout = 0.3
N = 6
epochs = 45
```
위 파라미터로 학습을 할 경우, 약 3.4G정도 되는 모델이 학습된다.

학습은 Multi-GPU 환경에서 진행했다. 하나의 GPU는 부족하다. 따라서 여러 개의 GPU를 이용해서 병렬로 학습을 진행했다. 하드웨어와 학습 시간은 아래와 같다.
- GPU: TitanX(Pascal) GPU 4개
- 학습시간: 약 50시간

Multi-GPU를 이용해서 병렬로 학습할 경우 아래와 같이 학습하면 된다.
![Figure 4](http://jinkilee.github.io/img/transformer/tmulti-gpu-trainin.png)
|:--:|
| *Figure 4: Multi-GPU Training* |


모델 학습 결과
--------------------
가장 중요한 모델 학습 결과이다. 번역된 결과를 보면 굉장히 깔끔하다는 것을 알 수 있다.
```
Input::	여성뿐만이 아니에요.
Translation:	It is not only a woman.
Target:	▁It ▁is ▁not ▁only ▁for ▁women . 

Input::	저희도 와이파이 비밀번호를 몰라요.
Translation:	We don't know the Wi-Fi password.
Target:	▁We ▁also ▁don ' t ▁know ▁the ▁wifi ▁password . 

Input::	나는 스마트폰이 유용하다고 생각해요.
Translation:	I think smartphones are useful.
Target:	▁I ▁think ▁smartphones ▁are ▁useful . 

Input::	당신은 로맨틱한 남자를 좋아하나요?
Translation:	Do you like romantic guy?
Target:	▁Do ▁you ▁like ▁a ▁romantic ▁guy ? 
```

물론 틀리거나 부족한 문장들도 있다.
```
Input::	결핵약을 어떻게 먹어야하죠?
Translation:	How can I take a nap?
Target:	▁How ▁can ▁I ▁take ▁this ▁tuberculosis ▁medicine ? 

Input::	열심히 노력해서 꼭 승무원이 되세요.
Translation:	Be sure to work hard and get a flight attendant.
Target:	▁Try ▁hard ▁to ▁be ▁a ▁flight ▁attendant . 
```

3월 4월에 걸쳐 트랜스포머로 번역기를 만들어봤다. 다음번에는 Torch 모델을 실시간으로 Deploy 하기 위한 방법을 알아보려고 한다.

Reference
--------------------
- [**한국어-영어 데이터셋**](http://www.aihub.or.kr/aidata/87)
- [**attention is all you need**](http://jalammar.github.io/illustrated-transformer/)
- [**multi-GPU training**](https://medium.com/daangn/pytorch-multi-gpu-%ED%95%99%EC%8A%B5-%EC%A0%9C%EB%8C%80%EB%A1%9C-%ED%95%98%EA%B8%B0-27270617936b)
- [**apex**](https://github.com/NVIDIA/apex)
- [**github**](https://github.com/jinkilee/LaH)
- [**sentencepiece**](https://lovit.github.io/nlp/2018/04/02/wpm/)

