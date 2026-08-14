# Software Supply Chain Security（软件供应链安全）


## What is Software Supply Chain Security (SSCS)?（什么是软件供应链安全（SSCS）？）

SSCS 涵盖旨在保护软件开发生命周期（从初始代码创建到部署和维护）各个阶段实践与策略。它专注于保护所有组件。这包括代码、依赖项、构建过程和分发渠道，以防止恶意行为者破坏软件供应链。鉴于对开源库和第三方组件的日益依赖，确保这些元素的完整性和安全性至关重要。

## Why is SSCS important?（为何 SSCS 很重要？）

由于针对软件供应链的复杂网络攻击不断升级，SSCS 的重要性也随之提高。备受瞩目的供应链攻击以及对开源组件中漏洞的利用，凸显了对强大供应链安全措施的迫切需求。软件生命周期中任何阶段的破坏都可能导致广泛的漏洞、数据泄露和重大的财务损失。

## How Docker Hardened Images contribute to SSCS（Docker Hardened Images 如何助力 SSCS）

Docker Hardened Images（DHI）是以安全为核心的专用容器镜像，旨在应对现代软件供应链安全的挑战。通过将 DHI 集成到你的开发和部署流水线中，你可以通过以下功能增强组织的 SSCS 态势：

- 最小攻击面：DHI 经过精心设计实现极致精简，去除不必要的组件，将攻击面最多减少 95%。这种 distroless 方法最大限度地减少了恶意行为者可能的入口点。

- 加密签名与来源：每个 DHI 都经过加密签名，确保真实性和完整性。构建来源得到维护，提供关于镜像来源和构建过程的可验证证据，符合 SLSA（Supply-chain Levels for Software Artifacts，软件制品供应链级别）等标准。

- 软件物料清单（SBOM）：DHI 包含全面的 SBOM，详细列出镜像中的所有组件和依赖项。这种透明度有助于漏洞管理和合规跟踪，使团队能够有效评估和降低风险。

- 持续维护与快速 CVE 修复：Docker 通过定期更新和安全补丁维护 DHI，并辅以[处理严重和高严重性漏洞的 SLA](https://docs.docker.com/go/dhi-sla/)。这种主动方法有助于确保镜像保持安全并符合企业标准。

