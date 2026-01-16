---
title: Docker Model Runner
url: /ai/model-runner/
parent:
  title: 手册
  url: /manuals/
breadcrumbs:
  - title: 手册
    url: /manuals/
  - title: Docker Model Runner
    url: /ai/model-runner/
children:
  - title: DMR 入门
    url: /ai/model-runner/get-started/
    description: 如何安装、启用并使用 Docker Model Runner 来管理和运行 AI 模型。
  - title: DMR REST API
    url: /ai/model-runner/api-reference/
    description: Docker Model Runner REST API 端点的参考文档，包括 OpenAI 和 Ollama 兼容性。
  - title: 配置选项
    url: /ai/model-runner/configuration/
    description: 在 Docker Model Runner 中配置上下文大小、运行时参数和模型行为。
  - title: DMR 示例
    url: /ai/model-runner/examples/
    description: Docker Model Runner 的示例项目和 CI/CD 工作流。
  - title: IDE 与工具集成
    url: /ai/model-runner/ide-integrations/
    description: 配置流行的 AI 编程助手和工具，将 Docker Model Runner 用作其后端。
  - title: Open WebUI 集成
    url: /ai/model-runner/openwebui-integration/
    description: 将 Open WebUI 设置为 Docker Model Runner 的类 ChatGPT 界面。
  - title: 推理引擎
    url: /ai/model-runner/inference-engines/
    description: 了解 Docker Model Runner 中的 llama.cpp 和 vLLM 推理引擎。
---




Docker Model Runner (DMR) 让使用 Docker 管理、运行和部署 AI 模型变得轻而易举。专为开发者设计，Docker Model Runner 简化了直接从 Docker Hub 或任何 OCI 兼容注册表中拉取、运行和提供大型语言模型 (LLM) 及其他 AI 模型的过程。

通过与 Docker Desktop 和 Docker Engine 无缝集成，您可以通过 OpenAI 和 Ollama 兼容 API 提供模型，将 GGUF 文件打包为 OCI 制品，并通过命令行和图形界面与模型交互。

无论您是在构建生成式 AI 应用、试验机器学习工作流，还是将 AI 集成到软件开发生命周期中，Docker Model Runner 都能为您提供一种一致、安全且高效的本地 AI 模型处理方式。

## 主要功能

- [从 Docker Hub 拉取和推送模型](https://hub.docker.com/u/ai)
- 通过 [OpenAI 和 Ollama 兼容 API](api-reference.md) 提供模型，轻松与现有应用集成
- 支持 [llama.cpp 和 vLLM 推理引擎](inference-engines.md)（vLLM 支持 Linux x86_64/amd64 和配备 NVIDIA GPU 的 Windows WSL2）
- 将 GGUF 和 Safetensors 文件打包为 OCI 制品并发布到任意容器注册表
- 直接从命令行或 Docker Desktop GUI 运行和交互 AI 模型
- [连接 AI 编码工具](ide-integrations.md)，如 Cline、Continue、Cursor 和 Aider
- [配置上下文大小和模型参数](configuration.md)以调整性能
- [设置 Open WebUI](openwebui-integration.md) 获得类似 ChatGPT 的网页界面
- 管理本地模型并显示日志
- 显示提示和响应详情
- 支持多轮交互的对话上下文

## 系统要求

Docker Model Runner 支持以下平台：

**Windows**



Windows(amd64)：
- NVIDIA GPU
- NVIDIA 驱动程序 576.57+

Windows(arm64)：
- Adreno 的 OpenCL
- 高通 Adreno GPU（6xx 系列及更高版本）

  > [!NOTE]
  > 6xx 系列可能不完全支持某些 llama.cpp 功能。

**MacOS**



- Apple Silicon

**Linux**



仅限 Docker Engine：

- 支持 CPU、NVIDIA (CUDA)、AMD (ROCm) 和 Vulkan 后端
- 使用 NVIDIA GPU 时需要 NVIDIA 驱动程序 575.57.08+



## Docker Model Runner 工作原理

模型首次使用时从 Docker Hub 拉取并本地存储。它们仅在收到请求时加载到内存中运行，不用时自动卸载以优化资源。由于模型可能较大，首次拉取可能需要一些时间。之后它们会被本地缓存以便更快访问。您可以使用 [OpenAI 和 Ollama 兼容 API](api-reference.md) 与模型交互。

### 推理引擎

Docker Model Runner 支持两种推理引擎：

| 引擎 | 适用场景 | 模型格式 |
|--------|----------|--------------|
| [llama.cpp](inference-engines.md#llamacpp) | 本地开发、资源效率 | GGUF（量化） |
| [vLLM](inference-engines.md#vllm) | 生产环境、高吞吐量 | Safetensors |

llama.cpp 是默认引擎，可在所有平台上运行。vLLM 需要 NVIDIA GPU，支持 Linux x86_64 和 Windows WSL2。详见 [推理引擎](inference-engines.md) 的详细比较和设置说明。

### 上下文大小

模型具有可配置的上下文大小（上下文长度），决定其可处理的 token 数量。默认值因模型而异，通常为 2,048-8,192 个 token。您可以按模型调整此设置：

```console
$ docker model configure --context-size 8192 ai/qwen2.5-coder
```

有关上下文大小和其他参数的详情，请参阅 [配置选项](configuration.md)。

> [!TIP]
>
> 正在使用 Testcontainers 或 Docker Compose？
> [Testcontainers for Java](https://java.testcontainers.org/modules/docker_model_runner/)
> 和 [Go](https://golang.testcontainers.org/modules/dockermodelrunner/)，以及
> [Docker Compose](/manuals/ai/compose/models-and-compose.md) 现已支持 Docker
> Model Runner。

## 已知问题

### `docker model` 无法识别

如果运行 Docker Model Runner 命令时看到：

```text
docker: 'model' is not a docker command
```

这意味着 Docker 无法找到插件，因为它不在预期的 CLI 插件目录中。

要解决此问题，请创建符号链接以便 Docker 能够检测到它：

```console
$ ln -s /Applications/Docker.app/Contents/Resources/cli-plugins/docker-model ~/.docker/cli-plugins/docker-model
```

链接完成后，重新运行命令。

## 反馈意见

感谢您试用 Docker Model Runner。要报告错误或请求功能，请 [在 GitHub 上提交 issue](https://github.com/docker/model-runner/issues)。您也可以通过 **启用 Docker Model Runner** 设置旁边的 **提供反馈** 链接提交反馈。

## 后续步骤

- [DMR 入门指南](get-started.md) - 启用 DMR 并运行您的第一个模型
- [API 参考](api-reference.md) - OpenAI 和 Ollama 兼容 API 文档
- [配置选项](configuration.md) - 上下文大小和运行时参数
- [推理引擎](inference-engines.md) - llama.cpp 和 vLLM 详情
- [IDE 集成](ide-integrations.md) - 连接 Cline、Continue、Cursor 等工具
- [Open WebUI 集成](openwebui-integration.md) - 设置网页聊天界面
---
