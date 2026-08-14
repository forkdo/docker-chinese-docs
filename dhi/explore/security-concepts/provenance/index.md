# Image provenance（镜像来源）


## What is image provenance?（什么是镜像来源？）

镜像来源（image provenance）是指追溯容器镜像的来源、作者和完整性的元数据。它回答了一些关键问题，例如：

- 这个镜像来自哪里？
- 谁构建的？
- 是否被篡改过？

来源建立了监管链（chain of custody），帮助你验证正在使用的镜像是一个受信任且可验证的构建过程的结果。

## Why image provenance matters（为何镜像来源很重要）

来源是保障软件供应链安全的基础。没有它，你将面临以下风险：

- 运行未经验证或恶意的镜像
- 无法满足内部或法规合规要求
- 对生成容器的组件和工作流失去可见性

拥有可靠的来源，你可以获得：

- 信任（Trust）：知道你的镜像是真实且未被更改的。
- 可追溯性（Traceability）：理解完整的构建过程和源输入。
- 可审计性（Auditability）：提供合规性和构建完整性的可验证证据。

来源还支持自动化策略执行，并且是 SLSA（Supply-chain Levels for Software Artifacts，软件制品供应链级别）等框架的关键要求。

## How Docker Hardened Images support provenance（Docker Hardened Images 如何支持来源）

Docker Hardened Images（DHI）在设计时即内置来源，帮助你采用默认安全的实践并满足供应链安全标准。

### Attestations（证明）

DHI 包含[证明](./attestations.md)——用于描述镜像在何时、何地以及如何构建的机器可读元数据。这些证明使用 [in-toto](https://in-toto.io/) 等行业标准生成，并与 [SLSA provenance](https://slsa.dev/spec/v1.0/provenance/) 保持一致。

证明可让你：

- 验证构建是否遵循了预期步骤
- 确认输入和环境符合策略
- 跨系统和阶段追踪构建过程

### Code signing（代码签名）

每个 Docker Hardened Image 都经过加密[签名](./signatures.md)并与它的摘要（digest）一同存储在仓库中。这些签名是可验证的真实性证明，并与 `cosign`、Docker Scout 和 Kubernetes 准入控制器等工具兼容。

通过镜像签名，你可以：

- 确认镜像由 Docker 发布
- 检测镜像是否被修改或重新发布
- 在 CI/CD 或生产部署中强制执行签名验证

## Additional resources（其他资源）

- [Provenance attestations](/build/metadata/attestations/slsa-provenance/)
- [Image signatures](./signatures.md)
- [Attestations overview](./attestations.md)

