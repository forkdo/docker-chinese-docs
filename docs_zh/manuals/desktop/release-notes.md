---
description: 查找适用于 Mac、Linux 和 Windows 的 Docker Desktop 发行说明。
keywords: Docker desktop, release notes, linux, mac, windows
title: Docker Desktop 发行说明
linkTitle: 发行说明
tags: [Release notes]
toc_max: 2
aliases:
- /docker-for-mac/edge-release-notes/
- /desktop/mac/release-notes/
- /docker-for-windows/edge-release-notes/
- /desktop/windows/release-notes/
- /desktop/linux/release-notes/
- /mackit/release-notes/
weight: 220
---
<!-- vale off -->

此页面包含有关 Docker Desktop 版本中的新功能、改进、已知问题和错误修复的信息。

版本会逐步推出以确保质量控制。如果您尚未获得最新版本，请稍作等待——更新通常在发布日期后的一周内可用。

Docker Desktop 的下载不提供早于最新版本 6 个月的版本。以前的发行说明可在我们的[文档存储库](https://github.com/docker/docs/tree/main/content/manuals/desktop/previous-versions)中找到。

有关更常见的问题，请参阅[常见问题解答](/manuals/desktop/troubleshoot-and-support/faqs/releases.md)。

## 4.86.0

{{< release-date date="2026-08-10" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.86.0" build_path="/236216/" >}}

### 更新

- [Docker Engine v29.7.2](https://docs.docker.com/engine/release-notes/29/#2972)
- [Docker Buildx v0.36.0](https://github.com/docker/buildx/releases/tag/v0.36.0)
- [Docker Scout CLI v1.24.0](https://github.com/docker/scout-cli/releases/tag/v1.24.0)
- [Docker Agent v1.119.0](https://github.com/docker/docker-agent/releases/tag/v1.119.0)

### 错误修复和增强

#### 适用于所有平台

- Docker VMM Beta 通过 Docker 自有的容器优化型虚拟机监控程序实现性能提升。适用于 Mac 和 Windows。
- Gordon 现在针对工具失败、策略阻止的操作以及循环检测显示具体的错误消息，而不是通用的 **Agent error**。
- 修复了引擎关闭期间未遵循容器停止超时和 `unless-stopped` 重启策略的问题。
- 修复了当代理由操作系统（而非环境变量）配置时，从 Docker Desktop 仪表板启用 Docker Offload 失败的 Bug。
- 修复了升级后启动时的崩溃问题，影响那些设置文件由非常旧的版本写入的用户。
- 修复了使用自动分配发布端口的 Swarm 服务的端口转发问题，包括主机模式任务端口和重复的 ingress 端口定义。
- 为 Gordon AI 代理的工具确认 UI 添加了三模式安全系统（Strict、Balanced、Autonomous），取代原有的二元批准/全部允许对话框，并在确认时带有风险等级标签。
- 修复了应用启动时错误 UI 内容的一闪而过，例如短暂的 "Waiting for the Docker Engine..." 屏幕或意外的从受限页面导航离开。
- 通过 VirtioFS 共享的 AF_UNIX 套接字现在可双向工作（主机到客户机以及客户机到主机）。
- 修复了重启 VM 会抢占窗口焦点的问题。

#### 适用于 Mac

- 修复了带有增强型容器隔离的 Kubernetes（kind）集群在 Docker Desktop 重启后可能无法恢复的 Bug。
- 修复了在 Apple Silicon 的 `inet` 表中 nftables `fib` 表达式以 "Operation not supported" 失败的问题。

#### 适用于 Windows

- 修复了当 Windows 安装程序无法写入其设置或企业策略文件时仍报告成功的问题。
- 修复了当 Docker Desktop 通过 Secondary Logon（run-as-user）会话启动时，Model Runner 因 `CreateJobObject: Access is denied` 而无法启动的问题。
- 更新了内置的 7-Zip 至 26.02，以避免在 Windows 上升级期间被防病毒软件隔离。

#### 适用于 Linux

- 修复了 Linux arm64 主机上因 QEMU 二进制路径解析不正确导致 Docker Desktop 无法启动的问题。

### 安全性

- 修复了 CVE-2026-17106，即 `docker container cp` 中的目标逃逸缺陷。

## 4.85.0

{{< release-date date="2026-08-03" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.85.0" build_path="/235549/" >}}

### 更新

- [Docker AI Agent v1.115.0](https://github.com/docker/docker-agent/releases/tag/v1.115.0)

### 错误修复和增强

#### 适用于所有平台

- 修复了即使用户禁用了分析功能，原生崩溃报告仍会被上传到 Bugsnag 的问题。
- 修复了在 Gordon 确认卡片中，当批准写入或编辑文件操作时，文件内容预览和差异被隐藏的问题。
- 修复了无效的 `install-settings.json` 导致在显示错误对话框前出现约 7 分钟启动延迟的问题。错误现在会立即显示。
- 修复了 Gordon 的计划模式在首条消息后静默回退到构建模式的问题，导致后续轮次以完整工具访问权限运行，尽管计划模式看似处于活动状态。
- 修复了启动时无效的 `config.json` 会将错误对话框延迟最多 7 分钟，而不是在数秒内出现的问题。
- 修复了当容器的文件观察器（inotify/fanotify）观察到绑定挂载上主机侧文件更改时，可能使 Docker Desktop 挂起的 Linux VM 内核崩溃。
- 修复了 Docker Hardened Images CLI 在将 JSON 输出到控制台时与号被编码的问题。
- 修复了由于扩展选择器在设置加载前错误地默认启用，导致启动时与扩展相关的请求失败的 Bug。
- 修复了重新加载历史多代理 Gordon 会话时子代理消息归属丢失，导致子代理消息看起来像是由主代理生成的问题。
- 修复了 Gordon 的 **清理 Docker** 建议提示，现在会先提出清理计划并等待用户确认后再移除任何资源，防止意外删除。
- 修复了 Gordon AI 计划模式开关的可见性，以准确反映后端支持情况，仅在连接的代理声明具有计划能力时才显示。

#### 适用于 Windows

- 修复了在 Windows 上尝试还原 hosts 文件时，Per-user 卸载 Docker Desktop 因未授权访问错误而失败的 Bug。
- 将 Per-user 安装模式设为从 Microsoft Store 全新安装 Docker Desktop 的默认模式，不再需要管理员权限。
- 修复了当 `docker-users` 组缺失时 Docker Desktop 崩溃的问题，现在会显示一个可恢复的组成员资格对话框。

#### 适用于 Linux

- 在增强型容器隔离容器内，移除主机绑定挂载上的文件不再因 "Value too large for data type" 而失败。

## 4.84.0

{{< release-date date="2026-07-27" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.84.0" build_path="/234817/" >}}


### 更新

- [Docker Agent v1.111.0](https://github.com/docker/docker-agent/releases/tag/v1.111.0)
- Kubernetes：
  - cri-dockerd v0.4.4
- [Docker Hardened Images CLI (`dhictl`) v0.0.7](https://github.com/docker-hardened-images/dhictl/releases/tag/v0.0.7)
- Docker Desktop CLI `v0.4.3`

### 错误修复和增强

#### 适用于所有平台

- 修复了一个 Bug，其中无效的 `~/.docker/config.json` 会导致 Docker Desktop 挂起并占用高 CPU/内存且不显示错误对话框。Docker Desktop 现在会显示错误对话框，提示用户更正该文件。
- 修复了一个阻止创建部分 Docker Hardened Images 自定义的 Bug。
- 修复了一个 Bug，其中删除无关凭据 ID 可能会意外清除 Docker Hub OAuth 令牌，导致用户被意外登出。
- 移除了在运行 `docker pull` 或 `docker buildx build` 命令后曾经出现的 Docker Scout CLI 提示。

#### 适用于 Windows

- 修复了 Windows 上一个空或格式错误的 `install-settings.json` 会导致 Docker Desktop 在启动时挂起并占用高 CPU/内存且不显示错误对话框的 Bug。
- MSI 安装程序现在会检测计算机上的 Per-user Docker Desktop 安装，并通过清晰指明受影响用户的消息阻止安装。受影响用户必须先卸载其 Per-user Docker Desktop，才能安装 MSI。
- 修复了一个 Bug，当卸载 Docker Desktop 在删除过程中途失败时，可能会永久锁定用户对其自身应用程序数据目录的访问。

## 4.83.0

{{< release-date date="2026-07-20" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.83.0" build_path="/234302/" >}}

### 更新

- Docker Desktop CLI `v0.4.2`
- [Docker Model Runner v1.2.6](https://github.com/docker/model-runner/releases/tag/v1.2.6)
- Docker Offload `v0.6.9`
- [Docker Agent v1.103.0](https://github.com/docker/docker-agent/releases/tag/v1.103.0)
- [Docker Compose v5.3.1](https://github.com/docker/compose/releases/tag/v5.3.1)
- Docker Desktop Build `v0.36.0`
- [Docker Engine v29.6.2](https://docs.docker.com/engine/release-notes/29/#2962)

### 错误修复和增强

#### 适用于所有平台

- 新增支持通过 Windows 上的 `install --user` 将 per-machine 的 Docker Desktop 安装就地迁移为 per-user 安装，保留用户数据而无需手动卸载。
- 修复了 v1.36 的 `kubectl exec` 和 `kubectl attach` 功能。
- 修复了 Docker Engine 启动失败被报告为通用的 `io: read/write on closed pipe` 错误，而非底层原因的问题。
- 修复了 **镜像** 视图在存在大量镜像时一段时间内显示可回收大小为 **0 Bytes** 的问题。
- 修复了卷列表未能按大小正确排序的问题。
- 修复了当 GPU 进程崩溃会通过自动禁用硬件加速并重启应用，从而阻止 Docker Desktop 仪表板加载的问题。
- 修复了直接从终端启动的 `docker ai` 会话在 Docker Desktop 重启时被终止的问题。
- 修复了格式错误的 `daemon.json` 会在启动时静默被默认值覆盖，导致用户丢失其自定义守护进程配置的问题。
- 在 Gordon 的权限对话框中新增了 **自定义规则** 选项卡。用户现在可以为特定命令或 MCP 工具添加允许/拒绝规则。
- 在 Gordon 的 **计划模式** 按钮、模型选择器和 **反馈/问题** 按钮上添加了脉冲式发现徽章，以帮助用户找到新功能。

#### 适用于 Mac

- 修复了陈旧的 `com.docker.virtualization` 进程可能以 `VZErrorInvalidVirtualMachineConfiguration` 错误阻止 Docker Desktop 启动新 VM 的问题。

#### 适用于 Windows

- 修复了失败的增量更新会将用户遗留在旧版本的问题，现在会自动回退到完整安装程序。
- 修复了 Windows MSI 安装程序在组件安装步骤实际失败时仍报告成功的问题。
- 修复了 Windows 安装向导在通过 DISM 启用 Windows 功能时冻结的问题。
- 修复了 Windows 安装程序中 UI 线程死锁导致在管理员安装期间注册但未运行必备服务时出现空白或挂起的窗口的问题。
- 修复了 Windows 安装程序在无法安装 Docker CLI 插件时仍静默报告成功的问题。
- 修复了 Windows 安装程序在重新链接 CLI 插件失败时会删除先前已安装的 CLI 插件的问题。
- 修复了注册表策略下载失败被静默忽略的问题，现在当管理员助手以非零代码退出时用户会看到正确的错误报告。
- 更改了 Windows 安装程序，默认选择 per-user 安装。
- 修复了 WSL 2.6.x 及更高版本上的 WSL 集成问题，其中 Docker Desktop 由于 0 字节的代理二进制文件在用户发行版中无法工作，导致 **Permission denied** 或 **Exec format error**。
- 修复了在 Resource Saver 停止 VM 后，集成 WSL 发行版中的 Docker CLI 中断的问题。当 WSL 集成处于活动状态时，VM 现在保持运行，并在启用时唤醒。修复了 [docker/desktop-feedback#522](https://github.com/docker/desktop-feedback/issues/522)。

## 4.82.0

{{< release-date date="2026-07-13" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.82.0" build_path="/233772/" >}}

### 更新

- [Docker Compose v5.3.0](https://github.com/docker/compose/releases/tag/v5.3.0)
- [Docker Agent v1.98.0](https://github.com/docker/docker-agent/releases/tag/v1.98.0)
- [Docker Scout CLI v1.23.1](https://github.com/docker/scout-cli/releases/tag/v1.23.1)

### 错误修复和增强

#### 适用于所有平台

- 在 Gordon 的回复中添加了点赞和点踩反馈按钮。用户可以直接从聊天中对回复评分或报告问题。
- 修复了一个 Bug，其中 Docker Desktop 创建的容器的停止超时被设为 1 秒，而非 Docker Engine 默认值，导致 `docker stop` 过快地终止进程。
- 修复了恢复出厂默认设置时未清除 MCP Toolkit 配置文件、目录和授权的问题。
- 修复了 Gordon 中选择的点赞/点踩反馈按钮在选择后视觉上难以区分的问题。
- 修复了恢复出厂默认设置时未清除已下载的 LLM 模型的问题。
- 修复了当代理通过 elicitation 请求自由文本输入时，Gordon 聊天区域会变空白的 Bug。
- 修复了 Kubernetes 屏幕中确认创建或删除集群后进度 UI 未立即出现的问题。
- 修复了 Docker Desktop 重启后 Kubernetes kind 集群以 **Failed to get API server port** 错误启动失败的 Bug。
- 使用 `docker pass` 时，`ls` 命令现在在所有平台上行为一致。
- 修复了因登录强制策略而登出的用户会看到通用登录提示，而非对其登出原因的清晰说明的问题。

#### 适用于 Mac

- 修复了在后端意外退出后 Docker Desktop 子进程可能残留的问题。
- 修复了主目录路径较长的用户因 Unix 套接字路径超出操作系统长度限制而导致 Docker Desktop 无法启动的问题。
- 修复了 vsock 监听器失败会显示隐晦崩溃，而非清晰的、可操作的恢复对话框的问题。

#### 适用于 Windows

- 修复了诊断包中缺失 `.log` 文件的问题，现在包含了 Docker Desktop 服务日志。
- 降低了 Docker Desktop 后台进程的优先级，并在空闲时启用 Windows 效率模式，以减少功耗和 CPU 占用。
- 修复了当 Docker Desktop 由非安装用户运行时，恢复出厂默认设置在 Hyper-V 上遗留容器和镜像的问题。
- 修复了在 wsl-bootstrap 进程意外失败时 WSL 引擎启动期间出现数分钟挂起的问题，现在会及时暴露错误。
- 修复了自动更新可能因成功安装被错误地回滚，导致 Docker Desktop 卡在 "connecting" 状态的问题。
- 修复了 Windows Hyper-V 上 vsock 监听器失败会显示隐晦崩溃，而非清晰的、可操作的恢复对话框的问题。
- 修复了在启动后立即连接 `com.docker.service` 时可能出现 **File not found** 错误的竞态条件。
- 修复了后台自动更新期间会闪现图形安装程序窗口的问题。现在更新以静默方式运行。
- 通过在执行更新前验证所下载安装程序的 Authenticode 签名，提高了安全性。
- 修复了缺失或禁用的 Windows 功能描述未显示在诊断输出中的问题。
- 改进了安装程序进度屏幕，使用单一的连续进度条，在整个安装过程中从 0% 平滑推进到 100%。
- 修复了当未设置 `HOME` 环境变量时，绑定挂载路径中的 `~` 未正确解析为 home 目录的问题。

#### 适用于 Linux

- 修复了主目录路径较长的用户因 Unix 套接字路径超出操作系统长度限制而导致 Docker Desktop 无法启动的问题。

## 4.81.0

{{< release-date date="2026-07-06" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.81.0" build_path="/232925/" >}}

### 更新

- [Docker Model Runner v1.2.5](https://github.com/docker/model-runner/releases/tag/v1.2.5)
- [Docker Agent v1.88.1](https://github.com/docker/docker-agent/releases/tag/v1.88.1)
- Docker Offload `v0.6.7`
- [Docker Compose v5.2.0](https://github.com/docker/compose/releases/tag/v5.2.0)
- [Docker Scout CLI v1.22.0](https://github.com/docker/scout-cli/releases/tag/v1.22.0)
- [DHI CLI (`dhictl`) v0.0.5](https://github.com/docker-hardened-images/dhictl/releases/tag/v0.0.5)

### 错误修复和增强

#### 适用于所有平台

- 修复了导致卷、镜像和容器无法在 Docker Desktop 仪表板中加载的错误。
- 从 Docker Desktop 中移除了已弃用的 `cagent` 二进制文件；请改用 `docker agent`。
- Kubernetes kind 集群现在可与 Registry Access Management 配合使用。
- 修复了在跨越版本号位数边界（例如 4.9.x 到 4.10.x）的版本之间升级时，未显示登录/更新提示的 Bug。
- 修复了 Ask Gordon 中工具调用权限对话框会阻塞聊天视图的问题，现将其替换为行内批准卡片，使用户能够在批准或拒绝之前阅读 Gordon 的完整消息。
- 修复了在工厂重置等情况下，构建服务崩溃可能导致 Docker Desktop 关闭的罕见问题。
- 修复了由于代理层强制对所有容器施加 1 秒超时，导致容器在正常操作中忽略用户配置的停止超时的问题。

#### 适用于 Mac

- 修复了当用户环境中包含非常长的环境变量时 Docker Desktop 无法启动的问题。
- 修复了由于 `__DATA_CONST` 段中未设置 `SG_READ_ONLY` 导致系统链接器无法加载可执行文件，从而在 Intel 机器上造成 Docker Offload 崩溃的问题。修复了 [docker/desktop-feedback#471](https://github.com/docker/desktop-feedback/issues/471)。

#### 适用于 Windows

- 修复了 Windows 上停止 Docker Desktop 会立即强制关闭 Hyper-V VM 而不等待客户机正常关闭，从而降低数据损坏风险的问题。
- 修复了 Windows 上一个 Bug，其中 `dockerd` 由于代理 URL 方案不正确导致的 TLS 握手错误，无法通过本地 HTTPS 代理连接。
- 修复了 Windows 更新在目标版本已安装后再次运行时回退并显示 **Mismatch patch version** 错误的问题。
- 修复了在 WSL 上运行时 Resource Saver 未停止 Docker 引擎的问题。
- 修复了 Docker Desktop 在无法附加 Synchronized File Shares eBPF 探针的 WSL2 内核（例如 Windows on Arm）上无法启动的回归问题。修复了 [docker/desktop-feedback#470](https://github.com/docker/desktop-feedback/issues/470)。

#### 适用于 Linux

- 修复了重置后 Docker Desktop 无法启动的 Bug。

## 4.80.0

{{< release-date date="2026-06-29" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.80.0" build_path="/232116/" >}}

### 更新

- Docker Offload `v0.6.6`
- [Docker Buildx v0.35.0](https://github.com/docker/buildx/releases/tag/v0.35.0)
- [Docker Model Runner v1.2.4](https://github.com/docker/model-runner/releases/tag/v1.2.4)
- [containerd v2.2.5](https://github.com/containerd/containerd/releases/tag/v2.2.5)
- [Docker Engine v29.6.1](https://docs.docker.com/engine/release-notes/29/#2961)
- [Runc v1.3.6](https://github.com/opencontainers/runc/releases/tag/v1.3.6)
- Kubernetes v1.36.1
   - CNI plugins v1.9.1
   - cri-tools v1.35.0
   - cri-dockerd v0.3.25
- 更新了 Kubernetes 镜像：
   - Kubeadm：
      - `docker/desktop-storage-provisioner:v4.0`
      - `docker/desktop-vpnkit-controller:v4.0`
      - `docker/desktop-kubernetes-etcd:3.6.8-0`
      - `docker/desktop-kubernetes-coredns:v1.14.2`
      - `docker/desktop-kubernetes-pause:3.10.2`
      - `docker/desktop-kubernetes-apiserver:v1.36.1`
      - `docker/desktop-kubernetes-controller-manager:v1.36.1`
      - `docker/desktop-kubernetes-scheduler:v1.36.1`
      - `docker/desktop-kubernetes-proxy:v1.36.1`
   - Kind：
      - `docker/desktop-containerd-registry-mirror:v0.0.4`
      - `docker/desktop-cloud-provider-kind:v0.6.0`
      - `envoyproxy/envoy:v1.36.7`

### 错误修复和增强

#### 适用于所有平台

- 实验性的 `docker sandbox` 插件已被移除。请迁移到 [`docker sbx`](/manuals/ai/sandboxes/_index.md)。
- 修复了磁盘空间耗尽时显示通用错误对话框，而非清晰的 **Disk full** 消息提示用户释放空间并重启的问题。
- 修复了在云上下文处于活动状态时使用 `docker -c desktop-linux`，会静默将命令路由到云引擎而非本地桌面 Linux 引擎的问题。
- 修复了一个 Bug，其中在空闲关闭后，后端会错误地报告已停止的 VM 仍在运行，尤其是在启用增强型容器隔离时。
- 修复了操作系统更新通知的时机问题，即启用了自动下载的用户是在更新可用时收到通知，而非在准备安装时收到通知。

#### 适用于 Mac

- 移除了旧版 osxfs 文件共享。仍在使用 osxfs 的用户已迁移到 VirtioFS。
- 通过不在主机上持久化（伪造的）文件所有权更改，提高了 VirtioFS 文件共享性能。对 `chown` 的调用将成功，但 `stat` 不会受到影响。

#### 适用于 Windows

- 修复了当目标目录包含来自先前被中断安装遗留的文件时，Windows 安装程序失败的问题。
- 修复了 Windows 上升级 Docker Desktop 会通过 `wsl --shutdown` 不必要地关闭并注销无关的 WSL 发行版的问题。
- 修复了 Windows 上短暂经过挂起或正在关闭状态时，Hyper-V 作业被错误报告为失败的虚假问题。
- 修复了在跨发行版 WSL 挂载被配置为 `noexec` 的机器上，WSL 引擎以 **Permission denied** 错误启动失败的问题。
- 修复了 Windows 上终端用户即使在管理员锁定了代理配置的情况下，也能覆盖 `NO_PROXY` 排除列表的问题。
- 修复了 Windows 上 Docker Desktop 在启动失败时静默消失的问题。现在会改为显示错误对话框。
- 修复了 Windows 上 Docker Desktop 显示通用的引擎启动失败，而非在较旧的 wsl.exe 不支持 --version 标志时路由到 WSL 更新恢复的问题。

## 4.79.0

{{< release-date date="2026-06-22" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.79.0" build_path="/230596/" >}}

### 更新

- [Docker Agent v1.79.0](https://github.com/docker/docker-agent/releases/tag/v1.79.0)
- `docker pass` v0.1.5
- Docker Desktop CLI v0.4.1
- Docker Offload v0.6.4

### 错误修复和增强

#### 适用于所有平台

- Gordon 改进：
   - 在 **容器**、**镜像**、**卷** 和 **构建** 选项卡的 Ask Gordon 菜单中添加了上下文感知的建议问题，在条目处于问题状态时优先显示相关诊断信息。
   - 为 Gordon 添加了 **提供反馈** 链接，方便你通过脱敏的会话预览或分享产品反馈来报告问题。
   - 修复了在 Gordon 侧边栏搜索输入框中，输入搜索查询时首次按键出现的 React 警告。
- 修复了 Docker Engine 设置编辑器在首次打开时显示压缩（minified）JSON 而非格式化 JSON 的问题。
- 修复了 VM 从空闲关闭唤醒后，紧接其后的 Docker API 调用出现虚假 500 错误的问题。
- 修复了由先前捆绑的二进制文件遗留的符号链接引起的虚假 "Integrity issue detected" 通知。
- 修复了当当前用户不是 `docker-users` 组成员时，错误屏幕上损坏的文档链接。
- 修复了导致 NVIDIA 等集成停止正常工作的 `/app/settings/grouped` API 的破坏性变更。
- 修复了 macOS Retina 显示屏上由 Gordon 登录页中的 SVG 动画引起的高 CPU 占用（约 30%）。
- 修复了 OAuth 网络错误导致 Docker Desktop 错误地将用户显示为已登出的问题。
- 修复了通过 OAuth 登录后，UI 中不会显示用户名和邮箱的问题。
- QEMU 已更新至 v10.2.3
- **日志** 视图改进：
   - 添加了复制按钮。可一次性复制所有可见的已过滤日志，或在悬停时复制单条日志条目，并遵循当前的时间戳可见性设置。
   - 通过重新组织的布局、现在可捕获容器选择和构建日志可见性的已保存筛选预设，以及持久化容器筛选状态的能力，改进了工具栏。
   - 添加了清除日志的能力。
   - 将 **复制** 和 **展开**/**折叠** 按钮合并为单个固定列，在水平滚动时保持可见，并修复了 **复制** 意外切换行详情面板的问题。
- 修复了 Registry Access Management 策略下载，通过在使用者自己的目录中获取和缓存策略并进行防篡改检测，避免 `permission denied` 错误。

#### 适用于 Windows

- 修复了一个 Bug，其中在强制终止的引导进程遗留陈旧的 rootfs 挂载后，WSL 上的 Docker Desktop 会以 "is already mounted" 错误启动失败。
- 修复了 Windows 上点击 "Quit Docker Desktop" 在后端崩溃或被杀死时无效的问题。
- 修复了 Windows 上 Docker Desktop 进程在意外退出或崩溃后可能作为孤儿进程残留的问题。
- 修复了在 Windows 上就地升级后，当 WSL 虚拟机尚未关闭时卡在 "Starting the Docker Engine…" 的问题。
- 修复了 Windows 上托盘图标与系统任务栏主题不匹配的问题，现在会显示正确的浅色或深色图标。
- 修复了 Windows 上后端启动错误仅写入日志文件的静默失败。现在当 Docker Desktop 启动失败时，用户会看到可见的错误对话框。

## 4.78.0

{{< release-date date="2026-06-15" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.78.0" build_path="/229452/" >}}

### 更新

- [Docker Agent v1.73.0](https://github.com/docker/docker-agent/releases/tag/v1.73.0)
- `docker pass` v0.1.4
- [Credential helpers v0.9.8](https://github.com/docker/docker-credential-helpers/releases/tag/v0.9.8)

### 错误修复和增强

#### 适用于所有平台

- 修复了在 Docker Desktop 仪表板中流式传输日志时，会导致 Docker Desktop 无响应或崩溃的内存不足崩溃。
- 通过重试停滞和瞬时的下载失败并从部分下载的文件继续，提高了更新的可靠性。
- 为 Gordon 工具调用添加了实时流式输出，因此像 `docker compose up` 这样的长时间运行命令会实时显示 STDOUT/STDERR，而不是等到完成才显示。
- 在 **日志** 视图中添加了颜色编码标签，使每个容器和构建来源在日志网格和容器筛选下拉列表中通过唯一颜色进行视觉区分。
- 改进了 Docker Desktop VM 启动失败时的错误消息。现在显示底层的 `VirtualizationFramework` / `libkrun` 原因，而非通用的 **Use of closed network connection**。
- 修复了 Docker Desktop 处于 Resource Saver 模式时，Docker CLI 错误消息以原始 JSON 而非人类可读文本显示的问题。
- 修复了在 **日志** 视图中取消选择容器筛选器时发生的崩溃。
- 修复了从故障排除弹出窗口访问时，支持页面被无虚拟化覆盖屏幕替换的问题。
- 修复了 Docker Desktop 在裸金属 EC2 实例（例如 `g4dn.metal`）上以 **Nested virtualization not supported** 错误启动失败的问题。
- 提高了重试延迟，以适应由防病毒软件持有文件锁导致的瞬时重命名失败。
- Gordon 现在在到 Docker 服务的出站 HTTPS 被阻止时，会显示清晰的网络错误消息，并指导检查 VPN、代理或防火墙设置，而非通用的代理错误。
- 修复了 Gordon AI 模型选择器错误地为未显式选择模型的会话显示内部模型标识符，而非 **Default** 的问题。

#### 适用于 Windows

- 修复了就地升级后卡在 **Starting the Docker Engine…** 的问题。
- 修复了失败更新回退到先前版本后，Docker Desktop 未重启的 Bug。
- 修复了增量更新未能准备的问题。
- 修复了在 Hyper-V 上，当引擎已空闲关闭或暂停后，`docker login` 等 Docker 命令首次尝试会失败的问题。
- 修复了 Windows 上未安装 WSL 时，Docker Desktop 显示通用的引擎启动失败，而非清晰、可操作的错误消息的问题。

## 4.77.0

{{< release-date date="2026-06-08" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.77.0" build_path="/228796/" >}}

### 新增功能

- 现在可以从 **日志** 视图导出日志数据。

### 更新

- Docker Offload v0.6.3
- [Docker Buildx v0.34.1](https://github.com/docker/buildx/releases/tag/v0.34.1)
- [Docker Agent v1.70.0](https://github.com/docker/docker-agent/releases/tag/v1.70.0)
- [Docker MCP gateway v0.42.2](https://github.com/docker/mcp-gateway/releases/tag/v0.42.2)
- `docker pass` v0.1.2
- [containerd v2.2.4](https://github.com/containerd/containerd/releases/tag/v2.2.4)
- [DHI CLI (`dhictl`) v0.0.4](https://github.com/docker-hardened-images/dhictl/releases/tag/v0.0.4)
- [Docker Engine v29.5.3](https://docs.docker.com/engine/release-notes/29/#2953)

### 错误修复和增强

#### 适用于所有平台

- 提高了重试延迟，以适应由防病毒软件持有文件锁导致的瞬时重命名失败。
- Marketplace 扩展现在通过固定的清单摘要（而非标签）进行安装和更新，以防止发布后标签被篡改。
- 在关于窗口中添加了 Buildx 版本信息。
- 在 **日志** 搜索栏中添加了大小写敏感切换，可在不区分大小写（默认）和区分大小写的日志筛选之间切换。
- 修复了 **日志** 视图网格中鼠标滚轮滚动不起作用的问题。
- 修复了在通过 SIGINT 或 SIGTERM 正常关闭时，后端错误地以错误代码 150 退出，导致虚假失败信号的问题。
- 从 Docker Desktop 中移除了捆绑的 `hub-tool` 二进制文件。
- 为 Gordon 中的 MCP OAuth 授权聊天气泡添加了可用的 **认证** 和 **取消** 按钮，让你能够从 MCP 服务器完成或拒绝 OAuth 登录流程。
- 为 `docker pass` 添加了两个新命令：
   - 使用 `docker pass run` 将密钥注入主机命令。
   - 使用 `docker pass plugins` 进行动态插件管理。
- 修复了在启用增强型容器隔离（ECI）的情况下 `docker cp` 到容器时，将文件所有权设置为 `nobody:nogroup` 的回归问题。

#### 适用于 Windows

- 修复了 Windows 上在失败的 WSL 发行版注册遗留 VHDX 在磁盘上后，Docker Desktop 会卡在 **Starting the Docker Engine...** 的问题。
- 修复了 Windows 容器模式下后端关闭挂起，导致 Docker Desktop 长时间或无法干净退出问题。

## 4.76.0

{{< release-date date="2026-06-01" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.76.0" build_path="/228118/" >}}

### 新增功能

- Docker Model Runner 现在支持注册表镜像。

### 更新

- [Docker Desktop Build v0.35.0](https://github.com/docker/desktop-build/releases/tag/v0.35.0)
- [Docker Agent v1.62.0](https://github.com/docker/docker-agent/releases/tag/v1.62.0)
- [NVIDIA Container Toolkit v1.19.1](https://github.com/NVIDIA/nvidia-container-toolkit/releases/tag/v1.19.1)
- [Docker Compose v5.1.4](https://github.com/docker/compose/releases/tag/v5.1.4)
- Docker Offload v0.5.93
- [Docker Scout CLI v1.21.0](https://github.com/docker/scout-cli/releases/tag/v1.21.0)
- `docker pass` v0.0.29

### 安全性

- 修复了 [CVE-2026-8936](https://www.cve.org/CVERecord?id=CVE-2026-8936)，该漏洞为 `grpcfuse` 内核模块中因无界递归引起的 VM 崩溃。当容器在绑定挂载的主机文件夹上创建深度嵌套的目录并触发 `dentry` 失效事件时会发生。

### 错误修复和增强

#### 适用于所有平台

- `docker sbom` 命令已被弃用，将在未来的版本中移除。请改用 [`docker scout sbom command`](/reference/cli/docker/scout/sbom/)。
- 修复了 **Resource Saver** 处于活动状态时 Docker Engine 中的竞态条件。
- 修复了一个 Bug，其中每次删除 `kind` 集群时都会泄漏匿名的 Docker 卷，导致孤立卷累积。
- 修复了 **所有日志** 网格中的列调整大小问题，使 **时间戳** 和 **对象** 列不再意外扩展，并且列宽现在在导航会话之间得以保留。
- 修复了即使底层文件系统正常，VM 磁盘调整操作遇到错误时 Docker Desktop 仍无法启动的问题。
- 修复了退出时导致 Docker Desktop 挂起的问题。
- 修复了停止或启动 Docker Offload 后，CPU 和 RAM 资源总计可能卡在 Docker Desktop 仪表板中显示 0 的 Bug。
- 修复了 Gordon 中最终答案文本会在跳转到回复气泡之前，短暂出现在工作组内的闪烁问题。
- 修复了在并发登出和令牌刷新操作期间可能发生的守护进程崩溃。
- 修复了 **卷** 视图为具有多个卷的容器显示错误挂载目标的问题。
- `docker pass` 现在在 `set` 命令上带有 `--force` 标志。
- `docker --help` 现在会显示 `docker pass`。
- 修复了重启空闲停止的引擎后，通过外部 API 调用返回的容器、镜像、网络、卷和插件的陈旧 API 缓存响应（合成 404）。
- 修复了在 **构建** 视图中选择构建后，**删除** 按钮可能不会立即可见的 Bug。修复了 [docker/desktop-feedback#329](https://github.com/docker/desktop-feedback/issues/329) 和 [docker/desktop-feedback#330](https://github.com/docker/desktop-feedback/issues/330)。
- 修复了启用增强型容器隔离（ECI）时时间命名空间不可用的问题。

#### 适用于 Windows

- 修复了 `--quiet` 安装标志在静默安装期间未能抑制安装类型对话框的回归问题。
- 修复了 Windows 上一个带有尾随换行的陈旧 PID 文件会阻止遗留守护进程被终止，导致 Windows 容器模式无法配置的 Bug。
- 修复了 Windows 上在另一个安装程序实例已在运行时触发更新，会显示通用错误而非特定消息的问题。
- 修复了 Windows 上安装程序和更新程序可执行文件由于 Windows 启发式安装程序检测而错误触发 UAC 提升提示的问题。
- 修复了在 Windows 容器模式下托盘菜单中双分隔符的问题。
- 修复了 Windows Hyper-V 上的端口绑定失败，其中 `docker run -p 0:N` 可能分配 HNS 保留端口，导致绑定错误。
- 修复了非英文 Windows 系统（例如使用 GBK 编码的中文 Windows）日志中乱码的 taskkill 错误消息。
- 修复了 WSL2 ISO 缓存的无界增长。安装新版本时会移除旧的 `docker-desktop.iso` 和 `docker-wsl-cli.iso` 条目。修复了 [docker/desktop-feedback#419](https://github.com/docker/desktop-feedback/issues/419)。

## 4.75.0

{{< release-date date="2026-05-26" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.75.0" build_path="/227598/" >}}

### 更新

- Docker Offload v0.5.92
- [Docker Engine v29.5.2](https://docs.docker.com/engine/release-notes/29/#2952)
- [Docker Buildx v0.34.0](https://github.com/docker/buildx/releases/tag/v0.34.0)

### 错误修复和增强

#### 适用于所有平台

- 移除了 Docker Scout 视图，并禁用了 Scout 相关的操作系统通知和通知弹窗。
- 新增对 ECI 受保护容器中的时间命名空间的支持。
- 修复了一个 Bug，其中 `http_proxy` 环境变量可能阻止 kind 集群拉取本地镜像。
- 修复了 VM 从空闲关闭唤醒后，首次 Docker API 调用可能出现 `500 Internal Server Error` 的问题。
- 修复了由相对 URL 被解析为无效的 `app://` 方案 URL 而导致的 Docker Hub 镜像描述中损坏的图片。

#### 适用于 Mac

- 添加了在启动时由于更新失败而 Docker Desktop 从暂存目录运行时出现的警告对话框。同时添加了下载全新安装的链接。

#### 适用于 Windows

- 与默认发行版的 WSL 集成已被禁用。要更改此设置，请访问 **设置**。
- 修复了在 Windows 上接受文件共享同意提示时，使用 Hyper-V 后端的 `docker compose up` 以 `EOF` 错误失败的 Bug。
- 修复了 Windows 安装程序可能导致安装期间后端模式检测错误或意外创建目录的 Bug。

## 4.74.0

{{< release-date date="2026-05-19" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.74.0" build_path="/227015/" >}}

### 新增功能

- [Gordon](/ai/gordon) 现已正式发布（GA）。同时也提供了新的使用计划。付费的 Gordon 计划可解锁更高的使用限额。

### 更新

- Docker Offload v0.5.89
- [Docker Agent v1.57.0](https://github.com/docker/docker-agent/releases/tag/v1.57.0)
- [Credential helpers v0.9.7](https://github.com/docker/docker-credential-helpers/releases/tag/v0.9.7)
- `docker pass` v0.0.26

### 错误修复和增强

#### 适用于所有平台

- 修复了一个 Bug，其中 Docker Desktop 自身的 Electron 辅助进程（GPU、渲染器、实用工具）在从开始菜单启动时会被错误地检测并作为残留进程杀死，导致崩溃循环。
- 修复了日志视图显示设置中的 **查看构建日志** 切换在重启 Docker Desktop 后被重置，而非持久化用户偏好的问题。
- Docker Extensions 现在默认禁用。

#### 适用于 Mac

- 修复了当容器同时连接到 Swarm 覆盖网络时发布端口不可访问的问题。修复了 [docker/for-mac#7854](https://github.com/docker/for-mac/issues/7854)。
- 修复了某些企业环境中的仪表板 TLS 失败。
- 通过内容哈希校验提高了 GUI 安全性。

#### 适用于 Linux

- 新增对 Ubuntu 26.04 的支持。

## 4.73.1

{{< release-date date="2026-05-13" >}}

{{< desktop-install-v2 win=true version="4.73.1" build_path="/226574/" >}}

### 错误修复和增强

#### 适用于 Windows

- 修复了从开始菜单启动时，Docker Desktop 自身的 Electron 进程被错误杀死的 Bug。修复了 [docker/desktop-feedback#367](https://github.com/docker/desktop-feedback/issues/367)。

## 4.73.0

{{< release-date date="2026-05-11" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.73.0" build_path="/226246/" >}}

### 更新

- [Docker Engine v29.4.3](https://docs.docker.com/engine/release-notes/29/#2943)
- [Docker Agent v1.54.0](https://github.com/docker/docker-agent/releases/tag/v1.54.0)

### 错误修复和增强

#### 适用于所有平台

- 修复了 Mac 上的 `Cmd+Q` 和 Windows/Linux 上的 `Ctrl+Q` 未能完全退出 Docker Desktop 的问题。修复了 [docker/for-mac#7833](https://github.com/docker/for-mac/issues/7833)。
- 修复了一个 Bug，其中取消 `docker load` 会持有 containerd 引用锁，导致后续加载同一镜像失败。
- 修复了当 MCP Toolkit 禁用时，Docker Desktop 在登录时向 `mcp.docker.com` 发出不必要网络请求，导致意外代理身份验证提示的问题。
- 修复了 Gordon 会话侧边栏中的搜索输入框在留空时不会关闭的问题。
- 改进了 Docker Desktop 对由防病毒软件同时访问这些文件导致的瞬时重命名失败的处理。

#### 适用于 Mac

- 通过改进 Linux VM 将释放的容器内存归还给主机操作系统的能力，修复了 Apple Silicon Mac 上内存占用过高的问题。
- 修复了一个 Bug，其中当另一个容器与同一子网范围内的 IP 存在活动出站连接时，容器收到的连接源 IP 被破坏。修复了 [docker/for-mac#7824](https://github.com/docker/for-mac/issues/7824)。

## 4.72.0

{{< release-date date="2026-05-06" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.72.0" build_path="/225998/" >}}

### 新增功能

- **日志** 视图现已正式发布（GA）。
- 新安装的 Windows 版 Docker Desktop 可以在 per-user（Beta）或 all-user 安装之间进行选择。

### 更新

- [Docker Agent v1.50.0](https://github.com/docker/docker-agent/releases/tag/v1.50.0)
- [Docker DHI (`dhictl`) v0.0.3](https://github.com/docker-hardened-images/dhictl/releases/tag/v0.0.3)
- [Docker Model Runner v1.1.37](https://github.com/docker/model-cli/releases/tag/v1.1.37)
- [credential helpers v0.9.6](https://github.com/docker/docker-credential-helpers/releases/tag/v0.9.6)

### 安全性

- 扩展设置页面现在包含一条安全提示，说明扩展以主机级权限运行，且未经 Docker 审核。
- 通过反向移植上游 Linux 内核补丁修复了 [CVE-2026-31431（"copy.fail"）](https://xint.io/blog/copy-fail-linux-distributions)，该补丁可防止未特权容器用户通过对主机 VM 页缓存的受控写入在容器内获取 root 权限。

### 错误修复和增强

#### 适用于所有平台

- 改进了 Docker Offload 空闲通知。
- 修复了由于 Docker Agent 命令参数中缺少 `run` 子命令，导致 **在 TUI 中打开 Gordon** 按钮不起作用的问题。
- 修复了登录期间瞬时网络错误或 Docker Hub 服务器错误会意外将用户登出，而非自动重试的问题。
- 通过导航到这些屏幕时按需获取最新数据，改进了容器、镜像和卷屏幕的数据刷新，减少了后台轮询负载。
- 修复了在大量容器文件活动后更改文件共享技术时可能发生的内核崩溃。
- 在 Docker Model Runner 中启用了 OpenAI Responses API（`/responses`）端点。
- 修复了通过 `docker login` 使用 OAuth 登录时，用户会在流程中途被意外登出 Docker Desktop 的 Bug。

#### 适用于 Windows

- 修复了 Windows 上多次选择 Docker Desktop 任务栏图标会生成多个后端进程的 Bug。在 Docker Desktop 运行时重新选择该图标现在会将仪表板置于前台。
- 修复了 Windows 上 Docker Desktop 正常启动或退出时，出现虚假的 "进程仍在运行" 对话框的竞态条件。

### 适用于 Linux

- 已放弃对 RHEL 8 的支持。

## 4.71.0

{{< release-date date="2026-04-27" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.71.0" build_path="/225177/" >}}

> [!重要]
>
> 对 RHEL 8 的支持已结束。在下一版本中，安装 Docker Desktop 将需要 RHEL 9 或 RHEL 10。

### 更新

- [Docker Model Runner v1.1.36](https://github.com/docker/model-runner/releases/tag/v1.1.36)
- [containerd to v2.2.3](https://github.com/containerd/containerd/releases/tag/v2.2.3)
- [Runc v1.3.5](https://github.com/opencontainers/runc/releases/tag/v1.3.5)
- [Docker Compose v5.1.3](https://github.com/docker/compose/releases/tag/v5.1.3)
- [Docker Agent v1.44.0](https://github.com/docker/docker-agent/releases/tag/v1.44.0)
- [Docker Engine v29.4.1](/manuals/engine/release-notes/29.md#2941)

### 错误修复和增强

#### 适用于所有平台

- Docker Model Runner 现在默认禁用，必须在 **设置** 中显式启用。启用时，TCP 主机端支持会自动激活。
- 修复了在磁盘可用空间不足时，下载 Docker Desktop 更新会因缺乏清晰错误而失败的问题。
- 修复了在检查镜像时，当基础镜像摘要或仓库名称为空时，Docker Scout 标签推荐失败的问题。
- 在登录屏幕上添加了 **切换到本地 Docker 上下文** 按钮，允许处于云上下文中的用户无需登录即可切换回其本地上下文。
- 为云引擎添加了专用的 **已停止** 状态屏幕，使用户在从 Docker Offload 切换离开时看到清晰的已停止状态，而非错误屏幕。

#### 适用于 Mac

- 修复了用户禁用分析后，错误跟踪会暂时继续直接发送会话数据的问题。修复了 [docker/for-mac#7768](https://github.com/docker/for-mac/issues/7768)。

#### 适用于 Windows

- 修复了由进程加固策略与 Chromium 冲突导致的 `ERR_FAILED` 错误，使 Docker Desktop 仪表板无法打开的严重问题。
- 修复了当 WSL 2 本身设置了 `HTTP_PROXY` 环境变量时，Kubernetes 可能在 WSL 2 上启动失败的 Bug。
- 修复了增强型容器隔离（ECI）中使用 WSL 时，会导致容器 `rootfs` 持久性在 Docker Desktop 重启之间丢失的 Bug。

### 安全性

- 修复了 [CVE-2026-5843](https://www.cve.org/cverecord?id=CVE-2026-5843)，即通过 MLX-LM `model_file` importlib 加载，在 Docker Model Runner MLX 推理后端中发生的容器到主机的代码执行。

## 4.70.0

{{< release-date date="2026-04-20" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.70.0" build_path="/224270/" >}}

### 新增功能

- 添加了一个 CLI 提示，在运行 `logs`、`compose logs`、`compose attach` 或 `compose up` 命令时显示 **日志** 视图，让你能够快速访问所有运行中的容器的日志。需启用 **日志**（Beta）功能。

### 更新

- [Docker Compose v5.1.2](https://github.com/docker/compose/releases/tag/v5.1.2)
- [Docker Engine v29.4.0](/manuals/engine/release-notes/29.md#2940)
- [Docker Agent v1.43.0](https://github.com/docker/docker-agent/releases/tag/v1.43.0)
- [Docker Model Runner v1.1.33](https://github.com/docker/model-runner/releases/tag/v1.1.33)
- [Docker Scout CLI v1.20.4](https://github.com/docker/scout-cli/releases/tag/v1.20.4)

### 错误修复和增强

#### 适用于所有平台

- 修复了在 CI 环境中，由于 Docker Hub 响应缓慢导致凭据存储更新超时，`docker login` 可能静默失败的 Bug。
- 修复了禁用 Beta 功能同时也会禁用 Docker Model Runner 的问题。
- 修复了 `docker desktop start` 由于继承的 CLI 插件环境变量，导致 Docker AI agent API 守护进程失败的问题。

#### 适用于 Mac

- 修复了由于损坏的 `DockerAppLaunchPath` 设置，更新后 Docker Desktop 以退出状态 `42` 反复启动失败的崩溃循环。
- 修复了失败的更新可能使 Docker Desktop 处于损坏状态的问题。现在安装程序会自动回退到先前版本并显示清晰的错误消息。
- 修复了一个 Bug，其中停止一个容器可能会干扰其他运行容器的活动 Unix 套接字转发。

#### 适用于 Windows

- 修复了失败的更新可能使 Docker Desktop 处于损坏状态的问题。现在安装程序会自动回退到先前版本并显示清晰的错误消息。
- 修复了一个 Bug，其中切换到 Windows 容器失败可能使 Docker Desktop 处于损坏状态，需要重启。
- 修复了 Docker Desktop 在环境中设置了 `DEVHOME` 的用户上无法启动的问题。
- 暂时回退了导致 Windows 上 Electron 崩溃的进程加固。修复了 [docker/desktop-feedback#245](https://github.com/docker/desktop-feedback/issues/245)。

## 4.69.0

{{< release-date date="2026-04-13" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.69.0" build_path="/224084/" >}}

### 更新

- [Docker Agent v1.42.0](https://github.com/docker/docker-agent/releases/tag/v1.42.0)
- [Docker Model v1.1.29](https://github.com/docker/model-runner/releases/tag/v1.1.29)
- [containerd v2.2.2](https://github.com/containerd/containerd/releases/tag/v2.2.2)
- [Docker Buildx v0.33.0](https://github.com/docker/buildx/releases/tag/v0.33.0)

### 错误修复和增强

#### 适用于所有平台

- 修复了当 OAuth 令牌仍保留在凭据存储中时，来自 CLI 的 `docker logout` 被 Docker Desktop 忽略，导致用户意外保持登录状态的问题。
- 修复了当无关的凭据更新、`docker login` 或瞬时网络错误触发登出时，Docker Desktop 可能意外将用户登出的问题。
- 修复了在失败的恢复操作中可能删除备份数据，导致用户无数据可用的数据丢失问题。
- 修复了登录凭据（`login-info.json`）可能被包含在诊断包中的问题，提高了隐私和安全性。请注意，该文件仅包含编码的组织名称、计划名称、编码的用户名和编码的邮箱。不包含任何密码或凭据。
- 修复了页脚更新标签在更新的准备/解包阶段错误地显示 **Downloading** 的问题。现在正确显示为 **Preparing**。
- 修复了内部存储磁盘已满时 Docker Desktop 无法启动的问题。

#### 适用于 Mac

- 修复了当 `Docker.app` 安装在非用户可写目录时，应用内更新按钮未禁用，从而避免失败更新尝试的问题。
- 修复了通过 Mac 上的 Homebrew 安装 Docker Desktop 的用户的更新失败问题。

#### 适用于 Windows

- 修复了在 Docker Desktop 安装或卸载期间，使用 Hyper-V 后端的 Windows 用户会意外弹出 WSL 终端的问题。
- 修复了 Windows 上恢复出厂默认设置会从 `~/.docker/cli-plugins` 删除 CLI 插件，导致 `docker build` 回退到旧版构建器的问题。
- 修复了一个 Bug，其中当 WSL 集成与另一个使用 cgroup v1 控制器的发行版同时启用时，Kubernetes 无法启动。
- 修复了在启动期间 Registry Access Management 策略更改发生时，导致 Kubernetes 无法启动的竞态条件。
- 防止 Docker Desktop 因 Windows 上文件操作期间的瞬时 "Access is denied" 错误而致命失败。

## 4.68.0

{{< release-date date="2026-04-07" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.68.0" build_path="/223695/" >}}

### 新增功能

- Gordon 现在拥有持久化的本地记忆，使其能够跨会话记住你的偏好和上下文。

### 更新

- [Docker Agent v1.39.0](https://github.com/docker/docker-agent/releases/tag/v1.39.0)
- [Docker Model v1.1.28](https://github.com/docker/model-runner/releases/tag/v1.1.28)
- Docker Offload v0.5.81

### 错误修复和增强

#### 适用于所有平台

- 修复了增强型容器隔离中导致容器在创建时无限期挂起的死锁（启用 ECI 时）。
- 添加了警告横幅，在 MCP 服务器由社区提供且未经 Docker 验证时发出提醒。
- 在 **日志** 视图中添加了持久的 **显示时间戳** 切换，允许在表格和可视化视图中跨会话隐藏时间戳。
- 修复了退出时 Docker Desktop 前端进程未被正确终止的问题。
- 修复了由管理员控制的设置在重新加载时可能导致 Docker Desktop 在登录或登出操作期间无响应的死锁。
- 修复了一个 Bug，其中由于磁盘映像上无法修复的文件系统错误未被修复，导致 Docker Desktop 无法启动。
- 修复了一个导致增强型容器隔离（ECI）无意中阻止 Kubernetes 集群启动的 Bug。
- 修复了失败的卷大小获取可能导致 **卷** 视图无法访问的问题；卷上的容器计数现在已正确排除绑定挂载。
- 修复了卷备份中的竞态条件，该条件可能导致容器被错误地重启、导出日志被损坏，或在调度任务时发生运行时崩溃。
- 修复了当无名容器导致 panic 时，API 缓存中发生的崩溃，该崩溃会干扰容器列表。
- 修复了一个 Bug，其中如果在没有容器使用绑定时删除了绑定挂载的父目录，启动容器可能以 `ENOENT` 失败。

#### 适用于 Mac

- 修复了一个安全漏洞，其中被篡改的用户部署配置 profile 可能绕过组织的登录强制策略。
- 修复了一个 Bug，其中失败的 `vmnetd` 握手可能在已断开的连接上分派虚假命令，导致意外的网络错误。
- 修复了在启动时恢复到全屏状态时，Docker Desktop 仪表板可能过早显示的问题。
- 修复了在使用 Docker Compose 且多个服务共享一个卷时，嵌套绑定挂载在 VirtioFS 上显示为空子挂载内容的问题。修复了 [docker/desktop-feedback#264](https://github.com/docker/desktop-feedback/issues/264)。

#### 适用于 Windows

- 修复了安装程序解压未更新进度条并可能耗时约 5 分钟（取决于机器）的问题。现在解压速度提高约 60%，并包含正确的进度更新。
- 修复了容器启动后容器端口有时无法正确发布的竞态条件，影响了临时端口、`--publish-all` 和网关 IP 绑定。
- 修复了失败的 WSL 发行版移动可能使该发行版处于未注册状态的问题。

### 安全性

- 修复了 [CVE-2026-5817](https://www.cve.org/cverecord?id=CVE-2026-5817)，即通过未沙箱化的 `trust_remote_code` tokenizer 加载，在 Docker Model Runner vllm-metal 推理后端中发生的容器到主机的代码执行。

## 4.67.0

{{< release-date date="2026-03-30" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.67.0" build_path="/222858/" >}}

### 新增功能

- Docker MCP Toolkit 现在拥有 MCP profile 模板卡片，以及可通过 **配置文件** 选项卡访问的入门导览。

### 更新

- [Docker Compose v5.1.1](https://github.com/docker/compose/releases/tag/v5.1.1)
- [Docker Agent v1.34.0](https://github.com/docker/docker-agent/releases/tag/v1.34.0)
- [Docker Scout CLI v1.20.3](https://github.com/docker/scout-cli/releases/tag/v1.20.3)
- [Docker Model v1.1.25](https://github.com/docker/model-runner/releases/tag/v1.1.25)

### 错误修复和小幅改动

#### 适用于所有平台

- Docker Model Runner 现在支持 Qwen3.5。
- 借助新的 **日志（Beta）** 视图，你现在可以按 Compose 堆栈筛选容器日志。
- 改进了在 Docker 引擎或 Kubernetes 启动或停止时与 **设置** 的交互。
- 修复了一个 Bug，其中随机 UDP 端口绑定报告端口 `0` 而非实际分配的端口。
- 修复了 Docker Desktop 快捷方式在 Docker Desktop 已运行时无法重新打开仪表板的问题。
- 修复了 **添加到现有 profile** 对话框在下拉列表中显示了已包含所有所选 MCP 服务器的 profile 的问题。

#### 适用于 Mac

- 修复了由于 Rosetta `binfmt` 注册与 `virtiofs` 设备可用性之间的竞态条件，在 Apple Silicon Mac 上启动 amd64 容器时出现的间歇性 `exec format error`。

#### 适用于 Windows

- 修复了 WSL 2 用户的 Hyper-V 在每次 EXE 升级时被静默重新启用的问题。
- 修复了 Windows 上卸载后 Docker Desktop 进程可能仍在运行的 MSI 安装程序 Bug。
- 修复了 Windows 上使用 `--installation-dir` 的安装或更新会因安装程序归档被解压到自定义安装目录而失败的问题。
- 通过 WSL 2 将 Windows 上的 Docker Desktop 启动时间缩短了数秒。
- 修复了 Windows 上 **模型** > **日志** 屏幕每次访问时导致 `docker-model` 进程累积的 Bug。

### 安全性

- 修复了 [CVE-2026-33990](https://www.cve.org/cverecord?id=CVE-2026-33990)，即 Docker Model Runner OCI Registry Client 中的 SSRF。

## 4.66.1

{{< release-date date="2026-03-26" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.66.1" build_path="/222799/" >}}

### 更新

- [Docker Engine v29.3.1](/manuals/engine/release-notes/29.md#2931)

## 4.66.0

{{< release-date date="2026-03-23" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.66.0" build_path="/222299/" >}}

### 更新

- [Docker Engine v29.3.0](https://docs.docker.com/engine/release-notes/29/#2930)
- [NVIDIA Container Toolkit v1.19.0](https://github.com/NVIDIA/nvidia-container-toolkit/releases/tag/v1.19.0)

### 错误修复和小幅改动

#### 适用于所有平台

- Gordon 改进：
   - 从命令行失败提示进行深层链接时提供预填充的提示。
   - 通过在发出请求前进行身份验证，防止 Docker Hub 速率限制。
- 修复了当 kube 上下文损坏或不可达时 Kubernetes pod 发现挂起的问题。
- 修复了终端调整大小期间由于未定义尺寸错误导致的终端崩溃。
- 修复了针对文件、镜像和注册表导出操作的卷备份导出错误处理。

#### 适用于 Windows

- 修复了 Windows API 代理中由不必要的进程枚举导致的高 CPU 占用。
- 修复了 Windows MSI 安装程序无法更新 Docker Desktop 的问题。4.56 到 4.65 之间的版本需要先卸载再重新安装 4.66 或更高版本。请注意，卸载会移除所有关联数据。

## 4.65.0

{{< release-date date="2026-03-16" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.65.0" build_path="/221669/" >}}

### 新增功能

- 添加了一个新的 **日志** 视图，你可以在其中通过统一视图探索所有来源的日志。（Beta）
- 当 `docker build`、`docker run` 或 `docker compose` 命令失败时，现在会出现 Gordon 提示，提供上下文建议。
- 社区 MCP 服务器现在支持直接在 UI 中进行 OAuth 身份验证。
- 添加了 [`docker dhi` CLI 插件](https://github.com/docker-hardened-images/dhictl) 用于管理 Docker Hardened Images。

### 更新

- [Docker Scout CLI v1.20.1](https://github.com/docker/scout-cli/releases/tag/v1.20.1)
- [Docker Agent v1.29.0](https://github.com/docker/docker-agent/releases/tag/v1.29.0)
- [Docker Buildx v0.32.1](https://github.com/docker/buildx/releases/tag/v0.32.1)

### 错误修复和小幅改动

#### 适用于所有平台

- Kubernetes 现在对新集群默认使用 kind。
- 修复了更新进度条无法正确恢复的问题。

#### 适用于 Windows

- 通过在使用 WSL2 后端时跳过 docker-users 组检查，缩短了启动时间。

### 已知问题

- Windows MSI 安装程序在 current version 介于 4.56 到 4.65 之间时无法更新现有的 Docker Desktop 安装。作为变通方法，请在重新安装最新版本之前卸载现有版本。请注意，卸载会移除所有关联数据。

## 4.64.0

{{< release-date date="2026-03-11" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.64.0" build_path="/221278/" >}}

### 更新

- [Docker Compose v5.1.0](https://github.com/docker/compose/releases/tag/v5.1.0)
- [Docker Scout CLI v1.20.0](https://github.com/docker/scout-cli/releases/tag/v1.20.0)
- [Docker Agent v1.27.1](https://github.com/docker/docker-agent/releases/tag/v1.27.1)

### 错误修复和小幅改动

#### 适用于所有平台

- 修复了 MCP Toolkit 中禁用 profile 中所有工具反而会启用所有工具的 Bug。
- 修复了 Docker Agent 更新后 `docker ai` 命令停止的问题。
- 修复了 Gordon 会话标题在悬停按钮出现时闪烁的问题。
- 改进了 Gordon 摘要渲染并减少了叙述冗长。
- 修复了 `docker ai` CLI 命令未正确调用 Docker Agent 的 Bug。
- 修复了 Docker MCP Toolkit 中的 **OAuth** 选项卡未显示来自所有目录的条目的问题。
- 改进了 MCP Catalog 搜索。
- 修复了 **构建日志** 选项卡在切换选项卡时未保留搜索词和筛选器的问题。
- 修复了 Kind 容器启动更可靠的问题。

#### 适用于 Mac

- 通过更具描述性的诊断信息改进了更新错误报告。
- 通过在 `Application Support` 下而非 `/tmp` 中准备更新后的 `Docker.app`，提高了更新可靠性。

### 已知问题

- Windows MSI 安装程序在 current version 介于 4.56 到 4.65 之间时无法更新现有的 Docker Desktop 安装。作为变通方法，请在重新安装最新版本之前卸载现有版本。请注意，卸载会移除所有关联数据。

## 4.63.0

{{< release-date date="2026-03-02" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.63.0" build_path="/220185/" >}}

### 新增功能

- 在 **构建** 视图中添加了 SLSA v1 来源（provenance）支持。

### 更新

- [Kubernetes v1.34.3](https://github.com/kubernetes/kubernetes/releases/tag/v1.34.3)
- Linux 内核 `v6.12.72`

### 错误修复和小幅改动

#### 适用于所有平台

- 增强了代理设置 UI，并为容器添加了单独的代理。
- 修复了当服务器的 config 对象包含 `"required": null` 时，社区注册表 MCP 目录无法加载的问题。
- 修复了当 Docker Desktop VM 处于 Resource Saver 模式时，`mcp-gateway` 从 Secrets Engine 获取密钥会挂起的问题。
- 将 "Docker AI" 相关引用重新命名为 "Gordon"。

#### 适用于 Windows

- 缩短了 Windows 上的启动时间。

### 已知问题

- Windows MSI 安装程序在 current version 介于 4.56 到 4.65 之间时无法更新现有的 Docker Desktop 安装。作为变通方法，请在重新安装最新版本之前卸载现有版本。请注意，卸载会移除所有关联数据。

## 4.62.0

{{< release-date date="2026-02-23" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.62.0" build_path="/219486/" >}}

### 新增功能

- 借助 Docker MCP Toolkit，你现在可以使用 [profiles](/manuals/ai/mcp-catalog-and-toolkit/profiles.md) 将你的 MCP 服务器组织到命名的集合中。你还可以创建自定义目录——为你的团队或组织精选的服务器集合。

### 更新

- Linux 内核 `v6.12.69`

### 错误修复和增强

#### 适用于所有平台

- 修复了后台更新检查在 **自动检查更新** 设置被禁用时未遵循该设置的问题。修复了 [docker/for-mac#3908](https://github.com/docker/for-mac/issues/3908)。

#### 适用于 Mac

- 为 Docker Model Runner 添加了对 vLLM Metal 的支持。

#### 适用于 Linux

- 修复了 QEMU 10.2.0 及更高版本上的网络崩溃。

### 安全性

- 修复了 [CVE-2026-2664](https://www.cve.org/cverecord?id=CVE-2026-2664)，即 grpcfuse 内核模块中的越界读取。
- 修复了 [CVE-2026-28400](https://www.cve.org/cverecord?id=CVE-2026-28400)，即 Docker Model Runner 中的运行时标志注入。

### 已知问题

- Windows MSI 安装程序在 current version 介于 4.56 到 4.65 之间时无法更新现有的 Docker Desktop 安装。作为变通方法，请在重新安装最新版本之前卸载现有版本。请注意，卸载会移除所有关联数据。

## 4.61.0

{{< release-date date="2026-02-18" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.61.0" build_path="/219004/" >}}

### 新增功能

- 你现在可以自定义左侧导航，仅显示对你重要的选项卡，并隐藏不需要的选项卡。

### 更新

- Linux 内核 `v6.12.68`
- [Docker Engine v29.2.1](https://docs.docker.com/engine/release-notes/29/#2921)
- Docker Sandbox `v0.12.0`

### 错误修复和增强

#### 适用于所有平台

- Docker Sandboxes：
   - 添加了自动镜像缓存，以防止不必要的重复下载镜像。
   - 为空白编码代理沙箱添加了 Shell 模式。
   - 添加了对 OpenCode 的支持。
   - 添加了对挂载多个工作区的支持。
   - 添加了实验性的 Linux 支持（仅单用户，UID 1000）。
   - 添加了对在 WSL 2 中运行的支持。
   - 如果未提供路径，沙箱现在会在当前工作目录中启动。

### 已知问题

- Windows MSI 安装程序在 current version 介于 4.56 到 4.65 之间时无法更新现有的 Docker Desktop 安装。作为变通方法，请在重新安装最新版本之前卸载现有版本。请注意，卸载会移除所有关联数据。

## 4.60.1

{{< release-date date="2026-02-10" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.60.1" build_path="/218372/" >}}

### 错误修复和增强

#### 适用于所有平台

- 修复了登录后导致 Docker Desktop 仪表板崩溃的罕见问题。

## 4.60.0

{{< release-date date="2026-02-09" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.60.0" build_path="/218231/" >}}

### 新增功能

- 添加了一个新的 `docker desktop diagnose` 命令来收集诊断信息。

### 错误修复和增强

#### 适用于所有平台

- 修复了 `ping6 host.docker.internal`。
- 启用了 landlock LSM。
- Docker Sandboxes 改进：
   - 通过包含网络访问文档改进了代理系统提示
   - 修复了 Gemini API 密钥注入
   - 沙箱现在在代理默认规则中屏蔽 `console.anthropic.com/claude.ai`
   - 修复了 `run <agent> --help` 的 CLI 帮助文本
   - 改进了终端大小处理

### 已知问题

- Windows MSI 安装程序在 current version 介于 4.56 到 4.65 之间时无法更新现有的 Docker Desktop 安装。作为变通方法，请在重新安装最新版本之前卸载现有版本。请注意，卸载会移除所有关联数据。

## 4.59.1

{{< release-date date="2026-02-03" >}}

{{< desktop-install-v2 mac=true version="4.59.1" build_path="/217750/" >}}

### 错误修复和增强

#### 适用于 Mac

- 修复了 CPU 使用率可能定期飙升的问题。修复了 [docker/for-mac#7839](https://github.com/docker/for-mac/issues/7839)。

## 4.59.0

{{< release-date date="2026-02-02" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.59.0" build_path="/217644/" >}}

### 更新

- Linux 内核 `v6.12.67`
- [Docker Compose v5.0.2](https://github.com/docker/compose/releases/tag/v5.0.2)
- Docker Sandbox `v0.10.1`
- [Docker Buildx v0.31.1](https://github.com/docker/buildx/releases/tag/v0.31.1)

### 错误修复和增强

#### 适用于所有平台

- 将 Neo4j 作为已知发布者添加到 Docker MCP Catalog。
- 修复了 **模型** 选项卡在显示通过 Anthropic Messages API 发出的请求时会崩溃的问题。

#### 适用于 Mac

- 修复了使用 DockerVMM 时共享文件权限可能被意外修改的问题。修复了 [docker/for-mac#7830](https://github.com/docker/for-mac/issues/7830)。

#### 适用于 Windows

- 修复了容器密钥注入可能因 `docker-pass` 失败的问题。
- 暂时禁用了 WSL 数据磁盘的 VHDX 压缩以提高稳定性。

### 安全性

- 修复了增强型容器隔离中的一个安全问题，其中在使用 `--use-api-socket` 标志时，Docker socket 挂载权限可能被绕过。

## 4.58.1

{{< release-date date="2026-01-29" >}}

{{< desktop-install-v2 mac=true version="4.58.1" build_path="/217134/" >}}

### 错误修复和增强

#### 适用于 Mac

- 修复了 CPU 使用率可能定期飙升的问题。修复了 [docker/for-mac#7839](https://github.com/docker/for-mac/issues/7839)。

## 4.58.0

{{< release-date date="2026-01-26" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.58.0" build_path="/216728/" >}}

### 新增功能

- Docker Desktop 现在提供新版本的 [Docker Sandboxes](/manuals/ai/sandboxes/_index.md)。它为运行编码代理提供了一个安全、隔离、基于微虚拟机 的环境。

### 更新

- Linux 内核 `v6.12.65`
- [Credential helpers v0.9.5](https://github.com/docker/docker-credential-helpers/releases/tag/v0.9.5)
- [Docker Engine v29.1.5](https://docs.docker.com/engine/release-notes/29/#2915)

### 错误修复和增强

#### 适用于所有平台

- Docker Model Runner 现在公开一个[与 Anthropic 兼容的 API](/manuals/ai/model-runner/api-reference.md#anthropic-compatible-api)。
- Docker Desktop 现在支持 `admin-settings.json` 和 `registry.json` 的 UTF-8 BOM。
- 修复了管理设置错误地在重启后更改用户代理设置的问题。

> [!重要]
>
> 从 Docker Desktop 版本 4.59 开始，从托盘菜单安装更新将不会打开 Docker Desktop 仪表板。

#### 适用于 Mac

- 修复了在 macOS 上使用 DockerVMM 时共享文件权限可能被意外修改的错误。修复了 [docker/for-mac#7830](https://github.com/docker/for-mac/issues/7830)。

#### 适用于 Windows

- 修复了由于 `ProgramData` 上设置了特殊 ACL 而导致安装程序失败的问题。

### 安全性

- 更新了 Kubernetes 镜像以解决 CVE。
   - Kind:
      - `docker/desktop-containerd-registry-mirror:v0.0.3`
      - `docker/desktop-cloud-provider-kind:v0.5.0`
   - Kubeadm:
      - `docker/desktop-vpnkit-controller:v4.0`
      - `docker/desktop-storage-provisioner:v3.0`
- `kind` 依赖镜像 `envoyproxy/envoy` 已从 v1.32.6 升级到 v1.36.4。如果您镜像 `kind` 镜像，请确保您的镜像已更新。

## 4.57.0

{{< release-date date="2026-01-19" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.57.0" build_path="/215387/" >}}

### 安全性

- 修复了 [CVE-2025-14740](https://www.cve.org/cverecord?id=CVE-2025-14740)，该漏洞涉及 Docker Desktop for Windows 安装程序在处理 `C:\ProgramData\DockerDesktop` 目录时存在多处不正确的权限分配漏洞。

### 新增功能

- Docker Desktop 现在在 https://github.com/docker/desktop-feedback 上有一个适用于所有平台的新问题跟踪器。来自以前特定于平台跟踪器的相关且积极讨论的问题将被迁移。

### 更新

- [Docker Compose v5.0.1](https://github.com/docker/compose/releases/tag/v5.0.1)

### 错误修复和增强

#### 适用于所有平台

- 改进了 Ask Gordon 流式指示器的对齐方式，使其在大屏幕上与内容保持同步。
- 修复了 `docker debug` 在启动时带有环境变量但没有 '=' 的容器上失败的错误。例如，`docker run -e NONEXISTENT_ENV_VAR`。

## 4.56.0

{{< release-date date="2026-01-12" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.56.0" build_path="/214940/" >}}

### 新增功能

- Docker Desktop 现在包含 Docker Compose v5，它引入了一个新的官方 Go SDK。此 SDK 提供了一个全面的 API，允许您将 Compose 功能直接集成到您的应用程序中，使您能够在不依赖 Compose CLI 的情况下加载、验证和管理多容器环境。有关更多信息，请参阅 [Compose SDK 文档](/manuals/compose/compose-sdk.md)。

### 更新

- [containerd v2.2.1](https://github.com/containerd/containerd/releases/tag/v2.2.1)
- [Docker Compose v5.0.0](https://github.com/docker/compose/releases/tag/v5.0.0)
- [Docker Agent v1.18.6](https://github.com/docker/cagent/releases/tag/v1.18.6)

### 错误修复和增强

#### 适用于所有平台

- 修复了当容器启动后没有 IP 地址时文件共享测试中的 panic。
- 添加了对 LinuxKit 虚拟机中自定义 DNS 条目的支持，使用 `ExtraDNSEntries` 配置字段。

#### 适用于 Windows

- 修复了在 Windows 上删除状态目录会失败的问题，因为日志文件仍处于打开状态。
- 修复了 Microsoft Store 中的安装错误地宣传新更新的问题。
- 通过将 QEMU 从 8.1.5 升级到 10.0.4，修复了在 `ubuntu:22.04` ARM64 容器中运行 `/sbin/ldconfig` 时崩溃的问题。这解决了 [docker/for-win#15004](https://github.com/docker/for-win/issues/15004) 中报告的已知问题。

  > [!注意]
  >
  > 在 ARM64 仿真下运行时，使用旧版本 Go 构建的一些 `amd64` Go 二进制文件可能仍然会段错误。为避免这种情况，请使用 Go 1.25.4 或更高版本重新构建受影响的二进制文件。有关详细信息，请参阅 [golang/go#69255](https://github.com/golang/go/issues/69255) 和相应的 [Go 提交](https://github.com/golang/go/commit/bf95b767394eb5643265f44c7b98bdbb85b897ce)。

#### 适用于 Linux

- 修复了 Linux 主机上 Kubernetes `hostPath` 卷挂载失败的问题。修复了 [docker/desktop-linux#12](https://github.com/docker/desktop-linux/issues/12)。

## 4.55.0

{{< release-date date="2025-12-16" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.55.0" build_path="/213807/" >}}

### 更新

- [Docker Engine v29.1.3](https://docs.docker.com/engine/release-notes/29/#2913)
- [Docker Agent v1.15.1](https://github.com/docker/cagent/releases/tag/v1.15.1)

### 错误修复和增强

#### 适用于所有平台

- 修复了导致 Docker Desktop 在启动期间卡住的问题。
- 改进了当 `daemon.json` 无效时的错误消息。
- 修复了在长 Ask Gordon 会话中每次击键时的性能问题。
- 修复了当组织配置了注册表访问管理以阻止 Docker Hub 时，kubeadm 模式中的 Kubernetes 无法启动的问题。

> [!重要]
>
> Wasm 工作负载将在未来的 Docker Desktop 版本中被弃用并移除。

## 4.54.0

{{< release-date date="2025-12-04" >}}


### 新增功能

- 在 Windows 上添加了对 WSL2 和 NVIDIA GPU 的 Docker Model Runner 中 vLLM 的支持。

### 错误修复和增强

#### 适用于 Mac

- 修复了 `/dev/shm` 没有足够权限供容器写入的错误。修复了 [docker/for-mac#7804](https://github.com/docker/for-mac/issues/7804)。

### 升级

- [Docker Buildx v0.30.1](https://github.com/docker/buildx/releases/tag/v0.30.1)
- [Docker Engine v29.1.2](https://docs.docker.com/engine/release-notes/29/#2912)
- [Runc v1.3.4](https://github.com/opencontainers/runc/releases/tag/v1.3.4)
- [Docker Model Runner CLI v1.0.2](https://github.com/docker/model-runner/releases/tag/cmd%2Fcli%2Fv1.0.2)

### 安全性

- 添加了一个安全补丁以解决 [CVE-2025-13743](https://www.cve.org/cverecord?id=CVE-2025-13743)，其中发现 Docker Desktop 诊断包由于错误对象序列化而在日志输出中包含过期的 Hub PAT。

## 4.53.0

{{< release-date date="2025-11-27" >}}


### 错误修复和增强

#### 适用于所有平台

- 修复了“支持诊断”工具无意中捕获已过期的 Docker Hub 授权 bearer token 的问题。

### 安全性

- 在使用[增强型容器隔离](https://docs.docker.com/enterprise/security/hardened-desktop/enhanced-container-isolation)时，添加了安全补丁以解决以下 CVE：[2025-52565](https://github.com/opencontainers/runc/security/advisories/GHSA-9493-h29p-rfm2)、[2025-52881](https://github.com/opencontainers/runc/security/advisories/GHSA-cgrx-mc8f-2prm) 和 [2025-31133](https://github.com/opencontainers/runc/security/advisories/GHSA-qw9x-cqr3-wc7r)。

## 4.52.0

{{< release-date date="2025-11-20" >}}


### 新增功能

- 为 Docker Desktop 添加了新的端口绑定设置。管理员也可通过“设置管理”使用 `admin-settings.json` 文件控制此功能。
- 添加了新的 Docker Model Runner 命令。使用 `docker model purge` 可移除所有模型。

### 升级组件

- [Docker Engine v29.0.0](/manuals/engine/release-notes/29.md#2900)
- [Docker Model Runner v1.0.3](https://github.com/docker/model-runner/releases/tag/v1.0.3)
- [Docker Model Runner CLI v1.0.0](https://github.com/docker/model-runner/releases/tag/cmd%2Fcli%2Fv1.0.0)
- Docker MCP 插件 `v0.28.0`

### Bug 修复与增强

#### 全平台通用

- Docker MCP 工具包改进：
   - 支持 Amazon Q 客户端
   - 与 Docker Engine 集成 OAuth DCR（动态客户端注册）
   - 使用 CLI 创建 MCP 配置文件
- Docker Model Runner 改进：
   - 现在可省略 [Docker Model Runner 的 OpenAI API 端点](/manuals/ai/model-runner/api-reference.md#rest-api-examples) 中的 `/engines` 前缀：`curl http://localhost:12434/v1/models`
   - 现在可省略从 Docker Hub 拉取模型时的 `ai/` 前缀（适用于[在 Docker Hub 上发布的模型](https://hub.docker.com/u/ai)）：`docker model pull`
   - 下载中断后现在支持断点续传

#### Windows 平台

- 修复了 Kerberos/NTLM 代理登录问题。

## 4.51.0

{{< release-date date="2025-11-13" >}}


### 新增功能

- 现在可通过 **Kubernetes** 视图设置 Kubernetes 资源。该新视图还提供 Pod、服务和 Deployment 的实时状态显示。

### 升级组件

- [Docker Engine v28.5.2](/manuals/engine/release-notes/28.md#2852)
- Linux 内核 `v6.12.54`

### Bug 修复与增强

#### 全平台通用

- Kind 现在仅在本地不存在所需依赖镜像时才会拉取。

## 4.50.0

{{< release-date date="2025-11-06" >}}


### 新增功能

- [动态 MCP](/manuals/ai/mcp-catalog-and-toolkit/dynamic-mcp.md)（实验性功能）现已在 Docker Desktop 中提供。
- 引入新的欢迎调查问卷以优化入门体验。新用户现在可提供信息，帮助定制其 Docker Desktop 使用体验。

### 升级组件

- [Docker Compose v2.40.3](https://github.com/docker/compose/releases/tag/v2.40.3)
- [NVIDIA Container Toolkit v1.18.0](https://github.com/NVIDIA/nvidia-container-toolkit/releases/tag/v1.18.0)

### Bug 修复与增强

#### 全平台通用

- Docker Desktop 现在可检测并尝试避免“Docker 子网”与使用 RFC1918 地址的物理网络发生冲突。例如，如果主机存在与 `192.168.65.0/24` 重叠的非默认路由，系统将自动选择替代网络。您仍可通过 Docker Desktop 设置和管理设置覆盖此选择。
- Docker Desktop 不再将 Stargz Snapshotter 故障视为致命错误。若发生故障，Docker Desktop 将继续运行（不包含 Stargz Snapshotter）。
- Ask Gordon 不再显示用户提供 URL 的镜像。
- Ask Gordon 现在运行所有内置及用户添加的 MCP 工具前会请求确认。

## 4.49.0

{{< release-date date="2025-10-23" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.49.0" build_path="/208700/" >}}

> [!重要]
>
> 对 Windows 10 21H2 (19044) 和 Windows 11 22H2 (22621) 的支持已结束。下一版本安装 Docker Desktop 将要求 Windows 10 22H2 (19045) 或 Windows 11 23H2 (22631)。

### 安全性

- 修复了 [CVE-2025-9164](https://www.cve.org/cverecord?id=CVE-2025-9164)：Docker Desktop for Windows 安装程序因 DLL 搜索顺序不安全而存在 DLL 劫持漏洞。安装程序在检查系统目录前会先在用户的“下载”文件夹中搜索所需 DLL，攻击者可通过放置恶意 DLL 实现本地权限提升。

### 新增功能

- [Docker Agent](/manuals/ai/docker-agent/_index.md) 现已通过 Docker Desktop 提供。
- [Docker Debug](/reference/cli/docker/debug/) 现已对所有用户免费开放。

### 升级组件

- [Docker Engine v28.5.1](/manuals/engine/release-notes/28.md#2851)
- [Docker Compose v2.40.2](https://github.com/docker/compose/releases/tag/v2.40.2)
- [NVIDIA Container Toolkit v1.17.9](https://github.com/NVIDIA/nvidia-container-toolkit/releases/tag/v1.17.9)
- Docker Debug `v0.0.45`

### Bug 修复与增强

#### 全平台通用

- 修复了 Docker Desktop 在等待用户输入新密码时使用过期代理密码的问题。
- 修复了 Docker Debug 启动时显示的 'chown' 错误。
- 修复了导致部分转发的 UDP 端口挂起的 Bug。

#### macOS 平台

- 修复了当其他 Kubernetes 上下文处于活动状态时 Kubernetes 启动挂起的问题。修复了 https://github.com/docker/for-mac/issues/7771。
- 如果 Rosetta 安装被取消或失败，将在 Docker Desktop 中禁用 Rosetta。
- 在 macOS 上安装或更新 Docker Desktop 的最低操作系统版本现为 macOS Sonoma（版本 14）或更高版本。

## 4.48.0

{{< release-date date="2025-10-09" >}}


> [!重要]
>
> 对 macOS 13 的支持已结束。下一版本安装 Docker Desktop 将要求 macOS 14。

### 新增功能

- 现在可通过安装程序标志为 [macOS](/manuals/desktop/setup/install/mac-install.md#proxy-configuration) 和 [Windows](/manuals/desktop/setup/install/windows-install.md#proxy-configuration) 指定 PAC 文件和嵌入式 PAC 脚本。
- 管理员可通过 [macOS 配置描述文件](/manuals/enterprise/security/enforce-sign-in/methods.md#macos-configuration-profiles-method-recommended) 设置代理配置。

### 升级组件

- [Docker Compose v2.40.0](https://github.com/docker/compose/releases/tag/v2.40.0)
- [Docker Buildx v0.29.1](https://github.com/docker/buildx/releases/tag/v0.29.1)
- [Docker Engine v28.5.1](https://docs.docker.com/engine/release-notes/28/#2851)
- Docker MCP 插件 `v0.22.0`
- [Docker Model CLI v0.1.42](https://github.com/docker/model-cli/releases/tag/v0.1.42)

### Bug 修复与增强

#### 全平台通用

- 修复了 Desktop 重启时 Kind 集群状态偶尔被重置的问题。修复了 [docker/for-mac#77445](https://github.com/docker/for-mac/issues/7745)。
- 移除了过时的 `mcp` 键，以适配最新版 VS Code MCP 服务器的变更。
- 将凭据助手更新至 [v0.9.4](https://github.com/docker/docker-credential-helpers/releases/tag/v0.9.4)。
- 修复了 Docker Desktop 在等待用户输入新密码时使用过期代理密码的问题。
- 修复了导致 Docker Desktop 在特定条件下定期创建带有 Docker CLI 工具的新进程的 Bug。修复了 [docker/for-win#14944](https://github.com/docker/for-win/issues/14944)。
- 修复了导致模型无法通过 Compose 为 Docker Model Runner 配置嵌入的 Bug。如需为模型配置嵌入，必须显式添加 `--embeddings` 运行时标志，详见 [Docker Compose 中的 AI 模型](https://docs.docker.com/ai/compose/models-and-compose/#model-configuration-options)。修复了 [docker/model-runner#166](https://github.com/docker/model-runner/issues/166)。

#### Windows 平台

- 移除了 `HKLM\SOFTWARE\Docker Inc.\Docker\1.0` 注册表项。请改为在 PATH 中查找 `docker.exe` 以确定 Docker Desktop 的安装位置。
- 修复了当 IPv6 被禁用时 WSL 2 模式下的启动问题。

## 4.47.0

{{< release-date date="2025-09-25" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.47.0" build_path="/206054/" >}}

### 安全

- 修复了 [CVE-2025-10657](https://www.cve.org/CVERecord?id=CVE-2025-10657)，该漏洞导致增强型容器隔离（Enhanced Container Isolation）的 [Docker Socket 命令限制](../enterprise/security/hardened-desktop/enhanced-container-isolation/config.md#command-restrictions) 功能在 Docker Desktop 4.46.0 中无法正常工作（相关配置被忽略）。

### 新增功能

- 为 Docker 的 MCP 目录添加了动态 MCP 服务器发现和支持功能。
- 在增强型容器隔离模式下，管理员现在可以阻止容器中挂载 Docker socket 时执行 `docker plugin` 和 `docker login` 命令。
- 新增了一个 Docker Model Runner 命令。使用 `docker model requests` 可以获取请求和响应。

### 升级

- [Docker Compose v2.39.4](https://github.com/docker/compose/releases/tag/v2.39.4)
- [Kubernetes v1.34.1](https://github.com/kubernetes/kubernetes/releases/tag/v1.34.1)
  - [CNI plugins v1.7.1](https://github.com/containernetworking/plugins/releases/tag/v1.7.1)
  - [cri-tools v1.33.0](https://github.com/kubernetes-sigs/cri-tools/releases/tag/v1.33.0)
  - [cri-dockerd v0.3.20](https://github.com/Mirantis/cri-dockerd/releases/tag/v0.3.20)
- Docker Debug `v0.0.44`

### Bug 修复与增强

#### 全平台通用

- 现在可以通过筛选、排序和改进的搜索功能更轻松地搜索 MCP 服务器。
- Docker Debug 在调试设置了空值环境变量的容器时不再挂起。
- 增强了 Docker Model Runner，在 CLI 中提供丰富的响应渲染、在 Docker Desktop Dashboard 中提供对话上下文，并支持可恢复下载。

#### macOS

- 移除了 `com.apple.security.cs.allow-dyld-environment-variables` 权限，该权限允许通过 `DYLD_INSERT_LIBRARIES` 环境变量加载任意签名的动态库到 Docker Desktop。
- 修复了某些客户环境中配置 profile 登录强制策略失效的问题。
- 修复了一个 bug，该 bug 有时会导致 `docker model package` 命令在向本地内容存储写入时挂起（未使用 `--push` 标志时）。
- 修复了以 `unless-stopped` 重启策略启动的容器永远不会重启的问题。修复了 [docker/for-mac#7744](https://github.com/docker/for-mac/issues/7744)。

#### Windows

- 修复了 Windows 上 Docker MCP Toolkit 的 Goose MCP 客户端连接问题。
- 解决了在集成尝试失败后，“跳过集成”WSL 发行版选项的问题。
- 修复了一个 bug，该 bug 有时会导致 `docker model package` 命令在向本地内容存储写入时挂起（未使用 `--push` 标志时）。

## 4.46.0

{{< release-date date="2025-09-11" >}}


### 新增功能

- 为 Docker MCP Toolkit 添加了新的学习中心引导教程以及其他入门改进。
- 管理员现在可以通过 [设置管理](/manuals/enterprise/security/hardened-desktop/settings-management/configure-json-file.md#proxy-settings) 控制 PAC 配置。
- 重新设计了更新体验，使用户更容易理解和管理 Docker Desktop 及其组件的更新。

### 升级

- [Docker Buildx v0.28.0](https://github.com/docker/buildx/releases/tag/v0.28.0)
- [Docker Engine v28.4.0](https://docs.docker.com/engine/release-notes/28/#2840)

### Bug 修复与增强

#### 全平台通用

- 在 Docker CLI 中，现在可以在 Docker 上下文元数据中存在键值对 (`"GODEBUG":"..."`) 时设置 `GODEBUG` 环境变量。这意味着 CLI 二进制文件中包含负序列号的证书现在默认被支持。
- 更新了 Docker 订阅服务协议链接，指向最新版本。

#### macOS

- 通过启用 `llama.cpp` 推理进程的沙盒化，提高了 Docker Model Runner 的安全性。
- 修复了导致 Docker Desktop 启动缓慢并显示为冻结状态的 bug。修复了 [docker/for-mac#7671](https://github.com/docker/for-mac/issues/7671)。

#### Windows

- 通过启用 `llama.cpp` 推理进程的沙盒化，提高了 Docker Model Runner 的安全性。

#### Linux

- 修复了 RHEL 卸载后序列中的路径问题。

## 4.45.0

{{< release-date date="2025-08-28" >}}


### 新增功能

- [Docker Model Runner](/manuals/ai/model-runner/_index.md) 现已全面可用。

### 升级

- [Docker Compose v2.39.2](https://github.com/docker/compose/releases/tag/v2.39.2)
- [Docker Buildx v0.27.0](https://github.com/docker/buildx/releases/tag/v0.27.0)
- [Docker Scout CLI v1.18.3](https://github.com/docker/scout-cli/releases/tag/v1.18.3)
- [Docker Engine v28.3.3](https://docs.docker.com/engine/release-notes/28/#2833)

### Bug 修复与增强

#### 全平台通用

- 修复了当通过需要身份验证的代理上传诊断包时，`com.docker.diagnose` 崩溃的问题。
- `kind` 依赖镜像 `envoyproxy/envoy` 已从 v1.32.0 升级到 v1.32.6。如果您镜像了 `kind` 镜像，请确保您的镜像已更新。

#### macOS

- 修复了笔记本电脑从睡眠状态唤醒后导致 Docker Desktop 崩溃的 bug。修复了 [docker/for-mac#7741](https://github.com/docker/for-mac/issues/7741)。
- 修复了虚拟机有时会因错误 **The virtual machine stopped unexpectedly.** 而失败的问题。
- 修复了容器启动后连接或断开网络时端口映射中断的 bug。修复了 [docker/for-mac#7693](https://github.com/docker/for-mac/issues/7693)。

#### Windows

- 修复了当用户缺乏正确权限时，CLI 插件无法默认部署到 `~/.docker/cli-plugins` 的 bug。
- 修复了当 `docker-desktop` 发行版不存在时，重新定位 WSL 数据发行版会失败的问题。
- 修复了 Docker Desktop Dashboard 中 WSL 安装 URL 的拼写错误。
- 修复了某些 WSL 发行版无法集成的问题。修复了 [docker/for-win#14686](https://github.com/docker/for-win/issues/14686)

## 4.44.3

{{< release-date date="2025-08-20" >}}


### 安全

- 修复了 [CVE-2025-9074](https://www.cve.org/CVERecord?id=CVE-2025-9074)，该漏洞允许在 Docker Desktop 上运行的恶意容器访问 Docker Engine 并启动其他容器，而无需挂载 Docker socket。这可能导致对主机系统上用户文件的未授权访问。增强型容器隔离（ECI）无法缓解此漏洞。

### Bug 修复与增强

- 修复了导致 Docker Offload 对话框阻止用户访问仪表板的 bug。

## 4.44.2

{{< release-date date="2025-08-15" >}}


### Bug 修复与增强

 - 在 **Beta 功能** 设置选项卡中添加了 [Docker Offload](/manuals/offload/_index.md)，并包含了对 [Docker Offload Beta](https://www.docker.com/products/docker-offload/) 的更新支持。

## 4.44.1

{{< release-date date="2025-08-13" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.44.1" build_path="/201842/" >}}

### Bug 修复与增强

#### 全平台通用

- 修复了 4.44.0 版本中发现的问题，该问题导致当 `vpnkit` CIDR 被锁定但未在 Desktop 设置管理中指定值时启动失败。

#### Windows

- 修复了从使用旧版 `version-pack-data` 目录结构的发行版升级后，卷和容器不可见的问题。
- 解决了 WSL 2 中 Docker CLI 偶尔出现 **Proxy Authentication Required**（代理身份验证失败）错误的问题。
- 修复了当用户对 `~/.docker/cli-plugins` 目录没有执行权限时，CLI 插件无法部署到该目录的问题。

## 4.44.0

{{< release-date date="2025-08-07" >}}


### 新增功能

- 提升 WSL 2 的稳定性。
- 您现在可以检查请求和响应，以帮助诊断 Docker Model Runner 中与模型相关的问题。
- 增加了运行多个模型并在资源不足时发出警告的功能。这避免了在使用大型模型时 Docker Desktop 冻结的问题。
- 为 MCP Toolkit 添加了新的 MCP 客户端：Gemini CLI、Goose。
- 为 `docker desktop enable model-runner` 命令引入了 `--gpu`（仅限 Windows）和 `--cors` 参数。
- 为 Docker Desktop CLI 添加了新的 `docker desktop kubernetes` 命令。
- 您现在可以在 **Settings**（设置）中搜索特定的配置选项。
- Apple Virtualization 现在是默认的 VMM，以获得更好的性能，QEMU Virtualization 已被移除。请参阅[博客文章](https://www.docker.com/blog/docker-desktop-for-mac-qemu-virtualization-option-to-be-deprecated-in-90-days/)。
- 对 DockerVMM 进行了性能和稳定性改进。

### 升级组件

- [Docker Compose v2.39.1](https://github.com/docker/compose/releases/tag/v2.39.1)
- [Docker Buildx v0.26.1](https://github.com/docker/buildx/releases/tag/v0.26.1)
- [Docker Engine v28.3.2](https://docs.docker.com/engine/release-notes/28/#2832)
- [Docker Scout CLI v1.18.2](https://github.com/docker/scout-cli/releases/tag/v1.18.2)
- [Docker Model CLI v0.1.36](https://github.com/docker/model-cli/releases/tag/v0.1.36)
- [Docker Desktop CLI v0.2.0](/manuals/desktop/features/desktop-cli.md)

### 安全更新

我们注意到 [CVE-2025-23266](https://nvd.nist.gov/vuln/detail/CVE-2025-23266) 这一严重漏洞，该漏洞影响 CDI 模式下 NVIDIA Container Toolkit 1.17.7 及更早版本。Docker Desktop 包含 1.17.8 版本，不受此漏洞影响。但是，如果手动启用了 CDI 模式，捆绑了早期工具包版本的旧版 Docker Desktop 可能会受到影响。请升级至 Docker Desktop 4.44 或更高版本，以确保使用已修复的版本。

### Bug 修复与增强

#### 所有平台通用

- 修复了在启用 containerd 镜像存储时，拉取带有 zstd 差分层的镜像时出现的问题。
- 修复了在使用增强容器隔离（Enhanced Container Isolation）时，使用 `--restart` 标志启动的容器无法正常重启的 Bug。
- 改进了 [Kubernetes 自定义镜像仓库](/manuals/desktop/use-desktop/kubernetes.md#configuring-a-custom-image-registry-for-kubernetes-control-plane-images) 与增强容器隔离（ECI）之间的交互，因此在使用 Kubernetes 控制平面镜像的自定义镜像仓库时，不再需要手动更新 [ECI Docker Socket 镜像列表](/manuals/enterprise/security/hardened-desktop/enhanced-container-isolation/config.md)。
- 修复了当用户需要登录但当前未登录时，重启 Docker Desktop 后 kind 模式的 Docker Desktop Kubernetes 集群无法启动的 Bug。
- 修复了当启用 [增强容器隔离（Enhanced Container Isolation）](/enterprise/security/hardened-desktop/enhanced-container-isolation/) 时，MCP 密钥无法挂载到容器中的 Bug。
- 修复了当已经指定 `--publish` 时，无法使用 `--publish-all` 的 Bug。
- 修复了 **Images**（镜像）视图无限滚动的 Bug。修复了 [docker/for-mac#7725](https://github.com/docker/for-mac/issues/7725)。
- 修复了资源节省模式（Resource Saver mode）下 **Volumes**（卷）标签页为空的 Bug。
- 更新了首次启动时的服务条款文本。
- 增强了对新发布的 GGUF 格式的解析鲁棒性。

#### macOS 平台

- 修复了在 DockerVMM 上回收磁盘空间时磁盘损坏的问题。
- 通过在一般使用中重新引入性能提升，修复了自 4.42.0 以来 DockerVMM 的回归问题。
- 移除了 QEMU 虚拟机管理程序，并切换到 Apple Virtualization 作为新的默认选项。请参阅[博客文章](https://www.docker.com/blog/docker-desktop-for-mac-qemu-virtualization-option-to-be-deprecated-in-90-days/)。
- 修复了 Traefik 无法自动检测容器端口的 Bug。修复了 [docker/for-mac#7693](https://github.com/docker/for-mac/issues/7693)。
- 修复了容器启动后连接或断开网络时，端口映射中断的 Bug。修复了 [docker/for-mac#7693](https://github.com/docker/for-mac/issues/7693#issuecomment-3131427879)。
- 移除了阻止 `io_uring` 的 eBPF。要在容器中启用 `io_uring`，请使用 `--security-opt seccomp=unconfined`。修复了 [docker/for-mac#7707](https://github.com/docker/for-mac/issues/7707)。
- Docker Model Runner 现在支持 GPT OSS 模型。

#### Windows 平台

- 重新将 `docker-users` 组添加到命名管道安全描述符中。
- 修复了当当前用户没有 `SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall` 注册表项时，安装程序崩溃的问题。
- 修复了 Docker Desktop 可能泄漏 `com.docker.build` 进程并无法启动的 Bug。修复了 [docker/for-win#14840](https://github.com/docker/for-win/issues/14840)。
- 修复了在使用 WSL 且启用了 `cgroups v1` 和增强容器隔离（ECI）时，kind 模式的 Docker Desktop Kubernetes 无法启动的 Bug。
- 修复了 UI 中 WSL 安装 URL 的拼写错误。
- Docker Model Runner 现在支持 GPT OSS 模型。

## 4.43.2

{{< release-date date="2025-07-15" >}}


### 升级组件

- [Docker Compose v2.38.2](https://github.com/docker/compose/releases/tag/v2.38.2)
- [Docker Engine v28.3.2](https://docs.docker.com/engine/release-notes/28/#2832)
- Docker Model CLI v0.1.33

## 4.43.1

{{< release-date date="2025-07-04" >}}


### Bug 修复与增强

#### 所有平台通用

- 修复了当 Ask Gordon 响应包含 HTML 标签时，导致 Docker Desktop UI 崩溃的问题。
- 修复了扩展程序无法与其后端通信的问题。

## 4.43.0

{{< release-date date="2025-07-03" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.43.0" build_path="/198134/" >}}

### 新增功能

- [Compose Bridge](/manuals/compose/bridge/_index.md) 现已全面可用。

### 升级组件

- [Docker Buildx v0.25.0](https://github.com/docker/buildx/releases/tag/v0.25.0)
- [Docker Compose v2.38.1](https://github.com/docker/compose/releases/tag/v2.38.1)
- [Docker Engine v28.3.0](https://docs.docker.com/engine/release-notes/28/#2830)
- [NVIDIA Container Toolkit v1.17.8](https://github.com/NVIDIA/nvidia-container-toolkit/releases/tag/v1.17.8)

### 安全更新

- 修复了 [CVE-2025-6587](https://www.cve.org/CVERecord?id=CVE-2025-6587)，该漏洞导致敏感系统环境变量被包含在 Docker Desktop 诊断日志中，可能导致密钥泄露。

### Bug 修复与增强

#### 所有平台通用

- 修复了 `docker start` 命令在启动已在运行的容器时，丢失容器端口映射的 Bug。
- 修复了容器重启后，GUI 上无法显示容器端口的 Bug。
- 修复了导致 Docker API 在应用启动时出现 `500 Internal Server Error for API route and version` 错误的 Bug。
- 设置中的 **Apply & restart**（应用并重启）按钮现在标记为 **Apply**（应用）。应用更改的设置时，虚拟机不再重启。
- 修复了如果在 `fsck` 期间关闭 Docker，磁盘会被损坏的 Bug。
- 修复了在使用 `kind` Kubernetes 集群时，WSL2 中生成错误的 `~/.kube/config` 的 Bug。
- 如果 Docker Desktop 已被手动暂停，现在会对 Docker API / `docker` CLI 命令返回明确的错误。
- 修复了 Admin 和 Cloud 设置中的未知键导致失败的问题。

#### macOS 平台

- 移除了会阻止 `io_uring` 的 `eBPF`。要在容器中启用 `io_uring`，请使用 `--security-opt seccomp=unconfined`。修复了 [docker/for-mac#7707](https://github.com/docker/for-mac/issues/7707)。

#### Windows 平台

- 修复了当当前用户没有 `SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall` 注册表项时，Docker Desktop 安装程序崩溃的问题。
- 修复了 Docker Desktop 可能泄漏 `com.docker.build` 进程且无法启动的 bug。修复了 [docker/for-win#14840](https://github.com/docker/for-win/issues/14840)

### 已知问题

#### 所有平台

- `docker buildx bake` 不会构建 Compose 文件中包含顶级 models 属性的镜像。请改用 `docker compose build`。
- 包含 HTML 的 Gordon 响应可能导致 Desktop UI 永久损坏。作为临时解决方案，您可以删除 `persisted-state.json` 文件以重置 UI。该文件位于以下目录：
  - Windows: `%APPDATA%\Docker Desktop\persisted-state.json`
  - Linux: `$XDG_CONFIG_HOME/Docker Desktop/persisted-state.json` 或 `~/.config/Docker Desktop/persisted-state.json`
  - Mac: `~/Library/Application Support/Docker Desktop/persisted-state.json`

#### Windows 平台

- Docker Desktop 的“主机网络”功能可能与最新的 WSL 2 Linux 内核存在兼容性问题。如果遇到此类问题，请将 WSL 2 降级至 2.5.7。

## 4.42.1

{{< release-date date="2025-06-18" >}}

### 升级

- [Docker Compose v2.37.1](https://github.com/docker/compose/releases/tag/v2.37.1)

### Bug 修复与增强

#### 所有平台

- 修复了当代理配置无效时 Docker 域名无法访问的问题。
- 修复了暴露端口时可能出现的死锁问题。
- 修复了可能导致 `docker run -p` 端口消失的竞态条件。

#### Mac 平台

- 修复了容器创建后立即查看时其端口列表显示为空的 bug，例如使用脚本时。[docker/for-mac#7693](https://github.com/docker/for-mac/issues/7693)

#### Windows 平台

- 禁用了 WSL 2 中的资源节省模式，以防止 `docker` CLI 命令在 WSL 2 发行版中挂起。[docker/for-win#14656](https://github.com/docker/for-win/issues/14656#issuecomment-2960285463)

## 4.42.0

{{< release-date date="2025-06-04" >}}

### 新增功能

- 扩展了网络兼容性，支持 IPv6。
- Docker MCP 工具包现已原生集成到 Docker Desktop 中。
- Docker Model Runner 现已支持在搭载高通/ARM GPU 的 Windows 系统上使用。
- 在模型视图中添加了**日志**选项卡，可实时查看推理引擎输出。
- Gordon 现已集成 MCP 工具包，可访问 100 多个 MCP 服务器。

### 升级

- [Docker Buildx v0.24.0](https://github.com/docker/buildx/releases/tag/v0.24.0)
- [Docker Engine v28.2.2](https://docs.docker.com/engine/release-notes/28/#2822)
- [Compose Bridge v0.0.20](https://github.com/docker/compose-bridge-binaries/releases/tag/v0.0.20)
- [Docker Compose v2.36.2](https://github.com/docker/compose/releases/tag/v2.36.2)
- [NVIDIA Container Toolkit v1.17.7](https://github.com/NVIDIA/nvidia-container-toolkit/releases/tag/v1.17.7)
- [Docker Scout CLI v1.18.0](https://github.com/docker/scout-cli/releases/tag/v1.18.0)

### Bug 修复与增强

#### 所有平台

- Docker Desktop 现在可接受序列号为负数的证书。
- 默认情况下重新为容器启用 `seccomp`。使用 `docker run --security-opt seccomp=unconfined` 可禁用容器的 seccomp。
- 修复了 Docker Desktop 内存耗尽时挂起的问题。
- 阻止容器中的 `io_uring` 系统调用。
- 添加了对直接从 Docker Hub 拉取模型的支持，简化了访问和使用模型的过程。
- Docker Desktop 现在在新安装时以及重置 Mac 和 Linux 默认设置时，会将磁盘使用限制设置为物理磁盘大小。
- 设置 UI 中的最大磁盘大小现在与主机文件系统的总容量保持一致。
- **模型**视图现在有一个 **Docker Hub** 选项卡，列出了 `ai` 命名空间下的模型。
- 改进了当强制执行超过 10 个组织时的登录强制消息。
- 更改了 Docker Desktop 映射端口的方式，以完全支持 IPv6 端口。
- 修复了仪表板容器日志屏幕中鼠标接近时滚动条消失的问题。
- 为 Teams 订阅用户修复了[强制登录](/manuals/enterprise/security/enforce-sign-in/_index.md)功能。
- `llama.cpp` 服务器现在在 Model Runner 中支持流式传输和工具调用。
- 强制登录功能现已对所有订阅开放。

#### Mac 平台

- 修复了使用 Docker VMM 时磁盘始终具有 64GB 最小使用限制的 bug。
- 禁用了 Docker Desktop Linux VM 中的内存保护密钥机制。这导致 VS Code Dev Containers 无法正常工作。参见 [docker/for-mac#7667](https://github.com/docker/for-mac/issues/7667)。
- 修复了 Kubernetes 下的持久卷声明。修复了 [docker/for-mac#7625](https://github.com/docker/for-mac/issues/7625)。
- 修复了使用 Apple virtualization.framework 时 VM 无法启动的 bug。
- 安装或更新 Docker Desktop 的最低版本现在是 macOS Ventura 13.3。

#### Windows 平台

- 修复了 Windows WSL 上增强容器隔离的 bug，该 bug 导致容器内具有硬链接的文件所有权为 `nobody:nogroup`。
- 修复了导致 Docker Desktop 崩溃的 bug。相关 [docker/for-win#14782](https://github.com/docker/for-win/issues/14782)。
- 修复了使用 WSL 2 启动时出现 `The network name cannot be found` 错误的 bug。修复了 [docker/for-win#14714](https://github.com/docker/for-win/issues/14714)。
- 修复了卸载时 Docker Desktop 不会删除 hosts 文件中条目的问题。
- 修复了读取某些系统语言的自动启动注册表项时的问题。修复了 [docker/for-win#14731](https://github.com/docker/for-win/issues/14731)。
- 修复了 Docker Desktop 添加无法识别的 /etc/wsl.conf `crossDistro` 选项导致 WSL 2 记录错误的 bug。参见 [microsoft/WSL#4577](https://github.com/microsoft/WSL/issues/4577)
- 修复了如果在 WSL 2.5.7 上另一个 WSL 发行版仍在使用 Linux cgroups v1，Docker Desktop 无法启动的 bug。修复了 [docker/for-win#14801](https://github.com/docker/for-win/issues/14801)
- Windows Subsystem for Linux (WSL) 版本 2.1.5 现在是 Docker Desktop 应用程序正常运行所需的最低版本

### 已知问题

#### 所有平台

- 此版本包含 `docker port` 的回归问题，使用 testcontainers-node 时会导致 "No host port found for host IP" 错误。参见 [testcontainers/testcontainers-node#818](https://github.com/testcontainers/testcontainers-node/issues/818#issuecomment-2941575369)

#### Windows 平台

- 使用 Wasm 运行容器时会偶发挂起。参见 [docker/for-mac#7666](https://github.com/docker/for-mac/issues/7666)。
- 在某些机器上，资源节省模式会导致其他 WSL 2 发行版冻结。临时解决方案是禁用资源节省模式。参见 [docker/for-win#14656](https://github.com/docker/for-win/issues/14656)。

## 4.41.2

{{< release-date date="2025-05-06" >}}

### Bug 修复与增强

#### 所有平台

- 修复了即使 Docker Model Runner 不受支持或未启用，GUI 中仍会显示 `Models` 菜单的问题。

## 4.41.1

{{< release-date date="2025-04-30" >}}

### Bug 修复与增强

#### 所有平台

- 修复了当在 `admin-settings.json` 文件中指定代理配置时 Docker Desktop 无法启动的问题。

#### Windows 平台

- 通过避免将 `llama.cpp` DLL 放置在系统 `PATH` 包含的目录中，修复了可能与第三方工具（例如 Ollama）的冲突。

## 4.41.0

{{< release-date date="2025-04-28" >}}

### 新增功能

- Docker Model Runner 现已支持配备 NVIDIA GPU 的 x86 Windows 设备。
- 您现在可以使用 Docker Model Runner 将模型[推送至 Docker Hub](/manuals/ai/model-runner.md#push-a-model-to-docker-hub)。
- 在 Docker Desktop for Mac 和 Windows（支持 Docker Model Runner 的硬件）中新增了对 Docker Model Runner 的模型管理和聊天界面的支持。用户现在可以通过全新的专用界面查看、交互和管理本地 AI 模型。
- [Docker Compose](/manuals/ai/compose/models-and-compose.md) 以及 Testcontainers 的 [Java](https://java.testcontainers.org/modules/docker_model_runner/) 和 [Go](https://golang.testcontainers.org/modules/dockermodelrunner/) 模块现已支持 Docker Model Runner。
- Docker Desktop 现已登陆 [Microsoft 应用商店](https://apps.microsoft.com/detail/xp8cbj40xlbwkx?hl=en-GB&gl=GB)。

### 升级内容

- [Docker Engine v28.1.1](https://docs.docker.com/engine/release-notes/28.1/#2811)
- [Docker Compose v2.35.1](https://github.com/docker/compose/releases/tag/v2.35.1)
- [Docker Buildx v0.23.0](https://github.com/docker/buildx/releases/tag/v0.23.0)
- [Docker Scout CLI v1.17.1](https://github.com/docker/scout-cli/releases/tag/v1.17.1)
- [Compose Bridge v0.0.19](https://github.com/docker/compose-bridge-binaries/releases/tag/v0.0.19)

### 安全修复

- 修复了 [CVE-2025-3224](https://www.cve.org/CVERecord?id=CVE-2025-3224)：当 Docker Desktop 更新时，拥有用户机器访问权限的攻击者可借此实现权限提升。
- 修复了 [CVE-2025-4095](https://www.cve.org/CVERecord?id=CVE-2025-4095)：在使用 macOS 配置描述文件时，注册表访问管理（RAM）策略未被强制执行，导致用户可从未经批准的注册表拉取镜像。
- 修复了 [CVE-2025-3911](https://www.cve.org/CVERecord?id=CVE-2025-3911)：拥有用户机器读取权限的攻击者可从 Docker Desktop 日志文件中获取敏感信息，包括为运行容器配置的环境变量。

### Bug 修复与增强

#### 全平台通用

- 修复了 DockerVMM 中导致主机上打开文件句柄数量过多的问题。
- 修复了当 `admin-settings.json` 文件中缺少可选配置项 `configurationFileVersion` 时 Docker Desktop 无法启动的问题。
- 修复了出站 UDP 连接被过早关闭的问题。
- 增强了日志读取体验，提供高级搜索功能和容器级过滤，便于更快地进行调试和故障排查。
- 改进了下载注册表访问管理配置时的错误提示信息。
- 当 Docker 无法绑定 ICMPv4 套接字时，现在会记录错误并继续运行，而非直接退出。
- 在 Docker Desktop Linux 虚拟机中启用了内存保护密钥机制，使得 Oracle 数据库镜像等容器能够正常运行。
- 修复了当在 Mac、Windows Hyper-V 或 Linux 上启用[增强型容器隔离](/manuals/enterprise/security/hardened-desktop/enhanced-container-isolation/_index.md)时，容器无法访问 `/proc/sys/kernel/shm*` sysctls 的问题。
- 添加了运行 firewalld 所需的 Linux 容器内核模块 `nft_fib_inet`。
- macOS 上的 QEMU 虚拟化选项将于 2025 年 7 月 14 日起弃用。

#### macOS 专用

- 修复了导致 CPU 使用率过高的问题。解决了 [docker/for-mac#7643](https://github.com/docker/for-mac/issues/7643)。
- 修复了 M3 Mac 上使用 Rosetta 进行多架构构建的问题。
- 修复了因缺少 `/Library/Application Support/com.docker.docker/` 目录而导致无法应用 RAM 策略限制的问题。

#### Windows 专用

- Windows `.exe` 安装程序现已改进对锁定文件的处理。解决了 [docker/for-win#14299](https://github.com/docker/for-win/issues/14299) 和 [docker/for-win#14316](https://github.com/docker/for-win/issues/14316)。
- 修复了安装后 `Docker Desktop.exe` 不显示版本信息的问题。解决了 [docker/for-win#14703](https://github.com/docker/for-win/issues/14703)。

### 已知问题

#### 全平台通用

- 如果您已通过 `desktop.plist`（macOS）或注册表键（Windows）强制执行登录，并且同时存在 `registry.json` 文件，则当用户属于 `desktop.plist`/注册表键中列出的组织但不属于 `registry.json` 中指定的任何组织时，登录将失败。要解决此问题，请删除 `registry.json` 文件。

#### Windows 专用

- 如果在 Windows 注册表键 `allowedOrgs` 中使用空格分隔格式指定多个组织，登录将失败且用户会被注销。解决方法是在注册表键值中每行指定一个组织。

## 4.40.0

{{< release-date date="2025-03-31" >}}

### 新增功能

- 您现在可以直接在 Docker Desktop 中使用 [Docker Model Runner（Beta）](/manuals/ai/model-runner.md) 从 Docker Hub 拉取、运行和管理 AI 模型。目前仅适用于搭载 Apple Silicon 芯片的 Docker Desktop for Mac。

### 升级内容

- [Docker Buildx v0.22.0](https://github.com/docker/buildx/releases/tag/v0.22.0)
- [Docker Compose v2.34.0](https://github.com/docker/compose/releases/tag/v2.34.0)
- [Docker Engine v28.0.4](https://docs.docker.com/engine/release-notes/28/#2804)
- [Docker Scout CLI v1.17.0](https://github.com/docker/scout-cli/releases/tag/v1.17.0)
- [compose-bridge v0.0.18](https://github.com/docker/compose-bridge-binaries/releases/tag/v0.0.18)
- [NVIDIA Container Toolkit v1.17.5](https://github.com/NVIDIA/nvidia-container-toolkit/releases/tag/v1.17.5)

### Bug 修复与增强

#### 全平台通用

- 修复了导致 `docker-proxy` 停止将 UDP 数据报转发至容器的问题。
- 修复了 docker-proxy 过早关闭与容器的 UDP 连接并导致源地址不必要变更的问题。
- 修复了某些场景下 Docker Desktop Kubernetes 无法启动的竞态条件问题。
- 改进了 ECI 在配置代理的环境中从仓库收集镜像摘要信息的方式。
- 用户现在可在生成私有扩展市场时使用新的 `--timeout` 标志指定超时时间。
- 移除了 macOS 和 Linux 上未使用的内部辅助工具 `com.docker.admin`。

#### macOS 专用

- 修复了 Docker VMM 中陈旧的目录缓存导致无法检测移动或新增文件的问题。
- 移除了当 Time Machine 工具受限时出现的“继续/重启”弹窗。
- Docker Desktop 现在允许通过 `docker run -v /path/to/unix.sock:/unix.sock` 将 Unix 域套接字共享给容器。绑定挂载时必须指定完整的套接字路径。参见 [for-mac/#483](https://github.com/docker/for-mac/issues/483)。
- 修复了当服务器指定端口存储令牌时，`docker-credential-osxkeychain` 和 `docker-credential-desktop` 返回格式错误 URI 的问题。

#### Windows 专用

- Windows MSI 和 `.exe` 安装程序在安装时默认禁用 Windows 容器（通过 GUI 安装时）。
- 提升了 WSL2 上的端口映射吞吐量。

### 已知问题

#### Windows 专用

- 在显示特权助手错误消息时切换到 Windows 容器可能导致状态不一致。解决方法：退出 Docker Desktop，在 `settings-store.json` 中将 `UseWindowsContainers` 改为 `false`，然后重启 Docker Desktop。
- 安装后，`Docker Desktop.exe` 不包含最新的版本信息。

## 4.39.0

{{< release-date date="2025-03-05" >}}

### 新增功能

- [Docker Desktop CLI](/manuals/desktop/features/desktop-cli.md) 现已全面可用。您现在还可以使用新的 `docker desktop logs` 命令打印日志。
- Docker Desktop 现已支持在 [`docker load`](/reference/cli/docker/image/load/) 和 [`docker save`](/reference/cli/docker/image/save/) 命令中使用 `--platform` 标志。这有助于您导入和导出多平台镜像的子集。

### 升级内容

- [Docker Compose v2.33.1](https://github.com/docker/compose/releases/tag/v2.33.1)  
- [Docker Buildx v0.21.1](https://github.com/docker/buildx/releases/tag/v0.21.1)  
- [Kubernetes v1.32.2](https://github.com/kubernetes/kubernetes/releases/tag/v1.32.2)  
- [Docker Engine v28.0.1](https://docs.docker.com/engine/release-notes/28/#2801)  
- [Docker Scout CLI v1.16.3](https://github.com/docker/scout-cli/releases/tag/v1.16.3)  

### 安全性

- 修复了 [CVE-2025-1696](https://www.cve.org/CVERecord?id=CVE-2025-1696)，该漏洞可能导致代理认证凭据以明文形式出现在日志文件中。

### Bug 修复与增强功能

#### 全平台通用

- Ask Gordon 现在可提供关于 Docker 镜像、容器和卷的更深入上下文信息，提供更快速的技术支持，并允许用户通过 Docker Desktop 和 Docker CLI 执行更多操作。
- 支持多平台镜像，用户可在 `docker history` 中选择特定平台。
- 修复了除 CLI 和 Docker Desktop 外的其他客户端在存在端口映射的容器时出现 3 秒延迟的问题。参见 [docker/for-mac#7575](https://github.com/docker/for-mac/issues/7575)。
- 修复了 ECI Docker 套接字权限中的一个 bug，该 bug 有时会导致允许的镜像或基于允许镜像派生的镜像的容器无法挂载 Docker 套接字。
- 修复了 Docker Desktop 在引擎重启后无法立即再次进入资源节省模式的问题。
- 修复了因 PKI 证书过期导致 Kubernetes 集群停止工作的问题。

#### macOS 平台

- 将 Linux 内核降级至 `v6.10.14`，以修复 OpenJDK 中因 cgroups 控制器识别错误导致 Java 容器终止的问题。参见 [docker/for-mac#7573](https://github.com/docker/for-mac/issues/7573)。
- 在根挂载命名空间中添加 `/usr/share/misc/usb.ids`，以修复 `usbip`。
- 修复了在使用 Docker VMM 时 CPU 限制显示上限为 8 的问题。
- 修复了启动时挂起且 `com.docker.backend` 进程占用 100% CPU 的问题。参见 [docker/for-mac#6951](https://github.com/docker/for-mac/issues/6951)。
- 修复了所有在 M4 MacBook Pro 上运行的 Java 程序发出 SIGILL 错误的问题。参见 [docker/for-mac#7583](https://github.com/docker/for-mac/issues/7583)。
- 阻止在 macOS 15.4 beta 1 上启动，因为启动虚拟机将导致主机崩溃。参见 https://developer.apple.com/documentation/macos-release-notes/macos-15_4-release-notes#Virtual-Machines。
- 修复了 `myIPAddress` PAC 文件函数从错误接口获取主机 IP 的问题，该问题导致代理选择错误。

#### Windows 平台

- 修复了 `docker compose log` 在 WSL 中运行应用时无法流式传输的问题。
- 修复了当 Docker Desktop 使用 WSL 时，Paketo buildpacks 在增强容器隔离（Enhanced Container Isolation）下失败的问题。
- 修复了如果安装了 WSL 版本 1 发行版，WSL 2 集成会失败的问题。
- 修复了当启用 WSL 发行版时，某些 CLI 插件更新失败的问题。
- 修复了使用 PAC 文件进行代理配置时，Docker Desktop 登录界面挂起的问题，该问题导致界面模糊并阻止访问。

#### Linux 平台

- 设置中的**软件更新**页面现在指向最新可用版本。

## 4.38.0

{{< release-date date="2025-01-30" >}}

### 新增功能

- 通过 PKG 安装程序安装 Docker Desktop 现已全面可用。
- 通过配置描述文件强制登录现已全面可用。
- Docker Compose、Docker Scout、Docker CLI 和 Ask Gordon 现在可以独立于 Docker Desktop 更新，且无需完全重启（Beta）。
- 新的 [`update` 命令](/reference/cli/docker/desktop/update/) 已添加到 Docker Desktop CLI（仅限 Mac）。
- [Bake](/manuals//build/bake/_index.md) 现已全面可用，支持权限和可组合属性。
- 您现在可以在 Docker Desktop 中创建[多节点 Kubernetes 集群](/manuals/desktop/settings-and-maintenance/settings.md#kubernetes)。
- [Ask Gordon](/manuals/ai/gordon/_index.md) 现在更广泛可用，仍处于 Beta 阶段。

### 升级组件

- [containerd v1.7.24](https://github.com/containerd/containerd/releases/tag/v1.7.24)
- [Docker Buildx v0.20.1](https://github.com/docker/buildx/releases/tag/v0.20.1)
- [Docker Compose v2.32.4](https://github.com/docker/compose/releases/tag/v2.32.4)
- [Docker Engine v27.5.1](https://docs.docker.com/engine/release-notes/27/#2751)
- [Docker Scout CLI v1.16.1](https://github.com/docker/scout-cli/releases/tag/v1.16.1)
- [Runc v1.2.2](https://github.com/opencontainers/runc/releases/tag/v1.2.2)
- [NVIDIA Container Toolkit v1.17.4](https://github.com/NVIDIA/nvidia-container-toolkit/releases/tag/v1.17.4)
- [Kubernetes v1.31.4](https://github.com/kubernetes/kubernetes/releases/tag/v1.31.4)
- Docker Debug `v0.0.38`

### Bug 修复与增强功能

#### 全平台通用

- 修复了由 `docker login` Web 流程生成的访问令牌无法被 Docker Desktop 刷新的问题。
- 修复了当启用[增强容器隔离（Enhanced Container Isolation）](/manuals/enterprise/security/hardened-desktop/enhanced-container-isolation/_index.md)时，通过 Docker API 使用 `curl` 创建容器失败的问题。
- 修复了刷新期过后 RAM 策略未刷新的问题。
- 修复了在增强容器隔离下，将 Docker 套接字挂载到容器中，然后在该容器内创建带有绑定挂载的 Docker 容器时出现的问题。
- 修复了 GUI 和 CLI 之间存在差异的问题，前者强制在端口映射中使用 `0.0.0.0` 作为 HostIP，导致通过 Engine 的 `ip` 标志或网桥选项 `com.docker.network.bridge.host_binding_ipv4` 配置的默认绑定 IP 未被使用。
- 修复了 `admin-settings.json` 中忽略 `pac` 设置的问题。
- 构建 UI：
  - 导入构建时添加了进度状态。
  - 修复了用户无法导入构建的问题。
  - 修复了某些使用 SSH 端点的构建器未被跳过的问题。

#### macOS 平台

- 修复了 Docker VMM 中从非根卷进行绑定挂载时无法按预期工作的问题。
- 修复了无 IPv6 的系统上启动失败的问题。修复了 [docker/for-mac#14298](https://github.com/docker/for-win/issues/14298)。
- 修复了导致 Docker Desktop 挂起的问题。参见 [docker/for-mac#7493](https://github.com/docker/for-mac/issues/7493#issuecomment-2568594070)。
- 修复了如果设置文件缺失，卸载程序会失败的问题。
- 修复了通过 Workspace One 部署的配置描述文件被忽略的问题。

#### Windows 平台

- Docker Desktop 安装程序现在启动时会显示 UAC 提示。
- 修复了对于使用旧版 WSL 创建且与其他 WSL 发行版共享相同标识符的数据磁盘，Docker Desktop 无法启动的问题。
- 当 WSL 集成设置更改时，Docker Desktop 现在会重启。这确保了在使用增强容器隔离时正确设置 WSL 集成。

#### Linux 平台

- 添加了对 gvisor 网络的支持。使用不兼容版本 qemu（8.x）的用户将继续使用 qemu 网络，其他用户将自动迁移。

### 弃用功能

#### 全平台通用

- 弃用 `com.docker.diagnose check|check-dot|check-hypervisordetect-host-hypervisor`。

## 4.37.2

{{< release-date date="2025-01-09" >}}

### Bug 修复与增强功能

#### macOS 平台

- 防止导致 Docker Desktop 无法将 `com.docker.vmnetd` 或 `com.docker.socket` 更新至较新版本的 bug。

### 已知问题

#### macOS 平台

- 如果您看到关于 `com.docker.vmnetd` 或 `com.docker.socket` 上存在恶意软件的安全弹窗，请按照 [docker/for-mac#7527](https://github.com/docker/for-mac/issues/7527) 中记录的步骤操作。

## 4.37.1

{{< release-date date="2024-12-17" >}}

### Bug 修复与增强功能

#### 全平台通用

- 修复了导致 Docker Hub 中的 AI Catalog 在 Docker Desktop 中不可用的问题。
- 修复了在使用[增强容器隔离](/manuals/enterprise/security/hardened-desktop/enhanced-container-isolation/_index.md)时，Docker Desktop 出现 `index out of range [0] with length 0` 错误的问题。

### 已知问题

#### 适用于 Mac

- 如果您看到关于 `com.docker.vmnetd` 或 `com.docker.socket` 存在恶意软件的安全弹窗，请按照 [docker/for-mac#7527](https://github.com/docker/for-mac/issues/7527) 中记录的步骤操作。

## 4.37.0

{{< release-date date="2024-12-12" >}}

### 新增功能

- 您现在可以直接从[命令行](/manuals/desktop/features/desktop-cli.md)（Beta 版）执行启动、停止、重启和检查 Docker Desktop 状态等关键操作。
- Docker Hub 中的 AI Catalog 现已直接集成到 Docker Desktop 中。

### 升级组件

- [Docker Buildx v0.19.2](https://github.com/docker/buildx/releases/tag/v0.19.2)
- [Docker Compose v2.31.0](https://github.com/docker/compose/releases/tag/v2.31.0)
- [Docker Engine v27.4.0](https://docs.docker.com/engine/release-notes/27/#2740)
- [Docker Scout CLI v1.15.1](https://github.com/docker/scout-cli/releases/tag/v1.15.1)
- [NVIDIA Container Toolkit v1.17.2](https://github.com/NVIDIA/nvidia-container-toolkit/releases/tag/v1.17.2)

### Bug 修复与增强

#### 适用于所有平台

- 新安装中 Docker Engine 的默认磁盘使用限制现已调整为 1TB。
- 修复了容器无法建立环回 `AF_VSOCK` 连接的问题。
- 修复了重置默认设置时也会重置 CLI 上下文的 Bug。
- 修复了以下情况下的 Docker Desktop 仪表板与 Docker 守护进程不同步的问题：
  - 在资源节省模式下重启引擎后（仅限 Windows 使用 WSL2 后端）
  - 在 macOS 上切换引擎后
- 修复了在资源节省模式下重启引擎后，资源节省模式无法重新启用的 Bug。
- Build UI：
  - 修复了某些构建中找不到源文件的 Bug。
  - 修复了 **Source** 标签页中不显示错误日志的 Bug。
  - 修复了 **Source** 标签页中需要滚动到底部才能查看错误日志的 Bug。
  - 修复了 **Logs** 标签页中时间戳显示异常的 Bug。

#### 适用于 Mac

- 修复了在以 `sudo` 权限运行卸载程序两次时，某些用户目录会被创建为 root 权限的 Bug。

#### 适用于 Windows

- 在 WSL 2 的单发行版模式下，增加了对使用 WSL 2 版本 2.3.24 及更高版本的 Windows on ARM 的支持。
- 修复了 Docker Desktop 无法启动的问题。修复了 [docker/for-win#14453](https://github.com/docker/for-win/issues/14453)

### 已知问题

#### 适用于所有平台

- 如果启用了 **Registry Access Manager**，Kubernetes 集群可能无法启动。作为临时解决方案，请将 `registry.k8s.io` 和 `<geo>-docker.pkg.dev` 添加到 **Registry Access Management** 策略中。

#### 适用于 Mac

- 如果您看到关于 `com.docker.vmnetd` 或 `com.docker.socket` 存在恶意软件的安全弹窗，请按照 [docker/for-mac#7527](https://github.com/docker/for-mac/issues/7527) 中记录的步骤操作。

### 弃用功能

#### 适用于 Mac

- 在未来的版本中，Apple Silicon 上的 QEMU（传统模式）将被移除。建议切换到 Apple 虚拟化框架以获得更高的性能和稳定性。如果遇到问题，请[联系 Docker 支持](https://www.docker.com/support/)或[提交 GitHub Issue](https://github.com/docker/for-mac/issues)。
- 在未来的版本中，osxfs（传统模式）将被移除。建议切换到 VirtioFS 以获得更高的性能。如果遇到问题，请[联系 Docker 支持](https://www.docker.com/support/)或[提交 GitHub Issue](https://github.com/docker/for-mac/issues)。

## 4.36.1

{{< release-date date="2025-01-09" >}}

### Bug 修复与增强

#### 适用于 Mac

- 防止了导致 Docker Desktop 无法将 `com.docker.vmnetd` 或 `com.docker.socket` 更新到较新版本的 Bug。

### 已知问题

#### 适用于 Mac

- 如果您看到关于 `com.docker.vmnetd` 或 `com.docker.socket` 存在恶意软件的安全弹窗，请按照 [docker/for-mac#7527](https://github.com/docker/for-mac/issues/7527) 中记录的步骤操作。

## 4.36.0

{{< release-date date="2024-11-18" >}}

### 新增功能

- 在 Windows 上使用 WSL2 引擎的现有 Docker Desktop 安装，现已自动迁移到统一的单发行版架构，以提升一致性和性能。
- 管理员现在可以：
  - 使用 macOS [配置描述文件](/manuals/enterprise/security/enforce-sign-in/methods.md#configuration-profiles-method-mac-only)强制登录（早期访问）。
  - 一次为多个组织强制登录（早期访问）。
  - 使用 [PKG 安装程序](/manuals/enterprise/enterprise-deployment/pkg-install-and-configure.md)批量部署 Docker Desktop for Mac（早期访问）。
  - 使用桌面设置管理功能，通过 admin.docker.com 管理和强制执行默认设置（早期访问）。
- 增强容器隔离（ECI）已改进为：
  - 允许管理员[关闭 Docker 套接字挂载限制](/manuals/enterprise/security/hardened-desktop/enhanced-container-isolation/config.md#allowing-all-containers-to-mount-the-docker-socket)。
  - 在使用 [`allowedDerivedImages` 设置](/manuals/enterprise/security/hardened-desktop/enhanced-container-isolation/config.md#docker-socket-mount-permissions-for-derived-images)时支持通配符标签。

### 升级组件

- [Docker Buildx v0.18.0](https://github.com/docker/buildx/releases/tag/v0.18.0)
- [Docker Compose v2.30.3](https://github.com/docker/compose/releases/tag/v2.30.3)
- [Kubernetes v1.30.5](https://github.com/kubernetes/kubernetes/releases/tag/v1.30.5)
- [NVIDIA Container Toolkit v1.17.0](https://github.com/NVIDIA/nvidia-container-toolkit/releases/tag/v1.17.0)
- [Docker Scout CLI v1.15.0](https://github.com/docker/scout-cli/releases/tag/v1.15.0)
- Docker Init v1.4.0
- Linux 内核 `v6.10.13`

### Bug 修复与增强

#### 适用于所有平台

- 修复了 `docker events` 命令在流式传输事件后不会终止的 Bug。
- Docker Init：改进了不使用 Docker Compose 的 PHP 应用的 Dockerfile 缓存。
- 同步文件共享现在会遵守 `admin-settings.json` 中的 `filesharingAllowedDirectories` 设置。
- 修复了如果 Docker Desktop 配置为使用代理，则由于获取身份验证令牌时内部超时而无法启动的问题。
- 增加了恢复横幅，以便在下载失败时重试更新。
- 修复了如果 `umask` 设置为 `577` 会导致 `rpmbuild` 失败的问题。修复了 [docker/for-mac#6511](https://github.com/docker/for-mac/issues/6511)。
- 修复了限制使用 `--network=host` 的容器只能打开 18 个主机端口的 Bug。
- 修复了非 root 容器的绑定挂载所有权问题。修复了 [docker/for-mac#6243](https://github.com/docker/for-mac/issues/6243)。
- Docker Desktop 在手动暂停后不会自动恢复。系统将保持暂停状态，直到您手动恢复 Docker 引擎。这修复了其他软件在后台运行 CLI 命令时意外触发恢复的 Bug。修复了 [for-mac/#6908](https://github.com/docker/for-mac/issues/6908)
- Build UI：
  - **Source** 标签页现在支持多个源文件。
  - **Info** 标签页中镜像依赖项的链接现在支持其他知名注册表，例如 GitHub、Google 和 GitLab。
  - 如果仅选择了云构建，则禁用 **Delete** 按钮。
  - 修复了用户无法删除构建的问题。
  - 修复了缺少事件和链接的格式错误的 Jaeger 跟踪。
  - 修复了使用云驱动程序构建时缺少导出属性的问题。

#### 适用于 Mac

- 修复了 Docker VMM 中的一个 bug，该 bug 导致 MySQL 和其他数据库容器无法启动。修复了 [docker/for-mac#7464](https://github.com/docker/for-mac/issues/7464) 中的报告。
- 现在，Docker VMM 会自动调整最低内存要求，从而改善用户体验，并解决 [docker/for-mac#7464](https://github.com/docker/for-mac/issues/7464) 和 [docker/for-mac#7482](https://github.com/docker/for-mac/issues/7482) 中的报告。
- 修复了高级选项 **允许特权端口映射** 未按预期工作的 bug。修复了 [docker/for-mac#7460](https://github.com/docker/for-mac/issues/7460)。
- Docker Desktop 现在可以在安装向导和设置界面中自动为 zsh、bash 和 fish 配置 shell 补全脚本。
- 修复了非管理员用户安装 Docker Desktop 或当前用户之前是管理员时，应用内更新会失败的 bug。修复了 [for-mac/#7403](https://github.com/docker/for-mac/issues/7403) 和 [for-mac/#6920](https://github.com/docker/for-mac/issues/6920)

#### 适用于 Windows

- 修复了阻止绑定 UDP 端口 53 的 bug。
- 修复了 Windows 守护进程选项在启动时被覆盖的 bug。

## 4.35.2

{{< release-date date="2025-01-09" >}}


### Bug 修复和增强功能

#### 适用于 Mac

- 防止 Docker Desktop 无法将 `com.docker.vmnetd` 或 `com.docker.socket` 更新到较新版本的 bug。

### 已知问题

#### 适用于 Mac

- 如果您看到关于 `com.docker.vmnetd` 或 `com.docker.socket` 上存在恶意软件的安全弹窗，请按照 [docker/for-mac#7527](https://github.com/docker/for-mac/issues/7527) 中记录的步骤操作。

## 4.35.1

{{< release-date date="2024-10-30" >}}

#### 适用于所有平台

- 修复了 Docker Desktop 错误绑定到端口 `8888` 的 bug。修复了 [docker/for-win#14389](https://github.com/docker/for-win/issues/14389) 和 [docker/for-mac#7468](https://github.com/docker/for-mac/issues/7468)

## 4.35.0

{{< release-date date="2024-10-24" >}}

### 新增功能

- 对 [Docker Desktop on Red Hat Enterprise Linux](/manuals/desktop/setup/install/linux/rhel.md) 的支持现已全面可用。
- 卷备份和共享现已全面可用，可在 **卷** 视图中找到。
- 使用系统 shell 在 Docker Desktop 中支持终端现已全面可用。
- Docker VMM 的测试版发布 - 在 macOS 上替代 Apple 虚拟化框架的更高性能选择（需要 Apple 芯片和 macOS 12.5 或更高版本）。

### 升级

- [containerd v1.7.21](https://github.com/containerd/containerd/releases/tag/v1.7.21)
- [Docker Buildx v0.17.1](https://github.com/docker/buildx/releases/tag/v0.17.1)
- [Docker Compose v2.29.7](https://github.com/docker/compose/releases/tag/v2.29.7)
- [Docker Engine v27.3.1](https://docs.docker.com/engine/release-notes/27/#2731)
- [Docker Scout CLI v1.14.0](https://github.com/docker/scout-cli/releases/tag/v1.14.0)
- Docker Debug `v0.0.37`
- Linux 内核 `v6.10.9`

### Bug 修复和增强功能

#### 适用于所有平台

- 修复了 `daemon.json` 中的代理设置会覆盖 Docker Desktop 设置中代理的 bug。
- 修复了某些 Docker 子网范围无法使用的 bug。
- 移除了 [docker-index](https://github.com/docker/index-cli-plugin)，因为它已被弃用，您可以改用 `docker scout cves fs://<path to binary>`。
- 修复了无法按标签对镜像进行排序或筛选的 bug。修复了 [docker/for-win#14297](https://github.com/docker/for-win/issues/14297)。
- 修复了当 `registry.json` 文件格式错误时，`docker` CLI 无法按预期工作的 bug。
- 修复了 **镜像** 视图中的 **推送到 Docker Hub** 操作会导致 `invalid tag format` 错误的 bug。修复了 [docker/for-win#14258](https://github.com/docker/for-win/issues/14258)。
- 修复了当 ICMPv6 设置不成功时，Docker Desktop 启动失败的问题。
- 添加了允许 USB/IP 工作的驱动程序。
- 修复了增强容器隔离 (ECI) [派生镜像的 Docker 套接字挂载权限](/manuals/enterprise/security/hardened-desktop/enhanced-container-isolation/config.md) 中的 bug，当 Docker Desktop 使用 containerd 镜像存储时，它会错误地拒绝某些镜像的 Docker 套接字挂载。
- 启用 `NFT_NUMGEN`、`NFT_FIB_IPV4` 和 `NFT_FIB_IPV6` 内核模块。
- 构建 UI：
  - 在 **已完成构建** 列表中突出显示构建检查警告。
  - 改进构建时间图表的可视化。
  - 在 **信息** 选项卡下的 **构建结果** 部分添加镜像标签。
- 提高了 Mac 和 Linux 上全新安装的主机端磁盘利用率。
- 修复了当令牌过期时，无法触发登录强制弹窗的 bug。
- 修复了使用 [强制登录](/manuals/enterprise/security/enforce-sign-in/_index.md) 时，登录后容器不会立即显示在 GUI 中的 bug。
- `settings.json` 已重命名为 `settings-store.json`
- 主机网络功能不再要求用户登录才能使用。

#### 适用于 Mac

- 修复了更改设置中的文件共享类型后，自动启动容器可能被错误配置的 bug。
- 修复了启动时 `~/.docker/cli-plugins` 不会被填充的 bug。
- 修复了阻止 php composer 或 postgres 以非 root 用户身份启动的 bug。修复了 [docker/for-mac#7415](https://github.com/docker/for-mac/issues/7415)。
- 修复了可能导致主机上文件更改显示为截断的 bug。修复了 [docker/for-mac#7438](https://github.com/docker/for-mac/issues/7438)。

#### 适用于 Windows

- 现在，Windows 版 Docker Desktop 的新安装需要 Windows 19045 或更高版本。
- 修复了如果在 WSL 的内核配置或内核命令行中禁用 IPv6，则会导致启动失败的问题。修复了 [docker/for-win#14240](https://github.com/docker/for-win/issues/14240)
- 修复了 Windows 上的 **清理/清除数据** 按钮。修复了 [docker/for-win#12650](https://github.com/docker/for-win/issues/14308)。
- 磁盘使用统计信息现在显示在仪表板页脚安装中。
- 改进了 WSL 发行版问题的恢复。

#### 适用于 Linux

- 现在，Docker Desktop 支持 Ubuntu 24.04。

### 已知问题

#### 适用于 Mac

- 自版本 4.34.0 起，高级设置中的切换开关“允许特权端口映射”不起作用。有关更多信息，请参阅 [docker/for-mac#7460](https://github.com/docker/for-mac/issues/7460)。

#### 适用于 Windows

- 版本 4.14.0 及更早版本的用户可能会遇到使用应用内更新的问题。要更新到最新版本，请从此页面下载并安装最新版本的 Docker Desktop。

## 4.34.4

{{< release-date date="2025-01-09" >}}

### Bug 修复和增强功能

#### 适用于 Mac

- 防止 Docker Desktop 无法将 `com.docker.vmnetd` 或 `com.docker.socket` 更新到较新版本的 bug。

### 已知问题

#### 适用于 Mac

- 如果您看到关于 `com.docker.vmnetd` 或 `com.docker.socket` 上存在恶意软件的安全弹窗，请按照 [docker/for-mac#7527](https://github.com/docker/for-mac/issues/7527) 中记录的步骤操作。

## 4.34.3

{{< release-date date="2024-10-09" >}}

{{< desktop-install-v2 all=true win_arm_release="Beta" version="4.34.3" build_path="/170107/" >}}

### 升级

- [NVIDIA Container Toolkit v1.16.2](https://github.com/NVIDIA/nvidia-container-toolkit/releases/tag/v1.16.2)

### 安全

- 修复了 [CVE-2024-9348](https://www.cve.org/cverecord?id=CVE-2024-9348)，该漏洞允许通过镜像构建详细信息源信息进行 RCE
- 修复了 NVIDIA Container Toolkit [CVE-2024-0132](https://nvidia.custhelp.com/app/answers/detail/a_id/5582)
- 修复了 NVIDIA Container Toolkit [CVE-2024-0133](https://nvidia.custhelp.com/app/answers/detail/a_id/5582)

## 4.34.2

{{< release-date date="2024-09-12" >}}

### Bug 修复和增强功能

#### 适用于所有平台

- 修复了在资源节省模式下，`docker compose up` 会变得无响应的 bug。

### 安全

- 修复了 [CVE-2024-8695](https://www.cve.org/cverecord?id=CVE-2024-8695)，该漏洞允许通过精心构造的扩展描述/更新日志实现远程代码执行（RCE），恶意扩展可能利用此漏洞。
- 修复了 [CVE-2024-8696](https://www.cve.org/cverecord?id=CVE-2024-8696)，该漏洞允许通过精心构造的扩展发布者 URL/附加 URL 实现远程代码执行（RCE），恶意扩展可能利用此漏洞。

## 4.34.1

{{< release-date date="2024-09-05" >}}

{{< desktop-install-v2 win=true win_arm_release="Beta" version="4.34.1" build_path="/166053/" >}}

### Bug 修复与增强

#### Windows 平台

- 修复了 Docker Desktop 无法启动（通常在首次启动时）并错误认为应用程序的另一个实例正在运行的 Bug。([docker/for-win#14294](https://github.com/docker/for-win/issues/14294) 和 [docker/for-win#14034](https://github.com/docker/for-win/issues/14034))。

## 4.34.0

{{< release-date date="2024-08-29" >}}

### 新增功能

- Docker Desktop 上的 [Host 网络](/manuals/engine/network/drivers/host.md#docker-desktop) 支持现已全面可用。
- 如果您通过 CLI 进行身份验证，现在可以通过基于浏览器的流程进行身份验证，无需手动生成 PAT。
- Windows 现在支持在 Docker Desktop 中自动回收 WSL2 安装所占用的磁盘空间 [使用托管虚拟硬盘](/manuals/desktop/features/wsl/best-practices.md)。
- 通过 [MSI 安装程序](/manuals/enterprise/enterprise-deployment/msi-install-and-configure.md) 部署 Docker Desktop 现已全面可用。
- 两种新的 [强制登录](/manuals/enterprise/security/enforce-sign-in/_index.md) 方法（Windows 注册表项和 `.plist` 文件）现已全面可用。
- 全新安装的 Docker Desktop 现在默认使用 containerd 镜像存储。
- [Compose Bridge](/manuals/compose/bridge/_index.md)（实验性）现已在 Compose 文件查看器中提供。轻松将您的 Compose 项目转换并部署到 Kubernetes 集群。

### 升级

- [Docker Engine v27.2.0](https://docs.docker.com/engine/release-notes/27.2/#2720)
- [Docker Compose v2.29.2](https://github.com/docker/compose/releases/tag/v2.29.2)
- [containerd v1.7.20](https://github.com/containerd/containerd/releases/tag/v1.7.20)
- [Docker Scout CLI v1.13.0](https://github.com/docker/scout-cli/releases/tag/v1.13.0)
- [Docker Buildx v0.16.2](https://github.com/docker/buildx/releases/tag/v0.16.2)
- Linux 内核 `v6.10.1`

### Bug 修复与增强

#### 所有平台

- 修复了当容器以 AutoRemove (`--rm`) 启动但其端口绑定在启动时被 Docker Desktop 拒绝时，CLI 会空闲的 Bug。
- 修复了 **Support** 屏幕上诊断信息收集偶尔会失败的 Bug。
- 修复了容器 **File** 选项卡中的文件夹无法展开的 Bug。修复了 [docker/for-win#14204](https://github.com/docker/for-win/issues/14204)。
- 应用内更新现在会遵循代理设置。
- 扩展了 ECI Docker 套接字挂载权限功能，可选择性地允许源自允许镜像的子镜像。这使得 ECI 能够与使用 Docker 套接字挂载创建临时本地镜像的构建包（例如 Paketo）配合使用。
- 修复了使用某些代理设置时 **Containers** 视图会闪烁的 Bug。修复了 [docker/for-win#13972](https://github.com/docker/for-win/issues/13972)。
- 改进了 `docker image list` 的输出，以显示与多平台相关的镜像信息。

#### Mac 平台

- 修复了触发配置完整性检查功能时偶尔会出现 `Partial repair error` 的 Bug。
- 配置完整性检查功能现在会显示 Docker 套接字配置错误的原因。
- 修复了如果 Docker Desktop 安装为 `User`，配置完整性检查功能会报告系统路径而不是用户路径的问题。
- 修复了尝试从绑定挂载卷读取扩展属性的应用程序可能会遇到失败的 Bug。修复了 [docker/for-mac#7377](https://github.com/docker/for-mac/issues/7377)。

#### Windows 平台

- 修复了当用户希望保持 `credsStore` 为空时，Docker Desktop 会将其重置为 `desktop` 的 Bug。修复了 [docker/for-win#9843](https://github.com/docker/for-win/issues/9843)。
- 修复了 Docker Desktop 无法在 WSL2 引擎中启动的 Bug [docker/for-win#14034](https://github.com/docker/for-win/issues/14034)。
- 修复了 WSL 发行版会突然终止的 Bug。修复了 [docker/for-win/14230](https://github.com/docker/for-win/issues/14230)。
- 修复了导致 WSL 在每次启动时都会更新的问题。修复了 [docker/for-win/13868](https://github.com/docker/for-win/issues/13868)，[docker/for-win/13806](https://github.com/docker/for-win/issues/13806)。

### 已知问题

- 在 **Experimental** 设置选项卡中启用 Compose Bridge 后，它不会自动工作。您需要等待几分钟，才会收到通知，提示您必须“修复”Docker Desktop，然后才会安装 `compose-bridge` 二进制文件。
- 即使 Kubernetes 正在运行且 Compose Bridge 已启用，Compose 文件查看器中的 **Convert and Deploy** 按钮也可能处于禁用状态。解决方法是：在 **Experimental** 设置选项卡中禁用 Compose Bridge，点击 **Apply & restart** 应用更改，然后重新启用并再次选择 **Apply & restart**。
- 在 Docker CLI 中对注册表进行身份验证时（`docker login [registry address]`），如果提供的注册表地址包含仓库/镜像名称（例如 `docker login index.docker.io/docker/welcome-to-docker`），则仓库部分（`docker/welcome-to-docker`）不会被标准化，导致凭据存储不正确，从而导致后续从该注册表拉取镜像（`docker pull index.docker.io/docker/welcome-to-docker`）时无法通过身份验证。为避免此问题，请在运行 `docker login` 时不要在注册表地址中包含任何无关后缀。
  > [!NOTE]
  > 使用包含 URL 路径段的地址进行 `docker login` 不是文档记录的使用案例，被视为不受支持。建议的用法是仅指定注册表主机名，并可选择指定端口，作为 `docker login` 的地址。
- 当运行 `docker compose up` 且 Docker Desktop 处于资源节省模式时，该命令无响应。解决方法是：手动退出资源节省模式，Docker Compose 将再次响应。
- 启用 [增强容器隔离 (ECI)](/manuals/enterprise/security/hardened-desktop/enhanced-container-isolation/_index.md) 后，Docker Desktop 可能无法进入资源节省模式。这将在未来的 Docker Desktop 版本中修复。
- 新的 [ECI Docker 套接字挂载权限（适用于派生镜像）](/manuals/enterprise/security/hardened-desktop/enhanced-container-isolation/config.md#docker-socket-mount-permissions-for-derived-images) 功能在 Docker Desktop 配置为 **Use containerd for pulling and storing images** 时还无法使用。这将在下一个 Docker Desktop 版本中修复。

## 4.33.2

{{< release-date date="2025-01-09" >}}

### Bug 修复与增强

#### Mac 平台

- 防止导致 Docker Desktop 无法将 `com.docker.vmnetd` 或 `com.docker.socket` 更新到较新版本的 Bug。

### 已知问题

#### Mac 平台

- 如果您看到关于 `com.docker.vmnetd` 或 `com.docker.socket` 上存在恶意软件的安全弹窗，请按照 [docker/for-mac#7527](https://github.com/docker/for-mac/issues/7527) 中记录的步骤操作。

## 4.33.1

{{< release-date date="2024-07-31" >}}

### Bug 修复与增强

#### Windows 平台

- 添加了对 WSL2 2.3.11 及以上版本的支持，其中包括可加载内核模块。修复了 [docker/for-win#14222](https://github.com/docker/for-win/issues/14222)

## 4.33.0

{{< release-date date="2024-07-25" >}}

{{< desktop-install-v2 all=true win_arm_release="Beta" version="4.33.0" build_path="/160616/" >}}

### 新增功能

- [Docker Debug](/reference/cli/docker/debug/) 现已全面发布。
- BuildKit 现在会评估 Dockerfile 规则，以告知您潜在问题。
- **资源分配**设置现在可以直接从仪表板页脚显示的资源使用数据中访问。
- [故障排除](/manuals/desktop/troubleshoot-and-support/troubleshoot/_index.md)体验焕然一新。

### 升级

- [Docker Compose v2.29.1](https://github.com/docker/compose/releases/tag/v2.29.1)
- [Docker Engine v27.1.1](https://docs.docker.com/engine/release-notes/27.1/#2711)
- [containerd v1.7.19](https://github.com/containerd/containerd/releases/tag/v1.7.19)
- [NVIDIA Container Toolkit v1.16.0](https://github.com/NVIDIA/nvidia-container-toolkit/releases/tag/v1.16.0)
- [Docker Scout CLI v1.11.0](https://github.com/docker/scout-cli/releases/tag/v1.11.0)
- [Kubernetes v1.30.2](https://github.com/kubernetes/kubernetes/releases/tag/v1.30.2)
- Linux 内核 `v6.10`

### Bug 修复与增强

#### 所有平台通用

- 修复了使用 `--net=host` 启动并监听 IPv6 地址的容器可从主机访问的问题。
- 优化了**设置**选项卡中启用 containerd 镜像存储的用户体验。
- 修复了在重负载下使用 `grpcfuse` 文件共享选项时出现的死锁问题。
- 修复了 Mac 特定管理设置影响其他平台的问题。
- 现在可以在 Docker Engine 的 `default-address-pools` 中指定 IPv6 地址块。
- 修复了 Docker Engine 的 `bip`、`fixed-cidr` 和 `fixed-cidr-v6` 验证问题。修复了 [docker/for-mac#7104](https://github.com/docker/for-mac/issues/7104)。
- Docker Engine 的 `default-network-opts` 参数现已正确验证。
- VirtioFS 性能改进包括：增加目录缓存超时时间、处理来自主机的变更通知、移除针对 security.capability 属性的额外 FUSE 操作、优化主机事件检测，并提供在容器终止后清理缓存的 API。
- Docker Desktop 现在在主机网络容器中存在端口冲突时会发出通知。
- Compose Bridge 命令行选项现已通过实验性功能提供。启用后，运行 `compose-bridge` 将您的 Compose 配置转换为 Kubernetes 资源。
- 构建视图：
  - 在构建详情的**源**选项卡中添加了[构建检查](/manuals/build/checks.md)。
  - 在构建详情的**信息**选项卡下的**源详情**部分添加了构建标签。
  - 新导入的构建现在会高亮显示。
  - 优化了错误消息处理的性能。
  - 修复了与构建器的连接问题，该问题导致构建记录无法显示。
  - 修复了通过 CLI 打开构建时的导航问题。

#### Mac 平台

- 配置完整性检查功能现在会提供更多上下文，说明您的 Docker Desktop 配置发生了哪些变化。更多信息请参阅 [常见问题解答](/manuals/desktop/troubleshoot-and-support/faqs/macfaqs.md)。
- 配置完整性检查功能在无法修复 Docker Desktop 时会显示错误。
- 修复了 IPv6 TCP 被设置为 `host.docker.internal` 的问题。修复了 [docker/for-mac#7332](https://github.com/docker/for-mac/issues/7332)。
- 修复了 `docker-compose` 符号链接指向空位置的问题。修复了 [docker/for-mac#7345](https://github.com/docker/for-mac/issues/7345)。

#### Linux 平台

- 修复了在卸载后某些 `wincred` 值仍被保留的问题。由 Javier Yong [@Javiery3889](https://github.com/Javiery3889) 报告。
- 修复了错误触发“另一个应用程序更改了您的桌面配置”通知的问题。

### 安全性

#### 所有平台通用

- 包含针对 Docker Engine 中 AuthZ 插件绕过回归问题的修复。更多信息请参阅 [CVE-2024-41110](https://www.cve.org/cverecord?id=CVE-2024-41110)。

#### Windows 平台

- 修复了在卸载后某些 `wincred` 值仍被保留的问题。由 Javier Yong [@Javiery3889](https://github.com/Javiery3889) 报告。

### 已知问题

#### Windows 平台

- Docker Desktop 无法在 WSL 预发布版本 `v2.3.11.0` 和 `v2.3.12.0`（包含在 Windows 11 Insider 中）上启动。要解决此问题，请确保安装了 WSL `v2.2.4.0`。
  更多信息请参阅 [microsoft/WSL#11794](https://github.com/microsoft/WSL/issues/11794)。此问题影响 Docker Desktop 4.33.0 及更早版本。

## 4.32.1

{{< release-date date="2025-01-09" >}}

{{< desktop-install-v2 mac=true version="4.32.1" build_path="/179691/" >}}

### Bug 修复与增强

#### Mac 平台

- 防止导致 Docker Desktop 无法将 `com.docker.vmnetd` 或 `com.docker.socket` 更新到较新版本的 Bug。

### 已知问题

#### Mac 平台

- 如果您看到关于 `com.docker.vmnetd` 或 `com.docker.socket` 上存在恶意软件的安全弹窗，请按照 [docker/for-mac#7527](https://github.com/docker/for-mac/issues/7527) 中记录的步骤操作。

## 4.32.0

{{< release-date date="2024-07-04" >}}

### 新增功能

- Docker Engine 和 CLI 更新至 27.0 版本。
- Docker Desktop 现在支持在 macOS 和 Windows（使用 WSL2 后端）上将数据移动到不同驱动器。请参阅 [docker/for-win#13384](https://github.com/docker/for-win/issues/13384)。
- 您现在可以在**卷**选项卡中为卷导出[安排备份](use-desktop/volumes.md)（Beta）。
- 可直接从 Docker Desktop 访问终端 shell（Beta）。

### 升级

- [Docker Buildx v0.15.1](https://github.com/docker/buildx/releases/tag/v0.15.1)
- [Docker Compose v2.28.1](https://github.com/docker/compose/releases/tag/v2.28.1)
- [Docker Scout CLI v1.10.0](https://github.com/docker/scout-cli/releases/tag/v1.10.0)
- [Docker Engine v27.0.3](https://docs.docker.com/engine/release-notes/27/#2703)
- Docker Init v1.3.0

### Bug 修复与增强

#### 所有平台通用

- 优化了 Compose 文件查看器中 `watch` 的说明
- 为 Docker Init 添加了对没有依赖项的 Golang 项目的支持。解决了 [docker/roadmap#611](https://github.com/docker/roadmap/issues/611)
- [设置管理](/manuals/enterprise/security/hardened-desktop/settings-management/_index.md)现在允许管理员将默认值设为 `ProxyEnableKerberosNTLM`。
- 移除了针对旧版 Visual Studio Code 的临时兼容性修复。
- 构建视图：
  - 将导入构建记录的图标更改为“文件”图标。
  - 优化了尝试连接到已连接的 Docker Build Cloud 构建器时的错误消息。
  - 修复了构建记录意外消失的问题。
  - 修复了用户无法重新打开[导入的构建](use-desktop/builds.md#import-builds)的问题。
  - 修复了当构建状态从运行中变为已完成时构建详情不显示的问题。
  - 修复了构建详情中格式错误的构建源链接。
  - 修复了命名上下文的构建统计信息缺失问题。
  - 修复了构建结果中不再显示镜像索引/清单的问题。
  - 修复了从 UI 导出的构建跟踪在导入 Jaeger 时显示为单一扁平列表的问题。
  - 修复了构建详情中截断的摘要/sha。
  - 修复了活动构建的最终状态动画。

#### Windows 平台

- 修复了 WSL 2 引擎上 Docker Desktop 无法检测到用户手动移动 `docker-desktop-data` 发行版存在的问题。
- Windows on ARM 安装程序和[特权服务](/manuals/desktop/setup/install/windows-permission-requirements.md#privileged-helper)现已针对 ARM64 构建。

#### Mac 平台

- 重新添加了 `CONFIG_DM_CRYPT` 内核模块。
- 重新添加了 `CONFIG_PSI` 内核模块。
- 重新添加了 `CONFIG_GTP` 内核模块。
- 重新添加了 `CONFIG_NFT_BRIDGE_META` 内核模块。
- 修复了当 `/var/run/docker.socket` 指向意外路径时，**另一个应用程序已更改您的桌面配置**警告消息反复出现的问题。
- 将“配置检查”菜单项和横幅更改为通知形式。
- 提升了绑定挂载（bind mounts）读写操作的性能。
- 修复了一些 `AMD64` Java 镜像的致命错误。修复了 [docker/for-mac/7286](https://github.com/docker/for-mac/issues/7286) 和 [docker/for-mac/7006](https://github.com/docker/for-mac/issues/7006)。
- 修复了从 `/Applications` 安装时 Docker Desktop 会删除 `Docker.app` 的问题。
- 修复了导致绑定挂载失败的问题。修复了 [docker/for-mac#7274](https://github.com/docker/for-mac/issues/7274)。

### 已知问题

#### 所有平台通用

- 对于选择启用**访问实验性功能**的所有用户，**使用 Compose 管理同步文件共享**设置会自动启用。这会将所有绑定挂载转换为同步文件共享。要禁用此行为，请取消选中**访问实验性功能**。然后，手动删除任何文件共享：进入**资源**中的**文件共享**选项卡，导航到**同步文件共享**部分，选择要删除的文件共享，然后点击**删除**。

#### macOS 平台

- 更新后运行 `docker-compose` 时，会返回 `command not found`。作为临时解决方案，您可以创建以下符号链接：`sudo ln -sf /Applications/Docker.app/Contents/Resources/cli-plugins/docker-compose /usr/local/bin/docker-compose`

## 4.31.1

### Bug 修复与增强

#### Windows 平台

- 修复了一个 Bug：用户在更新前创建的容器、镜像和卷可能不可见。修复了 [docker/for-win#14118](https://github.com/docker/for-win/issues/14118)。

## 4.31.0

### 新增功能

- [气隙容器（Air-Gapped Containers）](/manuals/enterprise/security/hardened-desktop/air-gapped-containers.md)现已全面可用。
- Docker Compose 文件查看器支持语法高亮显示 Compose YAML 文件，并提供指向相关文档的上下文链接（Beta 版本，逐步推出）。
- 全新的侧边栏用户体验。

### 组件升级

- [Docker Engine 和 CLI v26.1.4](https://github.com/moby/moby/releases/tag/v26.1.4)
- [Docker Scout CLI v1.9.1](https://github.com/docker/scout-cli/releases/tag/v1.9.1)
- [Docker Compose v2.27.1](https://github.com/docker/compose/releases/tag/v2.27.1)
- [Docker Buildx v0.14.1](https://github.com/docker/buildx/releases/tag/v0.14.1)
- [Containerd v1.6.33](https://github.com/containerd/containerd/releases/tag/v1.6.33)
- [Credential Helpers v0.8.2](https://github.com/docker/docker-credential-helpers/releases/tag/v0.8.2)
- [NVIDIA Container Toolkit v1.15.0](https://github.com/NVIDIA/nvidia-container-toolkit/releases/tag/v1.15.0)
- [Go 1.22.4](https://github.com/golang/go/releases/tag/go1.22.4)
- Linux 内核 `v6.6.31`

### Bug 修复与增强

#### 所有平台通用

- 当更新已下载时，**软件更新**设置选项卡现在会显示较新版本的发布信息。
- 在 `settings.json` 中添加了 `proxyEnableKerberosNTLM` 配置，以便在 Kerberos/NTLM 环境未正确设置时，回退到基本代理认证。
- 修复了启用增强容器隔离（Enhanced Container Isolation）时 Docker Debug 无法正常工作的问题。
- 修复了 UDP 响应未正确截断的问题。
- 修复了使用[设置管理（Settings Management）](/manuals/enterprise/security/hardened-desktop/settings-management/_index.md)时**更新**屏幕被隐藏的问题。
- 修复了 `admin-settings.json` 中定义的代理设置在启动时未正确应用的问题。
- 修复了**使用 Compose 管理同步文件共享**开关无法正确反映功能值的问题。
- 修复了在 macOS 上使用 gRPC FUSE 文件共享，以及在 Windows 上使用 Hyper-V 时，主机上修改的绑定挂载文件在容器重启后未更新的问题。修复了 [docker/for-mac#7274](https://github.com/docker/for-mac/issues/7274)、[docker/for-win#14060](https://github.com/docker/for-win/issues/14060)。
- 构建视图：
  - 新增[导入构建（Import builds）](use-desktop/builds.md#import-builds)功能，允许您导入其他人创建的构建记录，或[CI 环境中的构建](/manuals/build/ci/github-actions/build-summary.md)。
  - 修复了失败构建的构建结果中缺少 OpenTelemetry 跟踪的问题。
  - 修复了 `default-load` 在容器驱动中显示为无效 driver-opt 的问题。
  - 修复了指向构建详情的深度链接。

#### Windows 平台

- 将 `--allowed-org` 安装程序标志更改为写入策略注册表项，而非 `registry.json`。

#### macOS 平台

- 将**自动检查配置**设置从**高级**设置移至**常规**设置。
- 通过实现更长的属性超时和失效机制，改进了 VirtioFS 缓存。

#### Linux 平台

- 在虚拟机中添加了 Linux 头文件，以简化自定义内核模块的编译。

### 安全性

#### 所有平台通用

- 修复了增强容器隔离（ECI）模式中的一个安全漏洞：用户可以在 Docker Desktop 虚拟机中从受限目录创建 Docker 卷，并将其挂载到容器中，从而使容器能够访问这些受限的虚拟机目录。
- 默认情况下，仅允许安装市场（marketplace）中列出的扩展。此设置可在 Docker Desktop 的设置中更改。扩展开发者需要更改此选项才能测试其扩展。

#### Windows 平台

- 修复了 [CVE-2024-5652](https://www.cve.org/cverecord?id=CVE-2024-5652)：`docker-users` 组中的用户可通过 Windows 容器模式下的 `exec-path` Docker 守护进程配置选项，导致 Windows 拒绝服务（Denial-of-Service）。该漏洞由 Hashim Jawad ([@ihack4falafel](https://github.com/ihack4falafel)) 与 Trend Micro Zero Day Initiative 合作发现。

### 弃用

#### 所有平台通用

- 之前以 `com.docker.cli` 形式提供的 CLI 二进制文件，现在直接以 `docker` 提供。本版本仍保留 CLI 二进制文件为 `com.docker.cli`，但将在下一版本中移除。

#### Windows 平台

- 移除了对 WSL2 引擎中旧版本包的支持。

### 已知问题

#### Windows 平台

- 升级到 Docker Desktop 4.31.0 时，在仅使用 WSL 的 Windows 主机上，使用 Docker Desktop 4.8.0 或更早版本创建的现有容器、镜像和卷对用户将变得不可见。数据并未丢失，只是在 Docker Desktop 4.31.0 中不可见。如果受影响，请降级到 4.30 或更早版本。更多信息请参阅：[docker/for-win#14118](https://github.com/docker/for-win/issues/14118)。

#### Linux 平台

- Ubuntu 24.04 LTS 尚未支持，Docker Desktop 将无法启动。由于最新版 Ubuntu 对非特权命名空间的限制方式发生变化，需要至少运行一次 `sudo sysctl -w kernel.apparmor_restrict_unprivileged_userns=0`。请参阅 [Ubuntu 博客](https://ubuntu.com/blog/)。

## 4.30.0

{{< release-date date="2024-05-06" >}}

### 新增功能

#### 所有平台通用

- Docker Desktop 现在支持 [SOCKS5 代理](/manuals/desktop/features/networking.md#socks5-proxy-support)。需要 Business 订阅。
- 在[设置管理（Settings Management）](/manuals/enterprise/security/hardened-desktop/settings-management/_index.md)中添加了新的设置，用于管理入门调查。

#### Windows 平台

- 在 Windows 上添加了对 [Kerberos 和 NTLM 代理认证](/manuals/desktop/settings-and-maintenance/settings.md#proxy-authentication)的支持。需要 Business 订阅。

### 组件升级

- [Docker Compose v2.27.0](https://github.com/docker/compose/releases/tag/v2.27.0)
- [Docker Engine v26.1.1](https://docs.docker.com/engine/release-notes/26.1/#2611)
- [Wasm](/manuals/desktop/features/wasm.md) runtimes:
  - 更新 `runwasi` shims 至 `v0.4.0`
  - 更新 `deislabs` shims 至 `v0.11.1`
  - 更新 `spin` shim 至 `v0.13.1`
- [Docker Scout CLI v1.8.0](https://github.com/docker/scout-cli/releases/tag/v1.8.0)
- Docker Debug `v0.0.29`
- Linux 内核 `v6.6.26`
- [Go 1.22.2](https://github.com/golang/go/releases/tag/go1.22.2)

### Bug fixes and enhancements

#### For all platforms

- 改进了在无根容器中运行 `docker build` 命令时的增强容器隔离 (ECI) 安全性。
- 修复了当 Docker Desktop 进入/退出资源节省模式时，`docker events` 因 `Unexpected EOF` 而退出的问题。
- 修复了当 Docker Desktop 处于资源节省模式时，`docker stats --no-stream` 挂起的问题。
- 修复了自诊断 CLI 中错误显示虚拟机未启动的问题。修复了 [docker/for-mac#7241](https://github.com/docker/for-mac/issues/7241)。
- 修复了高吞吐量端口转发传输可能停滞的问题。修复了 [docker/for-mac#7207](https://github.com/docker/for-mac/issues/7207)。
- 修复了移除 CLI 应用时 CLI 插件符号链接未被移除的问题。
- 修复了共享端口抽屉中针对本地引擎显示错误消息的问题。
- 开发环境功能已停用，并移至 **开发中的功能** 下的 **Beta** 选项卡。
- 构建视图：
  - 改进了构建记录的批量删除功能。
  - 新增操作：在构建依赖项中打开容器镜像和 Git 源的相应网页。
  - 新增操作：以下载 Jaeger 或 OTLP 格式的 Provenance 和 OpenTelemetry 跟踪信息。
  - 修复了远程构建调用的源详细信息。
  - 修复了使用云构建器时多平台构建会显示为单独记录的问题。

#### For Mac

- 修复了在 2019 年之后的 Mac 上使用 Virtualization Framework 时触发段错误的问题。参见 [docker/for-mac#6824](https://github.com/docker/for-mac/issues/6824)。
- 启用了 `CONFIG_SECURITY=y` 内核配置，例如用于 [Tetragon](https://tetragon.io/)。修复了 [docker/for-mac#7250](https://github.com/docker/for-mac/issues/7250)。
- 重新添加了对 `SQUASHFS` 压缩的支持。修复了 [docker/for-mac#7260](https://github.com/docker/for-mac/issues/7260)。
- 修复了导致新版本 Docker Desktop 被标记为损坏的问题。
- 在使用 Apple Silicon 上的 qemu 时增加了网络 MTU。
- 修复了未安装 Rosetta 时 Docker Desktop 无法启动的问题。修复了 [docker/for-mac#7243](https://github.com/docker/for-mac/issues/7243)。

#### For Windows

- 为 WSL2 添加了简化的配置模式，避免了对辅助 `docker-desktop-data` WSL 发行版的需求（实验性）。
- 修复了 WSL 环境中 Docker CLI 的 bash 补全功能。
- 修复了 Docker Desktop 4.28 中的回归问题，该问题导致在使用 WSL 上的 Docker-in-Docker（通过挂载 `/var/run/docker.sock`）时，绑定挂载到容器中的主机文件在容器内无法正确显示。
- 修复了导致以下错误的问题：`merging settings: integratedWslDistros type mismatch`。

### Known issues

#### For all platforms

- 如果您启用了 Docker Desktop 中需要您登录的功能（例如 **主机网络**），则必须保持登录状态才能使用 Docker Desktop。要继续使用 Docker Desktop 或修改这些设置，请确保您已登录。
- 要启用或禁用 **使用 Compose 管理同步文件共享**，必须同时勾选或取消勾选 **访问实验性功能** 和 **使用 Compose 管理同步文件共享**。
- 当运行带有自动移除选项 (`--rm`) 的容器时，如果容器启动失败（例如：`docker run --rm alpine invalidcommand`），Docker CLI 有时会挂起。在这种情况下，可能需要手动终止 CLI 进程。

#### For Windows

- 当以非管理员用户身份启动 Docker Desktop 时，如果用户不是 **docker-users** 组的成员，可能会触发以下错误：`connect ENOENT \\.\pipe\errorReporter`。
  可以通过将用户添加到 **docker-users** 组来解决此问题。在启动 Docker Desktop 之前，请确保先注销，然后重新登录，并使用 `wsl --unregister docker-desktop` 注销 `docker-desktop` 发行版（如果已创建）。

#### For Linux

- Ubuntu 24.04 LTS 尚不受支持，Docker Desktop 将无法启动。由于最新 Ubuntu 版本对非特权命名空间的限制方式发生了变化，因此需要至少运行一次 `sudo sysctl -w kernel.apparmor_restrict_unprivileged_userns=0`。有关更多详细信息，请参阅 [Ubuntu 博客](https://ubuntu.com/blog/ubuntu-23-10-restricted-unprivileged-user-namespaces)。

## 4.29.0

{{< release-date date="2024-04-08" >}}

### New

- 您现在可以通过 [设置管理](/manuals/enterprise/security/hardened-desktop/settings-management/_index.md) 强制使用 Rosetta。
- 使用 ECI 的 [Docker 套接字挂载限制](/manuals/enterprise/security/hardened-desktop/enhanced-container-isolation/config.md) 现已全面可用。
- Docker Engine 和 CLI 已更新至 [Moby 26.0](https://github.com/moby/moby/releases/tag/v26.0.0)。这包括 Buildkit 0.13、子卷挂载、网络更新以及对 containerd 多平台镜像存储用户体验的改进。
- 全新且改进的 Docker Desktop 错误屏幕：快速故障排除、轻松上传诊断信息以及可操作的修复措施。
- Compose 支持 [同步文件共享（实验性）](/manuals/desktop/features/synchronized-file-sharing.md)。
- 新的 [交互式 Compose CLI（实验性）](/manuals/compose/how-tos/environment-variables/envvars.md#compose_menu)。
- Beta 版本发布：
  - 使用 [设置管理](/manuals/enterprise/security/hardened-desktop/air-gapped-containers.md) 的气隙容器。
  - Docker Desktop 中的 [主机网络](/manuals/engine/network/drivers/host.md#docker-desktop)。
  - 运行容器的 [Docker Debug](use-desktop/container.md#integrated-terminal)。
  - **卷**选项卡中提供 [卷备份与共享扩展](use-desktop/volumes.md) 功能。

### Upgrades

- [Docker Compose v2.26.1](https://github.com/docker/compose/releases/tag/v2.26.1)
- [Docker Scout CLI v1.6.3](https://github.com/docker/scout-cli/releases/tag/v1.6.3)
- [Docker Engine v26.0.0](https://docs.docker.com/engine/release-notes/26.0/#2600)
- [Buildx v0.13.1](https://github.com/docker/buildx/releases/tag/v0.13.1)
- [Kubernetes v1.29.2](https://github.com/kubernetes/kubernetes/releases/tag/v1.29.2)
- [cri-dockerd v0.3.11](https://github.com/Mirantis/cri-dockerd/releases/tag/v0.3.11)
- Docker Debug v0.0.27

### Bug fixes and enhancements

#### For all platforms

- 修复了下拉菜单在应用程序窗口外打开的问题。
- Docker Init：
  - 更新了 CLI 输出的格式，提高了可读性。
  - 修复了 `.dockerignore` 的问题，避免忽略以 "compose" 开头的应用程序文件。
  - 根据 Spring Boot 版本改进了 Java 应用程序的启动方式。修复了 [docker/for-mac#7171](https://github.com/docker/for-mac/issues/7171)。
  - 移除了用于 Rust 交叉编译的非官方 Docker 镜像。
- 每个[同步文件共享](/manuals/desktop/features/synchronized-file-sharing.md)的最大文件数现在超过 200 万。
- 修复了选择**导出到本地镜像**字段时出现警告“_提供给 Autocomplete 的值无效。_”的问题。
- **运行云端**现在可以从 Docker Desktop 仪表板访问。
- 选择退出分析数据发送后，现在也会禁用错误报告的数据收集。
- 您现在可以在**容器**视图中共享和取消共享端口到云端引擎。
- 共享云端现在可以从**仪表板**右侧页脚访问。
- 为 macOS、Windows 和 Linux 版 Docker Desktop 添加了主机网络连接的 Beta 支持 [docker#238](https://github.com/docker/roadmap/issues/238)。
- 为新的未读通知添加了时间戳。
- 修复了虚拟化支持错误消息中的拼写错误。修复了 [docker/desktop-linux#197](https://github.com/docker/desktop-linux/issues/197)。
- Docker Desktop 现在允许通过 PAC 文件中的规则阻止对 `host.docker.internal` 的连接。
- 修复了**镜像**和**容器**列表中二级菜单位置的问题。
- 修复了使用 QEMU 启动 Docker Desktop 时出现的竞态条件。
- 改进了当镜像拉取被注册表访问管理策略阻止时的错误消息。
- 在内核配置中重新添加了 `CONFIG_BONDING=y`。

#### 适用于 Mac

- 修复了 Kubernetes 无法成功启动的问题。修复了 [docker/for-mac#7136](https://github.com/docker/for-mac/issues/7136) 和 [docker/for-mac#7031](https://github.com/docker/for-mac/issues/7031)。
- 修复了浏览器无法将身份验证信息发送回 Docker Desktop 的错误。修复了 [docker/for-mac/issues#7160](https://github.com/docker/for-mac/issues/7160)。

#### 适用于 Windows

- 修复了在 WSL 2 和 Hyper-V 之间切换后 `docker run -v` 失败的问题。
- 修复了 Docker Desktop 关闭时未停止其 WSL 发行版（`docker-desktop` 和 `docker-desktop-data`）的问题。修复了 [docker/for-win/issues/13443](https://github.com/docker/for-win/issues/13443) 和 [docker/for-win/issues/13938](https://github.com/docker/for-win/issues/13938)。

#### 适用于 Linux

- 修复了 UI 中可用实验性功能列表与后端数据不同步的问题。

#### 安全性

- 禁用了 Electron 的 `runAsNode` 熔断机制以提高安全性。更多信息请参见 [Electron 文档](https://www.electronjs.org/blog/statement-run-as-node-cves)。
- 修复了 [CVE-2024-6222](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-6222)，该漏洞允许已通过容器逃逸获得 Docker Desktop 虚拟机访问权限的攻击者，通过传递扩展和仪表板相关的 IPC 消息进一步逃逸到主机。由 Trend Micro 零日计划合作的 Billy Jheng Bing-Jhong、Đỗ Minh Tuấn 和 Muhammad Alifa Ramdhan 报告。

### 已知问题

#### 适用于 Mac

- 如果未安装 Rosetta，Apple Silicon 上的 Docker Desktop 将无法启动。这将在未来版本中修复。参见 [docker/for-mac#7243](https://github.com/docker/for-mac/issues/7243)。

## 4.28.0

{{< release-date date="2024-02-26" >}}

### 新增功能

- [设置管理](/manuals/enterprise/security/hardened-desktop/settings-management/_index.md) 现在允许管理员设置默认的文件共享实现，并指定开发者可以添加文件共享的路径。
- 当启用 [`SOCKS` 代理支持 Beta 功能](/manuals/desktop/features/networking.md) 时，添加了对 `socks5://` HTTP 和 HTTPS 代理 URL 的支持。
- 用户现在可以在**卷**选项卡中筛选卷，查看哪些正在使用中。

### 升级

- [Compose v2.24.6](https://github.com/docker/compose/releases/tag/v2.24.6)
- [Docker Engine v25.0.3](https://docs.docker.com/engine/release-notes/25.0/#2503)
- [Docker Scout CLI v1.5.0](https://github.com/docker/scout-cli/releases/tag/v1.5.0)
- [Qemu 8.1.5](https://wiki.qemu.org/ChangeLog/8.1)
- [Wasm](/manuals/desktop/features/wasm.md) 运行时：
  - 将 runwasi shims 更新至 `v0.4.0`，包括：
    - wasmtime `v17.0`，初步支持 WASI preview 2
    - wasmedge `v0.13.5`
    - wasmer `v4.1.2`
  - 将 deislabs shims 更新至 `v0.11.1`，包括：
    - lunatic `v0.13.2`
    - slight `v0.5.1`
    - spin `v2.2.0`
    - wws `v1.7.0`

### Bug 修复与增强

#### 适用于所有平台

- 修复了 `postgis` 与 `Qemu` 的问题。修复了 [docker/for-mac#7172](https://github.com/docker/for-mac/issues/7172)。
- 为 `kpartx` 重新添加了 `CONFIG_BLK_DEV_DM` 内核配置。修复了 [docker/for-mac#7197](https://github.com/docker/for-mac/issues/7197)。
- 允许通过代理自动配置 `pac 文件` 设置 `SOCKS` 代理。
- 重新添加了 `CONFIG_AUDIT` 内核配置。
- 修复了 `virtiofs` 上 Rust 构建的错误。参见 [rust-lang/docker-rust#161](https://github.com/rust-lang/docker-rust/issues/161)。
- 修复了拉取 Kubernetes 镜像时出现“缺少注册表身份验证”错误的问题。
- 修复了导致 Docker Compose 命令挂起的问题。
- 修复了 `docker build` 中导致 Docker Desktop 崩溃的错误。修复了 [docker/for-win#13885](https://github.com/docker/for-win/issues/13885)、[docker/for-win#13896](https://github.com/docker/for-win/issues/13896)、[docker/for-win#13899](https://github.com/docker/for-win/issues/13899)、[docker/for-mac#7164](https://github.com/docker/for-mac/issues/7164)、[docker/for-mac#7169](https://github.com/docker/for-mac/issues/7169)
- Docker Init：
  - 根据 Spring Boot 版本改进了 Java 应用程序的启动方式。修复了 [docker/for-mac#7171](https://github.com/docker/for-mac/issues/7171)。
  - 移除了用于 Rust 交叉编译的非官方 Docker 镜像
- 构建视图：
  - 活跃和已完成的构建现在可以在专用选项卡中找到。
  - 构建详情现在显示构建持续时间和缓存步骤。
  - OpenTelemetry 跟踪现在显示在构建结果中。
  - 修复了上下文构建器事件并非总是触发的问题。
  - 重新设计了空状态视图，使仪表板更清晰。

#### 适用于 Mac

- 修复了 Rosetta 的 `httpd` 问题。[docker/for-mac#7182](https://github.com/docker/for-mac/issues/7182)
- 修复了 `virtualization.framework` 导致崩溃的错误。修复了 [docker/for-mac#7024](https://github.com/docker/for-mac/issues/7024)

#### 适用于 Windows

- 修复了 Windows 上的 DNS 超时问题。
- 添加了对 WSL 用户发行版中增强容器隔离 Docker 套接字挂载权限的支持。
- 修复了从 CLI 重定向输出时出现“无法获取控制台模式”错误的问题。
- 修复了容器内挂载引擎套接字权限的问题。修复了 [docker/for-win#13898](https://github.com/docker/for-win/issues/13898)

### 已知问题

#### 适用于 Windows

- 在深色模式下，**资源**>**高级**设置中的**磁盘镜像位置**不可见。解决方法：切换到浅色模式。

## 4.27.2

{{< release-date date="2024-02-08" >}}

### 升级

- [Compose v2.24.5](https://github.com/docker/compose/releases/tag/v2.24.5)
- [Docker Scout CLI v1.4.1](https://github.com/docker/scout-cli/releases/tag/v1.4.1)
- Docker Debug v0.0.24

### Bug 修复与增强

#### 适用于所有平台

- 修复了从终端上传诊断信息时诊断 ID 无法正确打印的问题。
- 修复了使用“设置管理”时，默认设置值在启动时被重置为默认值的问题。
- 修复了即使禁用了 **Docker Desktop 启动时打开 Docker 仪表板** 选项，仪表板仍会在启动时显示的问题。修复了 [docker/for-win#13887](https://github.com/docker/for-win/issues/13887)。
- 修复了构建后端服务中的错误，该错误导致 Docker Desktop 崩溃。修复了 [docker/for-win#13885](https://github.com/docker/for-win/issues/13885)、[docker/for-win#13896](https://github.com/docker/for-win/issues/13896)、[docker/for-win#13899](https://github.com/docker/for-win/issues/13899)、[docker/for-mac#7164](https://github.com/docker/for-mac/issues/7164)、[docker/for-mac#7169](https://github.com/docker/for-mac/issues/7169)。
- 修复了容器内挂载 Docker Engine 套接字时的权限问题。修复了 [docker/for-win#13898](https://github.com/docker/for-win/issues/13898)。
- Docker Scout：
  - 更新了依赖项，以解决 Leaky Vessels 系列 CVE 漏洞（[CVE-2024-21626](https://github.com/advisories/GHSA-xr7r-f8xq-vfvv)、[CVE-2024-24557](https://github.com/advisories/GHSA-xw73-rw38-6vjc)）
  - 添加了初始 VEX 文档，用于记录误报 [CVE-2020-8911](https://github.com/advisories/GHSA-f5pg-7wfw-84q9) 和 [CVE-2020-8912](https://github.com/advisories/GHSA-7f33-f4f5-xwgw)
  - 添加了对 cosign SBOM 证明的支持
  - 添加了对 VEX in-toto 证明的支持
- Docker Debug：
  - 修复了拉取镜像时资源访问管理背后的错误
  - 修复了连接问题

#### 适用于 Mac

- 重新添加了 `Istio` 所需的内核模块。修复了 [docker/for-mac#7148](https://github.com/docker/for-mac/issues/7148)。
- 现在，Node 在 Rosetta 下使用所有可用的核心。
- 修复了 `php-fpm` 的问题。修复了 [docker/for-mac#7037](https://github.com/docker/for-mac/issues/7037)。

## 4.27.1

{{< release-date date="2024-02-01" >}}

### 升级

- [Docker Engine v25.0.2](https://docs.docker.com/engine/release-notes/25.0/#2502)，其中包含对 [CVE-2024-24557](https://scout.docker.com/vulnerabilities/id/CVE-2024-24557)、[CVE-2024-23650](https://scout.docker.com/vulnerabilities/id/CVE-2024-23650)、[CVE-2024-23651](https://scout.docker.com/vulnerabilities/id/CVE-2024-23651)、[CVE-2024-23652](https://scout.docker.com/vulnerabilities/id/CVE-2024-23652) 和 [CVE-2024-23653](https://scout.docker.com/vulnerabilities/id/CVE-2024-23653) 的修复
- [Containerd v1.6.28](https://github.com/containerd/containerd/releases/tag/v1.6.28)
- [Runc v1.1.12](https://github.com/opencontainers/runc/releases/tag/v1.1.12)，其中包含对 [CVE-2024-21626](https://scout.docker.com/vulnerabilities/id/CVE-2024-21626) 的修复

### Bug 修复和增强

#### 适用于 Mac

- 修复了应用更新时导致 Docker Desktop 挂起的问题。

## 4.27.0

{{< release-date date="2024-01-25" >}}

### 新增功能

- Docker init 现在支持 Java，并向所有用户正式发布。
- [同步文件共享](/manuals/desktop/features/synchronized-file-sharing.md) 在 Docker Desktop 中提供快速灵活的宿主机到虚拟机文件共享。利用 [Docker 收购 Mutagen](https://www.docker.com/blog/mutagen-acquisition/) 背后的技术，此功能提供了一种替代虚拟绑定挂载的方法，使用同步文件系统缓存，提高了处理大型代码库的开发人员的性能。
- 组织管理员现在可以在启用 ECI 时[配置 Docker 套接字挂载权限](/manuals/enterprise/security/hardened-desktop/enhanced-container-isolation/config.md)。
- [Containerd 镜像存储](/manuals/desktop/features/containerd.md) 支持现在向所有用户正式发布。
- 使用新的 [`docker debug` 命令](/reference/cli/docker/debug.md)（Beta）获取任何容器或镜像的调试 shell。
- 拥有 Docker Business 订阅的组织管理员现在可以配置自定义扩展列表，并启用 [私有扩展市场](/manuals/extensions/private-marketplace.md)（Beta）

### 升级

- [Amazon ECR 凭据助手 v0.7.1](https://github.com/awslabs/amazon-ecr-credential-helper/releases/tag/v0.7.1)
- [Buildx v0.12.1](https://github.com/docker/buildx/releases/tag/v0.12.1)
- [Containerd v1.6.27](https://github.com/containerd/containerd/releases/tag/v1.6.27)
- [Compose v2.24.3](https://github.com/docker/compose/releases/tag/v2.24.3)
- [Docker 凭据助手 v0.8.1](https://github.com/docker/docker-credential-helpers/releases/tag/v0.8.1)
- [Runc v1.1.11](https://github.com/opencontainers/runc/releases/tag/v1.1.11)
- [Docker Engine v25.0.0](https://docs.docker.com/engine/release-notes/25.0/)
- [Kubernetes v1.29.1](https://github.com/kubernetes/kubernetes/releases/tag/v1.29.1)
- [Docker Scout v1.3.0](https://github.com/docker/scout-cli/releases/tag/v1.3.0)

### Bug 修复和增强

#### 适用于所有平台

- `docker scan` 命令已被移除。要继续了解镜像的漏洞以及许多其他功能，请使用 [`docker scout` 命令](/reference/cli/docker/scout/)。
- 修复了选中 **始终下载更新** 复选框时自动更新无法下载的问题。
- 修复了仪表板工具提示中的拼写错误。修复了 [docker/for-mac#7132](https://github.com/docker/for-mac/issues/7132)
- 改进了信号处理行为（例如，在终端中运行 `docker` 命令时按 Ctrl-C）。
- 重新添加了 `minikube start --cni=cilium` 所需的内核模块。
- 修复了登录后启用管理员控制时安装屏幕再次出现的问题。
- 修复了共享文件夹不再存在时 Docker 无法启动的问题。
- 修复了仪表板 **容器** 部分中显示的可用 CPU 数量。
- 重新添加了 `btrfs`、`xfs`、`vfat`、`exfat`、`ntfs3`、`f2fs`、`squashfs`、`udf`、`9p` 和 `autofs` 的内核模块。
- 容器使用图表已移至垂直的 **资源使用情况** 侧面板，以便在容器列表中提供更多空间。通过 **显示图表** 按钮访问使用图表的方式保持不变。
- 修复了登录时选择 **关闭应用程序** 会留下挂起的后端进程的问题。
- 修复了通过“设置管理”禁用分析时导致 Docker Desktop 无响应的问题。
- Docker init：
  - 添加了对容器化 Java 服务器的支持
  - 在 Windows 上的各种修复
- 构建器设置：
  - 现在可以随时刷新构建器的存储数据。
  - 现在可以删除构建器的构建历史记录。
- 构建视图：
  - 当构建记录无法删除时，现在会显示错误消息。
  - 修复了在 macOS 上以 rootless 模式创建云构建器的问题。
  - 内联缓存和 Git 源现在在 **信息** 标签的 **构建时间** 部分中得到正确处理。
  - 在 **历史记录** 标签的过去构建中，现在会显示使用的构建器和调用构建的作者。
  - 对 **历史记录** 标签的过去构建的链接进行了多项改进。
  - 对构建名称的准确性进行了多项改进。
  - 修复了当构建器无法访问时 **活动构建** 列表中构建卡住的问题。
  - 修复了在某些情况下无法删除构建记录的问题。
  - 修复了构建名称可能为空的问题。
  - 修复了在启用资源节省模式时构建视图的一般问题。

#### 适用于 Mac

- 启用了 `Huge Pages` 并修复了 Rosetta 下的 PHP 段错误。修复了 [docker/for-mac#7117](https://github.com/docker/for-mac/issues/7117)。
- 修复了 Rosetta 下的 `xvfb`。修复了 [docker/for-mac#7122](https://github.com/docker/for-mac/issues/7122)
- 修复了 Rosetta 下的 `ERR_WORKER_INVALID_EXEC_ARGV` 错误。[docker/for-mac#6998](https://github.com/docker/for-mac/issues/6998)。
- 修复了如果 `admin-settings.json` 语法无效，Docker Desktop 可能死锁的问题。

#### 适用于 Windows

- 修复了阻止某些区域设置将 UTF-16 字符串编码为 UTF-8 的错误。修复了 [docker/for-win#13868](https://github.com/docker/for-win/issues/13868)。
- 修复了 WSL 集成中应用重启时凭据存储配置会重置的错误。修复了 [docker/for-win#13529](https://github.com/docker/for-win/issues/13529)。
- 修复了阻止正确 WSL 引擎错误传递给用户的问题。
- 修复了从 Windows 容器模式退出时导致 Docker Desktop 挂起的问题。

### 安全

#### Windows 平台

- 缓解了 Windows 上 Docker Desktop 安装程序中的多个 DLL 侧加载漏洞，由 Suman Kumar Chakraborty ([@Hijack-Everything](https://github.com/Hijack-Everything)) 报告

### 已知问题

#### 所有平台

- 使用设置管理时，未在 `admin-settings.json` 中设置的配置项将在 Docker Desktop 启动时重置为默认值。

#### Mac 平台

- 从**软件更新**升级到 4.27.0 有时会卡住。作为临时解决方案，请使用此页面的 4.27.0 安装程序。

## 4.26.1

{{< release-date date="2023-12-14" >}}

### Bug 修复与增强

#### 所有平台

- 更新了 Docker Desktop 内部的反馈链接，确保其继续正常工作

#### Windows 平台

- 将 CLI 二进制文件切换为兼容旧版本 glibc 的版本，例如 Ubuntu 20.04 中使用的版本，修复了 [docker/for-win#13824](https://github.com/docker/for-win/issues/13824)

## 4.26.0

{{< release-date date="2023-12-04" >}}

### 新功能

- 管理员现在可以通过[设置管理](/manuals/enterprise/security/hardened-desktop/settings-management/_index.md)控制对**开发中的功能**标签页中测试版和实验性功能的访问权限。
- 在底部状态栏中引入了四种新的版本更新状态。
- `docker init`（测试版）现在支持 PHP + Apache + Composer。
- [**构建**视图](use-desktop/builds.md)现已正式发布（GA）。您现在可以检查构建、排查错误并优化构建速度。

### 升级

- [Compose v2.23.3](https://github.com/docker/compose/releases/tag/v2.23.3)
- [Docker Scout CLI v1.2.0](https://github.com/docker/scout-cli/releases/tag/v1.2.0)
- [Buildx v0.12.0](https://github.com/docker/buildx/releases/tag/v0.12.0)
- [Wasm](/manuals/desktop/features/wasm.md) 运行时：
  - wasmtime、wasmedge 和 wasmer `v0.3.1`
  - lunatic、slight、spin 和 wws `v0.10.0`
  - Wasmtime 现在基于 wasmtime `v14.0`，支持 wasi preview-2 组件
  - Wasmedge 现在基于 WasmEdge `v0.13.5`
  - Spin 现在基于 Spin `v2.0.1`
  - wws 现在基于 wws `v1.7.0`
- [Docker Engine v24.0.7](https://docs.docker.com/engine/release-notes/24.0/#2407)
- [Containerd v1.6.25](https://github.com/containerd/containerd/releases/tag/v1.6.25)
- [runc v1.1.10](https://github.com/opencontainers/runc/releases/tag/v1.1.10)

### Bug 修复与增强

#### 所有平台

- 您现在可以通过命令行使用 `docker feedback` 提交反馈。
- 改进了**通用**设置标签页中启动选项的文本和位置。
- 重新设计了仪表板的标题栏，添加了指向其他 Docker 资源的链接，并改进了账户信息的显示。
- 修复了同时启用 containerd 镜像存储和 Wasm 时无法启用 Wasm 的错误。
- containerd 集成：
  - 修复了在未提供 `ServerAddress` 的情况下，`docker push/pull` 认证未发送到非 DockerHub 注册表的问题。
  - 修复了 `docker history` 报告错误 ID 和标签的问题。
  - 修复了 `docker tag` 未保留内部元数据的问题。
  - 修复了配置了 `--userns-remap` 的守护进程执行 `docker commit` 时的问题。
  - 修复了 `docker image list` 以显示真实的镜像创建日期。
  - 为 `docker pull` 添加了 `-a` 标志支持（拉取所有远程仓库标签）。
  - 为 `docker run` 添加了 `--group-add` 标志支持（追加额外组）。
  - 调整了 `docker push/pull` 报告的一些错误。
- Docker Init：
  - 改进了 Golang 和 Rust 的 Dockerfile 交叉编译。
  - 改进了 ASP.NET Core 的 Dockerfile 缓存。
- Docker Desktop 现在在仪表板底部提供有关待处理更新的更详细信息。
- 修复了增强容器隔离模式下 `docker run --init` 失败的问题。
- 修复了提示用户下载新版本的 Docker Desktop 通知在用户开始下载后仍保持可见的错误。
- 添加了指示 Docker Desktop 正在安装新版本的提示。
- 修复了当用户悬停在无操作按钮的通知上时光标变为指针的错误。

#### Mac 平台

- 修复了 Rosetta 无法与 PHP 一起使用的问题。修复了 [docker/for-mac#6773](https://github.com/docker/for-mac/issues/6773) 和 [docker/for-mac#7037](https://github.com/docker/for-mac/issues/7037)。
- 修复了多个与 Rosetta 无法工作相关的问题。修复了 [[docker/for-mac#6973](https://github.com/docker/for-mac/issues/6973)、[[docker/for-mac#7009](https://github.com/docker/for-mac/issues/7009)、[[docker/for-mac#7068](https://github.com/docker/for-mac/issues/7068) 和 [[docker/for-mac#7075](https://github.com/docker/for-mac/issues/7075)
- 改进了 Rosetta 下 NodeJS 的性能。
- 修复了**无法打开 /proc/self/exe** Rosetta 错误。
- 修复了**登录时启动 Docker Desktop**设置无法工作的错误。修复了 [docker/for-mac#7052](https://github.com/docker/for-mac/issues/7052)。
- 您现在可以通过 UI 启用 UDP 的 Kernel 网络路径。修复了 [docker/for-mac#7008](https://github.com/docker/for-mac/issues/7008)。
- 修复了 `uninstall` CLI 工具丢失的回归问题。
- 解决了在使用设置管理禁用分析时导致 Docker Desktop 无响应的问题。

#### Windows 平台

- 添加了对 WSL 镜像模式网络的支持（需要 WSL `v2.0.4` 或更高版本）。
- 为 DLL 和 VBS 文件添加了缺失的签名。

### 已知问题

#### Windows 平台

- 在较旧的 Linux 发行版（例如 Ubuntu 20.04）上使用 WSL 2 集成时，Docker CLI 无法工作，这些发行版使用的 `glibc` 版本低于 `2.32`。这将在未来版本中修复。参见 [docker/for-win#13824](https://github.com/docker/for-win/issues/13824)。

## 4.25.2

{{< release-date date="2023-11-21" >}}

### Bug 修复与增强

#### 所有平台

- 修复了**欢迎调查**中提交响应后出现空白 UI 的错误。

#### Windows 平台

- 修复了 WSL 2 上的 Docker Desktop 在空闲时意外关闭 dockerd 的错误。修复了 [docker/for-win#13789](https://github.com/docker/for-win/issues/13789)

## 4.25.1

{{< release-date date="2023-11-13" >}}

### Bug 修复与增强

#### 所有平台

- 修复了 4.25 中的回归问题，即交换文件损坏时 Docker 无法启动。损坏的交换文件将在下次启动时重新创建。
- 修复了交换被禁用时的错误。修复了 [docker/for-mac#7045](https://github.com/docker/for-mac/issues/7045)、[docker/for-mac#7044](https://github.com/docker/for-mac/issues/7044) 和 [docker/for-win#13779](https://github.com/docker/for-win/issues/13779)。
- `sysctl vm.max_map_count` 现在设置为 262144。参见 [docker/for-mac#7047](https://github.com/docker/for-mac/issues/7047)

#### Windows 平台

- 修复了某些用户托盘菜单中不显示**切换到 Windows 容器**的问题。参见 [docker/for-win#13761](https://github.com/docker/for-win/issues/13761)。
- 修复了使用 `sh` 以外的 shell 时 WSL 集成无法工作的问题。参见 [docker/for-win#13764](https://github.com/docker/for-win/issues/13764)。
- 重新添加了 `DockerCli.exe`。

## 4.25.0

{{< release-date date="2023-10-26" >}}

### 新功能

- Rosetta 现已面向所有运行 macOS 13 或更高版本的用户全面开放。它可显著提升 Apple Silicon 芯片对基于 Intel 架构镜像的模拟运行速度。如需使用 Rosetta，请参阅[设置](/manuals/desktop/settings-and-maintenance/settings.md)。在 macOS 14.1 及更高版本中，Rosetta 默认已启用。
- Docker Desktop 现在能够检测 WSL 版本是否过时。若检测到 WSL 版本过旧，您可以允许 Docker Desktop 自动更新安装，也可以选择在 Docker Desktop 外部手动更新 WSL。
- 新版 Windows 版 Docker Desktop 的安装现要求 Windows 版本为 19044 或更高。
- 管理员现在可通过[设置管理](/manuals/enterprise/security/hardened-desktop/settings-management/_index.md)控制 Docker Scout 镜像分析功能。

### 升级内容

- [Compose v2.23.0](https://github.com/docker/compose/releases/tag/v2.23.0)
- [Docker Scout CLI v1.0.9](https://github.com/docker/scout-cli/releases/tag/v1.0.9)
- [Kubernetes v1.28.2](https://github.com/kubernetes/kubernetes/releases/tag/v1.28.2)
  - [cri-dockerd v0.3.4](https://github.com/Mirantis/cri-dockerd/releases/tag/v0.3.4)
  - [CNI 插件 v1.3.0](https://github.com/containernetworking/plugins/releases/tag/v1.3.0)
  - [cri-tools v1.28.0](https://github.com/kubernetes-sigs/cri-tools/releases/tag/v1.28.0)

### Bug 修复与增强功能

#### 全平台通用

- 修复了“接受许可协议”弹窗中的间距问题。
- 修复了**通知抽屉**在“通知列表”与“通知详情”视图间切换时尺寸变化的问题。
- containerd 集成改进：
  - `docker push` 现支持显示“Layer already exists”（层已存在）和“Mounted from”（挂载自）进度状态。
  - `docker save` 现在能够导出仓库中所有标签的镜像。
  - 隐藏清单、配置和索引（小型 JSON 数据块）的推送上传进度，以匹配原始推送行为。
  - 修复了 `docker diff` 包含额外差异的问题。
  - 修复了 `docker history` 无法显示使用经典构建器构建的镜像的中间镜像 ID 的问题。
  - 修复了 `docker load` 无法从压缩 tar 归档加载镜像的问题。
  - 修复了注册表镜像无法正常工作的问题。
  - 修复了 `docker diff` 在同一容器上并发多次调用时无法正常工作的问题。
  - 修复了 `docker push` 在向同一注册表的不同仓库推送层时无法复用层的问题。
- Docker Init 改进：
  - 修复了生成文件中包含的 Docker 文档链接过期的问题
  - 新增对 ASP.NET Core 8 的支持（除 6 和 7 之外）
- 修复了安装 Wasm shims 时失败的问题。
- 修复了 Docker Desktop 每 15 分钟退出[资源节省模式](https://docs.docker.com/desktop/use-desktop/resource-saver/)的问题；若计时器设置超过 15 分钟，则资源节省模式永远不会启动。
- 将**启用后台 SBOM 索引**选项提升至**通用设置**中。

#### macOS 专属

- 在 macOS 上安装或更新 Docker Desktop 所需的最低操作系统版本现为 macOS Monterey（版本 12）或更高。
- 当用户身份与 `Docker.app` 所有者不匹配导致无法完成更新时，增强了错误提示信息。修复了 [docker/for-mac#7000](https://github.com/docker/for-mac/issues/7000)。
- 修复了当 `/var/run/docker.sock` 配置错误时，**重新应用配置**可能失效的问题。
- 若 `/usr/local/bin` 中已存在 `ECRCredentialHelper`，Docker Desktop 将不再覆盖该文件。

#### Windows 专属

- 修复了 Windows 家庭版中托盘菜单仍显示**切换到 Windows 容器**选项的问题。修复了 [docker/for-win#13715](https://github.com/docker/for-win/issues/13715)

#### Linux 专属

- 修复了 `docker login` 的问题。修复了 [docker/docker-credential-helpers#299](https://github.com/docker/docker-credential-helpers/issues/299)

### 已知问题

#### macOS 专属

- 升级至 macOS 14 可能导致 Docker Desktop 自动更新至最新版本，即使已禁用自动更新选项。
- 暂不支持通过命令行卸载 Docker Desktop。作为临时解决方案，您可通过[仪表板卸载 Docker Desktop](https://docs.docker.com/desktop/uninstall/)。

#### Windows 专属

- Windows 系统托盘菜单中的**切换到 Windows 容器**选项可能不显示。作为临时解决方案，请编辑 [`settings.json` 文件](/manuals/desktop/settings-and-maintenance/settings.md) 并将 `"displaySwitchWinLinContainers"` 设置为 `true`。

#### 全平台通用

- 若交换文件大小设置为 0MB，执行拉取镜像或登录等 Docker 操作时将出现“连接被拒绝”或“超时”错误。作为临时解决方案，请在**设置**的**资源**选项卡中将交换文件大小配置为非零值。

## 4.24.2

{{< release-date date="2023-10-12" >}}

### Bug 修复与增强功能

#### 全平台通用

- 修复了 Docker Desktop 向 `notify.bugsnag.com` 发送多个请求的问题。修复了 [docker/for-win#13722](https://github.com/docker/for-win/issues/13722)。
- 修复了 PyTorch 的性能回归问题。

## 4.24.1

{{< release-date date="2023-10-04" >}}

### Bug 修复与增强功能

#### Windows 专属

- 修复了 Windows 版 Docker Desktop 仪表板无法正确显示容器日志的问题。修复了 [docker/for-win#13714](https://github.com/docker/for-win/issues/13714)。

## 4.24.0

{{< release-date date="2023-09-28" >}}

### 新增功能

- 全新的通知中心现已向所有用户开放，您可接收新版本发布、安装进度更新等通知。点击 Docker Desktop 仪表板右下角的铃铛图标即可访问通知中心。
- Compose Watch 现已向所有用户开放。更多信息请参阅[使用 Compose Watch](/manuals/compose/how-tos/file-watch.md)。
- 资源节省模式现已向所有用户开放并默认启用。如需配置此功能，请前往**设置**中的**资源**选项卡。更多信息请参阅 [Docker Desktop 的资源节省模式](use-desktop/resource-saver.md)。
- 您现在可直接通过 Docker Desktop 仪表板查看和管理 Docker 引擎状态，包括暂停、停止和恢复操作。

### 升级内容

- [Compose v2.22.0](https://github.com/docker/compose/releases/tag/v2.22.0)
- [Go 1.21.1](https://github.com/golang/go/releases/tag/go1.21.1)
- [Wasm](/manuals/desktop/features/wasm.md) 运行时：
  - wasmtime, wasmedge `v0.2.0`
  - lunatic, slight, spin 和 wws `v0.9.1`
  - 新增 wasmer wasm shims

### Bug 修复与增强功能

#### 全平台通用

- Docker Init 改进：
  - 修复了 Windows 上 ASP.NET 项目 Dockerfile 文件路径格式化的问题
  - 提升了包含大量文件的目录的语言检测性能
- 为**容器**视图使用的资源使用统计轮询添加了超时机制。修复了 [docker/for-mac#6962](https://github.com/docker/for-mac/issues/6962)。
- containerd 集成改进：
  - 实现了推送/拉取/保存镜像事件
  - 实现了拉取传统 schema1 镜像
  - 实现了 `docker push --all-tags`
  - 实现了统计使用特定镜像的容器数量（例如可在 `docker system df -v` 中查看）
  - 验证拉取的镜像名称未被保留
  - 处理 `userns-remap` 守护进程设置
  - 修复了使用多个 COPY/ADD 指令时传统构建器的构建错误
  - 修复了 `docker load` 导致存储池损坏从而影响后续镜像相关操作的问题
  - 修复了无法通过带 `sha256:` 前缀的截断摘要引用镜像的问题
  - 修复了 `docker images`（不带 `--all` 参数）显示中间层（由传统经典构建器创建）的问题
  - 修复了 `docker diff` 包含额外差异的问题
  - 更改了 `docker pull` 输出，使其与禁用 containerd 集成时的输出保持一致
- 修复了 Kubernetes 状态消息中的语法错误。参见 [docker/for-mac#6971](https://github.com/docker/for-mac/issues/6971)。
- Docker 容器现在默认使用所有主机 CPU 核心。
- 增强了仪表板 UI 的进程间安全性。

#### macOS 专属

- 修复了 macOS 版本早于 12.5 的 Apple Silicon Mac 上的内核崩溃问题。修复了 [docker/for-mac#6975](https://github.com/docker/for-mac/issues/6975)。
- 修复了当 `filesharingDirectories` 中包含无效目录时 Docker Desktop 无法启动的问题。修复了 [docker/for-mac#6980](https://github.com/docker/for-mac/issues/6980)。
- 修复了安装程序创建 root 用户拥有目录的问题。修复了 [docker/for-mac#6984](https://github.com/docker/for-mac/issues/6984)。
- 修复了在缺少 `/Library/LaunchDaemons` 时安装程序设置 docker socket 失败的问题。修复了 [docker/for-mac#6967](https://github.com/docker/for-mac/issues/6967)。
- 修复了在 macOS 上将特权端口绑定到非 localhost IP 时出现的权限被拒绝错误。修复了 [docker/for-mac#697](https://github.com/docker/for-mac/issues/6977)。
- 修复了 4.23 版本中引入的资源泄漏问题。相关 [docker/for-mac#6953](https://github.com/docker/for-mac/issues/6953)。

#### Windows 平台

- 修复了当服务已在运行时仍弹出“Docker Desktop 服务未运行”提示的问题。参见 [docker/for-win#13679](https://github.com/docker/for-win/issues/13679)。
- 修复了导致 Docker Desktop 在 Windows 主机上启动失败的问题。修复了 [docker/for-win#13662](https://github.com/docker/for-win/issues/13662)。
- 修改了 Docker Desktop 资源节省器功能，当没有容器运行时跳过减少 WSL 的内核内存，因为这在某些情况下会导致超时。建议用户直接在 .wslconfig 文件中启用 "autoMemoryReclaim"（自 WSL 1.3.10 起可用）。

### 已知问题

#### Mac 平台

- 使用端口 53 创建容器会失败，并显示地址 `already in use` 错误。作为解决方法，请在位于 `~/Library/Group Containers/group.com.docker/settings.json` 的 `settings.json` 文件中添加 `"kernelForUDP": false` 来停用网络加速。

## 4.23.0

{{< release-date date="2023-09-11" >}}

### 升级

- [Compose v2.21.0](https://github.com/docker/compose/releases/tag/v2.21.0)
- [Docker Engine v24.0.6](https://docs.docker.com/engine/release-notes/24.0/#2406)
- [Docker Scout CLI v0.24.1](https://github.com/docker/scout-cli/releases/tag/v0.24.1)。
- [Wasm](/manuals/desktop/features/wasm.md) 运行时：
  - wasmtime, wasmedge 版本 `d0a1a1cd`。
  - slight 和 spin wasm `v0.9.0`。

### 新增功能

- 新增对 Wasm 运行时的支持：wws 和 lunatic。
- [`docker init`](/reference/cli/docker/init/) 现在支持 ASP.NET
- 提高了 macOS 上暴露端口的性能，例如使用 `docker run -p` 时。

### 移除功能

- 从 Docker Desktop 中移除了 Compose V1，因为它已停止接收更新。Compose V2 已取代它，并集成到所有当前版本的 Docker Desktop 中。

### Bug 修复和增强

#### 所有平台

- 使用 [Docker Scout](../scout/_index.md)，您现在可以：
  - 使用 `docker scout cache` 管理临时和缓存文件。
  - 使用 `docker scout environment` 管理环境。
  - 使用 `docker scout config` 配置默认组织。
  - 使用 `docker scout cves --format only-packages` 列出镜像的包及其漏洞。
  - 使用 `docker scout enroll` 注册组织到 Docker Scout。
  - 使用 `docker scout cves --type fs` 停止、分析和比较本地文件系统。
- 修复了当 Docker Desktop 处于资源节省模式时 `docker stats` 会挂起的问题。
- 修复了通过 Docker Desktop 仪表板的 **设置** 关闭实验性功能后资源节省模式未完全关闭的问题。
- 修复了 **容器列表** 操作按钮被裁剪的问题。
- containerd 镜像存储：
  - 修复了与某些镜像交互时出现的 `failed to read config content` 错误。
  - 修复了在启用传统经典构建器 (`DOCKER_BUILDKIT=0`) 时构建带有 `FROM scratch` 指令的 Dockerfile 的问题。
  - 修复了在启用传统经典构建器 (`DOCKER_BUILDKIT=0`) 时构建镜像时出现的 `mismatched image rootfs errors` 错误。
  - 修复了 `ONBUILD` 和 `MAINTAINER` Dockerfile 指令。
  - 修复了健康检查。

#### Mac 平台

- 所有 macOS 12.5 或更高版本的用户现在默认启用 VirtioFS。您可以在 **设置** 的 **常规** 选项卡中恢复此设置。
- 提高了单流 TCP 吞吐量。
- 重新启用了 macOS 的健康检查，当系统发生变化可能导致 Docker 二进制文件运行问题时通知您。

#### Linux 平台

- 修复了当打开 Docker Desktop 应用两次时 GUI 被杀死的问题。参见 [docker/desktop-linux#148](https://github.com/docker/desktop-linux/issues/148)。

#### Windows 平台

- 修复了非管理员用户在切换到 Windows 容器或禁用 WSL 并切换到 Hyper-V 引擎时被提示输入凭据的问题。
  此问题会在操作系统重启后或 Docker Desktop 冷启动时发生。

### 安全性

#### 所有平台

- 修复了 [CVE-2023-5165](https://www.cve.org/cverecord?id=CVE-2023-5165)，该漏洞允许通过调试 shell 绕过增强容器隔离。受影响的功能仅对 Docker Business 客户可用，并假设用户未被授予本地 root 或管理员权限的环境。
- 修复了 [CVE-2023-5166](https://www.cve.org/cverecord?id=CVE-2023-5166)，该漏洞允许通过特制的扩展图标 URL 窃取访问令牌。

### 已知问题

- 在 Docker Desktop 上绑定特权端口在 macOS 上不起作用。作为解决方法，您可以将端口暴露在所有接口上（使用 `0.0.0.0`）或使用 localhost（使用 `127.0.0.1`）。

## 4.22.1

{{< release-date date="2023-08-24" >}}

### Bug 修复和增强

#### 所有平台

- 缓解了影响 Docker Desktop 启动和资源节省模式的多个问题。[docker/for-mac#6933](https://github.com/docker/for-mac/issues/6933)

#### Windows 平台

- 修复了 Windows 上的 `Clean / Purge data` 故障排除选项。[docker/for-win#13630](https://github.com/docker/for-win/issues/13630)

## 4.22.0

{{< release-date date="2023-08-03" >}}

### 升级

- [Buildx v0.11.2](https://github.com/docker/buildx/releases/tag/v0.11.2)
- [Compose v2.20.2](https://github.com/docker/compose/releases/tag/v2.20.2)
- [Docker Engine v24.0.5](https://docs.docker.com/engine/release-notes/24.0/#2405)

> [!NOTE]
>
> 在此版本中，捆绑的 Docker Compose 和 Buildx 二进制文件显示不同的版本字符串。这与我们测试新功能而不引起向后兼容性问题的努力有关。
>
> 例如，`docker buildx version` 输出 `buildx v0.11.2-desktop.1`。

### 新增功能

- [资源使用情况](use-desktop/container.md) 已从实验性功能移至正式版本。
- 您现在可以使用 [`include`](/manuals/compose/how-tos/multiple-compose-files/include.md) 将大型 Compose 项目拆分为多个子项目。

### Bug 修复和增强

#### 所有平台

- [设置管理](/manuals/enterprise/security/hardened-desktop/settings-management/_index.md) 现在允许您为您的组织关闭 Docker 扩展。
- 修复了当系统暂停时通过 UI 启用 Kubernetes 失败的问题。
- 修复了当系统暂停时通过 UI 启用 Wasm 失败的问题。
- 当您[检查容器](use-desktop/container.md)时，现在会显示绑定挂载。
- 您现在可以在启用 containerd 镜像存储时下载 Wasm 运行时。
- 使用 [快速搜索](/manuals/desktop/use-desktop/_index.md#quick-search)，您现在可以：
  - 查找本地系统上的任何容器或 Compose 应用。此外，您可以访问环境变量并执行基本操作，如启动、停止或删除容器。
  - 查找公共 Docker Hub 镜像、本地镜像或远程仓库中的镜像。
  - 发现特定扩展的更多信息并安装它们。
  - 浏览您的卷并了解相关容器的信息。
  - 搜索并访问 Docker 的文档。

#### Mac 平台

- 修复了导致 Docker Desktop 无法启动的错误。[docker/for-mac#6890](https://github.com/docker/for-mac/issues/6890)
- 资源节省器现已在 Mac 上可用。当没有容器运行时，它会优化 Docker Desktop 对系统资源的使用。要使用此功能，请确保已在设置中[开启对实验性功能的访问权限](/manuals/desktop/settings-and-maintenance/settings.md)。

#### 适用于 Windows

- 修复了自诊断工具在 vpnkit 预期未运行时显示误报失败的问题。修复了 [docker/for-win#13479](https://github.com/docker/for-win/issues/13479)。
- 修复了搜索栏中的无效正则表达式导致错误的问题。修复了 [docker/for-win#13592](https://github.com/docker/for-win/issues/13592)。
- 资源节省器现已在 Windows Hyper-V 上可用。当没有容器运行时，它会优化 Docker Desktop 对系统资源的使用。要使用此功能，请确保已在设置中[开启对实验性功能的访问权限](/manuals/desktop/settings-and-maintenance/settings.md)。

## 4.21.1

{{< release-date date="2023-07-03" >}}

#### 适用于所有平台

- 修复了使用 SSH 的 Docker 上下文连接泄漏问题 ([docker/for-mac#6834](https://github.com/docker/for-mac/issues/6834) 和 [docker/for-win#13564](https://github.com/docker/for-win/issues/13564))

#### 适用于 Mac

- 移除了配置健康检查，以便进一步调查并解决特定设置问题。

## 4.21.0

{{< release-date date="2023-06-29" >}}

### 新增功能

- 新增对新的 Wasm 运行时的支持：slight、spin 和 wasmtime。当启用 containerd 镜像存储时，用户可以按需下载 Wasm 运行时。
- 为 Docker init 添加 Rust 服务器支持。
- [**构建**视图](use-desktop/builds.md) 的 Beta 版本，可让您检查构建并管理构建器。您可以在**设置**中的**开发中的功能**选项卡中找到此功能。

### 升级

- [Buildx v0.11.0](https://github.com/docker/buildx/releases/tag/v0.11.0)
- [Compose v2.19.0](https://github.com/docker/compose/releases/tag/v2.19.0)
- [Kubernetes v1.27.2](https://github.com/kubernetes/kubernetes/releases/tag/v1.27.2)
- [cri-tools v1.27.0](https://github.com/kubernetes-sigs/cri-tools/releases/tag/v1.27.0)
- [cri-dockerd v0.3.2](https://github.com/Mirantis/cri-dockerd/releases/tag/v0.3.2)
- [coredns v1.10.1](https://github.com/coredns/coredns/releases/tag/v1.10.1)
- [cni v1.2.0](https://github.com/containernetworking/plugins/releases/tag/v1.2.0)
- [etcd v3.5.7](https://github.com/etcd-io/etcd/releases/tag/v3.5.7)

### 错误修复与增强

#### 适用于所有平台

- Docker Desktop 现在会在未使用时自动暂停 Docker 引擎，并在需要时再次唤醒。
- 对于 macOS 12.5 及更高版本的新 Docker Desktop 安装，VirtioFS 现在是默认的文件共享实现。
- 使用 OpenTelemetry 改进产品使用情况报告（实验性）。
- 修复了 Docker 套接字权限问题。修复了 [docker/for-win#13447](https://github.com/docker/for-win/issues/13447) 和 [docker/for-mac#6823](https://github.com/docker/for-mac/issues/6823)。
- 修复了暂停状态下退出应用程序时导致 Docker Desktop 挂起的问题。
- 修复了**容器**视图中的**日志**和**终端**选项卡内容被固定工具栏覆盖的问题 [docker/for-mac#6814](https://github.com/docker/for-mac/issues/6814)。
- 修复了容器运行对话框中输入标签与输入值重叠的问题。修复了 [docker/for-win#13304](https://github.com/docker/for-win/issues/13304)。
- 修复了用户无法选择 Docker 扩展菜单的问题。修复了 [docker/for-mac#6840](https://github.com/docker/for-mac/issues/6840) 和 [docker/for-mac#6855](https://github.com/docker/for-mac/issues/6855)

#### 适用于 Mac

- 为 macOS 添加了健康检查，通知用户其系统是否发生了可能导致 Docker 二进制文件运行问题的更改。

#### 适用于 Windows

- 修复了 WSL 2 上的错误：如果 Desktop 暂停、被终止然后重新启动，除非先用 `wsl --shutdown` 关闭 WSL，否则启动会挂起。
- 修复了 wsl.exe 不在 PATH 中时的 WSL 引擎问题 [docker/for-win#13547](https://github.com/docker/for-win/issues/13547)。
- 修复了 WSL 引擎检测 Docker Desktop 发行版的驱动器缺失情况的能力 [docker/for-win#13554](https://github.com/docker/for-win/issues/13554)。
- 缓慢或无响应的 WSL 集成不再阻止 Docker Desktop 启动。修复了 [docker/for-win#13549](https://github.com/docker/for-win/issues/13549)。
- 修复了导致 Docker Desktop 启动时崩溃的错误 [docker/for-win#6890](https://github.com/docker/for-mac/issues/6890)。
- 添加了以下安装程序标志：
  - `--hyper-v-default-data-root`：指定 Hyper-V 虚拟机磁盘的默认位置。
  - `--windows-containers-default-data-root`：指定 Windows 容器的默认数据根目录。
  - `--wsl-default-data-root`：指定 WSL 发行版磁盘的默认位置。

## 4.20.1

{{< release-date date="2023-06-05" >}}

### 错误修复与增强

#### 适用于所有平台

- containerd 镜像存储：修复了加载包含证明的镜像时 `docker load` 失败的问题。
- containerd 镜像存储：修复了构建期间的默认镜像导出器。

#### 适用于 Windows

- 修复了在非西方语言环境中难以解析主机上 WSL 版本的问题。修复了 [docker/for-win#13518](https://github.com/docker/for-win/issues/13518) 和 [docker/for-win#13524](https://github.com/docker/for-win/issues/13524)。

## 4.20.0

{{< release-date date="2023-05-30" >}}

### 升级

- [Buildx v0.10.5](https://github.com/docker/buildx/releases/tag/v0.10.5)
- [Compose v2.18.1](https://github.com/docker/compose/releases/tag/v2.18.1)
- [Docker Engine v24.0.2](https://docs.docker.com/engine/release-notes/24.0/#2402)
- [Containerd v1.6.21](https://github.com/containerd/containerd/releases/tag/v1.6.21)
- [runc v1.1.7](https://github.com/opencontainers/runc/releases/tag/v1.1.5)

### 错误修复与增强

#### 适用于所有平台

- [Docker Scout CLI](https://docs.docker.com/scout/#docker-scout-cli) 现在会查找最近构建的镜像（如果未提供为参数）。
- 改进了 [Docker Scout CLI](https://docs.docker.com/scout/#docker-scout-cli) 的 `compare` 命令。
- 添加了关于 [Docker Compose ECS/ACS 集成将于 2023 年 11 月停用](https://docs.docker.com/go/compose-ecs-eol/) 的警告。可通过 `COMPOSE_CLOUD_EOL_SILENT=1` 抑制。
- 修复了 HTTP 代理错误：HTTP 1.0 客户端可能收到 HTTP 1.1 响应的问题。
- 在 WSL-2 上启用了 Docker Desktop 的增强容器隔离 (ECI) 功能。此功能需要 Docker Business 订阅。
- 修复了**容器**表格中，Docker Desktop 全新安装后先前隐藏的列再次显示的问题。

#### 适用于 Mac

- 现在，在容器中删除文件时可以更快地回收磁盘空间。相关 issue：[docker/for-mac#371](https://github.com/docker/for-mac/issues/371)。
- 修复了容器无法访问 169.254.0.0/16 IP 的问题。修复了 [docker/for-mac#6825](https://github.com/docker/for-mac/issues/6825)。
- 修复了 `com.docker.diagnose check` 中的错误：即使 vpnkit 预期未运行，也会抱怨缺少 vpnkit。相关 issue：[docker/for-mac#6825](https://github.com/docker/for-mac/issues/6825)。

#### 适用于 Windows

- 修复了 WSL 数据无法移动到不同磁盘的问题。修复了 [docker/for-win#13269](https://github.com/docker/for-win/issues/13269)。
- 修复了 Docker Desktop 关闭时未停止其 WSL 发行版（docker-desktop 和 docker-desktop-data）的问题，从而避免不必要地消耗主机内存。
- 新增设置，允许 Windows Docker 守护进程在运行 Windows 容器时使用 Docker Desktop 的内部代理。请参阅 [Windows 代理设置](/manuals/desktop/settings-and-maintenance/settings.md#proxies)。

#### 适用于 Linux

- 修复了 Docker Compose V1/V2 兼容性设置的问题。

## 4.19.0

{{< release-date date="2023-04-27" >}}

### 新增功能

- Docker Engine 和 CLI 已更新至 [Moby 23.0](https://github.com/moby/moby/releases/tag/v23.0.0)。
- **Learning Center** 现已支持产品内引导式教程。
- Docker init（Beta 版）现已支持 Node.js 和 Python。
- 提升了 macOS 上虚拟机与主机之间的网络性能。
- 您现在可以直接检查和分析远程镜像，无需将其拉取到本地。
- 对 **Artifactory 镜像** 视图进行了可用性和性能优化。

### 移除功能

- 移除了 `docker scan` 命令。如需继续了解镜像漏洞及其他众多功能，请使用新的 `docker scout` 命令。运行 `docker scout --help` 或[阅读文档了解更多信息](/reference/cli/docker/scout/)。

### 升级组件

- [Docker Engine v23.0.5](https://docs.docker.com/engine/release-notes/23.0/#2305)
- [Compose 2.17.3](https://github.com/docker/compose/releases/tag/v2.17.3)
- [Containerd v1.6.20](https://github.com/containerd/containerd/releases/tag/v1.6.20)
- [Kubernetes v1.25.9](https://github.com/kubernetes/kubernetes/releases/tag/v1.25.9)
- [runc v1.1.5](https://github.com/opencontainers/runc/releases/tag/v1.1.5)
- [Go v1.20.3](https://github.com/golang/go/releases/tag/go1.20.3)

### Bug 修复与增强

#### 全平台通用

- 改进了 `docker scout compare` 命令，用于比较两个镜像，现也可通过别名 `docker scout diff` 调用。
- 当 `docker-compose` 操作失败时，仪表板错误信息中增加了更多详细信息（[docker/for-win#13378](https://github.com/docker/for-win/issues/13378)）。
- 安装期间支持设置 HTTP 代理配置。可通过 CLI 安装时的 `--proxy-http-mode`、`--override-proxy-http`、`--override-proxy-https` 和 `--override-proxy-exclude` 安装标志实现（适用于 [Mac](/manuals/desktop/setup/install/mac-install.md#install-from-the-command-line) 和 [Windows](/manuals/desktop/setup/install/windows-install.md#install-from-the-command-line)），或者在 `install-settings.json` 文件中设置相应值。
- Docker Desktop 现在不再在应用启动时覆盖 `.docker/config.json` 中的 `credsStore` 键。请注意，如果您使用自定义凭据助手，则 CLI 的 `docker login` 和 `docker logout` 不会影响 UI 是否已登录 Docker。通常建议通过 UI 登录 Docker，因为 UI 支持多因素身份验证。
- 添加了关于即将从 Docker Desktop 中移除 Compose V1 的警告。可通过设置环境变量 `COMPOSE_V1_EOL_SILENT=1` 来抑制该警告。
- 在 Compose 配置中，YAML 中的布尔字段应为 `true` 或 `false`。已弃用的 YAML 1.1 值（如 “on” 或 “no”）现在会触发警告。
- 改进了镜像表格的 UI，使行能够利用更多可用空间。
- 修复了端口转发中的多个 Bug。
- 修复了 HTTP 代理 Bug：当 HTTP 请求未包含服务器名称指示（SNI）记录时，不再返回错误并拒绝请求。

#### Windows 平台

- 恢复了在 Windows 上完整修补 `etc/hosts` 的行为（重新包含 `host.docker.internal` 和 `gateway.docker.internal`）。对于 WSL，此行为由 **General** 选项卡中的新设置控制。修复了 [docker/for-win#13388](https://github.com/docker/for-win/issues/13388) 和 [docker/for-win#13398](https://github.com/docker/for-win/issues/13398)。
- 修复了更新 Docker Desktop 时在桌面上出现虚假 `courgette.log` 文件的问题。修复了 [docker/for-win#12468](https://github.com/docker/for-win/issues/12468)。
- 修复了“放大”快捷键（Ctrl+=）。修复了 [docker/for-win#13392](https://github.com/docker/for-win/issues/13392)。
- 修复了托盘菜单在第二次切换容器类型后无法正确更新的 Bug。修复了 [docker/for-win#13379](https://github.com/docker/for-win/issues/13379)。

#### Mac 平台

- 提升了 macOS Ventura 及以上版本在使用虚拟化框架时的虚拟机网络性能。Docker Desktop for Mac 现在使用 gVisor 替代 VPNKit。如需继续使用 VPNKit，请在位于 `~/Library/Group Containers/group.com.docker/settings.json` 的 `settings.json` 文件中添加 `"networkType":"vpnkit"`。
- 修复了卸载时显示错误窗口的 Bug。
- 修复了 `deprecatedCgroupv1` 设置被忽略的问题。修复了 [docker/for-mac#6801](https://github.com/docker/for-mac/issues/6801)。
- 修复了 `docker pull` 返回 `EOF` 的情况。

#### Linux 平台

- 修复了虚拟机网络在运行 24 小时后崩溃的问题。修复了 [docker/desktop-linux#131](https://github.com/docker/desktop-linux/issues/131)。

### 安全性

#### 全平台通用

- 修复了允许用户绕过组织配置的镜像访问管理（IAM）限制的安全问题：通过删除 Docker CLI 配置文件中的 `credsStore` 键，可规避 `registry.json` 强制登录。仅影响 Docker Business 客户。
- 修复了 [CVE-2023-24532](https://github.com/advisories/GHSA-x2w5-7wp4-5qff)。
- 修复了 [CVE-2023-25809](https://github.com/advisories/GHSA-m8cg-xc2p-r3fc)。
- 修复了 [CVE-2023-27561](https://github.com/advisories/GHSA-vpvm-3wq2-2wvm)。
- 修复了 [CVE-2023-28642](https://github.com/advisories/GHSA-g2j6-57v7-gm8c)。
- 修复了 [CVE-2023-28840](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-28840)。
- 修复了 [CVE-2023-28841](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-28841)。
- 修复了 [CVE-2023-28842](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-28842)。

## 4.18.0

{{< release-date date="2023-04-03" >}}

### 新增功能

- 根据[路线图](https://github.com/docker/roadmap/issues/453)，首次发布 `docker init` 的 Beta 版本。
- 新增 **Learning Center** 选项卡，帮助用户快速上手 Docker。
- 为 Docker Compose 添加了实验性的文件监听命令，可在您编辑并保存代码时自动更新正在运行的 Compose 服务。

### 升级组件

- [Buildx v0.10.4](https://github.com/docker/buildx/releases/tag/v0.10.4)
- [Compose 2.17.2](https://github.com/docker/compose/releases/tag/v2.17.2)
- [Containerd v1.6.18](https://github.com/containerd/containerd/releases/tag/v1.6.18)，包含对 [CVE-2023-25153](https://github.com/advisories/GHSA-259w-8hf6-59c2) 和 [CVE-2023-25173](https://github.com/advisories/GHSA-hmfx-3pcx-653p) 的修复。
- [Docker Engine v20.10.24](https://docs.docker.com/engine/release-notes/20.10/#201024)，包含对 [CVE-2023-28841](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-28841)、[CVE-2023-28840](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-28840) 和 [CVE-2023-28842](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-28842) 的修复。

### Bug 修复与增强

#### 全平台通用

- [Docker Scout CLI](../scout/_index.md#docker-scout-cli) 现在可以比较两个镜像并显示软件包和漏洞差异。该命令处于[早期访问阶段](../release-lifecycle.md)，未来可能会发生变化。
- [Docker Scout CLI](../scout/_index.md#docker-scout-cli) 现在可通过 `docker scout recommendations` 显示基础镜像更新和修复建议，并通过 `docker scout quickview` 命令提供镜像的简要概览。
- 您现在可以直接从 Marketplace 搜索扩展，也可使用 **Global Search**。
- 修复了 `docker buildx` 容器构建器在 24 小时后失去网络访问权限的问题。
- 减少了 Docker Desktop 提示用户反馈的频率。
- 移除了虚拟机交换空间的最小限制。
- 支持在 HTTP 代理排除列表中使用子域名匹配、CIDR 匹配、`.` 和 `_`。
- 修复了透明 TLS 代理中未设置服务器名称指示（SNI）字段时的 Bug。
- 修复了 Docker Desktop 引擎状态消息中的语法错误。

### Windows 平台

（原文未提供 Windows 平台的具体修复内容，此处保留空节以保持结构一致）

- 修复了 `docker run --gpus=all` 命令挂起的问题。修复了 [docker/for-win#13324](https://github.com/docker/for-win/issues/13324)。
- 修复了注册表访问管理策略更新未下载的问题。
- 当 `C:` 盘启用 BitLocker 时，Docker Desktop 现在允许 Windows 容器正常工作。
- 使用 WSL 后端的 Docker Desktop 不再需要 `com.docker.service` 特权服务永久运行。更多信息请参阅 [Windows 权限要求](/manuals/desktop/setup/install/windows-permission-requirements.md)。

### 适用于 Mac

- 修复了性能问题：VirtioFS 用户存储在主机上的属性未被缓存。
- 首次启动 Docker Desktop for Mac 时，系统会弹出一个安装窗口，供用户确认或调整需要特权访问的配置。更多信息请参阅 [Mac 权限要求](https://docs.docker.com/desktop/mac/permission-requirements/)。
- 在 **设置** 中新增了 **高级** 选项卡，用户可在此调整需要特权访问的设置。

### 适用于 Linux

- 修复了虚拟机网络在 24 小时后崩溃的问题。[docker/for-linux#131](https://github.com/docker/desktop-linux/issues/131)

### 安全性

#### 适用于所有平台

- 修复了 [CVE-2023-1802](https://www.cve.org/cverecord?id=CVE-2023-1802)：Artifactory 集成中的安全问题可能导致 HTTPS 检查失败时回退到通过明文 HTTP 发送注册表凭据。仅启用了 `访问实验性功能` 的用户会受到影响。修复了 [docker/for-win#13344](https://github.com/docker/for-win/issues/13344)。

#### 适用于 Mac

- 移除了 `com.apple.security.cs.allow-dyld-environment-variables` 和 `com.apple.security.cs.disable-library-validation` 权限，这些权限允许通过 `DYLD_INSERT_LIBRARIES` 环境变量为 Docker Desktop 加载任意动态库。

### 已知问题

- 在 Mac 上通过 **故障排除** 页面卸载 Docker Desktop 时，可能会触发意外的致命错误弹窗。

## 4.17.1

{{< release-date date="2023-03-20" >}}

### Bug 修复与增强

#### 适用于 Windows

- 当 C: 盘启用 BitLocker 时，Docker Desktop 现在允许 Windows 容器正常工作。
- 修复了 `docker buildx` 容器构建器在 24 小时后会失去网络访问权限的问题。
- 修复了注册表访问管理策略更新未下载的问题。
- 改进了调试信息，以便更好地描述 WSL 2 下的故障。

### 已知问题

- 在 Windows 上使用 WSL 2 后端运行带有 `--gpus` 的容器无法正常工作。此问题将在未来版本中修复。请参阅 [docker/for-win/13324](https://github.com/docker/for-win/issues/13324)。

## 4.17.0

{{< release-date date="2023-02-27" >}}

### 新增功能

- Docker Desktop 现在随附 Docker Scout。可从 Docker Hub 和 Artifactory 仓库拉取并查看镜像分析结果，获取基础镜像更新及推荐的标签和摘要，并根据漏洞信息过滤镜像。更多信息请参阅 [Docker Scout](../scout/_index.md)。
- `docker scan` 已被 `docker scout` 取代。更多信息请参阅 [Docker Scout CLI](../scout/_index.md#docker-scout-cli)。
- 您现在可以在扩展市场中发现自主发布的扩展。关于自发布扩展的更多信息，请参阅 [市场扩展](/manuals/extensions/marketplace.md)。
- **容器文件浏览器** 作为实验性功能提供。可直接通过 GUI 调试容器内的文件系统。
- 您现在可以在 **全局搜索** 中搜索卷。

### 升级

- [Containerd v1.6.18](https://github.com/containerd/containerd/releases/tag/v1.6.18)，包含对 [CVE-2023-25153](https://github.com/advisories/GHSA-259w-8hf6-59c2) 和 [CVE-2023-25173](https://github.com/advisories/GHSA-hmfx-3pcx-653p) 的修复。
- [Docker Engine v20.10.23](https://docs.docker.com/engine/release-notes/20.10/#201023)。
- [Go 1.19.5](https://github.com/golang/go/releases/tag/go1.19.5)

### Bug 修复与增强

#### 适用于所有平台

- 修复了诊断信息收集可能因等待子进程退出而挂起的问题。
- 防止透明 HTTP 代理过度篡改请求。修复了 Tailscale 扩展登录问题，请参阅 [tailscale/docker-extension#49](https://github.com/tailscale/docker-extension/issues/49)。
- 修复了透明 TLS 代理中未设置服务器名称指示（Server Name Indication）字段的问题。
- 在 HTTP 代理排除列表中增加了对子域名匹配、CIDR 匹配、`.` 和 `*.` 的支持。
- 确保上传诊断信息时遵守 HTTP 代理设置。
- 修复了从凭据助手获取凭据时出现致命错误的问题。
- 修复了与并发日志记录相关的致命错误。
- 改进了扩展市场中扩展操作的 UI。
- 在扩展市场中新增了过滤器。您现在可以按类别和审核状态过滤扩展。
- 增加了向 Docker 报告恶意扩展的方式。
- 将开发环境更新至 v0.2.2，包含初始设置可靠性与安全性修复。
- 仅为新用户添加了欢迎调查。
- 故障排除页面上的确认对话框现在与其他类似对话框保持一致的样式。
- 修复了在 Kubernetes 集群启动前重置它导致的致命错误。
- 为 containerd 集成实现了 `docker import`。
- 修复了 containerd 集成中使用现有标签进行镜像标记的问题。
- 为 containerd 集成实现了镜像的悬空（dangling）过滤器。
- 修复了 containerd 集成中因镜像不再存在而导致 `docker ps` 失败的问题。

#### 适用于 Mac

- 修复了未安装特权助手工具 `com.docker.vmnetd` 的系统上无法下载注册表访问管理策略的问题。
- 修复了 `/Library/PrivilegedHelperTools` 不存在时无法安装 `com.docker.vmnetd` 的问题。
- 修复了“系统”代理无法处理“自动代理”/“PAC 文件”配置的问题。
- 修复了 vmnetd 安装在区分大小写的文件系统上无法读取 `Info.Plist` 的问题。实际文件名为 `Info.plist`。修复了 [docker/for-mac#6677](https://github.com/docker/for-mac/issues/6677)。
- 修复了用户每次启动时都被提示创建 docker 套接字符号链接的问题。修复了 [docker/for-mac#6634](https://github.com/docker/for-mac/issues/6634)。
- 修复了 **登录时启动 Docker Desktop** 设置不生效的问题。修复了 [docker/for-mac#6723](https://github.com/docker/for-mac/issues/6723)。
- 修复了 UDP 连接跟踪和 `host.docker.internal` 的问题。修复了 [docker/for-mac#6699](https://github.com/docker/for-mac/issues/6699)。
- 改进了 kubectl 符号链接逻辑，以尊重 `/usr/local/bin` 中已有的二进制文件。修复了 [docker/for-mac#6328](https://github.com/docker/for-mac/issues/6328)。
- 当您选择使用 Rosetta 但尚未安装时，Docker Desktop 现在会自动安装它。

### 适用于 Windows

- 针对 WSL 集成工具添加了与 `musl` 的静态链接，因此用户发行版无需再安装 `alpine-pkg-glibc`。
- 添加了在 WSL 2 下对 cgroupv2 的支持。您可以通过在 `%USERPROFILE%\.wslconfig` 文件的 `[wsl2]` 部分添加 `kernelCommandLine = systemd.unified_cgroup_hierarchy=1 cgroup_no_v1=all` 来启用此功能。
- 修复了 Docker Desktop 在 WSL 2 模式下卡在“正在启动”阶段的问题（该问题在 4.16 版本中引入）。
- 修复了当 `%LOCALAPPDATA%` 启用文件系统压缩或加密时，Docker Desktop 无法启动 WSL 2 后端的问题。
- 修复了 Docker Desktop 启动时无法报告缺失或过时（无法运行 WSL 版本 2 发行版）的 WSL 安装的问题。
- 修复了当目标路径包含空格时，在 Visual Studio Code 中打开失败的问题。
- 修复了导致 `~/.docker/context` 损坏并出现“JSON 输入意外结束”错误消息的 bug。您也可以删除 `~/.docker/context` 来规避此问题。
- 确保在 WSL 2 中使用的凭据助手已正确签名。相关问题：[docker/for-win#10247](https://github.com/docker/for-win/issues/10247)。
- 修复了导致 WSL 集成代理被错误终止的问题。相关问题：[docker/for-win#13202](https://github.com/docker/for-win/issues/13202)。
- 修复了启动时上下文损坏的问题。解决了 [docker/for-win#13180](https://github.com/docker/for-win/issues/13180) 和 [docker/for-win#12561](https://github.com/docker/for-win/issues/12561)。

### 针对 Linux

- 为 Linux 版 Docker Desktop 添加了 Docker Buildx 插件。
- 将 RPM 和 Arch Linux 发行版的压缩算法更改为 `xz`。
- 修复了导致 Debian 软件包在根目录留下残留文件的问题。解决了 [docker/for-linux#123](https://github.com/docker/desktop-linux/issues/123)。

### 安全性

#### 适用于所有平台

- 修复了 [CVE-2023-0628](https://www.cve.org/cverecord?id=CVE-2023-0628)，该漏洞允许攻击者通过在初始化期间诱骗用户打开特制的恶意 `docker-desktop://` URL，在 Dev Environments 容器内执行任意命令。
- 修复了 [CVE-2023-0629](https://www.cve.org/cverecord?id=CVE-2023-0629)，该漏洞允许非特权用户通过 `-H` (`--host`) CLI 标志或 `DOCKER_HOST` 环境变量将 Docker 主机设置为 `docker.raw.sock`（在 Windows 上为 `npipe:////.pipe/docker_engine_linux`），从而绕过增强型容器隔离 (ECI) 限制，并启动不包含 ECI 提供的额外加固功能的容器。这不会影响已经运行的容器，也不会影响通过常规方法（不使用 Docker 的原始套接字）启动的容器。

## 4.16.3

{{< release-date date="2023-01-30" >}}

### Bug 修复与增强

#### 针对 Windows

- 修复了当 `%LOCALAPPDATA%` 启用文件系统压缩或加密时，Docker Desktop 无法启动 WSL 2 后端的问题。解决了 [docker/for-win#13184](https://github.com/docker/for-win/issues/13184)。
- 修复了 Docker Desktop 启动时无法报告缺失或过时 WSL 安装的问题。解决了 [docker/for-win#13184](https://github.com/docker/for-win/issues/13184)。

## 4.16.2

{{< release-date date="2023-01-19" >}}

### Bug 修复与增强

#### 适用于所有平台

- 修复了当启用 containerd 集成功能时，`docker build` 和 `docker tag` 命令产生“镜像已存在”错误的问题。
- 修复了 Docker Desktop 4.16 引入的回归问题，该问题导致在 amd64 系统上针对 linux/386 目标平台的容器网络连接中断。解决了 [docker/for-mac/6689](https://github.com/docker/for-mac/issues/6689)。

#### 针对 Mac

- 修复了 `Info.plist` 的大小写问题，该问题导致 `vmnetd` 在区分大小写的文件系统上崩溃。解决了 [docker/for-mac/6677](https://github.com/docker/for-mac/issues/6677)。

#### 针对 Windows

- 修复了 Docker Desktop 4.16 引入的回归问题，该问题导致其在 WSL2 模式下卡在“正在启动”阶段。解决了 [docker/for-win/13165](https://github.com/docker/for-win/issues/13165)

## 4.16.1

{{< release-date date="2023-01-13" >}}

### Bug 修复与增强

#### 适用于所有平台

- 修复了某些镜像中容器内 `sudo` 因安全相关错误而失败的问题。解决了 [docker/for-mac/6675](https://github.com/docker/for-mac/issues/6675) 和 [docker/for-win/13161](https://github.com/docker/for-win/issues/13161)。

## 4.16.0

{{< release-date date="2023-01-12" >}}

### 新增功能

- 扩展已从 Beta 版移至 GA（正式发布）版。
- 快速搜索已从实验性功能移至 GA（正式发布）版。
- 扩展现已包含在快速搜索中。
- 分析大型镜像的速度现在最高可达 4 倍。
- 新的本地镜像视图已从实验性功能移至 GA（正式发布）版。
- 为 macOS 13 添加了新的 Beta 功能：Rosetta for Linux，可在 Apple Silicon 上更快地模拟基于 Intel 的镜像。

### 升级

- [Compose v2.15.1](https://github.com/docker/compose/releases/tag/v2.15.1)
- [Containerd v1.6.14](https://github.com/containerd/containerd/releases/tag/v1.6.14)
- [Docker Engine v20.10.22](https://docs.docker.com/engine/release-notes/20.10/#201022)
- [Buildx v0.10.0](https://github.com/docker/buildx/releases/tag/v0.10.0)
- [Docker Scan v0.23.0](https://github.com/docker/scan-cli-plugin/releases/tag/v0.23.0)
- [Go 1.19.4](https://github.com/golang/go/releases/tag/go1.19.4)

### Bug 修复与增强

#### 适用于所有平台

- 修复了使用 `containerd` 集成时，`docker build --quiet` 不输出镜像标识符的问题。
- 修复了使用 `containerd` 集成时，镜像检查不显示镜像标签的问题。
- 增加了正在运行和已停止容器图标之间的对比度，以便色盲人士更容易扫描容器列表。
- 修复了用户被反复提示输入新的 HTTP 代理凭据，直到 Docker Desktop 重启的问题。
- 添加了诊断命令 `com.docker.diagnose login` 以检查 HTTP 代理配置。
- 修复了 Compose 堆栈上的操作无法正常工作的问题。解决了 [docker/for-mac#6566](https://github.com/docker/for-mac/issues/6566)。
- 修复了 Docker Desktop 仪表板在启动时尝试获取磁盘使用情况信息并在引擎运行之前显示错误横幅的问题。
- 在所有实验性功能旁边添加了信息性横幅，其中包含有关如何退出实验性功能访问的说明。
- Docker Desktop 现在支持通过 HTTP 代理下载 Kubernetes 镜像。
- 修复了工具提示遮挡操作按钮的问题。解决了 [docker/for-mac#6516](https://github.com/docker/for-mac/issues/6516)。
- 修复了 **容器** 视图中空白“发生错误”容器列表的问题。

#### 针对 Mac

- 在 macOS 上安装或更新 Docker Desktop 的最低操作系统版本现在为 macOS Big Sur（版本 11）或更高版本。
- 修复了当启用增强型容器隔离且使用传统的 `osxfs` 实现进行文件共享时，Docker 引擎无法启动的问题。
- 修复了 VirtioFS 上创建的文件设置了可执行位的问题。解决了 [docker/for-mac#6614](https://github.com/docker/for-mac/issues/6614)。
- 重新添加了从命令行卸载 Docker Desktop 的方法。解决了 [docker/for-mac#6598](https://github.com/docker/for-mac/issues/6598)。
- 修复了硬编码的 `/usr/bin/kill`。解决了 [docker/for-mac#6589](https://github.com/docker/for-mac/issues/6589)。
- 修复了 VirtioFS 上共享的非常大的文件（> 38GB）截断（例如使用 `truncate` 命令）时大小不正确的问题。
- 将 **设置** 中的磁盘映像大小更改为使用十进制系统（以 10 为基数），以与 Finder 显示磁盘容量的方式保持一致。
- 修复了网络负载下 Docker 崩溃的问题。解决了 [docker/for-mac#6530](https://github.com/docker/for-mac/issues/6530)。
- 修复了导致 Docker 在每次重启后提示用户安装 `/var/run/docker.sock` 符号链接的问题。
- 确保安装 `/var/run/docker.sock` 符号链接的登录项已签名。
- 修复了工厂重置时 `$HOME/.docker` 被删除的问题。

### 针对 Windows

- 修复了 `docker build` 在打印 "load metadata for" 时挂起的问题。修复了 [docker/for-win#10247](https://github.com/docker/for-win/issues/10247)。
- 修复了 diagnose.exe 输出中的拼写错误。修复了 [docker/for-win#13107](https://github.com/docker/for-win/issues/13107)。
- 添加了对在 WSL 2 下使用 cgroupv2 运行的支持。可通过在 `%USERPROFILE%\.wslconfig` 文件的 `[wsl2]` 部分添加 `kernelCommandLine = systemd.unified_cgroup_hierarchy=1 cgroup_no_v1=all` 来启用此功能。

### 已知问题

- 在某些镜像中，容器内调用 `sudo` 会因安全相关错误而失败。请参阅 [docker/for-mac/6675](https://github.com/docker/for-mac/issues/6675) 和 [docker/for-win/13161](https://github.com/docker/for-win/issues/13161)。

## 4.15.0

{{< release-date date="2022-12-01" >}}

### 新增功能

- 为 macOS 用户带来显著的性能改进，可选择启用新的 VirtioFS 文件共享技术。适用于 macOS 12.5 及以上版本。
- Docker Desktop for Mac 在安装或首次运行时不再需要安装特权辅助进程 `com.docker.vmnetd`。更多信息请参阅 [Mac 权限要求](https://docs.docker.com/desktop/mac/permission-requirements/)。
- 添加了 [WebAssembly 功能](/manuals/desktop/features/wasm.md)。可与 [containerd 集成](/manuals/desktop/features/containerd.md) 配合使用。
- 改进了测试版和实验性设置的描述，以清晰解释其差异以及如何访问它们。
- 现在，Docker Desktop Dashboard（适用于 Mac 和 Linux）的页脚会显示虚拟机的可用磁盘空间。
- 如果可用空间低于 3GB，页脚现在会显示磁盘空间警告。
- 随着我们更加注重 ADA 无障碍访问和视觉统一性，对 Docker Desktop 界面进行了更改。
- 在 **Extensions** 中添加了 **Build** 选项卡，其中包含构建扩展所需的所有资源。
- 添加了更轻松地共享扩展的功能，可通过 `docker extension share` CLI 或在扩展的 **Manage** 选项卡中使用共享按钮实现。
- 现在，Marketplace 中的扩展会显示安装次数。您还可以按安装次数对扩展进行排序。
- Dev Environments 允许将 Git 仓库克隆到本地绑定挂载，以便您可以使用任何本地编辑器或 IDE。
- 更多 Dev Environments 改进：自定义名称、更好的私有仓库支持、改进的端口处理。

### 升级

- [Compose v2.13.0](https://github.com/docker/compose/releases/tag/v2.13.0)
- [Containerd v1.6.10](https://github.com/containerd/containerd/releases/tag/v1.6.10)
- [Docker Hub Tool v0.4.5](https://github.com/docker/hub-tool/releases/tag/v0.4.5)
- [Docker Scan v0.22.0](https://github.com/docker/scan-cli-plugin/releases/tag/v0.22.0)

### Bug 修复与增强

#### 适用于所有平台

- 现在，在重启时，使用 containerd 集成的容器会被恢复。
- 修复了使用 containerd 集成时列出多平台镜像的问题。
- 更好地处理使用 containerd 集成时的悬空镜像。
- 为使用 containerd 集成的镜像实现了 "reference" 过滤器。
- 添加了对通过容器中的 `proxy.pac` 自动选择上游 HTTP/HTTPS 代理的支持，适用于 `docker pull` 等操作。
- 修复了拉取时解析镜像引用的回归问题。修复了 [docker/for-win#13053](https://github.com/docker/for-win/issues/13053)、[docker/for-mac#6560](https://github.com/docker/for-mac/issues/6560) 和 [docker/for-mac#6540](https://github.com/docker/for-mac/issues/6540)。

#### 适用于 Mac

- 改进了 `docker pull` 的性能。

#### 适用于 Windows

- 修复了 Docker 启动且开发者登录时未使用系统 HTTP 代理的问题。
- 当 Docker Desktop 使用 "system" 代理且 Windows 设置发生更改时，Docker Desktop 现在无需重启即可使用新的 Windows 设置。

#### 适用于 Linux

- 修复了 Linux 上的热重载问题。修复了 [docker/desktop-linux#30](https://github.com/docker/desktop-linux/issues/30)。
- 禁用了 Linux 上的托盘图标动画，修复了部分用户的崩溃问题。

## 4.14.1

{{< release-date date="2022-11-17" >}}

### Bug 修复与增强

#### 适用于所有平台

- 修复了使用 Registry Access Management 时容器 DNS 查找的问题。

#### 适用于 Mac

- 修复了 **Images** 选项卡上的 **Analyze Image** 按钮无法工作的问题。
- 修复了如果 `/usr/local/lib` 不存在，则不会为用户创建符号链接的错误。修复了 [docker/for-mac#6569](https://github.com/docker/for-mac/issues/6569)

## 4.14.0

{{< release-date date="2022-11-10" >}}

### 新增功能

- 将 Virtualization framework 设置为 macOS >= 12.5 的默认虚拟机管理程序。
- 将之前的安装迁移到 macOS >= 12.5 的 Virtualization framework 虚拟机管理程序。
- 增强型容器隔离功能（Docker Business 用户可用）现在可以从“通用设置”中启用。

### 更新

- [Docker Engine v20.10.21](/manuals/engine/release-notes/20.10.md#201021)，其中包含针对 Git 漏洞的缓解措施（跟踪为 [CVE-2022-39253](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-39253)），并更新了 `image:tag@digest` 镜像引用的处理方式。
- [Docker Compose v2.12.2](https://github.com/docker/compose/releases/tag/v2.12.2)
- [Containerd v1.6.9](https://github.com/containerd/containerd/releases/tag/v1.6.9)
- [Go 1.19.3](https://github.com/golang/go/releases/tag/go1.19.3)

### Bug 修复与增强

#### 适用于所有平台

- Docker Desktop 现在需要一个大小为 /24 的内部网络子网。如果您之前使用的是 /28，它会自动扩展到 /24。如果您遇到网络问题，请检查 Docker 子网与您的基础设施之间是否存在冲突。修复了 [docker/for-win#13025](https://github.com/docker/for-win/issues/13025)。
- 修复了当 Git URL 包含大写字符时，用户无法创建 Dev Environments 的问题。
- 修复了诊断中报告的 `vpnkit.exe is not running` 错误。
- 将 qemu 回退到 6.2.0，以修复运行模拟 amd64 代码时出现的 `PR_SET_CHILD_SUBREAPER is unavailable` 等错误。
- 在 Extensions 中启用了 [contextIsolation](https://www.electronjs.org/docs/latest/tutorial/context-isolation) 和 [sandbox](https://www.electronjs.org/docs/latest/tutorial/sandbox) 模式。现在 Extensions 在单独的上下文中运行，这通过限制对大多数系统资源的访问来限制恶意代码可能造成的危害。
- 包含了 `unpigz` 以允许并行解压拉取的镜像。
- 修复了与对选定容器执行操作相关的问题。[修复了 https://github.com/docker/for-win/issues/13005](https://github.com/docker/for-win/issues/13005)
- 添加了允许您为容器或项目视图显示时间戳的功能。
- 修复了使用 Control+C 中断 `docker pull` 时可能出现的段错误。
- 增加了默认 DHCP 租约时间，以避免 VM 网络出现故障并每两小时断开连接。
- 移除了容器列表上的无限旋转图标。[修复了 https://github.com/docker/for-mac/issues/6486](https://github.com/docker/for-mac/issues/6486)
- 修复了 **Settings** 中显示已用空间值不正确的问题。
- 修复了使用 containerd 集成时 Kubernetes 无法启动的错误。
- 修复了使用 containerd 集成时 `kind` 无法启动的错误。
- 修复了使用 containerd 集成时 Dev Environments 无法工作的错误。
- 在 containerd 集成中实现了 `docker diff`。
- 在 containerd 集成中实现了 `docker run —-platform`。
- 修复了使用 containerd 集成时不安全注册表无法工作的错误。

#### 适用于 Mac

- 修复了 Virtualization framework 用户的启动失败问题。
- 默认情况下，重新在 Mac 上添加了 `/var/run/docker.sock`，以提高与 `tilt` 和 `docker-py` 等工具的兼容性。
- 修复了阻止在新 Mac 安装上创建 Dev Environments 的问题（错误 "Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?"）。

#### 适用于 Windows

- 重新添加了 `DockerCli.exe -SharedDrives`。修复了 [docker/for-win#5625](https://github.com/docker/for-win#5625)。
- Docker Desktop 现在允许在禁用 PowerShell 的机器上运行 Docker。
- 修复了 Compose v2 在 Windows 上并非总是默认启用的问题。
- Docker Desktop 现在会在卸载时删除 `C:\Program Files\Docker` 文件夹。

### 已知问题

- 对于部分 macOS 用户，安装程序存在一个已知问题，导致无法安装 Docker Desktop 实验性漏洞和软件包发现功能所需的新辅助工具。要解决此问题，需要创建一个符号链接，可通过以下命令创建：`sudo ln -s /Applications/Docker.app/Contents/Resources/bin/docker-index /usr/local/bin/docker-index`

## 4.13.1

{{< release-date date="2022-10-31" >}}

### 更新

- [Docker Compose v2.12.1](https://github.com/docker/compose/releases/tag/v2.12.1)

### Bug 修复与增强

#### 所有平台

- 修复了使用 `Control+C` 或 `CMD+C` 中断 `docker pull` 时可能出现的段错误。
- 增加了默认 DHCP 租约时间，以避免虚拟机网络每两小时出现故障和断开连接。
- 将 `Qemu` 回退至 `6.2.0`，以修复运行模拟 amd64 代码时出现的 `PR_SET_CHILD_SUBREAPER is unavailable` 等错误。

#### macOS

- 默认重新添加了 macOS 上的 `/var/run/docker.sock` 符号链接，以提高与 `tilt` 和 `docker-py` 等工具的兼容性。修复了 [docker/for-mac#6529](https://github.com/docker/for-mac/issues/6529)。
- 修复了阻止在新 Mac 安装上创建开发环境并导致 `error "Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?"` 的问题。

#### Windows

- Docker Desktop 现在可在禁用 PowerShell 的机器上运行。

## 4.13.0

{{< release-date date="2022-10-19" >}}

### 新增功能

- 为 Docker Business 用户引入了两项新的安全功能：设置管理和增强型容器隔离。详细了解 Docker Desktop 的新[强化 Docker Desktop 安全模型](/manuals/enterprise/security/hardened-desktop/_index.md)。
- 添加了新的开发环境 CLI 命令 `docker dev`，可通过命令行创建、列出和运行开发环境。现在可以更轻松地将开发环境集成到自定义脚本中。
- Docker Desktop 现在可使用 `--installation-dir` 安装到任意驱动器和文件夹。部分解决了 [docker/roadmap#94](https://github.com/docker/roadmap/issues/94)。

### 更新

- [Docker Scan v0.21.0](https://github.com/docker/scan-cli-plugin/releases/tag/v0.21.0)
- [Go 1.19.2](https://github.com/golang/go/releases/tag/go1.19.2)，用于修复 [CVE-2022-2879](https://www.cve.org/CVERecord?id=CVE-2022-2879)、[CVE-2022-2880](https://www.cve.org/CVERecord?id=CVE-2022-2880) 和 [CVE-2022-41715](https://www.cve.org/CVERecord?id=CVE-2022-41715)
- 将 Docker Engine 和 Docker CLI 更新至 [v20.10.20](/manuals/engine/release-notes/20.10.md#201020)，其中包含针对 Git 漏洞的缓解措施（[CVE-2022-39253](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-39253)），并更新了 `image:tag@digest` 镜像引用的处理方式，同时修复了 [CVE-2022-36109](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-36109)。
- [Docker Credential Helpers v0.7.0](https://github.com/docker/docker-credential-helpers/releases/tag/v0.7.0)
- [Docker Compose v2.12.0](https://github.com/docker/compose/releases/tag/v2.12.0)
- [Kubernetes v1.25.2](https://github.com/kubernetes/kubernetes/releases/tag/v1.25.2)
- [Qemu 7.0.0](https://wiki.qemu.org/ChangeLog/7.0)，用于 Docker Desktop 虚拟机内的 CPU 模拟。
- [Linux 内核 5.15.49](https://hub.docker.com/layers/docker/for-desktop-kernel/5.15.49-13422a825f833d125942948cf8a8688cef721ead/images/sha256-ebf1f6f0cb58c70eaa260e9d55df7c43968874d62daced966ef6a5c5cd96b493?context=explore)

### Bug 修复与增强

#### 所有平台

- Docker Desktop 现在允许在与 HTTP 和 HTTPS 代理通信时使用 TLS，以加密代理用户名和密码。
- Docker Desktop 现在将 HTTP 和 HTTPS 代理密码存储在操作系统凭据存储中。
- 如果 Docker Desktop 检测到 HTTP 或 HTTPS 代理密码已更改，则会提示开发者输入新密码。
- **为此主机和域绕过代理设置** 现在可正确处理 HTTPS 的域名。
- **远程仓库** 视图和每日提示现在支持需要身份验证的 HTTP 和 HTTPS 代理。
- 我们为产品开发生命周期早期阶段的功能引入了暗启动机制。已选择加入的用户可随时在“测试版功能”设置中取消选择。
- 为扩展市场添加了分类。
- 在鲸鱼菜单和 **扩展** 标签页中添加了扩展更新可用时的指示器。
- 修复了卸载不带命名空间的镜像名称（如 'my-extension'）的扩展时失败的问题。
- 在 **容器** 标签页中显式显示端口映射。
- 将镜像磁盘使用信息的刷新频率更改为每天自动一次。
- 使 **容器** 和 **卷** 标签页的标签样式保持一致。
- 修复了 **设置** 中 Grpcfuse 文件共享模式启用问题。修复了 [docker/for-mac#6467](https://github.com/docker/for-mac/issues/6467)。
- 对于运行 macOS < 12.5 的用户，已禁用虚拟化框架和 VirtioFS。
- **容器** 标签页中的端口现在可点击。
- 扩展 SDK 现在允许 `ddClient.extension.vm.cli.exec`、`ddClient.extension.host.cli.exec`、`ddClient.docker.cli.exec` 接受不同的工作目录并通过选项参数传递环境变量。
- 添加了在侧边栏点击 **扩展** 时导航至扩展市场的小改进。
- 为市场中的新扩展添加了标识徽章。
- 修复了使用 containerd 集成时 Kubernetes 无法启动的问题。
- 修复了使用 containerd 集成时 `kind` 无法启动的问题。
- 修复了使用 containerd 集成时开发环境无法工作的问题。
- 在 containerd 集成中实现了 `docker diff`。
- 在 containerd 集成中实现了 `docker run —-platform`。
- 修复了使用 containerd 集成时不安全注册表无法工作的问题。
- 修复了 **设置** 中已用空间显示错误值的问题。
- Docker Desktop 现在从 Github 发布版本安装凭据助手。参见 [docker/for-win#10247](https://github.com/docker/for-win/issues/10247)、[docker/for-win#12995](https://github.com/docker/for-win/issues/12995)。
- 修复了用户 7 天后从 Docker Desktop 注销的问题。

#### macOS

- 为 Docker Desktop 添加了 **隐藏**、**隐藏其他**、**显示全部** 菜单项。参见 [docker/for-mac#6446](https://github.com/docker/for-mac/issues/6446)。
- 修复了从已安装的应用程序运行安装实用程序时导致应用程序被删除的 Bug。修复了 [docker/for-mac#6442](https://github.com/docker/for-mac/issues/6442)。
- 默认情况下，Docker 不会在主机上创建 /var/run/docker.sock 符号链接，而是使用 docker-desktop CLI 上下文。

#### Linux

- 修复了无法从仪表板推送镜像的问题

## 4.12.0

{{< release-date date="2022-09-01" >}}

### 新增功能

- 新增支持使用 containerd 拉取和存储镜像。这是一项实验性功能。
- Docker Desktop 现在可以运行未打标签的镜像。修复了 [docker/for-mac#6425](https://github.com/docker/for-mac/issues/6425)。
- 为 Docker 扩展市场添加了搜索功能。修复了 [docker/roadmap#346](https://github.com/docker/roadmap/issues/346)。
- 新增缩放功能，可放大、缩小或将 Docker Desktop 设置为实际大小。在 Mac 和 Windows 上分别使用快捷键 ⌘ + / CTRL +、⌘ - / CTRL -、⌘ 0 / CTRL 0，或通过 Mac 上的“视图”菜单实现。
- 如果任何相关容器可停止，则新增 Compose 停止按钮。
- 现在可以从**容器**视图中删除单个 Compose 容器。
- 移除了针对 Fedora 35 上 virtiofsd <-> qemu 协议不匹配的临时解决方案，因为该方案已不再需要。Fedora 35 用户应将 qemu 软件包升级到最新版本（截至本文撰写时为 qemu-6.1.0-15.fc35）。
- 为容器实现了集成终端。
- 默认情况下，为所有外部链接添加工具提示以显示链接地址。

### 更新

- [Docker Compose v2.10.2](https://github.com/docker/compose/releases/tag/v2.10.2)
- [Docker Scan v0.19.0](https://github.com/docker/scan-cli-plugin/releases/tag/v0.19.0)
- [Kubernetes v1.25.0](https://github.com/kubernetes/kubernetes/releases/tag/v1.25.0)
- [Go 1.19](https://github.com/golang/go/releases/tag/go1.19)
- [cri-dockerd v0.2.5](https://github.com/Mirantis/cri-dockerd/releases/tag/v0.2.5)
- [Buildx v0.9.1](https://github.com/docker/buildx/releases/tag/v0.9.1)
- [containerd v1.6.8](https://github.com/containerd/containerd/releases/tag/v1.6.8)
- [containerd v1.6.7](https://github.com/containerd/containerd/releases/tag/v1.6.7)
- [runc v1.1.4](https://github.com/opencontainers/runc/releases/tag/v1.1.4)
- [runc v1.1.3](https://github.com/opencontainers/runc/releases/tag/v1.1.3)

### 安全

#### 所有平台

- 修复了 [CVE-2023-0626](https://www.cve.org/cverecord?id=CVE-2023-0626)，该漏洞允许通过 Electron 客户端中 message-box 路由的查询参数实现远程代码执行（RCE）。
- 修复了 [CVE-2023-0625](https://www.cve.org/cverecord?id=CVE-2023-0625)，该漏洞允许通过扩展描述/更新日志实现远程代码执行（RCE），恶意扩展可能滥用此漏洞。

#### Windows 平台

- 修复了 [CVE-2023-0627](https://www.cve.org/cverecord?id=CVE-2023-0627)，该漏洞允许绕过在 4.11 版本中引入的 `--no-windows-containers` 安装标志。此标志允许管理员禁用 Windows 容器功能。
- 修复了 [CVE-2023-0633](https://www.cve.org/cverecord?id=CVE-2023-0633)，该漏洞涉及 Docker Desktop 安装程序中的参数注入，可能导致本地权限提升。

### Bug 修复与小幅增强

#### 所有平台

- 工厂重置后，Compose V2 现已启用。
- 在新安装的 Docker Desktop 上，Compose V2 默认启用。
- Compose 中环境变量的优先级顺序更加一致，并已在[文档](/manuals/compose/how-tos/environment-variables/envvars-precedence.md)中明确说明。
- 内核升级至 5.10.124。
- 改进了因计算磁盘大小导致的整体性能问题。相关 issue：[docker/for-win#9401](https://github.com/docker/for-win/issues/9401)。
- Docker Desktop 现在会阻止未安装 Rosetta 的 ARM Mac 用户切换回仅包含 Intel 二进制文件的 Compose V1。
- 卷大小、“创建时间”列以及容器的“启动时间”列的默认排序顺序更改为降序。
- 重新组织了容器行操作：始终仅显示启动/停止和删除操作，其余操作通过行菜单项访问。
- 快速入门指南现在会立即执行每一条命令。
- 为容器/Compose 的“状态”列定义了排序顺序：运行中 > 部分运行中 > 已暂停 > 部分已暂停 > 已退出 > 部分已退出 > 已创建。
- 修复了即使存在镜像，Docker Desktop 中镜像列表仍显示为空的问题。相关 issue：[docker/for-win#12693](https://github.com/docker/for-win/issues/12693) 和 [docker/for-mac#6347](https://github.com/docker/for-mac/issues/6347)。
- 根据是否显示系统容器来定义哪些镜像“正在使用”。如果不显示与 Kubernetes 和扩展相关的系统容器，则相关镜像不会被定义为“正在使用”。
- 修复了某些语言环境下 `docker exec` 导致 Docker 客户端挂起的问题。修复了 [https://github.com/apocas/dockerode/issues/534](https://github.com/apocas/dockerode/issues/534)。
- 构建扩展时生成的命令失败不再导致 Docker Desktop 意外退出。
- 修复了扩展在左侧菜单中显示为禁用状态（实际未禁用）的问题。
- 修复了当启用注册表访问管理且阻止访问 Docker Hub 时，无法登录私有注册表的问题。
- 修复了如果当前集群元数据未存储在 `.kube/config` 文件中，Docker Desktop 无法启动 Kubernetes 集群的问题。
- 更新了 Docker Desktop 和 MUI 主题包中的工具提示，以与整体系统设计保持一致。
- 复制的终端内容不再包含不间断空格。

#### Mac 平台

- 在 macOS 上安装或更新 Docker Desktop 的最低版本要求现为 10.15。修复了 [docker/for-mac#6007](https://github.com/docker/for-mac/issues/6007)。
- 修复了下载更新后托盘菜单错误显示“下载即将开始...”的问题。修复了 [for-mac/issues#5677](https://github.com/docker/for-mac/issues/5677) 中报告的部分问题。
- 修复了应用更新后 Docker Desktop 未重启的问题。
- 修复了当用户使用 virtualization.framework 且防火墙软件限制严格时，计算机进入睡眠状态导致 Docker 连接丢失的问题。
- 修复了即使用户已退出应用程序，Docker Desktop 仍在后台运行的问题。修复了 [docker/for-mac##6440](https://github.com/docker/for-mac/issues/6440)。
- 对于运行 macOS < 12.5 的用户，已禁用 Virtualization Framework 和 VirtioFS。

#### Windows 平台

- 修复了更新过程中显示的版本可能不正确的问题。修复了 [for-win/issues#12822](https://github.com/docker/for-win/issues/12822)。

## 4.11.1

{{< release-date date="2022-08-05" >}}

### Bug 修复与增强

#### 所有平台

- 修复了阻止绑定挂载 VM 系统位置（例如 /var/lib/docker）的回归问题 [for-mac/issues#6433](https://github.com/docker/for-mac/issues/6433)

#### Windows 平台

- 修复了从 WSL2 发行版登录私有注册表的问题 [docker/for-win#12871](https://github.com/docker/for-win/issues/12871)

## 4.11.0

{{< release-date date="2022-07-28" >}}

### 新增功能

- Docker Desktop 现已全面支持在 VMware ESXi 和 Azure 虚拟机内的 Docker Business 客户使用。更多信息请参阅[在 VM 或 VDI 环境中运行 Docker Desktop](/manuals/desktop/setup/vm-vdi.md)
- 向扩展市场新增两个扩展：[vcluster](https://hub.docker.com/extensions/loftsh/vcluster-dd-extension) 和 [PGAdmin4](https://hub.docker.com/extensions/mochoa/pgadmin4-docker-extension)。
- 扩展市场现已支持对扩展进行排序。
- 修复了某些用户被频繁要求提供反馈的问题。现在每年仅会请求两次反馈。
- 为 Docker Desktop 添加了自定义主题设置。允许您独立于设备设置指定 Docker Desktop 的深色或浅色模式。修复了 [docker/for-win#12747](https://github.com/docker/for-win/issues/12747)
- 为 Windows 安装程序新增一个标志：`--no-windows-containers`，用于禁用 Windows 容器集成。
- 为 Mac 安装命令新增一个标志：`--user <username>`，用于为特定用户配置 Docker Desktop，避免首次运行时需要管理员密码。

### 更新

- [Docker Compose v2.7.0](https://github.com/docker/compose/releases/tag/v2.7.0)
- [Docker Compose "Cloud Integrations" v1.0.28](https://github.com/docker/compose-cli/releases/tag/v1.0.28)
- [Kubernetes v1.24.2](https://github.com/kubernetes/kubernetes/releases/tag/v1.24.2)
- [Go 1.18.4](https://github.com/golang/go/releases/tag/go1.18.4)

### Bug 修复与增强功能

#### 适用于所有平台

- 在“容器”页面中添加了容器/Compose 图标以及暴露的端口/退出代码。
- 更新了 Docker 主题调色板的颜色值，以匹配我们的设计系统。
- 改进了 `docker login` 的错误提示信息，当“注册表访问管理”阻止 Docker 引擎访问 Docker Hub 时，会显示更清晰的提示。
- 提高了主机与 Docker 之间的吞吐量。例如，提升了 `docker cp` 的性能。
- 收集诊断信息所需的时间更短。
- 在容器概览页面中，选择或取消选择一个 Compose 应用时，会自动选择/取消选择其所有容器。
- 容器概览页面的镜像列中，标签名称现在可见。
- 为终端滚动条添加了搜索高亮标记，以便查看视口外的匹配项。
- 修复了容器页面搜索功能无法正常工作的问题 [docker/for-win#12828](https://github.com/docker/for-win/issues/12828)。
- 修复了 **Volume** 页面无限加载的问题 [docker/for-win#12789](https://github.com/docker/for-win/issues/12789)。
- 修复了容器 UI 中调整列宽或隐藏列无效的问题。修复了 [docker/for-mac#6391](https://github.com/docker/for-mac/issues/6391)。
- 修复了同时安装、更新或卸载多个扩展时，离开扩展市场页面后状态丢失的问题。
- 修复了关于页面中 Compose 版本仅在重启 Docker Desktop 后才会从 v2 更新为 v1 的问题。
- 修复了由于底层硬件不支持 WebGL2 渲染导致用户无法查看日志视图的问题。修复了 [docker/for-win#12825](https://github.com/docker/for-win/issues/12825)。
- 修复了容器和镜像 UI 不同步的问题。
- 修复了启用实验性虚拟化框架时的启动竞争条件问题。

#### 适用于 Mac

- 修复了从 UI 执行 Compose 命令的问题。修复了 [docker/for-mac#6400](https://github.com/docker/for-mac/issues/6400)。

#### 适用于 Windows

- 修复了水平调整大小的问题。修复了 [docker/for-win#12816](https://github.com/docker/for-win/issues/12816)。
- 如果在 UI 中配置了 HTTP/HTTPS 代理，则会自动将镜像构建和运行容器的流量发送到代理。这避免了在每个容器或构建中单独配置环境变量的需要。
- 添加了 `--backend=windows` 安装程序选项，用于将 Windows 容器设置为默认后端。

#### 适用于 Linux

- 修复了设置路径中包含空格的共享文件夹时的错误。

## 4.10.1

{{< release-date date="2022-07-05" >}}

### Bug 修复与增强功能

#### 适用于 Windows

- 修复了 UI 中对从 WSL 创建的 Compose 应用执行操作失败的问题。修复了 [docker/for-win#12806](https://github.com/docker/for-win/issues/12806)。

#### 适用于 Mac

- 修复了安装命令因路径未初始化而失败的问题。修复了 [docker/for-mac#6384](https://github.com/docker/for-mac/issues/6384)。

## 4.10.0

{{< release-date date="2022-06-30" >}}

### 新增功能

- 现在可以在 Docker Desktop 中运行镜像之前添加环境变量。
- 添加了便于处理容器日志的功能，例如正则表达式搜索以及在容器运行时清除日志的能力。
- 实现了对容器表格的反馈。添加了端口信息，并分离了容器和镜像名称。
- 在扩展市场中添加了两个新扩展：Ddosify 和 Lacework。

### 移除功能

- 在重新设计期间移除了主页。您可以通过[此处](https://docs.google.com/forms/d/e/1FAIpQLSfYueBkJHdgxqsWcQn4VzBn2swu4u_rMQRIMa8LExYb_72mmQ/viewform?entry.1237514594=4.10)提供反馈。

### 更新内容

- [Docker Engine v20.10.17](/manuals/engine/release-notes/20.10.md#201017)
- [Docker Compose v2.6.1](https://github.com/docker/compose/releases/tag/v2.6.1)
- [Kubernetes v1.24.1](https://github.com/kubernetes/kubernetes/releases/tag/v1.24.1)
- [cri-dockerd v0.2.1](https://github.com/Mirantis/cri-dockerd/releases/tag/v0.2.1)
- [CNI 插件 v1.1.1](https://github.com/containernetworking/plugins/releases/tag/v1.1.1)
- [containerd v1.6.6](https://github.com/containerd/containerd/releases/tag/v1.6.6)
- [runc v1.1.2](https://github.com/opencontainers/runc/releases/tag/v1.1.2)
- [Go 1.18.3](https://github.com/golang/go/releases/tag/go1.18.3)

### Bug 修复与增强功能

#### 适用于所有平台

- 在 **容器** 标签页中为选中的容器添加了额外的批量操作，包括启动/暂停/停止。
- 在 **容器** 标签页中为 Compose 项目添加了暂停和重启操作。
- 在 **容器** 标签页中添加了图标以及暴露的端口或退出代码信息。
- 外部 URL 现在可以通过类似 `docker-desktop://extensions/marketplace?extensionId=docker/logs-explorer-extension` 的链接引用扩展市场中的扩展详情。
- Compose 应用的展开或折叠状态现在会被持久化保存。
- `docker extension` CLI 命令现在默认在 Docker Desktop 中可用。
- 扩展市场中显示的截图尺寸已增大。
- 修复了当扩展的后端容器停止时，Docker 扩展无法加载的问题。修复了 [docker/extensions-sdk#16](https://github.com/docker/extensions-sdk/issues/162)。
- 修复了镜像搜索字段无故被清空的问题。修复了 [docker/for-win#12738](https://github.com/docker/for-win/issues/12738)。
- 修复了许可协议未显示并静默阻止 Docker Desktop 启动的问题。
- 修复了未发布扩展的显示镜像和标签，现在会正确显示已安装的未发布扩展的实际镜像和标签。
- 修复了支持页面重复页脚的问题。
- 现在可以从 GitHub 仓库的子目录创建开发环境。
- 移除了离线使用 Docker Desktop 时无法加载每日提示的错误消息。修复了 [docker/for-mac#6366](https://github.com/docker/for-mac/issues/6366)。

#### 适用于 Mac

- 修复了 macOS 上 bash 补全文件位置的问题。修复了 [docker/for-mac#6343](https://github.com/docker/for-mac/issues/6343)。
- 修复了用户名超过 25 个字符时 Docker Desktop 无法启动的问题。修复了 [docker/for-mac#6122](https://github.com/docker/for-mac/issues/6122)。
- 修复了由于系统代理配置无效导致 Docker Desktop 无法启动的问题。修复了 [docker/for-mac#6289](https://github.com/docker/for-mac/issues/6289) 中报告的一些问题。
- 修复了启用实验性虚拟化框架时 Docker Desktop 启动失败的问题。
- 修复了卸载 Docker Desktop 后托盘图标仍然显示的问题。

#### 适用于 Windows

- 修复了导致 Hyper-V 高 CPU 使用率的错误。修复了 [docker/for-win#12780](https://github.com/docker/for-win/issues/12780)。
- 修复了 Docker Desktop for Windows 启动失败的问题。修复了 [docker/for-win#12784](https://github.com/docker/for-win/issues/12784)。
- 修复了 `--backend=wsl-2` 安装标志未将后端设置为 WSL 2 的问题。修复了 [docker/for-win#12746](https://github.com/docker/for-win/issues/12746)。

#### 适用于 Linux

- 修复了设置无法多次应用的问题。
- 修复了 `关于` 页面中显示的 Compose 版本。

### 已知问题

- 偶尔在执行 `docker system prune` 时，Docker 引擎会重启。这是当前引擎中使用的 buildkit 版本的[已知问题](https://github.com/moby/buildkit/pull/2177)，将在未来的版本中修复。

## 4.9.1

{{< release-date date="2022-06-16" >}}

{{< desktop-install all=true version="4.9.1" build_path="/81317/" >}}

### Bug 修复与增强功能

#### 适用于所有平台

- 修复了仪表盘空白屏幕的问题。修复 [docker/for-win#12759](https://github.com/docker/for-win/issues/12759)。

## 4.9.0

{{< release-date date="2022-06-02" >}}

### 新增功能

- 在主页上添加了以下额外指南：Elasticsearch、MariaDB、Memcached、MySQL、RabbitMQ 和 Ubuntu。
- 在 Docker Desktop 仪表盘中添加了页脚，显示 Docker Desktop 更新状态和 Docker Engine 统计信息
- 重新设计了容器表格，新增：
  - 复制容器 ID 到剪贴板的按钮
  - 每个容器的暂停按钮
  - 容器表格的列宽调整功能
  - 容器表格的排序和列宽调整持久化
  - 容器表格的批量删除功能

### 更新内容

- [Compose v2.6.0](https://github.com/docker/compose/releases/tag/v2.6.0)
- [Docker Engine v20.10.16](/manuals/engine/release-notes/20.10.md#201016)
- [containerd v1.6.4](https://github.com/containerd/containerd/releases/tag/v1.6.4)
- [runc v1.1.1](https://github.com/opencontainers/runc/releases/tag/v1.1.1)
- [Go 1.18.2](https://github.com/golang/go/releases/tag/go1.18.2)

### Bug 修复与增强

#### 全平台通用

- 修复了当 Docker Desktop 暂停时退出应用导致程序挂起的问题。
- 修复了 PKI 过期后 Kubernetes 集群无法正确重置的问题。
- 修复了扩展市场未使用已定义 HTTP 代理的问题。
- 改进了 Docker Desktop 仪表盘中的日志搜索功能，支持空格输入。
- 仪表盘中按钮的中键点击现在表现为左键点击，而不是打开空白窗口。

#### macOS 专用

- 修复了当 `/opt` 已添加到文件共享目录列表时，避免在主机上创建 `/opt/containerd/bin` 和 `/opt/containerd/lib` 的问题。

#### Windows 专用

- 修复了 WSL 2 集成中的一个 Bug：当文件或目录绑定挂载到容器，且容器退出时，该文件或目录会被替换为同名但类型不同的对象（例如文件被替换为目录，或目录被替换为文件），导致后续绑定挂载新对象失败。
- 修复了托盘图标和仪表盘 UI 不显示以及 Docker Desktop 无法完全启动的问题。修复 [docker/for-win#12622](https://github.com/docker/for-win/issues/12622)。

### 已知问题

#### Linux 专用

- 绑定挂载中文件的所有权权限更改失败。这是由于我们在运行 Docker Engine 的虚拟机与主机之间实现文件共享的方式导致的。我们计划在下一版本中解决此问题。

## 4.8.2

{{< release-date date="2022-05-18" >}}

### 更新内容

- [Compose v2.5.1](https://github.com/docker/compose/releases/tag/v2.5.1)

### Bug 修复与小幅增强

- 修复了手动代理设置导致拉取镜像时出现问题的问题。修复 [docker/for-win#12714](https://github.com/docker/for-win/issues/12714) 和 [docker/for-mac#6315](https://github.com/docker/for-mac/issues/6315)。
- 修复了禁用扩展时 CPU 占用过高的问题。修复 [docker/for-mac#6310](https://github.com/docker/for-mac/issues/6310)。
- Docker Desktop 现在在日志文件和诊断信息中隐藏 HTTP 代理密码。

### 已知问题

#### Linux 专用

- 绑定挂载中文件的所有权权限更改失败。这是由于我们在运行 Docker Engine 的虚拟机与主机之间实现文件共享的方式导致的。我们计划在下一版本中解决此问题。

## 4.8.1

{{< release-date date="2022-05-09" >}}

### 新增功能

- 发布 [Docker Desktop for Linux](/manuals/desktop/setup/install/linux/_index.md)。
- [Docker 扩展](/manuals/extensions/_index.md) 和扩展 SDK 进入 Beta 阶段。
- 创建了 Docker 主页，您可以在其中运行热门镜像并了解其使用方法。
- [Compose V2 现已正式发布 (GA)](https://www.docker.com/blog/announcing-compose-v2-general-availability/)

### Bug 修复与增强

- 修复了更新 Docker Desktop 时 Kubernetes 集群被删除的问题。

### 已知问题

#### Linux 专用

- 绑定挂载中文件的所有权权限更改失败。这是由于我们在运行 Docker Engine 的虚拟机与主机之间实现文件共享的方式导致的。我们计划在下一版本中解决此问题。

## 4.8.0

{{< release-date date="2022-05-06" >}}

### 新增功能

- 发布 [Docker Desktop for Linux](/manuals/desktop/setup/install/linux/_index.md)。
- [Docker 扩展](/manuals/extensions/_index.md) 和扩展 SDK 进入 Beta 阶段。
- 创建了 Docker 主页，您可以在其中运行热门镜像并了解其使用方法。
- [Compose V2 现已正式发布 (GA)](https://www.docker.com/blog/announcing-compose-v2-general-availability/)

### 更新内容

- [Compose v2.5.0](https://github.com/docker/compose/releases/tag/v2.5.0)
- [Go 1.18.1](https://github.com/golang/go/releases/tag/go1.18.1)
- [Kubernetes 1.24](https://github.com/kubernetes/kubernetes/releases/tag/v1.24.0)

### Bug 修复与小幅增强

#### 全平台通用

- 引入系统代理读取功能。除非您的代理设置与操作系统级别的代理不同，否则无需手动配置代理。
- 修复了在使用代理时在仪表盘中显示远程仓库的问题。
- 修复了 vpnkit 在服务器已断开的情况下仍建立并阻塞客户端连接的问题。参见 [docker/for-mac#6235](https://github.com/docker/for-mac/issues/6235)
- 对 Docker Desktop 中的卷标签页进行了改进：
  - 显示卷大小。
  - 列可以调整大小、隐藏和重新排序。
  - 列的排序顺序和隐藏状态会持久化保存，即使 Docker Desktop 重启后依然有效。
  - 切换标签页时行选择状态会持久化保存，即使 Docker Desktop 重启后依然有效。
- 修复了开发环境标签页在屏幕添加更多项目时未添加滚动条的问题。
- 标准化了仪表盘中的标题和操作按钮。
- 添加通过 HTTP 代理下载注册表访问管理策略的支持。
- 修复了机器长时间处于睡眠模式时远程仓库为空的问题。
- 修复了清理过程中未选中名称未标记为 "&lt;none>" 但标签为 "&lt;none>" 的悬空镜像的问题。
- 改进了因需要 HTTP 代理而导致 `docker pull` 失败时的错误提示信息。
- 添加了轻松清除 Docker Desktop 搜索栏的功能。
- 将“容器 / 应用”标签页重命名为“容器”。
- 修复了当 `C:\ProgramData\DockerDesktop` 是文件或符号链接时 Docker Desktop 安装程序静默崩溃的问题。
- 修复了没有命名空间的镜像（例如 `docker pull <私有注册表>/镜像`）会被注册表访问管理错误阻止的问题，除非在设置中启用了对 Docker Hub 的访问。

#### macOS 专用

- Docker Desktop 图标现在符合 Big Sur 风格指南。参见 [docker/for-mac#5536](https://github.com/docker/for-mac/issues/5536)
- 修复了 Dock 图标重复以及 Dock 图标行为异常的问题。修复 [docker/for-mac#6189](https://github.com/docker/for-mac/issues/6189)。
- 改进了对 `Cmd+Q` 快捷键的支持。

#### Windows 专用

- 改进了对 `Ctrl+W` 快捷键的支持。

### 已知问题

#### 全平台通用

- 目前，如果您正在运行 Kubernetes 集群，升级到 Docker Desktop 4.8.0 时集群将被删除。我们计划在下一版本中修复此问题。

#### Linux 专用

- 绑定挂载中文件的所有权权限更改失败。这是由于我们在运行 Docker Engine 的虚拟机与主机之间实现文件共享的方式导致的。我们计划在下一版本中解决此问题。

## 4.7.1

{{< release-date date="2022-04-19" >}}

### Bug 修复与增强

#### 全平台通用

- 修复了快速入门指南最后一屏崩溃的问题。

#### Windows 专用

- 修复了因符号链接错误导致更新失败的问题。修复 [docker/for-win#12650](https://github.com/docker/for-win/issues/12650)。
- 修复了无法使用 Windows 容器模式的问题。修复 [docker/for-win#12652](https://github.com/docker/for-win/issues/12652)。

## 4.7.0

{{< release-date date="2022-04-07" >}}

### 新增功能

- IT 管理员现在可以通过命令行远程安装 Docker Desktop。
- 添加 Docker 软件物料清单（SBOM）CLI 插件。这个新的 CLI 插件使用户能够为 Docker 镜像生成 SBOM。
- 新的 Kubernetes 集群现在使用 [cri-dockerd](https://github.com/Mirantis/cri-dockerd) 替代 `dockershim`。从用户的角度来看，这一变化是透明的，Kubernetes 容器仍像以前一样在 Docker Engine 上运行。`cri-dockerd` 允许 Kubernetes 使用标准的 [容器运行时接口](https://github.com/kubernetes/cri-api#readme) 来管理 Docker 容器，该接口与控制其他容器运行时使用的接口相同。更多信息请参阅 [Dockershim 的未来是 cri-dockerd](https://www.mirantis.com/blog/the-future-of-dockershim-is-cri-dockerd/)。

### 更新

- [Docker Engine v20.10.14](/manuals/engine/release-notes/20.10.md#201014)
- [Compose v2.4.1](https://github.com/docker/compose/releases/tag/v2.4.1)
- [Buildx 0.8.2](https://github.com/docker/buildx/releases/tag/v0.8.2)
- [containerd v1.5.11](https://github.com/containerd/containerd/releases/tag/v1.5.11)
- [Go 1.18](https://golang.org/doc/go1.18)

### 安全

- 更新 Docker Engine 至 v20.10.14 以解决 [CVE-2022-24769](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-24769)
- 更新 containerd 至 v1.5.11 以解决 [CVE-2022-24769](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-24769)

### Bug 修复和增强

#### 所有平台

- 修复了注册表访问管理策略在失败后从不刷新的错误。
- UI 中的日志和终端现在遵循操作系统的浅色和深色主题。
- 通过多选复选框可以一次性轻松清理多个卷。
- 改进了登录反馈。

#### Mac

- 修复了有时导致 Docker Desktop 显示空白白屏的问题。修复了 [docker/for-mac#6134](https://github.com/docker/for-mac/issues/6134)。
- 修复了使用 Hyperkit 时，从睡眠状态唤醒后 gettimeofday() 性能下降的问题。修复了 [docker/for-mac#3455](https://github.com/docker/for-mac/issues/3455)。
- 修复了当使用 `osxfs` 进行文件共享时，Docker Desktop 在启动期间变得无响应的问题。

#### Windows

- 修复了卷标题。修复了 [docker/for-win#12616](https://github.com/docker/for-win/issues/12616)。
- 修复了 WSL 2 集成中的一个错误，该错误导致在重启 Docker Desktop 或切换到 Windows 容器后 Docker 命令停止工作。

## 4.6.1

{{< release-date date="2022-03-22" >}}

### 更新

- [Buildx 0.8.1](https://github.com/docker/buildx/releases/tag/v0.8.1)

### Bug 修复和增强

- 防止 vpnkit-forwarder 不断旋转并在日志中填充错误消息。
- 修复了当没有设置 HTTP 代理时的诊断上传。修复了 [docker/for-mac#6234](https://github.com/docker/for-mac/issues/6234)。
- 从自我诊断中移除了误报的“vm is not running”错误。修复了 [docker/for-mac#6233](https://github.com/docker/for-mac/issues/6233)。

## 4.6.0

{{< release-date date="2022-03-14" >}}

### 新增

#### 所有平台

- Docker Desktop 仪表板卷管理功能现在提供了使用多选复选框高效清理卷的能力。

#### Mac

- Docker Desktop 4.6.0 为 macOS 用户提供了启用名为 VirtioFS 的新实验性文件共享技术的选项。在测试中，VirtioFS 被证明可以大幅减少主机和虚拟机之间同步更改所需的时间，从而带来显著的性能改进。更多信息请参阅 [VirtioFS](/manuals/desktop/settings-and-maintenance/settings.md#beta-features)。

### 更新

#### 所有平台

- [Docker Engine v20.10.13](/manuals/engine/release-notes/20.10.md#201013)
- [Compose v2.3.3](https://github.com/docker/compose/releases/tag/v2.3.3)
- [Buildx 0.8.0](https://github.com/docker/buildx/releases/tag/v0.8.0)
- [containerd v1.4.13](https://github.com/containerd/containerd/releases/tag/v1.4.13)
- [runc v1.0.3](https://github.com/opencontainers/runc/releases/tag/v1.0.3)
- [Go 1.17.8](https://golang.org/doc/go1.17)
- [Linux kernel 5.10.104](https://hub.docker.com/layers/docker/for-desktop-kernel/5.10.104-379cadd2e08e8b25f932380e9fdaab97755357b3/images/sha256-7753b60f4544e5c5eed629d12151a49c8a4b48d98b4fb30e4e65cecc20da484d?context=explore)

### 安全

#### 所有平台

- 修复了 [CVE-2022-0847](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-0847)，即“Dirty Pipe”，这是一个可能使攻击者能够在容器内部修改主机上容器镜像中文件的问题。
  如果使用 WSL 2 后端，必须通过运行 `wsl --update` 来更新 WSL 2。

#### Windows

- 修复了 [CVE-2022-26659](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-26659)，该漏洞可能允许攻击者在安装或更新 Docker Desktop 期间覆盖系统上任何管理员可写的文件。

#### Mac

- [Qemu 6.2.0](https://wiki.qemu.org/ChangeLog/6.2)

### Bug 修复和增强

#### 所有平台

- 修复了当设置了 HTTPS 代理时的诊断上传。
- 使从系统托盘菜单检查更新时打开软件更新设置部分。

#### Mac

- 修复了启动 Docker Desktop 后系统托盘菜单不显示所有菜单项的问题。修复了 [docker/for-mac#6192](https://github.com/docker/for-mac/issues/6192)。
- 修复了关于 Docker Desktop 不再在后台启动的回归问题。修复了 [docker/for-mac#6167](https://github.com/docker/for-mac/issues/6167)。
- 修复了丢失 Docker Desktop Dock 图标的问题。修复了 [docker/for-mac#6173](https://github.com/docker/for-mac/issues/6173)。
- 使用实验性的 `virtualization.framework` 时加快了块设备访问速度。参见 [基准测试](https://github.com/docker/roadmap/issues/7#issuecomment-1050626886)。
- 将默认虚拟机内存分配增加到物理内存的一半（最小 2 GB，最大 8 GB），以获得更好的开箱即用性能。

#### Windows

- 修复了 UI 卡在 `starting` 状态 forever 的问题，尽管 Docker Desktop 从命令行工作正常。
- 修复了丢失 Docker Desktop 系统托盘图标的问题 [docker/for-win#12573](https://github.com/docker/for-win/issues/12573)
- 修复了使用最新 5.10.60.1 内核时 WSL 2 下的注册表访问管理。
- 修复了从 WSL 2 环境启动 Compose 应用程序的容器时 UI 崩溃的问题。修复了 [docker/for-win#12567](https://github.com/docker/for-win/issues/12567)。
- 修复了从快速入门指南的终端复制文本的问题。修复了 [docker/for-win#12444](https://github.com/docker/for-win/issues/12444)。

### 已知问题

#### Mac

- 启用 VirtioFS 后，以不同 Unix 用户 ID 运行的进程的容器可能会遇到缓存问题。例如，如果以 `root` 身份运行的进程查询一个文件，而另一个以 `nginx` 用户身份运行的进程立即尝试访问同一文件，`nginx` 进程将获得“Permission Denied”错误。

## 4.5.1

{{< release-date date="2022-02-15" >}}

### Bug 修复和增强

#### Windows

- 修复了导致新安装默认使用 Hyper-V 后端而不是 WSL 2 的问题。
- 修复了 Docker Desktop 仪表板中的崩溃问题，该问题会导致系统托盘菜单消失。

如果您在 Windows Home 上运行 Docker Desktop，安装 4.5.1 将自动将其切换回 WSL 2。如果您运行的是其他版本的 Windows，并且希望 Docker Desktop 使用 WSL 2 后端，则必须通过在 **Settings > General** 部分启用 **Use the WSL 2 based engine** 选项来手动切换。
或者，您可以编辑位于 `%APPDATA%\Docker\settings.json` 的 Docker Desktop 设置文件，并手动将 `wslEngineEnabled` 字段的值切换为 `true`。

## 4.5.0

{{< release-date date="2022-02-10" >}}

### 新增

- Docker Desktop 4.5.0 引入了新版 Docker 菜单，为所有操作系统提供一致的用户体验。更多信息请参阅博客文章 [Docker Desktop 4.5 全新菜单与改进版发布亮点](https://www.docker.com/blog/new-docker-menu-improved-release-highlights-with-docker-desktop-4-5/)
- 现在 `docker version` 命令的输出会显示机器上安装的 Docker Desktop 版本。

### 更新内容

- [Amazon ECR 凭证助手 v0.6.0](https://github.com/awslabs/amazon-ecr-credential-helper/releases/tag/v0.6.0)

### 安全修复

#### macOS 平台

- 修复了 [CVE-2021-44719](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-44719) 漏洞：攻击者可通过容器绕过共享文件夹白名单限制，访问主机上的任意用户文件。

#### Windows 平台

- 修复了 [CVE-2022-23774](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-23774) 漏洞：Docker Desktop 存在允许攻击者移动任意文件的安全缺陷。

### Bug 修复与功能增强

#### 全平台通用

- 修复了用户退出 Docker Desktop 后重新启动应用时错误提示登录的问题
- 通过设置 Linux 系统参数 `fs.inotify.max_user_watches=1048576` 和 `fs.inotify.max_user_instances=8192` 提升文件系统监控（inotify）限制。修复了 [docker/for-mac#6071](https://github.com/docker/for-mac/issues/6071)

#### macOS 平台

- 修复了在未与虚拟机共享主机目录时，使用 `osxfs` 可能导致虚拟机启动过程中无响应的问题
- 修复了当 Docker Compose 应用在不同版本间切换时（例如从 V1 切换到 V2），Docker Desktop 仪表板无法停止该应用的问题
- 修复了用户退出 Docker Desktop 后重新启动应用时错误提示登录的问题
- 修复了 **关于 Docker Desktop** 窗口失效的问题
- 限制 Mac M1 设备 CPU 数量为 8 个以解决启动问题。修复了 [docker/for-mac#6063](https://github.com/docker/for-mac/issues/6063)

#### Windows 平台

- 修复了使用版本 2 启动 compose 应用但仪表板仅支持版本 1 的相关问题

### 已知问题

#### Windows 平台

全新安装 Docker Desktop 4.5.0 存在一个缺陷：默认会使用 Hyper-V 后端而非 WSL 2。这意味着 Windows Home 用户将无法启动 Docker Desktop（因为 WSL 2 是唯一受支持的后端）。要解决此问题，您必须从机器卸载 4.5.0，然后下载并安装 Docker Desktop 4.5.1 或更高版本。或者，您可以编辑位于 `%APPDATA%\Docker\settings.json` 的 Docker Desktop 配置文件，手动将 `wslEngineEnabled` 字段值切换为 `true`。

## 4.4.4

{{< release-date date="2022-01-24" >}}

### Bug 修复与功能增强

#### Windows 平台

- 修复了从 WSL 2 登录的问题。修复了 [docker/for-win#12500](https://github.com/docker/for-win/issues/12500)

### 已知问题

#### Windows 平台

- 通过浏览器登录后点击 **前往桌面** 有时无法将仪表板前置显示
- 登录后当仪表板获得焦点时，即使点击后台窗口有时仍会保持在前台。解决方法：在点击其他应用程序窗口前先点击仪表板
- 当通过 `registry.json` 文件启用组织限制时，每周提示会显示在强制登录对话框上方

## 4.4.3

{{< release-date date="2022-01-14" >}}

### Bug 修复与功能增强

#### Windows 平台

- 禁用仪表板快捷键以防止在最小化或失焦状态下仍被触发。修复了 [docker/for-win#12495](https://github.com/docker/for-win/issues/12495)

### 已知问题

#### Windows 平台

- 通过浏览器登录后点击 **前往桌面** 有时无法将仪表板前置显示
- 登录后当仪表板获得焦点时，即使点击后台窗口有时仍会保持在前台。解决方法：在点击其他应用程序窗口前先点击仪表板
- 当通过 `registry.json` 文件启用组织限制时，每周提示会显示在强制登录对话框上方

## 4.4.2

{{< release-date date="22-01-13" >}}

### 新功能

- 通过 Auth0 和单点登录（SSO）实现简单安全的登录
  - 单点登录：Docker Business 订阅用户现在可配置 SSO，使用其身份提供商（IdP）进行身份验证来访问 Docker。更多信息请参阅 [单点登录](/manuals/enterprise/security/single-sign-on/_index.md)
  - 现在 Docker Desktop 登录将通过浏览器完成，以便您享受密码管理器自动填充的所有便利

### 组件升级

- [Docker Engine v20.10.12](/manuals/engine/release-notes/20.10.md#201012)
- [Compose v2.2.3](https://github.com/docker/compose/releases/tag/v2.2.3)
- [Kubernetes 1.22.5](https://github.com/kubernetes/kubernetes/releases/tag/v1.22.5)
- [docker scan v0.16.0](https://github.com/docker/scan-cli-plugin/releases/tag/v0.16.0)

### 安全修复

- 修复了影响 Docker Desktop 4.3.0 或 4.3.1 用户的 [CVE-2021-45449](../security/_index.md#cve-2021-45449) 漏洞

Docker Desktop 4.3.0 和 4.3.1 版本存在一个缺陷：在登录过程中可能会在用户机器上记录敏感信息（访问令牌或密码）。
仅当用户使用的是 Docker Desktop 4.3.0 或 4.3.1，并且在此期间完成过登录操作时才会受到影响。要获取这些数据需要能够访问用户的本地文件。

### Bug 修复与功能增强

#### 全平台通用

- 如果 `registry.json` 文件在 `allowedOrgs` 字段中包含多个组织，Docker Desktop 将显示错误。如果您需要为不同开发者组使用多个组织，必须为每个组单独配置 `registry.json` 文件
- 修复了 Compose 中将容器名称分隔符从 `-` 回退到 `_` 的回归问题。修复了 [docker/compose-switch](https://github.com/docker/compose-switch/issues/24)

#### macOS 平台

- 修复了仪表板中容器的内存统计信息。修复了 [docker/for-mac/#4774](https://github.com/docker/for-mac/issues/6076)
- 在 `settings.json` 中添加已弃用选项：`"deprecatedCgroupv1": true`，可将 Linux 环境切换回 cgroups v1。如果您的软件需要 cgroups v1，应将其更新为兼容 cgroups v2。虽然 cgroups v1 应继续工作，但某些未来功能可能依赖 cgroups v2。此外，某些 Linux 内核漏洞可能仅在 cgroups v2 下才能修复
- 修复了暂停 Docker Desktop 后将机器置于睡眠模式，导致机器唤醒后 Docker Desktop 无法从暂停状态恢复的问题。修复了 [for-mac#6058](https://github.com/docker/for-mac/issues/6058)

#### Windows 平台

- 执行 **恢复出厂设置** 不再会关闭 Docker Desktop

### 已知问题

#### 全平台通用

- 当通过 `registry.json` 文件启用组织限制时，每周提示会显示在强制登录对话框上方

#### Windows 平台

- 通过浏览器登录后点击 **前往桌面** 有时无法将仪表板前置显示
- 登录后当仪表板获得焦点时，即使点击后台窗口有时仍会保持在前台。解决方法：在点击其他应用程序窗口前先点击仪表板
- 当仪表板打开时，即使失焦或最小化，仍会捕获键盘快捷键（例如 ctrl-r 重启快捷键）

## 4.3.2

{{< release-date date="2021-12-21" >}}

### 安全修复

- 修复了影响当前使用 Docker Desktop 4.3.0 或 4.3.1 版本的 [CVE-2021-45449](../security/_index.md#cve-2021-45449) 漏洞。

Docker Desktop 4.3.0 和 4.3.1 版本存在一个 bug，可能在用户登录期间在本地机器上记录敏感信息（访问令牌或密码）。  
此问题仅影响以下情况的用户：当前使用的是 Docker Desktop 4.3.0 或 4.3.1，并且曾在 4.3.0 或 4.3.1 版本中执行过登录操作。要获取这些数据，攻击者必须能够访问用户的本地文件。

### 升级内容

[docker scan v0.14.0](https://github.com/docker/scan-cli-plugin/releases/tag/v0.14.0)

### 安全性

**Log4j 2 CVE-2021-44228**：我们已更新 `docker scan` CLI 插件。  
此新版本的 `docker scan` 能够检测 [Log4j 2 CVE-2021-44228](https://nvd.nist.gov/vuln/detail/CVE-2021-44228) 和 [Log4j 2 CVE-2021-45046](https://nvd.nist.gov/vuln/detail/CVE-2021-45046)。

更多信息请参阅博客文章 [Apache Log4j 2 CVE-2021-44228](https://www.docker.com/blog/apache-log4j-2-cve-2021-44228/)。

## 4.3.1

{{< release-date date="2021-12-11" >}}

### 升级内容

[docker scan v0.11.0](https://github.com/docker/scan-cli-plugin/releases/tag/v0.11.0)

### 安全性

**Log4j 2 CVE-2021-44228**：我们已为您自动更新 `docker scan` CLI 插件。  
Docker Desktop 4.3.0 及更早版本中的旧版 `docker scan` 无法检测 [Log4j 2 CVE-2021-44228](https://nvd.nist.gov/vuln/detail/CVE-2021-44228)。

更多信息请参阅博客文章 [Apache Log4j 2 CVE-2021-44228](https://www.docker.com/blog/apache-log4j-2-cve-2021-44228/)。

## 4.3.0

{{< release-date date="2021-12-02" >}}

### 升级内容

- [Docker Engine v20.10.11](/manuals/engine/release-notes/20.10.md#201011)
- [containerd v1.4.12](https://github.com/containerd/containerd/releases/tag/v1.4.12)
- [Buildx 0.7.1](https://github.com/docker/buildx/releases/tag/v0.7.1)
- [Compose v2.2.1](https://github.com/docker/compose/releases/tag/v2.2.1)
- [Kubernetes 1.22.4](https://github.com/kubernetes/kubernetes/releases/tag/v1.22.4)
- [Docker Hub Tool v0.4.4](https://github.com/docker/hub-tool/releases/tag/v0.4.4)
- [Go 1.17.3](https://golang.org/doc/go1.17)

### Bug 修复与小幅改进

#### 全平台通用

- 新增：如果主机缺乏互联网连接，将显示自诊断警告。
- 修复：解决了用户无法通过卷管理界面中的“另存为”选项从卷保存文件的问题。修复了 [docker/for-win#12407](https://github.com/docker/for-win/issues/12407)。
- Docker Desktop 现在使用 cgroupv2。如果需要在容器中运行 `systemd`，请确保：
  - 您的 `systemd` 版本支持 cgroupv2（[至少为 `systemd` 247](https://github.com/systemd/systemd/issues/19760#issuecomment-851565075)）。建议将 `centos:7` 镜像升级至 `centos:8`。
  - 运行 `systemd` 的容器需添加以下选项：[`--privileged --cgroupns=host -v /sys/fs/cgroup:/sys/fs/cgroup:rw`](https://serverfault.com/questions/1053187/systemd-fails-to-run-in-a-docker-container-when-using-cgroupv2-cgroupns-priva)。

#### macOS 专用

- Apple 芯片上的 Docker Desktop 不再需要 Rosetta 2，[三个可选命令行工具](/manuals/desktop/troubleshoot-and-support/troubleshoot/known-issues.md)除外。

#### Windows 专用

- 修复：当用户主目录路径包含正则表达式中使用的特殊字符时，Docker Desktop 启动失败的问题。修复了 [docker/for-win#12374](https://github.com/docker/for-win/issues/12374)。

### 已知问题

在基于 Hyper-V 的机器上，Docker Desktop 仪表板错误地将容器内存使用量显示为零。  
可通过命令行使用 [`docker stats`](/reference/cli/docker/container/stats.md) 命令查看实际内存使用情况作为临时解决方案。参见 [docker/for-mac#6076](https://github.com/docker/for-mac/issues/6076)。

### 弃用功能

- 以下内部 DNS 名称已被弃用，将在未来版本中移除：`docker-for-desktop`、`docker-desktop`、`docker.for.mac.host.internal`、`docker.for.mac.localhost`、`docker.for.mac.gateway.internal`。请改用 `host.docker.internal`、`vm.docker.internal` 和 `gateway.docker.internal`。
- 移除：已从 Docker Desktop 中移除自定义 RBAC 规则，因其会向所有服务账户授予 `cluster-admin` 权限。修复了 [docker/for-mac/#4774](https://github.com/docker/for-mac/issues/4774)。

## 4.2.0

{{< release-date date="2021-11-09" >}}

### 新增功能

**暂停/恢复**：您现在可以在不活跃使用 Docker Desktop 时暂停会话，以节省机器的 CPU 资源。

- 实现 [Docker 公开路线图 #226](https://github.com/docker/roadmap/issues/226)

**软件更新**：所有 Docker 订阅用户（包括 Docker Personal 和 Docker Pro）现在均可关闭自动检查更新的选项。所有与更新相关的设置已移至**软件更新**部分。

- 实现 [Docker 公开路线图 #228](https://github.com/docker/roadmap/issues/228)

**窗口管理**：关闭并重新打开 Docker Desktop 时，仪表板窗口的大小和位置将保持不变。

### 升级内容

- [Docker Engine v20.10.10](/manuals/engine/release-notes/20.10.md#201010)
- [containerd v1.4.11](https://github.com/containerd/containerd/releases/tag/v1.4.11)
- [runc v1.0.2](https://github.com/opencontainers/runc/releases/tag/v1.0.2)
- [Go 1.17.2](https://golang.org/doc/go1.17)
- [Compose v2.1.1](https://github.com/docker/compose/releases/tag/v2.1.1)
- [docker-scan 0.9.0](https://github.com/docker/scan-cli-plugin/releases/tag/v0.9.0)

### Bug 修复与小幅改进

#### 全平台通用

- 改进：自诊断现在还会检查主机 IP 与 `docker networks` 之间是否存在重叠。
- 修复：修复了 Docker Desktop 仪表板上显示更新可用性的指示器位置问题。

#### macOS 专用

- 修复：解决了点击致命错误对话框中的**退出**按钮后 Docker Desktop 无响应的问题。
- 修复：解决了在主机目录上绑定挂载 `docker volume` 时偶尔出现的启动失败问题。如果存在，此修复还会自动移除用户手动添加到对应主机目录的 `DENY DELETE` ACL 条目。
- 修复：解决了升级时忽略 `Docker.qcow2` 文件而改用新的 `Docker.raw` 文件，导致容器和镜像消失的问题。注意：如果系统因之前的 bug 同时存在两个文件，将使用最近修改的文件，以避免再次丢失最近的容器和镜像。若要强制使用旧的 `Docker.qcow2`，请删除较新的 `Docker.raw` 文件。修复了 [docker/for-mac#5998](https://github.com/docker/for-mac/issues/5998)。
- 修复：解决了关闭期间子进程意外失败并触发意外致命错误弹窗的问题。修复了 [docker/for-mac#5834](https://github.com/docker/for-mac/issues/5834)。

#### Windows 专用

- 修复：解决了点击致命错误对话框中的**退出**按钮后 Docker Desktop 偶尔挂起的问题。
- 修复：解决了更新已下载但尚未应用时频繁弹出**下载更新**提示的问题 [docker/for-win#12188](https://github.com/docker/for-win/issues/12188)。
- 修复：解决了安装新更新时在应用关闭前终止进程的问题。
- 修复：现在即使组策略阻止用户启动必要服务（如 LanmanServer），也能成功安装 Docker Desktop [docker/for-win#12291](https://github.com/docker/for-win/issues/12291)。

## 4.1.1

{{< release-date date="2021-10-12" >}}

### Bug 修复与小幅改进

#### macOS 专用

> 从 4.1.0 升级时，Docker 菜单不会变为**更新并重启**，因此您只需等待下载完成（图标变化），然后选择**重启**即可。此 bug 已在 4.1.1 中修复，适用于未来的升级。

- 修复了升级过程中忽略 `Docker.qcow2` 文件而使用新的 `Docker.raw` 文件的问题，该问题曾导致容器和镜像消失。如果系统因之前的 bug 而同时存在这两个文件，则会使用最近修改的文件，以避免最近创建的容器和镜像再次消失。若要强制使用旧的 `Docker.qcow2` 文件，请删除较新的 `Docker.raw` 文件。修复了 [docker/for-mac#5998](https://github.com/docker/for-mac/issues/5998)。
- 修复了 Docker Desktop 仪表板中 **Settings** 按钮与 **Software update** 按钮之间的更新通知覆盖层有时不同步的问题。
- 修复了安装新下载的 Docker Desktop 更新的菜单项。当更新准备就绪时，**Restart** 选项将变为 **Update and restart**。

#### Windows 版本

- 修复了某些发行版（例如 Arch 或 Alpine）的 WSL 2 集成回归问题。修复了 [docker/for-win#12229](https://github.com/docker/for-win/issues/12229)。
- 修复了仪表板中 Settings 按钮与 Software update 按钮之间的更新通知覆盖层有时不同步的问题。

## 4.1.0

{{< release-date date="2021-09-30" >}}

### 新增功能

- **软件更新**：Settings 选项卡现在包含一个帮助管理 Docker Desktop 更新的新部分。**Software Updates** 部分会在有新更新时通知您，并允许您下载更新或查看新版本中包含的内容信息。
- **Compose V2**：您现在可以在 General 设置中指定是否使用 Docker Compose V2。
- **卷管理**：卷管理功能现已对所有订阅用户开放，包括 Docker Personal 用户。实现了 [Docker Public Roadmap#215](https://github.com/docker/roadmap/issues/215)。

### 升级组件

- [Compose V2](https://github.com/docker/compose/releases/tag/v2.0.0)
- [Buildx 0.6.3](https://github.com/docker/buildx/releases/tag/v0.6.3)
- [Kubernetes 1.21.5](https://github.com/kubernetes/kubernetes/releases/tag/v1.21.5)
- [Go 1.17.1](https://github.com/golang/go/releases/tag/go1.17.1)
- [Alpine 3.14](https://alpinelinux.org/posts/Alpine-3.14.0-released.html)
- [Qemu 6.1.0](https://wiki.qemu.org/ChangeLog/6.1)
- 基础发行版升级至 debian:bullseye

### Bug 修复与小幅改进

#### Windows 版本

- 修复了与反恶意软件触发相关的 bug，自诊断功能现在避免调用 `net.exe` 工具。
- 修复了自诊断中 WSL 2 Linux 虚拟机中的文件系统损坏问题。这可能由 [microsoft/WSL#5895](https://github.com/microsoft/WSL/issues/5895) 引起。
- 修复了 `SeSecurityPrivilege` 权限要求问题。参见 [docker/for-win#12037](https://github.com/docker/for-win/issues/12037)。
- 修复了 CLI 上下文切换与 UI 的同步问题。参见 [docker/for-win#11721](https://github.com/docker/for-win/issues/11721)。
- 在 `settings.json` 中添加了 `vpnKitMaxPortIdleTime` 键，以允许禁用或延长空闲网络连接超时时间。
- 修复了退出时的崩溃问题。参见 [docker/for-win#12128](https://github.com/docker/for-win/issues/12128)。
- 修复了 CLI 工具在 WSL 2 发行版中不可用的问题。
- 修复了因 panic.log 访问权限导致从 Linux 容器切换到 Windows 容器卡住的问题。参见 [for-win#11899](https://github.com/docker/for-win/issues/11899)。

### 已知问题

#### Windows 版本

在某些基于 WSL 的发行版（如 ArchWSL）上升级到 4.1.0 时，Docker Desktop 可能无法启动。参见 [docker/for-win#12229](https://github.com/docker/for-win/issues/12229)。

## 4.0.1

{{< release-date date="2021-09-13" >}}

### 升级组件

- [Compose V2 RC3](https://github.com/docker/compose/releases/tag/v2.0.0-rc.3)
  - Compose v2 现已托管在 github.com/docker/compose。
  - 修复了使用 `compose up --scale` 缩容时的 Go panic 问题。
  - 修复了在捕获退出代码时 `compose run --rm` 中的竞态条件。

### Bug 修复与小幅改进

#### 所有平台

- 修复了 Docker Desktop 仪表板中无法使用复制粘贴功能的问题。

#### Windows 版本

- 修复了 Docker Desktop 无法在 Hyper-V 引擎下正确启动的问题。参见 [docker/for-win#11963](https://github.com/docker/for-win/issues/11963)。

## 4.0.0

{{< release-date date="2021-08-31" >}}

### 新增功能

Docker 已[宣布](https://www.docker.com/blog/updating-product-subscriptions/)对订阅服务进行更新和扩展，以提高开发者和企业的生产力、协作能力和安全性。

更新后的 [Docker 订阅服务协议](https://www.docker.com/legal/docker-subscription-service-agreement) 对 **Docker Desktop** 的条款进行了调整：

- Docker Desktop **仍对小型企业免费**（员工少于 250 人 **且** 年收入低于 1000 万美元）、个人使用、教育用途以及非商业开源项目。
- 对于大型企业的专业用途，需要付费订阅（**Pro、Team 或 Business**），每月仅需 5 美元起。
- 这些条款的生效日期为 2021 年 8 月 31 日。对于需要使用付费订阅的用户，宽限期至 2022 年 1 月 31 日。
- Docker Pro 和 Docker Team 订阅现在**包含 Docker Desktop 的商业使用权限**。
- 原有的 Docker Free 订阅已更名为 **Docker Personal**。
- Docker Engine 及其他上游 **开源** Docker 或 Moby 项目**无任何变更**。

要了解这些变更如何影响您，请阅读 [常见问题解答](https://www.docker.com/pricing/faq)。  
更多信息请参见 [Docker 订阅概览](../subscription/_index.md)。

### 升级组件

- [Compose V2 RC2](https://github.com/docker/compose-cli/releases/tag/v2.0.0-rc.2)
  - 修复了 `compose down` 中项目名称大小写敏感的问题。参见 [docker/compose-cli#2023](https://github.com/docker/compose-cli/issues/2023)。
  - 修复了非标准化项目名称的问题。
  - 修复了部分引用时的端口合并问题。
- [Kubernetes 1.21.4](https://github.com/kubernetes/kubernetes/releases/tag/v1.21.4)

### Bug 修复与小幅改进

#### Mac 版本

- 修复了从 git URL 构建时 SSH 不可用的问题。修复了 [for-mac#5902](https://github.com/docker/for-mac/issues/5902)。

#### Windows 版本

- 修复了 CLI 工具在 WSL 2 发行版中不可用的问题。
