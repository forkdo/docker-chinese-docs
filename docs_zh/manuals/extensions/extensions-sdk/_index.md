---
title: 扩展 SDK 概览
linkTitle: 扩展 SDK
description: Docker 扩展 SDK 文档总索引
keywords: Docker, Extensions, sdk
aliases:
- /desktop/extensions-sdk/dev/overview/
- /desktop/extensions-sdk/
grid:
- title: 构建和发布流程
  description: 了解构建和发布扩展的流程。
  icon: checklist
  link: /extensions/extensions-sdk/process/
- title: 快速入门指南
  description: 遵循快速入门指南快速创建一个基本的 Docker 扩展。
  icon: explore
  link: /extensions/extensions-sdk/quickstart/
- title: 查看设计指南
  description: 确保您的扩展符合 Docker 的设计指南和原则。
  icon: design_services
  link: /extensions/extensions-sdk/design/design-guidelines/
- title: 发布您的扩展
  description: 了解如何将您的扩展发布到 Marketplace。
  icon: publish
  link: /extensions/extensions-sdk/extensions/
- title: 与 Kubernetes 交互
  description: 查找有关如何从您的 Docker 扩展中间接与 Kubernetes 集群交互的信息。
  icon: multiple_stop
  link: /extensions/extensions-sdk/guides/kubernetes/
- title: 多架构扩展
  description: 为您的扩展构建多个架构版本。
  icon: content_copy
  link: /extensions/extensions-sdk/extensions/multi-arch/
---

本节中的资源可帮助您创建自己的 Docker 扩展。

Docker CLI 工具提供了一组命令来帮助您构建和发布扩展，这些扩展被打包为特殊格式的 Docker 镜像。

镜像文件系统的根目录下有一个 `metadata.json` 文件，用于描述扩展的内容。这是 Docker 扩展的基本要素。

扩展可以包含 UI 部分和在主机或 Desktop 虚拟机中运行的后端部分。更多信息请参阅 [架构](architecture/_index.md)。

您可以通过 Docker Hub 分发扩展。不过，您也可以在本地开发扩展，而无需将扩展推送到 Docker Hub。详情请参阅 [扩展分发](extensions/DISTRIBUTION.md)。

{{% include "extensions-form.md" %}}

{{< grid >}}