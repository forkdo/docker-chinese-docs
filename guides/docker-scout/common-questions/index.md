# 常见挑战与问题

<!-- vale Docker.HeadingLength = NO -->

### Docker Scout 与其他安全工具有何不同？

与第三方安全工具相比，Docker Scout 采取了更广泛的容器安全方法。第三方安全工具即使提供修复指导，也常常因为其在软件供应链中应用安全态势的有限范围而有所欠缺，并且在建议修复方案方面通常指导有限。这类工具要么在运行时监控方面存在限制，要么根本没有运行时保护。当它们确实提供运行时监控时，其在遵守关键策略方面也有限制。第三方安全工具对 Docker 特定构建的策略评估范围有限。通过专注于整个软件供应链、提供可操作的指导，并提供具有强大策略执行能力的全面运行时保护，Docker Scout 不仅仅是识别容器中的漏洞。它帮助你从头开始构建安全的应用程序。

### 我可以将 Docker Scout 与 Docker Hub 以外的外部注册表一起使用吗？

你可以将 Scout 与 Docker Hub 以外的注册表一起使用。将 Docker Scout 与第三方容器注册表集成，使 Docker Scout 能够对这些仓库运行镜像分析，这样即使它们没有托管在 Docker Hub 上，你也可以深入了解这些镜像的构成。

提供以下容器注册表集成：

- Artifactory
- Amazon Elastic Container Registry
- Azure Container Registry

在[将 Docker Scout 与第三方注册表集成](/scout/integrations/#container-registries)中了解有关配置 Scout 与注册表的更多信息。

### Docker Scout CLI 是否默认随 Docker Desktop 提供？

是的，Docker Scout CLI 插件随 Docker Desktop 预装。

### 是否可以在没有 Docker Desktop 的 Linux 系统上运行 `docker scout` 命令？

如果你在没有 Docker Desktop 的情况下运行 Docker Engine，Docker Scout 不会预装，但你可以[将其作为独立二进制文件安装](/scout/install/)。

### Docker Scout 如何使用 SBOM？

SBOM（软件物料清单）是构成软件组件的成分列表。[Docker Scout 使用 SBOM](/scout/concepts/sbom/) 来确定 Docker 镜像中使用的组件。当你分析镜像时，Docker Scout 会使用附加到镜像的 SBOM（作为证明），或者通过分析镜像内容即时生成 SBOM。

SBOM 会与咨询数据库进行交叉引用，以确定镜像中的任何组件是否存在已知漏洞。

<div id="scout-lp-survey-anchor"></div>
