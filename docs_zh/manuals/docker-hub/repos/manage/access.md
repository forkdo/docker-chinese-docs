---
description: 了解如何管理对 Docker Hub 上仓库的访问权限。
keywords: Docker Hub, Hub, repository access, repository collaborators, repository privacy
title: 访问管理
LinkTItle: 访问
weight: 50
aliases:
- /docker-hub/repos/access/
---

在本主题中，了解可用于管理对仓库访问的功能。包括可见性、协作者、角色、团队和组织访问令牌。

## 仓库可见性

最基本的仓库访问控制是通过可见性实现的。仓库的可见性可以是公共的或私有的。

设置为公共可见性时，仓库会出现在 Docker Hub 的搜索结果中，并且任何人都可以拉取。要管理对公共个人仓库的推送访问权限，可以使用协作者。要管理对公共组织仓库的推送访问权限，可以使用角色、团队或组织访问令牌。

设置为私有可见性时，仓库不会出现在 Docker Hub 的搜索结果中，仅对获得授权的人员可访问。要管理对私有个人仓库的推送和拉取访问权限，可以使用协作者。要管理对私有组织仓库的推送和拉取访问权限，可以使用角色、团队或组织访问令牌。

### 更改仓库可见性

在 Docker Hub 中创建仓库时，可以设置仓库的可见性。此外，还可以在个人仓库设置中设置创建仓库时的默认可见性。以下描述了如何在仓库创建后更改其可见性。

要更改仓库可见性：

1. 登录 [Docker Hub](https://hub.docker.com)。
2. 选择 **我的 Hub** > **仓库**。
3. 选择一个仓库。

   将显示该仓库的 **常规** 页面。

4. 选择 **设置** 选项卡。
5. 在 **可见性设置** 下，选择以下选项之一：

   - **设为公共**：仓库将出现在 Docker Hub 的搜索结果中，并且任何人都可以拉取。
   - **设为私有**：仓库不会出现在 Docker Hub 的搜索结果中，仅对您和协作者可访问。此外，如果仓库位于组织的命名空间下，则具有相应角色或权限的人员也可以访问该仓库。

6. 输入仓库名称以确认更改。
7. 选择 **设为公共** 或 **设为私有**。

## 协作者

协作者是您希望授予其对个人仓库 `push` 和 `pull` 访问权限的人员。协作者无法执行任何管理任务，例如删除仓库或将其可见性从私有更改为公共。此外，协作者不能添加其他协作者。

只有个人仓库可以使用协作者。您可以向公共仓库添加无限数量的协作者，Docker Pro 账户可以向私有仓库添加最多 1 名协作者。

组织仓库不能使用协作者，但可以使用成员角色、团队或组织访问令牌来管理访问权限。

### 管理协作者

1. 登录 [Docker Hub](https://hub.docker.com)。

2. 选择 **我的 Hub** > **仓库**。

   将显示您的仓库列表。

3. 选择一个仓库。

   将显示该仓库的 **常规** 页面。

4. 选择 **协作者** 选项卡。

5. 根据 Docker 用户名添加或删除协作者。

您可以从仓库的 **设置** 页面选择协作者并管理其对私有仓库的访问权限。

## 组织角色

组织可以为个人分配角色，赋予他们在组织中的不同权限。有关更多详细信息，请参阅 [角色和权限](/manuals/enterprise/security/roles-and-permissions.md)。

## 组织团队

组织可以使用团队。可以为团队分配细粒度的仓库访问权限。

### 配置团队仓库权限

在配置仓库权限之前，您必须先创建一个团队。有关更多详细信息，请参阅 [创建和管理团队](/manuals/admin/organization/manage-a-team.md)。

要配置团队仓库权限：

1. 登录 [Docker Hub](https://hub.docker.com)。

2. 选择 **我的 Hub** > **仓库**。

   将显示您的仓库列表。

3. 选择一个仓库。

   将显示该仓库的 **常规** 页面。

4. 选择 **权限** 选项卡。

5. 添加、修改或删除团队的仓库权限。

   - 添加：指定 **团队**，选择 **权限**，然后选择 **添加**。
   - 修改：在团队旁边指定新的权限。
   - 删除：选择团队旁边的 **删除权限** 图标。

## 组织访问令牌 (OATs)

组织可以使用 OATs。OATs 允许您为令牌分配细粒度的仓库访问权限。有关更多详细信息，请参阅 [组织访问令牌](/manuals/enterprise/security/access-tokens.md)。

## 受控分发

{{< summary-bar feature_name="Gated distribution" >}}

受控分发允许发布者安全地与外部客户或合作伙伴共享私有容器镜像，而无需授予他们完整的组织访问权限，或让他们看到您的团队、协作者或其他仓库。

此功能非常适合希望控制谁可以拉取特定镜像的商业软件发布者，同时保持内部用户和外部消费者之间的清晰分离。

如果您对受控分发感兴趣，请联系 [Docker 销售团队](https://www.docker.com/pricing/contact-sales/) 获取更多信息。

### 主要功能

- **私有仓库分发**：内容存储在私有仓库中，仅对明确邀请的用户可访问。

- **无需组织成员的外部访问**：外部用户无需添加到您的内部组织即可拉取镜像。

- **仅拉取权限**：外部用户仅获得拉取访问权限，无法推送或修改仓库内容。

- **仅限邀请访问**：通过经过身份验证的电子邮件邀请授予访问权限，通过 API 管理。

### 通过 API 邀请分发成员

> [!NOTE]
> 邀请成员时，您需要为其分配角色。有关每种角色的访问权限的详细信息，请参阅 [角色和权限](/manuals/enterprise/security/roles-and-permissions.md)。

分发成员（用于受控分发）只能通过 Docker Hub API 邀请。目前不支持通过 UI 邀请此角色。要邀请分发成员，请使用批量创建邀请 API 端点。

要邀请分发成员：

1. 使用 [身份验证 API](https://docs.docker.com/reference/api/hub/latest/#tag/authentication-api/operation/AuthCreateAccessToken) 为您的 Docker Hub 账户生成一个 bearer token。

2. 在 Hub UI 中创建一个团队，或使用 [团队 API](https://docs.docker.com/reference/api/hub/latest/#tag/groups/paths/~1v2~1orgs~1%7Borg_name%7D~1groups/post)。

3. 授予团队仓库访问权限：
   - 在 Hub UI 中：导航到您的仓库设置，并添加具有“只读”权限的团队
   - 使用 [仓库团队 API](https://docs.docker.com/reference/api/hub/latest/#tag/repositories/paths/~1v2~1repositories~1%7Bnamespace%7D~1%7Brepository%7D~1groups/post)：将团队分配到您的仓库，并设置“只读”访问级别

4. 使用 [批量创建邀请端点](https://docs.docker.com/reference/api/hub/latest/#tag/invites/paths/~1v2~1invites~1bulk/post) 发送带有分发成员角色的电子邮件邀请。在请求正文中，将 "role" 字段设置为 "distributor_member"。

5. 被邀请的用户将收到一封包含接受邀请链接的电子邮件。使用其 Docker ID 登录后，他们将被授予作为分发成员对指定私有仓库的仅拉取访问权限。