---
description: 了解 Compose Bridge 如何将 Docker Compose 文件转换为 Kubernetes 清单，实现平台间的无缝迁移
keywords: docker compose bridge, compose to kubernetes, docker compose kubernetes integration, docker compose kustomize, compose bridge docker desktop
title: Compose Bridge 概述
linkTitle: Compose Bridge
weight: 50
---

{{< summary-bar feature_name="Compose bridge" >}}

Compose Bridge 将您的 Docker Compose 配置转换为特定平台的部署格式，例如 Kubernetes 清单。默认情况下，它会生成：

- Kubernetes 清单
- 一个 Kustomize 覆盖层

这些输出可直接在启用了 [Kubernetes](/manuals/desktop/settings-and-maintenance/settings.md#kubernetes) 的 Docker Desktop 上部署使用。

Compose Bridge 帮助您弥合 Compose 与 Kubernetes 之间的差距，让您在保持 Compose 简洁高效的同时，更轻松地采用 Kubernetes。

这是一个灵活的工具，您可以利用其 [默认转换](usage.md)，也可以 [创建自定义转换](customize.md) 以满足特定项目的需要和要求。

## 工作原理

Compose Bridge 使用转换将 Compose 模型转换为另一种形式。

转换被打包为 Docker 镜像，接收完全解析的 Compose 模型作为 `/in/compose.yaml`，并可在 `/out` 下生成任何目标格式的文件。

Compose Bridge 提供了基于 Go 模板的 Kubernetes 转换，因此通过替换或追加您自己的模板即可轻松扩展和自定义。

有关这些转换如何工作以及如何为您的项目自定义的详细信息，请参阅 [自定义](customize.md)。

Compose Bridge 还支持通过 Docker Model Runner 使用大语言模型（LLM）的应用程序。

更多详情，请参阅 [使用 Model Runner](use-model-runner.md)。

## 接下来做什么？

- [使用 Compose Bridge](usage.md)
- [探索如何自定义 Compose Bridge](customize.md)