---
title: 创建和管理团队
weight: 40
description: 了解如何为您的组织创建和管理团队
keywords: docker, registry, teams, organizations, plans, Dockerfile, Docker Hub, docs, documentation, repository permissions, configure repository access, team management
aliases:
- /docker-hub/manage-a-team/
---

{{< summary-bar feature_name="Admin orgs" >}}

您可以在 Admin Console 或 Docker Hub 中为您的组织创建团队，并在 Docker Hub 中配置团队仓库访问权限。

团队是属于某个组织的一组 Docker 用户。一个组织可以有多个团队。组织所有者可以创建新团队，并使用 Docker ID 或电子邮件地址将成员添加到现有团队。成员不需要成为团队的一部分即可与组织关联。

组织所有者可以通过分配所有者角色，添加额外的组织所有者来帮助他们管理组织中的用户、团队和仓库。

## 什么是组织所有者？

组织所有者是具有以下权限的管理员：

- 管理仓库并将团队成员添加到组织
- 访问私有仓库、所有团队、账单信息和组织设置
- 为组织中的每个团队指定[权限](#permissions-reference)
- 为组织启用 [SSO](/manuals/enterprise/security/single-sign-on/_index.md)

当为您的组织启用 SSO 时，组织所有者还可以管理用户。Docker 可以通过 SSO 强制执行为新的最终用户或希望拥有单独的 Docker ID 用于公司用途的用户自动配置 Docker ID。

组织所有者可以添加具有所有者角色的其他人来帮助他们管理组织中的用户、团队和仓库。

有关角色的更多信息，请参阅[角色和权限](/manuals/enterprise/security/roles-and-permissions.md)。

## 创建团队

1. 登录 [Docker Home](https://app.docker.com) 并选择您的组织。
1. 选择 **Teams**。

## 设置团队仓库权限

您必须先创建团队，然后才能配置仓库权限。更多详情，请参阅[创建和管理团队](/manuals/admin/organization/manage-a-team.md)。

设置团队仓库权限：

1. 登录 [Docker Hub](https://hub.docker.com)。
1. 选择 **My Hub** > **Repositories**。

   您的仓库列表将出现。

1. 选择一个仓库。

   仓库的 **General** 页面将出现。

1. 选择 **Permissions** 选项卡。
1. 添加、修改或删除团队的仓库权限。

   - 添加：指定 **Team**，选择 **Permission**，然后选择 **Add**。
   - 修改：在团队旁边指定新的权限。
   - 删除：选择团队旁边的 **Remove permission** 图标。

### 权限参考

- `Read-only` 访问权限允许用户查看、搜索和拉取私有仓库，方式与拉取公共仓库相同。
- `Read & Write` 访问权限允许用户拉取、推送和查看仓库。此外，它还允许用户查看、取消、重试或触发构建。
- `Admin` 访问权限允许用户拉取、推送、查看、编辑和删除仓库。您还可以编辑构建设置并更新仓库的描述、协作者权限、公共/私有可见性以及删除。

权限是累积的。例如，如果您拥有 "Read & Write" 权限，您将自动拥有 "Read-only" 权限。

下表显示了每个权限级别允许用户执行的操作：

| 操作 | Read-only | Read & Write | Admin |
|:------------------:|:---------:|:------------:|:-----:|
| 拉取仓库 | ✅ | ✅ | ✅ |
| 查看仓库 | ✅ | ✅ | ✅ |
| 推送仓库 | ❌ | ✅ | ✅ |
| 编辑仓库 | ❌ | ❌ | ✅ |
| 删除仓库 | ❌ | ❌ | ✅ |
| 更新仓库描述 | ❌ | ❌ | ✅ |
| 查看构建 | ✅ | ✅ | ✅ |
| 取消构建 | ❌ | ✅ | ✅ |
| 重试构建 | ❌ | ✅ | ✅ |
| 触发构建 | ❌ | ✅ | ✅ |
| 编辑构建设置 | ❌ | ❌ | ✅ |

> [!NOTE]
>
> 未验证其电子邮件地址的用户仅对仓库拥有 `Read-only` 访问权限，无论其团队成员资格赋予了他们什么权利。

## 删除团队

组织所有者可以删除团队。当您从组织中移除团队时，此操作会撤销成员对该团队允许资源的访问权限。它不会将用户从他们所属的其他团队中删除，也不会删除任何资源。

1. 登录 [Docker Home](https://app.docker.com/) 并选择您的组织。
1. 选择 **Teams**。
1. 选择要删除的团队名称旁边的 **Actions** 图标。
1. 选择 **Delete team**。
1. 查看确认消息，然后选择 **Delete**。

## 更多资源

- [视频：Docker 团队](https://youtu.be/WKlT1O-4Du8?feature=shared&t=348)
- [视频：角色、团队和仓库](https://youtu.be/WKlT1O-4Du8?feature=shared&t=435)