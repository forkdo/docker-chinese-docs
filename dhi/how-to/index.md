---
title: 操作指南
url: /dhi/how-to/
parent:
  title: Docker Hardened Images
  url: /dhi/
breadcrumbs:
  - title: 手册
    url: /manuals/
  - title: Docker Hardened Images
    url: /dhi/
  - title: 操作指南
    url: /dhi/how-to/
children:
  - title: 探索 Docker 硬化镜像
    url: /dhi/how-to/explore/
    description: 了解如何在 Docker Hub 上的 DHI 目录中查找和评估镜像仓库、变体、元数据和证明。
  - title: 镜像 Docker Hardened Image 仓库 <span class="not-prose bg-blue-500 dark:bg-blue-400 rounded-sm px-1 text-xs text-white whitespace-nowrap">DHI Enterprise</span>
    url: /dhi/how-to/mirror/
    description: 了解如何将镜像镜像到您组织的命名空间，并可选择将其推送到另一个私有注册中心。
  - title: 自定义 Docker 加固镜像或 Helm chart <span class="not-prose bg-blue-500 dark:bg-blue-400 rounded-sm px-1 text-xs text-white whitespace-nowrap">DHI Enterprise</span>
    url: /dhi/how-to/customize/
    description: 了解如何自定义 Docker 加固镜像（DHI）和 Helm chart。
  - title: 使用 Docker Hardened Image
    url: /dhi/how-to/use/
    description: 了解如何在 Dockerfile、CI 流程和标准开发工作流中拉取、运行和引用 Docker Hardened Image。
  - title: 在 Kubernetes 中使用 Docker Hardened 镜像
    url: /dhi/how-to/k8s/
    description: 了解如何在 Kubernetes 部署中使用 Docker Hardened Images。
  - title: 使用 Docker 加固镜像（DHI）Helm chart
    url: /dhi/how-to/helm/
    description: 了解如何使用 Docker 加固镜像（DHI）Helm chart。
  - title: 管理 Docker Hardened Images 和 charts <span class="not-prose bg-blue-500 dark:bg-blue-400 rounded-sm px-1 text-xs text-white whitespace-nowrap">DHI Enterprise</span>
    url: /dhi/how-to/manage/
    description: 了解如何在您的组织中管理已镜像和自定义的 Docker Hardened Images。
  - title: 使用 Docker Hardened Images 的扩展生命周期支持 <span class="not-prose bg-blue-500 dark:bg-blue-400 rounded-sm px-1 text-xs text-white whitespace-nowrap">DHI Enterprise</span>
    url: /dhi/how-to/els/
    description: 了解如何将扩展生命周期支持与 Docker Hardened Images 结合使用。
  - title: 对比 Docker Hardened 镜像
    url: /dhi/how-to/compare/
    description: 了解如何对比 Docker Hardened 镜像与其他容器镜像，以评估安全性改进和差异。
  - title: 验证 Docker Hardened 镜像或图表
    url: /dhi/how-to/verify/
    description: 使用 Docker Scout 或 cosign 验证 Docker Hardened 镜像和图表的签名证明，如 SBOM、来源和漏洞数据。
  - title: 扫描 Docker Hardened Images
    url: /dhi/how-to/scan/
    description: 了解如何使用 Docker Scout、Grype 或 Trivy 扫描 Docker Hardened Images 的已知漏洞。
  - title: 使用策略强制执行 Docker Hardened Image 用法
    url: /dhi/how-to/policies/
    description: 了解如何将镜像策略与 Docker Scout 结合使用，以管理 Docker Hardened Images。
  - title: 调试 Docker Hardened Image 容器
    url: /dhi/how-to/debug/
    description: 了解如何使用 Docker Debug 在本地或生产环境中对 Docker Hardened Images (DHI) 进行故障排除。
---


本节提供使用 Docker Hardened Images (DHIs) 的实用、基于任务的指导。无论您是首次评估 DHIs 还是将其集成到生产 CI/CD 流水线中，这些主题涵盖了从发现到调试的整个采用过程中的关键任务。

这些主题围绕使用 DHIs 的典型生命周期组织，但您可以根据特定的工作流按需使用它们。

探索下面符合您当前需求的主题。

## 发现

探索 DHI 目录中可用的镜像和元数据。



## 采用

同步受信任的镜像，根据需要进行自定义，并将其集成到您的工作流中。



## 评估

与其他镜像进行比较，以了解安全改进。



## 验证

检查签名、SBOM 和来源，并扫描漏洞。



## 治理

执行策略以保持安全性和合规性。



## 故障排除

调试基于 DHIs 的容器，而无需修改镜像。


