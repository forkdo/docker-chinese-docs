---
title: Docker Model Runner
linkTitle: Model Runner
params:
  sidebar:
    group: AI
weight: 30
description: 了解如何使用 Docker Model Runner 管理和运行 AI 模型。
keywords: Docker, ai, model runner, docker desktop, docker engine, llm, openai, llama.cpp, vllm, cpu, nvidia, cuda, amd, rocm, vulkan
aliases:
  - /desktop/features/model-runner/
  - /model-runner/
---

{{< summary-bar feature_name="Docker Model Runner" >}}

Docker Model Runner (DMR) 让使用 Docker 管理、运行和部署 AI 模型变得简单。Docker Model Runner 专为开发者设计，简化了从 Docker Hub 或任何符合 OCI 标准的注册中心拉取、运行和服务大型语言模型 (LLM) 及其他 AI 模型的流程。

通过与 Docker Desktop 和 Docker Engine 的无缝集成，您可以通过与 OpenAI 兼容的 API 提供模型服务，将 GGUF 文件打包为 OCI Artifacts，并通过命令行和图形界面与模型交互。

无论您是构建生成式 AI 应用、试验机器学习工作流，还是将 AI 集成到软件开发生命周期中，Docker Model Runner 都提供了一种一致、安全且高效的方式在本地使用 AI 模型。

## 主要特性

- [从 Docker Hub 拉取和推送模型](https://hub.docker.com/u/ai)
- 通过与 OpenAI 兼容的 API 提供模型服务，便于与现有应用集成
- 支持 llama.cpp 和 vLLM 推理引擎（vLLM 目前仅在 Linux x86_64/amd64 上支持 NVIDIA GPU）
- 将 GGUF 和 Safetensors 文件打包为 OCI Artifacts 并发布到任何容器注册中心
- 直接从命令行或 Docker Desktop GUI 运行和交互 AI 模型
- 管理本地模型并显示日志
- 显示提示和响应详情
- 支持对话上下文，实现多轮交互

## 系统要求

Docker Model Runner 支持以下平台：

{{< tabs >}}
{{< tab name="Windows">}}

Windows(amd64):
-  NVIDIA GPU
-  NVIDIA 驱动 576.57+

Windows(arm64):
- Adreno 的 OpenCL
- Qualcomm Adreno GPU（6xx 系列及更高版本）

  > [!NOTE]
  > 6xx 系列可能不完全支持某些 llama.cpp 功能。

{{< /tab >}}
{{< tab name="MacOS">}}

- Apple Silicon

{{< /tab >}}
{{< tab name="Linux">}}

仅限 Docker Engine：

- 支持 CPU、NVIDIA (CUDA)、AMD (ROCm) 和 Vulkan 后端
- 使用 NVIDIA GPU 时需要 NVIDIA 驱动 575.57.08+

{{< /tab >}}
{{< /tabs >}}

## Docker Model Runner 工作原理

模型在首次使用时从 Docker Hub 拉取并存储在本地。它们仅在运行时收到请求时加载到内存中，并在不使用时卸载以优化资源。由于模型可能很大，初始拉取可能需要一些时间。之后，它们会缓存在本地以便更快访问。您可以使用 [与 OpenAI 兼容的 API](api-reference.md) 与模型交互。

Docker Model Runner 同时支持 [llama.cpp](https://github.com/ggerganov/llama.cpp) 和 [vLLM](https://github.com/vllm-project/vllm) 作为推理引擎，为不同的模型格式和性能要求提供了灵活性。更多详情，请参阅 [Docker Model Runner 仓库](https://github.com/docker/model-runner)。

> [!TIP]
>
> 正在使用 Testcontainers 或 Docker Compose？
> [Testcontainers for Java](https://java.testcontainers.org/modules/docker_model_runner/)
> 和 [Go](https://golang.testcontainers.org/modules/dockermodelrunner/)，以及
> [Docker Compose](/manuals/ai/compose/models-and-compose.md) 现已支持 Docker Model Runner。

## 已知问题

### `docker model` 无法识别

如果您运行 Docker Model Runner 命令时看到：

```text
docker: 'model' is not a docker command
```

这表示 Docker 找不到该插件，因为它不在预期的 CLI 插件目录中。

要解决此问题，请创建一个符号链接，以便 Docker 能够检测到它：

```console
$ ln -s /Applications/Docker.app/Contents/Resources/cli-plugins/docker-model ~/.docker/cli-plugins/docker-model
```

链接后，重新运行该命令。

## 分享反馈

感谢您试用 Docker Model Runner。要报告错误或请求功能，请 [在 GitHub 上提交 issue](https://github.com/docker/model-runner/issues)。您也可以通过 **Enable Docker Model Runner** 设置旁边的 **Give feedback** 链接提供反馈。

## 下一步

[开始使用 DMR](get-started.md)