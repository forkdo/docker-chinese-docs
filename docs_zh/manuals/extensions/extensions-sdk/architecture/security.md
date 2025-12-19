---
title: 扩展安全性
linkTitle: 安全性
description: 扩展安全模型的各个方面
keywords: Docker, extensions, sdk, security
aliases:
 - /desktop/extensions-sdk/guides/security/
 - /desktop/extensions-sdk/architecture/security/
---

## 扩展功能

扩展可以包含以下可选部分：
* 以 HTML 或 JavaScript 编写的用户界面，显示在 Docker Desktop Dashboard 中
* 作为容器运行的后端部分
* 部署在主机上的可执行文件

扩展以与 Docker Desktop 用户相同的权限执行。扩展功能包括运行任何 Docker 命令（包括运行容器和挂载文件夹）、运行扩展二进制文件，以及访问机器上 Docker Desktop 用户可访问的文件。
请注意，扩展并不局限于在扩展元数据的 [host 部分](../architecture/metadata.md#host-section) 中列出的二进制文件：由于这些二进制文件可能包含以用户身份运行的任何代码，只要用户有权限，它们就可以进一步执行任何其他命令。

扩展 SDK 提供了一组 JavaScript API，用于从扩展 UI 代码中调用命令或这些二进制文件。扩展也可以提供一个后端部分，在后台启动一个长期运行的容器。

> [!IMPORTANT]
>
> 安装扩展时，请确保信任扩展的发布者或作者，因为扩展具有与运行 Docker Desktop 的用户相同的访问权限。