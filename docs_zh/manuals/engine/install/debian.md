---
description: 了解如何在 Debian 上安装 Docker Engine。这些说明涵盖了不同的安装方法、如何卸载以及后续步骤。
keywords: 需求, apt, 安装, debian, 安装, 卸载, 安装 debian, docker engine, 安装 docker engine, 升级, 更新
title: 在 Debian 上安装 Docker Engine
linkTitle: Debian
weight: 20
toc_max: 4
aliases:
- /engine/installation/debian/
- /engine/installation/linux/debian/
- /engine/installation/linux/docker-ce/debian/
- /install/linux/docker-ce/debian/
download-url-base: https://download.docker.com/linux/debian
---

要开始在 Debian 上使用 Docker Engine，请先确保你满足[先决条件](#prerequisites)，然后按照[安装步骤](#installation-methods)进行操作。

## 先决条件

### 防火墙限制

> [!WARNING]
>
> 在安装 Docker 之前，请注意以下安全影响和防火墙不兼容性。

- 如果你使用 ufw 或 firewalld 管理防火墙设置，请注意，当你使用 Docker 暴露容器端口时，这些端口会绕过你的防火墙规则。更多信息，请参考 [Docker 和 ufw](/manuals/engine/network/packet-filtering-firewalls.md#docker-and-ufw)。
- Docker 仅与 `iptables-nft` 和 `iptables-legacy` 兼容。在安装了 Docker 的系统上，使用 `nft` 创建的防火墙规则不受支持。请确保你使用的任何防火墙规则集都是使用 `iptables` 或 `ip6tables` 创建的，并将它们添加到 `DOCKER-USER` 链中，参见 [包过滤和防火墙](/manuals/engine/network/packet-filtering-firewalls.md)。

### 操作系统要求

要安装 Docker Engine，你需要以下 Debian 版本之一：

- Debian Trixie 13 (stable)
- Debian Bookworm 12 (oldstable)
- Debian Bullseye 11 (oldoldstable)

Debian 上的 Docker Engine 与 x86_64 (或 amd64)、armhf (arm/v7)、arm64 和 ppc64le (ppc64el) 架构兼容。

### 卸载旧版本

在安装 Docker Engine 之前，你需要卸载任何冲突的软件包。

你的 Linux 发行版可能提供非官方的 Docker 软件包，这些软件包可能与 Docker 提供的官方软件包冲突。在安装官方版本的 Docker Engine 之前，你必须卸载这些软件包。

需要卸载的非官方软件包包括：

- `docker.io`
- `docker-compose`
- `docker-doc`
- `podman-docker`

此外，Docker Engine 依赖于 `containerd` 和 `runc`。Docker Engine 将这些依赖项打包为一个包：`containerd.io`。如果你之前安装过 `containerd` 或 `runc`，请卸载它们以避免与 Docker Engine 捆绑的版本冲突。

运行以下命令卸载所有冲突的软件包：

```console
$ sudo apt remove $(dpkg --get-selections docker.io docker-compose docker-doc podman-docker containerd runc | cut -f1)
```

`apt` 可能报告你未安装这些软件包中的任何一个。

存储在 `/var/lib/docker/` 中的镜像、容器、卷和网络在卸载 Docker 时不会自动删除。如果你想从干净的安装开始，并希望清理任何现有数据，请阅读[卸载 Docker Engine](#uninstall-docker-engine) 部分。

## 安装方法

你可以根据需要以不同的方式安装 Docker Engine：

- Docker Engine 与 [Docker Desktop for Linux](/manuals/desktop/setup/install/linux/_index.md) 捆绑在一起。这是开始使用的最简单、最快的方法。

- 设置并从 [Docker 的 `apt` 仓库](#install-using-the-repository) 安装 Docker Engine。

- [手动安装](#install-from-a-package) 并手动管理升级。

- 使用 [便捷脚本](#install-using-the-convenience-script)。仅建议在测试和开发环境中使用。

{{% include "engine-license.md" %}}

### 使用 `apt` 仓库安装 {#install-using-the-repository}

首次在新主机上安装 Docker Engine 之前，你需要设置 Docker 的 `apt` 仓库。之后，你可以从该仓库安装和更新 Docker。

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
   Suites: $(. /etc/os-release && echo "$VERSION_CODENAME")
   Components: stable
   Signed-By: /etc/apt/keyrings/docker.asc
   EOF

   sudo apt update
   ```

   > [!NOTE]
   >
   > 如果你使用衍生发行版（如 Kali Linux），你可能需要替换此命令中预期打印版本代号的部分：
   >
   > ```console
   > $(. /etc/os-release && echo "$VERSION_CODENAME")
   > ```
   >
   > 将其替换为对应 Debian 发行版的代号，例如 `bookworm`。

2. 安装 Docker 软件包。

   {{< tabs >}}
   {{< tab name="最新版" >}}

   要安装最新版本，请运行：

   ```console
   $ sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
   ```

   {{< /tab >}}
   {{< tab name="特定版本" >}}

   要安装特定版本的 Docker Engine，首先列出仓库中可用的版本：

   ```console
   $ apt list --all-versions docker-ce

   docker-ce/bookworm 5:{{% param "docker_ce_version" %}}-1~debian.12~bookworm <arch>
   docker-ce/bookworm 5:{{% param "docker_ce_version_prev" %}}-1~debian.12~bookworm <arch>
   ...
   ```

   选择所需版本并安装：

   ```console
   $ VERSION_STRING=5:{{% param "docker_ce_version" %}}-1~debian.12~bookworm
   $ sudo apt install docker-ce=$VERSION_STRING docker-ce-cli=$VERSION_STRING containerd.io docker-buildx-plugin docker-compose-plugin
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

3. 通过运行 `hello-world` 镜像验证安装是否成功：

   ```console
   $ sudo docker run hello-world
   ```

   此命令下载测试镜像并在容器中运行它。当容器运行时，它会打印确认消息然后退出。

你现在已成功安装并启动了 Docker Engine。

{{% include "root-errors.md" %}}

#### 升级 Docker Engine

要升级 Docker Engine，请遵循[安装说明](#install-using-the-repository)的步骤 2，选择你想要安装的新版本。

### 从软件包安装

如果你无法使用 Docker 的 `apt` 仓库安装 Docker Engine，你可以下载适用于你发行版的 `deb` 文件并手动安装。每次要升级 Docker Engine 时，都需要下载新文件。

<!-- markdownlint-disable-next-line -->
1. 访问 [`{{% param "download-url-base" %}}/dists/`]({{% param "download-url-base" %}}/dists/)。

2. 在列表中选择你的 Debian 版本。

3. 进入 `pool/stable/` 并选择适用的架构（`amd64`、`armhf`、`arm64` 或 `s390x`）。

4. 下载 Docker Engine、CLI、containerd 和 Docker Compose 软件包的以下 `deb` 文件：

   - `containerd.io_<version>_<arch>.deb`
   - `docker-ce_<version>_<arch>.deb`
   - `docker-ce-cli_<version>_<arch>.deb`
   - `docker-buildx-plugin_<version>_<arch>.deb`
   - `docker-compose-plugin_<version>_<arch>.deb`

5. 安装 `.deb` 软件包。更新以下示例中的路径，指向你下载的 Docker 软件包。

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

6. 通过运行 `hello-world` 镜像验证安装是否成功：

   ```console
   $ sudo docker run hello-world
   ```

   此命令下载测试镜像并在容器中运行它。当容器运行时，它会打印确认消息然后退出。

你现在已成功安装并启动了 Docker Engine。

{{% include "root-errors.md" %}}

#### 升级 Docker Engine

要升级 Docker Engine，请下载较新的软件包文件并重复[安装过程](#install-from-a-package)，指向新文件。

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

你必须手动删除任何已编辑的配置文件。

## 后续步骤

- 继续阅读 [Linux 的安装后步骤](linux-postinstall.md)。