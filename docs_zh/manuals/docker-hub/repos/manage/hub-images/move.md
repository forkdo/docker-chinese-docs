---
description: 了解如何在仓库之间移动镜像。
keywords: Docker Hub, Hub, 仓库内容, 移动
title: 在仓库之间移动镜像
linkTitle: 移动镜像
weight: 40
---

在 Docker Hub 上整理和组织 Docker 镜像到不同仓库中，可以简化你的工作流程，无论你是在管理个人项目还是为组织贡献代码。本文档说明了如何在 Docker Hub 仓库之间移动镜像，确保你的内容在正确的账户或命名空间下保持可访问和有条理。

> [!NOTE]
>
> 对于批量迁移、多架构镜像或脚本化工作流，请参阅 [批量迁移 Docker 镜像](/manuals/docker-hub/repos/manage/hub-images/bulk-migrate.md)。

## 个人到个人

当你整合个人仓库时，可以从初始仓库中拉取私有镜像，然后推送到你拥有的另一个仓库。为避免丢失私有镜像，请执行以下步骤：

1. 使用个人订阅 [注册](https://app.docker.com/signup) 一个新的 Docker 账户。
2. 使用你的原始 Docker 账户登录 [Docker](https://app.docker.com/login)。
3. 拉取你的镜像：

   ```console
   $ docker pull namespace1/docker101tutorial
   ```

4. 使用你的新 Docker 用户名标记你的私有镜像，例如：

   ```console
   $ docker tag namespace1/docker101tutorial new_namespace/docker101tutorial
   ```

5. 使用 CLI 中的 `docker login` 登录到你的新 Docker 账户，并将新标记的私有镜像推送到你的新 Docker 账户命名空间：

   ```console
   $ docker push new_namespace/docker101tutorial
   ```

之前存在于你旧账户中的私有镜像现在在你的新账户中可用。

## 个人到组织

为避免丢失私有镜像，你可以从你的个人账户中拉取私有镜像，并推送到你拥有的组织中。

1. 导航到 [Docker Hub](https://hub.docker.com) 并选择 **My Hub**。
2. 选择适用的组织，并确认你的用户账户是该组织的成员。
3. 使用你的原始 Docker 账户登录 [Docker Hub](https://hub.docker.com)，并拉取你的镜像：

   ```console
   $ docker pull namespace1/docker101tutorial
   ```

4. 使用你的新组织命名空间标记你的镜像：

   ```console
   $ docker tag namespace1/docker101tutorial <new_org>/docker101tutorial
   ```

5. 将新标记的镜像推送到你的新组织命名空间：

   ```console
   $ docker push new_org/docker101tutorial
   ```

之前存在于你用户账户中的私有镜像现在在你的组织中可用。