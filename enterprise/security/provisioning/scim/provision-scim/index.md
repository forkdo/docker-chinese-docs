# 设置 SCIM 配置




## 支持的属性（Supported attributes）

SCIM 使用属性（姓名、电子邮件等）在你的身份提供商和 Docker 之间同步用户信息。在你的身份提供商中正确映射这些属性
可确保用户配置（provisioning）顺利进行，并防止在使用单点登录时出现重复用户账户等问题。

Docker 支持以下 SCIM 属性：

| 属性             | 描述                                                                       |
| :--------------- | :-------------------------------------------------------------------------------- |
| `userName`        | 用户的主电子邮件地址，用作唯一标识符                                          |
| `name.givenName`  | 用户的名                                                                       |
| `name.familyName` | 用户的姓                                                                       |
| `active`          | 指示用户是启用还是禁用，设置为 "false" 以取消配置（de-provision）用户          |

有关受支持属性和 SCIM 的更多详情，请参阅
[Docker Hub API SCIM 参考](/reference/api/hub/latest.md#tag/scim)。

> [!IMPORTANT]
>
> 默认情况下，Docker 对 SSO 使用即时（JIT）配置。如果启用了 SCIM，JIT 值仍然优先，并将覆盖 SCIM 设置的属性值。
> 为避免冲突，请确保你的 JIT 属性值与 SCIM 值匹配。
>
> 或者，你可以禁用 JIT 配置，仅依赖 SCIM。详情请参阅
> [Just-in-Time](/manuals/enterprise/security/provisioning/just-in-time.md)。

## 在 Docker 中启用 SCIM（Enable SCIM in Docker）

要启用 SCIM：

1. 登录 [Docker Home](https://app.docker.com)。
1. 选择 **Identity & auth**，然后 **SSO and SCIM**。
1. 在 **SSO connections**（SSO 连接）表中，选择你连接的 **Actions**（操作）图标，然后选择 **Setup SCIM**（设置 SCIM）。
1. 复制 **SCIM Base URL** 和 **API Token** 并将这些值粘贴到你的 IdP 中。

## 在 IdP 中启用 SCIM（Enable SCIM in your IdP）

你的身份提供商的用户界面可能与以下步骤略有不同。你可以参考你的身份提供商的文档进行核实。有关更多详情，请参阅
你的身份提供商的文档：

- [Okta](https://help.okta.com/en-us/Content/Topics/Apps/Apps_App_Integration_Wizard_SCIM.htm)
- [Entra ID/Azure AD SAML 2.0](https://learn.microsoft.com/en-us/azure/active-directory/app-provisioning/user-provisioning)

> [!NOTE]
>
> Microsoft 目前不支持在同一非库应用程序中同时使用 SCIM 和 OIDC。本页提供了一个经过验证的变通方案，使用单独的
> 非库应用进行 SCIM 配置。虽然 Microsoft 未正式记录此设置，但它在实践中被广泛使用并受支持。

**Okta**



### 第一步：启用 SCIM（Step one: Enable SCIM）

1. 登录 Okta 并选择 **Admin** 打开管理门户。
1. 打开你配置 SSO 连接时创建的应用程序。
1. 在应用程序页面，选择 **General** 标签页，然后 **Edit App Settings**。
1. 启用 SCIM 配置，然后选择 **Save**。
1. 导航到 **Provisioning**，然后选择 **Edit SCIM Connection**。
1. 要在 Okta 中配置 SCIM，请使用以下值和设置设置你的连接：
   - SCIM Base URL: SCIM 连接器基础 URL（从 Docker Home 复制）
   - Unique identifier field for users: `email`
   - Supported provisioning actions: **Push New Users** 和 **Push Profile Updates**
   - Authentication Mode: HTTP Header
   - SCIM Bearer Token: HTTP Header Authorization Bearer Token（从 Docker Home 复制）
1. 选择 **Test Connector Configuration**。
1. 查看测试结果并选择 **Save**。

### 第二步：启用同步（Step two: Enable synchronization）

1. 在 Okta 中，选择 **Provisioning**。
1. 选择 **To App**，然后 **Edit**。
1. 启用 **Create Users**、**Update User Attributes** 和 **Deactivate Users**。
1. 选择 **Save**。
1. 移除不必要的映射。必要的映射是：
   - Username
   - Given name
   - Family name
   - Email

接下来，[设置角色映射](#set-up-role-mapping)。

**Entra ID (OIDC)**



Microsoft 不支持在同一非库应用程序中同时使用 SCIM 和 OIDC。你必须在 Entra ID 中创建第二个非库应用程序用于 SCIM 配置。

### 第一步：创建单独的 SCIM 应用（Step one: Create a separate SCIM app）

1. 在 Azure 门户中，转到 **Microsoft Entra ID** > **Enterprise Applications** > **New application**。
1. 选择 **Create your own application**。
1. 为你的应用命名，并选择 **Integrate any other application you don't find in the gallery**。
1. 选择 **Create**。

### 第二步：配置 SCIM 配置（Step two: Configure SCIM provisioning）

1. 在你的新 SCIM 应用中，转到 **Provisioning** > **Get started**。
1. 将 **Provisioning Mode** 设置为 **Automatic**。
1. 在 **Admin Credentials** 下：
   - **Tenant URL**：粘贴来自 Docker Home 的 **SCIM Base URL**。
   - **Secret Token**：粘贴来自 Docker Home 的 **SCIM API token**。
1. 选择 **Test Connection** 验证。
1. 选择 **Save** 保存凭据。

接下来，[设置角色映射](#set-up-role-mapping)。

**Entra ID (SAML 2.0)**



1. 在 Azure 门户中，转到 **Microsoft Entra ID** > **Enterprise Applications**，并选择你的 Docker SAML 应用。
1. 选择 **Provisioning** > **Get started**。
1. 将 **Provisioning Mode** 设置为 **Automatic**。
1. 在 **Admin Credentials** 下：
   - **Tenant URL**：粘贴来自 Docker Home 的 **SCIM Base URL**。
   - **Secret Token**：粘贴来自 Docker Home 的 **SCIM API token**。
1. 选择 **Test Connection** 验证。
1. 选择 **Save** 保存凭据。

接下来，[设置角色映射](#set-up-role-mapping)。



## 设置角色映射（Set up role mapping）

你可以通过在 IdP 中添加可选的 SCIM 属性来为用户分配
[Docker 角色](/manuals/enterprise/security/roles-and-permissions/_index.md)。这些属性会覆盖在你的 SSO 配置中设置的
默认角色和团队值。

> [!NOTE]
>
> 角色映射同时支持 SCIM 和即时（JIT）配置。对于 JIT，角色映射仅在用户首次配置时应用。

下表列出了受支持的可选用户级属性：

| 属性          | 可能的值                            | 备注                                                                                                                                                                                                                                                            |
| ------------- | ---------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `dockerRole`  | `member`、`editor` 或 `owner`      | 如果未设置，用户默认为 `member` 角色。设置此属性会覆盖默认值。<br><br>有关角色定义，请参阅 [角色与权限](/manuals/enterprise/security/roles-and-permissions/_index.md)。                                                        |
| `dockerOrg`   | Docker `organizationName`（如 `moby`） | 覆盖在你的 SSO 连接中配置的默认组织。<br><br>如果未设置，用户将被配置到默认组织。如果 `dockerOrg` 和 `dockerTeam` 都设置了，用户将被配置到指定组织中的团队。 |
| `dockerTeam`  | Docker `teamName`（如 `developers`）   | 将用户配置到默认或指定组织中的指定团队。如果团队不存在，将自动创建。<br><br>你仍可以使用 [组映射](group-mapping.md) 将用户分配到跨组织的多个团队。   |

这些属性使用的外部命名空间为：`urn:ietf:params:scim:schemas:extension:docker:2.0:User`。在为 Docker 创建自定义 SCIM
属性时，此值在身份提供商中是必需的。

**Okta**



### 第一步：在 Okta 中设置角色映射（Step one: Set up role mapping in Okta）

1. 先设置 [SSO](/manuals/enterprise/security/single-sign-on/connect.md) 和 SCIM。
1. 在 Okta 管理门户中，转到 **Directory**，选择 **Profile Editor**，然后 **User (Default)**。
1. 选择 **Add Attribute** 并为你想添加的角色、组织或团队配置值。不要求名称完全匹配。
1. 返回 **Profile Editor** 并选择你的应用。
1. 选择 **Add Attribute** 并输入所需的值。**External Name** 和 **External Namespace** 必须完全准确。
   - 组织/团队/角色映射的外部名分别是 `dockerOrg`、`dockerTeam` 和 `dockerRole`，如前面的表中所列。
   - 它们的外部命名空间都相同：`urn:ietf:params:scim:schemas:extension:docker:2.0:User`。
1. 创建属性后，导航到页面顶部并选择 **Mappings**，然后 **Okta User to YOUR APP**。
1. 转到新创建的属性，将变量名映射到外部名，然后选择 **Save Mappings**。如果你使用 JIT 配置，请继续以下步骤。
1. 导航到 **Applications** 并选择 **YOUR APP**。
1. 选择 **General**，然后 **SAML Settings**，再 **Edit**。
1. 选择 **Step 2** 并配置从用户属性到 Docker 变量的映射。

### 第二步：按用户分配角色（Step two: Assign roles by user）

1. 在 Okta 管理门户中，选择 **Directory**，然后 **People**。
1. 选择 **Profile**，然后 **Edit**。
1. 选择 **Attributes** 并将属性更新为所需值。

### 第三步：按组分配角色（Step three: Assign roles by group）

1. 在 Okta 管理门户中，选择 **Directory**，然后 **People**。
1. 选择 **YOUR GROUP**，然后 **Applications**。
1. 打开 **YOUR APPLICATION** 并选择 **Edit** 图标。
1. 将属性更新为所需值。

如果用户尚未设置属性，添加到该组的用户将在配置时继承这些属性。

**Entra ID/Azure AD (SAML 2.0 and OIDC)**



### 第一步：配置属性映射（Step one: Configure attribute mappings）

1. 完成 [SCIM 配置设置](/manuals/enterprise/security/provisioning/scim/provision-scim.md#enable-scim-in-docker)。
1. 在 Azure 门户中，打开 **Microsoft Entra ID** > **Enterprise Applications**，并选择你的 SCIM 应用。
1. 转到 **Provisioning** > **Mappings** > **Provision Azure Active Directory Users**。
1. 添加或更新以下映射：
   - `userPrincipalName` -> `userName`
   - `mail` -> `emails.value`
   - 可选。使用以下
     [映射方法](/manuals/enterprise/security/provisioning/scim/provision-scim.md#set-up-role-mapping) 之一映射 `dockerRole`、`dockerOrg` 或 `dockerTeam`。
1. 移除任何不支持的属性以防止同步错误。
1. 可选。转到 **Mappings** > **Provision Azure Active Directory Groups**：
   - 如果组配置导致错误，将 **Enabled** 设置为 **No**。
   - 如果启用，请仔细测试组映射。
1. 选择 **Save** 应用映射。

### 第二步：选择角色映射方法（Step two: Choose a role mapping method）

你可以使用以下方法之一映射 `dockerRole`、`dockerOrg` 或 `dockerTeam`：

#### 表达式映射（Expression mapping）

如果你只需要分配像 `member`、`editor` 或 `owner` 这样的 Docker 角色，请使用此方法。

1. 在 **Edit Attribute** 视图中，将映射类型设置为 **Expression**。
1. 在 **Expression** 字段中：
   1. 如果你的 App Roles 与 Docker 角色完全匹配，使用：
      SingleAppRoleAssignment([appRoleAssignments])
   1. 如果不匹配，使用 switch 表达式：`Switch(SingleAppRoleAssignment([appRoleAssignments]), "My Corp Admins", "owner", "My Corp Editors", "editor", "My Corp Users", "member")`
1. 设置：
   - **Target attribute**：`urn:ietf:params:scim:schemas:extension:docker:2.0:User:dockerRole`
   - **Match objects using this attribute**：No
   - **Apply this mapping**：Always
1. 保存你的更改。

> [!WARNING]
>
> 你不能使用此方法与 `dockerOrg` 或 `dockerTeam`。表达式映射仅与一个属性兼容。

#### 直接映射（Direct mapping）

如果你需要映射多个属性（`dockerRole` + `dockerTeam`），请使用此方法。

1. 对于每个 Docker 属性，选择一个唯一的 Entra 扩展属性（`extensionAttribute1`、`extensionAttribute2` 等）。
1. 在 **Edit Attribute** 视图中：
   - 将映射类型设置为 **Direct**。
   - 将 **Source attribute** 设置为你选择的扩展属性。
   - 将 **Target attribute** 设置为以下之一：
     - `dockerRole: urn:ietf:params:scim:schemas:extension:docker:2.0:User:dockerRole`
     - `dockerOrg: urn:ietf:params:scim:schemas:extension:docker:2.0:User:dockerOrg`
     - `dockerTeam: urn:ietf:params:scim:schemas:extension:docker:2.0:User:dockerTeam`
   - 将 **Apply this mapping** 设置为 **Always**。
1. 保存你的更改。

要分配值，你需要使用 Microsoft Graph API。

### 第三步：分配用户和组（Step three: Assign users and groups）

对于任一映射方法：

1. 在 SCIM 应用中，转到 **Users and Groups** > **Add user/group**。
1. 选择要配置到 Docker 的用户或组。
1. 选择 **Assign**。

如果你使用表达式映射：

1. 转到 **App registrations** > 你的 SCIM 应用 > **App Roles**。
1. 创建与 Docker 角色匹配的 App Roles。
1. 在 **Users and Groups** 下将用户或组分配到 App Roles。

如果你使用直接映射：

1. 转到 [Microsoft Graph Explorer](https://developer.microsoft.com/en-us/graph/graph-explorer) 并以租户管理员身份登录。
1. 使用 Microsoft Graph API 分配属性值。示例 PATCH 请求：

```bash
PATCH https://graph.microsoft.com/v1.0/users/{user-id}
Content-Type: application/json

{
  "extensionAttribute1": "owner",
  "extensionAttribute2": "moby",
  "extensionAttribute3": "developers"
}
```

> [!NOTE]
>
> 你必须为每个 SCIM 字段使用不同的扩展属性。



有关其他详情，请参阅你的 IdP 的文档：

- [Okta](https://help.okta.com/en-us/Content/Topics/users-groups-profiles/usgp-add-custom-user-attributes.htm)
- [Entra ID/Azure AD](https://learn.microsoft.com/en-us/azure/active-directory/app-provisioning/customize-application-attributes#provisioning-a-custom-extension-attribute-to-a-scim-compliant-application)

## 测试 SCIM 配置（Test SCIM provisioning）

完成角色映射后，你可以手动测试配置。

**Okta**



1. 在 Okta 管理门户中，转到 **Directory > People**。
1. 选择一个你已分配到 SCIM 应用的用户。
1. 选择 **Provision User**。
1. 等待几秒，然后检查 [Docker Home](https://app.docker.com) 中的 Docker **Members**（成员）。
1. 如果用户没有出现，查看 **Reports > System Log** 中的日志，并确认应用中的 SCIM 设置。

**Entra ID/Azure AD (OIDC and SAML 2.0)**



1. 在 Azure 门户中，转到 **Microsoft Entra ID** > **Enterprise Applications**，并选择你的 SCIM 应用。
1. 转到 **Provisioning** > **Provision on demand**。
1. 选择一个用户或组并选择 **Provision**。
1. 确认用户出现在 [Docker Home](https://app.docker.com) 的 Docker **Members** 中。
1. 如有需要，检查 **Provisioning logs** 中的错误。



## 禁用 SCIM（Disable SCIM）

如果 SCIM 被禁用，任何通过 SCIM 配置的用户将保留在组织中。你用户的未来变更将不再从 IdP 同步。取消用户配置
（de-provisioning）仅在手动从组织中移除用户时才可能。

要禁用 SCIM：

1. 登录 [Docker Home](https://app.docker.com)。
1. 选择 **Identity & auth**，然后 **SSO and SCIM**。
1. 在 **SSO connections** 表中，选择 **Actions** 图标。
1. 选择 **Disable SCIM**。

## 下一步（Next steps）

- 设置 [组映射](/manuals/enterprise/security/provisioning/scim/group-mapping.md)。
- [排查配置问题](/manuals/enterprise/security/provisioning/troubleshoot-provisioning.md)。

