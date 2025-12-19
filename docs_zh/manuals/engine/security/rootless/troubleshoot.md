---
description: 排查 Rootless 模式的问题
keywords: security, namespaces, rootless, troubleshooting
title: 问题排查
weight: 30
---

### 各发行版的特定提示

{{< tabs >}}
{{< tab name="Ubuntu" >}}
- Ubuntu 24.04 及更高版本默认启用了受限的非特权用户命名空间，这会阻止非特权进程创建用户命名空间，除非配置了 AppArmor 配置文件以允许程序使用非特权用户命名空间。

  如果您使用 deb 包（`apt-get install docker-ce-rootless-extras`）安装 `docker-ce-rootless-extras`，那么 `rootlesskit` 的 AppArmor 配置文件已经包含在 `apparmor` deb 包中。使用此安装方法时，您无需手动添加任何 AppArmor 配置。但是，如果您使用[安装脚本](https://get.docker.com/rootless)安装 rootless 额外组件，则必须为 `rootlesskit` 手动添加 AppArmor 配置文件：

  1. 为当前登录用户创建并安装 AppArmor 配置文件：

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
- 将 `kernel.unprivileged_userns_clone=1` 添加到 `/etc/sysctl.conf`（或 `/etc/sysctl.d`）并运行 `sudo sysctl --system`
{{< /tab >}}
{{< tab name="openSUSE and SLES" >}}
- 需要运行 `sudo modprobe ip_tables iptable_mangle iptable_nat iptable_filter`。
  根据配置的不同，其他发行版可能也需要此操作。

- 已知在 openSUSE 15 和 SLES 15 上可用。
{{< /tab >}}
{{< tab name="CentOS, RHEL, and Fedora" >}}
- 对于 RHEL 8 及类似发行版，建议安装 `fuse-overlayfs`。运行 `sudo dnf install -y fuse-overlayfs`。
  在 RHEL 9 及类似发行版上，不需要此步骤。

- 您可能需要运行 `sudo dnf install -y iptables`。
{{< /tab >}}
{{< /tabs >}}

## 已知限制

- 仅支持以下存储驱动：
  - `overlay2`（仅在内核 5.11 或更高版本上运行时）
  - `fuse-overlayfs`（仅在内核 4.18 或更高版本上运行时，且已安装 `fuse-overlayfs`）
  - `btrfs`（仅在内核 4.18 或更高版本上运行时，或 `~/.local/share/docker` 使用 `user_subvol_rm_allowed` 挂载选项挂载时）
  - `vfs`
- 仅在使用 cgroup v2 和 systemd 运行时支持 cgroup。参见[限制资源](./tips.md#limiting-resources)。
- 不支持以下功能：
  - AppArmor
  - Checkpoint
  - Overlay 网络
  - 暴露 SCTP 端口
- 要使用 `ping` 命令，请参见[路由 ping 数据包](./tips.md#routing-ping-packets)。
- 要暴露特权 TCP/UDP 端口（< 1024），请参见[暴露特权端口](./tips.md#exposing-privileged-ports)。
- `docker inspect` 中显示的 `IPAddress` 在 RootlessKit 的网络命名空间内。
  这意味着如果不使用 `nsenter` 进入该网络命名空间，主机将无法访问该 IP 地址。
- 主机网络（`docker run --net=host`）也在 RootlessKit 的网络命名空间内。
- 不支持将 NFS 挂载作为 docker 的 "data-root"。此限制并非 rootless 模式特有。

## 问题排查

### 系统中存在 systemd 时无法通过 systemd 安装

``` console
$ dockerd-rootless-setuptool.sh install
[INFO] systemd not detected, dockerd-rootless.sh needs to be started manually:
...
```
如果您通过 `sudo su` 切换到您的用户，`rootlesskit` 可能无法正确检测 systemd。对于无法登录的用户，您必须使用 `machinectl` 命令，该命令是 `systemd-container` 包的一部分。安装 `systemd-container` 后，使用以下命令切换到 `myuser`：
``` console
$ sudo machinectl shell myuser@
```
其中 `myuser@` 是您期望的用户名，@ 表示这台机器。

### 启动 Docker 守护进程时出错

**\[rootlesskit:parent\] error: failed to start the child: fork/exec /proc/self/exe: operation not permitted**

此错误通常发生在 `/proc/sys/kernel/unprivileged_userns_clone` 的值设置为 0 时：

```console
$ cat /proc/sys/kernel/unprivileged_userns_clone
0
```

要解决此问题，请将 `kernel.unprivileged_userns_clone=1` 添加到
`/etc/sysctl.conf`（或 `/etc/sysctl.d`）并运行 `sudo sysctl --system`。

**\[rootlesskit:parent\] error: failed to start the child: fork/exec /proc/self/exe: no space left on device**

此错误通常发生在 `/proc/sys/user/max_user_namespaces` 的值过小时：

```console
$ cat /proc/sys/user/max_user_namespaces
0
```

要解决此问题，请将 `user.max_user_namespaces=28633` 添加到
`/etc/sysctl.conf`（或 `/etc/sysctl.d`）并运行 `sudo sysctl --system`。

**\[rootlesskit:parent\] error: failed to setup UID/GID map: failed to compute uid/gid map: No subuid ranges found for user 1001 ("testuser")**

当 `/etc/subuid` 和 `/etc/subgid` 未配置时，会发生此错误。参见[先决条件](./_index.md#prerequisites)。

**could not get XDG_RUNTIME_DIR**

当 `$XDG_RUNTIME_DIR` 未设置时，会发生此错误。

在非 systemd 主机上，您需要创建一个目录然后设置路径：

```console
$ export XDG_RUNTIME_DIR=$HOME/.docker/xrd
$ rm -rf $XDG_RUNTIME_DIR
$ mkdir -p $XDG_RUNTIME_DIR
$ dockerd-rootless.sh
```

> [!NOTE]
>
> 您每次注销时都必须删除该目录。

在 systemd 主机上，使用 `pam_systemd` 登录到主机（见下文）。
该值会自动设置为 `/run/user/$UID`，并在每次注销时清理。

**`systemctl --user` 失败并提示 "Failed to connect to bus: No such file or directory"**

当您使用 `sudo` 从 root 用户切换到非 root 用户时，通常会发生此错误：

```console
# sudo -iu testuser
$ systemctl --user start docker
Failed to connect to bus: No such file or directory
```

您需要使用 `pam_systemd` 登录，而不是 `sudo -iu <USERNAME>`。例如：

- 通过图形控制台登录
- `ssh <USERNAME>@localhost`
- `machinectl shell <USERNAME>@`

**守护进程不会自动启动**

您需要运行 `sudo loginctl enable-linger $(whoami)` 来使守护进程能够
自动启动。参见[高级用法](./tips.md/#advanced-usage)。

### `docker pull` 错误

**docker: failed to register layer: Error processing tar file(exit status 1): lchown &lt;FILE&gt;: invalid argument**

当 `/etc/subuid` 或 `/etc/subgid` 中可用条目数量不足时，会发生此错误。
所需条目数量因镜像而异。但是，65,536 个条目对于大多数镜像来说已经足够。参见
[先决条件](./_index.md#prerequisites)。

**docker: failed to register layer: ApplyLayer exit status 1 stdout:  stderr: lchown &lt;FILE&gt;: operation not permitted**

当 `~/.local/share/docker` 位于 NFS 上时，通常会发生此错误。

一种解决方法是在 `~/.config/docker/daemon.json` 中指定非 NFS 的 `data-root` 目录，如下所示：
```json
{"data-root":"/somewhere-out-of-nfs"}
```

### `docker run` 错误

**docker: Error response from daemon: OCI runtime create failed: ...: read unix @-&gt;/run/systemd/private: read: connection reset by peer: unknown.**

在 cgroup v2 主机上，当用户的 dbus 守护进程未运行时，通常会发生此错误。

```console
$ systemctl --user is-active dbus
inactive

$ docker run hello-world
docker: Error response from daemon: OCI runtime create failed: container_linux.go:380: starting container process caused: process_linux.go:385: applying cgroup configuration for process caused: error while starting unit "docker
-931c15729b5a968ce803784d04c7421f791d87e5ca1891f34387bb9f694c488e.scope" with properties [{Name:Description Value:"libcontainer container 931c15729b5a968ce803784d04c7421f791d87e5ca1891f34387bb9f694c488e"} {Name:Slice Value:"use
r.slice"} {Name:PIDs Value:@au [4529]} {Name:Delegate Value:true} {Name:MemoryAccounting Value:true} {Name:CPUAccounting Value:true} {Name:IOAccounting Value:true} {Name:TasksAccounting Value:true} {Name:DefaultDependencies Val
ue:false}]: read unix @->/run/systemd/private: read: connection reset by peer: unknown.
```

要解决此问题，请运行 `sudo apt-get install -y dbus-user-session` 或 `sudo dnf install -y dbus-daemon`，然后重新登录。

如果错误仍然存在，请尝试运行 `systemctl --user enable --now dbus`（无需 sudo）。

**`--cpus`、`--memory` 和 `--pids-limit` 被忽略**

在 cgroup v1 模式下，这是预期行为。
要使用这些标志，需要将主机配置为启用 cgroup v2。
有关更多信息，请参见[限制资源](./tips.md#limiting-resources)。

### 网络错误

本节提供 rootless 模式下网络问题的排查技巧。

Rootless 模式下的网络通过 RootlessKit 中的网络和端口驱动程序支持。
网络性能和特性取决于您使用的网络和端口驱动程序的组合。
如果您遇到与网络相关的意外行为或性能问题，请查看下表，其中显示了
RootlessKit 支持的配置及其比较：

| 网络驱动       | 端口驱动       | 网络吞吐量 | 端口吞吐量 | 源 IP 传播 | 无需 SUID | 备注                                                                         |
| -------------- | -------------- | ---------- | ---------- | ---------- | --------- | ---------------------------------------------------------------------------- |
| `slirp4netns`  | `builtin`      | 慢         | 快 ✅       | ❌          | ✅         | 典型设置中的默认选项                                                         |
| `vpnkit`       | `builtin`      | 慢         | 快 ✅       | ❌          | ✅         | 未安装 `slirp4netns` 时的默认选项                                            |
| `slirp4netns`  | `slirp4netns`  | 慢         | 慢         | ✅          | ✅         |                                                                              |
| `pasta`        | `implicit`     | 慢         | 快 ✅       | ✅          | ✅         | 实验性功能；需要 pasta 2023_12_04 或更高版本                                 |
| `lxc-user-nic` | `builtin`      | 快 ✅       | 快 ✅       | ❌          | ❌         | 实验性功能                                                                   |
| `bypass4netns` | `bypass4netns` | 快 ✅       | 快 ✅       | ✅          | ✅         | **注意：**由于需要自定义 seccomp 配置文件，尚未集成到 RootlessKit 中         |

有关排查特定网络问题的信息，请参见：

- [`docker run -p` 失败并提示 `cannot expose privileged port`](#docker-run--p-fails-with-cannot-expose-privileged-port)
- [Ping 不工作](#ping-doesnt-work)
- [`docker inspect` 中显示的 `IPAddress` 不可达](#ipaddress-shown-in-docker-inspect-is-unreachable)
- [`--net=host` 不在主机网络命名空间上监听端口](#--nethost-doesnt-listen-ports-on-the-host-network-namespace)
- [网络速度慢](#network-is-slow)
- [`docker run -p` 不传播源 IP 地址](#docker-run--p-does-not-propagate-source-ip-addresses)

#### `docker run -p` 失败并提示 `cannot expose privileged port`

当指定特权端口（< 1024）作为主机端口时，`docker run -p` 会失败并提示此错误。

```console
$ docker run -p 80:80 nginx:alpine
docker: Error response from daemon: driver failed programming external connectivity on endpoint focused_swanson (9e2e139a9d8fc92b37c36edfa6214a6e986fa2028c0cc359812f685173fa6df7): Error starting userland proxy: error while calling PortManager.AddPort(): cannot expose privileged port 80, you might need to add "net.ipv4.ip_unprivileged_port_start=0" (currently 1024) to /etc/sysctl.conf, or set CAP_NET_BIND_SERVICE on rootlesskit binary, or choose a larger port number (>= 1024): listen tcp 0.0.0.0:80: bind: permission denied.
```

当遇到此错误时，请考虑改用非特权端口。例如，用 8080 代替 80。

```console
$ docker run -p 8080:80 nginx:alpine
```

要允许暴露特权端口，请参见[暴露特权端口](./tips.md#exposing-privileged-ports)。

#### Ping 不工作

当 `/proc/sys/net/ipv4/ping_group_range` 设置为 `1 0` 时，Ping 不起作用：

```console
$ cat /proc/sys/net/ipv4/ping_group_range
1       0
```

有关详细信息，请参见[路由 ping 数据包](./tips.md#routing-ping-packets)。

#### `docker inspect` 中显示的 `IPAddress` 不可达

这是预期行为，因为守护进程在 RootlessKit 的
网络命名空间内。请改用 `docker run -p`。

#### `--net=host` 不在主机网络命名空间上监听端口

这是预期行为，因为守护进程在 RootlessKit 的
网络命名空间内。请改用 `docker run -p`。

#### 网络速度慢

如果安装了 slirp4netns v0.4.0 或更高版本，rootless 模式下的 Docker 默认使用 [slirp4netns](https://github.com/rootless-containers/slirp4netns) 作为默认网络栈。
如果未安装 slirp4netns，Docker 会回退到 [VPNKit](https://github.com/moby/vpnkit)。
安装 slirp4netns 可能会提高网络吞吐量。

有关 RootlessKit 网络驱动程序的更多信息，请参见
[RootlessKit 文档](https://github.com/rootless-containers/rootlesskit/blob/v2.0.0/docs/network.md)。

此外，更改 MTU 值也可能提高吞吐量。
可以通过创建 `~/.config/systemd/user/docker.service.d/override.conf` 文件并添加以下内容来指定 MTU 值：

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

这是因为 rootless 模式下的 Docker 默认使用 RootlessKit 的 `builtin` 端口
驱动程序，该驱动程序不支持源 IP 传播。要启用
源 IP 传播，您可以：

- 使用 `slirp4netns` RootlessKit 端口驱动程序
- 使用 `pasta` RootlessKit 网络驱动程序，配合 `implicit` 端口驱动程序

`pasta` 网络驱动程序是实验性的，但与 `slirp4netns` 端口驱动程序相比，提供了更高的吞吐量
性能。`pasta` 驱动程序
需要 Docker Engine 25.0 或更高版本。

要更改 RootlessKit 网络配置：

1. 在 `~/.config/systemd/user/docker.service.d/override.conf` 创建文件。
2. 根据您想使用的配置，添加以下内容：

   - `slirp4netns`

      ```systemd
      [Service]
      Environment="DOCKERD_ROOTLESS_ROOTLESSKIT_NET=slirp4netns"
      Environment="DOCKERD_ROOTLESS_ROOTLESSKIT_PORT_DRIVER=slirp4netns"
      ```

   - `pasta` 网络驱动程序配合 `implicit` 端口驱动程序

      ```systemd
      [Service]
      Environment="DOCKERD_ROOTLESS_ROOTLESSKIT_NET=pasta"
      Environment="DOCKERD_ROOTLESS_ROOTLESSKIT_PORT_DRIVER=implicit"
      ```

3. 重启守护进程：

   ```console
   $ systemctl --user daemon-reload
   $ systemctl --user restart docker
   ```

有关 RootlessKit 网络选项的更多信息，请参见：

- [网络驱动程序](https://github.com/rootless-containers/rootlesskit/blob/v2.0.0/docs/network.md)
- [端口驱动程序](https://github.com/rootless-containers/rootlesskit/blob/v2.0.0/docs/port.md)

### 调试技巧

**进入 `dockerd` 命名空间**

`dockerd-rootless.sh` 脚本在其自己的用户、挂载和网络命名空间中执行 `dockerd`。

为了进行调试，您可以通过运行
`nsenter -U --preserve-credentials -n -m -t $(cat $XDG_RUNTIME_DIR/docker.pid)` 进入这些命名空间。

## 卸载

要移除 Docker 守护进程的 systemd 服务，请运行 `dockerd-rootless-setuptool.sh uninstall`：

```console
$ dockerd-rootless-setuptool.sh uninstall
+ systemctl