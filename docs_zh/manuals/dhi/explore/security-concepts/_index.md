---
aliases:
  - /dhi/core-concepts/
title: Security concepts（安全概念）
linkTitle: Security concepts（安全概念）
description: 了解 Docker Hardened Images 背后的核心概念，包括安全元数据、漏洞管理、镜像结构和验证。
weight: 60
params:
  grid_concepts_metadata:
    - title: Attestations（证明）
      description: 查看每个 Docker Hardened Image 附带的一整套已签名证明，例如 SBOM、VEX、构建来源和扫描结果。
      icon: clipboard-document-list
      link: /dhi/explore/security-concepts/attestations/
    - title: Software Bill of Materials (SBOMs)（软件物料清单）
      description: 了解什么是 SBOM、为何重要，以及 Docker Hardened Images 如何包含已签名的 SBOM 以支持透明度和合规性。
      icon: list-bullet
      link: /dhi/explore/security-concepts/sbom/
    - title: Supply-chain Levels for Software Artifacts (SLSA)（软件制品供应链级别）
      description: 了解 Docker Hardened Images 如何符合 SLSA Build Level 3，以及如何验证来源以实现安全的防篡改构建。
      icon: clipboard-document-check
      link: /dhi/explore/security-concepts/slsa/
    - title: Image provenance（镜像来源）
      description: 了解构建来源元数据如何帮助追溯 Docker Hardened Images 的来源，并支持符合 SLSA 标准。
      icon: pencil-square
      link: /dhi/explore/security-concepts/provenance/

  grid_concepts_compliance:
    - title: FIPS
      description: 了解 Docker Hardened Images 如何使用经过验证的加密模块支持 FIPS 140，并为合规审计提供已签名的证明。
      icon: check-badge
      link: /dhi/explore/security-concepts/fips/
    - title: STIG
      description: 了解 Docker Hardened Images 如何提供 STIG 就绪的容器镜像，并附带可验证的安全扫描证明，以满足政府和企业合规要求。
      icon: shield-check
      link: /dhi/explore/security-concepts/stig/
    - title: CIS Benchmarks（CIS 基准）
      description: 了解 Docker Hardened Images 如何帮助你满足互联网安全中心（CIS）Docker Benchmark 对安全容器配置和部署的要求。
      icon: check-circle
      link: /dhi/explore/security-concepts/cis/

  grid_concepts_risk:
    - title: Common Vulnerabilities and Exposures (CVEs)（常见漏洞与暴露）
      description: 了解什么是 CVE、Docker Hardened Images 如何减少暴露面，以及如何使用常用工具扫描镜像中的漏洞。
      icon: exclamation-circle
      link: /dhi/explore/security-concepts/cves/
    - title: Vulnerability Exploitability eXchange (VEX)（漏洞可利用性交换）
      description: 了解 VEX 如何帮助识别 Docker Hardened Images 中实际可利用的漏洞，从而优先处理真实风险。
      icon: exclamation-triangle
      link: /dhi/explore/security-concepts/vex/
    - title: Software Supply Chain Security（软件供应链安全）
      description: 了解 Docker Hardened Images 如何通过签名元数据、来源和最小攻击面来保护软件供应链的每个阶段。
      icon: shield-check
      link: /dhi/explore/security-concepts/sscs/
    - title: Secure Software Development Lifecycle (SSDLC)（安全软件开发生命周期）
      description: 了解 Docker Hardened Images 如何通过与扫描、签名和调试工具的集成来支持安全的 SDLC。
      icon: wrench-screwdriver
      link: /dhi/explore/security-concepts/ssdlc/

  grid_concepts_structure:
    - title: Distroless images（Distroless 镜像）
      description: 了解 Docker Hardened Images 如何使用 distroless 变体来最小化攻击面并移除不必要的组件。
      icon: squares-2x2
      link: /dhi/explore/security-concepts/distroless/
    - title: glibc and musl support in Docker Hardened Images（DHI 中的 glibc 与 musl 支持）
      description: 比较 DHI 的 glibc 和 musl 变体，为应用程序的兼容性、大小和性能需求选择正确的基础镜像。
      icon: arrows-up-down
      link: /dhi/explore/security-concepts/glibc-musl/
    - title: Image immutability（镜像不可变性）
      description: 了解镜像摘要、只读容器和签名元数据如何确保 Docker Hardened Images 具有防篡改和不可变性。
      icon: minus-circle
      link: /dhi/explore/security-concepts/immutability/
    - title: Image hardening（镜像加固）
      description: 了解 Docker Hardened Images 如何以安全为设计目标，具备最小组件、非 root 执行和默认安全配置。
      icon: shield-check
      link: /dhi/explore/security-concepts/hardening/

  grid_concepts_verification:
    - title: Digests（摘要）
      description: 了解如何使用不可变的镜像摘要来保证一致性并验证你正在运行的 Docker Hardened Image 的确切版本。
      icon: finger-print
      link: /dhi/explore/security-concepts/digests/
    - title: Code signing（代码签名）
      description: 了解 Docker Hardened Images 如何使用 Cosign 进行加密签名，以验证真实性、完整性和安全来源。
      icon: key
      link: /dhi/explore/security-concepts/signatures/
---

Docker Hardened Images（DHI）建立在安全的软件供应链实践基础之上。本节讲解该基础背后的核心概念，从已签名的证明和不可变的摘要到 SLSA 和 VEX 等标准。

如果你想了解 Docker Hardened Images 如何支持合规性、透明度和安全性，请从此处开始。


## Security metadata and attestations（安全元数据和证明）

{{< grid items="grid_concepts_metadata" >}}

## Compliance standards（合规标准）

{{< grid items="grid_concepts_compliance" >}}

## Vulnerability and risk management（漏洞与风险管理）

{{< grid items="grid_concepts_risk" >}}

## Image structure and behavior（镜像结构与行为）

{{< grid items="grid_concepts_structure" >}}

## Verification and traceability（验证与可追溯性）

{{< grid items="grid_concepts_verification" >}}
