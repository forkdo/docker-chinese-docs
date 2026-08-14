# Secure Software Development Lifecycle（安全软件开发生命周期）


## What is a Secure Software Development Lifecycle?（什么是安全软件开发生命周期？）

安全软件开发生命周期（SSDLC）将安全实践整合到软件交付的每个阶段，从设计和开发到部署和监控。这不仅仅关乎编写安全的代码，还关乎将安全性嵌入用于构建和发布软件的工具、环境和工作流中。

SSDLC 实践通常由合规框架、组织策略和供应链安全标准（如 SLSA（Supply-chain Levels for Software Artifacts，软件制品供应链级别）或 NIST SSDF）指导。

## Why SSDLC matters（为何 SSDLC 很重要）

现代应用程序依赖于快速、迭代的开发，但如果在早期没有内建保护措施，快速交付往往会引入安全风险。SSDLC 有助于：

- 在漏洞进入生产环境之前加以预防
- 通过可追溯、可审计的工作流确保合规
- 通过保持一致的安全标准来降低运营风险
- 在 CI/CD 流水线和云原生环境中实现安全的自动化

通过使安全成为软件交付每个阶段的一等公民，组织可以左移（shift left），同时降低成本和复杂性。

## How Docker supports a secure SDLC（Docker 如何支持安全的 SDLC）

Docker 提供工具和安全的制品内容，使 SSDLC 实践更容易在容器生命周期中采用。借助 [Docker Hardened Images](../_index.md)（DHI）、[Docker Debug](/reference/cli/docker/debug/) 和 [Docker Scout](../../../scout/_index.md)，团队可以在不损失速度的情况下增加安全性。

### Plan and design（规划与设计）

在规划阶段，团队定义架构约束、合规目标和威胁模型。Docker Hardened Images 在此阶段提供帮助，提供：

- 面向常见语言和运行时、默认安全的镜像
- 经过验证的元数据，包括 SBOM、来源和 VEX 文档
- 跨多个 Linux 发行版对 glibc 和 musl 的支持

你可以使用 DHI 元数据和证明来支持设计评审、威胁建模或架构审批。

### Develop（开发）

在开发阶段，安全性应当透明且易于应用。Docker Hardened Images 支持默认安全的开发：

- 开发变体包含 shell、包管理器和编译器以便使用
- 最小的运行时变体减少最终镜像中的攻击面
- 多阶段构建让你可以将构建时工具与运行时环境分离

[Docker Debug](/reference/cli/docker/debug/) 可帮助开发人员：

- 将调试工具临时注入最小容器
- 避免在故障排查时修改基础镜像
- 即使在类似生产的环境中也能安全地排查问题

### Build and test（构建与测试）

构建流水线是尽早发现问题的理想位置。Docker Scout 与 Docker Hub 和 CLI 集成，以：

- 使用多个漏洞数据库扫描已知 CVE
- 将漏洞追溯到特定的层和依赖项
- 解析已签名的 VEX 数据以抑制已知不相关的问题
- 导出 JSON 扫描报告供 CI/CD 工作流使用

使用 Docker Hardened Images 的构建流水线受益于：

- 可复现、已签名的镜像
- 最小的构建表面以减少暴露
- 内置符合 SLSA Build Level 3 标准

### Release and deploy（发布与部署）

当你大规模发布软件时，安全自动化至关重要。Docker 通过以下方式支持此阶段：

- 部署前进行签名验证和来源验证
- 使用 Docker Scout 执行策略门禁（policy enforcement gates）
- 使用 Docker Debug 进行安全、非侵入式的容器检查

DHI 附带在部署期间自动化镜像验证所需的元数据和签名。

### Monitor and improve（监控与改进）

安全性在发布后仍在继续。借助 Docker 工具，你可以：

- 通过 Docker Hub 持续监控镜像漏洞
- 使用 Docker Scout 获取 CVE 修复指导和补丁可见性
- 接收已重建并重新签名的更新 DHI 镜像及安全层
- 使用 Docker Debug 调试正在运行的工作负载而无需修改镜像

## Summary（总结）

Docker 通过将安全内容（DHI）与对开发者友好的工具（Docker Scout 和 Docker Debug）相结合，帮助团队在 SSDLC 的各个环节嵌入安全性。这些集成在不引入摩擦的情况下促进了安全实践，使你的软件交付生命周期中更容易采用合规和供应链安全。

