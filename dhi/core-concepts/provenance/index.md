# 镜像溯源

## 什么是镜像溯源？

镜像溯源是指用于追踪容器镜像来源、作者身份和完整性的元数据。它可以回答一些关键问题，例如：

- 此镜像来自哪里？
- 它是由谁构建的？
- 它是否被篡改过？

溯源建立了一个监管链，帮助您验证您正在使用的镜像是可信且可验证的构建过程的结果。

## 为什么镜像溯源很重要

溯源是保障软件供应链安全的基础。没有它，您将面临以下风险：

- 运行未经验证或恶意的镜像
- 无法满足内部或法规合规性要求
- 对生成容器的组件和工作流失去可见性

拥有可靠的溯源，您可以获得：

- 信任：确保您的镜像是真实且未经更改的。
- 可追溯性：了解完整的构建过程和源输入。
- 可审计性：提供合规性和构建完整性的可验证证据。

溯源还支持自动化策略执行，并且是 SLSA (Supply-chain Levels for Software Artifacts) 等框架的一项关键要求。

## Docker Hardened Images 如何支持溯源

Docker Hardened Images (DHIs) 在设计时就内置了溯源功能，以帮助您采用默认安全的实践，并满足供应链安全标准。

### 证明

DHI 包含 [证明](./attestations.md)——一种机器可读的元数据，用于描述镜像的构建方式、时间和地点。这些证明使用 [in-toto](https://in-toto.io/) 等行业标准生成，并符合 [SLSA provenance](https://slsa.dev/spec/v1.0/provenance/) 规范。

证明允许您：

- 验证构建过程是否遵循了预期的步骤
- 确认输入和环境满足策略要求
- 跨系统和阶段追踪构建过程

### 代码签名

每个 Docker Hardened Image 都经过加密 [签名](./signatures.md)，并与摘要一起存储在镜像仓库中。这些签名是真实性的可验证证明，并与 cosign、Docker Scout 和 Kubernetes 准入控制器等工具兼容。

通过镜像签名，您可以：

- 确认镜像由 Docker 发布
- 检测镜像是否已被修改或重新发布
- 在 CI/CD 或生产部署中强制执行签名验证

## 其他资源

- [溯源证明](/build/metadata/attestations/slsa-provenance/)
- [镜像签名](./signatures.md)
- [证明概览](./attestations.md)
