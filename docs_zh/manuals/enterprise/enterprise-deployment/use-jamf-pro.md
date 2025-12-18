---
title: 使用 Jamf Pro 部署
description: 使用 Jamf Pro 部署 Mac 版 Docker Desktop
keywords: jamf, mac, docker desktop, 部署, mdm, 企业, 管理员, pkg
tags: [admin]
weight: 50
aliases: 
 - /desktop/setup/install/enterprise-deployment/use-jamf-pro/
---

{{< summary-bar feature_name="Jamf Pro" >}}

了解如何使用 Jamf Pro 部署 Mac 版 Docker Desktop，包括上传安装包和创建部署策略。

首先，上传安装包：

1. 在 Jamf Pro 控制台中，导航至 **Computers** > **Management Settings** > **Computer Management** > **Packages**。
2. 选择 **New** 以添加新安装包。
3. 上传 `Docker.pkg` 文件。

接下来，创建部署策略：

1. 导航至 **Computers** > **Policies**。
2. 选择 **New** 以创建新策略。
3. 输入策略名称，例如 "Deploy Docker Desktop"。
4. 在 **Packages** 选项卡下，添加您上传的 Docker 安装包。
5. 配置范围，以定位您要在其上安装 Docker 的设备或设备组。
6. 保存策略并部署。

更多信息，请参阅 [Jamf Pro 官方文档](https://learn.jamf.com/en-US/bundle/jamf-pro-documentation-current/page/Policies.html)。

## 附加资源

- 了解如何为您的用户 [强制登录](/manuals/enterprise/security/enforce-sign-in/_index.md)。