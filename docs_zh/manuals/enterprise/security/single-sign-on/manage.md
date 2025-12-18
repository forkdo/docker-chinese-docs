---
title: 管理单点登录
linkTitle: 管理
description: 了解如何为您的组织或公司管理单点登录（SSO）。
keywords: 管理, 单点登录, SSO, 登录, 管理控制台, 管理员, 安全, 域, 连接, 用户, 配置
aliases:
- /admin/company/settings/sso-management/
- /single-sign-on/manage/
- /security/for-admins/single-sign-on/manage/
---

{{< summary-bar feature_name="SSO" >}}

本页面涵盖 SSO 初始设置后的管理操作，包括管理域、连接、用户和配置设置。

## 管理域

### 添加域

为现有 SSO 连接添加域：

1. 登录 [Docker Home](https://app.docker.com)，从左上角账户下拉菜单中选择您的公司或组织。
1. 选择 **Admin Console**，然后选择 **SSO and SCIM**。
1. 在 SSO 连接表中，选择连接的 **Actions** 菜单，然后选择 **Edit connection**。
1. 选择 **Next** 导航到域部分。
1. 在 **Domains** 部分，选择 **Add domain**。
1. 输入您要添加到连接的域。
1. 选择 **Next** 确认或更改已连接的组织。
1. 选择 **Next** 确认或更改默认组织和团队配置选择。
1. 查看连接详细信息，选择 **Update connection**。

### 从 SSO 连接中移除域

> [!IMPORTANT]
>
> 如果您对同一域使用多个身份提供商，必须单独从每个 SSO 连接中移除该域。

1. 登录 [Docker Home](https://app.docker.com)，从左上角账户下拉菜单中选择您的公司或组织。
1. 选择 **Admin Console**，然后选择 **SSO and SCIM**。
1. 在 **SSO connections** 表中，选择连接的 **Actions** 菜单，然后选择 **Edit connection**。
1. 选择 **Next** 导航到域部分。
1. 在 **Domain** 部分，选择要移除的域旁边的 **X** 图标。
1. 选择 **Next** 确认或更改已连接的组织。
1. 选择 **Next** 确认或更改默认组织和团队配置选择。
1. 查看连接详细信息，选择 **Update connection**。

> [!NOTE]
>
> 重新添加域时，Docker 会分配新的 TXT 记录值。您必须使用新的 TXT 记录重新完成域验证。

## 管理 SSO 连接

### 查看连接

查看所有已配置的 SSO 连接：

1. 登录 [Docker Home](https://app.docker.com)，从左上角账户下拉菜单中选择您的公司或组织。
1. 选择 **Admin Console**，然后选择 **SSO and SCIM**。
1. 在 **SSO connections** 表中查看所有已配置的连接。

### 编辑连接

修改现有 SSO 连接：

1. 登录 [Docker Home](https://app.docker.com)，从左上角账户下拉菜单中选择您的公司或组织。
1. 选择 **Admin Console**，然后选择 **SSO and SCIM**。
1. 在 **SSO connections** 表中，选择连接的 **Actions** 菜单，然后选择 **Edit connection**。
1. 按照屏幕说明修改连接设置。

### 删除连接

移除 SSO 连接：

1. 登录 [Docker Home](https://app.docker.com)，从左上角账户下拉菜单中选择您的公司或组织。
1. 选择 **Admin Console**，然后选择 **SSO and SCIM**。
1. 在 **SSO connections** 表中，选择连接的 **Actions** 菜单，然后选择 **Delete connection**。
1. 按照屏幕说明确认删除。

> [!WARNING]
>
> 删除 SSO 连接会移除所有通过该连接认证的用户的访问权限。

## 管理用户和配置

Docker 在用户通过 SSO 登录时自动通过即时（JIT）配置添加用户。您也可以手动管理用户并配置不同的配置方法。

### 配置工作原理

Docker 支持以下配置方法：

- JIT 配置（默认）：用户通过 SSO 登录时自动添加到您的组织
- SCIM 配置：从您的身份提供商同步用户和组到 Docker
- 组映射：将身份提供商中的用户组与 Docker 组织中的团队同步
- 手动配置：关闭自动配置，手动邀请用户

有关配置方法的更多信息，请参阅 [配置用户](/manuals/enterprise/security/provisioning/_index.md)。

### 添加访客用户

邀请不通过您的身份提供商认证的用户：

1. 登录 [Docker Home](https://app.docker.com/)，选择您的组织。
1. 选择 **Members**。
1. 选择 **Invite**。
1. 按照屏幕说明邀请用户。

用户会收到电子邮件邀请，可以创建 Docker 账户或使用现有账户登录。

### 移除用户

从您的组织中移除用户：

1. 登录 [Docker Home](https://app.docker.com/)，选择您的组织。
1. 选择 **Members**。
1. 找到要移除的用户，选择其名称旁边的 **Actions** 菜单。
1. 选择 **Remove** 并确认移除。

用户在被移除后立即失去对您组织的访问权限。