---
title: Use Docker Hub
linktitle: Docker Hub
description: 在 Docker Hub 上浏览 DHI 目录，搜索仓库，检查镜像元数据，并查看 SBOM、CVE 和证明。
weight: 10
keywords: docker hub dhi catalog, hardened images hub, dhi repository details, image variants hub
---

[Docker Hub 上的 Docker Hardened Images 目录](https://hub.docker.com/hardened-images/catalog)
是浏览、搜索和检查 DHI 仓库及其元数据的主要 Web 界面。

## 目录页面

目录列出所有可用的 DHI 仓库。您可以按名称、镜像类型和合规要求（FIPS、STIG）进行筛选，以找到所需的镜像。

## 仓库详情页面

当您从目录中选择一个仓库时，仓库详情页面提供以下内容：

- 概述：关于该镜像的简要说明。
- 指南：关于如何使用该镜像并迁移现有应用程序的若干指南。
- 镜像：选择此选项以[查看镜像变体](#images-page)。
- 安全摘要：选择一个标签名称以查看快速安全摘要，包括包数量和已知漏洞总数。
- 最近推送的标签：最近更新的镜像变体列表及其最后更新时间。
- 使用此镜像：选择某个镜像变体后，您可以选择此选项以查看如何拉取和使用该镜像变体的说明，或选择 **Mirror repository**（镜像仓库）将其镜像到您的组织。

## 镜像页面

在仓库详情页面中，选择 **Images** 以查看该仓库所有可用的镜像变体。该表格包含：

- 镜像版本：镜像名称及其基础发行版（例如 `debian 13`）以及相关的标签。
- 类型：该变体的支持生命周期状态。
- 合规性：相关的合规标识，例如 `CIS`、`FIPS` 或 `STIG (100%)`。
- 包管理器：是否有包管理器可用。对勾表示存在包管理器（例如 `apt` 或 `apk`），破折号表示无。
- Shell：是否有 Shell 可用。对勾表示存在 Shell（例如 `bash` 或 `busybox`），破折号表示无。
- 用户：容器以该用户身份运行，例如 `root` 或 `nonroot (65532)`。
- 最近推送：镜像变体最后更新的时间。
- 漏洞：按严重级别统计的漏洞数量。

## 镜像变体详情页面

从镜像表中选择一个镜像版本，以查看该特定变体的详细信息：

- 包：镜像变体中包含的所有包的列表，包含每个包的名称、版本、发行版和许可信息。
- 规格：
  - 源和构建信息：用于构建该镜像的 Dockerfile 和 Git commit。
  - 构建参数、入口点、CMD、用户、工作目录、环境变量、标签和平台。
- 漏洞：镜像变体已知的 CVE 列表，包括 CVE ID、严重级别、受影响的包、修复版本、最后检测日期、状态以及被抑制的 CVE。
- 证明：涵盖该镜像构建过程、内容和安全性态势的签名安全证明。完整列表请参阅 [证明](/dhi/explore/security-concepts/attestations/)。

## 管理页面

管理页面（**My Hub** > **Hardened Images** > **Manage**）是用于管理组织已镜像 DHI 仓库的中心位置。它有两个标签页：

- 已镜像镜像：列出当前已镜像到您组织的所有镜像仓库，包含其源 DHI 仓库、目标仓库名称和镜像状态。从这里您可以停止镜像或打开仓库的设置。
- 已镜像 Helm 图表：针对 Helm 图表仓库的相同视图。

选择已镜像的仓库会打开其设置，您可以在其中启用或禁用扩展生命周期支持 (ELS) 并访问自定义配置。

有关分步说明，请参阅[镜像 Docker Hardened Image 仓库](/dhi/how-to/mirror/)。

## 自定义配置

自定义配置可从 **My Hub** > **Hardened Images** > **Manage** > **Mirrored Images** 访问。选择已镜像仓库旁边的菜单图标，然后选择 **Customize**。每个自定义配置定义了在重建期间叠加到基础 DHI 之上的额外包、OCI 制品、环境变量或标签。

自定义配置视图显示每个自定义配置的名称、状态和最后构建时间。选择某个自定义配置会打开其配置，您可以在其中编辑定义、触发重建或将其删除。

有关分步说明，请参阅[自定义 Docker Hardened Image](/dhi/how-to/customize/)。
