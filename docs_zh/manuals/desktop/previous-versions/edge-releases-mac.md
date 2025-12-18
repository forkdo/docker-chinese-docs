---
description: 每个 Edge 版本的更新日志/发布说明
keywords: Docker Desktop for Mac, edge, 发布说明
title: Docker Desktop for Mac Edge 发布说明
toc_min: 1
toc_max: 2
aliases:
- /desktop/mac/release-notes/edge-releases/
sitemap: false
---

本文档包含 Docker Desktop Edge 版本的发布信息。Edge 版本为您提供最新功能的早期访问权限。请注意，其中一些功能可能处于实验阶段，部分功能可能永远不会到达 Stable 版本。

有关 Docker Desktop 系统要求的信息，请参阅
[安装前须知](/manuals/desktop/setup/install/mac-install.md#system-requirements)。

## Docker Desktop Community 2.5.4
2020-12-07

### 升级

- [Docker Engine 20.10.0-rc2](https://github.com/docker/docker-ce/blob/master/CHANGELOG.md#20100)
- [Go 1.15.6](https://github.com/golang/go/issues?q=milestone%3AGo1.15.6+label%3ACherryPickApproved+)

### Bug 修复和小改动

- 将菜单中的 «Update and quit» 改为 «Update and restart»。
- 修复检查更新对话框报告新版本的构建号而不是版本号的问题。
- 将内核降级到 [4.19.121](https://hub.docker.com/layers/docker/for-desktop-kernel/4.19.121-2a1dbedf3f998dac347c499808d7c7e029fbc4d3-amd64/images/sha256-4e7d94522be4f25f1fbb626d5a0142cbb6e785f37e437f6fd4285e64a199883a?context=repo) 以减少 hyperkit 的 CPU 使用率。修复 [docker/for-mac#5044](https://github.com/docker/for-mac/issues/5044)
- 修复 DNS 在名称存在但未找到记录类型时返回 `NXDOMAIN` 的问题。修复 [docker/for-mac#5020](https://github.com/docker/for-mac/issues/5020)。相关：https://gitlab.alpinelinux.org/alpine/aports/-/issues/11879
- 使用 `osxfs` 时避免缓存错误的文件大小和模式。修复 [docker/for-mac#5045](https://github.com/docker/for-mac/issues/5045)。

## Docker Desktop Community 2.5.3
2020-11-30

### 新增

- [Compose CLI v1.0.3](https://github.com/docker/compose-cli/releases/tag/v1.0.3)

### Bug 修复和小改动

- 修复了文件共享错误，当文件在主机上被修改时，文件在容器中可能显示为错误大小。这是 [docker/for-mac#4999](https://github.com/docker/for-mac/issues/4999) 的部分修复。
- 移除不必要的日志消息，这些消息会降低文件系统事件注入的速度。

## Docker Desktop Community 2.5.2
2020-11-26

### 新增

- 开始使用三位数字版本号。
- 从 Docker Desktop 2.5.2 开始，更新将通过增量补丁应用，因此更新包会小得多。

### Bug 修复和小改动

- 重新启用实验性 SOCKS 代理。修复 [docker/for-mac#5048](https://github.com/docker/for-mac/issues/5048)。
- 修复尝试使用 `-v /var/run/docker.sock:` 启动不存在的容器时出现的意外 EOF 错误。参见 [docker/for-mac#5025](https://github.com/docker/for-mac/issues/5025)。
- 当应用程序需要在特定目录上获得写入权限时，显示错误消息而不是崩溃。参见 [docker/for-mac#5068](https://github.com/docker/for-mac/issues/5068)

## Docker Desktop Community 2.5.1.0
2020-11-18

此版本包含 Kubernetes 升级。注意，安装 Docker Desktop 后，您的本地 Kubernetes 集群将被重置。

### 升级

- [Docker Engine 20.10.0-rc1](https://github.com/docker/docker-ce/blob/master/CHANGELOG.md#20100)
- [Compose CLI v1.0.2](https://github.com/docker/compose-cli/releases/tag/v1.0.2)
- [Snyk v1.424.4](https://github.com/snyk/snyk/releases/tag/v1.424.4)
- [Kubernetes 1.19.3](https://github.com/kubernetes/kubernetes/releases/tag/v1.19.3)

### Bug 修复和小改动

- 将 'Run Diagnostics' 重命名为 'Get support'。
- 修复了在 MacOS 11.0 (Big Sur) 上安装 VirtualBox 时 Docker Desktop 崩溃的问题。参见 [docker/for-mac#4997](https://github.com/docker/for-mac/issues/4997)。
- 移除 BlueStacks 警告消息。修复 [docker/for-mac#4863](https://github.com/docker/for-mac/issues/4863)。
- 在共享卷包含大量文件的情况下，提高容器启动速度。修复 [docker/for-mac#4957](https://github.com/docker/for-mac/issues/4957)。
- 文件共享：修复更改只读文件的所有权。修复 [docker/for-mac#4989](https://github.com/docker/for-mac/issues/4989)、[docker/for-mac#4964](https://github.com/docker/for-mac/issues/4964)。
- 修复尝试启动不存在的容器时出现的意外 EOF 错误。参见 [docker/for-mac#5025](https://github.com/docker/for-mac/issues/5025)。

## Docker Desktop Community 2.4.2.0
2020-10-19

### 新增

- 如果您在 Docker Hub 中启用了 [漏洞扫描](/docker-hub/repos/manage/vulnerability-scanning/)，扫描结果现在将显示在 Docker Desktop 中。

### 升级

- [Docker Engine 20.10.0 beta1](https://github.com/docker/docker-ce/blob/0fc7084265b3786a5867ec311d3f916af7bf7a23/CHANGELOG.md)
- [Docker Compose CLI - 0.1.22](https://github.com/docker/compose-cli/releases/tag/v0.1.22)
- [Linux kernel 5.4.39](https://hub.docker.com/layers/linuxkit/kernel/5.4.39-f39f83d0d475b274938c86eaa796022bfc7063d2/images/sha256-8614670219aca0bb276d4749e479591b60cd348abc770ac9ecd09ee4c1575405?context=explore)。
- [Kubernetes 1.19.2](https://github.com/kubernetes/kubernetes/releases/tag/v1.19.2)
- [Go 1.15.2](https://github.com/golang/go/issues?q=milestone:Go1.15.2+label:CherryPickApproved)

### Bug 修复和小改动

- 共享 Linux 目录（`/var`、`/bin` 等）到容器时，Docker Desktop 会避免监视主机文件系统中的路径。
- 共享文件到容器时（例如 `docker run -v ~/.gitconfig`），Docker Desktop 不会监视父目录。修复 [docker/for-mac#4981](https://github.com/docker/for-mac/issues/4981)。
- gRPC FUSE：修复只读文件的 `chown`。修复 `rabbitmq`，参见 [docker/for-mac#4964](https://github.com/docker/for-mac/issues/4964)。
- gRPC FUSE：除了 `MODIFY` 外，还生成 `ATTRIB` inotify 事件。修复 [docker/for-mac#4962](https://github.com/docker/for-mac/issues/4962)。
- gRPC FUSE：对不支持的模式返回 `EOPNOTSUPP`。修复 `minio`。参见 [docker/for-mac#4964](https://github.com/docker/for-mac/issues/4964)。
- 修复 NFS 挂载相关问题。参见 [docker/for-mac#4958](https://github.com/docker/for-mac/issues/4958)。
- 容器启动时始终同步刷新文件系统缓存。参见 [docker/for-mac#4943](https://github.com/docker/for-mac/issues/4943)。
- 允许符号链接指向共享卷外部。修复 [docker/for-mac#4862](https://github.com/docker/for-mac/issues/4862)。
- 诊断：当 Kubernetes 处于损坏状态时避免挂起。
- 修复自动登录启动。参见 [docker/for-mac#4877](https://github.com/docker/for-mac/issues/4877) 和 [docker/for-mac#4890](https://github.com/docker/for-mac/issues/4890)。

## Docker Desktop Community 2.4.1.0
2020-10-01

### 升级

- [Docker Compose CLI - 0.1.18](https://github.com/docker/compose-cli)
- [Docker Compose 1.27.4](https://github.com/docker/compose/releases/tag/1.27.4)
- [Snyk v1.399.1](https://github.com/snyk/snyk/releases/tag/v1.399.1)
- [Docker Engine 19.03.13](https://github.com/docker/docker-ce/releases/tag/v19.03.13)

### Bug 修复和小改动

- Docker Desktop 在容器启动时始终同步刷新文件系统缓存。参见 [docker/for-mac#4943](https://github.com/docker/for-mac/issues/4943)。
- Docker Desktop 现在支持在共享文件系统上调用 `chmod(2)` 时使用 `S_ISUID`、`S_ISGID` 和 `S_ISVTX`。参见 [docker/for-mac#4943](https://github.com/docker/for-mac/issues/4943)。
- 修复使用 `gRPC-FUSE` 时可能发生的过早文件句柄关闭问题。

## Docker Desktop Community 2.3.7.0
2020-09-17

### 新增

- [Amazon ECR Credential Helper](https://github.com/awslabs/amazon-ecr-credential-helper/releases/tag/v0.4.0)

### 升级

- [Docker ACI integration 0.1.15](https://github.com/docker/aci-integration-beta/releases/tag/v0.1.15)
- [Snyk v0.393.0](https://github.com/snyk/snyk/releases/tag/v1.393.0)

### Bug 修复和小改动

- 修复自动登录启动。参见 [docker/for-mac#4877](https://github.com/docker/for-mac/issues/4877) 和 [docker/for-mac#4890](https://github.com/docker/for-mac/issues/4890)。
- Docker Desktop 现在允许符号链接指向共享卷外部。修复 [docker/for-mac#4862](https://github.com/docker/for-mac/issues/4862)。
- 移除人工文件描述符限制（`setrlimit`）`10240`。Docker Desktop 现在依赖内核通过 `kern.maxfiles` 和 `kern.maxfilesperproc` 施加限制。
- 修复用于低级调试的 VM 调试 shell。
- 修复与 Go 1.15 客户端的兼容性。参见 [docker/for-mac#4855](https://github.com/docker/for-mac/issues/4855)。
- 避免在 `docker container inspect` 和 `docker volume inspect` 中暴露 `/host_mnt` 路径。修复 [docker/for-mac#4859](https://github.com/docker/for-mac/issues/4859)。
- 修复重负载下容器日志滞后问题。参见 [docker/for-win#8216](https://github.com/docker/for-win/issues/8216)。

### 已知问题

- `clock_gettime64` 系统调用在 i386 镜像中返回 `EPERM` 而不是 `ENOSYS`。
解决方法是使用 `--privileged` 标志禁用 `seccomp`。参见 [docker/for-win#8326](https://github.com/docker/for-win/issues/8326)。

## Docker Desktop Community 2.3.6.1
2020-09-08

### 升级

- [Docker Compose 1.27.0](https://github.com/docker/compose/releases/tag/1.27.0)

### Bug 修复和小改动

-  Docker Desktop 现在在 UI 中正确显示 "Use gRPC FUSE for file sharing" 的状态。修复 [docker/for-mac#4864](https://github.com/docker/for-mac/issues/4864)。

## Docker Desktop Community 2.3.6.0
2020-09-01

### 新增

- 与 Snyk 合作，Docker Desktop 现在支持对本地 Docker 镜像进行漏洞扫描。
- Docker ECS 插件已被 ECS 云集成取代
- Docker UI：
  - 镜像视图现在具有搜索和筛选选项。
  - 您现在可以使用远程仓库下拉菜单将镜像推送到 Docker Hub。
- WSL 2 文件和目录现在可以从 Windows Docker CLI 挂载，例如 `docker run -v \\wsl$\Ubuntu\my-files:/my-files ...`。

### 移除

- macOS 10.13 的支持已结束，您需要更新系统以继续使用 Docker Desktop。

### 升级

- [Alpine 3.12](https://alpinelinux.org/posts/Alpine-3.12.0-released.html)
- [Kubernetes 1.18.8](https://github.com/kubernetes/kubernetes/releases/tag/v1.18.8)

### Bug 修复和小改动

- 通过从 `hyperkit` 中移除串行控制台修复了 Mac CPU 使用率问题，参见 [docker/roadmap#12]( https://github.com/docker/roadmap/issues/12#issuecomment-663163280)。要在 VM 中打开 shell，请使用 `nc -U ~/Library/Containers/com.docker.docker/Data/debug-shell.sock`（在 Mac 上）或 `putty -serial \\.\pipe\dockerDebugShell`（在 Windows 上）。

## Docker Desktop Community 2.3.5.0
2020-08-21

### 新增

- Docker Desktop 仪表板的 **Images** 视图现在允许您与 Docker Hub 上的镜像交互。您可以从 Docker Hub 拉取具有特定标签的远程仓库，或查看仓库在 Docker Hub 页面上的详细信息。要访问新的 Images 视图，请从 Docker 菜单中选择 **Dashboard** > **Images**。

- Docker Desktop 现在默认启用 BuildKit，但需要重置为出厂设置后生效。要恢复到旧的 docker build 体验，请转到 **Preferences** > **Docker Engine** 然后禁用 BuildKit 功能。

- Docker Desktop 现在默认使用 **gRPC-FUSE** 进行文件共享。这具有更快的文件共享速度并使用更少的 CPU，特别是当主机上有大量文件事件时。要切换回 `osxfs`，请转到 **Preferences** > **General** 并禁用 gRPC-FUSE。

### 升级

- [Go 1.14.7](https://github.com/golang/go/issues?q=milestone:Go1.14.7+label:CherryPickApproved)
- [Docker ECS integration v1.0.0-beta.5](https://github.com/docker/ecs-plugin/releases/tag/v1.0.0-beta.5)
- [Docker Engine 19.03.13-beta2](https://github.com/docker/docker-ce/releases/tag/v19.03.13-beta2)
- [Docker ACI integration 0.1.12](https://github.com/docker/aci-integration-beta/releases/tag/v0.1.12)

### 移除

- 我们最近在 Edge 版本中试验的 Mutagen 文件同步功能已被移除。感谢所有提供反馈的用户。我们正在基于收到的反馈重新考虑如何集成它。

### Bug 修复和小改动

- 