---
title: Docker Hardened Images 功能特性
linktitle: 功能特性
description: Docker Hardened Images 提供完全透明、最小攻击面和企业级安全保护，适用于所有应用——免费且开源。
weight: 5
aliases:
  - /dhi/features/secure/
  - /dhi/features/integration/
  - /dhi/features/support/
  - /dhi/features/patching/
  - /dhi/features/flexible/
  - /dhi/features/helm/
---

Docker Hardened Images（DHI）是由 Docker 维护的最小化、安全且可直接用于生产的容器基础镜像和应用镜像。DHI 旨在减少漏洞并简化合规性，可轻松集成到您现有的基于 Docker 的工作流中，几乎无需重新配置工具。

DHI 为所有人提供安全保障：

- [DHI Free](#dhi-free-功能特性) 提供面向所有人的核心安全功能，无许可证限制，采用 Apache 2.0 许可证
- [DHI Enterprise 订阅功能](#dhi-enterprise-订阅功能特性) 增加了 SLA 支持的安全更新、合规变体（如 FIPS 和 STIG）、镜像定制，以及可选的扩展生命周期支持（ELS）以覆盖已结束生命周期的版本

## DHI Free 功能特性

DHI 的核心功能开放且免费使用，可自由共享和构建，无许可证意外，由 Apache 2.0 许可证提供保障。

### 默认安全

- 极低 CVE 数量：持续扫描并打补丁，以保持最少的已知可利用漏洞，对非 DHI Enterprise 用户不承诺 SLA 时间要求
- 最小攻击面：distroless 变体通过移除不必要的组件，将攻击面减少高达 95%
- 非 root 执行：默认以非 root 身份运行，遵循最小权限原则
- 透明漏洞报告：每个 CVE 均通过公开数据可见并评估——无屏蔽的 feed 或专有评分

### 完全透明

每个镜像包含完整、可验证的安全元数据：

- SLSA 3 级构建证明：可验证、防篡改的构建，符合供应链安全标准
- 已签名的 SBOM：每个组件的完整软件物料清单
- VEX 声明：漏洞可利用性交换（Vulnerability Exploitability eXchange）文档提供已知 CVE 的上下文信息
- 密码学签名：所有镜像和元数据均签名以确保真实性

### 为开发者构建

- 熟悉的基础：基于 Alpine 和 Debian 构建，采用时几乎无需更改
- glibc 和 musl 支持：提供两种变体以实现广泛的应用兼容性
- 开发和运行时变体：使用 dev 镜像进行构建，在生产环境中使用最小化运行时镜像
- 即插即用兼容性：与现有 Docker 工作流、CI/CD 管道和工具无缝协作

### 持续维护

- 自动打补丁：当上游安全补丁可用时自动重建和更新镜像，对非 DHI Enterprise 用户不承诺 SLA 时间要求
- 扫描器集成：与扫描器和其他安全平台直接集成

### Kubernetes 和 Helm chart 支持

Docker Hardened Image（DHI）charts 是 Docker 提供的 Helm charts，基于上游源代码构建，专为与 Docker Hardened Images 兼容而设计。这些 charts 作为 OCI 工件在 Docker Hub 上的 DHI 目录中提供。DHI charts 在构建后经过严格测试，确保与 Docker Hardened Images 即开即用。这消除了迁移中的摩擦，减少了开发者实施 charts 的工作量，确保无缝兼容性。

与加固镜像一样，DHI charts 也集成了多层安全元数据，以确保透明度和信任：

- SLSA 3 级合规性：每个 chart 均使用 Docker 的 SLSA 3 级构建系统构建，包含详细的构建证明，并符合软件工件供应链级别（SLSA）框架设定的标准
- 软件物料清单（SBOM）：提供全面的 SBOM，详细列出 chart 中引用的所有组件，便于漏洞管理和合规审计
- 密码学签名：所有相关元数据均由 Docker 进行密码学签名，确保完整性和真实性
- 加固配置：charts 自动引用 Docker 加固镜像，确保部署安全性

## DHI Enterprise 订阅功能特性

对于有严格安全要求、监管需求或运维需求的组织，DHI Enterprise 提供额外能力。

### 合规变体 {tier="DHI Enterprise"}

- FIPS 启用镜像：适用于受监管行业和政府系统
- STIG 就绪镜像：满足美国国防部安全技术实施指南（DoD Security Technical Implementation Guide）要求

### SLA 支持的安全 {tier="DHI Enterprise"}

- CVE 修复 SLA：针对关键和高严重性漏洞提供 7 天 SLA，对其他严重性级别也有 SLA 承诺
- ELS CVE 修复 SLA：扩展生命周期支持镜像具有 CVE 修复的 SLA 承诺，即使在上游结束生命周期后也是如此
- 企业支持：可访问 Docker 支持团队，为关键任务应用提供支持

### 定制化和控制 {tier="DHI Enterprise"}

- 构建自定义镜像：添加您自己的软件包、工具、证书和配置
- 安全构建基础设施：在 Docker 可信基础设施上构建定制内容
- 完整的信任链：定制镜像保持构建证明和密码学签名
- 自动更新：当基础镜像打补丁时，自定义镜像会自动重建

### 扩展生命周期支持 {tier="DHI Enterprise 增值选项"}

- 生命周期结束后安全覆盖：在上游支持结束后多年内继续接收补丁
- 持续合规：为审计要求提供更新的 SBOM、构建证明和签名
- 生产连续性：在无需强制迁移的情况下，保持生产环境的安全运行

## 了解更多

- [探索 DHI 镜像的构建方式等更多内容](/dhi/explore/)
- [开始使用 DHI](/dhi/get-started/)
- [联系 Docker 了解 DHI Enterprise](https://www.docker.com/pricing/contact-sales/)