---
title: Docker Hardened Images 功能
linktitle: 功能
description: Docker Hardened Images 为每个应用提供完全透明、最小攻击面和企业级安全——免费且开源。
weight: 5
aliases:
  - /dhi/features/secure/
  - /dhi/features/integration/
  - /dhi/features/support/
  - /dhi/features/patching/
  - /dhi/features/flexible/
  - /dhi/features/helm/
---

Docker Hardened Images (DHI) 是由 Docker 维护的、最小的、安全的、可用于生产环境的容器基础镜像和应用镜像。DHI 旨在减少漏洞并简化合规性，可轻松集成到您现有的基于 Docker 的工作流中，几乎或完全无需重新配置。

DHI 为每个人提供安全保障：

- [DHI Free](#dhi-free-features) 为所有人提供核心安全功能，在 Apache 2.0 许可下无任何许可限制。
- [DHI Enterprise 订阅功能](#dhi-enterprise-subscription-features) 增加了
  SLA 支持的安全更新、合规性变体（如 FIPS 和 STIG）、镜像定制，以及可选的扩展生命周期支持 (ELS)，以覆盖 EOL 后的周期。

## DHI Free 免费功能

DHI 的核心功能是开放和免费的，可供任何人使用、共享和构建，无任何许可限制，并由 Apache 2.0 许可证提供支持。

### 默认安全

- 近乎零个 CVE：持续扫描和修补以保持最少的已知可利用漏洞，对于非 DHI Enterprise 用户，不提供基于 SLA 的时间承诺。
- 最小攻击面：Distroless 变体通过移除不必要的组件，将攻击面减少高达 95%。
- 非 root 执行：默认以非 root 身份运行，遵循最小权限原则。
- 透明的漏洞报告：每个 CVE 都使用公开数据可见和评估——没有隐藏的源或专有评分。

### 完全透明

每个镜像都包含完整的、可验证的安全元数据：

- SLSA 构建等级 3 来源证明：可验证的、防篡改的构建，满足供应链安全标准。
- 已签名的 SBOM：为每个组件提供完整的软件物料清单。
- VEX 声明：漏洞可利用性交换文档，提供有关已知 CVE 的背景信息。
- 加密签名：所有镜像和元数据都经过签名以确保真实性。

### 为开发者而构建

- 熟悉的基础：基于 Alpine 和 Debian 构建，采用时只需最少的更改。
- glibc 和 musl 支持：提供两种变体以确保广泛的应用兼容性。
- 开发和运行时变体：使用 dev 镜像进行构建，使用最小的运行时镜像用于生产。
- 无缝兼容：与现有的 Docker 工作流、CI/CD 流水线和工具无缝协作。

### 持续维护

- 自动修补：当上游安全补丁可用时，镜像会被重建和更新，对于非 DHI Enterprise 用户，不提供基于 SLA 的时间承诺。
- 扫描器集成：与扫描器和其他安全平台直接集成。

### Kubernetes 和 Helm chart 支持

Docker Hardened Image (DHI) chart 是由 Docker 提供的、从上游源构建的 Helm chart，旨在与 Docker Hardened Images 兼容。这些 chart 作为 OCI 制品在 Docker Hub 上的 DHI 目录中提供。DHI chart 在构建后会经过严格测试，以确保它们能与 Docker Hardened Images 开箱即用。这减少了迁移的阻力，并降低了开发者实施 chart 的工作量，确保了无缝的兼容性。

与加固镜像一样，DHI chart 融合了多层安全元数据以确保透明度和信任：

- SLSA 等级 3 合规性：每个 chart 都使用 Docker 的 SLSA 构建等级 3 系统构建，包括详细的构建来源证明，并满足软件制品供应链等级 (SLSA) 框架设定的标准。
- 软件物料清单 (SBOM)：提供全面的 SBOM，详细说明 chart 中引用的所有组件，以促进漏洞管理和合规审计。
- 加密签名：所有相关元数据都由 Docker 进行加密签名，确保完整性和真实性。
- 加固配置：Chart 自动引用 Docker 加固镜像，确保部署的安全性。

## DHI Enterprise 订阅功能

对于有严格安全要求、合规性需求或运营需求的组织，DHI Enterprise 提供了额外的功能。

### 合规性变体 {tier="DHI Enterprise"}

- 启用 FIPS 的镜像：适用于受监管的行业和政府系统。
- 满足 STIG 要求的镜像：满足 DoD 安全技术实施指南的要求。

### SLA 支持的安全 {tier="DHI Enterprise"}

- CVE 修复 SLA：针对严重和高危漏洞的 7 天 SLA，并为其他严重性级别提供 SLA 承诺。
- ELS CVE 修复 SLA：扩展生命周期支持镜像对 CVE 修复有 SLA 承诺，即使在上游 EOL 之后也是如此。
- 企业支持：可访问 Docker 的支持团队，以获得关键任务应用的支持。

### 定制与控制 {tier="DHI Enterprise"}

- 构建自定义镜像：添加您自己的包、工具、证书和配置。
- 安全的构建基础设施：在 Docker 的可信基础设施上构建定制项。
- 完整的信任链：自定义镜像保持来源证明和加密签名。
- 自动更新：当基础镜像被打补丁时，自定义镜像会自动重建。

### 扩展生命周期支持 {tier="DHI Enterprise add-on"}

- EOL 后的安全覆盖：在上游支持结束后继续多年接收补丁。
- 持续合规：提供更新的 SBOM、来源证明和签名，以满足审计要求。
- 生产连续性：在生产环境中安全运行，无需强制迁移。

## 了解更多

- [了解 DHI 镜像的构建方式及更多信息](/dhi/explore/)
- [开始使用 DHI](/dhi/get-started/)
- [联系 Docker 了解 DHI Enterprise](https://www.docker.com/pricing/contact-sales/)