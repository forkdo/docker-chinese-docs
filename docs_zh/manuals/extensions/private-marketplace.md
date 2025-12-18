---
description: 如何配置和使用 Docker Extensions 的私有市场
keywords: Docker Extensions, Docker Desktop, Linux, Mac, Windows, 市场, 私有, 安全, 管理员
title: 配置扩展的私有市场
tags: [admin]
linkTitle: 配置私有市场
weight: 30
aliases:
 - /desktop/extensions/private-marketplace/
---

{{< summary-bar feature_name="私有市场" >}}

了解如何配置并设置一个包含精选扩展列表的私有市场，供您的 Docker Desktop 用户使用。

Docker Extensions 的私有市场专为不向开发者提供机器 root 权限的组织设计。它利用 [Settings Management](/manuals/enterprise/security/hardened-desktop/settings-management/_index.md)，使管理员能够完全控制私有市场。

## 前提条件

- [下载并安装 Docker Desktop 4.26.0 或更高版本](https://docs.docker.com/desktop/release-notes/)。
- 您必须是组织的管理员。
- 您需要能够通过设备管理软件（例如 [Jamf](https://www.jamf.com/)）将 `extension-marketplace` 文件夹和 `admin-settings.json` 文件推送到下方指定的位置。

## 步骤一：初始化私有市场

1. 在本地创建一个文件夹，用于存放将部署到开发者机器上的内容：

   ```console
   $ mkdir my-marketplace
   $ cd my-marketplace
   ```

2. 初始化市场的配置文件：

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

这将创建 2 个文件：

- `admin-settings.json`，一旦应用到开发者机器上的 Docker Desktop，即可激活私有市场功能。
- `extensions.txt`，决定在私有市场中列出哪些扩展。

## 步骤二：设置行为

生成的 `admin-settings.json` 文件包含多个可修改的设置。

每个设置都有一个 `value` 值，您可以设置它，包括一个 `locked` 字段，允许您锁定设置，使其无法被开发者更改。

- `extensionsEnabled` 启用 Docker Extensions。
- `extensionsPrivateMarketplace` 激活私有市场，确保 Docker Desktop 连接到由管理员定义和控制的内容，而不是公共 Docker 市场。
- `onlyMarketplaceExtensions` 允许或阻止开发者通过命令行安装其他扩展。开发新扩展的团队必须解锁此设置（`"locked": false`）才能安装和测试正在开发的扩展。
- `extensionsPrivateMarketplaceAdminContactURL` 定义一个联系链接，供开发者请求在私有市场中添加新扩展。如果 `value` 为空，则 Docker Desktop 上不会向开发者显示链接，否则可以是 HTTP 链接或 "mailto:" 链接。例如：

  ```json
  "extensionsPrivateMarketplaceAdminContactURL": {
    "locked": true,
    "value": "mailto:admin@acme.com"
  }
  ```

如需了解 `admin-settings.json` 文件的更多信息，请参阅 [Settings Management](/manuals/enterprise/security/hardened-desktop/settings-management/_index.md)。

## 步骤三：列出允许的扩展

生成的 `extensions.txt` 文件定义了在私有市场中可用的扩展列表。

文件中的每一行代表一个允许的扩展，格式为 `org/repo:tag`。

例如，如果您想允许 Disk Usage 扩展，需要在 `extensions.txt` 文件中输入：

```console
docker/disk-usage-extension:0.2.8
```

如果未提供标签，则使用该镜像可用的最新标签。您也可以使用 `#` 注释掉行，这样扩展将被忽略。

此列表可以包含不同类型的扩展镜像：

- 来自公共市场或存储在 Docker Hub 上的任何公共镜像的扩展。
- 存储在 Docker Hub 上的私有镜像扩展。开发者需要登录并具有这些镜像的拉取权限。
- 存储在私有注册表中的扩展镜像。开发者需要登录并具有这些镜像的拉取权限。

> [!IMPORTANT]
>
> 您的开发者只能安装您列出的扩展版本。

## 步骤四：生成私有市场

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

市场内容从扩展镜像信息（作为镜像标签）生成，格式与公共扩展相同，包括扩展标题、描述、截图、链接等。

## 步骤五：测试私有市场设置

建议您在 Docker Desktop 安装上测试私有市场。

1. 在终端中运行以下命令。此命令会自动将生成的文件复制到 Docker Desktop 读取配置文件的位置。根据您的操作系统，位置为：

    - Mac: `/Library/Application\ Support/com.docker.docker`
    - Windows: `C:\ProgramData\DockerDesktop`
    - Linux: `/usr/share/docker-desktop`

   {{< tabs group="os_version" >}}
   {{< tab name="Mac" >}}

   ```console
   $ sudo /Applications/Docker.app/Contents/Resources/bin/extension-admin apply
   ```

   {{< /tab >}}
   {{< tab name="Windows (以管理员身份运行)" >}}

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

当您选择 **Extensions** 选项卡时，应该只能看到私有市场中列出的、您在 `extensions.txt` 中允许的扩展。

![Extensions Private Marketplace](/assets/images/extensions-private-marketplace.webp)

## 步骤六：分发私有市场

一旦确认私有市场配置正常工作，最后一步是使用组织使用的 MDM 软件（例如 [Jamf](https://www.jamf.com/)）将文件分发到开发者机器上。

需要分发的文件包括：
* `admin-settings.json`
* 整个 `extension-marketplace` 文件夹及其子文件夹

这些文件必须放置在开发者机器上。根据您的操作系统，目标位置为（如上所述）：

- Mac: `/Library/Application\ Support/com.docker.docker`
- Windows: `C:\ProgramData\DockerDesktop`
- Linux: `/usr/share/docker-desktop`

确保您的开发者登录 Docker Desktop，以便私有市场配置生效。作为管理员，您应该 [强制登录](/manuals/enterprise/security/enforce-sign-in/_index.md)。

## 反馈

请通过 `extensions@docker.com` 邮箱提供反馈或报告您发现的任何问题。