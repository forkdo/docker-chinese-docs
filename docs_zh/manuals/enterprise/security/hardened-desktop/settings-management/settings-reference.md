---
title: 设置参考
linkTitle: 设置参考
description: 所有 Docker Desktop 设置和配置选项的完整参考
keywords: docker desktop settings, configuration reference, admin controls, settings management
aliases:
- /security/for-admins/hardened-desktop/settings-management/settings-reference/
---

本参考文档记录了所有 Docker Desktop 设置和配置选项。使用此文档可以了解不同配置方法和平台上的设置行为。其组织结构与 Docker Desktop GUI 相匹配。

每个设置都包括：

- 默认值和可接受值
- 平台兼容性
- 配置方法（Docker Desktop GUI、Admin Console、`admin-settings.json` 文件或 CLI）
- 适用时的企业安全建议

## 常规设置

### 登录计算机时启动 Docker Desktop

| 默认值 | 可接受值 | 格式 |
|---------------|-----------------|--------|
| `false`       | `true`, `false` | Boolean |

- **描述：** 用户登录计算机时自动启动 Docker Desktop。
- **操作系统：** {{< badge color=blue text="All" >}}
- **使用场景：** 确保 Docker Desktop 在系统启动后始终可用。
- **配置此项设置的方式：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的 **常规** 设置

### Docker Desktop 启动时打开 Docker Dashboard

| 默认值 | 可接受值            | 格式 |
|---------------|----------------------------|--------|
| `false`      | `true`, `false`  | Boolean   |

- **描述：** Docker Desktop 启动时是否自动打开 Docker Dashboard。
- **操作系统：** {{< badge color=blue text="All" >}}
- **使用场景：** 启动后立即访问容器、镜像和数据卷。
- **配置此项设置的方式：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的 **常规** 设置

### 选择 Docker Desktop 的主题

| 默认值 | 可接受值            | 格式 |
|---------------|----------------------------|--------|
| `system`      | `light`, `dark`, `system`  | Enum   |

- **描述：** Docker Desktop 界面的视觉外观。
- **操作系统：** {{< badge color=blue text="All" >}}
- **使用场景：** 自定义界面外观以匹配用户偏好或系统主题。
- **配置此项设置的方式：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的 **常规** 设置

### 配置 Shell 自动补全

| 默认值 | 可接受值         | 格式 |
|---------------|-------------------------|--------|
| `integrated`  | `integrated`, `system`  | String |

- **描述：** Docker CLI 自动补全如何与用户的 Shell 集成。
- **操作系统：** {{< badge color=blue text="All" >}}
- **使用场景：** 控制 Docker 是否修改 Shell 配置文件以实现自动补全。
- **配置此项设置的方式：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的 **常规** 设置

### 选择容器终端

| 默认值 | 可接受值         | 格式 |
|---------------|-------------------------|--------|
| `integrated`  | `integrated`, `system`  | String |

- **描述：** 从 Docker Desktop 启动 Docker CLI 时使用的默认终端。
- **操作系统：** {{< badge color=blue text="All" >}}
- **使用场景：** 为 Docker CLI 交互设置首选终端应用程序。
- **配置此项设置的方式：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的 **常规** 设置

### 启用 Docker 终端

| 默认值 | 可接受值 | 格式 |
|---------------|-----------------|--------|
| `false`       | `true`, `false` | Boolean |

- **描述：** 访问 Docker Desktop 的集成终端功能。如果
该值设置为 `false`，则用户无法使用 Docker 终端与
主机交互并直接从 Docker Desktop 执行命令。
- **操作系统：** {{< badge color=blue text="All" >}}
- **使用场景：** 允许或限制开发人员访问内置终端以与主机系统交互。
- **配置此项设置的方式：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的 **常规** 设置
    - Settings Management: [`admin-settings.json` 文件](/manuals/enterprise/security/hardened-desktop/settings-management/configure-json-file.md)中的 `desktopTerminalEnabled` 设置

> [!NOTE]
>
> 在强化环境中，禁用并锁定此设置以限制主机访问。

### 默认启用 Docker 调试

| 默认值 | 可接受值 | 格式   |
|---------------|-----------------|----------|
| `false`       | `true`, `false` | Boolean  |

- **描述：** 是否默认为 Docker CLI 命令启用调试日志记录。
- **操作系统：** {{< badge color=blue text="All" >}}
- **使用场景：** 为故障排除和支持场景提供详细输出。
- **配置此项设置的方式：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的 **常规** 设置

### 将虚拟机包含在 Time Machine 备份中

| 默认值 | 可接受值 | 格式 |
|---------------|-----------------|--------|
| `false`       | `true`, `false` | Boolean |

- **描述：** Docker Desktop 虚拟机是否包含在 macOS Time Machine 备份中。
- **操作系统：** {{< badge color=blue text="Mac only" >}}
- **使用场景：** 平衡备份完整性与备份大小和性能。
- **配置此项设置的方式：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的 **常规** 设置

### 使用 containerd 拉取和存储镜像

| 默认值 | 可接受值 | 格式   |
|---------------|-----------------|----------|
| `false`       | `true`, `false` | Boolean  |

- **描述：** Docker Desktop 使用的镜像存储后端。
- **操作系统：** {{< badge color=blue text="All" >}}
- **使用场景：** 提升镜像处理性能并启用 containerd 原生功能。
- **配置此项设置的方式：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的 **常规** 设置

### 选择虚拟机管理器

#### Docker VMM

| 默认值 | 可接受值 | 格式   |
|---------------|-----------------|----------|
| `true`        | `true`, `false` | Boolean  |

#### Apple Virtualization framework

| 默认值 | 可接受值 | 格式   |
|---------------|-----------------|----------|
| `true`        | `true`, `false` | Boolean  |

- **描述：** 使用 Apple Virtualization Framework 运行 Docker 容器。
- **操作系统：** {{< badge color=blue text="Mac only" >}}
- **使用场景：** 在 Apple Silicon 上提升虚拟机性能。
- **配置此项设置的方式：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的 **常规** 设置

#### Rosetta

| 默认值 | 可接受值 | 格式   |
|---------------|-----------------|----------|
| `true`        | `true`, `false` | Boolean  |

- **描述：** 使用 Rosetta 在 Apple Silicon 上模拟 `amd64`。如果值
设置为 `true`，Docker Desktop 会启用 Rosetta 以加速
在 Apple Silicon 上对 x86_64/amd64 二进制文件的模拟。
- **操作系统：** {{< badge color=blue text="Mac only" >}} 13+
- **使用场景：** 在 Apple Silicon 主机上运行基于 Intel 的容器。
- **配置此项设置的方式：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的 **常规** 设置
    - Settings Management: [`admin-settings.json` 文件](/manuals/enterprise/security/hardened-desktop/settings-management/configure-json-file.md)中的 `useVirtualizationFrameworkRosetta` 设置
    - Settings Management: [Admin Console](/manuals/enterprise/security/hardened-desktop/settings-management/configure-admin-console.md) 中的 **Use Rosetta for x86_64/amd64 emulation on Apple Silicon** 设置

> [!NOTE]
>
> 在强化环境中，禁用并锁定此设置，以便仅允许 ARM 原生镜像。

> [!NOTE]
>
> Rosetta 需要启用 Apple Virtualization framework。

#### QEMU

> [!WARNING]
>
> Docker Desktop 4.44 及更高版本中已弃用 QEMU。更多信息，请参阅 [博客公告](https://www.docker.com/blog/docker-desktop-for-mac-qemu-virtualization-option-to-be-deprecated-in-90-days/)

| 默认值 | 可接受值 | 格式   |
|---------------|-----------------|----------|
| `true`        | `true`, `false` | Boolean  |

### 选择文件共享实现

#### VirtioFS

| 默认值 | 可接受值 | 格式   |
|---------------|-----------------|----------|
| `true`        | `true`, `false` | Boolean  |

- **描述：** 使用 VirtioFS 在主机和容器之间进行快速、原生的文件共享。如果值设置为 `true`，VirtioFS 将被设置为文件共享机制。如果 VirtioFS 和 gRPC 都设置为 `true`，则 VirtioFS 优先。
- **操作系统：** {{< badge color=blue text="Mac only" >}} 12.5+
- **使用场景：** 在现代 macOS 上获得更好的文件系统性能和兼容性。
- **配置此项设置的方式：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的 **常规设置**
    - Settings Management: [`admin-settings.json` 文件](/manuals/enterprise/security/hardened-desktop/settings-management/configure-json-file.md)中的 `useVirtualizationFrameworkVirtioFS` 设置
    - Settings Management: [Admin Console](/manuals/enterprise/security/hardened-desktop/settings-management/configure-admin-console.md) 中的 **Use VirtioFS for file sharing** 设置

> [!NOTE]
>
> 在强化环境中，对于 macOS 12.5 及更高版本，启用并锁定此设置。

#### gRPC FUSE

| 默认值 | 可接受值 | 格式   |
|---------------|-----------------|----------|
| `true`        | `true`, `false` | Boolean  |

- **描述：** 启用 gRPC FUSE 进行 macOS 文件共享。如果值设置为
`true`，gRPC Fuse 将被设置为文件共享机制。
- **操作系统：** {{< badge color=blue text="Mac only" >}}
- **使用场景：** 提供比传统 osxfs 性能更优的替代文件共享方案。
- **配置此项设置的方式：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的 **常规** 设置
    - Settings Management: [`admin-settings.json` 文件](/manuals/enterprise/security/hardened-desktop/settings-management/configure-json-file.md)中的 `useGrpcfuse` 设置
    - Settings Management: [Admin Console](/manuals/enterprise/security/hardened-desktop/settings-management/configure-admin-console.md) 中的 **Use gRPC FUSE for file sharing** 设置

> [!NOTE]
>
> 在强化环境中，禁用并锁定此设置。

#### osxfs

| 默认值 | 可接受值 | 格式  |
| ------------- | --------------- | ------- |
| `false`       | `true`, `false` | Boolean |

- **描述：** 使用原始的 osxfs 文件共享驱动程序用于 macOS。当
设置为 `true` 时，Docker Desktop 使用 osxfs 而不是 VirtioFS 或 gRPC FUSE 来将主机目录挂载到容器中。
- **操作系统：** {{< badge color=blue text="Mac only" >}}
- **使用场景：** 与需要原始文件共享实现的旧版工具兼容。
- **配置此项设置的方式：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的 **常规** 设置

### 发送使用统计

| 默认值 | 可接受值 | 格式 |
|---------------|-----------------|--------|
| `true`        | `true`, `false` | Boolean |

- **描述：** 控制 Docker Desktop 是否收集并向 Docker 发送本地
使用统计信息和崩溃报告。此设置影响从 Docker Desktop 应用程序本身收集的遥测数据。它不影响通过 Docker Hub 或其他后端服务（如登录时间戳、拉取或构建）收集的服务器端遥测数据。
- **操作系统：** {{< badge color=blue text="All" >}}
- **使用场景：** 帮助 Docker 根据使用模式改进产品。
- **配置此项设置的方式：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的 **常规** 设置
    - Settings Management: [`admin-settings.json` 文件](/manuals/enterprise/security/hardened-desktop/settings-management/configure-json-file.md)中的 `analyticsEnabled` 设置
    - Settings Management: [Admin Console](/manuals/enterprise/security/hardened-desktop/settings-management/configure-admin-console.md) 中的 **Send usage statistics** 设置

> [!NOTE]
>
> 在强化环境中，禁用并锁定此设置。这允许你控制所有数据流，并在需要时通过安全渠道收集支持日志。

> [!NOTE]
>
> 使用 Insights Dashboard 的组织可能需要启用此设置，以确保开发人员活动完全可见。如果用户选择退出且该设置未被锁定，他们的活动可能会从分析视图中被排除。

### 使用增强型容器隔离

| 默认值 | 可接受值 | 格式   |
|---------------|-----------------|----------|
| `false`       | `true`, `false` | Boolean  |

- **描述：** 通过 Linux 用户命名空间和额外的隔离措施实现高级容器安全。
- **操作系统：** {{< badge color=blue text="All" >}}
- **使用场景：** 防止容器修改 Docker Desktop 虚拟机配置或访问敏感的主机区域。
- **配置此项设置的方式：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的 **常规设置**
    - Settings Management: [`admin-settings.json` 文件](/manuals/enterprise/security/hardened-desktop/settings-management/configure-json-file.md)中的 `enhancedContainerIsolation` 设置
    - Settings Management: [Admin Console](/manuals/enterprise/security/hardened-desktop/settings-management/configure-admin-console.md) 中的 **Enable enhanced container isolation** 设置

> [!NOTE]
>
> 在强化环境中，禁用并锁定此设置。这允许你控制所有数据流，并在需要时通过安全渠道收集支持日志。

### 显示 CLI 提示

| 默认值 | 可接受值 | 格式   |
|---------------|-----------------|----------|
| `true`       | `true`, `false` | Boolean  |

- **描述：** 使用 Docker 命令时在终端中显示有用的 CLI 建议。
- **操作系统：** {{< badge color=blue text="All" >}}
- **使用场景：** 通过上下文提示帮助用户发现 Docker CLI 功能。
- **配置此项设置的方式：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的 **常规** 设置

### 启用 Scout 镜像分析

| 默认值 | 可接受值 | 格式   |
|---------------|-----------------|----------|
| `true`        | `true`, `false` | Boolean  |

- **描述：** 对容器镜像进行 Docker Scout SBOM（软件物料清单）生成和漏洞扫描。
- **操作系统：** {{< badge color=blue text="All" >}}
- **使用场景：** 启用漏洞扫描和软件物料清单分析。
- **配置此项设置的方式：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的 **常规设置**
    - Settings Management: [`admin-settings.json` 文件](/manuals/enterprise/security/hardened-desktop/settings-management/configure-json-file.md)中的 `sbomIndexing` 设置
    - Settings Management: [Admin Console](/manuals/enterprise/security/hardened-desktop/settings-management/configure-admin-console.md) 中的 **SBOM indexing** 设置

> [!NOTE]
>
> 在强化环境中，启用并锁定此设置以确保合规性扫描始终可用。

### 启用后台 Scout SBOM 索引

| 默认值 | 可接受值 | 格式   |
|---------------|-----------------|----------|
| `false`        | `true`, `false` | Boolean  |

- **描述：** 无需用户交互即可为镜像自动进行 SBOM 索引。
- **操作系统：** {{< badge color=blue text="All" >}}
- **使用场景：** 通过在空闲时间或镜像操作后进行索引，保持镜像元数据最新。
- **配置此项设置的方式：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的 **常规设置**

> [!NOTE]
>
> 在强化环境中，启用并锁定此设置以进行持续的安全分析。

### 自动检查配置

| 默认值         | 可接受值 | 格式  |
|-----------------------|-----------------|---------|
| `CurrentSettingsVersions` | Integer         | Integer |

- **描述：** 定期验证 Docker Desktop 配置是否未被外部应用程序修改。
- **操作系统：** {{< badge color=blue text="All" >}}
- **使用场景：** 跟踪配置版本以进行兼容性和变更检测。
- **配置此项设置的方式：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的 **常规** 设置
    - Settings Management: [`admin-settings.json` 文件](/manuals/enterprise/security/hardened-desktop/settings-management/configure-json-file.md)中的 `configurationFileVersion` 设置

## 资源设置

### CPU 限制

| 默认值                                 | 可接受值 | 格式  |
|-----------------------------------------------|-----------------|---------|
| 主机上可用的逻辑 CPU 核心数 | Integer         | Integer |

- **描述：** 分配给 Docker Desktop 虚拟机的 CPU 核心数。
- **操作系统：** {{< badge color=blue text="All" >}}
- **使用场景：** 平衡 Docker 性能与主机系统资源可用性。
- **配置此项设置的方式：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的 **高级** 资源设置

### 内存限制

| 默认值              | 可接受值 | 格式  |
|---------------------------|-----------------|---------|
| 基于系统资源 | Integer         | Integer |

- **描述：** 分配给 Docker Desktop 虚拟机的 RAM 量（以 MiB 为单位）。
- **操作系统：** {{< badge color=blue text="All" >}}
- **使用场景：** 控制内存分配以优化 Docker 和主机应用程序的性能。
- **配置此项设置的方式：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的 **高级** 资源设置

### 交换空间

| 默认值 | 可接受值 | 格式  |
|---------------|-----------------|---------|
| `1024`        | Integer         | Integer |

- **描述：** Docker 虚拟机可用的交换空间量（以 MiB 为单位）。
- **操作系统：** {{< badge color=blue text="All" >}}
- **使用场景：** 在物理 RAM 有限时扩展容器工作负载的可用内存。
- **配置此项设置的方式：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的 **高级** 资源设置

### 磁盘使用限制

| 默认值                  | 可接受值 | 格式  |
|-------------------------------|-----------------|---------|
| 虚拟机的默认磁盘大小。 | Integer         | Integer |

- **描述：** 为 Docker Desktop 数据分配的最大磁盘空间（以 MiB 为单位）。
- **操作系统：** {{< badge color=blue text="All" >}}
- **使用场景：** 防止 Docker 在主机系统上消耗过多的磁盘空间。
- **配置此项设置的方式：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的 **高级** 资源设置

### 磁盘镜像位置

| 默认值                                                                 | 可接受值 | 格式 |
|--------------------------------------------------|-----------------|--------|
| macOS: `~/Library/Containers/com.docker.docker/Data/vms/0`  <br> Windows: `%USERPROFILE%\AppData\Local\Docker\wsl\data` | 文件路径       | String |

- **描述：** Docker Desktop 存储虚拟机数据的文件系统路径。
- **操作系统：** {{< badge color=blue text="All" >}}
- **使用场景：** 将 Docker 数据移动到自定义存储位置以进行性能或空间管理。
- **配置此项设置的方式：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的 **高级** 资源设置

### 启用资源节省器

| 默认值 | 可接受值 | 格式   |
|---------------|-----------------|----------|
| `true`        | `true`, `false` | Boolean  |

- **描述：** 空闲时自动暂停 Docker Desktop 以节省系统资源。
- **操作系统：** {{< badge color=blue text="All" >}}
- **使用场景：** 在 Docker Desktop 未被主动使用时减少 CPU 和内存使用。
- **配置此项设置的方式：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的 **高级** 资源设置

### 文件共享目录

| 默认值                           | 可接受值                 | 格式                  |
|----------------------------------------|---------------------------------|--------------------------|
| 因操作系统而异                           | 作为字符串的文件路径列表   | 字符串数组列表   |

- **描述：** 可以作为卷挂载到容器中的主机目录。
- **操作系统：** {{< badge color=blue text="All" >}}
- **使用场景：** 定义容器可以访问哪些主机目录以用于开发工作流。
- **配置此项设置的方式：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的 **文件共享** 资源设置
    - Settings Management: [`admin-settings.json` 文件](/manuals/enterprise/security/hardened-desktop/settings-management/configure-json-file.md)中的 `filesharingAllowedDirectories` 设置
    - Settings Management: [Admin Console](/manuals/enterprise/security/hardened-desktop/settings-management/configure-admin-console.md) 中的 **Allowed file sharing directories** 设置

> [!NOTE]
>
> 在强化环境中，锁定为明确的允许列表，并禁用最终用户编辑。

### 代理排除

| 默认值 | 可接受值    | 格式 |
|---------------|--------------------|--------|
| `""`          | 地址列表  | String |

- **描述：** 容器在使用代理设置时应绕过的网络地址。
- **操作系统：** {{< badge color=blue text="All" >}}
- **使用场景：** 为内部服务或特定域定义代理例外。
- **配置此项设置的方式：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的 **代理** 资源设置
    - Settings Management: [`admin-settings.json` 文件](/manuals/enterprise/security/hardened-desktop/settings-management/configure-json-file.md)中带有 `manual` 和 `exclude` 模式的 `proxy` 设置
    - Settings Management: [Admin Console](/manuals/enterprise/security/hardened-desktop/settings-management/configure-admin-console.md) 中的 **代理** 部分

> [!NOTE]
>
> 在强化环境中，禁用并锁定此设置以维持严格的代理控制。

### Docker 子网

| 默认值     | 可接受值 | 格式 |
|-------------------|-----------------|--------|
| `192.168.65.0/24` | IP 地址      | String |

- **描述：** 覆盖用于 vpnkit DHCP/DNS 的网络范围以
支持 `*.docker.internal`。
- **操作系统：** {{< badge color=blue text="Mac only" >}}
- **使用场景：** 自定义用于 Docker 容器网络的子网。
- **配置此项设置的方式：**
    - Settings Management: [`admin-settings.json` 文件](/manuals/enterprise/security/hardened-desktop/settings-management/configure-json-file.md)中的 `vpnkitCIDR` 设置
    - Settings Management: [Admin Console](/manuals/enterprise/security/hardened-desktop/settings-management/configure-admin-console.md) 中的 **VPN Kit CIDR** 设置

### 对 UDP 使用内核网络

| 默认值 | 可接受值 | 格式   |
|---------------|-----------------|----------|
| `false`       | `true`, `false` | Boolean  |

- **描述：** 使用主机的内核网络堆栈处理 UDP 流量，而不是 Docker 的虚拟网络驱动程序。这可以实现更快、更直接的 UDP 通信，但可能会绕过某些容器隔离功能。
- **操作系统：** {{< badge color=blue text="All" >}}
- **使用场景：** 为 UDP 密集型应用（如实时媒体、DNS 或游戏）提升性能。
- **配置此项设置的方式：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的 **网络** 资源设置

### 启用主机网络

| 默认值 | 可接受值 | 格式   |
|---------------|-----------------|----------|
| `false`       | `true`, `false` | Boolean  |

- **描述：** 支持容器直接使用主机网络堆栈的实验性功能。
- **操作系统：** {{< badge color=blue text="All" >}}
- **使用场景：** 允许容器在特定场景下绕过 Docker 的网络隔离。
- **配置此项设置的方式：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的 **网络** 资源设置

### 网络模式

| 默认值 | 可接受值 | 格式   |
|---------------|-----------------|----------|
| `dual-stack` | `ipv4only`, `ipv6only` | String  |

- **描述：** Docker 创建新网络时使用的默认 IP 协议。
- **操作系统：** {{< badge color=blue text="Windows and Mac" >}}
- **使用场景：** 与仅支持 IPv4 或 IPv6 的网络基础设施对齐。
- **配置此项设置的方式：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的 **网络** 资源设置
    - Settings Management: [`admin-settings.json` 文件](/manuals/enterprise/security/hardened-desktop/settings-management/configure-json-file.md)中的 `defaultNetworkingMode` 设置
    - Settings Management: [Admin Console](/manuals/enterprise/security/hardened-desktop/settings-management/configure-admin-console.md) 中的 **Default network IP mode**

更多信息，请参阅 [网络](/manuals/desktop/features/networking.md#networking-mode-and-dns-behaviour-for-mac-and-windows)。

#### 抑制 IPv4/IPv6 的 DNS 解析

| 默认值 | 可接受值 | 格式   |
|---------------|-----------------|----------|
| `auto` | `ipv4`, `ipv6`, `none` | String  |

- **描述：** 过滤不支持的 DNS 记录类型。需要 Docker Desktop
4.43 及更高版本。
- **操作系统：** {{< badge color=blue text="Windows and Mac" >}}
- **使用场景：** 控制 Docker 过滤返回给容器的 DNS 记录，在仅支持 IPv4 或 IPv6 的环境中提高可靠性。
- **配置此项设置的方式：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的 **网络** 资源设置
    - Settings Management: [`admin-settings.json` 文件](/manuals/enterprise/security/hardened-desktop/settings-management/configure-json-file.md)中的 `dnsInhibition` 设置
    - Settings Management: [Admin Console](/manuals/enterprise/security/hardened-desktop/settings-management/configure-admin-console.md) 中的 **DNS filtering behavior**

更多信息，请参阅 [网络](/manuals/desktop/features/networking.md#networking-mode-and-dns-behaviour-for-mac-and-windows)。

### 启用 WSL 引擎

| 默认值 | 可接受值 | 格式   |
|---------------|-----------------|----------|
| `true`        | `true`, `false` | Boolean  |

- **描述：** 如果值设置为 `