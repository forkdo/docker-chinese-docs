---
description: 探索学习中心，了解登录 Docker Desktop 的优势
keywords: Docker Dashboard, 管理, 容器, GUI, 仪表板, 镜像, 用户手册, 学习中心, 指南, 登录
title: 登录 Docker Desktop
linkTitle: 登录
weight: 40
aliases:
- /desktop/linux/
- /desktop/linux/index/
- /desktop/mac/
- /desktop/mac/index/
- /desktop/windows/
- /desktop/windows/index/
- /docker-for-mac/
- /docker-for-mac/index/
- /docker-for-mac/osx/
- /docker-for-mac/started/
- /docker-for-windows/
- /docker-for-windows/index/
- /docker-for-windows/started/
- /mac/
- /mackit/
- /mackit/getting-started/
- /win/
- /windows/
- /winkit/
- /winkit/getting-started/
- /desktop/get-started/
---

Docker 建议通过 Docker Dashboard 右上角的 **登录** 选项进行登录。

在管理员权限受限的大型企业中，管理员可以[强制登录](/manuals/enterprise/security/enforce-sign-in/_index.md)。

> [!TIP]
>
> 探索 [Docker 核心订阅](https://www.docker.com/pricing/)，了解 Docker 可以为您提供的更多服务。

## 登录的优势

- 直接从 Docker Desktop 访问您的 Docker Hub 仓库。

- 相比匿名用户，提高拉取速率限制。请参阅[使用量和限制](/manuals/docker-hub/usage/_index.md)。

- 使用 [Hardened Desktop](/manuals/enterprise/security/hardened-desktop/_index.md) 增强组织在容器化开发中的安全态势。

> [!NOTE]
>
> Docker Desktop 会在 90 天后或 30 天未活动后自动将您登出。

## 使用 Linux 版 Docker Desktop 登录

Linux 版 Docker Desktop 依赖 [`pass`](https://www.passwordstore.org/) 将凭据存储在 GPG 加密的文件中。
在使用 [Docker ID](/accounts/create-account/) 登录 Docker Desktop 之前，您必须先初始化 `pass`。
如果未配置 `pass`，Docker Desktop 会显示警告。

1. 生成 GPG 密钥。您可以使用 gpg 密钥初始化 pass。运行以下命令：

   ``` console
   $ gpg --generate-key
   ``` 
2. 当提示时输入您的姓名和邮箱。

   确认后，GPG 会创建一个密钥对。查找包含您的 GPG ID 的 `pub` 行，例如：

   ```text
   ...
   pubrsa3072 2022-03-31 [SC] [expires: 2024-03-30]
    3ABCD1234EF56G78
   uid          Molly <molly@example.com>
   ```
3. 复制 GPG ID 并使用它初始化 `pass`。例如：

   ```console
   $ pass init 3ABCD1234EF56G78
   ``` 

   您应该看到类似以下的输出：

   ```text
   mkdir: created directory '/home/molly/.password-store/'
   Password store initialized for <generated_gpg-id_public_key>
   ```

初始化 `pass` 后，您可以登录并拉取您的私有镜像。
当 Docker CLI 或 Docker Desktop 使用凭据时，可能会弹出用户提示，要求输入您在 GPG 密钥生成期间设置的密码。

```console
$ docker pull molly/privateimage
Using default tag: latest
latest: Pulling from molly/privateimage
3b9cc81c3203: Pull complete 
Digest: sha256:3c6b73ce467f04d4897d7a7439782721fd28ec9bf62ea2ad9e81a5fb7fb3ff96
Status: Downloaded newer image for molly/privateimage:latest
docker.io/molly/privateimage:latest
```

## 下一步？

- [探索 Docker Desktop](/manuals/desktop/use-desktop/_index.md) 及其功能。
- 更改您的 [Docker Desktop 设置](/manuals/desktop/settings-and-maintenance/settings.md)。
- [浏览常见问题解答](/manuals/desktop/troubleshoot-and-support/faqs/general.md)。