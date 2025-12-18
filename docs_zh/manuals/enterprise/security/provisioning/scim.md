---
title: SCIM 配置
linkTitle: SCIM
description: 了解跨域身份管理系统 (SCIM) 的工作原理及如何设置。
keywords: SCIM, SSO, 用户配置, 用户取消配置, 角色映射, 分配用户
aliases:
  - /security/for-admins/scim/
  - /docker-hub/scim/
  - /security/for-admins/provisioning/scim/
weight: 20
---

{{< summary-bar feature_name="SSO" >}}

使用跨域身份管理系统 (SCIM) 自动管理 Docker 组织中的用户。SCIM 自动配置和取消配置用户、同步团队成员关系，并使您的 Docker 组织与身份提供商保持同步。

本文介绍如何使用 SCIM 自动配置和取消配置 Docker 用户。

## 前置条件

开始之前，您必须具备：

- 已为组织配置 SSO
- 拥有 Docker Home 和身份提供商的管理员访问权限

## SCIM 工作原理

SCIM 通过您的身份提供商自动配置和取消配置 Docker 用户。启用 SCIM 后，任何在身份提供商中被分配到 Docker 应用程序的用户都会自动被配置并添加到您的 Docker 组织中。当用户从身份提供商的 Docker 应用程序中移除时，SCIM 会停用并将其从 Docker 组织中移除。

除了配置和移除外，SCIM 还同步身份提供商中进行的个人资料更新（如姓名更改）。您可以将 SCIM 与 Docker 默认的即时 (JIT) 配置一起使用，或在禁用 JIT 的情况下单独使用 SCIM。

SCIM 自动化以下操作：

- 创建用户
- 更新用户个人资料
- 移除和停用用户
- 重新激活用户
- 组映射

> [!NOTE]
>
> SCIM 仅管理在启用 SCIM 后通过身份提供商配置的用户。它无法移除在 SCIM 设置之前手动添加到 Docker 组织的用户。
>
> 要移除这些用户，需手动从 Docker 组织中删除。更多信息，请参见
> [管理组织成员](/manuals/admin/organization/members.md)。

## 支持的属性

SCIM 使用属性（姓名、电子邮件等）在身份提供商和 Docker 之间同步用户信息。在身份提供商中正确映射这些属性可确保用户配置顺利进行，并防止在使用单点登录时出现重复用户账户等问题。

Docker 支持以下 SCIM 属性：

| 属性              | 描述                                                                              |
| :---------------- | :-------------------------------------------------------------------------------- |
| `userName`        | 用户的主要电子邮件地址，用作唯一标识符                                          |
| `name.givenName`  | 用户的名字                                                                        |
| `name.familyName` | 用户的姓氏                                                                        |
| `active`          | 指示用户是否启用或禁用，设置为 "false" 以取消配置用户                             |

有关支持的属性和 SCIM 的更多详细信息，请参见
[Docker Hub API SCIM 参考](/reference/api/hub/latest/#tag/scim)。

> [!IMPORTANT]
>
> 默认情况下，Docker 对 SSO 使用即时 (JIT) 配置。如果启用了 SCIM，JIT 值仍然优先，并会覆盖 SCIM 设置的属性值。为避免冲突，请确保您的 JIT 属性值与 SCIM 值匹配。
>
> 或者，您可以禁用 JIT 配置，仅依赖 SCIM。详细信息，请参见 [即时配置](just-in-time.md)。

## 在 Docker 中启用 SCIM

要启用 SCIM：

1. 登录到 [Docker Home](https://app.docker.com)。
1. 选择 **Admin Console**，然后选择 **SSO and SCIM**。
1. 在 **SSO connections** 表中，选择连接的 **Actions** 图标，然后选择 **Setup SCIM**。
1. 复制 **SCIM Base URL** 和 **API Token**，并将其值粘贴到您的身份提供商中。

## 在身份提供商中启用 SCIM

您的身份提供商的用户界面可能与以下步骤略有不同。您可以参考身份提供商的文档进行验证。有关更多详细信息，请参见身份提供商的文档：

- [Okta](https://help.okta.com/en-us/Content/Topics/Apps/Apps_App_Integration_Wizard_SCIM.htm)
- [Entra ID/Azure AD SAML 2.0](https://learn.microsoft.com/en-us/azure/active-directory/app-provisioning/user-provisioning)

> [!NOTE]
>
> Microsoft 目前不支持在 Entra ID 中的同一非库应用程序中使用 SCIM 和 OIDC。本文提供了一种使用单独的非库应用程序进行 SCIM 配置的验证解决方案。虽然 Microsoft 未正式记录此设置，但它在实践中被广泛使用并得到支持。

{{< tabs >}}
{{< tab name="Okta" >}}

### 步骤一：启用 SCIM

1. 登录到 Okta 并选择 **Admin** 以打开管理门户。
1. 打开您在配置 SSO 连接时创建的应用程序。
1. 在应用程序页面上，选择 **General** 选项卡，然后选择 **Edit App Settings**。
1. 启用 SCIM 配置，然后选择 **Save**。
1. 导航到 **Provisioning**，然后选择 **Edit SCIM Connection**。
1. 要在 Okta 中配置 SCIM，请使用以下值和设置配置连接：
   - SCIM Base URL：SCIM 连接器基础 URL（从 Docker Home 复制）
   - 用户的唯一标识符字段：`email`
   - 支持的配置操作：**Push New Users** 和 **Push Profile Updates**
   - 身份验证模式：HTTP Header
   - SCIM Bearer Token：HTTP Header Authorization Bearer Token（从 Docker Home 复制）
1. 选择 **Test Connector Configuration**。
1. 查看测试结果并选择 **Save**。

### 步骤二：启用同步

1. 在 Okta 中，选择 **Provisioning**。
1. 选择 **To App**，然后选择 **Edit**。
1. 启用 **Create Users**、**Update User Attributes** 和 **Deactivate Users**。
1. 选择 **Save**。
1. 移除不必要的映射。必要的映射包括：
   - Username
   - Given name
   - Family name
   - Email

接下来，[设置角色映射](#set-up-role-mapping)。

{{< /tab >}}
{{< tab name="Entra ID (OIDC)" >}}

Microsoft 不支持在同一非库应用程序中使用 SCIM 和 OIDC。您必须在 Entra ID 中为 SCIM 配置创建第二个非库应用程序。

### 步骤一：创建单独的 SCIM 应用

1. 在 Azure 门户中，转到 **Microsoft Entra ID** > **Enterprise Applications** > **New application**。
1. 选择 **Create your own application**。
1. 命名您的应用程序并选择
   **Integrate any other application you don't find in the gallery**。
1. 选择 **Create**。

### 步骤二：配置 SCIM 配置

1. 在您的新 SCIM 应用程序中，转到 **Provisioning** > **Get started**。
1. 将 **Provisioning Mode** 设置为 **Automatic**。
1. 在 **Admin Credentials** 下：
   - **Tenant URL**：粘贴来自 Docker Home 的 **SCIM Base URL**。
   - **Secret Token**：粘贴来自 Docker Home 的 **SCIM API token**。
1. 选择 **Test Connection** 进行验证。
1. 选择 **Save** 以存储凭据。

接下来，[设置角色映射](#set-up-role-mapping)。

{{< /tab >}}
{{< tab name="Entra ID (SAML 2.0)" >}}

1. 在 Azure 门户中，转到 **Microsoft Entra ID** > **Enterprise Applications**，并选择您的 Docker SAML 应用。
1. 选择 **Provisioning** > **Get started**。
1. 将 **Provisioning Mode** 设置为 **Automatic**。
1. 在 **Admin Credentials** 下：
   - **Tenant URL**：粘贴来自 Docker Home 的 **SCIM Base URL**。
   - **Secret Token**：粘贴来自 Docker Home 的 **SCIM API token**。
1. 选择 **Test Connection** 进行验证。
1. 选择 **Save** 以存储凭据。

接下来，[设置角色映射](#set-up-role-mapping)。

{{< /tab >}}
{{< /tabs >}}

## 设置角色映射

您可以通过在身份提供商中添加可选的 SCIM 属性来为用户分配 [Docker 角色](../roles-and-permissions.md)。这些属性会覆盖 SSO 配置中设置的默认角色和团队值。

> [!NOTE]
>
> 角色映射支持 SCIM 和即时 (JIT) 配置。对于 JIT，角色映射仅在用户首次配置时应用。

下表列出了支持的可选用户级属性：

| 属性       | 可能的值                      | 说明                                                                                                                                                                                                                                                            |
| ---------- | ----------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `dockerRole` | `member`、`editor` 或 `owner` | 如果未设置，用户默认为 `member` 角色。设置此属性会覆盖默认值。<br><br>角色定义，请参见 [角色和权限](../roles-and-permissions.md)。                                                                         |
| `dockerOrg`  | Docker `organizationName`（例如 `moby`） | 覆盖 SSO 连接中配置的默认组织。<br><br>如果未设置，用户将被配置到默认组织。如果同时设置了 `dockerOrg` 和 `dockerTeam`，用户将被配置到指定组织的团队中。   |
| `dockerTeam` | Docker `teamName`（例如 `developers`）   | 将用户配置到默认或指定组织中的指定团队。如果团队不存在，将自动创建。<br><br>您仍然可以使用 [组映射](group-mapping.md) 将用户分配到跨组织的多个团队。   |

这些属性使用的外部命名空间为：`urn:ietf:params:scim:schemas:extension:docker:2.0:User`。
在身份提供商中为 Docker 创建自定义 SCIM 属性时需要此值。

{{< tabs >}}
{{< tab name="Okta" >}}

### 步骤一：在 Okta 中设置角色映射

1. 首先设置 [SSO](../single-sign-on/configure/_index.md) 和 SCIM。
1. 在 Okta 管理门户中，转到 **Directory**，选择 **Profile Editor**，然后选择 **User (Default)**。
1. 选择 **Add Attribute** 并配置要添加的角色、组织或团队的值。确切的命名不是必需的。
1. 返回 **Profile Editor** 并选择您的应用程序。
1. 选择 **Add Attribute** 并输入所需的值。外部名称和外部命名空间必须准确。
   - 组织/团队/角色映射的外部名称值分别为 `dockerOrg`、`dockerTeam` 和 `dockerRole`，如上表所列。
   - 所有属性的外部命名空间相同：
     `urn:ietf:params:scim:schemas:extension:docker:2.0:User`。
1. 创建属性后，导航到页面顶部并选择 **Mappings**，然后选择 **Okta User to YOUR APP**。
1. 转到新创建的属性，将变量名映射到外部名称，然后选择 **Save Mappings**。如果您使用 JIT 配置，请继续以下步骤。
1. 导航到 **Applications** 并选择 **YOUR APP**。
1. 选择 **General**，然后选择 **SAML Settings**，并选择 **Edit**。
1. 选择 **Step 2** 并配置从用户属性到 Docker 变量的映射。

### 步骤二：按用户分配角色

1. 在 Okta 管理门户中，选择 **Directory**，然后选择 **People**。
1. 选择 **Profile**，然后选择 **Edit**。
1. 选择 **Attributes** 并将属性更新为所需的值。

### 步骤三：按组分配角色

1. 在 Okta 管理门户中，选择 **Directory**，然后选择 **People**。
1. 选择 **YOUR GROUP**，然后选择 **Applications**。
1. 打开 **YOUR APPLICATION** 并选择 **Edit** 图标。
1. 将属性更新为所需的值。

如果用户尚未设置属性，添加到组中的用户将在配置时继承这些属性。

{{< /tab >}}
{{< tab name="Entra ID/Azure AD (SAML 2.0 和 OIDC)" >}}

### 步骤一：配置属性映射

1. 完成 [SCIM 配置设置](#enable-scim-in-docker)。
1. 在 Azure 门户中，打开 **Microsoft Entra ID** > **Enterprise Applications**，并选择您的 SCIM 应用程序。
1. 转到 **Provisioning** > **Mappings** > **Provision Azure Active Directory Users**。
1. 添加或更新以下映射：
   - `userPrincipalName` -> `userName`
   - `mail` -> `emails.value`
   - 可选。使用以下 [映射方法](#step-two-choose-a-role-mapping-method) 之一映射 `dockerRole`、`dockerOrg` 或 `dockerTeam`。
1. 移除不受支持的属性以防止同步错误。
1. 可选。转到 **Mappings** > **Provision Azure Active Directory Groups**：
   - 如果组配置导致错误，将 **Enabled** 设置为 **No**。
   - 如果启用，请仔细测试组映射。
1. 选择 **Save** 以应用映射。

### 步骤二：选择角色映射方法

您可以使用以下方法之一映射 `dockerRole`、`dockerOrg` 或 `dockerTeam`：

#### 表达式映射

如果您只需要分配像 `member`、`editor` 或 `owner` 这样的 Docker 角色，请使用此方法。

1. 在 **Edit Attribute** 视图中，将映射类型设置为 **Expression**。
1. 在 **Expression** 字段中：
   1. 如果您的应用角色与 Docker 角色完全匹配，使用：
      SingleAppRoleAssignment([appRoleAssignments])
   1. 如果不匹配，使用 switch 表达式：`Switch(SingleAppRoleAssignment([appRoleAssignments]), "My Corp Admins", "owner", "My Corp Editors", "editor", "My Corp Users", "member")`
1. 设置：
   - **Target attribute**: `urn:ietf:params:scim:schemas:extension:docker:2.0:User:dockerRole`
   - **Match objects using this attribute**: No
   - **Apply this mapping**: Always
1. 保存更改。

> [!WARNING]
>
> 您不能使用此方法使用 `dockerOrg` 或 `dockerTeam`。表达式映射仅与一个属性兼容。

#### 直接映射

如果您需要映射多个属性（`dockerRole` + `dockerTeam`），请使用此方法。

1. 为每个 Docker 属性，选择一个唯一的 Entra 扩展属性（`extensionAttribute1`、`extensionAttribute2` 等）。
1. 在 **Edit Attribute** 视图中：
   - 将映射类型设置为 **Direct**。
   - 将 **Source attribute** 设置为您选择的扩展属性。
   - 将 **Target attribute** 设置为以下之一：
     - `dockerRole: urn:ietf:params:scim:schemas:extension:docker:2.0:User:dockerRole`
     - `dockerOrg: urn:ietf:params:scim:schemas:extension:docker:2.0:User:dockerOrg`
     - `dockerTeam: urn:ietf:params:scim:schemas:extension:docker:2.0:User:dockerTeam`
   - 将 **Apply this mapping** 设置为 **Always**。
1. 保存更改。

要分配值，您需要使用 Microsoft Graph API。

### 步骤三：分配用户和组

对于任一映射方法：

1. 在 SCIM 应用中，转到 **Users and Groups** > **Add user/group**。
1. 选择要配置到 Docker 的用户或组。
1. 选择 **Assign**。

如果您使用表达式映射：

1. 转到 [应用注册] > 您的 SCIM 应用 > **App Roles**。
1. 创建与 Docker 角色匹配的应用角色。
1. 在 **Users and Groups** 下为用户或组分配应用角色。

如果您使用直接映射：

1. 转到 [Microsoft Graph Explorer](https://developer.microsoft.com/en-us/graph/graph-explorer)
   并以租户管理员身份登录。
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
> 您必须为每个 SCIM 字段使用不同的扩展属性。

{{< /tab >}}
{{< /tabs >}}

请参阅身份提供商的文档以获取更多详细信息：

- [Okta](https://help.okta.com/en-us/Content/Topics/users-groups-profiles/usgp-add-custom-user-attributes.htm)
- [Entra ID/Azure AD](https://learn.microsoft.com/en-us/azure/active-directory/app-provisioning/customize-application-attributes#provisioning-a-custom-extension-attribute-to-a-scim-compliant-application)

## 测试 SCIM 配置

完成角色映射后，您可以手动测试配置。

{{< tabs >}}
{{< tab name="Okta" >}}

1. 在 Okta 管理门户中，转到 **Directory > People**。
1. 选择您已分配给 SCIM 应用程序的用户。
1. 选择 **Provision User**。
1. 等待几秒钟，然后在 Docker
   [Admin Console](https://app.docker.com/admin) 的 **Members** 下检查。
1. 如果用户未出现，请查看 **Reports > System Log** 中的日志并确认应用中的 SC