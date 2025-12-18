---
description: 关于 Docker 单点登录的常见问题
keywords: Docker, Docker Hub, SSO 常见问题, 单点登录, 管理, 安全
title: 一般 SSO 常见问题
linkTitle: 一般
weight: 10
tags: [FAQ]
aliases:
- /single-sign-on/faqs/
- /faq/security/single-sign-on/faqs/
- /single-sign-on/saml-faqs/
- /faq/security/single-sign-on/saml-faqs/
- /security/faqs/single-sign-on/saml-faqs/
- /security/faqs/single-sign-on/faqs/
---

## Docker 支持哪些 SSO 流程？

Docker 支持服务提供商发起（SP-initiated）的 SSO 流程。用户必须登录 Docker Hub 或 Docker Desktop 以启动 SSO 认证过程。

## Docker SSO 是否支持多因素认证？

当组织使用 SSO 时，多因素认证由身份提供商（IdP）控制，而不是由 Docker 平台控制。

## 使用 SSO 时我可以保留我的 Docker ID 吗？

拥有个人 Docker ID 的用户保留其仓库、镜像和资源的所有权。当强制执行 SSO 时，使用公司域名邮箱的现有账户将连接到组织。没有现有账户的用户在登录时会自动创建新的账户和 Docker ID。

## SSO 配置是否需要防火墙规则？

不需要特定的防火墙规则，只要 `login.docker.com` 可访问即可。此域名通常默认可访问，但如果 SSO 设置遇到问题，某些组织可能需要在其防火墙设置中允许该域名。

## Docker 是否使用我的 IdP 的默认会话超时设置？

是的，Docker 使用自定义的 `dockerSessionMinutes` SAML 属性（而不是标准的 `SessionNotOnOrAfter` 元素）来支持您的 IdP 的会话超时设置。更多信息请参见 [SSO 属性](/manuals/enterprise/security/provisioning/_index.md#sso-attributes)。