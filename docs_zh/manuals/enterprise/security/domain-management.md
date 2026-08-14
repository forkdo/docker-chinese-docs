---
title: 添加和管理域名
description: 为 Docker 组织添加、验证和管理域名以控制用户访问并启用自动配置
keywords: 域名管理, 域名验证, 自动配置, 用户管理, DNS, TXT 记录, Docker Home
weight: 10
aliases:
 - /security/for-admins/domain-management/
---

{{< summary-bar feature_name="Domain management" >}}

域名管理允许您为组织添加和验证域名，然后启用自动配置，以便在用户使用与您已验证域名匹配的电子邮件地址登录时自动将其添加到组织中。这种方法简化了用户管理，确保一致的安全设置，并降低未受管理的用户在无可见性或控制的情况下访问 Docker 的风险。

本页面提供添加和删除域名、配置自动配置以及审核未捕获用户的操作步骤。

## 添加和验证域名

添加域名需要验证以确认所有权。验证过程使用 DNS 记录来证明您控制该域名。

### 添加域名

1. 登录 [Docker Home](https://app.docker.com) 并选择您的组织。如果您的组织属于一家公司，请选择该公司并在公司级别为组织配置域名。
1. 选择 **Identity & auth**，然后选择 **域名管理**。
1. 选择 **添加域名**。
1. 输入您的域名并选择 **添加域名**。
1. 在弹出的模态框中，复制 **TXT 记录值** 以验证您的域名。

### 验证域名

验证通过在域名系统 (DNS) 主机中添加 TXT 记录来确认您拥有该域名。DNS 更改可能需要长达 72 小时才能传播。Docker 会自动检查该记录，一旦确认更改，即确认所有权。

> [!TIP]
>
> 记录名称字段决定了 TXT 记录在您的域名中的添加位置（根域名或子域名）。对于根域名（如 `example.com`），请使用 `@` 或留空记录名称，具体取决于您的提供商。不要输入诸如 docker、`docker-verification`、`www` 或您的域名名称等值，因为这些可能会指向错误的位置。请查阅您的 DNS 提供商的文档以确认记录名称要求。

按照您的 DNS 提供商的步骤添加 **TXT 记录值**。如果您的提供商未列出，请使用“其他提供商”的步骤：

{{< tabs >}}
{{< tab name="AWS Route 53" >}}

1. 按照 [使用 Amazon Route 53 控制台创建记录](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resource-record-sets-creating.html) 添加您的 TXT 记录到 AWS。
1. 等待最长 72 小时以完成 TXT 记录验证。
1. 返回 **Identity & auth**，然后 **域名管理**，并在域名旁选择 **验证**。

{{< /tab >}}
{{< tab name="Google Cloud DNS" >}}

1. 按照 [使用 TXT 记录验证您的域名](https://cloud.google.com/identity/docs/verify-domain-txt) 添加您的 TXT 记录到 Google Cloud DNS。
1. 等待最长 72 小时以完成 TXT 记录验证。
1. 返回 **Identity & auth**，然后 **域名管理**，并在域名旁选择 **验证**。

{{< /tab >}}
{{< tab name="GoDaddy" >}}

1. 按照 [添加 TXT 记录](https://www.godaddy.com/help/add-a-txt-record-19232) 添加您的 TXT 记录到 GoDaddy。
1. 等待最长 72 小时以完成 TXT 记录验证。
1. 返回 **Identity & auth**，然后 **域名管理**，并在域名旁选择 **验证**。

{{< /tab >}}
{{< tab name="Other providers" >}}

1. 登录您的域名主机。
1. 使用 Docker 提供的 **TXT 记录值** 在 DNS 设置中添加 TXT 记录。
1. 等待最长 72 小时以完成 TXT 记录验证。
1. 返回 **Identity & auth**，然后 **域名管理**，并在域名旁选择 **验证**。

{{< /tab >}}
{{< /tabs >}}

## 审核域名以识别未捕获的用户

域名审核可识别未捕获的用户。未捕获的用户是指使用与您已验证域名关联的电子邮件地址登录 Docker 但不是您 Docker 组织成员的用户。

### 限制

域名审核无法识别：

- 无需登录即可访问 Docker Desktop 的用户
- 使用未与您已验证域名之一关联电子邮件地址的账户登录的用户

为防止无法识别的用户访问 Docker Desktop，请 [强制登录](/manuals/enterprise/security/enforce-sign-in/_index.md)。

### 运行域名审核

1. 登录 [Docker Home](https://app.docker.com) 并选择您的公司。
1. 选择 **Identity & auth**，然后 **域名管理**。
1. 在 **域名审核** 中，选择 **导出用户** 以导出未捕获用户的 CSV 文件。

CSV 文件包含以下列：
- 姓名：Docker 用户的显示名称
- 用户名：用户的 Docker ID
- 邮箱：用户的电子邮件地址

### 邀请未捕获的用户

您可以使用导出的 CSV 文件批量邀请未捕获的用户加入您的组织。有关批量邀请用户的信息，请参阅 [管理组织成员](/manuals/admin/organization/manage/members.md)。

## 自动配置

[自动配置](/manuals/enterprise/security/provisioning/auto-provisioning.md) 使用已验证的域名将组织成员与匹配已验证域名的电子邮件地址关联起来。要覆盖自动配置，您可以配置以下两种方法之一：

- [即时（JIT）](/manuals/enterprise/security/provisioning/just-in-time.md) 配置
- [跨域身份管理系统（SCIM）](/manuals/enterprise/security/provisioning/scim/_index.md)

## 删除域名

删除域名将移除其 TXT 记录值并禁用任何相关的自动配置。

> [!WARNING]
>
> 删除域名将禁用该域名的自动配置并移除验证。此操作不可撤销。

要删除域名：

1. 登录 [Docker Home](https://app.docker.com) 并选择您的组织。如果您的组织属于一家公司，请选择该公司并在公司级别为组织配置域名。
1. 选择 **Identity & auth**，然后 **域名管理**。
1. 对于要删除的域名，选择 **操作** 菜单，然后选择 **删除域名**。
1. 在弹出的模态框中，选择 **删除域名** 以确认。
