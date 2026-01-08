# 
description: Change log / release notes for Docker Desktop for Mac 3.x
title: Docker Desktop for Mac 3.x release notes
toc_min: 1
toc_max: 2
sitemap: false
keywords: Docker Desktop for Mac 3.x release notes
aliases:
  - /desktop/mac/previous-versions/
  - /docker-for-mac/previous-versions/
  - /desktop/mac/release-notes/3.x/---
description: Docker Desktop for Mac 3.x 的变更日志 / 发布说明
title: Docker Desktop for Mac 3.x 发布说明
toc_min: 1
toc_max: 2
sitemap: false---
本页包含 Docker Desktop for Mac 3.x 的发布说明。

## Docker Desktop 3.6.0
2021-08-11

### 新功能

- **开发环境 (Dev Environments)**：现在可以从本地 Git 仓库创建开发环境。
- **卷管理 (Volume Management)**：现在可以按名称、创建日期和卷的大小对卷进行排序。还可以使用 **搜索** 字段搜索特定的卷。更多信息，请参阅 [探索卷](../use-desktop/volumes.md)。

### 升级

- [Compose V2 RC1](https://github.com/docker/compose-cli/releases/tag/v2.0.0-rc.1)
  - Docker compose 命令行补全。
  - 允许设置 0 个规模/副本。
  - 在 `logs --follow` 时检测新容器。
- [Go 1.16.7](https://github.com/golang/go/releases/tag/go1.16.7)
- [Docker Engine 20.10.8](/manuals/engine/release-notes/20.10.md#20108)
- [containerd v1.4.9](https://github.com/containerd/containerd/releases/tag/v1.4.9)
- [runc v1.0.1](https://github.com/opencontainers/runc/releases/tag/v1.0.1)
- [Kubernetes 1.21.3](https://github.com/kubernetes/kubernetes/releases/tag/v1.21.3)
- [Linux kernel 5.10.47](https://hub.docker.com/layers/docker/for-desktop-kernel/5.10.47-0b705d955f5e283f62583c4e227d64a7924c138f/images/sha256-a4c79bc185ec9eba48dcc802a8881b9d97e532b3f803d23e5b8d4951588f4d51?context=repo)

### Bug 修复和细微变更

- 更新内核配置以修复 [Docker Desktop 3.0.0](#docker-desktop-300) 中的性能回归问题，该问题导致发布容器端口的时间比旧版本长 10 倍。更多信息，请参阅 [linuxkit/linuxkit#3701](https://github.com/linuxkit/linuxkit/pull/3701) 和 [docker/for-mac#5668](https://github.com/docker/for-mac/issues/5668)。
- 修复了 DNS 服务器在接收到意外的大数据报文后会失败的 Bug。
- 修复了与硬件加速相关的问题 [docker/for-mac#5121](https://github.com/docker/for-mac/issues/5121)
- 修复了 Mac 上“跳过此更新”相关的问题 [docker/for-mac#5842](https://github.com/docker/for-mac/issues/5842)

## Docker Desktop 3.5.2
2021-07-08

### 新功能

**开发环境预览 (Dev Environments Preview)**：开发环境使您能够与团队成员无缝协作，无需在 Git 分支之间切换即可将代码放到团队成员的机器上。使用开发环境时，只需单击一下即可与团队成员共享正在进行的工作，且无需处理任何合并冲突。

### 升级

- [Compose V2 beta 6](https://github.com/docker/compose-cli/releases/tag/v2.0.0-beta.6)
  - `compose run` 和 `compose exec` 命令对 stdout 和 stderr 使用单独的流。请参阅 [docker/compose-cli#1873](https://github.com/docker/compose-cli/issues/1873)。
  - `compose run` 和 `compose exec` 命令支持分离键。修复了 [docker/compose-cli#1709](https://github.com/docker/compose-cli/issues/1709)。
  - 修复了 `compose rm` 命令上的 `--force` 和 `--volumes` 标志。请参阅 [docker/compose-cli#1844](https://github.com/docker/compose-cli/issues/1844)。
  - 修复了网络的 IPAM 配置。服务可以定义固定 IP。修复了 [docker/compose-cli#1678](https://github.com/docker/compose-cli/issues/1678) 和 [docker/compose-cli#1816](https://github.com/docker/compose-cli/issues/1816)。
- 开发环境
  - 支持 VS Code Insiders。
  - 允许用户在克隆项目时指定分支。

### Bug 修复和细微变更

- 开发环境：修复了在某些创建和删除场景中出现的空白屏幕。修复了 [dev-environments#4](https://github.com/docker/dev-environments/issues/4)
- 开发环境：修复了删除环境时的错误处理。修复了 [dev-environments#8](https://github.com/docker/dev-environments/issues/8)
- 开发环境：在环境正在创建或删除时，**启动**、**停止**和**共享**按钮被禁用。
- 修复了在使用 `virtualization.framework` 但不使用 `vpnkit` 时的连接泄漏问题。
- 修复了在 iptables 更新时出现的虚假跟踪。
- 修复了添加多个端口转发选项时的延迟。

## Docker Desktop 3.5.1
2021-06-25

### 新功能

**开发环境预览 (Dev Environments Preview)**：开发环境使您能够与团队成员无缝协作，无需在 Git 分支之间切换即可将代码放到团队成员的机器上。使用开发环境时，只需单击一下即可与团队成员共享正在进行的工作，且无需处理任何合并冲突。

**Compose V2 beta**：Docker Desktop 现在包含 Compose V2 的测试版，该版本支持作为 Docker CLI 一部分的 `docker compose` 命令。虽然 `docker-compose` 仍然受支持和维护，但 Compose V2 的实现直接依赖于作为规范一部分维护的 compose-go 绑定。Docker CLI 中的 compose 命令支持大多数 `docker-compose` 命令和标志。它有望成为 `docker-compose` 的直接替代品。还有一些标志尚未实现，请参阅 docker-compose 兼容性列表以了解新 compose 命令支持的标志。如果您在使用 Compose V2 时遇到任何问题，可以通过在 Docker Desktop **实验性** 设置中进行更改，或运行命令 `docker-compose disable-v2` 轻松切换回 Compose v1。请通过在 [Compose-CLI](https://github.com/docker/compose-cli/issues) GitHub 仓库中创建问题，让我们知道您对新 'compose' 命令的反馈。

### Bug 修复和细微变更

- 修复了指向提供有关 Docker 如何处理上传的诊断数据详细信息的策略的链接。修复了 [docker/for-mac#5741](https://github.com/docker/for-mac/issues/5741)

## Docker Desktop 3.5.0
2021-06-23

### 新功能

**开发环境预览 (Dev Environments Preview)**：开发环境使您能够与团队成员无缝协作，无需在 Git 分支之间切换即可将代码放到团队成员的机器上。使用开发环境时，只需单击一下即可与团队成员共享正在进行的工作，且无需处理任何合并冲突。

**Compose V2 beta**：Docker Desktop 现在包含 Compose V2 的测试版，该版本支持作为 Docker CLI 一部分的 `docker compose` 命令。虽然 `docker-compose` 仍然受支持和维护，但 Compose V2 的实现直接依赖于作为规范一部分维护的 compose-go 绑定。Docker CLI 中的 compose 命令支持大多数 `docker-compose` 命令和标志。它有望成为 `docker-compose` 的直接替代品。还有一些标志尚未实现，请参阅 docker-compose 兼容性列表以了解新 compose 命令支持的标志。如果您在使用 Compose V2 时遇到任何问题，可以通过在 Docker Desktop **实验性** 设置中进行更改，或运行命令 `docker-compose disable-v2` 轻松切换回 Compose v1。请通过在 [Compose-CLI](https://github.com/docker/compose-cli/issues) GitHub 仓库中创建问题，让我们知道您对新 'compose' 命令的反馈。

### 升级

- [Compose V2 beta](https://github.com/docker/compose-cli/releases/tag/v2.0.0-beta.4)
  - 修复了当文件绑定挂载到嵌套挂载点时容器无法启动的 Bug。修复了 [docker/compose-cli#1795](https://github.com/docker/compose-cli/issues/1795)。
  - 添加了对容器链接和外部链接的支持。
  - 引入了 `docker compose logs --since --until` 选项。
  - `docker compose config --profiles` 现在列出所有已定义的配置文件。
- 从 [Kubernetes 1.21.1](https://github.com/kubernetes/kubernetes/releases/tag/v1.21.1) 升级到 [Kubernetes 1.21.2](https://github.com/kubernetes/kubernetes/releases/tag/v1.21.2)

### Bug 修复和细微变更

- **卷管理 (Volume Management)**
  - 用户现在可以使用 Docker 仪表板删除卷内的文件或目录。
  - Docker 仪表板中的 **卷** 视图显示卷内内容的最后修改时间和大小。
  - 用户可以从 Docker 仪表板保存卷内的文件和目录。
- 修复了由于 `/usr/bin` 不在 `PATH` 中而导致 Docker 启动失败的 Bug。修复了 [docker/for-mac#5770](https://github.com/docker/for-mac/issues/5770)
- Docker Desktop 现在允许修改主机目录中的文件，该目录是容器中的嵌套挂载点。修复了 [docker/for-mac#5748](https://github.com/docker/for-mac/issues/5748)。
- 修复了设置迁移 Bug，该 Bug 导致 Docker Desktop 在升级到 3.4.0 后找不到镜像和容器数据。修复了 [docker/for-mac#5754](https://github.com/docker/for-mac/issues/5754)。
- Docker Desktop 现在在 Apple Silicon 上的 Docker 仪表板中突出显示非原生镜像的架构。
- 修复了在 macOS 12 (Monterey) 上使用 virtualization.framework 的问题。
- 默认的 `docker` CLI `context` 现在是 `desktop-linux`。
- 仅在单击 Docker 菜单时显示 Docker Desktop 反馈弹出窗口。

## Docker Desktop 3.4.0
2021-06-09

### 新功能

**卷管理 (Volume Management)**：Docker Desktop 用户现在可以使用 Docker 仪表板创建和删除卷，还可以查看正在使用的卷。更多信息，请参阅 [探索卷](../use-desktop/volumes.md)。

**Compose V2 beta**：Docker Desktop 现在包含 Compose V2 的测试版，该版本支持作为 Docker CLI 一部分的 `docker compose` 命令。虽然 `docker-compose` 仍然受支持和维护，但 Compose V2 的实现直接依赖于作为规范一部分维护的 compose-go 绑定。Docker CLI 中的 compose 命令支持大多数 `docker-compose` 命令和标志。它有望成为 `docker-compose` 的直接替代品。还有一些标志尚未实现，请参阅 docker-compose 兼容性列表以了解新 compose 命令支持的标志。如果您在使用 Compose V2 时遇到任何问题，可以通过在 Docker Desktop **实验性** 设置中进行更改，或运行命令 `docker-compose disable-v2` 轻松切换回 Compose v1。请通过在 [Compose-CLI](https://github.com/docker/compose-cli/issues) GitHub 仓库中创建问题，让我们知道您对新 'compose' 命令的反馈。

**跳过 Docker Desktop 更新**：所有用户现在在提示安装单个 Docker Desktop 版本时都可以跳过更新。

### 弃用

- Docker Desktop 不再安装 Notary。您现在可以使用 [Docker Content Trust](/manuals/engine/security/trust/_index.md) 进行镜像签名。

### 升级

- [Docker Engine 20.10.7](/manuals/engine/release-notes/20.10.md#20107)
- [Docker Compose 1.29.2](https://github.com/docker/compose/releases/tag/1.29.2)
- [Docker Hub Tool v0.4.1](https://github.com/docker/hub-tool/releases/tag/v0.4.1)
- [Compose CLI v1.0.16](https://github.com/docker/compose-cli/releases/tag/v1.0.16)
- [Kubernetes 1.21.1](https://github.com/kubernetes/kubernetes/releases/tag/v1.21.1)
- [containerd v1.4.6](https://github.com/containerd/containerd/releases/tag/v1.4.6)
- [runc v1.0.0-rc95](https://github.com/opencontainers/runc/releases/tag/v1.0.0-rc95)
- [Go 1.16.5](https://github.com/golang/go/releases/tag/go1.16.5)

### Bug 修复和细微变更

- 防止 `docker run` 在 inotify 事件注入失败时挂起。修复了 [docker/for-mac#5590](https://github.com/docker/for-mac/issues/5590)。
- 修复了 UI 中显示 stderr 日志的错误。修复了 [docker/for-mac#5688](https://github.com/docker/for-mac/issues/5688)。
- 修复了导致在 Docker Desktop 上 `riscv64` 仿真的问题。修复了 [docker/for-mac#5699](https://github.com/docker/for-mac/issues/5699)。
- 通过删除卷和构建缓存，在删除容器后自动回收空间。
- Docker Desktop 现在允许为 Docker 引擎配置空白的 HTTP 代理，这将完全禁用内部 HTTP 代理。请参阅 [docker/for-mac#2467](https://github.com/docker/for-mac/issues/2467)。
- 现在可以从 Docker Desktop 删除文件名不是 `docker-compose.yml` 的 Docker Compose 应用程序。修复了 [docker/for-win#11046](https://github.com/docker/for-win/issues/11046)
- Docker Desktop 现在在 Apple silicon 上暴露主机 CPU。修复了 [docker/for-mac#5681](https://github.com/docker/for-mac/issues/5681)。
- 避免在引擎重启后泄露绑定到特权端口和特定 IP 的开放端口。修复了 [docker/for-mac#5649](https://github.com/docker/for-mac/issues/5649)。
- 将 `vpnkit` 与 `virtualization.framework` 一起使用，以修复与 VPN 客户端（如 Cisco AnyConnect）的连接问题。
- 修复了更新对话框窗口中缺少版本号的问题。
- 修复了有时无法从 **支持** 对话框正确上传诊断数据的问题。
- 修复了在 VM IP 更改后 `*.docker.internal` 和 Kubernetes 集群重置的 DNS 条目。修复了 [docker/for-mac#5707](https://github.com/docker/for-mac/issues/5707)、[docker/for-mac#5680](https://github.com/docker/for-mac/issues/5680)、[docker/for-mac#5663](https://github.com/docker/for-mac/issues/5663) 和 [docker/for-mac#5653](https://github.com/docker/for-mac/issues/5653)。
- 在启用 gRPC FUSE 时避免运行 `com.docker.osxfs`。修复了 [docker/for-mac#5725](https://github.com/docker/for-mac/issues/5725)。

### 已知问题

- 在 Apple Silicon 的原生 `arm64` 容器中，`debian:buster`、`ubuntu:20.04` 和 `centos:8` 中的旧版本 `libssl` 在连接到某些 TLS 服务器时（例如 `curl https://dl.yarnpkg.com`）会出现段错误。该 Bug 已在 `debian:bullseye`、`ubuntu:21.04` 和 `fedora:35` 的新版本 `libssl` 中修复。

## Docker Desktop 3.3.3
2021-05-06

### 升级

- [Snyk v1.563.0](https://github.com/snyk/snyk/releases/tag/v1.563.0)
- [Docker Scan v0.8.0](https://github.com/docker/scan-cli-plugin/releases/tag/v0.8.0)

### Bug 修复和细微变更

- 修复了从故障排除屏幕上传诊断数据失败的问题。

### Docker Desktop 3.3.2
2021-05-03

### 升级

- [Compose CLI v1.0.14](https://github.com/docker/compose-cli/tree/v1.0.14)
- [Go 1.16.3](https://golang.org/doc/go1.16)
- [Docker Compose 1.29.1](https://github.com/docker/compose/releases/tag/1.29.1)
- [Docker Engine 20.10.6](/manuals/engine/release-notes/20.10.md#20106)

### Bug 修复和细微变更

- 修复了 Apple 芯片上的一个 Bug，该 Bug 导致网络传输中的最后一个字节偶尔丢失。
- 修复了引擎 `daemon.json` 中定义的 `metrics-port` 阻止应用程序重启的 Bug。
- 修复了临时端口泄漏问题。修复了 [docker/for-mac#5611](https://github.com/docker/for-mac/issues/5611)。
- 在 Apple 芯片上使用 `qemu` 模拟更现代的 Intel CPU，以获得更好的镜像兼容性。请参阅 [docker/for-mac#5561](https://github.com/docker/for-mac/issues/5561)。
- 默认启用 buildkit 垃圾回收。
- 修复了阻止绑定到端口 123 的 Bug。修复了 [docker/for-mac#5589](https://github.com/docker/for-mac/issues/5589)。
- 当没有设置上游代理时，禁用 HTTP 和 HTTPS 透明代理。修复了 [docker/for-mac#5572](https://github.com/docker/for-mac/issues/5572)。
- 恢复到 3.2.2 中使用的 HTTP 和 HTTPS 代理实现。
- 删除了“默认将 Docker Stacks 部署到 Kubernetes”的 Kubernetes 设置。该组件在 2.4.0.0 中已被移除，但我们忘记了删除该设置。修复了 [docker/for-mac#4966](https://github.com/docker/for-mac/issues/4966)。

## Docker Desktop 3.3.1
2021-04-15

### 新功能

Docker Desktop 现在可用于 Apple silicon 和 Intel 芯片。这使开发人员可以选择本地开发环境，并扩展了基于 ARM 的应用程序的开发管道。更多信息，请参阅 [适用于 Apple silicon 的 Docker Desktop](/manuals/desktop/setup/install/mac-install.md)。

### Bug 修复和细微变更

- Docker Desktop 现在确保 `/dev/null` 和其他设备的权限在 `--privileged` 容器内正确设置为 `0666` (`rw-rw-rw-`)。修复了 [docker/for-mac#5527](https://github.com/docker/for-mac/issues/5527)
- 修复了当 Docker Desktop 无法在后端与 Docker Hub 建立连接时导致其在启动期间失败的问题。修复了 [docker/for-win#10896](https://github.com/docker/for-win/issues/10896)
- **Apple silicon Mac**：Docker Desktop 现在减少了空闲 CPU 消耗。

### 已知问题

**Apple silicon**

- 从容器内部 `ping` 互联网无法按预期工作。为了测试网络，我们建议使用 `curl` 或 `wget`。请参阅 [docker/for-mac#5322](https://github.com/docker/for-mac/issues/5322#issuecomment-809392861)。
- 当 TCP 流半关闭时，用户偶尔可能会遇到数据丢失。

## Docker Desktop 3.3.0
2021-04-08

您现在可以指定何时下载和安装 Docker Desktop 更新。当有更新可用时，Docker Desktop 会显示一个图标以指示有新版本可用。您可以在方便时在后台下载更新。下载完成后，您只需单击“更新并重启”即可安装最新更新。

出于专业开发目的使用 Docker Desktop 的开发人员有时可能需要跳过特定的更新。因此，拥有付费 Docker 订阅的用户可以在提醒出现时跳过特定更新的通知。

对于在 IT 管理环境中工作的开发人员，他们没有管理权限来安装 Docker Desktop 更新，如果您的 Docker ID 是团队订阅的一部分，现在可以在设置菜单中选择完全退出 Docker Desktop 更新的通知。

### 升级

- [Docker Compose 1.29.0](https://github.com/docker/compose/releases/tag/1.29.0)
- [Compose CLI v1.0.12](https://github.com/docker/compose-cli/tree/v1.0.12)
- [Linux kernel 5.10.25](https://hub.docker.com/layers/docker/for-desktop-kernel/5.10.25-6594e668feec68f102a58011bb42bd5dc07a7a9b/images/sha256-80e22cd9c9e6a188a785d0e23b4cefae76595abe1e4a535449627c2794b10871?context=repo)
- [Snyk v1.461.0](https://github.com/snyk/snyk/releases/tag/v1.461.0)
- [Docker Hub Tool v0.3.1](https://github.com/docker/hub-tool/releases/tag/v0.3.1)
- [containerd v1.4.4](https://github.com/containerd/containerd/releases/tag/v1.4.4)
- [runc v1.0.0-rc93](https://github.com/opencontainers/runc/releases/tag/v1.0.0-rc93)

### Bug 修复和细微变更

- 修复了查看使用显式项目名称启动的 compose 应用程序时的问题。修复了 [docker/for-win#10564](https://github.com/docker/for-win/issues/10564)。
- 修复了 `--add-host host.docker.internal:host-gateway` 导致 `host.docker.internal` 解析到错误 IP 地址的 Bug。请参阅 [docker/for-linux#264](https://github.com/docker/for-linux/issues/264#issuecomment-785137844)。
- 修复了导致容器间 HTTP 流量被错误路由到外部 HTTP 代理的 Bug。修复了 [docker/for-mac#5476](https://github.com/docker/for-mac/issues/5476)。
- 修复了在调整磁盘大小时可能导致与 VM 磁盘在同一文件夹中的其他文件被删除的 Bug。修复了 [docker/for-mac#5486](https://github.com/docker/for-mac/issues/5486)。
- 修复了增量下载导致 `非法指令异常` 的问题。修复了 [docker/for-mac#5459](https://github.com/docker/for-mac/issues/5459)。
- 为加密连接应用基于域的 HTTPS 代理 `no_proxy` 规则。修复了 [docker/for-mac#2732](https://github.com/docker/for-mac/issues/2732)。
- 修复了恢复出厂默认设置对话框中缺少文本的问题。修复了 [docker/for-mac#5457](https://github.com/docker/for-mac/issues/5457)。
- 修复了在主机上使用随机端口运行容器导致 Docker Desktop 仪表板错误地使用端口 0 打开浏览器（而不是使用分配的端口）的问题。
- 修复了使用 Docker Desktop 仪表板从 Docker Hub 拉取镜像时静默失败的问题。
- 删除了未使用的 DNS 名称 `docker.for.mac.http.internal`。
- 在启动 Linux VM 时执行文件系统检查。
- 检测 Linux 内核崩溃并将其升级给用户。

## Docker Desktop 3.2.2
2021-03-15

### Bug 修复和细微变更

- 修复了阻止容器绑定到端口 53 的问题。修复了 [docker/for-mac#5416](https://github.com/docker/for-mac/issues/5416)。
- 修复了在 Intel CPU 上模拟 32 位 Intel 二进制文件的问题。修复了 [docker/for-win#10594](https://github.com/docker/for-win/issues/10594)。
- 修复了当网络连接丢失时导致高 CPU 消耗和 UI 冻结的问题。修复了 [for-win/#10563](https://github.com/docker/for-win/issues/10563)。
- 修复了在 iTerm2 没有其他窗口打开时打开终端的问题。修复了 [docker/roadmap#98](https://github.com/docker/roadmap/issues/98#issuecomment-791927788)。

## Docker Desktop 3.2.1
2021-03-05

### 升级

- [Docker Engine 20.10.5](/manuals/engine/release-notes/20.10.md#20105)

### Bug 修复和细微变更

- 修复了有时导致 Docker Desktop 在更新到版本 3.2.0 后无法启动的问题。修复了 [docker/for-mac#5406](https://github.com/docker/for-mac/issues/5406)。如果您在尝试从 3.2.0 更新到 3.2.1 时仍然遇到此问题，我们建议您卸载 3.2.0 并手动安装 Docker Desktop 3.2.1。

## Docker Desktop 3.2.0
2021-03-01

### 新功能

- Docker 仪表板在启动 Docker Desktop 时自动打开。
- Docker 仪表板每周显示一条提示。
- 如果安装了 iTerm2，Docker Desktop 会使用它在容器上启动终端。否则，它会启动默认的 Terminal.App。[docker/roadmap#98](https://github.com/docker/roadmap/issues/98)
- 添加了使用新 Apple Virtualization framework 的实验性支持（需要 macOS Big Sur 11.1 或更高版本）
- BuildKit 现在是所有用户的默认构建器，而不仅仅是新安装的用户。要关闭此设置，请转到 **首选项** > **Docker 引擎** 并将以下块添加到 Docker 守护进程配置文件中：
```json
"features": {
    "buildkit": false
}
```

### 升级

- [Docker Engine 20.10.3](/manuals/engine/release-notes/20.10.md#20103)
- [Docker Compose 1.28.5](https://github.com/docker/compose/releases/tag/1.28.5)
- [Compose CLI v1.0.9](https://github.com/docker/compose-cli/tree/v1.0.9)
- [Docker Hub Tool v0.3.0](https://github.com/docker/hub-tool/releases/tag/v0.3.0)
- [QEMU 5.0.1](https://wiki.qemu.org/ChangeLog/5.0)
- [Amazon ECR Credential Helper v0.5.0](https://github.com/awslabs/amazon-ecr-credential-helper/releases/tag/v0.5.0)
- [Alpine 3.13](https://alpinelinux.org/posts/Alpine-3.13.0-released.html)
- [Kubernetes 1.19.7](https://github.com/kubernetes/kubernetes/releases/tag/v1.19.7)
- [Go 1.16](https://golang.org/doc/go1.16)

### Bug 修复和细微变更

- 修复了容器详细信息屏幕上的一个问题，即当滚动日志时按钮会消失。修复了 [docker/for-mac#5290](https://github.com/docker/for-mac/issues/5290)
- 修复了使用 IPv6 容器网络进行多端口转发时的问题。修复了 [docker/for-mac#5247](https://github.com/docker/for-mac/issues/5247)
- 修复了一个回归问题，即 `docker load` 无法再使用 xz 存档。修复了 [docker/for-mac#5271](https://github.com/docker/for-mac/issues/5271)
- 修复了 **容器 / 应用程序** 视图中的导航问题。修复了 [docker/for-win#10160](https://github.com/docker/for-win/issues/10160#issuecomment-764660660)
- 修复了容器实例视图中容器/镜像名称过长的问题。修复了 [docker/for-mac#5290](https://github.com/docker/for-mac/issues/5290)
- 修复了在特定 IP 上绑定端口时的问题。注意：现在 `docker inspect` 命令显示开放端口可能需要一点时间。修复了 [docker/for-mac#4541](https://github.com/docker/for-mac/issues/4541)
- 修复了从 Docker 仪表板删除的镜像仍在 **镜像** 视图中显示的问题。

### 已知问题

Docker Desktop 有时在更新到版本 3.2.0 后可能无法启动。如果您遇到此问题，我们建议您卸载 3.2.0 并手动安装 [Docker Desktop 3.2.1](#docker-desktop-321)。请参阅 [docker/for-mac#5406](https://github.com/docker/for-mac/issues/5406)。

## Docker Desktop 3.1.0
2021-01-14

### 新功能

- Docker 守护进程现在在基于 Debian Buster 的容器中运行（而不是 Alpine）。

### 升级

- [Compose CLI v1.0.7](https://github.com/docker/compose-cli/tree/v1.0.7)

### Bug 修复和细微变更

- 修复了用户批量创建或删除大量对象时的 UI 可靠性问题。
- 修复了 Alpine 容器中的 DNS 地址解析问题。修复了 [docker/for-mac#5020](https://github.com/docker/for-mac/issues/5020)。
- 重新设计了 **支持** UI 以提高可用性。

## Docker Desktop 3.0.4
2021-01-06

### 升级

- [Docker Engine 20.10.2](/manuals/engine/release-notes/20.10.md#20102)

### Bug 修复和细微变更

- 通过使缓存失效更快来避免 `docker-compose up` 期间的超时。修复了 [docker/for-mac#4957](https://github.com/docker/for-mac/issues/4957)。
- 在使缓存失效时避免生成虚假的文件系统 DELETE 事件。修复了 [docker/for-mac#5124](https://github.com/docker/for-mac/issues/5124)。

### 已知问题

- 某些 DNS 地址在基于 Alpine Linux 3.13 的容器中无法解析。请参阅 [docker/for-mac#5020](https://github.com/docker/for-mac/issues/5020)。

## Docker Desktop 3.0.3
2020-12-21

### Bug 修复和细微变更

- 修复了导致重叠卷挂载失败的问题。修复了 [docker/for-mac#5157](https://github.com/docker/for-mac/issues/5157)。但是，[docker/for-mac#4957](https://github.com/docker/for-mac/issues/4957) 和 [docker/for-mac#5124](https://github.com/docker/for-mac/issues/5124) 的修复因此更改而被恢复，因此这些问题现在再次出现。

### 已知问题

- 某些 DNS 地址在基于 Alpine Linux 3.13 的容器中无法解析。请参阅 [docker/for-mac#5020](https://github.com/docker/for-mac/issues/5020)。
- 如果有多个服务启动，`docker-compose up` 期间可能会出现超时。请参阅 [docker/for-mac#4957](https://github.com/docker/for-mac/issues/4957) 和 [docker/for-mac#5124](https://github.com/docker/for-mac/issues/5124)。

## Docker Desktop 3.0.2
2020-12-18

### Bug 修复和细微变更

- 通过使缓存失效更快来避免 `docker-compose up` 期间的超时。修复了 [docker/for-mac#4957](https://github.com/docker/for-mac/issues/4957)。
- 在使缓存失效时避免生成虚假的文件系统 DELETE 事件。修复了 [docker/for-mac#5124](https://github.com/docker/for-mac/issues/5124)。
- 现在可以将 `~/Library` 中的目录（Docker Desktop 数据目录除外）与容器共享。修复了 [docker/for-mac#5115](https://github.com/docker/for-mac/issues/5115)。
- 如果您创建一个共享 `Home` 或用户 `Library` 目录的容器，现在会看到一个性能警告弹出消息。

### 已知问题

- 某些 DNS 地址在基于 Alpine Linux 3.13 的容器中无法解析。请参阅 [docker/for-mac#5020](https://github.com/docker/for-mac/issues/5020)。

## Docker Desktop 3.0.1
2020-12-11

### Bug 修复和细微变更

- 修复了导致某些目录无法挂载到容器中的问题。修复了 [docker/for-mac#5115](https://github.com/docker/for-mac/issues/5115)。请参阅下面的已知问题。

### 已知问题

- 目前无法将 `~/Library` 中的文件绑定挂载到容器中。请参阅 [docker/for-mac#5115](https://github.com/docker/for-mac/issues/5115)。
- 使用 BuildKit 从 git URL 构建镜像时，如果使用 `github.com/org/repo` 形式会失败。要解决此问题，请使用 `git://github.com/org/repo` 形式。
- 某些 DNS 地址在基于 Alpine Linux 3.13 的容器中无法解析。请参阅 [docker/for-mac#5020](https://github.com/docker/for-mac/issues/5020)。

## Docker Desktop 3.0.0
2020-12-10

### 新功能

- Docker Desktop 版本号使用三位数。
- 从 Docker Desktop 3.0.0 开始，更新现在小得多，因为它们将使用增量补丁应用。
- `docker compose` 的第一个版本（作为现有 `docker-compose` 的替代品）。支持一些基本命令，但尚未完全支持 `docker-compose` 的所有功能。

  - 支持以下子命令：`up`、`down`、`logs`、`build`、`pull`、`push`、`ls`、`ps`
  - 支持基本卷、绑定挂载、网络和环境变量

    请通过在 [compose-cli](https://github.com/docker/compose-cli/issues) GitHub 仓库中创建问题，让我们知道您的反馈。
- [Docker Hub Tool v0.2.0](https://github.com/docker/roadmap/issues/117)

### 升级

- [Docker Engine 20.10.0](/manuals/engine/release-notes/20.10.md#20100)
- [Go 1.15.6](https://github.com/golang/go/issues?q=milestone%3AGo1.15.6+label%3ACherryPickApproved+)
- [Compose CLI v1.0.4](https://github.com/docker/compose-cli/releases/tag/v1.0.4)
- [Snyk v1.432.0](https://github.com/snyk/snyk/releases/tag/v1.432.0)

### Bug 修复和细微变更

- 将内核降级到 [4.19.121](https://hub.docker.com/layers/docker/for-desktop-kernel/4.19.121-2a1dbedf3f998dac347c499808d7c7e029fbc4d3-amd64/images/sha256-4e7d94522be4f25f1fbb626d5a0142cbb6e785f37e437f6fd4285e64a199883a?context=repo) 以减少 hyperkit 的 CPU 使用率。修复了 [docker/for-mac#5044](https://github.com/docker/for-mac/issues/5044)
- 在使用 `osxfs` 时避免缓存错误的文件大小和模式。修复了 [docker/for-mac#5045](https://github.com/docker/for-mac/issues/5045)。
- 修复了一个可能的文件共享错误，即当主机上修改文件时，容器中文件可能显示为大小错误。这是对 [docker/for-mac#4999](https://github.com/docker/for-mac/issues/4999) 的部分修复。
- 删除了不必要的日志消息，这些消息会减慢文件系统事件注入的速度。
- 重新启用了实验性 SOCKS 代理。修复了 [docker/for-mac#5048](https://github.com/docker/for-mac/issues/5048)。
- 修复了尝试使用 `-v /var/run/docker.sock:` 启动不存在的容器时出现的意外 EOF 错误。请参阅 [docker/for-mac#5025](https://github.com/docker/for-mac/issues/5025)。
- 当应用程序需要对特定目录进行写访问时，显示错误消息而不是崩溃。请参阅 [docker/for-mac#5068](https://github.com/docker/for-mac/issues/5068)

### 已知问题

- 使用 BuildKit 从 git URL 构建镜像时，如果使用 `github.com/org/repo` 形式会失败。要解决此问题，请使用 `git://github.com/org/repo` 形式。
- 某些 DNS 地址在基于 Alpine Linux 3.13 的容器中无法解析。
