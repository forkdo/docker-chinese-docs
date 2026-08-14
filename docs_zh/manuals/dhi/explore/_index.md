---
linktitle: 探索
title: 探索 Docker 安全加固镜像
description: 了解 Docker 安全加固镜像的用途、构建和测试方式，以及安全方面的共同责任模型。
weight: 10
params:
  grid_about:
    - title: 什么是安全加固镜像以及为什么要使用它们？
      description: 了解什么是安全加固镜像、Docker 安全加固镜像的构建方式、它们与普通基础镜像和应用镜像的区别，以及为什么要使用它们。
      icon: information-circle
      link: /dhi/explore/what/
    - title: 构建流程
      description: 了解 Docker 如何通过自动化、以安全为中心的流水线构建、测试和维护 Docker 安全加固镜像。
      icon: wrench-screwdriver
      link: /dhi/explore/build-process/
    - title: 镜像类型
      description: 了解 Docker 安全加固镜像目录中提供的不同镜像类型、发行版和变体。
      icon: squares-2x2
      link: /dhi/explore/available/
    - title: 扫描器集成
      description: 了解哪些漏洞扫描器与 Docker 安全加固镜像集成，并支持 OpenVEX 等开放标准。
      icon: shield-check
      link: /dhi/explore/scanner-integrations/
    - title: 镜像测试
      description: 了解 Docker 安全加固镜像如何自动进行标准合规性、功能性和安全性测试。
      icon: beaker
      link: /dhi/explore/test/
    - title: 恶意软件扫描
      description: 了解 Docker 如何对 Docker 安全加固镜像进行病毒和恶意软件扫描，以及如何查看和验证扫描证明。
      icon: bug-ant
      link: /dhi/explore/malware-scanning/
    - title: 责任概览
      description: 了解在使用 Docker 安全加固镜像作为安全软件供应链的一部分时，Docker 的角色以及您的责任。
      icon: user-group
      link: /dhi/explore/responsibility/
    - title: 安全概念
      description: 了解 Docker 安全加固镜像背后的核心概念 —— 签名证明、不可变摘要、SLSA、VEX 等。
      icon: clipboard-document-check
      link: /dhi/explore/security-concepts/

aliases:
  - /dhi/about/
---

Docker 安全加固镜像（DHI）是由 Docker 维护的最小化、安全且可用于生产的容器基础镜像和应用镜像。DHI 旨在减少漏洞并简化合规性，可以轻松集成到您现有的基于 Docker 的工作流中，几乎无需重新配置。

本节帮助您了解 Docker 安全加固镜像是什么、它们的构建和测试方式、可用的不同类型，以及 Docker 与您作为用户之间的责任分担。

## 进一步了解 Docker 安全加固镜像

{{< grid
  items="grid_about"
>}}
