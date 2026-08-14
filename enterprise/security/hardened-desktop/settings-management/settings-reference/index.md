# 设置参考


本参考文档记录了管理员可以使用[设置管理](/manuals/enterprise/security/hardened-desktop/settings-management/_index.md)配置的 Docker Desktop 设置。使用本页可以了解哪些设置可用、它们的可接受值、平台兼容性以及适用的配置方法。

> [!NOTE]
>
> 本页仅涵盖面向向组织部署 Docker Desktop 的管理员的可配置设置。有关 Docker Desktop 面向用户的完整设置列表，请参阅[更改设置](/manuals/desktop/settings-and-maintenance/settings.md)。

## 常规

### 发送使用情况统计信息

控制 Docker Desktop 是否收集并向 Docker 发送本地使用情况统计信息和崩溃报告。不影响通过 Docker Hub 或其他后端服务（如登录时间戳、拉取或构建）收集的服务器端遥测数据。

| 属性 | 值 |
|---|---|
| 默认值 | `true` |
| 可接受值 | `true`, `false` |
| 格式 | Boolean |
| JSON 键 | `analyticsEnabled` |
| Docker Home | **发送使用情况统计信息** |

> [!NOTE]
>
> 在强化环境中，禁用并锁定此设置。这可让您控制所有数据流，并在需要时通过安全渠道收集支持日志。

### 自动检查更新

控制 Docker Desktop 是否检查并通知用户可用的更新。当设置为 `true` 时，将禁用更新检查和通知。

| 属性 | 值 |
|---|---|
| 默认值 | `false` |
| 可接受值 | `true`, `false` |
| 格式 | Boolean |
| JSON 键 | `disableUpdate` |
| Docker Home | **禁用更新** |

> [!NOTE]
>
> 在强化环境中，启用并锁定此设置。这可保证只安装经过内部审查的版本。

### 自动更新组件

允许 Docker Desktop 自动更新不需要重启的组件，例如 Docker Compose、Docker Scout 和 Docker CLI。

| 属性 | 值 |
|---|---|
| 默认值 | `true` |
| 可接受值 | `true`, `false` |
| 格式 | Boolean |
| JSON 键 | `silentModulesUpdate` |
| Docker Home | **自动更新组件** |

### 启用 Gordon

| 属性 | 值 |
|---|---|
| 默认值 | `false` |
| 可接受值（个人用户） | `true`, `false` |
| 可接受值（Business 套餐） | `"Disabled"`, `"Enabled"`, `"Always Enabled"` |
| JSON 键 | `enableDockerAI` |
| Docker Home | **启用 Gordon** |

> [!IMPORTANT]
>
> Docker Business 客户必须在 Docker Home 中将此设置为 `"Enabled"` 或 `"Always Enabled"`。仅设置为 `"User Defined"`（用户定义）不会激活 Gordon。

### 阻止 `docker load`

阻止用户使用 `docker load` 命令加载本地 Docker 镜像，通过要求所有镜像都来自注册表来强制镜像来源可信。

| 属性 | 值 |
|---|---|
| 默认值 | `false` |
| 可接受值 | `true`, `false` |
| 格式 | Boolean |
| JSON 键 | `blockDockerLoad` |
| Docker Home | **阻止 Docker Load** |

> [!NOTE]
>
> 在强化环境中，启用并锁定此设置。这会强制所有镜像都来自您经过安全扫描的注册表。

### 隐藏入门调查

阻止向新用户显示入门调查。

| 属性 | 值 |
|---|---|
| 默认值 | `false` |
| 可接受值 | `true`, `false` |
| 格式 | Boolean |
| JSON 键 | `displayedOnboarding` |
| Docker Home | **隐藏入门调查** |

### 启用 Docker 终端

允许或限制访问用于与主机系统交互的内置终端。当设置为 `false` 时，用户无法使用 Docker 终端与主机交互或直接从 Docker Desktop 执行命令。

| 属性 | 值 |
|---|---|
| 默认值 | `false` |
| 可接受值 | `true`, `false` |
| 格式 | Boolean |
| Docker Desktop GUI | **常规** 选项卡 |
| JSON 键 | `desktopTerminalEnabled` |
| Docker Home | 不可用 |

### 在 TCP 2375 上公开 Docker API \[仅限 Windows\]


通过端口 2375 上未经身份验证的 TCP 套接字公开 Docker API。仅建议在隔离且受保护的环境中使用。支持需要 TCP API 访问的遗留集成。

| 属性 | 值 |
|---|---|
| 默认值 | `false` |
| 可接受值 | `true`, `false` |
| 格式 | Boolean |
| JSON 键 | `exposeDockerAPIOnTCP2375` |
| Docker Home | **公开 Docker API** |

> [!NOTE]
>
> 在强化环境中，禁用并锁定此设置。这可确保 Docker API 仅能通过安全的内部套接字访问。

## 扩展

### 启用 Docker 扩展

控制用户是否可以安装和运行 Docker 扩展。

| 属性 | 值 |
|---|---|
| 默认值 | `true` |
| 可接受值 | `true`, `false` |
| 格式 | Boolean |
| JSON 键 | `extensionsEnabled` |
| Docker Home | **允许扩展** |

> [!NOTE]
>
> 在强化环境中，禁用并锁定此设置。这可防止安装第三方或未经验证的插件。

### 仅允许通过 Docker Marketplace 分发的扩展

阻止安装第三方或本地开发的扩展。

| 属性 | 值 |
|---|---|
| 默认值 | `false` |
| 可接受值 | `true`, `false` |
| 格式 | Boolean |
| JSON 键 | `onlyMarketplaceExtensions` |
| Docker Home | **仅限 Marketplace 扩展** |

### 启用私有应用市场

确保 Docker Desktop 连接到由管理员定义和控制的内容，而不是公共 Docker Marketplace。

| 属性 | 值 |
|---|---|
| 默认值 | `false` |
| 可接受值 | `true`, `false` |
| 格式 | Boolean |
| JSON 键 | `extensionsPrivateMarketplace` |
| Docker Home | **扩展私有应用市场** |

## AI

### 启用 Docker Model Runner

启用 Docker Model Runner 功能以在容器中运行 AI 模型。

| 属性 | 值 |
|---|---|
| 默认值 | `true` |
| 可接受值 | `true`, `false` |
| 格式 | Boolean |
| JSON 键 | `enableInference` |
| Docker Home | **启用 Docker Model Runner** |

#### 启用主机端 TCP 支持

为 Docker Model Runner 服务启用 TCP 连接，允许外部应用程序通过 TCP 连接到 Model Runner。

| 属性 | 值 |
|---|---|
| 默认值 | `false` |
| 可接受值 | `true`, `false` |
| 格式 | Boolean |
| JSON 键 | `enableInferenceTCP` |
| Docker Home | **主机端 TCP 支持** |
| 依赖 | 需先启用 Docker Model Runner |

##### 端口

指定 Model Runner TCP 连接使用的端口。

| 属性 | 值 |
|---|---|
| 默认值 | `12434` |
| 可接受值 | Integer |
| 格式 | Integer |
| JSON 键 | `enableInferenceTCPPort` |
| Docker Home | **主机端 TCP 端口** |
| 依赖 | 需先启用 Docker Model Runner 和主机端 TCP 支持 |

##### CORS 允许的来源

控制 Model Runner Web 集成的跨域资源共享。

| 属性 | 值 |
|---|---|
| 默认值 | 空字符串 |
| 可接受值 | 空字符串（拒绝全部）、`*`（接受全部）或逗号分隔的来源列表 |
| 格式 | String |
| JSON 键 | `enableInferenceCORS` |
| Docker Home | **CORS 允许的来源** |
| 依赖 | 需先启用 Docker Model Runner 和主机端 TCP 支持 |

### 启用 GPU 支持的推理 \[仅限 Windows\]


启用 GPU 支持的推理。额外的组件将被下载到 `~/.docker/bin/inference`。

| 属性 | 值 |
|---|---|
| 默认值 | `false` |
| 可接受值 | `true`, `false` |
| 格式 | Boolean |
| JSON 键 | `enableInferenceGPUVariant` |
| Docker Home | **启用 GPU 支持的推理** |

## 文件共享和仿真

### 文件共享目录

定义容器在开发工作流中可以访问的主机目录。

| 属性 | 值 |
|---|---|
| 默认值 | 随操作系统而异 |
| 可接受值 | 文件路径列表 |
| 格式 | 字符串数组 |
| JSON 键 | `filesharingAllowedDirectories` |
| Docker Home | 是 — **允许的文件共享目录** |

### VirtioFS \[仅限 Mac\]


使用 VirtioFS 在主机和容器之间进行快速、原生的文件共享。如果 VirtioFS 和 gRPC FUSE 都设置为 `true`，则 VirtioFS 优先。

| 属性 | 值 |
|---|---|
| 默认值 | `true` |
| 可接受值 | `true`, `false` |
| 格式 | Boolean |
| JSON 键 | `useVirtualizationFrameworkVirtioFS` |
| Docker Home | **使用 VirtioFS 进行文件共享** 选项卡 |

### gRPC FUSE \[仅限 Mac\]


为 macOS 文件共享启用 gRPC FUSE。

| 属性 | 值 |
|---|---|
| 默认值 | `true` |
| 可接受值 | `true`, `false` |
| 格式 | Boolean |
| JSON 键 | `useGrpcfuse` |
| Docker Home | **使用 gRPC FUSE 进行文件共享** |

### Rosetta \[仅限 Mac\]


使用 Rosetta 在 Apple Silicon 上进行 x86_64/amd64 仿真。

| 属性 | 值 |
|---|---|
| 默认值 | `true` |
| 可接受值 | `true`, `false` |
| 格式 | Boolean |
| JSON 键 | `useVirtualizationFrameworkRosetta` |
| Docker Home | **在 Apple Silicon 上使用 Rosetta 进行 x86_64/amd64 仿真** |

## Scout

### 启用 Scout 镜像分析

为容器镜像开启漏洞扫描和软件物料清单（SBOM）分析。

| 属性 | 值 |
|---|---|
| 默认值 | `true` |
| 可接受值 | `true`, `false` |
| 格式 | Boolean |
| JSON 键 | `sbomIndexing` |
| Docker Home | **SBOM 索引** |

### 启用后台 Scout SBOM 索引

通过在空闲时间或镜像操作后索引来保持镜像元数据的最新状态。

| 属性 | 值 |
|---|---|
| 默认值 | `false` |
| 可接受值 | `true`, `false` |
| 格式 | Boolean |
| JSON 键 | `useBackgroundIndexing` |
| Docker Home | **后台索引** |

## 代理

> [!NOTE]
>
> 代理配置是一个特例，因为它必须在两个地方进行配置：
>
> 1. 在您组织的 Docker Home 中。
> 2. 在安装了 Docker Desktop 的用户系统上。
>
> 在用户机器上，通过 `admin-settings.json` 文件或在 Docker Desktop 安装期间使用安装程序标志来配置代理。有关详细说明，请参阅[安装指南](/manuals/desktop/setup/install/windows-install.md#proxy-configuration)。
>
> 需要进行此额外配置，是因为 Docker Desktop 必须先知道使用哪个代理服务器，才能完成用户登录并从 Docker Home 获取组织设置。

### 嵌入式 PAC 脚本

指定嵌入式代理自动配置（PAC）脚本。例如：`"embeddedPac": "function FindProxyForURL(url, host) { return \"DIRECT\"; }"`。

| 属性 | 值 |
|---|---|
| 默认值 | `""` |
| 可接受值 | 嵌入式 PAC 脚本内容 |
| 格式 | String |
| JSON 键 | `embeddedPac` |
| Docker Home | 是 **嵌入式 PAC 脚本** |

### PAC 文件 URL

指定 Docker Desktop 在路由网络流量时使用的 PAC 文件 URL。例如：`"pac": "http://proxy/proxy.pac"`。

| 属性 | 值 |
|---|---|
| 默认值 | `""` |
| 可接受值 | PAC 文件 URL |
| 格式 | String |
| JSON 键 | `pac` |
| Docker Home | **PAC 文件** |

### 覆盖 Windows “dockerd” 端口 \[仅限 Windows\]


在本地此端口上公开 Docker Desktop 的内部代理，以供 Windows Docker 守护进程连接。如果设置为 0，则选择一个随机的空闲端口。如果值大于 0，则使用该确切值作为端口。

| 属性 | 值 |
|---|---|
| 默认值 | `-1` |
| 可接受值 | `-1` `0` |
| 格式 | String |
| JSON 键 | `windowsDockerdPort` |
| Docker Home | **覆盖 Windows “dockerd” 端口** |

### 启用 Kerberos 和 NTLM 身份验证

为企业代理身份验证启用 Kerberos 和 NTLM 协议支持。

| 属性 | 值 |
|---|---|
| 默认值 | `false` |
| 可接受值 | `true`, `false` |
| 格式 | Boolean |
| JSON 键 | `proxy.enableKerberosNtlm` |
| Docker Home | **Kerberos NTLM** |

### 代理绕过

定义容器在使用代理设置时应绕过的网络地址。

| 属性 | 值 |
|---|---|
| 默认值 | `""` |
| 可接受值 | 地址列表 |
| 格式 | String |
| Docker Desktop GUI | **代理** 选项卡 |
| JSON 键 | `proxy`（使用 `manual` 和 `exclude` 模式） |
| Docker Home | 是 — **代理** 部分 |

## 容器代理

### 隔离环境容器代理

配置一个 HTTP/HTTPS 代理，管理两条不同的流量路径：

- 守护进程镜像拉取（始终强制执行）：Docker Desktop 在 VM 启动时始终在 `daemon.json` 中将 `http.docker.internal:3128` 作为守护进程的代理注入。所有 `docker pull` 和 Compose 拉取操作都经过 `containersProxy` 路由，包括任何 PAC 文件规则。无论是否配置了 `transparentPorts`，这都适用。
- 运行中容器的出站流量（可选加入）：只有当配置了 `transparentPorts` 时，容器的 TCP 流量才受 `containersProxy` 规则约束。如果不配置，运行中的容器直接连接，PAC 文件规则不适用于其出站流量。

> [!IMPORTANT]
>
> 如果在 `containersProxy` 下配置了 PAC 文件，该 PAC 文件必须返回适当的代理服务器，以连接到托管镜像的注册表。

[`proxy`](#代理) 设置管理 Docker Desktop 主机级流量：Desktop 应用程序、Docker CLI 和扩展。它仅在未显式配置 `containersProxy` 时作为守护进程的回退。一旦设置了 `containersProxy`，`proxy` 就不再参与守护进程或容器流量。

| 属性 | 值 |
|---|---|
| 默认值 | 见下方示例 |
| 可接受值 | JSON 对象 |
| 格式 | JSON 对象 |
| JSON 键 | `containersProxy` |
| Docker Home | **容器代理** 部分 |

```json
"containersProxy": {
  "locked": true,
  "mode": "manual",
  "http": "",
  "https": "",
  "exclude": [],
  "pac": "",
  "transparentPorts": ""
}
```

有关更多信息，请参阅[隔离环境容器](/manuals/enterprise/security/hardened-desktop/air-gapped-containers.md)。

## LinuxVM

### 启用 WSL 引擎 \[仅限 Windows\]


设置为 `true` 时，Docker Desktop 使用基于 WSL 2 的引擎。覆盖安装时使用 `--backend=<backend name>` 设置的任何后端标志。

| 属性 | 值 |
|---|---|
| 默认值 | `true` |
| 可接受值 | `true`, `false` |
| 格式 | Boolean |
| JSON 键 | `wslEngineEnabled` |
| Docker Home | **Windows Subsystem for Linux (WSL) 引擎** |

### Docker 守护进程选项

覆盖容器中使用的 Docker 守护进程配置，而不修改本地配置文件。

| 属性 | 值 |
|---|---|
| 默认值 | `{}` |
| 可接受值 | JSON 对象 |
| 格式 | 字符串化 JSON |
| JSON 键 | `linuxVM.dockerDaemonOptions` |
| Docker Home | LinuxVM 下拉菜单中的 **Docker 守护进程选项** |

### VPNKit CIDR \[仅限 Mac\]


设置 Docker Desktop 内部 VPNKit DHCP/DNS 服务使用的网络子网。防止在具有重叠网络子网的环境中出现 IP 地址冲突。

| 属性 | 值 |
|---|---|
| 默认值 | `192.168.65.0/24` |
| 可接受值 | CIDR 表示法 |
| 格式 | String |
| JSON 键 | `vpnkitCIDR` |
| Docker Home | **VPNKit CIDR** |

## Windows 容器

### Docker 守护进程选项

覆盖 Windows 容器中使用的 Docker 守护进程配置，而不修改本地配置文件。

| 属性 | 值 |
|---|---|
| 默认值 | `{}` |
| 可接受值 | JSON 对象 |
| 格式 | 字符串化 JSON |
| JSON 键 | windowsContainers.dockerDaemonOptions |
| Docker Home | **Windows 容器下拉菜单** 中的 **Docker 守护进程选项** |

## Kubernetes

### 启用 Kubernetes

启用与 Docker Desktop 的本地 Kubernetes 集群集成。

| 属性 | 值 |
|---|---|
| 默认值 | `false` |
| 可接受值 | `true`, `false` |
| 格式 | Boolean |
| JSON 键 | `kubernetes` |
| Docker Home | **启用 Kubernetes** |

### 显示系统容器

控制 Kubernetes 系统容器在 Docker Desktop Dashboard 中的可见性。

| 属性 | 值 |
|---|---|
| 默认值 | `false` |
| 可接受值 | `true`, `false` |
| 格式 | Boolean |
| Docker Home | **显示系统容器** |

### Kubernetes 镜像仓库

指定用于 Kubernetes 控制平面镜像的注册表，以替代 Docker Hub。覆盖镜像名称的 `[registry[:port]/][namespace]` 部分。镜像必须从 Docker Hub 镜像，并带有匹配的标签。

| 属性 | 值 |
|---|---|
| 默认值 | `""` |
| 可接受值 | 注册表 URL |
| 格式 | String |
| JSON 键 | `KubernetesImagesRepository` |
| Docker Home | **Kubernetes 镜像仓库** |

> [!NOTE]
>
> 镜像必须从 Docker Hub 镜像，并带有匹配的标签。所需的镜像取决于集群置备方法。

> [!IMPORTANT]
>
> 将自定义镜像仓库与增强容器隔离一起使用时，请将以下镜像添加到 ECI 允许列表中：`[imagesRepository]/desktop-cloud-provider-kind:*` 和 `[imagesRepository]/desktop-containerd-registry-mirror:*`。

### 集群置备方法

控制 Kubernetes 集群拓扑和节点配置。

| 属性 | 值 |
|---|---|
| 默认值 | `kubeadm` |
| 可接受值 | `kubeadm`, `kind` |
| 格式 | String |
| Docker Home | **Kubernetes 模式** |

### 节点版本

固定集群节点使用的 Kubernetes 版本。

| 属性 | 值 |
|---|---|
| 默认值 | `1.31.1` |
| 可接受值 | 语义化版本（例如 `1.29.1`） |
| 格式 | String |
| Docker Home | **节点版本** 选项卡 |

### 节点数量

设置多节点 Kubernetes 集群中的节点数量。

| 属性 | 值 |
|---|---|
| 默认值 | `1` |
| 可接受值 | Integer |
| 格式 | Integer |
| Docker Home | **节点数量** |

## 开发中功能

### 访问 Beta 功能

控制用户是否可以访问所有处于公开 Beta 阶段的 Docker Desktop 功能。

| 属性 | 值 |
|---|---|
| 默认值 | `false` |
| 可接受值 | `true`, `false` |
| 格式 | Boolean |
| JSON 键 | `allowBetaFeatures` |
| Docker Home | **访问 Beta 功能** |

### 启用 Docker MCP Toolkit（Beta）

在 Docker Desktop 中启用 [Docker MCP Toolkit](/manuals/ai/mcp-catalog-and-toolkit/_index.md)，用于 AI 模型开发工作流。

| 属性 | 值 |
|---|---|
| 默认值 | `true` |
| 可接受值 | `true`, `false` |
| 格式 | Boolean |
| JSON 键 | `enableDockerMCPToolkit` |
| Docker Home | 不可用 |

## 增强容器隔离

### 启用增强容器隔离

防止容器修改 Docker Desktop VM 配置或访问敏感的主机区域。

| 属性 | 值 |
|---|---|
| 默认值 | `false` |
| 可接受值 | `true`, `false` |
| 格式 | Boolean |
| JSON 键 | `enhancedContainerIsolation` |
| Docker Home | **启用增强容器隔离** |

### Docker 套接字访问控制（ECI 例外）

定义当增强容器隔离处于活动状态时，允许使用 Docker 套接字的特定镜像和命令。支持 Testcontainers、LocalStack 或需要在保持安全性的同时访问 Docker 套接字的 CI 系统。

| 属性 | 值 |
|---|---|
| 可接受值 | JSON 对象 |
| 格式 | JSON 对象 |
| JSON 键 | `dockerSocketMount` |
| Docker Home | **镜像列表**、**命令列表** |

```json
"enhancedContainerIsolation": {
  ...
}
```

## 网络

### 网络模式

设置 Docker 创建新网络时使用的默认 IP 协议。

| 属性 | 值 |
|---|---|
| 默认值 | `dual-stack` |
| 可接受值 | `ipv4only`, `ipv6only` |
| 格式 | String |
| JSON 键 | `defaultNetworkingMode` |
| Docker Home | **默认网络 IP 模式** |

有关更多信息，请参阅[网络](/manuals/desktop/features/networking.md#networking-mode-and-dns-behaviour-for-mac-and-windows)。

### 抑制 IPv4/IPv6 的 DNS 解析

过滤不支持的 DNS 记录类型，以在仅支持 IPv4 或 IPv6 的环境中提高可靠性。需要 Docker Desktop 4.43 及更高版本。

| 属性 | 值 |
|---|---|
| 默认值 | `auto` |
| 可接受值 | `ipv4`, `ipv6`, `none` |
| 格式 | String |
| JSON 键 | `dnsInhibition` |
| Docker Home | **DNS 过滤行为** |

有关更多信息，请参阅[网络](/manuals/desktop/features/networking.md#networking-mode-and-dns-behaviour-for-mac-and-windows)。

### 端口绑定行为

指定如何处理新容器的端口绑定。

| 属性 | 值 |
|---|---|
| 默认值 | `default-port-binding` |
| 可接受值 | `default-local-port-binding`, `local-only-port-binding`, `default-port-binding` |
| 格式 | String |
| JSON 键 | `portBindingBehavior` |
| Docker Home | **端口绑定行为** |

## 其他

### 启用 Docker Offload

控制 Docker Offload 的可用性。启用后，用户会在 Docker Desktop 标题栏中看到 Docker Offload 开关。

| 属性 | 值 |
|---|---|
| 默认值 | `false` |
| 可接受值 | `true`, `false` |
| 格式 | Boolean |
| JSON 键 | `enableCloud` |
| Docker Home | **启用 Docker Offload** |

> [!NOTE]
>
> 此设置仅在对组织启用 Docker Offload 功能时可用。

