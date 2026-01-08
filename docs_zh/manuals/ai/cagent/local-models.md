---
title: 使用 Docker Model Runner 运行本地模型
linkTitle: 本地模型
description: 使用 Docker Model Runner 在本地运行 AI 模型 - 无需 API 密钥
keywords: [cagent, docker model runner, dmr, local models, embeddings, offline]
weight: 20
---

Docker Model Runner 允许您在本地机器上运行 AI 模型。无需 API 密钥，无持续成本，且您的数据保持私密。

## 为何使用本地模型

Docker Model Runner 允许您在本地运行模型，无需 API 密钥或持续成本。您的数据保留在您的机器上，模型下载后您可以离线工作。这是 [云模型提供商](model-providers.md) 的一种替代方案。

## 前置要求

您需要安装并运行 Docker Model Runner：

- Docker Desktop (macOS/Windows) - 在 **设置 > AI > 启用 Docker Model Runner** 中启用 Docker Model Runner。有关详细说明，请参阅 [DMR 入门](/manuals/ai/model-runner/get-started.md#enable-docker-model-runner)。
- Docker Engine (Linux) - 使用 `sudo apt-get install docker-model-plugin` 或 `sudo dnf install docker-model-plugin` 安装。请参阅 [DMR 入门](/manuals/ai/model-runner/get-started.md#docker-engine)。

验证 Docker Model Runner 是否可用：

```console
$ docker model version
```

如果该命令返回版本信息，您就可以使用本地模型了。

## 使用 DMR 运行模型

Docker Model Runner 可以运行任何兼容的模型。模型可以来自：

- Docker Hub 仓库 (`docker.io/namespace/model-name`)
- 您自己打包并推送到任何仓库的 OCI 制品
- 直接来自 HuggingFace 的模型 (`hf.co/org/model-name`)
- Docker Desktop 中的 Docker 模型目录

要查看本地 Docker 目录中可用的模型，请运行：

```console
$ docker model list --openai
```

要使用模型，请在您的配置中引用它。如果模型尚未在本地，DMR 会在首次使用时自动拉取。

## 配置

配置您的 agent 使用 `dmr` 提供商的 Docker Model Runner：

```yaml
agents:
  root:
    model: dmr/ai/qwen3
    instruction: You are a helpful assistant
    toolsets:
      - type: filesystem
```

当您首次运行 agent 时，如果模型尚未在本地可用，cagent 会提示您拉取模型：

```console
$ cagent run agent.yaml
Model not found locally. Do you want to pull it now? ([y]es/[n]o)
```

## 工作原理

当您配置 agent 使用 DMR 时，cagent 会自动连接到您的本地 Docker Model Runner 并将推理请求路由到它。如果模型在本地不可用，cagent 会在首次使用时提示您拉取它。无需 API 密钥或身份验证。

## 高级配置

为了更好地控制模型行为，请定义模型配置：

```yaml
models:
  local-qwen:
    provider: dmr
    model: ai/qwen3:14B
    temperature: 0.7
    max_tokens: 8192

agents:
  root:
    model: local-qwen
    instruction: You are a helpful coding assistant
```

### 使用推测解码加速推理

使用较小的草稿模型通过推测解码来加速模型响应：

```yaml
models:
  fast-qwen:
    provider: dmr
    model: ai/qwen3:14B
    provider_opts:
      speculative_draft_model: ai/qwen3:0.6B-Q4_K_M
      speculative_num_tokens: 16
      speculative_acceptance_rate: 0.8
```

草稿模型生成 token 候选，主模型验证它们。这可以显著提高较长响应的吞吐量。

### 运行时标志

传递特定于引擎的标志以优化性能：

```yaml
models:
  optimized-qwen:
    provider: dmr
    model: ai/qwen3
    provider_opts:
      runtime_flags: ["--ngl=33", "--threads=8"]
```

常用标志：

- `--ngl` - GPU 层数量
- `--threads` - CPU 线程数
- `--repeat-penalty` - 重复惩罚

## 将 DMR 用于 RAG

Docker Model Runner 支持 RAG 工作流的嵌入和重排序。

### 使用 DMR 进行嵌入

使用本地嵌入来索引您的知识库：

```yaml
rag:
  codebase:
    docs: [./src]
    strategies:
      - type: chunked-embeddings
        embedding_model: dmr/ai/embeddinggemma
        database: ./code.db
```

### 使用 DMR 进行重排序

DMR 提供原生重排序以改进 RAG 结果：

```yaml
models:
  reranker:
    provider: dmr
    model: hf.co/ggml-org/qwen3-reranker-0.6b-q8_0-gguf

rag:
  docs:
    docs: [./documentation]
    strategies:
      - type: chunked-embeddings
        embedding_model: dmr/ai/embeddinggemma
        limit: 20
    results:
      reranking:
        model: reranker
        threshold: 0.5
      limit: 5
```

原生 DMR 重排序是对 RAG 结果进行重排序的最快选项。

## 故障排除

如果 cagent 找不到 Docker Model Runner：

1. 验证 Docker Model Runner 状态：

   ```console
   $ docker model status
   ```

2. 检查可用模型：

   ```console
   $ docker model list
   ```

3. 检查模型日志以查找错误：

   ```console
   $ docker model logs
   ```

4. 确保 Docker Desktop 在设置中启用了 Model Runner (macOS/Windows)

## 后续步骤

- 按照[教程](tutorial.md)使用本地模型构建您的第一个 agent
- 了解 [RAG](rag.md) 以让您的 agent 能够访问代码库和文档
- 查看[配置参考](reference/config.md#docker-model-runner-dmr)了解所有 DMR 选项