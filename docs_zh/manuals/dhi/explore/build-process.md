---
title: Docker 强化镜像的构建方式
linkTitle: 构建流程
description: 了解 Docker 如何通过自动化、注重安全的流水线来构建、测试和维护 Docker 强化镜像。
keywords: docker hardened images, slsa build level 3, automated patching, ai guardrail, build process, signed sbom, supply chain security
weight: 15
aliases:
  - /dhi/about/build-process/
---

Docker 强化镜像通过自动化流水线构建，该流水线监控上游源、应用安全更新并发布已签名的构件。本页面解释了基础 DHI 镜像和 DHI Enterprise 定制镜像的构建流程。

通过 DHI Enterprise 订阅，基础镜像和定制镜像的自动化安全更新流水线均由 SLA 承诺提供支持，包括针对严重和高危漏洞的 7 天 SLA。仅 DHI Enterprise 包含 SLA。DHI Free 提供安全基线，但不保证修复时间表。

## 构建触发器

构建会自动开始。您无需手动触发它们。系统会监控变化并在以下两种场景下启动构建：

- [上游更新](#upstream-updates)
- [定制变更](#customization-changes)

### 上游更新

上游项目的新版本发布、软件包更新或 CVE 修复会触发基础镜像的重新构建。这些构建会经过质量检查，以确保安全性和可靠性。

#### 监控更新

Docker 持续监控上游项目的新版本发布、软件包更新和安全公告。当检测到变化时，系统会使用符合 SLSA 构建级别 3 (SLSA Build Level 3) 的构建系统自动将受影响的镜像加入重建队列。

Docker 使用三种策略来跟踪更新：

- GitHub releases：监控特定的 GitHub 仓库以获取新版本发布，并在发布新版本时自动更新镜像定义。
- GitHub tags：跟踪 GitHub 仓库中的标签以检测新版本。
- Package repositories：通过 Docker Scout 的软件包数据库监控 Alpine Linux、Debian 和 Ubuntu 软件包仓库，以检测已更新的软件包。

除了显式的上游跟踪外，Docker 还监控传递性依赖项。当检测到软件包更新时（例如，针对库的安全补丁），Docker 会自动识别并重建支持窗口内使用该软件包的所有镜像。

### 定制变更 {tier="DHI Enterprise"}

{{< summary-bar feature_name="Docker Hardened Images" >}}

对您的 OCI 构件定制的更新会触发您的定制镜像的重新构建。

当您使用 DHI Enterprise 定制 DHI 镜像时，您的更改被打包为叠加在基础镜像之上的 OCI 构件。Docker 会监控您的构件仓库，并在您推送更新时自动重建您的定制镜像。

重建过程会获取当前的基础镜像，应用您的 OCI 构件，对结果进行签名，然后自动发布。您无需管理构建或为您的定制镜像维护 CI 流水线。

当其所依赖的基础 DHI 镜像收到更新时，定制镜像也会自动重建，以确保您的镜像始终包含最新的安全补丁。

## 构建流水线

以下各节描述了基于以下内容的 Docker 强化镜像的构建流水线架构和工作流：

- [基础镜像流水线](#base-image-pipeline)
- [定制镜像流水线](#customized-image-pipeline)

### 基础镜像流水线

每个 Docker 强化镜像都通过自动化流水线构建：

1. 监控：Docker 监控上游源的更新（新版本发布、软件包更新、安全公告）。
2. 重建触发器：当检测到变化时，自动重建开始。
3. AI 防护：AI 系统获取上游差异并使用语言感知检查对其进行扫描。防护机制专注于可能引发重大问题的高杠杆问题，例如错误检查反转、被忽略的失败、资源处理不当或可疑的贡献者活动。当它发现潜在风险时，会阻止 PR 自动合并。
4. 人工审查：如果 AI 以高置信度识别出风险，Docker 工程师会审查标记的代码，重现问题，并决定采取适当的行动。工程师通常会将修复贡献回上游项目，从而改进整个社区的代码。当修复被上游接受后，DHI 构建流水线会立即应用该补丁，以便在修复通过上游发布流程期间保护客户。
5. 测试：镜像会经过全面的兼容性和功能测试。
6. 签名和证明：Docker 对每个镜像进行签名并生成证明（SBOM、VEX 文档、构建来源）。
7. 发布：已签名的镜像和证明会发布到 Docker Hub。
8. 级联重建：如果有任何定制镜像使用此基础镜像，它们的重建将自动触发。

Docker 对严重漏洞响应迅速。通过从源代码构建关键组件，而不是等待打包的更新，Docker 可以在上游修复后的几天内修补严重和高危 CVE，并发布带有新证明的更新镜像。对于 DHI Enterprise 订阅，这种快速响应由针对严重和高危漏洞的 7 天 SLA 提供支持。

下图显示了基础镜像的构建流程：

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

当您使用 DHI Enterprise 定制 DHI 镜像时，构建过程会得到简化：

1. 监控：Docker 监控您的 OCI 构件仓库的变更。
2. 重建触发器：当您向 OCI 构件推送更新，或者基础 DHI 镜像更新时，自动重建开始。
3. 获取基础镜像：获取最新的基础 DHI 镜像。
4. 应用定制：将您的 OCI 构件应用到基础镜像上。
5. 签名和证明：Docker 对定制镜像进行签名并生成证明（SBOM、VEX 文档、构建来源）。
6. 发布：已签名的定制镜像和证明会发布到 Docker Hub。

Docker 自动处理整个过程，因此您无需管理定制镜像的构建。但是，您有责任测试您的定制镜像并管理由您的 OCI 构件引入的任何 CVE。

下图显示了定制镜像的构建流程：

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