# Docker Engine 29 版本发布说明


此页面描述了 Docker Engine 29 版本的最新变更、新增功能、已知问题和修复。

更多信息请参阅：

- 已弃用和移除的功能，请参阅 [已弃用的 Engine 功能](../deprecated.md)。
- Engine API 的变更，请参阅 [Engine API 版本历史](/reference/api/engine/version-history/)。

## 29.2.0

<em class="text-gray-400 italic dark:text-gray-500">2026-01-26</em>


有关此版本中完整的拉取请求和变更列表，请参阅相关的 GitHub 里程碑：

- [docker/cli, 29.2.0 里程碑](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A29.2.0)
- [moby/moby, 29.2.0 里程碑](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A29.2.0)

### 新增功能

- `docker info` 现在包含 `NRI` 部分。[docker/cli#6710](https://github.com/docker/cli/pull/6710)
- 添加实验性 NRI 支持。[moby/moby#51711](https://github.com/moby/moby/pull/51711), [moby/moby#51712](https://github.com/moby/moby/pull/51712), [moby/moby#51675](https://github.com/moby/moby/pull/51675), [moby/moby#51674](https://github.com/moby/moby/pull/51674), [moby/moby#51636](https://github.com/moby/moby/pull/51636), [moby/moby#51634](https://github.com/moby/moby/pull/51634)
- 在检查端点中添加了新的 `Identity` 字段，以显示有关镜像的可信来源信息。这包括本地构建镜像的构建引用、拉取镜像的远程注册表仓库，以及包含有效签名证明声明的镜像的验证签名信息。[moby/moby#51737](https://github.com/moby/moby/pull/51737)

### 错误修复和增强

- 改进 `--detach-keys` 命令行选项的验证。[docker/cli#6742](https://github.com/docker/cli/pull/6742)
- 防止在不完整初始化后守护进程关闭时出现潜在的 panic。[moby/moby#51797](https://github.com/moby/moby/pull/51797)
- 移除对匿名只读卷的限制。[moby/moby#51682](https://github.com/moby/moby/pull/51682)
- dockerd 上的 `--validate` 标志现在还会验证系统要求，允许在启动守护进程之前检查系统要求。[moby/moby#51868](https://github.com/moby/moby/pull/51868)
- 如果可能，使用 CDI 处理对 NVIDIA 设备的 `--gpus` 请求。[moby/moby#50228](https://github.com/moby/moby/pull/50228)

### 包更新

- 将 BuildKit 更新到 [v0.27.0](https://github.com/moby/buildkit/releases/tag/v0.27.0)。[moby/moby#51886](https://github.com/moby/moby/pull/51886)
- 将 containerd（仅静态二进制文件）更新到 [v2.2.1](https://github.com/containerd/containerd/releases/tag/v2.2.1)。[moby/moby#51765](https://github.com/moby/moby/pull/51765)

### 无根模式

- 无根模式：在查找 CDI 设备时考虑 `$XDG_CONFIG_HOME/cdi` 和 `$XDG_RUNTIME_DIR/cdi`。[moby/moby#51624](https://github.com/moby/moby/pull/51624)
- 将 RootlessKit 更新到 [v2.3.6](https://github.com/rootless-containers/rootlesskit/releases/tag/v2.3.6)。[moby/moby#51757](https://github.com/moby/moby/pull/51757)

### API

- 在监听套接字上原生支持 gRPC。[moby/moby#50744](https://github.com/moby/moby/pull/50744)

### Go SDK

- cli/command: 添加 WithAPIClientOptions 选项。[docker/cli#6740](https://github.com/docker/cli/pull/6740)

### 弃用

- 从 Windows 上用于 CLI 插件的路径列表中移除 `%PROGRAMDATA%\Docker\cli-plugins`。此路径是为了与旧安装向后兼容而存在的，但已被 `%ProgramFiles%\Docker\cli-plugins` 替代。[docker/cli#6713](https://github.com/docker/cli/pull/6713)

## 29.1.5

<em class="text-gray-400 italic dark:text-gray-500">2026-01-16</em>


有关此版本中完整的拉取请求和变更列表，请参阅相关的 GitHub 里程碑：

- [docker/cli, 29.1.5 里程碑](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A29.1.5)
- [moby/moby, 29.1.5 里程碑](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A29.1.5)

### 包更新

- 将 Go 运行时更新到 [1.25.6](https://go.dev/doc/devel/release#go1.25.6)。[moby/moby#51860](https://github.com/moby/moby/pull/51860), [docker/cli#6750](https://github.com/docker/cli/pull/6750)

### 网络

- 修复了一个回归问题，其中在容器关闭宽限期期间可能会中断已建立的网络连接。[moby/moby#51843](https://github.com/moby/moby/pull/51843)

## 29.1.4

<em class="text-gray-400 italic dark:text-gray-500">2026-01-08</em>


有关此版本中完整的拉取请求和变更列表，请参阅相关的 GitHub 里程碑：

- [docker/cli, 29.1.4 里程碑](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A29.1.4)
- [moby/moby, 29.1.4 里程碑](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A29.1.4)

### 错误修复和增强

- 修复 Windows 上 `docker run --network none` 的 panic。[moby/moby#51830](https://github.com/moby/moby/pull/51830)
- 修复由于挂载路径过长导致的镜像挂载失败问题，错误为"文件名太长"。[moby/moby#51829](https://github.com/moby/moby/pull/51829)
- 修复可能创建孤立的 overlay2 层的问题。[moby/moby#51826](https://github.com/moby/moby/pull/51826), [moby/moby#51824](https://github.com/moby/moby/pull/51824)

### 包更新

- 将 BuildKit 更新到 [v0.26.3](https://github.com/moby/buildkit/releases/tag/v0.26.3)。[moby/moby#51821](https://github.com/moby/moby/pull/51821)

## 29.1.3

<em class="text-gray-400 italic dark:text-gray-500">2025-12-12</em>


有关此版本中完整的拉取请求和变更列表，请参阅相关的 GitHub 里程碑：

- [docker/cli, 29.1.3 里程碑](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A29.1.3)
- [moby/moby, 29.1.3 里程碑](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A29.1.3)

### 错误修复和增强

- 为 `docker stack deploy --compose-file` 添加 shell 补全。[docker/cli#6690](https://github.com/docker/cli/pull/6690)
- containerd 镜像存储：修复导致 `docker build` 忽略显式设置的 `unpack` 镜像导出器选项的错误。[moby/moby#51514](https://github.com/moby/moby/pull/51514)
- 修复 `docker image ls` 悬空镜像处理。[docker/cli#6704](https://github.com/docker/cli/pull/6704)
- 修复可能导致 Engine 在关闭时将设置了自动移除的容器留在 'dead' 状态且永远不会回收它们的错误。[moby/moby#51693](https://github.com/moby/moby/pull/51693)
- 修复在 i386 上的构建。[moby/moby#51528](https://github.com/moby/moby/pull/51528)
- 修复当存在先前的 graphdriver 状态时，显式 graphdriver 配置（`"storage-driver"`）被当作 containerd 快照器处理的问题。[moby/moby#51516](https://github.com/moby/moby/pull/51516)
- 修复可能创建孤立的 overlay2 层的问题。[moby/moby#51703](https://github.com/moby/moby/pull/51703)

### 网络

---
title: "29.0.0+"
description: "Docker Engine 29.0.0+ 发布说明"
keywords: "发布, Docker, Engine"
---

<em class="text-gray-400 italic dark:text-gray-500">2025-11-12</em>


- 允许在容器网络未配置特定子网时创建具有特定 IP 地址的容器。[moby/moby#51583](https://github.com/moby/moby/pull/51583)
- 修复在升级到 v29.1.2 之前通过 API 创建的容器（使用 `PublishAll` 和 nil 的 `PortBindings` 映射）启动时崩溃的问题。[moby/moby#51691](https://github.com/moby/moby/pull/51691)
- 修复节点加入 Swarm 集群后阻止连接到非 swarm 范围网络的容器进行 DNS 解析的错误。[moby/moby#51515](https://github.com/moby/moby/pull/51515)
- 修复使用远程网络驱动插件时导致守护进程崩溃的问题。[moby/moby#51558](https://github.com/moby/moby/pull/51558)
- 修复在创建具有多个网络连接的容器时可能导致"端点未找到"错误的问题，当其中一个网络是非内部网络但没有自己的外部 IP 连接时。[moby/moby#51538](https://github.com/moby/moby/pull/51538)
- 修复在 IPv6 禁用的主机上阻止无根 Docker 启动的问题。[moby/moby#51543](https://github.com/moby/moby/pull/51543)
- 当容器使用指向容器端口 0 的端口映射创建时返回错误。[moby/moby#51695](https://github.com/moby/moby/pull/51695)

## 29.1.2

<em class="text-gray-400 italic dark:text-gray-500">2025-12-02</em>


有关此版本中的完整拉取请求和变更列表，请参阅相关的 GitHub 里程碑：

- [docker/cli, 29.1.2 里程碑](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A29.1.2)
- [moby/moby, 29.1.2 里程碑](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A29.1.2)

### 安全性

- 更新 Go 运行时到 [1.25.5](https://go.dev/doc/devel/release#go1.25.5)。[moby/moby#51648](https://github.com/moby/moby/pull/51648)，[docker/cli#6688](https://github.com/docker/cli/pull/6688)
  - 修复在格式化主机名验证错误时可能导致通过过度资源使用进行拒绝服务攻击的问题 [**CVE-2025-61729**](https://nvd.nist.gov/vuln/detail/CVE-2025-61729)
  - 修复通配符 SAN 的排除子域约束的错误执行，这可能允许不当信任的证书 [**CVE-2025-61727**](https://nvd.nist.gov/vuln/detail/CVE-2025-22874)

### Bug 修复和增强

- containerd 镜像存储：修复 `docker image inspect` 在本地不可用所有可分发的 blob 时无法返回可用镜像数据的问题。[moby/moby#51629](https://github.com/moby/moby/pull/51629)
- dockerd-rootless-setuptool.sh：修复 `nsenter: no namespace specified`。[moby/moby#51622](https://github.com/moby/moby/pull/51622)
- 修复使用图形驱动程序作为存储时 `docker system df` 显示共享大小和唯一大小为 `N/A` 的问题。[moby/moby#51631](https://github.com/moby/moby/pull/51631)

### 打包更新

- 更新 runc（在静态二进制文件中）到 [v1.3.4](https://github.com/opencontainers/runc/releases/tag/v1.3.4)。[moby/moby#51633](https://github.com/moby/moby/pull/51633)

### 网络

- 修复在使用 slirp4netns 时阻止无根模式下端口映射的错误。[moby/moby#51616](https://github.com/moby/moby/pull/51616)
- 防止在使用 `HostConfig.PublishAllPorts` 设置（`-P`）且没有端口绑定的情况下进行 API 请求时崩溃。[moby/moby#51621](https://github.com/moby/moby/pull/51621)

## 29.1.1

<em class="text-gray-400 italic dark:text-gray-500">2025-11-28</em>


有关此版本中的完整拉取请求和变更列表，请参阅相关的 GitHub 里程碑：

- [docker/cli, 29.1.1 里程碑](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A29.1.1)
- [moby/moby, 29.1.1 里程碑](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A29.1.1)

### 网络

- 回滚破坏所有自定义桥接网络上外部 DNS 解析的 PR。[moby/moby#51615](https://github.com/moby/moby/pull/51615)

## 29.1.0

<em class="text-gray-400 italic dark:text-gray-500">2025-11-27</em>


有关此版本中的完整拉取请求和变更列表，请参阅相关的 GitHub 里程碑：

- [docker/cli, 29.1.0 里程碑](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A29.1.0)
- [moby/moby, 29.1.0 里程碑](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A29.1.0)

### 打包更新

- 更新 BuildKit 到 [v0.26.1](https://github.com/moby/buildkit/releases/tag/v0.26.1)。[moby/moby#51551](https://github.com/moby/moby/pull/51551)
- 更新 containerd 二进制文件到 v2.2.0（静态二进制文件）。[moby/moby#51271](https://github.com/moby/moby/pull/51271)

### 网络

- 不再在容器重启时覆盖用户修改的 `/etc/resolv.conf`。[moby/moby#51507](https://github.com/moby/moby/pull/51507)
- 修复 Windows 容器的 `--publish-all` / `-P`。[moby/moby#51586](https://github.com/moby/moby/pull/51586)
- 修复在容器停止或网络断开期间网关配置失败时阻止容器重启或网络重新连接的问题。[moby/moby#51592](https://github.com/moby/moby/pull/51592)
- Windows 容器：不要在端口映射中显示 IPv6 映射的 IPv4 地址。例如，显示 `0.0.0.0:8080->80/tcp` 而不是 `[::ffff:0.0.0.0]:8080->80/tcp`。[moby/moby#51587](https://github.com/moby/moby/pull/51587)

## 29.0.4

<em class="text-gray-400 italic dark:text-gray-500">2025-11-24</em>


有关此版本中的完整拉取请求和变更列表，请参阅相关的 GitHub 里程碑：

- [docker/cli, 29.0.4 里程碑](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A29.0.4)
- [moby/moby, 29.0.4 里程碑](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A29.0.4)

### Bug 修复和增强

- `docker image ls` 不再截断镜像名称。[docker/cli#6675](https://github.com/docker/cli/pull/6675)

### 网络

- 允许在容器网络未配置特定子网时创建具有特定 IP 地址的容器。[moby/moby#51583](https://github.com/moby/moby/pull/51583)

## 29.0.3

<em class="text-gray-400 italic dark:text-gray-500">2025-11-24</em>


有关此版本中的完整拉取请求和变更列表，请参阅相关的 GitHub 里程碑：

- [docker/cli, 29.0.3 里程碑](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A29.0.3)
- [moby/moby, 29.0.3 里程碑](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A29.0.3)

### Bug 修复和增强

- `docker version --format json`：恢复顶级 `BuildTime` 字段以使用 RFC3339Nano 格式。[docker/cli#6668](https://github.com/docker/cli/pull/6668)
- 修复 `docker image ls` 忽略来自 `docker.json` 的自定义 `imageFormat` 的问题。[docker/cli#6667](https://github.com/docker/cli/pull/6667)

### 网络

- 修复使用远程网络驱动插件时导致守护进程崩溃的问题。[moby/moby#51558](https://github.com/moby/moby/pull/51558)

## 29.0.2

<em class="text-gray-400 italic dark:text-gray-500">2025-11-17</em>


有关此版本中的完整拉取请求和变更列表，请参阅相关的 GitHub 里程碑：

- [docker/cli, 29.0.2 里程碑](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A29.0.2)
- [moby/moby, 29.0.2 里程碑](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A29.0.2)

### 网络

- 修复在创建具有多个网络连接的容器时可能导致"端点未找到"错误的问题，当其中一个网络是非内部网络但没有自己的外部 IP 连接时。[moby/moby#51538](https://github.com/moby/moby/pull/51538)
- 修复在 IPv6 禁用的主机上阻止无根 Docker 启动的问题。[moby/moby#51543](https://github.com/moby/moby/pull/51543)

## 29.0.1

<em class="text-gray-400 italic dark:text-gray-500">2025-11-14</em>


有关此版本中的完整拉取请求和变更列表，请参阅相关的 GitHub 里程碑：

- [docker/cli, 29.0.1 里程碑](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A29.0.1)
- [moby/moby, 29.0.1 里程碑](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A29.0.1)

### Bug 修复和增强

- `docker image ls` 在输出重定向时（例如用于 `grep`）不再截断名称宽度。[docker/cli#6656](https://github.com/docker/cli/pull/6656)
- `docker image ls` 现在考虑 `NO_COLOR` 环境变量来选择是否使用彩色输出。[docker/cli#6654](https://github.com/docker/cli/pull/6654)
- containerd 镜像存储：修复了一个导致 `docker build` 忽略显式设置的 `unpack` 镜像导出器选项的错误。[moby/moby#51514](https://github.com/moby/moby/pull/51514)
- 修复 `docker image ls --all` 无法显示未标记/悬空镜像的错误。[docker/cli#6657](https://github.com/docker/cli/pull/6657)
- 修复在 i386 上的构建问题。[moby/moby#51528](https://github.com/moby/moby/pull/51528)
- 修复当存在先前的图形驱动程序状态时，显式图形驱动程序配置（`"storage-driver"`）被当作 containerd 快照器处理的问题。[moby/moby#51516](https://github.com/moby/moby/pull/51516)
- 修复 `docker version --format=json` 中 `ApiVersion` 和 `MinApiVersion` 字段的输出格式，使其与先前版本对齐。[docker/cli#6648](https://github.com/docker/cli/pull/6648)

### 网络

- 修复了一个错误，该错误阻止了附加到非 Swarm 范围网络的容器在节点加入 Swarm 集群后进行 DNS 解析。[moby/moby#51515](https://github.com/moby/moby/pull/51515)

## 29.0.0

<em class="text-gray-400 italic dark:text-gray-500">2025-11-10</em>


有关此版本中所有拉取请求和更改的完整列表，请参阅相关的 GitHub 里程碑：

- [docker/cli, 29.0.0 里程碑](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A29.0.0)
- [moby/moby, 29.0.0 里程碑](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A29.0.0)

> [!CAUTION]
> 此版本包含多个破坏性变更和弃用。升级前请仔细查看发布说明。

- 现在可以通过将 Docker 守护进程的 `firewall-backend` 选项设置为 `nftables` 来启用对 nftables 的实验性支持。更多信息，请参见 [Docker Engine 文档](https://docs.docker.com/engine/network/firewall-nftables/)。
- containerd 镜像存储现在是**全新安装**的默认选项。这不适用于配置了 `userns-remap` 的守护进程（参见 [moby#47377](https://github.com/moby/moby/issues/47377)）。

### 破坏性变更

- Go 模块 `github.com/docker/docker` 已弃用，推荐使用 `github.com/moby/moby/client` 和 `github.com/moby/moby/api`。`github.com/moby/moby` 模块被视为**内部实现细节** - 唯一受支持的公共模块是 `client` 和 `api`。
  从 v29 开始，发布版本使用 `docker-` 前缀进行标记（例如，`docker-v29.0.0`）。**这仅影响 Go 模块用户和包维护者。**
- 守护进程现在需要 API 版本 `v1.44` 或更高版本（Docker v25.0+）。
- Debian armhf（32 位）包现在针对 ARMv7 CPU，无法在 ARMv6 设备上工作。
- 不再提供官方 Raspbian（32 位）包。对于 64 位设备，请使用 Debian arm64 包，或对于 32 位 ARMv7 设备，请使用 Debian armhf 包。
- **cgroup v1 已弃用。** 支持将持续到至少 2029 年 5 月，但请尽快迁移到 cgroup v2。参见 [moby#51111](https://github.com/moby/moby/issues/51111)。
- Docker Content Trust 已从 Docker CLI 中移除。可以作为单独的插件构建：https://github.com/docker/cli/blob/v29.0.0/cmd/docker-trust/main.go

---

### 新增功能

- `docker image load` 和 `docker image save` 现在通过 `--platform` 标志支持多平台选择（例如，`docker image load --platform linux/amd64,linux/arm64 -i image.tar`）。[docker/cli#6126](https://github.com/docker/cli/pull/6126)
- `docker image ls` 现在默认使用新视图（类似于 `--tree` 但已折叠）。[docker/cli#6566](https://github.com/docker/cli/pull/6566)
- `docker run --runtime <...>` 现在在 Windows 上受支持。[moby/moby#50546](https://github.com/moby/moby/pull/50546)
- `GET /containers/json` 现在包含一个描述容器健康检查状态的 `Health` 字段。[moby/moby#50281](https://github.com/moby/moby/pull/50281)
- 向构建器配置添加 `device` 权限。[moby/moby#50386](https://github.com/moby/moby/pull/50386)
- 为 `docker service create` 和 `docker service update` 命令添加对 `memory-swap` 和 `memory-swappiness` 标志的支持。[docker/cli#6619](https://github.com/docker/cli/pull/6619)
- 允许 Docker CLI 在 Docker 上下文元数据中存在键值对（`"GODEBUG":"..."`）时设置 `GODEBUG` 环境变量。[docker/cli#6371](https://github.com/docker/cli/pull/6371)

### 错误修复和增强

- `docker image ls --tree` 现在按名称字母顺序而不是创建日期对镜像进行排序。[docker/cli#6595](https://github.com/docker/cli/pull/6595)
- `docker image ls` 在未提供 `--all` 标志时不再默认显示未标记的镜像。[docker/cli#6574](https://github.com/docker/cli/pull/6574)
- `docker save`：修复了使用 overlay2 存储驱动程序导出镜像时 tar 成员时间戳不一致的问题。[moby/moby#51365](https://github.com/moby/moby/pull/51365)
- 为 fluentd 日志驱动程序添加了一个新的日志选项（`fluentd-read-timeout`），该选项允许指定从 fluentd 连接读取确认的超时时间。[moby/moby#50249](https://github.com/moby/moby/pull/50249)
- 为 `docker images` 添加镜像名称自动补全功能。[docker/cli#6452](https://github.com/docker/cli/pull/6452)
- 当设置了 `--type` 时，为 `docker inspect` 添加 shell 自动补全功能。[docker/cli#6444](https://github.com/docker/cli/pull/6444)
- 为 `docker plugin` 子命令添加 shell 自动补全功能。[docker/cli#6445](https://github.com/docker/cli/pull/6445)
- api/types/container：使 ContainerState、HealthStatus 成为具体类型。[moby/moby#51439](https://github.com/moby/moby/pull/51439)
- 当启用用户命名空间重新映射时，containerd 镜像存储暂时不可用，这是针对 [moby#47377](https://github.com/moby/moby/issues/47377) 的临时解决方案。[moby/moby#51042](https://github.com/moby/moby/pull/51042)
- contrib：移除 contrib/httpserver，该组件仅用于集成测试。[moby/moby#50654](https://github.com/moby/moby/pull/50654)
- daemon：改进 `--dns` 选项和 `daemon.json` 中相应 `"dns"` 字段的验证。[moby/moby#50600](https://github.com/moby/moby/pull/50600)
- dockerd-rootless.sh：如果未安装 slirp4netns，尝试使用 pasta (passt)。[moby/moby#51149](https://github.com/moby/moby/pull/51149)
- 修复 `--mount type=image` 在将同一镜像多次挂载到不同目标位置时的失败问题。[moby/moby#50268](https://github.com/moby/moby/pull/50268)
- 修复 `docker stats <container>` 无法正常退出的问题。[docker/cli#6582](https://github.com/docker/cli/pull/6582)
- 修复 API 服务器在有到 `/events` 端点的开放连接时无法快速关闭的错误。[moby/moby#51448](https://github.com/moby/moby/pull/51448)
- 修复在"一次性"模式下收集容器统计信息时不会包含容器 ID 和名称的错误。[moby/moby#51302](https://github.com/moby/moby/pull/51302)
- 修复在使用放置偏好扩展服务后，Swarm 中的所有新任务可能永远卡在 PENDING 状态的问题。[moby/moby#50202](https://github.com/moby/moby/pull/50202)
- 修复使用 containerd 镜像存储时自定义元头没有传递的问题。[moby/moby#51024](https://github.com/moby/moby/pull/51024)
- 修复以 `--log-level=trace` 运行守护进程时请求未被记录的问题。[moby/moby#50986](https://github.com/moby/moby/pull/50986)
- 修复 firewalld 重新加载后 Swarm 服务无法从发布端口访问的问题。[moby/moby#50443](https://github.com/moby/moby/pull/50443)
- 改进连接 API 失败时的错误，为用户提供更多上下文。[moby/moby#50285](https://github.com/moby/moby/pull/50285)
- 改进 `docker secret` 和 `docker config` 子命令的 shell 自动补全功能。[docker/cli#6446](https://github.com/docker/cli/pull/6446)
- 当使用 `docker run --gpus` 选择设备驱动程序时，优先使用显式的设备驱动程序名称而不是 GPU 功能。[moby/moby#50717](https://github.com/moby/moby/pull/50717)
- 更新 runc 至 [v1.3.3](https://github.com/opencontainers/runc/releases/tag/v1.3.3)。[moby/moby#51393](https://github.com/moby/moby/pull/51393)
- 更新 SwarmKit 内部 TLS 配置以排除已知的不安全密码套件。[moby/moby#51139](https://github.com/moby/moby/pull/51139)
- Windows：修复 BuildKit 创建的容器隔离模式与守护进程配置不一致的问题。[moby/moby#50942](https://github.com/moby/moby/pull/50942)

### 打包更新

- client：从客户端配置中移除遗留的 CBC 密码套件。[moby/moby#50126](https://github.com/moby/moby/pull/50126)
- contrib：移除 `editorconfig`，因为它已不再维护。[moby/moby#50607](https://github.com/moby/moby/pull/50607)
- contrib：移除 `nano` 和 TextMate (`tmbundle`) 的 Dockerfile 语法高亮文件，因为它们已不再维护且过时。[moby/moby#50606](https://github.com/moby/moby/pull/50606)
- contrib：移除 mkimage-xxx 脚本，因为它们已不再维护且未经过测试。[moby/moby#50297](https://github.com/moby/moby/pull/50297)
- 如果 Docker 降级到不支持此功能的版本，网络将变得不可用，必须删除并重新创建。[moby/moby#50114](https://github.com/moby/moby/pull/50114)
- Windows overlay 网络驱动程序现在支持 `--dns` 选项。[moby/moby#51229](https://github.com/moby/moby/pull/51229)
- 更新 BuildKit 至 [v0.25.2](https://github.com/moby/buildkit/releases/tag/v0.25.2)。[moby/moby#51397](https://github.com/moby/moby/pull/51397)
- 更新 containerd 至 [v2.1.5](https://github.com/containerd/containerd/releases/tag/v2.1.5)。[moby/moby#51409](https://github.com/moby/moby/pull/51409)

  containerd v2.1.5 现在使用 systemd 的默认 `LimitNOFILE` 用于容器，
  将打开的文件描述符限制（`ulimit -n`）从 `1048576` 改为
  `1024`。这扩展了 Docker Engine v25.0 中为构建容器引入的更改，
  现在适用于所有容器。

  这防止了基于 ulimit 调整行为的程序在限制设置为 `infinity` 时消耗
  过多内存。容器现在的行为与在主机上运行的程序相同。

  如果您的工作负载需要更高的限制，请使用 `docker run` 的 `--ulimit`，
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

  有关更多信息，请参见 [moby#51485](https://github.com/moby/moby/issues/51485)。
- 更新 Go 运行时至 [1.25.4](https://go.dev/doc/devel/release#go1.25.4)。[moby/moby#51418](https://github.com/moby/moby/pull/51418)，[docker/cli#6632](https://github.com/docker/cli/pull/6632)
- 用户可以通过使用未指定地址来请求从默认池分配的网络的特定前缀大小，例如 `--subnet 0.0.0.0/24 --subnet ::/96`。[moby/moby#50114](https://github.com/moby/moby/pull/50114)

### 网络

- 添加守护进程选项 `--bridge-accept-fwmark`。带有此防火墙标记的数据包将被桥接网络接受，覆盖 Docker 的 iptables 或 nftables "drop" 规则。[moby/moby#50476](https://github.com/moby/moby/pull/50476)
- api/types/system: 为类型特定字段弃用顶级 `DiskUsage` 字段。[moby/moby#51235](https://github.com/moby/moby/pull/51235)
- 确保在桥接网络创建失败时移除桥接设备。[moby/moby#51147](https://github.com/moby/moby/pull/51147)
- 确保 Engine 重启时，Windows NAT 网络使用其原始标签重新创建。[moby/moby#50447](https://github.com/moby/moby/pull/50447)
- 使用传统链接在容器上设置的环境变量已被弃用，不再自动添加。[moby/moby#50719](https://github.com/moby/moby/pull/50719)
  - 守护进程可以使用 `DOCKER_KEEP_DEPRECATED_LEGACY_LINKS_ENV_VARS=1` 启动以恢复它们
  - 鼓励用户停止依赖这些功能，因为它们已被弃用，逃生机制将在后续版本中移除
- 修复 NetworkDB 中的一个错误，该错误有时会导致某些节点上的条目卡在删除状态，导致覆盖网络上容器之间的连接问题。[moby/moby#50342](https://github.com/moby/moby/pull/50342)
- 修复一个错误，该错误可能导致 Engine 和另一个主机进程绑定相同的 UDP 端口。[moby/moby#50669](https://github.com/moby/moby/pull/50669)
- 修复一个死锁问题，如果在桥接网络驱动程序启动、创建或删除网络或创建端口映射时处理 firewalld 重载，可能会发生此问题。[moby/moby#50620](https://github.com/moby/moby/pull/50620)
- 修复在特定接口上仅禁用 IPv6 时阻止容器启动或选择其网络网关的问题。[moby/moby#48971](https://github.com/moby/moby/pull/48971)
- 对于 Linux，`docker info` 现在报告防火墙后端（如果可用）。[docker/cli#6191](https://github.com/docker/cli/pull/6191)
- 大幅提高覆盖网络和 Swarm 路由网格的可靠性。[moby/moby#50393](https://github.com/moby/moby/pull/50393)
- 改进 NetworkDB 的收敛速度，NetworkDB 是覆盖网络管理平面的一部分，在突发更新后。[moby/moby#50193](https://github.com/moby/moby/pull/50193)
- 提高覆盖网络驱动程序的可靠性。[moby/moby#50260](https://github.com/moby/moby/pull/50260)
- 改进容器连接到网络的错误处理。[moby/moby#50945](https://github.com/moby/moby/pull/50945)
- macvlan 和 IPvlan-l2 网络：除非在 IPAM 配置中明确包含 `--gateway`，否则不会配置默认网关。这解决了在启用了 IPv6 自动配置的网络中可能导致容器启动失败的问题。[moby/moby#50929](https://github.com/moby/moby/pull/50929)
- nftables: Docker 不会在主机上启用 IP 转发。如果桥接网络需要转发但未启用，守护进程启动或网络创建将失败并显示错误。您必须启用转发并确保防火墙规则到位以防止非 Docker 接口之间的不必要转发。或者，使用守护进程选项 `--ip-forward=false` 禁用检查，但某些桥接网络功能（包括端口转发）可能无法工作。有关从 iptables 迁移到 nftables 的更多信息，请参见 [Engine Docs](https://docs.docker.com/engine/network/firewall-nftables)。[moby/moby#50646](https://github.com/moby/moby/pull/50646)
- 在守护进程启动时，先重启共享其网络栈的容器，然后再重启需要这些栈的容器。[moby/moby#50327](https://github.com/moby/moby/pull/50327)
- 发布的端口现在在网关模式为 "routed" 的网络中始终可访问。以前，只有当路由模式网络被选为容器的默认网关时，才会添加打开这些端口的规则。[moby/moby#50140](https://github.com/moby/moby/pull/50140)
- 自 28.0.0 起，只有在设置了环境变量 `DOCKER_IPTABLES_SCTP_CHECKSUM=1` 时才会添加用于校验 SCTP 的 `iptables` mangle 规则。该规则现在已被移除，环境变量现在没有效果。[moby/moby#50539](https://github.com/moby/moby/pull/50539)
- 桥接网络的 iptables 规则已更新，包括移除 `DOCKER-ISOLATION-STAGE-1` 和 `DOCKER-ISOLATION-STAGE-2` 链。通过这些更改：[moby/moby#49981](https://github.com/moby/moby/pull/49981)
  - 当用户空间代理未运行时，容器现在可以访问发布到主机地址的端口
  - 容器现在可以访问具有 "nat-unprotected" 网关模式的其他网络上的容器地址端口
- 当动态链接时，Docker 守护进程现在依赖于 libnftables。[moby/moby#51033](https://github.com/moby/moby/pull/51033)
- Windows: `network inspect`: HNS 网络名称现在在选项 `com.docker.network.windowsshim.networkname` 中报告，而不是 Docker 网络名称，Docker 网络名称仅在守护进程重启后报告。[moby/moby#50961](https://github.com/moby/moby/pull/50961)
- Windows: 在守护进程重启时恢复网络时，保留它们与非默认 IPAM 驱动程序的关联。[moby/moby#50649](https://github.com/moby/moby/pull/50649)

### API

- `events` API 现在为换行符分隔的 JSON 事件流报告内容类型为 `application/x-ndjson`。[moby/moby#50953](https://github.com/moby/moby/pull/50953)
- `GET /images/{name}/get` 和 `POST /images/load` 现在接受多个 `platform` 查询参数，允许导出和加载多个平台的镜像。[moby/moby#50166](https://github.com/moby/moby/pull/50166)
- `GET /images/{name}/json` 现在在值为空时省略以下字段：`Parent`、`Comment`、`DockerVersion`、`Author`。[moby/moby#51072](https://github.com/moby/moby/pull/51072)
- `GET /images/{name}/json`：在未设置时省略空的 `Config` 字段。[moby/moby#50915](https://github.com/moby/moby/pull/50915)
- `POST /images/{name:}/push`：移除对 API v1.4 身份验证配置在请求体中的兼容性。[moby/moby#50371](https://github.com/moby/moby/pull/50371)
- 添加对 Swarm 服务中内存交换比的支持。[moby/moby#51114](https://github.com/moby/moby/pull/51114)
  - `GET /services` 现在在 `Resource` 要求中返回 `SwapBytes` 和 `MemorySwappiness` 字段
  - `GET /services/{id}` 现在在 `Resource` 要求中返回 `SwapBytes` 和 `MemorySwappiness` 字段
  - `POST /services/create` 现在在 `Resource` 要求中接受 `SwapBytes` 和 `MemorySwappiness` 字段
  - `POST /services/{id}/update` 现在在 `Resource` 要求中接受 `SwapBytes` 和 `MemorySwappiness` 字段
  - `GET /tasks` 现在在 `Resource` 要求中返回 `SwapBytes` 和 `MemorySwappiness` 字段
  - `GET /tasks/{id}` 现在在 `Resource` 要求中返回 `SwapBytes` 和 `MemorySwappiness` 字段
- api/types/build：将 `CachePruneOptions` 类型移动到 `client.BuildCachePruneOptions`。[moby/moby#50772](https://github.com/moby/moby/pull/50772)
- api/types/checkpoint：将检查点选项移动到客户端模块。[moby/moby#50905](https://github.com/moby/moby/pull/50905)
- api/types/container：如果 `OnBuild` 的值为空或零，则现在会被省略。[moby/moby#51154](https://github.com/moby/moby/pull/51154)
- api/types/container：使容器配置 `MacAddress` 在 v1.52 及更高版本中过时。请改用网络端点设置。[moby/moby#51189](https://github.com/moby/moby/pull/51189)
- api/types/container：将 `ResizeOptions` 类型移动到客户端中的 `ContainerResizeOptions`。[moby/moby#50773](https://github.com/moby/moby/pull/50773)
- api/types/events：将 `ListOptions` 类型移动到客户端 `EventsListOptions`。[moby/moby#50774](https://github.com/moby/moby/pull/50774)
- api/types/image：将镜像选项移出到客户端。[moby/moby#50776](https://github.com/moby/moby/pull/50776)
- api/types/network：将 `CreateOptions`、`ConnectOptions` 和 `DisconnectOptions` 移动到客户端模块。[moby/moby#50817](https://github.com/moby/moby/pull/50817)
- api/types/network：将 `ListOptions` 和 `InspectOptions` 类型移动到客户端。[moby/moby#50786](https://github.com/moby/moby/pull/50786)
- api/types/plugin：将 `ListResponse` 改为非指针切片。[moby/moby#51440](https://github.com/moby/moby/pull/51440)
- api/types/plugin：移除已弃用的 `Config.DockerVersion`。[moby/moby#51458](https://github.com/moby/moby/pull/51458)
- api/types/registry：将 `SearchOptions` 移动到客户端中的 `ImageSearchOptions`。[moby/moby#50787](https://github.com/moby/moby/pull/50787)
- api/types/registry：将 `ServiceConfig` 遗留字段序列化支持移到守护进程后端。[moby/moby#50826](https://github.com/moby/moby/pull/50826)
- api/types/registry：将编码/解码身份验证配置函数移到引用工具包。[moby/moby#50785](https://github.com/moby/moby/pull/50785)
- api/types/storage：添加 `Storage` 类型并集成到容器检查中。[moby/moby#50857](https://github.com/moby/moby/pull/50857)
- api/types/swarm：弃用并停止支持 `PortConfigProtocol`；请改用 `network.IPProtocol`。[moby/moby#51094](https://github.com/moby/moby/pull/51094)
- api/types/swarm：将选项类型移动到客户端模块。[moby/moby#50794](https://github.com/moby/moby/pull/50794)
- api/types/swarm：将 `SecretListOptions` 类型移动到客户端模块。[moby/moby#50816](https://github.com/moby/moby/pull/50816)
- api/types/system：将 `DiskUsageOptions` 移动到客户端。[moby/moby#50788](https://github.com/moby/moby/pull/50788)
- api/types/system：将 `SecurityOpt` 和 `DecodeSecurityOptions` 移动到客户端模块。[moby/moby#50825](https://github.com/moby/moby/pull/50825)
- api/types/volume：将 ListResponse.Volumes 改为非指针切片。[moby/moby#51454](https://github.com/moby/moby/pull/51454)
- api/types/volume：将 `ListOptions` 类型移动到客户端模块。[moby/moby#50789](https://github.com/moby/moby/pull/50789)
- api/types/volume：将 `UpdateOptions` 移动到客户端模块。[moby/moby#51205](https://github.com/moby/moby/pull/51205)
- api/types: daemon：将磁盘使用情况结构移动到后端服务器。[moby/moby#50764](https://github.com/moby/moby/pull/50764)
- api：使 `image.InspectResponse` 中的 `GraphDriver` 字段变为可选。在使用旧版图形驱动程序时将继续发出此字段，而在使用 containerd 镜像后端时将省略此字段。[moby/moby#50893](https://github.com/moby/moby/pull/50893)
- api：重新定义容器网络端口类型。[moby/moby#50710](https://github.com/moby/moby/pull/50710)
- client: PluginListResult：将 Items 字段更改为非指针切片。[moby/moby#51440](https://github.com/moby/moby/pull/51440)
- 使用 API v1.52 及更新版本检查网络时，提供分配给网络的子网的 IPAM 分配统计信息。[moby/moby#50917](https://github.com/moby/moby/pull/50917)
- MAC 地址字段表示为与标准库 net.HardwareAddr 类型兼容的字节切片，而不是字符串。[moby/moby#51355](https://github.com/moby/moby/pull/51355)
- 为 `NetworkSummary` 和 `NetworkInspect` 添加的 Swagger 定义已添加到描述 Engine API 的 Swagger 规范中。[moby/moby#50855](https://github.com/moby/moby/pull/50855)
- 将 API 版本更新为 1.52。[moby/moby#50418](https://github.com/moby/moby/pull/50418)

### Go SDK

- `api/pkg/progress` 和 `api/pkg/streamformatter` 已被移除。[moby/moby#51153](https://github.com/moby/moby/pull/51153)
- `api/types/registry`: `EncodeAuthConfig`: 零值时使用空字符串。[moby/moby#50426](https://github.com/moby/moby/pull/50426)
- `api/types/versions` 已移至客户端和守护进程。[moby/moby#51284](https://github.com/moby/moby/pull/51284)
- `client.ConfigCreate`、`client.ConfigList`、`client.ConfigInspectWithRaw`、`client.ConfigUpdate` 和 `client.ConfigRemove` 方法现在接受选项结构体而不是位置参数，并返回专用的结果结构体。[moby/moby#51078](https://github.com/moby/moby/pull/51078)
- `client.ImageBuild`、`client.BuildCancel`、`client.ImageList`、`client.ImageRemove`、`client.ImageTag` 和 `client.ImageSearch` 方法现在接受选项结构体而不是位置参数，并返回专用的结果结构体。[moby/moby#51227](https://github.com/moby/moby/pull/51227)
- `client`: `ContainerExec...` 方法已重命名为 `Exec...`。[moby/moby#51262](https://github.com/moby/moby/pull/51262)
- `client`: 将 `ImageInspect`、`ImageHistory`、`ImageLoad` 和 `ImageSave` 的返回值包装在结构体中。[moby/moby#51236](https://github.com/moby/moby/pull/51236)
- `ImagePull` 现在返回一个对象，该对象具有 `JSONMessages` 方法，返回消息对象的迭代器。[moby/moby#50935](https://github.com/moby/moby/pull/50935)
- `ImagePush` 现在返回一个对象，该对象具有 `JSONMessages` 方法，返回消息对象的迭代器。[moby/moby#51148](https://github.com/moby/moby/pull/51148)
- api/types/container: 将 `StatsResponseReader` 移至 `client` 包。[moby/moby#50521](https://github.com/moby/moby/pull/50521)
- api/types/container: 将容器选项移至客户端。[moby/moby#50897](https://github.com/moby/moby/pull/50897)
- api/types/container: 将 `Port` 重命名为 `PortSummary`。[moby/moby#50711](https://github.com/moby/moby/pull/50711)
- api/types/container: StatsResponse: 添加 `OSType` 字段。[moby/moby#51305](https://github.com/moby/moby/pull/51305)
- api/types: 将 `ErrorResponse` 移至 `common/ErrorResponse`。[moby/moby#50632](https://github.com/moby/moby/pull/50632)
- api: 移除未使用的 `DefaultVersion`、`MinSupportedAPIVersion` 常量。[moby/moby#50587](https://github.com/moby/moby/pull/50587)
- cli/command: 添加 `WithUserAgent` 选项。[docker/cli#4574](https://github.com/docker/cli/pull/4574)
- client: `ContainerCommitOptions`: 移除 `Pause` 字段，改用 `NoPause`。[moby/moby#51019](https://github.com/moby/moby/pull/51019)
- client: 添加 `DefaultAPIVersion` 常量，该常量定义了客户端支持的默认（和最大）API 版本。[moby/moby#50433](https://github.com/moby/moby/pull/50433)
- client: 添加 `ExecAPIClient` 接口，用于客户端提供的 exec 方法。[moby/moby#50997](https://github.com/moby/moby/pull/50997)
- client: Client.PluginList: 添加选项结构体。[moby/moby#51207](https://github.com/moby/moby/pull/51207)
- client: ContainersPrune: 重写为使用选项结构体和结果。[moby/moby#51200](https://github.com/moby/moby/pull/51200)
- client: ImagesPrune: 重写为使用选项结构体和结果。[moby/moby#51200](https://github.com/moby/moby/pull/51200)
- client: NetworksPrune: 重写为使用选项结构体和结果。[moby/moby#51200](https://github.com/moby/moby/pull/51200)
- client: 移除 `client.ContainerStatsResult.OSType` 字段。[moby/moby#51305](https://github.com/moby/moby/pull/51305)
- client: VolumesPrune: 重写为使用选项结构体和结果。[moby/moby#51200](https://github.com/moby/moby/pull/51200)
- daemon/config: 添加 `DefaultAPIVersion` 常量，该常量定义了守护进程支持的默认（和最大）API 版本。[moby/moby#50436](https://github.com/moby/moby/pull/50436)
- 修复 `ContainerExecStart`、`ContainerList` 和 `Events` 中的数据竞争。[moby/moby#50448](https://github.com/moby/moby/pull/50448)
- IP 地址和子网现在分别为 `netip.Addr` 和 `netip.Prefix` 类型。[moby/moby#50956](https://github.com/moby/moby/pull/50956)
- 移除 `NetworkSettingsBase` 和 `DefaultNetworkSettings` 结构体。`NetworkSettingsBase` 中未被弃用的字段现在直接位于 `NetworkSettings` 中。[moby/moby#50846](https://github.com/moby/moby/pull/50846)
- 客户端现在使用其自己的 `client.Filters` 类型来过滤 API 请求，具有更符合人体工程学的接口。使用 `github.com/docker/docker/api/types/filters` 包的用户在升级到 v29 客户端时需要重构。[moby/moby#51115](https://github.com/moby/moby/pull/51115)
- 类型 `"github.com/moby/moby/api/types/network".Summary` 和 `"github.com/moby/moby/api/types/network".Inspect` 不再是别名，它们的大多数字段已移至嵌入结构体中。在迁移到新的 github.com/moby/moby/api 模块时，Engine API 客户端可能需要一些源代码级别的更改。[moby/moby#50878](https://github.com/moby/moby/pull/50878)
- 将最低 Go 版本更新为 1.24。[docker/cli#6624](https://github.com/docker/cli/pull/6624)

### 弃用

- `client/pkg/jsonmessage`：移除已弃用的 `ProgressMessage`、`ErrorMessage`、`DisplayJSONMessagesToStream` 和 `Stream` 接口。[moby/moby#49264](https://github.com/moby/moby/pull/49264)
- `GET /events` 不再包含已弃用的 `status`、`id` 和 `from` 字段。这些字段在 API v1.22 中已被移除，但仍包含在响应中。使用 API v1.52 或更高版本时，这些字段现在将被省略。[moby/moby#50832](https://github.com/moby/moby/pull/50832)
- api/types/network: CreateRequest：移除已弃用的 CheckDuplicate 字段。[moby/moby#50998](https://github.com/moby/moby/pull/50998)
- api/types/plugin：弃用 `Config.DockerVersion` 字段。[moby/moby#51109](https://github.com/moby/moby/pull/51109)
- api/types/registry：移除已弃用的 AuthConfig.Email 字段。[moby/moby#51059](https://github.com/moby/moby/pull/51059)
- api/types/strslice：弃用 StrSlice，建议使用常规的 `[]string`。[moby/moby#50292](https://github.com/moby/moby/pull/50292)
- api/types/sytem：移除已弃用的 `DiskUsage.BuilderSize`。[moby/moby#51180](https://github.com/moby/moby/pull/51180)
- api/types：将插件类型移至 api/types/plugin。[moby/moby#48114](https://github.com/moby/moby/pull/48114)
- API：弃用：当启动容器时，Engine 会自动用带有空 HostIP 和 HostPort 的 PortBinding 来填充空的 `PortBindings` 列表。此行为在 API 1.52 中已弃用，并将在 API 1.53 中移除。[moby/moby#50874](https://github.com/moby/moby/pull/50874)
- build：移除经典构建器的 DCT 支持。[docker/cli#6195](https://github.com/docker/cli/pull/6195)
- cli/command：移除已弃用的 `ResolveDefaultContext`。[docker/cli#6555](https://github.com/docker/cli/pull/6555)
- client：ImageBuildResponse：移除 OSType 字段。[moby/moby#50995](https://github.com/moby/moby/pull/50995)
- client：移除 `ImageCreate` 方法 - 请使用 `ImagePull` 或 `ImageImport` 代替。[moby/moby#51366](https://github.com/moby/moby/pull/51366)
- client：移除已弃用的 `ImageListOptions.ContainerCount`。[moby/moby#51006](https://github.com/moby/moby/pull/51006)
- client：移除对协商 API 版本 < v1.44 (docker 25.0) 的支持。[moby/moby#51119](https://github.com/moby/moby/pull/51119)
- client：移除未使用的 `Client.HTTPClient()` 方法。[moby/moby#51011](https://github.com/moby/moby/pull/51011)
- daemon/graphdriver：移除已弃用的 `GetDriver()`。[moby/moby#50377](https://github.com/moby/moby/pull/50377)
- daemon：将最低 API 版本提升至 v1.44。[moby/moby#51186](https://github.com/moby/moby/pull/51186)
- 弃用 `docker commit` 中的 `--pause` 标志，推荐使用 `--no-pause`。[docker/cli#6460](https://github.com/docker/cli/pull/6460)
- 弃用 cgroup v1。[moby/moby#51360](https://github.com/moby/moby/pull/51360), [docker/cli#6598](https://github.com/docker/cli/pull/6598)
- Go SDK：`cli-plugins/manager`：弃用元数据别名，推荐使用 `cli-plugins/manager/metadata` 中的等效项。[docker/cli#6237](https://github.com/docker/cli/pull/6237)
- Go SDK：`cli-plugins/manager`：移除 `Candidate` 接口，该接口仅用于内部使用。[docker/cli#6237](https://github.com/docker/cli/pull/6237)
- Go SDK：`cli-plugins/manager`：移除 `NewPluginError` 函数，该函数仅用于内部使用。[docker/cli#6237](https://github.com/docker/cli/pull/6237)
- Go SDK：`cli-plugins/manager`：移除已弃用的 `ResourceAttributesEnvvar` 常量。[docker/cli#6237](https://github.com/docker/cli/pull/6237)
- Go SDK：`cli/command`：移除 `ErrPromptTerminated`、`DisableInputEcho`、`PromptForInput` 和 `PromptForConfirmation` 工具。这些工具仅供内部使用，不再使用。[docker/cli#6243](https://github.com/docker/cli/pull/6243)
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
- Go SDK：api：弃用 `NoBaseImageSpecifier` 常量。此常量不再使用，将在下次发布中移除。[moby/moby#50437](https://github.com/moby/moby/pull/50437)
- Go SDK：api：移除 `NoBaseImageSpecifier`。[moby/moby#50574](https://github.com/moby/moby/pull/50574)
- Go SDK：cli/command/builder：移除 `CachePrune()`，该函数不再使用。[docker/cli#6236](https://github.com/docker/cli/pull/6236)
- Go SDK：cli/command/builder：移除 `NewBuilderCommand` 和 `NewBakeStubCommand`。[docker/cli#6335](https://github.com/docker/cli/pull/6335)
- Go SDK：cli/command/checkpoint：移除 `NewCheckpointCommand`。[docker/cli#6335](https://github.com/docker/cli/pull/6335)
- Go SDK：cli/command/checkpoint：移除已弃用的 `NewFormat`、`FormatWrite`。[docker/cli#6339](https://github.com/docker/cli/pull/6339)
- Go SDK：cli/command/completion：移除已弃用的 `NoComplete`。[docker/cli#6408](https://github.com/docker/cli/pull/6408)
- Go SDK：cli/command/config：移除 `NewConfigCommand`。[docker/cli#6335](https://github.com/docker/cli/pull/6335)
- Go SDK：cli/command/config：移除已弃用的 `NewFormat`、`FormatWrite`、`InspectFormatWrite`。[docker/cli#6339](https://github.com/docker/cli/pull/6339)
- Go SDK：cli/command/config：移除已弃用的 `RunConfigCreate`、`CreateOptions`、`RunConfigInspect`、`InspectOptions`、`RunConfigList`、`ListOptions`、`RunConfigRemove` 和 `RemoveOptions`。[docker/cli#6370](https://github.com/docker/cli/pull/6370)
- Go SDK：cli/command/container：弃用 `NewDiffFormat`、`DiffFormatWrite`。这些函数仅在内部使用，将在下次发布中移除。[docker/cli#6187](https://github.com/docker/cli/pull/6187)
- Go SDK：cli/command/container：移除 `NewBuildCommand`、`NewPullCommand`、`NewPushCommand`、`NewImagesCommand`、`NewImageCommand`、`NewHistoryCommand`、`NewImportCommand`、`NewLoadCommand`、`NewRemoveCommand`、`NewSaveCommand`、`NewTagCommand`、`NewPruneCommand`。[docker/cli#6335](https://github.com/docker/cli/pull/6335)
- Go SDK：cli/command/container：移除 `NewRunCommand`、`NewExecCommand`、`NewPsCommand`、`NewContainerCommand`、`NewAttachCommand`、`NewCommitCommand`、`NewCopyCommand`、`NewCreateCommand`、`NewDiffCommand`、`NewExportCommand`、`NewKillCommand`、`NewLogsCommand`、`NewPauseCommand`、`NewPortCommand`、`NewRenameCommand`、`NewRestartCommand`、`NewRmCommand`、`NewStartCommand`、`NewStatsCommand`、`NewStopCommand`、`NewTopCommand`、`NewUnpauseCommand`、`NewUpdateCommand`、`NewWaitCommand`、`NewPruneCommand`。[docker/cli#6335](https://github.com/docker/cli/pull/6335)

- Go SDK: cli/command/container: 移除不再使用的 `RunPrune()`。[docker/cli#6236](https://github.com/docker/cli/pull/6236)
- Go SDK: cli/command/container: 移除已弃用的 `NewDiffFormat`、`DiffFormatWrite`。[docker/cli#6339](https://github.com/docker/cli/pull/6339)
- Go SDK: cli/command/context: 移除 `NewContextCommand`。[docker/cli#6335](https://github.com/docker/cli/pull/6335)
- Go SDK: cli/command/context: 移除已弃用的 `RunCreate` 和 `CreateOptions`。[docker/cli#6407](https://github.com/docker/cli/pull/6407)
- Go SDK: cli/command/context: 移除已弃用的 `RunExport` 和 `ExportOptions`。[docker/cli#6407](https://github.com/docker/cli/pull/6407)
- Go SDK: cli/command/context: 移除已弃用的 `RunImport`。[docker/cli#6407](https://github.com/docker/cli/pull/6407)
- Go SDK: cli/command/context: 移除已弃用的 `RunRemove` 和 `RemoveOptions`。[docker/cli#6407](https://github.com/docker/cli/pull/6407)
- Go SDK: cli/command/context: 移除已弃用的 `RunUpdate` 和 `UpdateOptions`。[docker/cli#6407](https://github.com/docker/cli/pull/6407)
- Go SDK: cli/command/context: 移除已弃用的 `RunUse`。[docker/cli#6407](https://github.com/docker/cli/pull/6407)
- Go SDK: cli/command/formatter/swarm: 移除已弃用的 `GetStacks` 函数。[docker/cli#6406](https://github.com/docker/cli/pull/6406)
- Go SDK: cli/command/image/build: 弃用 `DefaultDockerfileName`、`DetectArchiveReader`、`WriteTempDockerfile`、`ResolveAndValidateContextPath`。这些工具仅在内部使用，将在下一个版本中移除。[docker/cli#6561](https://github.com/docker/cli/pull/6561)
- Go SDK: cli/command/image: 移除不再使用的 `RunPrune()`。[docker/cli#6236](https://github.com/docker/cli/pull/6236)
- Go SDK: cli/command/image: 移除已弃用的 `AuthResolver` 工具。[docker/cli#6373](https://github.com/docker/cli/pull/6373)
- Go SDK: cli/command/image: 移除已弃用的 `NewHistoryFormat`、`HistoryWrite`。[docker/cli#6339](https://github.com/docker/cli/pull/6339), [docker/cli#6339](https://github.com/docker/cli/pull/6339)
- Go SDK: cli/command/manifest: 移除 `NewManifestCommand`。[docker/cli#6335](https://github.com/docker/cli/pull/6335)
- Go SDK: cli/command/network: 移除 `NewNetworkCommand`。[docker/cli#6335](https://github.com/docker/cli/pull/6335)
- Go SDK: cli/command/network: 移除不再使用的 `RunPrune()`。[docker/cli#6236](https://github.com/docker/cli/pull/6236)
- Go SDK: cli/command/network: 移除已弃用的 `NewFormat`、`FormatWrite`。[docker/cli#6339](https://github.com/docker/cli/pull/6339)
- Go SDK: cli/command/node: 移除 `NewNodeCommand`。[docker/cli#6335](https://github.com/docker/cli/pull/6335)
- Go SDK: cli/command/node: 移除已弃用的 `NewFormat`、`FormatWrite`、`InspectFormatWrite`。[docker/cli#6339](https://github.com/docker/cli/pull/6339)
- Go SDK: cli/command/plugin: 移除 `NewPluginCommand`。[docker/cli#6335](https://github.com/docker/cli/pull/6335)
- Go SDK: cli/command/plugin: 移除已弃用的 `NewFormat`、`FormatWrite`。[docker/cli#6339](https://github.com/docker/cli/pull/6339)
- Go SDK: cli/command/registry: 移除 `NewLoginCommand`、`NewLogoutCommand`、`NewSearchCommand`。[docker/cli#6335](https://github.com/docker/cli/pull/6335)
- Go SDK: cli/command/registry: 移除已弃用的 `NewSearchFormat`、`SearchWrite`。[docker/cli#6339](https://github.com/docker/cli/pull/6339)
- Go SDK: cli/command/registry: 移除已弃用的 `OauthLoginEscapeHatchEnvVar` 常量。[docker/cli#6463](https://github.com/docker/cli/pull/6463)
- Go SDK: cli/command/secret: 移除 `NewSecretCommand`。[docker/cli#6335](https://github.com/docker/cli/pull/6335)
- Go SDK: cli/command/secret: 移除已弃用的 `NewFormat`、`FormatWrite`、`InspectFormatWrite`。[docker/cli#6339](https://github.com/docker/cli/pull/6339)
- Go SDK: cli/command/service: 移除 `NewServiceCommand`。[docker/cli#6335](https://github.com/docker/cli/pull/6335)
- Go SDK: cli/command/service: 移除已弃用的 `NewFormat`、`InspectFormatWrite`。[docker/cli#6339](https://github.com/docker/cli/pull/6339)
- Go SDK: cli/command/stack/swarm: 移除已弃用的 RunPS 和 options.PS。[docker/cli#6398](https://github.com/docker/cli/pull/6398)
- Go SDK: cli/command/stack: 移除 `NewStackCommand`。[docker/cli#6335](https://github.com/docker/cli/pull/6335)
- Go SDK: cli/command/stack: 移除已弃用的 RunList 和 options.List。[docker/cli#6398](https://github.com/docker/cli/pull/6398)
- Go SDK: cli/command/stack: 移除已弃用的 RunServices 和 swarm.GetServices。[docker/cli#6398](https://github.com/docker/cli/pull/6398)
- Go SDK: cli/command/swarm: 移除 `NewSwarmCommand`。[docker/cli#6335](https://github.com/docker/cli/pull/6335)
- Go SDK: cli/command/system: 移除 `NewVersionCommand`、`NewInfoCommand`、`NewSystemCommand`、`NewEventsCommand`、`NewInspectCommand`。[docker/cli#6335](https://github.com/docker/cli/pull/6335)
- Go SDK: cli/command/task: 移除已弃用的 `NewTaskFormat`、`FormatWrite`。[docker/cli#6339](https://github.com/docker/cli/pull/6339)
- Go SDK: cli/command/trust: 移除 `NewTrustCommand`。[docker/cli#6335](https://github.com/docker/cli/pull/6335)
- Go SDK: cli/command/trust: 移除已弃用的 `NewPruneCommand`。[docker/cli#6344](https://github.com/docker/cli/pull/6344)
- Go SDK: cli/command/trust: 移除已弃用的 `SignedTagInfo`、`SignerInfo`、`NewTrustTagFormat`、`NewSignerInfoFormat`、`TagWrite`、`SignerInfoWrite`。[docker/cli#6339](https://github.com/docker/cli/pull/6339)
- Go SDK: cli/command/volume: 移除 `NewVolumeCommand`、`NewPruneCommand`。[docker/cli#6335](https://github.com/docker/cli/pull/6335)
- Go SDK: cli/command/volume: 移除不再使用的 `RunPrune()`。[docker/cli#6236](https://github.com/docker/cli/pull/6236)
- Go SDK: cli/command: 移除仅在内部使用的 `AddTrustSigningFlags`、`AddTrustVerificationFlags` 和 `AddPlatformFlag` 工具。[docker/cli#6244](https://github.com/docker/cli/pull/6244)
- Go SDK: cli/command: 移除已弃用的 `DockerCli.Apply`。[docker/cli#6503](https://github.com/docker/cli/pull/6503)
- Go SDK: cli/command: 移除已弃用的 `DockerCli.ContentTrustEnabled`。[docker/cli#6502](https://github.com/docker/cli/pull/6502)
- Go SDK: cli/command: 移除已弃用的 `DockerCli.DefaultVersion`。[docker/cli#6502](https://github.com/docker/cli/pull/6502)
- Go SDK: cli/command: 移除已弃用的 `RegistryAuthenticationPrivilegedFunc`。[docker/cli#6349](https://github.com/docker/cli/pull/6349)
- Go SDK: cli/command: 移除已弃用的 `WithContentTrustFromEnv`、`WithContentTrust` 选项。[docker/cli#6502](https://github.com/docker/cli/pull/6502)
- Go SDK: cli/config/configfile: 移除已弃用的 `ConfigFile.Experimental` 字段。[docker/cli#6464](https://github.com/docker/cli/pull/6464)
- Go SDK: cli/config/types: 移除已弃用的 `AuthConfig.Email` 字段。[docker/cli#6515](https://github.com/docker/cli/pull/6515)
- Go SDK: cli/manifest/store: 移除已弃用的 `IsNotFound`。[docker/cli#6523](https://github.com/docker/cli/pull/6523)
- Go SDK: cli: 移除已弃用的 `VisitAll`、`DisableFlagsInUseLine` 工具。[docker/cli#6296](https://github.com/docker/cli/pull/6296)
- Go SDK: client: 从 `APIClient` 接口中移除 `ImageInspectWithRaw`。[moby/moby#50485](https://github.com/moby/moby/pull/50485)
- Go SDK: client: 从 `ImageAPIClient` 接口中移除 `ImageAPIClient.ImageInspectWithRaw`。[moby/moby#50485](https://github.com/moby/moby/pull/50485)
- Go SDK: client: 从 `ImageAPIClientDeprecated` 中移除 `ImageAPIClientDeprecated.ImageInspectWithRaw`。[moby/moby#50485](https://github.com/moby/moby/pull/50485)
- Go SDK: client: 移除已弃用的 `ErrorConnectionFailed` 和 `IsErrNotFound` 函数。[moby/moby#50485](https://github.com/moby/moby/pull/50485)
- Go SDK: client: 移除已弃用的 `NewClient` 和 `NewEnvClient` 函数。[moby/moby#50485](https://github.com/moby/moby/pull/50485)
- Go SDK: client: 移除 `CommonAPIClient` 接口。[moby/moby#50485](https://github.com/moby/moby/pull/50485)

- Go SDK：client：移除 `ImageAPIClientDeprecated` 接口。[moby/moby#50485](https://github.com/moby/moby/pull/50485)
- Go SDK：client：移除已弃用的 `Client.ImageInspectWithRaw` 方法。[moby/moby#50485](https://github.com/moby/moby/pull/50485)
- Go SDK：container：移除已弃用的 `IsValidHealthString`。[moby/moby#50378](https://github.com/moby/moby/pull/50378)
- Go SDK：container：移除已弃用的 `IsValidStateString`。[moby/moby#50378](https://github.com/moby/moby/pull/50378)
- Go SDK：container：移除已弃用的 `StateStatus`、`WaitCondition` 以及相关的 `WaitConditionNotRunning`、`WaitConditionNextExit` 和 `WaitConditionRemoved` 常量。[moby/moby#50378](https://github.com/moby/moby/pull/50378)
- Go SDK：弃用 `pkg/stdcopy`，该包已移至 `api/pkg/stdcopy`。[moby/moby#50462](https://github.com/moby/moby/pull/50462)
- Go SDK：弃用字段 `NetworkSettingsBase.Bridge`、结构体 `NetworkSettingsBase`、`DefaultNetworkSettings` 的所有字段以及结构体 `DefaultNetworkSettings`。[moby/moby#50848](https://github.com/moby/moby/pull/50848)
- Go SDK：弃用 pkg/stringid，建议使用 `github.com/moby/moby/client/pkg/stringid`。[moby/moby#50504](https://github.com/moby/moby/pull/50504)
- Go SDK：弃用 profiles 包，该包已迁移至 `github.com/moby/profiles`。[moby/moby#50481](https://github.com/moby/moby/pull/50481)
- Go SDK：oci：弃用 SetCapabilities，以及一些小的清理/修复。[moby/moby#50461](https://github.com/moby/moby/pull/50461)
- Go SDK：opts：移除已弃用的 `ListOpts.GetAll`。它不再被使用，并被 `ListOpts.GetSlice` 替代。[docker/cli#6293](https://github.com/docker/cli/pull/6293)
- Go SDK：opts：移除已弃用的 `NewNamedListOptsRef`、`NewNamedMapOpts`、`NamedListOpts`、`NamedMapOpts` 和 `NamedOption`。这些类型和函数不再被使用，将在下一个版本中移除。[docker/cli#6293](https://github.com/docker/cli/pull/6293)
- Go SDK：opts：移除已弃用的 `ParseEnvFile`，建议使用 `kvfile.Parse`。[docker/cli#6382](https://github.com/docker/cli/pull/6382)
- Go SDK：opts：移除已弃用的 `QuotedString`。[docker/cli#6293](https://github.com/docker/cli/pull/6293)
- Go SDK：opts：移除已弃用的 `ValidateHost`。[docker/cli#6293](https://github.com/docker/cli/pull/6293)
- Go SDK：pkg/system 已被移除，现在是一个内部包。[moby/moby#50559](https://github.com/moby/moby/pull/50559)
- Go SDK：pkg/system：弃用 `EscapeArgs()` 和 `IsAbs`。这些函数仅在内部使用，将在下一个版本中移除。[moby/moby#50399](https://github.com/moby/moby/pull/50399)
- Go SDK：registry：移除已弃用的 `APIEndpoint.TrimHostName`、`APIEndpoint.Official` 和 `APIEndpoint.AllowNondistributableArtifacts` 字段。[moby/moby#50376](https://github.com/moby/moby/pull/50376)
- Go SDK：registry：移除已弃用的 `HostCertsDir()` 和 `SetCertsDir()` 函数。[moby/moby#50373](https://github.com/moby/moby/pull/50373)
- Go SDK：registry：移除已弃用的 `RepositoryInfo.Official` 和 `RepositoryInfo.Class` 字段。[moby/moby#50498](https://github.com/moby/moby/pull/50498)
- Go SDK：registry：移除已弃用的 `Service.ResolveRepository()`。[moby/moby#50374](https://github.com/moby/moby/pull/50374)
- Go SDK：移除 `buildkit.ClientOpts`。[moby/moby#50318](https://github.com/moby/moby/pull/50318)
- Go SDK：移除 `pkg/fileutils`。[moby/moby#50558](https://github.com/moby/moby/pull/50558)
- Go SDK：从 `cli-plugins/manager` 中移除已弃用的 `IsNotFound`、`CommandAnnotationPlugin`、`CommandAnnotationPluginVendor`、`CommandAnnotationPluginVersion`、`CommandAnnotationPluginInvalid`、`CommandAnnotationPluginCommandPath`、`NamePrefix`、`MetadataSubcommandName`、`HookSubcommandName`、`Metadata` 和 `ReexecEnvvar`，建议使用其 `cli-plugins/manager/metadata` 等价物。[docker/cli#6414](https://github.com/docker/cli/pull/6414)
- Go SDK：移除已弃用的 `types/plugins/logdriver` 和 `types/swarm/runtime` 包；插件运行时规范现在通过 `types/swarm.RuntimeSpec` 和 `types/swarm.RuntimePrivilege` 暴露。[moby/moby#50554](https://github.com/moby/moby/pull/50554)
- Go SDK：移除已弃用的 `cli/command/formatter` 包。[docker/cli#6406](https://github.com/docker/cli/pull/6406)
- Go SDK：移除已弃用的 `cli/registry/client` 包。[docker/cli#6462](https://github.com/docker/cli/pull/6462)
- Go SDK：移除已弃用的 `pkg/idtools` 包。[moby/moby#50456](https://github.com/moby/moby/pull/50456)
- Go SDK：templates：移除已弃用的 `NewParse` 函数。[docker/cli#6453](https://github.com/docker/cli/pull/6453)
- 在 `docker run` 和 `docker create` 上隐藏 `--kernel-memory` 选项，并在使用时产生警告，因为它不再被守护进程和内核支持。[docker/cli#6455](https://github.com/docker/cli/pull/6455)
- 在使用 JSON 格式时，从 `docker image ls` 输出中移除 `VirtualSize` 字段。[docker/cli#6524](https://github.com/docker/cli/pull/6524)
- 移除 `VirtualSize` 格式化选项和输出。[docker/cli#6524](https://github.com/docker/cli/pull/6524)
- 移除对 API 版本 < v1.44（Docker v24.0 及更早版本）的 API 版本兼容性。[docker/cli#6551](https://github.com/docker/cli/pull/6551)
- 移除 `--mount` 的已弃用 `bind-nonrecursive` 选项。[docker/cli#6241](https://github.com/docker/cli/pull/6241)
- 移除已弃用的包（`pkg/archive`、`pkg/chrootarchive`、`pkg/atomicwriter`、`pkg/reexec`、`pkg/platform`、`pkg/parsers`）、`pkg/system.MkdirAll`。有关替代方案，请参见 `github.com/moby/go-archive`、`github.com/moby/sys` 和标准库。[moby/moby#50208](https://github.com/moby/moby/pull/50208)
- 移除对 `--tlscacert`、`--tlscert` 和 `--tlskey` 命令行标志的带引号值的特殊处理。[docker/cli#6306](https://github.com/docker/cli/pull/6306)
- 移除对 API < 1.30 的 AutoRemove（`--rm`）支持。[docker/cli#6525](https://github.com/docker/cli/pull/6525)
- 移除对加载旧版（Docker 1.10 之前）镜像的支持。[moby/moby#50324](https://github.com/moby/moby/pull/50324)
