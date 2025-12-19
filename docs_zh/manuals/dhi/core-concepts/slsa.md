---
title: 软件制品供应链安全等级 (SLSA)
linktitle: SLSA
description: 了解 Docker 强化镜像如何符合 SLSA 构建等级 3，以及如何验证来源以实现安全、防篡改的构建。
keywords: slsa docker compliance, slsa build level 3, supply chain security, verified build provenance, secure container build
---

## 什么是 SLSA？

软件制品供应链安全等级 (SLSA) 是一个安全框架，旨在增强软件供应链的完整性。由 Google 开发并由开源安全基金会 (OpenSSF) 维护，SLSA 提供了一套指南和最佳实践，以防止篡改、提高完整性，并保护软件项目中的包和基础设施。

SLSA 定义了[四个构建等级 (0–3)](https://slsa.dev/spec/latest/build-track-basics)，其安全严格性逐步提升，重点关注构建来源、源码完整性和构建环境安全等领域。每个等级都建立在前一个等级的基础上，为实现更高水平的软件供应链安全提供结构化方法。

## 为什么 SLSA 很重要？

由于软件供应链的复杂性和相互关联性日益增加，SLSA 对现代软件开发至关重要。SolarWinds 入侵等供应链攻击凸显了软件开发流程中的漏洞。通过实施 SLSA，组织可以：

- 确保制品完整性：验证软件制品在构建和部署过程中是否未被篡改。

- 增强构建来源：保留软件制品如何以及何时生成的可验证记录，提供透明度和问责制。

- 保护构建环境：实施控制措施，防止构建系统被未经授权的访问和修改。

- 降低供应链风险：降低将漏洞或恶意代码引入软件供应链的风险。

## 什么是 SLSA 构建等级 3？

SLSA 构建等级 3（强化构建）是 SLSA 框架中四个递进等级中的最高等级。它引入了严格要求，以确保软件制品被安全且可追溯地构建。要满足等级 3，构建必须：

- 完全自动化和脚本化，以防止手动篡改
- 使用强制源码和构建器身份验证的可信构建服务
- 生成描述制品如何构建的已签名、防篡改的来源记录
- 捕获有关构建环境、源码仓库和构建步骤的元数据

该等级提供了强有力的保证，即软件是在受控、可审计的环境中从预期源码构建的，这显著降低了供应链攻击的风险。

## Docker 强化镜像和 SLSA

Docker 强化镜像 (DHIs) 是专为现代生产环境构建的安全默认容器镜像。每个 DHI 都经过加密签名，并符合 [SLSA 构建等级 3 标准](https://slsa.dev/spec/latest/build-track-basics#build-l3)，确保可验证的构建来源和完整性。

通过将符合 SLSA 的 DHI 集成到您的开发和部署流程中，您可以：

- 实现更高的安全等级：使用符合严格安全标准的镜像，降低漏洞和攻击的风险。

- 简化合规性：利用内置功能（如签名的软件物料清单 (SBOM) 和漏洞例外 (VEX) 声明），便于符合 FedRAMP 等法规。

- 增强透明度：访问有关每个镜像组件和构建流程的详细信息，促进透明度和信任。

- 简化审计：利用可验证的构建记录和签名，简化安全审计和评估。

## 获取并验证 Docker 强化镜像的 SLSA 来源

每个 Docker 强化镜像 (DHI) 都经过加密签名，并包含证明。这些证明提供了可验证的构建来源，并展示了对 SLSA 构建等级 3 标准的遵守。

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