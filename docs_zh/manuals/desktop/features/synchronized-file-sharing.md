---
title: 同步文件共享
weight: 70
description: 了解如何在 Docker Desktop 中使用同步文件共享。
keyword: mutagen, file sharing, docker desktop, bind mounts
aliases:
- /desktop/synchronized-file-sharing/
---

{{< summary-bar feature_name="Synchronized file sharing" >}}

同步文件共享（Synchronized file shares）是一种替代性的文件共享机制，它提供了快速且灵活的主机到虚拟机（VM）文件共享功能，通过使用同步的文件系统缓存来增强绑定挂载（bind mount）的性能。

![同步文件共享窗格图像](../images/synched-file-shares.webp)
 
## 适用人群

同步文件共享非常适合以下开发者：
- 拥有大型代码库或单体仓库（monorepo），其中包含 100,000 个或更多文件，总大小达数百兆字节甚至数千兆字节。
- 正在使用虚拟文件系统（如 VirtioFS、gRPC FUSE 和 osxfs），而这些系统已无法很好地扩展以适应其代码库。
- 经常遇到性能限制。
- 不希望担心文件所有权问题，或在修改多个容器时花费时间解决冲突的文件所有权信息。

## 同步文件共享如何工作？

同步文件共享的行为类似于虚拟文件共享，但它利用了一个高性能、低延迟的代码同步引擎，在 Docker Desktop VM 内的 ext4 文件系统上创建主机文件的同步缓存。如果您在主机或 VM 的容器中进行文件系统更改，这些更改将通过双向同步进行传播。

创建文件共享实例后，任何使用绑定挂载的容器，只要其挂载路径指向主机文件系统上与指定同步文件共享位置匹配的位置或其子目录，都将利用同步文件共享功能。不满足此条件的绑定挂载将传递给正常的虚拟文件系统[绑定挂载机制](/manuals/engine/storage/bind-mounts.md)，例如 VirtioFS 或 gRPC-FUSE。

> [!NOTE]
>
> Docker Desktop 中的 Kubernetes `hostPath` 卷不使用同步文件共享。

> [!IMPORTANT]
>
> 同步文件共享在 WSL 上或使用 Windows 容器时不可用。

## 创建文件共享实例

要创建文件共享实例：
1. 登录 Docker Desktop。
2. 在**设置（Settings）**中，导航到**资源（Resources）**部分的**文件共享（File sharing）**选项卡。
3. 在**同步文件共享（Synchronized file shares）**部分，选择**创建共享（Create share）**。
4. 选择要共享的主机文件夹。同步文件共享将初始化并可供使用。

文件共享需要几秒钟时间来初始化，因为文件会被复制到 Docker Desktop VM 中。在此期间，状态指示器显示**正在准备（Preparing）**。Docker Desktop 仪表板的页脚还有一个状态图标，会持续更新您的状态。

当状态指示器显示**正在监视文件系统更改（Watching for filesystem changes）**时，您的文件即可通过所有标准绑定挂载机制供 VM 使用，无论是命令行中的 `-v` 还是在 `compose.yml` 文件中指定的挂载。

> [!NOTE]
>
> 创建新服务时，将[绑定挂载选项一致性](/reference/cli/docker/service/create.md#options-for-bind-mounts)设置为 `:consistent` 会绕过同步文件共享。

> [!TIP]
>
> Docker Compose 可以自动为绑定挂载创建文件共享。
> 确保您已使用付费订阅登录 Docker，并在 Docker Desktop 设置中同时启用了**访问实验性功能（Access experimental features）**和**使用 Compose 管理同步文件共享（Manage Synchronized file shares with Compose）**。

## 探索您的文件共享实例

**同步文件共享（Synchronized file shares）**部分会显示您所有的文件共享实例，并提供有关每个实例的有用信息，包括：
- 文件共享内容的来源
- 状态更新
- 每个文件共享使用的空间量
- 文件系统条目数
- 符号链接数
- 哪个容器正在使用该文件共享实例

选择一个文件共享实例会展开下拉菜单并显示此信息。

## 使用 `.syncignore`

您可以在每个文件共享的根目录下使用 `.syncignore` 文件，以从文件共享实例中排除本地文件。它支持与 `.dockerignore` 文件相同的语法，用于排除和/或重新包含同步的路径。`.syncignore` 文件在文件共享根目录以外的任何位置都会被忽略。

您可能希望添加到 `.syncignore` 文件中的一些示例包括：
- 大型依赖目录，例如 `node_modules` 和 `composer` 目录（除非您依赖通过绑定挂载访问它们）
- `.git` 目录（同样，除非您需要它们）

通常，使用 `.syncignore` 文件来排除对您的工作流程不关键的项目，特别是那些同步速度慢或占用大量存储空间的项目。

## 已知问题

- 对 `.syncignore` 的更改不会导致立即删除文件，除非重新创建文件共享。换句话说，由于修改 `.syncignore` 文件而新被忽略的文件仍保留在其当前位置，但在同步期间不再更新。

- 文件共享实例目前限制为每个共享约 200 万个文件。为了获得最佳性能，如果您有如此大小的文件共享实例，请尝试将其分解为多个对应于单个绑定挂载位置的共享。

- 由于 Linux 区分大小写而 macOS/Windows 仅保留大小写，因此大小写冲突会在 GUI 中显示为**文件已存在（File exists）**问题。这些可以忽略。但是，如果问题持续存在，您可以报告该问题。

- 同步文件共享会主动报告临时问题，这可能导致在同步期间 GUI 中偶尔出现**冲突（Conflict）**和**问题（Problem）**指示器。这些可以忽略。但是，如果问题持续存在，您可以报告该问题。

- 如果您从 Windows 上的 WSL2 切换到 Hyper-V，则需要完全重启 Docker Desktop。

- 不支持 POSIX 风格的 Windows 路径。避免在 Docker Compose 中设置 [`COMPOSE_CONVERT_WINDOWS_PATHS`](/manuals/compose/how-tos/environment-variables/envvars.md#compose_convert_windows_paths) 环境变量。

- 如果您没有创建符号链接的正确权限，并且您的容器尝试在您的文件共享实例中创建符号链接，则会显示**无法创建符号链接（unable to create symbolic link）**错误消息。对于 Windows 用户，请参阅 Microsoft 的[创建符号链接文档](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/security-policy-settings/create-symbolic-links)以获取最佳实践和**创建符号链接（Create symbolic links）**安全策略设置的位置。对于 Mac 和 Linux 用户，请检查您是否对该文件夹具有写权限。