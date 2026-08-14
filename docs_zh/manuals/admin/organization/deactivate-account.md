---
title: 停用组织
linkTitle: 停用
description: 了解如何停用 Docker 组织以及所需的先决条件步骤。
keywords: deactivate organization, delete organization, organization
  management, Docker Home, cancel subscription, unlink GitHub, remove SSO
weight: 50
aliases:
  - /docker-hub/deactivate-account/
---

{{< summary-bar feature_name="General admin" >}}

了解如何停用 Docker 组织，包括所需的先决条件步骤。有关停用用户账户的信息，请参阅
[停用 Docker 账户](/manuals/accounts/deactivate-user-account.md)。

> [!WARNING]
>
> 停用组织后，所有使用该组织的 Docker 产品和服务都将无法访问。你的个人 Docker 账户
> 仍保持活跃。

## 先决条件

在停用组织之前，你必须完成以下所有步骤：

- 下载你想保留的任何镜像和标签。使用 `docker pull -a <image>`
  拉取所有标签，或使用 `docker pull <image>:<tag>` 拉取特定标签。
- 如果你有活跃的 Docker 订阅，[请将其降级为基础组织
  账户](/manuals/subscription/plans/docker.md#cancel-a-docker-plan)。
- 移除组织内的所有其他成员。
- 解除你的 [GitHub 和 Bitbucket
  账户](/manuals/docker-hub/repos/manage/builds/link-source.md#unlink-a-github-user-account) 的关联。
- 对于 Business 组织，[移除你的 SSO
  连接](/manuals/enterprise/security/single-sign-on/manage.md#delete-a-connection)。

## 停用

> [!WARNING]
>
> 停用组织是永久性的，无法撤销。请确保在停用之前已收集所需的所有数据。

1. 登录 [Docker Home](https://app.docker.com) 并选择要停用的组织。
1. 选择 **Organization settings**（组织设置），然后选择 **Deactivate**（停用）。如果 **Deactivate**（停用）
   按钮不可用，请确认你已完成所有 [先决条件](#先决条件)。
1. 输入组织名称以确认停用。
1. 选择 **Deactivate organization**（停用组织）。
