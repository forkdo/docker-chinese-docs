---
title: 故障排除单点登录
linkTitle: 故障排除 SSO
description: 排除 Docker 单点登录配置和身份验证的常见问题
toc_max: 2
tags:
- Troubleshooting
keywords: sso troubleshooting, single sign-on errors, authentication issues, identity provider problems
aliases:
- /security/for-admins/single-sign-on/troubleshoot/
- /security/troubleshoot/troubleshoot-sso/
---

本页介绍常见的单点登录 (SSO) 错误及其解决方案。问题可能源于您的身份提供商 (IdP) 配置或 Docker 设置。

## 检查错误

如果遇到 SSO 问题，请先检查 Docker 和身份提供商中的错误。

### 检查 Docker 错误日志

1. 登录 [Docker Home](https://app.docker.com/)，然后从左上角的帐户下拉菜单中选择您的组织。
2. 选择 **Admin Console**，然后选择 **SSO and SCIM**。
3. 在 SSO 连接表中，选择 **Action** 菜单，然后选择 **View error logs**。
4. 有关特定错误的更多详细信息，请选择错误消息旁边的 **View error details**。
5. 记录在此页面上看到的任何错误，以便进一步故障排除。

### 检查身份提供商错误

1. 查看您的 IdP 日志或审计跟踪，查找任何失败的身份验证或配置尝试。
2. 确认您的 IdP SSO 设置与 Docker 中提供的值匹配。
3. 如果适用，请确认您已正确配置用户配置，并且已在您的 IdP 中启用。
4. 如果适用，请验证您的 IdP 是否正确映射 Docker 所需的用户属性。
5. 尝试从您的 IdP 配置测试用户，并验证他们是否出现在 Docker 中。

如需进一步故障排除，请查阅您的 IdP 文档或联系其支持团队。

## 组格式不正确

### 错误消息

发生此问题时，通常会出现以下错误消息：
```text
Some of the groups assigned to the user are not formatted as '<organization name>:<team name>'. Directory groups will be ignored and user will be provisioned into the default organization and team.
```

### 原因

- 身份提供商 (IdP) 中的组名称格式不正确：Docker 要求组遵循 `<organization>:<team>` 格式。如果分配给用户的组不遵循此格式，它们将被忽略。
- IdP 和 Docker 组织之间的组不匹配：如果您的 IdP 中的组在 Docker 中没有对应的团队，则无法识别该组，用户将被放置在默认组织和团队中。

### 受影响的环境

- 使用 Okta 或 Azure AD 等 IdP 的 Docker 单点登录设置
- 在 Docker 中使用基于组的角色分配的组织

### 复现步骤

要复现此问题：
1. 尝试使用 SSO 登录 Docker。
2. 用户在 IdP 中被分配了组，但未被放置到预期的 Docker 团队中。
3. 查看 Docker 日志或 IdP 日志以查找错误消息。

### 解决方案

更新 IdP 中的组名称：
1. 转到 IdP 的组管理部分。
2. 检查分配给受影响用户的组。
3. 确保每个组都遵循所需的格式：`<organization>:<team>`
4. 更新任何格式不正确的组以匹配此模式。
5. 保存更改并重试使用 SSO 登录。

## 用户未分配到组织

### 错误消息

发生此问题时，通常会出现以下错误消息：
```text
User '$username' is not assigned to this SSO organization. Contact your administrator. TraceID: XXXXXXXXXXXXX
```

### 原因

- 用户未分配到组织：如果禁用了即时 (JIT) 配置，用户可能不会分配到您的组织。
- 用户未被邀请加入组织：如果禁用了 JIT 且您不想启用它，则必须手动邀请用户。
- SCIM 配置错误：如果您使用 SCIM 进行用户配置，它可能无法正确地从您的 IdP 同步用户。

### 解决方案

**启用 JIT 配置**

启用 SSO 时，JIT 默认处于启用状态。如果您禁用了 JIT 并需要重新启用它：

1. 登录 [Docker Home](https://app.docker.com/)，然后从左上角的帐户下拉菜单中选择您的组织。
2. 选择 **Admin Console**，然后选择 **SSO and SCIM**。
3. 在 SSO 连接表中，选择 **Action** 菜单，然后选择 **Enable JIT provisioning**。
4. 选择 **Enable** 进行确认。

**手动邀请用户**

当 JIT 被禁用时，用户在通过 SSO 身份验证时不会自动添加到您的组织中。
要手动邀请用户，请参阅 [邀请成员](/manuals/admin/organization/members.md#invite-members)

**配置 SCIM 配置**

如果您启用了 SCIM，请使用以下步骤对 SCIM 连接进行故障排除：

1. 登录 [Docker Home](https://app.docker.com/)，然后从左上角的帐户下拉菜单中选择您的组织。
2. 选择 **Admin Console**，然后选择 **SSO and SCIM**。
3. 在 SSO 连接表中，选择 **Action** 菜单，然后选择 **View error logs**。有关特定错误的更多详细信息，请选择错误消息旁边的 **View error details**。记录在此页面上看到的任何错误。
4. 导航回 Admin Console 的 **SSO and SCIM** 页面，并验证您的 SCIM 配置：
    - 确保您 IdP 中的 SCIM 基础 URL 和 API 令牌与 Docker Admin Console 中提供的匹配。
    - 验证 SCIM 是否在 Docker 和您的 IdP 中都已启用。
5. 确保从您的 IdP 同步的属性与 Docker 的 [支持的属性](/manuals/enterprise/security/provisioning/scim.md#supported-attributes) 匹配。
6. 通过尝试从您的 IdP 配置测试用户来测试用户配置，并验证他们是否出现在 Docker 中。

## 未为此连接启用 IdP 发起的登录

### 错误消息

发生此问题时，通常会出现以下错误消息：
```text
IdP-Initiated sign in is not enabled for connection '$ssoConnection'.
```

### 原因

Docker 不支持 IdP 发起的 SAML 流程。当用户尝试从您的 IdP 进行身份验证时（例如使用登录页面上的 Docker SSO 应用磁贴），会发生此错误。

### 解决方案

**从 Docker 应用进行身份验证**

用户必须从 Docker 应用程序（Hub、Desktop 等）发起身份验证。用户需要在 Docker 应用中输入其电子邮件地址，然后将被重定向到为其域配置的 SSO IdP。

**隐藏 Docker SSO 应用**

您可以在 IdP 中向用户隐藏 Docker SSO 应用。这可以防止用户尝试从 IdP 仪表板启动身份验证。您必须在 IdP 中隐藏并配置此设置。

## 组织中席位不足

### 错误消息

发生此问题时，通常会出现以下错误消息：
```text
Not enough seats in organization '$orgName'. Add more seats or contact your administrator.
```

### 原因

当组织在通过即时 (JIT) 配置或 SCIM 配置用户时没有可用席位时，会发生此错误。

### 解决方案

**向组织添加更多席位**

购买额外的 Docker Business 订阅席位。有关详细信息，请参阅 [管理订阅席位](/manuals/subscription/manage-seats.md)。

**删除用户或待处理的邀请**

查看您的组织成员和待处理的邀请。删除不活动的用户或待处理的邀请以释放席位。有关更多详细信息，请参阅 [管理组织成员](/manuals/admin/organization/members.md)。

## 域名未通过 SSO 连接验证

### 错误消息

发生此问题时，通常会出现以下错误消息：
```text
Domain '$emailDomain' is not verified for your SSO connection. Contact your company administrator. TraceID: XXXXXXXXXXXXXX
```

### 原因

如果 IdP 通过 SSO 对用户进行了身份验证，并且返回给 Docker 的用户主体名称 (UPN) 与在 Docker 中配置的 SSO 连接关联的任何已验证域名不匹配，则会发生此错误。

### 解决方案

**验证 UPN 属性映射**

确保 IdP SSO 连接在断言属性中返回正确的 UPN 值。

**添加并验证所有域名**

添加并验证您的 IdP 用作 UPN 的所有域名和子域名，并将它们与您的 Docker SSO 连接关联。有关详细信息，请参阅 [配置单点登录](/manuals/enterprise/security/single-sign-on/configure.md)。

## 找不到会话

### 错误消息

发生此问题时，通常会出现以下错误消息：
```text
We couldn't find your session. You may have pressed the back button, refreshed the page, opened too many sign-in dialogs, or there is some issue with cookies. Try signing in again. If the issue persists, contact your administrator.
```

### 原因

以下原因可能导致此问题：
- 用户在身份验证期间按下了后退或刷新按钮。
- 身份验证流程丢失了初始请求的跟踪，导致无法完成。

### 解决方案

**不要中断身份验证流程**

在登录期间不要按后退或刷新按钮。

**重新启动身份验证**

关闭浏览器标签页，并从 Docker 应用程序（Desktop、Hub 等）重新启动身份验证流程。

## 名称 ID 不是电子邮件地址

### 错误消息

发生此问题时，通常会出现以下错误消息：
```text
The name ID sent by the identity provider is not an email address. Contact your company administrator.
```

### 原因

以下原因可能导致此问题：
- IdP 发送的名称 ID (UPN) 不符合 Docker 要求的电子邮件格式。
- Docker SSO 要求名称 ID 是用户的主电子邮件地址。

### 解决方案

在您的 IdP 中，确保名称 ID 属性格式正确：
1. 验证您 IdP 中的名称 ID 属性格式是否设置为 `EmailAddress`。
2. 调整您的 IdP 设置以返回正确的名称 ID 格式。