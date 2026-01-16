---
title: 镜像管理
url: /docker-hub/repos/manage/hub-images/
parent:
  title: 仓库
  url: /docker-hub/repos/
breadcrumbs:
  - title: 手册
    url: /manuals/
  - title: Docker Hub
    url: /docker-hub/
  - title: 仓库
    url: /docker-hub/repos/
  - title: 镜像管理
    url: /docker-hub/repos/manage/hub-images/
children:
  - title: Docker Hub 上的标签
    url: /docker-hub/repos/manage/hub-images/tags/
    description: 了解如何在 Docker Hub 上管理仓库标签。
  - title: Docker Hub 上的不可变标签
    url: /docker-hub/repos/manage/hub-images/immutable-tags/
    description: 了解不可变标签以及它们如何帮助维护 Docker Hub 上的镜像版本一致性。
  - title: 镜像管理
    url: /docker-hub/repos/manage/hub-images/manage/
    description: 了解如何删除镜像标签。
  - title: Docker Hub 上的软件制品
    url: /docker-hub/repos/manage/hub-images/oci-artifacts/
    description: 您可以使用 Docker Hub 存储打包为 OCI 制品的软件制品。
  - title: 将镜像推送到仓库
    url: /docker-hub/repos/manage/hub-images/push/
    description: 了解如何向 Docker Hub 上的仓库添加内容。
  - title: 在仓库之间移动镜像
    url: /docker-hub/repos/manage/hub-images/move/
    description: 了解如何在仓库之间移动镜像。
  - title: 批量迁移镜像
    url: /docker-hub/repos/manage/hub-images/bulk-migrate/
    description: 学习如何使用脚本和自动化在组织之间迁移多个 Docker 镜像和标签。
---


Docker Hub 提供了强大的功能来管理和组织您的仓库内容，确保您的镜像和制品可访问、版本可控且易于共享。本节涵盖关键的镜像管理任务，包括标记、推送镜像、在仓库之间传输镜像以及支持的软件制品。

- [标签](./tags.md)：标签帮助您在单个仓库内对镜像的不同版本进行版本控制和组织。本主题解释了标记，并提供在 Docker Hub 中创建、查看和删除标签的指导。
- [镜像管理](./manage.md)：管理您的镜像和镜像索引，以优化仓库存储。
- [软件制品](./oci-artifacts.md)：Docker Hub 支持 OCI（开放容器倡议）制品，允许您存储、管理和分发超出标准 Docker 镜像范围的各种内容，包括 Helm 图表、漏洞报告等。本节提供 OCI 制品的概述，以及将它们推送到 Docker Hub 的一些示例。
- [将镜像推送到 Hub](./push.md)：Docker Hub 使您能够将本地镜像推送到它，使其对您的团队或 Docker 社区可用。了解如何配置您的镜像并使用 `docker push` 命令将它们上传到 Docker Hub。
- [在仓库之间移动镜像](./move.md)：在不同仓库之间组织内容可以帮助简化协作和资源管理。本主题详细说明如何将镜像从一个 Docker Hub 仓库移动到另一个，无论是用于个人整合还是与组织共享镜像。
