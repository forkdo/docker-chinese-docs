---
title: 操作指南
description: 提供从发现到调试 Docker Hardened Images 的分步指导。
weight: 20
params:
  grid_discover:
    - title: 探索 Docker Hardened Images
      description: 了解如何在 Docker Hub 上的 DHI 目录中查找和评估镜像仓库、变体、元数据和认证。
      icon: travel_explore
      link: /dhi/how-to/explore/
  grid_adopt:
    - title: 镜像 Docker Hardened Image 仓库
      description: 了解如何将镜像同步到组织的命名空间，并可选择将其推送到另一个私有仓库。
      icon: compare_arrows
      link: /dhi/how-to/mirror/
    - title: 自定义 Docker Hardened Image 或 chart
      description: 了解如何自定义 Docker Hardened Images 和 charts。
      icon: settings
      link: /dhi/how-to/customize/
    - title: 使用 Docker Hardened Image
      description: 了解如何在 Dockerfiles、CI 流水线和标准开发工作流中拉取、运行和引用 Docker Hardened Images。
      icon: play_arrow
      link: /dhi/how-to/use/
    - title: 在 Kubernetes 中使用 Docker Hardened Image
      description: 了解如何在 Kubernetes 部署中使用 Docker Hardened Images。
      icon: play_arrow
      link: /dhi/how-to/k8s/
    - title: 使用 Docker Hardened Image chart
      description: 了解如何使用 Docker Hardened Image chart。
      icon: leaderboard
      link: /dhi/how-to/helm/
    - title: 为 Docker Hardened Images 使用扩展生命周期支持
      description: 了解如何为 Docker Hardened Images 使用扩展生命周期支持。
      icon: update
      link: /dhi/how-to/els/
    - title: 管理 Docker Hardened Images 和 charts
      description: 了解如何在组织中管理已同步和自定义的 Docker Hardened Images。
      icon: reorder
      link: /dhi/how-to/manage/
  grid_evaluate:
    - title: 比较 Docker Hardened Images
      description: 了解如何比较 Docker Hardened Images 与其他容器镜像，以评估安全改进和差异。
      icon: compare
      link: /dhi/how-to/compare/
  grid_verify:
    - title: 验证 Docker Hardened Image 或 chart
      description: 使用 Docker Scout 或 cosign 验证 Docker Hardened Images 和 charts 的签名认证，如 SBOM、来源和漏洞数据。
      icon: check_circle
      link: /dhi/how-to/verify/
    - title: 扫描 Docker Hardened Images
      description: 了解如何使用 Docker Scout、Grype 或 Trivy 扫描 Docker Hardened Images 中的已知漏洞。
      icon: bug_report
      link: /dhi/how-to/scan/
  grid_govern:
    - title: 使用策略强制执行 Docker Hardened Image 使用
      description: 了解如何为 Docker Hardened Images 使用 Docker Scout 的镜像策略。
      icon: policy
      link: /dhi/how-to/policies/
  grid_troubleshoot:
    - title: 调试 Docker Hardened Image
      description: 使用 Docker Debug 检查基于加固镜像运行的容器，而无需修改镜像。
      icon: terminal
      link: /dhi/how-to/debug/
---

本节提供使用 Docker Hardened Images (DHIs) 的实用、基于任务的指导。无论您是首次评估 DHIs 还是将其集成到生产 CI/CD 流水线中，这些主题涵盖了从发现到调试的整个采用过程中的关键任务。

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

## 评估

与其他镜像进行比较，以了解安全改进。

{{< grid
  items="grid_evaluate"
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

调试基于 DHIs 的容器，而无需修改镜像。

{{< grid
  items="grid_troubleshoot"
>}}