---
---
title: How Docker Hardened Images are built
linkTitle: Build process
description: "Learn how Docker builds, tests, and maintains Docker Hardened Images through an automated, security-focused pipeline."
weight: 15
keywords: "docker hardened images, slsa build level 3, automated patching, ai guardrail, build process, signed sbom, supply chain security"
aliases:
  - /dhi/about/build-process/---
title: Docker Hardened Images 的构建过程
linkTitle: 构建流程
description: "了解 Docker 如何通过自动化的、以安全为中心的流水线来构建、测试和维护 Docker Hardened Images。"
weight: 15---
Docker Hardened Images 通过一个自动化的流水线构建，该流水线监控上游源、应用安全更新并发布已签名的制品。本文档解释了基础 DHI 镜像和 DHI Enterprise 定制镜像的构建流程。

通过 DHI Enterprise 订阅，基础镜像和定制镜像的自动化安全更新流水线由 SLA 承诺支持，包括对严重和高严重性漏洞的 7 天 SLA。只有 DHI Enterprise 包含 SLA。DHI Free 提供安全基线，但不保证修复时间。

## 构建触发

构建会自动启动。您无需手动触发。系统会监控变更并在以下两种情况下自动启动构建：

- [上游更新](#upstream-updates)
- [定制变更](#customization-changes)

### 上游更新

上游项目的发布、包更新或 CVE 修复会触发基础镜像的重建。这些构建会经过质量检查，以确保安全性和可靠性。

#### 监控更新

Docker 持续监控上游项目的新发布、包更新和安全公告。当检测到变更时，系统会使用符合 SLSA Build Level 3 标准的构建系统自动将受影响的镜像排队重建。

Docker 使用三种策略来跟踪更新：

- GitHub 发布：监控特定的 GitHub 仓库以获取新发布，并在发布新版本时自动更新镜像定义。
- GitHub 标签：跟踪 GitHub 仓库中的标签以检测新版本。
- 包仓库：通过 Docker Scout 的包数据库监控 Alpine Linux、Debian 和 Ubuntu 包仓库以检测更新的包。

除了显式的上游跟踪外，Docker 还监控传递依赖。当检测到包更新时（例如，库的安全补丁），Docker 会自动识别并重建支持窗口内使用该包的所有镜像。

### 定制变更 {tier="DHI Enterprise"}

{{< summary-bar feature_name="Docker Hardened Images" >}}

对您的 OCI 制品定制的更新会触发您的定制镜像的重建。

当您使用 DHI Enterprise 定制 DHI 镜像时，您的变更会被打包为 OCI 制品，这些制品会叠加在基础镜像之上。Docker 监控您的制品仓库，并在您推送更新时自动重建您的定制镜像。

重建流程会获取当前的基础镜像，应用您的 OCI 制品，签名结果并自动发布。您无需为定制镜像管理构建或维护 CI 流水线。

当依赖的基础 DHI 镜像收到更新时，定制镜像也会自动重建，确保您的镜像始终包含最新的安全补丁。

## 构建流水线

以下部分描述了基于以下内容的 Docker Hardened Images 构建流水线架构和工作流程：

- [基础镜像流水线](#base-image-pipeline)
- [定制镜像流水线](#customized-image-pipeline)

### 基础镜像流水线

每个 Docker Hardened Image 都通过自动化流水线构建：

1. 监控：Docker 监控上游源的更新（新发布、包更新、安全公告）。
2. 重建触发：检测到变更时，自动重建开始。
3. AI 守卫：AI 系统获取上游差异并使用语言感知检查进行扫描。守卫专注于可能导致重大问题的高杠杆问题，如反转错误检查、忽略失败、资源处理不当或可疑贡献者活动。当发现潜在风险时，它会阻止 PR 自动合并。
4. 人工审核：如果 AI 以高置信度识别出风险，Docker 工程师会审查标记的代码，重现问题并决定适当的行动。工程师经常向上游项目贡献修复，改善整个社区的代码。当修复被上游接受时，DHI 构建流水线会立即应用补丁以保护客户，同时修复在上游发布流程中传播。
5. 测试：镜像经过全面测试以确保兼容性和功能性。
6. 签名和证明：Docker 为每个镜像签名并生成证明（SBOM、VEX 文档、构建来源）。
7. 发布：已签名的镜像和证明发布到 Docker Hub。
8. 级联重建：如果任何定制镜像使用此基础镜像，它们的重建会自动触发。

Docker 对严重漏洞做出快速响应。通过从源代码构建关键组件而不是等待打包更新，Docker 可以在上游修复后的几天内修补严重和高严重性 CVE，并发布带有新证明的更新镜像。对于 DHI Enterprise 订阅，这种快速响应由严重和高严重性漏洞的 7 天 SLA 支持。

下图显示了基础镜像构建流程：

```goat {class="text-sm"}
.-------------------.      .-------------------.      .-------------------.      .-------------------.
| Docker monitors   |----->| Trigger rebuild   |----->| AI guardrail      |----->| Human review      |
| upstream sources  |      |                   |      | scans changes     |      |                   |
'-------------------'      '-------------------'      '-------------------'      '-------------------'
                                                                                           |
                                                                                           v
.-------------------.      .-------------------.      .-------------------.      .-------------------.
| Cascade rebuilds  |<-----| Publish to        |<-----| Sign & generate   |<-----| Testing           |
| (if needed)       |      | Docker Hub        |      | attestations      |      |                   |
'-------------------'      '-------------------'      '-------------------'      '-------------------'
```

### 定制镜像流水线 {tier="DHI Enterprise"}

{{< summary-bar feature_name="Docker Hardened Images" >}}

当您使用 DHI Enterprise 定制 DHI 镜像时，构建流程被简化：

1. 监控：Docker 监控您的 OCI 制品仓库的变更。
2. 重建触发：当您向 OCI 制品推送更新或基础 DHI 镜像更新时，自动重建开始。
3. 获取基础镜像：获取最新的基础 DHI 镜像。
4. 应用定制：将您的 OCI 制品应用到基础镜像。
5. 签名和证明：Docker 为定制镜像签名并生成证明（SBOM、VEX 文档、构建来源）。
6. 发布：已签名的定制镜像和证明发布到 Docker Hub。

Docker 自动处理整个流程，因此您无需为定制镜像管理构建。但是，您负责测试定制镜像并管理 OCI 制品引入的任何 CVE。

下图显示了定制镜像构建流程：

```goat {class="text-sm"}
.-------------------.      .-------------------.      .-------------------.
| Docker monitors   |----->| Trigger rebuild   |----->| Fetch base        |
| OCI artifacts     |      |                   |      | DHI image         |
'-------------------'      '-------------------'      '-------------------'
                                                               |
                                                               v
.-------------------.      .-------------------.      .-------------------.
| Publish to        |<-----| Sign & generate   |<-----| Apply             |
| Docker Hub        |      | attestations      |      | customizations    |
'-------------------'      '-------------------'      '-------------------'
```