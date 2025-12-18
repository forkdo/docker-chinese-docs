---
description: Docker Desktop for Mac 的常见问题解答
keywords: desktop, mac, faqs
title: Docker Desktop for Mac 常见问题解答
linkTitle: Mac
tags: [FAQ]
aliases:
- /desktop/mac/space/
- /docker-for-mac/space/
- /desktop/faqs/macfaqs/
weight: 20
---

### 什么是 HyperKit？

HyperKit 是基于 macOS 上的 Hypervisor.framework 构建的虚拟机监控器（hypervisor）。它完全在用户空间中运行，没有其他依赖项。

Docker 使用 HyperKit 来消除对其他虚拟机产品（如 Oracle VirtualBox 或 VMware Fusion）的需求。

### HyperKit 有什么优势？

HyperKit 比 VirtualBox 和 VMware Fusion 更轻量，且包含的版本针对 Mac 上的 Docker 工作负载进行了定制。

### Docker Desktop 将 Linux 容器和镜像存储在哪里？

Docker Desktop 将 Linux 容器和镜像存储在 Mac 文件系统中的单个大型“磁盘镜像”文件中。这与 Linux 上的 Docker 不同，后者通常将容器和镜像存储在 `/var/lib/docker` 目录中。

#### 磁盘镜像文件在哪里？

要定位磁盘镜像文件，请从 Docker Desktop 仪表板中选择 **Settings**（设置），然后选择 **Resources**（资源）选项卡中的 **Advanced**（高级）。

**Advanced**（高级）选项卡会显示磁盘镜像的位置、最大大小以及磁盘镜像实际占用的空间。请注意，其他工具可能会以最大文件大小显示文件的空间使用情况，而不是实际文件大小。

#### 如果文件太大怎么办？

如果磁盘镜像文件太大，你可以：

- 将其移动到更大的驱动器
- 删除不必要的容器和镜像
- 减少文件的最大允许大小

##### 如何将文件移动到更大的驱动器？

要将磁盘镜像文件移动到不同位置：

1. 选择 **Settings**（设置），然后从 **Resources**（资源）选项卡中选择 **Advanced**（高级）。

2. 在 **Disk image location**（磁盘镜像位置）部分，选择 **Browse**（浏览）并选择磁盘镜像的新位置。

3. 选择 **Apply**（应用）使更改生效。

> [!IMPORTANT]
>
> 不要直接在 Finder 中移动文件，这可能导致 Docker Desktop 无法跟踪该文件。

##### 如何删除不必要的容器和镜像？

检查是否有不必要的容器和镜像。如果你的客户端和守护进程 API 运行版本为 1.25 或更高版本（在客户端上使用 `docker version` 命令检查客户端和守护进程 API 版本），可以通过运行以下命令查看详细的空间使用信息：

```console
$ docker system df -v
```

或者，要列出镜像，请运行：

```console
$ docker image ls
```

要列出容器，请运行：

```console
$ docker container ls -a
```

如果有大量冗余对象，请运行命令：

```console
$ docker system prune
```

此命令会删除所有已停止的容器、未使用的网络、悬空镜像和构建缓存。

在主机上释放空间可能需要几分钟，具体取决于磁盘镜像文件的格式。如果文件名为：

- `Docker.raw`，主机上的空间会在几秒内被回收。
- `Docker.qcow2`，空间由后台进程在几分钟后释放。

只有在删除镜像时才会释放空间。在运行的容器内删除文件不会自动释放空间。要在任何时候触发空间回收，请运行命令：

```console
$ docker run --privileged --pid=host docker/desktop-reclaim-space
```

请注意，许多工具报告的是最大文件大小，而不是实际文件大小。要从终端查询主机上文件的实际大小，请运行：

```console
$ cd ~/Library/Containers/com.docker.docker/Data/vms/0/data
$ ls -klsh Docker.raw
2333548 -rw-r--r--@ 1 username  staff    64G Dec 13 17:42 Docker.raw
```

在此示例中，磁盘的实际大小为 `2333548` KB，而磁盘的最大大小为 `64` GB。

##### 如何减小文件的最大大小？

要减小磁盘镜像文件的最大大小：

1. 选择 **Settings**（设置），然后从 **Resources**（资源）选项卡中选择 **Advanced**（高级）。

2. **Disk image size**（磁盘镜像大小）部分包含一个滑块，允许你更改磁盘镜像的最大大小。调整滑块以设置较低的限制。

3. 选择 **Apply**（应用）。

当你减小最大大小时，当前的磁盘镜像文件会被删除，因此所有容器和镜像都会丢失。

### 如何添加 TLS 证书？

你可以将受信任的证书颁发机构（CA）（用于验证注册服务器证书）和客户端证书（用于向注册中心进行身份验证）添加到 Docker 守护进程中。

#### 添加自定义 CA 证书（服务器端）

支持所有受信任的 CA（根 CA 或中间 CA）。Docker Desktop 基于 Mac 密钥链创建所有用户受信任 CA 的证书包，并将其附加到 Moby 受信任证书中。因此，如果企业 SSL 证书在主机上被用户信任，它也会被 Docker Desktop 信任。

要手动添加自定义的自签名证书，请首先将证书添加到 macOS 密钥链，Docker Desktop 会自动识别。以下是一个示例：

```console
$ sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain ca.crt
```

或者，如果你只想将证书添加到自己的本地密钥链（而不是所有用户），请改用以下命令：

```console
$ security add-trusted-cert -d -r trustRoot -k ~/Library/Keychains/login.keychain ca.crt
```

另请参阅，[证书的目录结构](#directory-structures-for-certificates)。

> [!NOTE]
>
> 对密钥链或 `~/.docker/certs.d` 目录进行任何更改后，你需要重启 Docker Desktop 才能使更改生效。

有关如何操作的完整说明，请参阅博客文章 [Adding Self-signed Registry Certs to Docker & Docker Desktop for Mac](https://blog.container-solutions.com/adding-self-signed-registry-certs-docker-mac)。

#### 添加客户端证书

你可以将客户端证书放在 `~/.docker/certs.d/<MyRegistry>:<Port>/client.cert` 和 `~/.docker/certs.d/<MyRegistry>:<Port>/client.key` 中。

当 Docker Desktop 应用启动时，它会将 Mac 上的 `~/.docker/certs.d` 文件夹复制到 Moby（Docker Desktop `xhyve` 虚拟机）上的 `/etc/docker/certs.d` 目录。

> [!NOTE]
>
> * 对密钥链或 `~/.docker/certs.d` 目录进行任何更改后，你需要重启 Docker Desktop 才能使更改生效。
>
> * 注册中心不能列为_不安全注册中心_。Docker Desktop 会忽略不安全注册中心下列出的证书，并且不会发送客户端证书。尝试从注册中心拉取的 `docker run` 等命令会在命令行以及注册中心上产生错误消息。

#### 证书的目录结构

如果你有以下目录结构，则无需手动将 CA 证书添加到 Mac OS 系统登录中：

```text
/Users/<user>/.docker/certs.d/
└── <MyRegistry>:<Port>
   ├── ca.crt
   ├── client.cert
   └── client.key
```

以下内容进一步说明并解释了具有自定义证书的配置：

```text
/etc/docker/certs.d/        <-- Certificate directory（证书目录）
└── localhost:5000          <-- Hostname:port（主机名:端口）
   ├── client.cert          <-- Client certificate（客户端证书）
   ├── client.key           <-- Client key（客户端密钥）
   └── ca.crt               <-- Certificate authority that signed
                                the registry certificate（签署注册中心证书的证书颁发机构）
```

你也可以有以下目录结构，只要 CA 证书也在你的密钥链中即可：

```text
/Users/<user>/.docker/certs.d/
└── <MyRegistry>:<Port>
    ├── client.cert
    └── client.key
```

要了解如何为注册中心安装 CA 根证书以及如何设置用于验证的客户端 TLS 证书的更多信息，请参阅 Docker Engine 主题中的 [使用证书验证仓库客户端](/manuals/engine/security/certificates.md)。