---
layout: page
title: Real-Time VLM Video Monitoring
description: Prompt-driven detection over up to four live camera streams with a vision-language model on an 8 GB GPU.
importance: 1
category: work
thumb_text: "Prompt → Boxes"
thumb_gradient: "#b509ac, #6a5acd"
tags: [VLM, vLLM, FastAPI, React]
github: https://github.com/jinkilee/realtime-vlm
---

**Free-text video monitoring with a vision-language model** · [GitHub](https://github.com/jinkilee/realtime-vlm)

{% include figure.liquid loading="eager" path="assets/img/projects/realtime_vlm_ui.png" class="img-fluid rounded z-depth-1" alt="realtime-vlm UI" %}

realtime-vlm watches up to four RTSP cameras or MP4 videos at once. Instead of a fixed set of classes, you describe what to look for in plain text (for example `a person falling`), and the system shows where it is with bounding boxes in real time and keeps an event log with snapshots.

- Qwen3-VL-4B-Instruct-FP8 served by vLLM, running on a single RTX 4060 8GB
- FastAPI backend for stream decoding, frame sampling and event storage; React web UI with a 2×2 grid and event panel, updated over WebSocket
- Fully containerized with Docker Compose (serving, backend, frontend)

**Two-stage inference.** A judge step sends four frames from the last two seconds and reads the probability of "yes" from the logprobs as a detection score. Only when the score passes the threshold does a grounding step ask for boxes on the latest frame. The alert reaches the UI about 0.2 s after the frame, and the boxes follow about a second later.

| Model | Strategy | Precision | Recall | F1 | False positives |
|---|---|---|---|---|---|
| 2B | multi-image (4 frames → boxes in one call) | 0.28 | 0.31 | 0.29 | 21 |
| 2B | two-stage, 4 frames | 0.60 | 0.96 | 0.74 | 17 |
| 4B-FP8 | two-stage, 1 frame | 0.92 | 0.85 | 0.88 | 2 |
| **4B-FP8** | **two-stage, 4 frames** | **1.00** | **0.85** | **0.92** | **0** |

On the fall-detection samples, splitting judging from grounding raised F1 from 0.29 to 0.92 with no false positives. With four concurrent streams, judge latency stays around 200–300 ms, and detections with boxes arrive in about 1.7 s at p90.
