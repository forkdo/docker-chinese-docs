# 自动配置


自动配置会在用户使用与您已验证域名匹配的电子邮件地址登录时，自动将他们添加到您的组织。在启用自动配置之前，您必须验证一个域名。

> [!IMPORTANT]
>
> 对于属于 SSO 连接的域名，在将用户添加到组织时，即时 (JIT) 配置优先于自动配置。

### 概述

当为已验证的域名启用自动配置时：

- 使用匹配电子邮件地址登录 Docker 的用户会自动添加到您的组织。
- 自动配置仅将现有 Docker 用户添加到您的组织，它不会创建新账户。
- 用户的登录流程不会发生变化。
- 公司和组织的所有者会在新用户添加时收到电子邮件通知。
- 您可能需要[管理席位](/manuals/admin/organization/manage/manage-seats.md)以容纳新用户。

### 启用自动配置

自动配置是按域名配置的。要启用它：

1. 登录 [Docker Home](https://app.docker.com) 并选择您的公司或组织。
1. 选择 **Identity & auth**，然后选择 **Domain management**。
1. 选择您要启用自动配置的域名旁边的 **操作菜单**。
1. 选择 **Enable auto-provisioning**。
1. 可选。如果在公司级别启用自动配置，请选择一个组织。
1. 选择 **Enable** 进行确认。

该域名的 **Auto-provisioning** 列会更新为 **Enabled**。

### 禁用自动配置

要为某个用户禁用自动配置：

1. 登录 [Docker Home](https://app.docker.com) 并选择您的组织。如果您的组织是某个公司的一部分，请选择该公司并在公司级别为组织配置域名。
1. 选择 **Identity & auth**，然后选择 **Domain management**。
1. 选择您的域名旁边的 **操作菜单**。
1. 选择 **Disable auto-provisioning**。
1. 选择 **Disable** 进行确认。

## 后续步骤

要选择其他方法配置用户，您可以设置：

- [SCIM 配置](/manuals/enterprise/security/provisioning/scim/_index.md) 以进行高级用户管理。
- [组映射](/manuals/enterprise/security/provisioning/scim/group-mapping.md) 以自动将用户分配到团队。

