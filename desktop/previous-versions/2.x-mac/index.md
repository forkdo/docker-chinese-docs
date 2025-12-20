# Docker Desktop for Mac 2.x 发布说明

本页包含 Docker Desktop for Mac 2.x 的发布说明。

## Docker Desktop Community 2.5.0.1
2020-11-10

### 升级

- [Compose CLI v1.0.2](https://github.com/docker/compose-cli/releases/tag/v1.0.2)
- [Snyk v1.424.4](https://github.com/snyk/snyk/releases/tag/v1.424.4)

### 错误修复和次要更改
- 修复了在 MacOS 11.0 (Big Sur) 上同时安装了 VirtualBox 时导致 Docker Desktop 崩溃的问题。参见 [docker/for-mac#4997](https://github.com/docker/for-mac/issues/4997)。

## Docker Desktop Community 2.5.0.0
2020-11-02

Docker Desktop 2.5.0.0 包含 Kubernetes 升级。安装此版本后，您的本地 Kubernetes 集群将被重置。

### 新增

- 付费 Docker 订阅用户现在可以在 Docker Desktop 的“远程仓库”选项卡中查看漏洞扫描报告。
- Docker Desktop 为付费 Docker 订阅用户引入了支持选项。

### 安全

- 修复了因证书检查不足导致的本地权限提升漏洞。参见 [CVE-2021-3162](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-3162)。

### 升级

- [Linux kernel 5.4.39](https://hub.docker.com/layers/linuxkit/kernel/5.4.39-f39f83d0d475b274938c86eaa796022bfc7063d2/images/sha256-8614670219aca0bb276d4749e479591b60cd348abc770ac9ecd09ee4c1575405?context=explore)
- [Docker Compose CLI 1.0.1](https://github.com/docker/compose-cli/releases/tag/v1.0.1)
- [Snyk v1.421.1](https://github.com/snyk/snyk/releases/tag/v1.421.1)
- [Go 1.15.2](https://github.com/golang/go/releases/tag/go1.15.2)
- [Kubernetes 1.19.3](https://github.com/kubernetes/kubernetes/releases/tag/v1.19.3)

### 错误修复和次要更改

- 将“运行诊断”重命名为“获取支持”。
- 移除了 BlueStacks 警告消息。修复 [docker/for-mac#4863](https://github.com/docker/for-mac/issues/4863)。
- 在共享卷包含大量文件的情况下，加快了容器启动速度。修复 [docker/for-mac#4957](https://github.com/docker/for-mac/issues/4957)。
- 文件共享：修复了更改只读文件所有权的问题。修复 [docker/for-mac#4989](https://github.com/docker/for-mac/issues/4989), [docker/for-mac#4964](https://github.com/docker/for-mac/issues/4964)。
- 文件共享：生成 `ATTRIB` inotify 事件以及 `MODIFY`。修复 [docker/for-mac#4962](https://github.com/docker/for-mac/issues/4962)。
- 文件共享：为不支持的模式从 `fallocate` 返回 `EOPNOTSUPP`。修复 `minio`。修复 [docker/for-mac#4964](https://github.com/docker/for-mac/issues/4964)。
- 文件共享：修复了可能过早关闭文件句柄的问题。
- 当与容器共享 Linux 目录（`/var`, `/bin` 等）时，Docker Desktop 会避免监视主机文件系统中的路径。
- 当将文件共享到容器中时（例如 `docker run -v ~/.gitconfig`），Docker Desktop 不会监视父目录。修复 [docker/for-mac#4981](https://github.com/docker/for-mac/issues/4981), [docker/for-mac#4975](https://github.com/docker/for-mac/issues/4975)。
- 修复了与 NFS 挂载相关的问题。修复 [docker/for-mac#4958](https://github.com/docker/for-mac/issues/4958)。
- 允许符号链接指向共享卷之外。修复 [docker/for-mac#4862](https://github.com/docker/for-mac/issues/4862)。
- 诊断：避免在 Kubernetes 处于损坏状态时挂起。
- Docker Desktop 现在支持在共享文件系统上的 `chmod(2)` 调用中使用 `S_ISUID`、`S_ISGID` 和 `S_ISVTX`。修复 [docker/for-mac#4943](https://github.com/docker/for-mac/issues/4943)。

## Docker Desktop Community 2.4.0.0
2020-09-30

Docker Desktop 2.4.0.0 包含 Kubernetes 升级。安装此版本后，您的本地 Kubernetes 集群将被重置。

### 新增

- [Docker Compose CLI - 0.1.18](https://github.com/docker/compose-cli)，支持通过 ECS 和 ACI 在 Compose 和云中使用卷。
- Docker 在 Docker 仪表板中引入了新的“镜像”视图。“镜像”视图允许用户查看 Hub 镜像、拉取镜像以及管理磁盘上的本地镜像，包括清理不需要和未使用的镜像。要访问新的“镜像”视图，请从 Docker 菜单中选择 **Dashboard** > **Images**。
- Docker Desktop 现在在恢复出厂默认设置后默认启用 BuildKit。要恢复到旧的 `docker build` 体验，请转到 **Preferences** > **Docker Engine**，然后禁用 BuildKit 功能。
- [Amazon ECR Credential Helper](https://github.com/awslabs/amazon-ecr-credential-helper/releases/tag/v0.4.0)
- 当主机上有大量文件事件以及运行 Kubernetes 时，Docker Desktop 现在使用的 CPU 要少得多，参见 [docker/roadmap#12](https://github.com/docker/roadmap/issues/12)。
- Docker Desktop 现在默认使用 gRPC-FUSE 进行文件共享。这比 osxfs 使用的 CPU 少得多，尤其是在主机上有大量文件事件时。要切换回 `osxfs`，请转到 **Preferences** > **General** 并禁用 gRPC-FUSE。

### 升级

- [Docker 19.03.13](https://github.com/docker/docker-ce/releases/tag/v19.03.13)
- [Docker Compose 1.27.4](https://github.com/docker/compose/releases/tag/1.27.4)
- [Go 1.14.7](https://github.com/golang/go/releases/tag/go1.14.7)
- [Alpine 3.12](https://alpinelinux.org/posts/Alpine-3.12.0-released.html)
- [Kubernetes 1.18.8](https://github.com/kubernetes/kubernetes/releases/tag/v1.18.8)
- [Qemu 4.2.0](https://git.qemu.org/?p=qemu.git;a=tag;h=1e4aa2dad329852aa6c3f59cefd65c2c2ef2062c)

### 错误修复和次要更改

- macOS 10.13 上的 Docker Desktop 现已弃用。
- 移除了旧的 Kubernetes 上下文 `docker-for-desktop`。应改用上下文 `docker-desktop`。修复 [docker/for-win#5089](https://github.com/docker/for-win/issues/5089) 和 [docker/for-mac#4089](https://github.com/docker/for-mac/issues/5089)。
- 将应用程序添加到 Dock 并单击它时，如果 Docker 正在运行，将启动容器视图。
- 添加了通过 Qemu 4.2.0 模拟 Risc-V 的支持。
- 移除了 `10240` 的文件描述符限制 (`setrlimit`)。我们现在依赖内核通过 `kern.maxfiles` 和 `kern.maxfilesperproc` 来施加限制。
- 通过从 `hyperkit` 中移除串行控制台，修复了 Mac CPU 使用率错误，参见 [docker/roadmap#12]( https://github.com/docker/roadmap/issues/12#issuecomment-663163280)。要在 VM 中打开 shell，请使用 `nc -U ~/Library/Containers/com.docker.docker/Data/debug-shell.sock`。
- 将不带 ansi 颜色的容器日志复制到剪贴板。修复 [docker/for-mac#4786](https://github.com/docker/for-mac/issues/4786)。
- 修复了登录时自动启动的问题。参见 [docker/for-mac#4877] 和 [docker/for-mac#4890]。
- 修复了用户名过长时应用程序无法启动的错误。
- 修复了将 `/usr` 等目录添加到文件共享列表会阻止 Desktop 启动的错误。修复 [docker/for-mac#4488](https://github.com/docker/for-mac/issues/4488)
- 修复了如果在 Docker `daemon.json` 中指定了 `hosts` 会导致应用程序启动失败的问题。参见 [docker/for-win#6895](https://github.com/docker/for-win/issues/6895#issuecomment-637429117)
- Docker Desktop 现在在容器启动时同步刷新文件系统缓存。参见 [docker/for-mac#4943](https://github.com/docker/for-mac/issues/4943)。
- Docker Desktop 安装程序中不再包含 Compose-on-Kubernetes。您可以从 compose-on-kubernetes [发布页面](https://github.com/docker/compose-on-kubernetes/releases) 单独下载它。

### 已知问题

-  使用 `docker-compose` 和命名卷以及 gRPC FUSE 时存在一个已知问题：第二次及后续调用 `docker-compose up` 将失败，因为卷路径带有 `/host_mnt` 前缀。要解决此问题，请在设置中切换回 `osxfs`。参见 [docker/for-mac#4859](https://github.com/docker/for-mac/issues/4859)。
- 启用 Kubernetes 时存在一个已知问题，即设置 UI 无法更新 Kubernetes 状态。要解决此问题，请关闭并重新打开窗口。
- 切换用户时存在一个罕见的已知问题，即镜像视图继续显示上一个用户的仓库。要解决此问题，请关闭并重新打开窗口。

## Docker Desktop Community 2.3.0.5
2020-09-15

### 新增

- Docker CLI 中的新云集成使得使用 Amazon ECS 或 Microsoft ACI 在云中运行容器变得容易。
### 升级

- [Docker Compose 1.27.2](https://github.com/docker/compose/releases/tag/1.27.2)
- [Cloud integration v0.1.15](https://github.com/docker/aci-integration-beta/releases/tag/v0.1.15)

### 错误修复和次要更改

- 修复了登录时自动启动的问题。参见 [docker/for-mac#4877](https://github.com/docker/for-mac/issues/4877) 和 [docker/for-mac#4890](https://github.com/docker/for-mac/issues/4890)

### 已知问题

-  `clock_gettime64` 系统调用在 i386 镜像中返回 `EPERM` 而不是 `ENOSYS`。要解决此问题，请使用 `--privileged` 标志禁用 `seccomp`。参见 [docker/for-win#8326](https://github.com/docker/for-win/issues/8326)。

## Docker Desktop Community 2.3.0.4
2020-07-27

### 升级

- [Docker 19.03.12](https://github.com/docker/docker-ce/releases/tag/v19.03.12)
- [Docker Compose 1.26.2](https://github.com/docker/compose/releases/tag/1.26.2)
- [Go 1.13.14](https://github.com/golang/go/issues?q=milestone%3AGo1.13.14+label%3ACherryPickApproved)

### 错误修复和次要更改

- 修复了 `com.docker.vmnetd` 中的权限提升漏洞。参见 [CVE-2020-15360](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2020-15360)
- 修复了当 Kubernetes 证书过期时启动的问题。参见 [docker/for-mac#4594](https://github.com/docker/for-mac/issues/4594)
- 修复了 `hyperkit` 和 [osquery](https://osquery.io) 之间的不兼容问题，该问题导致 `hyperkit` CPU 使用率过高。参见 [docker/for-mac#3499](https://github.com/docker/for-mac/issues/3499#issuecomment-619544836)
- 仪表板：修复了容器日志有时被截断的问题。修复 [docker/for-win#5954](https://github.com/docker/for-win/issues/5954)

## Docker Desktop Community 2.3.0.3
2020-05-27

### 升级

- [Linux kernel 4.19.76](https://hub.docker.com/layers/docker/for-desktop-kernel/4.19.76-83885d3b4cff391813f4262099b36a529bca2df8-amd64/images/sha256-0214b82436af70054e013ea51cb1fea72bd943d0d6245b6521f1ff09a505c40f?context=repo)

### 错误修复和次要更改

- 重新将 device-mapper 添加到嵌入式 Linux 内核中。修复 [docker/for-mac#4549](https://github.com/docker/for-mac/issues/4549)。
- 修复了在新款 Mac 和新版 `Hypervisor.framework` 上的 `hyperkit` 问题。修复 [docker/for-mac#4562](https://github.com/docker/for-mac/issues/4562)。

## Docker Desktop Community 2.3.0.2
2020-05-11


### 新增

Docker Desktop 在首次启动时引入了新的入门教程。快速入门教程指导用户通过几个简单的步骤开始使用 Docker。它包括一个简单的练习，用于构建示例 Docker 镜像，将其作为容器运行，推送到 Docker Hub 并保存。

### 升级

- [Docker Compose 1.25.5](https://github.com/docker/compose/releases/tag/1.25.5)
- [Go 1.13.10](https://github.com/golang/go/issues?q=milestone%3AGo1.13.10+label%3ACherryPickApproved)
- [Linux kernel 4.19.76](https://hub.docker.com/layers/docker/for-desktop-kernel/4.19.76-ce15f646db9b062dc947cfc0c1deab019fa63f96-amd64/images/sha256-6c252199aee548e4bdc8457e0a068e7d8e81c2649d4c1e26e4150daa253a85d8?context=repo)
- LinuxKit [init](https://hub.docker.com/layers/linuxkit/init/1a80a9907b35b9a808e7868ffb7b0da29ee64a95/images/sha256-64cc8fa50d63940dbaa9979a13c362c89ecb4439bcb3ab22c40d300b9c0b597e?context=explore), [runc](https://hub.docker.com/layers/linuxkit/runc/69b4a35eaa22eba4990ee52cccc8f48f6c08ed03/images/sha256-57e3c7cbd96790990cf87d7b0f30f459ea0b6f9768b03b32a89b832b73546280?context=explore) 和 [containerd](https://hub.docker.com/layers/linuxkit/containerd/09553963ed9da626c25cf8acdf6d62ec37645412/images/sha256-866be7edb0598430709f88d0e1c6ed7bfd4a397b5ed220e1f793ee9067255ff1?context=explore)

### 错误修复和次要更改

- 将 Docker Desktop 安装程序的大小从 708 MB 减少到 456 MB。
- 修复了当 Kubernetes 上下文无效时容器从 UI 中消失的错误。修复 [docker/for-win#6037](https://github.com/docker/for-win/issues/6037)。
- 修复了 `vpnkit-bridge` 中的文件描述符泄漏问题。修复 [docker/for-win#5841](https://github.com/docker/for-win/issues/5841)。
- 在 UI 中添加了指向 Edge 频道的链接。
- 使嵌入式终端可调整大小。
- 修复了如果用户名包含空格，诊断上传会失败的错误。
- 修复了可以在没有引擎的情况下启动 Docker UI 的错误。
- 从 `ahci-hd` 切换到 `virtio-blk` 以避免 AHCI 死锁，参见 [moby/hyperkit#94](https://github.com/moby/hyperkit/issues/94) 和 [docker/for-mac#1835](https://github.com/docker/for-mac/issues/1835)。
- 修复了容器端口无法在特定主机 IP 上暴露的问题。参见 [docker/for-mac#4209](https://github.com/docker/for-mac/issues/4209)。
- 从仪表板中移除了端口探测，只是无条件地显示应可用端口的链接。修复 [docker/for-mac#4264](https://github.com/docker/for-mac/issues/4264)。
- Docker Desktop 现在默认共享 `/var/folders`，因为它存储每个用户的临时文件和缓存。
- 为了节省磁盘空间，已从 Docker Desktop 中移除了 Ceph 支持。
- 修复了在 2.2.0.5 中使用共享卷时的性能回归问题。修复 [docker/for-mac#4423]。

## Docker Desktop Community 2.2.0.5
2020-04-02

### 错误修复和次要更改

- 移除了悬空的 `/usr/local/bin/docker-machine` 符号链接，这可以避免在将来的升级中意外删除自定义安装的 Docker Machine。请注意，如果您手动安装了 Docker Machine，则安装可能遵循了符号链接并将 Docker Machine 安装在 `/Applications/Docker.app` 中。在这种情况下，安装此版本的 Docker Desktop 后，您必须手动重新安装 Docker Machine。修复 [docker/for-mac#4208](https://github.com/docker/for-mac/issues/4208)。

## Docker Desktop Community 2.2.0.4
2020-03-13

### 升级

- [Docker 19.03.8](https://github.com/docker/docker-ce/releases/tag/v19.03.8)

### 错误修复和次要更改

- Kubernetes：由声明创建的持久卷现在存储在虚拟机中。修复 [docker/for-win#5665](https://github.com/docker/for-win/issues/5665)。
- 修复了导致 Docker Desktop 仪表板尝试连接到容器内所有暴露端口的问题。修复 [docker/for-mac#4264](https://github.com/docker/for-mac/issues/4264)。

## Docker Desktop Community 2.2.0.3
2020-02-11

### 升级

- [Docker Compose 1.25.4](https://github.com/docker/compose/releases/tag/1.25.4)
- [Go 1.12.16](https://golang.org/doc/devel/release.html#go1.12)

## Docker Desktop Community 2.2.0.0
2020-01-21

Docker Desktop 2.2.0.0 包含 Kubernetes 升级。安装此版本后，您的本地 Kubernetes 集群将被重置。

### 升级

- [Docker Compose 1.25.2](https://github.com/docker/compose/releases/tag/1.25.2)
- [Kubernetes 1.15.5](https://github.com/kubernetes/kubernetes/releases/tag/v1.15.5)
- Linux kernel 4.19.76
- [QEMU 4.0.1](https://github.com/docker/binfmt)

### 新增

- **Docker Desktop 仪表板：** 新的 Docker Desktop **仪表板** 提供了一个用户友好的界面，使您能够与容器和应用程序交互，并直接从 UI 管理应用程序的生命周期。此外，它还允许您访问日志、查看容器详细信息并监控资源利用率以探索容器行为。
  有关新仪表板 UI 的详细信息，请参阅 [Docker Desktop 仪表板](../_index.md)。

- 为 Docker Desktop **首选项** 菜单引入了新的用户界面。
- “重启”、“重置”和“卸载”选项现在可在 **故障排除** 菜单中使用。
- 添加了在 Docker Desktop **仪表板** UI 中启动和停止现有的基于 Compose 的应用程序以及查看组合日志的功能。

### 错误修复和次要更改

- 为 Docker Compose 添加了 `fish` shell 的缺失补全。修复 [docker/for-mac#3795](https://github.com/docker/for-mac/issues/3795)。
- 修复了不允许用户在 **首选项** > **守护程序** 窗口中复制和粘贴文本的错误。修复 [docker/for-mac#3798](https://github.com/docker/for-mac/issues/3798)。
- 在 Docker API 代理中添加了对 `Expect: 100-continue` 标头的支持。某些 HTTP 客户端（如 `curl`）在有效负载较大时（例如创建容器时）会发送此标头。修复 [moby/moby#39693](https://github.com/moby/moby/issues/39693)。
- 在 **设置** 和 **故障排除** 窗口中添加了加载覆盖层，以防止编辑冲突。
- 当 Kubernetes 未激活时，停用 **重置 Kubernetes** 按钮。
- 改进了 **设置** 和 **故障排除** UI 中的导航。
- 修复了 UEFI 启动菜单中的一个错误，该错误有时会导致 Docker Desktop 在重启期间挂起。修复 [docker/for-mac#2655](https://github.com/docker/for-mac/issues/2655) 和 [docker/for-mac#3921](https://github.com/docker/for-mac/issues/3921)。
- Docker Desktop 现在允许用户在容器内访问主机的 SSH 代理。修复 [docker/for-mac#410](https://github.com/docker/for-mac/issues/410)
- Docker Machine 不再包含在 Docker Desktop 安装程序中。您可以从 [Docker Machine 发布](https://github.com/docker/machine/releases) 页面单独下载它。
- 修复了在运行 macOS Catalina 的旧硬件上运行的 VM 因错误 `processor does not support desired secondary processor-based controls` 而启动失败的问题。
- 修复了当容器使用 `overlay` 网络时的端口转发问题。
- 修复了当容器具有多个端口且具有任意或尚未配置的外部端口号时的容器启动错误。例如，`docker run -p 80 -p 443 nginx`。修复 [docker/for-win#4935](https://github.com/docker/for-win/issues/4935) 和 [docker/compose#6998](https://github.com/docker/compose/issues/6998)。
- 修复了共享重叠目录时发生的问题。
- 修复了阻止用户更改 VM 磁盘映像位置的错误。
- Docker Desktop 不再在目录上注入 `inotify` 事件，因为这些事件可能导致挂载点在容器内消失。修复 [docker/for-mac#3976](https://github.com/docker/for-mac/issues/3976)。
- 修复了当存在不完整的 Kubernetes 配置文件时导致 Docker Desktop 启动失败的问题。
- 修复了有时通过 Docker Desktop 登录 Docker 可能因 `Incorrect authentication credentials` 错误而失败的问题。修复 [docker/for-mac#4010](https://github.com/docker/for-mac/issues/4010)。

### 已知问题

- 当您启动一个 Docker Compose 应用程序，然后启动一个与 Compose 应用程序同名的 Docker App 时，Docker Desktop 在仪表板上只显示一个应用程序。但是，当您展开该应用程序时，属于这两个应用程序的容器都会显示在仪表板上。

- 当您在 Kubernetes 上部署具有多个容器的 Docker App 时，Docker Desktop 将每个 Pod 显示为仪表板上的一个应用程序。

## Docker Desktop Community 2.1.0.5
2019-11-18

Docker Desktop 2.1.0.5 包含 Kubernetes 升级。请注意，安装此版本后，您的本地 Kubernetes 集群将被重置。

### 升级

- [Docker 19.03.5](https://github.com/docker/docker-ce/releases/tag/v19.03.5)
- [Kubernetes 1.14.8](https://github.com/kubernetes/kubernetes/releases/tag/v1.14.8)
- [Go 1.12.13](https://golang.org/doc/devel/release.html#go1.12)

## Docker Desktop Community 2.1.0.4
2019-10-21

### 升级

- [Docker 19.03.4](https://github.com/docker/docker-ce/releases/tag/v19.03.4)
- [Kubernetes 1.14.7](https://github.com/kubernetes/kubernetes/releases/tag/v1.14.7)
- [Go 1.12.10](https://github.com/golang/go/issues?q=milestone%3AGo1.12.10+label%3ACherryPickApproved)
- [Kitematic 0.17.9](https://github.com/docker/kitematic/releases/tag/v0.17.9)

### 新增

Docker Desktop 现在允许您使用双因素认证登录 Docker Hub。


## Docker Desktop Community 2.1.0.3
2019-09-16

### 升级

- [Kitematic 0.17.8](https://github.com/docker/kitematic/releases/tag/v0.17.8)

### 错误修复和次要更改

- Docker Desktop 中包含的所有二进制文件现在都经过公证，以便可以在 macOS Catalina 上运行。有关更多信息，请参阅 [Mac 软件的公证要求](https://developer.apple.com/news/?id=06032019i)。

## Docker Desktop Community 2.1.0.2
2019-09-04

Docker Desktop 2.1.0.2 包含 Kubernetes 升级。请注意，安装此版本后，您的本地 Kubernetes 集群将被重置。

### 升级

- [Docker 19.03.2](https://github.com/docker/docker-ce/releases/tag/v19.03.2)
- [Kubernetes 1.14.6](https://github.com/kubernetes/kubernetes/releases/tag/v1.14.6)
- [Go 1.12.9](https://github.com/golang/go/issues?q=milestone%3AGo1.12.9+label%3ACherryPickApproved)
- [Docker Machine 0.16.2](https://github.com/docker/machine/releases/tag/v0.16.2)

## Docker Desktop Community 2.1.0.1
2019-08-08

请注意，您必须登录并创建 Docker ID 才能下载 Docker Desktop。

### 升级

* [Docker 19.03.1](https://github.com/docker/docker-ce/releases/tag/v19.03.1)
* [Docker Compose 1.24.1](https://github.com/docker/compose/releases/tag/1.24.1)
* [Kubernetes 1.14.3](https://github.com/kubernetes/kubernetes/releases/tag/v1.14.3)
* [Compose on Kubernetes 0.4.23](https://github.com/docker/compose-on-kubernetes/releases/tag/v0.4.23)
* [Docker Machine 0.16.1](https://github.com/docker/machine/releases/tag/v0.16.1)
* [linuxkit v0.7](https://github.com/linuxkit/linuxkit/releases/tag/v0.7)
* Linux Kernel 4.9.184
* [Kitematic 0.17.6](https://github.com/docker/kitematic/releases/tag/v0.17.6)
* [Qemu 4.0.0](https://github.com/docker/binfmt) 用于 ARM 交叉编译
* [Alpine 3.10](https://alpinelinux.org/posts/Alpine-3.10.0-released.html)
* [Docker Credential Helpers 0.6.3](https://github.com/docker/docker-credential-helpers/releases/tag/v0.6.3)
* [Hyperkit v0.20190802](https://github.com/moby/hyperkit/releases/tag/v0.20190802)

### 新增

* 在守护程序 **首选项** 菜单中选择“实验性功能”复选框，可为 Docker 守护程序和 Docker CLI 开启实验性功能。
* 改进了 `com.docker.osxfs trace` 性能分析命令的可靠性。用户现在可以运行 `com.docker.osxfs trace --summary` 选项来获取操作的高级摘要，而不是接收所有操作的跟踪。
* Docker Desktop 现在支持 Mac 上的大型 DNS 资源记录列表。修复 [docker/for-mac#2160](https://github.com/docker/for-mac/issues/2160#issuecomment-431571031)。

### 实验性

> 实验性功能提供对将来产品功能的早期访问。这些功能仅用于测试和反馈，因为它们可能在版本之间更改而不发出警告，或者可能在将来的版本中被完全移除。实验性功能不得在生产环境中使用。Docker 不为实验性功能提供支持。

Docker Desktop Community 2.1.0.0 包含以下实验性功能。

* Docker App：Docker App 是一个 CLI 插件，可帮助配置、共享和安装应用程序。
* Docker Buildx：Docker Buildx 是一个用于扩展 BuildKit 构建功能的 CLI 插件。有关更多信息，请参阅 [构建页面](/manuals/build/_index.md)。

### 错误修复和次要更改

* Docker Desktop 现在允许用户暴露特权 UDP 端口。[docker/for-mac#3775](https://github.com/docker/for-mac/issues/3775)
* 修复了如果您未使用凭证帮助程序，运行某些 Docker 命令可能会失败的问题。[docker/for-mac#3785](https://github.com/docker/for-mac/issues/3785)
* 更改了主机的 kubernetes 上下文，以便 `docker run -v .kube:kube ... kubectl` 可以工作。
* 将本地 Kubernetes 集群上的 `cluster-admin` 角色限制为 `kube-system` 命名空间。
* 减少了 VM 启动时间。每次虚拟机启动时不再创建交换空间。
* 修复了使用 VPNkit 子网的 Kubernetes 安装。
* 修复了在 Windows 上收集诊断信息时进程输出未重定向到 stdout 的错误，这有时会导致崩溃。
* 将 `/etc/machine-id` 添加到虚拟机中。修复 [docker/for-mac#3554](https://github.com/docker/for-mac/issues/3554)。
* Docker Desktop 不再每 10 秒发送一次 `docker-desktop.<domain>` 的 DNS 查询。它现在依赖于主机的 DNS 域搜索顺序，而不是尝试在 VM 内复制它。
* 移除了使用电子邮件地址作为用户名登录的功能，因为 Docker 命令行不支持此功能。
* Docker Desktop 现在允许在容器内运行 Docker 注册表。修复 [docker/for-mac#3611](https://github.com/docker/for-mac/issues/3611)。
* 修复了 DNS 解析器的稳定性问题。
* Docker Desktop 会截断超过 512 字节的 UDP DNS 响应。
* 修复了启动 Kubernetes 时在 localhost 上使用的端口 8080。修复 [docker/for-mac#3522](https://github.com/docker/for-mac/issues/3522)。
* 改进了错误消息传递：当不适用时，Docker Desktop 不会
