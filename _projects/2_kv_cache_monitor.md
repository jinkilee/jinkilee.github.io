---
layout: page
title: KV Cache Monitor
description: Real-time per-GPU dashboard for vLLM serving that breaks GPU memory into model weights, KV cache and everything else.
importance: 2
category: work
thumb_text: "KV Cache"
thumb_gradient: "#1d4ed8, #06b6d4"
tags: [vLLM, Prometheus, NVML, Docker]
github: https://github.com/jinkilee/kvmon
---

**Live GPU memory and KV cache monitoring for vLLM** · [GitHub](https://github.com/jinkilee/kvmon)

{% include figure.liquid loading="eager" path="assets/img/projects/kvmon_dashboard.png" class="img-fluid rounded z-depth-1" alt="kvmon dashboard" %}

kvmon is a dashboard that runs next to a vLLM server and shows, for every GPU it detects, how memory is actually being spent while the model serves traffic.

- **Memory breakdown**: model weights / KV cache (in use · reserved but unused) / other / free
- **Requests**: arrivals per second, completions per second, running and waiting requests
- **GPU utilization**, memory read/write activity, and PCIe RX/TX throughput
- Refreshes every 2 seconds with a 5 min / 15 min / 1 h time range; GPUs that vLLM is not using are marked as such

**Architecture.** Three containers in Docker Compose: a `serving` container with the vLLM OpenAI server and a custom GPU exporter, Prometheus scraping both `/metrics` endpoints every 2 seconds, and an nginx frontend serving a dependency-free HTML/JS dashboard that proxies `/api/*` to Prometheus. A `bench.sh` script runs `vllm bench serve` inside the container, so the KV cache and request curves can be watched filling up under load.

**How the numbers are derived.** The exporter reads the vLLM log, NVML and vLLM's own `/metrics` once per second.

| Dashboard item | Source |
|---|---|
| Model weights | vLLM log `Model loading took X GiB` (per rank) |
| KV cache reserved | vLLM log `Available KV cache memory: X GiB` (per rank) |
| KV cache in use | reserved × `vllm:kv_cache_usage_perc` |
| Other memory | NVML used − model − KV reserved |
| GPU utilization / memory R/W / PCIe | NVML |

vLLM has no counter that increments when a request *arrives* — its request counters are recorded on completion. So the exporter publishes `completed (all reasons) + running + waiting` as a cumulative counter, and its rate gives the arrival rate. GPUs are matched to ranks by setting `CUDA_DEVICE_ORDER=PCI_BUS_ID` so NVML and CUDA agree on numbering, with vLLM assumed to take the first `TP × PP` GPUs.
