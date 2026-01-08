---
---
title: 理解 Docker Hardened Images 的角色与职责
linkTitle: 职责概览
description: 了解使用 Docker Hardened Images 时，Docker、上游项目与您之间的责任划分。
weight: 46
keywords: "software supply chain security, signed sbom, vex document, container provenance, image attestation"
aliases:
  - /dhi/about/responsibility/---
Docker Hardened Images (DHIs) 由 Docker 策划和维护，并使用上游开源组件构建。
为了提供安全性、可靠性和合规性，责任由三方共享：

- 上游维护者：负责每个镜像中包含的开源软件的开发者和社区。
- Docker：经过加固、签名和维护的容器镜像的提供者。
- 您（客户）：在您的环境中运行并（可选）自定义 DHIs 的使用者。

本主题概述了各方负责的内容，以便您能够有效且安全地使用 DHIs。

## 发布

- 上游：发布并维护 DHIs 中包含的软件组件的官方版本。这包括版本控制、更新日志和弃用通知。
- Docker：基于上游版本构建、加固并签名 Docker Hardened Images。Docker 根据上游发布时间表和内部策略来维护这些镜像。
- 您：确保您使用的是受支持的 DHI 和上游项目版本。使用过时或不受支持的组件可能会引入安全风险。

## 补丁

- 上游：维护并更新每个组件的源代码，包括修复库和依赖项中的漏洞。
- Docker：在应用上游补丁后重新构建并重新发布镜像。Docker 监控漏洞并向受影响的镜像发布更新。仅 DHI Enterprise 包含 SLA。DHI Free 提供安全基线，但不保证修复时间表。
- 您：在您的环境中应用 DHI 更新，并为您在基础镜像之上安装的任何软件或依赖项打补丁。

## 测试

- 上游：定义原始软件的行为和功能，并负责验证核心功能。
- Docker：验证 DHI 能够启动、运行，并且其行为与上游预期一致。Docker 还会运行安全扫描，并为每个镜像包含一份[测试证明](../core-concepts/attestations.md)。
- 您：在 DHI 之上测试您的应用程序，并验证任何更改或自定义功能在您的环境中是否按预期运行。

## 安全与合规

- Docker：随每个镜像发布经过签名的 SBOM、VEX 文档、来源数据 和 CVE 扫描结果，以支持合规性和供应链安全。
  - 对于免费 DHI 用户：所有安全元数据和透明度功能均免费包含在内。
  - 对于 DHI Enterprise 用户：可提供额外的合规性变体（如 FIPS 和 STIG）和自定义功能，并在基础镜像打补丁时自动重新构建。
- 您：将 DHI 集成到您的安全和合规工作流中，包括漏洞管理和审计。

## 支持

- Docker：
  - 对于免费 DHI 用户：可提供社区支持和公开文档。
  - 对于 DHI Enterprise 用户：可为关键任务应用程序访问 Docker 的企业支持团队。
- 您：关注 Docker 的发布说明、安全公告和文档，以获取更新和最佳实践。

## 总结

Docker Hardened Images 为您提供了一个安全的基础，并附带签名的元数据和上游透明度。您的职责是明智地使用这些镜像，及时应用更新，并验证您的配置和应用程序满足您的内部要求。