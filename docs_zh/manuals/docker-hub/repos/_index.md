---
description: 了解如何在 Docker Hub 上管理仓库
keywords: Docker Hub, Hub, repositories
title: 仓库
weight: 20
aliases:
- /engine/tutorials/dockerrepos/
- /docker-hub/repos/configure/
---

Docker Hub 仓库是容器镜像的集合，使您能够公开或私下存储、管理和共享 Docker 镜像。每个仓库都作为一个专用空间，用于存储与特定应用程序、微服务或项目相关的镜像。仓库中的内容通过标签进行组织，这些标签代表同一应用程序的不同版本，允许用户在需要时拉取正确的版本。

在本节中，了解如何：

- [创建](./create.md) 仓库。
- 管理仓库，包括如何管理：

   - [仓库信息](./manage/information.md)：添加描述、概述和分类，以帮助用户了解仓库的用途和用法。清晰的仓库信息有助于提高可发现性和可用性。

   - [访问权限](./manage/access.md)：使用灵活的选项控制谁可以访问您的仓库。将仓库设为公开或私有，添加协作者，对于组织而言，可以管理角色和团队以维护安全和控制。

   - [镜像](./manage/hub-images/_index.md)：仓库支持多种内容类型，包括 OCI 工件，并允许通过标记进行版本控制。推送新镜像并跨仓库管理现有内容以实现灵活性。

   - [镜像安全洞察](./manage/vulnerability-scanning.md)：利用持续的 Docker Scout 分析和静态漏洞扫描来检测、了解和解决容器镜像中的安全问题。

   - [Webhook](./manage/webhooks.md)：通过设置 Webhook 来自动响应仓库事件（如镜像推送或更新），Webhook 可以在外部系统中触发通知或操作，从而简化工作流程。

   - [自动构建](./manage/builds/_index.md)：与 GitHub 或 Bitbucket 集成以进行自动构建。每次代码更改都会触发镜像重建，支持持续集成和交付。

   - [可信内容](./manage/trusted-content/_index.md)：为 Docker 官方镜像做出贡献，或管理已验证发布者 (Verified Publisher) 和赞助开源 (Sponsored Open Source) 计划中的仓库，包括设置徽标、访问分析和启用漏洞扫描等任务。

- [归档](./archive.md) 过时或不受支持的仓库。
- [删除](./delete.md) 仓库。
- [管理个人设置](./settings.md)：对于您的帐户，您可以为仓库设置个人偏好，包括默认仓库隐私和自动构建通知。