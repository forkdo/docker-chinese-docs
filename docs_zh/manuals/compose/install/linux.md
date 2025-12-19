---
description: 分步指导如何在 Linux 上使用软件包仓库或手动方法安装 Docker Compose 插件。
keywords: install docker compose linux, docker compose plugin, docker-compose-plugin linux, docker compose v2, docker compose manual install, linux docker compose
toc_max: 3
title: 安装 Docker Compose 插件
linkTitle: 插件
aliases:
- /compose/compose-plugin/
- /compose/compose-linux/
- /compose/install/compose-plugin/
weight: 10
---

本页包含如何在 Linux 上从命令行安装 Docker Compose 插件的说明。

要在 Linux 上安装 Docker Compose 插件，您可以：
- [在您的 Linux 系统上设置 Docker 的仓库](#install-using-the-repository)。
- [手动安装](#install-the-plugin-manually)。

> [!NOTE]
>
> 这些说明假设您已经安装了 Docker Engine 和 Docker CLI，现在想要安装 Docker Compose 插件。

## 使用仓库安装

1.  设置仓库。在以下链接中查找特定发行版的说明：

    [Ubuntu](/manuals/engine/install/ubuntu.md#install-using-the-repository) |
    [CentOS](/manuals/engine/install/centos.md#set-up-the-repository) |
    [Debian](/manuals/engine/install/debian.md#install-using-the-repository) |
    [Raspberry Pi OS](/manuals/engine/install/raspberry-pi-os.md#install-using-the-repository) |
    [Fedora](/manuals/engine/install/fedora.md#set-up-the-repository) |
    [RHEL](/manuals/engine/install/rhel.md#set-up-the-repository)。

2.  更新软件包索引，并安装最新版本的 Docker Compose：

    * 对于 Ubuntu 和 Debian，运行：

        ```console
        $ sudo apt-get update
        $ sudo apt-get install docker-compose-plugin
        ```
    * 对于基于 RPM 的发行版，运行：

        ```console
        $ sudo yum update
        $ sudo yum install docker-compose-plugin
        ```

3.  通过检查版本来验证 Docker Compose 是否已正确安装。

    ```console
    $ docker compose version
    ```

### 更新 Docker Compose

要更新 Docker Compose 插件，请运行以下命令：

* 对于 Ubuntu 和 Debian，运行：

    ```console
    $ sudo apt-get update
    $ sudo apt-get install docker-compose-plugin
    ```
* 对于基于 RPM 的发行版，运行：

    ```console
    $ sudo yum update
    $ sudo yum install docker-compose-plugin
    ```

## 手动安装插件

> [!WARNING]
>
> 手动安装不会自动更新。为了便于维护，请使用 Docker 仓库方法。

1.  要下载并安装 Docker Compose CLI 插件，请运行：

    ```console
    $ DOCKER_CONFIG=${DOCKER_CONFIG:-$HOME/.docker}
    $ mkdir -p $DOCKER_CONFIG/cli-plugins
    $ curl -SL https://github.com/docker/compose/releases/download/{{% param "compose_version" %}}/docker-compose-linux-x86_64 -o $DOCKER_CONFIG/cli-plugins/docker-compose
    ```

    此命令为当前用户在 `$HOME` 目录下下载并安装最新版本的 Docker Compose。

    要安装：
    - 供系统上_所有用户_使用的 Docker Compose，请将 `~/.docker/cli-plugins` 替换为 `/usr/local/lib/docker/cli-plugins`。
    - 不同版本的 Compose，请将 `{{% param "compose_version" %}}` 替换为您想要使用的 Compose 版本。
    - 用于不同的架构，请将 `x86_64` 替换为您想要的[架构](https://github.com/docker/compose/releases)。

2.  为二进制文件应用可执行权限：

    ```console
    $ chmod +x $DOCKER_CONFIG/cli-plugins/docker-compose
    ```
    或者，如果您选择为所有用户安装 Compose：

    ```console
    $ sudo chmod +x /usr/local/lib/docker/cli-plugins/docker-compose
    ```

3.  测试安装。

    ```console
    $ docker compose version
    ```

## 下一步是什么？

- [了解 Compose 的工作原理](/manuals/compose/intro/compose-application-model.md)
- [尝试快速入门指南](/manuals/compose/gettingstarted.md)