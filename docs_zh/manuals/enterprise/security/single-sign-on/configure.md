---
title: 配置单点登录
linkTitle: 配置
description: 了解如何为您的组织或公司配置单点登录。
keywords: configure, sso, docker hub, hub, docker admin, admin, security
aliases:
  - /docker-hub/domains/
  - /docker-hub/sso-connection/
  - /docker-hub/enforcing-sso/
  - /single-sign-on/configure/
  - /admin/company/settings/sso-configuration/
  - /admin/organization/security-settings/sso-configuration/
  - /security/for-admins/single-sign-on/configure/
---

{{< summary-bar feature_name="SSO" >}}

了解如何通过添加并验证成员用于登录的域名，为您的 Docker 组织设置单点登录 (SSO)。

## 第一步：添加域名

> [!NOTE]
>
> Docker 支持多个身份提供商 (IdP) 配置。您可以将一个域名与多个 IdP 关联。

添加域名：

1. 登录 [Docker Home](https://app.docker.com) 并选择您的组织。如果该组织是公司的一部分，请先选择公司以在该级别管理域名。
1. 选择 **Admin Console**，然后选择 **Domain management**。
1. 选择 **Add a domain**。
1. 在文本框中输入您的域名，然后选择 **Add domain**。
1. 在弹出的窗口中，复制为域名验证提供的 **TXT Record Value**。

## 第二步：验证您的域名

要确认域名所有权，请使用 Docker 提供的 TXT 记录值向您的域名系统 (DNS) 主机添加 TXT 记录。DNS 传播最多可能需要 72 小时。Docker 会在此期间自动检查记录。

> [!TIP]
>
> 添加记录名称时，对于根域名（如 `example.com`），**请使用 `@` 或留空**。**避免使用常见值**，如 `docker`、`docker-verification`、`www` 或您的域名本身。请务必**查阅您的 DNS 提供商文档**以验证其特定的记录名称要求。

{{< tabs >}}
{{< tab name="AWS Route 53" >}}

1. 要将 TXT 记录添加到 AWS，请参阅 [使用 Amazon Route 53 控制台创建记录](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resource-record-sets-creating.html)。
1. 等待 TXT 记录验证，最长 72 小时。
1. 记录生效后，转到 [Admin Console](https://app.docker.com/admin) 中的 **Domain management** 并选择 **Verify**。

{{< /tab >}}
{{< tab name="Google Cloud DNS" >}}

1. 要将 TXT 记录添加到 Google Cloud DNS，请参阅 [使用 TXT 记录验证您的域名](https://cloud.google.com/identity/docs/verify-domain-txt)。
1. 等待 TXT 记录验证，最长 72 小时。
1. 记录生效后，转到 [Admin Console](https://app.docker.com/admin) 中的 **Domain management** 并选择 **Verify**。

{{< /tab >}}
{{< tab name="GoDaddy" >}}

1. 要将 TXT 记录添加到 GoDaddy，请参阅 [添加 TXT 记录](https://www.godaddy.com/help/add-a-txt-record-19232)。
1. 等待 TXT 记录验证，最长 72 小时。
1. 记录生效后，转到 [Admin Console](https://app.docker.com/admin) 中的 **Domain management** 并选择 **Verify**。

{{< /tab >}}
{{< tab name="其他提供商" >}}

1. 登录您的域名主机。
1. 向您的 DNS 设置添加 TXT 记录并保存该记录。
1. 等待 TXT 记录验证，最长 72 小时。
1. 记录生效后，转到 [Admin Console](https://app.docker.com/admin) 中的 **Domain management** 并选择 **Verify**。

{{< /tab >}}
{{< /tabs >}}

## 后续步骤

- [连接 Docker 和您的 IdP](connect.md)。
- [排查](/manuals/enterprise/troubleshoot/troubleshoot-sso.md) SSO 问题。