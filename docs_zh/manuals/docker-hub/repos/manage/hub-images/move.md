---
description: 了解如何在仓库之间移动镜像。
keywords: Docker Hub, Hub, repository content, move
title: 在仓库之间移动镜像
linkTitle: 移动镜像
weight: 40
---

整合和组织不同仓库中的 Docker 镜像可以简化您的工作流程，无论您是在管理个人项目还是为组织做贡献。本主题介绍如何在 Docker Hub 仓库之间移动镜像，确保您的内容在正确的账户或命名空间下保持可访问性和组织性。

> [!NOTE]
>
> 对于批量迁移、多架构镜像或脚本化工作流，请参阅 [批量迁移 Docker 镜像](/manuals/docker-hub/repos/manage/hub-images/bulk-migrate.md)。

## 个人到个人

在整合个人仓库时，您可以从初始仓库拉取私有镜像，并将其推送到您拥有的另一个仓库。为避免丢失私有镜像，请执行以下步骤：

1. 使用个人订阅[注册](https://app.docker.com/signup)一个新的 Docker 账户。
2. 使用您的原始 Docker 账户登录 [Docker](https://app.docker.com/login)。
3. 拉取您的镜像：

   ```console
   $ docker pull namespace1/docker101tutorial
   ```

4. 使用您新创建的 Docker 用户名标记您的私有镜像，例如：

   ```console
   $ docker tag namespace1/docker101tutorial new_namespace/docker101tutorial
   ```

5. 使用 CLI 中的 `docker login`，用您新创建的 Docker 账户登录，并将新标记的私有镜像推送到您的新 Docker 账户命名空间：

   ```console
   $ docker push new_namespace/docker101tutorial
   ```

之前账户中的私有镜像现在可以在您的新账户中使用。

## 个人到组织

为避免丢失私有镜像，您可以从个人账户拉取私有镜像，并将其推送到您拥有的组织。

1. 导航到 [Docker Hub](https://hub.docker.com) 并选择 **My Hub**。
2. 选择适用的组织，并确认您的用户账户是该组织的成员。
3. 使用您的原始 Docker 账户登录 [Docker Hub](https://hub.docker.com)，并拉取您的镜像：

   ```console
   $ docker pull namespace1/docker101tutorial
   ```

4. 使用您的新组织命名空间标记您的镜像：

   ```console
   $ docker tag namespace1/docker101tutorial <new_org>/docker101tutorial
   ```

5. 将新标记的镜像推送到您的新组织命名空间：

   ```console
   $ docker push new_org/docker101tutorial
   ```

之前用户账户中的私有镜像现在可以在您的组织中使用。