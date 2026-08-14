---
title: Docker Build
weight: 20
description: 概览 Docker Build，了解如何打包和捆绑你的代码并将其发布到任何地方
keywords: build, buildx, buildkit
params:
  sidebar:
    group: Application development
grid:
- title: 打包你的软件
  description: '构建并打包你的应用程序，使其可以在任何地方运行：本地或云端。'
  icon: archive-box
  link: /build/concepts/overview/
- title: 多阶段构建
  description: 使用最少的依赖项保持镜像小巧且安全。
  icon: arrow-trending-up
  link: /build/building/multi-stage/
- title: 多平台镜像
  description: 在不同的计算机架构上无缝构建、推送、拉取和运行镜像。
  icon: document-duplicate
  link: /build/building/multi-platform/
- title: BuildKit
  description: 探索 BuildKit，这个开源构建引擎。
  icon: wrench-screwdriver
  link: /build/buildkit/
- title: 构建驱动
  description: 配置你在何处以及如何运行构建。
  icon: wrench-screwdriver
  link: /build/builders/drivers/
- title: 导出器
  description: 导出你喜欢的任何制品，不仅仅是 Docker 镜像。
  icon: arrow-up-on-square
  link: /build/exporters/
- title: 构建缓存
  description: 避免重复执行代价高昂的操作，例如包安装。
  icon: arrow-path
  link: /build/cache/
- title: Bake
  description: 使用 Bake 编排你的构建。
  icon: cake
  link: /build/bake/
aliases:
- /buildx/working-with-buildx/
- /develop/develop-images/build_enhancements/
---

Docker Build 是 Docker Engine 最常用的功能之一。每当你创建镜像时，你都在使用 Docker Build。Build 是你软件开发生命周期的关键部分，让你能够打包和捆绑你的代码并将其发布到任何地方。

Docker Build 不仅仅是一个用于构建镜像的命令，也不仅仅是关于打包你的代码。它是一个完整的工具和特性生态系统，不仅支持常见的工作流任务，还为更复杂和高级的场景提供支持。

{{< grid >}}
