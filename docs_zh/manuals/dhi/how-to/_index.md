---
title: 操作指南
description: 从发现到调试，逐步指导如何使用 Docker Hardened Images。
weight: 20
params:
  grid_discover:
    - title: 探索 Docker Hardened Images
      description: 了解如何在 Docker Hub 的 DHI 目录中查找和评估镜像仓库、变体、元数据和证明。
      icon: travel_explore
      link: /dhi/how-to/explore/
  grid_adopt:
    - title: 镜像 Docker Hardened Image 仓库
      description: 了解如何将镜像镜像到组织的命名空间中，并可选择推送到另一个私有注册表。
      icon: compare_arrows
      link: /dhi/how-to/mirror/
    - title: 自定义 Docker Hardened Image 或图表
      description: 了解如何自定义 Docker Hardened Images 和图表。
      icon: settings
      link: /dhi/how-to/customize/
    - title: 使用 Docker Hardened Image
      description: 了解如何在 Dockerfile、CI 管道和标准开发工作流中拉取、运行和引用 Docker Hardened Images。
      icon: play_arrow
      link: /dhi/how-to/use/
    - title: 在 Kubernetes 中使用 Docker Hardened Image
      description: 了解如何在 Kubernetes 部署中使用 Docker Hardened Images。
      icon: play_arrow
      link: /dhi/how-to/k8s/
    - title: 使用 Docker Hardened Image 图表
      description: 了解如何使用 Docker Hardened Image 图表。
      icon: leaderboard
      link: /dhi/how-to/helm/
    - title: 使用 Docker Hardened Images 的扩展生命周期支持
      description: 了解如何在 Docker Hardened Images 上使用扩展生命周期支持。
      icon: update
      link: /dhi/how-to/els/
    - title: 管理 Docker Hardened Images 和图表
      description: 了解如何在组织中管理镜像和自定义的 Docker Hardened Images。
      icon: reorder
      link: /dhi/how-to/manage/
  grid_evaluate:
    - title: 比较 Docker Hardened Images
      description: 了解如何将 Docker Hardened Images 与其他容器镜像进行比较，以评估安全改进和差异。
      icon: compare
      link: /dhi/how-to/compare/
  grid_verify:
    - title: 验证 Docker Hardened Image 或图表
      description: 使用 Docker Scout 或 cosign 验证 Docker Hardened Images 和图表的签名证明，如 SBOM、来源和漏洞数据。
      icon: check_circle
      link: /dhi/how-to/verify/
    - title: 扫描 Docker Hardened Images
      description: 了解如何使用 Docker Scout、Grype 或 Trivy 扫描 Docker Hardened Images 中的已知漏洞。
      icon: bug_report
      link: /dhi/how-to/scan/
  grid_govern:
    - title: 使用策略强制使用 Docker Hardened Images
      description: 了解如何在 Docker Hardened Images 上使用 Docker Scout 的镜像策略。
      icon: policy
      link: /dhi/how-to/policies/
  grid_troubleshoot:
    - title: 调试 Docker Hardened Image
      description: 使用 Docker Debug 检查基于强化镜像的运行中容器，无需修改它。
      icon: terminal
      link: /dhi/how-to/debug/
---

本节提供实用的、基于任务的 Docker Hardened Images (DHI) 使用指导。无论您是首次评估 DHI，还是将其集成到生产 CI/CD 管道中，这些主题都涵盖了采用过程中从发现到调试的关键任务。

主题围绕使用 DHI 的典型生命周期组织，但您可以根据特定工作流按需使用。

探索以下符合您当前需求的主题。

## 发现

在 DHI 目录中探索可用的镜像和元数据。

{{< grid
  items="grid_discover"
>}}

## 采用

镜像受信任的镜像，按需自定义，并集成到您的工作流中。

{{< grid
  items="grid_adopt"
>}}

## 评估

与其他镜像比较，了解安全改进。

{{< grid
  items="grid_evaluate"
>}}

## 验证

检查签名、SBOM 和来源，并扫描漏洞。

{{< grid
  items="grid_verify"
>}}

## 治理

使用策略维护安全和合规。

{{< grid
  items="grid_govern"
>}}

## 故障排除

调试基于 DHI 的容器，无需修改镜像。

{{< grid
  items="grid_troubleshoot"
>}}