---
linktitle: Image types
title: Docker Hardened Images 可用类型
description: 了解 Docker Hardened Images 目录中提供的不同类型、发行版和变体。
keywords: docker hardened images, distroless containers, distroless images, docker distroless, alpine base image, debian base image, development containers, runtime containers, secure base image, multi-stage builds
weight: 20
---

Docker Hardened Images (DHI) 是一个全面的安全强化容器镜像目录，构建用于满足多样化的开发和生产需求。

## 框架和应用镜像

DHI 包含一系列流行的框架和应用镜像，每个镜像都经过安全强化和维护，确保安全性和合规性。这些镜像能够无缝集成到现有工作流中，让开发者能够专注于构建应用，而不牺牲安全性。

例如，您可能在 DHI 目录中找到如下仓库：

- `node`：Node.js 应用的框架
- `python`：Python 应用的框架
- `nginx`：Web 服务器镜像

## 基础镜像发行版

Docker Hardened Images 提供多种基础镜像选项，让您能够灵活选择最适合环境和工作负载需求的镜像：

- Debian 基础镜像：适合已在 glibc 环境中工作的场景。Debian 应用广泛，提供对多种语言生态和企业系统的强兼容性。

- Alpine 基础镜像：一种更小、更轻量的选项，使用 musl libc。这些镜像体积更小，因此拉取速度更快，占用空间更少。

每个镜像通过移除非必要组件（如 shell、包管理器和调试工具）来维持最小且安全的运行时层。这有助于减少攻击面，同时保持与常见运行时环境的兼容性。为了维持这种精简、安全的基础，DHI 对 glibc 基础镜像标准化使用 Debian，这在最小化复杂性和维护开销的同时提供了广泛的兼容性。

示例标签包括：

- `3.9.23-alpine3.21`：Python 3.9.23 的 Alpine 基础镜像
- `3.9.23-debian12`：Python 3.9.23 的 Debian 基础镜像

如果您不确定如何选择，建议从您熟悉的基础开始。Debian 通常提供最广泛的兼容性。

## 开发和运行时变体

为了适应应用生命周期的不同阶段，DHI 为所有语言框架镜像和部分应用镜像提供两种变体：

- 开发（dev）镜像：配备必要的开发工具和库，这些镜像便于在安全环境中构建和测试应用。它们包含 shell、包管理器、root 用户和其他开发所需工具。

- 运行时镜像：移除开发工具，仅包含运行应用所需的必要组件，确保生产环境中的最小攻击面。

这种分离支持多阶段构建，使开发者能够在安全的构建环境中编译代码，并使用精简的运行时镜像进行部署。

例如，您可能在 DHI 仓库中找到如下标签：

- `3.9.23-debian12`：Python 3.9.23 的运行时镜像
- `3.9.23-debian12-dev`：Python 3.9.23 的开发镜像

## FIPS 和 STIG 变体 {tier="DHI Enterprise"}

{{< summary-bar feature_name="Docker Hardened Images" >}}

部分 Docker Hardened Images 包含 `-fips` 变体。这些变体使用经过 [FIPS 140](../core-concepts/fips.md) 验证的加密模块，FIPS 140 是美国政府关于安全加密操作的标准。

FIPS 变体旨在帮助组织满足敏感或受监管环境中与加密使用相关的法规和合规性要求。

您可以通过标签中包含 `-fips` 来识别 FIPS 变体。

例如：
- `3.13-fips`：Python 3.13 镜像的 FIPS 变体
- `3.9.23-debian12-fips`：Debian 基础 Python 3.9.23 镜像的 FIPS 变体

FIPS 变体可以像使用任何其他 Docker Hardened Image 一样使用，非常适合在受监管行业或需要加密验证的合规框架下运营的团队。

除了 FIPS 变体，部分 Docker Hardened Images 还包含 STIG 就绪变体。这些镜像会基于自定义 STIG 配置文件进行扫描，并提供签名的 STIG 扫描证明，以支持审计和合规报告。要识别 STIG 就绪变体，请查看 Docker Hub 目录中镜像标签列表的 **Compliance** 列中的 **STIG** 标识。

## 兼容性变体

部分 Docker Hardened Images 包含兼容性变体。这些变体为特定用例提供额外工具和配置，而不会使最小基础镜像变得臃肿。

兼容性变体的创建旨在支持：

- Helm chart 兼容性：通过 Helm chart 和 Kubernetes 部署的应用，需要特定运行时配置或工具以与流行 Helm chart 无缝集成。

- 特殊应用用例：需要可选工具的应用，这些工具未包含在最小镜像中。

通过提供这些独立的镜像风味，DHI 确保最小镜像保持精简和安全，同时在专用变体中提供您所需的工具。这种方法在标准部署中维持最小攻击面，同时在需要时支持特殊需求。

您可以通过标签中包含 `-compat` 来识别兼容性变体。

当您的部署需要超出最小运行时的额外工具时（例如使用 Helm chart 或具有特定工具需求的应用），请使用兼容性变体。