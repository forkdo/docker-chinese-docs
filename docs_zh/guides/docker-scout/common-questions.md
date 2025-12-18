---
title: 常见挑战与问题
description: 探索与 Docker Scout 相关的常见挑战与问题。
---

<!-- vale Docker.HeadingLength = NO -->

### Docker Scout 与其他安全工具有何不同？

Docker Scout 在容器安全方面采取了更全面的方法，与第三方安全工具相比，后者即使提供修复建议，其在软件供应链中的应用安全态势覆盖范围也十分有限，且在建议修复方案方面往往缺乏指导。这类工具要么在运行时监控方面存在限制，要么完全不提供运行时保护。即使它们提供运行时监控，其对关键策略的遵循也十分有限。第三方安全工具对 Docker 特定构建的策略评估范围也较为局限。通过专注于整个软件供应链、提供可执行的指导以及全面的运行时保护和强大的策略执行，Docker Scout 超越了仅仅识别容器漏洞的范畴。它帮助你从底层开始构建安全的应用程序。

### 我可以将 Docker Scout 与 Docker Hub 以外的外部注册表一起使用吗？

你可以将 Docker Scout 与 Docker Hub 以外的注册表一起使用。将 Docker Scout 与第三方容器注册表集成后，Docker Scout 可以对这些仓库运行镜像分析，从而让你深入了解这些镜像的组成，即使它们未托管在 Docker Hub 上。

以下容器注册表集成可用：

- Artifactory
- Amazon Elastic Container Registry
- Azure Container Registry

更多关于在第三方注册表中配置 Docker Scout 的信息，请参阅 [将 Docker Scout 与第三方注册表集成](/scout/integrations/#container-registries)。

### Docker Scout CLI 是否默认随 Docker Desktop 一起提供？

是的，Docker Scout CLI 插件已预装在 Docker Desktop 中。

### 是否可以在没有 Docker Desktop 的 Linux 系统上运行 `docker scout` 命令？

如果你在没有 Docker Desktop 的情况下运行 Docker Engine，Docker Scout 不会预装，但你可以将其作为独立二进制文件[安装](/scout/install/)。

### Docker Scout 如何使用 SBOM？

SBOM（软件物料清单）是构成软件组件的清单列表。[Docker Scout 使用 SBOM](/scout/concepts/sbom/) 来确定 Docker 镜像中使用的组件。当你分析镜像时，Docker Scout 会使用附加到镜像的 SBOM（作为证明），或通过分析镜像内容动态生成 SBOM。

SBOM 会与咨询数据库进行交叉引用，以确定镜像中的组件是否存在已知漏洞。

<div id="scout-lp-survey-anchor"></div>