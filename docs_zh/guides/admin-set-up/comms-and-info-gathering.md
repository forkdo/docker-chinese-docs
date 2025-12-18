---
title: 沟通与信息收集
description: 从关键利益相关者处收集公司的需求，并传达给开发人员。
weight: 10
---

## 与开发人员和 IT 团队沟通

在组织内部全面部署 Docker Desktop 之前，请与关键利益相关者协调，确保过渡顺利。

### 通知 Docker Desktop 用户

您的公司内部可能已经存在 Docker Desktop 用户。本次上手流程中的某些步骤可能会影响他们与平台的交互方式。

尽早与用户沟通，告知他们：

- 他们将升级到受支持版本的 Docker Desktop，作为订阅上手的一部分
- 设置将被审查并优化以提高效率
- 他们需要使用公司邮箱登录公司的 Docker 组织，以访问订阅权益

### 与 MDM 团队协作

设备管理解决方案（如 Intune 和 Jamf）在企业中常用于软件分发。这些工具通常由专门的 MDM 团队管理。

尽早与该团队协作，以：

- 了解他们的需求和部署变更的前置时间
- 协调配置文件的分发

本指南中的多个设置步骤需要将 JSON 文件、注册表项或 .plist 文件分发到开发人员机器。使用 MDM 工具部署这些配置文件，确保其完整性。

## 识别 Docker 组织

一些公司可能拥有多个
[Docker 组织](/manuals/admin/organization/_index.md)。这些组织可能是为特定目的创建的，或者可能不再需要。

如果您怀疑公司有多个 Docker 组织：

- 调查团队，查看他们是否有自己的组织
- 联系 Docker 支持，获取与其邮箱域名匹配的用户所属的组织列表

## 收集需求

[设置管理](/manuals/enterprise/security/hardened-desktop/settings-management/_index.md) 允许您为 Docker Desktop 预设多个配置参数。

与以下利益相关者协作，建立公司的基线配置：

- Docker 组织所有者
- 开发负责人
- 信息安全代表

共同审查以下领域：

- 安全功能和
  [强制 Docker Desktop 用户登录](/manuals/enterprise/security/enforce-sign-in/_index.md)
- 订阅中包含的其他 Docker 产品

要查看可预设的参数，请参阅 [配置设置管理](/manuals/enterprise/security/hardened-desktop/settings-management/configure-json-file.md#step-two-configure-the-settings-you-want-to-lock-in)。

## 可选：与 Docker 实施团队会面

Docker 实施团队可以帮助您设置组织、配置 SSO、强制登录以及配置 Docker Desktop。

如需安排会议，请发送邮件至 successteam@docker.com。