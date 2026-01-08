---
---
linktitle: Image types
title: Available types of Docker Hardened Images
description: "Learn about the different image types, distributions, and variants offered in the Docker Hardened Images catalog."
weight: 20
aliases:
  - /dhi/about/available/
keywords: "docker hardened images, distroless containers, distroless images, docker distroless, alpine base image, debian base image, development containers, runtime containers, secure base image, multi-stage builds"---
linktitle: 镜像类型
title: Docker Hardened Images 可用类型
description: "了解 Docker Hardened Images 目录中提供的不同镜像类型、发行版和变体。"
weight: 20---
Docker Hardened Images (DHI) 是一个全面的安全加固容器镜像目录，旨在满足各种开发和生产需求。

## 框架和应用程序镜像

DHI 包含一系列流行的框架和应用程序镜像，每个镜像都经过加固和维护，以确保安全性和合规性。这些镜像可以无缝集成到现有工作流中，使开发人员能够在不牺牲安全性的情况下专注于构建应用程序。

例如，您可能会在 DHI 目录中找到类似以下内容的仓库：

- `node`：Node.js 应用程序的框架
- `python`：Python 应用程序的框架
- `nginx`：Web 服务器镜像

## 基础镜像发行版

Docker Hardened Images 提供不同的基础镜像选项，使您可以灵活地选择最适合您环境和工作负载要求的选项：

- 基于 Debian 的镜像：如果您已经在使用基于 glibc 的环境，这是一个不错的选择。Debian 被广泛使用，并在许多语言生态系统和企业系统中提供强大的兼容性。

- 基于 Alpine 的镜像：使用 musl libc 的更小、更轻量的选项。这些镜像通常体积较小，因此拉取速度更快，且占用空间更少。

每个镜像通过移除非必要组件（如 Shell、包管理器和调试工具）来维护最小且安全的运行时层。这有助于减少攻击面，同时保持与常见运行时环境的兼容性。为了维护这种精简、安全的基础，DHI 在基于 glibc 的镜像上标准化使用 Debian，它在最大程度减少复杂性和维护开销的同时，提供了广泛的兼容性。

示例标签包括：

- `3.9.23-alpine3.21`：Python 3.9.23 的基于 Alpine 的镜像
- `3.9.23-debian12`：Python 3.9.23 的基于 Debian 的镜像

如果您不确定选择哪种，请从您已经熟悉的基础开始。Debian 往往提供最广泛的兼容性。

## 开发和运行时变体

为了适应应用程序生命周期的不同阶段，DHI 为所有语言框架镜像和选定的应用程序镜像提供两种变体：

- 开发 镜像：配备了必要的开发工具和库，这些镜像有助于在安全的环境中构建和测试应用程序。它们包括 Shell、包管理器、root 用户以及开发所需的其他工具。

- 运行时镜像：剥离了开发工具，这些镜像仅包含运行应用程序所需的基本组件，从而确保生产环境中的攻击面最小。

这种分离支持多阶段构建，使开发人员能够在安全的构建环境中编译代码，并使用精简的运行时镜像进行部署。

例如，您可能会在 DHI 仓库中找到类似以下内容的标签：

- `3.9.23-debian12`：Python 3.9.23 的运行时镜像
- `3.9.23-debian12-dev`：Python 3.9.23 的开发镜像

## FIPS 和 STIG 变体 {tier="DHI Enterprise"}

{{< summary-bar feature_name="Docker Hardened Images" >}}

某些 Docker Hardened Images 包含 `-fips` 变体。这些变体使用根据 [FIPS 140](../core-concepts/fips.md) 验证的加密模块，这是美国安全加密操作的标准。

FIPS 变体旨在帮助组织满足在敏感或受监管环境中与加密使用相关的监管和合规要求。

您可以通过包含 `-fips` 的标签来识别 FIPS 变体。

例如：
- `3.13-fips`：Python 3.13 镜像的 FIPS 变体
- `3.9.23-debian12-fips`：基于 Debian 的 Python 3.9.23 镜像的 FIPS 变体

FIPS 变体的使用方式与任何其他 Docker Hardened Image 相同，非常适合在受监管行业或需要加密验证的合规框架下运营的团队。

除了 FIPS 变体外，某些 Docker Hardened Images 还包含 STIG 就绪变体。这些镜像根据基于 STIG 的自定义配置文件进行扫描，并附有签名的 STIG 扫描证明，以支持审计和合规报告。要识别 STIG 就绪变体，请在 Docker Hub 目录的镜像标签列表中的 **Compliance** 列中查找 **STIG**。

## 兼容性变体

某些 Docker Hardened Images 包含兼容性变体。这些变体为特定用例提供额外的工具和配置，而不会使最小基础镜像变得臃肿。

创建兼容性变体是为了支持：

- Helm chart 兼容性：通过 Helm charts 和 Kubernetes 部署的应用程序，这些应用程序需要特定的运行时配置或实用程序，以便与流行的 Helm charts 无缝集成。

- 特殊应用程序用例：需要最小镜像中未包含的可选工具的应用程序。

通过将这些作为单独的镜像风格提供，DHI 确保最小镜像保持精简和安全，同时在专用变体中提供您所需的工具。这种方法为标准部署维持了最小的攻击面，同时在需要时支持特殊要求。

您可以通过包含 `-compat` 的标签来识别兼容性变体。

当您的部署需要超出最小运行时范围的其他工具时（例如使用 Helm charts 或具有特定工具要求的应用程序），请使用兼容性变体。