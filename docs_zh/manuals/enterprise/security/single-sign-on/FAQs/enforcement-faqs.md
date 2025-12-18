---
title: SSO 强制执行常见问题
linkTitle: 强制执行
description: 关于 Docker 单点登录强制执行及其对用户影响的常见问题
keywords: SSO 强制执行, 单点登录, 个人访问令牌, CLI 认证, 访客用户
tags: [FAQ]
aliases:
- /single-sign-on/enforcement-faqs/
- /faq/security/single-sign-on/enforcement-faqs/
- /security/faqs/single-sign-on/enforcement-faqs/
---

## Docker SSO 是否支持通过命令行进行认证？

当 SSO 被强制执行时，[密码将无法用于访问 Docker CLI](/security/security-announcements/#deprecation-of-password-logins-on-cli-when-sso-enforced)。您必须改用个人访问令牌 (PAT) 进行 CLI 认证。

每个用户都必须创建一个 PAT 才能访问 CLI。要了解如何创建 PAT，请参阅 [管理个人访问令牌](/security/access-tokens/)。在 SSO 强制执行之前已经使用 PAT 的用户可以继续使用该 PAT。

## SSO 如何影响自动化系统和 CI/CD 流水线？

在强制执行 SSO 之前，您必须[创建个人访问令牌](/security/access-tokens/) 来替换自动化系统和 CI/CD 流水线中的密码。

## 我可以启用 SSO 但不立即强制执行吗？

可以，您可以启用 SSO 但不强制执行。用户可以在登录屏幕上选择使用 Docker ID（标准的电子邮件和密码）或域验证的电子邮件地址（SSO）。

## SSO 已被强制执行，但某个用户仍可以使用用户名和密码登录。为什么会发生这种情况？

不属于您注册域但已被邀请到您组织的访客用户不会通过您的 SSO 身份提供商登录。SSO 强制执行仅适用于属于您已验证域的用户。

## 我可以在投入生产之前测试 SSO 功能吗？

可以，您可以创建一个拥有 5 个席位的 Business 订阅的测试组织。测试时，启用 SSO 但不要强制执行，否则所有域邮箱用户都会被强制登录到测试环境。

## 强制执行 SSO 和强制执行登录有什么区别？

这些是您可以独立使用或组合使用的不同功能：

- 强制执行 SSO 确保用户使用 SSO 凭据而不是 Docker ID 登录，从而实现更好的凭据管理。
- 强制执行 Docker Desktop 登录可确保用户始终登录到您组织成员的账户，以便始终应用安全设置和订阅权益。

更多详细信息，请参阅 [强制登录 Desktop](/manuals/enterprise/security/enforce-sign-in/_index.md#enforcing-sign-in-versus-enforcing-single-sign-on-sso)。