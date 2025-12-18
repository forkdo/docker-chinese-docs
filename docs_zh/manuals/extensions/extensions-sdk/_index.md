---
title: Extensions SDK 概述
linkTitle: Extensions SDK
description: Docker Extensions SDK 文档的总体索引
keywords: Docker, Extensions, sdk
aliases:
 - /desktop/extensions-sdk/dev/overview/
 - /desktop/extensions-sdk/
grid:
  - title: "构建和发布流程"
    description: 了解构建和发布扩展的流程。
    icon: "checklist"
    link: "/extensions/extensions-sdk/process/"
  - title: "快速开始指南"
    description: 遵循快速开始指南，快速创建一个基础的 Docker 扩展。
    icon: "explore"
    link: "/extensions/extensions-sdk/quickstart/"
  - title: "查看设计指南"
    description: 确保你的扩展符合 Docker 的设计指南和原则。
    icon: "design_services"
    link: "/extensions/extensions-sdk/design/design-guidelines/"
  - title: "发布你的扩展"
    description: 了解如何将你的扩展发布到 Marketplace。
    icon: "publish"
    link: "/extensions/extensions-sdk/extensions/"
  - title: "与 Kubernetes 交互"
    description: 查找如何从 Docker 扩展中与 Kubernetes 集群进行间接交互的信息。
    icon: "multiple_stop"
    link: "/extensions/extensions-sdk/guides/kubernetes/"
  - title: "多架构扩展"
    description: 为多个架构构建你的扩展。
    icon: "content_copy"
    link: "/extensions/extensions-sdk/extensions/multi-arch/"
---

本节中的资源可帮助你创建自己的 Docker 扩展。

Docker CLI 工具提供了一组命令，帮助你构建和发布扩展，这些扩展被打包为特殊格式的 Docker 镜像。

在镜像文件系统的根目录下，有一个 `metadata.json` 文件，用于描述扩展的内容。这是 Docker 扩展的核心元素。

扩展可以包含 UI 部分和后端部分，后端部分可以在主机或 Desktop 虚拟机中运行。更多详细信息，请参阅 [架构](architecture/_index.md)。

你通过 Docker Hub 分发扩展。但是，你可以在本地开发扩展，无需将扩展推送到 Docker Hub。详细信息，请参阅 [扩展分发](extensions/DISTRIBUTION.md)。

{{% include "extensions-form.md" %}}

{{< grid >}}