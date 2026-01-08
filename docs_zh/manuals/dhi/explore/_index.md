---
---
linktitle: Explore
title: Explore Docker Hardened Images
description: "Learn about Docker Hardened Images, their purpose, how they are built and tested, and the shared responsibility model for security."
weight: 10
params:
  grid_about:
    - title: What are hardened images and why use them?
      description: "Learn what a hardened image is, how Docker Hardened Images are built, what sets them apart from typical base and application images, and why you should use them."
      icon: info
      link: /dhi/explore/what/
    - title: Build process
      description: "Learn how Docker builds, tests, and maintains Docker Hardened Images through an automated, security-focused pipeline."
      icon: build
      link: /dhi/explore/build-process/
    - title: Image testing
      description: "See how Docker Hardened Images are automatically tested for standards compliance, functionality, and security."
      icon: science
      link: /dhi/explore/test/
    - title: Responsibility overview
      description: "Understand Docker's role and your responsibilities when using Docker Hardened Images as part of your secure software supply chain."
      icon: group
      link: /dhi/explore/responsibility/
    - title: Image types
      description: "Learn about the different image types, distributions, and variants offered in the Docker Hardened Images catalog."
      icon: view_module
      link: /dhi/explore/available/
    - title: Give feedback
      icon: question_exchange
      description: Docker welcomes all contributions and feedback.
      link: /dhi/explore/feedback
aliases:
  - /dhi/about/---
linktitle: 探索
title: 探索 Docker Hardened Images
description: "了解 Docker Hardened Images 的用途、构建和测试方式，以及安全性的共享责任模型。"
weight: 10
params:
  grid_about:
    - title: 什么是加固镜像，为什么使用它们？
      description: "了解什么是加固镜像，Docker Hardened Images 如何构建，它们与典型的基础镜像和应用镜像的区别，以及为何应该使用它们。"
      icon: info
      link: /dhi/explore/what/
    - title: 构建流程
      description: "了解 Docker 如何通过自动化的、以安全为重点的流水线构建、测试和维护 Docker Hardened Images。"
      icon: build
      link: /dhi/explore/build-process/
    - title: 镜像测试
      description: "查看 Docker Hardened Images 如何自动测试标准合规性、功能性和安全性。"
      icon: science
      link: /dhi/explore/test/
    - title: 责任概述
      description: "了解在使用 Docker Hardened Images 作为安全软件供应链的一部分时，Docker 的角色和您的责任。"
      icon: group
      link: /dhi/explore/responsibility/
    - title: 镜像类型
      description: "了解 Docker Hardened Images 目录中提供的不同类型、发行版和变体。"
      icon: view_module
      link: /dhi/explore/available/
    - title: 提供反馈
      icon: question_exchange
      description: Docker 欢迎所有贡献和反馈。
      link: /dhi/explore/feedback---
Docker Hardened Images (DHI) 是由 Docker 维护的最小化、安全且可直接用于生产的容器基础镜像和应用镜像。DHI 旨在减少漏洞并简化合规性，可以轻松集成到您现有的基于 Docker 的工作流中，几乎无需重新配置工具。

本节帮助您了解 Docker Hardened Images 是什么、它们如何构建和测试、可用的不同类型，以及 Docker 和您作为用户之间的责任共享方式。有关 DHI 功能和特性的完整列表，请参阅 [功能](/dhi/features/)。

## 了解更多关于 Docker Hardened Images 的信息

{{< grid
  items="grid_about"
>}}