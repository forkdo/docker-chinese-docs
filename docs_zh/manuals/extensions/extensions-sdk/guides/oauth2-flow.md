---
title: 身份验证
description: Docker 扩展 OAuth 2.0 流程
keywords: Docker, 扩展, sdk, OAuth 2.0
aliases:
 - /desktop/extensions-sdk/dev/oauth2-flow/
 - /desktop/extensions-sdk/guides/oauth2-flow/
---

> [!NOTE]
>
> 本文档假设您已拥有身份提供商 (IdP)，例如 Google、Entra ID（前身为 Azure AD）或 Okta，用于处理身份验证流程并返回访问令牌。

了解如何通过 OAuth 2.0 从您的扩展中让用户通过 Web 浏览器进行身份验证，并返回到您的扩展。

在 OAuth 2.0 中，“授权类型”（grant type）是指应用程序获取访问令牌的方式。尽管 OAuth 2.0 定义了多种授权类型，但本文档仅描述如何使用授权码授权类型从您的扩展中对用户进行授权。

## 授权码授权流程

授权码授权类型被机密和公开客户端用于将授权码交换为访问令牌。

当用户通过重定向 URL 返回客户端后，应用程序从 URL 中获取授权码，并使用它请求访问令牌。

![OAuth 2.0 流程图](images/oauth.png)

上图显示了以下流程：

- Docker 扩展请求用户授权访问其数据。
- 如果用户授予访问权限，扩展将向服务提供商请求访问令牌，传递用户的授权码和身份验证详细信息以标识客户端。
- 服务提供商验证这些详细信息后，返回访问令牌。
- 扩展使用访问令牌向服务提供商请求用户数据。

### OAuth 2.0 术语

- Auth URL：API 提供商授权服务器的端点，用于检索授权码。
- Redirect URI：客户端应用程序的回调 URL，用于授权后重定向。此 URL 必须在 API 提供商处注册。

用户输入用户名和密码后，即完成身份验证。

## 打开浏览器页面以验证用户身份

在扩展 UI 中，您可以提供一个按钮，点击后在浏览器中打开新窗口以验证用户身份。

使用 [ddClient.host.openExternal](../dev/api/dashboard.md#open-a-url) API 打开浏览器访问授权 URL。例如：

```typescript
window.ddClient.openExternal("https://authorization-server.com/authorize?
  response_type=code
  &client_id=T70hJ3ls5VTYG8ylX3CZsfIu
  &redirect_uri=${REDIRECT_URI});
```

## 获取授权码和访问令牌

您可以通过将 `docker-desktop://dashboard/extension-tab?extensionId=awesome/my-extension` 设置为 OAuth 应用中的 `redirect_uri`，并将授权码作为查询参数附加，从而从扩展 UI 获取授权码。然后扩展 UI 代码即可读取 URL 中对应的 code 查询参数。

> [!IMPORTANT]
>
> 使用此功能需要 Docker Desktop 中的扩展 SDK 0.3.3。您需要确保在 [image labels](../extensions/labels.md) 中通过 `com.docker.desktop.extension.api.version` 设置的扩展所需 SDK 版本高于 0.3.3。

#### 授权

此步骤中，用户在浏览器中输入凭据。授权完成后，用户被重定向回您的扩展用户界面，扩展 UI 代码可以从 URL 的查询参数中获取授权码。

#### 交换授权码

接下来，您需要将授权码交换为访问令牌。

扩展必须向 0Auth 授权服务器发送包含以下参数的 `POST` 请求：

```text
POST https://authorization-server.com/token
&client_id=T70hJ3ls5VTYG8ylX3CZsfIu
&client_secret=YABbyHQShPeO1T3NDQZP8q5m3Jpb_UPNmIzqhLDCScSnRyVG
&redirect_uri=${REDIRECT_URI}
&code=N949tDLuf9ai_DaOKyuFBXStCNMQzuQbtC1QbvLv-AXqPJ_f
```

> [!NOTE]
>
> 在此示例中，客户端凭据包含在 `POST` 查询参数中。OAuth 授权服务器可能要求凭据作为 HTTP Basic Authentication 头发送，或可能支持不同的格式。请参阅您的 OAuth 提供商文档了解详情。

### 存储访问令牌

Docker 扩展 SDK 不提供用于存储密钥的具体机制。

强烈建议您使用外部存储源来存储访问令牌。

> [!NOTE]
>
> 用户界面的本地存储在扩展之间是隔离的（一个扩展无法访问另一个扩展的本地存储），并且每个扩展的本地存储在用户卸载扩展时会被删除。

## 下一步

了解如何 [发布和分发您的扩展](../extensions/_index.md)