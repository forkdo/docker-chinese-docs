---
title: 操作指南
description: 提供从发现到治理 Docker Hardened Images 的分步指导。
weight: 20
aliases:
  - /dhi/how-to/manage/
params:
  grid_discover:
  - title: 搜索和评估 Docker Hardened Images
    description: 了解如何在 DHI 目录中查找和比较镜像仓库、变体和元数据。
    icon: globe-alt
    link: /dhi/how-to/search-evaluate/
  grid_adopt:
  - title: 开始使用 DHI Select 和 Enterprise
    description: 了解如何使用 DHI Select 和 Enterprise 订阅镜像仓库、自定义镜像并访问合规变体。
    icon: rocket-launch
    link: /dhi/how-to/select-enterprise/
  - title: 镜像 Docker Hardened Image 仓库
    description: 了解如何将镜像同步到组织的命名空间，并可选择将其推送到另一个私有仓库。
    icon: arrows-right-left
    link: /dhi/how-to/mirror/
  - title: 自定义 Docker Hardened Image 或 chart
    description: 了解如何自定义 Docker Hardened Images 和 charts。
    icon: cog-6-tooth
    link: /dhi/how-to/customize/
  - title: 使用 Docker 的加固系统包
    description: 了解如何在镜像中使用 Docker 的加固系统包。
    icon: archive-box
    link: /dhi/how-to/hardened-packages/
  - title: 使用 Docker Hardened Image
    description: 了解如何在 Dockerfiles、CI 流水线和标准开发工作流中拉取、运行和引用 Docker Hardened Images。
    icon: play
    link: /dhi/how-to/use/
  - title: 使用 Docker Hardened Image chart
    description: 了解如何使用 Docker Hardened Image chart。
    icon: chart-bar
    link: /dhi/how-to/helm/
  grid_verify:
  - title: 验证 Docker Hardened Image 或 chart
    description: 使用 Docker Scout 或 cosign 验证 Docker Hardened Images 和 charts 的签名认证，如 SBOM、来源和漏洞数据。
    icon: check-circle
    link: /dhi/how-to/verify/
  - title: 扫描 Docker Hardened Images
    description: 了解如何使用 Docker Scout、Grype 或 Trivy 扫描 Docker Hardened Images 中的已知漏洞。
    icon: bug-ant
    link: /dhi/how-to/scan/
  grid_govern:
  - title: 为您的镜像应用 Docker Hardened Image 策略
    description: 了解如何使用 Docker Scout CLI 让您自己的镜像符合 Docker Hardened Image 的安全和合规标准。
    icon: shield-check
    link: /dhi/how-to/policies/
  grid_troubleshoot:
  - title: 故障排除
    description: 解决构建、运行或调试 Docker Hardened Images 时的常见问题，例如非 root 行为、缺少 shell 和端口访问。
    icon: question-mark-circle
    link: /dhi/how-to/troubleshoot/
---

本节提供使用 Docker Hardened Images (DHIs) 的实用、基于任务的指导。无论您是首次评估 DHIs 还是将其集成到生产 CI/CD 流水线中，这些主题涵盖了从发现到治理整个采用过程中的关键任务：

发现、采用、验证和治理。

这些主题围绕使用 DHIs 的典型生命周期组织，但您可以根据特定的工作流按需使用它们。

探索下面符合您当前需求的主题。

## 发现

探索 DHI 目录中可用的镜像和元数据。

{{< grid
  items="grid_discover"
>}}

## 采用

同步受信任的镜像，根据需要进行自定义，并将其集成到您的工作流中。

{{< grid
  items="grid_adopt"
>}}

## 验证

检查签名、SBOM 和来源，并扫描漏洞。

{{< grid
  items="grid_verify"
>}}

## 治理

执行策略以保持安全性和合规性。

{{< grid
  items="grid_govern"
>}}

## 故障排除

{{< grid
  items="grid_troubleshoot"
>}}
