# 管理公司




创建公司后，你可以使用 Docker Home 管理多个组织。公司所有者可以使用公司门户邀请用户加入特定组织、查看跨组织的席位可用情况，并添加新公司所有者。

## 添加更多组织

公司所有者可以将拥有 Docker Business 套餐的 Docker 组织添加到其公司，前提是他们同时也是该组织的所有者。添加到公司的组织数量没有限制。

> [!IMPORTANT]
>
> 一旦将某个组织添加到公司，就无法将其从公司中移除。

1. 登录 [Docker Home](https://app.docker.com) 并选择你的公司。
1. 选择 **Managed organizations**（管理的组织）。
1. 选择 **Add organization**（添加组织），然后从下拉菜单中选择一个组织。

嵌套组织必须保持其 Docker Business 订阅，才能由公司管理。如果某个组织从 Docker Business 降级，你将无法再通过公司管理它，其所有者必须单独管理它。

## 公司所有者

一个公司可以有多个所有者来管理公司及其所有组织。有关公司所有者角色及其对席位的影响的详情，请参阅 [公司角色](/manuals/admin/company/_index.md#company-roles)。

### 添加公司所有者

1. 登录 [Docker Home](https://app.docker.com) 并选择你的公司。
1. 选择 **Company owners**（公司所有者），然后选择 **Add owner**（添加所有者）。
1. 指定用户的 Docker ID，然后选择 **Add company owner**（添加公司所有者）完成。

### 移除公司所有者

1. 登录 [Docker Home](https://app.docker.com) 并选择你的公司。
1. 选择 **Company owners**（公司所有者）。
1. 找到你想移除的公司所有者并选择 **Actions**（操作）菜单，
   然后选择 **Remove as company owner**（移除公司所有者身份）。

## 公司邀请

你可以通过将用户邀请到公司内的某个组织来将其添加到公司。公司所有者可以使用 Docker ID、邮箱地址，或通过包含邮箱地址的 CSV 文件批量邀请成员加入公司中的任何组织。

成员和邀请属于各个组织，而不属于公司本身。待处理的邀请会占用被邀请用户所在组织的一个席位。

### 邀请成员加入组织

1. 登录 [Docker Home](https://app.docker.com) 并选择你的公司。
1. 选择 **Users**（用户），然后选择 **Invite**（邀请）。
1. 选择你希望邀请成员的方式：
   - 要邀请单个用户，选择 **Emails or usernames**（邮箱或用户名）。
   - 要邀请用户组，选择 **CSV upload**（CSV 上传）。
1. 通过选择 **Select an organization**（选择组织）将用户添加到某个组织。

用户会收到包含接受邀请说明的邮件邀请。接受邀请后，新成员会出现在
**Users**（用户）页面上。该表会指明他们是哪些组织的成员。

### 重新发送邀请

公司所有者可以从公司级别的 **Users**（用户）页面重新发送邀请。
要重新发送单个邀请：

1. 从 [Docker Home](https://app.docker.com/) 选择你的公司。
1. 选择 **Users**（用户），然后从用户表中找到被邀请者。
1. 选择 **Actions**（操作）菜单，然后选择 **Resend**（重新发送）。
   - 在重新发送之前，请确认你正在将邀请重新发送给正确的被邀请者。
   - 重新发送邀请弹窗会显示你最初邀请该用户的日期。
1. 选择 **Invite**（邀请）进行确认。

要批量重新发送邀请：

1. 在用户表中，使用被邀请者旁边的多选复选框选择你要邀请的人员。
1. 选择 **Resend invites**（重新发送邀请），然后选择 **Resend**（重新发送）进行确认。

## 为组织添加席位

如果你拥有没有待处理订阅变更的自助订阅，可以使用 Docker Home 添加席位。有关添加席位的更多信息，请参阅 [管理席位](/manuals/admin/organization/manage/manage-seats.md#add-seats-to-your-subscription)。

如果你拥有销售协助的订阅，必须联系 Docker 支持或销售团队来添加席位。

## 管理团队

团队存在于组织级别，而非公司级别。将成员邀请到组织后，你可以将他们添加到该组织内的团队。更多详情，请参阅
[管理团队中的成员](/manuals/admin/organization/manage/members.md#manage-members-on-a-team)。

