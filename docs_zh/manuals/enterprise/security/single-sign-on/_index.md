---
title: 单点登录概述
linkTitle: 单点登录
description: 了解单点登录的工作原理、如何设置以及所需的 SSO 属性。
keywords: 单点登录, SSO, 登录, 管理员, docker hub, docker home, 安全, 身份提供者, SSO 配置, 企业登录, Docker Business, 用户身份验证
aliases:
  - /single-sign-on/
  - /admin/company/settings/sso/
  - /admin/organization/security-settings/sso-management/
  - /security/for-admins/single-sign-on/
weight: 10
---

{{< summary-bar feature_name="SSO" >}}

单点登录 (SSO) 允许用户通过其身份提供者 (IdP) 进行身份验证来访问 Docker。SSO 可以为整个公司（包括所有关联的组织）或具有 Docker Business 订阅的单个组织配置。

## SSO 的工作原理

启用 SSO 后，Docker 支持用户登录的非 IdP 初始化流程。用户不再使用 Docker 用户名和密码登录，而是被重定向到您的 IdP 登录页面。用户必须通过登录 Docker Hub 或 Docker Desktop 来启动 SSO 身份验证过程。

下图说明了 SSO 在 Docker Hub、Docker Desktop 和您的 IdP 之间如何运行和管理。

![SSO 架构](images/SSO.png)

## 设置 SSO

要在 Docker 中配置 SSO，请按照以下步骤操作：

1. [配置您的域名](connect.md)，创建并验证它。
1. [在 Docker 和您的 IdP 中创建 SSO 连接](connect.md)。
1. 将 Docker 链接到您的身份提供者。
1. 测试您的 SSO 连接。
1. 在 Docker 中配置用户。
1. 可选。[强制登录](../enforce-sign-in/_index.md)。
1. [管理您的 SSO 配置](manage.md)。

配置完成后，用户可以使用其公司电子邮件地址登录 Docker 服务。登录后，用户将被添加到您的公司，分配到组织，并加入团队。

> [!IMPORTANT]
>
> 当强制执行 SSO 时，不再支持基于密码的 CLI 登录。CLI 访问请使用个人访问令牌 (PAT)。更多信息请参阅 [安全公告](/manuals/security/security-announcements.md#deprecation-of-password-logins-on-cli-when-sso-enforced)。

## 后续步骤

- 开始 [配置 SSO](connect.md)。
- 阅读 [常见问题](/manuals/enterprise/security/single-sign-on/FAQs/general.md)。
- [排查](/manuals/enterprise/security/single-sign-on/troubleshoot-sso.md) SSO 问题。
