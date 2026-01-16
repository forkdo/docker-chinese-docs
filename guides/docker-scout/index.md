---
title: 使用 Docker Scout 保障您的软件供应链安全
url: /guides/docker-scout/
parent:
  title: Docker 指南
  url: /guides/
breadcrumbs:
  - title: Docker 指南
    url: /guides/
  - title: 使用 Docker Scout 保障您的软件供应链安全
    url: /guides/docker-scout/
children:
  - title: 为什么选择 Docker Scout？
    url: /guides/docker-scout/why/
    description: 了解 Docker Scout 如何帮助您保障供应链安全。
  - title: Docker Scout demo
    url: /guides/docker-scout/demo/
    description: 了解 Docker Scout 用于增强供应链安全的强大功能。
  - title: 软件供应链安全
    url: /guides/docker-scout/s3c/
    description: 了解软件供应链安全（S3C）、其含义及其重要性。
  - title: 软件物料清单
    url: /guides/docker-scout/sbom/
    description: 了解软件物料清单（SBOM）以及 Docker Scout 如何使用它。
  - title: 证明
    url: /guides/docker-scout/attestations/
    description: 介绍 Docker Build 中的 SBOM 和来源证明，
它们是什么以及为何存在

  - title: 修复
    url: /guides/docker-scout/remediation/
    description: 了解 Docker Scout 如何通过修复功能自动帮助您提升软件质量
  - title: 常见挑战与问题
    url: /guides/docker-scout/common-questions/
    description: 探索与 Docker Scout 相关的常见挑战与问题。
---


当容器镜像存在安全隐患时，可能会产生重大风险。约 60% 的组织报告称在一年内至少经历过一次安全漏洞或漏洞事件，[导致业务中断][CSA]。这些事件通常会导致相当长的停机时间，44% 的受影响公司每次事件的停机时间超过一小时。财务影响巨大，[数据泄露的平均成本达到 445 万美元][IBM]。这突显了保持强大容器安全措施的至关重要性。

Docker Scout 通过提供自动化漏洞检测和修复、解决不安全的容器镜像以及确保符合安全标准来增强容器安全性。

[CSA]: https://cloudsecurityalliance.org/blog/2023/09/21/2023-global-cloud-threat-report-cloud-attacks-are-lightning-fast
[IBM]: https://www.ibm.com/reports/data-breach

## 您将学习的内容

- 定义安全软件供应链 (SSSC)
- 了解 SBOM 及其使用方法
- 检测和监控漏洞

## 工具集成

与 Docker Desktop、GitHub Actions、Jenkins、Kubernetes 和其他 CI 解决方案配合良好。

## 适用对象

- 需要将自动化安全检查集成到 CI/CD 管道中以增强工作流安全性和效率的 DevOps 工程师。
- 希望使用 Docker Scout 在开发过程早期识别和修复漏洞，确保生产安全容器镜像的开发人员。
- 必须强制执行安全合规性、进行漏洞评估并确保容器化应用程序整体安全性的安全专业人员。

<div id="scout-lp-survey-anchor"></div>
