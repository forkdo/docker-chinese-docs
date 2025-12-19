---
description: Rootless 模式的使用技巧
keywords: security, namespaces, rootless
title: 使用技巧
weight: 20
---

## 高级用法

### 守护进程

{{< tabs >}}
{{< tab name="使用 systemd（强烈推荐）" >}}

systemd 单元文件安装在 `~/.config/systemd/user/docker.service`。

使用 `systemctl --user` 管理守护进程的生命周期：

```console
$ systemctl --user start docker
```

要在系统启动时启动守护进程，请启用 systemd 服务和 lingering：

```console
$ systemctl --user enable docker
$ sudo loginctl enable-linger $(whoami)
```

将 Rootless Docker 作为 systemd 全局服务（`/etc/systemd/system/docker.service`）运行不受支持，即使使用 `User=` 指令也是如此。

{{< /tab >}}
{{< tab name="不使用 systemd" >}}

要直接运行守护进程而不使用 systemd，您需要运行 `dockerd-rootless.sh` 而不是 `dockerd`。

必须设置以下环境变量：
- `$HOME`：主目录
- `$XDG_RUNTIME_DIR`：仅由预期用户访问的临时目录，例如 `~/.docker/run`。
  该目录应在每次主机关闭时被移除。
  该目录可以位于 tmpfs 上，但不应在 `/tmp` 下。
  将此目录定位在 `/tmp` 下可能容易受到 TOCTOU 攻击。

{{< /tab >}}
{{< /tabs >}}

重要的是要注意目录路径：

- Socket 路径默认设置为 `$XDG_RUNTIME_DIR/docker.sock`。
  `$XDG_RUNTIME_DIR` 通常设置为 `/run/user/$UID`。
- 数据目录默认设置为 `~/.local/share/docker`。
  数据目录不应位于 NFS 上。
- 守护进程配置目录默认设置为 `~/.config/docker`。
  此目录与客户端使用的 `~/.docker` 不同。

### 客户端

自 Docker Engine v23.0 起，`dockerd-rootless-setuptool.sh install` 会自动配置
`docker` CLI 使用 `rootless` 上下文。

在 Docker Engine v23.0 之前，用户必须显式指定 socket 路径或 CLI 上下文。

使用 `$DOCKER_HOST` 指定 socket 路径：

```console
$ export DOCKER_HOST=unix://$XDG_RUNTIME_DIR/docker.sock
$ docker run -d -p 8080:80 nginx
```

使用 `docker context` 指定 CLI 上下文：

```console
$ docker context use rootless
rootless
Current context is now "rootless"
$ docker run -d -p 8080:80 nginx
```

## 最佳实践

### Docker 中的 Rootless Docker

要在“rootful”Docker 中运行 Rootless Docker，请使用 `docker:<version>-dind-rootless`
镜像而不是 `docker:<version>-dind`。

```console
$ docker run -d --name dind-rootless --privileged docker:25.0-dind-rootless
```

`docker:<version>-dind-rootless` 镜像以非 root 用户（UID 1000）运行。
但是，需要 `--privileged` 来禁用 seccomp、AppArmor 和挂载掩码。

### 通过 TCP 暴露 Docker API socket

要通过 TCP 暴露 Docker API socket，您需要使用 `DOCKERD_ROOTLESS_ROOTLESSKIT_FLAGS="-p 0.0.0.0:2376:2376/tcp"` 启动 `dockerd-rootless.sh`。

```console
$ DOCKERD_ROOTLESS_ROOTLESSKIT_FLAGS="-p 0.0.0.0:2376:2376/tcp" \
  dockerd-rootless.sh \
  -H tcp://0.0.0.0:2376 \
  --tlsverify --tlscacert=ca.pem --tlscert=cert.pem --tlskey=key.pem
```

### 通过 SSH 暴露 Docker API socket

要通过 SSH 暴露 Docker API socket，您需要确保 `$DOCKER_HOST` 在远程主机上设置。

```console
$ ssh -l <REMOTEUSER> <REMOTEHOST> 'echo $DOCKER_HOST'
unix:///run/user/1001/docker.sock
$ docker -H ssh://<REMOTEUSER>@<REMOTEHOST> run ...
```

### 路由 ping 数据包

在某些发行版上，`ping` 默认不工作。

在 `/etc/sysctl.conf`（或 `/etc/sysctl.d`）中添加 `net.ipv4.ping_group_range = 0   2147483647` 并运行 `sudo sysctl --system` 以允许使用 `ping`。

### 暴露特权端口

要暴露特权端口（< 1024），请在 `rootlesskit` 二进制文件上设置 `CAP_NET_BIND_SERVICE` 并重启守护进程。

```console
$ sudo setcap cap_net_bind_service=ep $(which rootlesskit)
$ systemctl --user restart docker
```

或者在 `/etc/sysctl.conf`（或 `/etc/sysctl.d`）中添加 `net.ipv4.ip_unprivileged_port_start=0` 并运行 `sudo sysctl --system`。

### 限制资源

仅在使用 cgroup v2 和 systemd 运行时，才支持使用 cgroup 相关的 `docker run` 标志（如 `--cpus`、`--memory`、`--pids-limit`）限制资源。
请参阅 [更改 cgroup 版本](/manuals/engine/containers/runmetrics.md) 以启用 cgroup v2。

如果 `docker info` 显示 `Cgroup Driver` 为 `none`，则条件不满足。
当条件不满足时，rootless 模式会忽略 cgroup 相关的 `docker run` 标志。
请参阅 [无 cgroup 时限制资源](#limiting-resources-without-cgroup) 了解变通方法。

如果 `docker info` 显示 `Cgroup Driver` 为 `systemd`，则条件满足。
但是，通常默认只将 `memory` 和 `pids` 控制器委托给非 root 用户。

```console
$ cat /sys/fs/cgroup/user.slice/user-$(id -u).slice/user@$(id -u).service/cgroup.controllers
memory pids
```

要允许委托所有控制器，您需要按如下方式更改 systemd 配置：

```console
# mkdir -p /etc/systemd/system/user@.service.d
# cat > /etc/systemd/system/user@.service.d/delegate.conf << EOF
[Service]
Delegate=cpu cpuset io memory pids
EOF
# systemctl daemon-reload
```

> [!NOTE]
>
> 委托 `cpuset` 需要 systemd 244 或更高版本。

#### 无 cgroup 时限制资源

即使在 cgroup 不可用时，您仍然可以使用传统的 `ulimit` 和 [`cpulimit`](https://github.com/opsengine/cpulimit)，
尽管它们以进程粒度而不是容器粒度工作，并且可以被容器进程任意禁用。

例如：

- 要将 CPU 使用率限制为 0.5 个核心（类似于 `docker run --cpus 0.5`）：
  `docker run <IMAGE> cpulimit --limit=50 --include-children <COMMAND>`
- 要将最大 VSZ 限制为 64MiB（类似于 `docker run --memory 64m`）：
  `docker run <IMAGE> sh -c "ulimit -v 65536; <COMMAND>"`

- 要将每个命名空间 UID 2000 的最大进程数限制为 100（类似于 `docker run --pids-limit=100`）：
  `docker run --user 2000 --ulimit nproc=100 <IMAGE> <COMMAND>`