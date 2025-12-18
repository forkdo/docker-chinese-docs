---
title: 同步文件共享
weight: 70
description: 在 Docker Desktop 上开始使用同步文件共享。
keyword: mutagen, file sharing, docker desktop, bind mounts
aliases:
- /desktop/synchronized-file-sharing/
---

{{< summary-bar feature_name="同步文件共享" >}}

同步文件共享是一种替代的文件共享机制，通过使用同步文件系统缓存，提供快速灵活的主机到虚拟机文件共享，从而提升绑定挂载的性能。

![同步文件共享窗格示意图](../images/synched-file-shares.webp)

## 适用人群？

同步文件共享非常适合以下开发者：
- 拥有大型仓库或单体仓库，包含 100,000 个或更多文件，总计数百 MB 甚至数 GB。
- 正在使用虚拟文件系统（如 VirtioFS、gRPC FUSE 和 osxfs），但这些系统已无法很好地适应其代码库规模。
- 经常遇到性能限制。
- 不想担心文件所有权，或在修改多个容器时花费时间解决文件所有权冲突。

## 工作原理？

同步文件共享的行为与虚拟文件共享完全相同，但利用高性能、低延迟的代码同步引擎，在 Docker Desktop 虚拟机内的 ext4 文件系统上创建主机文件的同步缓存。如果您在主机或虚拟机容器中进行文件系统更改，它会通过双向同步进行传播。

创建文件共享实例后，任何使用绑定挂载的容器，只要其挂载点指向主机文件系统上的位置与指定的同步文件共享位置匹配（或为其子目录），就会利用同步文件共享功能。不满足此条件的绑定挂载将传递给正常的虚拟文件系统[绑定挂载机制](/manuals/engine/storage/bind-mounts.md)，例如 VirtioFS 或 gRPC-FUSE。

> [!NOTE]
>
> Docker Desktop 中 Kubernetes 的 `hostPath` 卷不使用同步文件共享。

> [!IMPORTANT]
>
> 同步文件共享在 WSL 或使用 Windows 容器时不可用。

## 创建文件共享实例

要创建文件共享实例：
1. 登录 Docker Desktop。
2. 在 **设置** 中，导航到 **资源** 部分的 **文件共享** 选项卡。
3. 在 **同步文件共享** 部分，选择 **创建共享**。
4. 选择要共享的主机文件夹。同步文件共享应初始化并可使用。

文件共享需要几秒钟初始化，因为文件需要复制到 Docker Desktop 虚拟机中。在此期间，状态指示器显示 **准备中**。Docker Desktop 仪表板的页脚中也有一个状态图标，持续更新状态。

当状态指示器显示 **监视文件系统更改** 时，您的文件已可通过所有标准绑定挂载机制供虚拟机使用，无论是命令行中的 `-v` 还是 `compose.yml` 文件中的指定。

> [!NOTE]
>
> 创建新服务时，将[绑定挂载选项 consistency](/reference/cli/docker/service/create.md#options-for-bind-mounts) 设置为 `:consistent` 会绕过同步文件共享。

> [!TIP]
>
> Docker Compose 可以自动为绑定挂载创建文件共享。
> 确保您已使用付费订阅登录 Docker，并在 Docker Desktop 设置中启用了 **访问实验性功能** 和 **使用 Compose 管理同步文件共享**。

## 探索您的文件共享实例

**同步文件共享** 部分显示所有文件共享实例，并提供每个实例的有用信息，包括：
- 文件共享内容的来源
- 状态更新
- 每个文件共享使用的空间
- 文件系统条目数量
- 符号链接数量
- 使用该文件共享实例的容器

选择文件共享实例会展开下拉菜单并显示这些信息。

## 使用 `.syncignore`

您可以在每个文件共享的根目录使用 `.syncignore` 文件，排除本地文件不包含在文件共享实例中。它支持与 `.dockerignore` 文件相同的语法，排除和/或重新包含路径进行同步。`.syncignore` 文件仅在文件共享根目录有效，其他位置会被忽略。

您可能想要添加到 `.syncignore` 文件中的一些示例包括：
- 大型依赖目录，例如 `node_modules` 和 `composer` 目录（除非您依赖通过绑定挂载访问它们）
- `.git` 目录（同样，除非您需要它们）

通常，使用您的 `.syncignore` 文件排除对工作流不关键的项目，特别是那些同步缓慢或占用大量存储的项目。

## 已知问题

- 对 `.syncignore` 的更改不会立即导致删除，除非重新创建文件共享。换句话说，由于 `.syncignore` 文件修改而新忽略的文件仍保留在当前位置，但在同步期间不再更新。

- 文件共享实例目前限制为每个共享约 200 万个文件。为了获得最佳性能，如果您有此规模的文件共享实例，请尝试将其分解为对应单个绑定挂载位置的多个共享。

- 由于 Linux 区分大小写而 macOS/Windows 仅大小写保持，大小写冲突在 GUI 中显示为 **文件已存在** 问题。这些可以忽略。但如果持续出现，您可以报告问题。

- 同步文件共享会主动报告临时问题，这可能导致同步期间 GUI 中偶尔出现 **冲突** 和 **问题** 指示器。这些可以忽略。但如果持续出现，您可以报告问题。

- 如果您在 Windows 上从 WSL2 切换到 Hyper-V，Docker Desktop 需要完全重启。

- 不支持 POSIX 风格的 Windows 路径。避免在 Docker Compose 中设置 [`COMPOSE_CONVERT_WINDOWS_PATHS`](/manuals/compose/how-tos/environment-variables/envvars.md#compose_convert_windows_paths) 环境变量。

- 如果您没有创建符号链接的正确权限，而您的容器尝试在文件共享实例中创建符号链接，会显示 **无法创建符号链接** 错误消息。对于 Windows 用户，请参阅 Microsoft 的[创建符号链接文档](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/security-policy-settings/create-symbolic-links)了解最佳实践和 **创建符号链接** 安全策略设置的位置。对于 Mac 和 Linux 用户，请检查您是否对文件夹具有写权限。