---
title: 核心概念
url: /dhi/core-concepts/
parent:
  title: Docker Hardened Images
  url: /dhi/
breadcrumbs:
  - title: 手册
    url: /manuals/
  - title: Docker Hardened Images
    url: /dhi/
  - title: 核心概念
    url: /dhi/core-concepts/
children:
  - title: CIS 基准
    url: /dhi/core-concepts/cis/
    description: 了解 Docker Hardened Images 如何符合 CIS Docker 基准，帮助组织加固容器镜像以实现安全部署。
  - title: 常见漏洞和暴露 (CVE)
    url: /dhi/core-concepts/cves/
    description: 了解什么是 CVE、Docker Hardened Images 如何减少暴露，以及如何使用常用工具扫描镜像漏洞。
  - title: FIPS <span class="not-prose bg-blue-500 dark:bg-blue-400 rounded-sm px-1 text-xs text-white whitespace-nowrap">DHI Enterprise</span>
    url: /dhi/core-concepts/fips/
    description: 了解 Docker Hardened Images 如何通过经验证的加密模块支持 FIPS 140，以帮助组织满足合规要求。
  - title: Docker Hardened Images 中的 glibc 和 musl 支持
    url: /dhi/core-concepts/glibc-musl/
    description: 比较 DHI 的 glibc 和 musl 变体，根据应用的兼容性、大小和性能需求选择合适的镜像。
  - title: 软件物料清单 (SBOM)
    url: /dhi/core-concepts/sbom/
    description: 了解什么是 SBOM、它们为何重要，以及 Docker Hardened Images 如何包含签名的 SBOM 以支持透明度和合规性。
  - title: 软件制品供应链安全等级 (SLSA)
    url: /dhi/core-concepts/slsa/
    description: 了解 Docker 强化镜像如何符合 SLSA 构建等级 3，以及如何验证来源以实现安全、防篡改的构建。
  - title: 安全软件开发生命周期
    url: /dhi/core-concepts/ssdlc/
    description: 了解 Docker Hardened Images 如何通过与扫描、签名和调试工具集成来支持安全的 SDLC。
  - title: STIG <span class="not-prose bg-blue-500 dark:bg-blue-400 rounded-sm px-1 text-xs text-white whitespace-nowrap">DHI Enterprise</span>
    url: /dhi/core-concepts/stig/
    description: 了解 Docker Hardened Images 如何提供支持 STIG 的容器镜像，并附带可验证的安全扫描证明，以满足政府和企业的合规要求。
  - title: 漏洞可利用性交换 (VEX)
    url: /dhi/core-concepts/vex/
    description: 了解 VEX 如何通过识别 Docker Hardened Images 中哪些漏洞实际可被利用，帮助您优先处理真实风险。
  - title: 不可变基础设施
    url: /dhi/core-concepts/immutability/
    description: 了解如何通过镜像摘要、只读容器和签名元数据来确保 Docker Hardened Images 具备防篡改和不可变特性。
  - title: 代码签名
    url: /dhi/core-concepts/signatures/
    description: 了解如何使用 Cosign 对 Docker Hardened Images 进行加密签名，以验证真实性、完整性和安全来源。
  - title: 基础镜像加固
    url: /dhi/core-concepts/hardening/
    description: 了解 Docker Hardened Images 如何通过精简组件、非 root 执行和默认安全配置来保障安全性。
  - title: 极简或无发行版镜像
    url: /dhi/core-concepts/distroless/
    description: 了解 Docker Hardened Images 如何使用无发行版变体来最小化攻击面并移除不必要的组件。
  - title: 证明
    url: /dhi/core-concepts/attestations/
    description: 查看每个 Docker Hardened Image 附带的完整签名证明，例如 SBOM、VEX、构建来源和扫描结果。
  - title: 软件供应链安全
    url: /dhi/core-concepts/sscs/
    description: 了解 Docker 加固镜像如何通过签名元数据、来源证明和最小化攻击面，帮助您保护软件供应链的每个阶段。
  - title: 镜像摘要
    url: /dhi/core-concepts/digests/
    description: 了解 Docker Hardened Images 如何通过签名元数据、来源证明和最小攻击面，保障软件供应链每个阶段的安全。
  - title: 镜像溯源
    url: /dhi/core-concepts/provenance/
    description: 了解构建溯源元数据如何帮助追踪 Docker Hardened Images 的来源，并支持符合 SLSA 规范。
---


Docker Hardened Images（DHIs）建立在安全的软件供应链实践基础之上。本节解释了这些基础背后的核心概念，从签名认证和不可变摘要到 SLSA 和 VEX 等标准。

如果您想了解 Docker Hardened Images 如何支持合规性、透明性和安全性，请从这里开始。


## 安全元数据和认证



## 合规性标准



## 漏洞和风险管理



## 镜像结构和行为



## 验证和可追溯性


