---
---
title: GPU support in Docker Desktop for Windows
linkTitle: GPU support
weight: 40
description: How to use GPU in Docker Desktop
toc_max: 3
aliases:
  - /desktop/gpu/
keywords: "gpu, gpu support, nvidia, wsl2, docker desktop, windows"---
title: Windows 版 Docker Desktop 中的 GPU 支持
linkTitle: GPU 支持
weight: 40
description: 如何在 Docker Desktop 中使用 GPU
toc_max: 3---
> [!NOTE]
>
> 目前，Docker Desktop 中的 GPU 支持仅在使用 WSL2 后端的 Windows 上可用。

Windows 版 Docker Desktop 支持 NVIDIA GPU 上的 NVIDIA GPU 半虚拟化 (GPU-PV)，允许容器访问 GPU 资源，用于 AI、机器学习或视频处理等计算密集型工作负载。

## 先决条件

要启用 WSL 2 GPU 半虚拟化，你需要：

- 一台配备 NVIDIA GPU 的 Windows 计算机
- 最新版本的 Windows 10 或 Windows 11 安装
- 来自 NVIDIA 的[最新驱动程序](https://developer.nvidia.com/cuda/wsl)，支持 WSL 2 GPU 半虚拟化
- 最新版本的 WSL 2 Linux 内核。在命令行中使用 `wsl --update`
- 确保在 Docker Desktop 中[已开启 WSL 2 后端](wsl/_index.md#turn-on-docker-desktop-wsl-2)

## 验证 GPU 支持

要确认 Docker 内部的 GPU 访问是否正常工作，请运行以下命令：

```console
$ docker run --rm -it --gpus=all nvcr.io/nvidia/k8s/cuda-sample:nbody nbody -gpu -benchmark
```

这会在 GPU 上运行一个 n-body 模拟基准测试。输出将类似于：

```console
Run "nbody -benchmark [-numbodies=<numBodies>]" to measure performance.
        -fullscreen       (run n-body simulation in fullscreen mode)
        -fp64             (use double precision floating point values for simulation)
        -hostmem          (stores simulation data in host memory)
        -benchmark        (run benchmark to measure performance)
        -numbodies=<N>    (number of bodies (>= 1) to run in simulation)
        -device=<d>       (where d=0,1,2.... for the CUDA device to use)
        -numdevices=<i>   (where i=(number of CUDA devices > 0) to use for simulation)
        -compare          (compares simulation results running once on the default GPU and once on the CPU)
        -cpu              (run n-body simulation on the CPU)
        -tipsy=<file.bin> (load a tipsy model file for simulation)

> NOTE: The CUDA Samples are not meant for performance measurements. Results may vary when GPU Boost is enabled.

> Windowed mode
> Simulation data stored in video memory
> Single precision floating point simulation
> 1 Devices used for simulation
MapSMtoCores for SM 7.5 is undefined.  Default to use 64 Cores/SM
GPU Device 0: "GeForce RTX 2060 with Max-Q Design" with compute capability 7.5

> Compute 7.5 CUDA device: [GeForce RTX 2060 with Max-Q Design]
30720 bodies, total time for 10 iterations: 69.280 ms
= 136.219 billion interactions per second
= 2724.379 single-precision GFLOP/s at 20 flops per interaction
```

## 运行一个真实世界的模型：使用 Docker Model Runner 运行 SmolLM2

> [!NOTE]
>
> 从 Docker Desktop 4.54 开始，适用于带有 WSL2 的 Windows 的、使用 vLLM 的 Docker Model Runner 已可用。

使用 Docker Model Runner 通过 vLLM 和 GPU 加速来运行 SmolLM2 LLM：

```console
$ docker model install-runner --backend vllm --gpu cuda
```

检查其是否已正确安装：

```console
$ docker model status
Docker Model Runner is running

Status:
llama.cpp: running llama.cpp version: c22473b
vllm: running vllm version: 0.11.0
```

运行该模型：

```console
$ docker model run ai/smollm2-vllm hi
Hello! I'm sure everything goes smoothly here. How can I assist you today?
```