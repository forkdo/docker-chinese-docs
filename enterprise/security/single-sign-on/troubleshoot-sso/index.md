# 排查单点登录问题


本页描述了常见的单点登录（SSO）错误及其解决方案。问题可能源自你的身份提供商（IdP）配置或 Docker 设置。

## 检查错误（Check for errors）

如果你遇到 SSO 问题，首先检查 Docker 和你的身份提供商中的错误。

### 检查 Docker 错误日志（Check Docker error logs）

1. 登录 [Docker Home](https://app.docker.com/) 并从左上角的账户下拉菜单中选择你的组织。
1. 选择 **Identity & auth**（身份与认证），然后 **SSO and SCIM**。
1. 在 SSO 连接表中，选择 **Action**（操作）菜单，然后 **View error logs**（查看错误日志）。
1. 要查看特定错误的更多详情，选择错误消息旁边的 **View error details**（查看错误详情）。
1. 记下你在此页面上看到的任何错误，以便进一步排查。

### 检查身份提供商错误（Check identity provider errors）

1. 查看你的 IdP 的日志或审计记录，查找任何失败的身份验证或配置（provisioning）尝试。
2. 确认你的 IdP 的 SSO 设置与 Docker 中提供的值匹配。
3. 如果适用，确认你已正确配置用户配置（provisioning），并且它在你的 IdP 中已启用。
4. 如果适用，验证你的 IdP 是否正确映射了 Docker 所需的用户属性。
5. 尝试从你的 IdP 配置一个测试用户，并验证他们是否出现在 Docker 中。

如需进一步排查，请查看你的 IdP 的文档或联系他们的支持团队。

## 组格式不正确（Groups are not formatted correctly）

### 错误消息（Error message）

当此问题发生时，出现以下错误消息很常见：

```text
Some of the groups assigned to the user are not formatted as '<organization name>:<team name>'. Directory groups will be ignored and user will be provisioned into the default organization and team.
```

### 原因（Causes）

- 身份提供商（IdP）中组名格式不正确：Docker 要求组的格式为 `<organization>:<team>`。如果分配给用户的组不遵循此格式，它们将被忽略。
- IdP 与 Docker 组织之间的组不匹配：如果你的 IdP 中的某个组在 Docker 中没有对应的团队，它将无法被识别，用户将被放置在默认组织和团队中。

### 受影响的环境（Affected environments）

- 使用 Okta 或 Azure AD 等 IdP 的 Docker 单点登录设置
- 在 Docker 中使用基于组的角色分配的组织

### 复现步骤（Steps to replicate）

要复现此问题：

1. 尝试使用 SSO 登录 Docker。
2. 用户在 IdP 中被分配了组，但未被放入预期的 Docker 团队。
3. 查看 Docker 日志或 IdP 日志以找到错误消息。

### 解决方案（Solutions）

在 IdP 中更新组名：

1. 进入你的 IdP 的组管理部分。
2. 检查分配给受影响用户的组。
3. 确保每个组都遵循所需格式：`<organization>:<team>`
4. 更新任何格式不正确的组以匹配此模式。
5. 保存更改并重试用 SSO 登录。

## 用户未被分配到组织（User is not assigned to the organization）

### 错误消息（Error message）

当此问题发生时，出现以下错误消息很常见：

```text
User '$username' is not assigned to this SSO organization. Contact your administrator. TraceID: XXXXXXXXXXXXX
```

### 原因（Causes）

- 用户未被分配到组织：如果即时（Just-in-Time，JIT）配置被禁用，用户可能未被分配到你的组织。
- 用户未被邀请到组织：如果 JIT 被禁用且你不想启用它，则必须手动邀请用户。
- SCIM 配置不正确：如果你使用 SCIM 进行用户配置，它可能未正确地从你的 IdP 同步用户。

### 解决方案（Solutions）

**启用 JIT 配置（Enable JIT provisioning）**

当你启用 SSO 时，JIT 默认是启用的。如果你禁用了 JIT 并需要重新启用它：

1. 登录 [Docker Home](https://app.docker.com/) 并从左上角的账户下拉菜单中选择你的组织。
1. 选择 **Identity & auth**，然后 **SSO and SCIM**。
1. 在 SSO 连接表中，选择 **Action** 菜单，然后 **Enable JIT provisioning**（启用 JIT 配置）。
1. 选择 **Enable** 确认。

**手动邀请用户（Manually invite users）**

当 JIT 被禁用时，用户通过 SSO 认证后不会自动添加到你的组织。要手动邀请用户，请参阅
[邀请成员](/manuals/admin/organization/manage/members.md#invite-members)。

**配置 SCIM 配置（Configure SCIM provisioning）**

如果你已启用 SCIM，请使用以下步骤排查你的 SCIM 连接：

1. 登录 [Docker Home](https://app.docker.com/) 并从左上角的账户下拉菜单中选择你的组织。
1. 选择 **Identity & auth**，然后 **SSO and SCIM**。
1. 在 SSO 连接表中，选择 **Action** 菜单，然后 **View error logs**。要查看特定错误的更多详情，选择错误消息旁边的
   **View error details**。记下你在此页面上看到的任何错误。
1. 导航回 **Identity & auth**，然后 **SSO and SCIM**，并验证你的 SCIM 配置：
   - 确保 IdP 中的 SCIM Base URL 和 API Token 与 Docker 中提供的值匹配。
   - 验证 SCIM 在 Docker 和你的 IdP 中都已启用。
1. 确保从你的 IdP 同步的属性与 Docker 的
   [SCIM 支持的属性](/manuals/enterprise/security/provisioning/scim/provision-scim.md#supported-attributes) 匹配。
1. 通过尝试从你的 IdP 配置一个测试用户来测试用户配置，并验证他们是否出现在 Docker 中。

## 连接未启用 IdP 发起的登录（IdP-initiated sign in is not enabled for connection）

### 错误消息（Error message）

当此问题发生时，出现以下错误消息很常见：

```text
IdP-Initiated sign in is not enabled for connection '$ssoConnection'.
```

### 原因（Causes）

Docker 不支持 IdP 发起的 SAML 流程。当用户尝试从你的 IdP 进行身份验证时（例如在登录页面使用 Docker SSO 应用磁贴），
会发生此错误。

### 解决方案（Solutions）

**从 Docker 应用进行身份验证（Authenticate from Docker apps）**

用户必须从 Docker 应用程序（Hub、Desktop 等）发起身份验证。用户需要在 Docker 应用中输入他们的电子邮件地址，然后
会被重定向到为其域名配置的 SSO IdP。

**隐藏 Docker SSO 应用（Hide the Docker SSO app）**

你可以在 IdP 中向用户隐藏 Docker SSO 应用。这可以防止用户尝试从 IdP 仪表盘发起身份验证。你必须在 IdP 中隐藏并
配置此项。

## 组织中席位不足（Not enough seats in organization）

### 错误消息（Error message）

当此问题发生时，出现以下错误消息很常见：

```text
Not enough seats in organization '$orgName'. Add more seats or contact your administrator.
```

### 原因（Causes）

当组织通过即时（JIT）配置或 SCIM 配置用户时，若组织没有可用的席位给用户，会发生此错误。

### 解决方案（Solutions）

**为组织添加更多席位（Add more seats to the organization）**

购买额外的 Docker Business 订阅席位。有关详情，请参阅
[管理订阅席位](/manuals/admin/organization/manage/manage-seats.md)。

**移除用户或待处理的邀请（Remove users or pending invitations）**

查看你的组织成员和待处理的邀请。移除非活跃用户或待处理的邀请以释放席位。有关更多详情，请参阅
[管理组织成员](/manuals/admin/organization/manage/members.md)。

## 域名未针对 SSO 连接进行验证（Domain is not verified for SSO connection）

### 错误消息（Error message）

当此问题发生时，出现以下错误消息很常见：

```text
Domain '$emailDomain' is not verified for your SSO connection. Contact your company administrator. TraceID: XXXXXXXXXXXXXX
```

### 原因（Causes）

如果 IdP 通过 SSO 对用户进行了身份验证，但返回给 Docker 的用户主体名（UPN）与 Docker 中配置的 SSO 连接关联的任何
已验证域名都不匹配，则会发生此错误。

### 解决方案（Solutions）

**验证 UPN 属性映射（Verify UPN attribute mapping）**

确保 IdP SSO 连接在断言属性中返回正确的 UPN 值。

**添加并验证所有域名（Add and verify all domains）**

添加并验证你的 IdP 用作 UPN 的所有域名和子域名，并将它们与你的 Docker SSO 连接关联。有关详情，请参阅
[配置单点登录](/manuals/enterprise/security/single-sign-on/connect.md)。

## 无法找到会话（Unable to find session）

### 错误消息（Error message）

当此问题发生时，出现以下错误消息很常见：

```text
We couldn't find your session. You may have pressed the back button, refreshed the page, opened too many sign-in dialogs, or there is some issue with cookies. Try signing in again. If the issue persists, contact your administrator.
```

### 原因（Causes）

以下原因可能导致此问题：

- 用户在身份验证期间按了后退或刷新按钮。
- 身份验证流程丢失了对初始请求的跟踪，导致无法完成。

### 解决方案（Solutions）

**不要中断身份验证流程（Do not disrupt the authentication flow）**

在登录期间不要按后退或刷新按钮。

**重新开始身份验证（Restart authentication）**

关闭浏览器标签页，并从 Docker 应用程序（Desktop、Hub 等）重新开始身份验证流程。

## Name ID 不是电子邮件地址（Name ID is not an email address）

### 错误消息（Error message）

当此问题发生时，出现以下错误消息很常见：

```text
The name ID sent by the identity provider is not an email address. Contact your company administrator.
```

### 原因（Causes）

以下原因可能导致此问题：

- IdP 发送的 Name ID（UPN）不符合 Docker 所需的电子邮件格式。
- Docker SSO 要求 Name ID 是用户的主电子邮件地址。

### 解决方案（Solutions）

在你的 IdP 中，确保 Name ID 属性格式正确：

1. 验证你的 IdP 中 Name ID 属性格式设置为 `EmailAddress`。
2. 调整你的 IdP 设置以返回正确的 Name ID 格式。

