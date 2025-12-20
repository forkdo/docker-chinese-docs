# 沟通与信息收集

## 与开发人员及IT团队沟通

在组织内部全面部署 Docker Desktop 之前，请与关键利益相关者协调，以确保平稳过渡。

### 通知 Docker Desktop 用户

您的公司可能已有 Docker Desktop 用户。此入职流程中的某些步骤可能会影响他们与平台的交互方式。

尽早与用户沟通，告知他们：

- 作为订阅入职的一部分，他们将被升级到受支持的 Docker Desktop 版本
- 设置将被审查并优化以提高生产力
- 他们需要使用企业邮箱登录公司的 Docker 组织，才能访问订阅权益

### 与MDM团队协作

设备管理解决方案（如 Intune 和 Jamf）通常用于企业内的软件分发。这些工具通常由专门的MDM团队管理。

在此流程早期与该团队协作，以：

- 了解他们的要求以及部署变更所需的前置时间
- 协调配置文件的分发

本指南中的多个设置步骤需要将 JSON 文件、注册表项或 .plist 文件分发到开发人员机器。使用MDM工具部署这些配置文件，并确保其完整性。

## 识别 Docker 组织

一些公司可能创建了多个 [Docker 组织](/manuals/admin/organization/_index.md)。这些组织可能是出于特定目的创建的，也可能已不再需要。

如果您怀疑公司拥有多个 Docker 组织：

- 调查您的团队，看他们是否有自己的组织
- 联系 Docker 支持，获取用户邮箱与您的域名匹配的组织列表

## 收集需求

[设置管理](/manuals/enterprise/security/hardened-desktop/settings-management/_index.md) 允许您为 Docker Desktop 预置大量配置参数。

与以下利益相关者合作，建立公司的基线配置：

- Docker 组织所有者
- 开发主管
- 信息安全代表

共同审查以下领域：

- 安全功能以及 [强制登录](/manuals/enterprise/security/enforce-sign-in/_index.md) 给 Docker Desktop 用户
- 订阅中包含的其他 Docker 产品

要查看可预置的参数，请参阅 [配置设置管理](/manuals/enterprise/security/hardened-desktop/settings-management/configure-json-file.md#step-two-configure-the-settings-you-want-to-lock-in)。

## 可选：与 Docker 实施团队会面

Docker 实施团队可以帮助您设置组织、配置 SSO、强制登录以及配置 Docker Desktop。

如需安排会议，请发送邮件至 successteam@docker.com。
