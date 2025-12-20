# Docker 的 AppArmor 安全配置文件

AppArmor (Application Armor) 是一种 Linux 安全模块，用于保护操作系统及其应用程序免受安全威胁。使用时，系统管理员需要将 AppArmor 安全配置文件与每个程序关联。Docker 期望找到已加载并强制执行的 AppArmor 策略。

Docker 会自动为容器生成并加载一个名为 `docker-default` 的默认配置文件。Docker 二进制文件会在 `tmpfs` 中生成此配置文件，然后将其加载到内核中。

> [!NOTE]
>
> 此配置文件用于容器，而非 Docker 守护进程。

Docker Engine 守护进程存在对应的配置文件，但目前并未随 `deb` 软件包安装。如果您对守护进程配置文件的源码感兴趣，可以在 Docker Engine 源代码仓库的 [contrib/apparmor](https://github.com/moby/moby/tree/master/contrib/apparmor) 目录中找到。

## 了解策略

`docker-default` 配置文件是运行容器的默认配置。它在提供广泛的应用程序兼容性的同时，也提供了适度的保护。该配置文件是根据以下 [模板](https://github.com/moby/profiles/blob/main/apparmor/template.go) 生成的。

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

要从 AppArmor 卸载配置文件：

```console
# 卸载配置文件
$ apparmor_parser -R /path/to/profile
```

### 编写配置文件的资源

AppArmor 中的文件通配符语法与其他一些通配符实现略有不同。强烈建议您查看以下有关 AppArmor 配置文件语法的资源。

- [Quick Profile Language](https://gitlab.com/apparmor/apparmor/wikis/QuickProfileLanguage)
- [Globbing Syntax](https://gitlab.com/apparmor/apparmor/wikis/AppArmor_Core_Policy_Reference#AppArmor_globbing_syntax)

## Nginx 示例配置文件

在此示例中，您将为 Nginx 创建一个自定义 AppArmor 配置文件。以下是自定义配置文件。

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

  deny @{PROC}/* w,   # 拒绝直接在 /proc 下（非子目录中）的所有文件的写入权限
  # 拒绝对非 /proc/<number>/** 或 /proc/sys/** 文件的写入权限
  deny @{PROC}/{[^1-9],[^1-9][^0-9],[^1-9s][^0-9y][^0-9s],[^1-9][^0-9][^0-9][^0-9]*}/** w,
  deny @{PROC}/sys/[^k]** w,  # 拒绝 /proc/sys，除了 /proc/sys/k*（实际上是 /proc/sys/kernel）
  deny @{PROC}/sys/kernel/{?,??,[^s][^h][^m]**} w,  # 拒绝 /proc/sys/kernel/ 中除 shm* 之外的所有内容
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

1. 将自定义配置文件保存到磁盘的 `/etc/apparmor.d/containers/docker-nginx` 文件中。

   此示例中的文件路径不是强制要求。在生产环境中，您可以使用其他路径。

2. 加载配置文件。

   ```console
   $ sudo apparmor_parser -r -W /etc/apparmor.d/containers/docker-nginx
   ```

3. 使用该配置文件运行容器。

   以分离模式运行 nginx：

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

您可以使用 `dmesg` 来调试问题，并使用 `aa-status` 检查已加载的配置文件。

### 使用 dmesg

以下是一些有用的提示，用于调试您可能遇到的任何与 AppArmor 相关的问题。

AppArmor 会向 `dmesg` 发送大量详细消息。通常，AppArmor 的一行日志如下所示：

```text
[ 5442.864673] audit: type=1400 audit(1453830992.845:37): apparmor="ALLOWED" operation="open" profile="/usr/bin/docker" name="/home/jessie/docker/man/man1/docker-attach.1" pid=10923 comm="docker" requested_mask="r" denied_mask="r" fsuid=1000 ouid=0
```

在上面的示例中，您可以看到 `profile=/usr/bin/docker`。这意味着用户已加载 `docker-engine` (Docker Engine 守护进程) 配置文件。

再看另一行日志：

```text
[ 3256.689120] type=1400 audit(1405454041.341:73): apparmor="DENIED" operation="ptrace" profile="docker-default" pid=17651 comm="docker" requested_mask="receive" denied_mask="receive"
```

这次的配置文件是 `docker-default`，除非在 `privileged` 模式下，否则默认在容器上运行。此行显示 apparmor 已在容器中拒绝了 `ptrace`。这完全符合预期。

### 使用 aa-status

如果需要检查哪些配置文件已加载，可以使用 `aa-status`。输出如下所示：

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

上面的输出显示，运行在各种容器 PID 上的 `docker-default` 配置文件处于 `enforce` 模式。这意味着 AppArmor 正在主动阻止任何超出 `docker-default` 配置文件范围的操作，并将这些操作记录到 `dmesg` 中。

上面的输出还显示 `/usr/bin/docker` (Docker Engine 守护进程) 配置文件正在 `complain` 模式下运行。这意味着 AppArmor 仅将超出配置文件范围的活动记录到 `dmesg` 中。（Ubuntu Trusty 的情况除外，该版本会强制执行一些有趣的行为。）

## 为 Docker 的 AppArmor 代码做贡献

高级用户和软件包管理器可以在 Docker Engine 源代码仓库的 [contrib/apparmor](https://github.com/moby/moby/tree/master/contrib/apparmor) 目录下找到 `/usr/bin/docker` (Docker Engine 守护进程) 的配置文件。

容器的 `docker-default` 配置文件位于 [profiles/apparmor](https://github.com/moby/profiles/blob/main/apparmor)。
