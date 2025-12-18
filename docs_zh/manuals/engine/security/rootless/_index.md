---
description: 以非 root 用户身份运行 Docker 守护进程（Rootless 模式）
keywords: security, namespaces, rootless
title: Rootless 模式
weight: 10
---

Rootless 模式允许你以非 root 用户身份运行 Docker 守护进程和容器，以减轻守护进程和容器运行时中潜在的安全漏洞。

只要满足[先决条件](#prerequisites)，Rootless 模式甚至在安装 Docker 守护进程期间也不需要 root 权限。

## 工作原理

Rootless 模式在用户命名空间内执行 Docker 守护进程和容器。这与 [`userns-remap` 模式](../userns-remap.md) 类似，但不同的是，在 `userns-remap` 模式下，守护进程本身以 root 权限运行，而在 Rootless 模式下，守护进程和容器都无需 root 权限即可运行。

Rootless 模式不使用带有 `SETUID` 位或文件功能的二进制文件，除了 `newuidmap` 和 `newgidmap`，这两个命令需要在用户命名空间中使用多个 UID/GID。

## 先决条件

- 你必须在主机上安装 `newuidmap` 和 `newgidmap`。这些命令在大多数 Linux 发行版中由 `uidmap` 软件包提供。

- `/etc/subuid` 和 `/etc/subgid` 应该包含至少 65,536 个从属 UID/GID。在以下示例中，用户 `testuser` 有 65,536 个从属 UID/GID（231072-296607）。

```console
$ id -u
1001
$ whoami
testuser
$ grep ^$(whoami): /etc/subuid
testuser:231072:65536
$ grep ^$(whoami): /etc/subgid
testuser:231072:65536
```

当先决条件未满足时，`dockerd-rootless-setuptool.sh install` 脚本（见下文）会自动显示帮助信息。

## 安装

> [!NOTE]
>
> 如果系统范围的 Docker 守护进程已经在运行，请考虑禁用它：
>```console
>$ sudo systemctl disable --now docker.service docker.socket
>$ sudo rm /var/run/docker.sock
>```
> 如果你选择不关闭 `docker` 服务和 socket，你需要在下一节中使用 `--force` 参数。目前没有已知问题，但在你关闭并禁用之前，你仍然在运行 rootful Docker。

{{< tabs >}}
{{< tab name="使用软件包 (RPM/DEB)" >}}

如果你使用 [RPM/DEB 软件包](/engine/install) 安装了 Docker 20.10 或更高版本，你应该在 `/usr/bin` 中找到 `dockerd-rootless-setuptool.sh`。

以非 root 用户身份运行 `dockerd-rootless-setuptool.sh install` 来设置守护进程：

```console
$ dockerd-rootless-setuptool.sh install
[INFO] Creating /home/testuser/.config/systemd/user/docker.service
...
[INFO] Installed docker.service successfully.
[INFO] To control docker.service, run: `systemctl --user (start|stop|restart) docker.service`
[INFO] To run docker.service on system startup, run: `sudo loginctl enable-linger testuser`

[INFO] Creating CLI context "rootless"
Successfully created context "rootless"
[INFO] Using CLI context "rootless"
Current context is now "rootless"

[INFO] Make sure the following environment variable(s) are set (or add them to ~/.bashrc):
export PATH=/usr/bin:$PATH

[INFO] Some applications may require the following environment variable too:
export DOCKER_HOST=unix:///run/user/1000/docker.sock
```

如果 `dockerd-rootless-setuptool.sh` 不存在，你可能需要手动安装 `docker-ce-rootless-extras` 软件包，例如：

```console
$ sudo apt-get install -y docker-ce-rootless-extras
```

{{< /tab >}}
{{< tab name="不使用软件包" >}}

如果你没有权限运行 `apt-get` 和 `dnf` 等包管理器，请考虑使用 [https://get.docker.com/rootless](https://get.docker.com/rootless) 上的安装脚本。
由于静态软件包不适用于 `s390x`，因此 `s390x` 不受支持。

```console
$ curl -fsSL https://get.docker.com/rootless | sh
...
[INFO] Creating /home/testuser/.config/systemd/user/docker.service
...
[INFO] Installed docker.service successfully.
[INFO] To control docker.service, run: `systemctl --user (start|stop|restart) docker.service`
[INFO] To run docker.service on system startup, run: `sudo loginctl enable-linger testuser`

[INFO] Creating CLI context "rootless"
Successfully created context "rootless"
[INFO] Using CLI context "rootless"
Current context is now "rootless"

[INFO] Make sure the following environment variable(s) are set (or add them to ~/.bashrc):
export PATH=/home/testuser/bin:$PATH

[INFO] Some applications may require the following environment variable too:
export DOCKER_HOST=unix:///run/user/1000/docker.sock
```

二进制文件将被安装在 `~/bin` 目录中。

{{< /tab >}}
{{< /tabs >}}

运行 `docker info` 确认 `docker` 客户端正在连接到 Rootless 守护进程：
```console
$ docker info
Client: Docker Engine - Community
 Version:    28.3.3
 Context:    rootless
...
Server:
...
 Security Options:
  seccomp
   Profile: builtin
  rootless
  cgroupns
...
```

如果遇到错误，请参阅 [故障排除](./troubleshoot.md)。