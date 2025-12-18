---
description: 了解如何在 Ubuntu 上安装、启动和升级 Docker Desktop。本快速指南涵盖先决条件、安装方法等内容。
keywords: install docker ubuntu, ubuntu install docker, install docker on ubuntu,
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

> **Docker Desktop 使用条款**
>
> 大型企业（超过 250 名员工或年收入超过 1000 万美元）商业使用 Docker Desktop 需要[付费订阅](https://www.docker.com/pricing/)。

本页面包含如何在 Ubuntu 发行版上成功安装、启动和升级 Docker Desktop 的信息。

## 先决条件

要成功安装 Docker Desktop，您必须：

- 满足[通用系统要求](_index.md#general-system-requirements)。
- 拥有 x86-64 架构的系统，运行 Ubuntu 22.04、24.04 或最新的非 LTS 版本。
- 如果您未使用 GNOME，则必须安装 `gnome-terminal` 以启用 Docker Desktop 的终端访问：
  ```console
  $ sudo apt install gnome-terminal
  ```

## 安装 Docker Desktop

在 Ubuntu 上安装 Docker Desktop 的推荐方法：

1. 设置 Docker 的软件包仓库。
   参见 [使用 `apt` 仓库安装](/manuals/engine/install/ubuntu.md#install-using-the-repository) 的第一步。

2. 下载最新的 [DEB 软件包](https://desktop.docker.com/linux/main/amd64/docker-desktop-amd64.deb?utm_source=docker&utm_medium=webreferral&utm_campaign=docs-driven-download-linux-amd64)。校验和信息请参阅 [发布说明](/manuals/desktop/release-notes.md)。

3. 使用 `apt` 安装软件包：

   ```console
   $ sudo apt-get update
   $ sudo apt-get install ./docker-desktop-amd64.deb
   ```

   > [!NOTE]
   >
   > 安装过程结束时，`apt` 会显示一条错误消息，这是由于安装了下载的软件包。您可以忽略此错误消息。
   >
   > ```text
   > N: 下载在未隔离的环境中以 root 身份执行，因为用户 '_apt' 无法访问文件 '/home/user/Downloads/docker-desktop.deb'。 - pkgAcquire::Run (13: Permission denied)
   > ```

   默认情况下，Docker Desktop 安装在 `/opt/docker-desktop` 目录。

DEB 软件包包含一个 post-install 脚本，可自动完成额外的设置步骤。

post-install 脚本会：

- 为 Docker Desktop 二进制文件设置能力，以映射特权端口并设置资源限制。
- 为 Kubernetes 在 `/etc/hosts` 中添加 DNS 名称。
- 创建从 `/usr/local/bin/com.docker.cli` 到 `/usr/bin/docker` 的符号链接。
  这是因为经典 Docker CLI 安装在 `/usr/bin/docker`。Docker Desktop 安装程序还在 `/usr/local/bin/com.docker.cli` 安装了一个 Docker CLI 二进制文件，它包含云集成功能，本质上是 Compose CLI 的包装器。该符号链接确保包装器可以访问经典 Docker CLI。

## 启动 Docker Desktop

{{% include "desktop-linux-launch.md" %}}

## 升级 Docker Desktop

当 Docker Desktop 发布新版本时，Docker UI 会显示通知。每次要升级 Docker Desktop 时，您需要下载新软件包并运行：

```console
$ sudo apt-get install ./docker-desktop-amd64.deb
```

## 后续步骤

- 查看 [Docker 订阅服务](https://www.docker.com/pricing/)，了解 Docker 能为您提供什么。
- 跟随 [Docker 工作坊](/get-started/workshop/_index.md) 学习如何构建镜像并将其作为容器化应用程序运行。
- [探索 Docker Desktop](/manuals/desktop/use-desktop/_index.md) 及其所有功能。
- [故障排除](/manuals/desktop/troubleshoot-and-support/troubleshoot/_index.md) 描述了常见问题、变通方法、如何运行和提交诊断信息以及提交问题。
- [常见问题解答](/manuals/desktop/troubleshoot-and-support/faqs/general.md) 提供了常见问题的答案。
- [发布说明](/manuals/desktop/release-notes.md) 列出了 Docker Desktop 发布相关的组件更新、新功能和改进。
- [备份和还原数据](/manuals/desktop/settings-and-maintenance/backup-and-restore.md) 提供了与 Docker 相关的数据备份和还原说明。