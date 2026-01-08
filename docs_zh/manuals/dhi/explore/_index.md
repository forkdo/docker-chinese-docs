---
linktitle: 探索
title: 探索 Docker Hardened Images
description: 了解 Docker Hardened Images 的用途、构建和测试方式，以及安全责任共担模型。
weight: 10
params:
  grid_about:
    - title: 什么是加固镜像，为什么使用它们？
      description: 了解什么是加固镜像，Docker Hardened Images 如何构建，它们与典型的基础镜像和应用镜像的区别，以及为何应使用它们。
      icon: info
      link: /dhi/explore/what/
    - title: 构建流程
      description: 了解 Docker 如何通过自动化的、以安全为重点的流水线构建、测试和维护 Docker Hardened Images。
      icon: build
      link: /dhi/explore/build-process/
    - title: 镜像测试
      description: 了解 Docker Hardened Images 如何自动测试标准合规性、功能性和安全性。
      icon: science
      link: /dhi/explore/test/
    - title: 责任概述
      description: 了解在使用 Docker Hardened Images 作为安全软件供应链的一部分时，Docker 和您作为用户各自的责任。
      icon: group
      link: /dhi/explore/responsibility/
    - title: 镜像类型
      description: 了解 Docker Hardened Images 目录中提供的不同镜像类型、发行版和变体。
      icon: view_module
      link: /dhi/explore/available/
    - title: 提供反馈
      icon: question_exchange
      description: Docker 欢迎所有贡献和反馈。
      link: /dhi/explore/feedback
aliases:
  - /dhi/about/
---

Docker Hardened Images (DHI) 是由 Docker 维护的最小化、安全且可直接用于生产的容器基础镜像和应用镜像。DHI 旨在减少漏洞并简化合规性，能够轻松集成到您现有的基于 Docker 的工作流中，几乎无需重新配置工具。

本节帮助您了解 Docker Hardened Images 是什么，它们如何构建和测试，有哪些可用的类型，以及 Docker 和您作为用户之间的责任如何分担。有关 DHI 功能和特性的完整列表，请参阅[功能](/dhi/features/)。

## 了解更多关于 Docker Hardened Images 的信息

{{< grid
  items="grid_about"
>}}