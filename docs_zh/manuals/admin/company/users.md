---
title: 管理公司成员
description: 了解如何在 Docker 管理控制台中管理公司用户。
keywords: 公司, 公司用户, 用户, 管理员, 管理控制台, 成员管理, 组织管理, 公司管理, 批量邀请, 重新发送邀请
---

{{< summary-bar feature_name="Company" >}}

公司所有者可以通过 Docker ID、电子邮件地址邀请新成员加入组织，或使用包含电子邮件地址的 CSV 文件进行批量邀请。

如果被邀请者没有 Docker 账户，他们必须创建账户并验证电子邮件地址，才能接受加入组织的邀请。待处理的邀请会占用被邀请组织的席位。

## 通过 Docker ID 或电子邮件地址邀请成员

请按照以下步骤通过 Docker ID 或电子邮件地址邀请成员加入您的组织。

1. 登录 [Docker Home](https://app.docker.com) 并选择您的公司。
2. 在**组织 (Organizations)** 页面上，选择您要邀请成员加入的组织。
3. 选择**成员 (Members)**，然后选择**邀请 (Invite)**。
4. 选择**电子邮件或用户名 (Emails or usernames)**。
5. 按照屏幕上的说明邀请成员。
   最多邀请 1000 名成员，多个条目之间用逗号、分号或空格分隔。

   > [!NOTE]
   >
   > 邀请成员时，您需要为他们分配一个角色。
   > 有关每个角色的访问权限详情，请参阅[角色和权限](/security/for-admins/roles-and-permissions/)。

   待处理的邀请会显示在成员页面上。被邀请者将收到一封包含 Docker Hub 链接的电子邮件，他们可以在该链接处接受或拒绝邀请。

## 通过 CSV 文件邀请成员

要通过包含电子邮件地址的 CSV 文件邀请多个成员加入组织：

1. 登录 [Docker Home](https://app.docker.com) 并选择您的公司。
2. 在**组织 (Organizations)** 页面上，选择您要邀请成员加入的组织。
3. 选择**成员 (Members)**，然后选择**邀请 (Invite)**。
4. 选择**CSV 上传 (CSV upload)**。
5. 选择**下载 CSV 模板文件 (Download the template CSV file)**，可选择下载示例 CSV 文件。以下是有效 CSV 文件内容的示例。

   ```text
   email
   docker.user-0@example.com
   docker.user-1@example.com
   ```

   CSV 文件要求：

   - 文件必须包含标题行，且至少有一个名为 `email` 的标题。允许附加列，导入时将忽略这些列。
   - 文件最多包含 1000 个电子邮件地址（行）。要邀请超过 1000 名用户，请创建多个 CSV 文件，并对每个文件执行此任务中的所有步骤。

6. 创建新的 CSV 文件或从其他应用程序导出 CSV 文件。

   - 要从其他应用程序导出 CSV 文件，请参阅该应用程序的文档。
   - 要创建新的 CSV 文件，请在文本编辑器中打开一个新文件，在第一行键入 `email`，在后续行中每行键入一个用户电子邮件地址，然后以 .csv 扩展名保存文件。

7. 选择**浏览文件 (Browse files)**，然后选择您的 CSV 文件，或将 CSV 文件拖放到**选择要上传的 CSV 文件 (Select a CSV file to upload)** 框中。一次只能选择一个 CSV 文件。

   > [!NOTE]
   >
   > 如果 CSV 文件中的电子邮件地址数量超过组织中的可用席位数量，您将无法继续邀请成员。
   > 要邀请成员，您可以购买更多席位，或从 CSV 文件中删除一些电子邮件地址并重新选择新文件。要购买更多席位，请参阅[向您的订阅添加席位](/subscription/add-seats/)或[联系销售](https://www.docker.com/pricing/contact-sales/)。

8. 上传 CSV 文件后，选择**审查 (Review)**。

   有效的电子邮件地址和任何有问题的电子邮件地址将显示出来。电子邮件地址可能存在以下问题：

   - 无效的电子邮件：电子邮件地址不是有效的地址。如果您发送邀请，该电子邮件地址将被忽略。您可以在 CSV 文件中更正电子邮件地址并重新导入文件。
   - 已邀请：已向该用户发送过邀请邮件，不会再发送另一封邀请邮件。
   - 成员：该用户已经是您组织的成员，不会发送邀请邮件。
   - 重复：CSV 文件中包含多个相同的电子邮件地址。只会向该用户发送一封邀请邮件。

9. 按照屏幕上的说明邀请成员。

   > [!NOTE]
   >
   > 邀请成员时，您需要为他们分配一个角色。
   > 有关每个角色的访问权限详情，请参阅[角色和权限](/security/for-admins/roles-and-permissions/)。

待处理的邀请会显示在成员页面上。被邀请者将收到一封包含 Docker Hub 链接的电子邮件，他们可以在该链接处接受或拒绝邀请。

## 重新向用户发送邀请

您可以从管理控制台重新发送单个邀请或批量邀请。

### 重新发送单个邀请

1. 在 [Docker Home](https://app.docker.com/) 中，从左上角的账户下拉菜单中选择您的公司。
2. 选择**管理控制台 (Admin Console)**，然后选择**用户 (Users)**。
3. 选择被邀请者旁边的**操作菜单 (action menu)**，然后选择**重新发送 (Resend)**。
4. 选择**邀请 (Invite)** 进行确认。

### 批量重新发送邀请

1. 在 [Docker Home](https://app.docker.com/) 中，从左上角的账户下拉菜单中选择您的公司。
2. 选择**管理控制台 (Admin Console)**，然后选择**用户 (Users)**。
3. 使用**用户名 (Usernames)** 旁边的**复选框 (checkboxes)** 批量选择用户。
4. 选择**重新发送邀请 (Resend invites)**。
5. 选择**重新发送 (Resend)** 进行确认。

## 通过 API 邀请成员

您可以使用 Docker Hub API 批量邀请成员。更多信息，请参阅[批量创建邀请](https://docs.docker.com/reference/api/hub/latest/#tag/invites/paths/~1v2~1invites~1bulk/post) API 端点。

## 管理团队中的成员

使用 Docker Hub 将成员添加到团队或从团队中移除成员。更多详情，请参阅[管理成员](../organization/members.md#manage-members-on-a-team)。