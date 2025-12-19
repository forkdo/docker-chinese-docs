---
title: Docker Engine 历史版本
linkTitle: 历史版本
weight: 100
description: Docker CE 发布说明
keywords: 发布说明, 社区
toc_max: 2
aliases:
- /cs-engine/1.12/release-notes/
- /cs-engine/1.12/release-notes/release-notes/
- /cs-engine/1.12/release-notes/prior-release-notes/
- /cs-engine/1.13/release-notes/
- /ee/engine/release-notes/
- /ee/docker-ee/release-notes/
---

## 1.13.1 (2017-02-08)

> [!IMPORTANT]
>
> 在默认存储驱动为 `devicemapper` 的 Linux 发行版上，现在默认使用 `overlay2` 或 `overlay`（如果内核支持）。要使用 devicemapper，可以通过 `--storage-driver` 守护进程选项手动配置要使用的存储驱动，或者在 `daemon.json` 配置文件中设置 "storage-driver"。

> [!IMPORTANT]
>
> 在 Docker 1.13 中，托管插件 API 相较于 Docker 1.12 中引入的实验性版本发生了变化。在升级到 Docker 1.13 之前，您必须**卸载**使用 Docker 1.12 安装的插件。您可以使用 `docker plugin rm` 命令卸载插件。

如果您在未卸载先前安装的插件的情况下升级到 Docker 1.13，当 Docker 守护进程启动时，您可能会看到以下消息：

    Error starting daemon: json: cannot unmarshal string into Go value of type types.PluginEnv

要手动删除所有插件并解决此问题，请执行以下步骤：

1. 从 `/var/lib/docker/plugins/` 中移除 plugins.json。
2. 重启 Docker。验证 Docker 守护进程是否无错误启动。
3. 重新安装您的插件。

### Contrib

* 不再需要自定义构建 tini [#28454](https://github.com/docker/docker/pull/28454)
* 升级到 Go 1.7.5 [#30489](https://github.com/docker/docker/pull/30489)

### Remote API (v1.26) & Client

+ 支持在 docker stack deploy 中使用 compose 文件处理 secrets [#30144](https://github.com/docker/docker/pull/30144)

### Runtime

* 修复 `docker system df` 中的大小问题 [#30378](https://github.com/docker/docker/pull/30378)
* 修复当 Swarm 证书过期时 `docker inspect` 的错误 [#29246](https://github.com/docker/docker/pull/29246)
* 修复 v1 插件在激活错误时的死锁问题 [#30408](https://github.com/docker/docker/pull/30408)
* 修复 SELinux 回归问题 [#30649](https://github.com/docker/docker/pull/30649)

### Plugins

* 在 swarm 模式下支持全局范围的网络插件 (v2) [#30332](https://github.com/docker/docker/pull/30332)
+ 添加 `docker plugin upgrade` [#29414](https://github.com/docker/docker/pull/29414)

### Windows

* 修复旧插件在 Windows 上的小回归问题 [#30150](https://github.com/docker/docker/pull/30150)
* 修复 Windows 上的警告 [#30730](https://github.com/docker/docker/pull/30730)

## 1.13.0 (2017-01-18)

> [!IMPORTANT]
>
> 在默认存储驱动为 `devicemapper` 的 Linux 发行版上，现在默认使用 `overlay2` 或 `overlay`（如果内核支持）。要使用 devicemapper，可以通过 `--storage-driver` 守护进程选项手动配置要使用的存储驱动，或者在 `daemon.json` 配置文件中设置 "storage-driver"。

> [!IMPORTANT]
>
> 在 Docker 1.13 中，托管插件 API 相较于 Docker 1.12 中引入的实验性版本发生了变化。在升级到 Docker 1.13 之前，您必须**卸载**使用 Docker 1.12 安装的插件。您可以使用 `docker plugin rm` 命令卸载插件。

如果您在未卸载先前安装的插件的情况下升级到 Docker 1.13，当 Docker 守护进程启动时，您可能会看到以下消息：

    Error starting daemon: json: cannot unmarshal string into Go value of type types.PluginEnv

要手动删除所有插件并解决此问题，请执行以下步骤：

1. 从 `/var/lib/docker/plugins/` 中移除 plugins.json。
2. 重启 Docker。验证 Docker 守护进程是否无错误启动。
3. 重新安装您的插件。

### Builder

+ 增加在构建时指定用作缓存源的镜像的能力。这些镜像不需要具有本地父链，可以从其他注册表拉取 [#26839](https://github.com/docker/docker/pull/26839)
+ (实验性) 增加在成功构建后将镜像层压缩到 FROM 镜像的选项 [#22641](https://github.com/docker/docker/pull/22641)
* 修复在转义符后有空行时 Dockerfile 解析器的问题 [#24725](https://github.com/docker/docker/pull/24725)
- 在 `docker build` 中增加步骤编号 [#24978](https://github.com/docker/docker/pull/24978)
+ 支持在镜像构建期间压缩构建上下文 [#25837](https://github.com/docker/docker/pull/25837)
+ 在 `docker build` 中添加 `--network` [#27702](https://github.com/docker/docker/pull/27702)
- 修复 `docker build` 和 `docker run` 上 `--label` 标志行为不一致的问题 [#26027](https://github.com/docker/docker/issues/26027)
- 修复使用 overlay 存储驱动时镜像层不一致的问题 [#27209](https://github.com/docker/docker/pull/27209)
* 现在允许未使用的 build-args。会显示警告而不是错误并导致构建失败 [#27412](https://github.com/docker/docker/pull/27412)
- 修复 Windows 上构建器缓存问题 [#27805](https://github.com/docker/docker/pull/27805)
+ 在 Windows 构建器中允许 `USER` [#28415](https://github.com/docker/docker/pull/28415)
+ 在 Windows 上处理环境变量时不区分大小写 [#28725](https://github.com/docker/docker/pull/28725)

### Contrib

+ 增加在 PPC64LE 上为 Ubuntu 16.04 Xenial 构建 docker deb 包的支持 [#23438](https://github.com/docker/docker/pull/23438)
+ 增加在 s390x 上为 Ubuntu 16.04 Xenial 构建 docker deb 包的支持 [#26104](https://github.com/docker/docker/pull/26104)
+ 增加在 PPC64LE 上为 Ubuntu 16.10 Yakkety Yak 构建 docker deb 包的支持 [#28046](https://github.com/docker/docker/pull/28046)
- 为 VMWare Photon OS 添加 RPM 构建器 [#24116](https://github.com/docker/docker/pull/24116)
+ 在 tgz 中添加 shell 自动补全 [#27735](https://github.com/docker/docker/pull/27735)
* 更新安装脚本以允许使用中国镜像 [#27005](https://github.com/docker/docker/pull/27005)
+ 为 Ubuntu 16.10 Yakkety Yak 添加 DEB 构建器 [#27993](https://github.com/docker/docker/pull/27993)
+ 为 Fedora 25 添加 RPM 构建器 [#28222](https://github.com/docker/docker/pull/28222)
+ 为 aarch64 添加 `make deb` 支持 [#27625](https://github.com/docker/docker/pull/27625)

### Distribution

* 将 notary 依赖更新到 0.4.2（完整变更日志 [此处](https://github.com/docker/notary/releases/tag/v0.4.2)） [#27074](https://github.com/docker/docker/pull/27074)
  - 支持在 windows 上编译 [docker/notary#970](https://github.com/docker/notary/pull/970)
  - 改进了客户端认证错误的错误消息 [docker/notary#972](https://github.com/docker/notary/pull/972)
  - 支持在 `~/.docker/trust/private` 目录下的任何位置查找密钥，而不仅仅是在 `~/.docker/trust/private/root_keys` 或 `~/.docker/trust/private/tuf_keys` 下 [docker/notary#981](https://github.com/docker/notary/pull/981)
  - 以前，在任何更新错误时，客户端都会回退到缓存。现在我们只在网络错误、服务器不可用或缺少 TUF 数据时才这样做。无效的 TUF 数据将导致更新失败 - 例如，如果存在无效的根轮换。[docker/notary#982](https://github.com/docker/notary/pull/982)
  - 改进根验证和 yubikey 调试日志 [docker/notary#858](https://github.com/docker/notary/pull/858) [docker/notary#891](https://github.com/docker/notary/pull/891)
  - 如果根或委派的证书即将过期则发出警告 [docker/notary#802](https://github.com/docker/notary/pull/802)
  - 如果角色元数据即将过期则发出警告 [docker/notary#786](https://github.com/docker/notary/pull/786)
  - 修复密码短语检索尝试计数和终端检测 [docker/notary#906](https://github.com/docker/notary/pull/906)
- 避免在不同用户将相同层推送到经过身份验证的注册表时进行不必要的 blob 上传 [#26564](https://github.com/docker/docker/pull/26564)
* 允许注册表凭据使用外部存储 [#26354](https://github.com/docker/docker/pull/26354)

### Logging

* 在所有日志驱动中标准化默认日志标签值 [#22911](https://github.com/docker/docker/pull/22911)
- 改进记录长日志行时的性能和内存使用 [#22982](https://github.com/docker/docker/pull/22982)
+ 为 Windows 启用 syslog 驱动程序 [#25736](https://github.com/docker/docker/pull/25736)
+ 添加 Logentries 驱动程序 [#27471](https://github.com/docker/docker/pull/27471)
+ 更新 AWS 日志驱动程序以支持标签 [#27707](https://github.com/docker/docker/pull/27707)
+ 为 fluentd 添加 Unix 套接字支持 [#26088](https://github.com/docker/docker/pull/26088)
* 在 Windows 上启用 fluentd 日志驱动程序 [#28189](https://github.com/docker/docker/pull/28189)
- 当用作 journald 字段名时，清理 docker 标签 [#23725](https://github.com/docker/docker/pull/23725)
- 修复 `docker logs --tail` 返回的行数少于预期的问题 [#28203](https://github.com/docker/docker/pull/28203)
- Splunk 日志驱动程序：性能和可靠性改进 [#26207](https://github.com/docker/docker/pull/26207)
- Splunk 日志驱动程序：可配置的格式和跳过连接验证 [#25786](https://github.com/docker/docker/pull/25786)

### Networking

+ 添加 `--attachable` 网络支持，使 `docker run` 能够在 swarm 模式覆盖网络中工作 [#25962](https://github.com/docker/docker/pull/25962)
+ 在使用 `docker service create` 的 `--publish` 选项时，支持主机端口发布模式 [#27917](https://github.com/docker/docker/pull/27917) 和 [#28943](https://github.com/docker/docker/pull/28943)
+ 支持 Windows Server 2016 覆盖网络驱动程序（需要即将到来的 ws2016 更新） [#28182](https://github.com/docker/docker/pull/28182)
* 将默认的 `FORWARD` 策略更改为 `DROP` [#28257](https://github.com/docker/docker/pull/28257)
+ 支持在 Windows 上为预定义网络指定静态 IP 地址 [#22208](https://github.com/docker/docker/pull/22208)
- 修复 `docker run` 上的 `--publish` 标志在使用 IPv6 地址时不起作用的问题 [#27860](https://github.com/docker/docker/pull/27860)
- 修复检查网络时显示带掩码的网关 [#25564](https://github.com/docker/docker/pull/25564)
- 修复当网桥中有多个地址时可能导致 `--fixed-cidr` 没有正确地址的问题 [#26659](https://github.com/docker/docker/pull/26659)
+ 在 `docker network inspect` 中添加创建时间戳 [#26130](https://github.com/docker/docker/pull/26130)
- 在 `docker network inspect` 中显示 swarm 覆盖网络的对等节点 [#28078](https://github.com/docker/docker/pull/28078)
- 为服务 VIP 地址启用 ping [#28019](https://github.com/docker/docker/pull/28019)

### Plugins

- 将插件移出实验性阶段 [#28226](https://github.com/docker/docker/pull/28226)
- 在 `docker plugin remove` 上添加 `--force` [#25096](https://github.com/docker/docker/pull/25096)
* 支持动态重新加载授权插件 [#22770](https://github.com/docker/docker/pull/22770)
+ 在 `docker plugin ls` 中添加描述 [#25556](https://github.com/docker/docker/pull/25556)
+ 在 `docker plugin inspect` 中添加 `-f`/`--format` [#25990](https://github.com/docker/docker/pull/25990)
+ 添加 `docker plugin create` 命令 [#28164](https://github.com/docker/docker/pull/28164)
* 将请求的 TLS 对等证书发送到授权插件 [#27383](https://github.com/docker/docker/pull/27383)
* 在 swarm 模式下支持全局范围的网络和 ipam 插件 [#27287](https://github.com/docker/docker/pull/27287)
* 将 `docker plugin install` 拆分为两个 API 调用 `/privileges` 和 `/pull` [#28963](https://github.com/docker/docker/pull/28963)

### Remote API (v1.25) & Client

+ 支持从 Compose 文件进行 `docker stack deploy` [#27998](https://github.com/docker/docker/pull/27998)
+ (实验性) 实现检查点和恢复 [#22049](https://github.com/docker/docker/pull/22049)
+ 在 `docker info` 中添加 `--format` 标志 [#23808](https://github.com/docker/docker/pull/23808)
* 从 `docker volume create` 中移除 `--name` [#23830](https://github.com/docker/docker/pull/23830)
+ 添加 `docker stack ls` [#23886](https://github.com/docker/docker/pull/23886)
+ 添加新的 `is-task` ps 过滤器 [#24411](https://github.com/docker/docker/pull/24411)
+ 在 `docker service create` 中添加 `--env-file` 标志 [#24844](https://github.com/docker/docker/pull/24844)
+ 在 `docker stats` 中添加 `--format` [#24987](https://github.com/docker/docker/pull/24987)
+ 使 `docker node ps` 在 swarm 节点中默认为 `self` [#25214](https://github.com/docker/docker/pull/25214)
+ 在 `docker service create` 中添加 `--group` [#25317](https://github.com/docker/docker/pull/25317)
+ 在 service/node/stack ps 输出中添加 `--no-trunc` [#25337](https://github.com/docker/docker/pull/25337)
+ 在 `ContainerAttachOptions` 中添加 Logs，以便 go 客户端可以在附加过程中请求检索容器日志 [#26718](https://github.com/docker/docker/pull/26718)
+ 允许客户端与旧服务器通信 [#27745](https://github.com/docker/docker/pull/27745)
* 通知客户端容器正在被移除 [#26074](https://github.com/docker/docker/pull/26074)
+ 在 /info 端点中添加 `Isolation` [#26255](https://github.com/docker/docker/pull/26255)
+ 在 /info 端点中添加 `userns` [#27840](https://github.com/docker/docker/pull/27840)
- 不允许在服务端点中同时请求多个模式 [#26643](https://github.com/docker/docker/pull/26643)
+ 为 /containers/create API 添加功能，以更精细和安全的方式指定挂载 [#22373](https://github.com/docker/docker/pull/22373)
+ 在 `network ls` 和 `volume ls` 中添加 `--format` 标志 [#23475](https://github.com/docker/docker/pull/23475)
* 允许顶级 `docker inspect` 命令检查任何类型的资源 [#23614](https://github.com/docker/docker/pull/23614)
+ 在 `docker run` 和 `docker create` 中添加 `--cpus` 标志以控制 CPU 资源，并在 `HostConfig` 中添加 `NanoCPUs` [#27958](https://github.com/docker/docker/pull/27958)
- 允许在 `docker run` 或 `docker create` 中取消设置 `--entrypoint` [#23718](https://github.com/docker/docker/pull/23718)
* 通过添加 `docker image` 和 `docker container` 命令来重构 CLI 命令，以实现更高的一致性 [#26025](https://github.com/docker/docker/pull/26025)
- 从 `service ls` 输出中移除 `COMMAND` 列 [#28029](https://github.com/docker/docker/pull/28029)
+ 在 `docker events` 中添加 `--format` [#26268](https://github.com/docker/docker/pull/26268)
* 允许在 `docker node ps` 上指定多个节点 [#26299](https://github.com/docker/docker/pull/26299)
* 在 `docker images` 输出中将小数位限制为 2 位小数 [#26303](https://github.com/docker/docker/pull/26303)
+ 在 `docker run` 中添加 `--dns-option` [#28186](https://github.com/docker/docker/pull/28186)
+ 在容器提交事件中添加镜像 ID [#28128](https://github.com/docker/docker/pull/28128)
+ 在 docker info 中添加外部二进制文件版本 [#27955](https://github.com/docker/docker/pull/27955)
+ 在 `docker info` 的输出中添加 `Manager Addresses` 信息 [#28042](https://github.com/docker/docker/pull/28042)
+ 为 `docker images` 添加新的引用过滤器 [#27872](https://github.com/docker/docker/pull/27872)

### Runtime

+ 添加 `--experimental` 守护进程标志以启用实验性功能，而不是在单独的构建中提供它们 [#27223](https://github.com/docker/docker/pull/27223)
+ 添加 `--shutdown-timeout` 守护进程标志，以指定在守护进程退出前优雅停止容器的默认超时（秒） [#23036](https://github.com/docker/docker/pull/23036)
+ 添加 `--stop-timeout` 以指定单个容器停止的超时值（秒） [#22566](https://github.com/docker/docker/pull/22566)
+ 添加新的守护进程标志 `--userland-proxy-path`，以允许配置用户空间代理，而不是使用硬编码的 `$PATH` 中的 `docker-proxy` [#26882](https://github.com/docker/docker/pull/26882)
+ 在 `dockerd` 和 `docker run` 上添加布尔标志 `--init`，以使用 [tini](https://github.com/krallin/tini) 作为 PID 1 的僵尸回收初始化进程 [#26061](https://github.com/docker/docker/pull/26061) [#28037](https://github.com/docker/docker/pull/28037)
+ 添加新的守护进程标志 `--init-path`，以允许配置 `docker-init` 二进制文件的路径 [#26941](https://github.com/docker/docker/pull/26941)
+ 支持在配置中热加载不安全的注册表 [#22337](https://github.com/docker/docker/pull/22337)
+ 支持 Windows 守护进程上的 storage-opt 大小 [#23391](https://github.com/docker/docker/pull/23391)
* 通过将 `docker run --rm` 从客户端移到守护进程来提高可靠性 [#20848](https://github.com/docker/docker/pull/20848)
+ 支持 `--cpu-rt-period` 和 `--cpu-rt-runtime` 标志，允许容器在内核中启用 `CONFIG_RT_GROUP_SCHED` 时运行实时线程 [#23430](https://github.com/docker/docker/pull/23430)
* 允许并行停止、暂停、取消暂停 [#24761](https://github.com/docker/docker/pull/24761) / [#26778](https://github.com/docker/docker/pull/26778)
* 为 overlay2 实现 XFS 配额 [#24771](https://github.com/docker/docker/pull/24771)
- 修复 `service tasks --filter` 中的部分/完整过滤器问题 [#24850](https://github.com/docker/docker/pull/24850)
- 允许引擎在用户命名空间内运行 [#25672](https://github.com/docker/docker/pull/25672)
- 修复在使用 devicemapper 图形驱动程序时设备延迟删除和恢复设备之间的竞争条件 [#23497](https://github.com/docker/docker/pull/23497)
- 在 Windows 中添加 `docker stats` 支持 [#25737](https://github.com/docker/docker/pull/25737)
- 允许在 `--userns=host` 时使用 `--pid=host` 和 `--net=host` [#25771](https://github.com/docker/docker/pull/25771)
+ (实验性) 为基本的 `container`、`image` 和 `daemon` 操作添加指标（Prometheus）输出 [#25820](https://github.com/docker/docker/pull/25820)
- 修复 `docker stats` 在 `NetworkDisabled=true` 时的问题 [#25905](https://github.com/docker/docker/pull/25905)
+ 在 Windows 中添加 `docker top` 支持 [#25891](https://github.com/docker/docker/pull/25891)
+ 记录 exec 进程的 pid [#27470](https://github.com/docker/docker/pull/27470)
+ 支持通过 `getent` 查找用户/组 [#27599](https://github.com/docker/docker/pull/27599)
+ 添加新的 `docker system` 命令，包含用于系统资源管理的 `df` 和 `prune` 子命令，以及 `docker {container,image,volume,network} prune` 子命令 [#26108](https://github.com/docker/docker/pull/26108) [#27525](https://github.com/docker/docker/pull/27525) / [#27525](https://github.com/docker/docker/pull/27525)
- 修复在使用 devicemapper 时，当 ENOSPC 时将 xfs max_retries 设置为 0 导致容器无法停止或杀死的问题 [#26212](https://github.com/docker/docker/pull/26212)
- 修复在 CentOS 上使用 devicemapper 时 `docker cp` 无法复制到容器卷目录的问题 [#28047](https://github.com/docker/docker/pull/28047)
* 提升 overlay(2) 图形驱动程序 [#27932](https://github.com/docker/docker/pull/27932)
+ 添加 `--seccomp-profile` 守护进程标志，以指定覆盖默认值的 seccomp 配置文件路径 [#26276](https://github.com/docker/docker/pull/26276)
- 修复当守护进程上设置了 `--default-ulimit` 时 `docker inspect` 中的 ulimits [#26405](https://github.com/docker/docker/pull/26405)
- 为旧内核中构建期间的 overlay 问题添加解决方法 [#28138](https://github.com/docker/docker/pull/28138)
+ 在 `docker exec -t` 上添加 `TERM` 环境变量 [#26461](https://github.com/docker/docker/pull/26461)
* 在 `docker kill` 时尊重容器的 `--stop-signal` 设置 [#26464](https://github.com/docker/docker/pull/26464)

### Swarm Mode

+ 添加 secret 管理 [#27794](https://github.com/docker/docker/pull/27794)
+ 支持服务选项（主机名、挂载和环境变量）的模板化 [#28025](https://github.com/docker/docker/pull/28025)
* 在 `docker service inspect --pretty` 的输出中显示端点模式 [#26906](https://github.com/docker/docker/pull/26906)
* 通过缩短任务名称中的服务 ID 使 `docker service ps` 输出更易读 [#28088](https://github.com/docker/docker/pull/28088)
* 使 `docker node ps` 默认为当前节点 [#25214](https://github.com/docker/docker/pull/25214)
+ 在 service create 中添加 `--dns`、`--dns-opt` 和 `--dns-search` [#27567](https://github.com/docker/docker/pull/27567)
+ 在 `docker service update` 中添加 `--force` [#27596](https://github.com/docker/docker/pull/27596)
+ 在 `docker service create` 和 `docker service update` 中添加 `--health-*` 和 `--no-healthcheck` 标志 [#27369](https://github.com/docker/docker/pull/27369)
+ 在 `docker service ps` 中添加 `-q` [#27654](https://github.com/docker/docker/pull/27654)
* 在 `docker service ls` 中显示全局服务的数量 [#27710](https://github.com/docker/docker/pull/27710)
- 从 `docker service update` 中移除 `--name` 标志。此标志仅在 `docker service create` 上有效，因此已从 `update` 命令中移除 [#26988](https://github.com/docker/docker/pull/26988)
- 修复工作节点因瞬态网络问题而无法恢复的问题 [#26646](https://github.com/docker/docker/issues/26646)
* 支持感知健康的负载均衡和 DNS 记录 [#27279](https://github.com/docker/docker/pull/27279)
+ 在 `docker service create` 中添加 `--hostname` [#27857](https://github.com/docker/docker/pull/27857)
+ 在 `docker service create` 中添加 `--host`，并在 `docker service update` 中添加 `--host-add`、`--host-rm` [#28031](https://github.com/docker/docker/pull/28031)
+ 在 `docker service create`/`update` 中添加 `--tty` 标志 [#28076](https://github.com/docker/docker/pull/28076)
* 自动检测、存储并暴露管理器看到的节点 IP 地址 [#27910](https://github.com/docker/docker/pull/27910)
* 管理器密钥和 raft 数据的静态加密 [#27967](https://github.com/docker/docker/pull/27967)
+ 在 `docker service update` 中添加 `--update-max-failure-ratio`、`--update-monitor` 和 `--rollback` 标志 [#26421](https://github.com/docker/docker/pull/26421)
- 修复在容器内运行 `docker swarm init` 时地址自动发现的问题 [#26457](https://github.com/docker/docker/pull/26457)
+ (实验性) 添加 `docker service logs` 命令以查看服务的日志 [#28089](https://github.com/docker/docker/pull/28089)
+ 为 `docker service create` 和 `update` 按摘要固定镜像 [#28173](https://github.com/docker/docker/pull/28173)
* 为 `docker node rm --force` 和 `docker swarm leave --force` 添加短标志 `-f` [#28196](https://github.com/docker/docker/pull/28196)
+ 添加选项以自定义 Raft 快照（`--max-snapshots`、`--snapshot-interval`） [#27997](https://github.com/docker/docker/pull/27997)
- 如果按摘要固定，则不重新拉取镜像 [#28265](https://github.com/docker/docker/pull/28265)
+ Swarm 模式支持 Windows [#27838](https://github.com/docker/docker/pull/27838)
+ 允许在服务上更新主机名 [#28771](https://github.com/docker/docker/pull/28771)
+ 支持 v2 插件 [#29433](https://github.com/docker/docker/pull/29433)
+ 为服务添加内容信任 [#29469](https://github.com/docker/docker/pull/29469)

### Volume

+ 支持卷上的标签 [#21270](https://github.com/docker/docker/pull/21270)
+ 支持按标签过滤卷 [#25628](https://github.com/docker/docker/pull/25628)
* 在 `docker volume rm` 中添加 `--force` 标志以强制清除已删除卷的数据 [#23436](https://github.com/docker/docker/pull/23436)
* 增强 `docker volume inspect` 以显示创建卷时使用的所有选项 [#26671](https://github.com/docker/docker/pull/26671)
* 支持本地 NFS 卷解析主机名 [#27329](https://github.com/docker/docker/pull/27329)

### Security

- 修复容器中共享卷的 selinux 标记 [#23024](https://github.com/docker/docker/pull/23024)
- 禁止通过 apparmor 访问 `/sys/firmware/**` [#26618](https://github.com/docker/docker/pull/26618)

### Deprecation

- 将 `docker daemon` 命令标记为已弃用。守护进程已移至单独的二进制文件 (`dockerd`)，应改用它 [#26834](https://github.com/docker/docker/pull/26834)
- 弃用未版本化的 API 端点 [#28208](https://github.com/docker/docker/pull/28208)
- 移除对 Ubuntu 15.10 (Wily Werewolf) 作为支持平台。Ubuntu 15.10 已终止支持，不再接收更新 [#27042](https://github.com/docker/docker/pull/27042)
- 移除对 Fedora 22 作为支持平台。Fedora 22 已终止支持，不再接收更新 [#27432](https://github.com/docker/docker/pull/27432)
- 移除对 Fedora 23 作为支持平台。Fedora 23 已终止支持，不再接收更新 [#29455](https://github.com/docker/docker/pull/29455)
- 弃用 `docker pull` 上的 `repo:shortid` 语法 [#27207](https://github.com/docker/docker/pull/27207)
- 弃用 overlay 和 overlay2 存储驱动程序不支持 `d_type` 的后备文件系统 [#27433](https://github.com/docker/docker/pull/27433)
- 弃用 Dockerfile 中的