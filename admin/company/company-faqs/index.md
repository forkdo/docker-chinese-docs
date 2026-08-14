# 公司常见问题


### 我的一些组织没有 Docker Business 订阅。我还能使用父级公司吗？

可以，但你只能将拥有 Docker Business 订阅的组织添加到公司。更多详情，请参阅 [添加更多组织](/manuals/admin/company/manage.md#add-more-organizations)。

### 如果我的某个组织从 Docker Business 降级，但我仍需要以公司所有者身份访问怎么办？

要访问和管理嵌套组织，该组织必须拥有 Docker Business 订阅。如果某个组织从 Docker Business 降级，其所有者必须在公司之外管理它。更多详情，请参阅
[添加更多组织](/manuals/admin/company/manage.md#add-more-organizations)。

### 公司所有者会占用订阅席位吗？

除非满足以下任一情况，否则公司所有者不会占用席位：

- 他们被添加为公司下某个组织的成员
- 启用了 SSO，且公司所有者通过 SSO 登录，这会将其自动添加为组织成员

当你首次创建公司时，你的账户既是公司所有者也是组织所有者，因此只要你仍是组织所有者，它就会占用一个席位。要释放该席位，请
[将另一名用户指定为组织所有者](/manuals/admin/organization/manage/members.md#update-a-member-role)
并将自己从组织中移除。作为公司所有者，你仍保留完整的管理访问权限，而无需占用订阅席位。

### 公司所有者在关联/嵌套组织中拥有哪些权限？

公司所有者可以导航到 **Organizations**（组织）页面，在单一位置查看其所有嵌套组织。他们还可以查看或编辑组织成员，并更改单点登录 (SSO) 与跨域身份管理系统 (SCIM) 设置。对公司设置的更改会影响公司下每个组织中的所有用户。

更多信息，请参阅 [角色与权限](/manuals/enterprise/security/roles-and-permissions.md)。

