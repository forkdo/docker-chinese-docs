# Docker Engine 17.11 发行说明

## 17.11.0-ce
2017-11-20

> [!重要]
> Docker CE 17.11 是基于 [containerd 1.0 beta](https://github.com/containerd/containerd/releases/tag/v1.0.0-beta.2) 的首个 Docker 版本。
> Docker CE 17.11 及后续版本无法识别使用早期 Docker 版本启动的容器。如果您使用了实时恢复（Live Restore）功能，
> 在升级到 Docker CE 17.11 之前必须停止所有容器。否则，任何由 17.11 之前版本启动的容器在升级后将无法被 Docker 识别，
> 并继续在系统上运行且处于无人管理的状态。

### 构建器

* 测试并修复使用 rm/force-rm 矩阵的构建问题 [moby/moby#35139](https://github.com/moby/moby/pull/35139)
- 修复使用 `--stream` 参数并带有大型上下文时的构建问题 [moby/moby#35404](https://github.com/moby/moby/pull/35404)

### 客户端

* 从帮助输出中隐藏帮助标志 [docker/cli#645](https://github.com/docker/cli/pull/645)
* 支持解析 Compose 卷中的命名管道 [docker/cli#560](https://github.com/docker/cli/pull/560)
* [Compose] 在插值后强制转换值为预期类型 [docker/cli#601](https://github.com/docker/cli/pull/601)
+ 在 `docker stack deploy` 命令中添加对 "secrets" 和 "configs" 的输出 [docker/cli#593](https://github.com/docker/cli/pull/593)
- 修复 `--host-add` 标志的描述 [docker/cli#648](https://github.com/docker/cli/pull/648)
* 在 docker service ps --quiet 命令中不截断 ID [docker/cli#579](https://github.com/docker/cli/pull/579)

### 弃用

* 更新 bash 补全并弃用同步服务更新功能 [docker/cli#610](https://github.com/docker/cli/pull/610)

### 日志

* 复制到日志驱动程序的 bufsize，修复 #34887 [moby/moby#34888](https://github.com/moby/moby/pull/34888)
+ 为 GELF 日志驱动程序添加 TCP 支持 [moby/moby#34758](https://github.com/moby/moby/pull/34758)
+ 为 awslogs 驱动程序添加凭证端点选项 [moby/moby#35055](https://github.com/moby/moby/pull/35055)

### 网络

- 修复删除时网络名称掩盖网络 ID 的问题 [moby/moby#34509](https://github.com/moby/moby/pull/34509)
- 修复网络创建返回的错误代码，从 500 改为 409 [moby/moby#35030](https://github.com/moby/moby/pull/35030)
- 修复任务失败并显示错误 "Unable to complete atomic operation, key modified" [docker/libnetwork#2004](https://github.com/docker/libnetwork/pull/2004)

### 运行时

* 切换到 Containerd 1.0 客户端 [moby/moby#34895](https://github.com/moby/moby/pull/34895)
* 增加 Windows 上容器的默认关闭超时时间 [moby/moby#35184](https://github.com/moby/moby/pull/35184)
* LCOW: API: 在 /images/create 和 /build 中添加 `platform` 参数 [moby/moby#34642](https://github.com/moby/moby/pull/34642)
* 停止按版本过滤 Windows 清单列表 [moby/moby#35117](https://github.com/moby/moby/pull/35117)
* 使用来自 Azure/go-ansiterm 的 Windows 控制台模式常量 [moby/moby#35056](https://github.com/moby/moby/pull/35056)
* Windows 守护进程应尊重 DOCKER_TMPDIR 环境变量 [moby/moby#35077](https://github.com/moby/moby/pull/35077)
* Windows: 修复启动日志记录 [moby/moby#35253](https://github.com/moby/moby/pull/35253)
+ 添加对拉取时 Windows 版本过滤的支持 [moby/moby#35090](https://github.com/moby/moby/pull/35090)
- 修复 containerd 1.0 引入回归后导致的 LCOW 问题 [moby/moby#35320](https://github.com/moby/moby/pull/35320)
* ContainerWait on remove: 在删除失败时不卡住 [moby/moby#34999](https://github.com/moby/moby/pull/34999)
* oci: 对用户命名空间守护进程遵守 CL_UNPRIVILEGED 设置 [moby/moby#35205](https://github.com/moby/moby/pull/35205)
* 设置 may_detach_mounts 时不中止 [moby/moby#35172](https://github.com/moby/moby/pull/35172)
- 修复获取实时恢复容器 PID 时的 panic 问题 [moby/moby#35157](https://github.com/moby/moby/pull/35157)
- 屏蔽容器的 `/proc/scsi` 路径以防止设备被移除 (CVE-2017-16539) [moby/moby#35399](https://github.com/moby/moby/pull/35399)
* 更新到 github.com/vbatts/tar-split@v0.10.2 (CVE-2017-14992) [moby/moby#35424](https://github.com/moby/moby/pull/35424)

### Swarm 模式

* 由于 swarmkit 中新的 IPAM 选项，修改集成测试 [moby/moby#35103](https://github.com/moby/moby/pull/35103)
- 修复获取 swarm 信息时的死锁问题 [moby/moby#35388](https://github.com/moby/moby/pull/35388)
+ 扩展 `TaskStatus` 中 `Err` 字段的作用范围，使其也涵盖阻止任务进展的非终端错误 [docker/swarmkit#2287](https://github.com/docker/swarmkit/pull/2287)

### 打包

+ 为 Debian 10 (Buster) 构建软件包 [docker/docker-ce-packaging#50](https://github.com/docker/docker-ce-packaging/pull/50)
+ 为 Ubuntu 17.10 (Artful) 构建软件包 [docker/docker-ce-packaging#55](https://github.com/docker/docker-ce-packaging/pull/55)
