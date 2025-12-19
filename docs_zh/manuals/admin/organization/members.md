---
title: 管理组织成员
weight: 30
description: 了解如何在 Docker Hub 和 Docker 管理控制台中管理组织成员。
keywords: members, teams, organizations, invite members, manage team members, export member list, edit roles, organization teams, user management
aliases:
- /docker-hub/members/
---

了解如何在 Docker Hub 和 Docker 管理控制台中为您的组织管理成员。

## 邀请成员

组织所有者可以通过 Docker ID、电子邮件地址或包含电子邮件地址的 CSV 文件邀请新成员加入组织。如果被邀请者没有 Docker 账户，则必须先创建账户并验证其电子邮件地址，然后才能接受加入组织的邀请。邀请成员时，其待处理的邀请会占用一个席位。

### 通过 Docker ID 或电子邮件地址邀请成员

使用以下步骤通过 Docker ID 或电子邮件地址邀请成员加入您的组织。

1. 登录 [Docker Home](https://app.docker.com)，然后从左上角的账户下拉菜单中选择您的组织。
1. 选择 **Members**（成员），然后选择 **Invite**（邀请）。
1. 选择 **Emails or usernames**（电子邮件或用户名）。
1. 按照屏幕上的说明邀请成员。最多邀请 1000 名成员，多个条目之间用逗号、分号或空格分隔。

> [!NOTE]
>
> 邀请成员时，您需要为其分配角色。有关每个角色的访问权限的详细信息，请参阅[角色和权限](/manuals/enterprise/security/roles-and-permissions.md)。

待处理的邀请会显示在表格中。被邀请者将收到一封电子邮件，其中包含一个指向 Docker Hub 的链接，他们可以通过该链接接受或拒绝邀请。

### 通过 CSV 文件邀请成员

要通过包含电子邮件地址的 CSV 文件邀请多名成员加入组织：

1. 登录 [Docker Home](https://app.docker.com)，然后从左上角的账户下拉菜单中选择您的组织。
1. 选择 **Members**（成员），然后选择 **Invite**（邀请）。
1. 选择 **CSV upload**（CSV 上传）。
1. 可选操作：选择 **Download the template CSV file**（下载模板 CSV 文件）以下载示例 CSV 文件。以下是有效 CSV 文件内容的示例。

```text
email
docker.user-0@example.com
docker.user-1@example.com
```

CSV 文件要求：

- 文件必须包含一个标题行，其中至少有一个名为 email 的标题。允许包含其他列，但在导入时会被忽略。
- 文件最多包含 1000 个电子邮件地址（行）。要邀请超过 1000 个用户，请创建多个 CSV 文件，并对每个文件执行此任务中的所有步骤。

1. 创建一个新的 CSV 文件，或从其他应用程序导出 CSV 文件。

- 要从其他应用程序导出 CSV 文件，请参阅该应用程序的文档。
- 要创建新的 CSV 文件，请在文本编辑器中打开一个新文件，在第一行键入 email，在接下来的每一行键入一个用户电子邮件地址，然后将文件保存为 .csv 扩展名。

1. 选择 **Browse files**（浏览文件），然后选择您的 CSV 文件，或者将 CSV 文件拖放到 **Select a CSV file to upload**（选择要上传的 CSV 文件）框中。您一次只能选择一个 CSV 文件。

> [!NOTE]
>
> 如果 CSV 文件中的电子邮件地址数量超过了组织中可用席位的数量，您将无法继续邀请成员。要邀请成员，您可以购买更多席位，或者从 CSV 文件中删除一些电子邮件地址并重新选择新文件。要购买更多席位，请参阅[为您的订阅添加席位](/manuals/subscription/manage-seats.md)或[联系销售](https://www.docker.com/pricing/contact-sales/)。

1. CSV 文件上传后，选择 **Review**（审查）。

有效的电子邮件地址和存在问题的电子邮件地址都会显示出来。电子邮件地址可能存在以下问题：

- 无效电子邮件：该电子邮件地址不是有效地址。如果发送邀请，该电子邮件地址将被忽略。您可以在 CSV 文件中更正电子邮件地址，然后重新导入文件。
- 已邀请：该用户已收到邀请电子邮件，不会再次发送邀请电子邮件。
- 成员：该用户已经是您组织的成员，不会发送邀请电子邮件。
- 重复：CSV 文件中多次出现相同的电子邮件地址。该用户只会收到一封邀请电子邮件。

1. 按照屏幕上的说明邀请成员。

> [!NOTE]
>
> 邀请成员时，您需要为其分配角色。有关每个角色的访问权限的详细信息，请参阅[角色和权限](/manuals/enterprise/security/roles-and-permissions.md)。

待处理的邀请会显示在表格中。被邀请者将收到一封电子邮件，其中包含一个指向 Docker Hub 的链接，他们可以通过该链接接受或拒绝邀请。

### 通过 API 邀请成员

您可以使用 Docker Hub API 批量邀请成员。有关更多信息，请参阅 [Bulk create invites](https://docs.docker.com/reference/api/hub/latest/#tag/invites/paths/~1v2~1invites~1bulk/post) API 端点。

## 接受邀请

当邀请发送至用户的电子邮件地址时，他们会收到一个指向 Docker Hub 的链接，可以通过该链接接受或拒绝邀请。要接受邀请：

1. 检查您的电子邮件收件箱，并打开 Docker 发送的邀请您加入 Docker 组织的电子邮件。
1. 要打开指向 Docker Hub 的链接，请选择 **click here**（点击此处）链接。

   > [!WARNING]
   >
   > 邀请电子邮件链接在 14 天后过期。如果您的电子邮件链接已过期，您可以使用链接发送到的电子邮件地址登录 [Docker Hub](https://hub.docker.com/)，然后从 **Notifications**（通知）面板接受邀请。

1. Docker 创建账户页面将打开。如果您已有账户，请选择 **Already have an account? Sign in**（已有账户？登录）。如果您还没有账户，请使用收到邀请的相同电子邮件地址创建一个账户。
1. 可选操作：如果您没有账户并已创建了一个账户，则必须返回到您的电子邮件收件箱，并使用 Docker 验证电子邮件验证您的电子邮件地址。
1. 登录 Docker Hub 后，从顶级导航菜单中选择 **My Hub**（我的 Hub）。
1. 在您的邀请上选择 **Accept**（接受）。

接受邀请后，您就成为该组织的成员了。

## 管理邀请

邀请成员后，您可以根据需要重新发送或删除邀请。

### 重新发送邀请

您可以从管理控制台重新发送单个邀请或批量邀请。

要重新发送单个邀请：

1. 登录 [Docker Home](https://app.docker.com/) 并选择您的组织。
1. 选择 **Members**（成员）。
1. 选择被邀请者旁边的 **action menu**（操作菜单），然后选择 **Resend**（重新发送）。
1. 选择 **Invite**（邀请）以确认。

要批量重新发送邀请：

1. 登录 [Docker Home](https://app.docker.com/) 并选择您的组织。
1. 选择 **Members**（成员）。
1. 使用 **Usernames**（用户名）旁边的 **checkboxes**（复选框）批量选择用户。
1. 选择 **Resend invites**（重新发送邀请）。
1. 选择 **Resend**（重新发送）以确认。

### 删除邀请

要从管理控制台删除邀请：

1. 登录 [Docker Home](https://app.docker.com/) 并选择您的组织。
1. 选择 **Members**（成员）。
1. 选择被邀请者旁边的 **action menu**（操作菜单），然后选择 **Remove invitee**（删除被邀请者）。
1. 选择 **Remove**（删除）以确认。

## 管理团队中的成员

使用 Docker Hub 或管理控制台添加或删除团队成员。组织所有者可以将成员添加到一个或多个组织内的团队中。

### 将成员添加到团队

要使用管理控制台将成员添加到团队：

1. 登录 [Docker Home](https://app.docker.com/) 并选择您的组织。
1. 选择 **Teams**（团队）。
1. 选择团队名称。
1. 选择 **Add member**（添加成员）。您可以通过搜索其电子邮件地址或用户名来添加成员。

   > [!NOTE]
   >
   > 被邀请者必须先接受加入组织的邀请，然后才能被添加到团队中。

### 从团队中删除成员

> [!NOTE]
>
> 如果您的组织启用了[SCIM](/manuals/enterprise/security/provisioning/scim.md) 的单点登录 (SSO)，您应该从您的身份提供商 (IdP) 中删除成员。这将从 Docker 中自动删除成员。如果未启用 SCIM，您必须手动在 Docker 中管理成员。

组织所有者可以在 Docker Hub 或管理控制台中从团队中删除成员。从团队中删除成员将撤销其对允许资源的访问权限。

要使用管理控制台从特定团队中删除成员：

1. 登录 [Docker Home](https://app.docker.com/) 并选择您的组织。
1. 选择 **Teams**（团队）。
1. 选择团队名称。
1. 选择用户名旁边的 **X** 以将其从团队中删除。
1. 出现提示时，选择 **Remove**（删除）以确认。

### 更新成员角色

组织所有者可以在组织内管理[角色](/security/for-admins/roles-and-permissions/)。如果组织属于某个公司，则公司所有者也可以管理该组织的角色。如果启用了 SSO，您可以使用 [SCIM 进行角色映射](/security/for-admins/provisioning/scim/)。

> [!NOTE]
>
> 如果您是组织的唯一所有者，在编辑自己的角色之前，需要先分配一位新的所有者。

要在管理控制台中更新成员角色：

1. 登录 [Docker Home](https://app.docker.com/) 并选择您的组织。
1. 选择 **Members**（成员）。
1. 找到您要编辑其角色的成员的用户名。选择 **Actions**（操作）菜单，然后选择 **Edit role**（编辑角色）。

## 导出成员 CSV 文件

{{< summary-bar feature_name="Admin orgs" >}}

所有者可以导出包含所有成员的 CSV 文件。公司的 CSV 文件包含以下字段：

- 姓名：用户的姓名
- 用户名：用户的 Docker ID
- 电子邮件：用户的电子邮件地址
- 组织成员：用户在某个公司内所属的所有组织
- 受邀加入组织：用户在某个公司内被邀请加入的所有组织
- 账户创建时间：用户账户创建的时间和日期

要导出成员的 CSV 文件：

1. 登录 [Docker Home](https://app.docker.com/) 并选择您的组织。
1. 选择 **Members**（成员）。
1. 选择 **download**（下载）图标以导出所有成员的 CSV 文件。