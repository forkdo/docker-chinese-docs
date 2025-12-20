# SSO 用户管理常见问题解答

## 我需要手动将用户添加到我的组织吗？

不需要，您无需手动将用户添加到您的组织。只需确保您的身份提供商 (IdP) 中存在用户帐户。当用户使用其域电子邮件地址登录 Docker 时，他们会在成功通过身份验证后自动添加到组织中。

## 用户可以使用不同的电子邮件地址通过 SSO 进行身份验证吗？

所有用户必须使用 SSO 设置期间指定的电子邮件域进行身份验证。如果用户的电子邮件地址与已验证的域不匹配，并且 SSO 未强制执行，则他们可以使用用户名和密码作为访客登录，但前提是他们已被邀请。

## 用户如何知道他们正在被添加到 Docker 组织？

当 SSO 开启时，用户下次登录 Docker Hub 或 Docker Desktop 时，系统会提示他们通过 SSO 进行身份验证。系统会检测他们的域电子邮件，并提示他们使用 SSO 凭据登录。

对于 CLI 访问，用户必须使用个人访问令牌进行身份验证。

## 我可以将现有用户从非 SSO 帐户转换为 SSO 帐户吗？

可以，您可以将现有用户转换为 SSO 帐户。请确保用户具备以下条件：

- 公司域电子邮件地址，并且在您的 IdP 中拥有帐户
- Docker Desktop 版本 4.4.2 或更高版本
- 已创建个人访问令牌，以替换 CLI 访问的密码
- 已更新 CI/CD 管道，以使用 PAT 而不是密码

有关详细说明，请参阅[配置单点登录](/manuals/enterprise/security/single-sign-on/configure.md)。

## Docker SSO 是否与 IdP 完全同步？

Docker SSO 默认提供即时 (JIT) 配置。用户在通过 SSO 进行身份验证时即被配置。如果用户离开组织，管理员必须手动从组织中[删除该用户](/manuals/admin/organization/members.md#remove-a-member-or-invitee)。

[SCIM](/manuals/enterprise/security/provisioning/scim.md) 提供与用户和组的完全同步。使用 SCIM 时，建议的配置是关闭 JIT，以便所有自动配置都由 SCIM 处理。

此外，您可以使用 [Docker Hub API](/reference/api/hub/latest/) 来完成此过程。

## 关闭即时配置如何影响用户登录？

当 JIT 关闭时（在管理控制台中使用 SCIM 时可用），用户必须是组织成员或拥有待处理的邀请才能访问 Docker。不符合这些条件的用户会收到“访问被拒绝”错误，需要管理员邀请。

请参阅[禁用 JIT 配置时的 SSO 身份验证](/manuals/enterprise/security/provisioning/just-in-time.md#sso-authentication-with-jit-provisioning-disabled)。

## 有人可以在没有邀请的情况下加入组织吗？

没有 SSO 的情况下不行。加入组织需要组织所有者的邀请。当强制执行 SSO 时，拥有已验证域电子邮件的用户可以在登录时自动加入组织。

## 当 SCIM 开启时，现有许可用户会发生什么情况？

开启 SCIM 不会立即删除或修改现有许可用户。他们保留当前的访问权限和角色，但在 SCIM 激活后，您需要通过您的 IdP 来管理他们。如果稍后关闭 SCIM，以前由 SCIM 管理的用户将保留在 Docker 中，但不再根据您的 IdP 自动更新。

## 用户信息在 Docker Hub 中是否可见？

所有 Docker 帐户都与其命名空间相关联的公共配置文件。如果您不希望用户信息（如全名）可见，请从您的 SSO 和 SCIM 映射中删除这些属性，或使用不同的标识符替换用户的全名。
