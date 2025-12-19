---
linktitle: 探索
title: 探索 Docker Hardened Images
description: 了解 Docker Hardened Images、其用途、构建和测试方式，以及安全方面的共同责任模型。
weight: 10
params:
  grid_about:
    - title: 什么是加固镜像以及为何要使用它们？
      description: 了解什么是加固镜像、Docker Hardened Images 的构建方式、它们与典型基础镜像和应用镜像的区别，以及您应该使用它们的原因。
      icon: info
      link: /dhi/explore/what/
    - title: 构建流程
      description: 了解 Docker 如何通过自动化、以安全为中心的管道来构建、测试和维护 Docker Hardened Images。
      icon: build
      link: /dhi/explore/build-process/
    - title: 镜像测试
      description: 查看 Docker Hardened Images 如何自动进行标准合规性、功能性和安全性测试。
      icon: science
      link: /dhi/explore/test/
    - title: 责任概述
      description: 了解在您将 Docker Hardened Images 作为安全软件供应链的一部分使用时，Docker 的角色和您的责任。
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
---

Docker Hardened Images (DHI) 是由 Docker 维护的最小化、安全且可用于生产的容器基础镜像和应用镜像。DHI 旨在减少漏洞并简化合规性，它可以轻松集成到您现有的基于 Docker 的工作流程中，几乎不需要或完全不需要进行工具调整。

本节帮助您了解 Docker Hardened Images 是什么、它们的构建和测试方式、可用的不同类型，以及 Docker 和您作为用户之间如何分担责任。有关 DHI 功能和特性的完整列表，请参阅 [功能](/dhi/features/)。

## 了解更多关于 Docker Hardened Images 的信息

{{< grid
  items="grid_about"
>}}