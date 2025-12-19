---
description: 查找适用于 Mac、Linux 和 Windows 的 Docker Desktop 发布说明。
keywords: Docker desktop, release notes, linux, mac, windows
title: Docker Desktop 发布说明
linkTitle: 发布说明
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
{{< rss-button feed="/desktop/release-notes/index.xml" text="订阅 Docker Desktop RSS 订阅源" >}}

<!-- vale off -->

本页面包含有关 Docker Desktop 发布版本的新功能、改进、已知问题和错误修复的信息。

发布版本会逐步推出，以确保质量控制。如果最新版本尚未提供给您，请稍等片刻——更新通常在发布日期后一周内可用。

比最新发布版本早 6 个月以上的 Docker Desktop 版本将不再提供下载。先前的发布说明可在我们的 [文档仓库](https://github.com/docker/docs/tree/main/content/manuals/desktop/previous-versions) 中获取。

有关更多常见问题，请参阅 [常见问题解答](/manuals/desktop/troubleshoot-and-support/faqs/releases.md)。

## 4.55.0

{{< release-date date="2025-12-16" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.55.0" build_path="/213807/" >}}

### 更新

- [Docker Engine v29.1.3](https://docs.docker.com/engine/release-notes/29/#2913)
- [cagent v1.15.1](https://github.com/docker/cagent/releases/tag/v1.15.1)

### 问题修复与增强

#### 适用于所有平台

- 修复了导致 Docker Desktop 在启动期间卡住的问题。
- 当 `daemon.json` 无效时，改进了错误消息。
- 修复了在长时间的 Ask Gordon 会话中，每次按键都会导致的性能问题。

> [!IMPORTANT]
>
> Wasm 工作负载将在未来的 Docker Desktop 版本中被弃用并移除。

## 4.54.0

{{< release-date date="2025-12-04" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.54.0" build_path="/212467/" >}}

### 新增功能

- 在带有 WSL2 和 NVIDIA GPU 的 Windows 上的 Docker Model Runner 中添加了对 vLLM 的支持。

### 问题修复与增强

#### 适用于 Mac

- 修复了 `/dev/shm` 权限不足，导致容器无法写入的问题。修复了 [docker/for-mac#7804](https://github.com/docker/for-mac/issues/7804)。 

### 升级

- [Docker Buildx v0.30.1](https://github.com/docker/buildx/releases/tag/v0.30.1)
- [Docker Engine v29.1.2](https://docs.docker.com/engine/release-notes/29/#2912)
- [Runc v1.3.4](https://github.com/opencontainers/runc/releases/tag/v1.3.4)
- [Docker Model Runner CLI v1.0.2](https://github.com/docker/model-runner/releases/tag/cmd%2Fcli%2Fv1.0.2)

### 安全性 

- 添加了一个安全补丁以解决 [CVE-2025-13743](https://www.cve.org/cverecord?id=CVE-2025-13743)，该漏洞导致 Docker Desktop 诊断包因错误对象序列化而在日志输出中包含了过期的 Hub PAT。

## 4.53.0

{{< release-date date="2025-11-27" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.53.0" build_path="/211793/" >}}

### 问题修复与增强

#### 适用于所有平台

- 修复了一个问题，该问题导致支持诊断工具无意中捕获了过期的 Docker Hub 授权 bearer 令牌。

### 安全性 

- 添加了安全补丁，以解决在使用 [增强容器隔离](https://docs.docker.com/enterprise/security/hardened-desktop/enhanced-container-isolation) 时的 CVE 漏洞 [2025-52565](https://github.com/opencontainers/runc/security/advisories/GHSA-9493-h29p-rfm2)、[2025-52881](https://github.com/opencontainers/runc/security/advisories/GHSA-cgrx-mc8f-2prm) 和 [2025-31133](https://github.com/opencontainers/runc/security/advisories/GHSA-qw9x-cqr3-wc7r)。 

## 4.52.0

{{< release-date date="2025-11-20" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.52.0" build_path="/210994/" >}}

### 新增功能

- 向 Docker Desktop 添加了新的端口绑定设置。管理员也可以通过使用 `admin-settings.json` 文件的设置管理来控制此项。
- 添加了一个新的 Docker Model Runner 命令。使用 `docker model purge` 可以删除您的所有模型。

### 升级

- [Docker Engine v29.0.0](/manuals/engine/release-notes/29.md#2900)
- [Docker Model Runner v1.0.3](https://github.com/docker/model-runner/releases/tag/v1.0.3)
- [Docker Model Runner CLI v1.0.0](https://github.com/docker/model-runner/releases/tag/cmd%2Fcli%2Fv1.0.0)
- Docker MCP 插件 `v0.28.0`

### 问题修复与增强

#### 适用于所有平台 

- Docker MCP Toolkit 改进：
   - Amazon Q 客户端支持
   - 与 Docker Engine 的 OAuth DCR (动态客户端注册)
   - 使用 CLI 创建 MCP 配置文件
- Docker Model Runner 改进：
   - 您现在可以跳过 [Docker Model Runner 的 OpenAI API 端点](/manuals/ai/model-runner/api-reference.md#rest-api-examples) `curl http://localhost:12434/v1/models` 的 `/engines` 前缀。
   - 您现在可以跳过使用 `docker model pull` 从 [Docker Hub 上发布的](https://hub.docker.com/u/ai) 模型的 `ai/` 前缀。
   - 下载中断后现在会恢复。

#### 适用于 Windows

- 修复了 Kerberos/NTLM 代理登录的问题。

## 4.51.0

{{< release-date date="2025-11-13" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.51.0" build_path="/210443/" >}}

### 新增功能

- 您现在可以从 **Kubernetes** 视图设置您的 Kubernetes 资源。这个新视图还实时显示您的 pods、服务和部署。

### 升级

- [Docker Engine v28.5.2](/manuals/engine/release-notes/28.md#2852)
- Linux 内核 `v6.12.54`

### 问题修复与增强

#### 适用于所有平台 

- Kind 现在仅在依赖镜像本地不可用时才拉取所需的镜像。

## 4.50.0

{{< release-date date="2025-11-06" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.50.0" build_path="/209931/" >}}

### 新增功能

- [动态 MCP](/manuals/ai/mcp-catalog-and-toolkit/dynamic-mcp.md)（实验性）现已在 Docker Desktop 中可用。
- 引入了新的欢迎调查，以改进新用户引导。新用户现在可以提供信息来帮助定制其 Docker Desktop 体验。

### 升级

- [Docker Compose v2.40.3](https://github.com/docker/compose/releases/tag/v2.40.3)
- [NVIDIA Container Toolkit v1.18.0](https://github.com/NVIDIA/nvidia-container-toolkit/releases/tag/v1.18.0)

### 问题修复与增强

#### 适用于所有平台 

- Docker Desktop 现在检测并尝试避免“Docker 子网”与使用 RFC1918 地址的物理网络之间的冲突。例如，如果主机具有与 `192.168.65.0/24` 重叠的非默认路由，则会自动选择一个备用网络。您仍然可以像以前一样通过 Docker Desktop 设置和管理员设置来覆盖该选择。
- Docker Desktop 不再将 Stargz Snapshotter 故障视为致命故障。如果发生故障，Docker Desktop 将继续运行而不使用 Stargz Snapshotter。
- Ask Gordon 不再显示用户提供 URL 的镜像。
- Ask Gordon 在运行所有内置和所有用户添加的 MCP 工具之前现在会请求确认。

## 4.49.0

{{< release-date date="2025-10-23" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.49.0" build_path="/208700/" >}}

> [!IMPORTANT]
>
> 对 Windows 10 21H2 (19044) 和 11 22H2 (22621) 的支持已结束。在下一版本中，安装 Docker Desktop 将需要 Windows 10 22H2 (19045) 或 Windows 11 23H2 (22631)。

### 安全性

- 修复了 [CVE-2025-9164](https://www.cve.org/cverecord?id=CVE-2025-9164)，该漏洞导致 Docker Desktop for Windows 安装程序由于不安全的 DLL 搜索顺序而容易受到 DLL 劫持攻击。安装程序在检查系统目录之前先在用户的“下载”文件夹中搜索所需的 DLL，从而允许通过恶意 DLL 放置进行本地权限提升。

### 新增功能 

- [cagent](/manuals/ai/cagent/_index.md) 现已通过 Docker Desktop 提供。 
- [Docker Debug](/reference/cli/docker/debug.md) 现在对所有用户免费。 

### 升级

- [Docker Engine v28.5.1](/manuals/engine/release-notes/28.md#2851)
- [Docker Compose v2.40.2](https://github.com/docker/compose/releases/tag/v2.40.2)
- [NVIDIA Container Toolkit v1.17.9](https://github.com/NVIDIA/nvidia-container-toolkit/releases/tag/v1.17.9)
- Docker Debug `v0.0.45` 

### 问题修复与增强

#### 适用于所有平台

- 修复了 Docker Desktop 在等待用户输入新密码时使用过期代理密码的问题。
- 修复了在启动 Docker Debug 时显示的 'chown' 错误。
- 修复了导致某些转发的 UDP 端口挂起的错误。 

#### 适用于 Mac

- 修复了当另一个 Kubernetes 上下文处于活动状态时，Kubernetes 启动挂起的问题。修复了 https://github.com/docker/for-mac/issues/7771。
- 如果 Rosetta 安装被取消或失败，Rosetta 将在 Docker Desktop 中被禁用。
- 在 macOS 上安装或更新 Docker Desktop 的最低操作系统版本现在是 macOS Sonoma (版本 14) 或更高版本。

## 4.48.0

{{< release-date date="2025-10-09" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.48.0" build_path="/207573/" >}}

> [!IMPORTANT]
>
> 对 macOS 13 的支持已结束。在下一版本中，安装 Docker Desktop 将需要 macOS 14。

### 新增功能

- 您现在可以使用安装程序标志为 [macOS](/manuals/desktop/setup/install/mac-install.md#proxy-configuration) 和 [Windows](/manuals/desktop/setup/install/windows-install.md#proxy-configuration) 指定 PAC 文件和嵌入式 PAC 脚本。 
- 管理员现在可以通过 [macOS 配置文件](/manuals/enterprise/security/enforce-sign-in/methods.md#macos-configuration-profiles-method-recommended) 设置代理设置。 

### 升级

- [Docker Compose v2.40.0](https://github.com/docker/compose/releases/tag/v2.40.0)
- [Docker Buildx v0.29.1](https://github.com/docker/buildx/releases/tag/v0.29.1)
- [Docker Engine v28.5.1](https://docs.docker.com/engine/release-notes/28/#2851)
- Docker MCP 插件 `v0.22.0`
- [Docker Model CLI v0.1.42](https://github.com/docker/model-cli/releases/tag/v0.1.42)

### 问题修复与增强

#### 适用于所有平台 

- 修复了有时在 Desktop 重启时 kind 集群状态被重置的问题。修复了 [docker/for-mac#77445](https://github.com/docker/for-mac/issues/7745)。
- 移除了过时的 `mcp` 键以与最新的 VS Code MCP 服务器更改保持一致。
- 将凭证辅助程序更新到 [v0.9.4](https://github.com/docker/docker-credential-helpers/releases/tag/v0.9.4)。
- 修复了 Docker Desktop 在等待用户输入新密码时使用过期代理密码的问题。 
- 修复了导致 Docker Desktop 在某些条件下定期使用 Docker CLI 工具创建新进程的错误。修复了 [docker/for-win#14944](https://github.com/docker/for-win/issues/14944)。
- 修复了导致通过 Compose 在 Docker Model Runner 中无法为嵌入配置模型的错误。要指定模型应配置为嵌入，您必须按照 [AI Models in Docker Compose](https://docs.docker.com/ai/compose/models-and-compose/#model-configuration-options) 中的描述显式添加 `--embeddings` 运行时标志。修复了 [docker/model-runner#166](https://github.com/docker/model-runner/issues/166)。

#### 适用于 Windows

- 移除了 `HKLM\SOFTWARE\Docker Inc.\Docker\1.0` 注册表项。改为在路径中查找 `docker.exe` 以确定 Docker Desktop 的安装位置。
- 修复了在 IPv6 被禁用时的 WSL 2 模式下的启动问题。

## 4.47.0

{{< release-date date="2025-09-25" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.47.0" build_path="/206054/" >}}

### 安全性

- 修复了 [CVE-2025-10657](https://www.cve.org/CVERecord?id=CVE-2025-10657)，该漏洞导致 Docker Desktop 4.46.0 版本中的增强容器隔离 [Docker Socket 命令限制](../enterprise/security/hardened-desktop/enhanced-container-isolation/config.md#command-restrictions) 功能无法正常工作（其配置被忽略）。

### 新增功能

- 向 Docker 的 MCP 目录添加了动态 MCP 服务器发现和支持。
- 使用增强容器隔离时，管理员现在可以阻止具有 Docker socket 挂载的容器中的 `docker plugin` 和 `docker login` 命令。
- 添加了一个新的 Docker Model Runner 命令。使用 `docker model requests` 可以获取请求和响应。

### 升级

- [Docker Compose v2.39.4](https://github.com/docker/compose/releases/tag/v2.39.4)
- [Kubernetes v1.34.1](https://github.com/kubernetes/kubernetes/releases/tag/v1.34.1)
  - [CNI plugins v1.7.1](https://github.com/containernetworking/plugins/releases/tag/v1.7.1)
  - [cri-tools v1.33.0](https://github.com/kubernetes-sigs/cri-tools/releases/tag/v1.33.0)
  - [cri-dockerd v0.3.20](https://github.com/Mirantis/cri-dockerd/releases/tag/v0.3.20)
- Docker Debug `v0.0.44`

### 问题修复与增强

#### 适用于所有平台

- 您现在可以通过过滤器、排序和改进的搜索功能更轻松地搜索 MCP 服务器。
- Docker Debug 在调试设置了环境变量为空值的容器时不再挂起。
- 增强了 Docker Model Runner，在 CLI 中提供丰富的响应渲染，在 Docker Desktop 仪表板中提供对话上下文，以及可恢复的下载。

#### 适用于 Mac

- 移除了 `com.apple.security.cs.allow-dyld-environment-variables` 权限，该权限允许通过 `DYLD_INSERT_LIBRARIES` 环境变量加载带有 Docker Desktop 的已签名的任意动态库。
- 修复了回归问题，该问题导致配置文件登录强制在某些客户环境中失效。
- 修复了有时导致 `docker model package` 命令在写入本地内容存储（不使用 `--push` 标志）时挂起的错误。
- 修复了导致使用 `unless-stopped` 重启策略启动的容器从未重启的错误。修复了 [docker/for-mac#7744](https://github.com/docker/for-mac/issues/7744)。

#### 适用于 Windows

- 修复了 Docker MCP Toolkit 在 Windows 上的 Goose MCP 客户端连接问题。
- 解决了在集成尝试失败后，“跳过集成”WSL 发行版选项的问题。
- 修复了有时导致 `docker model package` 命令在写入本地内容存储（不使用 `--push` 标志）时挂起的错误。

## 4.46.0

{{< release-date date="2025-09-11" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.46.0" build_path="/204649/" >}}

### 新增功能

- 为 Docker MCP Toolkit 添加了新的学习中心导览以及其他新用户引导改进。
- 管理员现在可以通过设置管理来控制 [PAC 配置](/manuals/enterprise/security/hardened-desktop/settings-management/configure-json-file.md#proxy-settings)。
- 更新体验已重新设计，使其更易于理解和管理 Docker Desktop 及其组件的更新。

### 升级

- [Docker Buildx v0.28.0](https://github.com/docker/buildx/releases/tag/v0.28.0)
- [Docker Engine v28.4.0](https://docs.docker.com/engine/release-notes/28/#2840)

### 问题修复与增强

#### 适用于所有平台

- 使用 Docker CLI，当 Docker 上下文元数据中存在键值对（`"GODEBUG":"..."`）时，您现在可以设置 `GODEBUG` 环境变量。这意味着默认情况下支持 CLI 二进制文件中具有负序列号的证书。
- 更新了 Docker 订阅服务协议链接以指向最新版本。

#### 适用于 Mac

- 通过启用 `llama.cpp` 推理进程的沙盒，提高了 Docker Model Runner 的安全性。
- 修复了导致 Docker Desktop 启动缓慢且显示为冻结状态的错误。修复了 [docker/for-mac#7671](https://github.com/docker/for-mac/issues/7671)。

#### 适用于 Windows

- 通过启用 `llama.cpp` 推理进程的沙盒，提高了 Docker Model Runner 的安全性。

#### 适用于 Linux

- 修复了 RHEL 卸载序列中的路径问题。

## 4.45.0

{{< release-date date="2025-08-28" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.45.0" build_path="/203075/" >}}

### 新增功能

- [Docker Model Runner](/manuals/ai/model-runner/_index.md) 现已正式发布。

### 升级

- [Docker Compose v2.39.2](https://github.com/docker/compose/releases/tag/v2.39.2)
- [Docker Buildx v0.27.0](https://github.com/docker/buildx/releases/tag/v0.27.0)
- [Docker Scout CLI v1.18.3](https://github.com/docker/scout-cli/releases/tag/v1.18.3)
- [Docker Engine v28.3.3](https://docs.docker.com/engine/release-notes/28/#2833)

### 问题修复与增强

#### 适用于所有平台

- 修复了导致 `com.docker.diagnose` 在通过需要身份验证的代理上传诊断包时崩溃的错误。
- `kind` 依赖镜像 `envoyproxy/envoy` 已从 v1.32.0 升级到 v1.32.6。如果您镜像 `kind` 镜像，请确保您的镜像已更新。

#### 适用于 Mac

- 修复了导致 Docker Desktop 在笔记本电脑从睡眠中唤醒后崩溃的错误。修复了 [docker/for-mac#7741](https://github.com/docker/for-mac/issues/7741)。
- 修复了虚拟机有时因错误 **The virtual machine stopped unexpectedly.** 而失败的问题。
- 修复了容器在启动后连接到网络或从网络断开时破坏端口映射的错误。修复了 [docker/for-mac#7693](https://github.com/docker/for-mac/issues/7693)。

#### 适用于 Windows

- 修复了当用户缺乏正确权限时，阻止 CLI 插件默认部署到 `~/.docker/cli-plugins` 的错误。
- 修复了如果 `docker-desktop` 发行版不存在，重新定位 WSL 数据分发将失败的问题。
- 修复了 Docker Desktop 仪表板中 WSL 安装 URL 的拼写错误。
- 修复了某些 WSL 发行版集成失败的问题。修复了 [docker/for-win#14686](https://github.com/docker/for-win/issues/14686)

## 4.44.3

{{< release-date date="2025-08-20" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.44.3" build_path="/202357/" >}}

### 安全性

- 修复了 [CVE-2025-9074](https://www.cve.org/CVERecord?id=CVE-2025-9074)，该漏洞允许在 Docker Desktop 上运行的恶意容器无需挂载 Docker socket 即可访问 Docker Engine 并启动其他容器。这可能允许未经授权访问主机系统上的用户文件。增强容器隔离 (ECI) 无法缓解此漏洞。

### 问题修复与增强

- 修复了导致 Docker Offload 对话框阻止用户访问仪表板的错误。

## 4.44.2

{{< release-date date="2025-08-15" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.44.2" build_path="/202017/" >}}

### 问题修复与增强

 - 添加了 [Docker Offload](/manuals/offload/_index.md) 到 **Beta 功能**设置选项卡，并包含支持 [Docker Offload Beta](https://www.docker.com/products/docker-offload/) 的更新。

## 4.44.1

{{< release-date date="2025-08-13" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.44.1" build_path="/201842/" >}}

### 问题修复与增强

#### 适用于所有平台

- 修复了 4.44.0 版本中发现的问题，该问题导致当 `vpnkit` CIDR 被锁定但在 Desktop 设置管理中未指定值时启动失败。

#### 适用于 Windows

- 修复了在使用旧版本包的 `version-pack-data` 目录结构的分发版升级后，卷和容器不可见的问题。
- 解决了 WSL 2 中一个罕见问题，该问题导致 Docker CLI 失败并出现 **Proxy Authentication Required** 错误。
- 修复了如果用户对该目录缺乏执行权限，CLI 插件未部署到 `~/.docker/cli-plugins` 的错误。

## 4.44.0

{{< release-date date="2025-08-07" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.55.0" build_path="/201307/" >}}

### 新增功能

- WSL 2 稳定性改进。
- 您现在可以检查请求和响应，以帮助诊断 Docker Model Runner 中的模型相关问题。
- 添加了运行多个模型的功能，并在资源不足时收到警告。这避免了使用大型模型时 Docker Desktop 冻结。
- 向 MCP Toolkit 添加了新的 MCP 客户端：Gemini CLI、Goose。
- 为 `docker desktop enable model-runner` 引入了 `--gpu`（仅限 Windows）和 `--cors` 标志。
- 向 Docker Desktop CLI 添加了新的 `docker desktop kubernetes` 命令。
- 您现在可以在 **设置**中搜索特定的配置选项。
- Apple Virtualization 现在是默认的 VMM，以获得更好的性能，并移除了 QEMU Virtualization。参阅[博客文章](https