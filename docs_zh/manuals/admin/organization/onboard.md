---
title: 为您的组织完成上车流程
weight: 20
description: 开始为您的 Docker Team 或 Business 组织完成上车流程。
keywords: business, team, organizations, get started, onboarding, Admin Console, organization management,
toc_min: 1
toc_max: 3
aliases:
- /docker-hub/onboard/
- /docker-hub/onboard-team/
- /docker-hub/onboard-business/
---

{{< summary-bar feature_name="Admin orgs" >}}

了解如何使用 Admin Console 或 Docker Hub 为您的组织完成上车流程。

为组织上车包括：

- 确定需要帮助您分配订阅席位的用户
- 邀请成员和所有者加入您的组织
- 为您的组织提供安全的身份验证和授权
- 强制 Docker Desktop 登录以确保最佳安全实践

这些操作帮助管理员了解用户活动情况并强制执行安全设置。组织成员登录后也能获得更高的拉取限制和其他权益。

## 前置条件

在开始为组织上车之前，请确保您：

- 拥有 Docker Team 或 Business 订阅。更多详情，请参阅
[Docker 订阅和功能](/manuals/subscription/details.md)。

  > [!NOTE]
  >
  > 购买自助订阅时，屏幕上的说明会引导您创建组织。如果您通过 Docker 销售购买了订阅但尚未创建组织，请参阅 [创建组织](/manuals/admin/organization/orgs.md)。

- 熟悉 Docker 管理概述中的概念和术语，参见
[administration overview](../_index.md)。

## 使用引导式设置上车

Admin Console 提供了引导式设置，帮助您
为组织完成上车流程。引导式设置的步骤包括基本的上车任务。如果您希望在引导式设置之外完成上车，请参阅 [推荐的上车步骤](/manuals/admin/organization/onboard.md#recommended-onboarding-steps)。

要使用引导式设置上车，
请导航至 [Admin Console](https://app.docker.com)，并在左侧导航栏中选择 **Guided setup**。

引导式设置将引导您完成以下上车步骤：

- **邀请您的团队**：邀请所有者和成员。
- **管理用户访问**：添加并验证域名，通过 SSO 管理用户，并
强制 Docker Desktop 登录。
- **Docker Desktop 安全**：配置镜像访问管理、注册表
访问管理以及设置管理。

## 推荐的上车步骤

### 步骤一：识别您的 Docker 用户

识别您的用户有助于高效分配席位，并确保他们获得
Docker 订阅的权益。

1. 确定您组织中的 Docker 用户。
   - 如果您的组织使用设备管理软件（如 MDM 或 Jamf），
   您可以使用设备管理软件帮助识别 Docker 用户。
   详情请参阅设备管理软件的文档。您可以通过检查用户机器上是否安装了 Docker Desktop 来识别 Docker 用户，安装位置如下：
      - Mac: `/Applications/Docker.app`
      - Windows: `C:\Program Files\Docker\Docker`
      - Linux: `/opt/docker-desktop`
   - 如果您的组织未使用设备管理软件，或者用户尚未安装 Docker Desktop，您可以通过问卷调查识别正在使用 Docker Desktop 的用户。
1. 要求用户将其 Docker 账户的电子邮件地址更新为与您组织域名关联的地址，或使用该邮箱创建新账户。
   - 要更新账户的电子邮件地址，请指导您的用户登录
   [Docker Hub](https://hub.docker.com)，并将电子邮件地址更新为
   他们组织域名下的邮箱地址。
   - 要创建新账户，请指导您的用户
   [注册](https://hub.docker.com/signup)，使用与您组织域名关联的邮箱地址。
1. 识别与您组织域名关联的 Docker 账户：
   - 请您的 Docker 销售代表或
   [联系销售](https://www.docker.com/pricing/contact-sales/) 获取使用您组织域名邮箱的 Docker 账户列表。

### 步骤二：邀请所有者

所有者可以帮助您完成组织的上车和管理工作。

创建组织时，您是唯一的所有者。添加额外的所有者是可选的。

要添加所有者，请邀请用户并为其分配所有者角色。更多
详情，请参阅 [邀请成员](/manuals/admin/organization/members.md) 和
[角色和权限](/manuals/enterprise/security/roles-and-permissions.md)。

### 步骤三：邀请成员

当您将用户添加到组织后，您就能了解他们的活动情况，并可以强制执行安全设置。您的成员登录后也能获得更高的拉取限制和其他组织范围的权益。

要添加成员，请邀请用户并为其分配成员角色。
更多详情，请参阅 [邀请成员](/manuals/admin/organization/members.md) 和
[角色和权限](/manuals/enterprise/security/roles-and-permissions.md)。

### 步骤四：使用 SSO 和 SCIM 管理用户访问

配置 SSO 和 SCIM 是可选的，仅 Docker Business 订阅用户可用。要将 Docker Team 订阅升级为 Docker Business 订阅，请参阅 [更改您的订阅](/manuals/subscription/change.md)。

使用您的身份提供商（IdP）通过 SSO 和 SCIM 自动管理成员并向 Docker 配置用户。详情请参阅：

   - [配置 SSO](/manuals/enterprise/security/single-sign-on/configure.md)
   以通过您的身份提供商进行身份验证，并在用户登录 Docker 时自动添加成员。
   - 可选。
   [强制 SSO](/manuals/enterprise/security/single-sign-on/connect.md)
   以确保用户登录 Docker 时必须使用 SSO。

     > [!NOTE]
     >
     > 强制单点登录（SSO）和强制 Docker Desktop 登录是不同的功能。更多详情，请参阅
     > [强制登录与强制单点登录（SSO）的区别](/manuals/enterprise/security/enforce-sign-in/_index.md#enforcing-sign-in-versus-enforcing-single-sign-on-sso)。

   - [配置 SCIM](/manuals/enterprise/security/provisioning/scim.md)
   以通过您的身份提供商自动向 Docker 配置、添加和取消配置成员。

### 步骤五：强制 Docker Desktop 登录

默认情况下，您的组织成员可以不登录直接使用 Docker Desktop。当用户未以组织成员身份登录时，他们无法获得
[您组织订阅的权益](../../subscription/details.md)，
并且可能绕过 [Docker 的安全功能](/manuals/enterprise/security/hardened-desktop/_index.md)。

根据您组织的 Docker 配置，有多种方式可以强制登录：
- [注册表键方法（仅 Windows）](/manuals/enterprise/security/enforce-sign-in/methods.md#registry-key-method-windows-only)
- [`.plist` 方法（仅 Mac）](/manuals/enterprise/security/enforce-sign-in/methods.md#plist-method-mac-only)
- [`registry.json` 方法（全平台）](/manuals/enterprise/security/enforce-sign-in/methods.md#registryjson-method-all)

### 步骤六：管理 Docker Desktop 安全

Docker 提供以下安全功能来管理您组织的
容器化开发安全态势：

- [镜像访问管理](/manuals/enterprise/security/hardened-desktop/image-access-management.md)：控制您的开发者可以从 Docker Hub 拉取哪些类型的镜像。
- [注册表访问管理](/manuals/enterprise/security/hardened-desktop/registry-access-management.md)：定义您的开发者可以访问哪些注册表。
- [设置管理](/manuals/enterprise/security/hardened-desktop/settings-management.md)：为您的用户设置和控制 Docker Desktop 设置。

## 下一步

- [管理 Docker 产品](./manage-products.md) 以配置访问和查看使用情况。
- 配置 [强化 Docker Desktop](/desktop/hardened-desktop/) 以改善您组织的容器化开发安全态势。
- [管理您的域名](/manuals/enterprise/security/domain-management.md) 以确保您域名下的所有 Docker 用户都属于您的组织。

您的 Docker 订阅提供许多额外功能。要了解更多信息，
请参阅 [Docker 订阅和功能](/subscription/details/)。