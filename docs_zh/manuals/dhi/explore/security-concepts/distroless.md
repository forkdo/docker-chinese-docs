---
aliases:
  - /dhi/core-concepts/distroless/
title: Minimal or distroless images（最小或 distroless 镜像）
linktitle: Distroless images（Distroless 镜像）
description: 了解 Docker Hardened Images 如何使用 distroless 变体来最小化攻击面并移除不必要的组件。
keywords: distroless container image, minimal docker image, secure base image, no shell container, reduced attack surface
---


Minimal images（最小镜像），有时称为 distroless 镜像，是去除了不必要组件（如包管理器、shell，甚至底层操作系统发行版）的容器镜像。Docker Hardened Images（DHI）采用这种精简方法以减少漏洞并强化安全的软件交付。[Docker Official Images](../../../docker-hub/image-library/trusted-content.md#docker-official-images) 和 [Docker Verified Publisher Images](../../../docker-hub/image-library/trusted-content.md#verified-publisher-images) 遵循类似的精简和安全最佳实践，但为确保在更广泛的使用场景中保持兼容性，可能不会删减得如此彻底。

## What are minimal or distroless images?（什么是最小或 distroless 镜像？）

传统容器镜像包含完整的操作系统，往往超出运行应用程序所需的范畴。相比之下，最小或 distroless 镜像仅包含：

- 应用程序二进制文件
- 其运行时依赖项（例如 libc、Java、Python）
- 任何明确需要的配置或元数据

它们通常排除：

- 操作系统工具（例如 `ls`、`ps`、`cat`）
- Shell（例如 `sh`、`bash`）
- 包管理器（例如 `apt`、`apk`）
- 调试工具（例如 `curl`、`wget`、`strace`）

Docker Hardened Images 基于此模型构建，确保更小且更安全的运行时面。

## What you gain（你将获得什么）

| 收益                | 描述                                                                   |
|------------------------|-------------------------------------------------------------------------------|
| 更小的攻击面 | 组件越少意味着漏洞更少，CVE 暴露面更小                                         |
| 更快的启动         | 更小的镜像体积带来更快的拉取和启动时间                     |
| 改进的安全性      | 缺少 shell 和包管理器限制了攻击者在系统被攻破时可以执行的操作 |
| 更好的合规性      | 更易于审计和验证，尤其是配合 SBOM 和证明 |

## Addressing common tradeoffs（应对常见权衡）

最小和 distroless 镜像提供了强大的安全优势，但它们可能改变你与容器协作的方式。Docker Hardened Images 在设计时兼顾了生产力与安全性。

| 关注点           | Docker Hardened Images 如何应对                                                                                                                                                                                         |
|-------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 可调试性（Debuggability） | 加固镜像默认排除 shell 和 CLI 工具。使用 [Docker Debug](/reference/cli/docker/debug/) 临时附加一个调试 sidecar 进行故障排查，而无需修改原始容器。 |
| 熟悉度（Familiarity）   | DHI 支持多个基础镜像，包括 Alpine 和 Debian 变体，因此你可以选择熟悉的环境，同时仍能受益于加固实践。                                                        |
| 灵活性（Flexibility）   | 运行时不可变性有助于保护你的容器。使用多阶段构建和 CI/CD 来控制变更，并在开发期间可选择使用以开发为重点的基础镜像。                                                  |

通过在精简与实用工具之间取得平衡，Docker Hardened Images 在不牺牲安全性或可靠性的前提下支持现代开发工作流。

## Best practices for using minimal images（使用最小镜像的最佳实践）

- 使用多阶段构建来分离构建时和运行时环境
- 使用 CI 流水线验证镜像行为，而非交互式检查
- 在你的 Dockerfile 中明确包含特定于运行时的依赖项
- 使用 Docker Scout 持续监控 CVE，即使在最小镜像中也是如此

通过 Docker Hardened Images 采用最小或 distroless 镜像，你将获得一个更安全、可预测且可用于生产的容器环境，它专为自动化、清晰和降低风险而设计。
