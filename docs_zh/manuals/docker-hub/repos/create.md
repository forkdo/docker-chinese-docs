---
description: 了解如何在 Docker Hub 上创建仓库
keywords: Docker Hub, Hub, 仓库, 创建
title: 创建仓库
linkTitle: 创建
toc_max: 3
weight: 20
---

1. 登录到 [Docker Hub](https://hub.docker.com)。
2. 选择 **My Hub** > **Repositories**。
3. 在右上角附近，选择 **Create repository**。
4. 选择一个 **Namespace**。

   您可以选择将其放在自己的用户账户下，或放在任何您是所有者或编辑者的组织下。

5. 指定 **Repository Name**。

   仓库名称需要满足以下条件：
    - 唯一
    - 长度在 2 到 255 个字符之间
    - 仅包含小写字母、数字、连字符（`-`）和下划线（`_`）

   > [!NOTE]
   >
   > Docker Hub 仓库一旦创建后无法重命名。

6. 指定 **Short description**。

   描述最多可包含 100 个字符，它会显示在搜索结果中。

7. 选择默认的可见性。

   - **Public**：仓库会出现在 Docker Hub 搜索结果中，所有人都可以拉取。
   - **Private**：仓库不会出现在 Docker Hub 搜索结果中，仅对您和协作者可见。此外，如果您选择了组织的命名空间，则具有相应角色或许可的用户也可以访问该仓库。更多详细信息，请参阅 [角色和权限](/manuals/enterprise/security/roles-and-permissions.md)。

   > [!NOTE]
   >
   > 对于创建新仓库的组织，如果您不确定选择哪种可见性，Docker 建议您选择 **Private**。

8. 选择 **Create**。

仓库创建后，将显示 **General** 页面。现在您可以管理：

- [仓库信息](./manage/information.md)
- [访问权限](./manage/access.md)
- [镜像](./manage/hub-images/_index.md)
- [自动构建](./manage/builds/_index.md)
- [Webhook](./manage/webhooks.md)
- [镜像安全洞察](./manage/vulnerability-scanning.md)