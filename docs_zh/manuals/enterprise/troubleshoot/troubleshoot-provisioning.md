---
title: 排查配置问题
linkTitle: 排查配置问题
description: 排查使用 SCIM 和即时 (JIT) 配置时常见的用户配置问题
toc_max: 2
tags:
- Troubleshooting
keywords: SCIM troubleshooting, user provisioning, JIT provisioning, group mapping, attribute conflicts
aliases:
- /security/troubleshoot/troubleshoot-provisioning/
---

本文档帮助排查使用 SCIM 和即时 (JIT) 配置时常见的用户配置问题，包括用户角色、属性以及意外的账户行为。

## SCIM 属性值被覆盖或忽略

### 错误消息

通常情况下，Docker 或您的身份提供商 (IdP) 中不会出现错误消息。此问题通常表现为角色或团队分配不正确。

### 原因

- 已启用 JIT 配置，Docker 正在使用来自 IdP 的 SSO 登录流程中的值来配置用户，这会覆盖 SCIM 提供的属性。
- 在用户已通过 JIT 配置后启用了 SCIM，因此 SCIM 更新不会生效。

### 受影响的环境

- 使用 SCIM 和 SSO 的 Docker 组织
- 在 SCIM 设置之前通过 JIT 配置的用户

### 复现步骤

1. 为您的 Docker 组织启用 JIT 和 SSO。
2. 通过 SSO 以用户身份登录 Docker。
3. 启用 SCIM 并为该用户设置角色/团队属性。
4. SCIM 尝试更新用户的属性，但角色或团队分配未反映更改。

### 解决方案

#### 禁用 JIT 配置（推荐）

1. 登录 [Docker Home](https://app.docker.com/)。
2. 选择 **Admin Console**，然后选择 **SSO and SCIM**。
3. 找到相关的 SSO 连接。
4. 选择 **操作菜单**，然后选择 **编辑**。
5. 禁用 **即时 (JIT) 配置**。
6. 保存更改。

禁用 JIT 后，Docker 将使用 SCIM 作为用户创建和角色分配的权威来源。

**保持 JIT 启用并匹配属性**

如果您希望保持 JIT 启用：

- 确保 IdP 的 SSO 属性映射与 SCIM 发送的值匹配。
- 避免配置 SCIM 覆盖已通过 JIT 设置的属性。

此选项需要在 IdP 配置中严格协调 SSO 和 SCIM 属性。

## SCIM 更新不适用于现有用户

### 原因

用户账户最初是手动创建或通过 JIT 创建的，SCIM 未链接以管理这些用户。

### 解决方案

SCIM 仅管理由其配置的用户。要允许 SCIM 管理现有用户：

1. 从 Docker [Admin Console](https://app.docker.com/admin) 手动删除用户。
2. 从 IdP 触发配置。
3. SCIM 将使用正确的属性重新创建用户。

> [!WARNING]
>
> 删除用户会移除其资源所有权（例如仓库）。在删除用户之前，请转移所有权。