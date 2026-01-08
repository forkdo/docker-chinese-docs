---
description: 如何配置和使用 Docker Extensions 的私有市场
keywords: Docker Extensions, Docker Desktop, Linux, Mac, Windows, Marketplace, private, security, admin
title: 为扩展配置私有市场
tags:
- admin
linkTitle: 配置私有市场
weight: 30
aliases:
- /desktop/extensions/private-marketplace/
---

{{< summary-bar feature_name="Private marketplace" >}}

了解如何为 Docker Desktop 用户配置和设置带有精选扩展列表的私有市场。

Docker Extensions 的私有市场专为那些不授予开发人员机器 root 访问权限的组织而设计。它利用[设置管理](/manuals/enterprise/security/hardened-desktop/settings-management/_index.md)，使管理员可以完全控制私有市场。

## 先决条件

- [下载并安装 Docker Desktop 4.26.0 或更高版本](https://docs.docker.com/desktop/release-notes/)。
- 您必须是您组织的管理员。
- 您有能力通过设备管理软件（如 [Jamf](https://www.jamf.com/)）将 `extension-marketplace` 文件夹和 `admin-settings.json` 文件推送到以下指定位置。

## 第一步：初始化私有市场

1. 在本地创建一个用于部署到开发人员机器的内容文件夹：

   ```console
   $ mkdir my-marketplace
   $ cd my-marketplace
   ```

2. 初始化您的市场配置文件：

   {{< tabs group="os_version" >}}
   {{< tab name="Mac" >}}

   ```console
   $ /Applications/Docker.app/Contents/Resources/bin/extension-admin init
   ```

   {{< /tab >}}
   {{< tab name="Windows" >}}

   ```console
   $ C:\Program Files\Docker\Docker\resources\bin\extension-admin init
   ```

   {{< /tab >}}
   {{< tab name="Linux" >}}

   ```console
   $ /opt/docker-desktop/extension-admin init
   ```

   {{< /tab >}}
   {{< /tabs >}}

这将创建两个文件：

- `admin-settings.json`，一旦应用到开发人员机器上的 Docker Desktop，将激活私有市场功能。
- `extensions.txt`，用于确定在私有市场中列出的扩展。

## 第二步：设置行为

生成的 `admin-settings.json` 文件包含您可以修改的各种设置。

每个设置都有一个可以设置的 `value`，包括一个 `locked` 字段，该字段允许您锁定设置并使其对开发人员不可更改。

- `extensionsEnabled` 启用 Docker Extensions。
- `extensionsPrivateMarketplace` 激活私有市场，并确保 Docker Desktop 连接到由管理员定义和控制的内容，而不是公共 Docker 市场。
- `onlyMarketplaceExtensions` 允许或阻止开发人员使用命令行安装其他扩展。开发新扩展的团队必须将此设置解锁（`"locked": false`）才能安装和测试正在开发的扩展。
- `extensionsPrivateMarketplaceAdminContactURL` 定义一个联系链接，开发人员可以通过该链接在私有市场中请求新扩展。如果 `value` 为空，则在 Docker Desktop 上不会向您的开发人员显示任何链接，否则这可以是 HTTP 链接或 “mailto:” 链接。例如，

  ```json
  "extensionsPrivateMarketplaceAdminContactURL": {
    "locked": true,
    "value": "mailto:admin@acme.com"
  }
  ```

有关 `admin-settings.json` 文件的更多信息，请参阅[设置管理](/manuals/enterprise/security/hardened-desktop/settings-management/_index.md)。

## 第三步：列出允许的扩展

生成的 `extensions.txt` 文件定义了在私有市场中可用的扩展列表。

文件中的每一行都是一个允许的扩展，格式为 `org/repo:tag`。

例如，如果您希望允许 Disk Usage 扩展，您可以在 `extensions.txt` 文件中输入以下内容：

```console
docker/disk-usage-extension:0.2.8
```

如果未提供标签，则使用镜像的最新可用标签。您还可以使用 `#` 注释掉行，以便忽略该扩展。

此列表可以包括不同类型的扩展镜像：

- 来自公共市场或 Docker Hub 中存储的任何公共镜像的扩展。
- 存储在 Docker Hub 中的私有镜像的扩展。开发人员需要登录并具有对这些镜像的拉取访问权限。
- 存储在私有注册表中的扩展镜像。开发人员需要登录并具有对这些镜像的拉取访问权限。

> [!IMPORTANT]
>
> 您的开发人员只能安装您列出的扩展版本。

## 第四步：生成私有市场

一旦 `extensions.txt` 中的列表准备就绪，您就可以生成市场：

{{< tabs group="os_version" >}}
{{< tab name="Mac" >}}

```console
$ /Applications/Docker.app/Contents/Resources/bin/extension-admin generate
```

{{< /tab >}}
{{< tab name="Windows" >}}

```console
$ C:\Program Files\Docker\Docker\resources\bin\extension-admin generate
```

{{< /tab >}}
{{< tab name="Linux" >}}

```console
$ /opt/docker-desktop/extension-admin generate
```

{{< /tab >}}
{{< /tabs >}}

这将创建一个 `extension-marketplace` 目录，并下载所有允许扩展的市场元数据。

市场内容从扩展镜像信息（如镜像标签）生成，这与[公共扩展的格式相同](extensions-sdk/extensions/labels.md)。它包括扩展标题、描述、截图、链接等。

## 第五步：测试私有市场设置

建议您在 Docker Desktop 安装上尝试私有市场。

1. 在终端中运行以下命令。此命令会自动将生成的文件复制到 Docker Desktop 读取配置文件的目录。根据您的操作系统，位置为：

    - Mac: `/Library/Application\ Support/com.docker.docker`
    - Windows: `C:\ProgramData\DockerDesktop`
    - Linux: `/usr/share/docker-desktop`

   {{< tabs group="os_version" >}}
   {{< tab name="Mac" >}}

   ```console
   $ sudo /Applications/Docker.app/Contents/Resources/bin/extension-admin apply
   ```

   {{< /tab >}}
   {{< tab name="Windows (run as admin)" >}}

   ```console
   $ C:\Program Files\Docker\Docker\resources\bin\extension-admin apply
   ```

   {{< /tab >}}
   {{< tab name="Linux" >}}

   ```console
   $ sudo /opt/docker-desktop/extension-admin apply
   ```

   {{< /tab >}}
   {{< /tabs >}}

2. 退出并重新打开 Docker Desktop。
3. 使用 Docker 账户登录。

当您选择 **Extensions** 选项卡时，您应该看到私有市场仅列出您在 `extensions.txt` 中允许的扩展。

![Extensions Private Marketplace](/assets/images/extensions-private-marketplace.webp)

## 第六步：分发私有市场

一旦您确认私有市场配置有效，最后一步是使用组织使用的 MDM 软件将文件分发到开发人员的机器上。例如，[Jamf](https://www.jamf.com/)。

要分发的文件是：
* `admin-settings.json`
* 整个 `extension-marketplace` 文件夹及其子文件夹

这些文件必须放置在开发人员的机器上。根据您的操作系统，目标位置为（如上所述）：

- Mac: `/Library/Application\ Support/com.docker.docker`
- Windows: `C:\ProgramData\DockerDesktop`
- Linux: `/usr/share/docker-desktop`

确保您的开发人员登录到 Docker Desktop，以便私有市场配置生效。作为管理员，您应该[强制登录](/manuals/enterprise/security/enforce-sign-in/_index.md)。

## 反馈

通过发送电子邮件到 `extensions@docker.com` 提供反馈或报告您可能发现的任何错误。