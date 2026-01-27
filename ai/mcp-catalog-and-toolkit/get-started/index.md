# Docker MCP Toolkit 入门指南




Docker MCP Toolkit 可以轻松设置、管理和运行容器化的 Model Context Protocol (MCP) 服务器，并将其连接到 AI 代理。它提供了安全的默认配置，并支持不断增长的基于 LLM 的客户端生态系统。本页面将向您展示如何快速开始使用 Docker MCP Toolkit。

## 设置

在开始之前，请确保您满足以下要求以开始使用 Docker MCP Toolkit。

1. 下载并安装最新版本的 [Docker Desktop](/get-started/get-docker/)。
2. 打开 Docker Desktop 设置，然后选择 **Beta features**。
3. 选择 **Enable Docker MCP Toolkit**。
4. 选择 **Apply**。

Docker Desktop 中的 **Learning center** 提供了教程和资源，帮助您开始使用 Docker 产品和功能。在 **MCP Toolkit** 页面上，**Get started** 教程将指导您安装 MCP 服务器、连接客户端并测试您的设置。

或者，请按照本页的分步说明来：

- [安装 MCP 服务器](#install-mcp-servers)
- [连接客户端](#connect-clients)
- [验证连接](#verify-connections)

## 安装 MCP 服务器

**Docker Desktop**



1. 在 Docker Desktop 中，选择 **MCP Toolkit**，然后选择 **Catalog** 选项卡。
2. 在目录中搜索 **GitHub Official** 服务器，然后选择加号图标将其添加。
3. 在 **GitHub Official** 服务器页面，选择 **Configuration** 选项卡，然后选择 **OAuth**。

   > [!NOTE]
   >
   > 所需的配置类型取决于您选择的服务器。对于 GitHub Official 服务器，您必须使用 OAuth 进行身份验证。

   您的浏览器将打开 GitHub 授权页面。请按照屏幕上的说明 [通过 OAuth 进行身份验证](/manuals/ai/mcp-catalog-and-toolkit/toolkit.md#authenticate-via-oauth)。

4. 身份验证完成后返回 Docker Desktop。
5. 在目录中搜索 **Playwright** 服务器并添加它。

**CLI**



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

   您的浏览器将打开 GitHub 授权页面。请按照屏幕上的说明 [通过 OAuth 进行身份验证](/manuals/ai/mcp-catalog-and-toolkit/toolkit.md#authenticate-via-oauth)。

3. 添加 **Playwright** 服务器。运行：

   ```console
   $ docker mcp server enable playwright
   ```

   

您已成功添加 MCP 服务器。接下来，连接 MCP 客户端以在 AI 应用程序中使用 MCP Toolkit。

## 连接客户端

要将客户端连接到 MCP Toolkit：

1. 在 Docker Desktop 中，选择 **MCP Toolkit**，然后选择 **Clients** 选项卡。
2. 在列表中找到您的应用程序。
3. 选择 **Connect** 以配置客户端。

如果您的客户端未列出，您可以通过 `stdio` 手动连接 MCP Toolkit，方法是配置您的客户端运行以下命令：

```plaintext
docker mcp gateway run
```

例如，如果您的客户端使用 JSON 文件来配置 MCP 服务器，您可以添加如下条目：

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

请查阅您正在使用的应用程序的文档，了解如何手动设置 MCP 服务器的说明。

## 验证连接

请参考相关部分，了解如何验证您的设置是否正常工作：

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

如果您为特定项目配置了 MCP Toolkit，请导航到相关的项目目录。然后运行 `claude mcp list`。输出应显示 `MCP_DOCKER`，状态为 "connected"：

```console
$ claude mcp list
Checking MCP server health...

MCP_DOCKER: docker mcp gateway run - ✓ Connected
```

通过提交一个调用您已安装的 MCP 服务器的提示来测试连接：

```console
$ claude "使用 GitHub MCP 服务器向我展示我的开放拉取请求"
```

### Claude Desktop

重启 Claude Desktop 并检查聊天输入中的 **Search and tools** 菜单。您应该看到 `MCP_DOCKER` 服务器已列出并启用：

![Claude Desktop](images/claude-desktop.avif)

通过提交一个调用您已安装的 MCP 服务器的提示来测试连接：

```plaintext
使用 GitHub MCP 服务器向我展示我的开放拉取请求
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
$ codex "使用 GitHub MCP 服务器向我展示我的开放拉取请求"
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
$ cn "使用 GitHub MCP 服务器向我展示我的开放拉取请求"
```

### Cursor

打开 Cursor。如果您为特定项目配置了 MCP Toolkit，请打开相关的项目目录。然后导航到 **Cursor Settings > Tools & MCP**。您应该在 **Installed MCP Servers** 下看到 `MCP_DOCKER`：

![Cursor](images/cursor.avif)

通过提交一个调用您已安装的 MCP 服务器的提示来测试连接：

```plaintext
使用 GitHub MCP 服务器向我展示我的开放拉取请求
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
$ gemini "使用 GitHub MCP 服务器向我展示我的开放拉取请求"
```

### Goose

**Desktop app**



打开 Goose 桌面应用程序，然后在侧边栏中选择 **Extensions**。在 **Enabled Extensions** 下，您应该看到一个名为 `Mcpdocker` 的扩展：

![Goose desktop app](images/goose.avif)

**CLI**



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



通过提交一个调用您已安装的 MCP 服务器的提示来测试连接：

```plaintext
使用 GitHub MCP 服务器向我展示我的开放拉取请求
```

### Gordon

在 Docker Desktop 中打开 **Ask Gordon** 视图，然后选择聊天输入区域中的工具箱图标。**MCP Toolkit** 选项卡显示 MCP Toolkit 是否已启用，并显示所有提供的工具：

![MCP Toolkit in the Ask Gordon UI](images/ask-gordon.avif)

通过提交一个调用您已安装的 MCP 服务器的提示来测试连接，可以直接在 Docker Desktop 中或使用 CLI：

```console
$ docker ai "使用 GitHub MCP 服务器向我展示我的开放拉取请求"
```

### LM Studio

重启 LM Studio 并开始新的聊天。打开集成菜单并查找名为 `mcp/mcp-docker` 的条目。使用切换按钮启用服务器：

![LM Studio](images/lm-studio.avif)

通过提交一个调用您已安装的 MCP 服务器的提示来测试连接：

```plaintext
使用 GitHub MCP 服务器向我展示我的开放拉取请求
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
$ opencode "使用 GitHub MCP 服务器向我展示我的开放拉取请求"
```

### Sema4.ai Studio {#sema4}

在 Sema4.ai Studio 中，在侧边栏中选择 **Actions**，然后选择 **MCP Servers** 选项卡。您应该在列表中看到 Docker MCP Toolkit：

![Docker MCP Toolkit in Sema4.ai Studio](./images/sema4-mcp-list.avif)

要在 Sema4.ai 中使用 MCP Toolkit，请将其添加为代理操作。找到您想要连接到 MCP Toolkit 的代理并打开代理编辑器。选择 **Add Action**，在列表中启用 Docker MCP Toolkit，然后保存您的代理：

![Editing an agent in Sema4.ai Studio](images/sema4-edit-agent.avif)

通过提交一个调用您已安装的 MCP 服务器的提示来测试连接：

```plaintext
使用 GitHub MCP 服务器向我展示我的开放拉取请求
```

### Visual Studio Code {#vscode}

打开 Visual Studio Code。如果您为特定项目配置了 MCP Toolkit，请打开相关的项目目录。然后打开 **Extensions** 面板。您应该看到 `MCP_DOCKER` 服务器已列出在已安装的 MCP 服务器下。

![MCP_DOCKER installed in Visual Studio Code](images/vscode-extensions.avif)

通过提交一个调用您已安装的 MCP 服务器的提示来测试连接：

```plaintext
使用 GitHub MCP 服务器向我展示我的开放拉取请求
```

### Zed

启动 Zed 并打开代理设置：

![Opening Zed agent settings from command palette](images/zed-cmd-palette.avif)

确保 `MCP_DOCKER` 在 MCP Servers 部分已列出并启用：

![MCP_DOCKER in Zed's agent settings](images/zed-agent-settings.avif)

通过提交一个调用您已安装的 MCP 服务器的提示来测试连接：

```plaintext
使用 GitHub MCP 服务器向我展示我的开放拉取请求
```

## 进一步阅读

- [MCP Toolkit](/manuals/ai/mcp-catalog-and-toolkit/toolkit.md)
- [MCP Catalog](/manuals/ai/mcp-catalog-and-toolkit/catalog.md)
- [MCP Gateway](/manuals/ai/mcp-catalog-and-toolkit/mcp-gateway.md)
