---
title: SSO 身份提供程序常见问题解答
linkTitle: 身份提供程序
description: 有关 Docker SSO 和身份提供程序配置的常见问题解答
keywords: identity providers, SSO IdP, SAML, Azure AD, Entra ID, certificate management
tags: [FAQ]
aliases:
- /single-sign-on/idp-faqs/
- /faq/security/single-sign-on/idp-faqs/
- /security/faqs/single-sign-on/idp-faqs/
---

## 我可以在 Docker SSO 中使用多个身份提供程序吗？

是的，Docker 支持多个 IdP 配置。一个域可以关联多个 IdP。Docker 支持 Entra ID（原 Azure AD）以及支持 SAML 2.0 的身份提供程序。

## 配置 SSO 后可以更换身份提供程序吗？

可以。在 Docker SSO 连接中删除现有的 IdP 配置，然后[使用新的 IdP 配置 SSO](/manuals/enterprise/security/single-sign-on/connect.md)。如果您已开启强制执行，请在更新提供程序连接之前关闭强制执行。

## 配置 SSO 需要从身份提供程序获取哪些信息？

要在 Docker 中开启 SSO，您需要从 IdP 获取以下信息：

- SAML：实体 ID、ACS URL、单点注销 URL 和公钥 X.509 证书
- Entra ID（原 Azure AD）：客户端 ID、客户端密钥、AD 域

## 如果现有证书过期会发生什么？

如果证书过期，请联系您的身份提供程序以获取新的 X.509 证书。然后在 Docker 管理控制台的 [SSO 配置设置](/manuals/enterprise/security/single-sign-on/manage.md#manage-sso-connections)中更新证书。

## 如果 SSO 开启后 IdP 发生故障会发生什么？

如果 SSO 处于强制执行状态，当您的 IdP 发生故障时，用户将无法访问 Docker Hub。用户仍然可以使用个人访问令牌从 CLI 访问 Docker Hub 镜像。

如果 SSO 已开启但未强制执行，用户可以回退到用户名/密码身份验证。

## 机器人账号是否需要席位才能访问使用 SSO 的组织？

是的，机器人账号需要像普通用户一样拥有席位，需要在 IdP 中使用非别名域电子邮件，并在 Docker Hub 中使用一个席位。您可以将机器人账号添加到您的 IdP，并创建访问令牌以替代其他凭据。

## SAML SSO 是否使用即时配置？

SSO 实现默认使用即时 (JIT) 配置。如果您使用 SCIM 开启自动配置，可以选择在管理控制台中关闭 JIT。请参阅[即时配置](/security/for-admins/provisioning/just-in-time/)。

## 我的 Entra ID SSO 连接无法工作并显示错误。如何解决此问题？

确认您已在 Entra ID 中为 SSO 连接配置了必要的 API 权限。您需要在 Entra ID 租户中授予管理员同意。请参阅 [Entra ID（原 Azure AD）文档](https://learn.microsoft.com/en-us/azure/active-directory/manage-apps/grant-admin-consent?pivots=portal#grant-admin-consent-in-app-registrations)。