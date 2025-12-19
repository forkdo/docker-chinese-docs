---
description: Docker Scout 仪表板可帮助您审查和共享镜像分析结果。
keywords: scout, scanning, analysis, vulnerabilities, Hub, supply chain, security, report, reports, dashboard
title: 仪表板
aliases:
- /scout/reports/
- /scout/web-app/
- /scout/dashboard/
---

[Docker Scout 仪表板](https://scout.docker.com/)可帮助您与团队共享组织中镜像的分析结果。开发人员现在可以查看 Docker Hub 上所有镜像的安全状态概览，并随时获取修复建议。它可帮助安全、合规和运维等角色的团队成员了解需要重点关注的漏洞和问题。

## 概览

![Docker Scout 仪表板概览截图](../images/dashboard-overview.webp?border=true)

**概览**选项卡为所选组织中的仓库提供摘要信息。

在此页面顶部，您可以选择要查看的**环境**。默认情况下，显示最近推送的镜像。要了解有关环境的更多信息，请参阅[环境监控](/manuals/scout/integrations/environment/_index.md)。

**策略**框显示您当前针对每个策略的合规性评级，以及所选环境的趋势指示。趋势描述了最近镜像与上一版本相比的策略变化。有关策略的更多信息，请参阅[策略评估](/manuals/scout/policy/_index.md)。

漏洞图表显示所选环境中镜像随时间变化的总漏洞数。您可以使用下拉菜单配置图表的时间范围。

使用网站顶部的标题菜单访问 Docker Scout 仪表板的不同主要部分：

- **策略**：显示组织的策略合规性，请参阅[策略](#policies)
- **镜像**：列出组织中所有启用了 Docker Scout 的仓库，请参阅[镜像](#images)
- **基础镜像**：列出组织中仓库使用的所有基础镜像
- **软件包**：列出组织中所有仓库的软件包
- **漏洞**：列出组织镜像中的所有 CVE，请参阅[漏洞](#vulnerabilities)
- **集成**：创建和管理第三方集成，请参阅[集成](#integrations)
- **设置**：管理仓库设置，请参阅[设置](#settings)

## 策略

**策略**视图显示所选组织和环境所有镜像的策略合规性细分。您可以使用**镜像**下拉菜单查看特定环境的策略细分。

有关策略的更多信息，请参阅[策略评估](/manuals/scout/policy/_index.md)。

## 镜像

**镜像**视图显示所选环境启用了 Scout 的仓库中的所有镜像。您可以通过选择不同的环境或使用文本过滤器按仓库名称来过滤列表。

![镜像视图截图](../images/dashboard-images.webp)

对于每个仓库，列表显示以下详细信息：

- 仓库名称（不含标签或摘要的镜像引用）
- 所选环境中镜像的最新标签
- 最新标签的操作系统和架构
- 最新标签的漏洞状态
- 最新标签的策略状态

选择仓库链接将带您进入该仓库中所有已分析镜像的列表。在此，您可以查看特定镜像的完整分析结果，并比较标签以查看软件包和漏洞的差异。

选择镜像链接将带您进入所选标签或摘要的详细信息视图。此视图包含两个选项卡，详细说明镜像的组成和策略合规性：

- **策略状态**显示所选镜像的策略评估结果。此处还提供有关策略违规的详细信息链接。

  有关策略的更多信息，请参阅[策略评估](/manuals/scout/policy/_index.md)。

- **镜像层**显示镜像分析结果的细分。您可以完整查看镜像包含的漏洞，并了解它们是如何引入的。

## 漏洞

**漏洞**视图显示组织中镜像的所有漏洞列表。此列表包括有关 CVE 的详细信息，例如严重性和通用漏洞评分系统 (CVSS) 分数，以及是否有可用的修复版本。此处显示的 CVSS 分数是所有可用[来源](/manuals/scout/deep-dive/advisory-db-sources.md)中的最高分数。

选择此页面上的链接将打开漏洞详细信息页面。此页面是公开可见的页面，显示有关 CVE 的详细信息。您可以将特定 CVE 描述的链接共享给其他人，即使他们不是您的 Docker 组织成员或未登录 Docker Scout。

如果您已登录，此页面上的**我的镜像**选项卡会列出受 CVE 影响的所有镜像。

## 集成

**集成**页面允许您创建和管理 Docker Scout 集成，例如环境集成和注册表集成。有关如何开始使用集成的信息，请参阅[将 Docker Scout 与其他系统集成](/manuals/scout/integrations/_index.md)。

## 设置

Docker Scout 仪表板中的设置菜单包含：

- [**仓库设置**](#repository-settings)，用于启用和禁用仓库
- [**通知**](#notification-settings)，用于管理 Docker Scout 的通知首选项。

### 仓库设置

为仓库启用 Docker Scout 后，当您推送到该仓库时，Docker Scout 会自动分析新标签。要在 Amazon ECR、Azure ACR 或其他第三方注册表中启用仓库，首先需要集成它们。请参阅[容器注册表集成](/manuals/scout/integrations/_index.md#container-registries)。

### 通知设置

[通知设置](https://scout.docker.com/settings/notifications)页面是您可以更改接收 Docker Scout 通知首选项的位置。通知设置是个人设置，更改通知设置仅影响您的个人账户，而不影响整个组织。

Docker Scout 中通知的目的是提高您对影响您的上游更改的认识。Docker Scout 会在安全公告中披露新漏洞并影响您的一个或多个镜像时通知您。您不会收到因推送新镜像而导致的漏洞暴露或策略合规性更改的通知。

> [!NOTE]
>
> 通知仅针对每个仓库的*最后推送*镜像标签触发。“最后推送”指的是最近推送到注册表并由 Docker Scout 分析的镜像标签。如果最后推送的镜像不受新披露的 CVE 影响，则不会触发通知。

可用的通知设置包括：

- **仓库范围**

  在此，您可以选择是否为所有仓库或仅特定仓库启用通知。这些设置适用于当前选定的组织，并且可以为您所属的每个组织进行更改。

  - **所有仓库**：选择此选项以接收您有权访问的所有仓库的通知。
  - **特定仓库**：选择此选项以接收特定仓库的通知。然后，您可以输入要接收通知的仓库名称。

- **传递首选项**

  这些设置控制您如何接收 Docker Scout 的通知。它们适用于您所属的所有组织。

  - **通知弹出窗口**：选中此复选框以在 Docker Scout 仪表板中接收通知弹出消息。
  - **操作系统通知**：选中此复选框以在浏览器标签中打开 Docker Scout 仪表板时从浏览器接收操作系统级通知。
  
  要启用操作系统通知，Docker Scout 需要权限以使用浏览器 API 发送通知。

在此页面，您还可以转到团队协作集成的设置，例如 [Slack](/manuals/scout/integrations/team-collaboration/slack.md) 集成。

您还可以通过转到**设置** > **通知**在 Docker Desktop 中配置通知设置。