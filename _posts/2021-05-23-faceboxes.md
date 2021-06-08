---
title: "FaceBoxes: A CPU Real-time Face Detector with High Accuracy"
date: 2021-05-23 08:26:28 -0400
categories: AI
---

개요
---------------
FaceBoxes는 CPU를 이용해서 실시간으로(Fast) 다양한 크기의 얼굴을 높은 정확도로(Accurate) 탐지할 수 있도록 한다. 이 논문에서 집중해야할 Contribution은 아래의 세가지이다.

- Rapidly Digested Convolutional Layers (RDCL)
- Multiple Scale Convolutional Layers (MSCL)
- Anchor densification strategy


논문 핵심 Contribution
---------------
2.1. Rapidly Digested Convolutional Layaers (RDCL)

FaceBoxes의 속도를 빠르게 하는 모델 구조로, 이 논문에서는 RDCL이라고 설명하고 있다. 모델 구조를 그림으로 살펴보면 조금 더 빠르게 이해할 수 있다.

| ![Figure 1](http://jinkilee.github.io/img/faceboxes/1.png) |
|:--:|
| *Figure 1: FaceBoxes model architecture* |

FaceBoxes의 input 이미지가 (1024x1024x3)의 크기를 가지고 있는데 RDCL에서 Convolution과 Pooling을 통해 빠르게 크기를 줄여나간다.
특히 다루는 이미지의 크기가 가장 큰 Conv1의 경우에는 stride를 비교적 크게 설정했고(=4) 이로 인해서 Conv1 연산을 빠르게 끝낼 수 있다.
Pool1과 Pool2에서 stride는 2인데 입력이 2D형태이기 때문에 크기는 4배씩 줄어들게 된다. 하나의 이미지를 FaceBoxes 모델에 forward 했을때 기대되는 각 단계별의 이미지 크기는 아래와 같다.

```
Batch 사이즈: 1(편의상)
Input 이미지: torch.Size([1, 3, 1024, 1024]) -> 3,145,728
------------------------
 
# Rapidly Digested Convolutional Layer
Conv1: torch.Size([1, 48, 256, 256]) -> 3,145,728
Pool1: torch.Size([1, 48, 128, 128]) -> 786,432
Conv2: torch.Size([1, 128, 64, 64]) -> 524,288
Pool1: torch.Size([1, 128, 32, 32]) -> 131,072
------------------------
 
# Multiple Scale Convolutional Layers
Inception1: torch.Size([1, 128, 32, 32]) -> 131,072
Inception2: torch.Size([1, 128, 32, 32]) -> 131,072
Inception3: torch.Size([1, 128, 32, 32]) -> 131,072
Conv3_1: torch.Size([1, 128, 32, 32]) -> 131,072
Conv3_2: torch.Size([1, 256, 16, 16]) -> 65,536
Conv4_1: torch.Size([1, 128, 16, 16]) -> 32,768
Conv4_2: torch.Size([1, 256, 8, 8]) -> 16,384
```

RDCL에서  약 310만 정도의 크기에서 13만 정도로 줄어들었다.  그리고 MSCL에서도 같은 원리로 1만6천으로 줄어들었다. MSCL에서는 이미 작은 사이즈의 크기를 다루기 때문에 효과가 RDCL만큼 크지 않다.


2.2. Multiple Scale Convolutional Layers (MSCL)
input 이미지가 RDCL에서 너무 급격하게 줄어버리고 또 MSCL에서도 크기가 약 1/10로 줄어들게 되면 다양한 크기의 얼굴들을 다루기에는 피쳐가 좀 부족해진다.

부족해진 피처를 강화시켜주기 위해 FaceBoxes에서는 두 가지 기법을 사용했다.

- Multi-scale design along the dimension of network <b>depth</b>
- Multi-scale design along the dimension of network <b>width</b>

depth를 이용한 해결책으로는 FaceBoxes의 모델 구조에서 MSCL의 Inception3, Conv3_2, Conv4_2에서 피처를 추출하는 것이다. 깊이 별로 서로 다르게 추출해서 피처를 강화시키는 것이다.

width를 이용한 해결책으로는 Inception 모듈을 사용하는 것이다. Inception 모듈의 내부적인 구조를 살펴보면 왜 width를 이용한 해결책인지 이해할 수 있다.

| ![Figure 2](http://jinkilee.github.io/img/faceboxes/2.png) |
|:--:|
| *Figure 2: MSCL architecture* |

Inception 모듈의 구조를 보면 Base를 4가지의 서로 다른 크기로 Conv를 수행해서 마지막에 모두 Concat하는 구조를 가지고 있다. 


2.3. Anchor densification strategy
FaceBoxes는 Anchor를 사용하는 모델이다. FaceBoxes에서는 무려 21,824개의 Anchor를 사용한다.
왜 이렇게 많이 사용하게 되는지를 설명하면 Anchor densification strategy를 이해할 수 있다. 우선 Anchor를 1024x1024 크기에 플랏팅해보자.

| ![Figure 3](http://jinkilee.github.io/img/faceboxes/3.png) |
|:--:|
| *Figure 3: Plotting anchors* |

왼쪽 그림은 전체 21824개의 Anchor 중 1%만 그린 것이고 오른쪽 그림은 모두 다 그린 것이다. 1% 그림에서 보면 알겠지만 Anchor 사이즈가 다양하다.
Anchor들을 모두 상하좌우로 타일링하는데 타일링하는 인터벌에 따라서 Anchor의 density(밀도)가 정해진다. 논문에서는 density 구하는 공식으로 아래의 식을 사용했다.
실제 Anchor의 크기와 인터벌에 따라서 density가 어떻게 변하는지 보자.

```
# 논문에서 소개한 밀도 구하는 공식
밀도 = 크기 / 인터벌
 
# 실제 논문에서 사용되는 Anchor 밀도
크기 = [32,64,128,256,512]
인터벌 = [32,32,32,64,128]
밀도 = [1,2,4,4,4]
```

크기가 작은 Anchor의 밀도가 큰 Anchor의 밀도보다 작다. 이렇게 되면 Anchor의 밀도 차이 때문에 문제가 생긴다고 논문에서 말하고 있다.
그래서 아래의 그림과 같이 크기가 작은 Anchor일 수록 더 많이 타일링 해줘서 밀도의 균형을 맞춰준다고 한다.

| ![Figure 4](http://jinkilee.github.io/img/faceboxes/4.png) |
|:--:|
| *Figure 4: Anchor densification strategy* |

크기에 따른 Anchor의 타일링 횟수를 고려할 때와 하지 않을 때의 Anchor 개수를 비교해보자.

| Anchor 크기 | Without Anchor Strategy <br> (총 3392개 Anchor 사용) | With Anchor Strategy <br> (총 21824개 Anchor 사용)  |
| ----------------- |:------------:|:----------:|
| 32 | 1024 | 16384 |
| 64 | 1024 | 4096 |
| 128 |1024 | 1024 |
| 256 | 256 | 256 |
| 512 | 64 | 64 |


크기가 32인 Anchor의 경우 논문에서 소개한 Anchor Strategy를 사용할 경우 개수가 16배 증가한다. Anchor 크기가 64인 경우는 4배 증가한다.
이와 같이 작은 사이즈의 Anchor에 대해서는 더 많은 Anchor를 추가함으로서 전체적으로 Anchor 밀도를 맞춰주는 전략을 취하고 있다.

