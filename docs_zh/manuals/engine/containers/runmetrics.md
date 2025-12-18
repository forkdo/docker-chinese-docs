---
description: 了解如何测量正在运行的容器及其不同的指标
keywords: docker, 指标, CPU, 内存, 磁盘, IO, run, runtime, stats
title: 运行时指标
weight: 50
aliases:
  - /articles/runmetrics/
  - /engine/articles/run_metrics/
  - /engine/articles/runmetrics/
  - /engine/admin/runmetrics/
  - /config/containers/runmetrics/
---

## Docker 统计信息

你可以使用 `docker stats` 命令实时流式传输容器的运行时指标。该命令支持 CPU、内存使用量、内存限制和网络 IO 指标。

以下是 `docker stats` 命令的示例输出：

```console
$ docker stats redis1 redis2

CONTAINER           CPU %               MEM USAGE / LIMIT     MEM %               NET I/O             BLOCK I/O
redis1              0.07%               796 KB / 64 MB        1.21%               788 B / 648 B       3.568 MB / 512 KB
redis2              0.07%               2.746 MB / 64 MB      4.29%               1.266 KB / 648 B    12.4 MB / 0 B
```

[`docker stats`](/reference/cli/docker/container/stats.md) 参考页面提供了更多关于 `docker stats` 命令的详细信息。

## 控制组

Linux 容器依赖于 [控制组](https://www.kernel.org/doc/Documentation/cgroup-v1/cgroups.txt)，它们不仅跟踪进程组，还暴露 CPU、内存和块 I/O 使用情况的指标。你可以访问这些指标，同时获得网络使用情况指标。这对于“纯”LXC 容器以及 Docker 容器都是相关的。

控制组通过伪文件系统暴露。在现代发行版中，你应该在 `/sys/fs/cgroup` 下找到这个文件系统。在该目录下，你会看到多个子目录，如 `devices`、`freezer`、`blkio` 等。每个子目录实际上对应一个不同的 cgroup 层级。

在较老的系统上，控制组可能挂载在 `/cgroup`，没有独立的层级。在这种情况下，你不会看到子目录，而是看到该目录下的许多文件，以及可能对应现有容器的一些目录。

要找出控制组挂载在哪里，你可以运行：

```console
$ grep cgroup /proc/mounts
```

### 枚举 cgroups

cgroup 的文件布局在 v1 和 v2 版本之间有显著差异。

如果你的系统上存在 `/sys/fs/cgroup/cgroup.controllers`，你使用的是 v2 版本，否则你使用的是 v1 版本。请参考与你的 cgroup 版本对应的子部分。

以下发行版默认使用 cgroup v2：

- Fedora（自 31 版起）
- Debian GNU/Linux（自 11 版起）
- Ubuntu（自 21.10 起）

#### cgroup v1

你可以查看 `/proc/cgroups` 来查看系统已知的不同控制组子系统、它们所属的层级以及包含的组数。

你也可以查看 `/proc/<pid>/cgroup` 来查看进程所属的控制组。控制组显示为相对于层级挂载点根目录的路径。`/` 表示进程未被分配到组，而 `/lxc/pumpkin` 表示进程是名为 `pumpkin` 的容器的成员。

#### cgroup v2

在使用 cgroup v2 的主机上，`/proc/cgroups` 的内容没有意义。请查看 `/sys/fs/cgroup/cgroup.controllers` 以获取可用的控制器。

### 更改 cgroup 版本

更改 cgroup 版本需要重启整个系统。

在基于 systemd 的系统上，可以通过在内核命令行中添加 `systemd.unified_cgroup_hierarchy=1` 来启用 cgroup v2。要将 cgroup 版本恢复到 v1，你需要设置 `systemd.unified_cgroup_hierarchy=0`。

如果系统上可用 `grubby` 命令（例如在 Fedora 上），可以通过以下方式修改命令行：

```console
$ sudo grubby --update-kernel=ALL --args="systemd.unified_cgroup_hierarchy=1"
```

如果 `grubby` 命令不可用，请编辑 `/etc/default/grub` 中的 `GRUB_CMDLINE_LINUX` 行并运行 `sudo update-grub`。

### 在 cgroup v2 上运行 Docker

Docker 自 20.10 版本起支持 cgroup v2。在 cgroup v2 上运行 Docker 还需要满足以下条件：

- containerd：v1.4 或更高版本
- runc：v1.0.0-rc91 或更高版本
- 内核：v4.15 或更高版本（推荐 v5.2 或更高版本）

请注意，cgroup v2 模式与 cgroup v1 模式的行为略有不同：

- 默认 cgroup 驱动（`dockerd --exec-opt native.cgroupdriver`）在 v2 上是 `systemd`，在 v1 上是 `cgroupfs`。
- 默认 cgroup 命名空间模式（`docker run --cgroupns`）在 v2 上是 `private`，在 v1 上是 `host`。
- `docker run` 标志 `--oom-kill-disable` 和 `--kernel-memory` 在 v2 上被丢弃。

### 查找给定容器的 cgroup

对于每个容器，在每个层级中创建一个 cgroup。在使用较老版本 LXC 用户空间工具的较老系统上，cgroup 的名称是容器的名称。使用更新版本的 LXC 工具时，cgroup 是 `lxc/<container_name>`。

对于使用 cgroups 的 Docker 容器，cgroup 名称是容器的完整 ID 或长 ID。如果容器在 `docker ps` 中显示为 ae836c95b4c3，其长 ID 可能是类似 `ae836c95b4c3c9e9179e0e91015512da89fdec91612f63cebae57df9a5444c79` 的内容。你可以通过 `docker inspect` 或 `docker ps --no-trunc` 找到它。

将所有内容整合在一起，查看 Docker 容器的内存指标，请查看以下路径：

- `/sys/fs/cgroup/memory/docker/<longid>/` 在 cgroup v1，`cgroupfs` 驱动上
- `/sys/fs/cgroup/memory/system.slice/docker-<longid>.scope/` 在 cgroup v1，`systemd` 驱动上
- `/sys/fs/cgroup/docker/<longid>/` 在 cgroup v2，`cgroupfs` 驱动上
- `/sys/fs/cgroup/system.slice/docker-<longid>.scope/` 在 cgroup v2，`systemd` 驱动上

### 来自 cgroups 的指标：内存、CPU、块 I/O

> [!NOTE]
>
> 本节尚未更新为 cgroup v2。有关 cgroup v2 的更多信息，请参考 [内核文档](https://www.kernel.org/doc/html/latest/admin-guide/cgroup-v2.html)。

对于每个子系统（内存、CPU 和块 I/O），存在一个或多个包含统计信息的伪文件。

#### 内存指标：`memory.stat`

内存指标在 `memory` cgroup 中找到。内存控制组增加了少量开销，因为它对主机上的内存使用情况进行非常细粒度的统计。因此，许多发行版选择默认不启用它。通常，要启用它，你只需添加一些内核命令行参数：`cgroup_enable=memory swapaccount=1`。

指标在伪文件 `memory.stat` 中。它看起来像这样：

    cache 11492564992
    rss 1930993664
    mapped_file 306728960
    pgpgin 406632648
    pgpgout 403355412
    swap 0
    pgfault 728281223
    pgmajfault 1724
    inactive_anon 46608384
    active_anon 1884520448
    inactive_file 7003344896
    active_file 4489052160
    unevictable 32768
    hierarchical_memory_limit 9223372036854775807
    hierarchical_memsw_limit 9223372036854775807
    total_cache 11492564992
    total_rss 1930993664
    total_mapped_file 306728960
    total_pgpgin 406632648
    total_pgpgout 403355412
    total_swap 0
    total_pgfault 728281223
    total_pgmajfault 1724
    total_inactive_anon 46608384
    total_active_anon 1884520448
    total_inactive_file 7003344896
    total_active_file 4489052160
    total_unevictable 32768

前半部分（没有 `total_` 前缀）包含与 cgroup 内进程相关的统计信息，不包括子组。后半部分（带有 `total_` 前缀）包括子组。

某些指标是“仪表”，或可以增加或减少的值。例如，`swap` 是 cgroup 成员使用的交换空间量。其他一些是“计数器”，或只能增加的值，因为它们表示特定事件的发生次数。例如，`pgfault` 表示 cgroup 进程触发“页面错误”的次数。

`cache`
: 进程组使用的可以与块设备上的块精确关联的内存量。当你从磁盘读取和写入文件时，此数量会增加。如果你使用“常规”I/O（`open`、`read`、`write` 系统调用）以及映射文件（使用 `mmap`），就会发生这种情况。它还计算 `tmpfs` 挂载使用的内存，尽管原因尚不清楚。

`rss`
: 不对应磁盘上任何内容的内存量：栈、堆和匿名内存映射。

`mapped_file`
: 指示 cgroup 中进程映射的内存量。它不提供关于使用了多少内存的信息；它只是告诉你如何使用。

`pgfault`、`pgmajfault`
: 指示 cgroup 进程触发“页面错误”和“主要错误”的次数。页面错误发生在进程访问不存在或受保护的虚拟内存空间部分时。如果进程试图访问无效地址（它会收到 `SIGSEGV` 信号，通常会以著名的 `Segmentation fault` 消息终止），前者可能发生。后者可能发生在进程从已交换出去或对应映射文件的内存区域读取时：在这种情况下，内核从磁盘加载页面，并让 CPU 完成内存访问。当进程写入写时复制内存区域时也可能发生：同样，内核抢占进程，复制内存页面，并在进程自己的页面副本上恢复写操作。“主要”错误发生在内核实际需要从磁盘读取数据时。当它只是复制现有页面或分配空页面时，它是一个常规（或“次要”）错误。

`swap`
: 当前由 cgroup 中进程使用的交换空间量。

`active_anon`、`inactive_anon`
: 内核已识别为分别为 _active_ 和 _inactive_ 的匿名内存量。“匿名”内存是与磁盘页面无关的内存。换句话说，这相当于上面描述的 rss 计数器。实际上，rss 计数器的定义是 `active_anon` + `inactive_anon` - `tmpfs`（其中 tmpfs 是此控制组挂载的 `tmpfs` 文件系统使用的内存量）。那么，“active”和“inactive”之间有什么区别？页面最初是“active”；在定期间隔，内核会扫描内存，并将一些页面标记为“inactive”。每当它们再次被访问时，它们会立即被重新标记为“active”。当内核几乎耗尽内存时，需要将页面交换到磁盘时，内核会交换“inactive”页面。

`active_file`、`inactive_file`
: 缓存内存，具有与上述 _anon_ 内存类似的 _active_ 和 _inactive_。确切的公式是 `cache` = `active_file` + `inactive_file` + `tmpfs`。内核在主动和非主动集之间移动内存页面所使用的精确规则与用于匿名内存的规则不同，但一般原则是相同的。当内核需要回收内存时，从这个池中回收一个干净的（=未修改的）页面更便宜，因为可以立即回收它（而匿名页面和脏/修改的页面需要先写入磁盘）。

`unevictable`
: 无法回收的内存量；通常，它用于通过 `mlock` “锁定”的内存。它通常被加密框架使用，以确保密钥和其他敏感材料永远不会被交换到磁盘。

`memory_limit`、`memsw_limit`
: 这些不是真正的指标，而是对应用于此 cgroup 的限制的提醒。第一个指示 cgroup 进程可以使用的最大物理内存量；第二个指示可以使用的最大 RAM+swap 量。

页面缓存中的内存统计非常复杂。如果不同控制组中的两个进程都读取同一个文件（最终依赖于磁盘上的相同块），相应的内存费用会在控制组之间分割。这很好，但也意味着当一个 cgroup 被终止时，它可能会增加另一个 cgroup 的内存使用量，因为它们不再为那些内存页面分担费用。

### CPU 指标：`cpuacct.stat`

现在我们已经涵盖了内存指标，其他一切都相对简单。CPU 指标在 `cpuacct` 控制器中找到。

对于每个容器，伪文件 `cpuacct.stat` 包含容器进程累积的 CPU 使用量，按 `user` 和 `system` 时间分解。区别在于：

- `user` 时间是进程直接控制 CPU 执行进程代码的时间量。
- `system` 时间是内核代表进程执行系统调用的时间。

这些时间以 1/100 秒的“tick”表示，也称为“用户 jiffy”。每秒有 `USER_HZ` 个“jiffy”，在 x86 系统上，`USER_HZ` 是 100。从历史上看，这正好映射到每个秒的调度器“tick”数，但更高频率的调度和 [无 tick 内核](https://lwn.net/Articles/549580/) 已经使 tick 数变得无关紧要。

#### 块 I/O 指标

块 I/O 在 `blkio` 控制器中统计。不同的指标分散在不同的文件中。虽然你可以在内核文档的 [blkio-controller](https://www.kernel.org/doc/Documentation/cgroup-v1/blkio-controller.txt) 文件中找到详细的细节，但这里是一个最相关指标的简短列表：

`blkio.sectors`
: 包含 cgroup 进程读取和写入的 512 字节扇区数，按设备分解。读取和写入合并到一个计数器中。

`blkio.io_service_bytes`
: 指示 cgroup 读取和写入的字节数。每个设备有 4 个计数器，因为对于每个设备，它区分同步与异步 I/O，以及读取与写入。

`blkio.io_serviced`
: 执行的 I/O 操作数，不考虑其大小。每个设备也有 4 个计数器。

`blkio.io_queued`
: 指示当前为此 cgroup 排队的 I/O 操作数。换句话说，如果 cgroup 没有执行任何 I/O，这个值为零。相反的情况不一定成立。换句话说，如果没有 I/O 排队，这并不意味着 cgroup 是空闲的（在 I/O 方面）。它可能在完全同步地对一个否则空闲的设备执行读取，因此可以直接处理它们，而无需排队。此外，虽然它有助于确定哪个 cgroup 正在对 I/O 子系统施加压力，但请记住它是一个相对量。即使进程组不执行更多 I/O，其队列大小也可能因为设备负载增加而增加，这是由于其他设备造成的。

### 网络指标

网络指标不直接由控制组暴露。这有一个很好的解释：网络接口存在于 _网络命名空间_ 的上下文中。内核可能能够累积关于组进程发送和接收的数据包和字节数的指标，但这些指标不会非常有用。你希望有每个接口的指标（因为在本地 `lo` 接口上发生的流量不算）。但由于单个 cgroup 中的进程可能属于多个网络命名空间，这些指标会更难解释：多个网络命名空间意味着多个 `lo` 接口，可能还有多个 `eth0` 接口等；这就是为什么没有简单的方法来使用控制组收集网络指标。

相反，你可以从其他来源收集网络指标。

#### iptables

iptables（或更准确地说，netfilter 框架，iptables 只是其接口）可以进行一些认真的统计。

例如，你可以设置一个规则来统计 Web 服务器上的出站 HTTP 流量：

```console
$ iptables -I OUTPUT -p tcp --sport 80
```

没有 `-j` 或 `-g` 标志，所以规则只是计算匹配的数据包并转到下一条规则。

稍后，你可以使用以下命令检查计数器的值：

```console
$ iptables -nxvL OUTPUT
```

从技术上讲，`-n` 不是必需的，但它可以防止 iptables 执行 DNS 反向查找，这在当前场景中可能是无用的。

计数器包括数据包和字节数。如果你想通过