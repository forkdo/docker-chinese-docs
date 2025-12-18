---
title: 设置参考
linkTitle: 设置参考
description: Docker Desktop 设置和配置选项的完整参考
keywords: docker desktop 设置, 配置参考, 管理员控制, 设置管理
aliases:
 - /security/for-admins/hardened-desktop/settings-management/settings-reference/
---

本文档提供了 Docker Desktop 所有设置和配置选项的完整参考。使用本文档可以了解不同配置方法和平台上的设置行为。内容结构与 Docker Desktop GUI 保持一致。

每个设置包括：

- 默认值和可接受值
- 平台兼容性
- 配置方法（Docker Desktop GUI、Admin Console、`admin-settings.json` 文件或 CLI）
- 适用的企业安全建议

## 通用设置

### 登录计算机时启动 Docker Desktop

| 默认值 | 可接受值 | 格式 |
|--------|----------|------|
| `false` | `true`, `false` | 布尔值 |

- **描述：** 用户登录计算机时自动启动 Docker Desktop。
- **操作系统：** {{< badge color=blue text="所有" >}}
- **使用场景：** 确保系统启动后 Docker Desktop 始终可用。
- **配置方法：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的 **通用** 设置

### Docker Desktop 启动时打开 Docker 仪表板

| 默认值 | 可接受值 | 格式 |
|--------|----------|------|
| `false` | `true`, `false` | 布尔值 |

- **描述：** Docker Desktop 启动时是否自动打开 Docker 仪表板。
- **操作系统：** {{< badge color=blue text="所有" >}}
- **使用场景：** 启动后立即访问容器、镜像和卷。
- **配置方法：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的 **通用** 设置

### 选择 Docker Desktop 主题

| 默认值 | 可接受值 | 格式 |
|--------|----------|------|
| `system` | `light`, `dark`, `system` | 枚举 |

- **描述：** Docker Desktop 界面的视觉外观。
- **操作系统：** {{< badge color=blue text="所有" >}}
- **使用场景：** 根据用户偏好或系统主题自定义界面外观。
- **配置方法：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的 **通用** 设置

### 配置 Shell 补全

| 默认值 | 可接受值 | 格式 |
|--------|----------|------|
| `integrated` | `integrated`, `system` | 字符串 |

- **描述：** Docker CLI 自动补全与用户 Shell 的集成方式。
- **操作系统：** {{< badge color=blue text="所有" >}}
- **使用场景：** 控制 Docker 是否修改 Shell 配置文件以实现自动补全。
- **配置方法：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的 **通用** 设置

### 选择容器终端

| 默认值 | 可接受值 | 格式 |
|--------|----------|------|
| `integrated` | `integrated`, `system` | 字符串 |

- **描述：** 从 Docker Desktop 启动 Docker CLI 时使用的默认终端。
- **操作系统：** {{< badge color=blue text="所有" >}}
- **使用场景：** 为 Docker CLI 交互设置首选的终端应用程序。
- **配置方法：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的 **通用** 设置

### 启用 Docker 终端

| 默认值 | 可接受值 | 格式 |
|--------|----------|------|
| `false` | `true`, `false` | 布尔值 |

- **描述：** 访问 Docker Desktop 集成终端功能。如果值设置为 `false`，用户无法使用 Docker 终端与主机交互或直接从 Docker Desktop 执行命令。
- **操作系统：** {{< badge color=blue text="所有" >}}
- **使用场景：** 允许或限制开发者访问内置终端以与主机系统交互。
- **配置方法：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的 **通用** 设置
    - 设置管理：[`admin-settings.json` 文件](/manuals/enterprise/security/hardened-desktop/settings-management/configure-json-file.md) 中的 `desktopTerminalEnabled` 设置

> [!NOTE]
>
> 在强化环境中，禁用并锁定此设置以限制主机访问。

### 默认启用 Docker 调试

| 默认值 | 可接受值 | 格式 |
|--------|----------|------|
| `false` | `true`, `false` | 布尔值 |

- **描述：** Docker CLI 命令是否默认启用调试日志记录。
- **操作系统：** {{< badge color=blue text="所有" >}}
- **使用场景：** 为故障排除和支持场景提供详细输出。
- **配置方法：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的 **通用** 设置

### 将 VM 包含在 Time Machine 备份中

| 默认值 | 可接受值 | 格式 |
|--------|----------|------|
| `false` | `true`, `false` | 布尔值 |

- **描述：** Docker Desktop 虚拟机是否包含在 macOS Time Machine 备份中。
- **操作系统：** {{< badge color=blue text="仅 Mac" >}}
- **使用场景：** 平衡备份完整性与备份大小和性能。
- **配置方法：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的 **通用** 设置

### 使用 containerd 拉取和存储镜像

| 默认值 | 可接受值 | 格式 |
|--------|----------|------|
| `false` | `true`, `false` | 布尔值 |

- **描述：** Docker Desktop 使用的镜像存储后端。
- **操作系统：** {{< badge color=blue text="所有" >}}
- **使用场景：** 提高镜像处理性能并启用 containerd 原生功能。
- **配置方法：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的 **通用** 设置

### 选择虚拟机管理器

#### Docker VMM

| 默认值 | 可接受值 | 格式 |
|--------|----------|------|
| `true` | `true`, `false` | 布尔值 |

#### Apple 虚拟化框架

| 默认值 | 可接受值 | 格式 |
|--------|----------|------|
| `true` | `true`, `false` | 布尔值 |

- **描述：** 使用 Apple 虚拟化框架运行 Docker 容器。
- **操作系统：** {{< badge color=blue text="仅 Mac" >}}
- **使用场景：** 在 Apple Silicon 上提高 VM 性能。
- **配置方法：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的 **通用** 设置

#### Rosetta

| 默认值 | 可接受值 | 格式 |
|--------|----------|------|
| `true` | `true`, `false` | 布尔值 |

- **描述：** 在 Apple Silicon 上使用 Rosetta 模拟 `amd64`。如果值设置为 `true`，Docker Desktop 会启用 Rosetta 以加速 Apple Silicon 上的 x86_64/amd64 二进制模拟。
- **操作系统：** {{< badge color=blue text="仅 Mac" >}} 13+
- **使用场景：** 在 Apple Silicon 主机上运行 Intel 基础的容器。
- **配置方法：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的 **通用** 设置
    - 设置管理：[`admin-settings.json` 文件](/manuals/enterprise/security/hardened-desktop/settings-management/configure-json-file.md) 中的 `useVirtualizationFrameworkRosetta` 设置
    - 设置管理：[Admin Console](/manuals/enterprise/security/hardened-desktop/settings-management/configure-admin-console.md) 中的 **在 Apple Silicon 上使用 Rosetta 进行 x86_64/amd64 模拟** 设置

> [!NOTE]
>
> 在强化环境中，禁用并锁定此设置，以便仅允许 ARM 原生镜像。

> [!NOTE]
>
> Rosetta 需要启用 Apple 虚拟化框架。

#### QEMU

> [!WARNING]
>
> QEMU 已在 Docker Desktop 4.44 及更高版本中弃用。更多信息请参阅[博客公告](https://www.docker.com/blog/docker-desktop-for-mac-qemu-virtualization-option-to-be-deprecated-in-90-days/)

| 默认值 | 可接受值 | 格式 |
|--------|----------|------|
| `true` | `true`, `false` | 布尔值 |

### 选择文件共享实现

#### VirtioFS

| 默认值 | 可接受值 | 格式 |
|--------|----------|------|
| `true` | `true`, `false` | 布尔值 |

- **描述：** 使用 VirtioFS 实现主机和容器之间的快速、原生文件共享。如果值设置为 `true`，VirtioFS 被设置为文件共享机制。如果 VirtioFS 和 gRPC 都设置为 `true`，VirtioFS 优先。
- **操作系统：** {{< badge color=blue text="仅 Mac" >}} 12.5+
- **使用场景：** 在现代 macOS 上实现更好的文件系统性能和兼容性。
- **配置方法：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的 **通用设置**
    - 设置管理：[`admin-settings.json` 文件](/manuals/enterprise/security/hardened-desktop/settings-management/configure-json-file.md) 中的 `useVirtualizationFrameworkVirtioFS` 设置
    - 设置管理：[Admin Console](/manuals/enterprise/security/hardened-desktop/settings-management/configure-admin-console.md) 中的 **使用 VirtioFS 进行文件共享** 设置

> [!NOTE]
>
> 在强化环境中，为 macOS 12.5 及更高版本启用并锁定此设置。

#### gRPC FUSE

| 默认值 | 可接受值 | 格式 |
|--------|----------|------|
| `true` | `true`, `false` | 布尔值 |

- **描述：** 为 macOS 文件共享启用 gRPC FUSE。如果值设置为 `true`，gRPC Fuse 被设置为文件共享机制。
- **操作系统：** {{< badge color=blue text="仅 Mac" >}}
- **使用场景：** 使用改进的性能替代传统的 osxfs。
- **配置方法：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的 **通用** 设置
    - 设置管理：[`admin-settings.json` 文件](/manuals/enterprise/security/hardened-desktop/settings-management/configure-json-file.md) 中的 `useGrpcfuse` 设置
    - 设置管理：[Admin Console](/manuals/enterprise/security/hardened-desktop/settings-management/configure-admin-console.md) 中的 **使用 gRPC FUSE 进行文件共享** 设置

> [!NOTE]
>
> 在强化环境中，禁用并锁定此设置。

#### osxfs

| 默认值 | 可接受值 | 格式 |
|--------|----------|------|
| `false` | `true`, `false` | 布尔值 |

- **描述：** 对 macOS 使用原始的 osxfs 文件共享驱动程序。当设置为 true 时，Docker Desktop 使用 osxfs 而不是 VirtioFS 或 gRPC FUSE 将主机目录挂载到容器中。
- **操作系统：** {{< badge color=blue text="仅 Mac" >}}
- **使用场景：** 与需要原始文件共享实现的遗留工具兼容。
- **配置方法：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的 **通用** 设置

### 发送使用情况统计信息

| 默认值 | 可接受值 | 格式 |
|--------|----------|------|
| `true` | `true`, `false` | 布尔值 |

- **描述：** 控制 Docker Desktop 是否收集并发送本地使用情况统计和崩溃报告到 Docker。此设置影响从 Docker Desktop 应用程序本身收集的遥测数据。它不影响通过 Docker Hub 或其他后端服务（如登录时间戳、拉取或构建）收集的服务器端遥测数据。
- **操作系统：** {{< badge color=blue text="所有" >}}
- **使用场景：** 帮助 Docker 根据使用模式改进产品。
- **配置方法：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的 **通用** 设置
    - 设置管理：[`admin-settings.json` 文件](/manuals/enterprise/security/hardened-desktop/settings-management/configure-json-file.md) 中的 `analyticsEnabled` 设置
    - 设置管理：[Admin Console](/manuals/enterprise/security/hardened-desktop/settings-management/configure-admin-console.md) 中的 **发送使用情况统计信息** 设置

> [!NOTE]
>
> 在强化环境中，禁用并锁定此设置。这允许您控制所有数据流，如有需要，可以通过安全通道收集支持日志。

> [!NOTE]
>
> 使用 Insights Dashboard 的组织可能需要启用此设置，以确保开发者活动完全可见。如果用户选择退出且设置未被锁定，他们的活动可能不会出现在分析视图中。

### 使用增强容器隔离

| 默认值 | 可接受值 | 格式 |
|--------|----------|------|
| `false` | `true`, `false` | 布尔值 |

- **描述：** 通过 Linux 用户命名空间和额外隔离实现高级容器安全。
- **操作系统：** {{< badge color=blue text="所有" >}}
- **使用场景：** 防止容器修改 Docker Desktop VM 配置或访问敏感主机区域。
- **配置方法：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的 **通用设置**
    - 设置管理：[`admin-settings.json` 文件](/manuals/enterprise/security/hardened-desktop/settings-management/configure-json-file.md) 中的 `enhancedContainerIsolation` 设置
    - 设置管理：[Admin Console](/manuals/enterprise/security/hardened-desktop/settings-management/configure-admin-console.md) 中的 **启用增强容器隔离** 设置

> [!NOTE]
>
> 在强化环境中，禁用并锁定此设置。这允许您控制所有数据流，如有需要，可以通过安全通道收集支持日志。

### 显示 CLI 提示

| 默认值 | 可接受值 | 格式 |
|--------|----------|------|
| `true` | `true`, `false` | 布尔值 |

- **描述：** 在使用 Docker 命令时，在终端中显示有用的 CLI 建议。
- **操作系统：** {{< badge color=blue text="所有" >}}
- **使用场景：** 通过上下文提示帮助用户发现 Docker CLI 功能。
- **配置方法：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的 **通用** 设置

### 启用 Scout 镜像分析

| 默认值 | 可接受值 | 格式 |
|--------|----------|------|
| `true` | `true`, `false` | 布尔值 |

- **描述：** Docker Scout SBOM 生成和容器镜像漏洞扫描。
- **操作系统：** {{< badge color=blue text="所有" >}}
- **使用场景：** 启用漏洞扫描和软件物料清单分析。
- **配置方法：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的 **通用设置**
    - 设置管理：[`admin-settings.json` 文件](/manuals/enterprise/security/hardened-desktop/settings-management/configure-json-file.md) 中的 `sbomIndexing` 设置
    - 设置管理：[Admin Console](/manuals/enterprise/security/hardened-desktop/settings-management/configure-admin-console.md) 中的 **SBOM 索引** 设置

> [!NOTE]
>
> 在强化环境中，启用并锁定此设置以确保合规性扫描始终可用。

### 启用后台 Scout SBOM 索引

| 默认值 | 可接受值 | 格式 |
|--------|----------|------|
| `false` | `true`, `false` | 布尔值 |

- **描述：** 自动 SBOM 索引，无需用户交互。
- **操作系统：** {{< badge color=blue text="所有" >}}
- **使用场景：** 通过在空闲时间或镜像操作后索引来保持镜像元数据最新。
- **配置方法：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的 **通用设置**

> [!NOTE]
>
> 在强化环境中，启用并锁定此设置以实现连续安全分析。

### 自动检查配置

| 默认值 | 可接受值 | 格式 |
|--------|----------|------|
| `CurrentSettingsVersions` | 整数 | 整数 |

- **描述：** 定期验证 Docker Desktop 配置未被外部应用程序修改。
- **操作系统：** {{< badge color=blue text="所有" >}}
- **使用场景：** 跟踪配置版本以实现兼容性和变更检测。
- **配置方法：**
    - [Docker Desktop GUI](/manuals/desktop/settings-and-maintenance/settings.md) 中的 **通用** 设置
    - 设置管理：[`admin-settings.json` 文件](/manuals/enterprise/security/hardened-desktop/settings-management/configure-json-file.md) 中的 `configurationFileVersion` 设置

## 资源设置

### CPU 限制

| 默认值