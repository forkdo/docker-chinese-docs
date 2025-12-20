# Docker Scout 发布说明
<!-- vale Docker.We = NO -->

本页面包含有关 Docker Scout 版本中的新功能、改进、已知问题和错误修复的信息。这些发布说明涵盖了 Docker Scout 平台，包括仪表盘。有关 CLI 发布说明，请参阅 [Docker Scout CLI 发布说明](./cli.md)。

## 2024 年第四季度

2024 年第四季度发布的新功能和增强功能。

### 2024-10-09

策略评估已从早期访问阶段毕业，进入正式发布阶段。

Docker Scout 仪表盘 UI 变更：

- 在 Docker Scout 仪表盘上，选择策略卡片现在会打开策略详情页面，而不是策略结果页面。
- 策略结果页面和策略详情侧边面板现在为只读。策略操作（编辑、禁用、删除）现在可以从策略详情页面访问。

## 2024 年第三季度

2024 年第三季度发布的新功能和增强功能。

### 2024-09-30

在此版本中，我们更改了自定义策略的工作方式。以前，自定义策略是通过复制开箱即用的策略来创建的。现在，您可以通过编辑来自**策略类型**的默认策略来自定义策略，该策略类型充当模板。Docker Scout 中的默认策略也是基于这些类型实现的。

有关更多信息，请参阅 [策略类型](/manuals/scout/policy/_index.md#policy-types)。

### 2024-09-09

此版本更改了 Docker Scout 中[健康评分](/manuals/scout/policy/scores.md)的计算方式。健康评分计算现在会考虑您为组织配置的可选策略和自定义策略。

这意味着，如果您已启用、禁用或自定义了任何默认策略，Docker Scout 在计算您组织镜像的健康评分时现在会将这些策略考虑在内。

如果您尚未为您的组织启用 Docker Scout，健康评分计算将基于开箱即用的策略。

### 2024-08-13

此版本更改了开箱即用的策略，以使其与用于评估 Docker Scout [健康评分](/manuals/scout/policy/scores.md)的策略配置保持一致。

默认的开箱即用策略现在是：

- **无高调漏洞**
- **无可修复的严重或高危漏洞**
- **已批准的基础镜像**
- **默认非 root 用户**
- **供应链证明**
- **最新的基础镜像**
- **无 AGPL v3 许可证**

这些策略的配置现在与用于计算健康评分的配置相同。以前，开箱即用策略的配置与健康评分策略的配置不同。

## 2024 年第二季度

2024 年第二季度发布的新功能和增强功能。

### 2024-06-27

此版本在 Docker Scout 仪表盘中引入了对**例外**的初步支持。例外功能允许您使用 VEX 文档来抑制在镜像中发现的漏洞（误报）。将 VEX 文档作为证明附加到镜像，或将其嵌入到镜像文件系统中，Docker Scout 将自动检测并将 VEX 语句合并到镜像分析结果中。

新的[例外页面](https://scout.docker.com/reports/vex/)列出了影响您组织中镜像的所有例外。您也可以转到 Docker Scout 仪表盘中的镜像视图，以查看应用于给定镜像的所有例外。

有关更多信息，请参阅[管理漏洞例外](/manuals/scout/explore/exceptions.md)。

### 2024-05-06

新的 HTTP 端点，允许您使用 Prometheus 从 Docker Scout 抓取数据，以便使用 Grafana 创建您自己的漏洞和策略仪表盘。
有关更多信息，请参阅 [Docker Scout 指标导出器](/manuals/scout/explore/metrics-exporter.md)。

## 2024 年第一季度

2024 年第一季度发布的新功能和增强功能。

### 2024-03-29

**无高调漏洞**策略现在报告 `xz` 后门漏洞 [CVE-2024-3094](https://scout.docker.com/v/CVE-2024-3094)。您的 Docker 组织中任何包含带有后门的 `xz/liblzma` 版本的镜像都将不符合**无高调漏洞**策略的要求。

### 2024-03-20

**无可修复的严重或高危漏洞**策略现在支持**仅限可修复漏洞**配置选项，该选项允许您决定是否仅标记具有可用修复版本的漏洞。

### 2024-03-14

**所有严重漏洞**策略已被移除。
**无可修复的严重或高危漏洞**策略提供了类似的功能，并将在未来更新以允许进行更广泛的定制，从而使现已移除的**所有严重漏洞**策略变得多余。

### 2024-01-26

**Azure Container Registry** 集成已从[早期访问](../../release-lifecycle.md#early-access-ea)阶段毕业，进入[正式发布](../../release-lifecycle.md#genera-availability-ga)阶段。

有关更多信息 and 设置说明，请参阅[集成 Azure Container Registry](../integrations/registry/acr.md)。

### 2024-01-23

新的**已批准的基础镜像**策略，允许您限制在构建中允许使用哪些基础镜像。您可以使用模式定义允许的基础镜像。其镜像引用与指定模式不匹配的基础镜像将导致策略失败。

### 2024-01-12

新的**默认非 root 用户**策略，该策略会标记默认情况下将以具有完整系统管理权限的 `root` 超级用户身份运行的镜像。为您的镜像指定非 root 默认用户有助于加强您的运行时安全。

### 2024-01-11

用于将 Docker Scout 与您的源代码管理集成的全新 GitHub 应用程序[Beta](../../release-lifecycle.md#beta)版发布，以及一个帮助您提高策略合规性的修复建议功能。

修复建议是 Docker Scout 的一项新功能，可根据策略评估结果提供上下文相关的推荐操作，指导您如何提高合规性。

GitHub 集成增强了修复建议功能。启用集成后，Docker Scout 能够将分析结果与源代码关联起来。这种关于镜像构建方式的额外上下文被用于生成更好、更精确的推荐。

有关 Docker Scout 可提供哪些类型的推荐来帮助您提高策略合规性的更多信息，请参阅[修复建议](../policy/remediation.md)。

有关如何在您的源代码存储库上授权 Docker Scout GitHub 应用程序的更多信息，请参阅[将 Docker Scout 与 GitHub 集成](../integrations/source-code-management/github.md)。

## 2023 年第四季度

2023 年第四季度发布的新功能和增强功能。

### 2023-12-20

**Azure Container Registry** 集成已从[Beta](../../release-lifecycle.md#beta)版毕业，进入[早期访问](../../release-lifecycle.md#early-access-ea)阶段。

有关更多信息 and 设置说明，请参阅[集成 Azure Container Registry](../integrations/registry/acr.md)。

### 2023-12-06

新的 [SonarQube](https://www.sonarsource.com/products/sonarqube/) 集成及相关策略。SonarQube 是一个用于持续检查代码质量的开源平台。此集成允许您将 SonarQube 的质量门作为 Docker Scout 中的策略评估。启用集成，推送您的镜像，然后在新的**SonarQube 质量门通过**策略中查看 SonarQube 质量门条件。

### 2023-12-01

全新的 **Azure Container Registry** (ACR) 集成的[Beta](../../release-lifecycle.md#beta)版发布，该集成允许 Docker Scout 自动拉取和分析 ACR 存储库中的镜像。

要了解有关该集成以及如何开始使用的更多信息，请参阅[集成 Azure Container Registry](../integrations/registry/acr.md)。

### 2023-11-21

新的**可配置策略**功能，使您能够根据自己的偏好调整开箱即用的策略，或者在它们不完全符合您的要求时完全禁用它们。一些如何为您的组织调整策略的示例包括：

- 更改漏洞相关策略使用的严重性阈值
- 自定义“高调漏洞”列表
- 添加或移除要标记为“著佐权”的软件许可证

有关更多信息，请参阅[可配置策略](../policy/configure.md)。

### 2023-11-10

新的**供应链证明**策略，帮助您跟踪镜像是否使用 SBOM 和来源证明构建。向镜像添加证明是改善供应链行为良好的第一步，并且通常是进行更多操作的先决条件。

### 2023-11-01

新的**无高调漏洞**策略，确保您的制品不包含一个经过精心策划的、被广泛认为有风险的漏洞列表。

### 2023-10-04

这标志着 Docker Scout 的正式发布 (GA) 版本。

此版本包含以下新功能：

- [策略评估](#policy-evaluation) (早期访问)
- [Amazon ECR 集成](#amazon-ecr-integration)
- [Sysdig 集成](#sysdig-integration)
- [JFrog Artifactory 集成](#jfrog-artifactory-integration)

#### 策略评估

策略评估是一个早期访问功能，可帮助您确保软件完整性并跟踪您的制品随时间的变化情况。此版本附带了四个开箱即用的策略，默认为所有组织启用。

![仪表盘中的策略概览](../images/release-notes/policy-ea.webp)

- **基础镜像未更新**评估基础镜像是否过时，需要更新。最新的基础镜像有助于确保您的环境可靠和安全。
- **有修复版本的严重和高危漏洞**报告您的镜像中是否存在严重或高危级别的漏洞，以及是否有可以升级到的修复版本。
- **所有严重漏洞**会查找在您的镜像中发现的任何严重级别的漏洞。
- **具有 AGPLv3、GPLv3 许可证的包**帮助您捕获镜像中可能不需要的著佐权许可证。

您可以使用 Docker Scout 仪表盘和 `docker scout policy` CLI 命令来查看和评估镜像的策略状态。有关更多信息，请参阅[策略评估文档](/scout/policy/)。

#### Amazon ECR 集成

新的 Amazon Elastic Container Registry (ECR) 集成支持对托管在 ECR 存储库中的镜像进行分析。

您可以使用预配置的 CloudFormation 堆栈模板来设置集成，该模板会在您的账户中引导启动必要的 AWS 资源。Docker Scout 会自动分析您推送到注册表的镜像，仅存储有关镜像内容的元数据，而不存储容器镜像本身。

该集成提供了一个简单直接的过程来添加额外的存储库、为特定存储库激活 Docker Scout，以及在需要时移除集成。要了解更多信息，请参阅 [Amazon ECR 集成文档](../integrations/registry/ecr.md)。

#### Sysdig 集成

新的 Sysdig 集成为您的 Kubernetes 运行时环境提供实时安全洞察。

启用此集成有助于您解决和确定用于运行生产工作负载的镜像的风险优先级。它还通过使用 VEX 文档自动排除从未加载到内存中的程序中的漏洞，来帮助减少监控噪音。

有关更多信息和入门指南，请参阅 [Sysdig 集成文档](../integrations/environment/sysdig.md)。

#### JFrog Artifactory 集成

新的 JFrog Artifactory 集成支持对 Artifactory 注册表上的镜像进行自动分析。

该集成涉及部署一个 Docker Scout Artifactory 代理，该代理会轮询新镜像、执行分析并将结果上传到 Docker Scout，同时在此过程中保持镜像数据的完整性。

#### 已知限制

- 镜像分析仅适用于 Linux 镜像
- Docker Scout 无法处理压缩后大小超过 12GB 的镜像
- 创建镜像 SBOM（镜像分析的一部分）有 4 分钟的超时限制
