---
linkTitle: Limitations
title: 增强型容器隔离的限制
description: 增强型容器隔离的已知限制和平台特定注意事项
keywords: enhanced container isolation, limitations, wsl, hyper-v, kubernetes, docker build
toc_max: 3
weight: 30
aliases:
 - /security/for-admins/hardened-desktop/enhanced-container-isolation/limitations/
---

{{< summary-bar feature_name="Hardened Docker Desktop" >}}

增强型容器隔离（ECI）在不同平台上存在一些特定的限制和功能约束。了解这些限制有助于您规划安全策略并设定合理的期望。

## WSL 2 安全注意事项

> [!NOTE]
>
> Docker Desktop 需要 WSL 2 版本 2.1.5 或更高版本。使用 `wsl --version` 检查您的版本，如有需要使用 `wsl --update` 更新。

增强型容器隔离根据您的 Windows 后端配置提供不同的安全级别。

下表比较了 WSL 2 上的 ECI 和 Hyper-V 上的 ECI：

| 安全功能                                   | WSL 上的 ECI   | Hyper-V 上的 ECI   | 说明               |
| -------------------------------------------------- | ------------ | ---------------- | --------------------- |
| 强安全容器                         | 是          | 是              | 使恶意容器工作负载更难破坏 Docker Desktop Linux VM 和主机。 |
| Docker Desktop Linux VM 受保护，防止用户访问 | 否           | 是              | 在 WSL 上，用户可以直接访问 Docker Engine 或绕过 Docker Desktop 安全设置。 |
| Docker Desktop Linux VM 拥有专用内核     | 否           | 是              | 在 WSL 上，Docker Desktop 无法保证内核级别配置的完整性。 |

WSL 2 的安全漏洞包括：

- 直接 VM 访问：用户可以通过直接访问 VM 来绕过 Docker Desktop 安全设置：`wsl -d docker-desktop`。这使用户能够以 root 身份访问并修改 Docker Engine 设置，绕过设置管理配置。
- 共享内核漏洞：所有 WSL 2 发行版共享同一个 Linux 内核实例。其他 WSL 发行版可以修改影响 Docker Desktop 安全性的内核设置。

### 建议

使用 Hyper-V 后端以获得最大安全性。WSL 2 提供更好的性能和资源利用率，但安全隔离性较低。

## 不支持 Windows 容器

ECI 仅适用于 Linux 容器（Docker Desktop 的默认模式）。不支持原生 Windows 容器模式。

## Docker Build 保护程度不同

Docker Build 保护取决于驱动程序和 Docker Desktop 版本：

| 构建驱动 | 保护 | 版本要求 |
|:------------|:-----------|:---------------------|
| `docker` (默认) | 受保护 | Docker Desktop 4.30 及以后版本（WSL 2 除外） |
| `docker` (旧版) | 未受保护 | Docker Desktop 4.30 之前版本 |
| `docker-container` | 始终受保护 | 所有 Docker Desktop 版本 |

以下 Docker Build 功能在 ECI 下无法工作：

- `docker build --network=host`
- Docker Buildx 权限：`network.host`、`security.insecure`

### 建议

对于需要这些功能的构建，请使用 `docker-container` 构建驱动：

```console
$ docker buildx create --driver docker-container --use
$ docker buildx build --network=host .
```

## Docker Desktop Kubernetes 未受保护

集成的 Kubernetes 功能无法从 ECI 保护中受益。恶意或特权 Pod 可以破坏 Docker Desktop VM 并绕过安全控制。

### 建议

使用 Kubernetes in Docker (KinD) 获得 ECI 保护的 Kubernetes：

```console
$ kind create cluster
```

启用 ECI 后，每个 Kubernetes 节点都在 ECI 保护的容器中运行，提供与 Docker Desktop VM 的更强隔离。

## 未受保护的容器类型

以下容器类型目前无法从 ECI 保护中受益：

- Docker Extensions：扩展容器在没有 ECI 保护的情况下运行
- Docker Debug：Docker Debug 容器绕过 ECI 限制
- Kubernetes pods：使用 Docker Desktop 集成 Kubernetes 时

### 建议

仅使用来自可信来源的扩展，在安全敏感环境中避免使用 Docker Debug。

## 全局命令限制

命令列表适用于所有允许挂载 Docker 套接字的容器。您无法为每个容器镜像配置不同的命令限制。

## 不支持仅本地镜像

除非满足以下条件，否则无法允许任意仅本地镜像（不在注册表中的镜像）挂载 Docker 套接字：

- 派生自允许的基础镜像（使用 `allowDerivedImages: true`）
- 使用通配符允许列表（`"*"`，Docker Desktop 4.36 及以后版本）

## 不支持的 Docker 命令

以下 Docker 命令目前不支持在命令列表限制中使用：

- `compose`：Docker Compose 命令
- `dev`：开发环境命令
- `extension`：Docker Extensions 管理
- `feedback`：Docker 反馈提交
- `init`：Docker 初始化命令
- `manifest`：镜像清单管理
- `plugin`：插件管理
- `sbom`：软件物料清单
- `scout`：Docker Scout 命令
- `trust`：镜像信任管理

## 性能考虑

### 派生镜像影响

启用 `allowDerivedImages: true` 会为镜像验证增加约 1 秒的容器启动时间。

### 注册表依赖

- Docker Desktop 定期从注册表获取镜像摘要以进行验证
- 容器首次启动需要注册表访问以验证允许的镜像
- 网络连接问题可能导致容器启动延迟

### 镜像摘要验证

当注册表中的允许镜像更新时，本地容器可能会被意外阻止，直到您刷新本地镜像：

```console
$ docker image rm <image>
$ docker pull <image>
```

## 版本兼容性

ECI 功能在不同 Docker Desktop 版本中逐步引入：

- Docker Desktop 4.36 及以后版本：通配符允许列表支持（`"*"`）和改进的派生镜像处理
- Docker Desktop 4.34 及以后版本：派生镜像支持（`allowDerivedImages`）
- Docker Desktop 4.30 及以后版本：使用默认驱动的 Docker Build 保护（WSL 2 除外）
- Docker Desktop 4.13 及以后版本：核心 ECI 功能

要获得最新的功能可用性，请使用最新版本的 Docker Desktop。

## 生产环境兼容性

### 容器行为差异

大多数容器在有无 ECI 的情况下运行相同。然而，某些高级工作负载的行为可能不同：

- 需要加载内核模块的容器
- 修改全局内核设置的工作负载（BPF、sysctl）
- 期望特定特权提升行为的应用程序
- 需要直接硬件设备访问的工具

在生产部署之前，请在开发环境中使用 ECI 测试高级工作负载以确保兼容性。

### 运行时考虑

使用 Sysbox 运行时（配合 ECI）的容器与生产环境中标准 OCI runc 运行时相比可能有细微差异。这些差异通常只影响特权或系统级操作。