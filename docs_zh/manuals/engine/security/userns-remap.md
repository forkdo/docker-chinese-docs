---
description: 在用户命名空间中隔离容器
keywords: security, namespaces
title: 使用用户命名空间隔离容器
---

Linux 命名空间为运行中的进程提供隔离，限制其对系统资源的访问，而进程本身并不会察觉到这些限制。有关 Linux 命名空间的更多信息，请参阅 [Linux 命名空间](https://www.linux.com/news/understanding-and-securing-linux-namespaces)。

防止容器内权限提升攻击的最佳方法是，将容器内的应用程序配置为以非特权用户身份运行。对于必须在容器内以 `root` 用户身份运行的容器进程，您可以将此用户重新映射到 Docker 主机上权限较低的用户。被映射的用户会被分配一个 UID 范围，该范围在命名空间内（如容器内）的功能与正常的 UID 范围（0 到 65536）相同，但在主机本身上没有任何权限。

## 关于重映射和从属用户与组 ID

重映射本身由两个文件处理：`/etc/subuid` 和 `/etc/subgid`。这两个文件的工作方式相同，但一个关注用户 ID 范围，另一个关注组 ID 范围。考虑 `/etc/subuid` 中的以下条目：

```text
testuser:231072:65536
```

这意味着 `testuser` 被分配了一个从属用户 ID 范围，起始值为 `231072`，后续连续 65536 个整数。UID `231072` 在命名空间内（本例中为容器内）被映射为 UID `0`（`root`）。UID `231073` 被映射为 UID `1`，依此类推。如果某个进程试图在命名空间之外提升权限，则该进程在主机上以一个无特权的、高数值的 UID 运行，该 UID 甚至不映射到真实用户。这意味着该进程在主机系统上完全没有任何权限。

> [!NOTE]
>
> 可以通过在 `/etc/subuid` 或 `/etc/subgid` 文件中为同一用户或组添加多个不重叠的映射，从而为指定用户或组分配多个从属范围。在这种情况下，Docker 仅使用前五个映射，这与内核对 `/proc/self/uid_map` 和 `/proc/self/gid_map` 仅允许五个条目的限制一致。

当您配置 Docker 使用 `userns-remap` 功能时，可以选择指定一个现有的用户和/或组，也可以指定 `default`。如果指定 `default`，则会创建一个用户和组 `dockremap` 并用于此目的。

> [!WARNING]
>
> 某些发行版不会自动将新组添加到 `/etc/subuid` 和 `/etc/subgid` 文件中。如果是这种情况，您可能需要手动编辑这些文件并分配不重叠的范围。此步骤在 [先决条件](#先决条件) 中有所介绍。

范围不重叠非常重要，以确保进程无法访问其他命名空间。在大多数 Linux 发行版中，当您添加或删除用户时，系统工具会自动为您管理这些范围。

这种重映射对容器是透明的，但在容器需要访问 Docker 主机上的资源（例如绑定挂载到系统用户无法写入的文件系统区域）的情况下，会带来一些配置复杂性。从安全角度来看，最好避免这些情况。

## 先决条件

1.  从属 UID 和 GID 范围必须与现有用户关联，即使这种关联是实现的细节。该用户拥有 `/var/lib/docker/` 下的命名空间存储目录。如果您不想使用现有用户，Docker 可以为您创建一个并使用。如果您想使用现有的用户名或用户 ID，则该用户必须已经存在。通常，这意味着相关条目需要位于 `/etc/passwd` 和 `/etc/group` 中，但如果您使用不同的身份验证后端，此要求可能会有所不同。

    要验证这一点，请使用 `id` 命令：

    ```console
    $ id testuser

    uid=1001(testuser) gid=1001(testuser) groups=1001(testuser)
    ```

2.  主机上处理命名空间重映射的方式是使用两个文件：`/etc/subuid` 和 `/etc/subgid`。这些文件通常在您添加或删除用户或组时自动管理，但在某些发行版中，您可能需要手动管理这些文件。

    每个文件包含三个字段：用户的用户名或 ID，后跟起始 UID 或 GID（在命名空间内被视为 UID 或 GID 0）以及该用户可用的 UID 或 GID 的最大数量。例如，给定以下条目：

    ```text
    testuser:231072:65536
    ```

    这意味着由 `testuser` 启动的用户命名空间进程，其主机 UID 范围为 `231072`（在命名空间内看起来像 UID `0`）到 `296607`（231072 + 65536 - 1）。这些范围不应重叠，以确保命名空间进程无法访问彼此的命名空间。

    添加用户后，请检查 `/etc/subuid` 和 `/etc/subgid`，查看您的用户是否在每个文件中都有条目。如果没有，则需要添加，并注意避免重叠。

    如果您想使用 Docker 自动创建的 `dockremap` 用户，请在配置并重启 Docker 后检查这些文件中是否存在 `dockremap` 条目。

3.  如果 Docker 主机上存在无特权用户需要写入的位置，请相应地调整这些位置的权限。如果您想使用 Docker 自动创建的 `dockremap` 用户，也是如此，但在配置并重启 Docker 之前，您无法修改权限。

4.  启用 `userns-remap` 会有效地屏蔽 `/var/lib/docker/` 中的现有镜像和容器层，以及其他 Docker 对象。这是因为 Docker 需要调整这些资源的所有权，并实际上将它们存储在 `/var/lib/docker/` 的子目录中。最好在新的 Docker 安装上启用此功能，而不是在现有安装上。

    同样，如果您禁用 `userns-remap`，则无法访问启用时创建的任何资源。

5.  检查用户命名空间的 [限制](#用户命名空间已知限制)，以确保您的用例是可行的。

## 在守护进程上启用 userns-remap

您可以使用 `--userns-remap` 标志启动 `dockerd`，或者按照以下步骤使用 `daemon.json` 配置文件配置守护进程。推荐使用 `daemon.json` 方法。如果使用标志，请使用以下命令作为模板：

```console
$ dockerd --userns-remap="testuser:testuser"
```

1.  编辑 `/etc/docker/daemon.json`。假设该文件之前为空，以下条目使用名为 `testuser` 的用户和组启用 `userns-remap`。您可以通过 ID 或名称指定用户和组。仅当组名或 ID 与用户名或 ID 不同时，才需要指定组名或 ID。如果同时提供用户名和组名或 ID，请使用冒号（`:`）分隔。假设 `testuser` 的 UID 和 GID 为 `1001`，以下所有格式都适用于该值：

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
    > 要使用 Docker 为您创建的 `dockremap` 用户，请将值设置为 `default` 而不是 `testuser`。

    保存文件并重启 Docker。

2.  如果您使用的是 `dockremap` 用户，请使用 `id` 命令验证 Docker 是否已创建该用户。

    ```console
    $ id dockremap

    uid=112(dockremap) gid=116(dockremap) groups=116(dockremap)
    ```

    验证 `/etc/subuid` 和 `/etc/subgid` 中是否已添加该条目：

    ```console
    $ grep dockremap /etc/subuid

    dockremap:231072:65536

    $ grep dockremap /etc/subgid

    dockremap:231072:65536
    ```

    如果这些条目不存在，请以 `root` 用户身份编辑文件，并分配一个起始 UID 和 GID，该值为已分配的最高值加上偏移量（本例中为 `65536`）。注意不要允许范围重叠。

3.  使用 `docker image ls` 命令验证之前的镜像是否不可用。输出应为空。

4.  从 `hello-world` 镜像启动一个容器。

    ```console
    $ docker run hello-world
    ```

5.  验证 `/var/lib/docker/` 中是否存在一个以命名空间用户的 UID 和 GID 命名的命名空间目录，该目录由该 UID 和 GID 拥有，并且不可被组或其他用户读取。某些子目录仍然由 `root` 拥有，并具有不同的权限。

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

    您的目录列表可能有一些差异，特别是如果您使用的容器存储驱动与 `aufs` 不同。

    由重映射用户拥有的目录用于替代 `/var/lib/docker/` 下的相同目录，未使用的版本（如本例中的 `/var/lib/docker/tmp/`）可以删除。在启用 `userns-remap` 时，Docker 不会使用它们。

## 为容器禁用命名空间重映射

如果在守护进程上启用了用户命名空间，则默认情况下所有容器都会启用用户命名空间。在某些情况下（如特权容器），您可能需要为特定容器禁用用户命名空间。有关其中一些限制，请参阅 [用户命名空间已知限制](#用户命名空间已知限制)。

要为特定容器禁用用户命名空间，请将 `--userns=host` 标志添加到 `docker container create`、`docker container run` 或 `docker container exec` 命令中。

使用此标志有一个副作用：该容器的用户重映射不会被启用，但由于只读（镜像）层在容器之间共享，容器文件系统的所有权仍会被重映射。

这意味着整个容器文件系统将属于 `--userns-remap` 守护进程配置中指定的用户（上例中为 `231072`）。这可能导致容器内程序的意外行为。例如，`sudo`（检查其二进制文件是否属于用户 `0`）或具有 `setuid` 标志的二进制文件。

## 用户命名空间已知限制

以下标准 Docker 功能与在启用用户命名空间的情况下运行 Docker 守护进程不兼容：

- 与主机共享 PID 或 NET 命名空间（`--pid=host` 或 `--network=host`）。
- 不了解或无法使用守护进程用户映射的外部（卷或存储）驱动。
- 在 `docker run` 上使用 `--privileged` 模式标志，但未同时指定 `--userns=host`。

用户命名空间是一项高级功能，需要与其他功能协调。例如，如果从主机挂载卷，则需要预先安排文件所有权，以便能够读取或写入卷内容。

虽然用户命名空间容器进程内的 root 用户在容器内拥有超级用户的许多预期权限，但 Linux 内核会根据内部知识（即这是一个用户命名空间进程）施加限制。一个显著的限制是无法使用 `mknod` 命令。当 `root` 用户在容器内运行时，设备创建权限被拒绝。