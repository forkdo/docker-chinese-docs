# 在 Docker Sandbox 中通过 Docker Model Runner 运行 Claude Code


本指南展示如何在 Docker Sandbox 中运行 Claude Code，并将 Docker Model Runner 作为后端模型提供者。您将把智能体隔离在微虚拟机中、将其指向您机器上的本地模型，并让所有模型流量都留在设备本地。

> **致谢**
>
> Docker 感谢 [Pradumna Saraf](https://twitter.com/pradumna_saraf) 对本指南的贡献。

在本指南中，您将学习如何：

- 拉取一个编码模型并启用 TCP 后启动 Docker Model Runner
- 允许沙箱访问您主机上的 Docker Model Runner
- 创建 Claude Code 沙箱并持久设置本地端点
- 使用本地模型启动 Claude Code 并验证连接
- 打包具有更大上下文窗口的 `gpt-oss`，以支持更长的提示

## 各部分如何协作

三个组件在运行时协同工作：

- **Docker Model Runner** 运行在您的主机上，并在 `http://localhost:12434` 提供一个兼容 Anthropic 的 API。
- **Docker Sandbox** 在隔离的微虚拟机中运行 Claude Code。微虚拟机拥有自己的网络，无法直接访问您主机的 `localhost`。
- **沙箱代理 (sandbox proxy)** 位于您的主机上，并为来自沙箱的每个出站请求进行中转。它强制执行网络策略，并将特殊主机名 `host.docker.internal` 转换为 `localhost`。

沙箱内的 Claude Code 将请求发送到 `http://host.docker.internal:12434`。代理将目标重写为 `localhost:12434`，由 Docker Model Runner 响应。没有任何模型流量离开您的机器。

## 先决条件

在开始之前，请确保您已具备：

- 已安装 [Docker Desktop](../get-started/get-docker.md) 或 Docker Engine
- 已[启用 Docker Model Runner](../manuals/ai/model-runner/get-started.md#enable-docker-model-runner)
- 已[安装并登录 Docker Sandboxes (`sbx`)](../manuals/ai/sandboxes/get-started.md#install-and-sign-in)

如果您使用 Docker Desktop，请在 **设置** > **AI** 中打开 TCP 访问，或运行：

```console
$ docker desktop enable model-runner --tcp 12434
```

## 步骤 1：拉取编码模型

在创建沙箱之前，先在您的主机上拉取一个模型：

```console
$ docker model pull ai/devstral-small-2
```

如果您想要另一个具有大上下文窗口、专注于编码的模型，也可以使用 `ai/qwen3-coder`。

## 步骤 2：允许沙箱访问 Docker Model Runner

默认情况下，沙箱是网络隔离的，因此在沙箱可以访问 Docker Model Runner 之前，您需要一个策略规则。

该规则针对代理转发到的目标进行匹配，而不是沙箱使用的主机名。由于代理在转发之前将 `host.docker.internal` 重写为 `localhost`，因此该规则允许 `localhost:12434`，即使 Claude Code 在其请求中使用的是 `host.docker.internal`：

```console
$ sbx policy allow network localhost:12434
```

有关从沙箱访问主机服务的背景信息，请参阅[从沙箱访问主机服务](../manuals/ai/sandboxes/workflows.md#accessing-host-services-from-a-sandbox)。

## 步骤 3：创建 Claude Code 沙箱

从您的项目目录中，创建一个不启动智能体的沙箱：

```console
$ cd ~/my-project
$ sbx create claude --name claude-dmr .
```

`sbx run` 也可以工作，但它会立即启动 Claude Code。如果没有设置 `ANTHROPIC_BASE_URL`，Claude Code 会指向 `api.anthropic.com`，并在您修复端点之前提示进行 OAuth 或报错。先创建沙箱可以让您在智能体启动之前将本地端点写入其中。

您无需设置 Anthropic API 密钥或运行 `sbx secret set anthropic`。Docker Model Runner 不会对本地端点进行身份验证，并且沙箱代理仅为发往 `api.anthropic.com` 的请求注入凭据。有关代理进行身份验证的完整服务列表，请参阅[凭据](../manuals/ai/sandboxes/security/credentials.md)。

## 步骤 4：在沙箱内设置本地端点

将 `ANTHROPIC_BASE_URL` 追加到沙箱的持久化环境文件中，以便 Claude Code 在每次启动时都能读取它：

```console
$ sbx exec -d claude-dmr bash -c "echo 'export ANTHROPIC_BASE_URL=http://host.docker.internal:12434' >> /etc/sandbox-persistent.sh"
```

`bash -c` 包装器确保 `>>` 重定向在沙箱内部运行，而不是在您的主机上运行。有关此方法的详细信息，请参阅[如何在沙箱内部设置自定义环境变量？](../manuals/ai/sandboxes/faq.md#how-do-i-set-custom-environment-variables-inside-a-sandbox)。

要确认变量已设置，请在沙箱中打开一个 shell：

```console
$ sbx exec -it claude-dmr bash
$ echo $ANTHROPIC_BASE_URL
http://host.docker.internal:12434
```

## 步骤 5：验证与 Docker Model Runner 的连接

仍在沙箱 shell 内部，向主机端点发送一个测试请求：

```console
$ curl http://host.docker.internal:12434/v1/messages \
  -H "Content-Type: application/json" \
  -d '{
    "model": "ai/devstral-small-2",
    "max_tokens": 32,
    "messages": [{"role": "user", "content": "Say hello"}]
  }'
```

成功的响应确认策略规则和基础 URL 是正确的。输入 `exit` 离开 shell。有关请求格式的更多详细信息，请参阅[兼容 Anthropic 的 API 参考](../manuals/ai/model-runner/api-reference.md#anthropic-compatible-api)。

## 步骤 6：使用本地模型启动 Claude Code

在沙箱中运行 Claude Code，并将模型标志转发给智能体：

```console
$ sbx run claude-dmr -- --model ai/devstral-small-2
```

`--` 之后的所有内容都会转发给 Claude Code CLI。由于 `ANTHROPIC_BASE_URL` 设置在沙箱的持久化环境中，Claude Code 会将请求路由到您主机上的 Docker Model Runner，而不是 `api.anthropic.com`。

## 步骤 7：检查 Claude Code 请求

要检查 Claude Code 发送的请求，请在您的主机上运行：

```console
$ docker model requests --model ai/devstral-small-2 | jq .
```

这有助于您在不附加到沙箱的情况下调试提示、上下文使用情况以及兼容性问题。

## 步骤 8：打包具有更大上下文窗口的 `gpt-oss`

`ai/gpt-oss` 默认使用比专注于编码的模型更小的上下文窗口。要将其用于仓库级别的提示，请在主机上打包一个更大的变体：

```console
$ docker model pull ai/gpt-oss
$ docker model package --from ai/gpt-oss --context-size 32000 gpt-oss:32k
```

然后在下次运行沙箱时，将 Claude Code 指向打包后的模型：

```console
$ sbx run claude-dmr -- --model gpt-oss:32k
```

## 清理

Claude Code 退出后，沙箱会持续存在。要在不删除沙箱的情况下停止它：

```console
$ sbx stop claude-dmr
```

要移除沙箱及其内部的所有内容，包括持久化环境文件：

```console
$ sbx rm claude-dmr
```

您工作区中的文件不受影响。

## 了解更多

- [将 Claude Code 与 Docker Model Runner 配合使用](claude-code-model-runner.md)
- [Docker Sandboxes 入门](../manuals/ai/sandboxes/get-started.md)
- [Docker Sandboxes 中的 Claude Code](../manuals/ai/sandboxes/agents/claude-code.md)
- [Docker Model Runner 概述](../manuals/ai/model-runner/_index.md)
- [Docker Model Runner API 参考](../manuals/ai/model-runner/api-reference.md)

