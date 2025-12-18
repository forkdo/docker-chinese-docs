---
title: 安全软件开发生命周期
linktitle: SSDLC
description: 了解 Docker Hardened Images 如何通过集成扫描、签名和调试工具来支持安全的 SDLC。
keywords: 安全软件开发, ssdlc 容器, slsa 合规性, docker scout 集成, 安全容器调试
---

## 什么是安全软件开发生命周期？

安全软件开发生命周期（SSDLC）将安全实践融入软件交付的每个阶段，从设计、开发到部署和监控。它不仅仅是编写安全的代码，更是关于在整个构建和发布软件的工具、环境和工作流中嵌入安全。

SSDLC 实践通常由合规框架、组织策略和供应链安全标准（如 SLSA（软件制品供应链级别）或 NIST SSDF）指导。

## 为什么 SSDLC 很重要

现代应用程序依赖于快速、迭代的开发，但如果不在早期构建保护措施，快速交付往往会引入安全风险。SSDLC 有助于：

- 在漏洞到达生产环境之前就加以防范
- 通过可追踪和可审计的工作流确保合规
- 通过保持一致的安全标准降低运营风险
- 在 CI/CD 流水线和云原生环境中实现安全自动化

通过在软件交付的每个阶段都将安全作为首要任务，组织可以左移安全控制，降低成本和复杂性。

## Docker 如何支持安全的 SDLC

Docker 提供了工具和安全内容，使团队能够在容器生命周期中更轻松地采用 SSDLC 实践。借助 [Docker Hardened Images](../_index.md)（DHIs）、[Docker Debug](../../../reference/cli/docker/debug.md) 和 [Docker Scout](../../../manuals/scout/_index.md)，团队可以在不损失效率的情况下增强安全性。

### 规划和设计

在规划阶段，团队定义架构约束、合规目标和威胁模型。Docker Hardened Images 在此阶段通过以下方式提供帮助：

- 为常见语言和运行时提供默认安全的基础镜像
- 提供包含 SBOM、来源和 VEX 文档的已验证元数据
- 支持多种 Linux 发行版中的 glibc 和 musl

您可以使用 DHI 元数据和证明来支持设计评审、威胁建模或架构签署。

### 开发

在开发过程中，安全应该是透明且易于应用的。Docker Hardened Images 支持默认安全的开发：

- Dev 变体包含用于便捷的 shell、包管理器和编译器
- 最小运行时变体减少最终镜像的攻击面
- 多阶段构建允许您将构建时工具与运行时环境分离

[Docker Debug](../../../reference/cli/docker/debug.md) 帮助开发人员：

- 临时将调试工具注入最小容器中
- 在故障排除期间避免修改基础镜像
- 在生产类环境中安全地调查问题

### 构建和测试

构建流水线是及早发现问题的理想场所。Docker Scout 与 Docker Hub 和 CLI 集成，可以：

- 使用多个漏洞数据库扫描已知的 CVE
- 将漏洞追溯到特定层和依赖项
- 解释已签名的 VEX 数据以抑制已知无关的问题
- 导出 JSON 扫描报告供 CI/CD 工作流使用

使用 Docker Hardened Images 的构建流水线受益于：

- 可重现、已签名的镜像
- 最小构建面以减少暴露
- 符合 SLSA Build Level 3 标准

### 发布和部署

在大规模发布软件时，安全自动化至关重要。Docker 通过以下方式支持此阶段：

- 在部署前验证签名和来源
- 使用 Docker Scout 强制执行策略门禁
- 使用 Docker Debug 进行安全、非侵入式的容器检查

DHIs 附带部署期间自动验证镜像所需的元数据和签名。

### 监控和改进

安全在发布后继续。借助 Docker 工具，您可以：

- 通过 Docker Hub 持续监控镜像漏洞
- 使用 Docker Scout 获取 CVE 修复指导和补丁可见性
- 接收使用重建和重新签名的安全层更新的 DHI 镜像
- 使用 Docker Debug 调试运行中的工作负载，而无需修改镜像

## 总结

Docker 通过结合安全内容（DHIs）和开发者友好的工具（Docker Scout 和 Docker Debug）来帮助团队在整个 SSDLC 中嵌入安全。这些集成促进了安全实践，而不会引入摩擦，使组织更容易在整个软件交付生命周期中采用合规和供应链安全。