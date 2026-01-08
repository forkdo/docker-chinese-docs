---
title: 强制登录 Docker Desktop
linkTitle: 强制登录
description: 要求用户登录 Docker Desktop 以访问组织权益和安全功能
toc_max: 2
keywords: authentication, registry.json, configure, enforce sign-in, docker desktop, security, .plist, registry key, mac, windows, organization
tags:
- admin
aliases:
- /security/for-admins/configure-sign-in/
- /docker-hub/configure-sign-in/
- /security/for-admins/enforce-sign-in/
weight: 30
---

{{< summary-bar feature_name="Enforce sign-in" >}}

默认情况下，用户可以不登录组织直接使用 Docker Desktop。
当用户未作为组织成员登录时，他们将无法享受订阅权益，并可能绕过组织配置的安全功能。

您可以使用多种方法强制登录，具体取决于您的设置：

- [注册表键方法（仅限 Windows）](methods.md#registry-key-method-windows-only)
- [配置文件方法（仅限 Mac）](methods.md#configuration-profiles-method-mac-only)
- [`.plist` 方法（仅限 Mac）](methods.md#plist-method-mac-only)
- [`registry.json` 方法（通用）](methods.md#registryjson-method-all)

本页面概述了登录强制机制的工作原理。

## 登录强制机制的工作原理

当 Docker Desktop 检测到注册表键、`.plist` 文件或
`registry.json` 文件时：

- 会显示 `需要登录！` 提示，要求用户作为组织成员登录才能使用 Docker Desktop。
- 如果用户使用非组织成员的账户登录，将被自动注销，无法使用 Docker Desktop。他们可以点击 **登录** 使用其他账户重试。
- 当用户使用组织成员账户登录后，可以正常使用 Docker Desktop。
- 当用户注销时，`需要登录！` 提示会重新出现，除非他们重新登录，否则无法使用 Docker Desktop。

> [!NOTE]
>
> 强制 Docker Desktop 登录不会影响 Docker CLI 访问。CLI 访问仅对强制单点登录（SSO）的组织进行限制。

## 强制登录与强制单点登录（SSO）的区别

强制 Docker Desktop 登录和[强制 SSO](/manuals/enterprise/security/single-sign-on/connect.md#optional-enforce-sso) 是不同的功能，服务于不同的目的：

| 强制类型                       | 描述                                                     | 优势                                                                                                                                                                                                                                                   |
|:----------------------------------|:----------------------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 仅强制登录              | 用户必须登录后才能使用 Docker Desktop                 | 确保用户获得订阅权益，确保应用安全功能。此外，您可以获得用户的活动洞察。                                                                                                                                                                                                                                    |
| 仅强制单点登录（SSO） | 如果用户登录，必须使用 SSO 登录                  | 集中身份验证，强制执行身份提供商设置的统一策略。                                                                                                                                                                                                                                     |
| 同时强制两者                      | 用户必须使用 SSO 登录后才能使用 Docker Desktop       | 确保用户获得订阅权益，确保应用安全功能。此外，您可以获得用户的活动洞察。同时集中身份验证，强制执行身份提供商设置的统一策略。 |
| 两者都不强制                   | 如果用户登录，可以使用 SSO 或 Docker 凭据 | 允许用户无障碍访问 Docker Desktop，但会降低安全性和洞察力。                                                                                                                                                  |

## 后续步骤

- 如需设置登录强制，请参阅 [配置登录强制](/manuals/enterprise/security/enforce-sign-in/methods.md)。
- 如需配置 SSO 强制，请参阅 [强制 SSO](/manuals/enterprise/security/single-sign-on/connect.md)。