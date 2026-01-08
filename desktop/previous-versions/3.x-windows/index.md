# Docker for Windows 3.x 发行说明

本页包含 Docker Desktop for Windows 3.x 的发行说明。

## Docker Desktop 3.6.0
2021-08-11

### 新增功能

- **开发环境 (Dev Environments)**：现在可以从本地 Git 仓库创建开发环境。
- **卷管理**：现在可以按名称、创建日期和卷的大小对卷进行排序。还可以使用**搜索**字段搜索特定卷。更多信息，请参阅[探索卷](../use-desktop/volumes.md)。

### 升级

- [Compose V2 RC1](https://github.com/docker/compose-cli/releases/tag/v2.0.0-rc.1)
  - Docker compose 命令行补全。
  - 允许设置 0 规模/副本数。
  - 在 `logs --follow` 时检测新容器。
- [Go 1.16.7](https://github.com/golang/go/releases/tag/go1.16.7)
- [Docker Engine 20.10.8](/manuals/engine/release-notes/20.10.md#20108)
- [containerd v1.4.9](https://github.com/containerd/containerd/releases/tag/v1.4.9)
- [runc v1.0.1](https://github.com/opencontainers/runc/releases/tag/v1.0.1)
- [Kubernetes 1.21.3](https://github.com/kubernetes/kubernetes/releases/tag/v1.21.3)
- [Linux kernel 5.10.47](https://hub.docker.com/layers/docker/for-desktop-kernel/5.10.47-0b705d955f5e283f62583c4e227d64a7924c138f/images/sha256-a4c79bc185ec9eba48dcc802a8881b9d97e532b3f803d23e5b8d4951588f4d51?context=repo)

### Bug 修复和细微变更

- 更新内核配置以修复 [Docker Desktop 3.0.0](#docker-desktop-300) 中的性能回归问题，该问题导致发布容器端口所需时间比旧版本长 10 倍。更多信息，请参阅 [linuxkit/linuxkit#3701](https://github.com/linuxkit/linuxkit/pull/3701) 和 [docker/for-mac#5668](https://github.com/docker/for-mac/issues/5668)。
- 修复了 DNS 服务器在收到意外大的数据报文后会失败的 Bug。
- 修复了 iptables 更新时的虚假跟踪。
- 修复了添加多个端口转发选项时的延迟问题。
- 修复了当 WSL 2 主目录与 Windows 主目录相同时，WSL 2 同步代码会创建悬空符号链接的 Bug。修复了 [docker/for-win#11668](https://github.com/docker/for-win/issues/11668)。
- 修复了当 Linux WSL 2 主目录与 Windows 主目录相同时，从 3.5.x 升级后 `docker context ls` 的问题。
- 修复了 `%PROGRAMDATA%\Docker` 的权限，以避免潜在的 Windows 容器安全风险。参见 [CVE-2021-37841](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-37841)。感谢 [Alessio Dalla Piazza](http://it.linkedin.com/in/alessiodallapiazza) 发现此问题，并感谢 @kevpar 的有益讨论。
- 修复了当 Linux 主目录在 WSL 2 下被设置为 Windows 主目录（例如 `/mnt/c/Users/...`）的 Bug。
- 修复了如果无法解析 CLI 上下文，Desktop 将无法启动的 Bug。修复了 [docker/for-win#11601](https://github.com/docker/for-win/issues/11601)。
- 修复了容器内日志显示的相关问题 [docker/for-win#11251](https://github.com/docker/for-win/issues/11251)。
- 修复了 Windows 后台智能传输服务 (BITS) 故障导致 Docker Desktop 无法启动的问题。[docker/for-win#11273](https://github.com/docker/for-win/issues/11273)

## Docker Desktop 3.5.2
2021-07-08

### 新增功能

**开发环境预览 (Dev Environments Preview)**：开发环境使您能够与团队成员无缝协作，无需在 Git 分支之间切换即可将代码放到团队成员的机器上。使用开发环境时，只需单击一下即可与团队成员共享进行中的工作，且无需处理任何合并冲突。

### 升级

- [Compose V2 beta 6](https://github.com/docker/compose-cli/releases/tag/v2.0.0-beta.6)
  - `compose run` 和 `compose exec` 命令为 stdout 和 stderr 使用独立的流。参见 [docker/compose-cli#1873](https://github.com/docker/compose-cli/issues/1873)。
  - `compose run` 和 `compose exec` 命令支持分离键。修复了 [docker/compose-cli#1709](https://github.com/docker/compose-cli/issues/1709)。
  - 修复了 `compose rm` 命令上的 `--force` 和 `--volumes` 标志。参见 [docker/compose-cli#1844](https://github.com/docker/compose-cli/issues/1844)。
  - 修复了网络的 IPAM 配置。服务可以定义固定 IP。修复了 [docker/compose-cli#1678](https://github.com/docker/compose-cli/issues/1678) 和 [docker/compose-cli#1816](https://github.com/docker/compose-cli/issues/1816)。

- 开发环境
  - 支持 VS Code Insiders。
  - 允许用户在克隆项目时指定分支。参见 [dev-environments#11](https://github.com/docker/dev-environments/issues/11)。

### Bug 修复和细微变更

- 开发环境：修复了在某些创建和删除场景中出现的空白屏幕。修复了 [dev-environments#4](https://github.com/docker/dev-environments/issues/4)。
- 开发环境：修复了删除环境时的错误处理。修复了 [dev-environments#8](https://github.com/docker/dev-environments/issues/8)。
- 开发环境：在环境正在创建或删除时，**开始**、**停止**和**共享**按钮被禁用。
- 在应用程序启动时或在 Windows 和 Linux 容器之间切换时，不再自动切换 CLI 上下文。修复了 [docker/for-mac#5787](https://github.com/docker/for-mac/issues/5787) 和 [docker/for-win#11530](https://github.com/docker/for-win/issues/11530)。
- 修复了 iptables 更新时的虚假跟踪。
- 修复了添加多个端口转发选项时的延迟问题。

## Docker Desktop 3.5.1
2021-06-25

### 新增功能

**开发环境预览 (Dev Environments Preview)**：开发环境使您能够与团队成员无缝协作，无需在 Git 分支之间切换即可将代码放到团队成员的机器上。使用开发环境时，只需单击一下即可与团队成员共享进行中的工作，且无需处理任何合并冲突。

**Compose V2 beta**：Docker Desktop 现在包含 Compose V2 的测试版，该版本支持作为 Docker CLI 一部分的 `docker compose` 命令。虽然 `docker-compose` 仍然受支持和维护，但 Compose V2 的实现直接依赖于作为规范一部分维护的 compose-go 绑定。Docker CLI 中的 compose 命令支持大多数 `docker-compose` 命令和标志。它有望成为 `docker-compose` 的直接替代品。还有一些标志尚未实现，请参阅 docker-compose 兼容性列表以获取有关新 compose 命令中支持的标志的更多信息。如果您在使用 Compose V2 时遇到任何问题，可以通过在 Docker Desktop **实验性**设置中进行更改，或运行命令 `docker-compose disable-v2` 轻松切换回 Compose v1。请通过在 [Compose-CLI](https://github.com/docker/compose-cli/issues) GitHub 仓库中创建问题，让我们知道您对新 'compose' 命令的反馈。

### Bug 修复和细微变更

- 修复了当临时文件夹路径包含点时用户无法安装 Docker Desktop 的 Bug。修复了 [docker/for-win#11514](https://github.com/docker/for-win/issues/11514)。
- 修复了指向提供有关 Docker 如何处理上传的诊断数据详细信息的策略的链接。修复了 [docker/for-mac#5741](https://github.com/docker/for-mac/issues/5741)。

## Docker Desktop 3.5.0
2021-06-23

### 新增功能

**开发环境预览 (Dev Environments Preview)**：开发环境使您能够与团队成员无缝协作，无需在 Git 分支之间切换即可将代码放到团队成员的机器上。使用开发环境时，只需单击一下即可与团队成员共享进行中的工作，且无需处理任何合并冲突。

**Compose V2 beta**：Docker Desktop 现在包含 Compose V2 的测试版，该版本支持作为 Docker CLI 一部分的 `docker compose` 命令。虽然 `docker-compose` 仍然受支持和维护，但 Compose V2 的实现直接依赖于作为规范一部分维护的 compose-go 绑定。Docker CLI 中的 compose 命令支持大多数 `docker-compose` 命令和标志。它有望成为 `docker-compose` 的直接替代品。还有一些标志尚未实现，请参阅 docker-compose 兼容性列表以获取有关新 compose 命令中支持的标志的更多信息。如果您在使用 Compose V2 时遇到任何问题，可以通过在 Docker Desktop **实验性**设置中进行更改，或运行命令 `docker-compose disable-v2` 轻松切换回 Compose v1。请通过在 [Compose-CLI](https://github.com/docker/compose-cli/issues) GitHub 仓库中创建问题，让我们知道您对新 'compose' 命令的反馈。

### 升级

- [Compose V2 beta](https://github.com/docker/compose-cli/releases/tag/v2.0.0-beta.4)
  - 修复了当文件绑定挂载到嵌套挂载点时无法启动容器的 Bug。修复了 [docker/compose-cli#1795](https://github.com/docker/compose-cli/issues/1795)。
  - 添加了对容器链接和外部链接的支持。
  - 引入了 `docker compose logs --since --until` 选项。
  - `docker compose config --profiles` 现在列出所有已定义的配置文件。
- 从 [Kubernetes 1.21.1](https://github.com/kubernetes/kubernetes/releases/tag/v1.21.1) 升级到 [Kubernetes 1.21.2](https://github.com/kubernetes/kubernetes/releases/tag/v1.21.2)。

### Bug 修复和细微变更

- **卷管理**
  - 用户现在可以使用 Docker Dashboard 删除卷内的文件或目录。
  - Docker Dashboard 中的**卷**视图显示卷内内容的最后修改时间和大小。
  - 用户可以从 Docker Dashboard 保存卷内的文件和目录。
- 修复了运行 `docker login` 命令时导致 credStore 超时错误的问题。修复了 [docker/for-win#11472](https://github.com/docker/for-win/issues/11472)。
- Docker Desktop 现在允许 WSL 2 集成代理在 `/etc/wsl.conf` 格式错误时启动。
- 修复了当由多个配置文件启动时，Docker Compose 应用程序未停止或删除的问题。[docker/for-win#11445](https://github.com/docker/for-win/issues/11445)。
- 修复了由于 Hyper-V VM 提前重启，Docker Desktop 在断电后无法重新启动的 Bug。
- 默认的 `docker` CLI `context` 在 Linux 容器模式下现在是 `desktop-linux`，在 Windows 容器模式下是 `desktop-windows`。
- 仅在单击 Docker 菜单时显示 Docker Desktop 反馈弹出窗口。

## Docker Desktop 3.4.0
2021-06-09

### 新增功能

**卷管理**：Docker Desktop 用户现在可以使用 Docker Dashboard 创建和删除卷，还可以查看正在使用的卷。更多信息，请参阅[探索卷](../use-desktop/volumes.md)。

**Compose V2 beta**：Docker Desktop 现在包含 Compose V2 的测试版，该版本支持作为 Docker CLI 一部分的 `docker compose` 命令。虽然 `docker-compose` 仍然受支持和维护，但 Compose V2 的实现直接依赖于作为规范一部分维护的 compose-go 绑定。Docker CLI 中的 compose 命令支持大多数 `docker-compose` 命令和标志。它有望成为 `docker-compose` 的直接替代品。还有一些标志尚未实现，请参阅 docker-compose 兼容性列表以获取有关新 compose 命令中支持的标志的更多信息。如果您在使用 Compose V2 时遇到任何问题，可以通过在 Docker Desktop **实验性**设置中进行更改，或运行命令 `docker-compose disable-v2` 轻松切换回 Compose v1。请通过在 [Compose-CLI](https://github.com/docker/compose-cli/issues) GitHub 仓库中创建问题，让我们知道您对新 'compose' 命令的反馈。

**跳过 Docker Desktop 更新**：所有用户在提示安装单个 Docker Desktop 版本时，现在都可以跳过更新。

### 弃用

- Docker Desktop 不再安装 Notary，应使用 `docker trust` 进行镜像签名。

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

- 修复了 UI 中显示 stderr 日志的错误。修复了 [docker/for-win#11251](https://github.com/docker/for-win/issues/11251)。
- 通过删除卷和构建缓存，在删除容器后自动回收空间。
- 现在可以从 Docker Desktop 删除文件名不是 `docker-compose.yml` 的 Docker Compose 应用程序。修复了 [docker/for-win#11046](https://github.com/docker/for-win/issues/11046)。
- 修复了更新对话框窗口中版本号丢失的问题。
- 修复了有时无法从**支持**对话框正确上传诊断数据的问题。
- 修复了 `*.docker.internal` 的 DNS 条目以及 VM IP 更改后 Kubernetes 集群重置的问题。
- 修复了导致 Docker Desktop 无法启动的损坏的内部缓存。修复了 [docker/for-win#8748](https://github.com/docker/for-win/issues/8748)。
- 修复了 `docker info` 有时响应时间较长的问题。修复了 [docker/for-win#10675](https://github.com/docker/for-win/issues/10675)。

## Docker Desktop 3.3.3
2021-05-06

### 升级

- [Snyk v1.563.0](https://github.com/snyk/snyk/releases/tag/v1.563.0)
- [Docker Scan v0.8.0](https://github.com/docker/scan-cli-plugin/releases/tag/v0.8.0)

### Bug 修复和细微变更

- 修复了从故障排除屏幕上传诊断数据失败的问题。

## Docker Desktop 3.3.2
2021-05-03

### 升级

- [Compose CLI v1.0.14](https://github.com/docker/compose-cli/tree/v1.0.14)
- [Go 1.16.3](https://golang.org/doc/go1.16)
- [Docker Compose 1.29.1](https://github.com/docker/compose/releases/tag/1.29.1)
- [Docker Engine 20.10.6](/manuals/engine/release-notes/20.10.md#20106)

### Bug 修复和细微变更

- 修复了引擎 `daemon.json` 中定义的 `metrics-port` 阻止应用程序重启的 Bug。
- 修复了临时端口泄漏。修复了 [docker/for-mac#5611](https://github.com/docker/for-mac/issues/5611)。
- 默认启用 buildkit 垃圾回收。
- 修复了阻止绑定到端口 123 的 Bug。修复了 [docker/for-mac#5589](https://github.com/docker/for-mac/issues/5589)。
- 删除了“默认将 Docker Stacks 部署到 Kubernetes”的 Kubernetes 设置。该组件在 2.4.0.0 中已被移除，但我们忘记了删除该设置。修复了 [docker/for-mac#4966](https://github.com/docker/for-mac/issues/4966)。

## Docker Desktop 3.3.1
2021-04-15

### Bug 修复和细微变更

- Docker Desktop 现在确保 `/dev/null` 和其他设备在 `--privileged` 容器内的权限正确设置为 `0666` (`rw-rw-rw-`)。修复了 [docker/for-mac#5527](https://github.com/docker/for-mac/issues/5527)。
- 修复了当使用 `\\wsl.localhost` 路径到目录时导致 `docker run` 失败的问题。修复了 [docker/for-win#10786](https://github.com/docker/for-win/issues/10786)。
- 修复了当 Docker Desktop 在后端无法与 Docker Hub 建立连接时导致其在启动期间失败的问题。修复了 [docker/for-win#10896](https://github.com/docker/for-win/issues/10896)。
- 修复了从增量更新创建文件时的文件权限问题。修复了 [docker/for-win#10881](https://github.com/docker/for-win/issues/10881)。

## Docker Desktop 3.3.0
2021-04-08

### 新增功能

您现在可以指定何时下载和安装 Docker Desktop 更新。当有更新可用时，Docker Desktop 会显示一个图标以指示有新版本可用。您可以在方便时在后台下载更新。下载完成后，您只需单击“更新并重启”即可安装最新更新。

出于专业开发目的使用 Docker Desktop 的开发人员有时可能需要跳过特定的更新。因此，拥有付费 Docker 订阅的用户可以在提醒出现时跳过特定更新的通知。

对于 IT 管理环境中没有管理权限来安装 Docker Desktop 更新的开发人员，如果您的 Docker ID 是团队订阅的一部分，现在可以在设置菜单中选择完全退出 Docker Desktop 更新的通知。

### 升级

- [Docker Compose 1.29.0](https://github.com/docker/compose/releases/tag/1.29.0)
- [Compose CLI v1.0.12](https://github.com/docker/compose-cli/tree/v1.0.12)
- [Linux kernel 5.10.25](https://hub.docker.com/layers/docker/for-desktop-kernel/4.19.76-83885d3b4cff391813f4262099b36a529bca2df8-amd64/images/sha256-0214b82436af70054e013ea51cb1fea72bd943d0d6245b6521f1ff09a505c40f?context=repo)
- [Snyk v1.461.0](https://github.com/snyk/snyk/releases/tag/v1.461.0)
- [Docker Hub Tool v0.3.1](https://github.com/docker/hub-tool/releases/tag/v0.3.1)
- [containerd v1.4.4](https://github.com/containerd/containerd/releases/tag/v1.4.4)
- [runc v1.0.0-rc93](https://github.com/opencontainers/runc/releases/tag/v1.0.0-rc93)

### Bug 修复和细微变更

- 修复了查看使用显式项目名称启动的 compose 应用程序时的问题。修复了 [docker/for-win#10564](https://github.com/docker/for-win/issues/10564)。
- 确保 `--add-host host.docker.internal:host-gateway` 导致 `host.docker.internal` 解析为主机 IP，而不是 IP 路由器的 IP。参见 [docker/for-linux#264](https://github.com/docker/for-linux/issues/264)。
- 修复了 Windows 容器的端口分配。修复了 [docker/for-win#10552](https://github.com/docker/for-win/issues/10552)。
- 修复了在主机上使用随机端口运行容器时，导致 Docker Desktop 仪表板错误地使用端口 0 打开浏览器，而不是使用已分配端口的问题。
- 修复了使用 Docker Desktop 仪表板从 Docker Hub 拉取镜像时静默失败的问题。
- 启动 Linux VM 时执行文件系统检查。

## Docker Desktop 3.2.2
2021-03-15

### Bug 修复和细微变更

- 修复了阻止容器绑定到端口 53 的问题。修复了 [docker/for-win#10601](https://github.com/docker/for-win/issues/10601)。
- 修复了 32 位 Intel 二进制文件在 Intel CPU 上被模拟的问题。修复了 [docker/for-win#10594](https://github.com/docker/for-win/issues/10594)。
- 修复了当网络连接丢失时导致高 CPU 消耗和 UI 冻结的问题。修复了 [for-win/#10563](https://github.com/docker/for-win/issues/10563)。

## Docker Desktop 3.2.1
2021-03-05

### 升级

- [Docker Engine 20.10.5](/manuals/engine/release-notes/20.10.md#20105)

## Docker Desktop 3.2.0
2021-03-01

### 新增功能

- Docker Dashboard 在您启动 Docker Desktop 时自动打开。
- Docker Dashboard 每周显示一次提示。
- BuildKit 现在是所有用户的默认构建器，而不仅仅是新安装的用户。要关闭此设置，请转到**设置** > **Docker 引擎**，并将以下块添加到 Docker 守护进程配置文件中：
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

### 弃用

- Docker Desktop 无法再安装在 Windows 1709 (build 16299) 上。
- 删除了已弃用的 DNS 名称 `docker.for.win.localhost`。在容器中使用 DNS 名称 `host.docker.internal` 来访问在主机上运行的服务。[docker/for-win#10619](https://github.com/docker/for-win/issues/10619)

### Bug 修复和细微变更

- 修复了容器详细信息屏幕上的问题，即滚动日志时按钮会消失。修复了 [docker/for-win#10160](https://github.com/docker/for-win/issues/10160)。
- 修复了在 IPv6 容器网络中转发多个端口时的问题。修复了 [docker/for-mac#5247](https://github.com/docker/for-mac/issues/5247)。
- 修复了回归问题，即 `docker load` 无法再使用 xz 存档。修复了 [docker/for-win#10364](https://github.com/docker/for-win/issues/10364)。
- 修复了导致 WSL 2 后端关闭过程干扰 Windows 关闭的问题。修复了 [docker/for-win#5825](https://github.com/docker/for-win/issues/5825) [docker/for-win#6933](https://github.com/docker/for-win/issues/6933) [docker/for-win#6446](https://github.com/docker/for-win/issues/6446)。
- 修复了使用 WSL 2 中的 `desktop.exe` 的凭证存储问题。修复了 [docker/compose-cli#1181](https://github.com/docker/compose-cli/issues/1181)。
- 修复了**容器/应用**视图中的导航问题。修复了 [docker/for-win#10160](https://github.com/docker/for-win/issues/10160#issuecomment-764660660)。
- 修复了容器实例视图中容器/镜像名称过长的问题。修复了 [docker/for-win#10160](https://github.com/docker/for-win/issues/10160)。
- 修复了在特定 IP 上绑定端口时的问题。注意：现在 `docker inspect` 命令显示开放端口可能需要一点时间。修复了 [docker/for-win#10008](https://github.com/docker/for-win/issues/10008)。
- 修复了从 Docker 仪表板删除的镜像仍在**镜像**视图中显示的问题。

## Docker Desktop 3.1.0
2021-01-14

### 新增功能

- 添加了对 WSL 2 后端 GPU 工作负载的实验性支持（需要 Windows Insider 开发者频道）。
- Docker 守护进程现在在基于 Debian Buster 的容器中运行（而不是 Alpine）。

### 升级

- [Compose CLI v1.0.7](https://github.com/docker/compose-cli/tree/v1.0.7)

### Bug 修复和细微变更

- 修复了禁用代理设置不起作用的问题。修复了 [docker/for-win#9357](https://github.com/docker/for-win/issues/9357)。
- 修复了用户批量创建或删除大量对象时的 UI 可靠性问题。
- 重新设计了**支持**UI 以提高可用性。

## Docker Desktop 3.0.4
2021-01-06

### 升级

- [Docker Engine 20.10.2](/manuals/engine/release-notes/20.10.md#20102)

### Bug 修复和细微变更

- 修复了升级到 3.0.0 后可能导致 Docker Desktop 无法启动的问题。修复了 [docker/for-win#9755](https://github.com/docker/for-win/issues/9755)。

## Docker Desktop 3.0.0
2020-12-10

### 新增功能

- Docker Desktop 版本号使用三位数。
- Docker Desktop 更新现在小得多，因为它们将使用增量补丁应用。更多信息，请参阅。
- `docker compose` 的第一个版本（作为现有 `docker-compose` 的替代品）。支持一些基本命令，但尚未具备 `docker-compose` 的完整功能。

  - 支持以下子命令：`up`, `down`, `logs`, `build`, `pull`, `push`, `ls`, `ps`
  - 支持基本卷、绑定挂载、网络和环境变量

    请通过在 [compose-cli](https://github.com/docker/compose-cli/issues) GitHub 仓库中创建问题，让我们知道您的反馈。
- [Docker Hub Tool v0.2.0](https://github.com/docker/roadmap/issues/117)

### 升级

- [Docker Engine 20.10.0](/manuals/engine/release-notes/20.10.md#20100)
- [Go 1.15.6](https://github.com/golang/go/issues?q=milestone%3AGo1.15.6+label%3ACherryPickApproved+)
- [Compose CLI v1.0.4](https://github.com/docker/compose-cli/releases/tag/v1.0.4)
- [Snyk v1.432.0](https://github.com/snyk/snyk/releases/tag/v1.432.0)

### Bug 修复和细微变更

- 将内核降级到 [4.19.121](https://hub.docker.com/layers/docker/for-desktop-kernel/4.19.121-2a1dbedf3f998dac347c499808d7c7e029fbc4d3-amd64/images/sha256-4e7d94522be4f25f1fbb626d5a0142cbb6e785f37e437f6fd4285e64a199883a?context=repo) 以减少 hyperkit 的 CPU 使用率。修复了 [docker/for-mac#5044](https://github.com/docker/for-mac/issues/5044)。
- 修复了尝试使用 `-v /var/run/docker.sock:` 启动不存在的容器时出现意外 EOF 错误的问题。参见 [docker/for-mac#5025](https://github.com/docker/for-mac/issues/5025)。

### 已知问题

- 当使用 `github.com/org/repo` 形式的 URL 时，使用 BuildKit 从 Git URL 构建镜像会失败。要解决此问题，请使用 `git://github.com/org/repo` 形式。
- 基于 Alpine Linux 3.13 的容器中某些 DNS 地址无法解析。
