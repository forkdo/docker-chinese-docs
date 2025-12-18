---
title: 核心概念
description: 了解 Docker Hardened Images 的核心概念，包括安全元数据、漏洞管理、镜像结构和验证。
weight: 30
params:
  grid_concepts_metadata:
    - title: 证明（Attestations）
      description: 查看每个 Docker Hardened Image 包含的完整签名证明，例如 SBOM、VEX、构建来源和扫描结果。
      icon: assignment
      link: /dhi/core-concepts/attestations/
    - title: 软件物料清单（SBOMs）
      description: 了解什么是 SBOM，为什么它们很重要，以及 Docker Hardened Images 如何包含签名的 SBOM 以支持透明度和合规性。
      icon: list_alt
      link: /dhi/core-concepts/sbom/
    - title: 软件工件供应链级别（SLSA）
      description: 了解 Docker Hardened Images 如何符合 SLSA Build Level 3，以及如何验证来源以实现安全、防篡改的构建。
      icon: fact_check
      link: /dhi/core-concepts/slsa/
    - title: 镜像来源（Image provenance）
      description: 了解构建来源元数据如何帮助追溯 Docker Hardened Images 的来源，并支持符合 SLSA 标准。
      icon: track_changes
      link: /dhi/core-concepts/provenance/

  grid_concepts_compliance:
    - title: FIPS
      description: 了解 Docker Hardened Images 如何通过使用经过验证的加密模块并为合规性审计提供签名证明来支持 FIPS 140。
      icon: verified
      link: /dhi/core-concepts/fips/
    - title: STIG
      description: 了解 Docker Hardened Images 如何为政府和企业合规需求提供 STIG 就绪的容器镜像，并提供可验证的安全扫描证明。
      icon: policy
      link: /dhi/core-concepts/stig/
    - title: CIS 基准（CIS Benchmarks）
      description: 了解 Docker Hardened Images 如何帮助您满足互联网安全中心（CIS）Docker 基准要求，实现安全的容器配置和部署。
      icon: check_circle
      link: /dhi/core-concepts/cis/

  grid_concepts_risk:
    - title: 通用漏洞和暴露（CVEs）
      description: 了解什么是 CVE，Docker Hardened Images 如何减少暴露，以及如何使用流行工具扫描镜像中的漏洞。
      icon: error
      link: /dhi/core-concepts/cves/
    - title: 漏洞可利用性交换（VEX）
      description: 了解 VEX 如何通过识别 Docker Hardened Images 中哪些漏洞真正可利用来帮助您优先处理真实风险。
      icon: warning
      link: /dhi/core-concepts/vex/
    - title: 软件供应链安全
      description: 了解 Docker Hardened Images 如何通过签名元数据、来源和最小攻击面保护软件供应链的每个阶段。
      icon: shield
      link: /dhi/core-concepts/sscs/
    - title: 安全软件开发生命周期（SSDLC）
      description: 了解 Docker Hardened Images 如何通过集成扫描、签名和调试工具来支持安全的 SDLC。
      icon: build_circle
      link: /dhi/core-concepts/ssdlc/

  grid_concepts_structure:
    - title: 无发行版镜像（Distroless images）
      description: 了解 Docker Hardened Images 如何使用无发行版变体来最小化攻击面并移除不必要的组件。
      icon: layers_clear
      link: /dhi/core-concepts/distroless/
    - title: Docker Hardened Images 中的 glibc 和 musl 支持
      description: 比较 DHIs 的 glibc 和 musl 变体，为您的应用程序选择合适的基镜像，满足兼容性、大小和性能需求。
      icon: swap_vert
      link: /dhi/core-concepts/glibc-musl/
    - title: 镜像不可变性
      description: 了解镜像摘要、只读容器和签名元数据如何确保 Docker Hardened Images 具有防篡改和不可变性。
      icon: do_not_disturb_on
      link: /dhi/core-concepts/immutability/
    - title: 镜像加固
      description: 了解 Docker Hardened Images 如何通过最小化组件、非 root 执行和默认安全配置来实现安全性设计。
      icon: security
      link: /dhi/core-concepts/hardening/

  grid_concepts_verification:
    - title: 摘要（Digests）
      description: 了解如何使用不可变的镜像摘要来保证一致性，并验证您正在运行的确切 Docker Hardened Image。
      icon: fingerprint
      link: /dhi/core-concepts/digests/
    - title: 代码签名
      description: 了解 Docker Hardened Images 如何使用 Cosign 进行加密签名，以验证真实性、完整性和安全来源。
      icon: key
      link: /dhi/core-concepts/signatures/
---

Docker Hardened Images (DHIs) 基于安全软件供应链实践构建。本节解释了这些实践的核心概念，从签名证明和不可变摘要到 SLSA 和 VEX 等标准。

如果您想了解 Docker Hardened Images 如何支持合规性、透明度和安全性，请从这里开始。


## 安全元数据和证明

{{< grid items="grid_concepts_metadata" >}}

## 合规标准

{{< grid items="grid_concepts_compliance" >}}

## 漏洞和风险管理

{{< grid items="grid_concepts_risk" >}}

## 镜像结构和行为

{{< grid items="grid_concepts_structure" >}}

## 验证和可追溯性

{{< grid items="grid_concepts_verification" >}}