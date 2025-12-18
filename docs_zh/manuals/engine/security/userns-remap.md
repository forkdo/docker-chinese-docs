---
description: 在用户命名空间中隔离容器
keywords: 安全, 命名空间
title: 使用用户命名空间隔离容器
---

Linux 命名空间为运行中的进程提供隔离，限制它们对系统资源的访问，而运行中的进程本身并不感知这些限制。有关 Linux 命名空间的更多信息，请参阅 [Linux 命名空间](https://www.linux.com/news/understanding-and-securing-linux-namespaces)。

防止容器内发生特权提升攻击的最佳方法是将容器的应用程序配置为以非特权用户身份运行。对于必须在容器内以 `root` 用户身份运行的容器，你可以将此用户重新映射为 Docker 主机上的一个权限较低的用户。映射的用户被分配一个 UID 范围，这些 UID 在命名空间内正常工作，范围从 0 到 65536，但在主机本身上没有任何特权。

## 关于重新映射和辅助用户及组 ID

重新映射本身由两个文件处理：`/etc/subuid` 和 `/etc/subgid`。每个文件的工作原理相同，但一个关注用户 ID 范围，另一个关注组 ID 范围。考虑 `/etc/subuid` 中的以下条目：

```text
testuser:231072:65536
```

这意味着 `testuser` 被分配了一个从 `231072` 开始的连续 65536 个整数的辅助用户 ID 范围。UID `231072` 在命名空间内（在本例中即容器内）被映射为 UID `0`（`root`）。UID `231073` 被映射为 UID `1`，依此类推。如果一个进程试图在命名空间外提升特权，该进程在主机上运行时使用的是一个无特权的高编号 UID，甚至不映射到真实的用户。这意味着该进程在主机系统上完全没有特权。

> [!NOTE]
>
> 可以通过在 `/etc/subuid` 或 `/etc/subgid` 文件中为同一用户或组添加多个不重叠的映射，来为给定用户或组分配多个辅助范围。在这种情况下，Docker 仅使用前五个映射，以符合内核对 `/proc/self/uid_map` 和 `/proc/self/gid_map` 中仅允许五条条目的限制。

当你配置 Docker 使用 `userns-remap` 功能时，你可以选择指定一个现有的用户和/或组，也可以指定 `default`。如果你指定 `default`，会创建并使用一个名为 `dockremap` 的用户和组来实现此目的。

> [!WARNING]
>
> 某些发行版不会自动将新组添加到 `/etc/subuid` 和 `/etc/subgid` 文件中。如果是这种情况，你可能需要手动编辑这些文件并分配不重叠的范围。这一步骤在[先决条件](#prerequisites)中涵盖。

这些范围非常重要，不能重叠，以确保进程无法在不同的命名空间中获得访问权限。在大多数 Linux 发行版上，系统工具在添加或删除用户时会自动管理这些范围。

这种重新映射对容器是透明的，但在容器需要访问主机资源的情况下（例如绑定挂载到系统用户无法写入的文件系统区域）会引入一些配置复杂性。从安全角度来看，最好避免这些情况。

## 先决条件

1.  辅助 UID 和 GID 范围必须与现有用户关联，即使这种关联是一个实现细节。该用户拥有 `/var/lib/docker/` 下的命名空间存储目录。如果你不想使用现有用户，Docker 可以为你创建一个并使用它。如果你想使用现有的用户名或用户 ID，它必须已经存在。通常，这意味着相关条目需要在 `/etc/passwd` 和 `/etc/group` 中，但如果你使用的是不同的身份验证后端，此要求可能会有所不同。

    要验证这一点，请使用 `id` 命令：

    ```console
    $ id testuser

    uid=1001(testuser) gid=1001(testuser) groups=1001(testuser)
    ```

2.  在主机上处理命名空间重新映射的方式是使用两个文件：`/etc/subuid` 和 `/etc/subgid`。这些文件通常在添加或删除用户或组时自动管理，但在某些发行版上，你可能需要手动管理这些文件。

    每个文件包含三个字段：用户名或用户 ID，后跟一个起始 UID 或 GID（在命名空间内被视为 UID 或 GID 0）以及该用户可用的最大 UID 或 GID 数量。例如，给定以下条目：

    ```text
    testuser:231072:65536
    ```

    这意味着由 `testuser` 启动的用户命名空间进程由主机 UID `231072`（在命名空间内看起来像 UID `0`）到 296607（231072 + 65536 - 1）拥有。这些范围不应重叠，以确保命名空间进程无法访问彼此的命名空间。

    添加用户后，检查 `/etc/subuid` 和 `/etc/subgid`，查看你的用户是否在每个文件中都有条目。如果没有，你需要添加它，注意避免重叠。

    如果你想使用 Docker 自动创建的 `dockremap` 用户，请在配置并重启 Docker 后检查这些文件中的 `dockremap` 条目。

3.  如果 Docker 主机上有任何位置需要无特权用户写入，请相应地调整这些位置的权限。如果你想使用 Docker 自动创建的 `dockremap` 用户也是如此，但你必须在配置并重启 Docker 后才能修改权限。

4.  启用 `userns-remap` 实际上会屏蔽 `/var/lib/docker/` 内的现有镜像和容器层，以及其他 Docker 对象。这是因为 Docker 需要调整这些资源的所有权，并实际上将它们存储在 `/var/lib/docker/` 内的一个子目录中。最好在新的 Docker 安装上启用此功能，而不是在现有安装上。

    同样，如果你禁用 `userns-remap`，就无法访问启用时创建的任何资源。

5.  检查用户命名空间的[限制](#user-namespace-known-limitations)，确保你的用例是可行的。

## 在守护进程上启用 userns-remap

你可以使用 `--userns-remap` 标志启动 `dockerd`，或者按照以下步骤使用 `daemon.json` 配置文件配置守护进程。建议使用 `daemon.json` 方法。如果你使用标志，请使用以下命令作为模型：

```console
$ dockerd --userns-remap="testuser:testuser"
```

1.  编辑 `/etc/docker/daemon.json`。假设文件之前为空，以下条目使用名为 `testuser` 的用户和组启用 `userns-remap`。你可以通过 ID 或名称引用用户和组。如果用户和组的名称或 ID 不同，才需要指定组名或 ID。如果同时提供用户名和组名或 ID，用冒号（`:`）字符分隔。以下所有格式都适用于该值，假设 `testuser` 的 UID 和 GID 为 `1001`：

    - `testuser`
    - `testuser:testuser`
    - `1001`
    - `1001:1001`
    - `testuser:1001`
    - `1001:testuser`

    ```json
    {
      "userns-remap": "testuser"
    }
    ```

    > [!NOTE]
    >
    > 要使用 `dockremap` 用户并让 Docker 为你创建它，请将值设置为 `default` 而不是 `testuser`。

    保存文件并重启 Docker。

2.  如果你使用的是 `dockremap` 用户，请使用 `id` 命令验证 Docker 是否创建了它。

    ```console
    $ id dockremap

    uid=112(dockremap) gid=116(dockremap) groups=116(dockremap)
    ```

    验证条目是否已添加到 `/etc/subuid` 和 `/etc/subgid`：

    ```console
    $ grep dockremap /etc/subuid

    dockremap:231072:65536

    $ grep dockremap /etc/subgid

    dockremap:231072:65536
    ```

    如果这些条目不存在，请以 `root` 用户身份编辑文件，并将起始 UID 和 GID 分配为最高分配值加偏移量（在本例中为 `65536`）。注意不要允许范围重叠。

3.  使用 `docker image ls` 命令验证之前的镜像是否不可用。输出应为空。

4.  从 `hello-world` 镜像启动一个容器。

    ```console
    $ docker run hello-world
    ```

5.  验证在 `/var/lib/docker/` 内是否存在一个以命名空间用户的 UID 和 GID 命名的命名空间目录，该目录由该 UID 和 GID 拥有，并且不被组或其他用户读取。某些子目录仍然由 `root` 拥有，并具有不同的权限。

    ```console
    $ sudo ls -ld /var/lib/docker/231072.231072/

    drwx------ 11 231072 231072 11 Jun 21 21:19 /var/lib/docker/231072.231072/

    $ sudo ls -l /var/lib/docker/231072.231072/

    total 14
    drwx------ 5 231072 231072 5 Jun 21 21:19 aufs
    drwx------ 3 231072 231072 3 Jun 21 21:21 containers
    drwx------ 3 root   root   3 Jun 21 21:19 image
    drwxr-x--- 3 root   root   3 Jun 21 21:19 network
    drwx------ 4 root   root   4 Jun 21 21:19 plugins
    drwx------ 2 root   root   2 Jun 21 21:19 swarm
    drwx------ 2 231072 231072 2 Jun 21 21:21 tmp
    drwx------ 2 root   root   2 Jun 21 21:19 trust
    drwx------ 2 231072 231072 3 Jun 21 21:19 volumes
    ```

    你的目录列表可能有一些差异，特别是如果你使用了不同于 `aufs` 的容器存储驱动程序。

    由重新映射用户拥有的目录被用来替代 `/var/lib/docker/` 下的同名目录，未使用的版本（如本例中的 `/var/lib/docker/tmp/`）可以被删除。启用 `userns-remap` 时，Docker 不会使用它们。

## 为容器禁用命名空间重新映射

如果你在守护进程上启用了用户命名空间，所有容器默认都会启用用户命名空间启动。在某些情况下，例如特权容器，你可能需要为特定容器禁用用户命名空间。请参阅 [用户命名空间已知限制](#user-namespace-known-limitations) 了解其中一些限制。

要为特定容器禁用用户命名空间，请在 `docker container create`、`docker container run` 或 `docker container exec` 命令中添加 `--userns=host` 标志。

使用此标志时会有一个副作用：该容器不会启用用户重新映射，但由于只读（镜像）层在容器之间共享，容器文件系统的所有权仍会被重新映射。

这意味着容器文件系统将属于 `--userns-remap` 守护进程配置中指定的用户（在上面的示例中为 `231072`）。这可能导致容器内程序出现意外行为。例如 `sudo`（它检查其二进制文件是否属于用户 `0`）或带有 `setuid` 标志的二进制文件。

## 用户命名空间已知限制

以下标准 Docker 功能与启用用户命名空间的 Docker 守护进程不兼容：

- 与主机共享 PID 或 NET 命名空间（`--pid=host` 或 `--network=host`）。
- 不了解或无法使用守护进程用户映射的外部（卷或存储）驱动程序。
- 在 `docker run` 上使用 `--privileged` 模式标志时，未同时指定 `--userns=host`。

用户命名空间是一个高级功能，需要与其他功能协调。例如，如果从主机挂载卷，必须预先安排文件所有权，如果你需要对卷内容的读或写访问权限。虽然用户命名空间容器进程内的 root 用户在容器内具有超级用户所需的许多特权，但 Linux 内核会基于内部知识（知道这是一个用户命名空间进程）施加限制。一个显著的限制是无法使用 `mknod` 命令。当由容器内的 `root` 用户运行时，会拒绝创建设备的权限。