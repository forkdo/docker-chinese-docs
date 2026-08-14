---
title: Docker Hardened Images release notes
linkTitle: Platform release notes
description: 了解 Docker Hardened Images 中的最新功能与变更
keywords: docker hardened images, dhi, release notes, changelog, features, changes, new, releases
tags: [Release notes]
---


本页面包含 Docker Hardened Images (DHI) 平台中新功能、改进和变更的信息。
发布说明按季度汇总，仅包含值得注意的产品变更。

## 2026 年第三季度（Q3 2026）

2026 年第三季度发布的全新功能与增强：

- DHI MCP 服务器：DHI 目录现在可通过位于 `https://dhi.io/mcp` 的远程 MCP 服务器访问。连接任何支持 MCP 的 AI 助手，即可使用自然语言搜索仓库、检查镜像元数据、检索 SBOM、检查 CVE 以及管理镜像。有关更多信息，请参阅[使用 DHI MCP 服务器](/dhi/tools/mcp/)。

## 2026 年第二季度（Q2 2026）

2026 年第二季度发布的全新功能与增强：

- Debian 加固系统包：新增对基于 Debian 的 Docker 加固系统包（HSP）的支持，包括用于在 Debian HSP 仓库进行身份验证的新 CLI 工作流。
- Mend.io 扫描器集成：Mend.io 现已成为可用于消费 DHI VEX 数据的扫描器。
- Black Duck 扫描器集成：Black Duck 现已成为可用于消费 DHI VEX 数据的扫描器。
- DHI Select 自助购买：DHI Select 现已可通过 Docker 网站直接自助购买。
- 批量自定义：通过 Docker Hub UI 和 CLI，在单次操作中将自定义配置应用到多个镜像。
- Terraform 提供商：使用官方 Terraform 提供商管理 DHI 资源，包括自定义配置和镜像。

## 2026 年第一季度（Q1 2026）

2026 年第一季度发布的全新功能与增强：

- Docker 加固系统包（HSP）：发布了 Docker 加固系统包，这是一种新的产品，提供用于在您自己的基础镜像中使用的单独加固包。有关更多信息，请参阅[公告博客文章](https://www.docker.com/blog/announcing-docker-hardened-system-packages/)。
- Wiz 扫描器集成：Wiz 现已成为可用于消费 DHI VEX 数据的扫描器。

## 2025 年第四季度（Q4 2025）

2025 年第四季度发布的全新功能与增强：

- Docker 加固镜像社区版（免费）：Docker 加固镜像现已通过社区订阅层级向每位开发者提供。订阅层级现为社区版、Select 版和企业版。有关更多信息，请参阅[公告博客文章](https://www.docker.com/blog/docker-hardened-images-for-every-developer/)。
- SRLabs 的独立安全验证：SRLabs 发布了针对 Docker 加固镜像的独立安全验证。请参阅[验证公告](https://www.docker.com/blog/docker-hardened-images-security-independently-validated-by-srlabs/)。
- 面向 DHI 的 Docker Scout 评分：Docker Scout 镜像评分现已考虑 DHI 提供的安全改进。
- Trivy VEX 仓库：DHI 的 VEX 数据发布在 Trivy 兼容的 OCI VEX 仓库中，使 Trivy 和其他扫描器更容易消费。
- Docker Scout DHI 策略：新增用于评估镜像是否使用 Docker 加固镜像的 Docker Scout 策略。
- 加固 Helm 图表（测试版）：发布 Docker 加固 Helm 图表的测试版。有关更多信息，请参阅[公告博客文章](https://www.docker.com/blog/docker-hardened-images-helm-charts-beta/)。
- 镜像用户体验：使用焕新的 UI 和更清晰的流程更新了 Docker Hub 中的镜像体验。

## 2025 年第三季度（Q3 2025）

2025 年第三季度发布的全新功能与增强：

- 下一阶段演进版本：一个重大版本，引入了自定义配置、FedRAMP 就绪镜像、AI 迁移代理以及更深入的扫描器集成。请参阅[公告博客文章](https://www.docker.com/blog/the-next-evolution-of-docker-hardened-images/)和 [FedRAMP 合规博客文章](https://www.docker.com/blog/fedramp-compliance-with-hardened-images/)。
- DHI 自定义配置：直接从 Docker Hub UI 自定义 DHI 镜像，提供在基础加固镜像之上添加包、文件和配置的选项。
- AI 迁移代理：用于帮助将现有 Dockerfile 转换为使用 Docker 加固镜像的 AI 辅助 Dockerfile 迁移。
- CIS 合规证明：DHI 镜像现已包含 CIS 基准合规证明。
- STIG 变体：适用于美国国防部合规用例的 STIG 加固镜像变体。

## 2025 年第二季度（Q2 2025）

2025 年第二季度发布的全新功能与增强：

- Docker 加固镜像发布：Docker 发布了 Docker 加固镜像，这是一系列由 Docker 维护的安全、最小化且可用于生产的容器镜像。有关更多信息，请参阅[发布博客文章](https://www.docker.com/blog/introducing-docker-hardened-images/)。
- FIPS 变体：适用于 Docker 加固镜像的 FIPS 验证镜像变体。
