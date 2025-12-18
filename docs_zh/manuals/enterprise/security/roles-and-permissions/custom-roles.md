---
title: 自定义角色
description: 为您的组织创建量身定制的权限集，使用自定义角色
keywords: 自定义角色, 权限, 访问控制, 组织管理, docker hub, 管理控制台, 安全
---

{{< summary-bar feature_name="通用管理员" >}}

自定义角色允许您为组织创建量身定制的权限集。本文档涵盖自定义角色的创建和管理步骤。

## 什么是自定义角色？

自定义角色允许您为组织创建量身定制的权限集。您可以将自定义角色分配给单个用户或团队。
用户和团队只能获得核心角色或自定义角色之一，不能同时拥有两者。

当 Docker 的核心角色不符合您的需求时，可以使用自定义角色。

## 前置条件

要配置自定义角色，您需要在 Docker 组织中拥有所有者权限。

## 创建自定义角色

在可以将自定义角色分配给用户之前，您必须先在管理控制台中创建一个：

1. 登录到 [Docker Home](https://app.docker.com)。
2. 选择 **Admin Console**（管理控制台）。
3. 在 **User management**（用户管理）下，选择 **Roles**（角色）> **Create role**（创建角色）。
4. 创建名称并描述该角色的用途：
   - 提供一个 **Label**（标签）
   - 输入唯一的 **Name**（名称）标识符（创建后无法更改）
   - 添加可选的 **Description**（描述）
5. 通过展开权限类别并选择权限复选框来设置角色权限。有关可用权限的完整列表，请参阅 [自定义角色权限参考](#自定义角色权限参考)。
6. 选择 **Review**（审核）以查看自定义角色配置并查看所选权限的摘要。
7. 选择 **Create**（创建）。

创建自定义角色后，您现在可以 [将自定义角色分配给用户](#分配自定义角色)。

## 编辑自定义角色

1. 登录到 [Docker Home](https://app.docker.com)。
2. 选择 **Admin Console**（管理控制台）。
3. 在 **User management**（用户管理）下，选择 **Roles**（角色）。
4. 从列表中找到您的自定义角色，然后选择 **Actions menu**（操作菜单）。
5. 选择 **Edit**（编辑）。
6. 您可以编辑以下自定义角色设置：
   - Label（标签）
   - Description（描述）
   - Permissions（权限）
7. 编辑完成后，选择 **Save**（保存）。

## 分配自定义角色

{{< tabs >}}
{{< tab name="单个用户" >}}

1. 登录到 [Docker Home](https://app.docker.com)。
2. 选择 **Members**（成员）。
3. 找到您要分配自定义角色的成员，然后选择 **Actions menu**（操作菜单）。
4. 在下拉菜单中选择 **Change role**（更改角色）。
5. 在 **Select a role**（选择角色）下拉菜单中，选择您的自定义角色。
6. 选择 **Save**（保存）。

{{< /tab >}}
{{< tab name="批量用户" >}}

1. 登录到 [Docker Home](https://app.docker.com)。
2. 选择 **Members**（成员）。
3. 使用用户名列中的复选框选择所有要分配自定义角色的用户。
4. 选择 **Change role**（更改角色）。
5. 在 **Select a role**（选择角色）下拉菜单中，选择您的自定义角色或核心角色。
6. 选择 **Save**（保存）。

{{< /tab >}}
{{< tab name="团队" >}}

1. 登录到 [Docker Home](https://app.docker.com)。
2. 选择 **Teams**（团队）。
3. 找到您要分配自定义角色的团队，然后选择 **Actions menu**（操作菜单）。
4. 选择 **Assign role**（分配角色）。
5. 选择您的自定义角色，然后选择 **Assign**（分配）。

角色列将更新为新分配的角色。

{{< /tab >}}
{{< /tabs >}}

## 查看角色分配

要查看哪些用户和团队被分配到角色：

1. 登录到 [Docker Home](https://app.docker.com)。
2. 选择 **Admin Console**（管理控制台）。
3. 在 **User management**（用户管理）下，选择 **Roles**（角色）。
4. 在角色列表中，查看 **Users**（用户）和 **Teams**（团队）列以查看分配数量。
5. 选择特定角色以查看其权限和分配的详细信息。

## 重新分配自定义角色

{{< tabs >}}
{{< tab name="单个用户" >}}

1. 登录到 [Docker Home](https://app.docker.com)。
2. 选择 **Members**（成员）。
3. 找到您要重新分配的成员，然后选择 **Actions menu**（操作菜单）。
4. 选择 **Change role**（更改角色）。
5. 在 **Select a role**（选择角色）下拉菜单中，选择新角色。
6. 选择 **Save**（保存）。

{{< /tab >}}
{{< tab name="批量用户" >}}

1. 登录到 [Docker Home](https://app.docker.com)。
2. 选择 **Members**（成员）。
3. 使用用户名列中的复选框选择所有要重新分配的用户。
4. 选择 **Change role**（更改角色）。
5. 在 **Select a role**（选择角色）下拉菜单中，选择新角色。
6. 选择 **Save**（保存）。

{{< /tab >}}
{{< tab name="团队" >}}

1. 登录到 [Docker Home](https://app.docker.com)。
2. 选择 **Teams**（团队）。
3. 找到团队，然后选择 **Actions menu**（操作菜单）。
4. 选择 **Change role**（更改角色）。
5. 在弹出窗口中，从下拉菜单中选择角色，然后选择 **Save**（保存）。

{{< /tab >}}
{{< /tabs >}}

## 删除自定义角色

在删除自定义角色之前，您必须先将所有用户和团队重新分配到其他角色。

1. 登录到 [Docker Home](https://app.docker.com)。
2. 选择 **Admin Console**（管理控制台）。
3. 在 **User management**（用户管理）下，选择 **Roles**（角色）。
4. 从列表中找到您的自定义角色，然后选择 **Actions menu**（操作菜单）。
5. 如果角色已分配给用户或团队：
   - 导航到 **Members**（成员）页面，并更改分配给此自定义角色的所有用户的角色
   - 导航到 **Teams**（团队）页面，并重新分配拥有此自定义角色的所有团队
6. 一旦没有用户或团队被分配，返回到 **Roles**（角色）。
7. 找到您的自定义角色并选择 **Actions menu**（操作菜单）。
8. 选择 **Delete**（删除）。
9. 在确认窗口中，选择 **Delete**（删除）以确认。

## 自定义角色权限参考

自定义角色通过在不同类别中选择特定权限来构建。下表列出了您可以分配给自定义角色的所有可用权限。

### 组织管理

| 权限                        | 描述                                                                                     |
| :-------------------------- | :---------------------------------------------------------------------------------------------- |
| View teams                  | 查看团队和团队成员                                                                     |
| Manage teams                | 创建、更新和删除团队及团队成员                                               |
| Manage registry access      | 控制成员可以访问哪些注册表                                                     |
| Manage image access         | 设置成员可以拉取和使用的镜像策略                                          |
| Update organization information | 更新组织信息，如名称和位置                                       |
| Member management           | 管理组织成员、邀请和角色                                                 |
| View custom roles           | 查看现有自定义角色及其权限                                                |
| Manage custom roles         | 完全访问自定义角色管理和分配                                            |
| Manage organization access tokens | 创建、更新和删除此组织中的仓库。不包括推送/拉取或注册表操作 |
| View activity logs          | 访问组织审计日志和活动历史                                             |
| View domains                | 查看域和域审计设置                                                          |
| Manage domains              | 管理已验证的域和域审计设置                                               |
| View SSO and SCIM           | 查看单点登录和用户配置设置                                        |
| Manage SSO and SCIM         | 完全访问 SSO 和 SCIM 管理                                                          |
| Manage Desktop settings     | 配置 Docker Desktop 设置策略并查看使用情况报告                               |

### Docker Hub

| 权限          | 描述                                                |
| :------------ | :-------------------------------------------------- |
| View repositories | 查看仓库详细信息和内容                       |
| Manage repositories | 创建、更新和删除仓库及其内容 |

### 账单

| 权限     | 描述                                      |
| :------- | :---------------------------------------- |
| View billing | 查看组织账单信息            |
| Manage billing | 完全访问管理组织账单 |