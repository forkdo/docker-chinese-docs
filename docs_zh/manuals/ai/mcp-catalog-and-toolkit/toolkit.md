---
title: Docker MCP Toolkit
linkTitle: MCP Toolkit
description: 使用 MCP Toolkit 设置 MCP 服务器和 MCP 客户端。
keywords: Docker MCP Toolkit, MCP 服务器, MCP 客户端, AI 代理
weight: 30
aliases:
  - /desktop/features/gordon/mcp/gordon-mcp-server/
  - /ai/gordon/mcp/gordon-mcp-server/
---

{{< summary-bar feature_name="Docker MCP Toolkit" >}}

Docker MCP Toolkit 是集成在 Docker Desktop 中的管理界面，可让您设置、管理和运行容器化的 MCP 服务器，并将它们连接到 AI 代理。它通过提供安全默认值、简化设置和支持不断增长的基于 LLM 的客户端生态系统，消除了工具使用的摩擦。这是从 MCP 工具发现到本地执行的最快方式。

## 主要功能

- 跨 LLM 兼容性：支持 Claude、Cursor 和其他 MCP 客户端。
- 集成工具发现：直接在 Docker Desktop 中浏览并从 Docker MCP 目录启动 MCP 服务器。
- 零手动设置：无需依赖管理、运行时配置或设置。
- 既可作为 MCP 服务器聚合器，也可作为客户端访问已安装 MCP 服务器的网关。

> [!TIP]
> MCP Toolkit 包含 [Dynamic MCP](/manuals/ai/mcp-catalog-and-toolkit/dynamic-mcp.md)，
> 它使 AI 代理能够在对话期间按需发现、添加和组合 MCP 服务器，无需手动配置。连接到网关时，您的代理可以搜索目录并根据需要添加工具。

## MCP Toolkit 的工作原理

MCP 引入了两个核心概念：MCP 客户端和 MCP 服务器。

- MCP 客户端通常嵌入在基于 LLM 的应用程序中，例如 Claude Desktop 应用。它们请求资源或执行操作。
- MCP 服务器由客户端启动，使用任何必要的工具、语言或流程执行请求的任务。

Docker 标准化了应用程序（包括 MCP 服务器）的开发、打包和分发。通过将 MCP 服务器打包为容器，Docker 消除了隔离和环境差异相关的问题。您可以直接运行容器，无需管理依赖或配置运行时。

根据 MCP 服务器的不同，其提供的工具可能在同一容器中运行，也可能在专用容器中运行以实现更好的隔离。

## 安全性

Docker MCP Toolkit 结合被动和主动措施，减少攻击面并确保安全的运行时行为。

### 被动安全

被动安全指在构建时（将 MCP 服务器代码打包为 Docker 镜像时）实施的措施。

- 镜像签名和证明：[MCP 目录](catalog.md) 中 `mcp/` 下的所有 MCP 服务器镜像均由 Docker 构建并数字签名，以验证其来源和完整性。每个镜像包含软件物料清单 (SBOM)，确保完全透明。

### 主动安全

主动安全指在运行时（工具调用前后）实施的安全措施，通过资源和访问限制强制执行。

- CPU 分配：MCP 工具在自己的容器中运行。它们被限制为 1 个 CPU，限制潜在计算资源滥用的影响。

- 内存分配：MCP 工具的容器限制为 2 GB。

- 文件系统访问：默认情况下，MCP 服务器无法访问主机文件系统。用户明确选择将被授予文件挂载的服务器。

- 工具请求拦截：阻止包含敏感信息（如密钥）的工具请求。

### OAuth 认证

某些 MCP 服务器需要认证才能访问 GitHub、Notion 和 Linear 等外部服务。MCP Toolkit 自动处理 OAuth 认证。您通过浏览器授权访问，Toolkit 安全地管理凭据。您无需手动创建 API 密钥或为每个服务配置认证。

#### 使用 OAuth 授权服务器

{{< tabs >}}
{{< tab name="Docker Desktop">}}

1. 在 Docker Desktop 中，转到 **MCP Toolkit** 并选择 **目录** 选项卡。
2. 找到并添加需要 OAuth 的 MCP 服务器。
3. 在服务器的 **配置** 选项卡中，选择 **OAuth** 认证方法。按照链接开始 OAuth 授权。
4. 浏览器打开服务的授权页面。按照屏幕说明完成认证。
5. 认证完成后返回 Docker Desktop。

在 **OAuth** 选项卡中查看所有已授权的服务。要撤销访问权限，请选择要断开连接的服务旁边的 **撤销**。

{{< /tab >}}
{{< tab name="CLI">}}

启用 MCP 服务器：

```console
$ docker mcp server enable github-official
```

如果服务器需要 OAuth，请授权连接：

```console
$ docker mcp oauth authorize github
```

浏览器打开授权页面。完成认证过程后，返回终端。

查看已授权的服务：

```console
$ docker mcp oauth ls
```

撤销对服务的访问权限：

```console
$ docker mcp oauth revoke github
```

{{< /tab >}}
{{< /tabs >}}

## 使用示例

### 示例：将 GitHub Official MCP 服务器与 Ask Gordon 一起使用

为了说明 MCP Toolkit 的工作原理，以下是如何启用 GitHub Official MCP 服务器并使用 [Ask Gordon](/manuals/ai/gordon/_index.md) 与您的 GitHub 账户交互：

1. 从 Docker Desktop 的 **MCP Toolkit** 菜单中，选择 **目录** 选项卡，找到 **GitHub Official** 服务器并添加。
2. 在服务器的 **配置** 选项卡中，通过 OAuth 进行认证。
3. 在 **客户端** 选项卡中，确保 Gordon 已连接。
4. 从 **Ask Gordon** 菜单中，现在可以发送与 GitHub 账户相关的请求，符合 GitHub Official 服务器提供的工具。测试一下，询问 Gordon：

   ```text
   我的 GitHub 用户名是什么？
   ```

   确保在 Gordon 的回答中选择 **始终允许**，以允许 Gordon 与 GitHub 交互。

> [!TIP]
> Gordon 客户端默认启用，这意味着 Gordon 可以自动与您的 MCP 服务器交互。

### 示例：将 Claude Desktop 用作客户端

假设您已安装 Claude Desktop，并想使用 GitHub MCP 服务器和 Puppeteer MCP 服务器，您无需在 Claude Desktop 中安装这些服务器。您可以简单地在 MCP Toolkit 中安装这两个 MCP 服务器，并将 Claude Desktop 添加为客户端：

1. 从 **MCP Toolkit** 菜单中，选择 **目录** 选项卡，找到 **Puppeteer** 服务器并添加。
1. 对 **GitHub Official** 服务器重复此操作。
1. 从 **客户端** 选项卡中，选择 **Claude Desktop** 旁边的 **连接**。如果它正在运行，请重启 Claude Desktop，现在它可以访问 MCP Toolkit 中的所有服务器。
1. 在 Claude Desktop 中，使用 Sonnet 3.5 模型提交以下提示进行测试：

   ```text
   截取 docs.docker.com 的屏幕截图，然后反转颜色
   ```

### 示例：将 Visual Studio Code 用作客户端

您可以在 Visual Studio Code 中与所有已安装的 MCP 服务器交互：

1. 启用 MCP Toolkit：

   {{< tabs group="" >}}
   {{< tab name="全局启用">}}

   1. 在 Visual Studio Code 的用户 `mcp.json` 中插入以下内容：

      ```json
      "mcp": {
       "servers": {
         "MCP_DOCKER": {
           "command": "docker",
           "args": [
             "mcp",
             "gateway",
             "run"
           ],
           "type": "stdio"
         }
       }
      }
      ```

   {{< /tab >}}
   {{< tab name="为特定项目启用">}}

   1. 在终端中，导航到项目的文件夹。
   1. 运行：

      ```bash
      docker mcp client connect vscode
      ```

      > [!NOTE]
      > 此命令在当前目录中创建 `.vscode/mcp.json` 文件。由于这是用户特定的文件，请将其添加到 `.gitignore` 文件中，以防止其被提交到仓库。
      >
      > ```console
      > echo ".vscode/mcp.json" >> .gitignore
      > ```

  {{< /tab >}}
  {{</tabs >}}

1. 在 Visual Studio Code 中，打开新的聊天并选择 **代理** 模式：

   ![Copilot 模式切换](./images/copilot-mode.png)

1. 您还可以检查可用的 MCP 工具：

   ![在 VSCode 中显示工具](./images/tools.png)

有关代理模式的更多信息，请参阅
[Visual Studio Code 文档](https://code.visualstudio.com/docs/copilot/chat/mcp-servers#_use-mcp-tools-in-agent-mode)。

## 进一步阅读

- [MCP 目录](/manuals/ai/mcp-catalog-and-toolkit/catalog.md)
- [MCP 网关](/manuals/ai/mcp-catalog-and-toolkit/mcp-gateway.md)