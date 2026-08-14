# 管理组织成员


了解如何管理组织的成员。

## 邀请成员

所有者可以通过 Docker ID、邮箱地址或包含邮箱地址的 CSV 文件邀请新成员加入组织。如果被邀请者没有 Docker 账户，他们必须先创建一个并验证其邮箱地址，才能接受加入组织的邀请。邀请成员时，其待处理的邀请会占用一个席位。

### 通过 Docker ID 或邮箱地址邀请成员

使用以下步骤通过 Docker ID 或邮箱地址邀请成员加入组织。

1. 登录 [Docker Home](https://app.docker.com) 并从左上角的账户下拉菜单中选择你的
   组织。
1. 选择 **Members**（成员），然后选择 **Invite**（邀请）。
1. 选择 **Emails or usernames**（邮箱或用户名）。
1. 按照屏幕上的说明邀请成员。最多可邀请 1000 名成员，多个条目用逗号、分号或空格分隔。

邀请成员时，你会为他们分配一个角色。有关每个角色访问权限的详情，请参阅
[角色与权限](/manuals/enterprise/security/roles-and-permissions/_index.md)。

待处理的邀请会显示在表格中。被邀请者会收到一封包含指向 Docker Hub 链接的电子邮件，他们可以在那里接受或拒绝邀请。

### 通过 CSV 文件邀请成员

要通过包含邮箱地址的 CSV 文件邀请多名成员加入组织：

1. 登录 [Docker Home](https://app.docker.com) 并从左上角的账户下拉菜单中选择你的
   组织。选择 **Members**（成员） >
   **Invite**（邀请） > **CSV upload**（CSV 上传）。
1. 可选。选择 **Download the template CSV file**（下载模板 CSV 文件）以下载一个示例
   CSV 文件。以下是有效 CSV 文件内容的示例：

   ```text
   email
   docker.user-0@example.com
   docker.user-1@example.com
   ```

   示例文件说明了 CSV 文件的要求：
   - 文件必须包含一个表头行，其中至少有一个标题为 email 的列。
     允许使用附加列，导入时会忽略它们。
   - 文件最多必须包含 1000 个邮箱地址（行）。要邀请
     超过 1000 名用户，请创建多个 CSV 文件，并对每个文件执行本任务中的所有步骤。

1. 创建新的 CSV 文件或从其他应用程序导出 CSV 文件。
   - 要从其他应用程序导出 CSV 文件，请参阅该应用程序的文档。
   - 要创建新的 CSV 文件，请在文本编辑器中打开一个新文件，在第一行输入 email，在后续各行每行输入一个用户邮箱地址，然后将文件保存为 .csv 扩展名。
1. 选择 **Browse files**（浏览文件），然后选择你的 CSV 文件，或将
   CSV 文件拖放到 **Select a CSV file to upload**（选择要上传的 CSV 文件）框中。一次只能选择一个 CSV 文件。
1. CSV 文件上传后，选择 **Review**（审查）以识别任何无效邮箱地址、已邀请的用户、已是成员的受邀用户，或同一 CSV 文件中的重复邮箱地址。
1. 按照屏幕上的说明邀请成员。

待处理的邀请会显示在表格中。被邀请者会收到一封包含指向 Docker Hub 链接的电子邮件，他们可以在那里接受或拒绝邀请。

### 通过 API 邀请成员

你可以使用 Docker Hub API 批量邀请成员。更多信息，请参阅
[Bulk create invites](https://docs.docker.com/reference/api/hub/latest/#tag/invites/paths/~1v2~1invites~1bulk/post)
API 端点。

## 接受邀请

收到邮件邀请后，用户可以访问指向 Docker Hub 的链接，在那里接受或拒绝邀请。

要接受邀请：

1. 查看你的收件箱，打开 Docker 发来的包含加入 Docker 组织邀请的电子邮件。
1. 要打开指向 Docker Hub 的链接，请选择邀请邮件中的链接。
1. Docker 账户创建页面会打开。如果你已有账户，
   选择 **Already have an account? Sign in**（已有账户？登录）。如果你没有账户，
   请使用收到邀请的同一个邮箱地址创建一个。
1. 可选。如果你没有账户并创建了一个，你必须返回收件箱，使用 Docker 验证邮件验证你的邮箱地址。
1. 登录 Docker Hub 后，从顶部导航菜单中选择 **My Hub**。
1. 在你的邀请上选择 **Accept**（接受）。

接受邀请后，你现在是该组织的成员。

邀请邮件链接在 14 天后过期。如果你的邮件链接已过期，可以使用发送该链接的
[Docker Hub](https://hub.docker.com/) 邮箱地址登录，并从
**Notifications**（通知）面板接受邀请。

## 管理邀请

邀请成员后，你可以根据需要重新发送或移除邀请。每个被邀请者占用一个席位，因此如果你的 CSV 文件中的邮箱地址数量超过了组织中可用席位的数量，你将无法邀请更多成员。

> [!TIP]
>
> 需要管理超过 1,000 名团队成员？
> [升级到 Docker Business 以无限量邀请用户](https://www.docker.com/pricing?ref=Docs&refAction=DocsAdminMembers)
> 并使用高级角色管理。你也可以
> [添加席位](/manuals/admin/organization/manage/manage-seats.md) 到你的订阅。

### 重新发送邀请

你可以发送单个邀请，也可以从 Admin Console 批量发送邀请。

要重新发送单个邀请：

1. 登录 [Docker Home](https://app.docker.com/) 并选择你的
   组织。
1. 选择 **Members**（成员）。
1. 选择被邀请者旁边的 **操作菜单**，然后选择 **Resend**（重新发送）。
1. 选择 **Invite**（邀请）进行确认。

要批量重新发送邀请：

1. 登录 [Docker Home](https://app.docker.com/) 并选择你的
   组织。
1. 选择 **Members**（成员）。
1. 使用 **Usernames**（用户名）旁边的**复选框**批量选择用户。
1. 选择 **Resend invites**（重新发送邀请）。
1. 选择 **Resend**（重新发送）进行确认。

### 移除邀请

要移除邀请：

1. 登录 [Docker Home](https://app.docker.com/) 并选择你的
   组织。
1. 选择 **Members**（成员）。
1. 选择被邀请者旁边的 **操作菜单**，然后选择
   **Remove invitee**（移除被邀请者）。
1. 选择 **Remove**（移除）进行确认。

## 管理团队中的成员

使用 Docker Hub 或 Docker Home 添加或移除团队成员。组织所有者可以将成员添加到组织内的一个或多个团队。

### 将成员添加到团队

要将成员添加到团队：

1. 登录 [Docker Home](https://app.docker.com/) 并选择你的
   组织。
1. 选择 **Teams**（团队）。
1. 选择团队名称。
1. 选择 **Add member**（添加成员）。你可以通过搜索其邮箱地址或用户名来添加成员。

被邀请者必须先接受加入组织的邀请，然后才能被添加到团队。

### 从团队中移除成员

如果你的组织使用了启用
[SCIM](/manuals/enterprise/security/provisioning/scim/_index.md) 的单点登录 (SSO)，你应该从身份提供商 (IdP) 中移除成员。这会自动从 Docker 中移除成员。如果 SCIM 已禁用，请按照本文档中的流程在 Docker 中手动移除成员。

组织所有者可以从团队中移除成员。将成员从团队中移除会撤销其对所允许资源的访问权限。要从特定团队中移除成员：

1. 登录 [Docker Home](https://app.docker.com/) 并选择你的
   组织。
1. 选择 **Teams**（团队），然后选择你要移除的团队成员的姓名。
1. 选择用户名旁边的 **X** 将其从团队中移除。
1. 出现提示时，选择 **Remove**（移除）进行确认。

### 更新成员角色

组织所有者可以在组织内管理
[角色](/manuals/enterprise/security/roles-and-permissions/_index.md)。如果某个组织属于公司，公司所有者也可以管理该组织的角色。如果你启用了 SSO，可以使用 [SCIM 进行角色映射](/manuals/enterprise/security/provisioning/scim/_index.md)。

要更新成员角色：

1. 登录 [Docker Home](https://app.docker.com/) 并选择你的
   组织。
1. 选择 **Members**（成员）。
1. 找到要编辑其角色的成员的用户名。选择
   **Actions**（操作）菜单，然后选择 **Edit role**（编辑角色）。

如果你是组织的唯一所有者并且想要编辑自己的角色，请为你的组织指定一个新的所有者，以便编辑你的角色。

## 导出成员 CSV 文件



所有者可以导出一个包含所有成员的 CSV 文件。公司的 CSV 文件包含以下字段：

- Name：用户的姓名
- Username：用户的 Docker ID
- Email：用户的邮箱地址
- Member of Organizations：用户在公司内所属的所有组织
- Invited to Organizations：用户在公司内被邀请加入的所有组织
- Account Created：用户账户创建的时间和日期

要导出成员的 CSV 文件：

1. 登录 [Docker Home](https://app.docker.com/) 并选择你的
   组织。
1. 选择 **Members**（成员）。
1. 选择**下载**图标以导出所有成员的 CSV 文件。

