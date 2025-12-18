---
description: 排查 Rootless 模式的问题
keywords: 安全, 命名空间, rootless, 排查
title: 排查问题
weight: 30
---

### 发行版特定提示

{{< tabs >}}
{{< tab name="Ubuntu" >}}
- Ubuntu 24.04 及更高版本默认启用受限的非特权用户命名空间，这会阻止非特权进程创建用户命名空间，除非配置了允许程序使用非特权用户命名空间的 AppArmor 配置文件。

  如果你使用 deb 包安装 `docker-ce-rootless-extras`（`apt-get install docker-ce-rootless-extras`），那么 `rootlesskit` 的 AppArmor 配置文件已经包含在 `apparmor` deb 包中。使用此安装方法时，你不需要手动添加任何 AppArmor 配置。但是，如果你使用 [安装脚本](https://get.docker.com/rootless) 安装 rootless extras，则必须手动为 `rootlesskit` 添加 AppArmor 配置文件：

  1. 创建并安装当前登录用户的 AppArmor 配置文件：

     ```console
     $ filename=$(echo $HOME/bin/rootlesskit | sed -e 's@^/@@' -e 's@/@.@g')
     $ [ ! -z "${filename}" ] && sudo cat <<EOF > /etc/apparmor.d/${filename}
     abi <abi/4.0>,
     include <tunables/global>

     "$HOME/bin/rootlesskit" flags=(unconfined) {
       userns,

       include if exists <local/${filename}>
     }
     EOF
     ```
  2. 重启 AppArmor。

     ```console
     $ systemctl restart apparmor.service
     ```

{{< /tab >}}
{{< tab name="Arch Linux" >}}
- 在 `/etc/sysctl.conf`（或 `/etc/sysctl.d`）中添加 `kernel.unprivileged_userns_clone=1` 并运行 `sudo sysctl --system`
{{< /tab >}}
{{< tab name="openSUSE and SLES" >}}
- 需要 `sudo modprobe ip_tables iptable_mangle iptable_nat iptable_filter`。根据配置，其他发行版也可能需要此步骤。

- 已知在 openSUSE 15 和 SLES 15 上可以正常工作。
{{< /tab >}}
{{< tab name="CentOS, RHEL, and Fedora" >}}
- 对于 RHEL 8 和类似的发行版，建议安装 `fuse-overlayfs`。运行 `sudo dnf install -y fuse-overlayfs`。
  在 RHEL 9 和类似的发行版上不需要此步骤。

- 你可能需要 `sudo dnf install -y iptables`。
{{< /tab >}}
{{< /tabs >}}

## 已知限制

- 仅支持以下存储驱动：
  - `overlay2`（仅在使用内核 5.11 或更高版本时支持）
  - `fuse-overlayfs`（仅在使用内核 4.18 或更高版本且已安装 `fuse-overlayfs` 时支持）
  - `btrfs`（仅在使用内核 4.18 或更高版本，或 `~/.local/share/docker` 以 `user_subvol_rm_allowed` 挂载选项挂载时支持）
  - `vfs`
- 仅在使用 cgroup v2 和 systemd 时支持 cgroup。请参阅 [限制资源](./tips.md#限制资源)。
- 以下功能不受支持：
  - AppArmor
  - Checkpoint
  - Overlay 网络
  - 暴露 SCTP 端口
- 要使用 `ping` 命令，请参阅 [路由 ping 数据包](./tips.md#路由-ping-数据包)。
- 要暴露特权 TCP/UDP 端口（< 1024），请参阅 [暴露特权端口](./tips.md#暴露特权端口)。
- `docker inspect` 中显示的 `IPAddress` 在 RootlessKit 的网络命名空间内。这意味着在不使用 `nsenter` 进入网络命名空间的情况下，该 IP 地址无法从主机访问。
- 主机网络（`docker run --net=host`）也在 RootlessKit 内的命名空间中。
- NFS 挂载作为 docker "data-root" 不受支持。此限制并非 rootless 模式特有。

## 排查问题

### 在系统上存在 systemd 时无法使用 systemd 安装

``` console
$ dockerd-rootless-setuptool.sh install
[INFO] systemd not detected, dockerd-rootless.sh needs to be started manually:
...
```
当你通过 `sudo su` 切换到用户时，`rootlesskit` 无法正确检测 systemd。对于无法登录的用户，你必须使用 `systemd-container` 包中的 `machinectl` 命令。安装 `systemd-container` 后，使用以下命令切换到 `myuser`：
``` console
$ sudo machinectl shell myuser@
```
其中 `myuser@` 是你想要的用户名，@ 表示此机器。

### 启动 Docker 守护进程时出错

**\[rootlesskit:parent\] error: failed to start the child: fork/exec /proc/self/exe: operation not permitted**

此错误通常发生在 `/proc/sys/kernel/unprivileged_userns_clone` 的值设置为 0 时：

```console
$ cat /proc/sys/kernel/unprivileged_userns_clone
0
```

要解决此问题，在 `/etc/sysctl.conf`（或 `/etc/sysctl.d`）中添加 `kernel.unprivileged_userns_clone=1` 并运行 `sudo sysctl --system`。

**\[rootlesskit:parent\] error: failed to start the child: fork/exec /proc/self/exe: no space left on device**

此错误通常发生在 `/proc/sys/user/max_user_namespaces` 的值太小时：

```console
$ cat /proc/sys/user/max_user_namespaces
0
```

要解决此问题，在 `/etc/sysctl.conf`（或 `/etc/sysctl.d`）中添加 `user.max_user_namespaces=28633` 并运行 `sudo sysctl --system`。

**\[rootlesskit:parent\] error: failed to setup UID/GID map: failed to compute uid/gid map: No subuid ranges found for user 1001 ("testuser")**

此错误发生在 `/etc/subuid` 和 `/etc/subgid` 未配置时。请参阅 [先决条件](./_index.md#先决条件)。

**could not get XDG_RUNTIME_DIR**

此错误发生在 `$XDG_RUNTIME_DIR` 未设置时。

在非 systemd 主机上，你需要创建一个目录并设置路径：

```console
$ export XDG_RUNTIME_DIR=$HOME/.docker/xrd
$ rm -rf $XDG_RUNTIME_DIR
$ mkdir -p $XDG_RUNTIME_DIR
$ dockerd-rootless.sh
```

> [!NOTE]
>
> 每次登出时都必须删除该目录。

在 systemd 主机上，使用 `pam_systemd` 登录（见下文）。该值会自动设置为 `/run/user/$UID` 并在每次登出时清理。

**`systemctl --user` 失败，提示 "Failed to connect to bus: No such file or directory"**

此错误通常发生在你通过 `sudo` 从 root 用户切换到非 root 用户时：

```console
# sudo -iu testuser
$ systemctl --user start docker
Failed to connect to bus: No such file or directory
```

你应该使用 `pam_systemd` 登录，而不是使用 `sudo -iu <USERNAME>`。例如：

- 通过图形控制台登录
- `ssh <USERNAME>@localhost`
- `machinectl shell <USERNAME>@`

**守护进程无法自动启动**

你需要 `sudo loginctl enable-linger $(whoami)` 来启用守护进程自动启动。请参阅 [高级用法](./tips.md/#高级用法)。

### `docker pull` 错误

**docker: failed to register layer: Error processing tar file(exit status 1): lchown &lt;FILE&gt;: invalid argument**

此错误发生在 `/etc/subuid` 或 `/etc/subgid` 中可用条目的数量不足时。不同镜像所需的条目数量各不相同。但是，65,536 个条目足以满足大多数镜像。请参阅 [先决条件](./_index.md#先决条件)。

**docker: failed to register layer: ApplyLayer exit status 1 stdout:  stderr: lchown &lt;FILE&gt;: operation not permitted**

此错误通常发生在 `~/.local/share/docker` 位于 NFS 上时。

一种解决方法是在 `~/.config/docker/daemon.json` 中指定非 NFS 的 `data-root` 目录，如下所示：
```json
{"data-root":"/somewhere-out-of-nfs"}
```

### `docker run` 错误

**docker: Error response from daemon: OCI runtime create failed: ...: read unix @-&gt;/run/systemd/private: read: connection reset by peer: unknown.**

此错误在 cgroup v2 主机上通常发生在 dbus 守护进程未为用户运行时。

```console
$ systemctl --user is-active dbus
inactive

$ docker run hello-world
docker: Error response from daemon: OCI runtime create failed: container_linux.go:380: starting container process caused: process_linux.go:385: applying cgroup configuration for process caused: error while starting unit "docker
-931c15729b5a968ce803784d04c7421f791d87e5ca1891f34387bb9f694c488e.scope" with properties [{Name:Description Value:"libcontainer container 931c15729b5a968ce803784d04c7421f791d87e5ca1891f34387bb9f694c488e"} {Name:Slice Value:"use
r.slice"} {Name:PIDs Value:@au [4529]} {Name:Delegate Value:true} {Name:MemoryAccounting Value:true} {Name:CPUAccounting Value:true} {Name:IOAccounting Value:true} {Name:TasksAccounting Value:true} {Name:DefaultDependencies Val
ue:false}]: read unix @->/run/systemd/private: read: connection reset by peer: unknown.
```

要解决此问题，运行 `sudo apt-get install -y dbus-user-session` 或 `sudo dnf install -y dbus-daemon`，然后重新登录。

如果错误仍然存在，尝试运行 `systemctl --user enable --now dbus`（不使用 sudo）。

**`--cpus`、`--memory` 和 `--pids-limit` 被忽略**

这是 cgroup v1 模式下的预期行为。要使用这些标志，主机需要配置为启用 cgroup v2。更多信息请参阅 [限制资源](./tips.md#限制资源)。

### 网络错误

本节提供 rootless 模式下网络的故障排除提示。

Rootless 模式下的网络通过 RootlessKit 中的网络和端口驱动程序支持。网络性能和特性取决于网络和端口驱动程序的组合。如果你遇到与网络相关的意外行为或性能问题，请查看以下显示 RootlessKit 支持的配置及其比较的表格：

| 网络驱动 | 端口驱动    | 网络吞吐量 | 端口吞吐量 | 源 IP 传播 | 无需 SUID | 备注                                                                         |
| -------------- | -------------- | -------------- | --------------- | --------------------- | ------- | ---------------------------------------------------------------------------- |
| `slirp4netns`  | `builtin`      | 慢           | 快 ✅         | ❌                    | ✅      | 典型设置中的默认值                                                   |
| `vpnkit`       | `builtin`      | 慢           | 快 ✅         | ❌                    | ✅      | 当未安装 `slirp4netns` 时的默认值                                   |
| `slirp4netns`  | `slirp4netns`  | 慢           | 慢            | ✅                    | ✅      |                                                                              |
| `pasta`        | `implicit`     | 慢           | 快 ✅         | ✅                    | ✅      | 实验性；需要 pasta 版本 2023_12_04 或更高版本                        |
| `lxc-user-nic` | `builtin`      | 快 ✅        | 快 ✅         | ❌                    | ❌      | 实验性                                                                 |
| `bypass4netns` | `bypass4netns` | 快 ✅        | 快 ✅         | ✅                    | ✅      | **注意：**未集成到 RootlessKit，因为它需要自定义 seccomp 配置文件 |

有关特定网络问题的故障排除信息，请参阅：

- [`docker run -p` 失败，提示 `cannot expose privileged port`](#docker-run--p-fails-with-cannot-expose-privileged-port)
- [Ping 不工作](#ping-doesnt-work)
- [`docker inspect` 中显示的 `IPAddress` 无法访问](#ipaddress-shown-in-docker-inspect-is-unreachable)
- [`--net=host` 不在主机网络命名空间中监听端口](#--nethost-doesnt-listen-ports-on-the-host-network-namespace)
- [网络很慢](#network-is-slow)
- [`docker run -p` 不传播源 IP 地址](#docker-run--p-does-not-propagate-source-ip-addresses)

#### `docker run -p` 失败，提示 `cannot expose privileged port`

当你指定特权端口（< 1024）作为主机端口时，`docker run -p` 会失败并显示此错误。

```console
$ docker run -p 80:80 nginx:alpine
docker: Error response from daemon: driver failed programming external connectivity on endpoint focused_swanson (9e2e139a9d8fc92b37c36edfa6214a6e986fa2028c0cc359812f685173fa6df7): Error starting userland proxy: error while calling PortManager.AddPort(): cannot expose privileged port 80, you might need to add "net.ipv4.ip_unprivileged_port_start=0" (currently 1024) to /etc/sysctl.conf, or set CAP_NET_BIND_SERVICE on rootlesskit binary, or choose a larger port number (>= 1024): listen tcp 0.0.0.0:80: bind: permission denied.
```

当你遇到此错误时，考虑使用非特权端口。例如，使用 8080 而不是 80。

```console
$ docker run -p 8080:80 nginx:alpine
```

要允许暴露特权端口，请参阅 [暴露特权端口](./tips.md#暴露特权端口)。

#### Ping 不工作

当 `/proc/sys/net/ipv4/ping_group_range` 设置为 `1 0` 时，ping 不工作：

```console
$ cat /proc/sys/net/ipv4/ping_group_range
1       0
```

详细信息请参阅 [路由 ping 数据包](./tips.md#路由-ping-数据包)。

#### `docker inspect` 中显示的 `IPAddress` 无法访问

这是预期行为，因为守护进程在 RootlessKit 的网络命名空间内。请改用 `docker run -p`。

#### `--net=host` 不在主机网络命名空间中监听端口

这是预期行为，因为守护进程在 RootlessKit 的网络命名空间内。请改用 `docker run -p`。

#### 网络很慢

Docker 在 rootless 模式下，如果安装了 slirp4netns v0.4.0 或更高版本，则默认使用 [slirp4netns](https://github.com/rootless-containers/slirp4netns) 作为网络栈。如果未安装 slirp4netns，Docker 会回退到 [VPNKit](https://github.com/moby/vpnkit)。
安装 slirp4netns 可能会提高网络吞吐量。

有关 RootlessKit 网络驱动的更多信息，请参阅
[RootlessKit 文档](https://github.com/rootless-containers/rootlesskit/blob/v2.0.0/docs/network.md)。

另外，更改 MTU 值可能会提高吞吐量。
可以通过创建 `~/.config/systemd/user/docker.service.d/override.conf` 并添加以下内容来指定 MTU 值：

```systemd
[Service]
Environment="DOCKERD_ROOTLESS_ROOTLESSKIT_MTU=<INTEGER>"
```

然后重启守护进程：
```console
$ systemctl --user daemon-reload
$ systemctl --user restart docker
```

#### `docker run -p` 不传播源 IP 地址

这是因为 rootless 模式下的 Docker 默认使用 RootlessKit 的 `builtin` 端口驱动，它不支持源 IP 传播。要启用源 IP 传播，你可以：

- 使用 `slirp4netns` RootlessKit 端口驱动
- 使用 `pasta` RootlessKit 网络驱动，配合 `implicit` 端口驱动

`pasta` 网络驱动是实验性的，但与 `slirp4netns` 端口驱动相比，它提供了改进的吞吐量性能。`pasta` 驱动需要 Docker Engine 版本 25.0 或更高版本。

要更改 RootlessKit 网络配置：

1. 在 `~/.config/systemd/user/docker.service.d/override.conf` 中创建文件。
2. 根据你想要使用的配置添加以下内容：

   - `slirp4netns`

      ```systemd
      [Service]
      Environment="DOCKERD_ROOTLESS_ROOTLESSKIT_NET=slirp4netns"
      Environment="DOCKERD_ROOTLESS_ROOTLESSKIT_PORT_DRIVER=slirp4netns"
      ```

   - `pasta` 网络驱动配合