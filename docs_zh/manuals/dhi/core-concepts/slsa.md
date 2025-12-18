---
title: 软件工件供应链层级（SLSA）
linktitle: SLSA
description: 了解 Docker Hardened Images 如何符合 SLSA Build Level 3 标准，以及如何验证构建来源以实现安全、防篡改的构建。
keywords: slsa docker 合规性, slsa build level 3, 供应链安全, 已验证构建来源, 安全容器构建
---

## 什么是 SLSA？

软件工件供应链层级（Supply-chain Levels for Software Artifacts，简称 SLSA）是一个旨在增强软件供应链完整性和安全性的安全框架。该框架由 Google 开发，由开源安全基金会（OpenSSF）维护，提供了一系列指南和最佳实践，用于防止篡改、提高完整性，并保护软件项目中的包和基础设施。

SLSA 定义了四个递增安全严格度的构建层级（0–3），重点关注构建来源、源代码完整性和构建环境安全等领域。每个层级都建立在前一个层级的基础上，提供了一种实现更高级别软件供应链安全的结构化方法。

## 为什么 SLSA 很重要？

SLSA 对现代软件开发至关重要，因为软件供应链的复杂性和相互关联性日益增加。供应链攻击（如 SolarWinds 泄露事件）凸显了软件开发流程中的漏洞。通过实施 SLSA，组织可以：

- 确保工件完整性：验证软件工件在构建和部署过程中未被篡改。

- 增强构建来源：维护软件工件如何以及何时生成的可验证记录，提供透明度和可问责性。

- 保护构建环境：实施控制措施以保护构建系统免受未授权访问和修改。

- 降低供应链风险：减少在软件供应链中引入漏洞或恶意代码的风险。

## 什么是 SLSA Build Level 3？

SLSA Build Level 3（Hardened Builds，强化构建）是 SLSA 框架中四个递进层级中的最高级别。它引入了严格的要求，以确保软件工件能够安全、可追溯地构建。要达到 Level 3，构建必须：

- 完全自动化和脚本化，以防止手动篡改
- 使用强制执行源代码和构建器身份验证的可信构建服务
- 生成描述工件如何构建的已签名、防篡改的来源记录
- 捕获有关构建环境、源代码仓库和构建步骤的元数据

此层级提供了强有力的保证，确保软件是从预期的源代码在受控、可审计的环境中构建的，从而显著降低了供应链攻击的风险。

## Docker Hardened Images 与 SLSA

Docker Hardened Images（DHIs）是为现代生产环境量身打造的默认安全容器镜像。每个 DHI 都经过加密签名，并符合 [SLSA Build Level 3 标准](https://slsa.dev/spec/latest/build-track-basics#build-l3)，确保可验证的构建来源和完整性。

通过将符合 SLSA 标准的 DHI 集成到您的开发和部署流程中，您可以：

- 实现更高级别的安全性：利用满足严格安全标准的镜像，降低漏洞和攻击的风险。

- 简化合规性：利用内置功能，如已签名的软件物料清单（SBOM）和漏洞例外（VEX）声明，以促进符合 FedRAMP 等法规要求。

- 增强透明度：访问有关每个镜像组件和构建流程的详细信息，促进透明度和信任。

- 简化审计：利用可验证的构建记录和签名来简化安全审计和评估。

## 获取并验证 Docker Hardened Images 的 SLSA 来源

每个 Docker Hardened Image（DHI）都经过加密签名，并包含证明。这些证明提供了可验证的构建来源，并展示了对 SLSA Build Level 3 标准的遵循。

要获取并验证 DHI 的 SLSA 来源，您可以使用 Docker Scout。

```console
$ docker scout attest get dhi.io/<image>:<tag> \
  --predicate-type https://slsa.dev/provenance/v0.2 \
  --verify
```

例如：

```console
$ docker scout attest get dhi.io/node:20.19-debian12 \
  --predicate-type https://slsa.dev/provenance/v0.2 \
  --verify
```

## 资源

有关 SLSA 定义和 Docker Build 的更多详细信息，请参阅 [SLSA 定义](/build/metadata/attestations/slsa-definitions/)。