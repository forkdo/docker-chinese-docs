# 配置登录强制执行




您可以使用多种方法强制执行 Docker Desktop 的登录。请根据您组织的基础设施和安全要求选择最适合的方法。

## 选择您的方法

| 方法 | 平台 |
|:-------|:---------|
| 注册表项 | 仅限 Windows |
| 配置配置文件 | 仅限 Mac |
| `plist` 文件 | 仅限 Mac |
| `registry.json` | 所有平台 |

> [!TIP]
>
> 对于 Mac，配置配置文件提供最高的安全性，因为它们受到 Apple 系统完整性保护 (SIP) 的保护。

## Windows：注册表项方法

**手动设置**



手动配置注册表项方法：

1. 创建注册表项：

   ```console
   $ HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Docker\Docker Desktop
   ```
1. 创建一个多字符串值名称 `allowedOrgs`。
1. 使用您的组织名称作为字符串数据。您可以添加多个组织：
   - 仅使用小写字母
   - 每个组织单独一行
   - 不要使用空格或逗号作为分隔符
1. 重启 Docker Desktop。
1. 验证 Docker Desktop 中是否出现 **Sign in required!** 提示。

**组策略部署**



使用组策略在您的组织中部署注册表项：

1. 创建具有以下结构的注册表脚本：
   - 路径：`HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Docker\Docker Desktop`
   - 值名称：`allowedOrgs`（多字符串）
   - 值数据：您的组织名称，每行一个，仅使用小写字母
1. 在组策略管理中，创建或编辑一个 GPO。
1. 导航到 **计算机配置** > **首选项** > **Windows 设置** > **注册表**。
1. 右键单击 **注册表** > **新建** > **注册表项**。
1. 配置注册表项：
   - 操作：**更新**
   - 路径：`HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Docker\Docker Desktop`
   - 值名称：`allowedOrgs`
   - 值数据：您的组织名称
1. 将 GPO 链接到目标组织单位。
1. 使用 `gpupdate/force` 在小组中进行测试。
1. 验证后在整个组织范围内部署。



## Mac：配置配置文件方法（推荐）

配置配置文件为 Mac 提供最安全的强制执行方法，因为它们受到 Apple 系统完整性保护的保护。

载荷是一个键值对的字典。Docker Desktop 支持以下键：

- `allowedOrgs`：在一个字符串中设置组织列表，每个组织仅使用小写字母，并以分号分隔。

- `overrideProxyHTTP`：设置必须用于传出 HTTP 请求的 HTTP 代理 URL。
- `overrideProxyHTTPS`：设置必须用于传出 HTTPS 请求的 HTTP 代理 URL。
- `overrideProxyExclude`：绕过指定主机和域名的代理设置。使用逗号分隔的列表。
- `overrideProxyPAC`：设置 PAC 文件所在的文件路径。它优先于所选代理上的远程 PAC 文件。
- `overrideProxyEmbeddedPAC`：设置内存中 PAC 文件的内容。它优先于 `overrideProxyPAC`。

通过配置配置文件覆盖至少一个代理设置将自动锁定这些设置，因为它们由 Mac 管理。

1. 创建一个名为 `docker.mobileconfig` 的文件，并包含以下内容：
   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
   <plist version="1.0">
   <dict>
      <key>PayloadContent</key>
      <array>
         <dict>
            <key>PayloadType</key>
            <string>com.docker.config</string>
            <key>PayloadVersion</key>
            <integer>1</integer>
            <key>PayloadIdentifier</key>
            <string>com.docker.config</string>
            <key>PayloadUUID</key>
            <string>eed295b0-a650-40b0-9dda-90efb12be3c7</string>
            <key>PayloadDisplayName</key>
            <string>Docker Desktop Configuration</string>
            <key>PayloadDescription</key>
            <string>Configuration profile to manage Docker Desktop settings.</string>
            <key>PayloadOrganization</key>
            <string>Your company name</string>
            <key>allowedOrgs</key>
            <string>first_org;second_org</string>
            <key>overrideProxyHTTP</key>
            <string>http://company.proxy:port</string>
            <key>overrideProxyHTTPS</key>
            <string>https://company.proxy:port</string>
         </dict>
      </array>
      <key>PayloadType</key>
      <string>Configuration</string>
      <key>PayloadVersion</key>
      <integer>1</integer>
      <key>PayloadIdentifier</key>
      <string>com.yourcompany.docker.config</string>
      <key>PayloadUUID</key>
      <string>0deedb64-7dc9-46e5-b6bf-69d64a9561ce</string>
      <key>PayloadDisplayName</key>
      <string>Docker Desktop Config Profile</string>
      <key>PayloadDescription</key>
      <string>Config profile to enforce Docker Desktop settings for allowed organizations.</string>
      <key>PayloadOrganization</key>
      <string>Your company name</string>
   </dict>
   </plist>
   ```
1. 替换占位符：
   - 将 `com.yourcompany.docker.config` 更改为您公司的标识符
   - 将 `Your company name` 替换为您的组织名称，确保全部为小写
   - 将 `PayloadUUID` 替换为随机生成的 UUID
   - 使用您的组织名称（用分号分隔）更新 `allowedOrgs` 值
   - 将 `company.proxy:port` 替换为 http/https 代理服务器主机（或 IP 地址）和端口
1. 使用您的 MDM 解决方案部署配置文件。
1. 验证配置文件是否出现在 **系统设置** > **通用** > **设备管理** 下的 **设备（受管理）** 中。确保配置文件以正确的名称和设置列出。

一些 MDM 解决方案允许您将载荷指定为键值设置的纯字典，而无需完整的 `.mobileconfig` 包装器：

```xml
<dict>
   <key>allowedOrgs</key>
   <string>first_org;second_org</string>
   <key>overrideProxyHTTP</key>
   <string>http://company.proxy:port</string>
   <key>overrideProxyHTTPS</key>
   <string>https://company.proxy:port</string>
</dict>
```

## Mac：plist 文件方法

**手动创建**



1. 创建文件 `/Library/Application Support/com.docker.docker/desktop.plist`。
1. 添加此内容，将 `myorg1` 和 `myorg2` 替换为您的组织名称，并确保它们仅使用小写字母：
   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
   <plist version="1.0">
     <dict>
	     <key>allowedOrgs</key>
	     <array>
             <string>myorg1</string>
             <string>myorg2</string>
         </array>
     </dict>
   </plist>
   ```
1. 设置文件权限以防止非管理员用户编辑。
1. 重启 Docker Desktop。
1. 验证 Docker Desktop 中是否出现 `Sign in required!` 提示。

**Shell 脚本部署**



创建并部署一个用于组织范围分发的脚本：

```bash
#!/bin/bash

# 如果目录不存在则创建目录
sudo mkdir -p "/Library/Application Support/com.docker.docker"

# 写入 plist 文件
sudo defaults write "/Library/Application Support/com.docker.docker/desktop.plist" allowedOrgs -array "myorg1" "myorg2"

# 设置适当的权限
sudo chmod 644 "/Library/Application Support/com.docker.docker/desktop.plist"
sudo chown root:admin "/Library/Application Support/com.docker.docker/desktop.plist"
```

使用 SSH、远程支持工具或您首选的部署方法部署此脚本。



## 所有平台：registry.json 方法

registry.json 方法适用于所有平台，并提供灵活的部署选项。

### 文件位置

在适当的位置创建 `registry.json` 文件（UTF-8 无 BOM）：

| 平台 | 位置 |
| --- | --- |
| Windows | `/ProgramData/DockerDesktop/registry.json` |
| Mac | `/Library/Application Support/com.docker.docker/registry.json` |
| Linux | `/usr/share/docker-desktop/registry/registry.json` |

### 基本设置

**手动创建**



1. 确保用户是您 Docker 组织的成员。
1. 在您平台的适当位置创建 `registry.json` 文件。
1. 添加此内容，将组织名称替换为您自己的，并确保它们仅使用小写字母：
      ```json
      {
         "allowedOrgs": ["myorg1", "myorg2"]
      }
      ```
1. 设置文件权限以防止用户编辑。
1. 重启 Docker Desktop。
1. 验证 Docker Desktop 中是否出现 `Sign in required!` 提示。

> [!TIP]
>
> 如果用户在强制执行登录后启动 Docker Desktop 有问题，
> 他们可能需要更新到最新版本。

**命令行设置**



#### Windows（以管理员身份运行 PowerShell）

```shell
Set-Content /ProgramData/DockerDesktop/registry.json '{"allowedOrgs":["myorg1","myorg2"]}'
```

#### Mac

```console
sudo mkdir -p "/Library/Application Support/com.docker.docker"
echo '{"allowedOrgs":["myorg1","myorg2"]}' | sudo tee "/Library/Application Support/com.docker.docker/registry.json"
```

#### Linux

```console
sudo mkdir -p /usr/share/docker-desktop/registry
echo '{"allowedOrgs":["myorg1","myorg2"]}' | sudo tee /usr/share/docker-desktop/registry/registry.json
```

**安装时设置**



在 Docker Desktop 安装期间创建 registry.json 文件：

#### Windows

```shell
# PowerShell
Start-Process '.\Docker Desktop Installer.exe' -Wait 'install --allowed-org=myorg'

# 命令提示符
"Docker Desktop Installer.exe" install --allowed-org=myorg1
```

> [!NOTE]
>
> `--allowed-org` 标志只接受一个组织。要在 Mac 上为多个组织强制登录，请在安装后配置 `registry.json` 文件。

#### Mac

```console
sudo hdiutil attach Docker.dmg
sudo /Volumes/Docker/Docker.app/Contents/MacOS/install --allowed-org=myorg
sudo hdiutil detach /Volumes/Docker
```

> [!NOTE]
>
> `--allowed-org` 标志只接受一个组织。要在 Mac 上为多个组织强制登录，请在安装后配置 `registry.json` 文件。



## 方法优先级

当同一系统上存在多种配置方法时，Docker Desktop 使用以下优先级顺序：

1. 注册表项（仅限 Windows）
1. 配置配置文件（仅限 Mac）
1. plist 文件（仅限 Mac）
1. registry.json 文件

## 故障排除登录强制执行

如果登录强制执行不起作用：

- 验证文件位置和权限
- 检查组织名称是否使用小写字母
- 重启 Docker Desktop 或重新启动系统
- 确认用户是指定组织的成员
- 将 Docker Desktop 更新到最新版本

