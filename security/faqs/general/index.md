# 通用安全常见问题解答

## 如何报告漏洞？

如果您在 Docker 中发现了安全漏洞，请负责任地报告至 security@docker.com，以便 Docker 能够迅速处理。

## Docker 是否会在登录失败后锁定用户？

Docker Hub 会在 5 分钟内连续 10 次登录失败后锁定用户。锁定持续时间为 5 分钟。此策略适用于 Docker Hub、Docker Desktop 和 Docker Scout 的身份验证。

## 是否支持使用 YubiKey 进行物理多因素认证 (MFA)？

您可以通过 SSO 使用身份提供商 (IdP) 配置物理多因素认证 (MFA)。请咨询您的 IdP 是否支持 YubiKey 等物理 MFA 设备。

## 如何管理会话以及会话会过期吗？

Docker 使用令牌来管理用户会话，不同会话具有不同的过期时间：

- Docker Desktop：90 天后或连续 30 天不活动后退出登录
- Docker Hub 和 Docker Home：24 小时后退出登录

Docker 还支持通过 SAML 属性使用您 IdP 的默认会话超时。更多信息，请参阅 [SSO 属性](/manuals/enterprise/security/provisioning/_index.md#sso-attributes)。

## 如何区分员工用户和承包商用户？

组织使用已验证的域名来区分用户类型。拥有非已验证域名的团队成员在组织中显示为“访客”用户。

## 活动日志保留多长时间？

Docker 活动日志保留 90 天。您有责任导出日志或设置驱动程序将日志发送到您的内部系统以延长保留时间。

## 我可以导出包含用户角色和权限的用户列表吗？

可以，使用 [导出成员](../../admin/organization/members.md#export-members) 功能导出 CSV 文件，其中包含您组织的用户及其角色和团队信息。

## Docker Desktop 如何处理身份验证信息？

Docker Desktop 使用主机操作系统的安全密钥管理来存储身份验证令牌：

- macOS：[钥匙串 (Keychain)](https://support.apple.com/guide/security/keychain-data-protection-secb0694df1a/web)
- Windows：[通过 Wincred 的安全和身份 API](https://learn.microsoft.com/en-us/windows/win32/api/wincred/)
- Linux：[Pass](https://www.passwordstore.org/)。

## 使用 SSO 但未启用 SCIM 时，如何移除不属于我 IdP 的用户？

如果未启用 SCIM，您必须手动从组织中移除用户。SCIM 可以自动移除用户，但仅适用于启用 SCIM 后添加的用户。在启用 SCIM 之前添加的用户必须手动移除。

更多信息，请参阅 [管理组织成员](/manuals/admin/organization/members.md)。

## Scout 从容器镜像收集哪些元数据？

有关 Docker Scout 存储的元数据信息，请参阅 [数据处理](/manuals/scout/deep-dive/data-handling.md)。

## 市场扩展程序如何进行安全审查？

扩展程序的安全审查已在路线图上，但目前尚未实施。扩展程序不属于 Docker 第三方风险管理计划的覆盖范围。

## 我能否阻止用户将镜像推送到 Docker Hub 私有仓库？

没有直接的设置可以禁用私有仓库。但是，[注册表访问管理](/manuals/enterprise/security/hardened-desktop/registry-access-management.md) 允许管理员通过管理控制台控制开发人员可以通过 Docker Desktop 访问哪些注册表。
