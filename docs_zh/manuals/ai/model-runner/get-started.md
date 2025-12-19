---
title: DMR 入门指南
description: 如何安装、启用和使用 Docker Model Runner 来管理和运行 AI 模型。
weight: 10
keywords: Docker, ai, model runner, setup, installation, getting started
---

Docker Model Runner (DMR) 让您能够使用 Docker 在本地运行和管理 AI 模型。本文将向您展示如何启用 DMR、拉取和运行模型、配置模型设置以及发布自定义模型。

## 启用 Docker Model Runner

您可以使用 Docker Desktop 或 Docker Engine 启用 DMR。请根据您的设置按照以下说明操作。

### Docker Desktop

1. 在设置视图中，转到 **AI** 选项卡。
1. 选择 **启用 Docker Model Runner** 设置。
1. 如果您使用的是支持 NVIDIA GPU 的 Windows 系统，您还会看到并可以选择
   **启用 GPU 支持的推理**。
1. 可选：要启用 TCP 支持，请选择 **启用主机端 TCP 支持**。
   1. 在 **端口** 字段中，输入您要使用的端口。
   1. 如果您通过本地前端 Web 应用与 Model Runner 交互，请在
      **CORS 允许的来源** 中选择 Model Runner 应接受请求的来源。来源是指您的 Web 应用运行的 URL，例如 `http://localhost:3131`。

现在，您可以在 CLI 中使用 `docker model` 命令，并在 Docker Desktop 仪表板的 **模型** 选项卡中查看和与您的本地模型交互。

> [!重要]
>
> 对于 Docker Desktop 4.45 及更早版本，此设置位于
> **Beta 功能** 选项卡下。

### Docker Engine

1. 确保您已安装 [Docker Engine](/engine/install/)。
1. Docker Model Runner 以软件包的形式提供。要安装它，请运行：

   {{< tabs >}}
   {{< tab name="Ubuntu/Debian">}}

   ```bash
   $ sudo apt-get update
   $ sudo apt-get install docker-model-plugin
   ```

   {{< /tab >}}
   {{< tab name="基于 RPM 的发行版">}}

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

> [!注意]
> 对于 Docker Engine，TCP 支持默认在端口 `12434` 上启用。

### 在 Docker Engine 中更新 DMR

要在 Docker Engine 中更新 Docker Model Runner，请先使用
[`docker model uninstall-runner`](/reference/cli/docker/model/uninstall-runner/)
卸载它，然后重新安装：

```bash
docker model uninstall-runner --images && docker model install-runner
```

> [!注意]
> 使用上述命令时，本地模型会被保留。
> 要在升级期间删除模型，请在 `uninstall-runner` 命令中添加 `--models` 选项。

## 拉取模型

模型会被缓存在本地。

> [!注意]
>
> 当您使用 Docker CLI 时，也可以直接从
> [HuggingFace](https://huggingface.co/) 拉取模型。

{{< tabs group="release" >}}
{{< tab name="从 Docker Desktop">}}

1. 选择 **模型**，然后选择 **Docker Hub** 选项卡。
1. 找到您想要的模型，然后选择 **拉取**。

![显示 Docker Hub 视图的屏幕截图。](./images/dmr-catalog.png)

{{< /tab >}}
{{< tab name="从 Docker CLI">}}

使用 [`docker model pull` 命令](/reference/cli/docker/model/pull/)。
例如：

```bash {title="从 Docker Hub 拉取"}
docker model pull ai/smollm2:360M-Q4_K_M
```

```bash {title="从 HuggingFace 拉取"}
docker model pull hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF
```

{{< /tab >}}
{{< /tabs >}}

## 运行模型

{{< tabs group="release" >}}
{{< tab name="从 Docker Desktop">}}

1. 选择 **模型**，然后选择 **本地** 选项卡。
1. 选择播放按钮。交互式聊天屏幕将打开。

![显示本地视图的屏幕截图。](./images/dmr-run.png)

{{< /tab >}}
{{< tab name="从 Docker CLI">}}

使用 [`docker model run` 命令](/reference/cli/docker/model/run/)。

{{< /tab >}}
{{< /tabs >}}

## 配置模型

您可以使用 Docker Compose 配置模型，例如其最大 token 限制等。
请参阅 [模型与 Compose - 模型配置选项](../compose/models-and-compose.md#model-configuration-options)。

## 发布模型

> [!注意]
>
> 这适用于任何支持 OCI Artifacts 的容器注册表，而不仅仅是
> Docker Hub。

您可以使用新名称标记现有模型，并将其发布到不同的命名空间和存储库下：

```bash
# 使用新名称标记已拉取的模型
$ docker model tag ai/smollm2 myorg/smollm2

# 将其推送到 Docker Hub
$ docker model push myorg/smollm2
```

有关更多详细信息，请参阅 [`docker model tag`](/reference/cli/docker/model/tag)
和 [`docker model push`](/reference/cli/docker/model/push) 命令文档。

您还可以将 GGUF 格式的模型文件打包为 OCI Artifact 并发布到 Docker Hub。

```bash
# 下载 GGUF 格式的模型文件，例如从 HuggingFace
$ curl -L -o model.gguf https://huggingface.co/TheBloke/Mistral-7B-v0.1-GGUF/resolve/main/mistral-7b-v0.1.Q4_K_M.gguf

# 将其打包为 OCI Artifact 并推送到 Docker Hub
$ docker model package --gguf "$(pwd)/model.gguf" --push myorg/mistral-7b-v0.1:Q4_K_M
```

有关更多详细信息，请参阅
[`docker model package`](/reference/cli/docker/model/package/) 命令文档。

## 故障排除

### 显示日志

要排查问题，请显示日志：

{{< tabs group="release" >}}
{{< tab name="从 Docker Desktop">}}

选择 **模型**，然后选择 **日志** 选项卡。

![显示模型视图的屏幕截图。](./images/dmr-logs.png)

{{< /tab >}}
{{< tab name="从 Docker CLI">}}

使用 [`docker model logs` 命令](/reference/cli/docker/model/logs/)。

{{< /tab >}}
{{< /tabs >}}

### 检查请求和响应

检查请求和响应有助于诊断与模型相关的问题。
例如，您可以评估上下文使用情况，以验证您是否保持在模型的上下文窗口内，或者在开发框架时显示请求的完整正文以控制传递给模型的参数。

在 Docker Desktop 中，要检查每个模型的请求和响应：

1. 选择 **模型**，然后选择 **请求** 选项卡。此视图显示对所有模型的所有请求：
   - 请求发送的时间。
   - 模型名称和版本
   - 提示/请求
   - 上下文使用情况
   - 生成响应所花费的时间。
1. 选择一个请求以显示更多详细信息：
   - 在 **概览** 选项卡中，查看 token 使用情况、响应元数据和生成速度，以及实际的提示和响应。
   - 在 **请求** 和 **响应** 选项卡中，查看请求和响应的完整 JSON 负载。

> [!注意]
> 您还可以在选择一个模型后选择 **请求** 选项卡来显示特定模型的请求。

## 相关页面

- [以编程方式与您的模型交互](./api-reference.md)
- [模型与 Compose](../compose/models-and-compose.md)
- [Docker Model Runner CLI 参考文档](/reference/cli/docker/model)