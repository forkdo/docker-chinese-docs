---
title: 连接单点登录
linkTitle: 连接
description: 连接 Docker 和您的身份提供商，测试设置并启用强制执行
keywords: 配置 sso, 设置 sso, docker sso 设置, docker 身份提供商, sso 强制执行, docker hub, 安全
aliases:
 - /security/for-admins/single-sign-on/connect/
---

{{< summary-bar feature_name="SSO" >}}

设置单点登录 (SSO) 连接需要在 Docker 和您的身份提供商 (IdP) 中进行配置。本指南将引导您完成 Docker 中的设置、IdP 中的设置，以及最终连接。

> [!TIP]
>
> 您需要在 Docker 和您的 IdP 之间复制和粘贴值。请在一次会话中完成本指南，并为 Docker 和您的 IdP 分别打开独立的浏览器窗口。

## 支持的身份提供商

Docker 支持任何兼容 SAML 2.0 或 OIDC 的身份提供商。本指南为最常用的提供商 Okta 和 Microsoft Entra ID 提供了详细的设置说明。

如果您使用的是其他 IdP，一般流程保持不变：

1. 在 Docker 中配置连接。
1. 使用 Docker 中的值在您的 IdP 中设置应用程序。
1. 通过将 IdP 的值输入回 Docker 来完成连接。
1. 测试连接。

## 前置条件

开始之前，请确认：

- 已验证您的域名
- 已在您的身份提供商 (IdP) 中设置账户
- 已完成 [配置单点登录](configure.md) 指南中的步骤

## 步骤一：在 Docker 中创建 SSO 连接

> [!NOTE]
>
> 在创建 SSO 连接之前，您必须[验证至少一个域名](/manuals/enterprise/security/single-sign-on/configure.md)。

1. 登录到 [Docker Home](https://app.docker.com) 并选择您的组织。
1. 选择 **Admin Console**，然后选择 **SSO and SCIM**。
1. 选择 **Create Connection** 并为连接提供名称。
1. 选择身份验证方法：**SAML** 或 **Azure AD (OIDC)**。
1. 复制 IdP 所需的值：
    - Okta SAML：**Entity ID**、**ACS URL**
    - Azure OIDC：**Redirect URL**

保持此窗口打开，以便稍后粘贴来自您的 IdP 的值。

## 步骤二：在您的 IdP 中创建 SSO 连接

根据您的 IdP 提供商使用以下标签页。

{{< tabs >}}
{{< tab name="Okta SAML" >}}

1. 登录到您的 Okta 账户并打开管理员门户。
1. 选择 **Administration**，然后选择 **Create App Integration**。
1. 选择 **SAML 2.0**，然后选择 **Next**。
1. 将您的应用命名为 "Docker"。
1. 可选：上传徽标。
1. 粘贴来自 Docker 的值：
    - Docker ACS URL -> **Single Sign On URL**
    - Docker Entity ID -> **Audience URI (SP Entity ID)**
1. 配置以下设置：
    - Name ID 格式：`EmailAddress`
    - 应用用户名：`Email`
    - 更新应用时间：`Create and update`
1. 可选：添加 SAML 属性。参见 [SSO 属性](/manuals/enterprise/security/provisioning/_index.md#sso-attributes)。
1. 选择 **Next**。
1. 选中 **This is an internal app that we have created** 复选框。
1. 选择 **Finish**。

{{< /tab >}}
{{< tab name="Entra ID SAML 2.0" >}}

1. 登录到 Microsoft Entra（前身为 Azure AD）。
1. 选择 **Default Directory** > **Add** > **Enterprise Application**。
1. 选择 **Create your own application**，将其命名为 "Docker"，并选择 **Non-gallery**。
1. 创建应用后，转到 **Single Sign-On** 并选择 **SAML**。
1. 在 **Basic SAML configuration** 部分选择 **Edit**。
1. 编辑 **Basic SAML configuration** 并粘贴来自 Docker 的值：
    - Docker Entity ID -> **Identifier**
    - Docker ACS URL -> **Reply URL**
1. 可选：添加 SAML 属性。参见 [SSO 属性](/manuals/enterprise/security/provisioning/_index.md#sso-attributes)。
1. 保存配置。
1. 从 **SAML Signing Certificate** 部分下载您的 **Certificate (Base64)**。

{{< /tab >}}
{{< tab name="Azure Connect (OIDC)" >}}

### 注册应用

1. 登录到 Microsoft Entra（前身为 Azure AD）。
1. 选择 **App Registration** > **New Registration**。
1. 将应用命名为 "Docker"。
1. 设置账户类型并粘贴来自 Docker 的 **Redirect URI**。
1. 选择 **Register**。
1. 复制 **Client ID**。

### 创建客户端密钥

1. 在您的应用中，转到 **Certificates & secrets**。
1. 选择 **New client secret**，描述并配置持续时间，然后选择 **Add**。
1. 复制新密钥的 **value**。

### 设置 API 权限

1. 在您的应用中，转到 **API permissions**。
1. 选择 **Grant admin consent** 并确认。
1. 选择 **Add a permissions** > **Delegated permissions**。
1. 搜索并选择 `User.Read`。
1. 确认已授予管理员同意。

{{< /tab >}}
{{< /tabs >}}

## 步骤三：将 Docker 连接到您的 IdP

通过将您的 IdP 值粘贴到 Docker 中来完成集成。

{{< tabs >}}
{{< tab name="Okta SAML" >}}

1. 在 Okta 中，选择您的应用并转到 **View SAML setup instructions**。
1. 复制 **SAML Sign-in URL** 和 **x509 Certificate**。

    > [!IMPORTANT]
    >
    > 复制整个证书，包括 `----BEGIN CERTIFICATE----` 和 `----END CERTIFICATE----` 行。
1. 返回 Docker Admin Console。
1. 粘贴 **SAML Sign-in URL** 和 **x509 Certificate** 值。
1. 可选：选择默认团队。
1. 审查并选择 **Create connection**。

{{< /tab >}}
{{< tab name="Entra ID SAML 2.0" >}}

1. 在文本编辑器中打开您下载的 **Certificate (Base64)**。
1. 复制以下值：
    - 来自 Azure AD：**Login URL**
    - **Certificate (Base64)** 内容

    > [!IMPORTANT]
    >
    > 复制整个证书，包括 `----BEGIN CERTIFICATE----` 和 `----END CERTIFICATE----` 行。
1. 返回 Docker Admin Console。
1. 粘贴 **Login URL** 和 **Certificate (Base64)** 值。
1. 可选：选择默认团队。
1. 审查并选择 **Create connection**。

{{< /tab >}}
{{< tab name="Azure Connect (OIDC)" >}}

1. 返回 Docker Admin Console。
1. 粘贴以下值：
    - **Client ID**
    - **Client Secret**
    - **Azure AD Domain**
1. 可选：选择默认团队。
1. 审查并选择 **Create connection**。

{{< /tab >}}
{{< /tabs >}}

## 步骤四：测试连接

1. 打开一个无痕浏览器窗口。
1. 使用您的**域名邮箱地址**登录 Admin Console。
1. 浏览器将重定向到您的身份提供商的登录页面进行身份验证。如果您配置了[多个 IdP](#optional-configure-multiple-idps)，请选择登录选项 **Continue with SSO**。
1. 通过您的域名邮箱进行身份验证，而不是使用 Docker ID。

如果您正在使用 CLI，则必须使用个人访问令牌进行身份验证。

## 可选：配置多个 IdP

Docker 支持多个 IdP 配置。要在单个域上使用多个 IdP：

- 对每个 IdP 重复本页面的步骤 1-4。
- 每个连接必须使用相同的域。
- 用户在登录时将选择 **Continue with SSO** 来选择他们的 IdP。

## 可选：强制执行 SSO

> [!IMPORTANT]
>
> 如果未强制执行 SSO，用户仍可以使用 Docker 用户名和密码登录。

强制执行 SSO 要求用户在登录 Docker 时使用 SSO。这集中了身份验证并强制执行 IdP 设置的策略。

1. 登录到 [Docker Home](https://app.docker.com/) 并选择您的组织或公司。
1. 选择 **Admin Console**，然后选择 **SSO and SCIM**。
1. 在 SSO 连接表中，选择 **Action** 菜单，然后选择 **Enable enforcement**。
1. 按照屏幕上的说明操作。
1. 选择 **Turn on enforcement**。

当强制执行 SSO 时，您的用户将无法修改其电子邮件地址和密码，无法将用户账户转换为组织，也无法通过 Docker Hub 设置 2FA。如果您想使用 2FA，必须通过您的 IdP 启用 2FA。

## 后续步骤

- [配置用户](/manuals/enterprise/security/provisioning/_index.md)。
- [强制执行登录](../enforce-sign-in/_index.md)。
- [创建个人访问令牌](/manuals/enterprise/security/access-tokens.md)。
- [排查 SSO](/manuals/enterprise/troubleshoot/troubleshoot-sso.md) 问题。