---
description: 了解如何在 Fedora 上安装 Docker Engine。这些说明涵盖了不同的安装方法、如何卸载以及后续步骤。
keywords: 需求, dnf, 安装, fedora, 安装 fedora, 安装 docker engine, rpm, 安装, 卸载, 升级,
  更新
title: 在 Fedora 上安装 Docker Engine
linkTitle: Fedora
weight: 40
toc_max: 4
aliases:
- /engine/installation/fedora/
- /engine/installation/linux/fedora/
- /engine/installation/linux/docker-ce/fedora/
- /install/linux/docker-ce/fedora/
download-url-base: https://download.docker.com/linux/fedora
---

要开始在 Fedora 上使用 Docker Engine，请确保你满足[先决条件](#prerequisites)，然后按照[安装步骤](#installation-methods)进行操作。

## 先决条件

### 操作系统要求

要安装 Docker Engine，你需要以下 Fedora 版本之一的受支持版本：

- Fedora 43
- Fedora 42
- Fedora 41

### 卸载旧版本

在安装 Docker Engine 之前，你需要卸载任何冲突的软件包。

你的 Linux 发行版可能提供非官方的 Docker 包，这些包可能与 Docker 提供的官方包冲突。你必须在安装官方版本的 Docker Engine 之前卸载这些包。

```console
$ sudo dnf remove docker \
                  docker-client \
                  docker-client-latest \
                  docker-common \
                  docker-latest \
                  docker-latest-logrotate \
                  docker-logrotate \
                  docker-selinux \
                  docker-engine-selinux \
                  docker-engine
```

`dnf` 可能报告你未安装这些包中的任何一个。

存储在 `/var/lib/docker/` 中的镜像、容器、卷和网络在卸载 Docker 时不会自动删除。

## 安装方法

你可以根据需要以不同的方式安装 Docker Engine：

- 你可以[设置 Docker 的仓库](#install-using-the-repository)并从中安装，以便于安装和升级任务。这是推荐的方法。

- 你可以下载 RPM 包，[手动安装](#install-from-a-package)，并完全手动管理升级。这在某些情况下很有用，例如在无法访问互联网的气隙系统上安装 Docker。

- 在测试和开发环境中，你可以使用自动化的[便捷脚本](#install-using-the-convenience-script)来安装 Docker。

{{% include "engine-license.md" %}}

### 使用 rpm 仓库安装 {#install-using-the-repository}

在新主机上首次安装 Docker Engine 之前，你需要设置 Docker 仓库。之后，你可以从该仓库安装和更新 Docker。

#### 设置仓库

```console
$ sudo dnf config-manager addrepo --from-repofile {{% param "download-url-base" %}}/docker-ce.repo
```

#### 安装 Docker Engine

1. 安装 Docker 包。

   {{< tabs >}}
   {{< tab name="最新版" >}}

   要安装最新版本，请运行：

   ```console
   $ sudo dnf install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
   ```

   如果提示接受 GPG 密钥，请验证指纹是否匹配 `060A 61C5 1B55 8A7F 742B 77AA C52F EB6B 621E 9F35`，如果匹配则接受。

   此命令安装 Docker，但不会启动 Docker。它还会创建一个 `docker` 组，但默认情况下不会向该组添加任何用户。

   {{< /tab >}}
   {{< tab name="特定版本" >}}

   要安装特定版本，首先列出仓库中可用的版本：

   ```console
   $ dnf list docker-ce --showduplicates | sort -r

   docker-ce.x86_64    3:{{% param "docker_ce_version" %}}-1.fc41    docker-ce-stable
   docker-ce.x86_64    3:{{% param "docker_ce_version_prev" %}}-1.fc41    docker-ce-stable
   <...>
   ```

   返回的列表取决于启用的仓库，并且特定于你的 Fedora 版本（在此示例中由 `.fc40` 后缀指示）。

   通过其完全限定的包名安装特定版本，包名是包名（`docker-ce`）加上版本字符串（第 2 列），用连字符（`-`）分隔。例如，`docker-ce-3:{{% param "docker_ce_version" %}}-1.fc41`。

   将 `<VERSION_STRING>` 替换为所需版本，然后运行以下命令进行安装：

   ```console
   $ sudo dnf install docker-ce-<VERSION_STRING> docker-ce-cli-<VERSION_STRING> containerd.io docker-buildx-plugin docker-compose-plugin
   ```

   此命令安装 Docker，但不会启动 Docker。它还会创建一个 `docker` 组，但默认情况下不会向该组添加任何用户。

   {{< /tab >}}
   {{< /tabs >}}

2. 启动 Docker Engine。

   ```console
   $ sudo systemctl enable --now docker
   ```

   这将配置 Docker systemd 服务，以便在系统启动时自动启动。如果你不希望 Docker 自动启动，请改用 `sudo systemctl start docker`。

3. 通过运行 `hello-world` 镜像验证安装是否成功：

   ```console
   $ sudo docker run hello-world
   ```

   此命令下载测试镜像并在容器中运行它。当容器运行时，它会打印确认消息然后退出。

你现在已经成功安装并启动了 Docker Engine。

{{% include "root-errors.md" %}}

#### 升级 Docker Engine

要升级 Docker Engine，请遵循[安装说明](#install-using-the-repository)，选择你想要安装的新版本。

### 从包安装

如果你无法使用 Docker 的 `rpm` 仓库安装 Docker Engine，你可以下载适用于你版本的 `.rpm` 文件并手动安装。每次要升级 Docker Engine 时，你都需要下载新文件。

<!-- markdownlint-disable-next-line -->
1. 访问 [{{% param "download-url-base" %}}/]({{% param "download-url-base" %}}/) 并选择你的 Fedora 版本。然后浏览到 `x86_64/stable/Packages/` 并下载你想要安装的 Docker 版本的 `.rpm` 文件。

2. 安装 Docker Engine，将以下路径更改为 Docker 包的下载路径。

   ```console
   $ sudo dnf install /path/to/package.rpm
   ```

   Docker 已安装但未启动。`docker` 组已创建，但没有向该组添加用户。

3. 启动 Docker Engine。

   ```console
   $ sudo systemctl enable --now docker
   ```

   这将配置 Docker systemd 服务，以便在系统启动时自动启动。如果你不希望 Docker 自动启动，请改用 `sudo systemctl start docker`。

4. 通过运行 `hello-world` 镜像验证安装是否成功：

   ```console
   $ sudo docker run hello-world
   ```

   此命令下载测试镜像并在容器中运行它。当容器运行时，它会打印确认消息然后退出。

你现在已经成功安装并启动了 Docker Engine。

{{% include "root-errors.md" %}}

#### 升级 Docker Engine

要升级 Docker Engine，请下载更新的包文件并重复[安装过程](#install-from-a-package)，使用 `dnf upgrade` 而不是 `dnf install`，并指向新文件。

{{% include "install-script.md" %}}

## 卸载 Docker Engine

1. 卸载 Docker Engine、CLI、containerd 和 Docker Compose 包：

   ```console
   $ sudo dnf remove docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin docker-ce-rootless-extras
   ```

2. 主机上的镜像、容器、卷或自定义配置文件不会自动删除。要删除所有镜像、容器和卷：

   ```console
   $ sudo rm -rf /var/lib/docker
   $ sudo rm -rf /var/lib/containerd
   ```

你需要手动删除任何编辑过的配置文件。

## 后续步骤

- 继续阅读 [Linux 的安装后步骤](linux-postinstall.md)。