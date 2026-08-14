# Onboard your organization（ onboard 你的组织）




了解如何 onboard 你的组织。

Onboarding 你的组织包括：

- 识别用户以帮助你分配订阅席位
- 邀请成员和所有者加入你的组织
- 为你的组织确保安全的身份验证和授权
- 强制 Docker Desktop 登录以确保安全最佳实践

这些操作帮助管理员获得对用户活动的可见性并执行安全设置。组织成员在登录后还会获得提升的拉取限制和其他权益。

## Prerequisites（先决条件）

在开始 onboard 你的组织之前，请确保你：

- 拥有 Docker Team 或 Business 订阅。更多详情，请参阅 [Docker subscriptions and features](https://www.docker.com/pricing?ref=Docs&refAction=DocsAdminOnboard)。

  > [!NOTE]
  >
  > 购买自助订阅时，屏幕上的说明会引导你完成创建组织的过程。如果你通过 Docker Sales 购买了订阅但尚未创建组织，请参阅 [Create an organization](/manuals/admin/organization/setup/orgs.md)。

- 熟悉 [administration overview](../../_index.md) 中的 Docker 概念和术语。

## Onboard with guided setup（通过引导式设置 onboard）

Docker Home 提供引导式设置来帮助你 onboard 你的组织。引导式设置的步骤由基本的 onboarding 任务组成。如果你想在引导式设置之外进行 onboard，请参阅 [Recommended onboarding steps](/manuals/admin/organization/setup/onboard.md#recommended-onboarding-steps)。

要使用引导式设置进行 onboard，请导航到 [Docker Home](https://app.docker.com) 并在左侧导航中选择 **Guided setup（引导式设置）**。

引导式设置会引导你完成以下 onboarding 步骤：

- **Invite your team（邀请你的团队）**：邀请所有者和成员。
- **Manage user access（管理用户访问）**：添加并验证域名、通过 SSO 管理用户，并强制 Docker Desktop 登录。
- **Docker Desktop security（Docker Desktop 安全）**：配置镜像访问管理、注册表访问管理和设置管理。

## Recommended onboarding steps（推荐的 onboarding 步骤）

### Step one: Identify your Docker users（第一步：识别你的 Docker 用户）

识别你的用户有助于你高效分配席位，并确保他们获得你的 Docker 订阅权益。

1. 识别你组织中的 Docker 用户。
   - 如果你的组织使用设备管理软件（如 MDM 或 Jamf），你可以使用设备管理软件来帮助识别 Docker 用户。详情请参阅你的设备管理软件文档。你可以通过检查每个用户的机器上是否安装了 Docker Desktop 来识别 Docker 用户，位置如下：
     - Mac：`/Applications/Docker.app`
     - Windows：`C:\Program Files\Docker\Docker`（全用户安装）或 `%LOCALAPPDATA%\Programs\DockerDesktop`（每用户安装（Beta））
     - Linux：`/opt/docker-desktop`
   - 如果你的组织不使用设备管理软件，或者你的用户尚未安装 Docker Desktop，你可以调查你的用户以识别谁在使用 Docker Desktop。
1. 要求用户将其 Docker 账户的电子邮件地址更新为与你组织域名关联的地址，或使用该电子邮件创建新账户。
   - 要更新账户的电子邮件地址，请指示你的用户登录 [Docker Hub](https://hub.docker.com)，并将电子邮件地址更新为其所在组织域名下的电子邮件地址。
   - 要创建新账户，请指示你的用户使用其所在组织域名下的电子邮件地址[注册](https://hub.docker.com/signup)。确保你的用户验证其电子邮件地址。
1. 识别与你组织域名关联的 Docker 账户：
   - 向你的 Docker 销售代表或 <a href="https://www.docker.com/pricing/contact-sales/" id="dkr_docs_cs_org_onboarding" class="link" rel="noopener">contact sales（联系销售）</a> 索取使用你组织域名中电子邮件地址的 Docker 账户列表。

### Step two: Invite owners（第二步：邀请所有者）

所有者可以帮助你 onboard 和管理你的组织。

当你创建组织时，你是唯一的所有者。添加额外的所有者是可选的。

要添加所有者，请邀请用户并为其分配所有者角色。更多详情，请参阅 [Invite members](/manuals/admin/organization/manage/members.md) 和 [Roles and permissions](/manuals/enterprise/security/roles-and-permissions.md)。

### Step three: Invite members（第三步：邀请成员）

当你将用户添加到组织时，你可以获得对其活动的可见性，并可以执行安全设置。你的成员在登录后还会获得提升的拉取限制和其他组织范围的权益。

要添加成员，请邀请用户并为其分配成员角色。更多详情，请参阅 [Invite members](/manuals/admin/organization/manage/members.md) 和 [Roles and permissions](/manuals/enterprise/security/roles-and-permissions.md)。

### Step four: Manage user access with SSO and SCIM（第四步：通过 SSO 和 SCIM 管理用户访问）

配置 SSO 和 SCIM 是可选的，仅对 Docker Business 订阅者可用。要将 Docker Team 订阅升级为 Docker Business 订阅，请参阅 [Upgrade a plan](/manuals/subscription/manage.md#upgrade-plans)。

使用你的身份提供商（IdP）通过 SSO 和 SCIM 管理成员并自动将其配置到 Docker。更多详情请参阅以下内容：

- [Configure SSO](/manuals/enterprise/security/single-sign-on/connect.md) 以在用户通过你的身份提供商登录 Docker 时对其身份验证并添加成员。
- 可选。[Enforce SSO](/manuals/enterprise/security/single-sign-on/connect.md) 以确保用户登录 Docker 时必须使用 SSO。

  > [!NOTE]
  >
  > 强制单点登录（SSO）和强制 Docker Desktop 登录是不同的功能。更多详情，请参阅 [Enforcing sign-in versus enforcing single sign-on (SSO)](/manuals/enterprise/security/enforce-sign-in/_index.md#enforcing-sign-in-versus-enforcing-single-sign-on-sso)。

- [Configure SCIM](/manuals/enterprise/security/provisioning/scim/_index.md) 以通过你的身份提供商自动配置、添加和取消配置成员到 Docker。

### Step five: Enforce sign-in for Docker Desktop（第五步：强制 Docker Desktop 登录）

默认情况下，你组织的成员可以在不登录的情况下使用 Docker Desktop。当用户不以你组织成员的身份登录时，他们无法获得[组织订阅的权益](https://www.docker.com/pricing?ref=Docs&refAction=DocsAdminOnboard)，并且可以规避 [Docker 的安全功能](/manuals/enterprise/security/hardened-desktop/_index.md)。

根据你的组织 Docker 配置，有多种方式可以强制登录：

- [Registry key method (Windows only)](/manuals/enterprise/security/enforce-sign-in/methods.md#registry-key-method-windows-only)（注册表项方法（仅 Windows））
- [`.plist` method (Mac only)](/manuals/enterprise/security/enforce-sign-in/methods.md#plist-method-mac-only)（`.plist` 方法（仅 Mac））
- [`registry.json` method (All)](/manuals/enterprise/security/enforce-sign-in/methods.md#registryjson-method-all)（`registry.json` 方法（全部））

### Step six: Manage Docker Desktop security（第六步：管理 Docker Desktop 安全）

Docker 提供以下安全功能来管理你组织的安全态势：

- [Image Access Management](/manuals/enterprise/security/hardened-desktop/image-access-management.md)：控制你的开发人员可以从 Docker Hub 拉取哪些类型的镜像。
- [Registry Access Management](/manuals/enterprise/security/hardened-desktop/registry-access-management.md)：定义你的开发人员可以访问哪些注册表。
- [Settings management](/manuals/enterprise/security/hardened-desktop/settings-management.md)：为你用户设置和控制 Docker Desktop 设置。

## Next steps（后续步骤）

- [Manage Docker products](../manage/manage-products.md) 以配置访问并查看使用情况。
- 配置 [Hardened Docker Desktop](/manuals/enterprise/security/hardened-desktop/_index.md) 以改善你组织面向容器化开发的安全态势。
- [Manage your domains](/manuals/enterprise/security/domain-management.md) 以确保你域名中的所有 Docker 用户都是你组织的一部分。

你的 Docker 订阅提供了更多附加功能。要了解更多信息，请参阅 [Docker subscriptions and features](https://www.docker.com/pricing?ref=Docs&refAction=DocsAdminOnboard)。

