---
title: 设置参考
linkTitle: 设置参考
description: Docker Desktop 所有设置和配置选项的完整参考
keywords: docker desktop settings, configuration reference, admin controls, settings management
aliases:
 - /security/for-admins/hardened-desktop/settings-management/settings-reference/
---

本文档记录了 Docker Desktop 的所有设置和配置选项。使用本文档可了解不同配置方法和平台上的设置行为。其组织结构与 Docker Desktop GUI 结构相匹配。

每个设置都包含：

- 默认值和接受值
- 平台兼容性
- 配置方法（Docker Desktop GUI、Admin Console、`admin-settings.json` 文件或 CLI）
- 适用的企业安全建议

## 常规设置

### 登录计算机时启动 Docker Desktop

| 默认值 | 接受值 | 格式 |
|---------------|-----------------|--------|
| `false`       | `true`, `false` | 布尔值 |

- **描述：** 用户登录计算机时自动启动 Docker Desktop。
- **操作系统：** {{< badge color=blue text="全部" >}}
- **用例：** 确保系统启动后 Docker Desktop 始终可用。
- **配置此设置的方法：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的**常规**设置

### Docker Desktop 启动时打开 Docker Dashboard

| 默认值 | 接受值 | 格式 |
|---------------|-----------------|--------|
| `false`      | `true`, `false`  | 布尔值   |

- **描述：** Docker Desktop 启动时是否自动打开 Docker Dashboard。
- **操作系统：** {{< badge color=blue text="全部" >}}
- **用例：** 启动后立即访问容器、镜像和卷。
- **配置此设置的方法：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的**常规**设置

### 为 Docker Desktop 选择主题

| 默认值 | 接受值 | 格式 |
|---------------|-----------------|--------|
| `system`      | `light`, `dark`, `system`  | 枚举值   |

- **描述：** Docker Desktop 界面的视觉外观。
- **操作系统：** {{< badge color=blue text="全部" >}}
- **用例：** 自定义界面外观以匹配用户偏好或系统主题。
- **配置此设置的方法：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的**常规**设置

### 配置 Shell 补全

| 默认值 | 接受值 | 格式 |
|---------------|-----------------|--------|
| `integrated`  | `integrated`, `system`  | 字符串 |

- **描述：** Docker CLI 自动补全如何与用户的 Shell 集成。
- **操作系统：** {{< badge color=blue text="全部" >}}
- **用例：** 控制 Docker 是否修改 Shell 配置文件以实现自动补全。
- **配置此设置的方法：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的**常规**设置

### 选择容器终端

| 默认值 | 接受值 | 格式 |
|---------------|-----------------|--------|
| `integrated`  | `integrated`, `system`  | 字符串 |

- **描述：** 从 Docker Desktop 启动 Docker CLI 时使用的默认终端。
- **操作系统：** {{< badge color=blue text="全部" >}}
- **用例：** 为 Docker CLI 交互设置首选终端应用程序。
- **配置此设置的方法：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的**常规**设置

### 启用 Docker 终端

| 默认值 | 接受值 | 格式 |
|---------------|-----------------|--------|
| `false`       | `true`, `false` | 布尔值 |

- **描述：** 访问 Docker Desktop 的集成终端功能。如果值设置为 `false`，用户将无法使用 Docker 终端与主机交互，也无法直接从 Docker Desktop 执行命令。
- **操作系统：** {{< badge color=blue text="全部" >}}
- **用例：** 允许或限制开发者访问内置终端以进行主机系统交互。
- **配置此设置的方法：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的**常规**设置
    - 设置管理：[`admin-settings.json` 文件](/manuals/enterprise/security/hardened-desktop/settings-management/configure-json-file.md) 中的 `desktopTerminalEnabled` 设置

> [!NOTE]
>
> 在加固环境中，禁用并锁定此设置以限制主机访问。

### 默认启用 Docker 调试

| 默认值 | 接受值 | 格式   |
|---------------|-----------------|----------|
| `false`       | `true`, `false` | 布尔值  |

- **描述：** Docker CLI 命令是否默认开启调试日志记录。
- **操作系统：** {{< badge color=blue text="全部" >}}
- **用例：** 为故障排除和支持场景提供详细输出。
- **配置此设置的方法：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的**常规**设置

### 将虚拟机包含在 Time Machine 备份中

| 默认值 | 接受值 | 格式 |
|---------------|-----------------|--------|
| `false`       | `true`, `false` | 布尔值 |

- **描述：** Docker Desktop 虚拟机是否包含在 macOS Time Machine 备份中。
- **操作系统：** {{< badge color=blue text="仅限 Mac" >}}
- **用例：** 平衡备份完整性与备份大小和性能。
- **配置此设置的方法：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的**常规**设置

### 使用 containerd 拉取和存储镜像

| 默认值 | 接受值 | 格式   |
|---------------|-----------------|----------|
| `false`       | `true`, `false` | 布尔值  |

- **描述：** Docker Desktop 使用的镜像存储后端。
- **操作系统：** {{< badge color=blue text="全部" >}}
- **用例：** 提高镜像处理性能并启用 containerd 原生功能。
- **配置此设置的方法：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的**常规**设置

### 选择虚拟机管理器

#### Docker VMM

| 默认值 | 接受值 | 格式   |
|---------------|-----------------|----------|
| `true`        | `true`, `false` | 布尔值  |

#### Apple 虚拟化框架

| 默认值 | 接受值 | 格式   |
|---------------|-----------------|----------|
| `true`        | `true`, `false` | 布尔值  |

- **描述：** 使用 Apple 虚拟化框架运行 Docker 容器。
- **操作系统：** {{< badge color=blue text="仅限 Mac" >}}
- **用例：** 在 Apple Silicon 上提升虚拟机性能。
- **配置此设置的方法：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的**常规**设置

#### Rosetta

| 默认值 | 接受值 | 格式   |
|---------------|-----------------|----------|
| `true`        | `true`, `false` | 布尔值  |

- **描述：** 使用 Rosetta 在 Apple Silicon 上模拟 `amd64`。如果值设置为 `true`，Docker Desktop 会开启 Rosetta 以加速 Apple Silicon 上的 x86_64/amd64 二进制模拟。
- **操作系统：** {{< badge color=blue text="仅限 Mac" >}} 13+
- **用例：** 在 Apple Silicon 主机上运行基于 Intel 的容器。
- **配置此设置的方法：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的**常规**设置
    - 设置管理：[`admin-settings.json` 文件](/manuals/enterprise/security/hardened-desktop/settings-management/configure-json-file.md) 中的 `useVirtualizationFrameworkRosetta` 设置
    - 设置管理：[Admin Console](/manuals/enterprise/security/hardened-desktop/settings-management/configure-admin-console.md) 中的**在 Apple Silicon 上使用 Rosetta 进行 x86_64/amd64 模拟**设置

> [!NOTE]
>
> 在加固环境中，禁用并锁定此设置，以便只允许运行 ARM 原生镜像。

> [!NOTE]
>
> Rosetta 需要启用 Apple 虚拟化框架。

#### QEMU

> [!WARNING]
>
> QEMU 在 Docker Desktop 4.44 及更高版本中已弃用。更多信息，请参阅[博客公告](https://www.docker.com/blog/docker-desktop-for-mac-qemu-virtualization-option-to-be-deprecated-in-90-days/)。

| 默认值 | 接受值 | 格式   |
|---------------|-----------------|----------|
| `true`        | `true`, `false` | 布尔值  |

### 选择文件共享实现

#### VirtioFS

| 默认值 | 接受值 | 格式   |
|---------------|-----------------|----------|
| `true`        | `true`, `false` | 布尔值  |

- **描述：** 使用 VirtioFS 在主机和容器之间进行快速的原生文件共享。如果值设置为 `true`，VirtioFS 将被设置为文件共享机制。如果 VirtioFS 和 gRPC 都设置为 `true`，则 VirtioFS 优先。
- **操作系统：** {{< badge color=blue text="仅限 Mac" >}} 12.5+
- **用例：** 在现代 macOS 上实现更好的文件系统性能和兼容性。
- **配置此设置的方法：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的**常规设置**
    - 设置管理：[`admin-settings.json` 文件](/manuals/enterprise/security/hardened-desktop/settings-management/configure-json-file.md) 中的 `useVirtualizationFrameworkVirtioFS` 设置
    - 设置管理：[Admin Console](/manuals/enterprise/security/hardened-desktop/settings-management/configure-admin-console.md) 中的**使用 VirtioFS 进行文件共享**设置

> [!NOTE]
>
> 在加固环境中，为 macOS 12.5 及更高版本启用并锁定此设置。

#### gRPC FUSE

| 默认值 | 接受值 | 格式   |
|---------------|-----------------|----------|
| `true`        | `true`, `false` | 布尔值  |

- **描述：** 为 macOS 文件共享启用 gRPC FUSE。如果值设置为 `true`，gRPC Fuse 将被设置为文件共享机制。
- **操作系统：** {{< badge color=blue text="仅限 Mac" >}}
- **用例：** 替代文件共享方案，性能优于旧版 osxfs。
- **配置此设置的方法：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的**常规**设置
    - 设置管理：[`admin-settings.json` 文件](/manuals/enterprise/security/hardened-desktop/settings-management/configure-json-file.md) 中的 `useGrpcfuse` 设置
    - 设置管理：[Admin Console](/manuals/enterprise/security/hardened-desktop/settings-management/configure-admin-console.md) 中的**使用 gRPC FUSE 进行文件共享**设置

> [!NOTE]
>
> 在加固环境中，禁用并锁定此设置。

#### osxfs

| 默认值 | 接受值 | 格式  |
| ------------- | --------------- | ------- |
| `false`       | `true`, `false` | 布尔值 |

- **描述：** 为 macOS 使用原始的 osxfs 文件共享驱动程序。当设置为 true 时，Docker Desktop 使用 osxfs 而不是 VirtioFS 或 gRPC FUSE 将主机目录挂载到容器中。
- **操作系统：** {{< badge color=blue text="仅限 Mac" >}}
- **用例：** 与需要原始文件共享实现的旧版工具兼容。
- **配置此设置的方法：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的**常规**设置

### 发送使用情况统计

| 默认值 | 接受值 | 格式 |
|---------------|-----------------|--------|
| `true`        | `true`, `false` | 布尔值 |

- **描述：** 控制 Docker Desktop 是否收集并向 Docker 发送本地使用情况统计和崩溃报告。此设置影响从 Docker Desktop 应用程序本身收集的遥测数据。它不影响通过 Docker Hub 或其他后端服务收集的服务器端遥测数据，例如登录时间戳、拉取或构建。
- **操作系统：** {{< badge color=blue text="全部" >}}
- **用例：** 帮助 Docker 根据使用模式改进产品。
- **配置此设置的方法：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的**常规**设置
    - 设置管理：[`admin-settings.json` 文件](/manuals/enterprise/security/hardened-desktop/settings-management/configure-json-file.md) 中的 `analyticsEnabled` 设置
    - 设置管理：[Admin Console](/manuals/enterprise/security/hardened-desktop/settings-management/configure-admin-console.md) 中的**发送使用情况统计**设置

> [!NOTE]
>
> 在加固环境中，禁用并锁定此设置。这允许您控制所有数据流，并在需要时通过安全通道收集支持日志。

> [!NOTE]
>
> 使用 Insights Dashboard 的组织可能需要启用此设置，以确保开发者的活动完全可见。如果用户选择退出且该设置未锁定，他们的活动可能会被排除在分析视图之外。

### 使用增强型容器隔离

| 默认值 | 接受值 | 格式   |
|---------------|-----------------|----------|
| `false`       | `true`, `false` | 布尔值  |

- **描述：** 通过 Linux 用户命名空间和额外隔离实现高级容器安全。
- **操作系统：** {{< badge color=blue text="全部" >}}
- **用例：** 防止容器修改 Docker Desktop 虚拟机配置或访问敏感的主机区域。
- **配置此设置的方法：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的**常规设置**
    - 设置管理：[`admin-settings.json` 文件](/manuals/enterprise/security/hardened-desktop/settings-management/configure-json-file.md) 中的 `enhancedContainerIsolation` 设置
    - 设置管理：[Admin Console](/manuals/enterprise/security/hardened-desktop/settings-management/configure-admin-console.md) 中的**启用增强型容器隔离**设置

> [!NOTE]
>
> 在加固环境中，禁用并锁定此设置。这允许您控制所有数据流，并在需要时通过安全通道收集支持日志。

### 显示 CLI 提示

| 默认值 | 接受值 | 格式   |
|---------------|-----------------|----------|
| `true`       | `true`, `false` | 布尔值  |

- **描述：** 使用 Docker 命令时在终端中显示有用的 CLI 建议。
- **操作系统：** {{< badge color=blue text="全部" >}}
- **用例：** 通过上下文提示帮助用户发现 Docker CLI 功能。
- **配置此设置的方法：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的**常规**设置

### 启用 Scout 镜像分析

| 默认值 | 接受值 | 格式   |
|---------------|-----------------|----------|
| `true`        | `true`, `false` | 布尔值  |

- **描述：** Docker Scout SBOM 生成和容器镜像漏洞扫描。
- **操作系统：** {{< badge color=blue text="全部" >}}
- **用例：** 开启漏洞扫描和软件物料清单分析。
- **配置此设置的方法：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的**常规设置**
    - 设置管理：[`admin-settings.json` 文件](/manuals/enterprise/security/hardened-desktop/settings-management/configure-json-file.md) 中的 `sbomIndexing` 设置
    - 设置管理：[Admin Console](/manuals/enterprise/security/hardened-desktop/settings-management/configure-admin-console.md) 中的**SBOM 索引**设置

> [!NOTE]
>
> 在加固环境中，启用并锁定此设置以确保合规性扫描始终可用。

### 启用后台 Scout SBOM 索引

| 默认值 | 接受值 | 格式   |
|---------------|-----------------|----------|
| `false`        | `true`, `false` | 布尔值  |

- **描述：** 无需用户交互即可自动为镜像进行 SBOM 索引。
- **操作系统：** {{< badge color=blue text="全部" >}}
- **用例：** 在空闲时间或镜像操作后进行索引，以保持镜像元数据最新。
- **配置此设置的方法：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的**常规设置**

> [!NOTE]
>
> 在加固环境中，启用并锁定此设置以进行持续的安全分析。

### 自动检查配置

| 默认值         | 接受值 | 格式  |
|-----------------------|-----------------|---------|
| `CurrentSettingsVersions` | 整数         | 整数 |

- **描述：** 定期验证 Docker Desktop 配置是否未被外部应用程序修改。
- **操作系统：** {{< badge color=blue text="全部" >}}
- **用例：** 跟踪配置版本以进行兼容性和变更检测。
- **配置此设置的方法：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的**常规**设置
    - 设置管理：[`admin-settings.json` 文件](/manuals/enterprise/security/hardened-desktop/settings-management/configure-json-file.md) 中的 `configurationFileVersion` 设置

## 资源设置

### CPU 限制

| 默认值                                 | 接受值 | 格式  |
|-----------------------------------------------|-----------------|---------|
| 主机上可用的逻辑 CPU 核心数 | 整数         | 整数 |

- **描述：** 分配给 Docker Desktop 虚拟机的 CPU 核心数。
- **操作系统：** {{< badge color=blue text="全部" >}}
- **用例：** 平衡 Docker 性能与主机系统资源可用性。
- **配置此设置的方法：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的**高级**资源设置

### 内存限制

| 默认值              | 接受值 | 格式  |
|---------------------------|-----------------|---------|
| 基于系统资源 | 整数         | 整数 |

- **描述：** 分配给 Docker Desktop 虚拟机的 RAM 量（以 MiB 为单位）。
- **操作系统：** {{< badge color=blue text="全部" >}}
- **用例：** 控制内存分配，以优化 Docker 和主机应用程序的性能。
- **配置此设置的方法：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的**高级**资源设置

### 交换空间

| 默认值 | 接受值 | 格式  |
|---------------|-----------------|---------|
| `1024`        | 整数         | 整数 |

- **描述：** Docker 虚拟机可用的交换空间量（以 MiB 为单位）。
- **操作系统：** {{< badge color=blue text="全部" >}}
- **用例：** 当物理 RAM 有限时，扩展容器工作负载的可用内存。
- **配置此设置的方法：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的**高级**资源设置

### 磁盘使用限制

| 默认值                  | 接受值 | 格式  |
|-------------------------------|-----------------|---------|
| 机器的默认磁盘大小。 | 整数         | 整数 |

- **描述：** 为 Docker Desktop 数据分配的最大磁盘空间（以 MiB 为单位）。
- **操作系统：** {{< badge color=blue text="全部" >}}
- **用例：** 防止 Docker 消耗主机系统上过多的磁盘空间。
- **配置此设置的方法：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的**高级**资源设置

### 磁盘镜像位置

| 默认值                                                                 | 接受值 | 格式 |
|--------------------------------------------------|-----------------|--------|
| macOS: `~/Library/Containers/com.docker.docker/Data/vms/0`  <br> Windows: `%USERPROFILE%\AppData\Local\Docker\wsl\data` | 文件路径       | 字符串 |

- **描述：** Docker Desktop 存储虚拟机数据的文件系统路径。
- **操作系统：** {{< badge color=blue text="全部" >}}
- **用例：** 将 Docker 数据移至自定义存储位置以进行性能或空间管理。
- **配置此设置的方法：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的**高级**资源设置

### 启用资源节省器

| 默认值 | 接受值 | 格式   |
|---------------|-----------------|----------|
| `true`        | `true`, `false` | 布尔值  |

- **描述：** 空闲时自动暂停 Docker Desktop 以节省系统资源。
- **操作系统：** {{< badge color=blue text="全部" >}}
- **用例：** 当 Docker Desktop 未被主动使用时，减少 CPU 和内存使用。
- **配置此设置的方法：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的**高级**资源设置

### 文件共享目录

| 默认值                           | 接受值                 | 格式                  |
|----------------------------------------|---------------------------------|--------------------------|
| 因操作系统而异                           | 文件路径字符串列表   | 字符串数组列表   |

- **描述：** 可以作为卷挂载到容器中的主机目录。
- **操作系统：** {{< badge color=blue text="全部" >}}
- **用例：** 定义容器可以访问哪些主机目录以用于开发工作流。
- **配置此设置的方法：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的**文件共享**资源设置
    - 设置管理：[`admin-settings.json` 文件](/manuals/enterprise/security/hardened-desktop/settings-management/configure-json-file.md) 中的 `filesharingAllowedDirectories` 设置
    - 设置管理：[Admin Console](/manuals/enterprise/security/hardened-desktop/settings-management/configure-admin-console.md) 中的**允许的文件共享目录**设置

> [!NOTE]
>
> 在加固环境中，锁定到明确的允许列表并禁用最终用户编辑。

### 代理排除

| 默认值 | 接受值    | 格式 |
|---------------|--------------------|--------|
| `""`          | 地址列表  | 字符串 |

- **描述：** 容器在使用代理设置时应绕过的网络地址。
- **操作系统：** {{< badge color=blue text="全部" >}}
- **用例：** 为内部服务或特定域定义代理例外。
- **配置此设置的方法：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的**代理**资源设置
    - 设置管理：[`admin-settings.json` 文件](/manuals/enterprise/security/hardened-desktop/settings-management/configure-json-file.md) 中 `proxy` 设置的 `manual` 和 `exclude` 模式
    - 设置管理：[Admin Console](/manuals/enterprise/security/hardened-desktop/settings-management/configure-admin-console.md) 中的**代理**部分

> [!NOTE]
>
> 在加固环境中，禁用并锁定此设置以保持严格的代理控制。

### Docker 子网

| 默认值     | 接受值 | 格式 |
|-------------------|-----------------|--------|
| `192.168.65.0/24` | IP 地址      | 字符串 |

- **描述：** 覆盖用于 `*.docker.internal` 的 vpnkit DHCP/DNS 的网络范围。
- **操作系统：** {{< badge color=blue text="仅限 Mac" >}}
- **用例：** 自定义用于 Docker 容器网络的子网。
- **配置此设置的方法：**
    - 设置管理：[`admin-settings.json` 文件](/enterprise/security/hardened-desktop/settings-management/configure-json-file.md) 中的 `vpnkitCIDR` 设置
    - 设置管理：[Admin Console](/enterprise/security/hardened-desktop/settings-management/configure-admin-console.md) 中的**VPN Kit CIDR** 设置

### 对 UDP 使用内核网络

| 默认值 | 接受值 | 格式   |
|---------------|-----------------|----------|
| `false`       | `true`, `false` | 布尔值  |

- **描述：** 对 UDP 流量使用主机的内核网络堆栈，而不是 Docker 的虚拟网络驱动程序。这可以实现更快、更直接的 UDP 通信，但可能会绕过某些容器隔离功能。
- **操作系统：** {{< badge color=blue text="全部" >}}
- **用例：** 提高 UDP 密集型应用程序（如实时媒体、DNS 或游戏）的性能。
- **配置此设置的方法：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的**网络**资源设置

### 启用主机网络

| 默认值 | 接受值 | 格式   |
|---------------|-----------------|----------|
| `false`       | `true`, `false` | 布尔值  |

- **描述：** 实验性支持容器直接使用主机网络堆栈。
- **操作系统：** {{< badge color=blue text="全部" >}}
- **用例：** 允许容器在特定场景下绕过 Docker 的网络隔离。
- **配置此设置的方法：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的**网络**资源设置

### 网络模式

| 默认值 | 接受值 | 格式   |
|---------------|-----------------|----------|
| `dual-stack` | `ipv4only`, `ipv6only` | 字符串  |

- **描述：** Docker 创建新网络时使用的默认 IP 协议。
- **操作系统：** {{< badge color=blue text="Windows 和 Mac" >}}
- **用例：** 与仅支持 IPv4 或 IPv6 的网络基础设施保持一致。
- **配置此设置的方法：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的**网络**资源设置
    - 设置管理：[`admin-settings.json` 文件](/enterprise/security/hardened-desktop/settings-management/configure-json-file.md) 中的 `defaultNetworkingMode` 设置
    - 设置管理：[Admin Console](/enterprise/security/hardened-desktop/settings-management/configure-admin-console.md) 中的**默认网络 IP 模式**

更多信息，请参阅[网络](/manuals/desktop/features/networking.md#networking-mode-and-dns-behaviour-for-mac-and-windows)。

#### 抑制 IPv4/IPv6 的 DNS 解析

| 默认值 | 接受值 | 格式   |
|---------------|-----------------|----------|
| `auto` | `ipv4`, `ipv6`, `none` | 字符串  |

- **描述：** 过滤不支持的 DNS 记录类型。需要 Docker Desktop 4.43 及更高版本。
- **操作系统：** {{< badge color=blue text="Windows 和 Mac" >}}
- **用例：** 控制 Docker 如何过滤返回给容器的 DNS 记录，在仅支持 IPv4 或 IPv6 的环境中提高可靠性。
- **配置此设置的方法：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的**网络**资源设置
    - 设置管理：[`admin-settings.json` 文件](/enterprise/security/hardened-desktop/settings-management/configure-json-file.md) 中的 `dnsInhibition` 设置
    - 设置管理：[Admin Console](/enterprise/security/hardened-desktop/settings-management/configure-admin-console.md) 中的**DNS 过滤行为**

更多信息，请参阅[网络](/manuals/desktop/features/networking.md#networking-mode-and-dns-behaviour-for-mac-and-windows)。

### 启用 WSL 引擎

| 默认值 | 接受值 | 格式   |
|---------------|-----------------|----------|
| `true`        | `true`, `false` | 布尔值  |

- **描述：** 如果值设置为 `true`，Docker Desktop 将使用基于 WSL2 的引擎。这会覆盖安装时使用 `--backend=<backend name>` 标志设置的任何内容。
- **操作系统：** {{< badge color=blue text="仅限 Windows" >}} + WSL
- **用例：** 使用 WSL 2 后端在 Windows 上运行 Linux 容器以获得更好的性能。
- **配置此设置的方法：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的**WSL 集成**资源设置
    - 设置管理：[`admin-settings.json` 文件](/enterprise/security/hardened-desktop/settings-management/configure-json-file.md) 中的 `wslEngineEnabled` 设置
    - 设置管理：[Admin Console](/enterprise/security/hardened-desktop/settings-management/configure-admin-console.md) 中的**Windows Subsystem for Linux (WSL) 引擎**设置

> [!NOTE]
>
> 在加固环境中，启用并锁定此设置以提高安全性和性能。

## Docker 引擎设置

Docker 引擎设置允许您通过原始 JSON 对象配置底层守护程序设置。这些设置直接传递给在 Docker Desktop 中提供容器管理的 dockerd 进程。

| 键                   | 示例                     | 描述                                        | 接受值 / 格式       | 默认值 |
| --------------------- | --------------------------- | -------------------------------------------------- | ------------------------------ | ------- |
| `debug`               | `true`                      | 在 Docker 守护程序中启用详细日志记录        | 布尔值                        | `false` |
| `experimental`        | `true`                      | 启用实验性的 Docker CLI 和守护程序功能 | 布尔值                        | `false` |
| `insecure-registries` | `["myregistry.local:5000"]` | 允许从没有 TLS 的 HTTP 注册表拉取     | 字符串数组 (`host:port`) | `[]`    |
| `registry-mirrors`    | `["https://mirror.gcr.io"]` | 定义备用注册表端点              | URL 数组                  | `[]`    |

- **描述：** 使用直接传递给 dockerd 的结构化 JSON 配置来自定义 Docker 守护程序的行为。
- **操作系统：** {{< badge color=blue text="全部" >}}
- **用例：** 配置注册表访问、启用调试日志记录或开启实验性功能。
- **配置此设置的方法：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的**Docker 引擎**设置

> [!NOTE]
>
> 在加固环境中，提供经过审查的配置并锁定它，以防止未经授权的守护程序修改。

> [!IMPORTANT]
>
> 此设置的值按原样传递给 Docker 守护程序。无效或不受支持的字段可能会导致 Docker Desktop 无法启动。

## 构建器设置

构建器设置允许您管理用于高级镜像构建场景的 Buildx 构建器实例，包括多平台构建和自定义后端。

| 键         | 示例                          | 描述                                                                | 接受值 / 格式  | 默认值   |
| ----------- | -------------------------------- | -------------------------------------------------------------------------- | ------------------------- | --------- |
| `name`      | `"my-builder"`                   | 构建器实例的名称                                               | 字符串                    | —         |
| `driver`    | `"docker-container"`             | 构建器使用的后端 (`docker`, `docker-container`, `remote`, 等.) | 字符串                    | `docker`  |
| `platforms` | `["linux/amd64", "linux/arm64"]` | 构建器支持的目标平台                                  | 平台字符串数组 | 主机架构 |

- **描述：** 用于高级镜像构建场景的 Buildx 构建器实例。
- **操作系统：** {{< badge color=blue text="全部" >}}
- **用例：** 设置跨平台构建、远程构建器或自定义构建环境。
- **配置此设置的方法：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的**构建器**设置

> [!NOTE]
>
> 构建器定义被构造为对象数组，每个对象描述一个构建器实例。冲突或不受支持的配置可能会导致构建错误。

## AI 设置

### 启用 Docker 模型运行器

| 默认值 | 接受值 | 格式   |
|---------------|-----------------|----------|
| `true`        | `true`, `false` | 布尔值  |

- **描述：** Docker 模型运行器功能，用于在容器中运行 AI 模型。
- **操作系统：** {{< badge color=blue text="全部" >}}
- **用例：** 使用 Docker 基础设施运行和管理 AI/ML 模型。
- **配置此设置的方法：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的**AI**设置
    - 设置管理：[`admin-settings.json` 文件](/enterprise/security/hardened-desktop/settings-management/configure-json-file.md) 中的 `enableInference` 设置
    - 设置管理：[Admin Console](/enterprise/security/hardened-desktop/settings-management/configure-admin-console.md) 中的**启用 Docker 模型运行器**设置

#### 启用主机端 TCP 支持

| 默认值 | 接受值 | 格式   |
|---------------|-----------------|----------|
| `false`       | `true`, `false` | 布尔值  |

- **描述：** Docker 模型运行器服务的 TCP 连接性。
- **操作系统：** {{< badge color=blue text="全部" >}}
- **用例：** 允许外部应用程序通过 TCP 连接到模型运行器。
- **配置此设置的方法：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的**AI**设置
    - 设置管理：[`admin-settings.json` 文件](/enterprise/security/hardened-desktop/settings-management/configure-json-file.md) 中的 `enableInferenceTCP` 设置
    - 设置管理：[Admin Console](/enterprise/security/hardened-desktop/settings-management/configure-admin-console.md) 中的**主机端 TCP 支持**设置

> [!NOTE]
>
> 此设置需要首先启用 Docker 模型运行器设置。

##### 端口

| 默认值 | 接受值 | 格式  |
|---------------|-----------------|---------|
| 12434         | 整数         | 整数 |

- **描述：** 用于模型运行器 TCP 连接的特定端口。
- **