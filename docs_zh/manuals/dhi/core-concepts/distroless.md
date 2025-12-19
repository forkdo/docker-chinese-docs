---
title: 极简或无发行版镜像
linktitle: 无发行版镜像
description: 了解 Docker Hardened Images 如何使用无发行版变体来最小化攻击面并移除不必要的组件。
keywords: distroless container image, minimal docker image, secure base image, no shell container, reduced attack surface
---


极简镜像（有时称为无发行版镜像）是去除了不必要组件（如包管理器、Shell，甚至底层操作系统发行版）的容器镜像。Docker Hardened Images (DHI) 采用这种极简方法，以减少漏洞并确保安全的软件交付。[Docker Official Images](../../docker-hub/image-library/trusted-content.md#docker-official-images) 和 [Docker Verified Publisher Images](../../docker-hub/image-library/trusted-content.md#verified-publisher-images) 也遵循类似的极简主义和安全性最佳实践，但为了确保更广泛用例的兼容性，它们可能不会削减得如此彻底。

## 什么是极简或无发行版镜像？

传统的容器镜像包含完整的操作系统，通常超出了运行应用程序所需的内容。相比之下，极简或无发行版镜像仅包含：

- 应用程序二进制文件
- 其运行时依赖项（例如，libc、Java、Python）
- 任何明确要求的配置或元数据

它们通常不包括：

- OS 工具（例如，`ls`、`ps`、`cat`）
- Shell（例如，`sh`、`bash`）
- 包管理器（例如，`apt`、`apk`）
- 调试工具（例如，`curl`、`wget`、`strace`）

Docker Hardened Images 基于此模型构建，确保更小、更安全的运行时环境。

## 优势

| 优势 | 描述 |
|------------------------|-------------------------------------------------------------------------------|
| 更小的攻击面 | 组件越少意味着漏洞越少，暴露于 CVE 的风险越低 |
| 启动更快 | 镜像体积更小，拉取和启动时间更快 |
| 安全性更高 | 缺少 Shell 和包管理器限制了攻击者在被攻破后能做的事情 |
| 更易于合规 | 更容易审计和验证，尤其是在使用 SBOM 和证明时 |

## 解决常见的权衡问题

极简和无发行版镜像提供了强大的安全性优势，但它们可能会改变你使用容器的方式。Docker Hardened Images 旨在提高安全性的同时保持生产力。

| 关注点 | Docker Hardened Images 如何提供帮助 |
|-------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 可调试性 | 强化镜像默认排除 Shell 和 CLI 工具。使用 [Docker Debug](../../../reference/cli/docker/debug.md) 临时附加调试 sidecar 进行故障排除，而无需修改原始容器。 |
| 熟悉度 | DHI 支持多种基础镜像，包括 Alpine 和 Debian 变体，因此你可以选择熟悉的环境，同时仍能受益于强化实践。 |
| 灵活性 | 运行时不可变性有助于保护容器安全。使用多阶段构建和 CI/CD 来控制变更，并可在开发阶段选择性地使用面向开发的基础镜像。 |

通过在极简主义与实用工具之间取得平衡，Docker Hardened Images 支持现代开发工作流程，同时不损害安全性或可靠性。

## 使用极简镜像的最佳实践

- 使用多阶段构建来分离构建时和运行时环境
- 使用 CI 流水线验证镜像行为，而非交互式检查
- 在 Dockerfile 中明确包含运行时特定的依赖项
- 使用 Docker Scout 持续监控 CVE，即使在极简镜像中也是如此

通过 Docker Hardened Images 采用极简或无发行版镜像，你将获得一个更安全、可预测且为生产环境准备就绪的容器环境，该环境专为自动化、清晰性和降低风险而设计。