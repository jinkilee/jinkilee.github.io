---
title: "BERT training detail"
date: 2020-06-18 08:26:28 -0400
categories: AI
---

이전의 글에서([**BERT Structure(https://github.com/jinkilee/jinkilee.github.io/blob/master/_posts/2020-05-24-bert.md)**]) BERT의 Input에 대해서 Output이 어떻게 나오게 되는지를 살펴봤다. 이번에는 BERT를 학습하는 방법에 대해서 알아보고자 한다.

BERT Pre-training
------------------------
BERT가 pre-train될 때 내부적으로 두 개의 classifier를 만들어서 그 두 classifier의 loss를 줄여서 total_loss를 줄여가는 방식으로 학습한다. 그 두 classifier는 아래와 같다.
- Masked Language Model (MLM, 빈 칸 채우기 문제)
- Next Sentence Prediction (NSP, 한 문장과 그 다음에 오는 문장이 서로 연결된 문장인지 맞추는 문제)

위의 두 문제는 모두 classifier이기 때문에 레이블링이 필요하다. 그런데 일일이 한땀 한땀 레이블링하지 않아도 된다. BERT의 pre-train과정은 `self-supervised learning`이기 때문에 레이블링을 단순한 규칙으로 해결할 수 있다.

Next Sentence Prediction, NSP
-------------------
우선 NSP 문제를 보자. 한 문장과 그 다음에 오는 문장이 서로 연결된 문장인지 맞춘다는 뜻은, 문장이 두 개 필요하다는 뜻이다. 즉 BERT의 pre-train 데이터는 두 문장으로 이루어져 있어야 한다는 뜻이다. 앞문장을 `sent_a`, 뒷문장을 `sent_b`라고 한다. BERT pre-train 의 NSP 과정에 데이터가 어떻게 쓰이는지  알아보자. 아래의 예시를 보자.
```
# 네이버 뉴스 일부 
정경심 동양대 교수 속행 공판에서 사모펀드 코링크프라이빗에쿼티(코링크PE) 이상훈 대표가 증인으로 출석해 인사청문회 과정에서 자료를 은닉·위조한 과정을 증언했다.
18일 서울중앙지법 형사합의25-2부(임정엽 권성수 김선희 부장판사)는 정 교수의 속행 공판을 열고 이 대표에 대한 증인신문을 진행했다.

# 선녀와 나무꾼 동화책
무슨 일이 있나요?
무엇 때문에 그리 슬픈 표정을 짓고 계신가요?
난 이곳 사람이 아니란다.
하늘에서 내려온 선녀야.
이곳 물이 맑아서 목욕하러 내려왔다가 그만 나무꾼이 날개옷을 감춰 버리는 바람에 그와 같이 살고 있단다.
```

위 데이터에서 랜덤으로 두 문장씩 뽑는 걸 다섯번 정도 해보자.
```python
# 데이터_1
sent_a = '18일 서울중앙지법 형사합의25-2부(임정엽 권성수 김선희 부장판사)는 정 교수의 속행 공판을 열고 이 대표에 대한 증인신문을 진행했다.'
sent_b = '무슨 일이 있나요?'
nsp_label = 0

# 데이터_2
sent_a = '정경심 동양대 교수 속행 공판에서 사모펀드 코링크프라이빗에쿼티(코링크PE) 이상훈 대표가 증인으로 출석해 인사청문회 과정에서 자료를 은닉·위조한 과정을 증언했다.'
sent_b = '18일 서울중앙지법 형사합의25-2부(임정엽 권성수 김선희 부장판사)는 정 교수의 속행 공판을 열고 이 대표에 대한 증인신문을 진행했다.'
nsp_label = 1

# 데이터_3
sent_a = '이곳 물이 맑아서 목욕하러 내려왔다가 그만 나무꾼이 날개옷을 감춰 버리는 바람에 그와 같이 살고 있단다.'
sent_b = '난 이곳 사람이 아니란다.'
nsp_label = 0

# 데이터_4
sent_a = '하늘에서 내려온 선녀야.'
sent_b = '18일 서울중앙지법 형사합의25-2부(임정엽 권성수 김선희 부장판사)는 정 교수의 속행 공판을 열고 이 대표에 대한 증인신문을 진행했다.'
nsp_label = 0

# 데이터_5
sent_a = '무엇 때문에 그리 슬픈 표정을 짓고 계신가요?'
sent_b = '난 이곳 사람이 아니란다.'
nsp_label = 1
```

위 데이터에서 `nsp_label`은 주어진 정보가 아니지만 문장의 순서에 따라 코딩으로 0 또는 1으로 레이블링 해줄 수 있다. 코딩으로 레이블링이 가능하기 때문에 `self-supervised learning`이라고 하는 것이다. 레이블이 필요하기는 하나 사람이 할 필요는 없다는 뜻이다.  그럼 NSP 문제는 위와 같이 레이블링 해서 풀면 된다. 

Masked Language Model, MLM
-----------------
그러면 MLM은 무엇인지 알아보자. `sent_a`와 `sent_b`가 위와 같이 주어졌을 때 MLM에 대한 self-labeling은 이와 같이 가능하다. `sent_a`와 `sent_b`를 각각 토큰화하고 index로 바꾼 것을 `token_a`, `token_b`라고 해보자.

```python
# 데이터_1
>>> sent_a = '18일 서울중앙지법 형사합의25-2부(임정엽 권성수 김선희 부장판사)는 정 교수의 속행 공판을 열고 이 대표에 대한 증인신문을 진행했다.'
>>> sent_b = '무슨 일이 있나요?'
>>> bos = ['[CLS]']
>>> sep = ['[SEP]']
>>> bos = tokenizer.convert_tokens_to_ids(bos)	# [101]
>>> sep = tokenizer.convert_tokens_to_ids(sep)	# [102]
>>> ids_a = tokenizer.convert_tokens_to_ids(token_a)	# [2324, 29999, 30019, 30022, ...
>>> ids_b = tokenizer.convert_tokens_to_ids(token_b)	# [1459, 30014, 29997, 30017, ...
>>> data = bos + ids_a + sep + ids_b + sep
>>> nsp_label = 0
>>> data
[101, 2324, 29999, 30019, 30022, 1461, 30008, 29999, 30014, 30022, 30000, 30014, 30025, 29999,
 30006, 30025, 30000, 30019, 29996, 30008, 30024, 1469, 30010, 30025, 29997, 30006, 30005, 30006, 30024,
 29999, 30018, 17788, 1011, 1016, 29996, 30014, 1006, 1463, 30019, 30023, 30000, 30008, 30025, 29999, 30010,
 30024, 1455, 30015, 30021, 29997, 30008, 30025, 29997, 30014, 1455, 30019, 30023, 29997, 30008, 30021,
 30005, 30018, 1460, 30014, 30000, 30006, 30025, 30004, 30006, 30021, 29997, 30006, 1007, 1456, 30017, 30021,
 1464, 30008, 30025, 1455, 30013, 29997, 30014, 29999, 30018, 1461, 30011, 30020, 30005, 30007, 30025, 1455,
 30011, 30025, 30004, 30006, 30021, 29999, 30017, 30022, 1463, 30010, 30022, 29991, 30011, 1463, 30019, 1457,
 30007, 30004, 30013, 29999, 30009, 1457, 30007, 30005, 30006, 30021, 1464, 30017, 30025, 29999, 30019, 30021,
 29997, 30019, 30021, 29995, 30014, 30021, 29999, 30017, 30022, 100, 1012, 102, 1459, 30014, 29997, 30017,
 30021, 1463, 30019, 30022, 29999, 30019, 100, 1029, 102]
```

위의 `data`에서 랜덤으로 15% 정도의 데이터를 `[MASK]`로 마스킹해보자. `[MASK]`는 tokenizer에서 103이므로
```python
>>> tokenizer.convert_tokens_to_ids(['[MASK]'])
[103]
```

랜덤으로 선택된 마스크들은 103으로 값을 바꾼다.
```python
>>> n_mask = int(len(data) * 0.15) # 22
>>> idx = np.random.randint(0, len(data), n_mask) # array([ 97, 140,  15,  15,  9 ...
>>> for i in idx:
>>>     data[i] = 103
>>> data
[101, 2324, 103, 30019, 30022, 1461, 30008, 29999, 103, 30022, 30000, 30014, 30025, 103, 103, 103, 30000,
 30019, 29996, 30008, 30024, 1469, 30010, 30025, 29997, 30006, 30005, 103, 30024, 29999, 30018, 17788, 1011,
 1016, 29996, 30014, 103, 103, 30019, 30023, 30000, 30008, 30025, 29999, 30010, 30024, 1455, 103, 30021,
 29997, 30008, 30025, 29997, 30014, 1455, 30019, 30023, 29997, 30008, 30021, 103, 30018, 1460, 30014, 103,
 30006, 30025, 30004, 30006, 30021, 29997, 30006, 1007, 1456, 30017, 30021, 1464, 30008, 30025, 1455, 30013,
 29997, 30014, 29999, 30018, 1461, 103, 30020, 30005, 30007, 30025, 103, 30011, 30025, 30004, 30006, 30021,
 103, 30017, 30022, 1463, 30010, 30022, 29991, 30011, 1463, 30019, 1457, 103, 30004, 30013, 103, 30009, 1457,
 30007, 30005, 30006, 30021, 1464, 30017, 30025, 29999, 30019, 30021, 29997, 30019, 103, 29995, 30014, 30021,
 29999, 30017, 30022, 100, 1012, 102, 1459, 30014, 29997, 30017, 103, 1463, 30019, 30022, 29999, 30019,
 103, 1029, 103]
```

위의 `data`에서 masking된 부분(103)의 정답은 순서대로 아래와 같다.
```python
mlm_label = [
	29999,
	30014,
	29999,
	30006,
	30025,
	30025,
	30006,
	1006,
	1463,
	30015,
	30005,
	30000,
	30011,
	1455,
	29999,
	30007,
	29999,
	29999,
	30021,
	30021,
	100,
	100
]
```

그런데 여기에서 중요한 것이 있다. 저 빈칸에 저 단어들만 들어갈 수 있는가? 즉, 저 빈 칸에 다른 단어는 들어가면 안되고 반드시 저 단어가 들어가야만 말이 되는 것인가? 꼭 그렇지 않다. 다른 단어를 넣어도 충분히 말이 될 수도 있다. 그래서 아래와 같은 규칙으로 빈칸을 레이블링한다.
- 전체의 80%는 `[MASK]`로 마스킹
- 전체의 10%는 원래와 다른 단어
- 전체의 10%는 원래의 단어

코딩으로 아래와 같이 구현된다.
```python
>>> import numpy as np
>>> vocab_size = 50
>>> ids = np.random.randint(0, vocab_size, (20))
>>> print(ids)
[41  7 30 30 28 38 18 18 13 46 17 13  4  1 31  5 17  7 33 32]
>>>
>>> for i in range(len(ids)):
...     p = np.random.random()  # random probability
...     print('{}th probability: {:.4f}'.format(i, p))
...     if p < 0.15:
...         p = np.random.random()
...         if p < 0.8:
...             ids[i] = 103
...             print('{}th value is changed to 103 ... {:.4f}'.format(i, p))
...         elif 0.8 <= p and p < 0.9:
...             while True:
...                 tok = np.random.randint(0, vocab_size)
...                 if tok != 103:
...                     break
...             ids[i] = tok# no 103 for rest of 10%
...             print('{}th value is changed to {} ... {:.4f}'.format(i, tok, p))
...         else:
...             print('{}th value is not changed'.format(i))
...             continue# no change
...
0th probability: 0.7826
1th probability: 0.0437
1th value is changed to 103 ... 0.0894
2th probability: 0.0126
2th value is changed to 103 ... 0.0886
3th probability: 0.5740
4th probability: 0.0645
4th value is changed to 103 ... 0.1540
5th probability: 0.0367
5th value is not changed
6th probability: 0.5883
7th probability: 0.4923
8th probability: 0.6770
9th probability: 0.3732
10th probability: 0.1152
10th value is changed to 103 ... 0.5462
11th probability: 0.0178
11th value is changed to 103 ... 0.1169
12th probability: 0.1146
12th value is changed to 103 ... 0.2098
13th probability: 0.8593
14th probability: 0.2803
15th probability: 0.2821
16th probability: 0.9048
17th probability: 0.8399
18th probability: 0.0920
18th value is changed to 47 ... 0.8118
19th probability: 0.1731
```

실제로 huggingface의 BERT를 pretrain할 때 아래와 같이 데이터가 들어가게 된다.
```python
# original input
tensor([  101,   134, 12226,  3781,  3464, 17758,  2684,   134, 14895, 21006,
         1185, 12226,  3781,  3464,   124,   131, 12118,  1874, 19248,  4902,
        17758,   113,  1983,   131,   100,   100,   100,   117,  4941,   119,
        12226,  3781,  3464,  1104,  1103,  2651,  2427,   124,   114,   117,
										...
         1115,  1169,  1129, 10297, 11812,  1194,  1105, 18723,  1174,  1112,
         1152,  1132, 14776,   119,  1109,  2438,  1106,  1296,  1642,  2450,
         1113,  1103,  4520,  9544,  5763,  1113,  1126,  2510,  1591,   112,
          188,   102])

# masked input
tensor([  101,   134, 12226,  3781,  3464, 17758,  2684,   103, 14895, 21006,
         1185, 12226,  3781,  3464,   124,   131, 12118,  1874, 19248,  4902,
        17758,   113,   103,   131,   100,   100,   100,   103,  4941,  3892,
        12226,  3781,  3464,  1104,  1103,  2651,  2427,   124,   114,   117,
										...
         1115,  1169,  1129, 10297, 11812,  1194,  1105, 18723,  1174,  1112,
         1152,  1132, 14776,   119,  1109,  2438,  1106,  1296,  1642,  2450,
         1113,  1103,  4520,  9544,   103,  1113,  1126,  2510,  1591,   103,
          188,   102])

# label for masked input
tensor([ -100,  -100,  -100,  -100,  -100,  -100,  -100,   134,  -100,  -100,
         -100,  -100,  -100,  -100,  -100,  -100,  -100,  -100,  -100,  -100,
         -100,  -100,  1983,  -100,  -100,  -100,  -100,   117,  -100,   119,
         -100,  -100,  -100,  -100,  -100,  -100,  -100,  -100,  -100,  -100,
										...
         -100,  -100,  -100,  -100,  -100,  -100,  -100,  -100,  -100,  -100,
         -100,  -100,  -100,  -100,  -100,  -100,  -100,  -100,  -100,  -100,
         -100,  -100,  -100,  -100,  5763,  -100,  -100,  -100,  -100,   112,
         -100,  -100])
```
여기에서 중요한 것이 있다. huggingface에서 pre-train된 BERT는 MLM으로만 학습돼 있다. NSP는 거의 학습 시작과 동시에 loss가 바닥으로 떨어지게 되기 때문에 일부러 학습에서 제외한 것 같다.

위와 같은 데이터로 MLM을 학습할 때 `masked input`과 `label for masked input`이 사용된다. `label for masked input`에 보면 `-100`으로 상당부분 체워져 있는데, 이 부분은 loss에 영향을 주지 않고 무시된다. 참고로 -100을 무시하는 부분에 대한 코딩은 따로 구현하지 않아도 된다. `nn.CrossEntropyLoss`에서 `ignore_index` 파라미터의 기본값이 -100이기 때문이다.
```python
# https://pytorch.org/docs/stable/nn.html
class torch.nn.CrossEntropyLoss(weight=None, size_average=None, ignore_index=-100, reduce=None, reduction='mean')
	...
	This criterion expects a class index in the range [0, C-1][0,C−1] as the target for each value of a 1D tensor of size minibatch; if ignore_index is specified, this criterion also accepts this class index (this index may not necessarily be in the class range).
	...
```

MLM VS NSP
---------------
당연히 MLM이 더 어렵다. 그래서 pre-trained 모델을 학습할 때 loss가 빈 칸 채우기와 NSP로부터 나오게 되는데, 빈 칸 채우기 문제의 loss가 훨씬 늦게 떨어진다.
이러한 이유로, NSP 문제를 조금 더 어렵게 만들려고 하는 시도가 ALBERT 등에서 나온다. 그 내용에 대해서는 다음에 다뤄보도록 하자.



