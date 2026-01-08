---
description: 查找适用于 Mac、Linux 和 Windows 的 Docker Desktop 发行说明。
keywords: Docker desktop, release notes, linux, mac, windows
title: Docker Desktop 发行说明
linkTitle: 发行说明
tags: [Release notes]
toc_max: 2
aliases:
- /docker-for-mac/release-notes/
- /docker-for-mac/edge-release-notes/
- /desktop/mac/release-notes/
- /docker-for-windows/edge-release-notes/
- /docker-for-windows/release-notes/
- /desktop/windows/release-notes/
- /desktop/linux/release-notes/
- /mackit/release-notes/
weight: 220
outputs: ["HTML", "markdown", "RSS"]
type: "desktop-release"
---
{{< rss-button feed="/desktop/release-notes/index.xml" text="Subscribe to Docker Desktop RSS feed" >}}

<!-- vale off -->

本页包含有关 Docker Desktop 新版本中的新功能、改进、已知问题和错误修复的信息。

为了确保质量控制，版本会逐步推出。如果最新版本尚未对您可用，请稍等片刻——更新通常会在发布日期后的一周内变得可用。

发布日期超过 6 个月的旧版 Docker Desktop 不再提供下载。以前的发行说明可在我们的[文档仓库](https://github.com/docker/docs/tree/main/content/manuals/desktop/previous-versions)中找到。

更多常见问题解答，请参见[常见问题解答](/manuals/desktop/troubleshoot-and-support/faqs/releases.md)。

## 4.55.0

{{< release-date date="2025-12-16" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.55.0" build_path="/213807/" >}}

### 更新

- [Docker Engine v29.1.3](https://docs.docker.com/engine/release-notes/29/#2913)
- [cagent v1.15.1](https://github.com/docker/cagent/releases/tag/v1.15.1)

### 错误修复和增强功能

#### 所有平台

- 修复了导致 Docker Desktop 在启动过程中卡住的问题。
- 改进了 `daemon.json` 无效时的错误消息。
- 修复了在长时间的 Ask Gordon 会话中每次击键都会出现的性能问题。
- 修复了当组织配置了注册表访问管理 (Registry Access Management) 以阻止 Docker Hub 时，kubeadm 模式下的 Kubernetes 无法启动的问题。

> [!IMPORTANT]
>
> Wasm 工作负载将在未来的 Docker Desktop 版本中被弃用并移除。

## 4.54.0

{{< release-date date="2025-12-04" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.54.0" build_path="/212467/" >}}

### 新增功能

- 在带有 WSL2 和 NVIDIA GPU 的 Windows 上，为 Docker Model Runner 添加了对 vLLM 的支持。

### 错误修复和增强功能

#### Mac

- 修复了 `/dev/shm` 权限不足导致容器无法写入的错误。修复 [docker/for-mac#7804](https://github.com/docker/for-mac/issues/7804)。

### 升级

- [Docker Buildx v0.30.1](https://github.com/docker/buildx/releases/tag/v0.30.1)
- [Docker Engine v29.1.2](https://docs.docker.com/engine/release-notes/29/#2912)
- [Runc v1.3.4](https://github.com/opencontainers/runc/releases/tag/v1.3.4)
- [Docker Model Runner CLI v1.0.2](https://github.com/docker/model-runner/releases/tag/cmd%2Fcli%2Fv1.0.2)

### 安全性

- 添加了安全补丁以解决 [CVE-2025-13743](https://www.cve.org/cverecord?id=CVE-2025-13743)，该问题导致 Docker Desktop 诊断包在日志输出中包含过期的 Hub PAT（个人访问令牌），原因是错误对象序列化。

## 4.53.0

{{< release-date date="2025-11-27" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.53.0" build_path="/211793/" >}}

### 错误修复和增强功能

#### 所有平台

- 修复了支持诊断工具无意中捕获过期的 Docker Hub 授权持有者令牌 (bearer tokens) 的问题。

### 安全性

- 添加了安全补丁以解决 CVE [2025-52565](https://github.com/opencontainers/runc/security/advisories/GHSA-9493-h29p-rfm2)、[2025-52881](https://github.com/opencontainers/runc/security/advisories/GHSA-cgrx-mc8f-2prm) 和 [2025-31133](https://github.com/opencontainers/runc/security/advisories/GHSA-qw9x-cqr3-wc7r)，这些 CVE 在使用[增强容器隔离](https://docs.docker.com/enterprise/security/hardened-desktop/enhanced-container-isolation)时存在。

## 4.52.0

{{< release-date date="2025-11-20" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.52.0" build_path="/210994/" >}}

### 新增功能

- 为 Docker Desktop 添加了新的端口绑定设置。管理员也可以通过 `admin-settings.json` 文件使用设置管理 (Settings Management) 来控制此功能。
- 添加了一个新的 Docker Model Runner 命令。使用 `docker model purge` 可以移除所有模型。

### 升级

- [Docker Engine v29.0.0](/manuals/engine/release-notes/29.md#2900)
- [Docker Model Runner v1.0.3](https://github.com/docker/model-runner/releases/tag/v1.0.3)
- [Docker Model Runner CLI v1.0.0](https://github.com/docker/model-runner/releases/tag/cmd%2Fcli%2Fv1.0.0)
- Docker MCP 插件 `v0.28.0`

### 错误修复和增强功能

#### 所有平台

- Docker MCP Toolkit 改进：
   - 支持 Amazon Q 客户端
   - 支持与 Docker Engine 进行 OAuth DCR（动态客户端注册）
   - 使用 CLI 创建 MCP 配置文件
- Docker Model Runner 改进：
   - 现在可以跳过 [Docker Model Runner 的 OpenAI API 端点](/manuals/ai/model-runner/api-reference.md#rest-api-examples) 的 `/engines` 前缀：`curl http://localhost:12434/v1/models`。
   - 现在可以跳过在 Docker Hub 上发布的模型的 `ai/` 前缀，使用 `docker model pull` 拉取。
   - 下载中断后现在可以恢复。

#### Windows

- 修复了 Kerberos/NTLM 代理登录的问题。

## 4.51.0

{{< release-date date="2025-11-13" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.51.0" build_path="/210443/" >}}

### 新增功能

- 现在可以从 **Kubernetes** 视图设置 Kubernetes 资源。此新视图还提供 Pod、服务和部署的实时显示。

### 升级

- [Docker Engine v28.5.2](/manuals/engine/release-notes/28.md#2852)
- Linux 内核 `v6.12.54`

### 错误修复和增强功能

#### 所有平台

- Kind 现在仅在本地不可用时才拉取所需的依赖镜像。

## 4.50.0

{{< release-date date="2025-11-06" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.50.0" build_path="/209931/" >}}

### 新增功能

- [动态 MCP](/manuals/ai/mcp-catalog-and-toolkit/dynamic-mcp.md)（实验性）现已在 Docker Desktop 中可用。
- 引入了新的欢迎调查以改进入门体验。新用户现在可以提供信息以帮助定制他们的 Docker Desktop 体验。

### 升级

- [Docker Compose v2.40.3](https://github.com/docker/compose/releases/tag/v2.40.3)
- [NVIDIA Container Toolkit v1.18.0](https://github.com/NVIDIA/nvidia-container-toolkit/releases/tag/v1.18.0)

### 错误修复和增强功能

#### 所有平台

- Docker Desktop 现在检测并尝试避免“Docker 子网”与使用 RFC1918 地址的物理网络发生冲突。例如，如果主机有一个与 `192.168.65.0/24` 重叠的非默认路由，则将自动选择替代网络。您仍然可以通过 Docker Desktop 设置和管理员设置覆盖此选择。
- Docker Desktop 不再将 Stargz Snapshotter 故障视为致命错误。如果发生故障，Docker Desktop 将继续运行而不使用 Stargz Snapshotter。
- Ask Gordon 不再显示用户提供的 URL 的镜像。
- Ask Gordon 现在在运行所有内置和用户添加的 MCP 工具之前请求确认。

## 4.49.0

{{< release-date date="2025-10-23" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.49.0" build_path="/208700/" >}}

> [!IMPORTANT]
>
> 对 Windows 10 21H2 (19044) 和 11 22H2 (22621) 的支持已结束。在下一个版本中，安装 Docker Desktop 将需要 Windows 10 22H2 (19045) 或 Windows 11 23H2 (22631)。

### 安全性

- 修复了 [CVE-2025-9164](https://www.cve.org/cverecord?id=CVE-2025-9164)，该问题导致 Windows 版 Docker Desktop 安装程序由于不安全的 DLL 搜索顺序而容易受到 DLL 劫持。安装程序在检查系统目录之前，会在用户的下载文件夹中搜索所需的 DLL，从而允许通过恶意 DLL 放置进行本地权限提升。

### 新增功能

- [cagent](/manuals/ai/cagent/_index.md) 现在可通过 Docker Desktop 获得。
- [Docker Debug](/reference/cli/docker/debug.md) 现在对所有用户免费。

### 升级

- [Docker Engine v28.5.1](/manuals/engine/release-notes/28.md#2851)
- [Docker Compose v2.40.2](https://github.com/docker/compose/releases/tag/v2.40.2)
- [NVIDIA Container Toolkit v1.17.9](https://github.com/NVIDIA/nvidia-container-toolkit/releases/tag/v1.17.9)
- Docker Debug `v0.0.45`

### 错误修复和增强功能

#### 所有平台

- 修复了 Docker Desktop 在等待用户输入新密码时使用过期代理密码的问题。
- 修复了使用 Docker Debug 时启动时显示的 'chown' 错误。
- 修复了导致某些转发的 UDP 端口挂起的错误。

#### Mac

- 修复了当另一个 Kubernetes 上下文处于活动状态时 Kubernetes 启动挂起的问题。修复 https://github.com/docker/for-mac/issues/7771。
- 如果 Rosetta 安装被取消或失败，Rosetta 将在 Docker Desktop 中被禁用。
- 在 macOS 上安装或更新 Docker Desktop 的最低操作系统版本现在是 macOS Sonoma（版本 14）或更高版本。

## 4.48.0

{{< release-date date="2025-10-09" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.48.0" build_path="/207573/" >}}

> [!IMPORTANT]
>
> 对 macOS 13 的支持已结束。在下一个版本中，安装 Docker Desktop 将需要 macOS 14。

### 新增功能

- 现在可以使用安装程序标志为 [macOS](/manuals/desktop/setup/install/mac-install.md#proxy-configuration) 和 [Windows](/manuals/desktop/setup/install/windows-install.md#proxy-configuration) 指定 PAC 文件和嵌入式 PAC 脚本。
- 管理员可以通过 [macOS 配置描述文件](/manuals/enterprise/security/enforce-sign-in/methods.md#macos-configuration-profiles-method-recommended) 设置代理设置。

### 升级

- [Docker Compose v2.40.0](https://github.com/docker/compose/releases/tag/v2.40.0)
- [Docker Buildx v0.29.1](https://github.com/docker/buildx/releases/tag/v0.29.1)
- [Docker Engine v28.5.1](https://docs.docker.com/engine/release-notes/28/#2851)
- Docker MCP 插件 `v0.22.0`
- [Docker Model CLI v0.1.42](https://github.com/docker/model-cli/releases/tag/v0.1.42)

### 错误修复和增强功能

#### 所有平台

- 修复了 Desktop 重启时 kind 集群状态有时会重置的问题。修复 [docker/for-mac#77445](https://github.com/docker/for-mac/issues/7745)。
- 移除了过时的 `mcp` 密钥，以符合最新的 VS Code MCP 服务器更改。
- 将凭证助手更新至 [v0.9.4](https://github.com/docker/docker-credential-helpers/releases/tag/v0.9.4)。
- 修复了 Docker Desktop 在等待用户输入新密码时使用过期代理密码的问题。
- 修复了在某些条件下导致 Docker Desktop 定期使用 Docker CLI 工具创建新进程的错误。修复 [docker/for-win#14944](https://github.com/docker/for-win/issues/14944)。
- 修复了通过 Compose 使用 Docker Model Runner 时模型未配置为嵌入的错误。要指定模型应配置为嵌入，必须显式添加 `--embeddings` 运行时标志，如 [Docker Compose 中的 AI 模型](https://docs.docker.com/ai/compose/models-and-compose/#model-configuration-options) 中所述。修复 [docker/model-runner#166](https://github.com/docker/model-runner/issues/166)。

#### Windows

- 移除了 `HKLM\SOFTWARE\Docker Inc.\Docker\1.0` 注册表项。请在路径中查找 `docker.exe` 以确定 Docker Desktop 的安装位置。
- 修复了在 IPv6 被禁用时 WSL 2 模式下的启动问题。

## 4.47.0

{{< release-date date="2025-09-25" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.47.0" build_path="/206054/" >}}

### 安全性

- 修复了 [CVE-2025-10657](https://www.cve.org/CVERecord?id=CVE-2025-10657)，该问题导致增强容器隔离的 [Docker Socket 命令限制](../enterprise/security/hardened-desktop/enhanced-container-isolation/config.md#command-restrictions) 功能仅在 Docker Desktop 4.46.0 中无法正常工作（其配置被忽略）。

### 新增功能

- 为 Docker 的 MCP 目录添加了动态 MCP 服务器发现和支持。
- 使用增强容器隔离时，管理员现在可以在挂载了 Docker 套接字的容器中阻止 `docker plugin` 和 `docker login` 命令。
- 添加了一个新的 Docker Model Runner 命令。使用 `docker model requests` 可以获取请求和响应。

### 升级

- [Docker Compose v2.39.4](https://github.com/docker/compose/releases/tag/v2.39.4)
- [Kubernetes v1.34.1](https://github.com/kubernetes/kubernetes/releases/tag/v1.34.1)
  - [CNI plugins v1.7.1](https://github.com/containernetworking/plugins/releases/tag/v1.7.1)
  - [cri-tools v1.33.0](https://github.com/kubernetes-sigs/cri-tools/releases/tag/v1.33.0)
  - [cri-dockerd v0.3.20](https://github.com/Mirantis/cri-dockerd/releases/tag/v0.3.20)
- Docker Debug `v0.0.44`

### 错误修复和增强功能

#### 所有平台

- 现在可以使用过滤器、排序和改进的搜索功能更轻松地搜索 MCP 服务器。
- Docker Debug 在调试环境变量设置为空值的容器时不再挂起。
- 增强了 Docker Model Runner，CLI 中具有丰富的响应渲染，Docker Desktop 仪表板中具有对话上下文，以及可恢复的下载。

#### Mac

- 移除了 `com.apple.security.cs.allow-dyld-environment-variables` 权限，该权限允许通过 `DYLD_INSERT_LIBRARIES` 环境变量将签名的任意动态库加载到 Docker Desktop 中。
- 修复了配置描述文件登录强制执行在某些客户环境中失效的回归问题。
- 修复了在写入本地内容存储（不带 `--push` 标志）时 `docker model package` 命令有时会挂起的错误。
- 修复了使用 `unless-stopped` 重启策略启动的容器永远不会重启的错误。修复 [docker/for-mac#7744](https://github.com/docker/for-mac/issues/7744)。

#### Windows

- 修复了 Windows 上 Docker MCP Toolkit 的 Goose MCP 客户端连接问题。
- 解决了在集成尝试失败后“跳过集成”WSL 发行版选项的问题。
- 修复了在写入本地内容存储（不带 `--push` 标志）时 `docker model package` 命令有时会挂起的错误。

## 4.46.0

{{< release-date date="2025-09-11" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.46.0" build_path="/204649/" >}}

### 新增功能

- 为 Docker MCP Toolkit 添加了新的学习中心演练以及其他入门改进。
- 管理员现在可以通过设置管理控制 [PAC 配置](/manuals/enterprise/security/hardened-desktop/settings-management/configure-json-file.md#proxy-settings)。
- 重新设计了更新体验，使理解和管理 Docker Desktop 及其组件的更新变得更加容易。

### 升级

- [Docker Buildx v0.28.0](https://github.com/docker/buildx/releases/tag/v0.28.0)
- [Docker Engine v28.4.0](https://docs.docker.com/engine/release-notes/28/#2840)

### 错误修复和增强功能

#### 所有平台

- 使用 Docker CLI 时，现在可以在 Docker 上下文元数据中存在键值对 (`"GODEBUG":"..."`) 时设置 `GODEBUG` 环境变量。这意味着 CLI 二进制文件中具有负序列号的证书默认受支持。
- 将 Docker 订阅服务协议链接更新为指向最新版本。

#### Mac

- 通过启用 `llama.cpp` 推理进程的沙箱化，提高了 Docker Model Runner 的安全性。
- 修复了导致 Docker Desktop 启动缓慢并看起来冻结的错误。修复 [docker/for-mac#7671](https://github.com/docker/for-mac/issues/7671)。

#### Windows

- 通过启用 `llama.cpp` 推理进程的沙箱化，提高了 Docker Model Runner 的安全性。

#### Linux

- 修复了 RHEL 卸载后序列中的路径问题。

## 4.45.0

{{< release-date date="2025-08-28" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.45.0" build_path="/203075/" >}}

### 新增功能

- [Docker Model Runner](/manuals/ai/model-runner/_index.md) 现已正式可用。

### 升级

- [Docker Compose v2.39.2](https://github.com/docker/compose/releases/tag/v2.39.2)
- [Docker Buildx v0.27.0](https://github.com/docker/buildx/releases/tag/v0.27.0)
- [Docker Scout CLI v1.18.3](https://github.com/docker/scout-cli/releases/tag/v1.18.3)
- [Docker Engine v28.3.3](https://docs.docker.com/engine/release-notes/28/#2833)

### 错误修复和增强功能

#### 所有平台

- 修复了在需要身份验证的代理后面上传诊断包时导致 `com.docker.diagnose` 崩溃的错误。
- `kind` 依赖镜像 `envoyproxy/envoy` 已从 v1.32.0 升级到 v1.32.6。如果您镜像 `kind` 镜像，请确保您的镜像已更新。

#### Mac

- 修复了笔记本电脑从睡眠状态唤醒后导致 Docker Desktop 崩溃的错误。修复 [docker/for-mac#7741](https://github.com/docker/for-mac/issues/7741)。
- 修复了 VM 有时会因 **The virtual machine stopped unexpectedly** 错误而失败的问题。
- 修复了在容器启动后连接到网络或从网络断开连接时会破坏端口映射的错误。修复 [docker/for-mac#7693](https://github.com/docker/for-mac/issues/7693)。

#### Windows

- 修复了当用户缺乏正确权限时，默认情况下无法将 CLI 插件部署到 `~/.docker/cli-plugins` 的错误。
- 修复了如果 `docker-desktop` 发行版不存在，则重新定位 WSL 数据发行版会失败的错误。
- 修复了 Docker Desktop 仪表板中 WSL 安装 URL 的拼写错误。
- 修复了某些 WSL 发行版无法集成的问题。修复 [docker/for-win#14686](https://github.com/docker/for-win/issues/14686)

## 4.44.3

{{< release-date date="2025-08-20" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.44.3" build_path="/202357/" >}}

### 安全性

- 修复了 [CVE-2025-9074](https://www.cve.org/CVERecord?id=CVE-2025-9074)，该问题导致在 Docker Desktop 上运行的恶意容器可以访问 Docker Engine 并启动其他容器，而无需挂载 Docker 套接字。这可能允许未经授权访问主机系统上的用户文件。增强容器隔离 (ECI) 无法缓解此漏洞。

### 错误修复和增强功能

- 修复了导致 Docker Offload 对话框阻止用户访问仪表板的错误。

## 4.44.2

{{< release-date date="2025-08-15" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.44.2" build_path="/202017/" >}}

### 错误修复和增强功能

 - 将 [Docker Offload](/manuals/offload/_index.md) 添加到 **Beta 功能** 设置选项卡，并包含对 [Docker Offload Beta](https://www.docker.com/products/docker-offload/) 的支持更新。

## 4.44.1

{{< release-date date="2025-08-13" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.44.1" build_path="/201842/" >}}

### 错误修复和增强功能

#### 所有平台

- 修复了 4.44.0 版本中发现的一个问题，该问题导致在 Desktop 设置管理中锁定 `vpnkit` CIDR 但未指定值时启动失败。

#### Windows

- 修复了从使用旧版 `version-pack-data` 目录结构的发行版升级后，卷和容器不可见的问题。
- 解决了 WSL 2 中一个罕见的问题，该问题导致 Docker CLI 因 **Proxy Authentication Required** 错误而失败。
- 修复了当用户对该目录缺乏执行权限时，CLI 插件未部署到 `~/.docker/cli-plugins` 的错误。

## 4.44.0

{{< release-date date="2025-08-07" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.44.0" build_path="/201307/" >}}

### 新增功能

- WSL 2 稳定性改进。
- 现在可以检查请求和响应，以帮助诊断 Docker Model Runner 中的模型相关问题。
- 添加了运行多个模型的功能，并在资源不足时收到警告。这避免了使用大型模型时 Docker Desktop 冻结。
- 为 MCP Toolkit 添加了新的 MCP 客户端：Gemini CLI、Goose。
- 为 `docker desktop enable model-runner` 引入了 `--gpu`（仅限 Windows）和 `--cors` 标志。
- 向 Docker Desktop CLI 添加了新的 `docker desktop kubernetes` 命令。
- 现在可以在 **设置** 中搜索特定的配置选项。
- Apple 虚拟化现在是默认的 VMM，以获得更好的性能，QEMU 虚拟化已被移除。请参阅[博客文章](https://www.docker.com/blog/docker-desktop-for-mac-qemu-virtualization-option-to-be-deprecated-in-90-days/)。
- DockerVMM 的性能和稳定性改进。

### 升级

- [Docker Compose v2.39.1](https://github.com/docker/compose/releases/tag/v2.39.1)
- [Docker Buildx v0.26.1](https://github.com/docker/buildx/releases/tag/v0.26.1)
- [Docker Engine v28.3.2](https://docs.docker.com/engine/release-notes/28/#2832)
- [Docker Scout CLI v1.18.2](https://github.com/docker/scout-cli/releases/tag/v1.18.2)
- [Docker Model CLI v0.1.36](https://github.com/docker/model-cli/releases/tag/v0.1.36)
- [Docker Desktop CLI v0.2.0](/manuals/desktop/features/desktop-cli.md)

### 安全性

我们注意到 [CVE-2025-23266](https://nvd.nist.gov/vuln/detail/CVE-2025-23266)，这是一个影响 CDI 模式下 NVIDIA Container Toolkit（最高至 1.17.7 版本）的关键漏洞。Docker Desktop 包含的 1.17.8 版本不受影响。但是，捆绑了较早工具包版本的旧版 Docker Desktop 如果手动启用了 CDI 模式，则可能受到影响。请升级到 Docker Desktop 4.44 或更高版本，以确保您使用的是已修补的版本。

### 错误修复和增强功能

#### 所有平台

- 修复了在启用 containerd 镜像存储时拉取具有 zstd 差异层的镜像的问题。
- 修复了使用增强容器隔离时，使用 `--restart` 标志启动的容器无法正确重启的错误。
- 改进了 [Kubernetes 自定义注册表镜像](/manuals/desktop/use-desktop/kubernetes.md#configuring-a-custom-image-registry-for-kubernetes-control-plane-images) 与增强容器隔离 (ECI) 之间的交互，因此在使用自定义注册表作为 Kubernetes 控制平面镜像时，不再需要手动更新 [ECI Docker Socket 镜像列表](/manuals/enterprise/security/hardened-desktop/enhanced-container-isolation/config.md)。
- 修复了当用户需要登录但当前已注销时，kind 模式下的 Docker Desktop Kubernetes 集群在重启 Docker Desktop 后无法启动的错误。
- 修复了启用[增强容器隔离](/enterprise/security/hardened-desktop/enhanced-container-isolation/) 时阻止将 MCP 秘密挂载到容器中的错误。
- 修复了在已指定 `--publish` 时阻止使用 `--publish-all` 的错误。
- 修复了导致 **镜像** 视图无限滚动的错误。修复 [docker/for-mac#7725](https://github.com/docker/for-mac/issues/7725)。
- 修复了在资源节省模式下 **卷** 选项卡为空白的错误。
- 更新了首次启动时的服务条款文本。
- 在解析新发布的 GGUF 格式方面更加健壮。

#### Mac

- 修复了在回收磁盘空间时 DockerVMM 上的磁盘损坏问题。
- 通过重新引入常规使用性能提升，修复了自 4.42.0 以来的回归问题。
- 移除了 QEMU 管理程序，并切换到 Apple 虚拟化作为新的默认值。请参阅[博客文章](https://www.docker.com/blog/docker-desktop-for-mac-qemu-virtualization-option-to-be-deprecated-in-90-days/)。
- 修复了阻止 Traefik 自动检测容器端口的错误。修复 [docker/for-mac#7693](https://github.com/docker/for-mac/issues/7693)。
- 修复了在容器启动后连接到网络或从网络断开连接时会破坏端口映射的错误。修复 [docker/for-mac#7693](https://github.com/docker/for-mac/issues/7693#issuecomment-3131427879)。
- 移除了阻止 `io_uring` 的 eBPF。要在容器中启用 `io_uring`，请使用 `--security-opt seccomp=unconfined`。修复 [docker/for-mac#7707](https://github.com/docker/for-mac/issues/7707)。
- Docker Model Runner 现在支持 GPT OSS 模型。

#### Windows

- 重新将 `docker-users` 组添加到命名管道安全描述符中。
- 修复了当当前用户没有 `SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall` 注册表项时安装程序崩溃的问题。
- 修复了 Docker Desktop 可能泄漏 `com.docker.build` 进程并无法启动的错误。修复 [docker/for-win#14840](https://github.com/docker/for-win/issues/14840)。
- 修复了在使用带有 `cgroups v1` 的 WSL 并启用增强容器隔离 (ECI) 时，阻止 kind 模式下的 Docker Desktop Kubernetes 启动的错误。
- 修复了 UI 中 WSL 安装 URL 的拼写错误。
- Docker Model Runner 现在支持 GPT OSS 模型

## 4.43.2

{{< release-date date="2025-07-15" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.43.2" build_path="/199162/" >}}

### 升级

- [Docker Compose v2.38.2](https://github.com/docker/compose/releases/tag/v2.38.2)
- [Docker Engine v28.3.2](https://docs.docker.com/engine/release-notes/28/#2832)
- Docker Model CLI v0.1.33

## 4.43.1

{{< release-date date="2025-07-04" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.43.1" build_path="/198352/" >}}

### 错误修复和增强功能

#### 所有平台

- 修复了当 Ask Gordon 响应包含 HTML 标签时导致 Docker Desktop UI 崩溃的问题。
- 修复了阻止扩展与其后端通信的问题。

## 4.43.0

{{< release-date date="2025-07-03" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.43.0" build_path="/198134/" >}}

### 新增功能

- [Compose Bridge](/manuals/compose/bridge/_index.md) 现已正式可用。

### 升级

- [Docker Buildx v0.25.0](https://github.com/docker/buildx/releases/tag/v0.25.0)
- [Docker Compose v2.38.1](https://github.com/docker/compose/releases/tag/v2.38.1)
- [Docker Engine v28.3.0](https://docs.docker.com/engine/release-notes/28/#2830)
- [NVIDIA Container Toolkit v1.17.8](https://github.com/NVIDIA/nvidia-container-toolkit/releases/tag/v1.17.8)

### 安全性

- 修复了 [CVE-2025-6587](https://www.cve.org/CVERecord?id=CVE-2025-6587)，该问题导致敏感的系统环境变量包含在 Docker Desktop 诊断日志中，可能导致机密泄露。

### 错误修复和增强功能

#### 所有平台

- 修复了 `docker start` 会为已在运行的容器丢弃端口映射的错误。
- 修复了当容器重新启动时，容器端口未在 GUI 上显示的错误。
- 修复了导致 Docker API `500 Internal Server Error for API route and version` 错误应用程序启动的错误。
- 设置中的 **应用并重启** 按钮现在标记为 **应用**。应用更改后的设置时不再重启 VM。
- 修复了如果在 `fsck` 期间关闭 Docker 会导致磁盘损坏的错误。
- 修复了在使用 `kind` Kubernetes 集群时导致 WSL2 中 `~/.kube/config` 不正确的错误。
- 如果 Docker Desktop 已被手动暂停，则向 Docker API / `docker` CLI 命令返回明确的错误。
- 修复了管理员和云设置中的未知密钥导致失败的问题。

#### Mac

- 移除了阻止 `io_uring` 的 `eBPF`。要在容器中启用 `io_uring`，请使用 `--security-opt seccomp=unconfined`。修复 [docker/for-mac#7707](https://github.com/docker/for-mac/issues/7707)。

#### Windows

- 修复了当当前用户没有 `SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall` 注册表项时 Docker Desktop 安装程序崩溃的问题。
- 修复了 Docker Desktop 可能泄漏 `com.docker.build` 进程并无法启动的错误。修复 [docker/for-win#14840](https://github.com/docker/for-win/issues/14840)

### 已知问题

#### 所有平台

- `docker buildx bake` 将不会构建具有顶级模型属性的 Compose 文件中的镜像。请改用 `docker compose build`。
- 包含 HTML 的 Gordon 响应可能导致 Desktop UI 永久损坏。作为解决方法，您可以删除 `persisted-state.json` 文件以重置 UI。该文件位于以下目录中：
  - Windows: `%APPDATA%\Docker Desktop\persisted-state.json`
  - Linux: `$XDG_CONFIG_HOME/Docker Desktop/persisted-state.json` 或 `~/.config/Docker Desktop/persisted-state.json`
  - Mac: `~/Library/Application Support/Docker Desktop/persisted-state.json`

#### Windows

- Docker Desktop 的“主机网络”功能与最新的 WSL 2 Linux 内核之间可能存在不兼容。如果您遇到此类问题，请将 WSL 2 降级到 2.5.7。

## 4.42.1

{{< release-date date="2025-06-18" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.42.1" build_path="/196648/" >}}

### 升级

- [Docker Compose v2.37.1](https://github.com/docker/compose/releases/tag/v2.37.1)

### 错误修复和增强功能

#### 所有平台

- 修复了当代理配置无效时 Docker 域名无法访问的问题。
- 修复了暴露端口时可能出现的死锁。
- 修复了可能导致 `docker run -p` 端口消失的竞争条件。

#### Mac

- 修复了在创建容器后立即检查时（例如使用脚本时）容器端口列表显示为空的错误。[docker/for-mac#7693](https://github.com/docker/for-mac/issues/7693)

#### Windows

- 禁用了 WSL 2 中的资源节省模式，以防止 `docker` CLI 命令在 WSL 2 发行版中挂起。[docker/for-win#14656](https://github.com/docker/for-win/issues/14656#issuecomment-2960285463)

## 4.42.0

{{< release-date date="2025-06-04" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.42.0" build_path="/195023/" >}}

### 新增功能

- 扩展了对 IPv6 支持的网络兼容性。
- Docker MCP Toolkit 现已原生集成到 Docker Desktop 中。
- Docker Model Runner 现已可用于在 Qualcomm/ARM GPU 上运行的 Windows 系统。
- 在模型视图中添加了 **日志** 选项卡，以便您可以实时查看推理引擎的输出。
- Gordon 现在集成了 MCP Toolkit，提供对 100 多个 MCP 服务器的访问。

### 升级

- [Docker Buildx v0.24.0](https://github.com/docker/buildx/releases/tag/v0.24.0)
- [Docker Engine v28.2.2](https://docs.docker.com/engine/release-notes/28/#2822)
- [Compose Bridge v0.0.20](https://github.com/docker/compose-bridge-binaries/releases/tag/v0.0.20)
- [Docker Compose v2.36.2](https://github.com/docker/compose/releases/tag/v2.36.2)
- [NVIDIA Container Toolkit v1.17.7](https://github.com/NVIDIA/nvidia-container-toolkit/releases/tag/v1.17.7)
- [Docker Scout CLI v1.18.0](https://github.com/docker/scout-cli/releases/tag/v1.18.0)

### 错误修复和增强功能

#### 所有平台

- Docker Desktop 现在接受具有负序列号的证书。
- 默认为容器重新启用 `seccomp`。使用 `docker run --security-opt seccomp=unconfined` 为容器禁用 seccomp。
- 修复了当内存不足时导致 Docker Desktop 挂起的错误。
- 在容器中阻止 `io_uring` 系统调用。
- 添加了直接从 Docker Hub 拉取模型的支持，简化了访问和使用模型的过程。
- Docker Desktop 现在在全新安装时将磁盘使用限制设置为物理磁盘的大小，并在 Mac 和 Linux 上重置为默认值。
- 设置 UI 中的最大磁盘大小现在与主机文件系统的总容量保持一致。
- **模型** 视图现在有一个 **Docker Hub** 选项卡，用于列出 `ai` 命名空间下的模型。
- 改进了当强制执行超过 10 个组织时的登录强制执行消息。
- 更改了 Docker Desktop 映射端口的方式，以完全支持 IPv6 端口。
- 修复了仪表板容器日志屏幕中的错误，该错误导致滚动条在鼠标接近时消失。
- 修复了团队订阅用户的[强制登录](/manuals/enterprise/security/enforce-sign-in/_index.md)。
- `llama.cpp` 服务器现在在 Model Runner 中支持流式传输和工具调用。
- 登录强制执行功能现已对所有订阅可用。

#### Mac

- 修复了使用 Docker VMM 时磁盘始终具有 64GB 最小使用限制的错误。
- 禁用了 Docker Desktop Linux VM 中的内存保护密钥机制。这导致 VS Code Dev Containers 无法正常工作。请参阅 [docker/for-mac#7667](https://github.com/docker/for-mac/issues/7667)。
- 修复了 Kubernetes 下的持久卷声明。修复 [docker/for-mac#7625](https://github.com/docker/for-mac/issues/7625)。
- 修复了使用 Apple virtualization.framework 时 VM 无法启动的错误。
- 安装或更新 Docker Desktop 的最低版本现在是 macOS Ventura 13.3。

#### Windows

- 修复了 Windows WSL 上增强容器隔离中的一个错误，即容器内具有硬链接的文件具有 `nobody:nogroup` 所有权。
- 修复了导致 Docker Desktop 崩溃的错误。与 [docker/for-win#14782](https://github.com/docker/for-win/issues/14782) 相关。
- 修复了在 WSL 2 启动时导致 **找不到网络名称** 错误的错误。修复 [docker/for-win#14714](https://github.com/docker/for-win/issues/14714)。
- 修复了在卸载时 Docker Desktop 不会删除 hosts 文件中的条目的问题。
- 修复了在某些系统语言中读取自动启动注册表项时的问题。修复 [docker/for-win#14731](https://github.com/docker/for-win/issues/14731)。
- 修复了 Docker Desktop 添加了无法识别的 /etc/wsl.conf `crossDistro` 选项的错误，这导致 WSL 2 记录错误。请参阅 [microsoft/WSL#4577](https://github.com/microsoft/WSL/issues/4577)
- 修复了如果另一个 WSL 发行版仍在使用 Linux cgroups v1，则 Docker Desktop 在 WSL 2.5.7 上无法启动的错误。修复 [docker/for-win#14801](https://github.com/docker/for-win/issues/14801)
- Windows Subsystem for Linux (WSL) 版本 2.1.5 现在是 Docker Desktop 应用程序正常运行所需的最低版本

### 已知问题

#### 所有平台

- 此版本包含 `docker port` 的回归，导致在使用 testcontainers-node 时出现“未找到主机 IP 的主机端口”错误。请参阅 [testcontainers/testcontainers-node#818](https://github.com/testcontainers/testcontainers-node/issues/818#issuecomment-2941575369)

#### Windows

- 运行 Wasm 容器会间歇性挂起。请参阅 [docker/for-mac#7666](https://github.com/docker/for-mac/issues/7666)。
- 在某些机器上，资源节省模式会导致其他 WSL 2 发行版冻结。解决方法是禁用资源节省模式。请参阅 [docker/for-win#14656](https://github.com/docker/for-win/issues/14656)。

## 4.41.2

{{< release-date date="2025-05-06" >}}

{{< desktop-install-v2 all=true win_arm_release="Beta" version="4.41.2" build_path="/191736/" >}}

### 错误修复和增强功能

#### 所有平台

- 修复了即使 Docker Model Runner 不受支持或未启用，GUI 中仍显示 **模型** 菜单的问题。

## 4.41.1

{{< release-date date="2025-04-30" >}}

{{< desktop-install-v2 all=true win_arm_release="Beta" version="4.41.1" build_path="/191279/" >}}

### 错误修复和增强功能

#### 所有平台

- 修复了当 `admin-settings.json` 文件中指定了代理配置时 Docker Desktop 无法启动的问题。

#### Windows

- 通过避免将 `llama.cpp` DLL 放置在系统 `PATH` 中包含的目录中，修复了与第三方工具（例如 Ollama）可能发生的冲突。

## 4.41.0

{{< release-date date="2025-04-28" >}}

{{< desktop-install-v2 all=true win_arm_release="Beta" version="4.41.0" build_path="/190950/" >}}

### 新增功能

- Docker Model Runner 现已可用于配备 NVIDIA GPU 的 x86 Windows 机器。
- 现在可以使用 Docker Model Runner 将模型[推送到 Docker Hub](/manuals/ai/model-runner.md#push-a-model-to-docker-hub)。
- 在支持 Docker Model Runner 的 Mac 和 Windows 版 Docker Desktop 中添加了对 Docker Model Runner 的模型管理和聊天界面的支持。用户现在可以通过新的专用界面查看、交互和管理本地 AI 模型。
- [Docker Compose](/manuals/ai/compose/models-and-compose.md) 和 Testcontainers [Java](https://java.testcontainers.org/modules/docker_model_runner/) 和 [Go](https://golang.testcontainers.org/modules/dockermodelrunner/) 现在支持 Docker Desktop。
- 在 [Microsoft 应用商店](https://apps.microsoft.com/detail/xp8cbj40xlbwkx?hl=en-GB&gl=GB) 中引入了 Docker Desktop。

### 升级

- [Docker Engine v28.1.1](https://docs.docker.com/engine/release-notes/28.1/#2811)
- [Docker Compose v2.35.1](https://github.com/docker/compose/releases/tag/v2.35.1)
- [Docker Buildx v0.23.0](https://github.com/docker/buildx/releases/tag/v0.23.0)
- [Docker Scout CLI v1.17.1](https://github.com/docker/scout-cli/releases/tag/v1.17.1)
- [Compose Bridge v0.0.19](https://github.com/docker/compose-bridge-binaries/releases/tag/v0.0.19)

### 安全性

- 修复了 [CVE-2025-3224](https://www.cve.org/CVERecord?id=CVE-2025-3224)，该问题允许有权访问用户机器的攻击者在 Docker Desktop 更新时执行权限提升。
- 修复了 [CVE-2025-4095](https://www.cve.org/CVERecord?id=CVE-2025-4095)，该问题导致在使用 MacOS 配置描述文件时未强制执行注册表访问管理 (RAM) 策略，允许用户从未经批准的注册表拉取镜像。
- 修复了 [CVE-2025-3911](https://www.cve.org/CVERecord?id=CVE-2025-3911)，该问题允许有权读取用户机器的攻击者从 Docker Desktop 日志文件中获取敏感信息，包括为运行中的容器配置的环境变量。

### 错误修复和增强功能

#### 所有平台

- 修复了 DockerVMM 中导致主机上打开过多文件句柄的错误。
- 修复了当 `admin-settings.json` 文件不包含可选的 `configurationFileVersion` 配置时 Docker Desktop 无法启动的问题。
- 修复了导致传出 UDP 连接被过早关闭的错误。
- 通过高级搜索功能和容器级过滤增强了日志读取体验，从而实现更快的调试和故障排除。
- 改进了下载注册表访问管理配置时的错误消息。
- 如果 Docker 无法绑定 ICMPv4 套接字，它现在会记录错误并继续运行而不是退出。
- 在 Docker Desktop Linux VM 中启用了内存保护密钥机制，允许像 Oracle 数据库镜像这样的容器正确运行。
- 修复了在 Mac、Windows Hyper-V 或 Linux 上启用[增强容器隔离](/manuals/enterprise/security/hardened-desktop/enhanced-container-isolation/_index.md) 时容器访问 `/proc/sys/kernel/shm*` sysctl 的问题。
- 添加了内核模块 `nft_fib_inet`，这是在 Linux 容器中运行 firewalld 所必需的。
- MacOS QEMU 虚拟化选项将于 2025 年 7 月 14 日弃用。

#### Mac

- 修复了导致高 CPU 使用率的错误。修复 [docker/for-mac#7643](https://github.com/docker/for-mac/issues/7643)。
- 修复了在 M3 Mac 上使用 Rosetta 进行多架构构建的问题。
- 修复了当 `/Library/Application Support/com.docker.docker/` 目录不存在时导致无法应用 RAM 策略限制的问题。

#### Windows

- Windows `.exe` 安装程序现在包含改进的锁定文件处理。修复 [docker/for-win#14299](https://github.com/docker/for-win/issues/14299) 和 [docker/for-win#14316](https://github.com/docker/for-win/issues/14316)。
- 修复了安装后 `Docker Desktop.exe` 不显示版本信息的问题。修复 [docker/for-win#14703](https://github.com/docker/for-win/issues/14703)。

### 已知问题

#### 所有平台

- 如果您使用 `desktop.plist`（在 macOS 上）或注册表项（在 Windows 上）强制执行登录，并且还有 `registry.json`，则如果用户属于 `desktop.plist`/注册表项中列出的组织，但不属于 `registry.json` 中指定的任何组织，登录将失败。要解决此问题，请删除 `registry.json` 文件。

#### Windows

- 如果在 Windows 注册表项 `allowedOrgs` 中使用空格分隔的格式指定了多个组织，登录将失败，用户将被注销。作为解决方法，请在注册表项值中将每个组织单独列在一行上。

## 4.40.0

{{< release-date date="2025-03-31" >}}

{{< desktop-install-v2 all=true win_arm_release="Beta" version="4.40.0" build_path="/187762/" >}}

### 新增功能

- 现在可以直接在 Docker Desktop 中使用 [Docker Model Runner (Beta)](/manuals/ai/model-runner.md) 从 Docker Hub 拉取、运行和管理 AI 模型。目前适用于配备 Apple Silicon 的 Docker Desktop for Mac。

### 升级

- [Docker Buildx v0.22.0](https://github.com/docker/buildx/releases/tag/v0.22.0)
- [Docker Compose v2.34.0](https://github.com/docker/compose/releases/tag/v2.34.0)
- [Docker Engine v28.0.4](https://docs.docker.com/engine/release-notes/28/#2804)
- [Docker Scout CLI v1.17.0](https://github.com/docker/scout-cli/releases/tag/v1.17.0)
- [compose-bridge v0.0.18](https://github.com/docker/compose-bridge-binaries/releases/tag/v0.0.18)
- [NVIDIA Container Toolkit v1.17.5](https://github.com/NVIDIA/nvidia-container-toolkit/releases/tag/v1.17.5)

### 错误修复和增强功能

#### 所有平台

- 修复了导致 `docker-proxy` 停止将 UDP 数据报转发到容器的错误。
- 修复了导致 docker-proxy 过早关闭与容器的 UDP 连接并导致源地址不必要更改的错误。
- 修复了在某些情况下阻止 Docker Desktop Kubernetes 启动的竞争条件。
- 改进了 ECI 在配置了代理的环境中从存储库收集镜像摘要信息的方式。
- 用户现在可以在使用新的 `--timeout` 标志生成私有扩展市场时指定超时。
- 移除了 Mac 和 Linux 上未使用的内部辅助工具 `com.docker.admin`。

#### Mac

- 修复了 Docker VMM 中陈旧的目录缓存导致无法检测移动或新文件的问题。
- 当 Time Machine 实用程序受限时，移除了继续/重启弹出窗口。
- Docker Desktop 现在允许通过 `docker run -v /path/to/unix.sock:/unix.sock` 将 Unix 域套接字与容器共享。必须在绑定挂载中指定完整的套接字路径。请参阅 [for-mac/#483](https://github.com/docker/for-mac/issues/483)。
- 修复了当为指定了端口的服务器存储令牌时，`docker-credential-osxkeychain` 和 `docker-credential-desktop` 返回格式错误的 URI 的错误。

#### Windows

- Windows MSI 和 `.exe` 安装程序现在在使用 GUI 安装时默认禁用 Windows 容器。
- 改进了 WSL2 上的端口映射吞吐量。

### 已知问题

#### Windows

- 在显示特权辅助程序错误消息时切换到 Windows 容器可能会导致状态不一致。作为解决方法，请退出 Docker Desktop，在 `settings-store.json` 中将 `UseWindowsContainers` 更改为 `false`，然后重新启动 Docker Desktop。
- 安装后，`Docker Desktop.exe` 不包含最新的版本信息。

## 4.39.0

{{< release-date date="2025-03-05" >}}

{{< desktop-install-v2 all=true win_arm_release="Beta" version="4.39.0" build_path="/184744/" >}}

### 新增功能

- [Docker Desktop CLI](/manuals/desktop/features/desktop-cli.md) 现已正式可用。您现在还可以使用新的 `docker desktop logs` 命令打印日志。
- Docker Desktop 现在支持在 [`docker load`](/reference/cli/docker/image/load.md) 和 [`docker save`](/reference/cli/docker/image/save.md) 上使用 `--platform` 标志。这有助于您导入和导出多平台镜像的子集。

### 升级

- [Docker Compose v2.33.1](https://github.com/docker/compose/releases/tag/v2.33.1)
- [Docker Buildx v0.21.1](https://github.com/docker/buildx/releases/tag/v0.21.1)
- [Kubernetes v1.32.2](https://github.com/kubernetes/kubernetes/releases/tag/v1.32.2)
- [Docker Engine v28.0.1](https://docs.docker.com/engine/release-notes/28/#2801)
- [Docker Scout CLI v1.16.3](https://github.com/docker/scout-cli/releases/tag/v1.16.3)

### 安全性

- 修复了 [CVE-2025-1696](https://www.cve.org/CVERecord?id=CVE-2025-1696)，该问题可能以明文形式在日志文件中泄露代理身份验证凭据。

### 错误修复和增强功能

#### 所有平台

- Ask Gordon 现在提供关于 Docker 镜像、容器和卷的更深入上下文，提供更快的支持，并通过 Docker Desktop 和 Docker CLI 启用更多用户操作。
- 通过在 `docker history` 中支持用户选择特定平台，支持多平台镜像。
- 修复了导致 CLI 和 Docker Desktop 以外的客户端在存在具有端口映射的容器时延迟 3 秒的问题。请参阅 [docker/for-mac#7575](https://github.com/docker/for-mac/issues/7575)
- 修复了 ECI Docker 套接字权限中的错误，该错误有时会阻止在允许的镜像或源自允许镜像的镜像的容器上挂载 Docker 套接字。
- 修复了在引擎重启后 Docker Desktop 无法立即再次进入资源节省模式的错误。
- 修复了由于过期的 PKI 证书导致 Kubernetes 集群停止工作的问题。

#### Mac

- 将 Linux 内核降级到 `v6.10.14`，以修复 OpenJDK 中的一个错误，该错误导致 Java 容器因 cgroups 控制器错误识别而终止。请参阅 [docker/for-mac#7573](https://github.com/docker/for-mac/issues/7573)。
- 在根挂载命名空间中添加了 `/usr/share/misc/usb.ids` 以修复 `usbip`。
- 修复了使用 Docker VMM 时 CPU 限制显示上限为 8 的问题。
- 修复了启动时挂起且 `com.docker.backend` 进程消耗 100% CPU 的问题。请参阅 [docker/for-mac#6951](https://github.com/docker/for-mac/issues/6951)。
- 修复了在 M4 Macbook Pro 上运行的所有 Java 程序都会发出 SIGILL 错误的错误。请参阅 [docker/for-mac#7583](https://github.com/docker/for-mac/issues/7583)。
- 阻止在 macOS 15.4 beta 1 上启动，因为启动 VM 会导致主机崩溃，请参阅 https://developer.apple.com/documentation/macos-release-notes/macos-15_4-release-notes#Virtual-Machines。
- 修复了 myIPAddress PAC 文件函数从错误的接口检索主机 IP 的问题，导致代理选择不正确。

#### Windows

- 修复了在 WSL 中运行应用程序时 `docker compose log` 无法流式传输的错误。
- 当 Docker Desktop 使用 WSL 时，修复了 Paketo buildpack 在增强容器隔离下失败的错误。
- 修复了如果安装了 WSL 版本 1 发行版，WSL 2 集成会失败的错误。
- 修复了在启用 WSL 发行版时导致某些 CLI 插件更新失败的错误。
- 修复了当使用 PAC 文件进行代理配置时，Docker Desktop 登录会挂起，导致 UI 模糊并阻止访问的错误。

#### Linux

- 设置中的 **软件更新** 页面现在指向最新的可用版本。

## 4.38.0

{{< release-date date="2025-01-30" >}}

### 新增功能

- 通过 PKG 安装程序安装 Docker Desktop 现已正式可用。
- 通过配置描述文件强制执行登录现已正式可用。
- Docker Compose、Docker Scout、Docker CLI 和 Ask Gordon 现在可以独立于 Docker Desktop 更新，无需完全重启（Beta）。
- 新的 [`update` 命令](/reference/cli/docker/desktop/update.md) 已添加到 Docker Desktop CLI（仅限 Mac）。
- [Bake](/manuals//build/bake/_index.md) 现已正式可用，支持授权和可组合属性。
- 您现在可以在 Docker Desktop 中创建[多节点 Kubernetes 集群](/manuals/desktop/settings-and-maintenance/settings.md#kubernetes)。
- [Ask Gordon](/manuals/ai/gordon/_index.md) 更广泛可用。它仍处于 Beta 阶段。

### 升级

- [containerd v1.7.24](https://github.com/containerd/containerd/releases/tag/v1.7.24)
- [Docker Buildx v0.20.1](https://github.com/docker/buildx/releases/tag/v0.20.1)
- [Docker Compose v2.32.4](https://github.com/docker/compose/releases/tag/v2.32.4)
- [Docker Engine v27.5.1](https://docs.docker.com/engine/release-notes/27/#2751)
- [Docker Scout CLI v1.16.1](https://github.com/docker/scout-cli/releases/tag/v1.16.1)
- [Runc v1.2.2](https://github.com/opencontainers/runc/releases/tag/v1.2.2)
- [NVIDIA Container Toolkit v1.17.4](https://github.com/NVIDIA/nvidia-container-toolkit/releases/tag/v1.17.4)
- [Kubernetes v1.31.4](https://github.com/kubernetes/kubernetes/releases/tag/v1.31.4)
- Docker Debug `v0.0.38`

### 错误修复和增强功能

#### 所有平台

- 修复了通过 `docker login` Web 流生成的访问令牌无法被 Docker Desktop 刷新的错误。
- 修复了在启用[增强容器隔离](/manuals/enterprise/security/hardened-desktop/enhanced-container-isolation/_index.md) 时，使用 `curl` 通过 Docker API 创建容器失败的错误。
- 修复了在刷新期过后 RAM 策略未刷新的错误。
- 修复了增强容器隔离中的一个错误，该错误发生在将 Docker 套接字挂载到容器中，然后在该容器内使用绑定挂载创建 Docker 容器时。
- 修复了导致 GUI 和 CLI 之间存在差异的问题，前者强制在端口映射中使用 `0.0.0.0` HostIP。这导致通过 Engine 的 `ip` 标志或通过桥接选项 `com.docker.network.bridge.host_binding_ipv4` 配置的默认绑定 IP 未被使用。
- 修复了 `pac` 设置在 `admin-settings.json` 中被忽略的错误。
- 构建 UI：
  - 导入构建时添加了进度状态。
  - 修复了用户无法导入构建的错误。
  - 修复了某些使用 SSH 端点的构建器未被跳过的错误。

#### Mac

- 修复了 Docker VMM 中从非根卷的绑定挂载无法按预期工作的错误。
- 修复了在没有 IPv6 的系统上导致启动失败的问题。修复 [docker/for-mac#14298](https://github.com/docker/for-win/issues/14298)。
- 修复了导致 Docker Desktop 挂起的错误。请参阅 [docker/for-mac#7493](https://github.com/docker/for-mac/issues/7493#issuecomment-2568594070)。
- 修复了如果缺少设置文件，卸载程序会失败的问题。
- 修复了通过 Workspace One 部署的配置描述文件被忽略的错误。

#### Windows

- Docker Desktop 安装程序现在在启动时会显示 UAC 提示。
- 修复了当使用旧版 WSL 版本创建的数据磁盘与其他 WSL 发行版共享相同标识符时，Docker Desktop 无法启动的问题。
- 当 WSL 集成设置更改时，Docker Desktop 现在会重新启动。这确保了在使用增强容器隔离时正确设置 WSL 集成。

#### Linux

- 添加了对 gvisor 网络的支持。具有不兼容版本 qemu (8.x) 的用户将保留在 qemu 网络上，其他用户将自动迁移。

### 弃用

#### 所有平台

- 弃用了 `com.docker.diagnose check|check-dot|check-hypervisordetect-host-hypervisor`。

## 4.37.2

{{< release-date date="2025-01-09" >}}

### 错误修复和增强功能

#### Mac

- 防止了导致 Docker Desktop 无法将 `com.docker.vmnetd` 或 `com.docker.socket` 更新到较新版本的错误。

### 已知问题

#### Mac

- 如果您看到关于 `com.docker.vmnetd` 或 `com.docker.socket` 的安全弹窗，请按照 [docker/for-mac#7527](https://github.com/docker/for-mac/issues/7527) 中记录的步骤操作。

## 4.37.1

{{< release-date date="2024-12-17" >}}

### 错误修复和增强功能

#### 所有平台

- 修复了导致 Docker Hub 中的 AI 目录在 Docker Desktop 中不可用的问题。
- 修复了在使用[增强容器隔离](/manuals/enterprise/security/hardened-desktop/enhanced-container-isolation/_index.md) 时，Docker Desktop 因 `index out of range [0] with length 0` 而发生 panic 的问题。

### 已知问题

#### Mac

- 如果您看到关于 `com.docker.vmnetd` 或 `com.docker.socket` 的安全弹窗，请按照 [docker/for-mac#7527](https://github.com/docker/for-mac/issues/7527) 中记录的步骤操作。

## 4.37.0

{{< release-date date="2024-12-12" >}}

### 新增功能

- 您现在可以直接从[命令行](/manuals/desktop/features/desktop-cli.md)（Beta）执行启动、停止、重启和检查 Docker Desktop 状态等关键操作。
- Docker Hub 中的 AI 目录现在可以直接通过 Docker Desktop 访问。

### 升级

- [Docker Buildx v0.19.2](https://github.com/docker/buildx/releases/tag/v0.19.2)
- [Docker Compose v2.31.0](https://github.com/docker/compose/releases/tag/v2.31.0)
- [Docker Engine v27.4.0](https://docs.docker.com/engine/release-notes/27/#2740)
- [Docker Scout CLI v1.15.1](https://github.com/docker/scout-cli/releases/tag/v1.15.1)
- [NVIDIA Container Toolkit v1.17.2](https://github.com/NVIDIA/nvidia-container-toolkit/releases/tag/v1.17.2)

### 错误修复和增强功能

#### 所有平台

- 新安装中 Docker Engine 的默认磁盘使用限制现在为 1TB。
- 修复了容器无法建立环回 `AF_VSOCK` 连接的问题。
- 修复了重置默认设置也会重置 CLI 上下文的错误。
- 修复了在资源节省模式下（仅限使用 WSL2 后端的 Windows）或在切换引擎后（macOS），重启引擎后 Docker Desktop 仪表板与 Docker 守护进程失去同步的错误。
- 修复了在资源节省模式下重启引擎后，资源节省模式无法重新启动的错误。
- 构建 UI：
  - 修复了某些构建找不到源文件的错误。
  - 修复了错误日志未在 **源** 选项卡中显示的错误。
  - 修复了用户必须滚动到 **源** 选项卡底部才能看到错误日志的错误。
  - 修复了 **日志** 选项卡中时间戳损坏的错误。

#### Mac

- 修复了在使用 `sudo` 两次运行卸载程序二进制文件时，某些用户目录以 root 权限创建的错误。

#### Windows

- 添加了对在 WSL 2 单发行版模式下使用 WSL 2 版本 2.3.24 及更高版本的 ARM 上 Windows 的支持。
- 修复了 Docker Desktop 无法启动的问题。修复 [docker/for-win#14453](https://github.com/docker/for-win/issues/14453)

### 已知问题

#### 所有平台

- 如果启用了 **注册表访问管理器**，Kubernetes 集群可能无法启动。作为解决方法，请将 `registry.k8s.io` 和 `<geo>-docker.pkg.dev` 添加到 **注册表访问管理** 策略中。

#### Mac

- 如果您看到关于 `com.docker.vmnetd` 或 `com.docker.socket` 的安全弹窗，请按照 [docker/for-mac#7527](https://github.com/docker/for-mac/issues/7527) 中记录的步骤操作。

### 弃用

#### Mac

- Apple Silicon 上的 QEMU（旧版）作为 VMM 将在未来的版本中被移除。建议您切换到 Apple 虚拟化框架以提高性能和稳定性。如果您遇到问题，[联系 Docker 支持](https://www.docker.com/support/) 或[提交 GitHub 问题](https://github.com/docker/for-mac/issues)。
- osxfs（旧版）将在未来的版本中被移除。建议您切换到 VirtioFS 以提高性能。如果您遇到问题，[联系 Docker 支持](https://www.docker.com/support/) 或[提交 GitHub 问题](https://github.com/docker/for-mac/issues)。

## 4.36.1

{{< release-date date="2025-01-09" >}}

### 错误修复和增强功能

#### Mac

- 防止了导致 Docker Desktop 无法将 `com.docker.vmnetd` 或 `com.docker.socket` 更新到较新版本的错误。

### 已知问题

#### Mac

- 如果您看到关于 `com.docker.vmnetd` 或 `com.docker.socket` 的安全弹窗，请按照 [docker/for-mac#7527](https://github.com/docker/for-mac/issues/7527) 中记录的步骤操作。

## 4.36.0

{{< release-date date="2024-11-18" >}}

### 新增功能

- 使用 WSL2 引擎的 Windows 上现有 Docker Desktop 安装现在会自动迁移到统一的单发行版架构，以增强一致性和性能。
- 管理员现在可以：
  - 使用 macOS [配置描述文件](/manuals/enterprise/security/enforce-sign-in/methods.md#configuration-profiles-method-mac-only) 强制执行登录（早期访问）。
  - 一次为多个组织强制执行登录（早期访问）。
  - 使用 [PKG 安装程序](/manuals/enterprise/enterprise-deployment/pkg-install-and-configure.md) 批量部署 Docker Desktop for Mac（早期访问）。
  - 使用 Desktop 设置管理通过 admin.docker.com 管理和强制执行默认值（早期访问）。
- 增强容器隔离 (ECI) 已得到改进：
  - 允许管理员[关闭 Docker 套接字挂载限制](/manuals/enterprise/security/hardened-desktop/enhanced-container-isolation/config.md#allowing-all-containers-to-mount-the-docker-socket)。
  - 在使用 [`allowedDerivedImages` 设置](/manuals/enterprise/security/hardened-desktop/enhanced-container-isolation/config.md#docker-socket-mount-permissions-for-derived-images) 时支持通配符标签。

### 升级

- [Docker Buildx v0.18.0](https://github.com/docker/buildx/releases/tag/v0.18.0)
- [Docker Compose v2.30.3](https://github.com/docker/compose/releases/tag/v2.30.3)
- [Kubernetes v1.30.5](https://github.com/kubernetes/kubernetes/releases/tag/v1.30.5)
- [NVIDIA Container Toolkit v1.17.0](https://github.com/NVIDIA/nvidia-container-toolkit/releases/tag/v1.17.0)
- [Docker Scout CLI v1.15.0](https://github.com/docker/scout-cli/releases/tag/v1.15.0)
- Docker Init v1.4.0
- Linux 内核 `v6.10.13`

### 错误修复和增强功能

#### 所有平台

- 修复了 `docker events` 命令在流式传输事件后不会终止的错误。
- Docker Init：改进了不使用 Docker Compose 的 PHP 应用程序的 Dockerfile 缓存。
- 同步文件共享现在尊重 `admin-settings.json` 中的 `filesharingAllowedDirectories` 设置。
- 修复了如果 Docker Desktop 配置为使用代理，由于在获取身份验证令牌时内部超时而导致启动失败的问题。
- 添加了恢复横幅，以便在下载失败时重试更新。
- 修复了如果 `umask` 设置为 `577` 会导致 `rpmbuild` 失败的问题。修复 [docker/for-mac#6511](https://github.com/docker/for-mac/issues/6511)。
- 修复了限制使用 `--network=host` 的容器只能打开 18 个主机端口的错误。
- 修复了非根容器的绑定挂载所有权。修复 [docker/for-mac#6243](https://github.com/docker/for-mac/issues/6243)。
- Docker Desktop 在手动暂停后不会自动取消暂停。系统将保持暂停状态，直到您手动恢复 Docker 引擎。这修复了其他软件在后台运行 CLI 命令时意外触发恢复的错误。修复 [for-mac/#6908](https://github.com/docker/for-mac/issues/6908)
- 构建 UI：
  - **源** 选项卡现在支持多个源文件。
  - **信息** 选项卡中的镜像依赖项链接现在支持其他知名注册表，如 GitHub、Google 和 GitLab。
  - 如果仅选择了云构建，则禁用 **删除** 按钮。
  - 修复了用户无法删除构建的问题。
  - 修复了缺少事件和链接的格式错误的 Jaeger 迹线。
  - 使用云驱动程序构建时，修复了缺少导出属性的问题。

#### Mac

- 修复了 Docker VMM 中的一个错误，该错误阻止 MySQL 和其他数据库容器启动。修复来自 [docker/for-mac#7464](https://github.com/docker/for-mac/issues/7464) 的报告。
- Docker VMM 的最低内存要求现在会自动调整，改善了用户体验并解决了 [docker/for-mac#7464](https://github.com/docker/for-mac/issues/7464) 和 [docker/for-mac#7482](https://github.com/docker/for-mac/issues/7482) 的报告。
- 修复了高级选项 **允许特权端口映射** 无法按预期工作的错误。修复 [docker/for-mac#7460](https://github.com/docker/for-mac/issues/7460)。
- Docker Desktop 现在可以在安装向导和设置屏幕中自动为 zsh、bash 和 fish 配置 shell 补全脚本。
- 修复了如果 Docker Desktop 由非管理员用户安装或当前用户以前是管理员，则应用内更新会失败的错误。修复 [for-mac/#7403](https://github.com/docker/for-mac/issues/7403) 和 [for-mac/#6920](https://github.com/docker/for-mac/issues/6920)

#### Windows

- 修复了阻止绑定 UDP 端口 53 的错误。
- 修复了在启动时 Windows 守护程序选项被覆盖的错误。

## 4.35.2

{{< release-date date="2025-01-09" >}}


### 错误修复和增强功能

#### Mac

- 防止了导致 Docker Desktop 无法将 `com.docker.vmnetd` 或 `com.docker.socket` 更新到较新版本的错误。

### 已知问题

#### Mac

- 如果您看到关于 `com.docker.vmnetd` 或 `com.docker.socket` 的安全弹窗，请按照 [docker/for-mac#7527](https://github.com/docker/for-mac/issues/7527) 中记录的步骤操作。

## 4.35.1

{{< release-date date="2024-10-30" >}}

#### 所有平台

- 修复了 Docker Desktop 会错误地绑定到端口 `8888` 的错误。修复 [docker/for-win#14389](https://github.com/docker/for-win/issues/14389) 和 [docker/for-mac#7468](https://github.com/docker/for-mac/issues/7468)

## 4.35.0

{{< release-date date="2024-10-24" >}}

### 新增功能

- 对 [Red Hat Enterprise Linux 上的 Docker Desktop](/manuals/desktop/setup/install/linux/rhd.md) 的支持现已正式可用。
- 卷备份和共享现已正式可用，可在 **卷** 视图中找到。
- 使用系统 shell 在 Docker Desktop 中进行终端支持现已正式可用。
- Docker VMM 的 Beta 版发布 - macOS 上 Apple 虚拟化框架的更高性能替代方案（需要 Apple Silicon 和 macOS 12.5 或更高版本）。

### 升级

- [containerd v1.7.21](https://github.com/containerd/containerd/releases/tag/v1.7.21)
- [Docker Buildx v0.17.1](https://github.com/docker/buildx/releases/tag/v0.17.1)
- [Docker Compose v2.29.7](https://github.com/docker/compose/releases/tag/v2.29.7)
- [Docker Engine v27.3.1](https://docs.docker.com/engine/release-notes/27/#2731)
- [Docker Scout CLI v1.14.0](https://github.com/docker/scout-cli/releases/tag/v1.14.0)
- Docker Debug `v0.0.37`
- Linux 内核 `v6.10.9`

### 错误修复和增强功能

#### 所有平台

- 修复了 `daemon.json` 中的代理设置会覆盖 Docker Desktop 设置中设置的代理的错误。
- 修复了某些 Docker 子网范围无法使用的错误。
- 移除了 [docker-index](https://github.com/docker/index-cli-plugin)，因为它现在已被弃用，您可以改用 `docker scout cves fs://<path to binary>`。
- 修复了镜像无法按标签排序或过滤的错误。修复 [docker/for-win#14297](https://github.com/docker/for-win/issues/14297)。
- 修复了当 `registry.json` 文件格式错误时 `docker` CLI 无法按预期工作的错误。
- 修复了 **镜像** 视图中的 **推送到 Docker Hub** 操作会导致 `invalid tag format` 错误的错误。修复 [docker/for-win#14258](https://github.com/docker/for-win/issues/14258)。
- 修复了当 ICMPv6 设置不成功时 Docker Desktop 启动失败的问题。
- 添加了允许 USB/IP 工作的驱动程序。
- 修复了增强容器隔离 (ECI) [派生镜像的 Docker 套接字挂载权限](/manuals/enterprise/security/hardened-desktop/enhanced-container-isolation/config.md) 中的错误，该错误在 Docker Desktop 使用 containerd 镜像存储时错误地拒绝了某些镜像的 Docker 套接字挂载。
- 启用 `NFT_NUMGEN`、`NFT_FIB_IPV4` 和 `NFT_FIB_IPV6` 内核模块。
- 构建 UI：
  - 在 **已完成的构建** 列表中突出显示构建检查警告。
  - 改进了构建时间图表的可视化。
  - 在 **信息** 选项卡下的 **构建结果** 部分添加了镜像标签。
- 改进了 Mac 和 Linux 上全新安装的主机端磁盘利用率效率。
- 修复了令牌过期时无法触发登录强制执行弹窗的错误。
- 修复了在使用[强制登录](/manuals/enterprise/security/enforce-sign-in/_index.md) 时，登录后容器不会立即在 GUI 中显示的错误。
- `settings.json` 已重命名为 `settings-store.json`
- 主机网络功能不再要求用户登录即可使用。

#### Mac

- 修复了在设置中更改文件共享类型后，自动启动容器可能配置错误的错误。
- 修复了在启动时 `~/.docker/cli-plugins` 可能无法填充的错误。
- 修复了阻止 php composer 或 postgres 以非 root 用户身份启动的错误。修复 [docker/for-mac#7415](https://github.com/docker/for-mac/issues/7415)。
- 修复了可能导致主机上更改的文件显示为截断的错误。修复 [docker/for-mac#7438](https://github.com/docker/for-mac/issues/7438)。

#### Windows

- Windows 上的 Docker Desktop 新安装现在需要 Windows 版本 19045 或更高版本。
- 修复了如果在内核配置中或通过内核命令行在 WSL 中禁用了 IPv6 会导致启动失败的问题。修复 [docker/for-win#14240](https://github.com/docker/for-win/issues/14240)
- 修复了 Windows 上的 **清理/清除数据** 按钮。修复 [docker/for-win#12650](https://github.com/docker/for-win/issues/14308)。
- 磁盘使用统计信息现在显示在仪表板页脚安装中。
- 改进了 WSL 发行版问题的恢复能力。

#### Linux

- Docker Desktop 现在支持 Ubuntu 24.04。

### 已知问题

#### Mac

- 自版本 4.34.0 起，高级设置中的“允许特权端口映射”切换不起作用。更多信息，请参阅 [docker/for-mac#7460](https://github.com/docker/for-mac/issues/7460)。

#### Windows

- 版本 4.14.0 及更早版本的用户在使用应用内更新时可能会遇到问题。要更新到最新版本，请从此页面下载并安装最新的 Docker Desktop。

## 4.34.4

{{< release-date date="2025-01-09" >}}

### 错误修复和增强功能

#### Mac

- 防止了导致 Docker Desktop 无法将 `com.docker.vmnetd` 或 `com.docker.socket` 更新到较新版本的错误。

### 已知问题

#### Mac

- 如果您看到关于 `com.docker.vmnetd` 或 `com.docker.socket` 的安全弹窗，请按照 [docker/for-mac#7527](https://github.com/docker/for-mac/issues/7527) 中记录的步骤操作。

## 4.34.3

{{< release-date date="2024-10-09" >}}

{{< desktop-install-v2 all=true win_arm_release="Beta" version="4.34.3" build_path="/170107/" >}}

### 升级

- [NVIDIA Container Toolkit v1.16.2](https://github.com/NVIDIA/nvidia-container-toolkit/releases/tag/v1.16.2)

### 安全性

- 修复了 [CVE-2024-9348](https://www.cve.org/cverecord?id=CVE-2024-9348)，该问题允许通过镜像构建详细信息源信息进行 RCE。
- 修复了 NVIDIA Container Toolkit [CVE-2024-0132](https://nvidia.custhelp.com/app/answers/detail/a_id/5582)
- 修复了 NVIDIA Container Toolkit [CVE-2024-0133](https://nvidia.custhelp.com/app/answers/detail/a_id/5582)

## 4.34.2

{{< release-date date="2024-09-12" >}}

### 错误修复和增强功能

#### 所有平台

- 修复了在资源节省模式下 `docker compose up` 会变得无响应的错误。

### 安全性

- 修复了 [CVE-2024-8695](https://www.cve.org/cverecord?id=CVE-2024-8695)，该问题允许通过精心制作的扩展描述/变更日志进行 RCE，可能被恶意扩展滥用。
- 修复了 [CVE-2024-8696](https://www.cve.org/cverecord?id=CVE-2024-8696)，该问题允许通过精心制作的扩展发布者 URL/附加 URL 进行 RCE，可能被恶意扩展滥用。

## 4.34.1

{{< release-date date="2024-09-05" >}}

{{< desktop-install-v2 win=true win_arm_release="Beta" version="4.34.1" build_path="/166053/" >}}

### 错误修复和增强功能

#### Windows

- 修复了 Docker Desktop 无法启动的错误（通常在首次启动时），错误地认为另一个应用程序实例正在运行。([docker/for-win#14294](https://github.com/docker/for-win/issues/14294) 和 [docker/for-win#14034](https://github.com/docker/for-win/issues/14034))。

## 4.34.0

{{< release-date date="2024-08-29" >}}

### 新增功能

- [主机网络](/manuals/engine/network/drivers/host.md#docker-desktop) 支持在 Docker Desktop 上现已正式可用。
- 如果您通过 CLI 进行身份验证，现在可以通过基于浏览器的流程进行身份验证，无需手动生成 PAT。
- Windows 现在支持在使用[托管虚拟硬盘](/manuals/desktop/features/wsl/best-practices.md) 的 WSL2 安装中自动回收磁盘空间。
- 通过 [MSI 安装程序](/manuals/enterprise/enterprise-deployment/msi-install-and-configure.md) 部署 Docker Desktop 现已正式可用。
- 两种新的[强制登录](/manuals/enterprise/security/enforce-sign-in/_index.md) 方法（Windows 注册表项和 `.plist` 文件）现已正式可用。
- Docker Desktop 的全新安装现在默认使用 containerd 镜像存储。
- [Compose Bridge](/manuals/compose/bridge/_index.md)（实验性）现在可通过 Compose 文件查看器获得。轻松将您的 Compose 项目转换并部署到 Kubernetes 集群。

### 升级

- [Docker Engine v27.2.0](https://docs.docker.com/engine/release-notes/27.2/#2720)
- [Docker Compose v2.29.2](https://github.com/docker/compose/releases/tag/v2.29.2)
- [containerd v1.7.20](https://github.com/containerd/containerd/releases/tag/v1.7.20)
- [Docker Scout CLI v1.13.0](https://github.com/docker/scout-cli/releases/tag/v1.13.0)
- [Docker Buildx v0.16.2](https://github.com/docker/buildx/releases/tag/v0.16.2)
- Linux 内核 `v6.10.1`

### 错误修复和增强功能

#### 所有平台

- 修复了当容器使用 AutoRemove (`--rm`) 启动但其端口绑定被 Docker Desktop 在启动时拒绝时，CLI 变得空闲的错误。
- 修复了在 **支持** 屏幕上诊断收集会随机失败的错误。
- 修复了容器的 **文件** 选项卡中文件夹无法展开的错误。修复 [docker/for-win#14204](https://github.com/docker/for-win/issues/14204)。
- 应用内更新现在尊重代理设置。
- 扩展了 ECI Docker 套接字挂载权限功能，可选择允许来自允许镜像的子镜像。这允许 ECI 与创建使用 Docker 套接字挂载的临时本地镜像的 buildpack（例如 Paketo）一起工作。
- 修复了在使用某些代理设置时导致 **容器** 视图闪烁的错误。修复 [docker/for-win#13972](https://github.com/docker/for-win/issues/13972)。
- 改进了 `docker image list` 的输出，以显示多平台相关的镜像信息。

#### Mac

- 修复了在触发配置完整性检查功能时偶尔出现 `Partial repair error` 的错误。
- 配置完整性检查功能现在显示有关 Docker 套接字配置错误原因的信息。
- 修复了如果 Docker Desktop 作为 `用户` 安装，配置完整性检查功能会报告系统路径而不是用户路径的问题。
- 修复了尝试从绑定挂载卷读取扩展属性的应用程序可能失败的错误。修复 [docker/for-mac#7377](https://github.com/docker/for-mac/issues/7377)。

#### Windows

- 修复了当用户打算保持 `credsStore` 为空时，Docker Desktop 会将 docker 的 `credsStore` 重置为 `desktop` 的错误。修复 [docker/for-win#9843](https://github.com/docker/for-win/issues/9843)。
- 修复了在 WSL2 引擎中 Docker Desktop 无法启动的错误 [docker/for-win#14034](https://github.com/docker/for-win/issues/14034)。
- 修复了导致 WSL 发行版突然终止的错误。修复 [docker/for-win/14230](https://github.com/docker/for-win/issues/14230)。
- 修复了导致 WSL 在每次启动时更新的问题。修复 [docker/for-win/13868](https://github.com/docker/for-win/issues/13868), [docker/for-win/13806](https://github.com/docker/for-win/issues/13806)。

### 已知问题

- Compose Bridge 在 **实验性** 设置选项卡中启用时不会自动工作。需要几分钟时间才会通知您必须“修复”Docker Desktop，然后安装 `compose-bridge` 二进制文件。
- 即使 Kubernetes 正在运行且 Compose Bridge 已启用，Compose 文件查看器中的 **转换和部署** 按钮也可能被禁用。解决方法是在 **实验性** 设置选项卡中禁用 Compose Bridge，使用 **应用并重启** 应用更改，然后重新启用并再次选择 **应用并重启**。
- 在 Docker CLI 中针对注册表进行身份验证时存在一个已知问题 (`docker login [registry address]`)，如果提供的注册表地址包含存储库/镜像名称（例如 `docker login index.docker.io/docker/welcome-to-docker`），则存储库部分 (`docker/welcome-to-docker`) 不会被规范化，导致凭据存储不正确，从而导致后续从注册表拉取 (`docker pull index.docker.io/docker/welcome-to-docker`) 时无法进行身份验证。为防止这种情况，在运行 `docker login` 时不要在注册表地址中包含任何额外的后缀。
  > [!NOTE]
  > 使用包含 URL 路径段的地址进行 `docker login` 不是记录在案的用例，被视为不受支持。推荐的用法是仅指定注册表主机名，以及可选的端口，作为 `docker login` 的地址。
- 当运行 `docker compose up` 且 Docker Desktop 处于资源节省模式时，该命令无响应。作为解决方法，请手动退出资源节省模式，Docker Compose 将再次变得有响应。
- 当启用[增强容器隔离 (ECI)](/manuals/enterprise/security/hardened-desktop/enhanced-container-isolation/_index.md) 时，Docker Desktop 可能无法进入资源节省模式。这将在未来的 Docker Desktop 版本中修复。
- 新的 [ECI 派生镜像的 Docker 套接字挂载权限](/manuals/enterprise/security/hardened-desktop/enhanced-container-isolation/config.md#docker-socket-mount-permissions-for-derived-images) 功能在 Docker Desktop 配置为 **使用 containerd 拉取和存储镜像** 时尚未生效。这将在下一个 Docker Desktop 版本中修复。

## 4.33.2

{{< release-date date="2025-01-09" >}}

### 错误修复和增强功能

#### Mac

- 防止了导致 Docker Desktop 无法将 `com.docker.vmnetd` 或 `com.docker.socket` 更新到较新版本的错误。

### 已知问题

#### Mac

- 如果您看到关于 `com.docker.vmnetd` 或 `com.docker.socket` 的安全弹窗，请按照 [docker/for-mac#7527](https://github.com/docker/for-mac/issues/7527) 中记录的步骤操作。

## 4.33.1

{{< release-date date="2024-07-31" >}}

### 错误修复和增强功能

#### Windows

- 添加了对 WSL2 2.3.11 及更高版本的支持，其中包括可加载内核模块。修复 [docker/for-win#14222](https://github.com/docker/for-win/issues/14222)

## 4.33.0

{{< release-date date="2024-07-25" >}}

{{< desktop-install-v2 all=true win_arm_release="Beta" version="4.33.0" build_path="/160616/" >}}

### 新增功能

- [Docker Debug](/reference/cli/docker/debug.md) 现已正式可用。
- BuildKit 现在评估 Dockerfile 规则以通知您潜在的问题。
- 现在可以直接从仪表板页脚显示的资源使用数据访问 **资源分配** 设置。
- [故障排除](/manuals/desktop/troubleshoot-and-support/troubleshoot/_index.md) 的全新改进体验。

### 升级

- [Docker Compose v2.29.1](https://github.com/docker/compose/releases/tag/v2.29.1)
- [Docker Engine v27.1.1](https://docs.docker.com/engine/release-notes/27.1/#2711)
- [containerd v1.7.19](https://github.com/containerd/containerd/releases/tag/v1.7.19)
- [NVIDIA Container Toolkit v1.16.0](https://github.com/NVIDIA/nvidia-container-toolkit/releases/tag/v1.16.0)
- [Docker Scout CLI v1.11.0](https://github.com/docker/scout-cli/releases/tag/v1.11.0)
- [Kubernetes v1.30.2](https://github.com/kubernetes/kubernetes/releases/tag/v1.30.2)
- Linux 内核 `v6.10`

### 错误修复和增强功能

#### 所有平台

- 修复了使用 `--net=host` 启动并侦听 IPv6 地址的容器可以从主机访问的问题。
- 改进了在 **设置** 选项卡中启用 containerd 镜像存储的用户体验。
- 修复了在重负载下使用 `grpcfuse` 文件共享选项时出现的死锁问题。
- 修复了特定于 Mac 的管理员设置影响其他平台的错误。
- IPv6 地址块现在可以在 Docker Engine 的 `default-address-pools` 中指定。
- 修复了 Docker Engine 的 `bip`、`fixed-cidr` 和 `fixed-cidr-v6` 验证问题。修复 [docker/for-mac#7104](https://github.com/docker/for-mac/issues/7104)。
- Docker Engine 的 `default-network-opts` 参数现在经过正确验证。
- VirtioFS 性能改进包括增加目录缓存超时、处理来自主机的更改通知、移除用于 security.capability 属性的额外 FUSE 操作、优化主机事件检测，以及提供 API 在容器终止后清理缓存。
- Docker Desktop 现在会在主机网络容器中存在端口冲突时发出通知。
- Compose Bridge 命令行选项现在可通过实验性功能获得。启用后，运行 `compose-bridge` 可将您的 Compose 配置转换为 Kubernetes 资源。
- 构建视图：
  - 在构建详细信息的 **源** 选项卡中添加了[构建检查](/manuals/build/checks.md)。
  - 在构建详细信息的 **信息** 选项卡下的 **源详细信息** 部分添加了构建标签。
  - 新导入的构建现在会突出显示。
  - 改进了错误消息处理的性能。
  - 修复了与构建器的连接问题，该问题阻止了构建记录的显示。
  - 修复了通过 CLI 打开构建时的导航问题。

#### Mac

- 配置完整性检查功能现在提供有关 Docker Desktop 配置更改内容的更多上下文。更多信息，请参阅[常见问题解答](/manuals/desktop/troubleshoot-and-support/faqs/macfaqs.md)。
- 配置完整性检查功能在修复 Docker Desktop 失败时会显示错误。
- 修复了 IPv6 TCP 设置为 `host.docker.internal` 的错误。修复 [docker/for-mac#7332](https://github.com/docker/for-mac/issues/7332)。
- 修复了 `docker-compose` 符号链接指向空位置的问题。修复 [docker/for-mac#7345](https://github.com/docker/for-mac/issues/7345)。

#### Linux

- 修复了卸载后某些 `wincred` 值仍然存在的问题。由 Javier Yong [@Javiery3889](https://github.com/Javiery3889) 报告。
- 修复了通知 **另一个应用程序更改了您的桌面配置** 被错误触发的问题。

### 安全性

#### 所有平台

- 包含了对 Docker Engine 中 AuthZ 插件绕过回归的修复。更多信息，请参阅 [CVE-2024-41110](https://www.cve.org/cverecord?id=CVE-2024-41110)。

#### Windows

- 修复了卸载后某些 `wincred` 值仍然存在的问题。由 Javier Yong [@Javiery3889](https://github.com/Javiery3889) 报告。

### 已知问题

#### Windows

- Docker Desktop 在 WSL 预发布版本 `v2.3.11.0` 和 `v2.3.12.0`（包含在 Windows 11 Insider 中）上无法启动。要修复此问题，请确保安装了 WSL `v2.2.4.0`。
  更多信息，请参阅 [microsoft/WSL#11794](https://github.com/microsoft/WSL/issues/11794)。这会影响 Docker Desktop 4.33.0 及更早版本。

## 4.32.1

{{< release-date date="2025-01-09" >}}

{{< desktop-install-v2 mac=true version="4.32.1" build_path="/179691/" >}}

### 错误修复和增强功能

#### Mac

- 防止了导致 Docker Desktop 无法将 `com.docker.vmnetd` 或 `com.docker.socket` 更新到较新版本的错误。

### 已知问题

#### Mac

- 如果您看到关于 `com.docker.vmnetd` 或 `com.docker.socket` 的安全弹窗，请按照 [docker/for-mac#7527](https://github.com/docker/for-mac/issues/7527) 中记录的步骤操作。

## 4.32.0

{{< release-date date="2024-07-04" >}}


### 新增功能

- Docker Engine 和 CLI 更新至版本 27.0。
- Docker Desktop 现在支持在 macOS 和使用 WSL2 后端的 Windows 上将数据移动到不同的驱动器。请参阅 [docker/for-win#13384](https://github.com/docker/for-win/issues/13384)。
- 您现在可以在 **卷** 选项卡中[安排卷导出备份](use-desktop/volumes.md)（Beta）。
- 直接从 Docker Desktop 访问终端 shell（Beta）。

### 升级

- [Docker Buildx v0.15.1](https://github.com/docker/buildx/releases/tag/v0.15.1)
- [Docker Compose v2.28.1](https://github.com/docker/compose/releases/tag/v2.28.1)
- [Docker Scout CLI v1.10.0](https://github.com/docker/scout-cli/releases/tag/v1.10.0)
- [Docker Engine v27.0.3](https://docs.docker.com/engine/release-notes/27/#2703)
- Docker Init v1.3.0

### 错误修复和增强功能

#### 所有平台

- 改进了 Compose 文件查看器中 `watch` 的说明
- 为 Docker Init 添加了对没有依赖项的 Golang 项目的支持。解决 [docker/roadmap#611](https://github.com/docker/roadmap/issues/611)
- [设置管理](/manuals/enterprise/security/hardened-desktop/settings-management/_index.md) 现在允许管理员将默认值设置为 `ProxyEnableKerberosNTLM`。
- 移除了旧版 Visual Studio Code 的临时兼容性修复。
- 构建视图：
  - 将导入的构建记录的图标更改为“文件”图标。
  - 改进了尝试连接到已连接的 Docker Build Cloud 构建器时的错误消息。
  - 修复了构建记录会意外消失的问题。
  - 修复了阻止用户重新打开[导入构建](use-desktop/builds.md#import-builds)的问题。
  - 修复了当构建状态从运行变为完成时，构建详细信息未显示的问题。
  - 修复了构建详细信息中格式错误的构建源链接。
  - 修复了命名上下文缺少构建统计信息的问题。
  - 修复了镜像索引/清单在构建结果中不再显示的问题。
  - 修复了从 UI 导出的构建迹线在导入到 Jaeger 时显示为单个扁平列表的问题
  - 修复了构建详细信息中截断的摘要/sha。
  - 修复了活动构建的最终状态动画。

#### Windows

- 修复了在 WSL 2 引擎上的一个问题，即如果用户手动移动了 `docker-desktop-data` 发行版，Docker Desktop 将无法检测到其存在。
- Windows on ARM 安装程序和[特权服务](/manuals/desktop/setup/install/windows-permission-requirements.md#privileged-helper) 现在是为 ARM64 构建的。

#### Mac

- 重新添加了 `CONFIG_DM_CRYPT` 内核模块。
- 重新添加了 `CONFIG_PSI` 内核模块。
- 重新添加了 `CONFIG_GTP` 内核模块。
- 重新添加了 `CONFIG_NFT_BRIDGE_META` 内核模块。
- 修复了回归问题，即当 `/var/run/docker.socket` 指向意外路径时，会出现 **另一个应用程序更改了您的桌面配置** 警告消息。
- 将配置检查菜单项和横幅更改为通知。
- 改进了绑定挂载上的读写操作性能。
- 修复了某些 `AMD64` Java 镜像的致命错误。修复 [docker/for-mac/7286](https://github.com/docker/for-mac/issues/7286) 和 [docker/for-mac/7006](https://github.com/docker/for-mac/issues/7006)。
- 修复了从 `/Applications` 安装时 Docker Desktop 会删除 `Docker.app` 的问题。
- 修复了导致绑定挂载失败的错误。修复 [docker/for-mac#7274](https://github.com/docker/for-mac/issues/7274)。

### 已知问题

#### 所有平台

- **使用 Compose 管理同步文件共享** 设置会自动为所有选择加入 **访问实验性功能** 的用户启用。这会将所有绑定挂载转换为同步文件共享。要禁用此行为，请取消选择 **访问实验性功能**。然后，手动删除任何文件共享：转到 **资源** 中的 **文件共享** 选项卡，导航到 **同步文件共享** 部分，选择要删除的文件共享，然后选择 **删除**。

#### Mac

- 更新后运行 `docker-compose` 将返回 `command not found`。作为解决方法，您可以创建以下符号链接：`sudo ln -sf /Applications/Docker.app/Contents/Resources/cli-plugins/docker-compose /usr/local/bin/docker-compose`

## 4.31.1

### 错误修复和增强功能

#### Windows

- 修复了在更新之前创建的容器、镜像和卷可能对用户不可见的错误。修复 [docker/for-win#14118](https://github.com/docker/for-win/issues/14118)。

## 4.31.0

### 新增功能

- [气隙容器](/manuals/enterprise/security/hardened-desktop/air-gapped-containers.md) 现已正式可用。
- Docker Compose 文件查看器使用语法高亮显示您的 Compose YAML，并提供指向相关文档的上下文链接（Beta，渐进式推出）。
- 新的侧边栏用户体验。

### 升级

- [Docker Engine and CLI v26.1.4](https://github.com/moby/moby/releases/tag/v26.1.4).
- [Docker Scout CLI v1.9.1](https://github.com/docker/scout-cli/releases/tag/v1.9.1)
- [Docker Compose v2.27.1](https://github.com/docker/compose/releases/tag/v2.27.1)
- [Docker Buildx v0.14.1](https://github.com/docker/buildx/releases/tag/v0.14.1)
- [Containerd v1.6.33](https://github.com/containerd/containerd/releases/tag/v1.6.33)
- [Credential Helpers v0.8.2](https://github.com/docker/docker-credential-helpers/releases/tag/v0.8.2)
- [NVIDIA Container Toolkit v1.15.0](https://github.com/NVIDIA/nvidia-container-toolkit/releases/tag/v1.15.0)
- [Go 1.22.4](https://github.com/golang/go/releases/tag/go1.22.4)
- Linux 内核 `v6.6.31`

### 错误修复和增强功能

#### 所有平台

- 当更新已下载时，较新的版本现在会显示在 **软件更新** 设置选项卡中。
- 在 `settings.json` 中添加了 `proxyEnableKerberosNTLM` 配置，以便在 Kerberos/NTLM 环境未正确设置时回退到基本代理身份验证。
- 修复了在启用增强容器隔离时 Docker Debug 无法正常工作的错误。
- 修复了 UDP 响应未正确截断的错误。
- 修复了在使用[设置管理](/manuals/enterprise/security/hardened-desktop/settings-management/_index.md) 时 **更新** 屏幕被隐藏的错误。
- 修复了 `admin-settings.json` 中定义的代理设置在启动时未正确应用的错误。
- 修复了 **使用 Compose 管理同步文件共享** 切换开关未正确反映功能值的错误。
- 修复了当在 macOS 和使用 Hyper-V 的 Windows 上使用 gRPC FUSE 文件共享时，主机上修改的绑定挂载文件在容器重启后未更新的错误。修复 [docker/for-mac#7274](https://github.com/docker/for-mac/issues/7274), [docker/for-win#14060](https://github.com/docker/for-win/issues/14060)。
- 构建视图：
  - 新的[导入构建](use-desktop/builds.md#import-builds) 功能，允许您导入其他人或 CI 环境中构建的构建记录。
  - 修复了失败构建的构建结果中缺少 OpenTelemetry 迹线的问题。
  - 修复了 `default-load` 显示为容器驱动程序的无效驱动程序选项的问题。
  - 修复了指向构建详细信息的深度链接。

#### Windows

- 将 `--allowed-org` 安装程序标志更改为写入策略注册表项，而不是写入 `registry.json`。

#### Mac

- 将 **自动检查配置** 设置从 **高级** 设置移至 **常规** 设置。
- 通过实现更长的属性超时和失效改进了 VirtioFS 缓存。

#### Linux

- 在 VM 中添加了 Linux 头文件，以简化自定义内核模块的编译。

### 安全性

#### 所有平台

- 修复了增强容器隔离 (ECI) 模式下的一个安全漏洞，该漏洞允许用户创建源自 Docker Desktop VM 内受限目录的 Docker 卷，并将其挂载到容器中，从而让容器访问此类受限的 VM 目录。
- 默认情况下，只有扩展市场中列出的扩展才能在 Docker Desktop 中安装。这可以在 Docker Desktop 的设置中更改。扩展开发人员需要更改此选项才能测试他们的扩展。

### Windows

- 修复了 [CVE-2024-5652](https://www.cve.org/cverecord?id=CVE-2024-5652)，该问题允许 `docker-users` 组中的用户通过 Windows 容器模式下的 `exec-path` Docker 守护程序配置选项导致 Windows 拒绝服务。此漏洞由 Hashim Jawad ([@ihack4falafel](https://github.com/ihack4falafel)) 与 Trend Micro Zero Day Initiative 合作发现。

### 弃用

#### 所有平台

- 以前作为 `com.docker.cli` 发送的 CLI 二进制文件现在仅作为 `docker` 发送。此版本将 CLI 二进制文件保留为 `com.docker.cli`，但将在下一个版本中移除。

#### Windows

- 从 WSL2 引擎中移除了对旧版版本包的支持。

### 已知问题

#### Windows

- 升级到 Docker Desktop 4.31.0 时，使用 Docker Desktop 4.8.0 或更低版本在仅使用 WSL 的 Windows 主机上创建的现有容器、镜像和卷对用户不可见。数据不会丢失，只是对 Docker Desktop 4.31.0 不可见。如果受到影响，请降级到 4.30 或更早版本。更多信息请参见：[docker/for-win#14118](https://github.com/docker/for-win/issues/14118)。

#### Linux

- 尚未支持 Ubuntu 24.04 LTS，Docker Desktop 将无法启动。由于最新 Ubuntu 版本限制非特权命名空间的方式发生了变化，需要至少运行一次 `sudo sysctl -w kernel.apparmor_restrict_unprivileged_userns=0`。请参阅 [Ubuntu 博客](https://ubuntu.com/blog/)。

## 4.30.0

{{< release-date date="2024-05-06" >}}

### 新增功能

#### 所有平台

- Docker Desktop 现在支持 [SOCKS5 代理](/manuals/desktop/features/networking.md#socks5-proxy-support)。需要商业订阅。
- 添加了一个新设置来管理[设置管理](/manuals/enterprise/security/hardened-desktop/settings-management/_index.md) 中的入职调查。

#### Windows

- 添加了对 [Kerberos 和 NTLM 代理身份验证](/manuals/desktop/settings-and-maintenance/settings.md#proxy-authentication) 的支持。需要商业订阅。

### 升级

- [Docker Compose v2.27.0](https://github.com/docker/compose/releases/tag/v2.27.0)
- [Docker Engine v26.1.1](https://docs.docker.com/engine/release-notes/26.1/#2611)
- [Wasm](/manuals/desktop/features/wasm.md) 运行时：
  - 将 `runwasi` shim 更新至 `v0.4.0`
  - 将 `deislabs` shim 更新至 `v0.11.1`
  - 将 `spin` shim 更新至 `v0.13.1`
- [Docker Scout CLI v1.8.0](https://github.com/docker/scout-cli/releases/tag/v1.8.0)
- Docker Debug `v0.0.29`
- Linux 内核 `v6.6.26`
- [Go 1.22.2](https://github.com/golang/go/releases/tag/go1.22.2)

### 错误修复和增强功能

#### 所有平台

- 改进了在无根容器中运行 `docker build` 命令时的增强容器隔离 (ECI) 安全性。
- 修复了当 Docker Desktop 进入/退出资源节省模式时，`docker events` 以 `Unexpected EOF` 退出的错误。
- 修复了当 Docker Desktop 处于资源节省模式时，`docker stats --no-stream` 挂起的错误。
- 修复了自诊断 CLI 中的一个错误，该错误错误地显示 VM 尚未启动。修复 [docker/for-mac#7241](https://github.com/docker/for-mac/issues/7241)。
- 修复了高吞吐量端口转发传输可能停滞的错误。修复 [docker/for-mac#7207](https://github.com/docker/for-mac/issues/7207)。
- 修复了在移除 CLI 应用程序时 CLI 插件符号链接未被移除的错误。
- 修复了共享端口抽屉中针对本地引擎显示正确消息的问题。
- 开发环境正在逐步淘汰，并已移至 **开发中功能** 中的 **Beta** 选项卡。
- 构建视图：
  - 更好的批量删除构建记录。
  - 为构建依赖项中的容器镜像和 Git 源添加了打开相关网页的操作。
  - 添加了下载 Jaeger 或 OTLP 格式的溯源和 OpenTelemetry 迹线的操作。
  - 修复了远程构建调用的源详细信息。
  - 修复了使用云构建器时多平台构建显示为单独记录的错误。

#### Mac

- 修复了在 2019 年后的 Mac 上使用虚拟化框架时触发分段错误的错误。请参阅 [docker/for-mac#6824](https://github.com/docker/for-mac/issues/6824)。
- 启用了 `CONFIG_SECURITY=y` 内核配置，例如用于 [Tetragon](https://tetragon.io/)。修复 [docker/for-mac#7250](https://github.com/docker/for-mac/issues/7250)。
- 重新添加了对 `SQUASHFS` 压缩的支持。修复 [docker/for-mac#7260](https://github.com/docker/for-mac/issues/7260)。
- 修复了导致新版本的 Docker Desktop 被标记为损坏的错误。
- 在 Apple Silicon 上使用 qemu 时增加了网络 MTU。
- 修复了如果未安装 Rosetta 则阻止 Docker Desktop 启动的错误。修复 [docker/for-mac#7243](https://github.com/docker/for-mac/issues/7243)。

#### Windows

- 为 WSL2 添加了简化的配置模式，避免了对辅助 `docker-desktop-data` WSL 发行版的需求（实验性）。
- 修复了 WSL 环境中 Docker CLI 的 bash 补全。
- 修复了 Docker Desktop 4.28 中的回归问题，该问题导致在 WSL 上使用 Docker-in-Docker（通过挂载 `/var/run/docker.sock`）时，绑定挂载到容器中的主机文件在容器内无法正确显示。
- 修复了导致以下错误的错误：`merging settings: integratedWslDistros type mismatch`。

### 已知问题

#### 所有平台

- 如果您启用了 Docker Desktop 中需要您登录的功能，例如 **主机网络**，您必须保持登录状态才能使用 Docker Desktop。要继续使用 Docker Desktop 或修改这些设置，请确保您已登录。
- 要启用或禁用 **使用 Compose 管理同步文件共享**，**访问实验性功能** 和 **使用 Compose 管理同步文件共享** 必须同时选中或取消选中。
- 当使用自动删除选项 (`--rm`) 运行容器时，如果容器启动失败（例如：`docker run --rm alpine invalidcommand`），Docker CLI 有时会挂起。在这种情况下，可能需要手动终止 CLI 进程。

#### Windows

- 以非管理员用户身份启动 Docker Desktop 时，如果用户不是 **docker-users** 组的成员，可能会触发以下错误连接 `ENOENT \\.\pipe\errorReporter`。
  可以通过将用户添加到 **docker-users** 组来解决此问题。在启动 Docker Desktop 之前，请确保注销并重新登录，并使用 `wsl --unregister docker-desktop` 注销（如果已创建）`docker-desktop` 发行版。

#### Linux

- 尚未支持 Ubuntu 24.04 LTS，Docker Desktop 将无法启动。由于最新 Ubuntu 版本限制非特权命名空间的方式发生了变化，需要至少运行一次 `sudo sysctl -w kernel.apparmor_restrict_unprivileged_userns=0`。有关更多详细信息，请参阅 [Ubuntu 博客](https://ubuntu.com/blog/ubuntu-23-10-restricted-unprivileged-user-namespaces)。

## 4.29.0

{{< release-date date="2024-04-08" >}}

### 新增功能

- 您现在可以通过[设置管理](/manuals/enterprise/security/hardened-desktop/settings-management/_index.md) 强制使用 Rosetta。
- [Docker 套接字挂载限制](/manuals/enterprise/security/hardened-desktop/enhanced-container-isolation/config.md) 与 ECI 现已正式可用。
- Docker Engine 和 CLI 更新至 [Moby 26.0](https://github.com/moby/moby/releases/tag/v26.0.0)。这包括 Buildkit 0.13、子卷挂载、网络更新以及对 containerd 多平台镜像存储 UX 的改进。
- 全新的改进版 Docker Desktop 错误屏幕：快速故障排除、轻松诊断上传和可操作的补救措施。
- Compose 支持[同步文件共享（实验性）](/manuals/desktop/features/synchronized-file-sharing.md)。
- 新的[交互式 Compose CLI（实验性）](/manuals/compose/how-tos/environment-variables/envvars.md#compose_menu)。
- 以下功能的 Beta 版发布：
  - 气隙容器与[设置管理](/manuals/enterprise/security/hardened-desktop/air-gapped-containers.md)。
  - Docker Desktop 中的[主机网络](/manuals/engine/network/drivers/host.md#docker-desktop)。
  - 用于运行容器的 [Docker Debug](use-desktop/container.md#integrated-terminal)。
  - [卷备份和共享扩展](use-desktop/volumes.md) 功能在 **卷** 选项卡中可用。

### 升级

- [Docker Compose v2.26.1](https://github.com/docker/compose/releases/tag/v2.26.1)
- [Docker Scout CLI v1.6.3](https://github.com/docker/scout-cli/releases/tag/v1.6.3)
- [Docker Engine v26.0.0](https://docs.docker.com/engine/release-notes/26.0/#2600)
- [Buildx v0.13.1](https://github.com/docker/buildx/releases/tag/v0.13.1)
- [Kubernetes v1.29.2](https://github.com/kubernetes/kubernetes/releases/tag/v1.29.2)
- [cri-dockerd v0.3.11](https://github.com/Mirantis/cri-dockerd/releases/tag/v0.3.11)
- Docker Debug v0.0.27

### 错误修复和增强功能

#### 所有平台

- 修复了下拉菜单在应用程序窗口之外打开的问题。
- Docker Init：
  - 更新了 CLI 输出的格式以提高可读性。
  - 修复了 `.dockerignore` 的问题，以避免忽略以 "compose" 开头的应用程序文件。
  - 改进了基于 Spring Boot 版本启动 Java 应用程序的方式。修复 [docker/for-mac#7171](https://github.com/docker/for-mac/issues/7171)。
  - 移除了用于 Rust 交叉编译的非官方 Docker 镜像。
- 每个[同步文件共享](/manuals/desktop/features/synchronized-file-sharing.md) 的最大文件数现在超过 200 万。
- 修复了在选择 **导出到本地镜像** 字段时导致警告：“_提供给自动完成的值无效。_” 的问题。
- **运行云** 现在可以从 Docker Desktop 仪表板访问。
- 选择退出发送分析现在也会禁用为错误报告收集数据。
- 您现在可以在 **容器** 视图中共享和取消共享端口到云引擎。
- 共享云现在可以从仪表板右侧的页脚访问。
- 添加了对 macOS、Windows 和 Linux 版 Docker Desktop 的主机网络的 Beta 支持 [docker#238](https://github.com/docker/roadmap/issues/238)。
- 为未读通知添加了时间戳。
- 修复了虚拟化支持错误消息中的拼写错误。修复 [docker/desktop-linux#197](https://github.com/docker/desktop-linux/issues/197)。
- Docker Desktop 现在允许通过 PAC 文件中的规则阻止连接到 `host.docker.internal`。
- 修复了 **镜像** 和 **容器** 列表中二级菜单位置的问题。
- 修复了使用 QEMU 启动 Docker Desktop 时发生的竞争条件。
- 当镜像拉取被注册表访问管理策略阻止时，改进了错误消息。
- 在内核配置中重新添加了 `CONFIG_BONDING=y`。

#### Mac

- 修复了 Kubernetes 无法成功启动的问题。修复 [docker/for-mac#7136](https://github.com/docker/for-mac/issues/7136) 和 [docker/for-mac#7031](https://github.com/docker/for-mac/issues/7031)。
- 修复了当浏览器无法将身份验证信息发送回 Docker Desktop 时的错误。修复 [docker/for-mac/issues#7160](https://github.com/docker/for-mac/issues/7160)。

#### Windows

- 修复了在 WSL 2 和 Hyper-V 之间切换后 `docker run -v` 失败的错误。
- 修复了在关闭时 Docker Desktop 未停止其 WSL 发行版 (`docker-desktop` 和 `docker-desktop-data`) 的错误。修复 [docker/for-win/issues/13443](https://github.com/docker/for-win/issues/13443) 和 [docker/for-win/issues/13938](https://github.com/docker/for-win/issues/13938)。

#### Linux

- 修复了导致 UI 中可用的实验性功能列表与后端数据不同步的问题。

#### 安全性

- 禁用了 Electron `runAsNode` 熔断器以提高安全性。更多信息，请参阅 [Electron 的文档。](https://www.electronjs.org/blog/statement-run-as-node-cves)。
- 修复了 [CVE-2024-6222](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-6222)，该问题允许通过容器逃逸获得对 Docker Desktop VM 访问权限的攻击者通过传递扩展和仪表板相关的 IPC 消息进一步逃逸到主机。由 Billy Jheng Bing-Jhong、Đỗ Minh Tuấn、Muhammad Alifa Ramdhan 与 Trend Micro Zero Day Initiative 合作报告。

### 已知问题

#### Mac

- 如果未安装 Rosetta，Apple Silicon 上的 Docker Desktop 无法启动。这将在未来的版本中修复。请参阅 [docker/for-mac#7243](https://github.com/docker/for-mac/issues/7243)。

## 4.28.0

{{< release-date date="2024-02-26" >}}

### 新增功能

- [设置管理](/manuals/enterprise/security/hardened-desktop/settings-management/_index.md) 现在允许管理员设置默认的文件共享实现，并指定开发人员可以向其添加文件共享的路径。
- 当启用 [`SOCKS` 代理支持 Beta 功能](/manuals/desktop/features/networking.md) 时，添加了对 `socks5://` HTTP 和 HTTPS 代理 URL 的支持。
- 用户现在可以在 **卷** 选项卡中过滤卷以查看哪些卷正在使用中。

### 升级

- [Compose v2.24.6](https://github.com/docker/compose/releases/tag/v2.24.6)
- [Docker Engine v25.0.3](https://docs.docker.com/engine/release-notes/25.0/#2503)
- [Docker Scout CLI v1.5.0](https://github.com/docker/scout-cli/releases/tag/v1.5.0)
- [Qemu 8.1.5](https://wiki.qemu.org/ChangeLog/8.1)
- [Wasm](/manuals/desktop/features/wasm.md) 运行时：
  - 将 runwasi shim 更新至 `v0.4.0`，包括：
    - wasmtime `v17.0`，初步支持 WASI preview 2
    - wasmedge `v0.13.5`
    - wasmer `v4.1.2`
  - 将 deislabs shim 更新至 `v0.11.1`，包括：
    - lunatic `v0.13.2`
    - slight `v0.5.1`
    - spin `v2.2.0`
    - wws `v1.7.0`

### 错误修复和增强功能

#### 所有平台

- 修复了 `postgis` 与 `Qemu` 的问题。修复 [docker/for-mac#7172](https://github.com/docker/for-mac/issues/7172)。
- 重新添加了 `CONFIG_BLK_DEV_DM` 内核配置以支持 `kpartx`。修复 [docker/for-mac#7197](https://github.com/docker/for-mac/issues/7197)。
- 允许通过代理自动配置 `pac 文件` 设置 `SOCKS` 代理。
- 重新添加了 `CONFIG_AUDIT` 内核配置。
- 修复了在 `virtiofs` 上 Rust 构建的问题。请参阅 [rust-lang/docker-rust#161](https://github.com/rust-lang/docker-rust/issues/161)。
- 修复了拉取 Kubernetes 镜像时导致 `缺少注册表身份验证` 错误的问题。
- 修复了导致 Docker Compose 命令挂起的问题。
- 修复了 `docker build` 中导致 Docker Desktop 崩溃的错误。修复 [docker/for-win#13885](https://github.com/docker/for-win/issues/13885), [docker/for-win#13896](https://github.com/docker/for-win/issues/13896), [docker/for-win#13899](https://github.com/docker/for-win/issues/13899), [docker/for-mac#7164](https://github.com/docker/for-mac/issues/7164), [docker/for-mac#7169](https://github.com/docker/for-mac/issues/7169)
- Docker Init：
  - 改进了基于 Spring Boot 版本启动 Java 应用程序的方式。修复 [docker/for-mac#7171](https://github.com/docker/for-mac/issues/7171)。
  - 移除了用于 Rust 交叉编译的非官方 Docker 镜像
- 构建视图：
  - 活动和已完成的构建可在专用选项卡中找到。
  - 构建详细信息现在显示构建持续时间和缓存步骤。
  - OpenTelemetry 迹线现在显示在构建结果中。
  - 修复了上下文构建器事件并非总是触发的问题。
  - 重新设计了空状态视图，使仪表板更清晰。

#### Mac

- 修复了 Rosetta 的 `httpd` 问题。[docker/for-mac#7182](https://github.com/docker/for-mac/issues/7182)
- 修复了在 `virtualization.framework` 上导致崩溃的错误。修复 [docker/for-mac#7024](https://github.com/docker/for-mac/issues/7024)

#### Windows

- 修复了 Windows 上 DNS 超时的问题。
- 添加了对 WSL 用户发行版中增强容器隔离 Docker 套接字挂载权限的支持。
- 修复了从 CLI 重定向输出时导致 `failed to get console mode` 错误的问题。
- 修复了在容器内挂载时引擎套接字权限的问题。修复 [docker/for-win#13898](https://github.com/docker/for-win/issues/13898)

### 已知问题

#### Windows

- 在深色模式下，**资源**>**高级** 设置中的 **磁盘镜像位置** 不可见。作为解决方法，请切换到浅色模式。

## 4.27.2

{{< release-date date="2024-02-08" >}}

### 升级

- [Compose v2.24.5](https://github.com/docker/compose/releases/tag/v2.24.5)
- [Docker Scout CLI v1.4.1](https://github.com/docker/scout-cli/releases/tag/v1.4.1)
- Docker Debug v0.0.24

### 错误修复和增强功能

#### 所有平台

- 修复了从终端上传诊断时诊断 ID 无法正确打印的错误。
- 修复了在使用设置管理时，默认设置值在启动时重置为默认值的错误。
- 修复了即使 **Docker Desktop 启动时打开 Docker 仪表板** 选项已禁用，仪表板在启动时仍会显示的错误。修复 [docker/for-win#13887](https://github.com/docker/for-win/issues/13887)。
- 修复了构建后端服务中的错误，该错误导致 Docker Desktop 崩溃。修复 [docker/for-win#13885](https://github.com/docker/for-win/issues/13885), [docker/for-win#13896](https://github.com/docker/for-win/issues/13896), [docker/for-win#13899](https://github.com/docker/for-win/issues/13899), [docker/for-mac#7164](https://github.com/docker/for-mac/issues/7164), [docker/for-mac#7169](https://github.com/docker/for-mac/issues/7169)。
- 修复了在容器内挂载时 Docker Engine 套接字权限的问题。修复 [docker/for-win#13898](https://github.com/docker/for-win/issues/13898)。
- Docker Scout：
  - 更新了依赖项以解决 Leaky Vessels 系列 CVE ([CVE-2024-21626](https://github.com/advisories/GHSA-xr7r-f8xq-vfvv), [CVE-2024-24557](https://github.com/advisories/GHSA-xw73-rw38-6vjc))
  - 添加了初始 VEX 文档以记录误报 [CVE-2020-8911](https://github.com/advisories/GHSA-f5pg-7wfw-84q9) 和 [CVE-2020-8912](https://github.com/advisories/GHSA-7f33-f4f5-xwgw)
  - 添加了对 cosign SBOM 证明的支持
  - 添加了对 VEX in-toto 证明的支持
- Docker Debug：
  - 修复了在资源访问管理后面拉取镜像时的错误
  - 修复了连接问题

#### Mac

- 重新添加了 `Istio` 所需的内核模块。修复 [docker/for-mac#7148](https://github.com/docker/for-mac/issues/7148)。
- Node 现在在 Rosetta 下使用所有可用的核心。
- 修复了 `php-fpm` 的问题。修复 [docker/for-mac#7037](https://github.com/docker/for-mac/issues/7037)。

## 4.27.1

{{< release-date date="2024-02-01" >}}

### 升级

- [Docker Engine v25.0.2](https://docs.docker.com/engine/release-notes/25.0/#2502)，其中包含对 [CVE-2024-24557](https://scout.docker.com/vulnerabilities/id/CVE-2024-24557)、[CVE-2024-23650](https://scout.docker.com/vulnerabilities/id/CVE-2024-23650)、[CVE-2024-23651](https://scout.docker.com/vulnerabilities/id/CVE-2024-23651)、[CVE-2024-23652](https://scout.docker.com/vulnerabilities/id/CVE-2024-23652) 和 [CVE-2024-23653](https://scout.docker.com/vulnerabilities/id/CVE-2024-23653) 的修复
- [Containerd v1.6.28](https://github.com/containerd/containerd/releases/tag/v1.6.28)
- [Runc v1.1.12](https://github.com/opencontainers/runc/releases/tag/v1.1.12)，其中包含对 [CVE-2024-21626](https://scout.docker.com/vulnerabilities/id/CVE-2024-21626) 的修复

### 错误修复和增强功能

#### Mac

- 修复了在应用更新时导致 Docker Desktop 挂起的错误。

## 4.27.0

{{< release-date date="2024-01-25" >}}

### 新增功能

- Docker init 现在支持 Java，并对所有用户正式可用。
- [同步文件共享](/manuals/desktop/features/synchronized-file-sharing.md) 在 Docker Desktop 内提供快速灵活的主机到 VM 文件共享。利用 [Docker 收购 Mutagen](https://www.docker.com/blog/mutagen-acquisition/) 背后的技术，此功能提供了虚拟绑定挂载的替代方案，使用同步文件系统缓存，为处理大型代码库的开发人员提高了性能。
- 组织管理员现在可以在启用 ECI 时[配置 Docker 套接字挂载权限](/manuals/enterprise/security/hardened-desktop/enhanced-container-isolation/config.md)。
- [Containerd 镜像存储](/manuals/desktop/features/containerd.md) 支持现已对所有用户正式可用。
- 使用新的 [`docker debug` 命令](/reference/cli/docker/debug.md)（Beta）获取任何容器或镜像的调试 shell。
- 拥有 Docker Business 订阅的组织管理员现在可以使用[私有扩展市场](/manuals/extensions/private-marketplace.md) 配置自定义扩展列表（Beta）。

### 升级

- [Amazon ECR Credential Helper v0.7.1](https://github.com/awslabs/amazon-ecr-credential-helper/releases/tag/v0.7.1)
- [Buildx v0.12.1](https://github.com/docker/buildx/releases/tag/v0.12.1)
- [Containerd v1.6.27](https://github.com/containerd/containerd/releases/tag/v1.6.27)
- [Compose v2.24.3](https://github.com/docker/compose/releases/tag/v2.24.3)
- [Docker Credential Helpers v0.8.1](https://github.com/docker/docker-credential-helpers/releases/tag/v0.8.1)
- [Runc v1.1.11](https://github.com/opencontainers/runc/releases/tag/v1.1.11)
- [Docker Engine v25.0.0](https://docs.docker.com/engine/release-notes/25.0/)
- [Kubernetes v1.29.1](https://github.com/kubernetes/kubernetes/releases/tag/v1.29.1)
- [Docker Scout v1.3.0](https://github.com/docker/scout-cli/releases/tag/v1.3.0)

### 错误修复和增强功能

#### 所有平台

- `docker scan` 命令已被移除。要继续了解镜像的漏洞以及许多其他功能，请使用 [`docker scout` 命令](/reference/cli/docker/scout/_index.md)。
- 修复了当选择 **始终下载更新** 复选框时自动更新不会下载的错误。
- 修复了仪表板工具提示中的拼写错误。修复 [docker/for-mac#7132](https://github.com/docker/for-mac/issues/7132)
- 改进了信号处理行为（例如，在运行 `docker` 命令时在终端中按 Ctrl-C）。
- 重新添加了 `minikube start --cni=cilium` 所需的内核模块。
- 修复了在启用管理员控制后登录时安装屏幕会再次出现的错误。
- 修复了如果共享文件夹不再存在 Docker 将无法启动的错误。
- 修复了仪表板 **容器** 部分中显示的可用 CPU 数量。
- 重新添加了 `btrfs`、`xfs`、`vfat`、`exfat`、`ntfs3`、`f2fs`、`squashfs`、`udf`、`9p` 和 `autofs` 的内核模块。
- 容器使用情况图表已移至垂直的 **资源使用情况** 侧面板，以在容器列表中留出更多空间。通过 **显示图表** 按钮访问使用情况图表保持不变。
- 修复了在登录时选择 **关闭应用程序** 会留下挂起的后端进程的错误。
- 修复了当通过设置管理禁用分析时导致 Docker Desktop 变得无响应的错误。
- Docker Init：
  - 添加了对容器化 Java 服务器的支持
  - Windows 上的各种修复
- 构建器设置：
  - 您现在可以随时刷新构建器的存储数据。
  - 您现在可以删除构建器的构建历史记录。
- 构建视图：
  - 当无法删除构建记录时，现在会显示错误消息。
  - 修复了在 macOS 上的无根模式下无法创建云构建器的问题。
  - 内联缓存和 Git 源现在在 **信息** 选项卡的 **构建时间** 部分得到正确处理。
  - 现在在 **历史记录** 选项卡上的过去构建中显示使用的构建器和调用构建的作者。
  - 对更好地链接 **历史记录** 选项卡上的过去构建进行了多项改进。
  - 对使构建名称更准确进行了多项改进。
  - 修复了当构建器无法访问时，**活动构建** 列表中卡住的构建。
  - 修复了在某些情况下无法删除构建记录的问题。
  - 修复了构建名称可能为空的问题。
  - 修复了启用资源节省模式时构建视图的常规问题。

#### Mac

- 启用了 `Huge Pages` 并修复了 Rosetta 下的 PHP 分段错误。修复 [docker/for-mac#7117](https://github.com/docker/for-mac/issues/7117)。
- 修复了 Rosetta 下的 `xvfb`。修复 [docker/for-mac#7122](https://github.com/docker/for-mac/issues/7122)
- 修复了 Rosetta 下的 `ERR_WORKER_INVALID_EXEC_ARGV` 错误。[docker/for-mac#6998](https://github.com/docker/for-mac/issues/6998)。
- 修复了当 `admin-settings.json` 语法无效时 Docker Desktop 可能死锁的错误。

#### Windows

- 修复了在某些区域设置中无法将 UTF-16 字符串编码为 UTF-8 的错误。修复 [docker/for-win#13868](https://github.com/docker/for-win/issues/13868)。
- 修复了在应用程序重启时使用 WSL 集成时凭证存储配置会重置的错误。修复 [docker/for-win#13529](https://github.com/docker/for-win/issues/13529)。
- 修复了阻止正确的 WSL 引擎错误传播给用户的问题。
- 修复了在退出 Windows 容器模式时导致 Docker Desktop 挂起的问题。

### 安全性

#### Windows

- 缓解了 Windows 版 Docker Desktop 安装程序中的多个 DLL 侧加载漏洞，由 Suman Kumar Chakraborty ([@Hijack-Everything](https://github.com/Hijack-Everything)) 报告

### 已知问题

#### 所有平台

- 使用设置管理时，未在 `admin-settings.json` 中设置的设置将在 Docker Desktop 启动时重置为默认值。

#### Mac

- 从 **软件更新** 更新到 4.27.0 有时会挂起。作为解决方法，请使用此页面上的 4.27.0 安装程序。

## 4.26.1

{{< release-date date="2023-12-14" >}}

### 错误修复和增强功能

#### 所有平台

- 更新了 Docker Desktop 内部的反馈链接以确保它们继续正常工作

#### Windows

- 将 CLI 二进制文件切换到与旧版 glibc（例如 Ubuntu 20.04 中使用的）兼容的版本，修复 [docker/for-win#13824](https://github.com/docker/for-win/issues/13824)

## 4.26.0

{{< release-date date="2023-12-04" >}}

### 新增功能

- 管理员现在可以使用[设置管理](/manuals/enterprise/security/hardened-desktop/settings-management/_index.md) 控制 **开发中功能** 选项卡中对 Beta 和实验性功能的访问。
- 在页脚引入了四种新的版本更新状态。
- `docker init` (Beta) 现在支持带有 Apache + Composer 的 PHP。
- [**构建** 视图](use-desktop/builds.md) 现已 GA。您现在可以检查构建、排查错误并优化构建速度。

### 升级

- [Compose v2.23.3](https://github.com/docker/compose/releases/tag/v2.23.3)
- [Docker Scout CLI v1.2.0](https://github.com/docker/scout-cli/releases/tag/v1.2.0).
- [Buildx v0.12.0](https://github.com/docker/buildx/releases/tag/v0.12.0)
- [Wasm](/manuals/desktop/features/wasm.md) 运行时：
  - wasmtime、wasmedge 和 wasmer `v0.3.1`。
  - lunatic、slight、spin 和 wws `v0.10.0`。
  - Wasmtime 现在基于 wasmtime `v14.0` 并支持 wasi preview-2 组件
  - Wasmedge 现在基于 WasmEdge `v0.13.5`
  - Spin 现在基于 Spin `v2.0.1`
  - wws 现在基于 wws `v1.7.0`
- [Docker Engine v24.0.7](https://docs.docker.com/engine/release-notes/24.0/#2407)
- [Containerd v1.6.25](https://github.com/containerd/containerd/releases/tag/v1.6.25)
- [runc v1.1.10](https://github.com/opencontainers/runc/releases/tag/v1.1.10)

### 错误修复和增强功能

#### 所有平台

- 您现在可以使用 `docker feedback` 从命令行提供反馈。
- 改进了 **常规** 设置选项卡中启动选项的文本和位置。
- 重新设计了仪表板的标题栏，添加了指向其他 Docker 资源的链接，改进了帐户信息的显示。
- 修复了同时启用 containerd 镜像存储和 Wasm 时无法启用 Wasm 的错误。
- containerd 集成：
  - 修复了在未提供 `ServerAddress` 的情况下，`docker push/pull` 身份验证未发送到非 DockerHub 注册表的问题。
  - 修复了 `docker history` 报告错误 ID 和标签的问题。
  - 修复了 `docker tag` 未保留内部元数据的问题。
  - 修复了在守护程序配置为 `--userns-remap` 时 `docker commit` 的问题。
  - 修复了 `docker image list` 以显示真实的镜像创建日期。
  - 为 `docker pull` 添加了对 `-a` 标志的支持（拉取所有远程存储库标签）。
  - 为 `docker run` 添加了对 `--group-add` 标志的支持（追加额外组）。
  - 调整了 `docker push/pull` 报告的一些错误。
- Docker Init：
  - 改进了 Golang 和 Rust 的 Dockerfile 中的交叉编译。
  - 改进了 ASP.NET Core 的 Dockerfile 缓存。
- Docker Desktop 现在在仪表板页脚提供有关待处理更新的更详细信息。
- 修复了增强容器隔离模式下 `docker run --init` 失败的错误。
- 修复了当用户开始下载新版本的 Docker Desktop 后，提示用户下载新版本的通知仍保持可见的错误。
- 添加了一个通知，指示 Docker Desktop 何时正在安装新版本。
- 修复了当用户将鼠标悬停在没有调用操作的通知上时，光标变为指针的错误。

#### Mac

- 修复了 Rosetta 无法与 PHP 一起工作的问题。修复 [docker/for-mac#6773](https://github.com/docker/for-mac/issues/6773) 和 [docker/for-mac#7037](https://github.com/docker/for-mac/issues/7037)。
- 修复了 Rosetta 不工作的多个问题。修复 [[docker/for-mac#6973](https://github.com/docker/for-mac/issues/6973), [[docker/for-mac#7009](https://github.com/docker/for-mac/issues/7009), [[docker/for-mac#7068](https://github.com/docker/for-mac/issues/7068) 和 [[docker/for-mac#7075](https://github.com/docker/for-mac/issues/7075)
- 改进了 NodeJS 在 Rosetta 下的性能。
- 修复了 **无法打开 /proc/self/exe** Rosetta 错误。
- 修复了 **登录时启动 Docker Desktop** 设置不起作用的错误。修复 [docker/for-mac#7052](https://github.com/docker/for-mac/issues/7052)。
- 您现在可以通过 UI 启用 UDP 的内核网络路径使用。修复 [docker/for-mac#7008](https://github.com/docker/for-mac/issues/7008)。
- 修复了 `uninstall` CLI 工具缺失的回归问题。
- 解决了在通过设置管理禁用分析时导致 Docker Desktop 变得无响应的问题。

#### Windows

- 添加了对 WSL 镜像模式网络的支持（需要 WSL `v2.0.4` 及更高版本）。
- 添加了 DLL 和 VBS 文件缺少的签名。

### 已知问题

#### Windows

- 在较旧的 Linux 发行版（例如 Ubuntu 20.04）上使用 WSL 2 集成时，Docker CLI 不起作用，这些发行版使用的 `glibc` 版本早于 `2.32`。这将在未来的版本中修复。请参阅 [docker/for-win#13824](https://github.com/docker/for-win/issues/13824)。

## 4.25.2

{{< release-date date="2023-11-21" >}}

### 错误修复和增强功能

#### 所有平台

- 修复了在 **欢迎调查** 中提交响应后出现空白 UI 的错误。

#### Windows

- 修复了在 WSL 2 上 Docker Desktop 在空闲时意外关闭 dockerd 的错误。修复 [docker/for-win#13789](https://github.com/docker/for-win/issues/13789)

## 4.25.1

{{< release-date date="2023-11-13" >}}

### 错误修复和增强功能

#### 所有平台

- 修复了 4.25 中的回归问题，如果交换文件损坏，Docker 将无法启动。损坏的交换文件将在下次启动时重新创建。
- 修复了交换被禁用时的错误。修复 [docker/for-mac#7045](https://github.com/docker/for-mac/issues/7045), [docker/for-mac#7044](https://github.com/docker/for-mac/issues/7044) 和 [docker/for-win#13779](https://github.com/docker/for-win/issues/13779)。
- `sysctl vm.max_map_count` 现在设置为 262144。请参阅 [docker/for-mac#7047](https://github.com/docker/for-mac/issues/7047)

#### Windows

- 修复了 **切换到 Windows 容器** 不会出现在某些用户的托盘菜单中的问题。请参阅 [docker/for-win#13761](https://github.com/docker/for-win/issues/13761)。
- 修复了当用户使用 `sh` 以外的 shell 时 WSL 集成不起作用的错误。请参阅 [docker/for-win#13764](https://github.com/docker/for-win/issues/13764)。
- 重新添加了 `DockerCli.exe`。

## 4.25.0

{{< release-date date="2023-10-26" >}}

### 新增功能

- Rosetta 现已对 macOS 13 或更高版本的所有用户正式可用。它在 Apple Silicon 上提供更快的 Intel 镜像仿真。要使用 Rosetta，请参阅[设置](/manuals/desktop/settings-and-maintenance/settings.md)。在 macOS 14.1 及更高版本上默认启用 Rosetta。
- Docker Desktop 现在检测 WSL 版本是否过时。如果检测到过时的 WSL 版本，您可以允许 Docker Desktop 自动更新安装，也可以在 Docker Desktop 外手动更新 WSL。
- Windows 上的 Docker Desktop 新安装现在需要 Windows 版本 19044 或更高版本。
- 管理员现在可以在[设置管理](/manuals/enterprise/security/hardened-desktop/settings-management/_index.md) 中控制 Docker Scout 镜像分析。

### 升级

- [Compose v2.23.0](https://github.com/docker/compose/releases/tag/v2.23.0)
- [Docker Scout CLI v1.0.9](https://github.com/docker/scout-cli/releases/tag/v1.0.9).
- [Kubernetes v1.28.2](https://github.com/kubernetes/kubernetes/releases/tag/v1.28.2)
  - [cri-dockerd v0.3.4](https://github.com/Mirantis/cri-dockerd/releases/tag/v0.3.4)
  - [CNI plugins v1.3.0](https://github.com/containernetworking/plugins/releases/tag/v1.3.0)
  - [cri-tools v1.28.0](https://github.com/kubernetes-sigs/cri-tools/releases/tag/v1.28.0)

### 错误修复和增强功能

#### 所有平台

- 修复了 `接受许可` 弹出窗口中的间距问题。
- 修复了在 **通知列表** 和 **通知详细信息** 视图之间导航时 **通知抽屉** 大小会改变的错误。
- containerd 集成：
  - `docker push` 现在支持 `Layer already exists` 和 `Mounted from` 进度状态。
  - `docker save` 现在能够导出存储库所有标签的镜像。
  - 隐藏清单、配置和索引（小的 json blob）的推送上传进度，以匹配原始推送行为。
  - 修复了 `docker diff` 包含额外差异的问题。
  - 修复了 `docker history` 未显示使用经典构建器构建的镜像的中间镜像 ID 的问题。
  - 修复了 `docker load` 无法从压缩的 tar 存档加载镜像的问题。
  - 修复了注册表镜像不起作用的问题。
  - 修复了当为同一容器多次并发调用 `docker diff` 时无法正常工作的问题。
  - 修复了 `docker push` 在将层推送到同一注册表上的不同存储库时未重用层的问题。
- Docker Init：
  - 修复了生成文件中包含的过时 Docker 文档链接
  - 添加了对 ASP.NET Core 8 的支持（除了 6 和 7）
- 修复了安装 Wasm shim 时导致失败的错误。
- 修复了 Docker Desktop 每 15 分钟退出一次[资源节省模式](https://docs.docker.com/desktop/use-desktop/resource-saver/)，或者如果计时器设置为超过 15 分钟，资源节省模式永远不会启动的错误。
- 将 **启用后台 SBOM 索引** 选项提升到 **常规设置**。

#### Mac

- 在 macOS 上安装或更新 Docker Desktop 的最低操作系统版本现在是 macOS Monterey（版本 12）或更高版本。
- 当用户与 `Docker.app` 的所有者不匹配时，如果更新无法完成，则增强了错误消息。修复 [docker/for-mac#7000](https://github.com/docker/for-mac/issues/7000)。
- 修复了当 `/var/run/docker.sock` 配置错误时 **重新应用配置** 可能不起作用的错误。
- 如果 `/usr/local/bin` 中已存在，Docker Desktop 不会覆盖 `ECRCredentialHelper`。

#### Windows

- 修复了 **切换到 Windows 容器** 选项在 Windows 家庭版上显示在托盘菜单中的问题。修复 [docker/for-win#13715](https://github.com/docker/for-win/issues/13715)

#### Linux

- 修复了 `docker login` 中的错误。修复 [docker/docker-credential-helpers#299](https://github.com/docker/docker-credential-helpers/issues/299)

### 已知问题

#### Mac

- 升级到 MacOS 14 可能会导致 Docker Desktop 也更新到最新版本，即使自动更新选项已禁用。
- 无法从命令行卸载 Docker Desktop。作为解决方法，您可以[从仪表板卸载 Docker Desktop](https://docs.docker.com/desktop/uninstall/)。

#### Windows

- 托盘菜单中的 **切换到 Windows 容器** 选项可能不会在 Windows 上显示。作为解决方法，请编辑 [`settings.json` 文件](/manuals/desktop/settings-and-maintenance/settings.md) 并设置 `"displaySwitchWinLinContainers": true`。

#### 所有平台

- 如果交换文件大小设置为 0MB，Docker 操作（例如拉取镜像或登录）会失败并出现“连接被拒绝”或“超时”错误。作为解决方法，请在 **设置** 的 **资源** 选项卡中将交换文件大小配置为非零值。

## 4.24.2

{{< release-date date="2023-10-12" >}}

### 错误修复和增强功能

#### 所有平台

- 修复了 Docker Desktop 会向 `notify.bugsnag.com` 发送多个请求的错误。修复 [docker/for-win#13722](https://github.com/docker/for-win/issues/13722)。
- 修复了 PyTorch 的性能回归问题。

## 4.24.1

{{< release-date date="2023-10-04" >}}

### 错误修复和增强功能

#### Windows

- 修复了 Windows 版 Docker Desktop 中 Docker Desktop 仪表板无法正确显示容器日志的错误。修复 [docker/for-win#13714](https://github.com/docker/for-win/issues/13714)。

## 4.24.0

{{< release-date date="2023-09-28" >}}

### 新增功能

- 新的通知中心现已对所有用户开放，因此您可以收到有关新版本、安装进度更新等的通知。选择 Docker Desktop 仪表板右下角的铃铛图标即可访问通知中心。
- Compose Watch 现已对所有用户可用。更多信息，请参阅[使用 Compose Watch](/manuals/compose/how-tos/file-watch.md)。
- 资源节省模式现已对所有用户可用，并默认启用。要配置此功能，请导航到 **设置** 中的 **资源** 选项卡。有关更多信息，请参阅 [Docker Desktop 的资源节省模式](use-desktop/resource-saver.md)。
- 您现在可以直接从 Docker Desktop 仪表板查看和管理 Docker Engine 状态，包括暂停、停止和恢复。

### 升级

- [Compose v2.22.0](https://github.com/docker/compose/releases/tag/v2.22.0)
- [Go 1.21.1](https://github.com/golang/go/releases/tag/go1.21.1)
- [Wasm](/manuals/desktop/features/wasm.md) 运行时：
  - wasmtime、wasmedge `v0.2.0`。
  - lunatic、slight、spin 和 wws`v0.9.1`。
  - 添加了 wasmer wasm shim。


### 错误修复和增强功能

#### 所有平台

- Docker Init：
  - 修复了在 Windows 上为 ASP.NET 项目格式化 Dockerfile 文件路径的问题。
  - 改进了对包含大量文件的大型目录进行语言检测的性能。
- 为 **容器** 视图使用的资源使用统计轮询添加了超时。修复 [docker/for-mac#6962](https://github.com/docker/for-mac/issues/6962)。
- containerd 集成：
  - 实现了推送/拉取/保存镜像事件。
  - 实现了拉取旧式 schema1 镜像。
  - 实现了 `docker push --all-tags`。
  - 实现了计算使用特定镜像的容器（例如在 `docker system df -v` 中可见）。
  - 验证拉取的镜像名称是否未被保留。
  - 处理 `userns-remap` 守护程序设置。
  - 修复了在使用多个 COPY/ADD 指令时旧式构建器构建错误的问题。
  - 修复了 `docker load` 导致池损坏的问题，这可能会影响后续的镜像相关操作。
  - 修复了无法通过带有 `sha256:` 前缀的截断摘要引用镜像的问题。
  - 修复了 `docker images`（不带 `--all`）显示中间层（由旧式经典构建器创建）的问题。
  - 修复了 `docker diff` 包含额外差异的问题。
  - 更改了 `docker pull` 输出，以匹配禁用 containerd 集成时的输出。
- 修复了 Kubernetes 状态消息中的语法错误。请参阅 [docker/for-mac#6971](https://github.com/docker/for-mac/issues/6971)。
- Docker 容器现在默认使用所有主机 CPU 核心。
- 改进了仪表板 UI 中的进程间安全性。

#### Mac

- 修复了在早于 12.5 的 macOS 版本的 Apple Silicon Mac 上的内核恐慌问题。修复 [docker/for-mac#6975](https://github.com/docker/for-mac/issues/6975)。
- 修复了当 `filesharingDirectories` 中包含无效目录时 Docker Desktop 无法启动的错误。修复 [docker/for-mac#6980](https://github.com/docker/for-mac/issues/6980)。
- 修复了安装程序创建 root 拥有的目录的错误。修复 [docker/for-mac#6984](https://github.com/docker/for-mac/issues/6984)。
- 修复了当缺少 `/Library/LaunchDaemons` 时安装程序在设置 docker 套接字时失败的错误。修复 [docker/for-mac#6967](https://github.com/docker/for-mac/issues/6967)。
- 修复了在 macOS 上将特权端口绑定到非 localhost IP 时出现权限被拒绝的错误。修复 [docker/for-mac#697](https://github.com/docker/for-mac/issues/6977)。
- 修复了 4.23 中引入的资源泄漏。与 [docker/for-mac#6953](https://github.com/docker/for-mac/issues/6953) 相关。

#### Windows

- 修复了当服务已在运行时出现“Docker Desktop 服务未运行”弹出窗口的错误。请参阅 [docker/for-win#13679](https://github.com/docker/for-win/issues/13679)。
- 修复了导致 Docker Desktop 在 Windows 主机上无法启动的错误。修复 [docker/for-win#13662](https://github.com/docker/for-win/issues/13662)。
- 修改了 Docker Desktop 资源节省功能，以在 WSL 上没有容器运行时跳过减少内核内存，因为在某些情况下这会导致超时。相反，鼓励用户通过 .wslconfig 文件直接在 WSL 上启用 "autoMemoryReclaim"（自 WSL 1.3.10 起可用）。

### 已知问题

#### Mac

- 创建端口为 53 的容器会失败并出现地址 `already in use` 错误。作为解决方法，请通过在 `~/Library/Group Containers/group.com.docker/settings.json` 中的 `settings.json` 文件中添加 `"kernelForUDP": false` 来停用网络加速。

## 4.23.0

{{< release-date date="2023-09-11" >}}

### 升级

- [Compose v2.21.0](https://github.com/docker/compose/releases/tag/v2.21.0)
- [Docker Engine v24.0.6](https://docs.docker.com/engine/release-notes/24.0/#2406)
- [Docker Scout CLI v0.24.1](https://github.com/docker/scout-cli/releases/tag/v0.24.1).
- [Wasm](/manuals/desktop/features/wasm.md) 运行时：
  - wasmtime、wasmedge 修订版 `d0a1a1cd`。
  - slight 和 spin wasm `v0.9.0`。

### 新增功能

- 添加了对新 Wasm 运行时的支持：wws 和 lunatic。
- [`docker init`](/reference/cli/docker/init.md) 现在支持 ASP.NET
- 提高了 macOS 上暴露端口的性能，例如使用 `docker run -p`。

### 移除

- 从 Docker Desktop 中移除了 Compose V1，因为它已停止接收更新。Compose V2 已取代它，并已集成到所有当前的 Docker Desktop 版本中。

### 错误修复和增强功能

#### 所有平台

- 使用 [Docker Scout](../scout/_index.md)，您现在可以：
  - 使用 `docker scout cache` 管理临时文件和缓存文件。
  - 使用 `docker scout environment` 管理环境。
  - 使用 `docker scout config` 配置默认组织。
  - 使用 `docker scout cves --format only-packages` 列出镜像的包及其漏洞。
  - 使用 `docker scout enroll` 注册组织以使用 Docker scout。
  - 使用 `docker scout cves --type fs` 停止、分析和比较本地文件系统。
- 修复了当 Docker Desktop 处于资源节省模式时 `docker stats` 会挂起的错误。
- 修复了通过 Docker Desktop 仪表板中的 **设置** 关闭实验性功能无法完全关闭资源节省模式的错误。
- 修复了 **容器列表** 操作按钮被裁剪的错误。
- containerd 镜像存储：
  - 修复了与某些镜像交互时出现 `failed to read config content` 错误的问题。
  - 修复了使用旧式经典构建器 (`DOCKER_BUILDKIT=0`) 构建带有 `FROM scratch` 指令的 Dockerfile 的问题。
  - 修复了使用旧式经典构建器 (`DOCKER_BUILDKIT=0`) 构建镜像时出现 `mismatched image rootfs errors` 的问题。
  - 修复了 `ONBUILD` 和 `MAINTAINER` Dockerfile 指令
  - 修复了健康检查。

#### Mac

- macOS 12.5 或更高版本的所有用户现在默认启用 VirtioFS。您可以在 **常规** 选项卡的 **设置** 中恢复此设置。
- 改进了单流 TCP 吞吐量。
- 恢复了 macOS 的健康检查，如果系统上发生可能导致运行 Docker 二进制文件出现问题的更改，会通知您。

#### Linux

- 修复了在打开 Docker Desktop 应用程序两次时 GUI 被终止的错误。请参阅 [docker/desktop-linux#148](https://github.com/docker/desktop-linux/issues/148)。

#### Windows

- 修复了当非管理员用户切换到 Windows 容器或禁用 WSL 并切换到 Hyper-V 引擎时，会提示输入凭据的错误。
  此问题会在操作系统重启后或 Docker Desktop 冷启动时发生。

### 安全性

#### 所有平台

- 修复了 [CVE-2023-5165](https://www.cve.org/cverecord?id=CVE-2023-5165)，该问题允许通过调试 shell 绕过增强容器隔离。受影响的功能仅适用于 Docker Business 客户，并假设用户未被授予本地 root 或管理员权限的环境。
- 修复了 [CVE-2023-5166](https://www.cve.org/cverecord?id=CVE-2023-5166)，该问题允许通过精心制作的扩展图标 URL 窃取访问令牌。

### 已知问题

- 在 Docker Desktop 上绑定特权端口在 macOS 上不起作用。作为解决方法，您可以使用 `0.0.0.0` 将端口暴露到所有接口，或使用 `127.0.0.1` 使用 localhost。

## 4.22.1

{{< release-date date="2023-08-24" >}}

### 错误修复和增强功能

#### 所有平台

- 缓解了影响 Docker Desktop 启动和资源节省模式的多个问题。[docker/for-mac#6933](https://github.com/docker/for-mac/issues/6933)

#### Windows

- 修复了 Windows 上的 **清理/清除数据** 故障排除选项。[docker/for-win#13630](https://github.com/docker/for-win/issues/13630)

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

- [资源使用情况](use-desktop/container.md) 已从实验性移至 GA。
- 您现在可以使用 [`include`](/manuals/compose/how-tos/multiple-compose-files/include.md) 将大型 Compose 项目拆分为多个子项目。

### 错误修复和增强功能

#### 所有平台

- [设置管理](/manuals/enterprise/security/hardened-desktop/settings-management/_index.md) 现在允许您为组织关闭 Docker 扩展。
- 修复了当系统暂停时从 UI 开启 Kubernetes 失败的错误。
- 修复了当系统暂停时从 UI 开启 Wasm 失败的错误。
- 绑定挂载现在在您[检查容器](use-desktop/container.md)时显示。
- 当启用 containerd 镜像存储时，您现在可以下载 Wasm 运行时。
- 使用[快速搜索](/manuals/desktop/use-desktop/_index.md#quick-search)，您现在可以：
  - 查找驻留在本地系统上的任何容器或 Compose 应用。此外，您可以访问环境变量并执行基本操作，例如启动、停止或删除容器。
  - 查找公共 Docker Hub 镜像、本地镜像或来自远程存储库的镜像。
  - 发现有关特定扩展的更多信息并安装它们。
  - 浏览您的卷并获取有关关联容器的见解。
  - 搜索并访问 Docker 的文档。

#### Mac

- 修复了阻止 Docker Desktop 启动的错误。[docker/for-mac#6890](https://github.com/docker/for-mac/issues/6890)
- 资源节省模式现已在 Mac 上可用。当没有容器运行时，它会优化 Docker Desktop 对系统资源的使用。要访问此功能，请确保您已在设置中[开启了对实验性功能的访问](/manuals/desktop/settings-and-maintenance/settings.md)。

#### Windows

- 修复了当 vpnkit 预期不运行时自诊断工具显示误报失败的错误。修复 [docker/for-win#13479](https://github.com/docker/for-win/issues/13479)。
- 修复了搜索栏中无效正则表达式导致错误的错误。修复 [docker/for-win#13592](https://github.com/docker/for-win/issues/13592)。
- 资源节省模式现已在 Windows Hyper-V 上可用。当没有容器运行时，它会优化 Docker Desktop 对系统资源的使用。要访问此功能，请确保您已在设置中[开启了对实验性功能的访问](/manuals/desktop/settings-and-maintenance/settings.md)。

## 4.21.1

{{< release-date date="2023-07-03" >}}

#### 所有平台

- 修复了使用 SSH 的 Docker 上下文的连接泄漏 ([docker/for-mac#6834](https://github.com/docker/for-mac/issues/6834) 和 [docker/for-win#13564](https://github.com/docker/for-win/issues/13564))

#### Mac

- 移除了配置健康检查以进行进一步调查和解决特定设置问题。

## 4.21.0

{{< release-date date="2023-06-29" >}}

### 新增功能

- 添加了对新 Wasm 运行时的支持：slight、spin 和 wasmtime。当启用 containerd 镜像存储时，用户可以按需下载 Wasm 运行时。
- 为 Docker init 添加了 Rust 服务器支持。
- [**构建** 视图](use-desktop/builds.md) 的 Beta 版发布，允许您检查构建和管理构建器。这可以在 **设置** 中的 **开发中功能** 选项卡中找到。

### 升级

- [Buildx v0.11.0](https://github.com/docker/buildx/releases/tag/v0.11.0)
- [Compose v2.19.0](https://github.com/docker/compose/releases/tag/v2.19.0)
- [Kubernetes v1.27.2](https://github.com/kubernetes/kubernetes/releases/tag/v1.27.2)
- [cri-tools v1.27.0](https://github.com/kubernetes-sigs/cri-tools/releases/tag/v1.27.0)
- [cri-dockerd v0.3.2](https://github.com/Mirantis/cri-dockerd/releases/tag/v0.3.2)
- [coredns v1.10.1](https://github.com/coredns/coredns/releases/tag/v1.10.1)
- [cni v1.2.0](https://github.com/containernetworking/plugins/releases/tag/v1.2.0)
- [etcd v3.5.7](https://github.com/etcd-io/etcd/releases/tag/v3.5.7)

### 错误修复和增强功能

#### 所有平台

- Docker Desktop 现在会在 Docker Engine 不使用时自动暂停，并在需要时唤醒。
- VirtioFS 现在是 macOS 12.5 及更高版本上 Docker Desktop 新安装的默认文件共享实现。
- 改进了使用 OpenTelemetry 的产品使用情况报告（实验性）。
- 修复了 Docker 套接字权限。修复 [docker/for-win#13447](https://github.com/docker/for-win/issues/13447) 和 [docker/for-mac#6823](https://github.com/docker/for-mac/issues/6823)。
- 修复了在暂停状态下退出应用程序时导致 Docker Desktop 挂起的问题。
- 修复了导致 **容器** 视图中的 **日志** 和 **终端** 选项卡内容被固定工具栏覆盖的错误 [docker/for-mac#6814](https://github.com/docker/for-mac/issues/6814)。
- 修复了在容器运行对话框中输入标签与输入值重叠的错误。修复 [docker/for-win#13304](https://github.com/docker/for-win/issues/13304)。
- 修复了用户无法选择 Docker 扩展菜单的错误。修复 [docker/for-mac#6840](https://github.com/docker/for-mac/issues/6840) 和 [docker/for-mac#6855](https://github.com/docker/for-mac/issues/6855)

#### Mac

- 添加了 macOS 健康检查，如果系统上发生可能导致运行 Docker 二进制文件出现问题的更改，会通知用户。

#### Windows

- 修复了 WSL 2 上的一个错误，即如果 Desktop 被暂停、终止然后重新启动，除非先使用 `wsl --shutdown` 关闭 WSL，否则启动会挂起。
- 修复了当 wsl.exe 不在 PATH 中时 WSL 引擎的问题 [docker/for-win#13547](https://github.com/docker/for-win/issues/13547)。
- 修复了 WSL 引擎检测 Docker Desktop 发行版驱动器缺失的情况的能力 [docker/for-win#13554](https://github.com/docker/for-win/issues/13554)。
- 缓慢或无响应的 WSL 集成不再阻止 Docker Desktop 启动。修复 [docker/for-win#13549](https://github.com/docker/for-win/issues/13549)。
- 修复了导致 Docker Desktop 在启动时崩溃的错误 [docker/for-win#6890](https://github.com/docker/for-mac/issues/6890)。
- 添加了以下安装程序标志：
  - `--hyper-v-default-data-root` 指定 Hyper-V VM 磁盘的默认位置。
  - `--windows-containers-default-data-root` 指定 Windows 容器的默认数据根目录。
  - `--wsl-default-data-root` 指定 WSL 发行版磁盘的默认位置。

## 4.20.1

{{< release-date date="2023-06-05" >}}

### 错误修复和增强功能

#### 所有平台

- containerd 镜像存储：修复了在加载包含证明的镜像时 `docker load` 失败的错误。
- containerd 镜像存储：修复了构建期间的默认镜像导出器。

#### Windows

- 修复了在非西方语言环境中难以解析主机上 WSL 版本的错误。修复 [docker/for-win#13518](https://github.com/docker/for-win/issues/13518) 和 [docker/for-win#13524](https://github.com/docker/for-win/issues/13524)。

## 4.20.0

{{< release-date date="2023-05-30" >}}

### 升级

- [Buildx v0.10.5](https://github.com/docker/buildx/releases/tag/v0.10.5)
- [Compose v2.18.1](https://github.com/docker/compose/releases/tag/v2.18.1)
- [Docker Engine v24.0.2](https://docs.docker.com/engine/release-notes/24.0/#2402)
- [Containerd v1.6.21](https://github.com/containerd/containerd/releases/tag/v1.6.21)
- [runc v1.1.7](https://github.com/opencontainers/runc/releases/tag/v1.1.5)

### 错误修复和增强功能

#### 所有平台

- [Docker Scout CLI](https://docs.docker.com/scout/#docker-scout-cli) 现在会查找最近构建的镜像（如果未作为参数提供）。
- 改进了 [Docker Scout CLI](https://docs.docker.com/scout/#docker-scout-cli) `compare` 命令。
- 添加了关于 [2023 年 11 月 Docker Compose ECS/ACS 集成退役](https://docs.docker.com/go/compose-ecs-eol/) 的警告。可以使用 `COMPOSE_CLOUD_EOL_SILENT=1` 抑制。
- 修复了 HTTP 代理错误，即 HTTP 1.0 客户端可能收到 HTTP 1.1 响应。
- 在 WSL-2 上启用了 Docker Desktop 的增强容器隔离 (ECI) 功能。这需要 Docker Business 订阅。
- 修复了 **容器** 表中的一个错误，即在全新安装 Docker Desktop 后，先前隐藏的列会再次显示。

#### Mac

- 当在容器中删除文件时，您现在可以更快地回收磁盘空间。与 [docker/for-mac#371](https://github.com/docker/for-mac/issues/371) 相关。
- 修复了阻止容器访问 169.254.0.0/16 IP 的错误。修复 [docker/for-mac#6825](https://github.com/docker/for-mac/issues/6825)。
- 修复了 `com.docker.diagnose check` 中的错误，即使 vpnkit 预期不运行，它也会抱怨缺少 vpnkit。与 [docker/for-mac#6825](https://github.com/docker/for-mac/issues/6825) 相关。

#### Windows

- 修复了无法将 WSL 数据移动到不同磁盘的错误。修复 [docker/for-win#13269](https://github.com/docker/for-win/issues/13269)。
- 修复了在关闭时 Docker Desktop 未停止其 WSL 发行版（docker-desktop 和 docker-desktop-data）的错误，不必要地消耗主机内存。
- 添加了一个新设置，允许 Windows Docker 守护程序在运行 Windows 容器时使用 Docker Desktop 的内部代理。请参阅 [Windows 代理设置](/manuals/desktop/settings-and-maintenance/settings.md#proxies)。

#### Linux

- 修复了 Docker Compose V1/V2 兼容性设置的问题。

## 4.19.0

{{< release-date date="2023-04-27" >}}

### 新增功能

- Docker Engine 和 CLI 更新至 [Moby 23.0](https://github.com/moby/moby/releases/tag/v23.0.0)。
- **学习中心** 现在支持产品内演练。
- Docker init (Beta) 现在支持 Node.js 和 Python。
- macOS 上 VM 和主机之间的网络连接速度更快。
- 您现在可以在不拉取的情况下检查和分析来自 Docker Desktop 的远程镜像。
- **Artifactory 镜像** 视图的可用性和性能改进。

### 移除

- 移除了 `docker scan` 命令。要继续了解镜像的漏洞以及许多其他功能，请使用新的 `docker scout` 命令。运行 `docker scout --help`，或[阅读文档以了解更多信息](/reference/cli/docker/scout/_index.md)。

### 升级

- [Docker Engine v23.0.5](https://docs.docker.com/engine/release-notes/23.0/#2305)
- [Compose 2.17.3](https://github.com/docker/compose/releases/tag/v2.17.3)
- [Containerd v1.6.20](https://github.com/containerd/containerd/releases/tag/v1.6.20)
- [Kubernetes v1.25.9](https://github.com/kubernetes/kubernetes/releases/tag/v1.25.9)
- [runc v1.1.5](https://github.com/opencontainers/runc/releases/tag/v1.1.5)
- [Go v1.20.3](https://github.com/golang/go/releases/tag/go1.20.3)

### 错误修复和增强功能

#### 所有平台

- 改进了 `docker scout compare` 命令以比较两个镜像，现在也别名为 `docker scout diff`。
- 当 `docker-compose` 操作失败时，为仪表板错误添加了更多详细信息 ([docker/for-win#13378](https://github.com/docker/for-win/issues/13378))。
- 添加了在安装期间设置 HTTP 代理配置的支持。这可以通过安装程序标志 `--proxy-http-mode`、`--overrider-proxy-http`、`--override-proxy-https` 和 `--override-proxy-exclude` 在 [Mac](/manuals/desktop/setup/install/mac-install.md#install-from-the-command-line) 和 [Windows](/manuals/desktop/setup/install/windows-install.md#install-from-the-command-line) 上从 CLI 安装时完成，或者通过在 `install-settings.json` 文件中设置值来完成。
- Docker Desktop 现在停止在应用程序启动时覆盖 .docker/config.json `credsStore` 密钥。请注意，如果您使用自定义凭证助手，则 CLI `docker login` 和 `docker logout` 不会影响 UI 是否登录到 Docker。通常，最好通过 UI 登录到 Docker，因为 UI 支持多因素身份验证。
- 添加了关于即将从 Docker Desktop 中移除 Compose V1 的警告。可以使用 `COMPOSE_V1_EOL_SILENT=1` 抑制。
- 在 Compose 配置中，YAML 中的布尔字段应为 `true` 或 `false`。YAML 1.1 的弃用值（如 “on” 或 “no”）现在会产生警告。
- 改进了镜像表的 UI，允许行使用更多可用空间。
- 修复了端口转发中的各种错误。
- 修复了 HTTP 代理错误，即没有服务器名称指示 (SNI) 记录的 HTTP 请求会被错误拒绝。

#### Windows

- 恢复了在 Windows 上完全修补 etc/hosts（再次包括 `host.docker.internal` 和 `gateway.docker.internal`）。对于 WSL，此行为由 **常规** 选项卡中的新设置控制。修复 [docker/for-win#13388](https://github.com/docker/for-win/issues/13388) 和 [docker/for-win#13398](https://github.com/docker/for-win/issues/13398)。
- 修复了在更新 Docker Desktop 时桌面上出现虚假的 `courgette.log` 文件的错误。修复 [docker/for-win#12468](https://github.com/docker/for-win/issues/12468)。
- 修复了“放大”快捷方式 (ctrl+=)。修复 [docker/for-win#13392](https://github.com/docker/for-win/issues/13392)。
- 修复了在第二次容器类型切换后托盘菜单未正确更新的错误。修复 [docker/for-win#13379](https://github.com/docker/for-win/issues/13379)。

#### Mac

- 提高了在 macOS Ventura 及更高版本上使用虚拟化框架时的 VM 网络性能。Mac 版 Docker Desktop 现在使用 gVisor 代替 VPNKit。要继续使用 VPNKit，请在位于 `~/Library/Group Containers/group.com.docker/settings.json` 的 `settings.json` 文件中添加 `"networkType":"vpnkit"`。
- 修复了在卸载时显示错误窗口的错误。
- 修复了 `deprecatedCgroupv1` 设置被忽略的错误。修复 [docker/for-mac#6801](https://github.com/docker/for-mac/issues/6801)。
- 修复了 `docker pull` 返回 `EOF` 的情况。

#### Linux

- 修复了 VM 网络在 24 小时后崩溃的错误。修复 [docker/desktop-linux#131](https://github.com/docker/desktop-linux/issues/131)。

### 安全性

#### 所有平台

- 修复了一个安全问题，该问题允许用户通过从其 Docker CLI 配置文件中删除 `credsStore` 密钥来绕过其组织配置的镜像访问管理 (IAM) 限制。仅影响 Docker Business 客户。
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

- `docker init` 的初始 Beta 版发布，符合[路线图](https://github.com/docker/roadmap/issues/453)。
- 添加了新的 **学习中心** 选项卡以帮助用户开始使用 Docker。
- 为 Docker Compose 添加了实验性的文件监视命令，可在您编辑和保存代码时自动更新正在运行的 Compose 服务。

### 升级

- [Buildx v0.10.4](https://github.com/docker/buildx/releases/tag/v0.10.4)
- [Compose 2.17.2](https://github.com/docker/compose/releases/tag/v2.17.2)
- [Containerd v1.6.18](https://github.com/containerd/containerd/releases/tag/v1.6.18)，其中包含对 [CVE-2023-25153](https://github.com/advisories/GHSA-259w-8hf6-59c2) 和 [CVE-2023-25173](https://github.com/advisories/GHSA-hmfx-3pcx-653p) 的修复。
- [Docker Engine v20.10.24](https://docs.docker.com/engine/release-notes/20.10/#201024)，其中包含对 [CVE-2023-28841](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-28841)、[CVE-2023-28840](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-28840) 和 [CVE-2023-28842](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-28842) 的修复。

### 错误修复和增强功能

#### 所有平台

- [Docker Scout CLI](../scout/_index.md#docker-scout-cli) 现在可以比较两个镜像并显示包和漏洞差异。此命令处于[早期访问](../release-lifecycle.md)阶段，将来可能会更改。
- [Docker Scout CLI](../scout/_index.md#docker-scout-cli) 现在使用 `docker scout recommendations` 显示基础镜像更新和修复建议。它还使用 `docker scout quickview` 命令显示镜像的简短概述。
- 您现在可以直接从市场以及使用 **全局搜索** 搜索扩展。
- 修复了 `docker buildx` 容器构建器在 24 小时后失去网络访问权限的错误。
- 减少了提示用户对 Docker Desktop 提供反馈的频率。
- 移除了最小 VM 交换大小。
- 在 HTTP 代理排除列表中添加了对子域匹配、CIDR 匹配、`.` 和 `_.` 的支持。
- 修复了当服务器名称指示 (SNI) 字段未设置时透明 TLS 代理中的错误。
- 修复了 Docker Desktop 引擎状态消息中的语法错误。

### Windows

- 修复了 `docker run --gpus=all` 挂起的错误。修复 [docker/for-win#13324](https://github.com/docker/for-win/issues/13324)。
- 修复了注册表访问管理策略更新未下载的错误。
- Docker Desktop 现在允许在 `C:` 上启用 BitLocker 时使用 Windows 容器。
- 使用 WSL 后端的 Docker Desktop 不再需要 `com.docker.service` 特权服务永久运行。有关更多信息，请参阅 [Windows 的权限要求](https://docs.docker.com/desktop/windows/permission-requirements/)。

### Mac

- 修复了在 VirtioFS 用户中存储在主机上的属性未被缓存导致的性能问题。
- 首次启动 Mac 版 Docker Desktop 时，用户会看到一个安装窗口，以确认或调整需要特权访问的配置。有关更多信息，请参阅 [Mac 的权限要求](https://docs.docker.com/desktop/mac/permission-requirements/)。
- 在 **设置** 中添加了 **高级** 选项卡，用户可以在其中调整需要特权访问的设置。

### Linux

- 修复了 VM 网络在 24 小时后崩溃的错误。[docker/for-linux#131](https://github.com/docker/desktop-linux/issues/131)

### 安全性

#### 所有平台

- 修复了 [CVE-2023-1802](https://www.cve.org/cverecord?id=CVE-2023-1802)，该问题导致 Artifactory 集成中的安全问题会在 HTTPS 检查失败时回退到通过纯 HTTP 发送注册表凭据。仅启用了 **访问实验性功能** 的用户受影响。修复 [docker/for-win#13344](https://github.com/docker/for-win/issues/13344)。

#### Mac

- 移除了 `com.apple.security.cs.allow-dyld-environment-variables` 和 `com.apple.security.cs.disable-library-validation` 权限，这些权限允许通过 `DYLD_INSERT_LIBRARIES` 环境变量将任意动态库加载到 Docker Desktop 中。

### 已知问题

- 从 **故障排除** 页面卸载 Mac 上的 Docker Desktop 可能会触发意外的致命错误弹出窗口。

## 4.17.1

{{< release-date date="2023-03-20" >}}

### 错误修复和增强功能

#### Windows

- Docker Desktop 现在允许在 `C:` 上启用 BitLocker 时使用 Windows 容器。
- 修复了 `docker buildx` 容器构建器在 24 小时后失去网络访问权限的错误。
- 修复了注册表访问管理策略更新未下载的错误。
- 改进了调试信息以更好地表征 WSL 2 下的故障。

### 已知问题

#### Windows

- 在带有 WSL 2 后端的 Windows 上使用 `--gpus` 运行容器不起作用。这将在未来的版本中修复。请参阅 [docker/for-win/13324](https://github.com/docker/for-win/issues/13324)。

## 4.17.0

{{< release-date date="2023-02-27" >}}

### 新增功能

- Docker Desktop 现在附带 Docker Scout。从 Docker Hub 和 Artifactory 存储库拉取和查看镜像分析，获取基础镜像更新和推荐的标签和摘要，并根据漏洞信息过滤您的镜像。要了解更多信息，请参阅 [Docker Scout](../scout/_index.md)。
- `docker scout` 取代了 `docker scan`。有关更多信息，请参阅 [Docker Scout CLI](../scout/_index.md#docker-scout-cli)。
- 您现在可以发现已在扩展市场中自主发布的扩展。有关自行发布扩展的更多信息，请参阅[市场扩展](/manuals/extensions/marketplace.md)。
- **容器文件资源管理器** 作为实验性功能提供。直接从 GUI 调试容器内的文件系统。
- 您现在可以在 **全局搜索** 中搜索卷。

### 升级

- [Containerd v1.6.18](https://github.com/containerd/containerd/releases/tag/v1.6.18)，其中包含对 [CVE-2023-25153](https://github.com/advisories/GHSA-259w-8hf6-59c2) 和 [CVE-2023-25173](https://github.com/advisories/GHSA-hmfx-3pcx-653p) 的修复。
- [Docker Engine v20.10.23](https://docs.docker.com/engine/release-notes/20.10/#201023).
- [Go 1.19.5](https://github.com/golang/go/releases/tag/go1.19.5)

### 错误修复和增强功能

#### 所有平台

- 修复了在等待子进程退出时诊断收集可能挂起的错误。
- 防止透明 HTTP 代理过度破坏请求。修复 Tailscale 扩展登录，参见 [tailscale/docker-extension#49](https://github.com/tailscale/docker-extension/issues/49)。
- 修复了透明 TLS 代理中未设置服务器名称指示 (SNI) 字段的错误。
- 在 HTTP 代理排除列表中添加了对子域匹配、CIDR 匹配、`.` 和 `*.` 的支持。
- 确保在上传诊断时遵守 HTTP 代理设置。
- 修复了从凭证助手获取凭证时的致命错误。
- 修复了与并发日志记录相关的致命错误。
- 改进了市场中扩展操作的 UI。
- 在扩展市场中添加了新的过滤器。您现在可以按类别和审核状态过滤扩展。
- 添加了向 Docker 报告恶意扩展的方法。
- 将 Dev Environments 更新为 v0.2.2，包含初始设置可靠性和安全性修复。
- 仅为新用户添加了欢迎调查。
- 故障排除页面上的确认对话框现在与其他类似对话框的样式一致。
- 在 Kubernetes 集群启动之前重置它导致的致命错误。
- 为 containerd 集成实现了 `docker import`。
- 修复了使用现有标签进行镜像标记的问题。
- 为 containerd 集成实现了镜像上的悬空过滤器。
- 修复了当镜像不再存在时 `docker ps` 对容器失败的问题。

#### Mac

- 修复了在未安装特权辅助工具 `com.docker.vmnetd` 的系统上下载注册表访问管理策略的问题。
- 修复了当 `/Library/PrivilegedHelperTools` 不存在时 `com.docker.vmnetd` 无法安装的错误。
- 修复了“系统”代理无法处理“自动代理”/“pac 文件”配置的错误。
- 修复了在区分大小写的文件系统上 vmnetd 安装无法读取 `Info.Plist` 的错误。实际文件名是 `Info.plist`。修复 [docker/for-mac#6677](https://github.com/docker/for-mac/issues/6677)。
- 修复了在每次启动时提示用户创建 docker 套接字符号链接的错误。修复 [docker/for-mac#6634](https://github.com/docker/for-mac/issues/6634)。
- 修复了 **登录时启动 Docker Desktop** 设置不起作用的错误。修复 [docker/for-mac#6723](https://github.com/docker/for-mac/issues/6723)。
- 修复了 UDP 连接跟踪和 `host.docker.internal` 的问题。修复 [docker/for-mac#6699](https://github.com/docker/for-mac/issues/6699)。
- 改进了 kubectl 符号链接逻辑，以尊重 `/usr/local/bin` 中的现有二进制文件。修复 [docker/for-mac#6328](https://github.com/docker/for-mac/issues/6328)。
- Docker Desktop 现在会在您选择使用 Rosetta 但尚未安装时自动安装 Rosetta。

### Windows

- 添加了针对 `musl` 静态链接的 WSL 集成工具，因此无需在用户发行版中安装 `alpine-pkg-glibc`。
- 添加了在 WSL 2 上运行 cgroupv2 的支持。这通过在 `%USERPROFILE%\.wslconfig` 文件的 `[wsl2]` 部分添加 `kernelCommandLine = systemd.unified_cgroup_hierarchy=1 cgroup_no_v1=all` 来激活。
- 修复了在 WSL 2 模式下（在 4.16 中引入）Docker Desktop 陷入“启动”阶段的问题。
- 修复了当在 `%LOCALAPPDATA%` 上启用文件系统压缩或加密时，Docker Desktop 无法启动 WSL 2 后端的问题。
- 修复了在启动时无法报告缺少或过时（无法运行 WSL 版本 2 发行版）的 WSL 安装的问题。
- 修复了在目标路径有空格时在 Visual Studio Code 中打开失败的错误。
- 修复了导致 `~/.docker/context` 损坏和错误消息“意外的 JSON 输入结束”的错误。您也可以删除 `~/.docker/context` 来解决此问题。
- 确保在 WSL 2 中使用的凭证助手已正确签名。与 [docker/for-win#10247](https://github.com/docker/for-win/issues/10247) 相关。
- 修复了导致 WSL 集成代理被错误终止的问题。与 [docker/for-win#13202](https://github.com/docker/for-win/issues/13202) 相关。
- 修复了启动时损坏的上下文。修复 [docker/for-win#13180](https://github.com/docker/for-win/issues/13180) 和 [docker/for-win#12561](https://github.com/docker/for-win/issues/12561)。

### Linux

- 为 Linux 版 Docker Desktop 添加了 Docker Buildx 插件。
- 将 RPM 和 Arch Linux 发行版的压缩算法更改为 `xz`。
- 修复了导致残留文件留在 Debian 包根目录中的错误。修复 [docker/for-linux#123](https://github.com/docker/desktop-linux/issues/123)。

### 安全性

#### 所有平台

- 修复了 [CVE-2023-0628](https://www.cve.org/cverecord?id=CVE-2023-0628)，该问题允许攻击者通过诱骗用户打开精心制作的恶意 `docker-desktop://` URL，在开发环境容器初始化期间在其中执行任意命令。
- 修复了 [CVE-2023-0629](https://www.cve.org/cverecord?id=CVE-2023-0629)，该问题允许非特权用户通过使用 `-H` (`--host`) CLI 标志或 `DOCKER_HOST` 环境变量将 Docker 主机设置为 `docker.raw.sock`（或在 Windows 上设置为 `npipe:////.pipe/docker_engine_linux`）来绕过增强容器隔离 (ECI) 限制，并在没有 ECI 提供的额外强化功能的情况下启动容器。这不会影响已在运行的容器，也不会影响通过常规方法（不使用 Docker 原始套接字）启动的容器。

## 4.16.3

{{< release-date date="2023-01-30" >}}

### 错误修复和增强功能

#### Windows

- 修复了当在 `%LOCALAPPDATA%` 上启用文件系统压缩或加密时，Docker Desktop 无法启动 WSL 2 后端的问题。修复 [docker/for-win#13184](https://github.com/docker/for-win/issues/13184)。
- 修复了在启动时无法报告缺少或过时的 WSL 安装的问题。修复 [docker/for-win#13184](https://github.com/docker/for-win/issues/13184)。

## 4.16.2

{{< release-date date="2023-01-19" >}}

### 错误修复和增强功能

#### 所有平台

- 修复了在启用 containerd 集成功能时，`docker build` 和 `docker tag` 命令产生 `镜像已存在` 错误的问题。
- 修复了 Docker Desktop 4.16 中引入的回归问题，该问题导致在 amd64 系统上使用目标平台 linux/386 的容器网络中断。修复 [docker/for-mac/6689](https://github.com/docker/for-mac/issues/6689)。

#### Mac

- 修复了 `Info.plist` 的大小写问题，该问题导致 `vmnetd` 在区分大小写的文件系统上中断。修复 [docker/for-mac/6677](https://github.com/docker/for-mac/issues/6677)。

#### Windows

- 修复了 Docker Desktop 4.16 中引入的回归问题，该问题导致在 WSL2 模式下陷入“启动”阶段。修复 [docker/for-win/13165](https://github.com/docker/for-win/issues/13165)

## 4.16.1

{{< release-date date="2023-01-13" >}}

### 错误修复和增强功能

#### 所有平台

- 修复了容器内 `sudo` 因某些镜像出现安全相关错误而失败的问题。修复 [docker/for-mac/6675](https://github.com/docker/for-mac/issues/6675) 和 [docker/for-win/13161](https://github.com/docker/for-win/issues/13161)。

## 4.16.0

{{< release-date date="2023-01-12" >}}

### 新增功能

- 扩展已从 Beta 移至 GA。
- 快速搜索已从实验性移至 GA。
- 扩展现在包含在快速搜索中。
- 分析大型镜像的速度现在快了 4 倍。
- 新的本地镜像视图已从实验性移至 GA。
- 为 macOS 13 添加了新的 Beta 功能 Rosetta for Linux，可在 Apple Silicon 上更快地仿真基于 Intel 的镜像。

### 升级

- [Compose v2.15.1](https://github.com/docker/compose/releases/tag/v2.15.1)
- [Containerd v1.6.14](https://github.com/containerd/containerd/releases/tag/v1.6.14)
- [Docker Engine v20.10.22](https://docs.docker.com/engine/release-notes/20.10/#201022)
- [Buildx v0.10.0](https://github.com/docker/buildx/releases/tag/v0.10.0)
- [Docker Scan v0.23.0](https://github.com/docker/scan-cli-plugin/releases/tag/v0.23.0)
- [Go 1.19.4](https://github.com/golang/go/releases/tag/go1.19.4)

### 错误修复和增强功能

#### 所有平台

- 修复了 `docker build --quiet` 在使用 `containerd` 集成时不输出镜像标识符的问题。
- 修复了在使用 `containerd` 集成时镜像检查不显示镜像标签的问题。
- 增加了运行中和已停止容器图标之间的对比度，使色盲用户更容易扫描容器列表。
- 修复了在用户输入新 HTTP 代理凭据之前，会反复提示用户输入新 HTTP 代理凭据的错误。
- 添加了诊断命令 `com.docker.diagnose login` 来检查 HTTP 代理配置。
- 修复了 Compose 堆栈操作无法正常工作的问题。修复 [docker/for-mac#6566](https://github.com/docker/for-mac/issues/6566)。
- 修复了 Docker Desktop 仪表板在启动时尝试获取磁盘使用信息并在引擎运行之前显示错误横幅的问题。
- 在所有实验性功能旁边添加了信息性横幅，其中包含如何选择退出实验性功能访问的说明。
- Docker Desktop 现在支持通过 HTTP 代理下载 Kubernetes 镜像。
- 修复了工具提示阻塞操作按钮的问题。修复 [docker/for-mac#6516](https://github.com/docker/for-mac/issues/6516)。
- 修复了 **容器** 视图中空白的“发生错误”容器列表。

#### Mac

- 在 macOS 上安装或更新 Docker Desktop 的最低操作系统版本现在是 macOS Big Sur（版本 11）或更高版本。
- 修复了当使用旧版 `osxfs` 实现进行文件共享时，如果启用了增强容器隔离，Docker 引擎无法启动的问题。
- 修复了在 VirtioFS 上创建的文件设置了可执行位的问题。修复 [docker/for-mac#6614](https://github.com/docker/for-mac/issues/6614)。
- 重新添加了从命令行卸载 Docker Desktop 的方法。修复 [docker/for-mac#6598](https://github.com/docker/for-mac/issues/6598)。
- 修复了硬编码的 `/usr/bin/kill`。修复 [docker/for-mac#6589](https://github.com/docker/for-mac/issues/6589)。
- 修复了在 VirtioFS 上共享的非常大的文件（> 38GB）被截断时大小不正确的问题。
- 将 **设置** 中的磁盘镜像大小更改为使用十进制系统（基数 10），以与 Finder 显示磁盘容量的方式一致。
- 修复了在网络负载下 Docker 崩溃的问题。修复 [docker/for-mac#6530](https://github.com/docker/for-mac/issues/6530)。
- 修复了导致 Docker 在每次重启后提示用户安装 `/var/run/docker.sock` 符号链接的问题。
- 确保安装 `/var/run/docker.sock` 符号链接的登录项已签名。
- 修复了在恢复出厂设置时删除 `$HOME/.docker` 的错误。

### Windows

- 修复了 `docker build` 在打印“加载元数据”时挂起的错误。修复 [docker/for-win#10247](https://github.com/docker/for-win/issues/10247)。
- 修复了 diagnose.exe 输出中的拼写错误。修复 [docker/for-win#13107](https://github.com/docker/for-win/issues/13107)。
- 添加了在 WSL 2 上运行 cgroupv2 的支持。这通过在 `%USERPROFILE%\.wslconfig` 文件的 `[wsl2]` 部分添加 `kernelCommandLine = systemd.unified_cgroup_hierarchy=1 cgroup_no_v1=all` 来激活。

### 已知问题

- 在某些镜像中，容器内的 `sudo` 因安全相关错误而失败。请参阅 [docker/for-mac/6675](https://github.com/docker/for-mac/issues/6675) 和 [docker/for-win/13161](https://github.com/docker/for-win/issues/13161)。

## 4.15.0

{{< release-date date="2022-12-01" >}}

### 新增功能

- 对 macOS 用户进行了重大的性能改进，可以选择启用新的 VirtioFS 文件共享技术。适用于 macOS 12.5 及更高版本。
- Mac 版 Docker Desktop 在安装或首次运行时不再需要安装特权辅助进程 `com.docker.vmnetd`。有关更多信息，请参阅 [Mac 的权限要求](https://docs.docker.com/desktop/mac/permission-requirements/)。
- 添加了 [WebAssembly 功能](/manuals/desktop/features/wasm.md)。与 [containerd 集成](/manuals/desktop/features/containerd.md) 一起使用。
- 改进了 Beta 和实验性设置的描述，以清楚解释差异以及人们如何访问它们。
- Mac 和 Linux 上 Docker Desktop 仪表板的页脚中现在显示 VM 的可用磁盘空间。
- 如果可用空间低于 3GB，页脚中会显示磁盘空间警告。
- 对 Docker Desktop 界面进行了更改，使其更加 ADA 可访问且视觉统一。
- 在 **扩展** 中添加了 **构建** 选项卡，其中包含构建扩展所需的所有资源。
- 添加了更轻松地共享扩展的功能，无论是使用 `docker extension share` CLI 还是使用扩展 **管理** 选项卡中的共享按钮。
- 市场中的扩展现在显示安装数量。您还可以按安装数量对扩展进行排序。
- 开发环境允许将 Git 存储库克隆到本地绑定挂载，因此您可以使用任何本地编辑器或 IDE。
- 更多开发环境改进：自定义名称、更好的私有存储库支持、改进的端口处理。

### 升级

- [Compose v2.13.0](https://github.com/docker/compose/releases/tag/v2.13.0)
- [Containerd v1.6.10](https://github.com/containerd/containerd/releases/tag/v1.6.10)
- [Docker Hub Tool v0.4.5](https://github.com/docker/hub-tool/releases/tag/v0.4.5)
- [Docker Scan v0.22.0](https://github.com/docker/scan-cli-plugin/releases/tag/v0.22.0)

### 错误修复和增强功能

#### 所有平台

- 使用 containerd 集成时，容器现在会在重启时恢复。
- 修复了使用 containerd 集成时列出多平台镜像的问题。
- 使用 containerd 集成时，更好地处理悬空镜像。
- 为 containerd 集成实现了镜像的“引用”过滤器。
- 添加了通过容器、`docker pull` 等中的 `proxy.pac` 自动选择上游 HTTP/HTTPS 代理的支持。
- 修复了在拉取时解析镜像引用时的回归问题。修复 [docker/for-win#13053](https://github.com/docker/for-win/issues/13053), [docker/for-mac#6560](https://github.com/docker/for-mac/issues/6560), 和 [docker/for-mac#6540](https://github.com/docker/for-mac/issues/6540)。

#### Mac

- 改进了 `docker pull` 的性能。

#### Windows

- 修复了在 Docker 启动和开发者登录时未使用系统 HTTP 代理的问题。
- 当 Docker Desktop 使用“系统”代理且 Windows 设置更改时，Docker Desktop 现在会使用新的 Windows 设置而无需重新启动。

#### Linux

- 修复了 Linux 上的热重载问题。修复 [docker/desktop-linux#30](https://github.com/docker/desktop-linux/issues/30)。
- 禁用了 Linux 上的托盘图标动画，这修复了某些用户的崩溃问题。

## 4.14.1

{{< release-date date="2022-11-17" >}}

### 错误修复和增强功能

#### 所有平台

- 修复了使用注册表访问管理时容器 DNS 查找的问题。

#### Mac

- 修复了阻止 **镜像** 选项卡上的 **分析镜像** 按钮工作的问题。
- 修复了如果 `/usr/local/lib` 不存在，则不会为用户创建符号链接的错误。修复 [docker/for-mac#6569](https://github.com/docker/for-mac/issues/6569)

## 4.14.0

{{< release-date date="2022-11-10" >}}

### 新增功能

- 将虚拟化框架设置为 macOS >= 12.5 的默认管理程序。
- 将以前的安装迁移到 macOS >= 12.5 的虚拟化框架管理程序。
- 增强容器隔离功能（适用于 Docker Business 用户）现在可以从常规设置中启用。

### 更新

- [Docker Engine v20.10.21](/manuals/engine/release-notes/20.10.md#201021)，
  其中包含针对 Git 漏洞的缓解措施，跟踪为 [CVE-2022-39253](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-39253)，
  并更新了 `image:tag@digest` 镜像引用的处理。
- [Docker Compose v2.12.2](https://github.com/docker/compose/releases/tag/v2.12.2)
- [Containerd v1.6.9](https://github.com/containerd/containerd/releases/tag/v1.6.9)
- [Go 1.19.3](https://github.com/golang/go/releases/tag/go1.19.3)

### 错误修复和增强功能

#### 所有平台

- Docker Desktop 现在需要一个大小为 /24 的内部网络子网。如果您以前使用的是 /28，它会自动扩展到 /24。如果您遇到网络问题，请检查 Docker 子网与您的基础架构之间是否存在冲突。修复 [docker/for-win#13025](https://github.com/docker/for-win/issues/13025)。
- 修复了当 Git URL 包含大写字符时阻止用户创建开发环境的问题。
- 修复了诊断中报告的 `vpnkit.exe is not running` 错误。
- 将 qemu 恢复到 6.2.0，以修复在运行仿真 amd64 代码时出现 `PR_SET_CHILD_SUBREAPER is unavailable` 等错误。
- 在扩展中启用了 [contextIsolation](https://www.electronjs.org/docs/latest/tutorial/context-isolation) 和 [sandbox](https://www.electronjs.org/docs/latest/tutorial/sandbox) 模式。现在扩展在单独的上下文中运行，这限制了恶意代码可能造成的危害，限制了对大多数系统资源的访问。
- 包含了 `unpigz` 以允许并行解压缩拉取的镜像。
- 修复了对选定容器执行操作时的问题。[修复 https://github.com/docker/for-win/issues/13005](https://github.com/docker/for-win/issues/13005)
- 添加了允许您在容器或项目视图中显示时间戳的功能。
- 修复了在使用 Control+C 中断 `docker pull` 时可能出现的分段错误。
- 将默认 DHCP 租约时间增加到 2 小时，以避免 VM 网络故障和连接断开。
- 移除了容器列表上的无限旋转器。[修复 https://github.com/docker/for-mac/issues/6486](https://github.com/docker/for-mac/issues/6486)
- 修复了在 **设置** 中显示已用空间值不正确的错误。
- 修复了在使用 containerd 集成时导致 Kubernetes 无法启动的错误。
- 修复了在使用 containerd 集成时导致 `kind` 无法启动的错误。
- 修复了在使用 containerd 集成时导致开发环境无法工作的错误。
- 在 containerd 集成中实现了 `docker diff`。
- 在 containerd 集成中实现了 `docker run —-platform`。
- 修复了在使用 containerd 集成时导致不安全注册表无法工作的错误。

#### Mac

- 修复了虚拟化框架用户的启动失败。
- 重新在 Mac 上添加了 `/var/run/docker.sock`，以提高与 `tilt` 和 `docker-py` 等工具的兼容性。
- 修复了在新 Mac 安装上无法创建开发环境的问题（错误“无法连接到 Docker 守护程序 at unix:///var/run/docker.sock。docker 守护程序正在运行吗？”）。

#### Windows

- 重新添加了 `DockerCli.exe -SharedDrives`。修复 [docker/for-win#5625](https://github.com/docker/for-win#5625)。
- Docker Desktop 现在允许在禁用 PowerShell 的机器上运行 Docker。
- 修复了在 Windows 上 Compose v2 未默认启用的问题。
- Docker Desktop 现在会在卸载时删除 `C:\Program Files\Docker` 文件夹。

### 已知问题

#### Mac

- 对于某些 Mac OS 用户，安装程序存在一个已知问题，会阻止安装 Docker Desktop 中漏洞和包发现实验性功能所需的新辅助工具。要解决此问题，需要使用以下命令创建一个符号链接：`sudo ln -s /Applications/Docker.app/Contents/Resources/bin/docker-index /usr/local/bin/docker-index`

## 4.13.1

{{< release-date date="2022-10-31" >}}

### 更新

- [Docker Compose v2.12.1](https://github.com/docker/compose/releases/tag/v2.12.1)

### 错误修复和增强功能

#### 所有平台

- 修复了在使用 `Control+C` 或 `CMD+C` 中断 `docker pull` 时可能出现的分段错误。
- 将默认 DHCP 租约时间增加到 2 小时，以避免 VM 网络故障和连接断开。
- 将 `Qemu` 恢复到 `6.2.0`，以修复在运行仿真 amd64 代码时出现 `PR_SET_CHILD_SUBREAPER is unavailable` 等错误。

#### Mac

- 默认在 Mac 上重新添加了 `/var/run/docker.sock` 符号链接，以提高与 `tilt` 和 `docker-py` 等工具的兼容性。修复 [docker/for-mac#6529](https://github.com/docker/for-mac/issues/6529)。
- 修复了在新 Mac 安装上无法创建开发环境并导致 `错误“无法连接到 Docker 守护程序 at unix:///var/run/docker.sock。docker 守护程序正在运行吗？”` 的问题。

#### Windows

- Docker Desktop 现在可以在禁用 PowerShell 的机器上运行。

## 4.13.0

{{< release-date date="2022-10-19" >}}

### 新增功能

- 为 Docker Business 用户引入了两个新的安全功能：设置管理和增强容器隔离。阅读有关[Docker Desktop 的新强化 Docker Desktop 安全模型](/manuals/enterprise/security/hardened-desktop/_index.md) 的更多信息。
- 添加了新的开发环境 CLI `docker dev`，因此您可以通过命令行创建、列出和运行开发环境。现在更容易将开发环境集成到自定义脚本中。
- Docker Desktop 现在可以使用 `--installation-dir` 安装到任何驱动器和文件夹。部分解决了 [docker/roadmap#94](https://github.com/docker/roadmap/issues/94)。

### 更新

- [Docker Scan v0.21.0](https://github.com/docker/scan-cli-plugin/releases/tag/v0.21.0)
- [Go 1.19.2](https://github.com/golang/go/releases/tag/go1.19.2) 以解决 [CVE-2022-2879](https://www.cve.org/CVERecord?id=CVE-2022-2879)、[CVE-2022-2880](https://www.cve.org/CVERecord?id=CVE-2022-2880) 和 [CVE-2022-41715](https://www.cve.org/CVERecord?id=CVE-2022-41715)
- 将 Docker Engine 和 Docker CLI 更新至 [v20.10.20](/manuals/engine/release-notes/20.10.md#201020)，
  其中包含针对 Git 漏洞的缓解措施，跟踪为 [CVE-2022-39253](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-39253)，
  并更新了 `image:tag@digest` 镜像引用的处理，以及对 [CVE-2022-36109](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-36109) 的修复。
- [Docker Credential Helpers v0.7.0](https://github.com/docker/docker-credential-helpers/releases/tag/v0.7.0)
- [Docker Compose v2.12.0](https://github.com/docker/compose/releases/tag/v2.12.0)
- [Kubernetes v1.25.2](https://github.com/kubernetes/kubernetes/releases/tag/v1.25.2)
- [Qemu 7.0.0](https://wiki.qemu.org/ChangeLog/7.0) 用于 Docker Desktop VM 内部的 CPU 仿真。
- [Linux kernel 5.15.49](https://hub.docker.com/layers/docker/for-desktop-kernel/5.15.49-13422a825f833d125942948cf8a8688cef721ead/images/sha256-ebf1f6f0cb58c70eaa260e9d55df7c43968874d62daced966ef6a5c5cd96b493?context=explore)

### 错误修复和增强功能

#### 所有平台

- Docker Desktop 现在允许在与 HTTP 和 HTTPS 代理通信时使用 TLS 来加密代理用户名和密码。
- Docker Desktop 现在将 HTTP 和 HTTPS 代理密码存储在 OS 凭证存储中。
- 如果 Docker Desktop 检测到 HTTP 或 HTTPS 代理密码已更改，它将提示开发人员输入新密码。
- **绕过代理设置的主机和域** 设置现在正确处理 HTTPS 的域名。
- **远程存储库** 视图和每日提示现在适用于需要身份验证的 HTTP 和 HTTPS 代理。
- 我们为处于产品开发生命周期早期阶段的功能引入了暗启动。选择加入的用户可以随时在设置中的“Beta 功能”部分选择退出。
- 为扩展市场添加了类别。
- 在鲸鱼菜单和 **扩展** 选项卡上添加了指示器，指示扩展更新何时可用。
- 修复了镜像名称没有命名空间（例如 'my-extension'）的扩展卸载失败的问题。
- 在 **容器** 选项卡中显式显示端口映射。
- 将镜像磁盘使用信息的刷新率更改为每天自动进行一次。
- 使 **容器** 和 **卷** 选项卡的标签样式一致。
- 修复了 **设置** 中 Grpcfuse 文件共享模式启用的问题。修复 [docker/for-mac#6467](https://github.com/docker/for-mac/issues/6467)
- 虚拟化框架和 VirtioFS 对于运行 macOS < 12.5 的用户被禁用。
- **容器** 选项卡上的端口现在可点击。
- 扩展 SDK 现在允许 `ddClient.extension.vm.cli.exec`、`ddClient.extension.host.cli.exec`、`ddClient.docker.cli.exec` 接受不同的工作目录并通过选项参数传递环境变量。
- 添加了一个小改进，可在单击侧边栏中的 **扩展** 时导航到扩展市场。
- 添加了徽章以标识市场中的新扩展。
- 修复了在使用 containerd 集成时 Kubernetes 无法启动的问题。
- 修复了在使用 containerd 集成时 `kind` 无法启动的问题。
- 修复了在使用 containerd 集成时开发环境无法工作的问题。
- 在 containerd 集成中实现了 `docker diff`。
- 在 containerd 集成中实现了 `docker run —-platform`。
- 修复了在使用 containerd 集成时不安全注册表无法工作的问题。
- 修复了在 **设置** 中显示已用空间值不正确的错误。
- Docker Desktop 现在从 Github 发布版安装凭证助手。参见 [docker/for-win#10247](https://github.com/docker/for-win/issues/10247), [docker/for-win#12995](https://github.com/docker/for-win/issues/12995)。
- 修复了用户在 7 天后被注销出 Docker Desktop 的问题。

#### Mac

- 为 Docker Desktop 添加了 **隐藏**、**隐藏其他**、**显示全部** 菜单项。参见 [docker/for-mac#6446](https://github.com/docker/for-mac/issues/6446)。
- 修复了从已安装的应用程序运行安装实用程序时删除应用程序的错误。修复 [docker/for-mac#6442](https://github.com/docker/for-mac/issues/6442)。
- 默认情况下，Docker 不会在主机上创建 /var/run/docker.sock 符号链接，而是使用 docker-desktop CLI 上下文。

#### Linux

- 修复了阻止从仪表板推送镜像的错误

## 4.12.0

{{< release-date date="2022-09-01" >}}

### 新功能

- 添加了使用 containerd 拉取和存储镜像的功能。这是一个实验性功能。
- Docker Desktop 现在可以运行无标签镜像。修复 [docker/for-mac#6425](https://github.com/docker/for-mac/issues/6425)。
- 为 Docker Extension 的 Marketplace 添加了搜索功能。修复 [docker/roadmap#346](https://github.com/docker/roadmap/issues/346)。
- 添加了放大、缩小或将 Docker Desktop 设置为实际大小的功能。这可以通过在 Mac 和 Windows 上分别使用键盘快捷键 ⌘ + / CTRL +, ⌘ - / CTRL -, ⌘ 0 / CTRL 0 来实现，或者通过 Mac 上的 View 菜单实现。
- 如果任何相关容器可停止，则添加 compose stop 按钮。
- 单个 compose 容器现在可以从 **Container** 视图中删除。
- 移除了 Fedora 35 上 virtiofsd <-> qemu 协议不匹配的变通方法，因为不再需要。Fedora 35 用户应将 qemu 包升级到最新版本（撰写时为 qemu-6.1.0-15.fc35）。
- 为容器实现了集成终端。
- 默认添加了工具提示，以显示所有外部链接的链接地址。

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

#### 适用于所有平台

- 修复了 [CVE-2023-0626](https://www.cve.org/cverecord?id=CVE-2023-0626)，该漏洞允许通过 Electron 客户端中 message-box 路由的查询参数进行 RCE。
- 修复了 [CVE-2023-0625](https://www.cve.org/cverecord?id=CVE-2023-0625)，该漏洞允许通过扩展描述/changelog 进行 RCE，可能被恶意扩展滥用。

#### 适用于 Windows

- 修复了 [CVE-2023-0627](https://www.cve.org/cverecord?id=CVE-2023-0627)，该漏洞允许绕过 4.11 版本中引入的 `--no-windows-containers` 安装标志。该标志允许管理员禁用 Windows 容器的使用。
- 修复了 [CVE-2023-0633](https://www.cve.org/cverecord?id=CVE-2023-0633)，该漏洞中对 Docker Desktop 安装程序的参数注入可能导致本地权限提升。

### 错误修复和小增强

#### 适用于所有平台

- Compose V2 在工厂重置后现在已启用。
- Compose V2 现在在新安装的 Docker Desktop 上默认启用。
- Compose 中环境变量的优先顺序更一致，并明确[记录](/manuals/compose/how-tos/environment-variables/envvars-precedence.md)。
- 将内核升级到 5.10.124。
- 改进了因计算磁盘大小导致的整体性能问题。与 [docker/for-win#9401](https://github.com/docker/for-win/issues/9401) 相关。
- Docker Desktop 现在阻止未安装 Rosetta 的 ARM mac 用户切换回仅具有 intel 二进制文件的 Compose V1。
- 将卷大小和 **Created** 列的默认排序顺序更改为降序，以及容器的 **Started** 列。
- 通过始终仅保持 start/stop 和 delete 操作可见来重新组织容器行操作，同时允许通过行菜单项访问其余操作。
- Quickstart 指南现在立即运行每个命令。
- 为容器/compose **Status** 列定义排序顺序：running > some running > paused > some paused > exited > some exited > created。
- 修复了即使有镜像 Docker Desktop 中的镜像列表显示为空的问题。与 [docker/for-win#12693](https://github.com/docker/for-win/issues/12693) 和 [docker/for-mac#6347](https://github.com/docker/for-mac/issues/6347) 相关。
- 根据是否显示系统容器定义“使用中”的镜像。如果未显示与 Kubernetes 和 Extensions 相关的系统容器，则相关镜像不定义为“使用中”。
- 修复了导致某些语言中的 Docker 客户端在 `docker exec` 上挂起的错误。修复 [https://github.com/apocas/dockerode/issues/534](https://github.com/apocas/dockerode/issues/534)。
- 构建扩展时失败的生成命令不再导致 Docker Desktop 意外退出。
- 修复了导致扩展在左侧菜单中显示为禁用但实际未禁用的错误。
- 修复了在启用 Registry Access Management 并阻止对 Docker Hub 的访问时对私有注册表的 `docker login`。
- 修复了如果当前集群元数据未存储在 `.kube/config` 文件中，则 Docker Desktop 无法启动 Kubernetes 集群的错误。
- 更新了 Docker Desktop 和 MUI 主题包中的工具提示，以与整体系统设计一致。
- 复制的终端内容不再包含不间断空格。

#### 适用于 Mac

- 安装或更新 Docker Desktop on macOS 的最低版本现在为 10.15。修复 [docker/for-mac#6007](https://github.com/docker/for-mac/issues/6007)。
- 修复了 Tray 菜单在下载更新后错误显示“Download will start soon...”的问题。修复了 [for-mac/issues#5677](https://github.com/docker/for-mac/issues/5677) 中报告的一些问题
- 修复了应用更新后未重启 Docker Desktop 的错误。
- 修复了如果用户使用 virtualization.framework 和限制性防火墙软件，则计算机睡眠时导致与 Docker 的连接丢失的问题。
- 修复了即使用户已退出应用程序，Docker Desktop 仍在后台运行的错误。修复 [docker/for-mac##6440](https://github.com/docker/for-mac/issues/6440)
- 为运行 macOS < 12.5 的用户禁用 Virtualization Framework 和 VirtioFS

#### 适用于 Windows

- 修复了更新期间显示的版本可能不正确的错误。修复 [for-win/issues#12822](https://github.com/docker/for-win/issues/12822)。

## 4.11.1

{{< release-date date="2022-08-05" >}}

### 错误修复和增强功能

#### 适用于所有平台

- 修复了阻止 VM 系统位置（例如 /var/lib/docker）绑定挂载的回归问题 [for-mac/issues#6433](https://github.com/docker/for-mac/issues/6433)

#### 适用于 Windows

- 修复了从 WSL2 发行版对私有注册表的 `docker login` [docker/for-win#12871](https://github.com/docker/for-win/issues/12871)

## 4.11.0

{{< release-date date="2022-07-28" >}}

### 新功能

- Docker Desktop 现在在 VMware ESXi 和 Azure VM 内完全支持 Docker Business 客户。有关更多信息，请参阅 [在 VM 或 VDI 环境中运行 Docker Desktop](/manuals/desktop/setup/vm-vdi.md)
- 为 Extensions Marketplace 添加了两个新扩展（[vcluster](https://hub.docker.com/extensions/loftsh/vcluster-dd-extension) 和 [PGAdmin4](https://hub.docker.com/extensions/mochoa/pgadmin4-docker-extension)）。
- 为 Extensions Marketplace 添加了对扩展进行排序的功能。
- 修复了导致某些用户过于频繁被要求提供反馈的错误。您现在每年仅被要求提供两次反馈。
- 为 Docker Desktop 添加了自定义主题设置。这允许您指定 Docker Desktop 的深色或浅色模式，独立于设备设置。修复 [docker/for-win#12747](https://github.com/docker/for-win/issues/12747)
- 为 Windows 安装程序添加了新标志。`--no-windows-containers` 禁用 Windows 容器集成。
- 为 Mac 安装命令添加了新标志。`--user <username>` 为特定用户设置 Docker Desktop，防止他们在首次运行时需要管理员密码。

### 更新

- [Docker Compose v2.7.0](https://github.com/docker/compose/releases/tag/v2.7.0)
- [Docker Compose "Cloud Integrations" v1.0.28](https://github.com/docker/compose-cli/releases/tag/v1.0.28)
- [Kubernetes v1.24.2](https://github.com/kubernetes/kubernetes/releases/tag/v1.24.2)
- [Go 1.18.4](https://github.com/golang/go/releases/tag/go1.18.4)

### 错误修复和增强功能

#### 适用于所有平台

- 为 Containers 屏幕添加了 Container / Compose 图标以及暴露的端口/退出代码。
- 更新了 Docker 主题调色板颜色值以匹配我们的设计系统。
- 改进了如果 Registry Access Management 阻止 Docker 引擎访问 Docker Hub，则 `docker login` 的错误消息。
- 提高了主机和 Docker 之间的吞吐量。例如，提高 `docker cp` 的性能。
- 收集诊断所需的时间更少。
- 在容器概述中选择或取消选择 compose 应用现在会选择/取消选择其所有容器。
- 容器概述镜像列中的标签名称可见。
- 为终端的滚动条添加了搜索装饰，以便视口外的匹配项可见。
- 修复了容器页面搜索效果不佳的问题 [docker/for-win#12828](https://github.com/docker/for-win/issues/12828)。
- 修复了导致 **Volume** 屏幕无限加载的问题 [docker/for-win#12789](https://github.com/docker/for-win/issues/12789)。
- 修复了 Container UI 中调整大小或隐藏列无效的问题。修复 [docker/for-mac#6391](https://github.com/docker/for-mac/issues/6391)。
- 修复了同时安装、更新或卸载多个扩展的状态在离开 Marketplace 屏幕时丢失的问题。
- 修复了关于页面中的 compose 版本仅在重启 Docker Desktop 后从 v2 更新为 v1 的问题。
- 修复了用户无法看到日志视图的问题，因为其底层硬件不支持 WebGL2 渲染。修复 [docker/for-win#12825](https://github.com/docker/for-win/issues/12825)。
- 修复了 Containers 和 Images 的 UI 不同步的错误。
- 修复了启用实验性 virtualization framework 时的启动竞争条件。

#### 适用于 Mac

- 修复了从 UI 执行 Compose 命令的问题。修复 [docker/for-mac#6400](https://github.com/docker/for-mac/issues/6400)。

#### 适用于 Windows

- 修复了水平调整大小问题。修复 [docker/for-win#12816](https://github.com/docker/for-win/issues/12816)。
- 如果在 UI 中配置了 HTTP/HTTPS 代理，则它会自动将镜像构建和运行容器的流量发送到代理。这避免了在每个容器或构建中单独配置环境变量的需要。
- 添加了 `--backend=windows` 安装程序选项，以将 Windows 容器设置为默认后端。

#### 适用于 Linux

- 修复了与设置路径中包含空格的文件共享相关的错误。

## 4.10.1

{{< release-date date="2022-07-05" >}}

### 错误修复和增强功能

#### 适用于 Windows

- 修复了 UI 中的操作在使用从 WSL 创建的 Compose 应用时失败的错误。修复 [docker/for-win#12806](https://github.com/docker/for-win/issues/12806)。

#### 适用于 Mac

- 修复了因为路径未初始化导致安装命令失败的错误。修复 [docker/for-mac#6384](https://github.com/docker/for-mac/issues/6384)。

## 4.10.0

{{< release-date date="2022-06-30" >}}

### 新功能

- 现在可以在 Docker Desktop 中运行镜像之前添加环境变量。
- 添加了功能，使处理容器的日志更容易，例如正则表达式搜索以及在容器仍在运行时清除容器日志的能力。
- 实现了对容器表的反馈。添加了端口并分离了容器和镜像名称。
- 为 Extensions Marketplace 添加了两个新扩展，Ddosify 和 Lacework。

### 移除

- 在开发新设计时移除了 Homepage。您可以在[此处](https://docs.google.com/forms/d/e/1FAIpQLSfYueBkJHdgxqsWcQn4VzBn2swu4u_rMQRIMa8LExYb_72mmQ/viewform?entry.1237514594=4.10)提供反馈。

### 更新

- [Docker Engine v20.10.17](/manuals/engine/release-notes/20.10.md#201017)
- [Docker Compose v2.6.1](https://github.com/docker/compose/releases/tag/v2.6.1)
- [Kubernetes v1.24.1](https://github.com/kubernetes/kubernetes/releases/tag/v1.24.1)
- [cri-dockerd to v0.2.1](https://github.com/Mirantis/cri-dockerd/releases/tag/v0.2.1)
- [CNI plugins to v1.1.1](https://github.com/containernetworking/plugins/releases/tag/v1.1.1)
- [containerd to v1.6.6](https://github.com/containerd/containerd/releases/tag/v1.6.6)
- [runc to v1.1.2](https://github.com/opencontainers/runc/releases/tag/v1.1.2)
- [Go 1.18.3](https://github.com/golang/go/releases/tag/go1.18.3)

### 错误修复和增强功能

#### 适用于所有平台

- 为 **Containers** 选项卡中的选定容器添加了额外的批量操作，用于启动/暂停/停止。
- 为 **Containers** 选项卡中的 compose 项目添加了暂停和重启操作。
- 为 **Containers** 选项卡添加了图标和暴露端口或退出代码信息。
- 外部 URL 现在可以使用如下链接引用 Extension Marketplace 中的扩展详细信息：`docker-desktop://extensions/marketplace?extensionId=docker/logs-explorer-extension`。
- Compose 应用的展开或折叠状态现在会持久化。
- `docker extension` CLI 命令默认在 Docker Desktop 中可用。
- 增加了 Extension marketplace 中显示的截图大小。
- 修复了如果其后端容器停止，则 Docker 扩展无法加载的错误。修复 [docker/extensions-sdk#16](https://github.com/docker/extensions-sdk/issues/162)。
- 修复了镜像搜索字段无故清除的错误。修复 [docker/for-win#12738](https://github.com/docker/for-win/issues/12738)。
- 修复了许可证协议不显示并静默阻止 Docker Desktop 启动的错误。
- 修复了未发布扩展的显示镜像和标签实际显示已安装未发布扩展的镜像和标签的问题。
- 修复了 Support 屏幕上的重复页脚。
- Dev Environments 可以从 GitHub 存储库的子目录创建。
- 如果无法加载每日提示，则移除了使用 Docker Desktop 离线时的错误消息。修复 [docker/for-mac#6366](https://github.com/docker/for-mac/issues/6366)。

#### 适用于 Mac

- 修复了 macOS 上 bash 补全文件位置的错误。修复 [docker/for-mac#6343](https://github.com/docker/for-mac/issues/6343)。
- 修复了如果用户名超过 25 个字符，则 Docker Desktop 不启动的错误。修复 [docker/for-mac#6122](https://github.com/docker/for-mac/issues/6122)。
- 修复了由于无效的系统代理配置导致 Docker Desktop 未启动的错误。修复了 [docker/for-mac#6289](https://github.com/docker/for-mac/issues/6289) 中报告的一些问题。
- 修复了启用实验性 virtualization framework 时 Docker Desktop 无法启动的错误。
- 修复了卸载 Docker Desktop 后托盘图标仍显示的错误。

#### 适用于 Windows

- 修复了导致 Hyper-V 高 CPU 使用率的错误。修复 [docker/for-win#12780](https://github.com/docker/for-win/issues/12780)。
- 修复了 Docker Desktop for Windows 无法启动的错误。修复 [docker/for-win#12784](https://github.com/docker/for-win/issues/12784)。
- 修复了未将后端设置为 WSL 2 的 `--backend=wsl-2` 安装程序标志。修复 [docker/for-win#12746](https://github.com/docker/for-win/issues/12746)。

#### 适用于 Linux

- 修复了设置无法多次应用的问题。
- 修复了 `About` 屏幕中显示的 Compose 版本。

### 已知问题

- 偶尔在 `docker system prune` 期间 Docker 引擎会重启。这是当前引擎中使用 buildkit 版本的[已知问题](https://github.com/moby/buildkit/pull/2177)，将在未来版本中修复。

## 4.9.1

{{< release-date date="2022-06-16" >}}

{{< desktop-install all=true version="4.9.1" build_path="/81317/" >}}

### 错误修复和增强功能

#### 适用于所有平台

- 修复了空白仪表板屏幕。修复 [docker/for-win#12759](https://github.com/docker/for-win/issues/12759)。

## 4.9.0

{{< release-date date="2022-06-02" >}}

### 新功能

- 在主页上添加了更多指南：Elasticsearch、MariaDB、Memcached、MySQL、RabbitMQ 和 Ubuntu。
- 为 Docker Desktop Dashboard 添加了页脚，其中包含有关 Docker Desktop 更新状态和 Docker Engine 统计信息的通用信息
- 重新设计了容器表，添加了：
  - 将容器 ID 复制到剪贴板的按钮
  - 每个容器的暂停按钮
  - 容器表的列调整大小
  - 容器表的排序和调整大小持久化
  - 容器表的批量删除

### 更新

- [Compose v2.6.0](https://github.com/docker/compose/releases/tag/v2.6.0)
- [Docker Engine v20.10.16](/manuals/engine/release-notes/20.10.md#201016)
- [containerd v1.6.4](https://github.com/containerd/containerd/releases/tag/v1.6.4)
- [runc v1.1.1](https://github.com/opencontainers/runc/releases/tag/v1.1.1)
- [Go 1.18.2](https://github.com/golang/go/releases/tag/go1.18.2)

### 错误修复和增强功能

#### 适用于所有平台

- 修复了如果退出应用时 Docker Desktop 处于暂停状态，则导致 Docker Desktop 挂起的错误。
- 修复了 PKI 过期后 Kubernetes 集群未正确重置的问题。
- 修复了 Extensions Marketplace 未使用定义的 http 代理的问题。
- 改进了 Docker Desktop Dashboard 中的日志搜索功能，以允许空格。
- Dashboard 中的中键鼠标点击现在表现为左键点击，而不是打开空白窗口。

#### 适用于 Mac

- 修复了如果 `/opt` 已添加到文件共享目录列表中，则避免在主机上创建 `/opt/containerd/bin` 和 `/opt/containerd/lib` 的问题。

#### 适用于 Windows

- 修复了 WSL 2 集成中的错误，如果文件或目录绑定挂载到容器，并且容器退出，则文件或目录被同名其他类型对象替换。例如，如果文件被目录替换或目录被文件替换，则任何绑定挂载新对象的尝试都会失败。
- 修复了托盘图标和 Dashboard UI 未显示且 Docker Desktop 未完全启动的错误。修复 [docker/for-win#12622](https://github.com/docker/for-win/issues/12622)。

### 已知问题

#### 适用于 Linux

- 绑定挂载中文件的权限更改失败。这是由于我们在主机和运行 Docker Engine 的 VM 之间实现文件共享的方式导致的。我们计划在下一个版本中解决此问题。

## 4.8.2

{{< release-date date="2022-05-18" >}}

### 更新

- [Compose v2.5.1](https://github.com/docker/compose/releases/tag/v2.5.1)

### 错误修复和小增强

- 修复了手动代理设置导致拉取镜像问题的问题。修复 [docker/for-win#12714](https://github.com/docker/for-win/issues/12714) 和 [docker/for-mac#6315](https://github.com/docker/for-mac/issues/6315)。
- 修复了扩展禁用时的高 CPU 使用率。修复 [docker/for-mac#6310](https://github.com/docker/for-mac/issues/6310)。
- Docker Desktop 现在在日志文件和诊断中隐藏 HTTP 代理密码。

### 已知问题

#### 适用于 Linux

- 绑定挂载中文件的权限更改失败。这是由于我们在主机和运行 Docker Engine 的 VM 之间实现文件共享的方式导致的。我们计划在下一个版本中解决此问题。

## 4.8.1

{{< release-date date="2022-05-09" >}}

### 新功能

- 发布了 [Docker Desktop for Linux](/manuals/desktop/setup/install/linux/_index.md)。
- Beta 发布了 [Docker Extensions](/manuals/extensions/_index.md) 和 Extensions SDK。
- 创建了 Docker Homepage，您可以在其中运行流行镜像并发现如何使用它们。
- [Compose V2 现在正式可用](https://www.docker.com/blog/announcing-compose-v2-general-availability/)

### 错误修复和增强功能

- 修复了更新 Docker Desktop 时 Kubernetes 集群被删除的错误。

### 已知问题

#### 适用于 Linux

- 绑定挂载中文件的权限更改失败。这是由于我们在主机和运行 Docker Engine 的 VM 之间实现文件共享的方式导致的。我们计划在下一个版本中解决此问题。

## 4.8.0

{{< release-date date="2022-05-06" >}}

### 新功能

- 发布了 [Docker Desktop for Linux](/manuals/desktop/setup/install/linux/_index.md)。
- Beta 发布了 [Docker Extensions](/manuals/extensions/_index.md) 和 Extensions SDK。
- 创建了 Docker Homepage，您可以在其中运行流行镜像并发现如何使用它们。
- [Compose V2 现在正式可用](https://www.docker.com/blog/announcing-compose-v2-general-availability/)

### 更新

- [Compose v2.5.0](https://github.com/docker/compose/releases/tag/v2.5.0)
- [Go 1.18.1](https://github.com/golang/go/releases/tag/go1.18.1)
- [Kubernetes 1.24](https://github.com/kubernetes/kubernetes/releases/tag/v1.24.0)

### 错误修复和小增强

#### 适用于所有平台

- 引入了读取系统代理。您不再需要手动配置代理，除非它与您的操作系统级代理不同。
- 修复了在代理后面运行时 Dashboard 中显示 Remote Repositories 的错误。
- 修复了即使服务器已消失，vpnkit 仍建立并阻塞客户端连接的问题。请参阅 [docker/for-mac#6235](https://github.com/docker/for-mac/issues/6235)
- 对 Docker Desktop 中的 Volume 选项卡进行了改进：
  - 显示卷大小。
  - 列可以调整大小、隐藏和重新排序。
  - 列排序顺序和隐藏状态会持久化，即使在 Docker Desktop 重启后。
  - 在选项卡之间切换时行选择会持久化，即使在 Docker Desktop 重启后。
- 修复了 Dev Environments 选项卡中添加更多项目时未添加滚动的错误。
- 标准化了 Dashboard 中的标题和操作。
- 添加了对通过 HTTP 代理下载 Registry Access Management 策略的支持。
- 修复了机器长时间处于睡眠模式时远程存储库为空的相关问题。
- 修复了如果镜像名称未标记为“&lt;none>”但其标签是，则悬挂镜像未在清理过程中选择的问题。
- 改进了 `docker pull` 失败时因为需要 HTTP 代理的错误消息。
- 添加了轻松清除 Docker Desktop 中搜索栏的功能。
- 将“Containers / Apps”选项卡重命名为“Containers”。
- 修复了当 `C:\ProgramData\DockerDesktop` 是文件或符号链接时 Docker Desktop 安装程序的静默崩溃。
- 修复了例如 `docker pull <private registry>/image` 的无命名空间镜像会被 Registry Access Management 错误阻止的错误，除非在设置中启用对 Docker Hub 的访问。

#### 适用于 Mac

- Docker Desktop 的图标现在匹配 Big Sur 风格指南。请参阅 [docker/for-mac#5536](https://github.com/docker/for-mac/issues/5536)
- 修复了重复 Dock 图标和 Dock 图标未按预期工作的问题。修复 [docker/for-mac#6189](https://github.com/docker/for-mac/issues/6189)。
- 改进了对 `Cmd+Q` 快捷键的支持。

#### 适用于 Windows

- 改进了对 `Ctrl+W` 快捷键的支持。

### 已知问题

#### 适用于所有平台

- 当前，如果您正在运行 Kubernetes 集群，则在升级到 Docker Desktop 4.8.0 时它将被删除。我们计划在下一个版本中修复此问题。

#### 适用于 Linux

- 绑定挂载中文件的权限更改失败。这是由于我们在主机和运行 Docker Engine 的 VM 之间实现文件共享的方式导致的。我们计划在下一个版本中解决此问题。

## 4.7.1

{{< release-date date="2022-04-19" >}}

### 错误修复和增强功能

#### 适用于所有平台

- 修复了 Quick Start Guide 最终屏幕上的崩溃。

#### 适用于 Windows

- 修复了因符号链接错误导致更新失败的错误。修复 [docker/for-win#12650](https://github.com/docker/for-win/issues/12650)。
- 修复了阻止使用 Windows 容器模式的错误。修复 [docker/for-win#12652](https://github.com/docker/for-win/issues/12652)。

## 4.7.0

{{< release-date date="2022-04-07" >}}

### 新功能

- IT 管理员现在可以使用命令行远程安装 Docker Desktop。
- 添加 Docker Software Bill of Materials (SBOM) CLI 插件。新 CLI 插件允许用户为 Docker 镜像生成 SBOM。
- 为新 Kubernetes 集群使用 [cri-dockerd](https://github.com/Mirantis/cri-dockerd) 而不是 `dockershim`。从用户角度来看，此更改是透明的，Kubernetes 容器像以前一样在 Docker Engine 上运行。`cri-dockerd` 允许 Kubernetes 使用标准 [Container Runtime Interface](https://github.com/kubernetes/cri-api#readme) 管理 Docker 容器，与用于控制其他容器运行时的相同接口。有关更多信息，请参阅 [The Future of Dockershim is cri-dockerd](https://www.mirantis.com/blog/the-future-of-dockershim-is-cri-dockerd/)。

### 更新

- [Docker Engine v20.10.14](/manuals/engine/release-notes/20.10.md#201014)
- [Compose v2.4.1](https://github.com/docker/compose/releases/tag/v2.4.1)
- [Buildx 0.8.2](https://github.com/docker/buildx/releases/tag/v0.8.2)
- [containerd v1.5.11](https://github.com/containerd/containerd/releases/tag/v1.5.11)
- [Go 1.18](https://golang.org/doc/go1.18)

### 安全

- 将 Docker Engine 更新到 v20.10.14 以解决 [CVE-2022-24769](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-24769)
- 将 containerd 更新到 v1.5.11 以解决 [CVE-2022-24769](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-24769)

### 错误修复和增强功能

#### 适用于所有平台

- 修复了失败后 Registry Access Management 策略从未刷新的错误。
- UI 中的日志和终端现在在浅色和深色模式下尊重您的操作系统主题。
- 通过多选复选框轻松一次性清理多个卷。
- 改进了登录反馈。

#### 适用于 Mac

- 修复了有时导致 Docker Desktop 显示空白白屏的问题。修复 [docker/for-mac#6134](https://github.com/docker/for-mac/issues/6134)。
- 修复了使用 Hyperkit 时从睡眠中唤醒后 gettimeofday() 性能下降的问题。修复 [docker/for-mac#3455](https://github.com/docker/for-mac/issues/3455)。
- 修复了在使用 `osxfs` 进行文件共享且没有主机目录与 VM 共享时启动期间 VM 变得无响应的问题。

#### 适用于 Windows

- 修复了卷标题。修复 [docker/for-win#12616](https://github.com/docker/for-win/issues/12616)。
- 修复了 WSL 2 集成中的错误，该错误导致在重启 Docker Desktop 或切换到 Windows 容器后 Docker 命令停止工作。

## 4.6.1

{{< release-date date="2022-03-22" >}}

### 更新

- [Buildx 0.8.1](https://github.com/docker/buildx/releases/tag/v0.8.1)

### 错误修复和增强功能

- 防止 vpnkit-forwarder 中的旋转用错误消息填充日志。
- 修复了没有 HTTP 代理设置时的诊断上传。修复 [docker/for-mac#6234](https://github.com/docker/for-mac/issues/6234)。
- 从 self-diagnose 中移除了虚假的“vm is not running”错误。修复 [docker/for-mac#6233](https://github.com/docker/for-mac/issues/6233)。

## 4.6.0

{{< release-date date="2022-03-14" >}}

### 新功能

#### 适用于所有平台

- Docker Desktop Dashboard 卷管理功能现在提供使用多选复选框高效清理卷的能力。

#### 适用于 Mac

- Docker Desktop 4.6.0 为 macOS 用户提供了启用名为 VirtioFS 的新实验性文件共享技术的选项。在测试期间，VirtioFS 已显示大幅减少主机和 VM 之间同步更改所需的时间，从而带来实质性的性能改进。有关更多信息，请参阅 [VirtioFS](/manuals/desktop/settings-and-maintenance/settings.md#beta-features)。

### 更新

#### 适用于所有平台

- [Docker Engine v20.10.13](/manuals/engine/release-notes/20.10.md#201013)
- [Compose v2.3.3](https://github.com/docker/compose/releases/tag/v2.3.3)
- [Buildx 0.8.0](https://github.com/docker/buildx/releases/tag/v0.8.0)
- [containerd v1.4.13](https://github.com/containerd/containerd/releases/tag/v1.4.13)
- [runc v1.0.3](https://github.com/opencontainers/runc/releases/tag/v1.0.3)
- [Go 1.17.8](https://golang.org/doc/go1.17)
- [Linux kernel 5.10.104](https://hub.docker.com/layers/docker/for-desktop-kernel/5.10.104-379cadd2e08e8b25f932380e9fdaab97755357b3/images/sha256-7753b60f4544e5c5eed629d12151a49c8a4b48d98b4fb30e4e65cecc20da484d?context=explore)

### 安全

#### 适用于所有平台

- 修复了 [CVE-2022-0847](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-0847)，即“Dirty Pipe”，该问题可能允许攻击者从容器内部修改主机上容器镜像中的文件。
  如果使用 WSL 2 后端，您必须通过运行 `wsl --update` 更新 WSL 2。

#### 适用于 Windows

- 修复了 [CVE-2022-26659](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-26659)，该漏洞可能允许攻击者在 Docker Desktop 的安装或更新期间覆盖系统上任何管理员可写文件。

#### 适用于 Mac

- [Qemu 6.2.0](https://wiki.qemu.org/ChangeLog/6.2)

### 错误修复和增强功能

#### 适用于所有平台

- 修复了上传诊断时 HTTPS 代理设置的问题。
- 使从 systray 菜单检查更新打开 Software updates 设置部分。

#### 适用于 Mac

- 修复了启动 Docker Desktop 后 systray 菜单未显示所有菜单项的问题。修复 [docker/for-mac#6192](https://github.com/docker/for-mac/issues/6192)。
- 修复了关于 Docker Desktop 不再在后台启动的回归问题。修复 [docker/for-mac#6167](https://github.com/docker/for-mac/issues/6167)。
- 修复了缺失的 Docker Desktop Dock 图标。修复 [docker/for-mac#6173](https://github.com/docker/for-mac/issues/6173)。
- 在使用实验性 `virtualization.framework` 时加速块设备访问。请参阅 [benchmarks](https://github.com/docker/roadmap/issues/7#issuecomment-1050626886)。
- 将默认 VM 内存分配增加到物理内存的一半（最小 2 GB，最大 8 GB），以获得更好的开箱即用性能。

#### 适用于 Windows

- 修复了虽然从命令行 Docker Desktop 正常工作，但 UI 永远卡在 `starting` 状态的问题。
- 修复了缺失的 Docker Desktop systray 图标 [docker/for-win#12573](https://github.com/docker/for-win/issues/12573)
- 修复了最新 5.10.60.1 内核下的 WSL 2 Registry Access Management。
- 修复了从 WSL 2 环境启动的 Compose 应用程序选择容器时的 UI 崩溃。修复 [docker/for-win#12567](https://github.com/docker/for-win/issues/12567)。
- 修复了 Quick Start Guide 中从终端复制文本的问题。修复 [docker/for-win#12444](https://github.com/docker/for-win/issues/12444)。

### 已知问题

#### 适用于 Mac

- 启用 VirtioFS 后，具有不同 Unix 用户 ID 运行进程的容器可能遇到缓存问题。例如，如果以 `root` 运行的进程查询文件，而以用户 `nginx` 运行的另一个进程立即尝试访问同一文件，则 `nginx` 进程将收到“Permission Denied”错误。

## 4.5.1

{{< release-date date="2022-02-15" >}}

### 错误修复和增强功能

#### 适用于 Windows

- 修复了导致新安装默认使用 Hyper-V 后端而不是 WSL 2 的问题。
- 修复了导致 Docker Desktop Dashboard 崩溃从而使 systray 菜单消失的问题。

如果您在 Windows Home 上运行 Docker Desktop，安装 4.5.1 将自动将其切换回 WSL 2。如果您运行其他版本的 Windows，并且希望 Docker Desktop 使用 WSL 2 后端，则必须通过在 **Settings > General** 部分启用 **Use the WSL 2 based engine** 选项手动切换。
或者，您可以编辑位于 `%APPDATA%\Docker\settings.json` 的 Docker Desktop 设置文件，并手动将 `wslEngineEnabled` 字段的值切换为 `true`。

## 4.5.0

{{< release-date date="2022-02-10" >}}

### 新功能

- Docker Desktop 4.5.0 引入了 Docker 菜单的新版本，该版本在所有操作系统上创建一致的用户体验。有关更多信息，请参阅博客文章 [New Docker Menu & Improved Release Highlights with Docker Desktop 4.5](https://www.docker.com/blog/new-docker-menu-improved-release-highlights-with-docker-desktop-4-5/)
- 'docker version' 输出现在显示机器上安装的 Docker Desktop 版本。

### 更新

- [Amazon ECR Credential Helper v0.6.0](https://github.com/awslabs/amazon-ecr-credential-helper/releases/tag/v0.6.0)

### 安全

#### 适用于 Mac

- 修复了 [CVE-2021-44719](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-44719)，该漏洞允许使用 Docker Desktop 从容器访问主机上的任何用户文件，绕过共享文件夹的允许列表。

#### 适用于 Windows

- 修复了 [CVE-2022-23774](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-23774)，该漏洞允许攻击者移动任意文件。

### 错误修复和增强功能

#### 适用于所有平台

- 修复了在退出 Docker Desktop 并启动应用程序后 Docker Desktop 错误提示用户登录的问题。
- 通过在 Linux 中设置 `fs.inotify.max_user_watches=1048576` 和 `fs.inotify.max_user_instances=8192` 增加了文件系统监视 (inotify) 限制。修复 [docker/for-mac#6071](https://github.com/docker/for-mac/issues/6071)。

#### 适用于 Mac

- 修复了在使用 `osxfs` 且没有主机目录与 VM 共享时启动期间 VM 变得无响应的问题。
- 修复了如果应用程序以不同版本的 Docker Compose 启动，则不允许用户使用 Docker Desktop Dashboard 停止 Docker Compose 应用程序的问题。例如，如果用户在 V1 中启动 Docker Compose 应用程序，然后切换到 Docker Compose V2，则停止 Docker Compose 应用程序的尝试将失败。
- 修复了在退出 Docker Desktop 并启动应用程序后 Docker Desktop 错误提示用户登录的问题。
- 修复了 **About Docker Desktop** 窗口不再工作的问题。
- 将 Mac M1 上的 CPU 数量限制为 8 以修复启动问题。修复 [docker/for-mac#6063](https://github.com/docker/for-mac/issues/6063)。

#### 适用于 Windows

- 修复了与以版本 2 启动的 compose 应用相关的问题，但仪表板仅处理版本 1

### 已知问题

#### 适用于 Windows

从头安装 Docker Desktop 4.5.0 存在错误，该错误默认 Docker Desktop 使用 Hyper-V 后端而不是 WSL 2。这意味着 Windows Home 用户将无法启动 Docker Desktop，因为 WSL 2 是唯一支持的后端。要解决此问题，您必须从机器上卸载 4.5.0，然后下载并安装 Docker Desktop 4.5.1 或更高版本。或者，您可以编辑位于 `%APPDATA%\Docker\settings.json` 的 Docker Desktop settings.json 文件，并手动将 `wslEngineEnabled` 字段的值切换为 `true`。

## 4.4.4

{{< release-date date="2022-01-24" >}}

### 错误修复和增强功能

#### 适用于 Windows

- 修复了从 WSL 2 登录的问题。修复 [docker/for-win#12500](https://github.com/docker/for-win/issues/12500)。

### 已知问题

#### 适用于 Windows

- 通过浏览器登录后点击 **Proceed to Desktop**，有时不会将 Dashboard 置于前列。
- 登录后，当 Dashboard 获得焦点时，即使点击背景窗口，它有时仍保持在前台。作为变通方法，您需要在点击其他应用程序窗口之前点击 Dashboard。
- 当启用通过 `registry.json` 文件的组织限制时，每周提示显示在强制登录对话框之上。

## 4.4.3

{{< release-date date="2022-01-14" >}}

### 错误修复和增强功能

#### 适用于 Windows

- 禁用 Dashboard 快捷键以防止即使最小化或未聚焦时捕获它们。修复 [docker/for-win#12495](https://github.com/docker/for-win/issues/12495)。

### 已知问题

#### 适用于 Windows

- 通过浏览器登录后点击 **Proceed to Desktop**，有时不会将 Dashboard 置于前列。
- 登录后，当 Dashboard 获得焦点时，即使点击背景窗口，它有时仍保持在前台。作为变通方法，您需要在点击其他应用程序窗口之前点击 Dashboard。
- 当启用通过 `registry.json` 文件的组织限制时，每周提示显示在强制登录对话框之上。

## 4.4.2

{{< release-date date="22-01-13" >}}

### 新功能

- 使用 Auth0 和单点登录的简单、安全登录
  - 单点登录：具有 Docker Business 订阅的用户现在可以配置 SSO 以使用其身份提供程序 (IdP) 进行身份验证来访问 Docker。有关更多信息，请参阅 [单点登录](/manuals/enterprise/security/single-sign-on/_index.md)。
  - 登录 Docker Desktop 现在通过浏览器进行，因此您可以获得密码管理器自动填充的所有优势。

### 升级

- [Docker Engine v20.10.12](/manuals/engine/release-notes/20.10.md#201012)
- [Compose v2.2.3](https://github.com/docker/compose/releases/tag/v2.2.3)
- [Kubernetes 1.22.5](https://github.com/kubernetes/kubernetes/releases/tag/v1.22.5)
- [docker scan v0.16.0](https://github.com/docker/scan-cli-plugin/releases/tag/v0.16.0)

### 安全

- 修复了影响当前在 Docker Desktop 版本 4.3.0 或 4.3.1 上的用户的 [CVE-2021-45449](../security/_index.md#cve-2021-45449)。

Docker Desktop 版本 4.3.0 和 4.3.1 存在错误，该错误可能在登录期间在用户机器上记录敏感信息（访问令牌或密码）。
这仅影响用户如果他们在 4.3.0、4.3.1 上并且用户在 4.3.0、4.3.1 上登录。获取此数据需要访问用户的本地文件。

### 错误修复和增强功能

#### 适用于所有平台

- 如果 `registry.json` 中的 `allowedOrgs` 字段包含多个组织，则 Docker Desktop 显示错误。如果您为不同的开发人员组使用多个组织，则必须为每个组提供单独的 `registry.json` 文件。
- 修复了 Compose 中的回归问题，该问题将容器名称分隔符从 `-` 恢复为 `_`。修复 [docker/compose-switch](https://github.com/docker/compose-switch/issues/24)。

#### 适用于 Mac

- 修复了 Dashboard 中的容器内存统计信息。修复 [docker/for-mac/#4774](https://github.com/docker/for-mac/issues/6076)。
- 添加了 `settings.json` 中的弃用选项：`"deprecatedCgroupv1": true`，该选项将 Linux 环境切换回 cgroups v1。如果您的软件需要 cgroups v1，您应更新它以兼容 cgroups v2。虽然 cgroups v1 应继续工作，但一些未来功能可能依赖 cgroups v2。有些 Linux 内核错误也可能仅在 cgroups v2 中修复。
- 修复了将机器置于睡眠模式后暂停 Docker Desktop 导致机器从睡眠模式中恢复后 Docker Desktop 无法从暂停中恢复的问题。修复 [for-mac#6058](https://github.com/docker/for-mac/issues/6058)。

#### 适用于 Windows

- 执行 `Reset to factory defaults` 不再关闭 Docker Desktop。

### 已知问题

#### 适用于所有平台

- 当启用通过 `registry.json` 文件的组织限制时，每周提示显示在强制登录对话框之上。

#### 适用于 Windows

- 通过浏览器登录后点击 **Proceed to Desktop**，有时不会将 Dashboard 置于前列。
- 登录后，当 Dashboard 获得焦点时，即使点击背景窗口，它有时仍保持在前台。作为变通方法，您需要在点击其他应用程序窗口之前点击 Dashboard。
- 当 Dashboard 打开时，即使它没有焦点或最小化，它仍会捕获键盘快捷键（例如 ctrl-r 用于重启）

## 4.3.2

{{< release-date date="2021-12-21" >}}

### 安全

- 修复了影响当前在 Docker Desktop 版本 4.3.0 或 4.3.1 上的用户的 [CVE-2021-45449](../security/_index.md#cve-2021-45449)。

Docker Desktop 版本 4.3.0 和 4.3.1 存在错误，该错误可能在登录期间在用户机器上记录敏感信息（访问令牌或密码）。
这仅影响用户如果他们在 4.3.0、4.3.1 上并且用户在 4.3.0、4.3.1 上登录。获取此数据需要访问用户的本地文件。

### 升级

[docker scan v0.14.0](https://github.com/docker/scan-cli-plugin/releases/tag/v0.14.0)

### 安全

**Log4j 2 CVE-2021-44228**：我们已为您更新了 `docker scan` CLI 插件。
此新版本的 `docker scan` 能够检测 [Log4j 2
CVE-2021-44228](https://nvd.nist.gov/vuln/detail/CVE-2021-44228) 和 [Log4j 2
CVE-2021-45046](https://nvd.nist.gov/vuln/detail/CVE-2021-45046)

有关更多信息，请阅读博客文章 [Apache Log4j 2
CVE-2021-44228](https://www.docker.com/blog/apache-log4j-2-cve-2021-44228/)。

## 4.3.1

{{< release-date date="2021-12-11" >}}

### 升级

[docker scan v0.11.0](https://github.com/docker/scan-cli-plugin/releases/tag/v0.11.0)

### 安全

**Log4j 2 CVE-2021-44228**：我们已为您更新了 `docker scan` CLI 插件。
Docker Desktop 4.3.0 及更早版本中的旧版 `docker scan`
无法检测 [Log4j 2
CVE-2021-44228](https://nvd.nist.gov/vuln/detail/CVE-2021-44228)。

有关更多信息，请阅读
博客文章 [Apache Log4j 2
CVE-2021-44228](https://www.docker.com/blog/apache-log4j-2-cve-2021-44228/)。

## 4.3.0

{{< release-date date="2021-12-02" >}}

### 升级

- [Docker Engine v20.10.11](/manuals/engine/release-notes/20.10.md#201011)
- [containerd v1.4.12](https://github.com/containerd/containerd/releases/tag/v1.4.12)
- [Buildx 0.7.1](https://github.com/docker/buildx/releases/tag/v0.7.1)
- [Compose v2.2.1](https://github.com/docker/compose/releases/tag/v2.2.1)
- [Kubernetes 1.22.4](https://github.com/kubernetes/kubernetes/releases/tag/v1.22.4)
- [Docker Hub Tool v0.4.4](https://github.com/docker/hub-tool/releases/tag/v0.4.4)
- [Go 1.17.3](https://golang.org/doc/go1.17)

### 错误修复和小更改

#### 适用于所有平台

- 如果主机缺少 Internet 连接，则添加 self-diagnose 警告。
- 修复了阻止用户使用 Volumes UI 中的 Save As 选项从卷保存文件的问题。修复 [docker/for-win#12407](https://github.com/docker/for-win/issues/12407)。
- Docker Desktop 现在使用 cgroupv2。如果需要在容器中运行 `systemd`，则：
  - 确保您的 `systemd` 版本支持 cgroupv2。[它必须至少为 `systemd` 247](https://github.com/systemd/systemd/issues/19760#issuecomment-851565075)。考虑将任何 `centos:7` 镜像升级到 `centos:8`。
  - 运行 `systemd` 的容器需要以下选项：[`--privileged --cgroupns=host -v /sys/fs/cgroup:/sys/fs/cgroup:rw`](https://serverfault.com/questions/1053187/systemd-fails-to-run-in-a-docker-container-when-using-cgroupv2-cgroupns-priva)。

#### 适用于 Mac

- Apple silicon 上的 Docker Desktop 不再需要 Rosetta 2，[三个可选命令行工具](/manuals/desktop/troubleshoot-and-support/troubleshoot/known-issues.md)除外。

#### 适用于 Windows

- 修复了如果主目录路径包含正则表达式中使用的字符，则导致 Docker Desktop 在启动期间失败的问题。修复 [docker/for-win#12374](https://github.com/docker/for-win/issues/12374)。

### 已知问题

Hyper-V 基于的机器上 Docker Desktop Dashboard 错误地将容器内存使用量显示为零。
您可以使用命令行上的 [`docker stats`](/reference/cli/docker/container/stats.md)
命令作为变通方法查看
实际内存使用量。请参阅
[docker/for-mac#6076](https://github.com/docker/for-mac/issues/6076)。

### 弃用

- 以下内部 DNS 名称已弃用，并将在未来版本中移除：`docker-for-desktop`、`docker-desktop`、`docker.for.mac.host.internal`、`docker.for.mac.localhost`、`docker.for.mac.gateway.internal`。您现在必须使用 `host.docker.internal`、`vm.docker.internal` 和 `gateway.docker.internal`。
- 移除：自定义 RBAC 规则已从 Docker Desktop 中移除，因为它为所有 Service Accounts 提供了 `cluster-admin` 权限。修复 [docker/for-mac/#4774](https://github.com/docker/for-mac/issues/4774)。

## 4.2.0

{{< release-date date="2021-11-09" >}}

### 新功能

**暂停/恢复**：当您不积极使用时，现在可以暂停 Docker Desktop 会话并节省机器上的 CPU 资源。

- 实现 [Docker Public Roadmap#226](https://github.com/docker/roadmap/issues/226)

**软件更新**：关闭自动检查更新的选项现在适用于所有 Docker 订阅的用户，包括 Docker Personal 和 Docker Pro。所有更新相关设置已移至 **Software Updates** 部分。

- 实现 [Docker Public Roadmap#228](https://github.com/docker/roadmap/issues/228)

**窗口管理**：关闭并重新打开 Docker Desktop 时，Docker Desktop Dashboard 窗口大小和位置会持久化。

### 升级

- [Docker Engine v20.10.10](/manuals/engine/release-notes/20.10.md#201010)
- [containerd v1.4.11](https://github.com/containerd/containerd/releases/tag/v1.4.11)
- [runc v1.0.2](https://github.com/opencontainers/runc/releases/tag/v1.0.2)
- [Go 1.17.2](https://golang.org/doc/go1.17)
- [Compose v2.1.1](https://github.com/docker/compose/releases/tag/v2.1.1)
- [docker-scan 0.9.0](https://github.com/docker/scan-cli-plugin/releases/tag/v0.9.0)

### 错误修复和小更改

#### 适用于所有平台

- 改进：Self-diagnose 现在还检查主机 IP 和 `docker networks` 之间的重叠。
- 修复了 Docker Desktop Dashboard 上显示更新可用性的指示器位置。

#### 适用于 Mac

- 修复了点击致命错误对话框上的 **Exit** 时导致 Docker Desktop 停止响应的问题。
- 修复了影响具有从主机目录顶部绑定挂载的 `docker volume` 的用户的罕见启动失败。如果存在，此修复还将移除相应主机目录上手动用户添加的 `DENY DELETE` ACL 条目。
- 修复了升级时 `Docker.qcow2` 文件被忽略而使用新的 `Docker.raw` 导致容器和镜像消失的错误。请注意，如果系统同时具有两个文件（由于之前的错误），则将使用最近修改的文件，以避免最近的容器和镜像再次消失。要强制使用旧的 `Docker.qcow2`，请删除较新的 `Docker.raw` 文件。修复 [docker/for-mac#5998](https://github.com/docker/for-mac/issues/5998)。
- 修复了关闭期间子进程意外失败从而触发意外致命错误弹出窗口的错误。修复 [docker/for-mac#5834](https://github.com/docker/for-mac/issues/5834)。

#### 适用于 Windows

- 修复了点击致命错误对话框中的 Exit 时 Docker Desktop 有时挂起的错误。
- 修复了更新已下载但尚未应用时频繁显示 **Download update** 弹出窗口的问题 [docker/for-win#12188](https://github.com/docker/for-win/issues/12188)。
- 修复了安装新更新在应用程序有时间关闭之前杀死应用程序的问题。
- 修复：Docker Desktop 的安装现在即使组策略阻止用户启动先决条件服务（例如 LanmanServer）也能工作 [docker/for-win#12291](https://github.com/docker/for-win/issues/12291)。

## 4.1.1

{{< release-date date="2021-10-12" >}}

### 错误修复和小更改

#### 适用于 Mac

> 从 4.1.0 升级时，Docker 菜单不会更改为 **Update and restart**，因此您可以等待下载完成（图标更改）然后选择 **Restart**。此错误已在 4.1.1 中修复，用于未来升级。

- 修复了升级时 `Docker.qcow2` 文件被忽略而使用新的 `Docker.raw` 导致容器和镜像消失的错误。如果系统同时具有两个文件（由于之前的错误），则将使用最近修改的文件，以避免最近的容器和镜像再次消失。要强制使用旧的 `Docker.qcow2`，请删除较新的 `Docker.raw` 文件。修复 [docker/for-mac#5998](https://github.com/docker/for-mac/issues/5998)。
- 修复了更新通知叠加层有时在 **Settings** 按钮和 Docker Desktop Dashboard 中的 **Software update** 按钮之间不同步的问题。
- 修复了安装新下载的 Docker Desktop 更新的菜单条目。当更新准备好安装时，**Restart** 选项更改为 **Update and restart**。

#### 适用于 Windows

- 修复了某些发行版（例如 Arch 或 Alpine）的 WSL 2 集成回归问题。修复 [docker/for-win#12229](https://github.com/docker/for-win/issues/12229)
- 修复了更新通知叠加层有时在 Settings 按钮和 Dashboard 中的 Software update 按钮之间不同步的问题。

## 4.1.0

{{< release-date date="2021-09-30" >}}

### 新功能

- **软件更新**：Settings 选项卡现在包含一个新部分，以帮助您管理 Docker Desktop 更新。**Software Updates** 部分在有新更新时通知您，并允许您下载更新或查看较新版本中包含的内容的信息。
- **Compose V2** 现在可以在 General 设置中指定是否使用 Docker Compose V2。
- **卷管理**：卷管理现在适用于任何订阅的用户，包括 Docker Personal。实现 [Docker Public Roadmap#215](https://github.com/docker/roadmap/issues/215)

### 升级

- [Compose V2](https://github.com/docker/compose/releases/tag/v2.0.0)
- [Buildx 0.6.3](https://github.com/docker/buildx/releases/tag/v0.6.3)
- [Kubernetes 1.21.5](https://github.com/kubernetes/kubernetes/releases/tag/v1.21.5)
- [Go 1.17.1](https://github.com/golang/go/releases/tag/go1.17.1)
- [Alpine 3.14](https://alpinelinux.org/posts/Alpine-3.14.0-released.html)
- [Qemu 6.1.0](https://wiki.qemu.org/ChangeLog/6.1)
- 基础发行版为 debian:bullseye

### 错误修复和小更改

#### 适用于 Windows

- 修复了与反恶意软件软件触发相关的错误，self-diagnose 避免调用 `net.exe` 实用程序。
- 修复了 self-diagnose 中的 WSL 2 Linux VM 文件系统损坏。这可能由 [microsoft/WSL#5895](https://github.com/microsoft/WSL/issues/5895) 引起。
- 修复了 `SeSecurityPrivilege` 要求问题。请参阅 [docker/for-win#12037](https://github.com/docker/for-win/issues/12037)。
- 修复了与 UI 的 CLI 上下文切换同步。请参阅 [docker/for-win#11721](https://github.com/docker/for-win/issues/11721)。
- 将键 `vpnKitMaxPortIdleTime` 添加到 `settings.json` 以允许禁用或扩展空闲网络连接超时。
- 修复了退出时的崩溃。请参阅 [docker/for-win#12128](https://github.com/docker/for-win/issues/12128)。
- 修复了 CLI 工具在 WSL 2 发行版中不可用的问题。
- 修复了因 panic.log 上的访问权限而卡在从 Linux 到 Windows 容器的切换。 [for-win#11899](https://github.com/docker/for-win/issues/11899)。

### 已知问题

#### 适用于 Windows

在某些基于 WSL 的发行版（如 ArchWSL）上升级到 4.1.0 时 Docker Desktop 可能无法启动。请参阅 [docker/for-win#12229](https://github.com/docker/for-win/issues/12229)

## 4.0.1

{{< release-date date="2021-09-13" >}}

### 升级

- [Compose V2 RC3](https://github.com/docker/compose/releases/tag/v2.0.0-rc.3)
  - Compose v2 现在托管在 github.com/docker/compose。
  - 修复了使用 `compose up --scale` 缩减时的 go 恐慌。
  - 修复了 `compose run --rm` 捕获退出代码时的竞争条件。

### 错误修复和小更改

#### 适用于所有平台

- 修复了 Docker Desktop Dashboard 中复制粘贴不可用的问题。

#### 适用于 Windows

- 修复了 Hyper-V 引擎下 Docker Desktop 未正确启动的问题。请参阅 [docker/for-win#11963](https://github.com/docker/for-win/issues/11963)

## 4.0.0

{{< release-date date="2021-08-31" >}}

### 新功能

Docker 已[宣布](https://www.docker.com/blog/updating-product-subscriptions/)对产品订阅的更新和扩展，以提高开发人员和企业的生产力、协作和安全性。

更新的 [Docker Subscription Service Agreement](https://www.docker.com/legal/docker-subscription-service-agreement) 包括对 **Docker Desktop** 条款的更改。

- Docker Desktop 对于小型企业（员工少于 250 人且年收入少于 1000 万美元）、个人使用、教育和非商业开源项目**保持免费**。
- 对于大型企业的专业使用，需要付费订阅（**Pro、Team 或 Business**），每月低至 5 美元。
- 这些条款的生效日期为 2021 年 8 月 31 日。对于需要付费订阅使用 Docker Desktop 的用户，有至 2022 年 1 月 31 日的宽限期。
- Docker Pro 和 Docker Team 订阅现在**包括** Docker Desktop 的商业使用。
- 现有的 Docker Free 订阅已重命名为 **Docker Personal**。
- 对 Docker Engine 或任何其他上游**开源** Docker 或 Moby 项目**无更改**。

要了解这些更改如何影响您，请阅读 [常见问题解答](https://www.docker.com/pricing/faq)。
有关更多信息，请参阅 [Docker 订阅概述](../subscription/_index.md)。

### 升级

- [Compose V2 RC2](https://github.com/docker/compose-cli/releases/tag/v2.0.0-rc.2)
  - 修复了 `compose down` 的项目名称对大小写不敏感。请参阅 [docker/compose-cli#2023](https://github.com/docker/compose-cli/issues/2023)
  - 修复了非规范化项目名称。
  - 修复了部分引用上的端口合并。
- [Kubernetes 1.21.4](https://github.com/kubernetes/kubernetes/releases/tag/v1.21.4)

### 错误修复和小更改

#### 适用于 Mac

- 修复了从 git URL 构建时 SSH 不可用的问题。修复 [for-mac#5902](https://github.com/docker/for-mac/issues/5902)

#### 适用于 Windows

- 修复了 CLI 工具在 WSL 2 发行版中不可用的问题。
- 修复了因 panic.log 上的访问权限而导致从 Linux 到 Windows 容器的切换问题。 [for-win#11899](https://github.com/docker/for-win/issues/11899)