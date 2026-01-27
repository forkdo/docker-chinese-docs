---
title: 推理引擎
description: 了解 Docker Model Runner 中的 llama.cpp、vLLM 和 Diffusers 推理引擎。
weight: 50
keywords: Docker, ai, model runner, llama.cpp, vllm, diffusers, inference, gguf, safetensors, cuda, gpu, image generation, stable diffusion
---

Docker Model Runner 支持三种推理引擎：**llama.cpp**、**vLLM** 和 **Diffusers**。
每种引擎都有不同的优势、支持的平台和模型格式要求。本指南帮助您选择正确的引擎并针对您的用例进行配置。

## 引擎对比

| 特性 | llama.cpp | vLLM | Diffusers                           |
|---------|-----------|------|-------------------------------------|
| **模型格式** | GGUF | Safetensors, HuggingFace | DDUF                                |
| **平台** | 全部 (macOS, Windows, Linux) | 仅限 Linux x86_64 | Linux (x86_64, ARM64)               |
| **GPU 支持** | NVIDIA, AMD, Apple Silicon, Vulkan | 仅限 NVIDIA CUDA | 仅限 NVIDIA CUDA                    |
| **CPU 推理** | 支持 | 不支持 | 不支持                                  |
| **量化** | 内置 (Q4, Q5, Q8 等) | 有限 | 有限                             |
| **内存效率** | 高 (使用量化时) | 中等 | 中等                            |
| **吞吐量** | 良好 | 高 (使用批处理时) | 良好                                |
| **最适合** | 本地开发、资源受限环境 | 生产环境、高吞吐量 | 图像生成                    |
| **用例** | 文本生成 (LLM) | 文本生成 (LLM) | 图像生成 (Stable Diffusion) |

## llama.cpp

[llama.cpp](https://github.com/ggerganov/llama.cpp) 是 Docker Model Runner 中的默认推理引擎。它专为高效的本地推理而设计，支持广泛的硬件配置。

### 平台支持

| 平台 | GPU 支持 | 说明 |
|----------|-------------|-------|
| macOS (Apple Silicon) | Metal | 自动 GPU 加速 |
| Windows (x64) | NVIDIA CUDA | 需要 NVIDIA 驱动 576.57+ |
| Windows (ARM64) | Adreno OpenCL | 高通 6xx 系列及更新版本 |
| Linux (x64) | NVIDIA, AMD, Vulkan | 多种后端选项 |
| Linux | 仅 CPU | 可在任何 x64/ARM64 系统上运行 |

### 模型格式：GGUF

llama.cpp 使用 GGUF 格式，支持高效量化以减少内存使用，而不会显著损失质量。

#### 量化级别

| 量化 | 每权重位数 | 内存使用 | 质量 |
|--------------|-----------------|--------------|---------|
| Q2_K | ~2.5 | 最低 | 降低 |
| Q3_K_M | ~3.5 | 极小 | 可接受 |
| Q4_K_M | ~4.5 | 低 | 良好 |
| Q5_K_M | ~5.5 | 中等 | 优秀 |
| Q6_K | ~6.5 | 较高 | 优秀 |
| Q8_0 | 8 | 高 | 接近原始 |
| F16 | 16 | 最高 | 原始 |

**推荐**：Q4_K_M 在大多数用例中提供了质量与内存使用之间的最佳平衡。

#### 拉取量化模型

Docker Hub 上的模型通常在标签中包含量化信息：

```console
$ docker model pull ai/llama3.2:3B-Q4_K_M
```

### 使用 llama.cpp

llama.cpp 是默认引擎。无需特殊配置：

```console
$ docker model run ai/smollm2
```

运行模型时显式指定 llama.cpp：

```console
$ docker model run ai/smollm2 --backend llama.cpp
```

### llama.cpp API 端点

使用 llama.cpp 时，API 调用使用 llama.cpp 引擎路径：

```text
POST /engines/llama.cpp/v1/chat/completions
```

或不使用引擎前缀：

```text
POST /engines/v1/chat/completions
```

## vLLM

[vLLM](https://github.com/vllm-project/vllm) 是一个高性能推理引擎，针对具有高吞吐量要求的生产工作负载进行了优化。

### 平台支持

| 平台 | GPU | 支持状态 |
|----------|-----|----------------|
| Linux x86_64 | NVIDIA CUDA | 支持 |
| Windows with WSL2 | NVIDIA CUDA | 支持 (Docker Desktop 4.54+) |
| macOS | - | 不支持 |
| Linux ARM64 | - | 不支持 |
| AMD GPU | - | 不支持 |

> [!重要]
> vLLM 需要支持 CUDA 的 NVIDIA GPU。它不支持仅 CPU 的推理。

### 模型格式：Safetensors

vLLM 使用 Safetensors 格式的模型，这是 HuggingFace 模型的标准格式。这些模型通常比量化 GGUF 模型使用更多内存，但在强大硬件上可能提供更好的质量和更快的推理速度。

### 设置 vLLM

#### Docker Engine (Linux)

安装带有 vLLM 后端的 Model Runner：

```console
$ docker model install-runner --backend vllm --gpu cuda
```

验证安装：

```console
$ docker model status
Docker Model Runner is running

Status:
llama.cpp: running llama.cpp version: c22473b
vllm: running vllm version: 0.11.0
```

#### Docker Desktop (Windows with WSL2)

1. 确保您具备：
   - Docker Desktop 4.54 或更高版本
   - 更新了驱动的 NVIDIA GPU
   - 已启用 WSL2

2. 安装 vLLM 后端：
   ```console
   $ docker model install-runner --backend vllm --gpu cuda
   ```

### 使用 vLLM 运行模型

vLLM 模型通常在标签中包含 `-vllm` 后缀：

```console
$ docker model run ai/smollm2-vllm
```

显式指定 vLLM 后端：

```console
$ docker model run ai/model --backend vllm
```

### vLLM API 端点

使用 vLLM 时，在 API 路径中指定引擎：

```text
POST /engines/vllm/v1/chat/completions
```

### vLLM 配置

#### HuggingFace 覆盖

使用 `--hf_overrides` 传递模型配置覆盖：

```console
$ docker model configure --hf_overrides '{"max_model_len": 8192}' ai/model-vllm
```

#### 常见 vLLM 设置

| 设置 | 描述 | 示例 |
|---------|-------------|---------|
| `max_model_len` | 最大上下文长度 | 8192 |
| `gpu_memory_utilization` | 使用的 GPU 内存比例 | 0.9 |
| `tensor_parallel_size` | 用于张量并行的 GPU 数量 | 2 |

### vLLM 与 llama.cpp 性能对比

| 场景 | 推荐引擎 |
|----------|-------------------|
| 单用户、本地开发 | llama.cpp |
| 多个并发请求 | vLLM |
| GPU 内存有限 | llama.cpp (使用量化) |
| 最大吞吐量 | vLLM |
| 仅 CPU 系统 | llama.cpp |
| Apple Silicon Mac | llama.cpp |
| 生产部署 | vLLM (如果硬件支持) |

## Diffusers

[Diffusers](https://github.com/huggingface/diffusers) 是一个用于图像生成模型（包括 Stable Diffusion）的推理引擎。与专注于使用 LLM 进行文本生成的 llama.cpp 和 vLLM 不同，Diffusers 使您能够根据文本提示生成图像。

### 平台支持

| 平台 | GPU | 支持状态 |
|----------|-----|----------------|
| Linux x86_64 | NVIDIA CUDA | 支持 |
| Linux ARM64 | NVIDIA CUDA | 支持 |
| Windows | - | 不支持 |
| macOS | - | 不支持 |

> [!重要]
> Diffusers 需要支持 CUDA 的 NVIDIA GPU。它不支持仅 CPU 的推理。

### 设置 Diffusers

安装带有 Diffusers 后端的 Model Runner：

```console
$ docker model reinstall-runner --backend diffusers --gpu cuda
```

验证安装：

```console
$ docker model status
Docker Model Runner is running

Status:
llama.cpp: running llama.cpp version: 34ce48d
mlx: not installed
sglang: sglang package not installed
vllm: vLLM binary not found
diffusers: running diffusers version: 0.36.0
```

### 拉取 Diffusers 模型

拉取 Stable Diffusion 模型：

```console
$ docker model pull stable-diffusion:Q4
```

### 使用 Diffusers 生成图像

Diffusers 使用图像生成 API 端点。要生成图像：

```console
$ curl -s -X POST http://localhost:12434/engines/diffusers/v1/images/generations \
  -H "Content-Type: application/json" \
  -d '{
    "model": "stable-diffusion:Q4",
    "prompt": "A picture of a nice cat",
    "size": "512x512"
  }' | jq -r '.data[0].b64_json' | base64 -d > image.png
```

此命令：
1. 向 Diffusers 图像生成端点发送 POST 请求
2. 指定模型、提示和输出图像大小
3. 从响应中提取 base64 编码的图像
4. 解码并将其保存为 `image.png`

### Diffusers API 端点

使用 Diffusers 时，在 API 路径中指定引擎：

```text
POST /engines/diffusers/v1/images/generations
```

### 支持的参数

| 参数 | 类型 | 描述 |
|-----------|------|-------------|
| `model` | string | 必需。模型标识符（例如：`stable-diffusion:Q4`）。 |
| `prompt` | string | 必需。要生成的图像的文字描述。 |
| `size` | string | 图像尺寸，格式为 `宽度x高度`（例如：`512x512`）。 |

## 运行多个引擎

您可以同时运行 llama.cpp、vLLM 和 Diffusers。Docker Model Runner 会根据模型或显式指定的引擎选择，将请求路由到相应的引擎。

查看正在运行的引擎：

```console
$ docker model status
Docker Model Runner 正在运行

状态：
llama.cpp: 运行中 llama.cpp 版本：34ce48d
mlx: 未安装
sglang: sglang 包未安装
vllm: 运行中 vllm 版本：0.11.0
diffusers: 运行中 diffusers 版本：0.36.0
```

### 各引擎专用 API 路径

| 引擎 | API 路径 | 使用场景 |
|--------|----------|----------|
| llama.cpp | `/engines/llama.cpp/v1/chat/completions` | 文本生成 |
| vLLM | `/engines/vllm/v1/chat/completions` | 文本生成 |
| Diffusers | `/engines/diffusers/v1/images/generations` | 图像生成 |
| 自动选择 | `/engines/v1/chat/completions` | 文本生成（自动选择引擎） |

## 管理推理引擎

### 安装引擎

```console
$ docker model install-runner --backend <engine> [--gpu <type>]
```

选项：
- `--backend`：`llama.cpp`、`vllm` 或 `diffusers`
- `--gpu`：`cuda`、`rocm`、`vulkan` 或 `metal`（取决于平台）

### 重新安装引擎

```console
$ docker model reinstall-runner --backend <engine>
```

### 检查引擎状态

```console
$ docker model status
```

### 查看引擎日志

```console
$ docker model logs
```

## 为各引擎打包模型

### 打包 GGUF 模型（llama.cpp）

```console
$ docker model package --gguf ./model.gguf --push myorg/mymodel:Q4_K_M
```

### 打包 Safetensors 模型（vLLM）

```console
$ docker model package --safetensors ./model/ --push myorg/mymodel-vllm
```

## 故障排除

### vLLM 无法启动

1. 验证 NVIDIA GPU 是否可用：
   ```console
   $ nvidia-smi
   ```

2. 检查 Docker 是否有 GPU 访问权限：
   ```console
   $ docker run --rm --gpus all nvidia/cuda:12.0-base nvidia-smi
   ```

3. 确认您使用的是受支持的平台（Linux x86_64 或 Windows WSL2）。

### llama.cpp 运行缓慢

1. 确保 GPU 加速正常工作（检查日志中是否有 Metal/CUDA 相关消息）。

2. 尝试使用更激进的量化方式：
   ```console
   $ docker model pull ai/model:Q4_K_M
   ```

3. 减小上下文大小：
   ```console
   $ docker model configure --context-size 2048 ai/model
   ```

### 内存不足错误

1. 使用更小的量化方式（Q4 而非 Q8）。
2. 减小上下文大小。
3. 对于 vLLM，调整 `gpu_memory_utilization`：
   ```console
   $ docker model configure --hf_overrides '{"gpu_memory_utilization": 0.8}' ai/model
   ```

## 下一步

- [配置选项](configuration.md) - 详细参数参考
- [API 参考](api-reference.md) - API 文档
- [GPU 支持](/manuals/desktop/features/gpu.md) - Docker Desktop 的 GPU 配置