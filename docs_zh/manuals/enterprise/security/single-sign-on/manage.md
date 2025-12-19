---
title: 管理单点登录
linkTitle: 管理
description: 了解如何为您的组织或公司管理单点登录。
keywords: 管理, 单点登录, SSO, 登录, 管理控制台, 管理员, 安全, 域, 连接, 用户, 配置
aliases:
- /admin/company/settings/sso-management/
- /single-sign-on/manage/
- /security/for-admins/single-sign-on/manage/
---

{{< summary-bar feature_name="SSO" >}}

本页介绍在初始设置后如何管理单点登录 (SSO)，
包括管理域、连接、用户和配置设置。

## 管理域

### 添加域

要将域添加到现有的 SSO 连接：

1. 登录 [Docker Home](https://app.docker.com)，然后从左上角的帐户下拉菜单中选择您的公司或组织。
1. 选择 **Admin Console**（管理控制台），然后选择 **SSO and SCIM**。
1. 在 SSO 连接表中，选择您的连接的 **Actions**（操作）菜单，然后选择 **Edit connection**（编辑连接）。
1. 选择 **Next**（下一步）导航到域部分。
1. 在 **Domains**（域）部分，选择 **Add domain**（添加域）。
1. 输入要添加到连接的域。
1. 选择 **Next**（下一步）确认或更改连接的组织。
1. 选择 **Next**（下一步）确认或更改默认组织和团队配置选择。
1. 查看连接详细信息，然后选择 **Update connection**（更新连接）。

### 从 SSO 连接中移除域

> [!IMPORTANT]
>
> 如果您对同一域使用多个身份提供者，则必须从每个 SSO 连接中单独移除该域。

1. 登录 [Docker Home](https://app.docker.com)，然后从左上角的帐户下拉菜单中选择您的公司或组织。
1. 选择 **Admin Console**（管理控制台），然后选择 **SSO and SCIM**。
1. 在 **SSO connections**（SSO 连接）表中，选择您的连接的 **Actions**（操作）菜单，然后选择 **Edit connection**（编辑连接）。
1. 选择 **Next**（下一步）导航到域部分。
1. 在 **Domain**（域）部分，选择您要移除的域旁边的 **X** 图标。
1. 选择 **Next**（下一步）确认或更改连接的组织。
1. 选择 **Next**（下一步）确认或更改默认组织和团队配置选择。
1. 查看连接详细信息，然后选择 **Update connection**（更新连接）。

> [!NOTE]
>
> 当您重新添加域时，Docker 会分配一个新的 TXT 记录值。您必须使用新的 TXT 记录再次完成域验证。

## 管理 SSO 连接

### 查看连接

要查看所有已配置的 SSO 连接：

1. 登录 [Docker Home](https://app.docker.com)，然后从左上角的帐户下拉菜单中选择您的公司或组织。
1. 选择 **Admin Console**（管理控制台），然后选择 **SSO and SCIM**。
1. 在 **SSO connections**（SSO 连接）表中查看所有已配置的连接。

### 编辑连接

要修改现有的 SSO 连接：

1. 登录 [Docker Home](https://app.docker.com)，然后从左上角的帐户下拉菜单中选择您的公司或组织。
1. 选择 **Admin Console**（管理控制台），然后选择 **SSO and SCIM**。
1. 在 **SSO connections**（SSO 连接）表中，选择您的连接的 **Actions**（操作）菜单，然后选择 **Edit connection**（编辑连接）。
1. 按照屏幕上的说明修改您的连接设置。

### 删除连接

要移除 SSO 连接：

1. 登录 [Docker Home](https://app.docker.com)，然后从左上角的帐户下拉菜单中选择您的公司或组织。
1. 选择 **Admin Console**（管理控制台），然后选择 **SSO and SCIM**。
1. 在 **SSO connections**（SSO 连接）表中，选择您的连接的 **Actions**（操作）菜单，然后选择 **Delete connection**（删除连接）。
1. 按照屏幕上的说明确认删除。

> [!WARNING]
>
> 删除 SSO 连接会移除所有通过该连接进行身份验证的用户的访问权限。

## 管理用户和配置

Docker 会在用户通过 SSO 登录时，通过即时 (JIT) 配置自动配置用户。您也可以手动管理用户并配置不同的配置方法。

### 配置工作原理

Docker 支持以下配置方法：

- JIT 配置（默认）：用户通过 SSO 登录时会自动添加到您的组织
- SCIM 配置：将用户和组从您的身份提供者同步到 Docker
- 组映射：将您的身份提供者中的用户组与 Docker 组织中的团队同步
- 手动配置：关闭自动配置并手动邀请用户

有关配置方法的更多信息，请参阅[配置用户](/manuals/enterprise/security/provisioning/_index.md)。

### 添加访客用户

要邀请不通过您的身份提供者进行身份验证的用户：

1. 登录 [Docker Home](https://app.docker.com/)，然后选择您的组织。
1. 选择 **Members**（成员）。
1. 选择 **Invite**（邀请）。
1. 按照屏幕上的说明邀请用户。

用户将收到一封电子邮件邀请，并可以创建 Docker 帐户或使用其现有帐户登录。

### 移除用户

要从您的组织中移除用户：

1. 登录 [Docker Home](https://app.docker.com/)，然后选择您的组织。
1. 选择 **Members**（成员）。
1. 找到您要移除的用户，然后选择其姓名旁边的 **Actions**（操作）菜单。
1. 选择 **Remove**（移除）并确认移除。

用户在被移除后会立即失去对您组织的访问权限。