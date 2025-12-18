---
title: SSO 域常见问题
linkTitle: 域
description: 关于 Docker 单点登录域验证和管理的常见问题
keywords: SSO 域, 域验证, DNS, TXT 记录, 单点登录
tags: [FAQ]
aliases:
- /single-sign-on/domain-faqs/
- /faq/security/single-sign-on/domain-faqs/
- /security/faqs/single-sign-on/domain-faqs/
---

## 我可以添加子域吗？

是的，您可以向 SSO 连接添加子域。所有电子邮件地址必须使用您已添加到连接中的域。请确认您的 DNS 提供商支持同一域的多个 TXT 记录。

## 我需要永久保留 DNS TXT 记录吗？

完成一次性验证以添加域后，您可以删除 TXT 记录。但是，如果您的组织更改身份提供商并需要重新设置 SSO，则需要再次验证域。

## 我可以为多个组织验证同一个域吗？

您无法在组织级别为多个组织验证同一个域。要为多个组织验证一个域，您必须拥有 Docker Business 订阅并创建一个公司。公司允许在公司级别集中管理组织和域验证。