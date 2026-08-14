---
title: Create and manage a team（创建和管理团队）
linkTitle: Teams（团队）
weight: 20
description: 了解如何为你的组织创建和管理团队
keywords: docker, registry, teams, organizations, plans, Dockerfile, Docker
  Hub, docs, documentation, repository permissions, configure repository access, team management
aliases:
  - /docker-hub/manage-a-team/
  - /admin/organization/manage-a-team/
---

{{< summary-bar feature_name="Admin orgs" >}}

你可以在 Docker Home 或 Docker Hub 中为你的组织创建团队，并在 Docker Hub 中配置团队仓库访问权限。

团队是属于某个组织的一组 Docker 用户。一个组织可以有多个团队。组织所有者可以使用其 Docker ID 或电子邮件地址创建新团队并向现有团队添加成员。成员不一定要属于某个团队才能与组织关联。

组织所有者可以添加额外的组织所有者，通过为其分配所有者角色来帮助他们管理组织中的用户、团队和仓库。

## What is an organization owner?（什么是组织所有者？）

组织所有者是拥有以下权限的管理员：

- 管理仓库并向组织添加团队成员
- 访问私有仓库、所有团队、账单信息和组织设置
- 为组织中的每个团队指定 [permissions](#permissions-reference)（权限）
- 为组织启用 [SSO](/manuals/enterprise/security/single-sign-on/_index.md)

当为你的组织启用 SSO 时，组织所有者还可以管理用户。Docker 可以通过 SSO 强制执行为新最终用户或希望拥有单独 Docker ID 用于公司用途的用户自动配置 Docker ID。

组织所有者可以添加具有所有者角色的其他人来帮助他们管理组织中的用户、团队和仓库。

有关角色的更多信息，请参阅 [Roles and permissions](/manuals/enterprise/security/roles-and-permissions.md)。

## Create a team（创建团队）

1. 登录 [Docker Home](https://app.docker.com) 并选择你的组织。
1. 选择 **Teams**。
1. 选择 **Create team**。
1. 提供团队信息，然后选择 **Create**。

## Set team repository permissions（设置团队仓库权限）

你必须先创建团队，然后才能配置仓库权限。更多详情，请参阅 [Create and manage a team](/manuals/admin/organization/manage/manage-a-team.md)。

要设置团队仓库权限：

1. 登录 [Docker Hub](https://hub.docker.com)。
1. 选择 **My Hub** > **Repositories**。

   将显示你的仓库列表。

1. 选择一个仓库。

   将显示该仓库的 **General** 页面。

1. 选择 **Permissions** 选项卡。
1. 添加、修改或移除团队的仓库权限。
   - 添加（Add）：指定 **Team**，选择 **Permission**，然后选择 **Add**。
   - 修改（Modify）：在团队旁边指定新的权限。
   - 移除（Remove）：选择团队旁边的 **Remove permission** 图标。

### Permissions reference（权限参考）

- `Read-only`（只读）访问允许用户以与公共仓库相同的方式查看、搜索和拉取私有仓库。
- `Read & Write`（读写）访问允许用户拉取、推送和查看仓库。此外，它还允许用户查看、取消、重试或触发构建。
- `Admin`（管理员）访问允许用户拉取、推送、查看、编辑和删除仓库。你还可以编辑构建设置并更新仓库的描述、协作者权限、公开/私有可见性以及删除。

权限是累积的。例如，如果你拥有“Read & Write”权限，你会自动拥有“Read-only”权限。

下表显示了每个权限级别允许用户执行的操作：

|             Action（操作）              | Read-only（只读） | Read & Write（读写） | Admin（管理员） |
| :-----------------------------: | :-------: | :----------: | :---: |
|        Pull a Repository（拉取仓库）        |    ✅     |      ✅      |  ✅   |
|        View a Repository（查看仓库）        |    ✅     |      ✅      |  ✅   |
|        Push a Repository（推送仓库）        |    ❌     |      ✅      |  ✅   |
|        Edit a Repository（编辑仓库）        |    ❌     |      ❌      |  ✅   |
|       Delete a Repository（删除仓库）       |    ❌     |      ❌      |  ✅   |
| Update a Repository Description（更新仓库描述） |    ❌     |      ❌      |  ✅   |
|           View Builds（查看构建）           |    ✅     |      ✅      |  ✅   |
|          Cancel Builds（取消构建）          |    ❌     |      ✅      |  ✅   |
|          Retry Builds（重试构建）           |    ❌     |      ✅      |  ✅   |
|         Trigger Builds（触发构建）         |    ❌     |      ✅      |  ✅   |
|       Edit Build Settings（编辑构建设置）       |    ❌     |      ❌      |  ✅   |

> [!NOTE]
>
> 未验证电子邮件地址的用户只有对该仓库的 `Read-only` 访问权限，无论其团队成员身份赋予了他们什么权限。

## Delete a team（删除团队）

组织所有者可以删除团队。当你从组织中移除一个团队时，此操作会撤销该团队成员对其被许可资源的访问权限。它不会将用户从他们所属的其他团队中移除，也不会删除任何资源。

1. 登录 [Docker Home](https://app.docker.com/) 并选择你的组织。
1. 选择 **Teams**。
1. 选择你要删除的团队名称旁边的 **Actions** 图标。
1. 选择 **Delete team**。
1. 查看确认消息，然后选择 **Delete**。

## More resources（更多资源）

- [Video: Docker Teams](https://youtu.be/WKlT1O-4Du8?feature=shared&t=348)
- [Video: Roles, teams, and repositories](https://youtu.be/WKlT1O-4Du8?feature=shared&t=435)
