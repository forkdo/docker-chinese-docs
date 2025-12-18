---
title: 强制 Docker Desktop 登录
linkTitle: 强制登录
description: 要求用户登录 Docker Desktop 以访问组织权益和安全功能
toc_max: 2
keywords: authentication, registry.json, configure, enforce sign-in, docker desktop, security, .plist, registry key, mac, windows, organization
tags: [admin]
aliases:
 - /security/for-admins/configure-sign-in/
 - /docker-hub/configure-sign-in/
 - /security/for-admins/enforce-sign-in/
weight: 30
---

{{< summary-bar feature_name="强制登录" >}}

默认情况下，用户可以不登录组织直接访问 Docker Desktop。
当用户未以组织成员身份登录时，他们将无法享受订阅权益，并可能绕过组织配置的安全功能。

您可以使用以下几种方法强制登录，具体取决于您的设置：

- [注册表键方法（仅限 Windows）](methods.md#注册表键方法-仅限-windows)
- [配置文件方法（仅限 Mac）](methods.md#配置文件方法-仅限-mac)
- [`.plist` 方法（仅限 Mac）](methods.md#plist-方法-仅限-mac)
- [`registry.json` 方法（全部）](methods.md#registryjson-方法-全部)

本文档提供了登录强制机制的工作原理概述。

## 登录强制的工作原理

当 Docker Desktop 检测到注册表键、`.plist` 文件或
`registry.json` 文件时：

- 会显示 `需要登录！` 提示，要求用户以组织成员身份登录才能使用 Docker Desktop。
- 如果用户使用非组织成员的账户登录，将被自动登出，无法使用 Docker Desktop。他们可以点击 **登录** 尝试使用其他账户重新登录。
- 当用户使用组织成员账户登录时，可以正常使用 Docker Desktop。
- 当用户登出后，`需要登录！` 提示会重新出现，除非他们重新登录，否则无法使用 Docker Desktop。

> [!NOTE]
>
> 强制 Docker Desktop 登录不会影响 Docker CLI 的访问。CLI 访问仅对强制单点登录（SSO）的组织进行限制。

## 强制登录与强制单点登录（SSO）的区别

强制 Docker Desktop 登录和 [强制 SSO](/manuals/enterprise/security/single-sign-on/connect.md#可选-强制-sso) 是两个不同的功能，服务于不同的目的：

| 强制类型                       | 描述                                                     | 优势                                                                                                                                                                                                                                                   |
|:----------------------------------|:----------------------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 仅强制登录              | 用户必须登录后才能使用 Docker Desktop                 | 确保用户获得组织订阅的权益，并确保应用安全功能。此外，您可以获得用户活动的洞察。                                                                                                                                                                    |
| 仅强制单点登录（SSO） | 如果用户登录，必须使用 SSO 登录                  | 集中身份验证并强制执行身份提供商设置的统一策略。                                                                                                                                                                     |
| 两者都强制                      | 用户必须使用 SSO 登录后才能使用 Docker Desktop       | 确保用户获得组织订阅的权益，并确保应用安全功能。此外，您可以获得用户活动的洞察。同时集中身份验证并强制执行身份提供商设置的统一策略。 |
| 两者都不强制                   | 如果用户登录，可以使用 SSO 或 Docker 凭据登录 | 允许用户无阻碍地访问 Docker Desktop，但会降低安全性和洞察力。                                                                                                                                                  |

## 后续步骤

- 要设置登录强制，请参阅 [配置登录强制](/manuals/enterprise/security/enforce-sign-in/methods.md)。
- 要配置 SSO 强制，请参阅 [强制 SSO](/manuals/enterprise/security/single-sign-on/connect.md)。