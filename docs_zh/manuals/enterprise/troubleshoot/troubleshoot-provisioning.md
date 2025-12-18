---
title: 排查配置问题
linkTitle: 排查配置问题
description: 排查 SCIM 和即时（JIT）配置中的常见用户配置问题
keywords: SCIM 排查、用户配置、JIT 配置、组映射、属性冲突
tags: [Troubleshooting]
toc_max: 2
aliases:
 - /security/troubleshoot/troubleshoot-provisioning/
---

本页面帮助您排查常见的用户配置问题，包括 SCIM 和即时（JIT）配置中的用户角色、属性和意外账户行为。

## SCIM 属性值被覆盖或忽略

### 错误消息

通常，此场景不会在 Docker 或您的 IdP 中产生错误消息。此问题通常表现为角色或团队分配不正确。

### 原因

- 已启用 JIT 配置，Docker 正在使用来自 IdP 的 SSO 登录流的值来配置用户，这会覆盖 SCIM 提供的属性。
- 在用户已通过 JIT 配置后才启用 SCIM，因此 SCIM 更新不会生效。

### 受影响的环境

- 使用 SSO 配置 SCIM 的 Docker 组织
- 在配置 SCIM 之前已通过 JIT 配置的用户

### 复现步骤

1. 为您的 Docker 组织启用 JIT 和 SSO。
1. 用户通过 SSO 登录 Docker。
1. 为该用户启用 SCIM 并设置角色/团队属性。
1. SCIM 尝试更新用户属性，但角色或团队分配未反映更改。

### 解决方案

#### 禁用 JIT 配置（推荐）

1. 登录到 [Docker Home](https://app.docker.com/)。
1. 选择 **Admin Console**，然后选择 **SSO and SCIM**。
1. 找到相关的 SSO 连接。
1. 选择 **actions menu** 并选择 **Edit**。
1. 禁用 **Just-in-Time provisioning**。
1. 保存您的更改。

禁用 JIT 后，Docker 将使用 SCIM 作为用户创建和角色分配的唯一真实来源。

**保持启用 JIT 并匹配属性**

如果您希望保持启用 JIT：

- 确保您的 IdP 的 SSO 属性映射与 SCIM 发送的值匹配。
- 避免配置 SCIM 覆盖通过 JIT 设置的属性。

此选项需要在您的 IdP 配置中严格协调 SSO 和 SCIM 属性。

## SCIM 更新未应用于现有用户

### 原因

用户账户最初是手动创建或通过 JIT 创建的，而 SCIM 未关联以管理它们。

### 解决方案

SCIM 仅管理其配置的用户。要允许 SCIM 管理现有用户：

1. 从 Docker [Admin Console](https://app.docker.com/admin) 中手动删除该用户。
1. 从您的 IdP 触发配置。
1. SCIM 将使用正确的属性重新创建该用户。

> [!WARNING]
>
> 删除用户会移除其资源所有权（例如，仓库）。在删除用户之前请先转移所有权。