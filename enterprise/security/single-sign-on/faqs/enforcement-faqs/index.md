# SSO 强制执行常见问题

## Docker SSO 是否支持通过命令行进行身份验证？

当强制执行 SSO 时，[系统会阻止使用密码访问 Docker CLI](/security/security-announcements/#deprecation-of-password-logins-on-cli-when-sso-enforced)。您必须改用个人访问令牌 (PAT) 进行 CLI 身份验证。

每个用户都必须创建一个 PAT 才能访问 CLI。要了解如何创建 PAT，请参阅[管理个人访问令牌](/security/access-tokens/)。在强制执行 SSO 之前已经使用过 PAT 的用户可以继续使用该 PAT。

## SSO 如何影响自动化系统和 CI/CD 管道？

在强制执行 SSO 之前，您必须[创建个人访问令牌](/security/access-tokens/)以替换自动化系统和 CI/CD 管道中的密码。

## 我能否在不立即强制执行的情况下开启 SSO？

是的，您可以在不强制执行的情况下开启 SSO。用户可以在登录界面选择使用 Docker ID（标准电子邮件和密码）或经过域验证的电子邮件地址（SSO）。

## SSO 已强制执行，但用户仍可使用用户名和密码登录。为什么会发生这种情况？

不属于您注册域但已被邀请到您组织的访客用户不会通过您的 SSO 身份提供程序登录。SSO 强制执行仅适用于属于您已验证域的用户。

## 我能否在投入生产环境之前测试 SSO 功能？

是的，您可以创建一个包含 5 个席位的 Business 订阅的测试组织。测试时，请开启 SSO 但不要强制执行，否则所有域电子邮件用户都将被强制登录到测试环境。

## 强制执行 SSO 与强制执行登录有什么区别？

这些是您可以独立使用或一起使用的独立功能：

- 强制执行 SSO 可确保用户使用 SSO 凭据而不是其 Docker ID 登录，从而实现更好的凭据管理。
- 强制登录 Docker Desktop 可确保用户始终登录到属于您组织成员的帐户，从而始终应用安全设置和订阅权益。

更多详情，请参阅[强制 Desktop 登录](/manuals/enterprise/security/enforce-sign-in/_index.md#enforcing-sign-in-versus-enforcing-single-sign-on-sso)。
