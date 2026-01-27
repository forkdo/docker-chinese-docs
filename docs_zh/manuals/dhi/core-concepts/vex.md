---
title: 漏洞可利用性交换 (VEX)
linktitle: VEX
description: 了解 VEX 如何通过识别 Docker 加固镜像中的哪些漏洞实际上可利用，帮助您优先处理真正的风险。
keywords: vex container security, vulnerability exploitability, filter false positives, docker scout vex, cve prioritization
---

## 什么是 VEX？

漏洞可利用性交换 (Vulnerability Exploitability eXchange, VEX) 是一种用于记录软件组件中漏洞可利用性状态的规范。VEX 主要通过行业标准（如 CSAF (OASIS) 和 CycloneDX VEX）定义，美国网络安全和基础设施安全局 (CISA) 鼓励采用该规范。VEX 通过添加生产者声明的状态信息来补充 CVE（常见漏洞和暴露）标识符，指示漏洞在交付的产品中是否可利用。这有助于组织通过识别不影响其特定产品配置的漏洞来优先处理修复工作。

## 为什么 VEX 很重要？

VEX 通过以下方式增强传统的漏洞管理：

- **抑制不适用漏洞**：通过提供供应商的产品级可利用性声明，VEX 有助于过滤掉不影响交付产品的漏洞。

- **优先处理修复**：组织可以将资源集中在处理生产者已确认在产品可利用的漏洞上，提高漏洞管理的效率。

- **支持漏洞文档记录**：VEX 声明可以支持审计讨论，并帮助记录为什么某些漏洞不需要修复。

在处理复杂软件组件时，这种方法特别有益，因为并非所有报告的 CVE 都适用于特定的产品配置。

## Docker 加固镜像如何集成 VEX

为了增强漏洞管理，Docker 加固镜像 (DHI) 集成了 VEX 报告，提供对已知漏洞的特定上下文评估。

这种集成允许您：

- **使用生产者声明**：查看 Docker 关于镜像组件中已知漏洞在交付产品中是否可利用的声明。

- **优先处理操作**：将修复工作集中在 Docker 已确认在镜像中可利用的漏洞上，优化资源分配。

- **支持审计文档**：使用 VEX 声明记录为什么某些报告的漏洞不需要立即采取行动。

通过将 DHI 的安全功能与 VEX 的产品级可利用性声明相结合，组织可以实现更有效和高效的漏洞管理方法。

> [!提示]
>
> 要了解哪些扫描器支持 VEX 以及为什么它对你的安全工作流程很重要，请参阅[扫描器集成](/manuals/dhi/explore/scanner-integrations.md)。

## 使用 VEX 抑制不适用 CVE

Docker 加固镜像包含 VEX 证明，漏洞扫描器可以使用这些证明来抑制不适用 CVE。有关在不同工具（包括 Docker Scout、Trivy 和 Grype）中使用 VEX 支持的详细扫描说明，请参阅[扫描 Docker 加固镜像](/manuals/dhi/how-to/scan.md)。