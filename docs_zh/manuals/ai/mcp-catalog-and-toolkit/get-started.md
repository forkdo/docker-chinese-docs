---
title: Docker MCP Toolkit 快速入门
linkTitle: 快速开始
description: 了解如何快速安装和使用 MCP Toolkit 来设置服务器和客户端。
keywords: Docker MCP Toolkit, MCP server, MCP client, AI agents
weight: 10
params:
  test_prompt: 使用 GitHub MCP 服务器向我展示我的待处理拉取请求
---

{{< summary-bar feature_name="Docker MCP Toolkit" >}}

Docker MCP Toolkit 使您能够轻松设置、管理和运行容器化的模型上下文协议（MCP）服务器，并将其连接到 AI 代理。它提供安全的默认配置，并支持不断发展的基于大语言模型（LLM）的客户端生态系统。本文档将指导您快速上手 Docker MCP Toolkit。

## 环境准备

在开始之前，请确保满足以下要求以使用 Docker MCP Toolkit。

1. 下载并安装最新版本的 [Docker Desktop](/get-started/get-docker/)。
2. 打开 Docker Desktop 设置，选择 **Beta features**。
3. 勾选 **Enable Docker MCP Toolkit**。
4. 选择 **Apply**。

Docker Desktop 中的 **Learning center** 提供了教程和资源，帮助您快速上手 Docker 产品和功能。在 **MCP Toolkit** 页面中，**Get started** 教程将引导您完成安装 MCP 服务器、连接客户端和测试配置。

或者，您也可以按照本文档中的分步说明进行操作：

- [安装 MCP 服务器](#install-mcp-servers)
- [连接客户端](#connect-clients)
- [验证连接](#verify-connections)

## 安装 MCP 服务器

{{< tabs >}}
{{< tab name="Docker Desktop">}}

1. 在 Docker Desktop 中，选择 **MCP Toolkit**，然后选择 **Catalog** 选项卡。
2. 在目录中搜索 **GitHub Official** 服务器，然后点击加号图标添加它。
3. 在 **GitHub Official** 服务器页面中，选择 **Configuration** 选项卡，然后选择 **OAuth**。

   > [!NOTE]
   >
   > 所需的配置类型取决于您选择的服务器。对于 GitHub Official 服务器，您必须使用 OAuth 进行身份验证。

   您的浏览器将打开 GitHub 授权页面。请按照屏幕上的说明[通过 OAuth 进行身份验证](/manuals/ai/mcp-catalog-and-toolkit/toolkit.md#authenticate-via-oauth)。

4. 身份验证完成后，返回 Docker Desktop。
5. 在目录中搜索 **Playwright** 服务器并添加它。

{{< /tab >}}
{{< tab name="CLI">}}

1. 添加 GitHub Official MCP 服务器。运行：

   ```console
   $ docker mcp server enable github-official
   ```

2. 通过运行以下命令对服务器进行身份验证：

   ```console
   $ docker mcp oauth authorize github
   ```

   > [!NOTE]
   >
   > 所需的配置类型取决于您选择的服务器。对于 GitHub Official 服务器，您必须使用 OAuth 进行身份验证。

   您的浏览器将打开 GitHub 授权页面。请按照屏幕上的说明[通过 OAuth 进行身份验证](/manuals/ai/mcp-catalog-and-toolkit/toolkit.md#authenticate-via-oauth)。

3. 添加 **Playwright** 服务器。运行：

   ```console
   $ docker mcp server enable playwright
   ```

   {{< /tab >}}
   {{< /tabs >}}

现在您已成功添加了 MCP 服务器。接下来，连接一个 MCP 客户端以在 AI 应用中使用 MCP Toolkit。

## 连接客户端

要将客户端连接到 MCP Toolkit：

1. 在 Docker Desktop 中，选择 **MCP Toolkit**，然后选择 **Clients** 选项卡。
2. 在列表中找到您的应用程序。
3. 选择 **Connect** 以配置客户端。

如果您的客户端未在列表中显示，您可以通过配置客户端运行以下命令，手动通过 `stdio` 连接 MCP Toolkit：

```plaintext
docker mcp gateway run
```

例如，如果您的客户端使用 JSON 文件配置 MCP 服务器，您可以添加如下条目：

```json {title="Example configuration"
{
  "servers": {
    "MCP_DOCKER": {
      "command": "docker",
      "args": ["mcp", "gateway", "run"],
      "type": "stdio"
    }
  }
}
```

请查阅您正在使用的应用程序的文档，了解如何手动设置 MCP 服务器。

## 验证连接

请参考以下相关部分，了解如何验证您的配置是否正常工作：

- [Claude Code](#claude-code)
- [Claude Desktop](#claude-desktop)
- [OpenAI Codex](#codex)
- [Continue](#continue)
- [Cursor](#cursor)
- [Gemini](#gemini)
- [Goose](#goose)
- [Gordon](#gordon)
- [LM Studio](#lm-studio)
- [OpenCode](#opencode)
- [Sema4.ai](#sema4)
- [Visual Studio Code](#vscode)
- [Zed](#zed)

### Claude Code

如果您为特定项目配置了 MCP Toolkit，请导航到相应的项目目录。然后运行 `claude mcp list`。输出应显示 `MCP_DOCKER` 并显示“connected”状态：

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

重启 Claude Desktop，然后在聊天输入框中检查 **Search and tools** 菜单。您应该看到 `MCP_DOCKER` 服务器已列出并启用：

![Claude Desktop](images/claude-desktop.avif)

通过提交一个调用您已安装的 MCP 服务器的提示来测试连接：

```plaintext
{{% param test_prompt %}}
```

### Codex

运行 `codex mcp list` 查看活动的 MCP 服务器及其状态。`MCP_DOCKER` 服务器应出现在列表中，并显示“enabled”状态：

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

通过运行 `cn` 启动 Continue 终端界面。使用 `/mcp` 命令查看活动的 MCP 服务器及其状态。`MCP_DOCKER` 服务器应出现在列表中，并显示“connected”状态：

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

打开 Cursor。如果您为特定项目配置了 MCP Toolkit，请打开相应的项目目录。然后导航到 **Cursor Settings > Tools & MCP**。您应该在 **Installed MCP Servers** 下看到 `MCP_DOCKER`：

![Cursor](images/cursor.avif)

通过提交一个调用您已安装的 MCP 服务器的提示来测试连接：

```plaintext
{{% param test_prompt %}}
```

### Gemini

运行 `gemini mcp list` 查看活动的 MCP 服务器及其状态。`MCP_DOCKER` 应出现在列表中，并显示“connected”状态。

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

运行 `goose info -v` 并在扩展部分查找名为 `mcpdocker` 的条目。状态应显示 `enabled: true`：

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

### Gordon

在 Docker Desktop 中打开 **Ask Gordon** 视图，然后在聊天输入区域选择工具箱图标。**MCP Toolkit** 选项卡显示 MCP Toolkit 是否已启用，并显示所有提供的工具：

![MCP Toolkit in the Ask Gordon UI](images/ask-gordon.avif)

通过提交一个调用您已安装的 MCP 服务器的提示来测试连接，可以在 Docker Desktop 中直接操作，也可以使用 CLI：

```console
$ docker ai "{{% param "test_prompt" %}}"
```

### LM Studio

重启 LM Studio 并开始新对话。打开集成菜单，查找名为 `mcp/mcp-docker` 的条目。使用切换开关启用服务器：

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

在 Sema4.ai Studio 中，选择侧边栏中的 **Actions**，然后选择 **MCP Servers** 选项卡。您应该在列表中看到 Docker MCP Toolkit：

![Docker MCP Toolkit in Sema4.ai Studio](./images/sema4-mcp-list.avif)

要在 Sema4.ai 中使用 MCP Toolkit，请将其添加为代理操作。找到您想要连接到 MCP Toolkit 的代理，然后打开代理编辑器。选择 **Add Action**，在列表中启用 Docker MCP Toolkit，然后保存您的代理：

![Editing an agent in Sema4.ai Studio](images/sema4-edit-agent.avif)

通过提交一个调用您已安装的 MCP 服务器的提示来测试连接：

```plaintext
{{% param test_prompt %}}
```

### Visual Studio Code {#vscode}

打开 Visual Studio Code。如果您为特定项目配置了 MCP Toolkit，请打开相应的项目目录。然后打开 **Extensions** 窗格。您应该在已安装的 MCP 服务器下看到 `MCP_DOCKER` 服务器。

![MCP_DOCKER installed in Visual Studio Code](images/vscode-extensions.avif)

通过提交一个调用您已安装的 MCP 服务器的提示来测试连接：

```plaintext
{{% param test_prompt %}}
```

### Zed

启动 Zed 并打开代理设置：

![Opening Zed agent settings from command palette](images/zed-cmd-palette.avif)

确保在 MCP Servers 部分中列出并启用了 `MCP_DOCKER`：

![MCP_DOCKER in Zed's agent settings](images/zed-agent-settings.avif)

通过提交一个调用您已安装的 MCP 服务器的提示来测试连接：

```plaintext
{{% param test_prompt %}}
```

## 延伸阅读

- [MCP Toolkit](/manuals/ai/mcp-catalog-and-toolkit/toolkit.md)
- [MCP Catalog](/manuals/ai/mcp-catalog-and-toolkit/catalog.md)
- [MCP Gateway](/manuals/ai/mcp-catalog-and-toolkit/mcp-gateway.md)