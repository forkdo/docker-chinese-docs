# Supply-chain Levels for Software Artifacts (SLSA)


## 什么是 SLSA？（What is SLSA?）

Supply-chain Levels for Software Artifacts（SLSA，软件制品供应链等级）是一个安全框架，旨在增强软件供应链的完整性和安全性。SLSA 由 Google 开发、由 Open Source Security Foundation（OpenSSF，开源安全基金会）维护，它提供了一套指南与最佳实践，用于防止篡改、提升完整性，并保护软件项目中的包与基础设施。

SLSA 定义了 [四个构建等级（0–3）](https://slsa.dev/spec/latest/build-track-basics)，安全严格程度逐级递增，重点关注构建来源（build provenance）、源完整性以及构建环境安全等领域。每个等级都建立在前一个等级之上，为实现更高水平的软件供应链安全提供了一条结构化的路径。

## 为什么 SLSA 很重要？（Why is SLSA important?）

由于软件供应链日益复杂且相互关联，SLSA 对于现代软件开发至关重要。SolarWinds 入侵等供应链攻击事件，已经暴露出软件开发流程中的诸多漏洞。通过实施 SLSA，组织可以：

- 确保制品完整性：验证软件制品在构建和部署过程中未被篡改。
- 增强构建来源：维护关于软件制品如何以及何时产生的可验证记录，提供透明度与可追溯性。
- 保护构建环境：实施控制措施，防止构建系统被未授权访问和修改。
- 降低供应链风险：降低在软件供应链中引入漏洞或恶意代码的风险。

## 什么是 SLSA Build Level 3？

SLSA Build Level 3（加固构建，Hardened Builds）是 SLSA 框架四个递进等级中的最高级。它引入了严格的要求，以确保软件制品在安全且可追溯的方式下构建。要满足 Level 3，一次构建必须：

- 完全自动化并通过脚本驱动，以防止人工篡改
- 使用受信任的构建服务，强制实施源和构建者的身份验证
- 生成已签名、防篡改的来源（provenance）记录，描述制品是如何构建的
- 捕获关于构建环境、源仓库以及构建步骤的元数据

这一等级有力地保证了软件是在受控、可审计的环境中从预期的源码构建而来，从而显著降低供应链攻击的风险。

## Docker Hardened Images 与 SLSA

Docker Hardened Images（DHIs，Docker 加固镜像）是安全优先的容器镜像，专为现代生产环境量身打造。每个 DHI 都经过加密签名，并符合 [SLSA Build Level 3 标准](https://slsa.dev/spec/latest/build-track-basics#build-l3)，确保构建来源与完整性可验证。

通过将符合 SLSA 的 DHI 集成到你的开发和部署流程中，你可以：

- 实现更高的安全等级：使用符合严格安全标准的镜像，降低漏洞与攻击风险。
- 简化合规：借助内置特性，如已签名的软件物料清单（SBOM）和漏洞例外（VEX）声明，来满足 FedRAMP 等法规的合规要求。
- 增强透明度：获取关于每个镜像的组件和构建流程的详细信息，提升透明度与信任感。
- 简化审计：利用可验证的构建记录和签名，简化安全审计与评估工作。

## 获取并验证 Docker Hardened Images 的 SLSA 来源（Get and verify SLSA provenance for Docker Hardened Images）

每个 Docker Hardened Image（DHI）都经过加密签名，并包含证明（attestation）。这些证明提供可验证的构建来源，并证明符合 SLSA Build Level 3 标准。

要获取并验证 DHI 的 SLSA 来源，你可以使用 Docker Scout。

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

## 相关资源（Resources）

有关 SLSA 定义和 Docker Build 的更多细节，请参阅 [SLSA definitions](/build/metadata/attestations/slsa-definitions/)。

