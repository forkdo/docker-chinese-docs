# Docker Model Runner




Docker Model Runner (DMR) 让您能够轻松地使用 Docker 管理、运行和部署 AI 模型。专为开发人员设计，Docker Model Runner 简化了直接从 Docker Hub、任何 OCI 兼容注册表或 [Hugging Face](https://huggingface.co/) 拉取、运行和提供大型语言模型 (LLM) 及其他 AI 模型的过程。

通过与 Docker Desktop 和 Docker Engine 无缝集成，您可以通过 OpenAI 和 Ollama 兼容 API 提供模型，将 GGUF 文件打包为 OCI 工件，并通过命令行和图形界面与模型进行交互。

无论您是在构建生成式 AI 应用程序、试验机器学习工作流，还是将 AI 集成到软件开发生命周期中，Docker Model Runner 都提供了一种一致、安全且高效的方式来在本地处理 AI 模型。

## 主要功能

- [从 Docker Hub 或任何 OCI 兼容注册表拉取和推送模型](https://hub.docker.com/u/ai)
- [从 Hugging Face 拉取模型](https://huggingface.co/)
- 通过 [OpenAI 和 Ollama 兼容 API](api-reference.md) 提供模型，轻松与现有应用程序集成
- 支持 [llama.cpp、vLLM 和 Diffusers 推理引擎](inference-engines.md)（vLLM 和 Diffusers 在配备 NVIDIA GPU 的 Linux 系统上可用）
- 使用 Diffusers 后端通过 Stable Diffusion 模型[根据文本提示生成图像](inference-engines.md#diffusers)
- 将 GGUF 和 Safetensors 文件打包为 OCI 工件并发布到任何容器注册表
- 直接通过命令行或 Docker Desktop GUI 运行和与 AI 模型交互
- [连接到 AI 编码工具](ide-integrations.md)，如 Cline、Continue、Cursor 和 Aider
- [配置上下文大小和模型参数](configuration.md)以调整性能
- [设置 Open WebUI](openwebui-integration.md) 以获得类似 ChatGPT 的 Web 界面
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



## Docker Model Runner 的工作原理

模型在您首次使用时从 Docker Hub、OCI 兼容注册表或 [Hugging Face](https://huggingface.co/) 拉取并存储在本地。它们仅在运行时收到请求时加载到内存中，并在不使用时卸载以优化资源。由于模型可能很大，初始拉取可能需要一些时间。之后，它们会被缓存在本地以便更快访问。您可以使用 [OpenAI 和 Ollama 兼容 API](api-reference.md) 与模型进行交互。

### 推理引擎

Docker Model Runner 支持三种推理引擎：

| 引擎 | 最适合 | 模型格式 |
|--------|----------|--------------|
| [llama.cpp](inference-engines.md#llamacpp) | 本地开发、资源效率 | GGUF（量化） |
| [vLLM](inference-engines.md#vllm) | 生产环境、高吞吐量 | Safetensors |
| [Diffusers](inference-engines.md#diffusers) | 图像生成（Stable Diffusion） | Safetensors |

llama.cpp 是默认引擎，可在所有平台上运行。vLLM 需要 NVIDIA GPU，支持 Linux x86_64 和 Windows with WSL2。Diffusers 支持图像生成，需要在 Linux（x86_64 或 ARM64）上使用 NVIDIA GPU。有关详细比较和设置，请参阅 [推理引擎](inference-engines.md)。

### 上下文大小

模型具有可配置的上下文大小（上下文长度），用于确定它们可以处理的 token 数量。默认值因模型而异，但通常为 2,048-8,192 个 token。您可以按模型调整此设置：

```console
$ docker model configure --context-size 8192 ai/qwen2.5-coder
```

有关上下文大小和其他参数的详细信息，请参阅 [配置选项](configuration.md)。

> [!TIP]
>
> 正在使用 Testcontainers 或 Docker Compose？
> [Testcontainers for Java](https://java.testcontainers.org/modules/docker_model_runner/)
> 和 [Go](https://golang.testcontainers.org/modules/dockermodelrunner/)，以及
> [Docker Compose](/manuals/ai/compose/models-and-compose.md) 均支持 Docker
> Model Runner。

## 安全与隔离

### 执行环境

Docker Model Runner 将推理引擎与你的主机隔离开来：

- 在 Linux 上，Docker Model Runner 及其推理引擎（例如 Diffusers）在容器内运行，容器提供了隔离边界。
- 在 macOS 和 Windows 上，这些引擎不在容器内运行，因此 Docker Model Runner 会在沙箱环境中运行它们（分别为 seatbelt/sandbox-exec 和 Job Objects）。

### 网络

Model Runner API 不进行身份验证。任何能够访问它的客户端（包括同一 Docker 网络上的其他容器）都可以拉取、加载和运行模型，并发送推理请求。

## 已知问题

### `docker model` 未被识别

如果您运行 Docker Model Runner 命令时看到：

```text
docker: 'model' is not a docker command
```

这意味着 Docker 无法找到插件，因为它不在预期的 CLI 插件目录中。

要解决此问题，请创建符号链接以便 Docker 能够检测到它：

```console
$ ln -s /Applications/Docker.app/Contents/Resources/cli-plugins/docker-model ~/.docker/cli-plugins/docker-model
```

链接完成后，重新运行命令。

## 隐私和数据收集

Docker Model Runner 尊重您在 Docker Desktop 中的隐私设置。数据收集由**发送使用情况统计信息**设置控制：

- **已禁用**：不收集任何使用数据
- **已启用**：仅收集最小量的非个人数据：
  - [模型名称](https://github.com/docker/model-runner/blob/eb76b5defb1a598396f99001a500a30bbbb48f01/pkg/metrics/metrics.go#L96)（通过向 Docker Hub 发送 HEAD 请求）
  - 用户代理信息
  - 请求是来自主机还是容器

在使用 Docker Engine 运行 Docker Model Runner 时，无论任何设置如何，都会向 Docker Hub 发送 HEAD 请求以跟踪模型名称。

绝不会收集任何提示内容、响应或个人身份信息。

## 分享反馈

感谢您试用 Docker Model Runner。要报告错误或请求功能，请在 [GitHub 上创建问题](https://github.com/docker/model-runner/issues)。您也可以通过**启用 Docker Model Runner**设置旁边的**提供反馈**链接提交反馈。

## 后续步骤

- [开始使用 DMR](get-started.md) - 启用 DMR 并运行您的第一个模型
- [API 参考](api-reference.md) - OpenAI 和 Ollama 兼容 API 文档
- [配置选项](configuration.md) - 上下文大小和运行时参数
- [推理引擎](inference-engines.md) - llama.cpp、vLLM 和 Diffusers 详情
- [IDE 集成](ide-integrations.md) - 连接 Cline、Continue、Cursor 等工具
- [Open WebUI 集成](openwebui-integration.md) - 设置 Web 聊天界面

