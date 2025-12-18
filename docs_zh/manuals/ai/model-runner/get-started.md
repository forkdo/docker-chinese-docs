---
title: DMR 快速入门
description: 如何安装、启用和使用 Docker Model Runner 来管理和运行 AI 模型。
weight: 10
keywords: Docker, ai, model runner, setup, installation, getting started
---

Docker Model Runner (DMR) 让您能够使用 Docker 在本地运行和管理 AI 模型。本文档将向您展示如何启用 DMR、拉取和运行模型、配置模型设置，以及发布自定义模型。

## 启用 Docker Model Runner

您可以通过 Docker Desktop 或 Docker Engine 启用 DMR。请根据您的设置选择下方相应的说明。

### Docker Desktop

1. 在设置视图中，转到 **AI** 选项卡。
1. 选中 **Enable Docker Model Runner** 设置。
1. 如果您在 Windows 上使用支持的 NVIDIA GPU，您还会看到并可以选中 **Enable GPU-backed inference**。
1. 可选：要启用 TCP 支持，请选中 **Enable host-side TCP support**。
   1. 在 **Port** 字段中，输入您要使用的端口。
   1. 如果您从本地前端 Web 应用与 Model Runner 交互，请在 **CORS Allows Origins** 中选择 Model Runner 应该接受请求的来源。来源是您的 Web 应用运行的 URL，例如 `http://localhost:3131`。

现在，您可以在 CLI 中使用 `docker model` 命令，并在 Docker Desktop 仪表板的 **Models** 选项卡中查看和与您的本地模型交互。

> [!IMPORTANT]
>
> 对于 Docker Desktop 4.45 及更早版本，此设置位于 **Beta features** 选项卡下。

### Docker Engine

1. 确保您已安装 [Docker Engine](/engine/install/)。
1. Docker Model Runner 作为一个软件包提供。要安装它，请运行：

   {{< tabs >}}
   {{< tab name="Ubuntu/Debian">}}

   ```bash
   $ sudo apt-get update
   $ sudo apt-get install docker-model-plugin
   ```

   {{< /tab >}}
   {{< tab name="RPM-base distributions">}}

   ```bash
   $ sudo dnf update
   $ sudo dnf install docker-model-plugin
   ```

   {{< /tab >}}
   {{< /tabs >}}

1. 测试安装：

   ```bash
   $ docker model version
   $ docker model run ai/smollm2
   ```

> [!NOTE]
> Docker Engine 默认启用 TCP 支持，端口为 `12434`。

### 更新 Docker Engine 中的 DMR

要更新 Docker Engine 中的 Docker Model Runner，请使用
[`docker model uninstall-runner`](/reference/cli/docker/model/uninstall-runner/)
卸载它，然后重新安装：

```bash
docker model uninstall-runner --images && docker model install-runner
```

> [!NOTE]
> 使用上述命令，本地模型将被保留。
> 要在升级期间删除模型，请在 `uninstall-runner` 命令中添加 `--models` 选项。

## 拉取模型

模型会被缓存在本地。

> [!NOTE]
>
> 当您使用 Docker CLI 时，您也可以直接从
> [HuggingFace](https://huggingface.co/) 拉取模型。

{{< tabs group="release" >}}
{{< tab name="From Docker Desktop">}}

1. 选择 **Models**，然后选择 **Docker Hub** 选项卡。
1. 找到您想要的模型，然后选择 **Pull**。

![Screenshot showing the Docker Hub view.](./images/dmr-catalog.png)

{{< /tab >}}
{{< tab name="From the Docker CLI">}}

使用 [`docker model pull` 命令](/reference/cli/docker/model/pull/)。
例如：

```bash {title="Pulling from Docker Hub"}
docker model pull ai/smollm2:360M-Q4_K_M
```

```bash {title="Pulling from HuggingFace"}
docker model pull hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF
```

{{< /tab >}}
{{< /tabs >}}

## 运行模型

{{< tabs group="release" >}}
{{< tab name="From Docker Desktop">}}

1. 选择 **Models**，然后选择 **Local** 选项卡。
1. 选择播放按钮。交互式聊天界面将打开。

![Screenshot showing the Local view.](./images/dmr-run.png)

{{< /tab >}}
{{< tab name="From the Docker CLI" >}}

使用 [`docker model run` 命令](/reference/cli/docker/model/run/)。

{{< /tab >}}
{{< /tabs >}}

## 配置模型

您可以使用 Docker Compose 配置模型，例如其最大 token 限制等。
请参阅 [Models and Compose - Model configuration options](../compose/models-and-compose.md#model-configuration-options)。

## 发布模型

> [!NOTE]
>
> 这适用于任何支持 OCI Artifacts 的容器注册表，不仅仅是 Docker Hub。

您可以为现有模型打上新名称的标签，并在不同的命名空间和仓库下发布它们：

```bash
# Tag a pulled model under a new name
$ docker model tag ai/smollm2 myorg/smollm2

# Push it to Docker Hub
$ docker model push myorg/smollm2
```

更多详细信息，请参阅 [`docker model tag`](/reference/cli/docker/model/tag)
和 [`docker model push`](/reference/cli/docker/model/push) 命令文档。

您还可以将 GGUF 格式的模型文件打包为 OCI Artifact 并发布到 Docker Hub。

```bash
# Download a model file in GGUF format, for example from HuggingFace
$ curl -L -o model.gguf https://huggingface.co/TheBloke/Mistral-7B-v0.1-GGUF/resolve/main/mistral-7b-v0.1.Q4_K_M.gguf

# Package it as OCI Artifact and push it to Docker Hub
$ docker model package --gguf "$(pwd)/model.gguf" --push myorg/mistral-7b-v0.1:Q4_K_M
```

更多详细信息，请参阅
[`docker model package`](/reference/cli/docker/model/package/) 命令文档。

## 故障排除

### 显示日志

要排除问题，请显示日志：

{{< tabs group="release" >}}
{{< tab name="From Docker Desktop">}}

选择 **Models**，然后选择 **Logs** 选项卡。

![Screenshot showing the Models view.](./images/dmr-logs.png)

{{< /tab >}}
{{< tab name="From the Docker CLI">}}

使用 [`docker model logs` 命令](/reference/cli/docker/model/logs/)。

{{< /tab >}}
{{< /tabs >}}

### 检查请求和响应

检查请求和响应有助于诊断模型相关问题。例如，您可以评估上下文使用情况以确认您保持在模型的上下文窗口内，或者显示请求的完整内容以控制在使用框架开发时传递给模型的参数。

在 Docker Desktop 中，要检查每个模型的请求和响应：

1. 选择 **Models**，然后选择 **Requests** 选项卡。此视图显示所有发送到所有模型的请求：
   - 请求发送的时间。
   - 模型名称和版本
   - 提示/请求
   - 上下文使用情况
   - 生成响应所花费的时间。
1. 选择其中一个请求以显示更多详细信息：
   - 在 **Overview** 选项卡中，查看 token 使用情况、响应元数据和生成速度，以及实际的提示和响应。
   - 在 **Request** 和 **Response** 选项卡中，查看请求和响应的完整 JSON 负载。

> [!NOTE]
> 您也可以在选择特定模型后，选择 **Requests** 选项卡来显示该模型的请求。

## 相关页面

- [以编程方式与您的模型交互](./api-reference.md)
- [Models and Compose](../compose/models-and-compose.md)
- [Docker Model Runner CLI 参考文档](/reference/cli/docker/model)