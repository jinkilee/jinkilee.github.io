---
layout: page
title: High-Throughput Vision Pipeline
description: GPU-resident data path and C++ hot paths for better throughput and P99 latency.
importance: 2
category: work
thumb_text: "P99 ↓"
thumb_gradient: "#0f766e, #22c55e"
tags: [CUDA, C++, Nsight]
---

**GPU optimization with graph-level kernel fusion**

This vision inference pipeline was held back by CPU-bound preprocessing and postprocessing. I re-architected it so data stays on the GPU across preprocessing, inference and postprocessing, which removed host-device transfers and synchronization overhead.

- Performance-critical components rewritten in C++ and integrated into the Python inference workflow
- Unneeded CPU–GPU synchronization points removed
- Profiled with Nsight Systems / Nsight Compute

The system gained a clear throughput improvement and more stable P99 latency in real-time inference.
