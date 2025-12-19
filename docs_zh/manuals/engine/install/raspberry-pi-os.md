---
description: 了解如何在 32 位 Raspberry Pi OS 系统上安装 Docker Engine。这些说明涵盖了不同的安装方法、如何卸载以及后续步骤。请注意，32 位支持将在 Docker Engine v29 及更高版本中被弃用。
keywords: requirements, apt, installation, install docker engine, Raspberry Pi OS, install, uninstall, upgrade, update, deprecated
title: 在 Raspberry Pi OS (32-bit / armhf) 上安装 Docker Engine
linkTitle: Raspberry Pi OS (32-bit / armhf)
weight: 50
toc_max: 4
aliases:
- /engine/installation/linux/raspbian/
- /engine/install/raspbian/
download-url-base: https://download.docker.com/linux/raspbian
---

> [!WARNING]
>
> **Raspberry Pi OS 32 位 (armhf) 弃用**
>
> Docker Engine v28 将是支持 Raspberry Pi OS 32 位 (armhf) 的最后一个主要版本。
> 从 Docker Engine v29 开始，新的主要版本将不再为 Raspberry Pi OS 32 位 (armhf) 提供软件包。
>
> **迁移选项**
> - **64 位 ARM：** 安装 Debian `arm64` 软件包（完全支持）。请参阅
>   [Debian 安装说明](debian.md)。
> - **32 位 ARM (v7)：** 安装 Debian `armhf` 软件包（针对 ARMv7 CPU）。
>
> **注意：** 基于 ARMv6 架构的旧设备不再受官方软件包支持，包括：
> - Raspberry Pi 1 (Model A/B/A+/B+)
> - Raspberry Pi Zero 和 Zero W

要在 Raspberry Pi OS 上开始使用 Docker Engine，请确保您
[满足先决条件](#prerequisites)，然后按照
[安装步骤](#installation-methods) 操作。

> [!IMPORTANT]
>
> 本安装说明指的是 Raspberry Pi OS 的 32 位 (armhf) 版本。如果您使用的是 64 位 (arm64) 版本，请遵循
> [Debian](debian.md) 的说明。

## 先决条件

### 防火墙限制

> [!WARNING]
>
> 在安装 Docker 之前，请确保您考虑了以下
> 安全影响和防火墙不兼容性。

- 如果您使用 ufw 或 firewalld 管理防火墙设置，请注意，当您使用 Docker 暴露容器端口时，这些端口会绕过您的防火墙规则。更多信息，请参阅
  [Docker 和 ufw](/manuals/engine/network/packet-filtering-firewalls.md#docker-and-ufw)。
- Docker 仅兼容 `iptables-nft` 和 `iptables-legacy`。
  在安装了 Docker 的系统上，不支持使用 `nft` 创建的防火墙规则。
  确保您使用的任何防火墙规则集都是使用 `iptables` 或 `ip6tables` 创建的，
  并将它们添加到 `DOCKER-USER` 链中，
  请参阅 [数据包过滤和防火墙](/manuals/engine/network/packet-filtering-firewalls.md)。

### 操作系统要求

要安装 Docker Engine，您需要以下操作系统版本之一：

- 32 位 Raspberry Pi OS Bookworm 12 (stable)
- 32 位 Raspberry Pi OS Bullseye 11 (oldstable)

> [!WARNING]
>
> Docker Engine v28 是支持 Raspberry Pi OS 32 位 (armhf) 的最后一个主要版本。从 v29 开始，
> 将不再为 32 位 Raspberry Pi OS 提供新的软件包。
>
> 迁移选项：
> - 64 位 ARM：使用 Debian `arm64` 软件包；请参阅 [Debian 安装说明](debian.md)。
> - 32 位 ARM (v7)：使用 Debian `armhf` 软件包（针对 ARMv7 CPU）。
>
> 注意：基于 ARMv6 的设备（Raspberry Pi 1 型号和 Raspberry Pi Zero/Zero W）不受
> 官方软件包支持。

### 卸载旧版本

在安装 Docker Engine 之前，您需要卸载任何冲突的软件包。

您的 Linux 发行版可能会提供非官方的 Docker 软件包，这些软件包可能与 Docker 提供的官方软件包冲突。在安装官方版本的 Docker Engine 之前，您必须卸载这些软件包。

需要卸载的非官方软件包是：

- `docker.io`
- `docker-compose`
- `docker-doc`
- `podman-docker`

此外，Docker Engine 依赖于 `containerd` 和 `runc`。Docker Engine
将这些依赖项捆绑为一个包：`containerd.io`。如果您之前安装了
`containerd` 或 `runc`，请卸载它们以避免与 Docker Engine 捆绑的版本发生冲突。

运行以下命令以卸载所有冲突的软件包：

```console
$ for pkg in docker.io docker-doc docker-compose podman-docker containerd runc; do sudo apt-get remove $pkg; done
```

`apt-get` 可能会报告您没有安装这些软件包。

存储在 `/var/lib/docker/` 中的镜像、容器、卷和网络在您卸载 Docker 时不会自动删除。如果您想从头开始安装，并希望清理任何现有数据，请阅读
[卸载 Docker Engine](#uninstall-docker-engine) 部分。

## 安装方法

您可以根据需要以不同的方式安装 Docker Engine：

- Docker Engine 与
  [Docker Desktop for Linux](/manuals/desktop/setup/install/linux/_index.md) 捆绑在一起。这是
  最简单、最快速的入门方式。

- 从 [Docker 的 `apt` 仓库](#install-using-the-repository) 设置并安装 Docker Engine。

- [手动安装](#install-from-a-package) 并手动管理升级。

- 使用 [便捷脚本](#install-using-the-convenience-script)。仅
  推荐用于测试和开发环境。

{{% include "engine-license.md" %}}

### 使用 `apt` 仓库安装 {#install-using-the-repository}

在新主机上首次安装 Docker Engine 之前，您需要设置 Docker `apt` 仓库。之后，您可以从仓库安装和更新 Docker。

1. 设置 Docker 的 `apt` 仓库。

   ```bash
   # 添加 Docker 的官方 GPG 密钥：
   sudo apt-get update
   sudo apt-get install ca-certificates curl
   sudo install -m 0755 -d /etc/apt/keyrings
   sudo curl -fsSL {{% param "download-url-base" %}}/gpg -o /etc/apt/keyrings/docker.asc
   sudo chmod a+r /etc/apt/keyrings/docker.asc

   # 将仓库添加到 Apt 源中：
   echo \
     "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] {{% param "download-url-base" %}} \
     $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
     sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
   sudo apt-get update
   ```

2. 安装 Docker 软件包。

   {{< tabs >}}
   {{< tab name="最新版" >}}

   要安装最新版本，请运行：

   ```console
   $ sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
   ```

   {{< /tab >}}
   {{< tab name="特定版本" >}}

   要安装特定版本的 Docker Engine，首先列出仓库中可用的版本：

   ```console
   # 列出可用版本：
   $ apt-cache madison docker-ce | awk '{ print $3 }'

   5:{{% param "docker_ce_version" %}}-1~raspbian.12~bookworm
   5:{{% param "docker_ce_version_prev" %}}-1~raspbian.12~bookworm
   ...
   ```

   选择所需的版本并安装：

   ```console
   $ VERSION_STRING=5:{{% param "docker_ce_version" %}}-1~raspbian.12~bookworm
   $ sudo apt-get install docker-ce=$VERSION_STRING docker-ce-cli=$VERSION_STRING containerd.io docker-buildx-plugin docker-compose-plugin
   ```

   {{< /tab >}}
   {{< /tabs >}}

    > [!NOTE]
    >
    > Docker 服务在安装后会自动启动。要验证 Docker 是否正在运行，请使用：
    > 
    > ```console
    > $ sudo systemctl status docker
    > ```
    >
    > 某些系统可能禁用了此行为，需要手动启动：
    >
    > ```console
    > $ sudo systemctl start docker
    > ```

3. 通过运行 `hello-world` 镜像来验证安装是否成功：

   ```console
   $ sudo docker run hello-world
   ```

   此命令下载测试镜像并在容器中运行。当容器运行时，它会打印一条确认消息并退出。

您现已成功安装并启动了 Docker Engine。

{{% include "root-errors.md" %}}

#### 升级 Docker Engine

要升级 Docker Engine，请按照 [安装说明](#install-using-the-repository) 的步骤 2
操作，选择您要安装的新版本。

### 从软件包安装

如果您无法使用 Docker 的 `apt` 仓库来安装 Docker Engine，您可以下载适用于您发行版的 `deb` 文件并手动安装。每次想要升级 Docker Engine 时，都需要下载一个新文件。

<!-- markdownlint-disable-next-line -->
1. 转到 [`{{% param "download-url-base" %}}/dists/`]({{% param "download-url-base" %}}/dists/)。

2. 在列表中选择您的 Raspberry Pi OS 版本。

3. 转到 `pool/stable/` 并选择适用的架构（`amd64`、`armhf`、`arm64` 或 `s390x`）。

4. 下载 Docker Engine、CLI、containerd 和 Docker Compose 软件包的以下 `deb` 文件：

   - `containerd.io_<version>_<arch>.deb`
   - `docker-ce_<version>_<arch>.deb`
   - `docker-ce-cli_<version>_<arch>.deb`
   - `docker-buildx-plugin_<version>_<arch>.deb`
   - `docker-compose-plugin_<version>_<arch>.deb`

5. 安装 `.deb` 软件包。更新以下示例中的路径，指向您下载 Docker 软件包的位置。

   ```console
   $ sudo dpkg -i ./containerd.io_<version>_<arch>.deb \
     ./docker-ce_<version>_<arch>.deb \
     ./docker-ce-cli_<version>_<arch>.deb \
     ./docker-buildx-plugin_<version>_<arch>.deb \
     ./docker-compose-plugin_<version>_<arch>.deb
   ```

    > [!NOTE]
    >
    > Docker 服务在安装后会自动启动。要验证 Docker 是否正在运行，请使用：
    > 
    > ```console
    > $ sudo systemctl status docker
    > ```
    >
    > 某些系统可能禁用了此行为，需要手动启动：
    >
    > ```console
    > $ sudo systemctl start docker
    > ```

6. 通过运行 `hello-world` 镜像来验证安装是否成功：

   ```console
   $ sudo docker run hello-world
   ```

   此命令下载测试镜像并在容器中运行。当容器运行时，它会打印一条确认消息并退出。

您现已成功安装并启动了 Docker Engine。

{{% include "root-errors.md" %}}

#### 升级 Docker Engine

要升级 Docker Engine，请下载较新的软件包文件，并重复
[安装过程](#install-from-a-package)，指向新的文件。

{{% include "install-script.md" %}}

## 卸载 Docker Engine

1. 卸载 Docker Engine、CLI、containerd 和 Docker Compose 软件包：

   ```console
   $ sudo apt-get purge docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin docker-ce-rootless-extras
   ```

2. 主机上的镜像、容器、卷或自定义配置文件不会自动删除。要删除所有镜像、容器和卷：

   ```console
   $ sudo rm -rf /var/lib/docker
   $ sudo rm -rf /var/lib/containerd
   ```

3. 删除源列表和密钥环

   ```console
   $ sudo rm /etc/apt/sources.list.d/docker.list
   $ sudo rm /etc/apt/keyrings/docker.asc
   ```

您必须手动删除任何编辑过的配置文件。

## 后续步骤

- 继续执行 [Linux 安装后步骤](linux-postinstall.md)。