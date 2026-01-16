---
title: Docker Engine 29 版本发布说明
url: /engine/release-notes/29/
parent:
  title: Docker Engine
  url: /engine/
breadcrumbs:
  - title: 手册
    url: /manuals/
  - title: Docker Engine
    url: /engine/
  - title: Docker Engine 29 版本发布说明
    url: /engine/release-notes/29/
next:
  title: Docker Engine version 28 release notes
  url: /engine/release-notes/28/
---


本文档介绍了 Docker Engine 29 版本的最新变更、新增功能、已知问题和修复内容。

更多信息请参阅：

- 已弃用和移除的功能，请参阅[已弃用的 Engine 功能](../deprecated.md)。
- Engine API 的变更，请参阅 [Engine API 版本历史](/reference/api/engine/version-history/)。

## 29.1.4

<em class="text-gray-400 italic dark:text-gray-500">2026-01-08</em>


有关此版本中拉取请求和变更的完整列表，请参阅相关的 GitHub 里程碑：

- [docker/cli, 29.1.4 里程碑](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A29.1.4)
- [moby/moby, 29.1.4 里程碑](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A29.1.4)

### 错误修复和增强功能

- 修复 Windows 上 `docker run --network none` 导致的崩溃问题。[moby/moby#51830](https://github.com/moby/moby/pull/51830)
- 修复挂载路径过长时镜像挂载失败并提示“文件名过长”的问题。[moby/moby#51829](https://github.com/moby/moby/pull/51829)
- 修复可能导致创建孤立 overlay2 层的问题。[moby/moby#51826](https://github.com/moby/moby/pull/51826)、[moby/moby#51824](https://github.com/moby/moby/pull/51824)

### 打包更新

- 将 BuildKit 更新至 [v0.26.3](https://github.com/moby/buildkit/releases/tag/v0.26.3)。[moby/moby#51821](https://github.com/moby/moby/pull/51821)

## 29.1.3

<em class="text-gray-400 italic dark:text-gray-500">2025-12-12</em>


有关此版本中拉取请求和变更的完整列表，请参阅相关的 GitHub 里程碑：

- [docker/cli, 29.1.3 里程碑](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A29.1.3)
- [moby/moby, 29.1.3 里程碑](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A29.1.3)

### 错误修复和增强功能

- 为 `docker stack deploy --compose-file` 添加 Shell 自动补全支持。[docker/cli#6690](https://github.com/docker/cli/pull/6690)
- containerd 镜像存储：修复 `docker build` 忽略显式设置的 `unpack` 镜像导出器选项的错误。[moby/moby#51514](https://github.com/moby/moby/pull/51514)
- 修复 `docker image ls` 对悬空镜像的处理逻辑。[docker/cli#6704](https://github.com/docker/cli/pull/6704)
- 修复 Engine 在关闭时可能遗留设置了自动删除的容器处于“dead”状态且永不回收的问题。[moby/moby#51693](https://github.com/moby/moby/pull/51693)
- 修复在 i386 架构上的构建问题。[moby/moby#51528](https://github.com/moby/moby/pull/51528)
- 修复当先前存在 graphdriver 状态时，显式 graphdriver 配置（`"storage-driver"`）被当作 containerd snapshotter 处理的问题。[moby/moby#51516](https://github.com/moby/moby/pull/51516)
- 修复可能导致创建孤立 overlay2 层的问题。[moby/moby#51703](https://github.com/moby/moby/pull/51703)

### 网络

- 允许在容器网络未配置特定子网的情况下创建具有特定 IP 地址的容器。[moby/moby#51583](https://github.com/moby/moby/pull/51583)
- 避免在升级到 v29.1.2 之前通过 API 创建的容器启动时崩溃（该容器设置了 `PublishAll` 且 `PortBindings` 映射为 nil）。[moby/moby#51691](https://github.com/moby/moby/pull/51691)
- 修复节点加入 Swarm 集群后，连接到非 Swarm 范围网络的容器无法解析 DNS 的问题。[moby/moby#51515](https://github.com/moby/moby/pull/51515)
- 修复使用远程网络驱动插件时导致守护进程崩溃的问题。[moby/moby#51558](https://github.com/moby/moby/pull/51558)
- 修复在创建具有多个网络连接的容器时可能导致“endpoint not found”错误的问题（其中一个网络非内部网络但无外部 IP 连接）。[moby/moby#51538](https://github.com/moby/moby/pull/51538)
- 修复在禁用 IPv6 的主机上无法启动 Rootless Docker 的问题。[moby/moby#51543](https://github.com/moby/moby/pull/51543)
- 当容器创建时端口映射指向容器端口 0 时返回错误。[moby/moby#51695](https://github.com/moby/moby/pull/51695)

## 29.1.2

<em class="text-gray-400 italic dark:text-gray-500">2025-12-02</em>


有关此版本中拉取请求和变更的完整列表，请参阅相关的 GitHub 里程碑：

- [docker/cli, 29.1.2 里程碑](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A29.1.2)
- [moby/moby, 29.1.2 里程碑](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A29.1.2)

### 安全性

- 将 Go 运行时更新至 [1.25.5](https://go.dev/doc/devel/release#go1.25.5)。[moby/moby#51648](https://github.com/moby/moby/pull/51648)、[docker/cli#6688](https://github.com/docker/cli/pull/6688)
  - 修复格式化主机名验证错误时因资源使用过多导致的潜在 DoS 问题 [**CVE-2025-61729**](https://nvd.nist.gov/vuln/detail/CVE-2025-61729)
  - 修复通配符 SAN 的排除子域名约束执行不正确的问题，该问题可能导致证书被错误信任 [**CVE-2025-61727**](https://nvd.nist.gov/vuln/detail/CVE-2025-22874)

### 错误修复和增强功能

- containerd 镜像存储：修复 `docker image inspect` 在并非所有可分发 blob 都在本地可用时无法返回可用镜像数据的问题。[moby/moby#51629](https://github.com/moby/moby/pull/51629)
- dockerd-rootless-setuptool.sh：修复 `nsenter: no namespace specified` 错误。[moby/moby#51622](https://github.com/moby/moby/pull/51622)
- 修复使用 graph-drivers 作为存储时 `docker system df` 显示共享大小和唯一大小为 `N/A` 的问题。[moby/moby#51631](https://github.com/moby/moby/pull/51631)

### 打包更新

- 将 runc（静态二进制文件）更新至 [v1.3.4](https://github.com/opencontainers/runc/releases/tag/v1.3.4)。[moby/moby#51633](https://github.com/moby/moby/pull/51633)

### 网络

- 修复在 Rootless 模式下使用 slirp4netns 时端口映射失败的问题。[moby/moby#51616](https://github.com/moby/moby/pull/51616)
- 防止在发起设置了 `HostConfig.PublishAllPorts`（`-P`）且无端口绑定的 API 请求时崩溃。[moby/moby#51621](https://github.com/moby/moby/pull/51621)

## 29.1.1

<em class="text-gray-400 italic dark:text-gray-500">2025-11-28</em>


有关此版本中拉取请求和变更的完整列表，请参阅相关的 GitHub 里程碑：

- [docker/cli, 29.1.1 里程碑](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A29.1.1)
- [moby/moby, 29.1.1 里程碑](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A29.1.1)

### 网络

- 回退一个破坏所有自定义桥接网络外部 DNS 解析的 PR。[moby/moby#51615](https://github.com/moby/moby/pull/51615)

## 29.1.0

<em class="text-gray-400 italic dark:text-gray-500">2025-11-27</em>


有关此版本中拉取请求和变更的完整列表，请参阅相关的 GitHub 里程碑：

- [docker/cli, 29.1.0 里程碑](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A29.1.0)
- [moby/moby, 29.1.0 里程碑](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A29.1.0)

### 打包更新

- 将 BuildKit 更新至 [v0.26.1](https://github.com/moby/buildkit/releases/tag/v0.26.1)。[moby/moby#51551](https://github.com/moby/moby/pull/51551)
- 将 containerd 二进制文件更新至 v2.2.0（静态二进制文件）。[moby/moby#51271](https://github.com/moby/moby/pull/51271)

### 网络

- 不再在容器重启时覆盖用户修改的 `/etc/resolv.conf`。[moby/moby#51507](https://github.com/moby/moby/pull/51507)
- 修复 Windows 容器的 `--publish-all` / `-P` 功能。[moby/moby#51586](https://github.com/moby/moby/pull/51586)
- 修复容器停止或网络断开期间网关配置失败时导致容器无法重启或重新连接网络的问题。[moby/moby#51592](https://github.com/moby/moby/pull/51592)
- Windows 容器：不在端口映射中显示 IPv6 映射的 IPv4 地址。例如，显示 `[::ffff:0.0.0.0]:8080->80/tcp` 而非 `0.0.0.0:8080->80/tcp`。[moby/moby#51587](https://github.com/moby/moby/pull/51587)

## 29.0.4

<em class="text-gray-400 italic dark:text-gray-500">2025-11-24</em>


有关此版本中拉取请求和变更的完整列表，请参阅相关的 GitHub 里程碑：

- [docker/cli, 29.0.4 里程碑](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A29.0.4)
- [moby/moby, 29.0.4 里程碑](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A29.0.4)

### 错误修复和增强功能

- `docker image ls` 不再截断镜像名称。[docker/cli#6675](https://github.com/docker/cli/pull/6675)

### 网络

- 允许在容器网络未配置特定子网的情况下创建具有特定 IP 地址的容器。[moby/moby#51583](https://github.com/moby/moby/pull/51583)

## 29.0.3

<em class="text-gray-400 italic dark:text-gray-500">2025-11-24</em>


有关此版本中拉取请求和变更的完整列表，请参阅相关的 GitHub 里程碑：

- [docker/cli, 29.0.3 里程碑](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A29.0.3)
- [moby/moby, 29.0.3 里程碑](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A29.0.3)

### 错误修复和增强功能

- `docker version --format json`：恢复顶级 `BuildTime` 字段使用 RFC3339Nano 格式。[docker/cli#6668](https://github.com/docker/cli/pull/6668)
- 修复 `docker image ls` 忽略 `docker.json` 中自定义 `imageFormat` 的问题。[docker/cli#6667](https://github.com/docker/cli/pull/6667)

### 网络

- 修复使用远程网络驱动插件时导致守护进程崩溃的问题。[moby/moby#51558](https://github.com/moby/moby/pull/51558)

## 29.0.2

<em class="text-gray-400 italic dark:text-gray-500">2025-11-17</em>


有关此版本中拉取请求和变更的完整列表，请参阅相关的 GitHub 里程碑：

- [docker/cli, 29.0.2 里程碑](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A29.0.2)
- [moby/moby, 29.0.2 里程碑](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A29.0.2)

### 网络

- 修复在创建具有多个网络连接的容器时可能导致“endpoint not found”错误的问题（其中一个网络非内部网络但无外部 IP 连接）。[moby/moby#51538](https://github.com/moby/moby/pull/51538)
- 修复在禁用 IPv6 的主机上无法启动 Rootless Docker 的问题。[moby/moby#51543](https://github.com/moby/moby/pull/51543)

## 29.0.1

<em class="text-gray-400 italic dark:text-gray-500">2025-11-14</em>


有关此版本中拉取请求和变更的完整列表，请参阅相关的 GitHub 里程碑：

- [docker/cli, 29.0.1 里程碑](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A29.0.1)
- [moby/moby, 29.0.1 里程碑](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A29.0.1)

### 错误修复和增强功能

- `docker image ls` 在输出重定向时（例如用于 `grep`）不再截断名称宽度。[docker/cli#6656](https://github.com/docker/cli/pull/6656)
- `docker image ls` 现在会考虑 `NO_COLOR` 环境变量来决定是否使用彩色输出。[docker/cli#6654](https://github.com/docker/cli/pull/6654)
- containerd 镜像存储：修复 `docker build` 忽略显式设置的 `unpack` 镜像导出器选项的错误。[moby/moby#51514](https://github.com/moby/moby/pull/51514)
- 修复 `docker image ls --all` 不显示未标记/悬空镜像的问题。[docker/cli#6657](https://github.com/docker/cli/pull/6657)
- 修复在 i386 架构上的构建问题。[moby/moby#51528](https://github.com/moby/moby/pull/51528)
- 修复当先前存在 graphdriver 状态时，显式 graphdriver 配置（`"storage-driver"`）被当作 containerd snapshotter 处理的问题。[moby/moby#51516](https://github.com/moby/moby/pull/51516)
- 修复 `docker version --format=json` 中 `ApiVersion` 和 `MinApiVersion` 字段输出格式与之前版本不一致的问题。[docker/cli#6648](https://github.com/docker/cli/pull/6648)

### 网络

- 修复节点加入 Swarm 集群后，连接到非 Swarm 范围网络的容器无法解析 DNS 的问题。[moby/moby#51515](https://github.com/moby/moby/pull/51515)

## 29.0.0

<em class="text-gray-400 italic dark:text-gray-500">2025-11-10</em>


有关此版本中拉取请求和变更的完整列表，请参阅相关的 GitHub 里程碑：

- [docker/cli, 29.0.0 里程碑](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A29.0.0)
- [moby/moby, 29.0.0 里程碑](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A29.0.0)

> [!CAUTION]
> 此版本包含多项重大变更和弃用内容。升级前请仔细查阅发布说明。

- 现在可通过将 Docker 守护进程的 `firewall-backend` 选项设置为 `nftables` 来启用对 nftables 的实验性支持。更多信息请参阅 [Docker Engine 文档](https://docs.docker.com/engine/network/firewall-nftables/)。
- containerd 镜像存储现在成为**全新安装**的默认选项。这不适用于配置了 `userns-remap` 的守护进程（参见 [moby#47377](https://github.com/moby/moby/issues/47377)）。

### 重大变更

- Go 模块 `github.com/docker/docker` 已弃用，推荐使用 `github.com/moby/moby/client` 和 `github.com/moby/moby/api`。`github.com/moby/moby` 模块被视为**内部实现细节**——唯一受支持的公共模块是 `client` 和 `api`。
  从 v29 开始，发布版本将使用 `docker-` 前缀进行标记（例如 `docker-v29.0.0`）。**这仅影响 Go 模块用户和软件包维护者。**
- 守护进程现在要求 API 版本为 `v1.44` 或更高（Docker v25.0+）。
- Debian armhf（32 位）软件包现在面向 ARMv7 CPU，无法在 ARMv6 设备上运行。
- 官方 Raspbian（32 位）软件包不再提供。64 位设备请使用 Debian arm64 软件包，32 位 ARMv7 设备请使用 Debian armhf 软件包。
- **cgroup v1 已弃用。** 支持将持续到至少 2029 年 5 月，但请尽快迁移至 cgroup v2。参见 [moby#51111](https://github.com/moby/moby/issues/51111)。
- Docker 内容信任（Docker Content Trust）已从 Docker CLI 中移除，可作为独立插件构建：https://github.com/docker/cli/blob/v29.0.0/cmd/docker-trust/main.go

---

### 新增功能

- `docker image load` 和 `docker image save` 现在支持通过 `--platform` 标志选择多个平台（例如 `docker image load --platform linux/amd64,linux/arm64 -i image.tar`）。[docker/cli#6126](https://github.com/docker/cli/pull/6126)
- `docker image ls` 现在默认使用新视图（类似 `--tree` 但已折叠）。[docker/cli#6566](https://github.com/docker/cli/pull/6566)
- `docker run --runtime <...>` 现在支持在 Windows 上使用。[moby/moby#50546](https://github.com/moby/moby/pull/50546)
- `GET /containers/json` 现在包含描述容器健康检查状态的 `Health` 字段。[moby/moby#50281](https://github.com/moby/moby/pull/50281)
- 在构建器配置中添加 `device` 权限。[moby/moby#50386](https://github.com/moby/moby/pull/50386)
- 为 `docker service create` 和 `docker service update` 命令添加对 `memory-swap` 和 `memory-swappiness` 标志的支持。[docker/cli#6619](https://github.com/docker/cli/pull/6619)
- 允许 Docker CLI 在键值对（`"GODEBUG":"..."`）存在于 Docker 上下文元数据中时设置 `GODEBUG` 环境变量。[docker/cli#6371](https://github.com/docker/cli/pull/6371)

### 错误修复和增强功能

- `docker image ls --tree` 现在按名称字母顺序排序镜像，而非按创建时间排序。[docker/cli#6595](https://github.com/docker/cli/pull/6595)
- `docker image ls` 默认不再显示未标记的镜像（除非提供 `--all` 标志）。[docker/cli#6574](https://github.com/docker/cli/pull/6574)
- `docker save`：修复使用 overlay2 存储驱动导出镜像时 tar 成员时间戳不一致的问题。[moby/moby#51365](https://github.com/moby/moby/pull/51365)
- 为 fluentd 日志驱动添加新的日志选项（`fluentd-read-timeout`），用于指定从 fluentd 连接读取确认信息的超时时间。[moby/moby#50249](https://github.com/moby/moby/pull/50249)
- 为 `docker images` 添加镜像名称自动补全功能。[docker/cli#6452](https://github.com/docker/cli/pull/6452)
- 为 `docker inspect` 添加 Shell 自动补全支持（当设置 `--type` 时）。[docker/cli#6444](https://github.com/docker/cli/pull/6444)
- 为 `docker plugin` 子命令添加 Shell 自动补全支持。[docker/cli#6445](https://github.com/docker/cli/pull/6445)
- api/types/container：将 ContainerState 和 HealthStatus 设为具体类型。[moby/moby#51439](https://github.com/moby/moby/pull/51439)
- 当启用 userns 重映射时，containerd 镜像存储暂时不可用，作为 [moby#47377](https://github.com/moby/moby/issues/47377) 的临时解决方案。[moby/moby#51042](https://github.com/moby/moby/pull/51042)
- contrib：移除仅用于集成测试的 contrib/httpserver。[moby/moby#50654](https://github.com/moby/moby/pull/50654)
- 守护进程：改进对 `--dns` 选项及 `daemon.json` 中对应 `"dns"` 字段的验证。[moby/moby#50600](https://github.com/moby/moby/pull/50600)
- dockerd-rootless.sh：如果未安装 slirp4netns，则尝试使用 pasta (passt)。[moby/moby#51149](https://github.com/moby/moby/pull/51149)
- 修复多次将同一镜像挂载到不同目标时 `--mount type=image` 失败的问题。[moby/moby#50268](https://github.com/moby/moby/pull/50268)
- 修复 `docker stats <container>` 无法优雅退出的问题。[docker/cli#6582](https://github.com/docker/cli/pull/6582)
- 修复 API 服务器在 `/events` 端点存在开放连接时无法快速关闭的问题。[moby/moby#51448](https://github.com/moby/moby/pull/51448)
- 修复在“一次性”模式下收集容器统计信息时不包含容器 ID 和名称的问题。[moby/moby#51302](https://github.com/moby/moby/pull/51302)
- 修复在扩大具有放置偏好的服务后，Swarm 中所有新任务可能永远卡在 PENDING 状态的问题。[moby/moby#50202](https://github.com/moby/moby/pull/50202)
- 修复使用 containerd 镜像存储时自定义元头未传递的问题。[moby/moby#51024](https://github.com/moby/moby/pull/51024)
- 修复使用 `--log-level=trace` 运行守护进程时请求未被记录的问题。[moby/moby#50986](https://github.com/moby/moby/pull/50986)
- 修复 firewalld 重载后 Swarm 服务无法通过发布端口访问的问题。[moby/moby#50443](https://github.com/moby/moby/pull/50443)
- 改进连接 API 失败时的错误提示，为用户提供更多上下文信息。[moby/moby#50285](https://github.com/moby/moby/pull/50285)
- 改进 `docker secret` 和 `docker config` 子命令的 Shell 自动补全功能。[docker/cli#6446](https://github.com/docker/cli/pull/6446)
- 使用 `docker run --gpus` 选择设备驱动时，优先使用显式设备驱动名称而非 GPU 能力。[moby/moby#50717](https://github.com/moby/moby/pull/50717)
- 将 runc 更新至 [v1.3.3](https://github.com/opencontainers/runc/releases/tag/v1.3.3)。[moby/moby#51393](https://github.com/moby/moby/pull/51393)
- 更新 SwarmKit 内部 TLS 配置以排除已知不安全的密码套件。[moby/moby#51139](https://github.com/moby/moby/pull/51139)
- Windows：修复 BuildKit 创建隔离模式与守护进程配置不一致的容器的问题。[moby/moby#50942](https://github.com/moby/moby/pull/50942)

### 打包更新

- 客户端：从客户端配置中移除传统的 CBC 密码套件。[moby/moby#50126](https://github.com/moby/moby/pull/50126)
- contrib：移除无人维护的 `editorconfig`。[moby/moby#50607](https://github.com/moby/moby/pull/50607)
- contrib：移除 `nano` 和 TextMate (`tmbundle`) 的 Dockerfile 语法高亮文件（因其无人维护且过时）。[moby/moby#50606](https://github.com/moby/moby/pull/50606)
- contrib：移除 mkimage-xxx 脚本（因其无人维护且未经测试）。[moby/moby#50297](https://github.com/moby/moby/pull/50297)
- 如果 Docker 降级至不支持此功能的版本，网络将变得不可用，必须删除并重新创建。[moby/moby#50114](https://github.com/moby/moby/pull/50114)
- Windows overlay 网络驱动现在支持 `--dns` 选项。[moby/moby#51229](https://github.com/moby/moby/pull/51229)
- 将 BuildKit 更新至 [v0.25.2](https://github.com/moby/buildkit/releases/tag/v0.25.2)。[moby/moby#51397](https://github.com/moby/moby/pull/51397)
- 将 containerd 更新至 [v2.1.5](https://github.com/containerd/containerd/releases/tag/v2.1.5)。[moby/moby#51409](https://github.com/moby/moby/pull/51409)

  containerd v2.1.5 现在使用 systemd 默认的 `LimitNOFILE` 设置容器，
  将打开文件描述符限制（`ulimit -n`）从 `1048576` 更改为
  `1024`。此更改将 Docker Engine v25.0 中针对构建容器引入的调整扩展至所有容器。

  这可以防止程序根据 ulimit 调整行为时在限制设为 `infinity` 时消耗过多内存。
  容器现在与主机上运行的程序行为一致。

  如果工作负载需要更高限制，请使用 `docker run` 的 `--ulimit` 选项，
  或在 `/etc/docker/daemon.json` 中设置默认值：

  ```json
  {
    "default-ulimits": {
      "nofile": {
        "Name": "nofile",
        "Soft": 1048576,
        "Hard": 1048576
      }
    }
  }
  ```

  更多信息请参阅 [moby#51485](https://github.com/moby/moby/issues/51485)。
- 将 Go 运行时更新至 [1.25.4](https://go.dev/doc/devel/release#go1.25.4)。[moby/moby#51418](https://github.com/moby/moby/pull/51418)、[docker/cli#6632](https://github.com/docker/cli/pull/6632)
- 用户可通过使用未指定地址请求默认池分配网络的特定前缀大小，例如 `--subnet 0.0.0.0/24 --subnet ::/96`。[moby/moby#50114](https://github.com/moby/moby/pull/50114)

### 网络

- 添加守护进程选项 `--bridge-accept-fwmark`。具有此防火墙标记的数据包将被桥接网络接受，覆盖 Docker 的 iptables 或 nftables “drop” 规则。[moby/moby#50476](https://github.com/moby/moby/pull/50476)
- api/types/system：弃用 `DiskUsage` 的顶级字段，改用类型特定字段。[moby/moby#51235](https://github.com/moby/moby/pull/51235)
- 确保桥接网络创建失败时移除桥接设备。[moby/moby#51147](https://github.com/moby/moby/pull/51147)
- 确保 Engine 重启时 Windows NAT 网络以其原始标签重新创建。[moby/moby#50447](https://github.com/moby/moby/pull/50447)
- 使用传统链接在容器上设置的环境变量已弃用，不再自动添加。[moby/moby#50719](https://github.com/moby/moby/pull/50719)
  - 可通过使用 `DOCKER_KEEP_DEPRECATED_LEGACY_LINKS_ENV_VARS=1` 启动守护进程来恢复此功能
  - 鼓励用户停止使用这些变量（因其已弃用），且此临时解决方案将在后续版本中移除
- 修复 NetworkDB 中的错误，该错误有时会导致条目在某些节点上卡在已删除状态，从而导致 overlay 网络上容器之间的连接问题。[moby/moby#50342](https://github.com/moby/moby/pull/50342)
- 修复可能导致 Engine 和另一主机进程绑定同一 UDP 端口的错误。[moby/moby#50669](https://github.com/moby/moby/pull/50669)
- 修复在桥接网络驱动启动、创建或删除网络或创建端口映射时处理 firewalld 重载可能导致死锁的问题。[moby/moby#50620](https://github.com/moby/moby/pull/50620)
- 修复在特定接口上仅禁用 IPv6 时导致容器无法启动或选择其网络网关的问题。[moby/moby#48971](https://github.com/moby/moby/pull/48971)
- 对于 Linux，`docker info` 现在报告可用的防火墙后端。[docker/cli#6191](https://github.com/docker/cli/pull/6191)
- 大幅提升 overlay 网络和 Swarm 路由网格的可靠性。[moby/moby#50393](https://github.com/moby/moby/pull/50393)
- 提升 NetworkDB（overlay 网络管理平面的一部分）在更新突发后的收敛速率。[moby/moby#50193](https://github.com/moby/moby/pull/50193)
- 提升 overlay 网络驱动的可靠性。[moby/moby#50260](https://github.com/moby/moby/pull/50260)
- 改进容器连接至网络时的错误处理。[moby/moby#50945](https://github.com/moby/moby/pull/50945)
- macvlan 和 IPvlan-l2 网络：除非 IPAM 配置中明确包含 `--gateway`，否则不会配置默认网关。这解决了在启用 IPv6 自动配置的网络中可能导致容器启动失败的问题。[moby/moby#50929](https://github.com/moby/moby/pull/50929)
- nftables：Docker 不会在主机上启用 IP 转发。如果桥接网络需要转发但未启用，守护进程启动或网络创建将失败并显示错误。必须启用转发并确保防火墙规则到位以防止非 Docker 接口之间的 unwanted 转发；或使用守护进程选项 `--ip-forward=false` 禁用检查（但某些桥接网络功能包括端口转发可能无法工作）。有关从 iptables 迁移至 nftables 的更多信息，请参阅 [Engine 文档](https://docs.docker.com/engine/network/firewall-nftables)。[moby/moby#50646](https://github.com/moby/moby/pull/50646)
- 守护进程启动时，先重启共享其网络栈的容器，再重启需要这些栈的容器。[moby/moby#50327](https://github.com/moby/moby/pull/50327)
- 发布端口现在在网关模式为 "routed" 的网络中始终可访问。此前，仅当路由模式网络被选为容器的默认网关时才会添加打开这些端口的规则。[moby/moby#50140](https://github.com/moby/moby/pull/50140)
- 自 28.0.0 起，仅当环境变量 `DOCKER_IPTABLES_SCTP_CHECKSUM=1` 设置时才会添加用于 SCTP 校验和的 `iptables` mangle 规则。该规则现已移除，环境变量不再生效。[moby/moby#50539](https://github.com/moby/moby/pull/50539)
- 桥接网络的 iptables 规则已更新，包括移除 `DOCKER-ISOLATION-STAGE-1` 和 `DOCKER-ISOLATION-STAGE-2` 链。通过这些更改：[moby/moby#49981](https://github.com/moby/moby/pull/49981)
  - 当 userland-proxy 未运行时，容器现在可以访问其他网络中容器发布到主机地址的端口
  - 容器现在可以访问其他网络中网关模式为 "nat-unprotected" 的容器地址上的端口
- 动态链接时，Docker 守护进程现在依赖 libnftables。[moby/moby#51033](https://github.com/moby/moby/pull/51033)
- Windows：`network inspect`：HNS 网络名称现在在选项 `com.docker.network.windowsshim.networkname` 中报告，而非 Docker 网络名称（后者仅在守护进程重启后报告）。[moby/moby#50961](https://github.com/moby/moby/pull/50961)
- Windows：守护进程重启时恢复网络，保留其与非默认 IPAM 驱动的关联。[moby/moby#50649](https://github.com/moby/moby/pull/50649)

### API

- `events` API 现在将内容类型报告为 `application/x-ndjson`（用于换行分隔的 JSON 事件流）。[moby/moby#50953](https://github.com/moby/moby/pull/50953)
- `GET /images/{name}/get` 和 `POST /images/load` 现在接受多个 `platform` 查询参数，允许导出和加载多平台镜像。[moby/moby#50166](https://github.com/moby/moby/pull/50166)
- `GET /images/{name}/json` 现在在其值为空时省略以下字段：`Parent`、`Comment`、`DockerVersion`、`Author`。[moby/moby#51072](https://github.com/moby/moby/pull/51072)
- `GET /images/{name}/json`：未设置时省略空的 `Config` 字段。[moby/moby#50915](https://github.com/moby/moby/pull/50915)
- `POST /images/{name:}/push`：移除对请求体中 API v1.4 auth-config 的兼容性支持。[moby/moby#50371](https://github.com/moby/moby/pull/50371)
- 为 Swarm 服务添加对内存交换性的支持。[moby/moby#51114](https://github.com/moby/moby/pull/51114)
  - `GET /services` 现在在 `Resource` 需求中返回 `SwapBytes` 和 `MemorySwappiness` 字段
  - `GET /services/{id}` 现在在 `Resource` 需求中返回 `SwapBytes` 和 `MemorySwappiness` 字段
  - `POST /services/create` 现在接受 `SwapBytes` 和 `MemorySwappiness` 字段作为 `Resource` 需求的一部分
  - `POST /services/{id}/update` 现在接受 `SwapBytes` 和 `MemorySwappiness` 字段作为 `Resource` 需求的一部分
  - `GET /tasks` 现在在 `Resource` 需求中返回 `SwapBytes` 和 `MemorySwappiness` 字段
  - `GET /tasks/{id}` 现在在 `Resource` 需求中返回 `SwapBytes` 和 `MemorySwappiness` 字段
- api/types/build：将 `CachePruneOptions` 类型移至 `client.BuildCachePruneOptions`。[moby/moby#50772](https://github.com/moby/moby/pull/50772)
- api/types/checkpoint：将检查点选项移至客户端模块。[moby/moby#50905](https://github.com/moby/moby/pull/50905)
- api/types/container：`OnBuild` 现在在其值为空或零时被省略。[moby/moby#51154](https://github.com/moby/moby/pull/51154)
- api/types/container：使容器配置中的 `MacAddress` 对 v1.52 及更高版本过时，改用网络端点设置。[moby/moby#51189](https://github.com/moby/moby/pull/51189)
- api/types/container：将 `ResizeOptions` 类型移至客户端中的 `ContainerResizeOptions`。[moby/moby#50773](https://github.com/moby/moby/pull/50773)
- api/types/events：将 `ListOptions` 类型移至客户端 `EventsListOptions`。[moby/moby#50774](https://github.com/moby/moby/pull/50774)
- api/types/image：将镜像选项移至客户端。[moby/moby#50776](https://github.com/moby/moby/pull/50776)
- api/types/network：将 `CreateOptions`、`ConnectOptions` 和 `DisconnectOptions` 移至客户端模块。[moby/moby#50817](https://github.com/moby/moby/pull/50817)
- api/types/network：将 `ListOptions` 和 `InspectOptions` 类型移至客户端。[moby/moby#50786](https://github.com/moby/moby/pull/50786)
- api/types/plugin：将 `ListResponse` 更改为非指针切片。[moby/moby#51440](https://github.com/moby/moby/pull/51440)
- api/types/plugin：移除已弃用的 `Config.DockerVersion`。[moby/moby#51458](https://github.com/moby/moby/pull/51458)
- api/types/registry：将 `SearchOptions` 移至客户端中的 `ImageSearchOptions`。[moby/moby#50787](https://github.com/moby/moby/pull/50787)
- api/types/registry：将 `ServiceConfig` 传统字段编组支持移至守护进程后端。[moby/moby#50826](https://github.com/moby/moby/pull/50826)
- api/types/registry：将编码/解码认证配置函数移至参考工具包。[moby/moby#50785](https://github.com/moby/moby/pull/50785)
- api/types/storage：添加 `Storage` 类型并集成到容器 inspect 中。[moby/moby#50857](https://github.com/moby/moby/pull/50857)
- api/types/swarm：弃用并移除对 `PortConfigProtocol` 的支持，改用 `network.IPProtocol`。[moby/moby#51094](https://github.com/moby/moby/pull/51094)
- api/types/swarm：将选项类型移至客户端模块。[moby/moby#50794](https://github.com/moby/moby/pull/50794)
- api/types/swarm：将 `SecretListOptions` 类型移至客户端模块。[moby/moby#50816](https://github.com/moby/moby/pull/50816)
- api/types/system：将 `DiskUsageOptions` 移至客户端。[moby/moby#50788](https://github.com/moby/moby/pull/50788)
- api/types/system：将 `SecurityOpt` 和 `DecodeSecurityOptions` 移至客户端模块。[moby/moby#50825](https://github.com/moby/moby/pull/50825)
- api/types/volume：将 ListResponse.Volumes 更改为非指针切片。[moby/moby#51454](https://github.com/moby/moby/pull/51454)
- api/types/volume：将 `ListOptions` 类型移至客户端模块。[moby/moby#50789](https://github.com/moby/moby/pull/50789)
- api/types/volume：将 `UpdateOptions` 移至客户端模块。[moby/moby#51205](https://github.com/moby/moby/pull/51205)
- api/types：守护进程：将磁盘使用结构体移至后端服务器。[moby/moby#50764](https://github.com/moby/moby/pull/50764)
- api：使 `image.InspectResponse` 中的 `GraphDriver` 字段变为可选。使用传统 graph 驱动时该字段将继续发送，使用 containerd 镜像后端时将被省略。[moby/moby#50893](https://github.com/moby/moby/pull/50893)
- api：重新定义容器网络端口类型。[moby/moby#50710](https://github.com/moby/moby/pull/50710)
- client：PluginListResult：将 Items 字段更改为非指针切片。[moby/moby#51440](https://github.com/moby/moby/pull/51440)
- 使用 API v1.52 及更高版本检查网络时，提供关于分配给网络的子网 IPAM 分配的统计信息。[moby/moby#50917](https://github.com/moby/moby/pull/50917)
- MAC 地址字段现在表示为与标准库 net.HardwareAddr 类型兼容的字节切片，而非字符串。[moby/moby#51355](https://github.com/moby/moby/pull/51355)
- 为描述 Engine API 的 Swagger 规范添加 `NetworkSummary` 和 `NetworkInspect` 的 Swagger 定义。[moby/moby#50855](https://github.com/moby/moby/pull/50855)
- 将 API 版本更新至 1.52。[moby/moby#50418](https://github.com/moby/moby/pull/50418)

### Go SDK

- 已移除 `api/pkg/progress` 和 `api/pkg/streamformatter`。[moby/moby#51153](https://github.com/moby/moby/pull/51153)
- `api/types/registry`：`EncodeAuthConfig`：零值使用空字符串。[moby/moby#50426](https://github.com/moby/moby/pull/50426)
- `api/types/versions` 已移至客户端和守护进程。[moby/moby#51284](https://github.com/moby/moby/pull/51284)
- `client.ConfigCreate`、`client.ConfigList`、`client.ConfigInspectWithRaw`、`client.ConfigUpdate` 和 `client.ConfigRemove` 方法现在接受选项结构体而非位置参数，并返回专用结果结构体。[moby/moby#51078](https://github.com/moby/moby/pull/51078)
- `client.ImageBuild`、`client.BuildCancel`、`client.ImageList`、`client.ImageRemove`、`client.ImageTag` 和 `client.ImageSearch` 方法现在接受选项结构体而非位置参数，并返回专用结果结构体。[moby/moby#51227](https://github.com/moby/moby/pull/51227)
- `client`：`ContainerExec...` 方法已重命名为 `Exec...`。[moby/moby#51262](https://github.com/moby/moby/pull/51262)
- `client`：将 `ImageInspect`、`ImageHistory`、`ImageLoad` 和 `ImageSave` 的返回值包装在结构体中。[moby/moby#51236](https://github.com/moby/moby/pull/51236)
- `ImagePull` 现在返回一个带有 `JSONMessages` 方法的对象，该方法返回消息对象的迭代器。[moby/moby#50935](https://github.com/moby/moby/pull/50935)
- `ImagePush` 现在返回一个带有 `JSONMessages` 方法的对象，该方法返回消息对象的迭代器。[moby/moby#51148](https://github.com/moby/moby/pull/51148)
- api/types/container：将 `StatsResponseReader` 移至 `client` 包。[moby/moby#50521](https://github.com/moby/moby/pull/50521)
- api/types/container：将容器选项移至客户端。[moby/moby#50897](https://github.com/moby/moby/pull/50897)
- api/types/container：将 `Port` 重命名为 `PortSummary`。[moby/moby#50711](https://github.com/moby/moby/pull/50711)
- api/types/container：StatsResponse：添加 `OSType` 字段。[moby/moby#51305](https://github.com/moby/moby/pull/51305)
- api/types：将 `ErrorResponse` 移至 `common/ErrorResponse`。[moby/moby#50632](https://github.com/moby/moby/pull/50632)
- api：移除未使用的 `DefaultVersion`、`MinSupportedAPIVersion` 常量。[moby/moby#50587](https://github.com/moby/moby/pull/50587)
- cli/command：添加 `WithUserAgent` 选项。[docker/cli#4574](https://github.com/docker/cli/pull/4574)
- client：`ContainerCommitOptions`：移除 `Pause` 字段，改用 `NoPause`。[moby/moby#51019](https://github.com/moby/moby/pull/51019)
- client：添加 `DefaultAPIVersion` 常量，定义客户端支持默认（及最大）API 版本。[moby/moby#50433](https://github.com/moby/moby/pull/50433)
- client：为客户端提供的 exec 方法添加 `ExecAPIClient` 接口。[moby/moby#50997](https://github.com/moby/moby/pull/50997)
- client：Client.PluginList：添加选项结构体。[moby/moby#51207](https://github.com/moby/moby/pull/51207)
- client：ContainersPrune：重写以使用选项结构体和结果。[moby/moby#51200](https://github.com/moby/moby/pull/51200)
- client：ImagesPrune：重写以使用选项结构体和结果。[moby/moby#51200](https://github.com/moby/moby/pull/51200)
- client：NetworksPrune：重写以使用选项结构体和结果。[moby/moby#51200](https://github.com/moby/moby/pull/51200)
- client：移除 `client.ContainerStatsResult.OSType` 字段。[moby/moby#51305](https://github.com/moby/moby/pull/51305)
- client：VolumesPrune：重写以使用选项结构体和结果。[moby/moby#51200](https://github.com/moby/moby/pull/51200)
- daemon/config：添加 `DefaultAPIVersion` 常量，定义守护进程支持默认（及最大）API 版本。[moby/moby#50436](https://github.com/moby/moby/pull/50436)
- 修复 `ContainerExecStart`、`ContainerList` 和 `Events` 中的数据竞争问题。[moby/moby#50448](https://github.com/moby/moby/pull/50448)
- IP 地址和子网现在分别为 `netip.Addr` 和 `netip.Prefix` 类型。[moby/moby#50956](https://github.com/moby/moby/pull/50956)
- 移除结构体 `NetworkSettingsBase` 和 `DefaultNetworkSettings`。`NetworkSettingsBase` 中未弃用的字段现在直接位于 `NetworkSettings` 中。[moby/moby#50846](https://github.com/moby/moby/pull/50846)
- 客户端现在使用其自己的 `client.Filters` 类型来过滤 API 请求，接口更人性化。使用 `github.com/docker/docker/api/types/filters` 包的用户在升级至 v29 客户端时需要重构代码。[moby/moby#51115](https://github.com/moby/moby/pull/51115)
- 类型 `"github.com/moby/moby/api/types/network".Summary` 和 `"github.com/moby/moby/api/types/network".Inspect` 不再是别名，其大部分字段已移至嵌入结构体中。迁移至新的 github.com/moby/moby/api 模块时，Engine API 客户端可能需要进行一些源码级更改。[moby/moby#50878](https://github.com/moby/moby/pull/50878)
- 将最低 Go 版本更新至 1.24。[docker/cli#6624](https://github.com/docker/cli/pull/6624)

### 弃用内容

- `client/pkg/jsonmessage`：移除已弃用的 `ProgressMessage`、`ErrorMessage`、`DisplayJSONMessagesToStream` 和 `Stream` 接口。[moby/moby#49264](https://github.com/moby/moby/pull/49264)
- `GET /events` 不再包含已弃用的 `status`、`id` 和 `from` 字段。这些字段已在 API v1.22 中移除，但仍包含在响应中。使用 API v1.52 或更高版本时这些字段现在被省略。[moby/moby#50832](https://github.com/moby/moby/pull/50832)
- api/types/network：CreateRequest：移除已弃用的 CheckDuplicate 字段。[moby/moby#50998](https://github.com/moby/moby/pull/50998)
- api/types/plugin：弃用 `Config.DockerVersion` 字段。[moby/moby#51109](https://github.com/moby/moby/pull/51109)
- api/types/registry：移除已弃用的 AuthConfig.Email 字段。[moby/moby#51059](https://github.com/moby/moby/pull/51059)
- api/types/strslice：弃用 StrSlice，推荐使用常规 `[]string`。[moby/moby#50292](https://github.com/moby/moby/pull/50292)
- api/types/sytem：移除已弃用的 `DiskUsage.BuilderSize`。[moby/moby#51180](https://github.com/moby/moby/pull/51180)
- api/types：将插件类型移至 api/types/plugin。[moby/moby#48114](https://github.com/moby/moby/pull/48114)
- API：弃用说明：Engine 在启动容器时自动回填空的 `PortBindings` 列表（使用空的 HostIP 和 HostPort 的 PortBinding）的行为已弃用（针对 API 1.52），并将在 API 1.53 中移除。[moby/moby#50874](https://github.com/moby/moby/pull/50874)
- build：移除经典构建器对 DCT 的支持。[docker/cli#6195](https://github.com/docker/cli/pull/6195)
- cli/command：移除已弃用的 `ResolveDefaultContext`。[docker/cli#6555](https://github.com/docker/cli/pull/6555)
- client：ImageBuildResponse：移除 OSType 字段。[moby/moby#50995](https://github.com/moby/moby/pull/50995)
- client：移除 `ImageCreate` 方法，请改用 `ImagePull` 或 `ImageImport`。[moby/moby#51366](https://github.com/moby/moby/pull/51366)
- client：移除已弃用的 `ImageListOptions.ContainerCount`。[moby/moby#51006](https://github.com/moby/moby/pull/51006)
- client：移除对协商 API 版本 < v1.44 (docker 25.0) 的支持。[moby/moby#51119](https://github.com/moby/moby/pull/51119)
- client：移除未使用的 `Client.HTTPClient()` 方法。[moby/moby#51011](https://github.com/moby/moby/pull/51011)
- daemon/graphdriver：移除已弃用的 `GetDriver()`。[moby/moby#50377](https://github.com/moby/moby/pull/50377)
- daemon：将最低 API 版本提高至 v1.44。[moby/moby#51186](https://github.com/moby/moby/pull/51186)
- 弃用 `docker commit` 上的 `--pause` 标志，推荐使用 `--no-pause`。[docker/cli#6460](https://github.com/docker/cli/pull/6460)
- 弃用 cgroup v1。[moby/moby#51360](https://github.com/moby/moby/pull/51360)、[docker/cli#6598](https://github.com/docker/cli/pull/6598)
- Go SDK：`cli-plugins/manager`：弃用元数据别名，推荐使用 `cli-plugins/manager/metadata` 中的等效项。[docker/cli#6237](https://github.com/docker/cli/pull/6237)
- Go SDK：`cli-plugins/manager`：移除仅用于内部使用的 `Candidate` 接口。[docker/cli#6237](https://github.com/docker/cli/pull/6237)
- Go SDK：`cli-plugins/manager`：移除仅用于内部使用的 `NewPluginError` 函数。[docker/cli#6237](https://github.com/docker/cli/pull/6237)
- Go SDK：`cli-plugins/manager`：移除已弃用的 `ResourceAttributesEnvvar` 常量。[docker/cli#6237](https://github.com/docker/cli/pull/6237)
- Go SDK：`cli/command`：移除 `ErrPromptTerminated`、`DisableInputEcho`、`PromptForInput` 和 `PromptForConfirmation` 工具。这些工具仅用于内部且不再使用。[docker/cli#6243](https://github.com/docker/cli/pull/6243)
- Go SDK：`cli/registry/client`：移除已弃用的 `RepoNameForReference`。[docker/cli#6206](https://github.com/docker/cli/pull/6206)
- Go SDK：api/types/build：移除已弃用的 BuildCache.Parent 字段。[moby/moby#51185](https://github.com/moby/moby/pull/51185)
- Go SDK：api/types/container：移除已弃用的 `ContainerTopOKBody` 别名。[moby/moby#50400](https://github.com/moby/moby/pull/50400)
- Go SDK：api/types/container：移除已弃用的 `ContainerUpdateOKBody` 别名。[moby/moby#50400](https://github.com/moby/moby/pull/50400)
- Go SDK：api/types/container：移除已弃用的 `Stats` 类型。[moby/moby#50492](https://github.com/moby/moby/pull/50492)
- Go SDK：api/types/filters：移除已弃用的 `ToParamWithVersion`。[moby/moby#50561](https://github.com/moby/moby/pull/50561)
- Go SDK：api/types/image：`InspectResponse`：移除已弃用的 `VirtualSize`、`Container`、`ContainerConfig`、`Parent` 和 `DockerVersion` 字段。[moby/moby#51103](https://github.com/moby/moby/pull/51103)
- Go SDK：api/types/image：移除已弃用的 Summary.VirtualSize 字段。[moby/moby#51190](https://github.com/moby/moby/pull/51190)
- Go SDK：api/types/registry：移除已弃用的 `ServiceConfig.AllowNondistributableArtifactsCIDRs` 和 `ServiceConfig.AllowNondistributableArtifactsHostnames` 字段。[moby/moby#50375](https://github.com/moby/moby/pull/50375)
- Go SDK：api/types/swarm：移除已弃用的 ServiceSpec.Networks 字段。[moby/moby#51184](https://github.com/moby/moby/pull/51184)
- GO SDK：api/types/system：移除已弃用的 `Commit.Expected` 字段。[moby/moby#51127](https://github.com/moby/moby/pull/51127)
- Go SDK：api/types：移除已弃用的别名。[moby/moby#50452](https://github.com/moby/moby/pull/50452)
- Go SDK：api：弃用 `NoBaseImageSpecifier` 常量。该常量不再使用，将在下一版本中移除。[moby/moby#50437](https://github.com/moby/moby/pull/50437)
- Go SDK：api：移除 `NoBaseImageSpecifier`。[moby/moby#50574](https://github.com/moby/moby/pull/50574)
- Go SDK：cli/command/builder：移除不再使用的 `CachePrune()`。[docker/cli#6236](https://github.com/docker/cli/pull/6236)
- Go SDK：cli/command/builder：移除 `NewBuilderCommand` 和 `NewBakeStubCommand`。[docker/cli#6335](https://github.com/docker/cli/pull/6335)
- Go SDK：cli/command/checkpoint：移除 `NewCheckpointCommand`。[docker/cli#6335](https://github.com/docker/cli/pull/6335)
- Go SDK：cli/command/checkpoint：移除已弃用的 `NewFormat`、`FormatWrite`。[docker/cli#6339](https://github.com/docker/cli/pull/6339)
- Go SDK：cli/command/completion：移除已弃用的 `NoComplete`。[docker/cli#6408](https://github.com/docker/cli/pull/6408)
- Go SDK：cli/command/config：移除 `NewConfigCommand`。[docker/cli#6335](https://github.com/docker/cli/pull/6335)
- Go SDK：cli/command/config：移除已弃用的 `NewFormat`、`FormatWrite`、`InspectFormatWrite`。[docker/cli#6339](https://github.com/docker/cli/pull/6339)
- Go SDK：cli/command/config：移除已弃用的 `RunConfigCreate`、`CreateOptions`、`RunConfigInspect`、`InspectOptions`、`RunConfigList`、`ListOptions`、`RunConfigRemove` 和 `RemoveOptions`。[docker/cli#6370](https://github.com/docker/cli/pull/6370)
- Go SDK：cli/command/container：弃用 `NewDiffFormat`、`DiffFormatWrite`。这些函数仅用于内部，将在下一版本中移除。[docker/cli#6187](https://github.com/docker/cli/pull/6187)
- Go SDK：cli/command/container：移除 `NewBuildCommand`、`NewPullCommand`、`NewPushCommand`、`NewImagesCommand`、`NewImageCommand`、`NewHistoryCommand`、`NewImportCommand`、`NewLoadCommand`、`NewRemoveCommand`、`NewSaveCommand`、`NewTagCommand`、`NewPruneCommand`。[docker/cli#6335](https://github.com/docker/cli/pull/6335)
- Go SDK：cli/command/container：移除 `NewRunCommand`、`NewExecCommand`、`NewPsCommand`、`NewContainerCommand`、`NewAttachCommand`、`NewCommitCommand`、`NewCopyCommand`、`NewCreateCommand`、`NewDiffCommand`、`NewExportCommand`、`NewKillCommand`、`NewLogsCommand`、`NewPauseCommand`、`NewPortCommand`、`NewRenameCommand`、`NewRestartCommand`、`NewRmCommand`、`NewStartCommand`、`NewStatsCommand`、`NewStopCommand`、`NewTopCommand`、`NewUnpauseCommand`、`NewUpdateCommand`、`NewWaitCommand`、`NewPruneCommand`。[docker/cli#6335](https://github.com/docker/cli/pull/6335)
- Go SDK：cli/command/container：移除不再使用的 `RunPrune()`。[docker/cli#6236](https://github.com/docker/cli/pull/6236)
- Go SDK：cli/command/container：移除已弃用的 `NewDiffFormat`、`DiffFormatWrite`。[docker/cli#6339](https://github.com/docker/cli/pull/6339)
- Go SDK：cli/command/context：移除 `NewContextCommand`。[docker/cli#6335](https://github.com/docker/cli/pull/6335)
- Go SDK：cli/command/context：移除已弃用的 `RunCreate` 和 `CreateOptions`。[docker/cli#6407](https://github.com/docker/cli/pull/6407)
- Go SDK：cli/command/context：移除已弃用的 `RunExport` 和 `ExportOptions`。[docker/cli#6407](https://github.com/docker/cli/pull/6407)
- Go SDK：cli/command/context：移除已弃用的 `RunImport`。[docker/cli#6407](https://github.com/docker/cli/pull/6407)
- Go SDK：cli/command/context：移除已弃用的 `RunRemove` 和 `RemoveOptions`。[docker/cli#6407](https://github.com/docker/cli/pull/6407)
- Go SDK：cli/command/context：移除已弃用的 `RunUpdate` 和 `UpdateOptions`。[docker/cli#6407](https://github.com/docker/cli/pull/6407)
- Go SDK：cli/command/context：移除已弃用的 `RunUse`。[docker/cli#6407](https://github.com/docker/cli/pull/6407)
- Go SDK：cli/command/formatter/swarm：移除已弃用的 `GetStacks` 函数。[docker/cli#6406](https://github.com/docker/cli/pull/6406)
- Go SDK：cli/command/image/build：弃用 `DefaultDockerfileName`、`DetectArchiveReader`、`WriteTempDockerfile`、`ResolveAndValidateContextPath`。这些工具仅用于内部，将在下一版本中移除。[docker/cli#6561](https://github.com/docker/cli/pull/6561)
- Go SDK：cli/command/image：移除不再使用的 `RunPrune()`。[docker/cli#6236](https://github.com/docker/cli/pull/6236)
- Go SDK：cli/command/image：移除已弃用的 `AuthResolver` 工具。[docker/cli#6373](https://github.com/docker/cli/pull/6373)
- Go SDK：cli/command/image：移除已弃用的 `NewHistoryFormat`、`HistoryWrite`。[docker/cli#6339](https://github.com/docker/cli/pull/6339)、[docker/cli#6339](https://github.com/docker/cli/pull/6339)
- Go SDK：cli/command/manifest：移除 `NewManifestCommand`。[docker/cli#6335](https://github.com/docker/cli/pull/6335)
- Go SDK：cli/command/network：移除 `NewNetworkCommand`。[docker/cli#6335](https://github.com/docker/cli/pull/6335)
- Go SDK：cli/command/network：移除不再使用的 `RunPrune()`。[docker/cli#6236](https://github.com/docker/cli/pull/6236)
- Go SDK：cli/command/network：移除已弃用的 `NewFormat`、`FormatWrite`。[docker/cli#6339](https://github.com/docker/cli/pull/6339)
- Go SDK：cli/command/node：移除 `NewNodeCommand`。[docker/cli#6335](https://github.com/docker/cli/pull/6335)
- Go SDK：cli/command/node：移除已弃用的 `NewFormat`、`FormatWrite`、`InspectFormatWrite`。[docker/cli#6339](https://github.com/docker/cli/pull/6339)
- Go SDK：cli/command/plugin：移除 `NewPluginCommand`。[docker/cli#6335](https://github.com/docker/cli/pull/6335)
- Go SDK：cli/command/plugin：移除已弃用的 `NewFormat`、`FormatWrite`。[docker/cli#6339](https://github.com/docker/cli/pull/6339)
- Go SDK：cli/command/registry：移除 `NewLoginCommand`、`NewLogoutCommand`、`NewSearchCommand`。[docker/cli#6335](https://github.com/docker/cli/pull/6335)
- Go SDK：cli/command/registry：移除已弃用的 `NewSearchFormat`、`SearchWrite`。[docker/cli#6339](https://github.com/docker/cli/pull/6339)
- Go SDK：cli/command/registry：移除已弃用的 `OauthLoginEscapeHatchEnvVar` 常量。[docker/cli#6463](https://github.com/docker/cli/pull/6463)
- Go SDK：cli/command/secret：移除 `NewSecretCommand`。[docker/cli#6335](https://github.com/docker/cli/pull/6335)
- Go SDK：cli/command/secret：移除已弃用的 `NewFormat`、`FormatWrite`、`InspectFormatWrite`。[docker/cli#6339](https://github.com/docker/cli/pull/6339)
- Go SDK：cli/command/service：移除 `NewServiceCommand`。[docker/cli#6335](https://github.com/docker/cli/pull/6335)
- Go SDK：cli/command/service：移除已弃用的 `NewFormat`、`InspectFormatWrite`。[docker/cli#6339](https://github.com/docker/cli/pull/6339)
- Go SDK：cli/command/stack/swarm：移除已弃用的 RunPS 和 options.PS。[docker/cli#6398](https://github.com/docker/cli/pull/6398)
- Go SDK：cli/command/stack：移除 `NewStackCommand`。[docker/cli#6335](https://github.com/docker/cli/pull/6335)
- Go SDK：cli/command/stack：移除已弃用的 RunList 和 options.List。[docker/cli#6398](https://github.com/docker/cli/pull/6398)
- Go SDK：cli/command/stack：移除已弃用的 RunServices 和 swarm.GetServices。[docker/cli#6398](https://github.com/docker/cli/pull/6398)
- Go SDK：cli/command/swarm：移除 `NewSwarmCommand`。[docker/cli#6335](https://github.com/docker/cli/pull/6335)
- Go SDK：cli/command/system：移除 `NewVersionCommand`、`NewInfoCommand`、`NewSystemCommand`、`NewEventsCommand`、`NewInspectCommand`。[docker/cli#6335](https://github.com/docker/cli/pull/6335)
- Go SDK：cli/command/task：移除已弃用的 `NewTaskFormat`、`FormatWrite`。[docker/cli#6339](https://github.com/docker/cli/pull/6339)
- Go SDK：cli/command/trust：移除 `NewTrustCommand`。[docker/cli#6335](https://github.com/docker/cli/pull/6335)
- Go SDK：cli/command/trust：移除已弃用的 `NewPruneCommand`。[docker/cli#6344](https://github.com/docker/cli/pull/6344)
- Go SDK：cli/command/trust：移除已弃用的 `SignedTagInfo`、`SignerInfo`、`NewTrustTagFormat`、`NewSignerInfoFormat`、`TagWrite`、`SignerInfoWrite`。[docker/cli#6339](https://github.com/docker/cli/pull/6339)
- Go SDK：cli/command/volume：移除 `NewVolumeCommand`、`NewPruneCommand`。[docker/cli#6335](https://github.com/docker/cli/pull/6335)
- Go SDK：cli/command/volume：移除不再使用的 `RunPrune()`。[docker/cli#6236](https://github.com/docker/cli/pull/6236)
- Go SDK：cli/command：移除仅用于内部的 `AddTrustSigningFlags`、`AddTrustVerificationFlags` 和 `AddPlatformFlag` 工具。[docker/cli#6244](https://github.com/docker/cli/pull/6244)
- Go SDK：cli/command：移除已弃用的 `DockerCli.Apply`。[docker/cli#6503](https://github.com/docker/cli/pull/6503)
- Go SDK：cli/command：移除已弃用的 `DockerCli.ContentTrustEnabled`。[docker/cli#6502](https://github.com/docker/cli/pull/6502)
- Go SDK：cli/command：移除已弃用的 `DockerCli.DefaultVersion`。[docker/cli#6502](https://github.com/docker/cli/pull/6502)
- Go SDK：cli/command：移除已弃用的 `RegistryAuthenticationPrivilegedFunc`。[docker/cli#6349](https://github.com/docker/cli/pull/6349)
- Go SDK：cli/command：移除已弃用的 `WithContentTrustFromEnv`、`WithContentTrust` 选项。[docker/cli#6502](https://github.com/docker/cli/pull/6502)
- Go SDK：cli/config/configfile：移除已弃用的 `ConfigFile.Experimental` 字段。[docker/cli#6464](https://github.com/docker/cli/pull/6464)
- Go SDK：cli/config/types：移除已弃用的 `AuthConfig.Email` 字段。[docker/cli#6515](https://github.com/docker/cli/pull/6515)
- Go SDK：cli/manifest/store：移除已弃用的 `IsNotFound`。[docker/cli#6523](https://github.com/docker/cli/pull/6523)
- Go SDK：cli：移除已弃用的 `VisitAll`、`DisableFlagsInUseLine` 工具。[docker/cli#6296](https://github.com/docker/cli/pull/6296)
- Go SDK：client：从 `APIClient` 接口中移除 `APIClient.ImageInspectWithRaw`。[moby/moby#50485](https://github.com/moby/moby/pull/50485)
- Go SDK：client：从 `ImageAPIClient` 接口中移除 `ImageAPIClient.ImageInspectWithRaw`。[moby/moby#50485](https://github.com/moby/moby/pull/50485)
- Go SDK：client：从 `ImageAPIClientDeprecated` 中移除 `ImageAPIClientDeprecated.ImageInspectWithRaw`。[moby/moby#50485](https://github.com/moby/moby/pull/50485)
- Go SDK：client：移除已弃用的 `ErrorConnectionFailed` 和 `IsErrNotFound` 函数。[moby/moby#50485](https://github.com/moby/moby/pull/50485)
- Go SDK：client：移除已弃用的 `NewClient` 和 `NewEnvClient` 函数。[moby/moby#50485](https://github.com/moby/moby/pull/50485)
- Go SDK：client：移除 `CommonAPIClient` 接口。[moby/moby#50485](https://github.com/moby/moby/pull/50485)
- Go SDK：client：移除 `ImageAPIClientDeprecated` 接口。[moby/moby#50485](https://github.com/moby/moby/pull/50485)
- Go SDK：client：移除已弃用的 `Client.ImageInspectWithRaw` 方法。[moby/moby#50485](https://github.com/moby/moby/pull/50485)
- Go SDK：container：移除已弃用的 `IsValidHealthString`。[moby/moby#50378](https://github.com/moby/moby/pull/50378)
- Go SDK：container：移除已弃用的 `IsValidStateString`。[moby/moby#50378](https://github.com/moby/moby/pull/50378)
- Go SDK：container：移除已弃用的 `StateStatus`、`WaitCondition` 及相关常量 `WaitConditionNotRunning`、`WaitConditionNextExit` 和 `WaitConditionRemoved`。[moby/moby#50378](https://github.com/moby/moby/pull/50378)
- Go SDK：弃用 `pkg/stdcopy`（已移至 `api/pkg/stdcopy`）。[moby/moby#50462](https://github.com/moby/moby/pull/50462)
- Go SDK：弃用字段 `NetworkSettingsBase.Bridge`、结构体 `NetworkSettingsBase`、`DefaultNetworkSettings` 的所有字段及结构体 `DefaultNetworkSettings`。[moby/moby#50848](https://github.com/moby/moby/pull/50848)
- Go SDK：弃用 pkg/stringid，推荐使用 `github.com/moby/moby/client/pkg/stringid`。[moby/moby#50504](https://github.com/moby/moby/pull/50504)
- Go SDK：弃用已迁移至 `github.com/moby/profiles` 的 profiles 包。[moby/moby#50481](https://github.com/moby/moby/pull/50481)
- Go SDK：oci：弃用 SetCapabilities，并进行一些 minor 清理/修复。[moby/moby#50461](https://github.com/moby/moby/pull/50461)
- Go SDK：opts：移除已弃用的 `ListOpts.GetAll`（不再使用，已被 `ListOpts.GetSlice` 替代）。[docker/cli#6293](https://github.com/docker/cli/pull/6293)
- Go SDK：opts：移除已弃用的 `NewNamedListOptsRef`、`NewNamedMapOpts`、`NamedListOpts`、`NamedMapOpts` 和 `NamedOption`。这些类型
