# Gordon




Gordon 是一个 AI 驱动的助手，可对你的 Docker 工作流采取行动。它会分析你的环境、提出解决方案，并在你许可的情况下执行命令。

## Gordon 能做什么

Gordon 会采取行动来帮助你完成 Docker 任务：

- 解释 Docker 概念和命令
- 搜索 Docker 文档和网络资源以寻找解决方案
- 遵循最佳实践编写和修改 Dockerfile
- 通过阅读日志并提议修复来调试容器故障
- 管理容器、镜像、卷和网络

Gordon 在执行每项操作之前都会先提出方案，由你批准。

## 在哪里使用 Gordon

Gordon 在四个入口可用：

- 从 Docker Desktop 侧边栏打开 Gordon 视图，在获得你批准的情况下运行 Docker 命令。请参阅 [在 Docker Desktop 中使用 Gordon](./how-to/docker-desktop.md)。
- 在终端中运行 `docker ai`，从命令行使用完整的助手。请参阅 [通过 CLI 使用 Gordon](./how-to/cli.md)。
- 在 [hub.docker.com](https://hub.docker.com) 任意仓库页面选择 Gordon 图标，询问该仓库的镜像、标签和元数据。可移交到 Docker Desktop 以执行操作。
- 在 [docs.docker.com](https://docs.docker.com) 任意页面选择 Gordon 图标，向 Docker 提问。

Docker Desktop 和 CLI 会计入你 Gordon 套餐的[用量限制](./usage-limits.md)。Docker Hub 和 docs.docker.com 上的 Gordon 是免费的，不需要 Docker 账户或安装 Docker Desktop。它有自己的共享公共用量限制，并且不访问你的 Docker 环境。

## 开始使用

### 先决条件

在开始之前：

- Docker Desktop 4.74 或更高版本
- 登录你的 Docker 账户

> [!NOTE]
> Gordon 默认对已登录的 Docker 用户启用。如果你的账户属于拥有 Business 订阅的组织，访问还需两个额外步骤：
>
> 1. 联系 Docker 支持为你的组织激活 Gordon。Docker 会在激活完成后确认。
> 2. 确认后，组织管理员必须通过 [设置管理](/manuals/enterprise/security/hardened-desktop/settings-management/_index.md) 开启 Gordon。将 **Enable Gordon** 设置为 **Enabled** 或 **Always enabled**。请确保所有设置管理先决条件都已满足，以使该设置对 Docker Desktop 客户端生效。

### 快速开始

**Docker Desktop**



1. 打开 Docker Desktop。
2. 在侧边栏中选择 **Gordon**。
3. 选择你的项目目录。
4. 输入一个问题："What containers are running?"（正在运行哪些容器？）

   ![Gordon 在 Docker Desktop 中运行](./images/gordon_gui.avif)

5. 查看 Gordon 提议的操作并批准。

**CLI**



1. 打开终端并运行：

   ```console
   $ docker ai
   ```

   这将打开 Gordon 的终端用户界面 (TUI)。

2. 输入一个问题："what containers are running?"（正在运行哪些容器？），然后按 <kbd>Enter</kbd>。

   ![Gordon 在终端中运行](./images/gordon_tui.avif)

3. 查看 Gordon 提议的操作并输入 `y` 批准。



### 权限

默认情况下，Gordon 在执行操作前会请求批准。你可以批准单个操作，或允许当前会话的所有操作。

![Gordon 权限请求](./images/gordon_permissions_prompt.avif)

权限在每个会话都会重置。要配置默认权限或启用自动批准模式，请参阅 [权限](./how-to/permissions.md)。

### 试试这些示例

检查容器：

```console
$ docker ai "show me logs from my nginx container"
```

审查 Dockerfile：

```console
$ docker ai "review my Dockerfile for best practices"
```

管理镜像：

```console
$ docker ai "list my local images and their sizes"
```

