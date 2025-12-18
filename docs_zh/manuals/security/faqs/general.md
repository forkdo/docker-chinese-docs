---
description: 关于 Docker 安全、身份验证和组织管理的常见问题解答
keywords: Docker 安全, 常见问题, 身份验证, SSO, 漏洞报告, 会话管理
title: 通用安全常见问题
linkTitle: 通用
weight: 10
tags: [FAQ]
aliases:
- /faq/security/general/
---

## 如何报告漏洞？

如果您发现 Docker 存在安全漏洞，请负责任地将其报告至 security@docker.com，以便 Docker 团队能够快速处理。

## Docker 是否在登录失败后锁定用户？

Docker Hub 在 5 分钟内发生 10 次失败登录尝试后会锁定用户。锁定时长为 5 分钟。此策略适用于 Docker Hub、Docker Desktop 和 Docker Scout 的身份验证。

## 你们是否支持通过 YubiKey 等物理设备进行多因素身份验证（MFA）？

您可以通过 SSO 与身份提供商（IdP）配置物理多因素身份验证（MFA）。请咨询您的 IdP 是否支持 YubiKey 等物理 MFA 设备。

## 会话如何管理？会过期吗？

Docker 使用令牌管理用户会话，具有不同的过期时间：

- Docker Desktop：90 天后或 30 天不活动后自动退出登录
- Docker Hub 和 Docker Home：24 小时后自动退出登录

Docker 还通过 SAML 属性支持您的 IdP 默认会话超时设置。更多信息，请参阅 [SSO 属性](/manuals/enterprise/security/provisioning/_index.md#sso-attributes)。

## Docker 如何区分员工用户和合同工用户？

组织使用已验证域名来区分用户类型。组织中电子邮件域名非已验证域名的成员将显示为“访客”用户。

## 活动日志保留多长时间？

Docker 活动日志保留 90 天。您需要自行导出日志或将日志发送到内部系统以实现更长时间的保留。

## 我可以导出包含用户角色和权限的列表吗？

可以，使用 [导出成员](../../admin/organization/members.md#export-members) 功能可导出包含组织用户及其角色和团队信息的 CSV 文件。

## Docker Desktop 如何处理身份验证信息？

Docker Desktop 使用主机操作系统的安全密钥管理来存储身份验证令牌：

- macOS：[Keychain](https://support.apple.com/guide/security/keychain-data-protection-secb0694df1a/web)
- Windows：[通过 Wincred 的安全和身份 API](https://learn.microsoft.com/en-us/windows/win32/api/wincred/)
- Linux：[Pass](https://www.passwordstore.org/)。

## 使用 SSO 但未启用 SCIM 时，如何移除不属于我 IdP 的用户？

如果未启用 SCIM，则必须手动从组织中移除用户。SCIM 可以自动移除用户，但仅适用于在启用 SCIM 之后添加的用户。在启用 SCIM 之前添加的用户必须手动移除。

更多信息，请参阅 [管理组织成员](/manuals/admin/organization/members.md)。

## Scout 从容器镜像收集哪些元数据？

有关 Docker Scout 存储的元数据信息，请参阅 [数据处理](/manuals/scout/deep-dive/data-handling.md)。

## Marketplace 扩展如何进行安全审核？

扩展的安全审核已列入路线图，但目前尚未实施。扩展不在 Docker 第三方风险管理计划的覆盖范围内。

## 我能否阻止用户向 Docker Hub 私有仓库推送镜像？

没有直接设置可禁用私有仓库。但是，[注册表访问管理](/manuals/enterprise/security/hardened-desktop/registry-access-management.md) 允许管理员通过管理控制台控制开发者可通过 Docker Desktop 访问哪些注册表。