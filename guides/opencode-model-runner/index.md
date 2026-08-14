# 将 OpenCode 与 Docker Model Runner 配合使用


本指南介绍如何将 OpenCode 连接到 Docker Model Runner，以便 OpenCode 能够使用本地模型完成编码任务。您将配置一个 `opencode.json` 文件，验证 API 端点，并针对本地 Docker 环境中提供的模型运行 OpenCode。

> **致谢**
>
> Docker 感谢 [Pradumna Saraf](https://twitter.com/pradumna_saraf) 对本指南的贡献。

与 [OpenCode 沙箱指南](../manuals/ai/sandboxes/agents/opencode.md) 不同，本指南侧重于将 OpenCode 用作由 Docker Model Runner 支撑的本地编码工具，而不是在容器化沙箱中运行 OpenCode。

在本指南中，您将学习如何：

- 为 OpenCode 拉取编码模型
- 配置 OpenCode 以使用 Docker Model Runner
- 验证本地 API 端点并启动 OpenCode
- 在需要时，使用更大的上下文窗口打包 `gpt-oss`

## 前提条件

在开始之前，请确保您已具备：

- 已安装 [Docker Desktop](../get-started/get-docker.md) 或 Docker Engine
- 已[启用 Docker Model Runner](../manuals/ai/model-runner/get-started.md#enable-docker-model-runner)
- 已[安装 OpenCode](https://opencode.ai/docs)

如果您使用 Docker Desktop，请在 **Settings** > **AI** 中开启 TCP 访问，或运行：

```console
$ docker desktop enable model-runner --tcp 12434
```

## 第 1 步：拉取编码模型

在配置 OpenCode 之前，先拉取一个或多个模型：

```console
$ docker model pull ai/qwen3-coder
$ docker model pull ai/devstral-small-2
```

这些模型非常适合编码工作流，因为它们支持较大的上下文窗口。

## 第 2 步：创建 OpenCode 配置

OpenCode 会从以下任一位置读取配置：

- `~/.config/opencode/opencode.json`（用于全局配置）
- 项目根目录中的 `opencode.json`（用于项目级配置）

项目级配置会覆盖全局文件。

添加一个指向 Docker Model Runner 的 provider：

```json {title="opencode.json"}
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "dmr": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Docker Model Runner",
      "options": {
        "baseURL": "http://localhost:12434/v1"
      },
      "models": {
        "qwen3-coder": {
          "name": "ai/qwen3-coder"
        },
        "devstral-small-2": {
          "name": "ai/devstral-small-2"
        }
      }
    }
  }
}
```

此配置将 Docker Model Runner 添加为 OpenCode 的 provider，并暴露两个本地模型。

> [!NOTE]
>
> 如果您的设置期望使用旧的兼容 OpenAI 的路径，请改用 `http://localhost:12434/engines/v1`。

## 第 3 步：验证端点

在打开 OpenCode 之前，检查 Docker Model Runner 是否可访问：

```console
$ curl http://localhost:12434/v1/models
```

如果您使用的是旧路径，请运行：

```console
$ curl http://localhost:12434/engines/v1/models
```

响应中应列出通过 Docker Model Runner 可用的模型。

## 第 4 步：启动 OpenCode

从您的项目目录运行：

```console
$ opencode
```

若要从 TUI 切换模型，请运行：

```text
/models
```

然后从 `dmr` provider 中选择模型。

## 第 5 步：使用更大的上下文窗口打包 `gpt-oss`

此步骤为可选。如果您需要更大的上下文窗口来处理仓库级别的任务，可以使用它。

`gpt-oss` 默认的上下文窗口比面向编码的模型要小。如果您希望将其用于仓库级别的任务，请打包一个更大的变体：

```console
$ docker model pull ai/gpt-oss
$ docker model package --from ai/gpt-oss --context-size 128000 gpt-oss:128k
```

然后将其添加到您的 OpenCode 配置中：

```json {title="opencode.json"}
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "dmr": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Docker Model Runner",
      "options": {
        "baseURL": "http://localhost:12434/v1"
      },
      "models": {
        "gpt-oss:128k": {
          "name": "gpt-oss:128k"
        }
      }
    }
  }
}
```

## 故障排查

如果 OpenCode 无法连接，请检查 Docker Model Runner 的状态：

```console
$ docker model status
```

如果 OpenCode 没有显示您的模型，请列出本地模型：

```console
$ docker model ls
```

如果模型缺失，请先拉取它，并确认 `opencode.json` 中的模型名称与您想要使用的本地模型一致。

## 了解更多

- [Docker Model Runner 概述](../manuals/ai/model-runner/_index.md)
- [Docker Model Runner API 参考](../manuals/ai/model-runner/api-reference.md)
- [IDE 与工具集成](../manuals/ai/model-runner/ide-integrations.md)
