# 登录强制执行


登录强制执行将 Docker Sandboxes 限制为特定 Docker 组织成员的用户使用。管理员将一份强制执行配置部署到受管终端，`sbx login` 会在用户认证后验证其组织成员身份。如果检查失败，凭据会被立即吊销，用户无法运行沙箱。

如果没有这项强制执行，开发者可以用个人账户登录，从而绕过组织的 [治理策略](../access-controls/organization.md)。登录强制执行在终端一侧堵住了这一缺口，用户无法在此处覆盖它。

> [!NOTE]
> 登录强制执行是 Docker AI Governance 产品的一部分。
> [联系 Docker Sales](https://www.docker.com/products/ai-governance/#contact-sales)
> 了解更多。

## How it works（工作原理）

1. 管理员通过 MDM、组策略或配置管理，将一份强制执行配置部署到受管终端，并指定一个或多个允许的 Docker 组织 slug。
2. 当用户运行 `sbx login` 时，他们向 Docker 进行认证。凭据被临时保存，随后 Docker Sandboxes 调用 Docker API 验证组织成员身份。
3. 如果用户至少属于一个允许的组织，登录成功，凭据被保留。
4. 如果不属于，Docker Sandboxes 会立即吊销已保存的凭据，用户会收到一条列出所需组织的 [错误信息](#error-messages)。

无论组织成员身份如何，`sbx login` 和 `sbx logout` 始终可以运行。其他命令需要有效的已登录会话，因此在被拒绝的登录之后它们会失败，直到用户以允许的账户登录。

## Enforcement configuration（强制执行配置）

所有平台都表达相同的逻辑架构（schema）。规范的 JSON 表示形式：

```json
{
  "allowedOrgs": ["docker", "acme-corp"],
  "adminEmail": "it-security@acme-corp.com",
  "adminURL": "https://acme-corp.atlassian.net/servicedesk/it",
  "adminName": "ACME IT Security Team"
}
```

| 字段          | 类型            | 是否必填 | 说明                                                                                             |
| ------------- | --------------- | -------- | ------------------------------------------------------------------------------------------------ |
| `allowedOrgs` | 字符串列表      | 是       | Docker 组织 slug。用户必须至少是其中一个的成员。匹配不区分大小写。                                |
| `adminName`   | 字符串          | 否       | 在拒绝信息中显示的管理员或团队显示名称。                                                          |
| `adminEmail`  | 字符串          | 否       | 在拒绝信息中显示的联系邮箱。                                                                      |
| `adminURL`    | 字符串          | 否       | 在拒绝信息中显示的服务台或访问申请 URL。                                                          |

如果 `allowedOrgs` 为空或缺失，则强制执行处于非激活状态，任何已认证的用户都可以使用 Docker Sandboxes。

可选的 `adminName`、`adminEmail` 和 `adminURL` 字段为被拒绝的用户提供了解决途径。请填入你组织用于访问申请的联系方式。

## Deploy the configuration（部署配置）

使用你现有的终端管理工具部署配置。每个平台都从普通用户无法修改的原生位置读取它。

**macOS**



在 macOS 上，配置是一个受管首选项域 `com.docker.sbx`。

通过任意 MDM 解决方案（如 Jamf 或 Intune）以自定义配置档（configuration profile）形式部署它。MDM 部署的配置档优先级高于用户级首选项，只能通过将设备从 MDM 管理中移除来删除，因此用户无法覆盖它们。

以下 `.mobileconfig` 载荷设置允许的组织和管理员联系方式：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>PayloadContent</key>
  <array>
    <dict>
      <key>PayloadType</key>
      <string>com.apple.ManagedClient.preferences</string>
      <key>PayloadVersion</key>
      <integer>1</integer>
      <key>PayloadIdentifier</key>
      <string>com.docker.sbx.policy</string>
      <key>PayloadUUID</key>
      <string><!-- generate a UUID --></string>
      <key>PayloadEnabled</key>
      <true/>
      <key>PayloadDisplayName</key>
      <string>Docker Sandboxes Policy</string>
      <key>PayloadContent</key>
      <dict>
        <key>com.docker.sbx</key>
        <dict>
          <key>Forced</key>
          <array>
            <dict>
              <key>mcx_preference_settings</key>
              <dict>
                <key>allowedOrgs</key>
                <array>
                  <string>acme-corp</string>
                </array>
                <key>adminEmail</key>
                <string>it-security@acme-corp.com</string>
                <key>adminURL</key>
                <string>https://acme-corp.atlassian.net/servicedesk/it</string>
                <key>adminName</key>
                <string>ACME IT Security</string>
              </dict>
            </dict>
          </array>
        </dict>
      </dict>
    </dict>
  </array>
</dict>
</plist>
```

要在不使用 MDM 的情况下本地测试配置，写入用户首选项域：

```console
$ defaults write com.docker.sbx allowedOrgs -array "acme-corp"
$ defaults write com.docker.sbx adminEmail "it@acme.com"
```

移除测试配置：

```console
$ defaults delete com.docker.sbx
```

`defaults write` 使用的是用户首选项域，而非受管首选项域。在受管设备上，MDM 配置档具有权威性，同一域中的用户级设置会被忽略。

**Windows**



通过组策略、Intune 或任何可写入注册表值的终端管理工具部署它。

| 值名称        | 类型           | 说明                                            |
| ------------- | -------------- | ----------------------------------------------- |
| `allowedOrgs` | `REG_MULTI_SZ` | 多字符串列表，每个字符串一个组织 slug           |
| `adminName`   | `REG_SZ`       | 管理员或团队名称（可选）                        |
| `adminEmail`  | `REG_SZ`       | 联系邮箱（可选）                                |
| `adminURL`    | `REG_SZ`       | 服务台 URL（可选）                              |

要在本地测试配置，在提升权限的 PowerShell 会话中运行以下命令。使用 `New-ItemProperty` 创建带显式类型的值；`Set-ItemProperty` 不会创建新值。

```powershell
New-Item -Path "HKLM:\SOFTWARE\Policies\Docker\SBX" -Force

New-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Docker\SBX" `
  -Name "allowedOrgs" -Value @("acme-corp") -PropertyType MultiString -Force
New-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Docker\SBX" `
  -Name "adminEmail" -Value "it@acme.com" -PropertyType String -Force
```

移除配置：

```powershell
Remove-Item -Path "HKLM:\SOFTWARE\Policies\Docker\SBX" -Recurse -Force
```

**Linux**



在 Linux 上，配置是位于 `/etc/docker-sbx/config.json` 的一个 root 所有的 JSON 文件。

通过 Ansible、Puppet、Chef 或 Salt 等配置管理工具部署它。该文件必须归 root 所有并具有 `644` 权限。

```json
{
  "allowedOrgs": ["acme-corp"],
  "adminEmail": "it-security@acme-corp.com",
  "adminURL": "https://acme-corp.atlassian.net/servicedesk/it",
  "adminName": "ACME IT Security"
}
```

部署并设置所有权：

```console
$ sudo mkdir -p /etc/docker-sbx
$ sudo tee /etc/docker-sbx/config.json <<'EOF'
{"allowedOrgs": ["acme-corp"], "adminEmail": "it@acme.com"}
EOF
$ sudo chown root:root /etc/docker-sbx/config.json
$ sudo chmod 644 /etc/docker-sbx/config.json
```

移除配置：

```console
$ sudo rm -f /etc/docker-sbx/config.json
```

如果该文件是符号链接、不是普通文件、不归 root 所有，或对组或其他用户可写，Linux 加载器会以“失败即关闭”（fail closed）的方式处理。任何偏差都会被视为配置错误，`sbx login` 会被拒绝并附带描述性信息。使用上述命令部署可以通过这些检查。



## Error messages（错误信息）

当用户以非允许组织成员的账户登录时，他们会被登出并看到一条拒绝信息。只有你配置的联系字段才会出现：如果只设置了 `adminEmail`，则会省略 URL 行。

未配置管理员联系方式时：

```text
Access denied: Your administrator requires you to be logged into an account
that is a member of one of the following Docker organizations:
  - acme-corp

Sign in with an account that belongs to one of these organizations, or
contact your administrator for access.
```

配置了管理员联系方式时：

```text
Access denied: Your administrator requires you to be logged into an account
that is a member of one of the following Docker organizations:
  - acme-corp

For access, contact ACME IT Security:
  Email: it-security@acme-corp.com
  URL:   https://acme-corp.atlassian.net/servicedesk/it
```

## Related pages（相关页面）

- [组织策略](../access-controls/organization.md)：从 Docker Admin Console 集中管理沙箱的网络、文件系统和 MCP 访问控制
- [治理概览](../_index.md)：本地治理与组织治理如何协同工作
- [为 Docker Desktop 强制登录](/manuals/enterprise/security/enforce-sign-in/_index.md)：Docker Desktop 的等效控制

