---
description: 在 Debian 上安装 Docker Desktop 的说明
keywords: debian, install, uninstall, upgrade, update, linux, desktop, docker desktop,
  docker desktop for linux, dd4l
title: 在 Debian 上安装 Docker Desktop
linkTitle: Debian
weight: 20
toc_max: 4
aliases:
- /desktop/linux/install/debian/
- /desktop/install/debian/
- /desktop/install/linux/debian/
---

> **Docker Desktop 使用条款**
>
> 大型企业（超过 250 名员工或年收入超过 1000 万美元）商业使用 Docker Desktop 需要 [付费订阅](https://www.docker.com/pricing/)。

本页面包含如何在 Debian 发行版上安装、启动和升级 Docker Desktop 的信息。

## 前置条件

要成功安装 Docker Desktop，您必须：

- 满足 [通用系统要求](_index.md#general-system-requirements)。
- 拥有 64 位版本的 Debian 12。
- 对于 Gnome 桌面环境，还必须安装 AppIndicator 和 KStatusNotifierItem [Gnome 扩展](https://extensions.gnome.org/extension/615/appindicator-support/)。
- 如果您未使用 GNOME，则必须安装 `gnome-terminal` 以启用 Docker Desktop 的终端访问：

  ```console
  $ sudo apt install gnome-terminal
  ```

## 安装 Docker Desktop

在 Debian 上安装 Docker Desktop 的推荐方法：

1. 设置 Docker 的 `apt` 软件源。参见 [使用 `apt` 软件源安装](/manuals/engine/install/debian.md#install-using-the-repository) 的第一步。

2. 下载最新的 [DEB 包](https://desktop.docker.com/linux/main/amd64/docker-desktop-amd64.deb?utm_source=docker&utm_medium=webreferral&utm_campaign=docs-driven-download-linux-amd64)。校验和信息请参见 [发布说明](/manuals/desktop/release-notes.md)。

3. 使用 `apt` 安装软件包：

  ```console
  $ sudo apt-get update
  $ sudo apt-get install ./docker-desktop-amd64.deb
  ```

  > [!NOTE]
  >
  > 安装过程结束时，`apt` 会显示一条错误信息，这是由于安装了下载的软件包所致。您可以忽略此错误消息。
  >
  > ```text
  > N: Download is performed unsandboxed as root, as file '/home/user/Downloads/docker-desktop.deb' couldn't be accessed by user '_apt'. - pkgAcquire::Run (13: Permission denied)
  > ```

   默认情况下，Docker Desktop 安装在 `/opt/docker-desktop` 目录。

RPM 软件包包含一个 post-install 脚本，可自动完成额外的设置步骤。

post-install 脚本会：

- 为 Docker Desktop 二进制文件设置能力，以映射特权端口并设置资源限制。
- 为 Kubernetes 添加 DNS 名称到 `/etc/hosts`。
- 创建一个从 `/usr/local/bin/com.docker.cli` 到 `/usr/bin/docker` 的符号链接。这是因为经典 Docker CLI 安装在 `/usr/bin/docker`。Docker Desktop 安装程序还会安装一个包含云集成功能的 Docker CLI 二进制文件（本质上是 Compose CLI 的包装器），位于 `/usr/local/bin/com.docker.cli`。该符号链接确保包装器可以访问经典 Docker CLI。

## 启动 Docker Desktop

{{% include "desktop-linux-launch.md" %}}

## 升级 Docker Desktop

Docker Desktop 发布新版本后，Docker UI 会显示通知。每次要升级 Docker Desktop 时，您需要下载新软件包并运行：

```console
$ sudo apt-get install ./docker-desktop-amd64.deb
```

## 后续步骤

- 探索 [Docker 订阅](https://www.docker.com/pricing/)，了解 Docker 能为您提供的服务。
- 查看 [Docker 工作坊](/get-started/workshop/_index.md)，学习如何构建镜像并将其作为容器化应用程序运行。
- [探索 Docker Desktop](/manuals/desktop/use-desktop/_index.md) 及其所有功能。
- [故障排除](/manuals/desktop/troubleshoot-and-support/troubleshoot/_index.md) 描述了常见问题、变通方案、如何运行和提交诊断信息以及提交问题的方法。
- [常见问题解答](/manuals/desktop/troubleshoot-and-support/faqs/general.md) 提供了常见问题的答案。
- [发布说明](/manuals/desktop/release-notes.md) 列出了 Docker Desktop 发布相关的组件更新、新功能和改进。
- [备份和还原数据](/manuals/desktop/settings-and-maintenance/backup-and-restore.md) 提供了与 Docker 相关数据的备份和还原说明。