---
description: 在 Ubuntu 上使用 Docker Engine 快速启动您的客户端服务器应用程序。本指南详细介绍了在 Ubuntu 上安装 Docker Engine 的先决条件和多种方法。
keywords: docker install script, ubuntu docker server, ubuntu server docker, install docker engine ubuntu, install docker on ubuntu server, ubuntu 22.04 docker-ce, install docker engine on ubuntu, ubuntu install docker ce, ubuntu install docker engine
title: 在 Ubuntu 上安装 Docker Engine
linkTitle: Ubuntu
weight: 10
toc_max: 4
aliases:
- /ee/docker-ee/ubuntu/
- /engine/installation/linux/docker-ce/ubuntu/
- /engine/installation/linux/docker-ee/ubuntu/
- /engine/installation/linux/ubuntu/
- /engine/installation/linux/ubuntulinux/
- /engine/installation/ubuntulinux/
- /install/linux/docker-ce/ubuntu/
- /install/linux/docker-ee/ubuntu/
- /install/linux/ubuntu/
- /installation/ubuntulinux/
- /linux/step_one/
download-url-base: https://download.docker.com/linux/ubuntu
---

要在 Ubuntu 上使用 Docker Engine，请确保您[满足先决条件](#prerequisites)，然后按照[安装步骤](#installation-methods)操作。

## 先决条件

### 防火墙限制

> [!WARNING]
>
> 在安装 Docker 之前，请确保您考虑以下安全影响和防火墙不兼容问题。

- 如果您使用 ufw 或 firewalld 管理防火墙设置，请注意，当您使用 Docker 公开容器端口时，这些端口将绕过您的防火墙规则。有关更多信息，请参阅
  [Docker 和 ufw](/manuals/engine/network/packet-filtering-firewalls.md#docker-and-ufw)。
- Docker 仅兼容 `iptables-nft` 和 `iptables-legacy`。
  在安装了 Docker 的系统上，不支持使用 `nft` 创建的防火墙规则。
  请确保您使用的任何防火墙规则集均使用 `iptables` 或 `ip6tables` 创建，
  并将其添加到 `DOCKER-USER` 链中，
  参见[数据包过滤和防火墙](/manuals/engine/network/packet-filtering-firewalls.md)。

### 操作系统要求

要安装 Docker Engine，您需要以下任一 Ubuntu 版本的 64 位版本：

- Ubuntu Questing 25.10
- Ubuntu Plucky 25.04
- Ubuntu Noble 24.04 (LTS)
- Ubuntu Jammy 22.04 (LTS)

适用于 Ubuntu 的 Docker Engine 兼容 x86_64（或 amd64）、armhf、arm64、
s390x 和 ppc64le（ppc64el）架构。

> [!NOTE]
>
> 官方不支持在 Ubuntu 衍生发行版（如 Linux Mint）上安装（尽管可能可以工作）。

### 卸载旧版本

在安装 Docker Engine 之前，您需要卸载任何冲突的软件包。

您的 Linux 发行版可能提供非官方的 Docker 软件包，这些软件包可能与 Docker 提供的官方软件包冲突。在安装 Docker Engine 官方版本之前，您必须卸载这些软件包。

需要卸载的非官方软件包包括：

- `docker.io`
- `docker-compose`
- `docker-compose-v2`
- `docker-doc`
- `podman-docker`

此外，Docker Engine 依赖于 `containerd` 和 `runc`。Docker Engine
将这些依赖项捆绑为一个包：`containerd.io`。如果您之前已安装
`containerd` 或 `runc`，请将其卸载，以避免与 Docker Engine 捆绑的版本发生冲突。

运行以下命令卸载所有冲突的软件包：

```console
$ sudo apt remove $(dpkg --get-selections docker.io docker-compose docker-compose-v2 docker-doc podman-docker containerd runc | cut -f1)
```

`apt` 可能会报告您未安装这些软件包中的任何一个。

存储在 `/var/lib/docker/` 中的镜像、容器、卷和网络在卸载 Docker 时不会
自动删除。如果您希望进行全新安装，并希望清理任何现有数据，请阅读
[卸载 Docker Engine](#uninstall-docker-engine) 部分。

## 安装方法

您可以根据需要以不同方式安装 Docker Engine：

- Docker Engine 与
  [Docker Desktop for Linux](/manuals/desktop/setup/install/linux/_index.md) 捆绑提供。这是
  最简单、最快速的入门方式。

- 从 [Docker 的 `apt` 仓库](#install-using-the-repository)设置并安装 Docker Engine。

- [手动安装](#install-from-a-package)并手动管理升级。

- 使用[便捷脚本](#install-using-the-convenience-script)。仅
  推荐用于测试和开发环境。

{{% include "engine-license.md" %}}

### 使用 `apt` 仓库安装 {#install-using-the-repository}

在新主机上首次安装 Docker Engine 之前，您需要设置 Docker 的 `apt` 仓库。之后，您可以从该仓库安装和更新 Docker。

1. 设置 Docker 的 `apt` 仓库。

   ```bash
   # 添加 Docker 的官方 GPG 密钥：
   sudo apt update
   sudo apt install ca-certificates curl
   sudo install -m 0755 -d /etc/apt/keyrings
   sudo curl -fsSL {{% param "download-url-base" %}}/gpg -o /etc/apt/keyrings/docker.asc
   sudo chmod a+r /etc/apt/keyrings/docker.asc

   # 将仓库添加到 Apt 源：
   sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
   Types: deb
   URIs: {{% param "download-url-base" %}}
   Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
   Components: stable
   Signed-By: /etc/apt/keyrings/docker.asc
   EOF

   sudo apt update
   ```

2. 安装 Docker 软件包。

   {{< tabs >}}
   {{< tab name="Latest" >}}

   要安装最新版本，请运行：

   ```console
   $ sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
   ```

   {{< /tab >}}
   {{< tab name="Specific version" >}}

   要安装特定版本的 Docker Engine，请先列出仓库中
   可用的版本：

   ```console
   $ apt list --all-versions docker-ce

   docker-ce/noble 5:{{% param "docker_ce_version" %}}-1~ubuntu.24.04~noble <arch>
   docker-ce/noble 5:{{% param "docker_ce_version_prev" %}}-1~ubuntu.24.04~noble <arch>
   ...
   ```

   选择所需版本并安装：

   ```console
   $ VERSION_STRING=5:{{% param "docker_ce_version" %}}-1~ubuntu.24.04~noble
   $ sudo apt install docker-ce=$VERSION_STRING docker-ce-cli=$VERSION_STRING containerd.io docker-buildx-plugin docker-compose-plugin
   ```

   {{< /tab >}}
   {{< /tabs >}}

    > [!NOTE]
    >
    > 安装后 Docker 服务会自动启动。要验证 Docker 是否正在运行，请使用：
    > 
    > ```console
    > $ sudo systemctl status docker
    > ```
    >
    > 某些系统可能已禁用此行为，需要手动启动：
    >
    > ```console
    > $ sudo systemctl start docker
    > ```

3. 通过运行 `hello-world` 镜像验证安装是否成功：

   ```console
   $ sudo docker run hello-world
   ```

   此命令会下载一个测试镜像并在容器中运行它。当容器运行时，它会打印一条确认消息并退出。

您已成功安装并启动了 Docker Engine。

{{% include "root-errors.md" %}}

#### 升级 Docker Engine

要升级 Docker Engine，请按照[安装说明](#install-using-the-repository)的第 2 步操作，
选择您要安装的新版本。

### 从软件包安装

如果您无法使用 Docker 的 `apt` 仓库安装 Docker Engine，您可以
下载对应版本的 `deb` 文件并手动安装。每次升级 Docker Engine 时，您都需要
下载新文件。

<!-- markdownlint-disable-next-line -->
1. 访问 [`{{% param "download-url-base" %}}/dists/`]({{% param "download-url-base" %}}/dists/)。

2. 在列表中选择您的 Ubuntu 版本。

3. 进入 `pool/stable/` 并选择适用的架构（`amd64`、
   `armhf`、`arm64` 或 `s390x`）。

4. 下载 Docker Engine、CLI、containerd 和 Docker Compose 软件包对应的以下 `deb` 文件：

   - `containerd.io_<version>_<arch>.deb`
   - `docker-ce_<version>_<arch>.deb`
   - `docker-ce-cli_<version>_<arch>.deb`
   - `docker-buildx-plugin_<version>_<arch>.deb`
   - `docker-compose-plugin_<version>_<arch>.deb`

5. 安装 `.deb` 软件包。更新以下示例中的路径，以指向您下载的 Docker 软件包所在位置。

   ```console
   $ sudo dpkg -i ./containerd.io_<version>_<arch>.deb \
     ./docker-ce_<version>_<arch>.deb \
     ./docker-ce-cli_<version>_<arch>.deb \
     ./docker-buildx-plugin_<version>_<arch>.deb \
     ./docker-compose-plugin_<version>_<arch>.deb
   ```

    > [!NOTE]
    >
    > 安装后 Docker 服务会自动启动。要验证 Docker 是否正在运行，请使用：
    > 
    > ```console
    > $ sudo systemctl status docker
    > ```
    >
    > 某些系统可能已禁用此行为，需要手动启动：
    >
    > ```console
    > $ sudo systemctl start docker
    > ```

6. 通过运行 `hello-world` 镜像验证安装是否成功：

   ```console
   $ sudo docker run hello-world
   ```

   此命令会下载一个测试镜像并在容器中运行它。当容器运行时，它会打印一条确认消息并退出。

您已成功安装并启动了 Docker Engine。

{{% include "root-errors.md" %}}

#### 升级 Docker Engine

要升级 Docker Engine，请下载新的软件包文件并重复
[安装过程](#install-from-a-package)，指向新文件。

{{% include "install-script.md" %}}

## 卸载 Docker Engine

1. 卸载 Docker Engine、CLI、containerd 和 Docker Compose 软件包：

   ```console
   $ sudo apt purge docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin docker-ce-rootless-extras
   ```

2. 主机上的镜像、容器、卷或自定义配置文件不会自动删除。要删除所有镜像、容器和卷：

   ```console
   $ sudo rm -rf /var/lib/docker
   $ sudo rm -rf /var/lib/containerd
   ```

3. 删除源列表和密钥环

   ```console
   $ sudo rm /etc/apt/sources.list.d/docker.sources
   $ sudo rm /etc/apt/keyrings/docker.asc
   ```

您必须手动删除任何已编辑的配置文件。

## 后续步骤

- 继续 [Linux 安装后步骤](linux-postinstall.md)。