# 组织入驻




了解如何使用管理控制台或 Docker Hub 入驻您的组织。

组织入驻包括以下内容：

- 识别用户，帮助您分配订阅席位
- 邀请成员和所有者加入您的组织
- 为您的组织配置安全的身份验证和授权
- 强制要求 Docker Desktop 登录，确保遵循安全最佳实践

这些操作有助于管理员了解用户活动并强制执行安全设置。当组织成员登录后，他们还可以享受更高的拉取限制和其他权益。

## 先决条件

在开始入驻组织之前，请确保您：

- 拥有 Docker 团队或商业订阅。有关更多详情，请参阅 [Docker 订阅和功能](https://www.docker.com/pricing/)。

  > [!NOTE]
  >
  > 购买自助订阅时，屏幕上的说明会引导您创建组织。如果您通过 Docker 销售团队购买了订阅但尚未创建组织，请参阅 [创建组织](/manuals/admin/organization/orgs.md)。

- 熟悉 [管理概览](../_index.md) 中的 Docker 概念和术语。

## 使用引导式设置入驻

管理控制台提供引导式设置，帮助您入驻组织。引导式设置的步骤包含基本的入驻任务。如果您希望不通过引导式设置入驻，请参阅 [推荐的入驻步骤](/manuals/admin/organization/onboard.md#recommended-onboarding-steps)。

要使用引导式设置入驻，请导航至 [管理控制台](https://app.docker.com)，然后在左侧导航栏中选择 **引导式设置**。

引导式设置将引导您完成以下入驻步骤：

- **邀请您的团队**：邀请所有者和成员。
- **管理用户访问权限**：添加并验证域名，使用 SSO 管理用户，并强制要求 Docker Desktop 登录。
- **Docker Desktop 安全性**：配置镜像访问管理、注册表访问管理和设置管理。

## 推荐的入驻步骤

### 第一步：识别您的 Docker 用户

识别用户有助于您高效分配席位，并确保他们享受到 Docker 订阅的权益。

1. 识别您组织中的 Docker 用户。
   - 如果您的组织使用设备管理软件（如 MDM 或 Jamf），您可以使用该软件帮助识别 Docker 用户。有关详情，请参阅您的设备管理软件的文档。您可以通过检查每位用户的机器上是否安装了 Docker Desktop 来识别 Docker 用户，安装路径如下：
      - Mac：`/Applications/Docker.app`
      - Windows：`C:\Program Files\Docker\Docker`
      - Linux：`/opt/docker-desktop`
   - 如果您的组织未使用设备管理软件，或用户尚未安装 Docker Desktop，您可以对用户进行调查，以确定谁在使用 Docker Desktop。
1. 要求用户将其 Docker 账户的电子邮件地址更新为与您的组织域名关联的地址，或使用该电子邮件创建一个新账户。
   - 要更新账户的电子邮件地址，请指示用户登录 [Docker Hub](https://hub.docker.com)，并将其电子邮件地址更新为组织域名下的电子邮件地址。
   - 要创建新账户，请指示用户使用与组织域名关联的电子邮件地址 [注册](https://hub.docker.com/signup)。确保用户验证其电子邮件地址。
1. 识别与您的组织域名关联的 Docker 账户：
   - 联系您的 Docker 销售代表或 [联系销售](https://www.docker.com/pricing/contact-sales/)，获取使用您组织域名下电子邮件地址的 Docker 账户列表。

### 第二步：邀请所有者

所有者可以帮助您入驻并管理组织。

创建组织时，您是唯一的所有者。添加其他所有者是可选的。

要添加所有者，请邀请用户并将其角色分配为所有者。有关更多详情，请参阅 [邀请成员](/manuals/admin/organization/members.md) 和 [角色和权限](/manuals/enterprise/security/roles-and-permissions.md)。

### 第三步：邀请成员

将用户添加到组织后，您可以了解他们的活动并强制执行安全设置。当成员登录后，他们还可以享受更高的拉取限制和其他组织范围的权益。

要添加成员，请邀请用户并将其角色分配为成员。有关更多详情，请参阅 [邀请成员](/manuals/admin/organization/members.md) 和 [角色和权限](/manuals/enterprise/security/roles-and-permissions.md)。

### 第四步：使用 SSO 和 SCIM 管理用户访问权限

配置 SSO 和 SCIM 是可选的，仅适用于 Docker 商业订阅用户。要将 Docker 团队订阅升级为 Docker 商业订阅，请参阅 [更改订阅](/manuals/subscription/change.md)。

使用您的身份提供商 (IdP) 通过 SSO 和 SCIM 自动管理成员并将其配置到 Docker。有关更多详情，请参阅以下内容：

   - [配置 SSO](/manuals/enterprise/security/single-sign-on/configure.md)，以便用户在通过身份提供商登录 Docker 时进行身份验证并添加成员。
   - 可选。[强制执行 SSO](/manuals/enterprise/security/single-sign-on/connect.md)，确保用户在登录 Docker 时必须使用 SSO。

     > [!NOTE]
     >
     > 强制执行单点登录 (SSO) 和强制执行 Docker Desktop 登录是不同的功能。有关更多详情，请参阅 [强制执行登录与强制执行单点登录 (SSO)](/manuals/enterprise/security/enforce-sign-in/_index.md#enforcing-sign-in-versus-enforcing-single-sign-on-sso)。

   - [配置 SCIM](/manuals/enterprise/security/provisioning/scim.md)，以便通过身份提供商自动配置、添加和取消配置 Docker 成员。

### 第五步：强制要求 Docker Desktop 登录

默认情况下，组织成员可以在不登录的情况下使用 Docker Desktop。当用户不以组织成员身份登录时，他们无法享受 [组织的订阅权益](https://www.docker.com/pricing/)，并且可能绕过 [Docker 的安全功能](/manuals/enterprise/security/hardened-desktop/_index.md)。

根据您组织的 Docker 配置，有多种方式可以强制执行登录：
- [注册表键方法（仅限 Windows）](/manuals/enterprise/security/enforce-sign-in/methods.md#registry-key-method-windows-only)
- [`.plist` 方法（仅限 Mac）](/manuals/enterprise/security/enforce-sign-in/methods.md#plist-method-mac-only)
- [`registry.json` 方法（全部）](/manuals/enterprise/security/enforce-sign-in/methods.md#registryjson-method-all)

### 第六步：管理 Docker Desktop 安全性

Docker 提供以下安全功能来管理组织的安全态势：

- [镜像访问管理](/manuals/enterprise/security/hardened-desktop/image-access-management.md)：控制开发人员可以从 Docker Hub 拉取哪些类型的镜像。
- [注册表访问管理](/manuals/enterprise/security/hardened-desktop/registry-access-management.md)：定义开发人员可以访问哪些注册表。
- [设置管理](/manuals/enterprise/security/hardened-desktop/settings-management.md)：为您的用户设置并控制 Docker Desktop 设置。

## 下一步

- [管理 Docker 产品](./manage-products.md)，配置访问权限并查看使用情况。
- 配置[强化版 Docker Desktop](/desktop/hardened-desktop/)，提升组织在容器化开发方面的安全态势。
- [管理您的域](/manuals/enterprise/security/domain-management.md)，确保您域中的所有 Docker 用户都属于您的组织。

您的 Docker 订阅还提供许多其他功能。如需了解更多信息，请参阅 [Docker 订阅和功能](https://www.docker.com/pricing/)。
