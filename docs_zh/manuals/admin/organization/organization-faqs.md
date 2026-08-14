---
title: Organization FAQs（组织常见问题）
linkTitle: FAQs（常见问题）
weight: 60
description: 组织常见问题
keywords: Docker, Docker Hub, SSO FAQs, single sign-on, organizations, administration, Docker Home, members, organization management, manage orgs
tags: [FAQ]
aliases:
  - /docker-hub/organization-faqs/
  - /faq/admin/organization-faqs/
  - /admin/faqs/organization-faqs/
---

### How can I see how many active users are in my organization?（如何查看我组织中有多少活跃用户？）

如果你的组织使用软件资产管理（Software Asset Management）工具，你可以使用它来查明有多少用户安装了 Docker Desktop。如果你的组织不使用该软件，你可以进行内部调查以查明谁在使用 Docker Desktop。

更多信息，请参阅 [Identify your Docker users and their Docker accounts](../../admin/organization/setup/onboard.md#step-one-identify-your-docker-users)。

### Do users need to authenticate with Docker before an owner can add them to an organization?（所有者将用户添加到组织之前，用户是否需要先通过 Docker 进行身份验证？）

不需要。组织所有者可以使用用户的电子邮件地址邀请他们，并在邀请过程中将其分配到团队。

### Can I force my organization's members to authenticate before using Docker Desktop and are there any benefits?（我能否强制组织成员在使用 Docker Desktop 之前进行身份验证？这样做有什么好处吗？）

可以。你可以[强制登录](/manuals/enterprise/security/enforce-sign-in/_index.md)。

强制登录的一些好处包括：

- 确保用户获得你订阅的权益。
- 确保 [Image Access Management](/manuals/enterprise/security/hardened-desktop/image-access-management.md) 和 [Registry Access Management](/manuals/enterprise/security/hardened-desktop/registry-access-management.md) 等安全功能得以应用。
- 确保你获得对用户活动的洞察。

### Can I convert my personal Docker ID to an organization account?（我可以将个人 Docker ID 转换为组织账户吗？）

可以。你可以将用户账户转换为组织账户。一旦将用户账户转换为组织，就无法再将其恢复为个人用户账户。

有关先决条件和说明，请参阅 [Convert an account into an organization](setup/convert-account.md)。

### Do organization invitees take up seats?（组织被邀请者会占用席位吗？）

会。被邀请加入组织的用户将占用一个已配置的席位，即使该用户尚未接受邀请。

要管理邀请，请参阅 [Manage organization members](/manuals/admin/organization/manage/members.md)。

### Do organization owners take a seat?（组织所有者会占用席位吗？）

会。组织所有者占用一个席位。

### What is the difference between user, invitee, seat, and member?（user、invitee、seat 和 member 之间有什么区别？）

- User（用户）：拥有 Docker ID 的 Docker 用户。
- Invitee（被邀请者）：管理员已邀请其加入组织但尚未接受邀请的用户。
- Seats（席位）：组织中已购买的席位数。
- Member（成员）：已收到并接受加入组织邀请的用户。Member 也可以指组织内某个团队的成员。

### If I have two organizations and a user belongs to both organizations, do they take up two seats?（如果我有两个组织，而一个用户同时属于这两个组织，他们会占用两个席位吗？）

会。在用户属于两个组织的场景下，他们在每个组织中各占用一个席位。
