# 管理 Docker 账户


您可以使用 Docker Home 管理您的 Docker 账户，包括管理和安全设置。

> [!TIP]
>
> 如果您的账户关联了强制执行单点登录 (SSO) 的组织，您可能没有权限更新账户设置。
> 请联系管理员来更新您的设置。

## 更新账户信息

账户信息在您的**账户设置**页面上可见。您可以更新以下信息：

- 全名
- 公司
- 位置
- 网站
- Gravatar 电子邮件

要使用 Gravatar 添加或更新您的头像：

1. 创建一个 [Gravatar 账户](https://gravatar.com/)。
2. 创建您的头像。
3. 将您的 Gravatar 电子邮件添加到您的 Docker 账户设置中。

您的头像在 Docker 中更新可能需要一些时间。

## 更新电子邮件地址

要更新您的电子邮件地址：

1. 登录您的 [Docker 账户](https://app.docker.com/login)。
2. 在右上角选择您的头像，然后选择**账户设置**。
3. 选择**电子邮件**。
4. 输入您的新电子邮件地址并使用您的密码确认身份。
   选择 **Verify email**（验证邮箱）。
5. 转到新的 Docker 电子邮件并复制 6 位验证码。
6. 粘贴验证码以完成邮箱更新。

您的验证会话会在 15 分钟后过期。

> [!NOTE]
>
> Docker 账户一次仅支持一个已验证的电子邮件地址，该地址用于账户通知和安全相关通信。您
> 无法向您的账户添加多个已验证的电子邮件地址。

## 更改您的密码

通过电子邮件发起密码重置：

1. 登录您的 [Docker 账户](https://app.docker.com/login)。
2. 在右上角选择您的头像，然后选择**账户设置**。
3. 选择**密码**，然后选择**重置密码**。
4. Docker 会向您发送一封包含重置密码说明的密码重置电子邮件。

## 管理双重身份验证

要更新您的双重身份验证 (2FA) 设置：

1. 登录您的 [Docker 账户](https://app.docker.com/login)。
2. 在右上角选择您的头像，然后选择**账户设置**。
3. 选择**2FA**。

更多信息，请参阅[启用双重身份验证](/manuals/security/2fa/_index.md)。

## 管理个人访问令牌

要管理个人访问令牌：

1. 登录您的 [Docker 账户](https://app.docker.com/login)。
2. 在右上角选择您的头像，然后选择**账户设置**。
3. 选择**个人访问令牌**。

更多信息，请参阅[创建和管理访问令牌](/manuals/security/access-tokens.md)。

## 管理关联账户

如果您使用 Google 或 GitHub 注册，该提供商会显示在
**关联账户**下。解除关联会移除 OAuth 连接。它
不会改变您的 Docker ID，也不允许您添加不同的登录方式。
您无法将 Google 和 GitHub 同时关联到同一个账户。

要解除关联账户：

1. 登录您的 [Docker 账户](https://app.docker.com/login)。
2. 在右上角选择您的头像，然后选择**账户设置**。
3. 选择**关联账户**。
4. 在您关联的账户上选择**解除关联**。

要完全取消关联您的 Docker 账户，您还必须从 Google 或 GitHub 取消关联 Docker。更多信息请参阅 Google 或 GitHub 的文档：

- [管理您的 Google 账户与
  第三方之间的关联](https://support.google.com/accounts/answer/13533235?hl=en)
- [审查和撤销 GitHub
  Apps 的授权](https://docs.github.com/en/apps/using-github-apps/reviewing-and-revoking-authorization-of-github-apps)

## 转换您的账户

有关将您的账户转换为组织的信息，请参阅
[将账户转换为
组织](/manuals/admin/organization/setup/convert-account.md)。

## 停用您的账户

有关停用账户的信息，请参阅
[停用 Docker 账户](/manuals/accounts/deactivate-user-account.md)。

## 后续步骤

- [Docker 账户概览](/manuals/accounts/_index.md)
- [创建 Docker 账户](/manuals/accounts/create-account.md)
- [启用双重身份验证](/manuals/security/2fa/_index.md)

