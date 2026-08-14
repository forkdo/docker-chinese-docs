---
title: 命名空间访问控制
linkTitle: 命名空间访问
description: 控制组织成员是否可以向其在 Docker Hub 上的个人命名空间推送内容
keywords: namespace access, docker hub, personal namespace, organization security, docker business
tags: [admin]
weight: 60
---

{{< summary-bar feature_name="Namespace access" >}}

命名空间访问控制让组织管理员能够控制组织内所有成员是否可以向其在 Docker Hub 上的个人命名空间推送内容。这可防止组织意外地将镜像发布到已批准的、受管控位置之外。

启用命名空间访问控制后，组织成员仍可以查看和拉取来自其个人命名空间的镜像，并继续访问所有现有的仓库和内容。但是，他们无法创建新的仓库或向个人命名空间推送新的镜像。

> [!IMPORTANT]
>
> 对于属于多个组织的用户，如果在任一组织中启用了命名空间访问控制，该用户就无法向其个人命名空间推送内容，也无法在个人命名空间中创建新的仓库。

### 配置命名空间访问控制

要配置命名空间访问控制：

1. 登录 [Docker Home](https://app.docker.com/)，从左上角账户下拉菜单中选择您的组织。
2. 选择 **Docker Desktop**，然后 **Namespace access**。
3. 使用开关启用或禁用命名空间访问控制。
4. 选择 **Save changes**。

启用命名空间访问控制后，组织成员仍可以查看其个人命名空间和现有仓库，但无法创建任何新仓库或向现有仓库推送任何新镜像。

### 验证访问限制

配置命名空间访问控制后，测试限制是否正常工作。

在尝试向个人命名空间中的现有仓库推送后，您会看到类似以下的错误消息：

```console
$ docker push <personal-namespace>/<image>:<tag>
Unavailable
authentication required - namespace access restriction from an organization you belong to prevents pushing new content in your personal namespace. Restriction applied by: <organizations>. Please contact your organization administrator
```
