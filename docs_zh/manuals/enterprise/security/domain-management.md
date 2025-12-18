---
title: 管理域名
description: 添加、验证和管理域名，以控制用户访问并为 Docker 组织启用自动配置
keywords: 域名管理, 域名验证, 自动配置, 用户管理, DNS, TXT 记录, 管理控制台
weight: 55
aliases:
 - /security/for-admins/domain-management/
---

{{< summary-bar feature_name="Domain management" >}}

域名管理允许您为组织添加并验证域名，然后启用自动配置，当用户使用与已验证域名匹配的电子邮件地址登录时，系统会自动将其添加到组织中。这种方法简化了用户管理，确保一致的安全设置，并降低未受管理的用户在无可见性或控制的情况下访问 Docker 的风险。

本文档提供添加和删除域名、配置自动配置以及审核未捕获用户的步骤。

## 添加并验证域名

添加域名需要通过验证来确认所有权。验证过程使用 DNS 记录来证明您控制该域名。

### 添加域名

1. 登录到 [Docker Home](https://app.docker.com) 并选择您的组织。如果您的组织属于某个公司，请选择该公司，并在公司级别为组织配置域名。
1. 选择 **Admin Console**，然后选择 **Domain management**。
1. 选择 **Add a domain**。
1. 输入您的域名并选择 **Add domain**。
1. 在弹出的模态框中，复制 **TXT Record Value** 以验证您的域名。

### 验证域名

验证通过在您的域名系统 (DNS) 托管商处添加 TXT 记录来确认您拥有该域名。DNS 变更最多可能需要 72 小时才能传播。Docker 会自动检查记录，并在识别到变更后确认所有权。

> [!TIP]
>
> 记录名称字段决定 TXT 记录添加在域名的哪个位置（根域名或子域名）。对于 `example.com` 等根域名，在记录名称中使用 `@` 或留空，具体取决于您的提供商。不要输入 `docker`、`docker-verification`、`www` 或您的域名等值，因为这些可能会指向错误的位置。请查看您的 DNS 提供商文档以确认记录名称要求。

按照您的 DNS 提供商的步骤添加 **TXT Record Value**。如果您的提供商未在以下列表中，请使用“其他提供商”的步骤：

{{< tabs >}}
{{< tab name="AWS Route 53" >}}

1. 通过遵循 [使用 Amazon Route 53 控制台创建记录](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resource-record-sets-creating.html) 将您的 TXT 记录添加到 AWS。
1. 等待最多 72 小时以完成 TXT 记录验证。
1. 返回 [Admin Console](https://app.docker.com/admin) 的 **Domain management** 页面，并在您的域名旁选择 **Verify**。

{{< /tab >}}
{{< tab name="Google Cloud DNS" >}}

1. 通过遵循 [使用 TXT 记录验证您的域名](https://cloud.google.com/identity/docs/verify-domain-txt) 将您的 TXT 记录添加到 Google Cloud DNS。
1. 等待最多 72 小时以完成 TXT 记录验证。
1. 返回 [Admin Console](https://app.docker.com/admin) 的 **Domain management** 页面，并在您的域名旁选择 **Verify**。

{{< /tab >}}
{{< tab name="GoDaddy" >}}

1. 通过遵循 [添加 TXT 记录](https://www.godaddy.com/help/add-a-txt-record-19232) 将您的 TXT 记录添加到 GoDaddy。
1. 等待最多 72 小时以完成 TXT 记录验证。
1. 返回 [Admin Console](https://app.docker.com/admin) 的 **Domain management** 页面，并在您的域名旁选择 **Verify**。

{{< /tab >}}
{{< tab name="Other providers" >}}

1. 登录到您的域名托管商。
1. 使用来自 Docker 的 **TXT Record Value** 在您的 DNS 设置中添加 TXT 记录。
1. 等待最多 72 小时以完成 TXT 记录验证。
1. 返回 [Admin Console](https://app.docker.com/admin) 的 **Domain management** 页面，并在您的域名旁选择 **Verify**。

{{< /tab >}}
{{< /tabs >}}

## 配置自动配置

自动配置会在用户使用与您已验证域名匹配的电子邮件地址登录 Docker 时，自动将其添加到您的组织中。您必须先验证域名，然后才能启用自动配置。

> [!IMPORTANT]
>
> 对于属于 SSO 连接一部分的域名，即时预配 (JIT) 在向组织添加用户时优先于自动配置。

### 自动配置的工作原理

启用已验证域名的自动配置后：

- 使用匹配电子邮件地址登录 Docker 的用户将自动添加到您的组织中。
- 自动配置仅将现有的 Docker 用户添加到您的组织，不会创建新账户。
- 用户的登录流程不会发生任何变化。
- 公司和组织所有者在添加新用户时会收到电子邮件通知。
- 您可能需要 [管理席位](/manuals/subscription/manage-seats.md) 以容纳新用户。

### 启用自动配置

自动配置按域名配置。要启用它：

1. 登录到 [Docker Home](https://app.docker.com) 并选择您的公司或组织。
1. 选择 **Admin Console**，然后选择 **Domain management**。
1. 选择您要启用自动配置的域名旁边的 **Actions menu**。
1. 选择 **Enable auto-provisioning**。
1. 可选。如果在公司级别启用自动配置，请选择一个组织。
1. 选择 **Enable** 以确认。

域名的 **Auto-provisioning** 列将更新为 **Enabled**。

### 禁用自动配置

要禁用用户的自动配置：

1. 登录到 [Docker Home](https://app.docker.com) 并选择您的组织。如果您的组织属于某个公司，请选择该公司，并在公司级别为组织配置域名。
1. 选择 **Admin Console**，然后选择 **Domain management**。
1. 在您的域名旁，选择 **Actions menu**，然后选择 **Disable auto-provisioning**。
1. 选择 **Disable** 以确认。

## 审核域名以查找未捕获的用户

{{< summary-bar feature_name="Domain audit" >}}

域名审核可识别未捕获的用户。未捕获的用户是指使用与您已验证域名关联的电子邮件地址进行身份验证，但不是您的 Docker 组织成员的 Docker 用户。

### 限制

域名审核无法识别：

- 未进行身份验证就访问 Docker 的用户
- 使用未关联您任一已验证域名的电子邮件地址进行身份验证的用户

为防止无法识别的用户访问 Docker Desktop，请[强制登录](/manuals/enterprise/security/enforce-sign-in/_index.md)。

### 运行域名审核

1. 登录到 [Docker Home](https://app.docker.com) 并选择您的公司。
1. 选择 **Admin Console**，然后选择 **Domain management**。
1. 在 **Domain audit** 中，选择 **Export Users** 以导出未捕获用户的 CSV 文件。

CSV 文件包含以下列：
- Name：Docker 用户的显示名称
- Username：用户的 Docker ID
- Email：用户的电子邮件地址

### 邀请未捕获的用户

您可以使用导出的 CSV 文件批量邀请未捕获的用户加入您的组织。有关批量邀请用户的更多信息，请参阅 [管理组织成员](/manuals/admin/organization/members.md)。

## 删除域名

删除域名将移除其 TXT 记录值并禁用任何关联的自动配置。

>[!WARNING]
>
> 删除域名将禁用该域名的自动配置并移除验证。此操作无法撤销。

要删除域名：

1. 登录到 [Docker Home](https://app.docker.com) 并选择您的组织。如果您的组织属于某个公司，请选择该公司，并在公司级别为组织配置域名。
1. 选择 **Admin Console**，然后选择 **Domain management**。
1. 对于要删除的域名，选择 **Actions** 菜单，然后选择 **Delete domain**。
1. 为确认，请在弹出的模态框中选择 **Delete domain**。