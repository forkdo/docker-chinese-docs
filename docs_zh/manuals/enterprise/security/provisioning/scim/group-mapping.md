---
title: 组映射
description: 通过将身份提供商组与 Docker 团队同步来自动化团队成员资格
keywords: Group Mapping, SCIM, Docker Admin, admin, security, team management, user provisioning, identity provider
aliases:
- /admin/company/settings/group-mapping/
- /admin/organization/security-settings/group-mapping/
- /security/for-admins/group-mapping/
- /security/for-admins/provisioning/scim/group-mapping/
- /enterprise/security/provisioning/group-mapping/
weight: 20
---

{{< summary-bar feature_name="SSO" >}}

组映射会自动将你的身份提供商（IdP）中的用户组与你的 Docker 组织中的团队同步。例如，当你在 IdP 中将一个开发者
添加到 "backend-team" 组时，他们会自动被添加到 Docker 中对应的团队。

本页解释了组映射的工作原理，以及如何设置组映射。

> [!TIP]
>
> 组映射非常适合将用户添加到多个组织或同一组织内的多个团队。如果你不需要设置多组织或多团队分配，SCIM 的
> [用户级属性](provision-scim.md#set-up-role-mapping) 可能更适合你的需求。

## 先决条件（Prerequisites）

在开始之前，你必须拥有：

- 为你的组织配置好的 SSO
- 对 Docker Home 和你的身份提供商的管理员访问权限

## 组映射的工作原理（How group mapping works）

组映射通过以下关键组件使你的 Docker 团队与 IdP 组保持同步：

- 认证流程：当用户通过 SSO 登录时，你的 IdP 会与 Docker 共享用户属性，包括电子邮件、姓名和组成员身份。
- 自动更新：Docker 使用这些属性来创建或更新用户配置文件，并根据 IdP 组的更改管理团队分配。
- 唯一标识：Docker 使用电子邮件地址作为唯一标识符，因此每个 Docker 账户必须拥有唯一的电子邮件地址。
- 团队同步：用户在 Docker 中的团队成员身份会自动反映你在 IdP 组中所做的更改。

## 设置组映射（Set up group mapping）

组映射设置涉及配置你的身份提供商以与 Docker 共享组信息。这需要：

- 使用 Docker 的命名格式在 IdP 中创建组
- 配置属性，使你的 IdP 在认证期间发送组数据
- 将用户添加到适当的组
- 测试连接以确保组正确同步

你可以单独将组映射与 SSO 一起使用，或与 SSO 和 SCIM 一起使用以增强用户生命周期管理。

### 组命名格式（Group naming format）

在你的 IdP 中使用格式 `organization:team` 创建组。

例如：

- 对于 "moby" 组织中的 "developers" 团队：`moby:developers`
- 对于多组织访问：`moby:backend` 和 `whale:desktop`

Docker 会在组同步时自动创建团队（如果它们尚不存在）。

### 支持的属性（Supported attributes）

| 属性 | 描述 |
|:--------- | :---------- |
| `id` | 组的唯一 ID，UUID 格式。此属性为只读。 |
| `displayName` | 遵循组映射格式的组名：`organization:team`。 |
| `members` | 作为该组成员的用户列表。 |
| `members(x).value` | 作为该组成员的用户的唯一 ID。成员通过 ID 引用。 |

## 使用 SSO 配置组映射（Configure group mapping with SSO）

将组映射用于使用 SAML 认证方法的 SSO 连接。

> [!NOTE]
>
> 使用 Azure AD（OIDC）认证方法的 SSO 不支持组映射。这些配置不需要 SCIM。

{{< tabs >}}
{{< tab name="Okta" >}}

你的 IdP 的用户界面可能与以下步骤略有不同。请参考 [Okta 文档](https://help.okta.com/oie/en-us/content/topics/apps/define-group-attribute-statements.htm) 核实。

要设置组映射：

1. 登录 Okta 并打开你的应用。
1. 导航到你应用的 **SAML Settings** 页面。
1. 在 **Group Attribute Statements (optional)** 部分，按如下配置：
   - **Name**：`groups`
   - **Name format**：`Unspecified`
   - **Filter**：`Starts with` + `organization:`，其中 `organization` 是你的组织名
   筛选选项会过滤掉与你的 Docker 组织无关的组。
1. 通过选择 **Directory**，然后 **Groups** 来创建你的组。
1. 使用格式 `organization:team` 添加你的组，使其匹配 Docker 中你的组织（或组织们）和团队的名称。
1. 将用户分配到你创建的组。

下次你将组与 Docker 同步时，你的用户将映射到你所定义的 Docker 组。

{{< /tab >}}
{{< tab name="Entra ID" >}}

你的 IdP 的用户界面可能与以下步骤略有不同。请参考 [Entra ID 文档](https://learn.microsoft.com/en-us/azure/active-directory/app-provisioning/customize-application-attributes) 核实。

要设置组映射：

1. 登录 Entra ID 并打开你的应用。
1. 选择 **Manage**，然后 **Single sign-on**。
1. 选择 **Add a group claim**。
1. 在 Group Claims 部分，选择 **Groups assigned to the application**，源属性为 **Cloud-only group display names (Preview)**。
1. 选择 **Advanced options**，然后 **Filter groups** 选项。
1. 按如下配置属性：
   - **Attribute to match**：`Display name`
   - **Match with**：`Contains`
   - **String**：`:`
1. 选择 **Save**。
1. 选择 **Groups**、**All groups**，然后 **New group** 来创建你的组。
1. 将用户分配到你创建的组。

下次你将组与 Docker 同步时，你的用户将映射到你所定义的 Docker 组。

{{< /tab >}}
{{< /tabs >}}

## 使用 SCIM 配置组映射（Configure group mapping with SCIM）

将组映射与 SCIM 一起使用，以获得更高级的用户生命周期管理。在开始之前，请确保你先
[设置了 SCIM](./provision-scim.md#enable-scim)。

{{< tabs >}}
{{< tab name="Okta" >}}

你的 IdP 的用户界面可能与以下步骤略有不同。请参考 [Okta 文档](https://help.okta.com/en-us/Content/Topics/users-groups-profiles/usgp-enable-group-push.htm) 核实。

要设置你的组：

1. 登录 Okta 并打开你的应用。
1. 选择 **Applications**，然后 **Provisioning**，再 **Integration**。
1. 选择 **Edit** 以在你的连接上启用组，然后选择 **Push groups**。
1. 选择 **Save**。保存此配置会将 **Push Groups** 标签页添加到你的应用。
1. 通过导航到 **Directory** 并选择 **Groups** 来创建你的组。
1. 使用格式 `organization:team` 添加你的组，使其匹配 Docker 中你的组织（或组织们）和团队的名称。
1. 将用户分配到你创建的组。
1. 返回 **Integration** 页面，然后选择 **Push Groups** 标签页，打开你可以控制和管理组如何配置的视图。
1. 选择 **Push Groups**，然后 **Find groups by rule**。
1. 按如下通过规则配置组：
   - 输入规则名称，例如 `Sync groups with Docker Hub`
   - 按名称匹配组，例如以 `docker:` 开头或包含 `:`（针对多组织）
   - 如果你启用 **Immediately push groups by rule**，则一旦组或组分配发生更改，同步就会发生。如果你不想手动推送组，请启用此项。

在 **Pushed Groups** 列的 **By rule** 下找到你的新规则。匹配该规则的组列在右侧的组表中。

要从该表推送组：

1. 选择 **Group in Okta**。
1. 选择 **Push Status** 下拉菜单。
1. 选择 **Push Now**。

{{< /tab >}}
{{< tab name="Entra ID" >}}

你的 IdP 的用户界面可能与以下步骤略有不同。请参考 [Entra ID 文档](https://learn.microsoft.com/en-us/azure/active-directory/app-provisioning/customize-application-attributes) 核实。

在配置组映射之前，先完成以下操作：

1. 登录 Entra ID 并转到你的应用。
1. 在你的应用中，选择 **Provisioning**，然后 **Mappings**。
1. 选择 **Provision Microsoft Entra ID Groups**。
1. 选择 **Show advanced options**，然后 **Edit attribute list**。
1. 将 `externalId` 类型更新为 `reference`，然后选择 **Multi-Value** 复选框，并选择被引用的对象属性 `urn:ietf:params:scim:schemas:core:2.0:Group`。
1. 选择 **Save**，然后 **Yes** 确认。
1. 转到 **Provisioning**。
1. 将 **Provision Status** 切换为 **On**，然后选择 **Save**。

接下来，设置组映射：

1. 转到应用概览页面。
1. 在 **Provision user accounts** 下，选择 **Get started**。
1. 选择 **Add user/group**。
1. 使用 `organization:team` 格式创建你的组。
1. 将组分配到配置组。
1. 选择 **Start provisioning** 开始同步。

要验证，选择 **Monitor**，然后 **Provisioning logs** 查看你的组是否成功配置。在你的 Docker 组织中，你可以检查
组是否正确配置，以及成员是否已添加到适当的团队。

{{< /tab >}}
{{< /tabs >}}

一旦完成，通过 SSO 登录 Docker 的用户会自动被添加到 IdP 中映射的组织和团队。

> [!TIP]
>
> [启用 SCIM](provision-scim.md) 以利用自动用户配置和取消配置。如果你不启用 SCIM，用户仅会被自动配置。你必须
> 手动取消配置他们。

## 下一步（Next steps）

- [为组织成员分配角色](/manuals/enterprise/security/roles-and-permissions/core-roles.md)。
- 根据需要 [强制登录](/manuals/enterprise/security/enforce-sign-in.md)。
