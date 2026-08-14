---
description: 了解 Compose Bridge 如何将 Docker Compose 文件转换为 Kubernetes 清单，以实现无缝的平台迁移
keywords: docker compose bridge, compose to kubernetes, docker compose kubernetes integration, docker compose kustomize, compose bridge docker desktop
title: Compose Bridge 概述
linkTitle: Compose Bridge
weight: 50
---

{{< summary-bar feature_name="Compose bridge" >}}

Compose Bridge 将您的 Docker Compose 配置转换为特定于平台的部署格式，例如 Kubernetes 清单。默认情况下，它会生成：

- Kubernetes 清单
- Kustomize 覆盖层 (overlay)

这些输出已准备好部署在启用了 [Kubernetes](/manuals/desktop/settings-and-maintenance/settings.md#kubernetes) 的 Docker Desktop 上。

Compose Bridge 帮助您弥合 Compose 和 Kubernetes 之间的差距，让您在保持 Compose 的简洁性和高效性的同时，更轻松地采用 Kubernetes。

它是一个灵活的工具，您可以利用[默认转换](usage.md)，也可以[创建自定义转换](customize.md)以满足特定的项目需求和要求。

## 工作原理

Compose Bridge 使用转换 (transformation) 将 Compose 模型转换为另一种形式。

转换被打包为一个 Docker 镜像，它接收完全解析后的 Compose 模型作为 `/in/compose.yaml`，并可以在 `/out` 下生成任何目标格式的文件。

Compose Bridge 使用 Go 模板提供了自己的 Kubernetes 转换，因此通过替换或附加您自己的模板，可以轻松地进行扩展和自定义。

有关这些转换如何工作以及如何为您的项目进行自定义的更多详细信息，请参阅[自定义](customize.md)。

Compose Bridge 还支持通过 Docker Model Runner 使用 LLM 的应用程序。

更多详情，请参阅[使用 Model Runner](use-model-runner.md)。

## 大规模应用组织标准

Compose Bridge 支持自定义转换模板，这让平台团队能够一次性编入组织标准，并在每次将 `compose.yaml`
文件转换为 Kubernetes 清单或其他格式时一致地应用它们。

开发人员继续编写标准的 Compose 文件。在转换期间，Compose Bridge 运行你的自定义转换，并自动将
所需的安全上下文、资源限制、标签和网络策略注入到输出清单中——无需开发人员了解或管理这些细节。

当你的需求变化时，在一个地方更新转换模板。每个团队在下一次转换时都会获取这些更改，无需编辑
各个 Compose 文件。

这种关注点分离让开发人员专注于应用配置，而平台团队通过转换层控制治理并执行策略。

要开始使用，请参阅[自定义 Compose Bridge](/manuals/compose/bridge/customize.md)。

## 下一步是什么？

- [使用 Compose Bridge](usage.md)
- [探索如何自定义 Compose Bridge](customize.md)