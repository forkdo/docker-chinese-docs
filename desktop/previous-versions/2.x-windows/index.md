# Docker for Windows 2.x 发布说明

此页面包含 Docker Desktop for Windows 2.x 的发布说明。

## Docker Desktop Community 2.5.0.1
2020-11-10

### 升级

- [Compose CLI v1.0.2](https://github.com/docker/compose-cli/releases/tag/v1.0.2)
- [Snyk v1.424.4](https://github.com/snyk/snyk/releases/tag/v1.424.4)

## Docker Desktop Community 2.5.0.0
2020-11-02

Docker Desktop 2.5.0.0 包含 Kubernetes 升级。安装此版本后，您的本地 Kubernetes 集群将被重置。

### 新增功能

- 付费 Docker 订阅用户现在可以在 Docker Desktop 的“远程仓库”选项卡中查看漏洞扫描报告。
- Docker Desktop 为拥有付费 Docker 订阅的用户引入了支持选项。

### 升级

- [Linux kernel 5.4.39](https://hub.docker.com/layers/linuxkit/kernel/5.4.39-f39f83d0d475b274938c86eaa796022bfc7063d2/images/sha256-8614670219aca0bb276d4749e479591b60cd348abc770ac9ecd09ee4c1575405?context=explore)
- [Docker Compose CLI 1.0.1](https://github.com/docker/compose-cli/releases/tag/v1.0.1)
- [Snyk v1.421.1](https://github.com/snyk/snyk/releases/tag/v1.421.1)
- [Go 1.15.2](https://github.com/golang/go/releases/tag/go1.15.2)
- [Kubernetes 1.19.3](https://github.com/kubernetes/kubernetes/releases/tag/v1.19.3)

### 弃用

- Docker Desktop 不再支持在 Windows 1703 (build 15063) 上安装。

### Bug 修复和次要更改

- 将“运行诊断”重命名为“获取支持”。
- 修复了间歇性导致 WSL 2 后端启动失败的问题。
- 修复了与 NFS 挂载相关的问题。参见 [docker/for-mac#4958](https://github.com/docker/for-mac/issues/4958)。
- 修复了在 Docker Desktop 启动之前启动 WSL 中的 bash 时找不到 docker CLI 的问题。
- 修复了 HTTP 代理排除列表包含 `localhost` 或 `127.0.0.1` 等条目时的问题。修复 [docker/for-win#8750](https://github.com/docker/for-win/issues/8750)。
- 当 WSL 集成进程意外停止时，现在会通知用户，并且可以决定是否重新启动，而不是总是尝试循环重启。修复 [docker/for-win#8968](https://github.com/docker/for-win/issues/8968)。
- 修复了在高负载下容器日志滞后的问题。修复 [docker/for-win#8216](https://github.com/docker/for-win/issues/8216)。
- 诊断：避免在 Kubernetes 处于损坏状态时挂起。
- 修复了当用户名包含空格时安装程序日志文件默认位置的路径。修复 [docker/for-win#7941](https://github.com/docker/for-win/issues/7941)。
- 修复了某些网络插件可能加载失败，导致 Docker 守护进程崩溃的问题 [docker/for-win#9282](https://github.com/docker/for-win/issues/9282)。
- 当将文件共享到容器中时（例如 `docker run -v ~/.gitconfig`），Docker Desktop 不再监视父目录。修复 [docker/for-mac#4981](https://github.com/docker/for-mac/issues/4981)。

## Docker Desktop Community 2.4.0.0
2020-09-30

Docker Desktop 2.4.0.0 包含 Kubernetes 升级。安装此版本后，您的本地 Kubernetes 集群将被重置。

### 新增功能

- [Docker Compose CLI - 0.1.18](https://github.com/docker/compose-cli)，支持通过 ECS 和 ACI 在 Compose 和云中使用卷。
- Docker 在 Docker 仪表板中引入了新的“镜像”视图。镜像视图允许用户查看 Hub 镜像、拉取它们并管理磁盘上的本地镜像，包括清理不需要和未使用的镜像。要访问新的“镜像”视图，请从 Docker 菜单中选择 **Dashboard** > **Images**。
- Docker Desktop 在恢复出厂默认设置后默认启用 BuildKit。要恢复到旧的 `docker build` 体验，请转到 **Settings** > **Docker Engine**，然后禁用 BuildKit 功能。
- [Amazon ECR Credential Helper](https://github.com/awslabs/amazon-ecr-credential-helper/releases/tag/v0.4.0)

### 升级

- [Docker 19.03.13](https://github.com/docker/docker-ce/releases/tag/v19.03.13)
- [Docker Compose 1.27.4](https://github.com/docker/compose/releases/tag/1.27.4)
- [Go 1.14.7](https://github.com/golang/go/releases/tag/go1.14.7)
- [Alpine 3.12](https://alpinelinux.org/posts/Alpine-3.12.0-released.html)
- [Kubernetes 1.18.8](https://github.com/kubernetes/kubernetes/releases/tag/v1.18.8)
- [Qemu 4.2.0](https://git.qemu.org/?p=qemu.git;a=tag;h=1e4aa2dad329852aa6c3f59cefd65c2c2ef2062c)

### Bug 修复和次要更改

- 移除了旧的 Kubernetes 上下文 `docker-for-desktop`。应改用上下文 `docker-desktop`。修复 [docker/for-win#5089](https://github.com/docker/for-win/issues/5089) 和 [docker/for-mac#4089](https://github.com/docker/for-mac/issues/4089)。
- 从安装程序中移除了使用 Windows 容器启动的选项。
- 将应用程序固定到任务栏并点击它时，如果 Docker 正在运行，将启动容器视图。
- 在系统托盘中左键点击鲸鱼图标现在会启动仪表板容器视图。
- Docker Desktop 现在为深色和浅色模式使用不同的系统托盘图标。修复 [docker/for-win#4113](https://github.com/docker/for-win/issues/4113)。
- 通过 Qemu 4.2.0 添加了对模拟 Risc-V 的支持。
- 添加了一个可通过 `putty -serial \\.\pipe\dockerDebugShell` 访问的低级调试 shell。
- 将不带 ansi 颜色的容器日志复制到剪贴板。修复 [docker/for-mac#4786](https://github.com/docker/for-mac/issues/4786)。
- 修复了如果在 Docker `daemon.json` 中指定了 `hosts` 导致应用程序启动失败的问题。参见 [docker/for-win#6895](https://github.com/docker/for-win/issues/6895#issuecomment-637429117)
- 修复了短名称的 DNS 解析。参见 [docker/for-win#4425](https://github.com/docker/for-win/issues/4425)。
- 从 `chronyd` 切换到 `sntpcd` 以解决主机时间同步问题。修复 [docker/for-win#4526](https://github.com/docker/for-win/issues/4526)。
- 如果设置了“在 tcp://localhost:2375 上公开守护进程（无 TLS）”且 `localhost:2375` 被其他程序占用，避免阻止启动。参见 [docker/for-win#6929](https://github.com/docker/for-win/issues/6929) [docker/for-win#6961](https://github.com/docker/for-win/issues/6961)。
- 修复了在设置中向不存在的驱动器添加文件夹会创建空条目的问题。参见 [docker/for-win#6797](https://github.com/docker/for-win/issues/6797)。
- 避免在共享卷上进行文件 I/O 时出现“功能未实现”错误。修复 [docker/for-win#5955](https://github.com/docker/for-win/issues/5955)
- 确保 `docker run -v /var/run/docker.sock` 正确重写 Windows 路径，参见 [docker/for-win#6628](https://github.com/docker/for-win/issues/6628)。
- 修复了 Docker Desktop 加载损坏的 Docker CLI 配置文件时发生的崩溃。修复 [docker/for-win#6657](https://github.com/docker/for-win/issues/6657)。
- 确保 `localhost` 和 `127.0.0.1` 都可以在代理设置中用于重定向到主机上的代理。修复 [docker/for-win#5715](https://github.com/docker/for-win/issues/5715) 和 [docker/for-win#6260](https://github.com/docker/for-win/issues/6260)。
- 修复了在没有互联网连接时登录失败导致的崩溃。
- 修复了处理带有“..”字符的共享卷路径时的错误。修复 [docker/for-win#5375](https://github.com/docker/for-win/issues/5375)。
- 在 toast 通知中报告检查更新错误。修复 [docker/for-win#6364](https://github.com/docker/for-win/issues/6364)。
- 修复了一个升级错误，即仍在使用基于 PowerShell 的 VM 管理的版本的用户可能会遇到静默卸载崩溃，导致 Docker Desktop 被卸载而不是升级。
- 修复了当用户名包含空格时安装程序日志文件默认位置的路径。修复 [docker/for-win#7941](https://github.com/docker/for-win/issues/7941)。
- Docker Desktop 在容器启动时始终同步刷新文件系统缓存。参见 [docker/for-mac#4943](https://github.com/docker/for-mac/issues/4943)。
- Docker Desktop 安装程序中不再包含 Compose-on-Kubernetes。您可以从 compose-on-kubernetes [发布页面](https://github.com/docker/compose-on-kubernetes/releases) 单独下载它。

### WSL 2 更改

- Docker 上下文现在在 Windows 和 WSL 发行版之间同步。
- 修复了间歇性导致后端启动失败的问题。
- 修复了当 glibc 不兼容时发生的代理崩溃。参见 [docker/for-win#8183](https://github.com/docker/for-win/issues/8183)。
- 修复了移除挂载 `/mnt/wsl` 的容器时会破坏 WSL 集成的问题。参见 [docker/for-win#7836](https://github.com/docker/for-win/issues/7836)。
- 添加了使用 Windows CLI 从发行版挂载文件的支持（例如 `docker run -v \\wsl$\Ubuntu\home\simon\web:/web ...`）。
- 修复了尝试使用相对路径的共享卷时的错误消息。修复 [docker/for-win#6894](https://github.com/docker/for-win/issues/6894)。
- 修复了将 Windows 更新到支持 WSL 2 的版本时，配置文件被旧的 Hyper-V VM 锁定的问题。
- 修复了 WSL 2 内外 Docker Compose 版本不一致的问题。修复 [docker/for-win#6461](https://github.com/docker/for-win/issues/6461)。
- 检测到 `docker-desktop` wsl 发行版停止时，显示更清晰的错误消息。
- 修复了暴露端口时的竞争条件。
- 启用对话框不再阻止其他窗口。

### 已知问题

-  使用 `docker-compose` 和命名卷以及 gRPC FUSE 时存在一个已知问题：第二次及后续调用 `docker-compose up` 将失败，因为卷路径带有前缀 `/host_mnt`。
- 启用 Kubernetes 时存在一个已知问题，即设置 UI 有时无法更新 Kubernetes 状态。要解决此问题，请关闭并重新打开窗口。
- 切换用户时存在一个罕见的已知问题，即镜像 UI 有时会继续显示上一个用户的仓库。要解决此问题，请关闭并重新打开窗口。

## Docker Desktop Community 2.3.0.5
2020-09-15

### 新增功能

- Docker CLI 中的新云集成使得使用 Amazon ECS 或 Microsoft ACI 在云中运行容器变得容易。

### 升级

- [Docker Compose 1.27.2](https://github.com/docker/compose/releases/tag/1.27.2)
- [Cloud integration v0.1.15](https://github.com/docker/aci-integration-beta/releases/tag/v0.1.15)

### Bug 修复和次要更改

- WSL2：修复了使用不兼容的 glibc 时发生的崩溃。参见 [docker/for-win#8183](https://github.com/docker/for-win/issues/8183)。

### 已知问题

-  `clock_gettime64` 系统调用在 i386 镜像中返回 `EPERM` 而不是 `ENOSYS`。要解决此问题，请使用 `--privileged` 标志禁用 `seccomp`。参见 [docker/for-win#8326](https://github.com/docker/for-win/issues/8326)。

## Docker Desktop Community 2.3.0.4
2020-07-27

### 升级

- [Docker 19.03.12](https://github.com/docker/docker-ce/releases/tag/v19.03.12)
- [Docker Compose 1.26.2](https://github.com/docker/compose/releases/tag/1.26.2)
- [Go 1.13.14](https://github.com/golang/go/issues?q=milestone%3AGo1.13.14+label%3ACherryPickApproved)

### Bug 修复和次要更改

- Docker Desktop 现在会提示用户共享像 `////c/Users/foo` 这样的路径，而不仅仅是像 `C:\Users\foo` 和 `C:/Users/foo` 这样的路径。
- 安装程序现在在出错或用户取消安装时返回非零退出代码。
- 修复了当用户名包含空格时安装程序日志文件默认位置的路径。修复 [docker/for-win#6552](https://github.com/docker/for-win/issues/6552)
- 仪表板：修复了为 Windows 容器打开 CLI 的问题。参见 [docker/for-win#7079](https://github.com/docker/for-win/issues/7079)
- 仪表板：修复了容器日志有时被截断的问题。修复 [docker/for-win#5954](https://github.com/docker/for-win/issues/5954)
- WSL 2：修复了更改用户默认 shell 会阻止 WSL 集成的问题。修复 [docker/for-win#7653](https://github.com/docker/for-win/issues/7653)
- WSL 2：修复了恢复卡在“正在安装”状态的 WSL 发行版的问题。

## Docker Desktop Community 2.3.0.3
2020-05-27

### 升级

- [Linux kernel 4.19.76](https://hub.docker.com/layers/docker/for-desktop-kernel/4.19.76-83885d3b4cff391813f4262099b36a529bca2df8-amd64/images/sha256-0214b82436af70054e013ea51cb1fea72bd943d0d6245b6521f1ff09a505c40f?context=repo)

### Bug 修复和次要更改

- 修复了在禁用 Hyper-V 时恢复出厂默认设置导致的崩溃。修复 [docker/for-win#6738](https://github.com/docker/for-win/issues/6738)。
- 修复了从 WSL 2 运行的应用程序中在 VS Code 中打开应用程序的问题。修复 [docker/for-win#6472](https://github.com/docker/for-win/issues/6472)。
- 修复了 WSL 2 中的 Swarm 挂载。修复 [docker/for-win#6507](https://github.com/docker/for-win/issues/6507)。
- 修复了使用 Microsoft `mssql` 镜像时的错误。修复 [docker/for-win#6646](https://github.com/docker/for-win/issues/6646)
- 为共享文件系统实现了 `fallocate`。参见 [docker/for-win#6658](https://github.com/docker/for-win/issues/6658#issuecomment-627736820)
- 修复了当系统上存在旧的和/或部分卸载的 Docker Desktop 版本时安装程序崩溃的问题。修复 [docker/for-win#6536](https://github.com/docker/for-win/issues/6536)。
- 修复了打开系统托盘菜单时的延迟。修复 [docker/for-win#1011](https://github.com/docker/for-win/issues/1011)。
- 修复了一个回归问题，即容器无法再使用主机驱动器字母引用挂载的文件夹。修复 [docker/for-win#6628](https://github.com/docker/for-win/issues/6628)。
- 修复了一个回归问题，即使用双前导斜杠表示法共享文件夹会失败。修复 [docker/for-win#6668](https://github.com/docker/for-win/issues/6668)。
- 重新将 device-mapper 添加到嵌入式 Linux 内核中。修复 [docker/for-mac#4549](https://github.com/docker/for-mac/issues/4549)。
- 修复了导致绑定挂载中的 `:z` 属性失败的问题。修复 [docker/for-win#6634](https://github.com/docker/for-win/issues/6634)。

## Docker Desktop Community 2.3.0.2
2020-05-11

### 新增功能

- Windows 10 Home 用户现在可以通过 WSL 2 使用 Docker Desktop。这需要 Windows 10 版本 2004 或更高版本。有关更多信息，请参阅 [在 Windows 上安装 Docker Desktop](/manuals/desktop/setup/install/windows-install.md)。
- Docker Desktop 在首次启动时引入了新的入门教程。快速入门教程指导用户通过几个简单的步骤开始使用 Docker。它包括一个简单的练习，用于构建示例 Docker 镜像，将其作为容器运行，推送到 Docker Hub 并保存。
- Docker Desktop 现在允许共享单个文件夹，而不是整个驱动器，让用户对共享内容有更多控制。

### 升级

- [Docker Compose 1.25.5](https://github.com/docker/compose/releases/tag/1.25.5)
- [Go 1.13.10](https://github.com/golang/go/issues?q=milestone%3AGo1.13.10+label%3ACherryPickApproved)
- [Linux kernel 4.19.76](https://hub.docker.com/layers/docker/for-desktop-kernel/4.19.76-ce15f646db9b062dc947cfc0c1deab019fa63f96-amd64/images/sha256-6c252199aee548e4bdc8457e0a068e7d8e81c2649d4c1e26e4150daa253a85d8?context=repo)
- LinuxKit [init](https://hub.docker.com/layers/linuxkit/init/1a80a9907b35b9a808e7868ffb7b0da29ee64a95/images/sha256-64cc8fa50d63940dbaa9979a13c362c89ecb4439bcb3ab22c40d300b9c0b597e?context=explore), [runc](https://hub.docker.com/layers/linuxkit/runc/69b4a35eaa22eba4990ee52cccc8f48f6c08ed03/images/sha256-57e3c7cbd96790990cf87d7b0f30f459ea0b6f9768b03b32a89b832b73546280?context=explore) 和 [containerd](https://hub.docker.com/layers/linuxkit/containerd/09553963ed9da626c25cf8acdf6d62ec37645412/images/sha256-866be7edb0598430709f88d0e1c6ed7bfd4a397b5ed220e1f793ee9067255ff1?context=explore)

### Bug 修复和次要更改

**WSL 2**

- Docker Desktop 仅在 Windows 端口可用时才在 Linux 中暴露主机端口。
- Docker Desktop 现在允许用户刷新发行版列表。
- Docker Desktop 在兼容的操作系统版本上安装时默认使用 WSL 2。
- Docker Desktop 检测缺少的 Linux 内核，并添加指向 Microsoft 文档的指针以下载内核。
- 检测到 WSL 2 后端停止时，允许用户重新启动它。
- 添加了对 WSL 2 绑定挂载的 `chmod/chown` 支持。修复 [docker/for-win#6284](https://github.com/docker/for-win/issues/6284)。
- 添加了检查 BIOS 中是否启用了虚拟化。

**文件共享**

- 修复了重命名共享文件夹的父目录会导致虚假的“找不到文件”错误的错误。修复 [docker/for-win#6200](https://github.com/docker/for-win/issues/6200)。
- 修复了字母加两位数的根文件夹名称导致 docker-compose 无法在卷内创建目录的错误。修复 [docker/for-win#6248](https://github.com/docker/for-win/issues/6248)。
- 修复了一个错误，该错误在负载下且容器重新启动时阻止容器看到共享卷上的文件更新。修复 [docker/for-win#5530](https://github.com/docker/for-win/issues/5530#issuecomment-608804192)。
- 修复了主机路径被错误地转换为 VM 路径的错误。修复 [docker/for-win#6209](https://github.com/docker/for-win/issues/6209)。
- 修复了在长路径（> 260 个字符）上接收文件事件的错误。修复 [docker/for-win#6337](https://github.com/docker/for-win/issues/6337)。
- Docker Desktop 将有效的目录联合作为目录（而不是符号链接）表示，并正确处理缓存失效和事件注入。修复 [docker/for-win#5582](https://github.com/docker/for-win/issues/5582)。

**其他修复**

- 将 Docker Desktop 安装程序的大小从 960 MB 减少到 409 MB。
- 在“故障排除”屏幕中添加了删除数据的选项。
- 修复了当 Kubernetes 上下文无效时容器从 UI 中消失的错误。修复 [docker/for-win#6037](https://github.com/docker/for-win/issues/6037)。
- 修复了将 Windows 事件日志复制到 Docker Desktop 日志文件时的过滤问题。修复 [docker/for-win#6258](https://github.com/docker/for-win/issues/6258)。
- 修复了 `vpnkit-bridge` 中的句柄泄漏。修复 [docker/for-win#5841](https://github.com/docker/for-win/issues/5841)
- 修复了移除 Docker Desktop 虚拟交换机时的错误。
- 从 UI 添加了指向 Edge 频道的链接。
- 使嵌入式终端可调整大小。
- 修复了一个错误，该错误仅在应用程序重新启动时才尊重 Docker 引擎 API 的 `expose on TCP` 设置。现在单击“应用”按钮后设置就会生效。
- 修复了如果用户名包含空格，诊断上传会失败的错误。
- Docker Desktop 现在在启动时读取 Hyper-V VM 磁盘最大大小，并将其用作在设置中显示的值。
- 修复了 Docker Desktop UI 可以在没有引擎的情况下启动的错误。修复 [docker/for-win#5376](https://github.com/docker/for-win/issues/5376)。
- Docker Desktop 现在使用最小的权限来查询服务器服务。修复 [docker/for-win#5150](https://github.com/docker/for-win/issues/5150)。
- 修复了容器端口无法在特定主机 IP 上暴露的问题。参见 [docker/for-win#5546](https://github.com/docker/for-mac/issues/5546)。
- 从仪表板中移除了端口探测，只是无条件地显示应可用端口的链接。修复 [docker/for-win#5903](https://github.com/docker/for-win/issues/5903)。
- 为了节省磁盘空间，已从 Docker Desktop 中移除了 Ceph 支持。
- 修复了导致 Windows 日志文件归档无限增长的问题。修复 [docker/for-win#5113](https://github.com/docker/for-win/issues/5113)。
- 在安装程序中添加了对 LanmanServer 服务的先决条件检查。修复 [docker/for-win#5150](https://github.com/docker/for-win/issues/5150)

### 已知问题

- 如果您在实验性的 Windows 上 Linux 容器 (LCOW) 模式下运行 Docker Desktop，某些 CLI 命令会失败。作为替代方案，我们建议运行传统的 Linux 容器，或 [WSL 2 后端](/manuals/desktop/features/wsl/_index.md)。

**WSL 2**

- Swarm 服务绑定挂载并不总是正确恢复。
- 当多个容器挂载位于根挂载点之外的文件（位于 `/mnt/c`、`/tmp`、`/run...` 中的文件）时，绑定挂载无法正常工作。

## Docker Desktop Community 2.2.0.5
2020-04-02

### Bug 修复和次要更改

- 当主机上的文件更改时，Docker Desktop 在 Linux 容器中生成 `fsnotify.WRITE` 事件。修复 [docker/for-win#5530](https://github.com/docker/for-win/issues/5530#issuecomment-585572414)。
- 修复了使用 "mfsymlinks" 的共享卷上 `readlink` 的竞争条件。修复 [docker/for-win#5793](https://github.com/docker/for-win/issues/5793)。
- 使 VM 时间同步更可靠。参见 [docker/for-win#4526](https://github.com/docker/for-win/issues/4526)。
- 修复了在 `docker-compose.yml` 中使用 `volumes_from` 时共享卷中文件不更改的错误。参见 [docker/for-win#5530](https://github.com/docker/for-win/issues/5530)。
- 修复了打开只读文件会因 `Operation not permitted` 错误而失败的错误。修复 [docker/for-win#6016](https://github.com/docker/for-win/issues/6016) 和 [docker/for-win#6017](https://github.com/docker/for-win/issues/6017)。

## Docker Desktop Community 2.2.0.4
2020-03-13

### 升级

- [Docker 19.03.8](https://github.com/docker/docker-ce/releases/tag/v19.03.8)

### Bug 修复和次要更改

- 安全性：诊断是使用管理员权限收集的，这在 Docker Desktop 用户不是管理员的系统上可能导致可能的权限升级。
- Docker Desktop 现在在共享卷中显示隐藏文件。修复 [docker/for-win#5808](https://github.com/docker/for-win/issues/5808)。
- Docker Desktop 现在为 Windows 文件共享在共享文件系统上生成 inotify `MODIFY` 事件。修复 [docker/for-win#5530](https://github.com/docker/for-win/issues/5530)。
- 尝试在共享卷中创建具有相同文件名但大小写不同（大写/小写）的文件现在将失败并显示 `EEXIST` 错误。修复 [docker/for-win#5894](https://github.com/docker/for-win/issues/5894)。
- 修复了主机路径长于 260 个字符的共享卷中的缓存失效和事件注入。
- Docker Desktop 现在允许用户重命名共享卷中的打开文件。修复 [docker/for-win#5565](https://github.com/docker/for-win/issues/5565)。
- 修复了导致 Docker Desktop 仪表板尝试连接到容器内所有暴露端口的问题。修复 [docker/for-win#5903](https://github.com/docker/for-win/issues/5903)。
- Kubernetes：由声明创建的持久卷现在存储在虚拟机中。修复 [docker/for-win#5665](https://github.com/docker/for-win/issues/5665)。
- 修复了当用户尝试恢复出厂默认设置时导致 Docker Desktop 挂起的问题。
- 修复了导致 Docker Desktop 锁定随机文件的文件共享问题。修复 [docker/for-win#5624](https://github.com/docker/for-win/issues/5624) 和 [docker/for-win#5575](https://github.com/docker/for-win/issues/5575)。

### 已知问题

- 如果您在实验性的 Windows 上 Linux 容器 (LCOW) 模式下运行 Docker Desktop，某些 CLI 命令会失败。作为替代方案，我们建议运行传统的 Linux 容器，或实验性的 [WSL 后端](/manuals/desktop/features/wsl/_index.md)。
- 无法使用 Docker Desktop **设置** UI 调整磁盘映像的大小。如果要更新磁盘映像的大小（例如，更新为 128 GB），请在 PowerShell 中运行以下命令：

  ```powershell
  Resize-VHD -Path 'C:\ProgramData\DockerDesktop\vm-data\DockerDesktop.vhdx' -SizeBytes 128gb
  ```

## Docker Desktop Community 2.3.0.3
2020-02-11

### 升级

- [Docker Compose 1.25.4](https://github.com/docker/compose/releases/tag/1.25.4)
- [Go 1.12.16](https://golang.org/doc/devel/release.html#go1.12)

### Bug 修复和次要更改

- 修复了阻止用户在共享卷中创建带有特殊字符文件名的文件的问题。修复 [docker/for-win#5520](https://github.com/docker/for-win/issues/5520)。
- 修复了处理 `docker-compose.yml` 中带有相对路径的共享卷的问题。修复 [docker/for-win#5516](https://github.com/docker/for-win/issues/5516)。
- 修复了处理路径大小写（大写/小写）与主机不完全匹配的共享卷的问题。修复 [docker/for-win#5516](https://github.com/docker/for-win/issues/5516)。
- 修复了在 Windows 文件系统中更改文件不会更新容器内文件的问题。修复 [docker/for-win#5530](https://github.com/docker/for-win/issues/5530) 和 [docker/for-win#5550](https://github.com/docker/for-win/issues/5550)。
- 修复了阻止用户共享驱动器并有时错误地提示用户输入文件系统凭据的问题。修复 [docker/for-win#5567](https://github.com/docker/for-win/issues/5567)。
- 修复了阻止用户挂载嵌套卷的问题。修复 [docker/for-win#5540](https://github.com/docker/for-win/issues/5540)。
- 修复了绑定挂载上的文件同步问题。修复 [docker/for-win#5533](https://github.com/docker/for-win/issues/5533)。
- 修复了共享卷中文件时间戳重置为零的问题。修复 [docker/for-win#5528](https://github.com/docker/for-win/issues/5528) 和 [docker/for-win#5543](https://github.com/docker/for-win/issues/5543)。
- 修复了当共享文件路径长于 260 个字符时导致 Docker Desktop 失败的错误。修复 [docker/for-win#5572](https://github.com/docker/for-win/issues/5572)。
- 修复了如果共享卷中存在符号链接，某些用户无法启动容器的问题。修复 [docker/for-win#5582](https://github.com/docker/for-win/issues/5582)。
- 修复了用户无法通过 Docker Desktop UI 修改**手动代理配置**设置的错误。修复 [docker/for-win#5606](https://github.com/docker/for
