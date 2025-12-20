# 使用 Docker Model Runner 运行本地模型

Docker Model Runner 允许您在本地机器上运行 AI 模型。无需 API 密钥，无持续费用，您的数据将保持私密。

## 为何使用本地模型

Docker Model Runner 允许您在本地运行模型，无需 API 密钥或持续费用。您的数据保留在本地机器上，模型下载后即可离线工作。这是[云模型提供商](model-providers.md)的替代方案。

## 前提条件

您需要安装并运行 Docker Model Runner：

- Docker Desktop (macOS/Windows) - 在 **设置 > AI > 启用 Docker Model Runner** 中启用 Docker Model Runner。详细操作请参见[DMR 入门指南](/manuals/ai/model-runner/get-started.md#enable-docker-model-runner)。
- Docker Engine (Linux) - 使用 `sudo apt-get install docker-model-plugin` 或 `sudo dnf install docker-model-plugin` 安装。请参见[DMR 入门指南](/manuals/ai/model-runner/get-started.md#docker-engine)。

验证 Docker Model Runner 是否可用：

```console
$ docker model version
```

如果命令返回版本信息，则您已准备好使用本地模型。

## 使用 DMR 运行模型

Docker Model Runner 可以运行任何兼容的模型。模型来源包括：

- Docker Hub 仓库 (`docker.io/namespace/model-name`)
- 您自己的 OCI 制品（打包并推送到任意注册表）
- HuggingFace 模型（直接引用 `hf.co/org/model-name`）
- Docker Desktop 中的 Docker Model 目录

要查看 Docker 目录中可用的模型，请运行：

```console
$ docker model list --available
```

要使用模型，请在配置中引用它。如果模型尚未在本地，DMR 会在首次使用时自动拉取。

## 配置

使用 `dmr` 提供商配置您的代理以使用 Docker Model Runner：

```yaml
agents:
  root:
    model: dmr/ai/qwen3
    instruction: 你是一个有帮助的助手
    toolsets:
      - type: filesystem
```

首次运行代理时，如果模型尚未在本地，cagent 会提示您拉取模型：

```console
$ cagent run agent.yaml
本地未找到模型。是否要现在拉取？([y]es/[n]o)
```

## 工作原理

当您配置代理使用 DMR 时，cagent 会自动连接到本地 Docker Model Runner 并将推理请求路由到它。如果模型尚未在本地，cagent 会在首次使用时提示您拉取模型。无需 API 密钥或身份验证。

## 高级配置

如需更精细地控制模型行为，请定义模型配置：

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
    instruction: 你是一个有帮助的编程助手
```

### 使用推测解码加速推理

使用较小的草稿模型通过推测解码加速模型响应：

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

传递引擎特定标志以优化性能：

```yaml
models:
  optimized-qwen:
    provider: dmr
    model: ai/qwen3
    provider_opts:
      runtime_flags: ["--ngl=33", "--threads=8"]
```

常用标志：

- `--ngl` - GPU 层数
- `--threads` - CPU 线程数
- `--repeat-penalty` - 重复惩罚

## 使用 DMR 进行 RAG

Docker Model Runner 支持嵌入和重排序，适用于 RAG 工作流。

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

DMR 提供原生重排序功能，以改善 RAG 结果：

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

原生 DMR 重排序是重排序 RAG 结果的最快选项。

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

3. 检查模型日志中的错误：

   ```console
   $ docker model logs
   ```

4. 确保 Docker Desktop 在设置中启用了 Model Runner (macOS/Windows)

## 下一步

- 按照[教程](tutorial.md)使用本地模型构建您的第一个代理
- 了解 [RAG](rag.md) 以让您的代理访问代码库和文档
- 参见[配置参考](reference/config.md#docker-model-runner-dmr)了解所有 DMR 选项
