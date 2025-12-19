---
description: 各边缘版本更新日志 / 发布说明
keywords: Docker Desktop for Windows, edge, release notes
title: Docker Desktop for Windows Edge 版本发布说明
toc_min: 1
toc_max: 2
aliases:
- /desktop/windows/release-notes/edge-releases/
sitemap: false
---

此页面包含 Docker Desktop Edge 版本的相关信息。Edge 版本可让您抢先体验我们的最新功能。请注意，部分功能可能仍处于实验阶段，甚至可能永远不会进入稳定版发布。

有关 Docker Desktop 系统要求，请参阅
[安装前须知](/manuals/desktop/setup/install/windows-install.md#system-requirements)。

## Docker Desktop Community 2.5.4
2020-12-07

### 升级项

- [Docker Engine 20.10.0-rc2](https://github.com/docker/docker-ce/blob/master/CHANGELOG.md#20100)
- [Go 1.15.6](https://github.com/golang/go/issues?q=milestone%3AGo1.15.6+label%3ACherryPickApproved+)

### Bug 修复与小幅改动

- 修复了当前用户非管理员时后台更新失败的问题。
- 将内核降级至 [4.19.121](https://hub.docker.com/layers/docker/for-desktop-kernel/4.19.121-2a1dbedf3f998dac347c499808d7c7e029fbc4d3-amd64/images/sha256-4e7d94522be4f25f1fbb626d5a0142cbb6e785f37e437f6fd4285e64a199883a?context=repo)，以降低 hyperkit 的 CPU 占用率。修复了 [docker/for-mac#5044](https://github.com/docker/for-mac/issues/5044)

## Docker Desktop Community 2.5.3
2020-11-30

### 升级项

- [Compose CLI v1.0.3](https://github.com/docker/compose-cli/releases/tag/v1.0.3)

## Docker Desktop Community 2.5.2
2020-11-26

### 新增功能

- 采用三位数字版本号。
- 自 Docker Desktop 2.5.2 起，更新将使用增量补丁方式应用，体积更小。

### Bug 修复与小幅改动

- 修复了尝试以 `-v /var/run/docker.sock:` 启动不存在的容器时出现的意外 EOF 错误。参见 [docker/for-mac#5025](https://github.com/docker/for-mac/issues/5025)。

## Docker Desktop Community 2.5.1.0
2020-11-18

此版本包含 Kubernetes 升级。请注意，安装 Docker Desktop 后本地 Kubernetes 集群将被重置。

### 升级项

- [Docker Engine 20.10.0-rc1](https://github.com/docker/docker-ce/blob/master/CHANGELOG.md#20100)
- [Compose CLI v1.0.2](https://github.com/docker/compose-cli/releases/tag/v1.0.2)
- [Snyk v1.424.4](https://github.com/snyk/snyk/releases/tag/v1.424.4)
- [Kubernetes 1.19.3](https://github.com/kubernetes/kubernetes/releases/tag/v1.19.3)

### Bug 修复与小幅改动

- 将“运行诊断”重命名为“获取支持”。
- 修复了 WSL 2 后端中某些网络插件可能加载失败导致 Docker 守护进程崩溃的问题。
- 修复了尝试启动不存在的容器时出现的意外 EOF 错误。参见 [docker/for-mac#5025](https://github.com/docker/for-mac/issues/5025)。

## Docker Desktop Community 2.4.2.0
2020-10-19

### 新增功能

- 若您已在 Docker Hub 启用[漏洞扫描](../../docker-hub/repos/manage/vulnerability-scanning.md)，扫描结果现在将显示在 Docker Desktop 中。

### 升级项

- [Docker Engine 20.10.0 beta1](https://github.com/docker/docker-ce/blob/0fc7084265b3786a5867ec311d3f916af7bf7a23/CHANGELOG.md)
- [Docker Compose CLI - 0.1.22](https://github.com/docker/compose-cli/releases/tag/v0.1.22)
- [Linux kernel 5.4.39](https://hub.docker.com/layers/linuxkit/kernel/5.4.39-f39f83d0d475b274938c86eaa796022bfc7063d2/images/sha256-8614670219aca0bb276d4749e479591b60cd348abc770ac9ecd09ee4c1575405?context=explore)
- [Kubernetes 1.19.2](https://github.com/kubernetes/kubernetes/releases/tag/v1.19.2)
- [Go 1.15.2](https://github.com/golang/go/issues?q=milestone:Go1.15.2+label:CherryPickApproved)

* 弃用项
  - 不再支持在 Windows 1703 (build 15063) 上安装 Docker Desktop。

### Bug 修复与小幅改动

- 修复了 WSL 2 后端间歇性启动失败的问题。
- 修复了 NFS 挂载相关问题。参见 [docker/for-mac#4958](https://github.com/docker/for-mac/issues/4958)。
- 修复了 http 代理排除列表中包含 `localhost` 或 `127.0.0.1` 等条目时的问题。修复了 [docker/for-win#8750](https://github.com/docker/for-win/issues/8750)。
- 当 WSL 集成进程意外停止时，现在会通知用户并可选择是否重启，而非无限循环尝试重启。修复了 [docker/for-win#8968](https://github.com/docker/for-win/issues/8968)。
- 修复了高负载下容器日志滞后的问题。修复了 [docker/for-win#8216](https://github.com/docker/for-win/issues/8216)。
- 诊断：避免 Kubernetes 处于损坏状态时挂起。
- 向容器共享文件时（如 `docker run -v ~/.gitconfig`），Docker Desktop 不再监视父目录。修复了 [docker/for-mac#4981](https://github.com/docker/for-mac/issues/4981)。
- 容器启动时始终同步刷新文件系统缓存。参见 [docker/for-mac#4943](https://github.com/docker/for-mac/issues/4943)。

## Docker Desktop Community 2.4.1.0
2020-10-01

### 升级项

- [Docker Compose CLI - 0.1.18](https://github.com/docker/compose-cli)
- [Docker Compose 1.27.4](https://github.com/docker/compose/releases/tag/1.27.4)
- [Snyk v1.399.1](https://github.com/snyk/snyk/releases/tag/v1.399.1)
- [Docker Engine 19.03.13](https://github.com/docker/docker-ce/releases/tag/v19.03.13)

### Bug 修复与小幅改动

- 修复了用户名包含空格时安装日志文件默认路径错误的问题。修复了 [docker/for-win#7941](https://github.com/docker/for-win/issues/7941)。

## Docker Desktop Community 2.3.7.0
2020-09-17

### 新增功能

- [Amazon ECR 凭证助手](https://github.com/awslabs/amazon-ecr-credential-helper/releases/tag/v0.4.0)

### 升级项

- [Docker ACI 集成 0.1.15](https://github.com/docker/aci-integration-beta/releases/tag/v0.1.15)
- [Snyk v0.393.0](https://github.com/snyk/snyk/releases/tag/v1.393.0)

### Bug 修复与小幅改动

**WSL 2**

  - 修复了后端间歇性启动失败的问题。
  - 修复了 glibc 不兼容时导致的代理崩溃问题。参见 [docker/for-win#8183](https://github.com/docker/for-win/issues/8183)。
  - 修复了重启 Docker Desktop 可能删除容器中挂载文件的问题。
  - 修复了重启 Docker Desktop 时单个文件挂载到容器中文件被截断的问题。参见 [docker/for-win#8439](https://github.com/docker/for-win/issues/8439)。

**其他修复**

- 修复了用于底层调试的 VM 调试 shell。
- 修复了与 Go 1.15 客户端的兼容性问题。参见 [docker/for-mac#4855](https://github.com/docker/for-mac/issues/4855)。
- 避免在 `docker container inspect` 和 `docker volume inspect` 中暴露 `/host_mnt` 路径。修复了 [docker/for-mac#4859](https://github.com/docker/for-mac/issues/4859)。
- 修复了高负载下容器日志滞后的问题。参见 [docker/for-win#8216](https://github.com/docker/for-win/issues/8216)。

### 已知问题

- 在 i386 镜像中，`clock_gettime64` 系统调用返回 `EPERM` 而非 `ENOSYS`。
为解决此问题，请使用 `--privileged` 标志禁用 `seccomp`。参见 [docker/for-win#8326](https://github.com/docker/for-win/issues/8326)。

## Docker Desktop Community 2.3.6.2
2020-09-09

### 升级项

- [Docker Compose 1.27.0](https://github.com/docker/compose/releases/tag/1.27.0)

### Bug 修复与小幅改动

- 修复了 WSL 2 中挂载遮蔽的问题。参见 [docker/for-win#8183](https://github.com/docker/for-win/issues/8183) 和 [docker/for-win#8316](https://github.com/docker/for-win/issues/8316)。

## Docker Desktop Community 2.3.6.0
2020-09-01

### 新增功能

- 与 Snyk 合作，Docker Desktop 为本地镜像推出漏洞扫描功能。
- Docker ECS 插件已被 ECS 云集成取代。
- Docker UI：
  - 镜像视图现在支持搜索和筛选选项。
  - 您现在可通过远程仓库下拉菜单将镜像推送至 Docker Hub。

### 升级项

- [Alpine 3.12](https://alpinelinux.org/posts/Alpine-3.12.0-released.html)
- [Kubernetes 1.18.8](https://github.com/kubernetes/kubernetes/releases/tag/v1.18.8)

### Bug 修复与小幅改动

- 修复了 Docker Desktop 与其他 WSL 2 发行版集成的问题。参见 [docker/for-win#6894](https://github.com/docker/for-win/issues/6894)
- 修复了短名称 DNS 解析问题。参见 [docker/for-win#4425](https://github.com/docker/for-win/issues/4425)

## Docker Desktop Community 2.3.5.1
2020-08-25

### Bug 修复与小幅改动

- 修复了停止 Docker Desktop 时存在绑定挂载的容器导致 WSL 2 集成中断的问题。参见 [docker/for-win#8164](https://github.com/docker/for-win/issues/8164)

## Docker Desktop Community 2.3.5.0
2020-08-20

### 新增功能

- 仪表板上的 **镜像** 视图现在允许您与 Docker Hub 上的镜像交互。您现在可从 Docker Hub 拉取带特定标签的远程仓库，或查看仓库在 Docker Hub 页面上的详细信息。要访问新的镜像视图，请从 Docker 菜单选择 **仪表板** > **镜像**。

- Docker Desktop 现在在恢复出厂设置后默认启用 BuildKit。要恢复旧的 docker build 体验，请前往 **偏好设置** > **Docker Engine** 并禁用 BuildKit 功能。

- Docker Desktop 现在支持在 Windows 10 1903 和 1909 版本的最新更新（除现有对 2004 版本的支持外）上通过 WSL 2 运行。这也意味着 Docker Desktop 可安装在 Windows 10 家庭版的这些构建版本上。

### 升级项

- [Go 1.14.7](https://github.com/golang/go/issues?q=milestone:Go1.14.7+label:CherryPickApproved)
- [Docker ECS 集成 v1.0.0-beta.5](https://github.com/docker/ecs-plugin/releases/tag/v1.0.0-beta.5)
- [Docker Engine 19.03.13-beta2](https://github.com/docker/docker-ce/releases/tag/v19.03.13-beta2)
- [Docker ACI 集成 0.1.12](https://github.com/docker/aci-integration-beta/releases/tag/v0.1.12)

### Bug 修复与小幅改动

- 将 **仪表板** 移至鲸鱼菜单顶部。
- 系统托盘图标现在响应深色或浅色模式。参见 [docker/for-win#4113](https://github.com/docker/for-win/issues/4113)
- 改进了 `dockerd` 崩溃时的错误处理。
- 修复了 **镜像** 视图中的小 bug。

## Docker Desktop Community 2.3.4.0
2020-07-28

### 新增功能

- Docker Desktop 为 Docker 仪表板引入了新的 **镜像** 视图。镜像视图允许用户查看磁盘上的 Docker 镜像列表，将镜像作为容器运行，从 Docker Hub 拉取镜像的最新版本，检查镜像，并从磁盘删除不需要的镜像。

  要访问新的镜像视图，请从 Docker 菜单选择 **仪表板** > **镜像**。

### 升级项

- [Docker ECS 集成 v1.0.0-beta.4](https://github.com/docker/ecs-plugin/releases/tag/v1.0.0-beta.4)
- [Kubernetes 1.18.6](https://github.com/kubernetes/kubernetes/releases/tag/v1.18.6)

### Bug 修复与小幅改动

- UI 根据 Windows 默认应用模式切换深色或浅色主题。
- 从仪表板复制容器日志时不再将 ANSI 颜色代码复制到剪贴板。

## Docker Desktop Community 2.3.3.2
2020-07-21

### 升级项

- [Docker ECS 集成 v1.0.0-beta.2](https://github.com/docker/ecs-plugin/releases/tag/v1.0.0-beta.2)
- [Docker ACI 集成 0.1.10](https://github.com/docker/aci-integration-beta/releases/tag/v0.1.10)

## Docker Desktop Community 2.3.3.1
2020-07-10

### Bug 修复与小幅改动

- 修复了 ECS 插件在 WSL 2 中不可见的问题。

## Docker Desktop Community 2.3.3.0
2020-07-09

### 升级项

- Docker ECS 集成 v1.0.0-beta.1 测试版发布。
- [Docker ACI 集成 v0.1.7](https://github.com/docker/aci-integration-beta/releases/tag/v0.1.7)
- [Docker Compose 1.26.2](https://github.com/docker/compose/releases/tag/1.26.2)

### Bug 修复与小幅改动

- Compose-on-Kubernetes 不再包含在 Docker Desktop 安装程序中。您可单独从 compose-on-kubernetes [发布页面](https://github.com/docker/compose-on-kubernetes/releases) 下载。

## Docker Desktop Community 2.3.2.1
2020-06-29

### 安全性

- 修复了 Windows 上 Docker Desktop Edge 2.3.2.0 中将 Docker API 默认暴露在随机端口所有接口上的回归问题。

## Docker Desktop Community 2.3.2.0
2020-06-25

### 升级项

- [Docker 19.03.12](https://github.com/docker/docker-ce/releases/tag/v19.03.12)
- [Docker Compose 1.26.0](https://github.com/docker/compose/releases/tag/1.26.0)
- [Kubernetes 1.18.3](https://github.com/kubernetes/kubernetes/releases/tag/v1.18.3)
- [Docker ACI 集成](/engine/context/aci-integration/) 测试版发布

### Bug 修复与小幅改动

- 修复了若 Docker `daemon.json` 中指定了 `hosts` 则应用启动失败的问题。参见 [docker/for-win#6895](https://github.com/docker/for-win/issues/6895#issuecomment-637429117)。
- 修复了从仪表板为 Windows 容器打开 CLI 的问题。参见 [docker/for-win#7079](https://github.com/docker/for-win/issues/7079)。
- 修复了在设置中向不存在的驱动器添加文件夹会创建空条目的问题。参见 [docker/for-win#6797](https://github.com/docker/for-win/issues/6797)。
- 修复了将 Windows 更新至支持 WSL 2 的版本时配置文件被旧 Hyper-V VM 锁定的问题。
- 将应用固定到任务栏并点击它，若 Docker 已在运行则将启动容器视图。
- 现在左键单击系统托盘中的 Docker 图标将启动容器视图仪表板。参见 [docker/for-win#6650](https://github.com/docker/for-win/issues/6650)。
- 修复了若 `localhost:2375` 被其他程序使用则 Docker Desktop 启动被阻止的问题。参见 [docker/for-win#6929](https://github.com/docker/for-win/issues/6929) 和 [docker/for-win#6961](https://github.com/docker/for-win/issues/6961)。
- Docker 上下文现在在 Windows 和 WSL 2 发行版之间同步。
- Docker Desktop 现在提示用户共享类似 `////c/Users/foo` 路径的驱动器，而不仅限于 `C:\Users\foo` 和 `C:/Users/foo` 等路径。
- 安装程序现在在出错或用户取消安装时返回非零退出代码。
- 避免因文件 I/O 在共享卷上出现 `Function not implemented` 错误导致失败。修复了 [docker/for-win#5955](https://github.com/docker/for-win/issues/5955)。
- 修复了绑定挂载容器内已挂载主机目录时的问题。参见 [docker/for-win#5089](https://github.com/docker/for-win/issues/5089)。
- 移除了遗留的 Kubernetes 上下文 `docker-for-desktop`。应改用上下文 `docker-desktop`。参见 [docker/for-win#5089](https://github.com/docker/for-win/issues/5089)。

## Docker Desktop Community 2.3.1.0
2020-05-20

### 升级项

- [Docker Compose 1.26.0-rc4](https://github.com/docker/compose/releases/tag/1.26.0-rc4)
- 升级至 Qemu 4.2.0，添加 Risc-V 支持

### Bug 修复与小幅改动

**Hyper-V**

- 在 VM 启动时创建驱动器符号链接，避免破坏使用它们的设置。修复了 [docker/for-win#6628](https://github.com/docker/for-win/issues/6628)。
- 为共享文件系统实现 `fallocate`。参见 [docker/for-win#6658](https://github.com/docker/for-win/issues/6658#issuecomment-627736820)。

**WSL 2**

- 配置 CLI 使用 Docker Desktop 凭证存储。
- 在提示用户安装 Linux 内核的弹窗中添加重启按钮。
- 更可靠的引导，不依赖 `wslpath` 进行路径转换，启动时出错重试挂载。

**仪表板**

- 修复了容器日志有时被截断的问题。修复了 [docker/for-win#5954](https://github.com/docker/for-win/issues/5954)
- 修复了从 WSL 2 Linux 工作区部署的 compose 应用的 `open with vs code` 按钮。

**其他修复**

- 修复了系统存在旧版本和/或部分卸载的 Docker Desktop 时安装程序崩溃的问题。[修复了 docker/for-win/6536](https://github.com/docker/for-win/issues/6536)。
- 修复了在绑定挂载源中使用波浪号（如 `-v ~/dir:/vm-dir`）时的主目录扩展问题。
- `localhost` 和 `127.0.0.1` 现在都可用于代理设置以重定向到主机上的代理。修复了 [docker/for-win#5715](https://github.com/docker/for-win/issues/5715)。
- 修复了后端销毁通知中的拼写错误。修复了 [docker/for-win#6739](https://github.com/docker/for-win/issues/6739)。
- 修复了 Docker Desktop 加载损坏的 Docker CLI 配置文件时有时崩溃的问题。修复了 [docker/for-win#6657](https://github.com/docker/for-win/issues/6657)。
- 修复了打开系统托盘菜单时的延迟问题。修复了 [docker/for-win#1011](https://github.com/docker/for-win/issues/1011)。

### 已知问题

**WSL 2**

- Swarm 服务绑定挂载并非总能正确恢复。
- 在根挂载点之外的文件（`/mnt/c`、`/tmp`、`/run...` 内的文件）的绑定挂载在多个容器挂载它们时无法正常工作。

## Docker Desktop Community 2.3.0.1
2020-04-28

### Bug 修复与小幅改动

- 修复了仍使用基于 PowerShell 的 VM 管理体验的用户在升级时遭遇静默卸载崩溃导致 Docker Desktop 被卸载而非升级的问题。
- 修复了因无网络连接导致登录失败时的崩溃问题。
- 修复了处理含 `..` 字符的共享卷路径时的 bug。修复了 [docker/for-win#5375](https://github.com/docker/for-win/issues/5375)。
- WSL 2：Docker Desktop 检测到 wsl 发行版停止时显示可操作的错误消息。
- 修复了 `ftruncate` 中的 bug，该 bug 阻止 [libgit2sharp](https://github.com/libgit2/libgit2sharp) 在共享卷上克隆仓库。参见 [docker/for-win#5808](https://github.com/docker/for-win/issues/5808#issuecomment-610996272)。
- 修复了当路径包含空格时从 UI 启动和停止 Compose 应用失败的问题。

## Docker Desktop Community 2.3.0.0
2020-04-20

### 升级项

- [Docker Compose 1.25.5](https://github.com/docker/compose/releases/tag/1.25.5)
- [Go 1.13.10](https://github.com/golang/go/issues?q=milestone%3AGo1.13.10+label%3ACherryPickApproved)
- [Linux kernel 4.19.76](https://hub.docker.com/layers/docker/for-desktop-kernel/4.19.76-ce15f646db9b062dc947cfc0c1deab019fa63f96-amd64/images/sha256-6c252199aee548e4bdc8457e0a068e7d8e81c2649d4c1e26e4150daa253a85d8?context=repo)
- LinuxKit [init](https://hub.docker.com/layers/linuxkit/init/1a80a9907b35b9a808e7868ffb7b0da29ee64a95/images/sha256-64cc8fa50d63940dbaa9979a13c362c89ecb4439bcb3ab22c40d300b9c0b597e?context=explore)、[runc](https://hub.docker.com/layers/linuxkit/runc/69b4a35eaa22eba4990ee52cccc8f48f6c08ed03/images/sha256-57e3c7cbd96790990cf87d7b0f30f459ea0b6f9768b03b32a89b832b73546280?context=explore) 和 [containerd](https://hub.docker.com/layers/linuxkit/containerd/09553963ed9da626c25cf8acdf6d62ec37645412/images/sha256-866be7edb0598430709f88d0e1c6ed7bfd4a397b5ed220e1f793ee9067255ff1?context=explore)

### Bug 修复与小幅改动

> Docker Desktop Edge 2.3.0.0 修复了 [docker/for-win](https://github.com/docker/for-win/issues) GitHub 仓库中报告的 10 个问题。

**WSL 2**

- 检测 WSL 2 后端何时停止并允许用户重启它。
- 添加对 WSL 2 绑定挂载上 chmod/chown 的支持。修复了 [docker/for-win#6284](https://github.com/docker/for-win/issues/6284)。
- 修复了暴露端口时的竞态条件。
- 防止 WSL 2 对话框阻塞其他窗口。
- 添加检查 BIOS 中是否启用虚拟化。

**文件共享**

- 修复了共享文件夹的父目录重命名时导致虚假 `File not found` 错误的 bug。修复了 [docker/for-win#6200](https://github.com/docker/for-win/issues/6200)。
- 修复了字母加两位数字根文件夹名称导致 Docker Compose 在卷内创建目录失败的 bug。修复了 [docker/for-win#6248](https://github.com/docker/for-win/issues/6248)。
- 修复了在高负载和容器重启时容器无法看到共享卷上文件更新的 bug。修复了 [docker/for-win#5530](https://github.com/docker/for-win/issues/5530#issuecomment-608804192)
- 修复了主机路径被错误转换为 VM 路径的 bug。修复了 [docker/for-win#6209](https://github.com/docker/for-win/issues/6209)。
- 修复了接收长路径（> 260 字符）文件事件的 bug。修复了 [docker/for-win#6337](https://github.com/docker/for-win/issues/6337)。

**其他修复**

- 修复了 Kubernetes 上下文无效时容器从 UI 消失的问题。修复了 [docker/for-win#6037](https://github.com/docker/for-win/issues/6037)。
- 修复了将 Windows 事件日志复制到 Docker Desktop 日志文件时的过滤问题。修复了 [docker/for-win#6258](https://github.com/docker/for-win/issues/6258)。
- 修复了 `vpnkit-bridge` 中的句柄泄漏。修复了 [docker/for-win#5841](https://github.com/docker/for-win/issues/5841)
- 修复了删除 Docker Desktop 虚拟交换机时的 bug。
- 在 Docker Desktop UI 中添加指向稳定版的链接。
- 在嵌入式 Linux 内核中重新启用 IPv6，因此监听 IPv6 地址再次生效。修复了 [docker/for-win#6206](https://github.com/docker/for-win/issues/6206) 和 [docker/for-mac#4415](https://github.com/docker/for-mac/issues/4415)。
- 使嵌入式终端可调整大小。
- 修复了仅在应用重启时遵守“在 TCP 上暴露”Docker 引擎 API 设置的 bug。现在点击 Apply 按钮设置即生效。
- 修复了用户名包含空格时诊断上传失败的问题。

## Docker Desktop Community 2.2.3.0
2020-04-02

### 升级项

- [Docker 19.03.8](https://github.com/docker/docker-ce/releases/tag/v19.03.8)
- [Docker Compose 1.26.0-rc3](https://github.com/docker/compose/releases/tag/1.26.0-rc3)
- [Linux 4.19.76](https://hub.docker.com/layers/docker/for-desktop-kernel/4.19.76-4e5d9e5f3bde0abf236f97e4a81b029ae0f5f6e7-amd64/images/sha256-11dc0f6ee3187088219ba1463ebb378f5093a7d98f176ddfd62dd6b741c2dd2d?context=repo)

### 新增功能

- Docker Desktop 在首次启动时引入新的入门教程。快速入门教程指导用户在几个简单步骤内开始使用 Docker。它包括一个构建示例 Docker 镜像、将其作为容器运行、推送并保存镜像到 Docker Hub 的简单练习。

### Bug 修复与小幅改动

> Docker Desktop Edge 2.2.3.0 修复了 [docker/for-win](https://github.com/docker/for-win/issues) GitHub 仓库中报告的 28 个问题。

**WSL 2**
- Docker Desktop 仅在 Windows 端口可用时才在 Linux 中暴露主机端口。
- Docker Desktop 现在允许用户刷新 Linux 发行版列表。
- Docker Desktop 在兼容的 OS 版本上安装时默认使用 WSL 2。
- Docker Desktop 检测缺失的 Linux 内核并添加指向 Microsoft 文档的指针以下载内核。

**文件共享**
- Kubernetes：由声明创建的持久卷现在存储在虚拟机中。修复了 [for-win/issues/5665](https://github.com/docker/for-win/issues/5665)。
- Docker Desktop 确保容器访问的主机路径在共享文件夹列表中。
- 修复了打开只读文件时出现 `Operation not permitted error` 的问题。修复了 [docker/for-win#6016](https://github.com/docker/for-win/issues/6016) 和 [docker/for-win#6017](https://github.com/docker/for-win/issues/6017)。
- 修复了 `docker volume create -o type=none -o o=bind -o device=C:\Some\Windows\path` 的路径处理。
- 修复了阻止删除打开文件的问题。修复了 [docker/for-win#5565](https://github.com/docker/for-win/issues/5565)。
- Docker Desktop 现在避免锁定在容器中打开的主机上的文件。
- 当主机上的文件更改时，Docker Desktop 在 Linux 容器中生成 `fsnotify.WRITE` 事件。[docker/for-win#5530](https://github.com/docker/for-win/issues/5530#issuecomment-585572414)
- Docker Desktop 现在在共享卷上显示隐藏文件。修复了 [docker/for-win#5808](https://github.com/docker/for-win/issues/5808)。
- 修复了长路径共享卷的缓存失效和事件注入。
- Docker Desktop 现在在文件创建期间正确处理大小写不敏感。
- Docker Desktop 将有效的目录连接表示为目录（而非符号链接）并正确处理缓存失效和事件注入。修复了 [docker/for-win#5582](https://github.com/docker/for-win/issues/5582)。
- 修复了共享卷上使用 "mfsymlinks" 时 `readlink` 的竞态条件。修复了 [docker/for-win#5793](https://github.com/docker/for-win/issues/5793)
- 修复了使用 docker-compose.yml 中的 `volumes_from` 时共享卷中的文件不更改的问题。修复了 [docker/for-win#5530](https://github.com/docker/for-win/issues/5530)。

**其他修复**
- 将 Docker Desktop 安装程序大小从 960 MB 减少到 400 MB。
- 在 **Troubleshoot** 屏幕添加删除容器和镜像数据的选项。
- Docker Desktop 现在在启动时读取 Hyper-V VM 磁盘最大大小并将其用作设置中显示的值。
- 修复了 Hyper-V 已用磁盘映像大小报告错误的问题。
- 修复了 Hyper-V VM 磁盘大小增加的问题。修复了 [docker/for-win#5881](https://github.com/docker/for-win/issues/5881)。
- 修复了系统休眠时容器时间漂移的问题。修复了 [docker/for-win#4526](https://github.com/docker/for-win/issues/4526)。
- 修复了 Docker Desktop UI 可在无引擎情况下启动的 bug。修复了 [docker/for-win#5376](https://github.com/docker/for-win/issues/5376)。
- Docker Desktop 现在以尽可能低的权限查询 `Server service`。修复了 [docker/for-win#5150](https://github.com/docker/for-win/issues/5150)。
- 修复了诊断上传可能静默失败的问题。
- 捕获诊断现在更快更轻松。
- 修复了无法在特定主机 IP 上暴露容器端口的问题。参见 [docker/for-win#5546](https://github.com/docker/for-mac/issues/5546)。
- 从仪表板移除端口探测，仅无条件显示应可用端口的链接。修复了 [docker/for-win#5903](https://github.com/docker/for-win/issues/5903)