---
description: 关于 Docker 单点登录的常见问题
keywords: Docker, Docker Hub, SSO FAQs, single sign-on, administration, security
title: 通用 SSO 常见问题
linkTitle: 通用
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

Docker 支持服务提供商发起（SP-initiated）的 SSO 流程。用户必须登录 Docker Hub 或 Docker Desktop 才能启动 SSO 身份验证流程。

## Docker SSO 是否支持多因素身份验证？

当组织使用 SSO 时，多因素身份验证由身份提供商（IdP）控制，而非 Docker 平台。

## 使用 SSO 时能否保留我的 Docker ID？

拥有个人 Docker ID 的用户保留其仓库、镜像和资产的所有权。强制执行 SSO 后，使用公司域名邮箱的现有账户将关联到组织。没有现有账户的用户在登录时会自动创建新账户和 Docker ID。

## 配置 SSO 是否需要设置防火墙规则？

只要可以访问 `login.docker.com`，就不需要特定的防火墙规则。该域名通常默认可访问，但如果 SSO 配置遇到问题，某些组织可能需要在防火墙设置中允许该域名。

## Docker 是否会使用我的 IdP 的默认会话超时时间？

是的，Docker 支持通过自定义的 `dockerSessionMinutes` SAML 属性（而非标准的 `SessionNotOnOrAfter` 元素）使用 IdP 的会话超时时间。更多信息请参见 [SSO 属性](/manuals/enterprise/security/provisioning/_index.md#sso-attributes)。