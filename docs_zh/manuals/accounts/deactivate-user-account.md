---
title: 停用 Docker 账户
linkTitle: 停用账户
weight: 30
description: 了解如何停用 Docker 用户账户。
keywords: Docker Hub, 删除, 停用, 账户, 账户管理, 删除 Docker 账户, 关闭 Docker 账户, 禁用 Docker 账户
---

了解如何停用个人 Docker 账户，包括停用账户所需的前提条件。

有关停用组织的信息，请参阅[停用组织](../admin/organization/deactivate-account.md)。

> [!WARNING]
>
> 停用账户后，您将无法访问所有使用 Docker 账户的 Docker 产品和服务。

## 前提条件

在停用 Docker 账户之前，请确保满足以下要求：

- 如果您是组织或公司的所有者，必须在停用 Docker 账户之前离开该组织或公司：
    1. 登录 [Docker Home](https://app.docker.com/admin) 并选择您的组织。
    1. 选择 **成员** 并找到您的用户名。
    1. 选择 **操作** 菜单，然后选择 **离开组织**。
- 如果您是组织的唯一所有者，必须将所有者角色分配给组织中的其他成员，然后将自己从组织中移除，或停用该组织。同样，如果您是公司的唯一所有者，可以添加其他人为公司所有者，然后将自己移除，或停用该公司。
- 如果您有活跃的 Docker 订阅，请[将其降级为 Docker Personal 订阅](../subscription/change.md)。
- 下载您要保留的所有镜像和标签。使用 `docker pull -a <image>:<tag>`。
- 解除您的 [GitHub 和账户](../docker-hub/repos/manage/builds/link-source.md#unlink-a-github-user-account) 的关联。

## 停用

完成上述所有步骤后，您可以停用您的账户。

> [!WARNING]
>
> 停用账户是永久性的，无法撤销。请务必备份所有重要数据。

1. 登录 [Docker Home](https://app.docker.com/login)。
1. 选择您的头像以打开下拉菜单。
1. 选择 **账户设置**。
1. 选择 **停用**。
1. 选择 **停用账户**，然后再次选择以确认。

## 删除个人数据

停用账户不会删除您的个人数据。如需申请删除个人数据，请填写 Docker 的[隐私请求表单](https://preferences.docker.com/)。