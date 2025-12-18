---
description: 在 Docker 中启用 AppArmor
keywords: AppArmor, 安全, docker, 文档
title: Docker 的 AppArmor 安全配置文件
---

AppArmor（应用程序防护）是一个 Linux 安全模块，用于保护操作系统及其应用程序免受安全威胁。要使用它，系统管理员需要将 AppArmor 安全配置文件与每个程序关联。Docker 期望找到一个已加载并正在执行的 AppArmor 策略。

Docker 会自动为容器生成并加载一个名为 `docker-default` 的默认配置文件。Docker 二进制文件在 `tmpfs` 中生成此配置文件，然后将其加载到内核中。

> [!NOTE]
>
> 此配置文件用于容器，而不是 Docker 守护进程。

Docker Engine 守护进程也存在一个配置文件，但目前 `deb` 软件包并未安装它。如果您对守护进程配置文件的源码感兴趣，它位于 Docker Engine 源码仓库的
[contrib/apparmor](https://github.com/moby/moby/tree/master/contrib/apparmor) 目录中。

## 了解策略

`docker-default` 配置文件是运行容器的默认配置文件。它在提供广泛应用程序兼容性的同时，提供适度的保护。该配置文件由以下
[模板](https://github.com/moby/profiles/blob/main/apparmor/template.go) 生成。

运行容器时，除非您使用 `security-opt` 选项覆盖，否则它将使用 `docker-default` 策略。例如，以下命令显式指定了默认策略：

```console
$ docker run --rm -it --security-opt apparmor=docker-default hello-world
```

## 加载和卸载配置文件

要将新配置文件加载到 AppArmor 中以供容器使用：

```console
$ apparmor_parser -r -W /path/to/your_profile
```

然后，使用 `--security-opt` 运行自定义配置文件：

```console
$ docker run --rm -it --security-opt apparmor=your_profile hello-world
```

要从 AppArmor 中卸载配置文件：

```console
# 卸载配置文件
$ apparmor_parser -R /path/to/profile
```

### 编写配置文件的资源

AppArmor 中文件通配符的语法与某些其他通配符实现略有不同。强烈建议您查看以下资源，了解 AppArmor 配置文件语法。

- [快速配置文件语言](https://gitlab.com/apparmor/apparmor/wikis/QuickProfileLanguage)
- [通配符语法](https://gitlab.com/apparmor/apparmor/wikis/AppArmor_Core_Policy_Reference#AppArmor_globbing_syntax)

## Nginx 示例配置文件

在本例中，您将为 Nginx 创建一个自定义 AppArmor 配置文件。以下是自定义配置文件。

```c
#include <tunables/global>


profile docker-nginx flags=(attach_disconnected,mediate_deleted) {
  #include <abstractions/base>

  network inet tcp,
  network inet udp,
  network inet icmp,

  deny network raw,

  deny network packet,

  file,
  umount,

  deny /bin/** wl,
  deny /boot/** wl,
  deny /dev/** wl,
  deny /etc/** wl,
  deny /home/** wl,
  deny /lib/** wl,
  deny /lib64/** wl,
  deny /media/** wl,
  deny /mnt/** wl,
  deny /opt/** wl,
  deny /proc/** wl,
  deny /root/** wl,
  deny /sbin/** wl,
  deny /srv/** wl,
  deny /tmp/** wl,
  deny /sys/** wl,
  deny /usr/** wl,

  audit /** w,

  /var/run/nginx.pid w,

  /usr/sbin/nginx ix,

  deny /bin/dash mrwklx,
  deny /bin/sh mrwklx,
  deny /usr/bin/top mrwklx,


  capability chown,
  capability dac_override,
  capability setuid,
  capability setgid,
  capability net_bind_service,

  deny @{PROC}/* w,   # deny write for all files directly in /proc (not in a subdir)
  # deny write to files not in /proc/<number>/** or /proc/sys/**
  deny @{PROC}/{[^1-9],[^1-9][^0-9],[^1-9s][^0-9y][^0-9s],[^1-9][^0-9][^0-9][^0-9]*}/** w,
  deny @{PROC}/sys/[^k]** w,  # deny /proc/sys except /proc/sys/k* (effectively /proc/sys/kernel)
  deny @{PROC}/sys/kernel/{?,??,[^s][^h][^m]**} w,  # deny everything except shm* in /proc/sys/kernel/
  deny @{PROC}/sysrq-trigger rwklx,
  deny @{PROC}/mem rwklx,
  deny @{PROC}/kmem rwklx,
  deny @{PROC}/kcore rwklx,

  deny mount,

  deny /sys/[^f]*/** wklx,
  deny /sys/f[^s]*/** wklx,
  deny /sys/fs/[^c]*/** wklx,
  deny /sys/fs/c[^g]*/** wklx,
  deny /sys/fs/cg[^r]*/** wklx,
  deny /sys/firmware/** rwklx,
  deny /sys/kernel/security/** rwklx,
}
```

1. 将自定义配置文件保存到磁盘上的
   `/etc/apparmor.d/containers/docker-nginx` 文件中。

   本例中的文件路径不是必需的。在生产环境中，您可以使用其他路径。

2. 加载配置文件。

   ```console
   $ sudo apparmor_parser -r -W /etc/apparmor.d/containers/docker-nginx
   ```

3. 使用配置文件运行容器。

   要以分离模式运行 nginx：

   ```console
   $ docker run --security-opt "apparmor=docker-nginx" \
        -p 80:80 -d --name apparmor-nginx nginx
   ```

4. 进入正在运行的容器。

   ```console
   $ docker container exec -it apparmor-nginx bash
   ```

5. 尝试一些操作来测试配置文件。

   ```console
   root@6da5a2a930b9:~# ping 8.8.8.8
   ping: Lacking privilege for raw socket.

   root@6da5a2a930b9:/# top
   bash: /usr/bin/top: Permission denied

   root@6da5a2a930b9:~# touch ~/thing
   touch: cannot touch 'thing': Permission denied

   root@6da5a2a930b9:/# sh
   bash: /bin/sh: Permission denied

   root@6da5a2a930b9:/# dash
   bash: /bin/dash: Permission denied
   ```


您刚刚部署了一个使用自定义 apparmor 配置文件保护的容器。


## 调试 AppArmor

您可以使用 `dmesg` 调试问题，并使用 `aa-status` 检查已加载的配置文件。

### 使用 dmesg

以下是一些关于 AppArmor 调试的有用提示。

AppArmor 会向 `dmesg` 发送非常详细的日志消息。通常，AppArmor 行如下所示：

```text
[ 5442.864673] audit: type=1400 audit(1453830992.845:37): apparmor="ALLOWED" operation="open" profile="/usr/bin/docker" name="/home/jessie/docker/man/man1/docker-attach.1" pid=10923 comm="docker" requested_mask="r" denied_mask="r" fsuid=1000 ouid=0
```

在上面的例子中，您可以看到 `profile=/usr/bin/docker`。这意味着用户已加载 `docker-engine`（Docker Engine 守护进程）配置文件。

再看另一个日志行：

```text
[ 3256.689120] type=1400 audit(1405454041.341:73): apparmor="DENIED" operation="ptrace" profile="docker-default" pid=17651 comm="docker" requested_mask="receive" denied_mask="receive"
```

这次配置文件是 `docker-default`，默认情况下它在容器上运行，除非处于 `privileged` 模式。此行显示 apparmor 已拒绝容器中的 `ptrace`。这正是预期的行为。

### 使用 aa-status

如果您需要检查哪些配置文件已加载，可以使用 `aa-status`。输出如下所示：

```console
$ sudo aa-status
apparmor module is loaded.
14 profiles are loaded.
1 profiles are in enforce mode.
   docker-default
13 profiles are in complain mode.
   /usr/bin/docker
   /usr/bin/docker///bin/cat
   /usr/bin/docker///bin/ps
   /usr/bin/docker///sbin/apparmor_parser
   /usr/bin/docker///sbin/auplink
   /usr/bin/docker///sbin/blkid
   /usr/bin/docker///sbin/iptables
   /usr/bin/docker///sbin/mke2fs
   /usr/bin/docker///sbin/modprobe
   /usr/bin/docker///sbin/tune2fs
   /usr/bin/docker///sbin/xtables-multi
   /usr/bin/docker///sbin/zfs
   /usr/bin/docker///usr/bin/xz
38 processes have profiles defined.
37 processes are in enforce mode.
   docker-default (6044)
   ...
   docker-default (31899)
1 processes are in complain mode.
   /usr/bin/docker (29756)
0 processes are unconfined but have a profile defined.
```

上述输出显示，运行在各种容器 PID 上的 `docker-default` 配置文件处于 `enforce` 模式。这意味着 AppArmor 正在阻止并审计 `docker-default` 配置文件范围外的任何操作，并记录到 `dmesg` 中。

上述输出还显示 `/usr/bin/docker`（Docker Engine 守护进程）配置文件处于 `complain` 模式。这意味着 AppArmor 仅将配置文件范围外的活动记录到 `dmesg` 中。（除了 Ubuntu Trusty 的某些有趣行为被强制执行的情况。）

## 为 Docker 的 AppArmor 代码做贡献

高级用户和软件包管理员可以在 Docker Engine 源码仓库的
[contrib/apparmor](https://github.com/moby/moby/tree/master/contrib/apparmor)
目录下找到 `/usr/bin/docker`（Docker Engine 守护进程）的配置文件。

容器的 `docker-default` 配置文件位于
[profiles/apparmor](https://github.com/moby/profiles/blob/main/apparmor)。