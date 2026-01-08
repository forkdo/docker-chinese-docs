---
title: 连接单点登录
linkTitle: 连接
description: 连接 Docker 与您的身份提供商，测试配置，并启用强制策略
keywords: 配置 sso, 设置 sso, docker sso 设置, docker 身份提供商, sso 强制策略, docker hub, 安全
aliases:
- /security/for-admins/single-sign-on/connect/
---

{{< summary-bar feature_name="SSO" >}}

设置单点登录（SSO）连接需要同时配置 Docker 和您的身份提供商（IdP）。本指南将引导您完成在 Docker 中的设置、在 IdP 中的设置，以及最终的连接步骤。

> [!TIP]
>
> 您需要在 Docker 和 IdP 之间复制粘贴多个值。建议在一个会话中完成本指南，同时打开两个浏览器窗口分别访问 Docker 和您的 IdP。

## 支持的身份提供商

Docker 支持任何兼容 SAML 2.0 或 OIDC 的身份提供商。本指南为最常用的提供商（Okta 和 Microsoft Entra ID）提供了详细的设置说明。

如果您使用的是其他 IdP，基本流程保持一致：

1. 在 Docker 中配置连接。
1. 使用 Docker 提供的值在 IdP 中设置应用程序。
1. 将 IdP 的值输入回 Docker 以完成连接。
1. 测试连接。

## 前提条件

开始前请确保：

- 已验证您的域名
- 已在身份提供商（IdP）中设置账户
- 已完成[配置单点登录](configure.md)指南中的步骤

## 第一步：在 Docker 中创建 SSO 连接

> [!NOTE]
>
> 创建 SSO 连接前，您必须[至少验证一个域名](/manuals/enterprise/security/single-sign-on/configure.md)。

1. 登录 [Docker Home](https://app.docker.com) 并选择您的组织。
1. 选择 **Admin Console**，然后选择 **SSO and SCIM**。
1. 选择 **Create Connection** 并为连接命名。
1. 选择认证方式：**SAML** 或 **Azure AD (OIDC)**。
1. 复制 IdP 所需的值：
    - Okta SAML：**Entity ID**、**ACS URL**
    - Azure OIDC：**Redirect URL**

保持此窗口打开，以便稍后粘贴来自 IdP 的值。

## 第二步：在 IdP 中创建 SSO 连接

根据您的 IdP 提供商选择以下标签页。

{{< tabs >}}
{{< tab name="Okta SAML" >}}

1. 登录 Okta 账户并打开管理员门户。
1. 选择 **Administration**，然后选择 **Create App Integration**。
1. 选择 **SAML 2.0**，然后选择 **Next**。
1. 将应用命名为 "Docker"。
1. （可选）上传 Logo。
1. 粘贴来自 Docker 的值：
    - Docker ACS URL -> **Single Sign On URL**
    - Docker Entity ID -> **Audience URI (SP Entity ID)**
1. 配置以下设置：
    - Name ID format: `EmailAddress`
    - Application username: `Email`
    - Update application on: `Create and update`
1. （可选）添加 SAML 属性。参见 [SSO 属性](/manuals/enterprise/security/provisioning/_index.md#sso-attributes)。
1. 选择 **Next**。
1. 勾选 **This is an internal app that we have created**。
1. 选择 **Finish**。

{{< /tab >}}
{{< tab name="Entra ID SAML 2.0" >}}

1. 登录 Microsoft Entra（原 Azure AD）。
1. 选择 **Default Directory** > **Add** > **Enterprise Application**。
1. 选择 **Create your own application**，命名为 "Docker"，并选择 **Non-gallery**。
1. 创建应用后，进入 **Single Sign-On** 并选择 **SAML**。
1. 在 **Basic SAML configuration** 部分选择 **Edit**。
1. 编辑 **Basic SAML configuration** 并粘贴来自 Docker 的值：
    - Docker Entity ID -> **Identifier**
    - Docker ACS URL -> **Reply URL**
1. （可选）添加 SAML 属性。参见 [SSO 属性](/manuals/enterprise/security/provisioning/_index.md#sso-attributes)。
1. 保存配置。
1. 在 **SAML Signing Certificate** 部分，下载您的 **Certificate (Base64)**。

{{< /tab >}}
{{< tab name="Azure Connect (OIDC)" >}}

### 注册应用

1. 登录 Microsoft Entra（原 Azure AD）。
1. 选择 **App Registration** > **New Registration**。
1. 将应用命名为 "Docker"。
1. 设置账户类型并粘贴来自 Docker 的 **Redirect URI**。
1. 选择 **Register**。
1. 复制 **Client ID**。

### 创建客户端密钥

1. 在应用中，进入 **Certificates & secrets**。
1. 选择 **New client secret**，填写描述并配置有效期，然后选择 **Add**。
1. 复制新密钥的 **value**。

### 设置 API 权限

1. 在应用中，进入 **API permissions**。
1. 选择 **Grant admin consent** 并确认。
1. 选择 **Add a permissions** > **Delegated permissions**。
1. 搜索并选择 `User.Read`。
1. 确认已授予管理员同意。

{{< /tab >}}
{{< /tabs >}}

## 第三步：将 Docker 连接到 IdP

通过将 IdP 的值粘贴到 Docker 中完成集成。

{{< tabs >}}
{{< tab name="Okta SAML" >}}

1. 在 Okta 中，选择您的应用并进入 **View SAML setup instructions**。
1. 复制 **SAML Sign-in URL** 和 **x509 Certificate**。

    > [!IMPORTANT]
    >
    > 请复制整个证书，包括 `----BEGIN CERTIFICATE
----` 和 `----END CERTIFICATE
----` 行。
1. 返回 Docker Admin Console。
1. 粘贴 **SAML Sign-in URL** 和 **x509 Certificate** 的值。
1. （可选）选择默认团队。
1. 检查后选择 **Create connection**。

{{< /tab >}}
{{< tab name="Entra ID SAML 2.0" >}}

1. 用文本编辑器打开下载的 **Certificate (Base64)**。
1. 复制以下值：
    - 来自 Azure AD 的：**Login URL**
    - **Certificate (Base64)** 内容

    > [!IMPORTANT]
    >
    > 请复制整个证书，包括 `----BEGIN CERTIFICATE
----` 和 `----END CERTIFICATE
----` 行。
1. 返回 Docker Admin Console。
1. 粘贴 **Login URL** 和 **Certificate (Base64)** 的值。
1. （可选）选择默认团队。
1. 检查后选择 **Create connection**。

{{< /tab >}}
{{< tab name="Azure Connect (OIDC)" >}}

1. 返回 Docker Admin Console。
1. 粘贴以下值：
    - **Client ID**
    - **Client Secret**
    - **Azure AD Domain**
1. （可选）选择默认团队。
1. 检查后选择 **Create connection**。

{{< /tab >}}
{{< /tabs >}}

## 第四步：测试连接

1. 打开一个无痕浏览器窗口。
1. 使用您的**域名邮箱地址**登录 Admin Console。
1. 浏览器将重定向到您的身份提供商的登录页面进行认证。如果您有[多个 IdP](#optional-configure-multiple-idps)，请选择 **Continue with SSO** 登录选项。
1. 通过域名邮箱认证，而非使用 Docker ID。

如果您使用 CLI，则必须使用个人访问令牌进行认证。

## 可选：配置多个 IdP

Docker 支持多个 IdP 配置。要为同一域名使用多个 IdP：

- 对每个 IdP 重复本页的步骤 1-4。
- 每个连接必须使用相同的域名。
- 用户登录时选择 **Continue with SSO** 以选择其 IdP。

## 可选：强制启用 SSO

> [!IMPORTANT]
>
> 如果未强制启用 SSO，用户仍可使用 Docker 用户名和密码登录。

强制启用 SSO 后，用户在登录 Docker 时必须使用 SSO。这将集中认证流程，并强制执行 IdP 设置的策略。

1. 登录 [Docker Home](https://app.docker.com/) 并选择您的组织或公司。
1. 选择 **Admin Console**，然后选择 **SSO and SCIM**。
1. 在 SSO 连接表中，选择 **Action** 菜单，然后选择 **Enable enforcement**。
1. 按照屏幕上的说明操作。
1. 选择 **Turn on enforcement**。

启用 SSO 强制策略后，用户将无法修改其邮箱地址和密码、将用户账户转换为组织，或通过 Docker Hub 设置 2FA。如果您希望使用 2FA，则必须通过 IdP 启用 2FA。

## 后续步骤

- [配置用户预配](/manuals/enterprise/security/provisioning/_index.md)。
- [强制登录](../enforce-sign-in/_index.md)。
- [创建个人访问令牌](/manuals/enterprise/security/access-tokens.md)。
- [排查 SSO 问题](/manuals/enterprise/troubleshoot/troubleshoot-sso.md)。