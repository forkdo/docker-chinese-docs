---
description: 如何卸载 Docker Compose
keywords: compose, 编排, uninstall, uninstallation, docker, 文档
title: 卸载 Docker Compose
linkTitle: 卸载
---

卸载 Docker Compose 的方式取决于它的安装方式。本指南涵盖以下卸载说明：

- 通过 Docker Desktop 安装的 Docker Compose
- 作为 CLI 插件安装的 Docker Compose

## 使用 Docker Desktop 卸载 Docker Compose

如果您想卸载 Docker Compose，且您已安装 Docker Desktop，请参阅 [卸载 Docker Desktop](/manuals/desktop/uninstall.md)。

> [!WARNING]
>
> 除非您在该特定环境中安装了其他 Docker 实例，否则卸载 Docker Desktop 会移除所有 Docker 组件，包括 Docker Engine、Docker CLI 和 Docker Compose。

## 卸载 Docker Compose CLI 插件

如果您通过包管理器安装了 Docker Compose，请运行以下命令：

在 Ubuntu 或 Debian 上：

   ```console
   $ sudo apt-get remove docker-compose-plugin
   ```

在基于 RPM 的发行版上：

   ```console
   $ sudo yum remove docker-compose-plugin
   ```

### 手动安装

如果您手动安装了 Docker Compose（使用 curl），请通过删除二进制文件来移除它：

   ```console
   $ rm $DOCKER_CONFIG/cli-plugins/docker-compose
   ```

### 为所有用户移除

如果为所有用户安装，请从系统目录中移除它：

   ```console
   $ rm /usr/local/lib/docker/cli-plugins/docker-compose
   ```

> [!NOTE]
>
> 如果使用上述任一方法时出现 **Permission denied**（权限被拒绝）错误，说明您没有足够的权限移除 Docker Compose。要强制移除，请在上述任一指令前添加 `sudo` 并再次运行。

### 检查 Compose CLI 插件的安装位置

要检查 Compose 安装在哪里，请使用：

```console
$ docker info --format '{{range .ClientInfo.Plugins}}{{if eq .Name "compose"}}{{.Path}}{{end}}{{end}}'
```