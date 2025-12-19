---
title: Docker Scout 版本说明
linkTitle: 平台版本说明
description: 了解 Docker Scout 的最新功能
keywords: docker scout, release notes, changelog, features, changes, delta, new, releases
aliases:
- /scout/release-notes/
tags: [版本说明]
---

<!-- vale Docker.We = NO -->

本页包含 Docker Scout 各版本的新功能、改进、已知问题和错误修复信息。这些版本说明涵盖 Docker Scout 平台，包括仪表板。有关 CLI 版本说明，请参阅 [Docker Scout CLI 版本说明](./cli.md)。

## 2024 年第四季度

2024 年第四季度发布的新功能和增强功能。

### 2024-10-09

策略评估 已从早期访问 正式发布为正式版 。

Docker Scout 仪表板 UI 变更：

- 在 Docker Scout 仪表板上，选择策略卡现在会打开策略详情页面，而不是策略结果页面。
- 策略结果页面和策略详情侧边面板现在为只读。策略操作（编辑、禁用、删除）现在可以从策略详情页面访问。

## 2024 年第三季度

2024 年第三季度发布的新功能和增强功能。

### 2024-09-30

在此版本中，我们更改了自定义策略的工作方式。此前，自定义策略是通过复制开箱即用策略来创建的。现在，您可以通过编辑**策略类型** 的默认策略来自定义策略，这些类型充当模板。Docker Scout 中的默认策略同样基于这些类型实现。

有关更多信息，请参阅 [策略类型](/manuals/scout/policy/_index.md#policy-types)。

### 2024-09-09

此版本更改了 Docker Scout 中[健康度评分](/manuals/scout/policy/scores.md)的计算方式。健康度评分的计算现在会考虑您为组织配置的可选策略和自定义策略。

这意味着，如果您已启用、禁用或自定义了任何默认策略，Docker Scout 在计算您组织镜像的健康度评分时，现在会将这些策略纳入考虑范围。

如果您的组织尚未启用 Docker Scout，健康度评分将基于开箱即用策略进行计算。

### 2024-08-13

此版本更改了开箱即用策略，以使其与用于评估 Docker Scout [健康度评分](/manuals/scout/policy/scores.md)的策略配置保持一致。

现在默认的开箱即用策略包括：

- **No high-profile vulnerabilities**
- **No fixable critical or high vulnerabilities**
- **Approved Base Images**
- **Default non-root user**
- **Supply chain attestations**
- **Up-to-Date Base Images**
- **No AGPL v3 licenses**

这些策略的配置现在与用于计算健康度评分的配置相同。此前，开箱即用策略与健康度评分策略的配置是不同的。

## 2024 年第二季度

2024 年第二季度发布的新功能和增强功能。

### 2024-06-27

此版本为 Docker Scout 仪表板引入了**例外** 的初步支持。例外功能允许您使用 VEX 文档来屏蔽镜像中发现的漏洞（误报）。将 VEX 文档作为证明 附加到镜像，或将它们嵌入到镜像文件系统中，Docker Scout 将自动检测 VEX 声明并将其整合到镜像分析结果中。

新的[例外页面](https://scout.docker.com/reports/vex/)列出了影响您组织中所有镜像的例外。您也可以转到 Docker Scout 仪表板中的镜像视图，以查看应用于特定镜像的所有例外。

有关更多信息，请参阅 [管理漏洞例外](/manuals/scout/explore/exceptions.md)。

### 2024-05-06

新增了一个 HTTP 端点，允许您使用 Prometheus 从 Docker Scout 抓取数据，以便使用 Grafana 创建您自己的漏洞和策略仪表板。
有关更多信息，请参阅 [Docker Scout 指标导出器](/manuals/scout/explore/metrics-exporter.md)。

## 2024 年第一季度

2024 年第一季度发布的新功能和增强功能。

### 2024-03-29

**No high-profile vulnerabilities** 策略现在会报告 `xz` 后门漏洞 [CVE-2024-3094](https://scout.docker.com/v/CVE-2024-3094)。您的 Docker 组织中任何包含带有后门的 `xz/liblzma` 版本的镜像，都将不符合 **No high-profile vulnerabilities** 策略。

### 2024-03-20

**No fixable critical or high vulnerabilities** 策略现在支持**仅限可修复漏洞** 配置选项，您可以使用该选项来决定是否仅标记具有可用修复版本的漏洞。

### 2024-03-14

**All critical vulnerabilities** 策略已被移除。
**No fixable critical or high vulnerabilities** 策略提供了类似的功能，并将在未来更新以支持更广泛的定制，这使得现已移除的 **All critical vulnerabilities** 策略变得冗余。

### 2024-01-26

**Azure Container Registry** 集成已从[早期访问](../../release-lifecycle.md#early-access-ea) 正式发布为[正式版](../../release-lifecycle.md#genera-availability-ga)。

有关更多信息和设置说明，请参阅 [集成 Azure Container Registry](../integrations/registry/acr.md)。

### 2024-01-23

新增 **Approved Base Images** 策略，允许您限制构建中允许使用的基础镜像。您可以使用模式来定义允许的基础镜像。其镜像引用与指定模式不匹配的基础镜像将导致策略评估失败。

### 2024-01-12

新增 **Default non-root user** 策略，该策略会标记默认情况下以具有完整系统管理权限的 `root` 超级用户身份运行的镜像。为镜像指定非 root 默认用户有助于加强您的运行时安全性。

### 2024-01-11

[Beta](../../release-lifecycle.md#beta) 版发布了一款新的 GitHub 应用程序，用于将 Docker Scout 与您的源代码管理集成，并提供一项修复建议功能，以帮助您提高策略合规性。

修复建议是 Docker Scout 的一项新功能，它基于策略评估结果，提供上下文相关的、可推荐的操作，指导您如何提高合规性。

GitHub 集成增强了修复建议功能。启用集成后，Docker Scout 能够将分析结果与源代码关联起来。这种关于镜像构建方式的额外上下文，被用于生成更好、更精确的建议。

有关 Docker Scout 为帮助您提高策略合规性而可提供的建议类型，请参阅 [修复建议](../policy/remediation.md)。

有关如何在您的源代码仓库上授权 Docker Scout GitHub 应用程序的信息，请参阅 [将 Docker Scout 与 GitHub 集成](../integrations/source-code-management/github.md)。

## 2023 年第四季度

2023 年第四季度发布的新功能和增强功能。

### 2023-12-20

**Azure Container Registry** 集成已从 [Beta](../../release-lifecycle.md#beta) 版晋升至[早期访问](../../release-lifecycle.md#early-access-ea) 版。

有关更多信息和设置说明，请参阅 [集成 Azure Container Registry](../integrations/registry/acr.md)。

### 2023-12-06

新增 [SonarQube](https://www.sonarsource.com/products/sonarqube/) 集成及相关策略。SonarQube 是一个用于代码质量持续检查的开源平台。此集成允许您将 SonarQube 的质量门作为 Docker Scout 中的策略评估。启用集成，推送您的镜像，即可在新的 **SonarQube quality gates passed** 策略中看到 SonarQube 质量门条件。

### 2023-12-01

[Beta](../../release-lifecycle.md#beta) 版发布了一项新的 **Azure Container Registry** (ACR) 集成，该集成允许 Docker Scout 自动拉取和分析 ACR 仓库中的镜像。

要了解有关该集成及如何开始使用的更多信息，请参阅 [集成 Azure Container Registry](../integrations/registry/acr.md)。

### 2023-11-21

新增**可配置策略** 功能，使您可以根据自己的偏好调整开箱即用策略，或者在策略与您的需求不完全匹配时完全禁用它们。一些如何为您的组织调整策略的示例包括：

- 更改漏洞相关策略使用的严重性阈值
- 自定义“高危漏洞”列表
- 添加或移除要标记为“copyleft”的软件许可证

有关更多信息，请参阅 [可配置策略](../policy/configure.md)。

### 2023-11-10

新增 **Supply chain attestations** 策略，用于帮助您跟踪镜像是否使用 SBOM 和来源证明 构建。向镜像添加证明 是改善您的供应链行为良好性的良好第一步，并且通常是进行更多操作的先决条件。

### 2023-11-01

新增 **No high-profile vulnerabilities** 策略，确保您的制品不包含一个精选的、被广泛认为有风险的漏洞列表。

### 2023-10-04

这标志着 Docker Scout 正式版 的发布。

此版本包含以下新功能：

- [策略评估](#policy-evaluation) (早期访问)
- [Amazon ECR 集成](#amazon-ecr-integration)
- [Sysdig 集成](#sysdig-integration)
- [JFrog Artifactory 集成](#jfrog-artifactory-integration)

#### 策略评估

策略评估 是一项早期访问功能，可帮助您确保软件完整性并跟踪您的制品随时间变化的情况。此版本附带了四个开箱即用的策略，默认为所有组织启用。

![仪表板中的策略概览](../images/release-notes/policy-ea.webp)

- **Base images not up-to-date** 评估基础镜像是否过时，需要更新。最新的基础镜像有助于您确保环境的可靠性和安全性。
- **Critical and high vulnerabilities with fixes** 报告您的镜像中是否存在严重性为“严重”或“高危”的漏洞，以及是否有可升级的修复版本。
- **All critical vulnerabilities** 会查找您镜像中发现的任何“严重”级别的漏洞。
- **Packages with AGPLv3, GPLv3 license** 帮助您发现镜像中可能存在的不需要的 copyleft 许可证。

您可以使用 Docker Scout 仪表板和 `docker scout policy` CLI 命令来查看和评估镜像的策略状态。有关更多信息，请参阅 [策略评估文档](/scout/policy/)。

#### Amazon ECR 集成

新的 Amazon Elastic Container Registry (ECR) 集成可对托管在 ECR 仓库中的镜像进行分析。

您使用预配置的 CloudFormation 堆栈模板来设置集成，该模板会在您的账户中引导初始化必要的 AWS 资源。Docker Scout 会自动分析您推送到仓库的镜像，仅存储有关镜像内容的元数据，而不存储容器镜像本身。

该集成提供了一个简单直接的过程来添加额外的仓库、为特定仓库激活 Docker Scout，以及在需要时移除集成。要了解更多信息，请参阅 [Amazon ECR 集成文档](../integrations/registry/ecr.md)。

#### Sysdig 集成

新的 Sysdig 集成为您的 Kubernetes 运行时环境提供了实时安全洞见。

启用此集成有助于您解决和确定用于运行生产工作负载的镜像的风险优先级。它还通过使用 VEX 文档自动排除从未加载到内存中的程序中的漏洞，来帮助减少监控噪音。

有关更多信息和入门指南，请参阅 [Sysdig 集成文档](../integrations/environment/sysdig.md)。

#### JFrog Artifactory 集成

新的 JFrog Artifactory 集成可对 Artifactory 注册表上的镜像进行自动分析。

该集成涉及部署一个 Docker Scout Artifactory 代理，该代理会轮询新镜像、执行分析并将结果上传到 Docker Scout，同时保持镜像数据的完整性。

#### 已知限制

- 镜像分析仅适用于 Linux 镜像
- Docker Scout 无法处理压缩大小超过 12GB 的镜像
- 创建镜像 SBOM（镜像分析的一部分）的超时限制为 4 分钟