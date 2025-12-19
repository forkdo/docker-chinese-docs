---
description: Docker Desktop for Linux 的常见问题解答
keywords: desktop, linux, faqs
title: Docker Desktop for Linux 常见问题解答
linkTitle: Linux
tags: [FAQ]
aliases:
- /desktop/linux/space/
- /desktop/faqs/linuxfaqs/
weight: 40
---

### 为什么 Docker Desktop for Linux 要运行一个虚拟机 (VM)？

Docker Desktop for Linux 运行虚拟机 (VM) 的原因如下：

1.  **确保 Docker Desktop 跨平台体验一致。**

    在调研中，用户希望使用 Docker Desktop for Linux 的最常见原因是为了确保 Docker Desktop 在所有主流操作系统上具有一致的体验和功能对等性。使用虚拟机可以确保 Linux 用户的 Docker Desktop 体验与 Windows 和 macOS 用户非常接近。

2.  **利用新的内核特性。**

    有时我们需要利用新的操作系统特性。由于我们在虚拟机内部控制内核和操作系统，我们可以立即将这些特性推送给所有用户，即使是那些有意坚持使用其机器操作系统 LTS 版本的用户。

3.  **增强安全性。**

    容器镜像漏洞对主机环境构成安全风险。存在大量非官方镜像，无法保证已针对已知漏洞进行验证。恶意用户可以将镜像推送到公共注册表，并使用各种方法诱骗用户拉取并运行它们。虚拟机方法可以减轻这种威胁，因为任何获得 root 权限的恶意软件都会被限制在虚拟机环境中，无法访问主机。

    为什么不运行 rootless Docker？虽然这样做在表面上限制了对 root 用户的访问，使得在 "top" 中看起来更安全，但它允许无特权用户在其自己的用户命名空间中获得 `CAP_SYS_ADMIN` 并访问本不期望被无特权用户使用的内核 API，从而导致[漏洞](https://www.openwall.com/lists/oss-security/2022/01/18/7)。

4.  **在提供功能对等性和增强安全性的同时，将对性能的影响降至最低。**

    Docker Desktop for Linux 使用的虚拟机采用了 [`VirtioFS`](https://virtio-fs.gitlab.io)，这是一种共享文件系统，允许虚拟机访问主机上的目录树。我们的内部基准测试表明，只要为虚拟机分配适当的资源，使用 VirtioFS 就能获得接近原生文件系统的性能。

    因此，我们调整了 Docker Desktop for Linux 中虚拟机的默认可用内存。您可以使用 Docker Desktop **设置** > **资源**选项卡中的**内存**滑块，根据您的具体需求调整此设置。

### 如何启用文件共享？

Docker Desktop for Linux 使用 [VirtioFS](https://virtio-fs.gitlab.io/) 作为默认（也是目前唯一的）机制来启用主机和 Docker Desktop 虚拟机之间的文件共享。

{{< accordion title="Docker Desktop 4.34 及更早版本的附加信息" >}}

为了不使用提升的权限，同时又不必要地限制对共享文件的操作，Docker Desktop 在用户命名空间（参见 `user_namespaces(7)`）内运行文件共享服务 (`virtiofsd`)，并配置了 UID 和 GID 映射。因此，Docker Desktop 依赖于主机的配置，以允许当前用户使用从属 ID 委托。为此，`/etc/subuid`（参见 `subuid(5)`）和 `/etc/subgid`（参见 `subgid(5)`）必须存在。Docker Desktop 仅支持通过文件配置的从属 ID 委托。Docker Desktop 将当前用户 ID 和 GID 映射到容器中的 0。它使用 `/etc/subuid` 和 `/etc/subgid` 中对应当前用户的第一条记录来设置容器中大于 0 的 ID 的映射。

| 容器中的 ID | 主机上的 ID                                                                       |
| --------------- | -------------------------------------------------------------------------------- |
| 0 (root)        | 运行 Docker Desktop 的用户 ID (例如 1000)                                            |
| 1               | 0 + `/etc/subuid`/`/etc/subgid` 中指定的 ID 范围的起始值 (例如 100000) |
| 2               | 1 + `/etc/subuid`/`/etc/subgid` 中指定的 ID 范围的起始值 (例如 100001) |
| 3               | 2 + `/etc/subuid`/`/etc/subgid` 中指定的 ID 范围的起始值 (例如 100002) |
| ...             | ...                                                                              |

如果 `/etc/subuid` 和 `/etc/subgid` 不存在，则需要创建它们。两者都应包含以下格式的条目：
`<用户名>:<ID 范围起始值>:<ID 范围大小>`。例如，要允许当前用户使用从 100000 到 165535 的 ID：

```console
$ grep "$USER" /etc/subuid >> /dev/null 2&>1 || (echo "$USER:100000:65536" | sudo tee -a /etc/subuid)
$ grep "$USER" /etc/subgid >> /dev/null 2&>1 || (echo "$USER:100000:65536" | sudo tee -a /etc/subgid)
```

要验证配置是否已正确创建，请检查其内容：

```console
$ echo $USER
exampleuser
$ cat /etc/subuid
exampleuser:100000:65536
$ cat /etc/subgid
exampleuser:100000:65536
```

在这种情况下，如果在 Docker Desktop 容器内将共享文件 `chown` 给一个 UID 为 1000 的用户，它在主机上显示为由一个 UID 为 100999 的用户拥有。这会产生一个不利的副作用，即阻止在主机上轻松访问此类文件。通过创建一个具有新 GID 的组并将我们的用户添加到该组中，或者通过为与 Docker Desktop 虚拟机共享的文件夹设置递归 ACL（参见 `setfacl(1)`），可以解决此问题。

{{< /accordion >}}

### Docker Desktop 将 Linux 容器存储在哪里？

Docker Desktop 将 Linux 容器和镜像存储在 Linux 文件系统中的一个单一、巨大的 "磁盘镜像" 文件中。这与 Linux 上的 Docker 不同，后者通常将容器和镜像存储在主机文件系统的 `/var/lib/docker` 目录中。

#### 磁盘镜像文件在哪里？

要定位磁盘镜像文件，请从 Docker Desktop 仪表板中选择**设置**，然后从**资源**选项卡中选择**高级**。

**高级**选项卡会显示磁盘镜像的位置。它还会显示磁盘镜像的最大大小以及磁盘镜像实际消耗的空间。请注意，其他工具可能会根据文件的最大大小而不是实际文件大小来显示空间使用情况。

##### 如果文件太大怎么办？

如果磁盘镜像文件太大，您可以：

- 将其移动到更大的驱动器
- 删除不必要的容器和镜像
- 减小文件的最大允许大小

##### 如何将文件移动到更大的驱动器？

要将磁盘镜像文件移动到其他位置：

1.  选择**设置**，然后从**资源**选项卡中选择**高级**。
2.  在**磁盘镜像位置**部分，选择**浏览**并为磁盘镜像选择一个新位置。
3.  选择**应用**以使更改生效。

请勿直接在 Finder 中移动文件，这可能导致 Docker Desktop 无法追踪该文件。

##### 如何删除不必要的容器和镜像？

检查您是否有任何不必要的容器和镜像。如果您的客户端和守护程序 API 运行的是 1.25 或更高版本（在客户端上使用 `docker version` 命令检查您的客户端和守护程序 API 版本），您可以通过运行以下命令查看详细的空间使用信息：

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

如果存在大量冗余对象，请运行命令：

```console
$ docker system prune
```

此命令将移除所有已停止的容器、未使用的网络、悬空的镜像和构建缓存。

根据磁盘镜像文件的格式，回收主机空间可能需要几分钟时间：

- 如果文件名为 `Docker.raw`：主机上的空间将在几秒钟内回收。
- 如果文件名为 `Docker.qcow2`：空间将在几分钟后由后台进程释放。

空间仅在删除镜像时释放。在运行的容器内删除文件时，空间不会自动释放。要在任何时候触发空间回收，请运行命令：

```console
$ docker run --privileged --pid=host docker/desktop-reclaim-space
```

请注意，许多工具报告的是文件的最大大小，而不是实际文件大小。
要从终端查询主机上文件的实际大小，请运行：

```console
$ cd ~/.docker/desktop/vms/0/data
$ ls -klsh Docker.raw
2333548 -rw-r--r--@ 1 username  staff    64G Dec 13 17:42 Docker.raw
```

在此示例中，磁盘的实际大小为 `2333548` KB，而磁盘的最大大小为 `64` GB。

##### 如何减小文件的最大大小？

要减小磁盘镜像文件的最大大小：

1.  从 Docker Desktop 仪表板中选择**设置**，然后从**资源**选项卡中选择**高级**。
2.  **磁盘镜像大小**部分包含一个滑块，允许您更改磁盘镜像的最大大小。调整滑块以设置更低的限制。
3.  选择**应用**。

当您减小最大大小时，当前的磁盘镜像文件将被删除，因此，所有容器和镜像都会丢失。