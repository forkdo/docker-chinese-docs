---
title: 排查配置问题
linkTitle: 排查
description: 排查 SCIM 和即时（JIT）配置中常见的用户配置问题
keywords: SCIM troubleshooting, user provisioning, JIT provisioning, group mapping, attribute conflicts
tags: [Troubleshooting]
toc_max: 2
aliases:
    - /enterprise/troubleshoot/troubleshoot-provisioning/
---

本页帮助排查常见的用户配置问题，包括使用 SCIM 和即时（JIT）配置时用户角色、属性以及意外的账户行为。

## SCIM 属性值被覆盖或忽略（SCIM attribute values are overwritten or ignored）

### 错误消息（Error message）

通常，此场景不会在 Docker 或你的 IdP 中产生错误消息。此问题通常表现为角色或团队分配不正确。

### 原因（Causes）

- 启用了 JIT 配置，Docker 使用你 IdP 的 SSO 登录流程中的值来配置用户，这会覆盖 SCIM 提供的属性。
- SCIM 是在用户已通过 JIT 配置之后才启用的，因此 SCIM 的更新不会生效。

### 受影响的环境（Affected environments）

- 使用 SCIM 配合 SSO 的 Docker 组织
- 在 SCIM 设置之前通过 JIT 配置的用户

### 复现步骤（Steps to replicate）

1. 为你的 Docker 组织启用 JIT 和 SSO。
1. 以用户身份通过 SSO 登录 Docker。
1. 启用 SCIM 并为该用户设置角色/团队属性。
1. SCIM 尝试更新用户的属性，但角色或团队的分配未反映更改。

### 解决方案（Solutions）

#### 禁用 JIT 配置（推荐）（Disable JIT provisioning (recommended)）

1. 登录 [Docker Home](https://app.docker.com/)。
1. 选择 **Identity & auth**，然后 **SSO and SCIM**。
1. 找到相关的 SSO 连接。
1. 选择 **操作菜单（actions menu）** 并选择 **Edit**。
1. 禁用 **Just-in-Time provisioning**。
1. 保存你的更改。

禁用 JIT 后，Docker 使用 SCIM 作为用户创建和角色分配的事实来源。

**保持 JIT 启用并匹配属性（Keep JIT enabled and match attributes）**

如果你倾向于保持 JIT 启用：

- 确保你的 IdP 的 SSO 属性映射与 SCIM 发送的值匹配。
- 避免配置 SCIM 覆盖已通过 JIT 设置的属性。

此选项需要在你的 IdP 配置中严格协调 SSO 和 SCIM 属性。

## SCIM 更新不适用于现有用户（SCIM updates don't apply to existing users）

### 原因（Causes）

用户账户最初是手动创建的或通过 JIT 创建的，而 SCIM 未关联以管理它们。

### 解决方案（Solution）

SCIM 只管理它配置的用户。要允许 SCIM 管理现有用户：

1. 在 [Docker Home](https://app.docker.com) 的 **Members** 下手动移除该用户。
1. 从你的 IdP 触发配置。
1. SCIM 将以正确的属性重新创建该用户。

> [!WARNING]
>
> 删除用户会移除他们的资源所有权（例如仓库）。在移除用户之前请转移所有权。
