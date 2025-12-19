---
title: 使用 Jamf Pro 部署
description: 使用 Jamf Pro 部署适用于 Mac 的 Docker Desktop
keywords: jamf, mac, docker desktop, deploy, mdm, enterprise, administrator, pkg
tags: [admin]
weight: 50
aliases: 
 - /desktop/setup/install/enterprise-deployment/use-jamf-pro/
---

{{< summary-bar feature_name="Jamf Pro" >}}

了解如何使用 Jamf Pro 部署适用于 Mac 的 Docker Desktop，包括上传安装程序以及创建部署策略。

首先，上传软件包：

1. 在 Jamf Pro 控制台中，导航至 **计算机** > **管理设置** > **计算机管理** > **软件包**。
2. 选择 **新建** 以添加新软件包。
3. 上传 `Docker.pkg` 文件。

接下来，创建用于部署的策略：

1. 导航至 **计算机** > **策略**。
2. 选择 **新建** 以创建新策略。
3. 为策略输入名称，例如“部署 Docker Desktop”。
4. 在 **软件包** 选项卡下，添加您上传的 Docker 软件包。
5. 配置范围以指定要在哪些设备或设备组上安装 Docker。
6. 保存策略并部署。

有关更多信息，请参阅 [Jamf Pro 官方文档](https://learn.jamf.com/en-US/bundle/jamf-pro-documentation-current/page/Policies.html)。

## 其他资源

- 了解如何为您的用户[强制登录](/manuals/enterprise/security/enforce-sign-in/_index.md)。