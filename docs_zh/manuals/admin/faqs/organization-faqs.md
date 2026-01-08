---
description: 组织常见问题解答
linkTitle: 组织
weight: 20
keywords: Docker, Docker Hub, SSO FAQs, single sign-on, organizations, administration, Admin Console, members, organization management, manage orgs
title: 关于组织的常见问题解答
tags:
- FAQ
aliases:
- /docker-hub/organization-faqs/
- /faq/admin/organization-faqs/
---

### 如何查看我的组织中有多少活跃用户？

如果您的组织使用 Software Asset Management 工具，您可以使用它来查明有多少用户安装了 Docker Desktop。如果您的组织不使用此软件，您可以进行一次内部调查，以查明谁在使用 Docker Desktop。

有关更多信息，请参阅 [识别您的 Docker 用户及其 Docker 账户](../../admin/organization/onboard.md#step-1-identify-your-docker-users-and-their-docker-accounts)。

### 在 owner 将用户添加到组织之前，用户是否需要向 Docker 进行身份验证？

不需要。Organization owners 可以使用电子邮件地址邀请用户，也可以在邀请过程中将他们分配给一个团队。

### 我是否可以强制组织 members 在使用 Docker Desktop 之前进行身份验证？这样做有什么好处吗？

可以。您可以 [强制登录](/manuals/enterprise/security/enforce-sign-in/_index.md)。

强制登录的一些好处包括：

- Administrators 可以强制执行 [Image Access Management](/manuals/enterprise/security/hardened-desktop/image-access-management.md) 和 [Registry Access Management](/manuals/enterprise/security/hardened-desktop/registry-access-management.md) 等功能。
 - Administrators 可以通过阻止未以组织 members 身份登录的用户使用 Docker Desktop 来确保合规性。

### 我可以把我个人的 Docker ID 转换为组织账户吗？

可以。您可以将您的用户账户转换为组织账户。一旦将用户账户转换为组织，就无法再将其恢复为个人用户账户。

有关先决条件和说明，请参阅 [将账户转换为组织](convert-account.md)。

### organization 的 invitees 会占用 seats 吗？

是的。被邀请加入 organization 的用户将占用一个已配置的 seats，即使用户尚未接受邀请。

要管理邀请，请参阅 [管理 organization members](/manuals/admin/organization/members.md)。

### organization owners 会占用 seat 吗？

是的。Organization owners 占用一个 seat。

### user、invitee、seat 和 member 之间有什么区别？

- User: 拥有 Docker ID 的 Docker user。
- Invitee: 已被 administrator 邀请加入 organization 但尚未接受邀请的用户。
- Seats: organization 中购买的 seats 数量。
- Member: 已收到并接受加入 organization 邀请的用户。Member 也可以指 organization 中某个团队的成员。

### 如果我有两个 organizations，且一个用户同时属于这两个 organizations，他们会占用两个 seats 吗？

是的。在一个用户属于两个 organizations 的情况下，他们在每个 organization 中各占用一个 seat。