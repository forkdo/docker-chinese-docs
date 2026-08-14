---
title: 设置单点登录
linkTitle: 设置
weight: 20
description: 连接 Docker 与您的身份提供商，测试配置，并启用强制策略
keywords: 配置 sso, 设置 sso, docker sso 设置, docker 身份提供商, sso 强制策略, docker hub, 安全
aliases:
  - /security/for-admins/single-sign-on/connect/
  - /docker-hub/domains/
  - /docker-hub/sso-connection/
  - /docker-hub/enforcing-sso/
  - /single-sign-on/configure/
  - /admin/company/settings/sso-configuration/
  - /admin/organization/security-settings/sso-configuration/
  - /security/for-admins/single-sign-on/configure/
  - /enterprise/security/single-sign-on/configure
---

{{< summary-bar feature_name="SSO" >}}

要设置单点登录（SSO），您需要在 Docker 和您的身份提供商（IdP）之间建立连接。虽然本指南以 Okta 和 Microsoft Entra ID 作为实际示例，但其他 IdP 的总体流程相同。

如果您不熟悉 SSO 流程，请先查看 [SSO 概述](/manuals/enterprise/security/single-sign-on/_index.md) 了解 SSO 的工作原理。

## 前提条件

Docker 支持任何兼容 SAML 2.0 或 OIDC 的身份提供商。开始之前，请确保满足以下条件：

- 通知您的公司即将进行的 SSO 登录流程。
- 确认每个 Docker 用户都拥有一个有效的 IdP 账户，使用与其唯一主要标识符 (UPN) 相同的电子邮件地址。
- 确保 CI/CD 管道使用 PAT 或 OAT 而非密码。

## 设置 SSO 连接

> [!TIP]
> 这些步骤需要您在 Docker 和 IdP 之间复制粘贴值。请在一个会话中完成本指南，并打开两个浏览器窗口分别访问 Docker 和您的 IdP。

### 第 1 步：添加域名

要添加域名：

1. 登录 [app.docker.com](https://app.docker.com)，然后选择您的组织。如果您的组织是某个公司的一部分，请选择该公司以在公司级别管理域名。
1. 选择 **Identity & auth**，然后选择 **Domain management**。
1. 选择 **Add a domain**。
1. 在文本框中输入您的域名，然后选择 **Add domain**。
1. 在弹出的对话框中，复制用于域名验证的 **TXT Record Value**。

### 第 2 步：验证您的域名

要确认域名所有权，请使用 Docker 提供的 TXT Record Value 在您的域名系统 (DNS) 主机中添加一条 TXT 记录。DNS 传播最多可能需要 72 小时。在此期间 Docker 会自动检查该记录。

> [!TIP]
>
> 添加记录名称时，对于 `example.com` 这样的根域名，请使用 `@` 或留空。避免使用 `docker`、`docker-verification`、`www` 或您的域名本身等常见值。请务必查阅您的 DNS 提供商文档以确认其特定的记录名称要求。

{{< tabs >}}
{{< tab name="AWS Route 53" >}}

1. 要向 AWS 添加 TXT 记录，请参阅[使用 Amazon Route 53 控制台创建记录](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resource-record-sets-creating.html)。
1. 等待最多 72 小时以进行 TXT 记录验证。
1. 记录生效后，进入 **Identity & auth**，然后进入 **Domain management**，并选择 **Verify**。

{{< /tab >}}
{{< tab name="Google Cloud DNS" >}}

1. 要向 Google Cloud DNS 添加 TXT 记录，请参阅[使用 TXT 记录验证您的域名](https://cloud.google.com/identity/docs/verify-domain-txt)。
1. 等待最多 72 小时以进行 TXT 记录验证。
1. 记录生效后，进入 **Identity & auth**，然后进入 **Domain management**，并选择 **Verify**。

{{< /tab >}}
{{< tab name="GoDaddy" >}}

1. 要向 GoDaddy 添加 TXT 记录，请参阅[添加 TXT 记录](https://www.godaddy.com/help/add-a-txt-record-19232)。
1. 等待最多 72 小时以进行 TXT 记录验证。
1. 记录生效后，进入 **Identity & auth**，然后进入 **Domain management**，并选择 **Verify**。

{{< /tab >}}
{{< tab name="Other providers" >}}

1. 登录您的域名主机。
1. 在 DNS 设置中添加一条 TXT 记录并保存。
1. 等待最多 72 小时以进行 TXT 记录验证。
1. 记录生效后，进入 **Identity & auth**，然后进入 **Domain management**，并选择 **Verify**。

{{< /tab >}}
{{< /tabs >}}

### 第 3 步：在 Docker 中创建 SSO 连接

1. 从 [app.docker.com](https://app.docker.com) 选择您的组织。
1. 选择 **Identity & auth**，然后选择 **SSO and SCIM**。
1. 选择 **Create Connection**。为连接命名，然后选择 **SAML 2.0**。
1. 保持此窗口打开。您需要在 Okta 窗口中复制并粘贴这些值：
   - **Entity ID**
   - **ACS URL**
   - **Connection ID**

您将在 IdP 中创建 SSO 连接后返回此处完成连接。

### 第 4 步：在 IdP 中创建 SSO 连接

根据您的 IdP 提供商选择以下标签页。

{{< tabs >}}
{{< tab name="Okta SAML" >}}

您需要 Okta 组织的[超级管理员权限](https://help.okta.com/en-us/content/topics/security/administrators-super-admin.htm)。

1. 登录您的 Okta 管理员账户。从顶部导航栏中选择 **Admin** 按钮进入 Okta 的管理控制台。
1. 从左侧导航的 **Applications** 部分，选择 **Applications**。选择 **Create App Integration**。
1. 选择 SAML 2.0 以匹配您在 Docker Home 中的选择。
1. 对于 **General Settings**，将应用命名为 "Docker"。上传 Logo 为可选项。
1. 对于 **Configure SAML**，输入以下值：
   - 对于 **Single Sign On URL** 值，粘贴 Docker 的 ACS URL。
   - 对于 **Audience URI (SP Entity ID)** 值，粘贴 Docker 的 Entity ID。
   - 对于 **Name ID format**，选择 `EmailAddress`
   - 对于 **Application username**，选择 `Email`
   - 对于 **Update application username on**，选择 `Create and update`
   - 可选。如果您的组织需要，添加 [SAML 属性](/manuals/enterprise/security/provisioning/_index.md#sso-attributes)。
1. 对于 **Feedback**，在结束前勾选 **This is an internal app that we have created**。

保持您的 Okta 窗口打开以进行下一步。

{{< /tab >}}
{{< tab name="Entra ID SAML 2.0" >}}

要启用 Microsoft Entra 的 SSO，您需要 [Cloud Application Administrator](https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/permissions-reference#cloud-application-administrator) 权限。

1. 在 Microsoft Entra 管理中心，选择 **Entra ID**，然后进入 **Enterprise apps**。选择 **All applications**。
1. 选择 **Create your own application**，将应用命名为 "Docker"。选择 **Non-gallery**。
1. 创建应用后，进入 **Single Sign-On** 并选择 **SAML**。
1. 在 **Basic SAML configuration** 部分选择 **Edit**。在 **Basic SAML configuration** 中，选择 **Edit** 并粘贴您从 Docker 中创建 SSO 连接时复制的值：
   - 对于 **Identifier** 值，粘贴 Docker 的 Entity ID。
   - 对于 **Reply URL** 值，粘贴 Docker 的 ACS URL。
1. 可选。如果您的组织需要，添加 [SAML 属性](/manuals/enterprise/security/provisioning/_index.md#sso-attributes)。
1. 从 **SAML Signing Certificate** 部分，下载您的 **Certificate (Base64)**。

{{< /tab >}}
{{< tab name="Azure OpenID Connect (OIDC)" >}}

#### 注册应用

1. 登录 [Microsoft Entra 管理中心](https://entra.microsoft.com/)。
1. 进入 **App Registration** 并选择 **New Registration**。
1. 将应用命名为 "Docker"。
1. 设置账户类型并粘贴来自 Docker 的 **Redirect URI**。
1. 选择 **Register**。
1. 复制 **Client ID**。

#### 创建客户端密钥

1. 在您的应用中，进入 **Certificates & secrets**。
1. 选择 **New client secret**，填写描述并配置有效期，然后选择 **Add**。
1. 复制新密钥的 **value**。

#### 设置 API 权限

1. 在您的应用中，进入 **API permissions**。
1. 选择 **Grant admin consent** 并确认。
1. 选择 **Add a permissions** > **Delegated permissions**。
1. 搜索并选择 `User.Read`。
1. 确认已授予管理员同意。

{{< /tab >}}
{{< /tabs >}}

### 第 5 步：将 Docker 连接到 IdP

通过将 IdP 的值粘贴到 Docker 中完成集成。

> [!IMPORTANT]
> 当提示复制证书时，请复制整个证书，从 `----BEGIN CERTIFICATE----` 开始并包含 `----END CERTIFICATE----` 行。

{{< tabs >}}
{{< tab name="Okta SAML" >}}

1. 进入 **Applications** 并选择 **Applications**。从 **ACTIVE** 表中选择您的应用。
1. 从 **Sign on** 进入 **View SAML setup instructions**。此页面包含 **SAML Sign-in URL** 和 **x509 Certificate**。保持此页面打开。
1. 返回您已打开的 Docker 窗口中的 **Create single sign-on connection** 步骤。粘贴 **SAML Sign-in URL** 和 **x509 Certificate** 值。
1. 可选。如果您的组织需要，选择一个默认团队。
1. 检查后选择 **Create connection**。

{{< /tab >}}
{{< tab name="Entra ID SAML 2.0" >}}

1. 用文本编辑器打开下载的 **Certificate (Base64)**。
1. 复制以下值：
   - 来自 Azure AD 的：**Login URL**
   - **Certificate (Base64)** 内容
1. 返回 Docker Home，然后粘贴 **Login URL** 和 **Certificate (Base64)** 值。
1. 从下拉菜单中选择您的域名。
1. 可选。如果您的组织需要，选择一个默认团队。
1. 检查后选择 **Create connection**。

{{< /tab >}}
{{< tab name="Azure OpenID Connect (OIDC)" >}}

1. 返回 Docker Home。
1. 粘贴以下值：
   - **Client ID**
   - **Client Secret**
   - **Azure AD Domain**
1. 可选。如果您的组织需要，选择一个默认团队。
1. 检查后选择 **Create connection**。

{{< /tab >}}
{{< /tabs >}}

### 第 6 步：测试连接

Microsoft Entra 和 Okta 等 IdP 可能要求您在测试 SSO 之前将用户分配到应用程序。您可以查阅 [Microsoft Entra](https://learn.microsoft.com/en-us/entra/identity/enterprise-apps/add-application-portal-setup-sso#test-single-sign-on) 的文档和 [Okta](https://help.okta.com/wf/en-us/content/topics/workflows/connector-reference/okta/actions/assignusertoapplicationforsso.htm) 的文档，了解如何将您自己或其他用户分配到应用。

将自己分配到应用后：

1. 打开一个无痕浏览器窗口，使用您的域名邮箱地址登录 Docker Home。
1. 当重定向到 IdP 的登录页面时，使用您的域名邮箱进行认证，而非使用 Docker ID。

如果您有多个 IdP，请选择 **Continue with SSO** 登录选项。如果您使用 CLI，则必须使用个人访问令牌进行认证。

## 配置多个 IdP

Docker 支持多个身份提供商 (IdP) 配置，让您可以将一个域名与多个 IdP 关联。每个连接必须使用相同的域名，这样用户在登录时选择 **Continue with SSO** 即可选择其 IdP。

要添加多个 IdP：

1. 为每个连接使用相同的域名。
1. 重复本页[设置 SSO 连接](/manuals/enterprise/security/single-sign-on/connect.md#set-up-an-sso-connection)流程中的步骤 3-6。为您组织打算使用的每个 IdP 重复这些步骤。

因为每个 IdP 必须使用相同的域名，您无需重复添加和验证域名的步骤。

## 强制启用 SSO

如果未强制启用 SSO，用户仍可使用 Docker 用户名和密码登录。强制启用 SSO 后，用户在登录 Docker 时必须使用 SSO，这将集中认证流程并强制执行 IdP 设置的策略。

在强制启用 SSO 之前，通过 CLI 访问 Docker 的用户必须[创建个人访问令牌 (PAT)](/manuals/security/access-tokens.md)。PAT 替代其用户名和密码进行认证。

1. 登录 [Docker Home](https://app.docker.com/) 并选择您的组织或公司。
1. 选择 **Identity & auth**，然后选择 **SSO and SCIM**。
1. 在 SSO 连接表中，选择 **Action** 菜单，然后选择 **Enable enforcement**。
1. 按照屏幕上的说明操作。
1. 选择 **Turn on enforcement**。

当您强制启用 SSO 后，用户将无法修改其邮箱地址和密码、将用户账户转换为组织，或通过 Docker Hub 设置 2FA。如果您希望使用 2FA，则必须通过 IdP 启用 2FA。

## 后续步骤

- [配置用户预配](/manuals/enterprise/security/provisioning/_index.md)。
- [强制登录](../enforce-sign-in/_index.md)。
- [创建个人访问令牌](/manuals/security/access-tokens.md)。
- [排查 SSO 问题](/manuals/enterprise/security/single-sign-on/troubleshoot-sso.md)。
