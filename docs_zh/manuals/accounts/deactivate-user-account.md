---
title: 停用 Docker 账户
linkTitle: 停用账户
weight: 30
description: 了解如何停用 Docker 用户账户。
keywords: Docker Hub, 删除, 停用, 账户, 账户管理, 删除 Docker 账户, 关闭 Docker 账户, 禁用 Docker 账户
---

了解如何停用个人 Docker 账户，包括停用所需的先决条件。

有关停用组织的信息，
请参阅 [停用组织](../admin/organization/deactivate-account.md)。

> [!WARNING]
>
> 停用账户后，所有使用您 Docker 账户的 Docker 产品和服务都将无法访问。

## 先决条件

在停用 Docker 账户之前，请确保满足以下要求：

- 如果您是组织或公司的所有者，在停用 Docker 账户之前必须先退出组织或公司：
    1. 登录 [Docker Home](https://app.docker.com/admin) 并选择您的组织。
    1. 选择 **成员**，找到您的用户名。
    1. 选择 **操作** 菜单，然后选择 **退出组织**。
- 如果您是组织的唯一所有者，必须先将所有者角色分配给组织中的其他成员，然后将自己从组织中移除，或者停用该组织。同样，如果您是公司的唯一所有者，要么添加其他人为公司所有者然后将自己移除，要么停用该公司。
- 如果您有活跃的 Docker 订阅，请[降级为 Docker 个人订阅](../subscription/change.md)。
- 下载并保存您想要保留的所有镜像和标签。使用 `docker pull -a <image>:<tag>`。
- 取消关联您的 [GitHub 账户](../docker-hub/repos/manage/builds/link-source.md#unlink-a-github-user-account)。

## 停用账户

完成以上所有步骤后，即可停用您的账户。

> [!WARNING]
>
> 停用账户是永久性的，无法撤销。请务必备份任何重要数据。

1. 登录 [Docker Home](https://app.docker.com/login)。
1. 选择您的头像以打开下拉菜单。
1. 选择 **账户设置**。
1. 选择 **停用**。
1. 选择 **停用账户**，然后再次确认。

## 删除个人数据

停用账户不会删除您的个人数据。要请求删除个人数据，请填写 Docker 的
[隐私请求表单](https://preferences.docker.com/)。