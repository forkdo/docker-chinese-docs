# Docker Engine 23.0 发布说明

> [!NOTE]
>
> 从 Docker Engine 23.0.0 版本开始，Buildx 现在以一个独立的软件包形式分发：`docker-buildx-plugin`。
> 在早期版本中，Buildx 包含在 `docker-ce-cli` 软件包中。
> 当你升级到此版本的 Docker Engine 时，请确保更新所有
> 软件包。例如，在 Ubuntu 上：
>
> ```console
> $ sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
> ```
>
> 有关升级 Docker Engine 的更多详情，请参阅适用于你操作系统的 [Docker Engine 安装说明][1]。

[1]: ../install/_index.md

本页面描述了 Docker Engine 23.0 版本的最新变更、新增内容、已知问题和修复。

欲了解更多信息：

- 已弃用和移除的功能，请参阅 [已弃用的 Engine 功能](../deprecated.md)。
- Engine API 的变更，请参阅 [Engine API 版本历史](/reference/api/engine/version-history/)。

从 23.0.0 版本开始，Docker Engine 不再使用 CalVer 版本号，
转而开始使用 [SemVer 版本格式](https://semver.org/)。
更改版本格式是实现 Go 模块兼容性的一个垫脚石，
但该仓库尚未使用 Go 模块，仍然需要使用 `+incompatible` 版本。
在未来的版本中，实现 Go 模块兼容性的工作将继续进行。

## 23.0.6

<em class="text-gray-400 italic dark:text-gray-500">2023-05-08</em>


有关此版本中 pull request 和变更的完整列表，请参阅相关的 GitHub里程碑：

- [docker/cli, 23.0.6 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A23.0.6)
- [moby/moby, 23.0.6 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A23.0.6)

### 问题修复和功能改进

- 修复 vfs 存储驱动在 NFS 上无法工作的问题。[moby/moby#45465](https://github.com/moby/moby/pull/45465)

### 打包更新

- 将 Go 升级到 `1.19.9`。[docker/docker-ce-packaging#889](https://github.com/docker/docker-ce-packaging/pull/889),
  [docker/cli#4254](https://github.com/docker/cli/pull/4254), [moby/moby#45455](https://github.com/moby/moby/pull/45455)
- 将 `containerd` 升级到 [v1.6.21](https://github.com/containerd/containerd/releases/tag/v1.6.21)
- 将 `runc` 升级到 [v1.1.7](https://github.com/opencontainers/runc/releases/tag/v1.1.7)


## 23.0.5

<em class="text-gray-400 italic dark:text-gray-500">2023-04-26</em>


有关此版本中 pull request 和变更的完整列表，请参阅相关的 GitHub里程碑：

- [docker/cli, 23.0.5 milestone](https://github.com/docker/cli/milestone/79?closed=1)
- [moby/moby, 23.0.5 milestone](https://github.com/moby/moby/milestone/118?closed=1)

### 问题修复和功能改进

- 为清理卷时添加 `--all` / `-a` 选项。[docker/cli#4229](https://github.com/docker/cli/pull/4229)
- 为 `docker info` 添加 `--format=json`。[docker/cli#4320](https://github.com/docker/cli/pull/4230)
- 修复 AWSLogs 日志驱动导致的日志丢失问题。[moby/moby#45350](https://github.com/moby/moby/pull/45350)
- 修复在 v23.0.4 中引入的一个回归问题，如果提供了 fixed-cidr 配置参数但未提供 bip，dockerd 将拒绝启动。[moby/moby#45403](https://github.com/moby/moby/pull/45403)
- 修复守护进程启动期间 libnetwork 中的 panic [moby/moby#45376](https://github.com/moby/moby/pull/45376)
- 修复使用 `buildx` 构建镜像时不发送“tag”事件的问题。[moby/moby#45410](https://github.com/moby/moby/pull/45410)

### 打包更新

- 将 Compose 升级到 `2.17.3`。[docker/docker-ce-packaging#883](https://github.com/docker/docker-ce-packaging/pull/883)

## 23.0.4

<em class="text-gray-400 italic dark:text-gray-500">2023-04-17</em>


有关此版本中 pull request 和变更的完整列表，请参阅相关的 GitHub里程碑：

- [docker/cli, 23.0.4 milestone](https://github.com/docker/cli/milestone/77?closed=1)
- [moby/moby, 23.0.4 milestone](https://github.com/moby/moby/milestone/117?closed=1)

### 问题修复和功能改进

- 修复 Docker CLI 23.0.0 中的一个性能回归问题 [docker/cli#4141](https://github.com/docker/cli/pull/4141)。
- 修复 `docker cp` 上的进度指示器未按预期工作的问题 [docker/cli#4157](https://github.com/docker/cli/pull/4157)。
- 修复 `docker compose --file` 的 shell 补全 [docker/cli#4177](https://github.com/docker/cli/pull/4177)。
- 修复因 `daemon.json` 中对“default-address-pools”的错误处理导致的错误 [moby/moby#45246](https://github.com/moby/moby/pull/45246)。

### 打包更新

- 修复 CentOS 9 Stream 缺失的软件包。
- 将 Go 升级到 `1.19.8`。[docker/docker-ce-packaging#878](https://github.com/docker/docker-ce-packaging/pull/878),
  [docker/cli#4164](https://github.com/docker/cli/pull/4164), [moby/moby#45277](https://github.com/moby/moby/pull/45277),
  此版本包含对 [CVE-2023-24537](https://github.com/advisories/GHSA-fp86-2355-v99r),
  [CVE-2023-24538](https://github.com/advisories/GHSA-v4m2-x4rp-hv22),
  [CVE-2023-24534](https://github.com/advisories/GHSA-8v5j-pwr7-w5f8),
  和 [CVE-2023-24536](https://github.com/advisories/GHSA-9f7g-gqwh-jpf5) 的修复


## 23.0.3

<em class="text-gray-400 italic dark:text-gray-500">2023-04-04</em>


> [!NOTE]
> 
> 由于 CentOS 9 Stream 的软件包仓库存在问题，CentOS 9 的软件包
> 目前不可用。CentOS 9 的软件包可能会稍后添加，
> 或作为下一个（23.0.4）补丁版本的一部分。

### 问题修复和功能改进

- 修复了多个可能导致 Swarm 加密覆盖网络
  无法保证其安全性的问题，解决了 [CVE-2023-28841](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-28841)、
  [CVE-2023-28840](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-28840) 和
  [CVE-2023-28842](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-28842)。
  - 内核不支持加密覆盖网络现在会报告为错误。
  - 加密覆盖网络现在会主动设置，而不是等待多个节点连接。
  - 通过使用 `xt_bpf` 内核模块，加密覆盖网络现在可在 Red Hat Enterprise Linux 9 上使用。
  - Swarm 覆盖网络的用户应查看 [GHSA-vwm3-crmr-xfxw](https://github.com/moby/moby/security/advisories/GHSA-vwm3-crmr-xfxw)
    以确保没有发生意外暴露。

### 打包更新

- 将 `containerd` 升级到 [v1.6.20](https://github.com/containerd/containerd/releases/tag/v1.6.20)。
- 将 `runc` 升级到 [v1.1.5](https://github.com/opencontainers/runc/releases/tag/v1.1.5)。


## 23.0.2

<em class="text-gray-400 italic dark:text-gray-500">2023-03-28</em>


有关此版本中 pull request 和变更的完整列表，请参阅相关的 GitHub里程碑：

- [docker/cli, 23.0.2 milestone](https://github.com/docker/cli/milestone/75?closed=1)
- [moby/moby, 23.0.2 milestone](https://github.com/moby/moby/milestone/114?closed=1)

### 问题修复和功能改进

- 完全解决了在检测到启用 AppArmor 的内核时缺少对 `apparmor_parser` 的检查问题。[containerd/containerd#8087](https://github.com/containerd/containerd/pull/8087), [moby/moby#45043](https://github.com/moby/moby/pull/45043)
- 确保在生成 BuildKit buildinfo 时，Git URL 中的凭据被脱敏。修复了 [CVE-2023-26054](https://github.com/moby/buildkit/security/advisories/GHSA-gc89-7gcr-jxqc)。[moby/moby#45110](https://github.com/moby/moby/pull/45110)
- 修复由 Dockerfile 中的 `VOLUME` 行创建的匿名卷在卷清理时被排除的问题。[moby/moby#45159](https://github.com/moby/moby/pull/45159)
- 修复在 Swarm 节点上删除卷时未能正确传播错误的问题。[moby/moby#45155](https://github.com/moby/moby/pull/45155)
- 通过禁用 mergeop/diffop 优化来临时规避 BuildKit `COPY --link` 中的一个错误。[moby/moby#45112](https://github.com/moby/moby/pull/45112)
- 当父级 Swarm 作业被移除时，正确清理子任务。[moby/swarmkit#3112](https://github.com/moby/swarmkit/pull/3112), [moby/moby#45107](https://github.com/moby/moby/pull/45107)
- 修复 Swarm 服务创建逻辑，使得 GenericResource 和非默认网络可以一起使用。[moby/swarmkit#3082](https://github.com/moby/swarmkit/pull/3082), [moby/moby#45107](https://github.com/moby/moby/pull/45107)
- 修复 Swarm CSI 支持要求 CSI 插件提供 staging 端点才能发布卷的问题。[moby/swarmkit#3116](https://github.com/moby/swarmkit/pull/3116), [moby/moby#45107](https://github.com/moby/moby/pull/45107)
- 修复在某些配置下由日志缓冲导致的 panic。[containerd/fifo#47](https://github.com/containerd/fifo/pull/47), [moby/moby#45051](https://github.com/moby/moby/pull/45051)
- 将 REST 到 Swarm gRPC API 转换层中的错误记录在调试级别，以减少冗余和噪音。[moby/moby#45016](https://github.com/moby/moby/pull/45016)
- 修复当容器外部使用 `systemd-resolved` 时，影响使用 `--dns-opt` 或 `--dns-search` 创建的容器的 DNS 解析问题。[moby/moby#45000](https://github.com/moby/moby/pull/45000)
- 修复在记录源自容器内部的 DNS 查询错误时的 panic。[moby/moby#44980](https://github.com/moby/moby/pull/44980)
- 通过允许用户使用 `--size=false` 选择退出大小计算，提高 `docker ps` 的速度。[docker/cli#4107](https://github.com/docker/cli/pull/4107)
- 将 Bash 补全支持扩展到所有插件。[docker/cli#4092](https://github.com/docker/cli/pull/4092)
- 修复当存在由 `cmd.exe` 设置的特殊环境变量时，`docker stack deploy` 在 Windows 上失败的问题。[docker/cli#4083](https://github.com/docker/cli/pull/4083)
- 通过将空的镜像标签视为与 `<none>` 相同，为未来的 API 版本增加前向兼容性。[docker/cli#4065](https://github.com/docker/cli/pull/4065)
- 原子化地写入上下文文件，以大大降低损坏的可能性，并改进损坏上下文的错误消息。[docker/cli#4063](https://github.com/docker/cli/pull/4063)

### 打包

- 将 Go 升级到 `1.19.7`。[docker/docker-ce-packaging#857](https://github.com/docker/docker-ce-packaging/pull/857), [docker/cli#4086](https://github.com/docker/cli/pull/4086), [moby/moby#45137](https://github.com/moby/moby/pull/45137)
- 将 `containerd` 升级到 `v1.6.19`。[moby/moby#45084](https://github.com/moby/moby/pull/45084), [moby/moby#45099](https://github.com/moby/moby/pull/45099)
- 将 Buildx 升级到 `v0.10.4`。[docker/docker-ce-packaging#855](https://github.com/docker/docker-ce-packaging/pull/855)
- 将 Compose 升级到 `v2.17.2`。[docker/docker-ce-packaging#867](https://github.com/docker/docker-ce-packaging/pull/867)

## 23.0.1

<em class="text-gray-400 italic dark:text-gray-500">2023-02-09</em>


有关此版本中 pull request 和变更的完整列表，请参阅相关的 GitHub里程碑：

- [docker/cli, 23.0.1 milestone](https://github.com/docker/cli/milestone/73?closed=1)
- [moby/moby, 23.0.1 milestone](https://github.com/moby/moby/milestone/113?closed=1)

### 问题修复和功能改进

- 修复如果内核启用了 AppArmor 但 `apparmor_parser` 不可用时容器无法启动的问题。[moby/moby#44942](https://github.com/moby/moby/pull/44942)
- 修复启用 BuildKit 的构建使用内联缓存导致守护进程崩溃的问题。[moby/moby#44944](https://github.com/moby/moby/pull/44944)
- 修复 BuildKit 错误加载由先前版本创建的缓存层的问题。[moby/moby#44959](https://github.com/moby/moby/pull/44959)
- 修复升级前创建的 `ipvlan` 网络导致守护进程无法启动的问题。[moby/moby#44937](https://github.com/moby/moby/pull/44937)
- 修复 `overlay2` 存储驱动在不支持的备份文件系统上初始化时，在 `metacopy` 测试早期失败的问题。[moby/moby#44922](https://github.com/moby/moby/pull/44922)
- 修复在某些运行时（如 Kata Containers）中，`exec` 退出事件被误解释为容器退出的问题。[moby/moby#44892](https://github.com/moby/moby/pull/44892)
- 改进 CLI 在收到因 API 在请求中途挂断而导致的截断 JSON 响应时返回的错误消息。[docker/cli#4004](https://github.com/docker/cli/pull/4004)
- 修复在使用 Go 1.20 编译的 `runc` 尝试执行目录时错误的 CLI 退出代码。[docker/cli#4004](https://github.com/docker/cli/pull/4004)
- 修复对 `--device-write-bps` 的 size 参数的错误处理（误将其当作路径）。[docker/cli#4004](https://github.com/docker/cli/pull/4004)

### 打包

- 将 `/etc/docker` 添加到 RPM 和 DEB 打包中。[docker/docker-ce-packaging#842](https://github.com/docker/docker-ce-packaging/pull/842)
  - 并非所有用例都会受益；如果你依赖此功能，应明确执行 `mkdir -p /etc/docker`。
- 将 Compose 升级到 `v2.16.0`。[docker/docker-ce-packaging#844](https://github.com/docker/docker-ce-packaging/pull/844)

## 23.0.0

<em class="text-gray-400 italic dark:text-gray-500">2023-02-01</em>


有关此版本中 pull request 和变更的完整列表，请参阅相关的 GitHub里程碑：

- [docker/cli, 23.0.0 milestone](https://github.com/docker/cli/milestone/51?closed=1)
- [moby/moby, 23.0.0 milestone](https://github.com/moby/moby/milestone/91?closed=1)

### 新增

- 在 Linux 上将 Buildx 和 BuildKit 设为默认构建器。[moby/moby#43992](https://github.com/moby/moby/pull/43992)
  - 将 `docker build` 设置为 `docker buildx build` 的别名。[docker/cli#3314](https://github.com/docker/cli/pull/3314)
  - 仍然可以通过显式设置 `DOCKER_BUILDKIT=0` 来使用旧版构建器。
  - BuildKit 和旧版构建器在处理多阶段构建方面存在差异。更多信息，请参阅
    [多阶段构建](/manuals/build/building/multi-stage.md#differences-between-legacy-builder-and-buildkit)。
- 添加对拉取 `zstd` 压缩层的支持。[moby/moby#41759](https://github.com/moby/moby/pull/41759), [moby/moby#42862](https://github.com/moby/moby/pull/42862)
- 添加对 Linux 上替代 OCI 运行时的支持，兼容 containerd runtime v2 API。[moby/moby#43887](https://github.com/moby/moby/pull/43887), [moby/moby#43993](https://github.com/moby/moby/pull/43993)
- 添加对 Windows 上 containerd `runhcs` shim 的支持（默认关闭）。[moby/moby#42089](https://github.com/moby/moby/pull/42089)
- 添加 `dockerd --validate` 以检查守护进程 JSON 配置并退出。[moby/moby#42393](https://github.com/moby/moby/pull/42393)
- 添加通过标志或 JSON 配置守护进程 HTTP 代理的功能。[moby/moby#42835](https://github.com/moby/moby/pull/42835)
- 添加对 RFC 3021 点对点网络（IPv4 /31）和单主机（IPv4 /32）的支持。对于有两个或更少地址的网络，IPAM 不会保留网络和广播地址。[moby/moby#42626](https://github.com/moby/moby/pull/42626)
- 添加在 `ipvlan` 网络驱动中设置 `ipvlan_flag` 和使用 `l3s` `ipvlan_mode` 的支持。[moby/moby#42542](https://github.com/moby/moby/pull/42542)
- 添加显示 `overlay2` 存储驱动的 `metacopy` 选项值的支持。[moby/moby#43557](https://github.com/moby/moby/pull/43557)
- 添加使用 `IDType://ID` 语法描述 Windows 设备的支持。[moby/moby#43368](https://github.com/moby/moby/pull/43368)
- 添加 `RootlessKit`、`slirp4netns` 和 `VPNKit` 版本报告。[moby/moby#42330](https://github.com/moby/moby/pull/42330)
- 添加对 SwarmKit 集群卷（CSI）的实验性支持。[moby/moby#41982](https://github.com/moby/moby/pull/41982)
  - CLI：向 `docker volume` 添加集群卷（CSI）选项。[docker/cli#3606](https://github.com/docker/cli/pull/3606)
  - CLI：向 `docker stack` 添加集群卷（CSI）支持。[docker/cli#3662](https://github.com/docker/cli/pull/3662)
- 在 `docker stack deploy` 中添加对 SwarmKit 作业的支持。[docker/cli#2907](https://github.com/docker/cli/pull/2907)
- 添加新的 `docker stack config` 命令，用于输出 `stack deploy` 使用的合并和插值后的配置文件。[docker/cli#3544](https://github.com/docker/cli/pull/3544)
- 添加新的 `docker context show` 命令，用于打印当前上下文的名称。[docker/cli#3567](https://github.com/docker/cli/pull/3567)
- 向所有支持 `--format` 标志的命令添加 `--format=json` 作为 `--format="{{ json . }}"` 的简写变体。[docker/cli#2936](https://github.com/docker/cli/pull/2936)
- 向 `docker create` 和 `docker run` 命令添加 `--quiet` 选项，以在拉取镜像时抑制输出。[docker/cli#3377](https://github.com/docker/cli/pull/3377)
- 向 `docker network rm` 子命令添加 `--force` 选项。即使网络不存在，也会导致 CLI 返回 0 退出代码。对服务器端移除网络的流程没有影响。[docker/cli#3547](https://github.com/docker/cli/pull/3547)
- 向 `docker stop` 和 `docker restart` 添加 `--signal` 选项。[docker/cli#3614](https://github.com/docker/cli/pull/3614)
- 向 `docker-proxy` 添加 `-v/--version` 标志。[moby/moby#44703](https://github.com/moby/moby/pull/44703)
- 当守护进程以 rootless 模式运行时，现在会在众所周知的用户级路径中发现插件。[moby/moby#44778](https://github.com/moby/moby/pull/44778)
- 守护进程现在可以优雅地处理 JSON 配置文件中常见的替代 JSON 编码，并报告有用的错误。[moby/moby#44777](https://github.com/moby/moby/pull/44777), [moby/moby#44832](https://github.com/moby/moby/pull/44832)
  - 接受带字节顺序标记 (BOM) 的 UTF-8。
  - 接受带字节顺序标记 (BOM) 的 UTF-16。
  - 无效的 UTF-8 会提早报告并带有易于理解的错误消息。
- 允许通过 `docker commit` 使用 `STOPSIGNAL`。[moby/moby#43369](https://github.com/moby/moby/pull/43369)
- 向 `awslogs` 日志驱动添加一个新选项，允许跳过在 CloudWatch 中创建日志流。[moby/moby#42132](https://github.com/moby/moby/pull/42132)
- 向 `awslogs` 日志驱动添加一个新选项，以指定发送到 CloudWatch 的日志格式。[moby/moby#42838](https://github.com/moby/moby/pull/42838)
- 向 `fluentd` 日志驱动添加一个新选项，以设置重连间隔。[moby/moby#43100](https://github.com/moby/moby/pull/43100)
- 向 Go API 客户端添加新的选项设置器：`WithTLSClientConfigFromEnv()`、`WithHostFromEnv()` 和 `WithVersionFromEnv()`。[moby/moby#42224](https://github.com/moby/moby/pull/42224)
- 通过 `docker completion` 子命令添加生成 shell 命令补全的功能。[docker/cli#3429](https://github.com/docker/cli/pull/3429)
- API：向 `GET /_ping` 和 `HEAD /_ping` 添加 `Sw
