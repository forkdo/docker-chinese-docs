---
description: 在 Docker 中启用 seccomp
keywords: seccomp, 安全, docker, 文档
title: Docker 的 Seccomp 安全配置文件
---

安全计算模式（`seccomp`）是 Linux 内核的一项功能。您可以使用它来限制容器内的操作。`seccomp()` 系统调用作用于调用进程的 seccomp 状态。您可以使用此功能来限制应用程序的访问。

只有在 Docker 使用 `seccomp` 编译且内核配置了 `CONFIG_SECCOMP` 时，此功能才可用。要检查您的内核是否支持 `seccomp`：

```console
$ grep CONFIG_SECCOMP= /boot/config-$(uname -r)
CONFIG_SECCOMP=y
```

## 为容器传递配置文件

[默认 `seccomp` 配置文件](https://github.com/moby/profiles/blob/main/seccomp/default.json)
为使用 seccomp 运行容器提供了一个合理的默认值，默认情况下禁用了大约 44 个系统调用（总共约 300 多个）。它在提供广泛应用程序兼容性的同时，具有适度的保护作用。

实际上，该配置文件是一个允许列表，默认拒绝访问系统调用，然后允许特定的系统调用。配置文件通过定义 `defaultAction` 为 `SCMP_ACT_ERRNO` 并仅对特定系统调用覆盖该操作来实现。`SCMP_ACT_ERRNO` 的效果是导致“权限被拒绝”错误。接下来，配置文件定义了一个特定的系统调用列表，这些调用被完全允许，因为它们的 `action` 被覆盖为 `SCMP_ACT_ALLOW`。最后，一些特定规则针对诸如 `personality` 等个别系统调用，允许这些系统调用在特定参数下的变体。

`seccomp` 对于以最小权限运行 Docker 容器至关重要。不建议更改默认的 `seccomp` 配置文件。

当您运行容器时，除非使用 `--security-opt` 选项覆盖，否则它会使用默认配置文件。例如，以下命令显式指定了一个策略：

```console
$ docker run --rm \
             -it \
             --security-opt seccomp=/path/to/seccomp/profile.json \
             hello-world
```

### 默认配置文件阻止的重要系统调用

Docker 的默认 seccomp 配置文件是一个允许列表，指定了允许的调用。下表列出了由于不在允许列表上而被有效阻止的显著（但不是全部）系统调用。表中包括每个系统调用被阻止而不是被列入白名单的原因。

| 系统调用            | 描述                                                                                                                                                                                                                                    |
| ------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `acct`              | 会计系统调用，可能允许容器禁用自身的资源限制或进程会计。也受 `CAP_SYS_PACCT` 限制。                                                                                                                                                           |
| `add_key`           | 阻止容器使用内核密钥环，因为密钥环未被命名空间化。                                                                                                                                                                     |
| `bpf`               | 拒绝加载可能持久的 BPF 程序到内核，已通过 `CAP_SYS_ADMIN` 限制。                                                                                                                                                |
| `clock_adjtime`     | 时间/日期未被命名空间化。也受 `CAP_SYS_TIME` 限制。                                                                                                                                                                                     |
| `clock_settime`     | 时间/日期未被命名空间化。也受 `CAP_SYS_TIME` 限制。                                                                                                                                                                                     |
| `clone`             | 拒绝克隆新命名空间。也受 `CAP_SYS_ADMIN` 限制（针对 CLONE\_\* 标志），除了 `CLONE_NEWUSER`。                                                                                                                                        |
| `create_module`     | 拒绝对内核模块的操作和函数。已废弃。也受 `CAP_SYS_MODULE` 限制。                                                                                                                                                   |
| `delete_module`     | 拒绝对内核模块的操作和函数。也受 `CAP_SYS_MODULE` 限制。                                                                                                                                                             |
| `finit_module`      | 拒绝对内核模块的操作和函数。也受 `CAP_SYS_MODULE` 限制。                                                                                                                                                             |
| `get_kernel_syms`   | 拒绝检索导出的内核和模块符号。已废弃。                                                                                                                                                                                |
| `get_mempolicy`     | 修改内核内存和 NUMA 设置的系统调用。已通过 `CAP_SYS_NICE` 限制。                                                                                                                                                        |
| `init_module`       | 拒绝对内核模块的操作和函数。也受 `CAP_SYS_MODULE` 限制。                                                                                                                                                             |
| `ioperm`            | 阻止容器修改内核 I/O 特权级别。已通过 `CAP_SYS_RAWIO` 限制。                                                                                                                                               |
| `iopl`              | 阻止容器修改内核 I/O 特权级别。已通过 `CAP_SYS_RAWIO` 限制。                                                                                                                                               |
| `kcmp`              | 限制进程检查功能，已通过删除 `CAP_SYS_PTRACE` 阻止。                                                                                                                                                        |
| `kexec_file_load`   | 与 `kexec_load` 相同功能的姐妹系统调用，参数略有不同。也受 `CAP_SYS_BOOT` 限制。                                                                                                                           |
| `kexec_load`        | 拒绝加载新内核以供稍后执行。也受 `CAP_SYS_BOOT` 限制。                                                                                                                                                                   |
| `keyctl`            | 阻止容器使用内核密钥环，因为密钥环未被命名空间化。                                                                                                                                                                     |
| `lookup_dcookie`    | 跟踪/分析系统调用，可能泄露主机上的大量信息。也受 `CAP_SYS_ADMIN` 限制。                                                                                                                                   |
| `mbind`             | 修改内核内存和 NUMA 设置的系统调用。已通过 `CAP_SYS_NICE` 限制。                                                                                                                                                        |
| `mount`             | 拒绝挂载，已通过 `CAP_SYS_ADMIN` 限制。                                                                                                                                                                                               |
| `move_pages`        | 修改内核内存和 NUMA 设置的系统调用。                                                                                                                                                                                         |
| `nfsservctl`        | 拒绝与内核 NFS 守护进程交互。自 Linux 3.1 起已废弃。                                                                                                                                                                         |
| `open_by_handle_at` | 旧容器逃逸的原因。也受 `CAP_DAC_READ_SEARCH` 限制。                                                                                                                                                                       |
| `perf_event_open`   | 跟踪/分析系统调用，可能泄露主机上的大量信息。                                                                                                                                                                  |
| `personality`       | 阻止容器启用 BSD 仿真。本身并不危险，但测试不足，可能存在大量内核漏洞。                                                                                                     |
| `pivot_root`        | 拒绝 `pivot_root`，应为特权操作。                                                                                                                                                                                             |
| `process_vm_readv`  | 限制进程检查功能，已通过删除 `CAP_SYS_PTRACE` 阻止。                                                                                                                                                        |
| `process_vm_writev` | 限制进程检查功能，已通过删除 `CAP_SYS_PTRACE` 阻止。                                                                                                                                                        |
| `ptrace`            | 跟踪/分析系统调用。在 Linux 内核 4.8 之前的版本中被阻止以避免 seccomp 旁路。跟踪/分析任意进程已通过删除 `CAP_SYS_PTRACE` 阻止，因为它可能泄露主机上的大量信息。 |
| `query_module`      | 拒绝对内核模块的操作和函数。已废弃。                                                                                                                                                                                   |
| `quotactl`          | 配额系统调用，可能允许容器禁用自身的资源限制或进程会计。也受 `CAP_SYS_ADMIN` 限制。                                                                                                               |
| `reboot`            | 不允许容器重启主机。也受 `CAP_SYS_BOOT` 限制。                                                                                                                                                                            |
| `request_key`       | 阻止容器使用内核密钥环，因为密钥环未被命名空间化。                                                                                                                                                                     |
| `set_mempolicy`     | 修改内核内存和 NUMA 设置的系统调用。已通过 `CAP_SYS_NICE` 限制。                                                                                                                                                        |
| `setns`             | 拒绝将线程与命名空间关联。也受 `CAP_SYS_ADMIN` 限制。                                                                                                                                                                     |
| `settimeofday`      | 时间/日期未被命名空间化。也受 `CAP_SYS_TIME` 限制。                                                                                                                                                                                     |
| `stime`             | 时间/日期未被命名空间化。也受 `CAP_SYS_TIME` 限制。                                                                                                                                                                                     |
| `swapon`            | 拒绝开始/停止交换到文件/设备。也受 `CAP_SYS_ADMIN` 限制。                                                                                                                                                                        |
| `swapoff`           | 拒绝开始/停止交换到文件/设备。也受 `CAP_SYS_ADMIN` 限制。                                                                                                                                                                        |
| `sysfs`             | 已废弃的系统调用。                                                                                                                                                                                                                              |
| `_sysctl`           | 已废弃，被 /proc/sys 替代。                                                                                                                                                                                                               |
| `umount`            | 应为特权操作。也受 `CAP_SYS_ADMIN` 限制。                                                                                                                                                                               |
| `umount2`           | 应为特权操作。也受 `CAP_SYS_ADMIN` 限制。                                                                                                                                                                               |
| `unshare`           | 拒绝为进程克隆新命名空间。也受 `CAP_SYS_ADMIN` 限制，除了 `unshare --user`。                                                                                                                              |
| `uselib`            | 与共享库相关的旧系统调用，已长时间未使用。                                                                                                                                                                             |
| `userfaultfd`       | 用户空间页面错误处理，主要用于进程迁移。                                                                                                                                                                           |
| `ustat`             | 已废弃的系统调用。                                                                                                                                                                                                                              |
| `vm86`              | 内核中的 x86 实模式虚拟机。也受 `CAP_SYS_ADMIN` 限制。                                                                                                                                                                        |
| `vm86old`           | 内核中的 x86 实模式虚拟机。也受 `CAP_SYS_ADMIN` 限制。                                                                                                                                                                        |

## 不使用默认 seccomp 配置文件运行

您可以传递 `unconfined` 来运行不使用默认 seccomp 配置文件的容器。

```console
$ docker run --rm -it --security-opt seccomp=unconfined debian:latest \
    unshare --map-root-user --user sh -c whoami
```