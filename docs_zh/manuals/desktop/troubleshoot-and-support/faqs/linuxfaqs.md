---
description: Docker Desktop for Linux 常见问题解答
keywords: desktop, linux, faqs
title: Docker Desktop for Linux 常见问题
linkTitle: Linux
tags: [FAQ]
aliases:
- /desktop/linux/space/
- /desktop/faqs/linuxfaqs/
weight: 40
---

### 为什么 Docker Desktop for Linux 需要运行虚拟机？

Docker Desktop for Linux 运行虚拟机（VM）的原因如下：

1. **确保跨平台的一致性体验。**

    在调研中，用户希望使用 Docker Desktop for Linux 最常提及的原因是确保 Docker Desktop 在所有主流操作系统上提供一致的体验和功能对等。使用虚拟机可以确保 Linux 用户的 Docker Desktop 体验与 Windows 和 macOS 用户高度一致。

2. **利用新的内核功能。**

    有时我们希望利用新的操作系统功能。由于我们可以控制虚拟机内的内核和操作系统，因此可以立即向所有用户推出这些功能，即使用户有意停留在其机器操作系统的 LTS 版本上。

3. **增强安全性。**

    容器镜像漏洞对主机环境构成安全风险。大量非官方镜像无法保证已验证已知漏洞。恶意用户可以向公共注册表推送镜像，并使用不同方法诱骗用户拉取和运行它们。虚拟机方法通过将获得 root 权限的恶意软件限制在虚拟机环境中（无法访问主机）来缓解这一威胁。

    为什么不运行无 root 权限的 Docker？虽然这在表面上限制了对 root 用户的访问，使“top”中的情况看起来更安全，但它允许无特权用户在自己的用户命名空间中获得 `CAP_SYS_ADMIN` 权限，并访问未预期由无特权用户使用的内核 API，从而导致 [漏洞](https://www.openwall.com/lists/oss-security/2022/01/18/7)。

4. **在最小化性能影响的前提下，提供功能对等和增强安全性的优势。**

    Docker Desktop for Linux 使用的虚拟机利用了 [`VirtioFS`](https://virtio-fs.gitlab.io)，这是一种共享文件系统，允许虚拟机访问位于主机上的目录树。我们的内部基准测试表明，在为虚拟机分配合适的资源后，VirtioFS 可以实现接近原生的文件系统性能。

    因此，我们调整了 Docker Desktop for Linux 中虚拟机的默认可用内存。您可以通过 Docker Desktop 的 **Settings** > **Resources** 选项卡中的 **Memory** 滑块根据自身需求调整此设置。

### 如何启用文件共享？

Docker Desktop for Linux 使用 [VirtioFS](https://virtio-fs.gitlab.io/) 作为默认（也是当前唯一）机制，在主机和 Docker Desktop 虚拟机之间启用文件共享。

{{< accordion title="Docker Desktop 4.34 及更早版本的附加信息" >}}

为了不依赖提升的权限，同时不无端限制共享文件上的操作，Docker Desktop 在用户命名空间（参见 `user_namespaces(7)`）内运行文件共享服务（`virtiofsd`），并配置了 UID 和 GID 映射。因此，Docker Desktop 依赖于主机配置，以启用当前用户使用从属 ID 委派。要满足此条件，必须存在 `/etc/subuid`（参见 `subuid(5)`）和 `/etc/subgid`（参见 `subgid(5)`）。Docker Desktop 仅支持通过文件配置的从属 ID 委派。Docker Desktop 将当前用户 ID 和 GID 映射为容器中的 0。它使用 `/etc/subuid` 和 `/etc/subgid` 中当前用户的第一条条目来设置容器中大于 0 的 ID 的映射。

| 容器中的 ID | 主机上的 ID                                                                       |
| --------------- | -------------------------------------------------------------------------------- |
| 0 (root)        | 运行 Docker Desktop 的用户 ID（例如 1000）                                            |
| 1               | 0 + `/etc/subuid`/`/etc/subgid` 中指定范围的起始 ID（例如 100000） |
| 2               | 1 + `/etc/subuid`/`/etc/subgid` 中指定范围的起始 ID（例如 100001） |
| 3               | 2 + `/etc/subuid`/`/etc/subgid` 中指定范围的起始 ID（例如 100002） |
| ...             | ...                                                                              |

如果缺少 `/etc/subuid` 和 `/etc/subgid`，则需要创建它们。两者都应包含格式为 `<username>:<id 范围起始>:<id 范围大小>` 的条目。例如，允许当前用户使用 100 000 到 165 535 的 ID：

```console
$ grep "$USER" /etc/subuid >> /dev/null 2&>1 || (echo "$USER:100000:65536" | sudo tee -a /etc/subuid)
$ grep "$USER" /etc/subgid >> /dev/null 2&>1 || (echo "$USER:100000:65536" | sudo tee -a /etc/subgid)
```

要验证配置是否正确创建，请检查其内容：

```console
$ echo $USER
exampleuser
$ cat /etc/subuid
exampleuser:100000:65536
$ cat /etc/subgid
exampleuser:100000:65536
```

在此场景中，如果在 Docker Desktop 容器内将共享文件 `chown` 给 UID 为 1000 的用户，则它在主机上显示为 UID 为 100999 的用户所有。这不幸地导致无法在主机上轻松访问该文件。通过为 Docker Desktop 虚拟机共享的文件夹创建具有新 GID 的组并添加用户，或设置递归 ACL（参见 `setfacl(1)`），可以解决此问题。

{{< /accordion >}}

### Docker Desktop 将 Linux 容器存储在哪里？

Docker Desktop 在 Linux 文件系统中的单个大型“磁盘镜像”文件中存储 Linux 容器和镜像。这与 Linux 上的 Docker 不同，后者通常将容器和镜像存储在主机文件系统上的 `/var/lib/docker` 目录中。

#### 磁盘镜像文件在哪里？

要定位磁盘镜像文件，请从 Docker Desktop 仪表板选择 **Settings**，然后从 **Resources** 选项卡选择 **Advanced**。

**Advanced** 选项卡显示磁盘镜像的位置。它还显示磁盘镜像的最大大小和磁盘镜像实际占用的空间。注意，其他工具可能以磁盘镜像文件的最大大小显示其空间使用情况，而非实际大小。

##### 如果文件过大怎么办？

如果磁盘镜像文件过大，您可以：

- 将其移动到更大的驱动器
- 删除不必要的容器和镜像
- 减少文件的最大允许大小

##### 如何将文件移动到更大的驱动器？

要将磁盘镜像文件移动到不同位置：

1. 选择 **Settings**，然后从 **Resources** 选项卡选择 **Advanced**。

2. 在 **Disk image location** 部分，选择 **Browse** 并选择磁盘镜像的新位置。

3. 选择 **Apply** 使更改生效。

不要直接在 Finder 中移动文件，这可能导致 Docker Desktop 无法跟踪该文件。

##### 如何删除不必要的容器和镜像？

检查是否有不必要的容器和镜像。如果您的客户端和守护进程 API 运行版本 1.25 或更高版本（在客户端上使用 `docker version` 命令检查客户端和守护进程 API 版本），可以通过运行以下命令查看详细的空间使用信息：

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

此命令删除所有已停止的容器、未使用的网络、悬空镜像和构建缓存。

根据磁盘镜像文件的格式，释放主机上的空间可能需要几分钟：

- 如果文件名为 `Docker.raw`：主机上的空间应在几秒内被回收。
- 如果文件名为 `Docker.qcow2`：空间将由后台进程在几分钟后释放。

只有在删除镜像时才会释放空间。在运行中的容器内删除文件不会自动释放空间。要在任何时候触发空间回收，请运行命令：

```console
$ docker run --privileged --pid=host docker/desktop-reclaim-space
```

注意，许多工具报告的是文件的最大大小，而非实际大小。要从终端查询主机上文件的实际大小，请运行：

```console
$ cd ~/.docker/desktop/vms/0/data
$ ls -klsh Docker.raw
2333548 -rw-r--r--@ 1 username  staff    64G Dec 13 17:42 Docker.raw
```

在此示例中，磁盘的实际大小为 `2333548` KB，而磁盘的最大大小为 `64` GB。

##### 如何减小文件的最大大小？

要减小磁盘镜像文件的最大大小：

1. 从 Docker Desktop 仪表板选择 **Settings**，然后从 **Resources** 选项卡选择 **Advanced**。

2. **Disk image size** 部分包含一个滑块，允许您更改磁盘镜像的最大大小。调整滑块以设置较低的限制。

3. 选择 **Apply**。

减小最大大小时，当前磁盘镜像文件将被删除，因此所有容器和镜像都会丢失。