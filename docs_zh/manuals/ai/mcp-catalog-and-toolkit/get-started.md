---
title: Docker MCP Toolkit 入门指南
linkTitle: 入门
description: 了解如何快速安装和使用 MCP Toolkit 来设置服务器和客户端。
keywords: Docker MCP Toolkit, MCP server, MCP client, AI agents
weight: 5
params:
  test_prompt: 使用 GitHub MCP 服务器向我展示我的开放拉取请求
---

{{< summary-bar feature_name="Docker MCP Toolkit" >}}

> [!NOTE]
> 本页描述的是 Docker Desktop 4.62 及更高版本中的 MCP Toolkit 界面。较早版本的界面有所不同。请升级后再严格按照这些说明操作。

Docker MCP Toolkit 可以轻松地在配置文件中设置、管理和运行容器化的 Model Context Protocol (MCP) 服务器，并将其连接到 AI 代理。它提供了安全的默认配置，并支持不断增长的基于 LLM 的客户端生态系统。本页面将向您展示如何快速开始使用 Docker MCP Toolkit。

## 设置

在开始之前，请确保您满足以下要求以开始使用 Docker MCP Toolkit。

1. 下载并安装最新版本的 [Docker Desktop](/get-started/get-docker/)。
2. 打开 Docker Desktop 设置，然后选择 **Beta features**。
3. 选择 **Enable Docker MCP Toolkit**。
4. 选择 **Apply**。

Docker Desktop 中的 **Learning center** 提供了教程和资源，帮助您开始使用 Docker 产品和功能。在 **MCP Toolkit** 页面上，**Get started** 教程将指导您安装 MCP 服务器、连接客户端并测试您的设置。

或者，请按照本页的分步说明操作：

- [创建配置文件](#create-a-profile) —— 用于组织服务器的工作区
- [向配置文件添加 MCP 服务器](#add-mcp-servers) —— 从目录中选择工具
- [连接客户端](#connect-clients) —— 将 AI 应用程序关联到你的配置文件
- [验证连接](#verify-connections) —— 测试一切是否正常工作

配置完成后，你的 AI 应用程序即可使用配置文件中的所有服务器。

> [!TIP]
> 更喜欢在终端中操作？有关使用 `docker mcp` 命令的说明，参见[从 CLI 使用 MCP Toolkit](cli.md)。

## Create a profile（创建配置文件）

配置文件将你的 MCP 服务器组织成集合。为你的工作创建一个配置文件：

> [!NOTE]
> 如果你是从旧版本的 MCP Toolkit 升级而来，你现有的服务器配置已经存在于 `default` 配置文件中。你可以继续使用默认配置文件，也可以为不同项目创建新的配置文件。

1. 在 Docker Desktop 中，选择 **MCP Toolkit**，然后选择 **Profiles** 选项卡。
2. 选择 **Create profile**。
3. 为配置文件输入名称（例如 "Frontend development"）。
4. 你可以选择现在添加服务器和客户端，也可以稍后再添加。
5. 选择 **Create**。

你的新配置文件会出现在配置文件列表中。

## Add MCP servers（添加 MCP 服务器）

1. 在 Docker Desktop 中，选择 **MCP Toolkit**，然后选择 **Catalog** 选项卡。
2. 浏览目录并选择你想添加的服务器。
3. 选择 **Add to** 按钮，并选择要将服务器添加到现有配置文件，还是创建新的配置文件。

如果某个服务器需要配置，其名称旁会出现 **Configuration Required** 徽章。你必须完成必填配置后才能使用该服务器。

您已成功将 MCP 服务器添加到配置文件。接下来，连接 MCP 客户端以使用配置文件中的服务器。

## Connect clients（连接客户端）

要将客户端连接到 MCP Toolkit：

1. 在 Docker Desktop 中，选择 **MCP Toolkit**，然后选择 **Clients** 选项卡。
2. 在列表中找到您的应用程序。
3. 选择 **Connect** 以配置客户端。

如果您的客户端未列出，您可以通过 `stdio` 手动连接 MCP Toolkit，方法是配置您的客户端使用你的配置文件运行网关：

```plaintext
docker mcp gateway run --profile my_profile
```

例如，如果您的客户端使用 JSON 文件来配置 MCP 服务器，您可以添加如下条目：

```json {title="Example configuration"
{
  "servers": {
    "MCP_DOCKER": {
      "command": "docker",
      "args": ["mcp", "gateway", "run", "--profile", "my_profile"],
      "type": "stdio"
    }
  }
}
```

请查阅您正在使用的应用程序的文档，了解如何手动设置 MCP 服务器的说明。

## Verify connections（验证连接）

请参考相关部分，了解如何验证您的设置是否正常工作：

- [Claude Code](#claude-code)
- [Claude Desktop](#claude-desktop)
- [OpenAI Codex](#codex)
- [Continue](#continue)
- [Cursor](#cursor)
- [Gemini](#gemini)
- [Goose](#goose)
- [LM Studio](#lm-studio)
- [OpenCode](#opencode)
- [Sema4.ai](#sema4)
- [Visual Studio Code](#vscode)
- [Zed](#zed)

### Claude Code

如果您为特定项目配置了 MCP Toolkit，请导航到相关的项目目录。然后运行 `claude mcp list`。输出应显示 `MCP_DOCKER`，状态为 "connected"：

```console
$ claude mcp list
Checking MCP server health...

MCP_DOCKER: docker mcp gateway run - ✓ Connected
```

通过提交一个调用您已安装的 MCP 服务器的提示来测试连接：

```console
$ claude "{{% param test_prompt %}}"
```

### Claude Desktop

重启 Claude Desktop 并检查聊天输入中的 **Search and tools** 菜单。您应该看到 `MCP_DOCKER` 服务器已列出并启用：

![Claude Desktop](images/claude-desktop.avif)

通过提交一个调用您已安装的 MCP 服务器的提示来测试连接：

```plaintext
{{% param test_prompt %}}
```

### Codex

运行 `codex mcp list` 以查看活动的 MCP 服务器及其状态。`MCP_DOCKER` 服务器应出现在列表中，状态为 "enabled"：

```console
$ codex mcp list
Name        Command  Args             Env  Cwd  Status   Auth
MCP_DOCKER  docker   mcp gateway run  -    -    enabled  Unsupported
```

通过提交一个调用您已安装的 MCP 服务器的提示来测试连接：

```console
$ codex "{{% param test_prompt %}}"
```

### Continue

通过运行 `cn` 启动 Continue 终端 UI。使用 `/mcp` 命令查看活动的 MCP 服务器及其状态。`MCP_DOCKER` 服务器应出现在列表中，状态为 "connected"：

```plaintext
   MCP Servers

   ➤ 🟢 MCP_DOCKER (🔧75 📝3)
     🔄 Restart all servers
     ⏹️ Stop all servers
     🔍 Explore MCP Servers
     Back

   ↑/↓ to navigate, Enter to select, Esc to go back
```

通过提交一个调用您已安装的 MCP 服务器的提示来测试连接：

```console
$ cn "{{% param test_prompt %}}"
```

### Cursor

打开 Cursor。如果您为特定项目配置了 MCP Toolkit，请打开相关的项目目录。然后导航到 **Cursor Settings > Tools & MCP**。您应该在 **Installed MCP Servers** 下看到 `MCP_DOCKER`：

![Cursor](images/cursor.avif)

通过提交一个调用您已安装的 MCP 服务器的提示来测试连接：

```plaintext
{{% param test_prompt %}}
```

### Gemini

运行 `gemini mcp list` 以查看活动的 MCP 服务器及其状态。`MCP_DOCKER` 应出现在列表中，状态为 "connected"。

```console
$ gemini mcp list
Configured MCP servers:

✓ MCP_DOCKER: docker mcp gateway run (stdio) - Connected
```

通过提交一个调用您已安装的 MCP 服务器的提示来测试连接：

```console
$ gemini "{{% param test_prompt %}}"
```

### Goose

{{< tabs >}}
{{< tab name="Desktop app" >}}

打开 Goose 桌面应用程序，然后在侧边栏中选择 **Extensions**。在 **Enabled Extensions** 下，您应该看到一个名为 `Mcpdocker` 的扩展：

![Goose desktop app](images/goose.avif)

{{< /tab >}}
{{< tab name="CLI" >}}

运行 `goose info -v` 并在 extensions 下查找名为 `mcpdocker` 的条目。状态应显示为 `enabled: true`：

```console
$ goose info -v
…
    mcpdocker:
      args:
      - mcp
      - gateway
      - run
      available_tools: []
      bundled: null
      cmd: docker
      description: The Docker MCP Toolkit allows for easy configuration and consumption of MCP servers from the Docker MCP Catalog
      enabled: true
      env_keys: []
      envs: {}
      name: mcpdocker
      timeout: 300
      type: stdio
```

{{< /tab >}}
{{< /tabs >}}

通过提交一个调用您已安装的 MCP 服务器的提示来测试连接：

```plaintext
{{% param "test_prompt" %}}
```

### LM Studio

重启 LM Studio 并开始新的聊天。打开集成菜单并查找名为 `mcp/mcp-docker` 的条目。使用切换按钮启用服务器：

![LM Studio](images/lm-studio.avif)

通过提交一个调用您已安装的 MCP 服务器的提示来测试连接：

```plaintext
{{% param "test_prompt" %}}
```

### OpenCode

OpenCode 配置文件（默认位于 `~/.config/opencode/opencode.json`）包含 MCP Toolkit 的设置：

```json
{
  "mcp": {
    "MCP_DOCKER": {
      "type": "local",
      "command": ["docker", "mcp", "gateway", "run"],
      "enabled": true
    }
  },
  "$schema": "https://opencode.ai/config.json"
}
```

通过提交一个调用您已安装的 MCP 服务器的提示来测试连接：

```console
$ opencode "{{% param "test_prompt" %}}"
```

### Sema4.ai Studio {#sema4}

在 Sema4.ai Studio 中，在侧边栏中选择 **Actions**，然后选择 **MCP Servers** 选项卡。您应该在列表中看到 Docker MCP Toolkit：

![Docker MCP Toolkit in Sema4.ai Studio](./images/sema4-mcp-list.avif)

要在 Sema4.ai 中使用 MCP Toolkit，请将其添加为代理操作。找到您想要连接到 MCP Toolkit 的代理并打开代理编辑器。选择 **Add Action**，在列表中启用 Docker MCP Toolkit，然后保存您的代理：

![Editing an agent in Sema4.ai Studio](images/sema4-edit-agent.avif)

通过提交一个调用您已安装的 MCP 服务器的提示来测试连接：

```plaintext
{{% param test_prompt %}}
```

### Visual Studio Code {#vscode}

打开 Visual Studio Code。如果您为特定项目配置了 MCP Toolkit，请打开相关的项目目录。然后打开 **Extensions** 面板。您应该看到 `MCP_DOCKER` 服务器已列出在已安装的 MCP 服务器下。

![MCP_DOCKER installed in Visual Studio Code](images/vscode-extensions.avif)

通过提交一个调用您已安装的 MCP 服务器的提示来测试连接：

```plaintext
{{% param test_prompt %}}
```

### Zed

启动 Zed 并打开代理设置：

![Opening Zed agent settings from command palette](images/zed-cmd-palette.avif)

确保 `MCP_DOCKER` 在 MCP Servers 部分已列出并启用：

![MCP_DOCKER in Zed's agent settings](images/zed-agent-settings.avif)

通过提交一个调用您已安装的 MCP 服务器的提示来测试连接：

```plaintext
{{% param test_prompt %}}
```

## 进一步阅读

- [MCP Profiles](/manuals/ai/mcp-catalog-and-toolkit/profiles.md)
- [MCP Toolkit](/manuals/ai/mcp-catalog-and-toolkit/toolkit.md)
- [MCP Catalog](/manuals/ai/mcp-catalog-and-toolkit/catalog.md)
- [MCP Gateway](/manuals/ai/mcp-catalog-and-toolkit/mcp-gateway.md)
