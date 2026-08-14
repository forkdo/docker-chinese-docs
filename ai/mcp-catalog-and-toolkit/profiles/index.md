# MCP 配置文件




配置文件将你的 MCP 服务器组织成命名集合。如果没有配置文件，你就得为使用的每个 AI 应用程序分别配置服务器。每次想改变可用的服务器时，你都要逐一更新 Claude Desktop、VS Code、Cursor 和其他工具。配置文件通过集中管理服务器配置解决了这个问题。

## 配置文件的作用

配置文件是一组带有各自配置和设置的 MCP 服务器命名集合。你从 [MCP 目录](/manuals/ai/mcp-catalog-and-toolkit/catalog.md)（可用服务器的来源）中选择服务器，并将它们添加到配置文件（为特定工作而配置的服务器集合）中。可以把目录看作工具库，把配置文件看作为不同工作整理好的工具箱。

你的 "web-dev" 配置文件可能包含 GitHub、Playwright 和数据库服务器；"data-analysis" 配置文件可能包含电子表格、API 和可视化服务器。你可以将不同的 AI 客户端连接到不同的配置文件，或在切换任务时切换配置文件。

当你运行 MCP Gateway 或连接客户端时若未指定配置文件，Docker MCP 会使用你的默认配置文件。如果你是从旧版本的 MCP Toolkit 升级而来，你现有的服务器配置已经存在于默认配置文件中。

## 配置文件的能力

每个配置文件都维护自己独立的服务器和配置集合。你的 "web-dev" 配置文件可能包含 GitHub、Playwright 和数据库服务器，而 "data-analysis" 配置文件则包含电子表格、API 和可视化服务器。你可以按需创建任意多个配置文件，每个仅包含与该场景相关的服务器。

> [!NOTE]
>
> OAuth 凭据是配置文件隔离的一个例外——它们在所有配置文件之间共享。如果你需要为不同项目使用不同账户，请在切换配置文件时撤销并重新授权。

你可以将不同的 AI 应用程序连接到不同的配置文件。连接客户端时，你需要指定它应使用哪个配置文件。这意味着 Claude Desktop 和 VS Code 在需要时可以访问不同的服务器集合。

配置文件可以与团队共享。将配置文件推送到你的注册表，团队成员就可以拉取它，获得与你完全相同的服务器集合和配置。

## 创建和管理配置文件

### 创建配置文件

1. 在 Docker Desktop 中，选择 **MCP Toolkit**，然后选择 **Profiles** 选项卡。
2. 选择 **Create profile**。
3. 为配置文件输入名称（例如 "web-dev"）。
4. 你可以选择现在搜索并添加服务器到配置文件，也可以稍后再添加。
5. 你还可以选择搜索并添加要连接到该配置文件的客户端。
6. 选择 **Create**。

你的新配置文件会出现在配置文件列表中。

### 查看配置文件详情

在 **Profiles** 选项卡中选择某个配置文件即可查看其详情。配置文件视图有两个选项卡：

- **Overview**：显示配置文件中的服务器、密钥配置和已连接的客户端。使用 **+** 按钮可添加更多服务器或客户端。
- **Tools**：列出配置文件中各服务器提供的所有可用工具。你可以启用或禁用单个工具。

### 移除配置文件

1. 在 **Profiles** 选项卡中，找到你要移除的配置文件。
2. 选择配置文件名称旁的 ⋮，然后选择 **Delete**。
3. 确认移除。

> [!CAUTION]
> 移除配置文件会删除其所有服务器配置和设置，并更新客户端配置（移除 MCP Toolkit）。此操作无法撤销。

### 默认配置文件

当你运行 MCP Gateway 或使用 MCP Toolkit 而未指定配置文件时，Docker MCP 会使用名为 `default` 的配置文件；如果 `default` 配置文件不存在，则使用空配置。

如果你是从旧版本的 MCP Toolkit 升级而来，你现有的服务器配置会自动迁移到 `default` 配置文件。你无需手动重建设置——一切照旧工作。

你随时可以在 gateway 命令中使用 `--profile` 标志指定其他配置文件：

```console
$ docker mcp gateway run --profile web-dev
```

## 向配置文件添加服务器

配置文件包含你从目录中选择的 MCP 服务器。添加服务器可以为特定工作流整理你的工具。

### 添加服务器

你可以通过两种方式向配置文件添加服务器。

从 Catalog 选项卡：

1. 选择 **Catalog** 选项卡。
2. 勾选你想添加的服务器旁的复选框，以查看可添加到哪个配置文件。
3. 从下拉菜单中选择你的配置文件。

从配置文件内部：

1. 选择 **Profiles** 选项卡并选择你的配置文件。
2. 在 **Servers** 部分，选择 **+** 按钮。
3. 搜索并选择要添加的服务器。

如果某个服务器需要 OAuth 身份验证，系统会提示你进行授权。详情参见 [OAuth authentication](/manuals/ai/mcp-catalog-and-toolkit/toolkit.md#oauth-authentication)。

### 列出配置文件中的服务器

在 **Profiles** 选项卡中选择某个配置文件，即可查看其包含的所有服务器。

### 移除服务器

1. 选择 **Profiles** 选项卡并选择你的配置文件。
2. 在 **Servers** 部分，找到你要移除的服务器。
3. 选择该服务器旁的删除图标。

## 配置配置文件

### 服务器配置

有些服务器除身份验证外还需要其他配置。请在你的配置文件中配置服务器设置。

1. 选择 **Profiles** 选项卡并选择你的配置文件。
2. 在 **Servers** 部分，选择该服务器旁的配置图标。
3. 按需调整服务器的配置设置。

### OAuth 凭据

OAuth 凭据在所有配置文件之间共享。当你授权访问 GitHub 或 Notion 等服务后，该授权可供任意配置文件中任何需要它的服务器使用。

这意味着所有配置文件对同一服务使用相同的 OAuth 凭据。如果你需要为不同项目使用不同账户，就需要在切换配置文件时撤销并重新授权。

有关授权服务器的详情，参见 [OAuth authentication](/manuals/ai/mcp-catalog-and-toolkit/toolkit.md#oauth-authentication)。

### 配置的持久化

配置文件的配置会持久保存在你的 Docker 安装中。重启 Docker Desktop 或系统后，你的配置文件、服务器和配置都会完好保留。

## 共享配置文件

配置文件可以作为制品推送到兼容 OCI 的注册表，从而与团队共享。这对于在组织内分发标准化的 MCP 设置很有用。出于安全原因，共享的配置文件中不包含凭据。团队成员在拉取后需单独配置 OAuth。

### 推送配置文件

1. 在 **Profiles** 选项卡中选择你要共享的配置文件。
2. 选择 **Push to Registry**。
3. 输入注册表目标地址（例如 `registry.example.com/profiles/web-dev:v1`）。
4. 如有需要，完成身份验证。

### 拉取配置文件

1. 在 **Profiles** 选项卡中选择 **Pull from Registry**。
2. 输入注册表引用（例如 `registry.example.com/profiles/team-standard:latest`）。
3. 如有需要，完成身份验证。

配置文件会被下载并添加到你的配置文件列表中。请单独配置所需的 OAuth 凭据。

### 团队协作工作流

在团队中共享配置文件的典型工作流：

1. 创建并配置一个包含团队所需服务器的配置文件。
2. 测试该配置文件，确保其按预期工作。
3. 使用版本标签将配置文件推送到团队的注册表（例如 `registry.example.com/profiles/team-dev:v1`）。
4. 与团队共享该注册表引用。
5. 团队成员拉取配置文件并配置所需的 OAuth 凭据。

这可确保每个人都使用相同的服务器集合和配置，减少设置时间和不一致性。

## 在客户端中使用配置文件

当你将 AI 客户端连接到 MCP Gateway 时，需指定该客户端可以访问哪个配置文件中的服务器。

### 使用配置文件运行网关

通过 MCP Toolkit 中的 **Clients** 部分将客户端连接到你的配置文件。你可以在创建配置文件时添加客户端，也可以稍后将其添加到现有配置文件中。

### 为特定配置文件配置客户端

手动设置客户端时，你可以指定该客户端使用哪个配置文件。这样不同的客户端就能连接到不同的配置文件。

例如，你的 Claude Desktop 配置可能使用：

```json
{
  "mcpServers": {
    "MCP_DOCKER": {
      "command": "docker",
      "args": ["mcp", "gateway", "run", "--profile", "claude-work"]
    }
  }
}
```

而你的 VS Code 配置使用另一个配置文件：

```json
{
  "mcp": {
    "servers": {
      "MCP_DOCKER": {
        "command": "docker",
        "args": ["mcp", "gateway", "run", "--profile", "vscode-dev"],
        "type": "stdio"
      }
    }
  }
}
```

### 在配置文件之间切换

要切换客户端使用的配置文件，请更新客户端配置，在 gateway 命令参数中指定不同的 `--profile` 值。

## 延伸阅读

- [开始使用 MCP Toolkit](/manuals/ai/mcp-catalog-and-toolkit/get-started.md)
- [从 CLI 使用 MCP Toolkit](/manuals/ai/mcp-catalog-and-toolkit/cli.md)
- [MCP Catalog](/manuals/ai/mcp-catalog-and-toolkit/catalog.md)
- [MCP Toolkit](/manuals/ai/mcp-catalog-and-toolkit/toolkit.md)

