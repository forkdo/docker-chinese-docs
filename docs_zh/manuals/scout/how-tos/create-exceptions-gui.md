---
title: 使用 GUI 创建例外
description: 使用 Docker Scout Dashboard 或 Docker Desktop 为镜像中的漏洞创建例外。
keywords: Docker, Docker Scout, Docker Desktop, 漏洞, 例外, 创建, GUI
---

Docker Scout Dashboard 和 Docker Desktop 提供了用户友好的界面，用于为容器镜像中发现的[例外](/manuals/scout/explore/exceptions.md)创建例外。例外可让您确认已接受的风险或解决镜像分析中的误报。

## 先决条件

要在 Docker Scout Dashboard 或 Docker Desktop 中创建例外，您需要一个 Docker 账户，该账户对拥有镜像的 Docker 组织拥有 **Editor** 或 **Owner** 权限。

## 步骤

使用 Docker Scout Dashboard 或 Docker Desktop 为镜像中的漏洞创建例外：

{{< tabs >}}
{{< tab name="Docker Scout Dashboard" >}}

1. 前往 [Images 页面](https://scout.docker.com/reports/images)。
2. 选择包含您要为其创建例外的漏洞的镜像标签。
3. 打开 **Image layers** 选项卡。
4. 选择包含您要为其创建例外的漏洞的层。
5. 在 **Vulnerabilities** 选项卡中，找到您要为其创建例外的漏洞。漏洞按软件包分组。找到包含您要为其创建例外的漏洞的软件包，然后展开该软件包。
6. 选择漏洞旁边的 **Create exception** 按钮。

{{% create_panel.inline %}}
选择 **Create exception** 按钮会打开 **Create exception** 侧面板。在此面板中，您可以提供例外的详细信息：

- **Exception type**：例外类型。支持的类型有：

  - **Accepted risk**：由于安全风险极小、修复成本高、依赖上游修复或类似原因，漏洞未被解决。
  - **False positive**：漏洞在您的特定用例、配置中不存在安全风险，或者由于已采取的措施阻止了漏洞利用。

    如果您选择 **False positive**，则必须提供为什么该漏洞是误报的理由：

- **Additional details**：您想提供的关于该例外的任何其他信息。

- **Scope**：例外的范围。范围可以是：

  - **Image**：例外适用于所选镜像。
  - **All images in repository**：例外适用于仓库中的所有镜像。
  - **Specific repository**：例外适用于指定仓库中的所有镜像。
  - **All images in my organization**：例外适用于您组织中的所有镜像。

- **Package scope**：例外的范围。软件包范围可以是：

  - **Selected package**：例外适用于所选软件包。
  - **Any packages**：例外适用于易受此 CVE 影响的所有软件包。

填写完详细信息后，选择 **Create** 按钮以创建例外。

例外现已创建，并计入您所选镜像的分析结果中。该例外也会列在 Docker Scout Dashboard 中 [Vulnerabilities 页面](https://scout.docker.com/reports/vulnerabilities/exceptions) 的 **Exceptions** 选项卡上。

{{% /create_panel.inline %}}

{{< /tab >}}
{{< tab name="Docker Desktop" >}}

1. 在 Docker Desktop 中打开 **Images** 视图。
2. 打开 **Hub** 选项卡。
3. 选择包含您要为其创建例外的漏洞的镜像标签。
4. 选择包含您要为其创建例外的漏洞的层。
5. 在 **Vulnerabilities** 选项卡中，找到您要为其创建例外的漏洞。
6. 选择漏洞旁边的 **Create exception** 按钮。

{{% create_panel.inline / %}}

{{< /tab >}}
{{< /tabs >}}