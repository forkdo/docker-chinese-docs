---
title: 打包和发布你的扩展
description: Docker 扩展分发
keywords: Docker, extensions, sdk, distribution
aliases: 
 - /desktop/extensions-sdk/extensions/DISTRIBUTION/
weight: 30
---

本页面包含有关如何打包和分发扩展的附加信息。

## 打包你的扩展

Docker 扩展被打包为 Docker 镜像。扩展运行时的全部内容，包括 UI、后端服务（主机或虚拟机）以及任何必要的二进制文件，都必须包含在扩展镜像中。
每个扩展镜像必须在其文件系统的根目录包含一个 `metadata.json` 文件，用于定义 [扩展的内容](../architecture/metadata.md)。

Docker 镜像必须包含多个 [镜像标签](labels.md)，以提供有关扩展的信息。请参阅如何使用 [扩展标签](labels.md) 来提供扩展概述信息。

要打包和发布扩展，你必须构建 Docker 镜像（`docker build`），并将镜像推送到 [Docker Hub](https://hub.docker.com/)（`docker push`），使用特定的标签来管理扩展的版本。

## 发布你的扩展

扩展镜像的标签必须遵循语义化版本（semver）约定，以便允许获取扩展的最新版本，并知道是否有可用的更新。请参阅 [semver.org](https://semver.org/) 了解语义化版本的更多信息。

扩展镜像必须是多架构镜像，以便用户可以在 ARM/AMD 硬件上安装扩展。这些多架构镜像可以包含针对 ARM/AMD 的特定二进制文件。Mac 用户将根据其架构自动使用正确的镜像。
在主机上安装二进制文件的扩展还必须在同一个扩展镜像中提供 Windows 二进制文件。请参阅如何为你的扩展 [构建多架构镜像](multi-arch.md)。

你可以不受代码仓库限制地实现扩展。Docker 不需要访问代码仓库即可使用扩展。此外，你可以管理扩展的新版本发布，而无需依赖 Docker Desktop 的发布。

## 新版本和更新

你可以通过将带有新标签的镜像推送到 Docker Hub 来发布 Docker 扩展的新版本。

推送到对应扩展的镜像仓库的任何新镜像，都会定义该扩展的新版本。镜像标签用于标识版本号。扩展版本必须遵循语义化版本（semver），以便轻松理解和比较版本。

Docker Desktop 会扫描市场中发布的扩展列表，检查是否有新版本，并在用户可以升级特定扩展时提供通知。目前，不属于市场一部分的扩展没有自动更新通知。

用户可以下载并安装任何扩展的较新版本，而无需更新 Docker Desktop 本身。

## 扩展 API 依赖项

扩展必须指定其依赖的扩展 API 版本。Docker Desktop 会检查扩展所需的版本，并且只建议安装与当前安装的 Docker Desktop 版本兼容的扩展。用户可能需要更新 Docker Desktop 才能安装最新的可用扩展。

扩展镜像标签必须指定扩展所依赖的 API 版本。这允许 Docker Desktop 在不预先下载完整扩展镜像的情况下检查扩展镜像的新版本。

## 扩展和扩展 SDK 的许可证

[Docker 扩展 SDK](https://www.npmjs.com/package/@docker/extension-api-client) 根据 Apache 2.0 许可证授权，可免费使用。

对于每个扩展应如何授权，没有约束，这由你在创建新扩展时自行决定。