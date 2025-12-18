---
title: 分享你的扩展
description: 使用分享链接分享你的扩展
keywords: Docker, extensions, share
aliases: 
 - /desktop/extensions-sdk/extensions/share/
weight: 40
---

一旦你的扩展镜像在 Docker Hub 上可访问，任何能够访问该镜像的人都可以安装这个扩展。

用户可以在终端中输入 `docker extension install my/awesome-extension:latest` 来安装你的扩展。

但是，这种方式不支持在安装前预览扩展。

## 创建分享 URL

Docker 允许你使用 URL 分享你的扩展。

当用户访问此 URL 时，它会打开 Docker Desktop 并以与 Marketplace 中扩展相同的方式显示你的扩展预览。从预览界面，用户可以选择 **Install（安装）**。

![Navigate to extension link](images/open-share.png)

要生成此链接，你可以：

- 运行以下命令：

  ```console
  $ docker extension share my/awesome-extension:0.0.1
  ```

- 或者，在本地安装你的扩展后，导航到 **Manage（管理）** 选项卡并选择 **Share（分享）**。

  ![Share button](images/list-preview.png)

> [!NOTE]
>
> 扩展描述或截图等内容的预览是通过 [扩展标签](labels.md) 创建的。