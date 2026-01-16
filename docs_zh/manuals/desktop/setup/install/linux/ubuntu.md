---
description:
  了解如何在 Ubuntu 上安装、启动和升级 Docker Desktop。本快速指南将涵盖先决条件、安装方法等内容。
keywords:
  install docker ubuntu, ubuntu install docker, install docker on ubuntu,
  docker install ubuntu, how to install docker on ubuntu, ubuntu docker install, docker
  installation on ubuntu, docker ubuntu install, docker installing ubuntu, installing
  docker on ubuntu, docker desktop for ubuntu
title: 在 Ubuntu 上安装 Docker Desktop
linkTitle: Ubuntu
weight: 10
toc_max: 4
aliases:
  - /desktop/linux/install/ubuntu/
  - /desktop/install/ubuntu/
  - /desktop/install/linux/ubuntu/

---

> **Docker Desktop 条款**
>
> 在大型企业（员工人数超过 250 人或年收入超过 1000 万美元）中进行商业用途的 Docker Desktop 使用需要[付费订阅](https://www.docker.com/pricing/)。

此页面包含有关如何在 Ubuntu 发行版上安装、启动和升级 Docker Desktop 的信息。

## 先决条件

要成功安装 Docker Desktop，您必须：

- 满足[通用系统要求](_index.md#general-system-requirements)。
- 拥有搭载 Ubuntu 22.04、24.04 或最新非 LTS 版本的 x86-64 系统。
- 如果您不使用 GNOME，则必须安装 `gnome-terminal` 以启用从 Docker Desktop 访问终端：
  ```console
  $ sudo apt install gnome-terminal
  ```

## 安装 Docker Desktop

在 Ubuntu 上安装 Docker Desktop 的推荐方法：

1. 设置 Docker 的软件包仓库。
   请参阅[使用 `apt` 仓库安装](/manuals/engine/install/ubuntu.md#install-using-the-repository)的第一步。

2. 下载最新的 [DEB 软件包](https://desktop.docker.com/linux/main/amd64/docker-desktop-amd64.deb?utm_source=docker&utm_medium=webreferral&utm_campaign=docs-driven-download-linux-amd64)。有关校验和，请参阅[发行说明](/manuals/desktop/release-notes.md)。

3. 使用 `apt` 安装该软件包：

   ```console
   $ sudo apt-get update
   $ sudo apt install ./docker-desktop-amd64.deb
   ```

   > [!NOTE]
   >
   > 在安装过程结束时，`apt` 会显示一个错误，这是由于安装了下载的软件包。您可以忽略此错误消息。
   >
   > ```text
   > N: Download is performed unsandboxed as root, as file '/home/user/Downloads/docker-desktop.deb' couldn't be accessed by user '_apt'. - pkgAcquire::Run (13: Permission denied)
   > ```

   默认情况下，Docker Desktop 安装在 `/opt/docker-desktop`。

DEB 软件包包含一个安装后脚本，可自动完成其他设置步骤。

安装后脚本会：

- 为 Docker Desktop 二进制文件设置功能，以映射特权端口并设置资源限制。
- 为 Kubernetes 添加一个 DNS 名称到 `/etc/hosts`。
- 从 `/usr/local/bin/com.docker.cli` 创建一个符号链接到 `/usr/bin/docker`。
  这是因为经典 Docker CLI 安装在 `/usr/bin/docker`。Docker Desktop 安装程序还会安装一个包含云集成功能的 Docker CLI 二进制文件，它本质上是 Compose CLI 的包装器，位于 `/usr/local/bin/com.docker.cli`。符号链接确保包装器可以访问经典 Docker CLI。

## 启动 Docker Desktop

{{% include "desktop-linux-launch.md" %}}

## 升级 Docker Desktop

当 Docker Desktop 发布新版本时，Docker UI 会显示通知。
每次要升级 Docker Desktop 时，您需要下载新软件包并运行：

```console
$ sudo apt install ./docker-desktop-amd64.deb
```

## 后续步骤

- 查看 [Docker 的订阅](https://www.docker.com/pricing/)，了解 Docker 可以为您提供什么。
- 按照 [Docker 研讨会](/get-started/workshop/_index.md) 学习如何构建镜像并将其作为容器化应用程序运行。
- [探索 Docker Desktop](/manuals/desktop/use-desktop/_index.md) 及其所有功能。
- [故障排除](/manuals/desktop/troubleshoot-and-support/troubleshoot/_index.md) 描述了常见问题、解决方法、如何运行和提交诊断信息以及提交问题。
- [常见问题解答](/manuals/desktop/troubleshoot-and-support/faqs/general.md) 提供常见问题的答案。
- [发行说明](/manuals/desktop/release-notes.md) 列出了与 Docker Desktop 版本相关的组件更新、新功能和改进。
- [备份和恢复数据](/manuals/desktop/settings-and-maintenance/backup-and-restore.md) 提供了有关备份和恢复 Docker 相关数据的说明。