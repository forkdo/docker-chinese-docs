---
title: 组映射
description: 通过将身份提供商组与 Docker 团队同步来自动管理团队成员
keywords: 组映射, SCIM, Docker 管理员, 管理员, 安全, 团队管理, 用户配置, 身份提供商
aliases:
- /admin/company/settings/group-mapping/
- /admin/organization/security-settings/group-mapping/
- /docker-hub/group-mapping/
- /security/for-admins/group-mapping/
- /security/for-admins/provisioning/group-mapping/
weight: 30
---

{{< summary-bar feature_name="SSO" >}}

组映射会自动将用户组从您的身份提供商（IdP）同步到 Docker 组织中的团队。例如，当您在 IdP 中将开发人员添加到 "backend-team" 组时，他们会被自动添加到 Docker 中对应的团队。

本文档解释了组映射的工作原理，以及如何设置组映射。

> [!TIP]
>
> 组映射非常适合将用户添加到多个组织或单个组织内的多个团队。如果您不需要设置多组织或多团队分配，SCIM [用户级属性](scim.md#set-up-role-mapping) 可能更适合您的需求。

## 前置条件

开始之前，您必须具备：

- 为您的组织配置了 SSO
- 对 Docker Home 和您的身份提供商具有管理员访问权限

## 组映射的工作原理

组映射通过以下关键组件保持 Docker 团队与 IdP 组的同步：

- 认证流程：当用户通过 SSO 登录时，您的 IdP 会与 Docker 共享用户属性，包括电子邮件、姓名和组成员身份。
- 自动更新：Docker 使用这些属性创建或更新用户配置文件，并根据 IdP 组的变化管理团队分配。
- 唯一标识：Docker 使用电子邮件地址作为唯一标识符，因此每个 Docker 账户必须具有唯一的电子邮件地址。
- 团队同步：Docker 中用户的团队成员身份会自动反映 IdP 组中的变化。

## 设置组映射

组映射设置涉及配置您的身份提供商，使其与 Docker 共享组信息。这需要：

- 在您的 IdP 中使用 Docker 的命名格式创建组
- 配置属性，使您的 IdP 在认证期间发送组数据
- 将用户添加到适当的组
- 测试连接以确保组正确同步

您可以仅使用 SSO 进行组映射，也可以同时使用 SSO 和 SCIM 以实现增强的用户生命周期管理。

### 组命名格式

在您的 IdP 中使用格式：`organization:team` 创建组。

例如：

- 对于 "moby" 组织中的 "developers" 团队：`moby:developers`
- 对于多组织访问：`moby:backend` 和 `whale:desktop`

Docker 在组同步时会自动创建团队（如果它们尚不存在）。

### 支持的属性

| 属性 | 描述 |
|:--------- | :---------- |
| `id` | 组在 UUID 格式中的唯一 ID。此属性为只读。 |
| `displayName` | 组的名称，遵循组映射格式：`organization:team`。 |
| `members` | 此组成员的用户列表。 |
| `members(x).value` | 此组成员的用户的唯一 ID。成员通过 ID 引用。 |

## 使用 SSO 配置组映射

对使用 SAML 认证方法的 SSO 连接使用组映射。

> [!NOTE]
>
> 使用 SSO 的组映射不支持 Azure AD (OIDC) 认证方法。这些配置不需要 SCIM。

{{< tabs >}}
{{< tab name="Okta" >}}

您的 IdP 用户界面可能与以下步骤略有不同。请参考 [Okta 文档](https://help.okta.com/oie/en-us/content/topics/apps/define-group-attribute-statements.htm) 进行验证。

设置组映射的步骤：

1. 登录 Okta 并打开您的应用程序。
1. 导航到应用程序的 **SAML Settings** 页面。
1. 在 **Group Attribute Statements (optional)** 部分，按如下方式配置：
   - **Name**: `groups`
   - **Name format**: `Unspecified`
   - **Filter**: `Starts with` + `organization:`，其中 `organization` 是您的组织名称
   过滤选项将过滤掉与您的 Docker 组织无关的组。
1. 通过选择 **Directory**，然后选择 **Groups** 创建您的组。
1. 使用格式 `organization:team` 添加您的组，该格式需与 Docker 中的组织和团队名称匹配。
1. 将用户分配给您创建的组。

下次您与 Docker 同步组时，您的用户将映射到您定义的 Docker 组。

{{< /tab >}}
{{< tab name="Entra ID" >}}

您的 IdP 用户界面可能与以下步骤略有不同。请参考 [Entra ID 文档](https://learn.microsoft.com/en-us/azure/active-directory/app-provisioning/customize-application-attributes) 进行验证。

设置组映射的步骤：

1. 登录 Entra ID 并打开您的应用程序。
1. 选择 **Manage**，然后选择 **Single sign-on**。
1. 选择 **Add a group claim**。
1. 在 Group Claims 部分，选择 **Groups assigned to the application**，源属性为 **Cloud-only group display names (Preview)**。
1. 选择 **Advanced options**，然后选择 **Filter groups** 选项。
1. 按如下方式配置属性：
   - **Attribute to match**: `Display name`
   - **Match with**: `Contains`
   - **String**: `:`
1. 选择 **Save**。
1. 选择 **Groups**，**All groups**，然后 **New group** 创建您的组。
1. 将用户分配给您创建的组。

下次您与 Docker 同步组时，您的用户将映射到您定义的 Docker 组。

{{< /tab >}}
{{< /tabs >}}

## 使用 SCIM 配置组映射

使用 SCIM 进行组映射以实现更高级的用户生命周期管理。开始之前，请确保您已先 [设置 SCIM](./scim.md#enable-scim)。

{{< tabs >}}
{{< tab name="Okta" >}}

您的 IdP 用户界面可能与以下步骤略有不同。请参考 [Okta 文档](https://help.okta.com/en-us/Content/Topics/users-groups-profiles/usgp-enable-group-push.htm) 进行验证。

设置组的步骤：

1. 登录 Okta 并打开您的应用程序。
1. 选择 **Applications**，然后选择 **Provisioning** 和 **Integration**。
1. 选择 **Edit** 以在连接上启用组，然后选择 **Push groups**。
1. 选择 **Save**。保存此配置将向您的应用程序添加 **Push Groups** 选项卡。
1. 通过导航到 **Directory** 并选择 **Groups** 创建您的组。
1. 使用格式 `organization:team` 添加您的组，该格式需与 Docker 中的组织和团队名称匹配。
1. 将用户分配给您创建的组。
1. 返回 **Integration** 页面，然后选择 **Push Groups** 选项卡，打开可以控制和管理组配置方式的视图。
1. 选择 **Push Groups**，然后选择 **Find groups by rule**。
1. 按如下方式配置组规则：
    - 输入规则名称，例如 `Sync groups with Docker Hub`
    - 按名称匹配组，例如以 `docker:` 开头或包含 `:`（用于多组织）
    - 如果启用 **Immediately push groups by rule**，组或组分配发生更改时会立即同步。如果您不想手动推送组，请启用此选项。

在 **Pushed Groups** 列中的 **By rule** 下找到您的新规则。匹配该规则的组列在右侧的组表中。

从该表推送组：

1. 选择 **Group in Okta**。
1. 选择 **Push Status** 下拉菜单。
1. 选择 **Push Now**。

{{< /tab >}}
{{< tab name="Entra ID" >}}

您的 IdP 用户界面可能与以下步骤略有不同。请参考 [Entra ID 文档](https://learn.microsoft.com/en-us/azure/active-directory/app-provisioning/customize-application-attributes) 进行验证。

配置组映射之前完成以下操作：

1. 登录 Entra ID 并进入您的应用程序。
1. 在您的应用程序中，选择 **Provisioning**，然后选择 **Mappings**。
1. 选择 **Provision Microsoft Entra ID Groups**。
1. 选择 **Show advanced options**，然后选择 **Edit attribute list**。
1. 将 `externalId` 类型更新为 `reference`，然后选择 **Multi-Value** 复选框并选择引用的对象属性 `urn:ietf:params:scim:schemas:core:2.0:Group`。
1. 选择 **Save**，然后选择 **Yes** 确认。
1. 进入 **Provisioning**。
1. 将 **Provision Status** 切换为 **On**，然后选择 **Save**。

接下来，设置组映射：

1. 进入应用程序概览页面。
1. 在 **Provision user accounts** 下，选择 **Get started**。
1. 选择 **Add user/group**。
1. 使用 `organization:team` 格式创建您的组。
1. 将组分配给配置组。
1. 选择 **Start provisioning** 开始同步。

验证：选择 **Monitor**，然后选择 **Provisioning logs** 查看您的组是否成功配置。在您的 Docker 组织中，您可以检查组是否正确配置，以及成员是否已添加到适当的团队。

{{< /tab >}}
{{< /tabs >}}

完成后，通过 SSO 登录 Docker 的用户会自动添加到 IdP 中映射的组织和团队。

> [!TIP]
>
> [启用 SCIM](scim.md) 以利用自动用户配置和取消配置。如果您不启用 SCIM，用户只会自动配置，您必须手动取消配置他们。