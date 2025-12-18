---
title: SSO 身份提供商常见问题
linkTitle: 身份提供商
description: Docker SSO 和身份提供商配置的常见问题解答
keywords: identity providers, SSO IdP, SAML, Azure AD, Entra ID, certificate management
tags: [FAQ]
aliases:
- /single-sign-on/idp-faqs/
- /faq/security/single-sign-on/idp-faqs/
- /security/faqs/single-sign-on/idp-faqs/
---

## 我可以对 Docker SSO 使用多个身份提供商吗？

可以，Docker 支持多个 IdP 配置。一个域名可以关联到多个 IdP。Docker 支持 Entra ID（前 Azure AD）以及支持 SAML 2.0 的身份提供商。

## 配置 SSO 后可以更改我的身份提供商吗？

可以。在 Docker SSO 连接中删除现有的 IdP 配置，然后使用新的 IdP [配置 SSO](/manuals/enterprise/security/single-sign-on/connect.md)。如果您已启用强制执行，请在更新提供商连接之前先关闭强制执行。

## 配置 SSO 时，我需要从身份提供商获取哪些信息？

要在 Docker 中启用 SSO，您需要从 IdP 获取以下信息：

- SAML：实体 ID、ACS URL、单一注销 URL 以及公共 X.509 证书
- Entra ID（前 Azure AD）：客户端 ID、客户端密钥、AD 域

## 如果我的现有证书过期会怎样？

如果您的证书过期，请联系您的身份提供商以获取新的 X.509 证书。然后在 Docker Admin Console 的 [SSO 配置设置](/manuals/enterprise/security/single-sign-on/manage.md#manage-sso-connections) 中更新证书。

## 当 SSO 启用时，如果我的 IdP 出现故障会怎样？

如果 SSO 已强制执行，当您的 IdP 出现故障时，用户将无法访问 Docker Hub。用户仍可使用个人访问令牌通过 CLI 访问 Docker Hub 镜像。

如果 SSO 已启用但未强制执行，用户可以回退到用户名/密码身份验证。

## 机器人账户需要席位才能访问使用 SSO 的组织吗？

是的，机器人账户需要像常规用户一样拥有席位，在 IdP 中需要非别名域名的电子邮件，并且会占用 Docker Hub 中的一个席位。您可以将机器人账户添加到您的 IdP 中，并创建访问令牌以替换其他凭据。

## SAML SSO 是否使用即时预配（Just-in-Time provisioning）？

SSO 实现默认使用即时预配（JIT）。如果您启用了 SCIM 自动预配，可以在 Admin Console 中选择关闭 JIT。参见 [即时预配](/security/for-admins/provisioning/just-in-time/)。

## 我的 Entra ID SSO 连接无法工作并显示错误。如何排查此问题？

请确认您已在 Entra ID 中为 SSO 连接配置了必要的 API 权限。您需要在您的 Entra ID 租户内授予管理员同意。参见 [Entra ID（前 Azure AD）文档](https://learn.microsoft.com/en-us/azure/active-directory/manage-apps/grant-admin-consent?pivots=portal#grant-admin-consent-in-app-registrations)。