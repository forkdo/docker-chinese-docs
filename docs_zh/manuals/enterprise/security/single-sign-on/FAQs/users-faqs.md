---
title: SSO 用户管理常见问题
linkTitle: 用户管理
description: 关于使用 Docker 单点登录管理用户的常见问题
keywords: SSO 用户管理, 用户配置, SCIM, 即时配置, 组织成员
tags: [FAQ]
aliases:
- /single-sign-on/users-faqs/
- /faq/security/single-sign-on/users-faqs/
- /security/faqs/single-sign-on/users-faqs/
---

## 我是否需要手动将用户添加到组织中？

不需要，您无需手动将用户添加到组织中。只需确保用户账户在您的 IdP 中存在即可。当用户使用其域名邮箱地址登录 Docker 时，经过成功认证后，他们会被自动添加到组织中。

## 用户是否可以使用不同的邮箱地址通过 SSO 认证？

所有用户必须使用 SSO 设置期间指定的邮箱域名进行认证。如果 SSO 未被强制启用，且用户已被邀请，则邮箱地址不匹配验证域名的用户可以使用用户名和密码作为访客登录，但仅限于此情况。

## 用户如何知道自己被添加到了 Docker 组织？

启用 SSO 后，用户下次登录 Docker Hub 或 Docker Desktop 时，系统会提示他们通过 SSO 进行认证。系统会检测其域名邮箱，并提示他们改用 SSO 凭据登录。

对于 CLI 访问，用户必须使用个人访问令牌进行认证。

## 我可以将现有用户从非 SSO 账户转换为 SSO 账户吗？

可以，您可以将现有用户转换为 SSO 账户。请确保用户具备以下条件：

- 拥有公司域名邮箱地址和在您的 IdP 中的账户
- Docker Desktop 版本为 4.4.2 或更高版本
- 已创建个人访问令牌以替代 CLI 访问的密码
- CI/CD 流水线已更新为使用 PAT 而非密码

详细说明，请参阅 [配置单点登录](/manuals/enterprise/security/single-sign-on/configure.md)。

## Docker SSO 是否与 IdP 完全同步？

Docker SSO 默认提供即时（JIT）配置。用户在通过 SSO 认证时会被配置。如果用户离开组织，管理员必须手动 [移除用户](/manuals/admin/organization/members.md#remove-a-member-or-invitee)。

[SCIM](/manuals/enterprise/security/provisioning/scim.md) 提供用户和组的完全同步。使用 SCIM 时，建议在管理控制台中关闭 JIT，以便所有自动配置均由 SCIM 处理。

此外，您也可以使用 [Docker Hub API](/reference/api/hub/latest/) 完成此流程。

## 关闭即时配置对用户登录有何影响？

关闭 JIT 后（在管理控制台中使用 SCIM 时可用），用户必须是组织成员或拥有待处理的邀请才能访问 Docker。不满足这些条件的用户会收到“访问被拒绝”错误，需要管理员发送邀请。

参见 [JIT 配置关闭时的 SSO 认证](/manuals/enterprise/security/provisioning/just-in-time.md#sso-authentication-with-jit-provisioning-disabled)。

## 没有邀请，用户能否加入组织？

在启用 SSO 的情况下不能。加入组织需要组织所有者的邀请。当 SSO 被强制启用时，拥有已验证域名邮箱的用户在登录时可以自动加入组织。

## 启用 SCIM 后，现有授权用户会发生什么？

启用 SCIM 不会立即移除或修改现有授权用户。他们保留当前的访问权限和角色，但启用 SCIM 后，您将通过 IdP 管理他们。如果之后关闭 SCIM，之前由 SCIM 管理的用户仍保留在 Docker 中，但不再根据您的 IdP 自动更新。

## Docker Hub 中是否可见用户信息？

所有 Docker 账户都有与其命名空间关联的公开资料。如果您不希望用户信息（如全名）可见，请从您的 SSO 和 SCIM 映射中移除这些属性，或使用其他标识符替代用户的全名。