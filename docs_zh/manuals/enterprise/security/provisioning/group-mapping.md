---
title: 组映射
description: 通过将身份提供程序组与 Docker 团队同步，实现团队成员资格的自动化管理
keywords: 组映射, SCIM, Docker Admin, 管理员, 安全, 团队管理, 用户配置, 身份提供程序
aliases:
- /admin/company/settings/group-mapping/
- /admin/organization/security-settings/group-mapping/
- /docker-hub/group-mapping/
- /security/for-admins/group-mapping/
- /security/for-admins/provisioning/group-mapping/
weight: 30
---

{{< summary-bar feature_name="SSO" >}}

组映射功能可自动将身份提供程序 (IdP) 中的用户组与 Docker 组织中的团队进行同步。例如，当您在 IdP 中将开发者添加到 "backend-team" 组时，他们会自动添加到 Docker 中的相应团队。

本文档将介绍组映射的工作原理以及如何设置组映射。

> [!TIP]
>
> 如果您需要将用户添加到多个组织或一个组织内的多个团队，组映射是理想的选择。如果您不需要设置多组织或多团队分配，SCIM [用户级属性](scim.md#set-up-role-mapping) 可能更适合您的需求。

## 前提条件

在开始之前，您必须满足以下条件：

- 为您的组织配置了 SSO
- 拥有 Docker Home 和身份提供程序的管理员访问权限

## 组映射的工作原理

组映射通过以下关键组件使您的 Docker 团队与 IdP 组保持同步：

- **认证流程**：当用户通过 SSO 登录时，您的 IdP 会与 Docker 共享用户属性，包括电子邮件、姓名和组成员资格。
- **自动更新**：Docker 使用这些属性创建或更新用户配置文件，并根据 IdP 组的更改管理团队分配。
- **唯一标识**：Docker 使用电子邮件地址作为唯一标识符，因此每个 Docker 账户必须拥有唯一的电子邮件地址。
- **团队同步**：用户的团队成员资格在 Docker 中会自动反映您在 IdP 组中所做的更改。

## 设置组映射

组映射的设置涉及配置您的身份提供程序以与 Docker 共享组信息。这需要：

- 使用 Docker 的命名格式在 IdP 中创建组
- 配置属性，以便您的 IdP 在认证期间发送组数据
- 将用户添加到相应的组中
- 测试连接以确保组正确同步

您可以将组映射与仅使用 SSO 的场景配合使用，也可以与 SSO 和 SCIM 结合使用，以实现增强的用户生命周期管理。

### 组命名格式

在 IdP 中使用以下格式创建组：`organization:team`。

例如：

- 对于 "moby" 组织中的 "developers" 团队：`moby:developers`
- 对于多组织访问：`moby:backend` 和 `whale:desktop`

如果组同步时团队尚不存在，Docker 会自动创建团队。

### 支持的属性

| 属性 | 描述 |
|:--------- | :---------- |
| `id` | 组的唯一 ID，采用 UUID 格式。此属性为只读。 |
| `displayName` | 组的名称，遵循组映射格式：`organization:team`。 |
| `members` | 属于此组的成员用户列表。 |
| `members(x).value` | 作为此组成员的用户的唯一 ID。成员通过 ID 引用。 |

## 使用 SSO 配置组映射

将组映射与使用 SAML 认证方法的 SSO 连接配合使用。

> [!NOTE]
>
> 使用 Azure AD (OIDC) 认证方法时不支持通过 SSO 进行组映射。这些配置不需要 SCIM。

{{< tabs >}}
{{< tab name="Okta" >}}

您的 IdP 用户界面可能与以下步骤略有不同。请参阅 [Okta 文档](https://help.okta.com/oie/en-us/content/topics/apps/define-group-attribute-statements.htm) 进行验证。

设置组映射：

1. 登录 Okta 并打开您的应用程序。
2. 导航到应用程序的 **SAML 设置** 页面。
3. 在 **组属性声明（可选）** 部分，按如下方式配置：
   - **名称**：`groups`
   - **名称格式**：`Unspecified`
   - **筛选器**：`Starts with` + `organization:`，其中 `organization` 是您组织的名称
   筛选器选项将筛选掉与您的 Docker 组织无关的组。
4. 选择 **目录**，然后选择 **组** 来创建您的组。
5. 使用格式 `organization:team` 添加您的组，该格式应与 Docker 中的组织和团队名称匹配。
6. 将用户分配到您创建的组。

下次与 Docker 同步组时，您的用户将映射到您定义的 Docker 组。

{{< /tab >}}
{{< tab name="Entra ID" >}}

您的 IdP 用户界面可能与以下步骤略有不同。请参阅 [Entra ID 文档](https://learn.microsoft.com/en-us/azure/active-directory/app-provisioning/customize-application-attributes) 进行验证。

设置组映射：

1. 登录 Entra ID 并打开您的应用程序。
2. 选择 **管理**，然后选择 **单一登录**。
3. 选择 **添加组声明**。
4. 在组声明部分，选择 **分配给应用程序的组**，源属性为 **仅限云的组显示名称（预览）**。
5. 选择 **高级选项**，然后选择 **筛选组** 选项。
6. 按如下方式配置属性：
   - **要匹配的属性**：`显示名称`
   - **匹配方式**：`包含`
   - **字符串**：`:`
7. 选择 **保存**。
8. 选择 **组**、**所有组**，然后选择 **新建组** 来创建您的组。
9. 将用户分配到您创建的组。

下次与 Docker 同步组时，您的用户将映射到您定义的 Docker 组。

{{< /tab >}}
{{< /tabs >}}

## 使用 SCIM 配置组映射

将组映射与 SCIM 结合使用，以实现更高级的用户生命周期管理。在开始之前，请确保您已先 [设置 SCIM](./scim.md#enable-scim)。

{{< tabs >}}
{{< tab name="Okta" >}}

您的 IdP 用户界面可能与以下步骤略有不同。请参阅 [Okta 文档](https://help.okta.com/en-us/Content/Topics/users-groups-profiles/usgp-enable-group-push.htm) 进行验证。

设置您的组：

1. 登录 Okta 并打开您的应用程序。
2. 选择 **应用程序**，然后选择 **配置** 和 **集成**。
3. 选择 **编辑** 以在您的连接上启用组，然后选择 **推送组**。
4. 选择 **保存**。保存此配置会将 **推送组** 选项卡添加到您的应用程序。
5. 选择 **目录**，然后选择 **组** 来创建您的组。
6. 使用格式 `organization:team` 添加您的组，该格式应与 Docker 中的组织和团队名称匹配。
7. 将用户分配到您创建的组。
8. 返回到 **集成** 页面，然后选择 **推送组** 选项卡以打开可控制和管理组配置方式的视图。
9. 选择 **推送组**，然后选择 **按规则查找组**。
10. 按规则配置组，如下所示：
    - 输入规则名称，例如 `与 Docker Hub 同步组`
    - 按名称匹配组，例如以 `docker:` 开头或包含 `:`（用于多组织）
    - 如果启用 **立即按规则推送组**，则组或组分配发生更改时同步会立即发生。如果您不想手动推送组，请启用此选项。

在 **推送的组** 列的 **按规则** 下找到您的新规则。匹配该规则的组会列在右侧的组表中。

要推送此表中的组：

1. 选择 **Okta 中的组**。
2. 选择 **推送状态** 下拉菜单。
3. 选择 **立即推送**。

{{< /tab >}}
{{< tab name="Entra ID" >}}

您的 IdP 用户界面可能与以下步骤略有不同。请参阅 [Entra ID 文档](https://learn.microsoft.com/en-us/azure/active-directory/app-provisioning/customize-application-attributes) 进行验证。

在配置组映射之前，请完成以下操作：

1. 登录 Entra ID 并转到您的应用程序。
2. 在您的应用程序中，选择 **配置**，然后选择 **映射**。
3. 选择 **配置 Microsoft Entra ID 组**。
4. 选择 **显示高级选项**，然后选择 **编辑属性列表**。
5. 将 `externalId` 类型更新为 `reference`，然后选中 **多值** 复选框并选择引用的对象属性 `urn:ietf:params:scim:schemas:core:2.0:Group`。
6. 选择 **保存**，然后选择 **是** 进行确认。
7. 转到 **配置**。
8. 将 **配置状态** 切换为 **开**，然后选择 **保存**。

接下来，设置组映射：

1. 转到应用程序概览页面。
2. 在 **配置用户账户** 下，选择 **开始**。
3. 选择 **添加用户/组**。
4. 使用 `organization:team` 格式创建您的组。
5. 将组分配给配置组。
6. 选择 **开始配置** 以开始同步。

要进行验证，请选择 **监视**，然后选择 **配置日志** 以查看您的组是否已成功配置。在您的 Docker 组织中，您可以检查组是否已正确配置以及成员是否已添加到相应的团队。

{{< /tab >}}
{{< /tabs >}}

完成后，通过 SSO 登录 Docker 的用户将自动添加到 IdP 中映射的组织和团队。

> [!TIP]
>
> [启用 SCIM](scim.md) 以利用自动用户配置和取消配置功能。如果您不启用 SCIM，用户只会自动配置。您必须手动取消配置。