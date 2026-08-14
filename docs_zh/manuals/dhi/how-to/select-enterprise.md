---
title: 开始使用 DHI Select 和 Enterprise
linkTitle: 使用 DHI Select 和 Enterprise
description: 镜像仓库并开始将 Docker Hardened Images 用于 Select 和 Enterprise 订阅。
keywords: docker hardened images, enterprise, select, mirror, quickstart
---

{{< summary-bar feature_name="Docker Hardened Images" >}}

本指南向您展示如何开始使用 DHI Select 和 Enterprise 订阅。与 DHI Community 不同，此工作流允许您将仓库镜像到 Docker Hub 上的组织命名空间，访问合规变体（FIPS）、自定义镜像，并获取 SLA 支持的更新。

## 先决条件

要使用此工作流，您需要：

- 在您的 Docker Hub 命名空间中的组织所有者访问权限。
- 以下之一：
  - DHI Select 或 Enterprise 订阅。[联系 Docker 销售](https://www.docker.com/products/hardened-images/#compare) 购买 DHI Enterprise，或[了解有关 DHI 计划的更多信息](../../subscription/plans/dhi.md)。
  - 有效的 DHI 试用。[开始免费的 DHI 试用](https://hub.docker.com/hardened-images/start-free-trial)。
- [Docker Desktop](../../desktop/release-notes.md) 4.65 或更高版本，以使用 `docker dhi` CLI。

在适用的情况下，每个步骤都会显示 Docker Hub 和命令行说明。您可以使用任一界面。

## 步骤 1：查找要使用的镜像

{{< tabs group="interface" >}}
{{< tab name="Docker Hub" >}}

1. 访问 [Docker Hub](https://hub.docker.com/) 并登录。
2. 在左侧边栏中选择您的组织。
3. 导航至 **Hardened Images** > **Catalog**。
4. 使用搜索栏或筛选器查找镜像（例如 `python`、`node` 或 `golang`）。本示例搜索 `python`。

   要搜索带有合规变体（FIPS 或 STIG）的镜像，请选择 **Filter by** 并选择相关的合规选项。

5. 选择 Python 仓库以查看其详细信息。

6. 选择 **Images** 以查看可用的镜像变体。

{{< /tab >}}
{{< tab name="Command line" >}}

1. 列出可用的镜像仓库：

   ```console
   $ docker dhi catalog list --type image
   ```

2. 要按名称和 FIPS 合规性筛选，请使用 `--filter` 和 `--fips` 标志：

   ```console
   $ docker dhi catalog list --filter python --fips
   ```

3. 获取仓库的镜像详细信息：

   ```console
   $ docker dhi catalog get python
   ```

{{< /tab >}}
{{< /tabs >}}

继续下一步以镜像镜像。要深入了解镜像探索，请参阅[搜索和评估 Docker 安全加固镜像](search-evaluate.md)。

## 步骤 2：镜像仓库

镜像将 DHI 仓库复制到您在 Docker Hub 上的组织命名空间中。这使您能够接收镜像的 SLA 支持的 Docker 安全补丁，并使用自定义以及合规变体。只有组织所有者可以镜像仓库。

{{< tabs group="interface" >}}
{{< tab name="Docker Hub" >}}

1. 在您在上一步中找到的镜像仓库详细信息页面中，选择 **Use this image** > **Mirror repository**。请注意，您必须登录 Docker Hub 才能执行此操作。
2. 选择 **Mirror**。
3. 等待镜像完成镜像。这可能需要几分钟时间。
4. 验证镜像仓库是否以 `dhi-` 前缀出现在您的组织命名空间中（例如 `dhi-python`）。

{{< /tab >}}
{{< tab name="Command line" >}}

要使用以下命令，您必须使用 Docker 令牌进行身份验证或配置 DHI CLI 身份验证。有关详细信息，请参阅[使用 DHI CLI](../tools/cli.md#configuration)。

1. 开始将仓库镜像到您的组织命名空间。将 `<your-org>` 替换为您的组织名称。

   ```console
   $ docker dhi mirror start --org <your-org> dhi/python,<your-org>/dhi-python
   ```

2. 等待镜像完成镜像。这可能需要几分钟时间。

3. 验证镜像仓库。将 `<your-org>` 替换为您的组织名称。

   ```console
   $ docker dhi mirror list --org <your-org>
   ```

{{< /tab >}}
{{< /tabs >}}

继续下一步以自定义镜像。要深入了解镜像，请参阅[镜像仓库](mirror.md)。

## 步骤 3：自定义镜像

DHI Select 和 Enterprise 的主要优势之一是能够自定义您镜像的镜像。您可以添加系统软件包、配置设置或进行其他修改，以满足您组织的特定要求。

本示例展示了如何将 `curl` 系统软件包添加到您镜像的 Python 镜像中。

{{< tabs group="interface" >}}
{{< tab name="Docker Hub" >}}

1. 访问 Docker Hub 上您的组织命名空间。
2. 导航至您的镜像仓库（例如 `dhi-python`）。
3. 选择 **Customizations**。
4. 选择 **Create customization**。
5. 搜索 `3-alpine3.23` 并选择其中任意一个镜像。
6. 在 **Add packages** 中，选择 **curl**。
7. 选择 **Next: Configure**。
8. 在 **Customization name** 中，为您的自定义输入一个名称（例如 `curl`）。
9. 选择 **Next: Review customization**。
10. 选择 **Create customization** 以开始构建。

自定义构建可能需要几分钟时间。转到您镜像仓库的 **Customizations** 选项卡并查看 **Last build** 列以监控构建状态。

{{< /tab >}}
{{< tab name="Command line" >}}

要使用以下命令，您必须使用 Docker 令牌进行身份验证或配置 DHI CLI 身份验证。有关详细信息，请参阅[使用 DHI CLI](../tools/cli.md#configuration)。

1. 创建自定义。将 `<your-org>` 替换为您的组织名称。这将创建一个名为 `my-customization.yaml` 的文件，其中包含自定义详细信息。

   ```console
   $ docker dhi customization prepare --org <your-org> python 3-alpine3.23 \
       --destination <your-org>/dhi-python \
       --name "python with curl" \
       > my-customization.yaml
   ```

2. 将 `curl` 软件包添加到自定义中。您可以使用任何文本或代码编辑器编辑文件。以下命令使用 `echo` 将必要的行添加到 YAML 文件中：

   ```console
   $ echo "contents:" >> my-customization.yaml
   $ echo "  packages:" >> my-customization.yaml
   $ echo "    - curl" >> my-customization.yaml
   ```

3. 应用自定义：

   ```console
   $ docker dhi customization create --org <your-org> my-customization.yaml
   ```

4. 验证自定义是否已创建：

   ```console
   $ docker dhi customization list --org <your-org>
   ```

自定义构建可能需要几分钟时间。要检查构建状态：

1. 访问 Docker Hub 上您的组织命名空间。
2. 导航至您的镜像仓库（例如 `dhi-python`）。
3. 选择 **Customizations**。
4. 查看 **Last build** 列以监控构建状态。

{{< /tab >}}
{{< /tabs >}}

要深入了解自定义，请参阅[自定义 Docker 安全加固镜像](customize.md)。

## 步骤 4：拉取并运行您的自定义镜像

自定义构建完成后，您可以从 Docker Hub 上的组织命名空间拉取并运行自定义镜像。

1. 登录 Docker Hub：

   ```console
   $ docker login
   ```

2. 从您的组织拉取自定义镜像。将 `<your-org>` 替换为您的组织名称。自定义标签包含基于您自定义名称的后缀。

   ```console
   $ docker pull <your-org>/dhi-python:3-alpine3.23_python-with-curl
   ```

3. 运行镜像并测试 `curl` 是否已安装：

   ```console
   $ docker run --rm <your-org>/dhi-python:3-alpine3.23_python-with-curl curl --version
   ```

   这确认 `curl` 软件包已成功添加到镜像中。

要深入了解镜像使用，请参阅：

- [使用 Docker 安全加固镜像](use.md)：一般用法
- [使用 Helm chart](helm.md)：使用 Helm 部署

## 步骤 5：删除自定义并停止镜像

要删除自定义并停止镜像仓库：

1. 访问 Docker Hub 上您的组织命名空间。
2. 导航至您的镜像仓库（例如 `dhi-python`）。
3. 选择 **Customizations**。
4. 找到您要删除的自定义（例如 `python with curl`）。
5. 选择垃圾桶图标。
6. 选择 **Delete customization** 以确认删除。
7. 要停止镜像，请返回您组织的仓库列表。
8. 找到镜像仓库（例如 `dhi-python`）。
9. 选择 **Settings**。
10. 选择 **Stop mirroring**。
11. 选择 **Stop mirroring** 以确认。

## 下一步

您已经镜像、自定义并运行了 Docker 安全加固镜像。以下是继续操作的几种方式：

- [将现有应用程序迁移到 DHI](../migration/migrate-with-ai.md)：使用 Gordon 更新您的 Dockerfile，以使用 Docker 安全加固镜像作为基础。

- [验证 DHI](verify.md)：使用 [Docker Scout](/scout/) 或 Cosign 等工具检查和验证签名证明，例如 SBOM 和溯源。

- [扫描 DHI](scan.md)：使用 Docker Scout 或其他扫描器分析镜像以识别已知 CVE。
