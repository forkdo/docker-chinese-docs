---
title: Docker Scout 发布说明
linkTitle: 平台发布说明
description: 了解 Docker Scout 的最新功能
keywords: docker scout, release notes, changelog, features, changes, delta, new, releases
aliases:
- /scout/release-notes/
tags: [Release notes]
---

<!-- vale Docker.We = NO -->

本页面包含 Docker Scout 发布中的新功能、改进、已知问题和错误修复信息。这些发布说明涵盖 Docker Scout 平台，包括仪表板。如需 CLI 发布说明，请参阅 [Docker Scout CLI 发布说明](./cli.md)。

## 2024 年第四季度

2024 年第四季度发布的新功能和增强功能。

### 2024-10-09

Policy Evaluation 从早期访问（Early Access）阶段毕业，进入正式发布（General Availability）。

Docker Scout 仪表板 UI 变更：

- 在 Docker Scout 仪表板上，选择策略卡片现在会打开策略详情页面，而不是策略结果页面。
- 策略结果页面和策略详情侧边面板现在为只读模式。策略操作（编辑、禁用、删除）现在可从策略详情页面访问。

## 2024 年第三季度

2024 年第三季度发布的新功能和增强功能。

### 2024-09-30

本次发布更改了自定义策略的工作方式。之前，自定义策略是通过复制开箱即用的策略创建的。现在，您可以通过从作为模板的**策略类型**编辑默认策略来自定义策略。Docker Scout 中的默认策略也基于这些类型实现。

更多信息，请参阅 [策略类型](/manuals/scout/policy/_index.md#policy-types)。

### 2024-09-09

本次发布更改了 Docker Scout 中 [健康分数](/manuals/scout/policy/scores.md) 的计算方式。健康分数计算现在会考虑您为组织配置的可选和自定义策略。

这意味着，如果您已启用、禁用或自定义了任何默认策略，Docker Scout 现在会在计算组织镜像的健康分数时考虑这些策略。

如果您尚未为组织启用 Docker Scout，健康分数计算将基于开箱即用的策略。

### 2024-08-13

本次发布更改了开箱即用的策略，以与用于评估 Docker Scout [健康分数](/manuals/scout/policy/scores.md) 的策略配置保持一致。

现在默认的开箱即用策略为：

- **无高风险漏洞**
- **无可修复的关键或高严重性漏洞**
- **已批准的基础镜像**
- **默认非 root 用户**
- **供应链证明**
- **最新的基础镜像**
- **无 AGPL v3 许可证**

这些策略的配置现在与用于计算健康分数的配置相同。之前，开箱即用的策略配置与健康分数策略不同。

## 2024 年第二季度

2024 年第二季度发布的新功能和增强功能。

### 2024-06-27

本次发布在 Docker Scout 仪表板中引入了 **Exceptions** 的初始支持。Exceptions 允许您使用 VEX 文档抑制在镜像中发现的漏洞（误报）。将 VEX 文档作为证明附加到镜像上，或嵌入到镜像文件系统中，Docker Scout 会自动检测并将 VEX 语句合并到镜像分析结果中。

新的 [Exceptions 页面](https://scout.docker.com/reports/vex/) 列出了影响组织中镜像的所有 exceptions。您也可以在 Docker Scout 仪表板的镜像视图中查看适用于特定镜像的所有 exceptions。

更多信息，请参阅 [管理漏洞例外](/manuals/scout/explore/exceptions.md)。

### 2024-05-06

新增 HTTP 端点，允许您使用 Prometheus 从 Docker Scout 抓取数据，以便使用 Grafana 创建自己的漏洞和策略仪表板。更多信息，请参阅 [Docker Scout 指标导出器](/manuals/scout/explore/metrics-exporter.md)。

## 2024 年第一季度

2024 年第一季度发布的新功能和增强功能。

### 2024-03-29

**无高风险漏洞** 策略现在报告 `xz` 后门漏洞 [CVE-2024-3094](https://scout.docker.com/v/CVE-2024-3094)。您 Docker 组织中包含带有后门的 `xz/liblzma` 版本的任何镜像都将不符合 **无高风险漏洞** 策略。

### 2024-03-20

**无可修复的关键或高严重性漏洞** 策略现在支持 **仅可修复漏洞** 配置选项，允许您决定是否仅标记有可用修复版本的漏洞。

### 2024-03-14

**所有关键漏洞** 策略已被移除。**无可修复的关键或高严重性漏洞** 策略提供类似功能，并将在未来更新以允许更广泛的自定义，使现在移除的 **所有关键漏洞** 策略变得多余。

### 2024-01-26

**Azure 容器注册表** 集成从 [早期访问](../../release-lifecycle.md#early-access-ea) 毕业至 [正式发布](../../release-lifecycle.md#genera-availability-ga)。

更多信息和设置说明，请参阅 [集成 Azure 容器注册表](../integrations/registry/acr.md)。

### 2024-01-23

新增 **已批准的基础镜像** 策略，允许您限制构建中允许的基础镜像。您使用模式定义允许的基础镜像。镜像引用不匹配指定模式的基础镜像将导致策略失败。

### 2024-01-12

新增 **默认非 root 用户** 策略，标记默认以 `root` 超级用户身份运行并具有完全系统管理权限的镜像。为镜像指定非 root 默认用户有助于加强运行时安全性。

### 2024-01-11

[Beta](../../release-lifecycle.md#beta) 发布新的 GitHub 应用，用于将 Docker Scout 与源代码管理集成，以及提供帮助改善策略合规性的修复功能。

修复是 Docker Scout 的新功能，可根据策略评估结果提供上下文相关的推荐操作，帮助您改善合规性。

GitHub 集成增强了修复功能。启用集成后，Docker Scout 能够将分析结果连接到源代码。关于镜像构建方式的额外上下文用于生成更好、更精确的建议。

有关 Docker Scout 可提供哪些类型的建议以帮助改善策略合规性的更多信息，请参阅 [修复](../policy/remediation.md)。

有关如何在源代码仓库中授权 Docker Scout GitHub 应用的更多信息，请参阅 [将 Docker Scout 与 GitHub 集成](../integrations/source-code-management/github.md)。

## 2023 年第四季度

2023 年第四季度发布的新功能和增强功能。

### 2023-12-20

**Azure 容器注册表** 集成从 [Beta](../../release-lifecycle.md#beta) 毕业至 [早期访问](../../release-lifecycle.md#early-access-ea)。

更多信息和设置说明，请参阅 [集成 Azure 容器注册表](../integrations/registry/acr.md)。

### 2023-12-06

新增 [SonarQube](https://www.sonarsource.com/products/sonarqube/) 集成及相关策略。SonarQube 是一个用于代码质量连续检查的开源平台。此集成允许您将 SonarQube 的质量门作为策略评估添加到 Docker Scout 中。启用集成，推送镜像，即可在新的 **SonarQube 质量门通过** 策略中看到 SonarQube 质量门条件。

### 2023-12-01

[Beta](../../release-lifecycle.md#beta) 发布新的 **Azure 容器注册表** (ACR) 集成，允许 Docker Scout 自动拉取和分析 ACR 仓库中的镜像。

如需了解集成信息和入门方法，请参阅 [集成 Azure 容器注册表](../integrations/registry/acr.md)。

### 2023-11-21

新增 **可配置策略** 功能，允许您根据偏好调整开箱即用的策略，或在策略不完全符合需求时完全禁用。您可以为组织调整策略的一些示例包括：

- 更改漏洞相关策略使用的严重性阈值
- 自定义"高风险漏洞"列表
- 添加或删除要标记为"著佐权"的软件许可证

更多信息，请参阅 [可配置策略](../policy/configure.md)。

### 2023-11-10

新增 **供应链证明** 策略，帮助您跟踪镜像是否使用 SBOM 和来源证明构建。为镜像添加证明是改善供应链行为的良好第一步，通常也是执行更多操作的先决条件。

### 2023-11-01

新增 **无高风险漏洞** 策略，确保您的制品免于一个经过策划的、被广泛认为有风险的漏洞列表。

### 2023-10-04

这标志着 Docker Scout 的正式发布 (GA)。

本次发布包含以下新功能：

- [策略评估](#policy-evaluation)（早期访问）
- [Amazon ECR 集成](#amazon-ecr-integration)
- [Sysdig 集成](#sysdig-integration)
- [JFrog Artifactory 集成](#jfrog-artifactory-integration)

#### 策略评估

策略评估是一个早期访问功能，帮助您确保软件完整性并跟踪制品的状态变化。本次发布包含四个开箱即用的策略，默认为所有组织启用。

![Policy overview in Dashboard](../images/release-notes/policy-ea.webp)

- **基础镜像未更新** 评估基础镜像是否过期，需要更新。最新的基础镜像有助于确保您的环境可靠且安全。
- **关键和高严重性漏洞可修复** 报告镜像中是否存在关键或高严重性漏洞，以及是否有可用的修复版本可升级。
- **所有关键漏洞** 监控镜像中发现的任何关键严重性漏洞。
- **包含 AGPLv3、GPLv3 许可证的软件包** 帮助您发现镜像中可能不需要的著佐权许可证。

您可以使用 Docker Scout 仪表板和 `docker scout policy` CLI 命令查看和评估镜像的策略状态。更多信息，请参阅 [策略评估文档](/scout/policy/)。

#### Amazon ECR 集成

新的 Amazon Elastic Container Registry (ECR) 集成支持分析托管在 ECR 仓库中的镜像。

您使用预配置的 CloudFormation 堆栈模板设置集成，该模板在您的账户中引导必要的 AWS 资源。Docker Scout 自动分析您推送到注册表的镜像，仅存储镜像内容的元数据，而不存储容器镜像本身。

该集成提供了添加额外仓库、为特定仓库激活 Docker Scout 以及在需要时移除集成的直接流程。更多信息，请参阅 [Amazon ECR 集成文档](../integrations/registry/ecr.md)。

#### Sysdig 集成

新的 Sysdig 集成为您的 Kubernetes 运行时环境提供实时安全洞察。

启用此集成有助于您解决和优先处理用于运行生产工作负载的镜像的风险。它还通过使用 VEX 文档自动排除从不加载到内存中的程序中的漏洞来帮助减少监控噪音。

更多信息和入门指南，请参阅 [Sysdig 集成文档](../integrations/environment/sysdig.md)。

#### JFrog Artifactory 集成

新的 JFrog Artifactory 集成支持在 Artifactory 注册表上自动镜像分析。

该集成涉及部署 Docker Scout Artifactory 代理，该代理轮询新镜像，执行分析并将结果上传到 Docker Scout，同时保持镜像数据的完整性。

#### 已知限制

- 镜像分析仅适用于 Linux 镜像
- Docker Scout 无法处理压缩大小超过 12GB 的镜像
- 创建镜像 SBOM（镜像分析的一部分）的超时限制为 4 分钟