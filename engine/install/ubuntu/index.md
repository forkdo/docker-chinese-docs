---
title: 在 Ubuntu 上安装 Docker Engine
url: /engine/install/ubuntu/
parent:
  title: 安装 Docker Engine
  url: /engine/install/
breadcrumbs:
  - title: 手册
    url: /manuals/
  - title: Docker Engine
    url: /engine/
  - title: 安装 Docker Engine
    url: /engine/install/
  - title: 在 Ubuntu 上安装 Docker Engine
    url: /engine/install/ubuntu/
prev:
  title: 在 Debian 上安装 Docker Engine
  url: /engine/install/debian/
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



Apache License, Version 2.0. 请参阅 [LICENSE](https://github.com/moby/moby/blob/master/LICENSE) 获取完整许可证。

### 使用 `apt` 仓库安装 {#install-using-the-repository}

在新主机上首次安装 Docker Engine 之前，您需要设置 Docker 的 `apt` 仓库。之后，您可以从该仓库安装和更新 Docker。

1. 设置 Docker 的 `apt` 仓库。

   ```bash
   # 添加 Docker 的官方 GPG 密钥：
   sudo apt update
   sudo apt install ca-certificates curl
   sudo install -m 0755 -d /etc/apt/keyrings
   sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
   sudo chmod a+r /etc/apt/keyrings/docker.asc

   # 将仓库添加到 Apt 源：
   sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
   Types: deb
   URIs: https://download.docker.com/linux/ubuntu
   Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
   Components: stable
   Signed-By: /etc/apt/keyrings/docker.asc
   EOF

   sudo apt update
   ```

2. 安装 Docker 软件包。

   **Latest**



   要安装最新版本，请运行：

   ```console
   $ sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
   ```

   **Specific version**



   要安装特定版本的 Docker Engine，请先列出仓库中
   可用的版本：

   ```console
   $ apt list --all-versions docker-ce

   docker-ce/noble 5:29.1.4-1~ubuntu.24.04~noble <arch>
   docker-ce/noble 5:29.1.3-1~ubuntu.24.04~noble <arch>
   ...
   ```

   选择所需版本并安装：

   ```console
   $ VERSION_STRING=5:29.1.4-1~ubuntu.24.04~noble
   $ sudo apt install docker-ce=$VERSION_STRING docker-ce-cli=$VERSION_STRING containerd.io docker-buildx-plugin docker-compose-plugin
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

3. 通过运行 `hello-world` 镜像验证安装是否成功：

   ```console
   $ sudo docker run hello-world
   ```

   此命令会下载一个测试镜像并在容器中运行它。当容器运行时，它会打印一条确认消息并退出。

您已成功安装并启动了 Docker Engine。



> [!TIP]
> 
> 尝试以非 root 用户身份运行时遇到错误？
>
> `docker` 用户组存在但不包含任何用户，这就是为什么您需要使用 `sudo` 来运行 Docker 命令。请继续阅读 [Linux 安装后配置](/engine/install/linux-postinstall)，了解如何允许非特权用户运行 Docker 命令以及其他可选配置步骤。

#### 升级 Docker Engine

要升级 Docker Engine，请按照[安装说明](#install-using-the-repository)的第 2 步操作，
选择您要安装的新版本。

### 从软件包安装

如果您无法使用 Docker 的 `apt` 仓库安装 Docker Engine，您可以
下载对应版本的 `deb` 文件并手动安装。每次升级 Docker Engine 时，您都需要
下载新文件。

<!-- markdownlint-disable-next-line -->
1. 访问 [`https://download.docker.com/linux/ubuntu/dists/`](https://download.docker.com/linux/ubuntu/dists/)。

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



> [!TIP]
> 
> 尝试以非 root 用户身份运行时遇到错误？
>
> `docker` 用户组存在但不包含任何用户，这就是为什么您需要使用 `sudo` 来运行 Docker 命令。请继续阅读 [Linux 安装后配置](/engine/install/linux-postinstall)，了解如何允许非特权用户运行 Docker 命令以及其他可选配置步骤。

#### 升级 Docker Engine

要升级 Docker Engine，请下载新的软件包文件并重复
[安装过程](#install-from-a-package)，指向新文件。



### 使用便捷脚本安装

Docker 提供了一个便捷脚本，位于 [https://get.docker.com/](https://get.docker.com/)，用于以非交互方式将 Docker 安装到开发环境中。该便捷脚本不推荐用于生产环境，但对于创建符合您需求的配置脚本很有用。另请参阅[使用仓库安装](#install-using-the-repository)步骤，了解使用软件包仓库进行安装的相关步骤。该脚本的源代码是开源的，您可以在 GitHub 上的 [`docker-install` 仓库](https://github.com/docker/docker-install) 中找到它。

<!-- prettier-ignore -->
在本地运行从互联网下载的脚本之前，请务必仔细检查。在安装之前，请熟悉便捷脚本的潜在风险和限制：

- 该脚本需要 `root` 或 `sudo` 权限才能运行。
- 该脚本会尝试检测您的 Linux 发行版和版本，并为您配置包管理系统。
- 该脚本不允许您自定义大多数安装参数。
- 该脚本会安装依赖项和推荐包，而不会要求确认。根据主机机器的当前配置，这可能会安装大量软件包。
- 默认情况下，该脚本会安装 Docker、containerd 和 runc 的最新稳定版本。使用此脚本配置机器时，可能会导致 Docker 意外地进行主要版本升级。在将升级部署到生产系统之前，请务必在测试环境中测试升级。
- 该脚本并非用于升级现有的 Docker 安装。使用该脚本更新现有安装时，依赖项可能不会更新到预期版本，从而导致版本过时。

> [!TIP]
>
> 在运行脚本之前预览脚本步骤。您可以使用 `--dry-run` 选项运行脚本，以了解脚本被调用时将运行的步骤：
>
> ```console
> $ curl -fsSL https://get.docker.com -o get-docker.sh
> $ sudo sh ./get-docker.sh --dry-run
> ```

此示例从 [https://get.docker.com/](https://get.docker.com/) 下载脚本并运行它，以在 Linux 上安装 Docker 的最新稳定版本：

```console
$ curl -fsSL https://get.docker.com -o get-docker.sh
$ sudo sh get-docker.sh
Executing docker install script, commit: 7cae5f8b0decc17d6571f9f52eb840fbc13b2737
<...>
```

现在，您已成功安装并启动了 Docker 引擎。基于 Debian 的发行版会自动启动 `docker` 服务。在基于 `RPM` 的发行版（如 CentOS、Fedora 或 RHEL）上，您需要使用适当的 `systemctl` 或 `service` 命令手动启动它。如消息所示，默认情况下，非 root 用户无法运行 Docker 命令。

> **以非特权用户使用 Docker，或以无根模式安装？**
>
> 安装脚本需要 `root` 或 `sudo` 权限才能安装和使用 Docker。如果您想授予非 root 用户访问 Docker 的权限，请参阅 [Linux 安装后步骤](/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user)。您也可以在没有 `root` 权限的情况下安装 Docker，或配置为以无根模式运行。有关以无根模式运行 Docker 的说明，请参阅[以非 root 用户身份运行 Docker 守护进程（无根模式）](/engine/security/rootless/)。

#### 安装预发布版本

Docker 还在 [https://test.docker.com/](https://test.docker.com/) 提供了一个便捷脚本，用于在 Linux 上安装 Docker 的预发布版本。该脚本与 `get.docker.com` 上的脚本相同，但会将您的包管理器配置为使用 Docker 软件包仓库的测试通道。测试通道包括 Docker 的稳定版本和预发布版本（测试版本、候选发布版本）。使用此脚本可以提前获取新版本，并在它们作为稳定版本发布之前在测试环境中对其进行评估。

要在 Linux 上从测试通道安装 Docker 的最新版本，请运行：

```console
$ curl -fsSL https://test.docker.com -o test-docker.sh
$ sudo sh test-docker.sh
```

#### 使用便捷脚本后升级 Docker

如果您使用便捷脚本安装了 Docker，则应直接使用包管理器升级 Docker。重新运行便捷脚本没有任何优势。如果它尝试重新安装主机上已存在的仓库，重新运行它可能会导致问题。

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
