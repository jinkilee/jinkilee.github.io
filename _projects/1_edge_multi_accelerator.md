---
layout: page
title: Edge Multi-Accelerator Inference
description: Real-time safety monitoring on GPU + NPU, with over 50% lower hardware cost.
importance: 1
category: work
thumb_text: "GPU ⇄ NPU"
thumb_gradient: "#b509ac, #6a5acd"
tags: [TensorRT, NPU, DALI, CUDA]
---

**GPU/NPU runtime optimization**

I developed a real-time safety monitoring inference system that runs under tight latency budgets and hardware limits. It is built on asynchronous inference pipelines designed for heterogeneous GPU and NPU execution, so the same system can be deployed flexibly across edge environments.

- TensorRT asynchronous execution and kernel fusion
- GPU-resident postprocessing through custom TensorRT plugins
- Mixed CPU/GPU preprocessing with NVIDIA DALI to cut data transfer and synchronization overhead
- NPU inference integrated by modifying ONNX graphs to fit accelerator-specific constraints

The result is stable real-time inference, much lower latency, and **more than 50% savings** in hardware infrastructure cost.
