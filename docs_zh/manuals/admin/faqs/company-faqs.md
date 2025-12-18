---
title: 公司相关常见问题
linkTitle: Company
weight: 30
description: 公司常见问题解答
keywords: Docker, Docker Hub, SSO 常见问题, 单点登录, 公司, 管理, 公司管理
tags: [FAQ]
aliases:
- /docker-hub/company-faqs/
- /faq/admin/company-faqs/
---

### 我的部分组织没有 Docker Business 订阅。我还能使用父公司吗？

可以，但你只能将拥有 Docker Business 订阅的组织添加到公司中。

### 如果我的某个组织降级到非 Docker Business，但我仍需要作为公司所有者访问，会发生什么？

要访问和管理子组织，该组织必须拥有 Docker Business 订阅。如果该组织未包含在此订阅中，组织所有者必须在公司外部自行管理该组织。

### 公司所有者会占用订阅席位吗？

公司所有者不会占用席位，除非满足以下任一条件：

- 被添加为公司下属组织的成员
- 启用了 SSO

尽管公司所有者在公司内所有组织中拥有与组织所有者相同的访问权限，但通常无需将他们添加到任何组织中。否则会导致他们占用一个席位。

首次创建公司时，你的账户同时是公司所有者和组织所有者。在这种情况下，只要你的账户仍是组织所有者，就会占用一个席位。

为避免占用席位，你可以[将另一用户指定为组织所有者](/manuals/admin/organization/members.md#update-a-member-role) 并将自己从组织中移除。这样你仍可作为公司所有者保留完整的管理访问权限，而不会占用订阅席位。

### 公司所有者在关联/嵌套组织中拥有哪些权限？

公司所有者可以导航到 **Organizations** 页面，在一个位置查看所有嵌套组织。他们还可以查看或编辑组织成员，并更改单点登录（SSO）和跨域身份管理系统（SCIM）设置。公司设置的更改会影响公司下每个组织中的所有用户。

更多信息，请参阅 [角色和权限](/manuals/enterprise/security/roles-and-permissions.md)。