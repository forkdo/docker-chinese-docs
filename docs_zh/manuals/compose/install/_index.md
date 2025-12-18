---
description: 了解如何安装 Docker Compose。Compose 可通过 Docker Desktop 原生安装、作为 Docker Engine 插件安装，或作为独立工具安装。
keywords: 安装 docker compose, docker compose 插件, 在 linux 上安装 compose, 安装 docker desktop, 在 windows 上安装 docker compose, 独立的 docker compose, docker compose 未找到
title: Docker Compose 安装概览
linkTitle: 安装
weight: 20
toc_max: 3
aliases:
- /compose/compose-desktop/
- /compose/install/other/
- /compose/install/compose-desktop/
---

本页面总结了根据您的平台和需求安装 Docker Compose 的不同方式。

## 安装场景

### Docker Desktop（推荐）

获取 Docker Compose 最简单且推荐的方式是安装 Docker Desktop。

Docker Desktop 包含 Docker Compose，以及 Compose 的先决条件 Docker Engine 和 Docker CLI。

Docker Desktop 可用于：
- [Linux](/manuals/desktop/setup/install/linux/_index.md)
- [Mac](/manuals/desktop/setup/install/mac-install.md)
- [Windows](/manuals/desktop/setup/install/windows-install.md)

> [!TIP]
>
> 如果您已安装 Docker Desktop，可以通过从 Docker 菜单 {{< inline-image src="../../desktop/images/whale-x.svg" alt="whale menu" >}} 选择 **About Docker Desktop** 来检查您当前的 Compose 版本。

### 插件（仅限 Linux）

> [!IMPORTANT]
>
> 此方法仅在 Linux 上可用。

如果您已安装 Docker Engine 和 Docker CLI，可以通过命令行安装 Docker Compose 插件，方式包括：
- [使用 Docker 的仓库](linux.md#install-using-the-repository)
- [手动下载并安装](linux.md#install-the-plugin-manually)

### 独立版（旧版）

> [!WARNING]
>
> 此安装场景不推荐使用，仅为了向后兼容而提供支持。

您可以在 Linux 或 Windows Server 上[安装 Docker Compose 独立版](standalone.md)。