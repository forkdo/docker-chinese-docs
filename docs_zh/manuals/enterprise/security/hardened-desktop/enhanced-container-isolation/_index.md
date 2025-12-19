---
title: 增强容器隔离
linkTitle: 增强容器隔离
description: 增强容器隔离（ECI）通过防止恶意容器危害 Docker Desktop 或主机系统，为 Docker Desktop 提供额外的安全保护
keywords: enhanced container isolation, container security, sysbox runtime, linux user namespaces, hardened desktop
aliases:
 - /desktop/hardened-desktop/enhanced-container-isolation/
 - /security/for-admins/hardened-desktop/enhanced-container-isolation/
 - /security/hardened-desktop/enhanced-container-isolation/how-eci-works
 - /security/hardened-desktop/enhanced-container-isolation/features-benefits
weight: 10
---

{{< summary-bar feature_name="Hardened Docker Desktop" >}}

增强容器隔离（ECI）可防止恶意容器危害 Docker Desktop 或主机系统。它自动应用高级安全技术，同时保持完整的开发者生产力和工作流兼容性。

ECI 加强了容器隔离，并锁定管理员创建的安全配置，例如 [注册表访问管理策略](/manuals/enterprise/security/hardened-desktop/registry-access-management.md) 和 [设置管理](../settings-management/_index.md) 控制。

> [!NOTE]
>
> ECI 与其他 Docker 安全功能（如减少的 Linux 能力、seccomp 和 AppArmor）协同工作。

## 谁应该使用增强容器隔离？

增强容器隔离专为以下场景设计：

- 希望防止基于容器的攻击并减少开发者环境中安全漏洞的组织
- 需要更强容器隔离而不影响开发者工作流的安全团队
- 需要在运行不受信任或第三方容器镜像时获得额外保护的企业

## 增强容器隔离的工作原理

Docker 使用 [Sysbox 容器运行时](https://github.com/nestybox/sysbox) 实现 ECI，这是一个
标准 OCI runc 运行时的安全增强分支。启用 ECI 后，通过 `docker run` 或 `docker create` 创建的容器自动使用 Sysbox 而非 runc，无需更改开发者工作流。

即使使用 `--privileged` 标志的容器也能在增强容器隔离下安全运行，防止它们突破 Docker Desktop 虚拟机或其他容器。

> [!NOTE]
>
> 启用 ECI 时，Docker CLI 的 `--runtime` 标志将被忽略。
Docker 的默认运行时仍然是 runc，但所有用户容器
隐式使用 Sysbox 启动。

## 关键安全功能

### Linux 用户命名空间隔离

启用增强容器隔离后，所有容器都利用 Linux 用户命名空间实现更强隔离。容器中的 root 用户映射到 Docker Desktop VM 中的非特权用户：

```console
$ docker run -it --rm --name=first alpine
/ # cat /proc/self/uid_map
         0     100000      65536
```

此输出显示容器 root（0）映射到 VM 中的非特权用户 100000，范围为 64K 用户 ID。每个容器获得独占映射：

```console
$ docker run -it --rm --name=second alpine
/ # cat /proc/self/uid_map
         0     165536      65536
```

未启用增强容器隔离时，容器以真正的 root 身份运行：

```console
$ docker run -it --rm alpine
/ # cat /proc/self/uid_map
         0       0     4294967295
```

通过使用 Linux 用户命名空间，ECI 确保容器进程在 Linux VM 中从未以有效用户 ID 运行，将其能力限制在容器内的资源。

### 安全的特权容器

特权容器（`docker run --privileged`）通常构成重大安全风险，因为它们提供对 Linux 内核的无限制访问。未启用 ECI 时，特权容器可以：

- 以真正的 root 身份运行并拥有所有能力
- 绕过 seccomp 和 AppArmor 限制
- 访问所有硬件设备
- 修改全局内核设置

在保护开发者环境时，特权容器给组织带来挑战，因为它们可能控制 Docker Desktop VM 并更改安全设置，如注册表访问管理和网络代理。

增强容器隔离通过确保特权容器只能访问容器边界内的资源来转换它们。例如，特权容器无法访问 Docker Desktop 的网络配置：

```console
$ docker run --privileged djs55/bpftool map show
Error: can't get next map: Operation not permitted
```

未启用 ECI 时，特权容器可以轻松访问和修改这些设置：

```console
$ docker run --privileged djs55/bpftool map show
17: ringbuf  name blocked_packets  flags 0x0
        key 0B  value 0B  max_entries 16777216  memlock 0B
18: hash  name allowed_map  flags 0x0
        key 4B  value 4B  max_entries 10000  memlock 81920B
```

高级容器工作负载（如 Docker-in-Docker 和 Kubernetes-in-Docker）在 ECI 下仍可工作，但安全性大大提高。

> [!NOTE]
>
> ECI 不阻止用户运行特权容器，而是通过限制其访问范围使其安全。修改全局内核设置的特权工作负载（加载内核模块、更改 Berkeley Packet Filter 设置）将收到"权限被拒绝"错误。

### 命名空间隔离强制执行

增强容器隔离防止容器与 Docker Desktop VM 共享 Linux 命名空间，维持隔离边界：

**PID 命名空间共享被阻止：**

```console
$ docker run -it --rm --pid=host alpine
docker: Error response from daemon: failed to create shim task: OCI runtime create failed: error in the container spec: invalid or unsupported container spec: sysbox containers can't share namespaces [pid] with the host (because they use the linux user-namespace for isolation): unknown.
```

**网络命名空间共享被阻止：**

```console
$ docker run -it --rm --network=host alpine
docker: Error response from daemon: failed to create shim task: OCI runtime create failed: error in the container spec: invalid or unsupported container spec: sysbox containers can't share a network namespace with the host (because they use the linux user-namespace for isolation): unknown.
```

**用户命名空间覆盖被忽略：**

```console
$ docker run -it --rm --userns=host alpine
/ # cat /proc/self/uid_map
         0     100000      65536
```

使用 `--network-host` 的 Docker 构建操作和 Docker buildx 特权（`network.host`、`security.insecure`）也被阻止。

### 受保护的绑定挂载

增强容器隔离在防止访问敏感 VM 目录的同时，保持对标准文件共享的支持：

主机目录挂载继续工作：

```console
$ docker run -it --rm -v $HOME:/mnt alpine
/ # ls /mnt
# 成功列出主目录内容
```

VM 配置挂载被阻止：

```console
$ docker run -it --rm -v /etc/docker/daemon.json:/mnt/daemon.json alpine
docker: Error response from daemon: failed to create shim task: OCI runtime create failed: error in the container spec: can't mount /etc/docker/daemon.json because it's configured as a restricted host mount: unknown
```

这防止容器读取或修改 Docker Engine 配置、注册表访问管理设置、代理配置和其他安全相关的 VM 文件。

> [!NOTE]
>
> 默认情况下，ECI 阻止绑定挂载 Docker Engine 套接字（/var/run/docker.sock），因为这会授予容器对 Docker Engine 的控制权。管理员可以为受信任的容器镜像创建例外。

### 高级系统调用保护

增强容器隔离拦截敏感系统调用，防止容器恶意使用合法能力：

```console
$ docker run -it --rm --cap-add SYS_ADMIN -v $HOME:/mnt:ro alpine
/ # mount -o remount,rw /mnt /mnt
mount: permission denied (are you root?)
```

即使具有 `CAP_SYS_ADMIN` 能力，容器也无法将只读绑定挂载更改为读写，确保它们无法突破容器边界。

容器仍可在其文件系统内创建内部挂载：

```console
/ # mkdir /root/tmpfs
/ # mount -t tmpfs tmpfs /root/tmpfs
/ # mount -o remount,ro /root/tmpfs /root/tmpfs
/ # findmnt | grep tmpfs
├─/root/tmpfs    tmpfs      tmpfs    ro,relatime,uid=100000,gid=100000
```

ECI 通过仅拦截控制路径系统调用（很少使用）而保持数据路径系统调用不受影响，高效执行系统调用过滤，维持容器性能。

### 自动文件系统用户 ID 映射

增强容器隔离通过自动文件系统映射解决具有不同用户 ID 范围的容器之间的文件共享挑战。

每个容器获得独占用户 ID 映射，但 Sysbox 使用 Linux 内核 ID 映射挂载（2021 年添加）或替代 shiftsfs 模块进行文件系统用户 ID 重映射。这将容器真实用户 ID 的文件系统访问映射到标准范围，实现：

- 在具有不同用户 ID 范围的容器之间共享卷
- 无论容器用户 ID 映射如何，文件所有权保持一致
- 无需用户干预的透明文件访问

### 通过文件系统仿真隐藏信息

ECI 在容器内仿真 `/proc` 和 `/sys` 文件系统的部分，以隐藏敏感主机信息并为内核资源提供每个容器的视图：

```console
$ docker run -it --rm alpine
/ # cat /proc/uptime
5.86 5.86
```

这显示容器正常运行时间而非 Docker Desktop VM 正常运行时间，防止系统信息泄露到容器中。

几个 Linux 内核未命名空间化的 `/proc/sys` 资源被每个容器仿真，Sysbox 在编程内核设置时协调值。这使得通常需要特权访问的容器工作负载能够安全运行。

## 性能和兼容性

增强容器隔离维持优化的性能和完全兼容性：

- 无性能影响：系统调用过滤仅针对控制路径调用，不影响数据路径操作
- 完全工作流兼容性：现有开发流程、工具和容器镜像无需更改即可工作
- 高级工作负载支持：Docker-in-Docker、Kubernetes-in-Docker 和其他复杂场景安全运行
- 自动管理：用户 ID 映射、文件系统访问和安全策略自动处理
- 标准镜像支持：无需特殊容器镜像或修改

> [!IMPORTANT]
>
> ECI 保护因 Docker Desktop 版本而异，目前不保护扩展容器。Docker 构建和 Docker Desktop 中的 Kubernetes 具有不同程度的保护，具体取决于版本。详细信息请参阅 [增强容器隔离限制](/manuals/enterprise/security/hardened-desktop/enhanced-container-isolation/limitations.md)。