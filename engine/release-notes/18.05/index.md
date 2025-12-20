# Docker Engine 18.05 发布说明

## 18.05.0-ce
2018-05-09

### Builder

*  为 `pkg/term` 包添加 `netbsd` 兼容性。 [moby/moby#36887](https://github.com/moby/moby/pull/36887)
*  将中间构建产物的输出路径标准化为 `/build/`。 [moby/moby#36858](https://github.com/moby/moby/pull/36858)

### Client

- 修复 `docker stack deploy` 的 reference 标志。 [docker/cli#981](https://github.com/docker/cli/pull/981)
- 修复在使用 `--force` 更新服务后，docker stack deploy 会重新部署服务的问题。 [docker/cli#963](https://github.com/docker/cli/pull/963)
+ 为 `secret|config create --template-driver` 添加 bash 补全。 [docker/cli#1004](https://github.com/docker/cli/pull/1004)
+ 为 docker trust 子命令添加 fish 补全。 [docker/cli#984](https://github.com/docker/cli/pull/984)
- 修复 docker history 的 --format 示例。 [docker/cli#980](https://github.com/docker/cli/pull/980)
- 修复合并包含网络的 composefile 时出现的错误。 [docker/cli#983](https://github.com/docker/cli/pull/983)

### Logging
* 标准化 storage-driver 日志消息的属性。 [moby/moby#36492](https://github.com/moby/moby/pull/36492)
* 改进 logger 中对部分消息的支持。 [moby/moby#35831](https://github.com/moby/moby/pull/35831)

### Networking

- 允许更大的预设属性值，不进行覆盖。 [docker/libnetwork#2124](https://github.com/docker/libnetwork/pull/2124)
- networkdb: 在 handleNodeEvent 中使用写锁。 [docker/libnetwork#2136](https://github.com/docker/libnetwork/pull/2136)
* 导入 libnetwork 的滚动更新修复。 [moby/moby#36638](https://github.com/moby/moby/pull/36638)
* 更新 libnetwork 以提高桥接网络隔离规则的可扩展性。 [moby/moby#36774](https://github.com/moby/moby/pull/36774)
- 修复一个被误用的网络对象名称。 [moby/moby#36745](https://github.com/moby/moby/pull/36745)

### Runtime

* LCOW: 实现 `docker save`。 [moby/moby#36599](https://github.com/moby/moby/pull/36599)
* Pkg: devmapper: 动态加载 dm_task_deferred_remove。 [moby/moby#35518](https://github.com/moby/moby/pull/35518)
* Windows: 在 graphdriver 中添加 GetLayerPath 实现。 [moby/moby#36738](https://github.com/moby/moby/pull/36738)
- 修复写入失败时的 Windows 层泄漏问题。 [moby/moby#36728](https://github.com/moby/moby/pull/36728)
- 修复在用户命名空间中运行时的 FIFO、套接字和设备文件问题。 [moby/moby#36756](https://github.com/moby/moby/pull/36756)
- 修复 docker version 输出的对齐问题。 [docker/cli#965](https://github.com/docker/cli/pull/965)
* 使用特权模式时始终使 sysfs 为读写状态。 [moby/moby#36808](https://github.com/moby/moby/pull/36808)
* 将 Golang 升级到 1.10.1。 [moby/moby#35739](https://github.com/moby/moby/pull/35739)
* 升级 containerd 客户端。 [moby/moby#36684](https://github.com/moby/moby/pull/36684)
* 将 golang.org/x/net 升级到 go1.10 的发布提交。 [moby/moby#36894](https://github.com/moby/moby/pull/36894)
* Context.WithTimeout: 调用 cancel 函数。 [moby/moby#36920](https://github.com/moby/moby/pull/36920)
* Copy: 避免在使用 authz 插件时耗尽所有系统内存。 [moby/moby#36595](https://github.com/moby/moby/pull/36595)
* Daemon/cluster: 在配置期间处理部分 attachment 条目。 [moby/moby#36769](https://github.com/moby/moby/pull/36769)
* 不要使容器挂载不可绑定。 [moby/moby#36768](https://github.com/moby/moby/pull/36768)
* 在卸载前进行额外检查。 [moby/moby#36879](https://github.com/moby/moby/pull/36879)
* 将挂载解析移至单独的包。 [moby/moby#36896](https://github.com/moby/moby/pull/36896)
* 无全局卷驱动存储。 [moby/moby#36637](https://github.com/moby/moby/pull/36637)
* Pkg/mount 改进。 [moby/moby#36091](https://github.com/moby/moby/pull/36091)
* 放宽部分 libcontainerd 客户端锁。 [moby/moby#36848](https://github.com/moby/moby/pull/36848)
* 移除 daemon 对 api 包的依赖。 [moby/moby#36912](https://github.com/moby/moby/pull/36912)
* 移除服务更新的重试。 [moby/moby#36827](https://github.com/moby/moby/pull/36827)
* 撤销未加密存储的警告提示。 [docker/cli#1008](https://github.com/docker/cli/pull/1008)
* 在 `directory.Size()` 中支持取消。 [moby/moby#36734](https://github.com/moby/moby/pull/36734)
* 从 x/net/context 切换到 context。 [moby/moby#36904](https://github.com/moby/moby/pull/36904)
* 修复一个用于检查 Content-type 是否为 `application/json` 的函数。 [moby/moby#36778](https://github.com/moby/moby/pull/36778)
+ 添加默认的 pollSettings 配置函数。 [moby/moby#36706](https://github.com/moby/moby/pull/36706)
+ 在接收 daemonWaitCh 的操作前添加 if 判断。 [moby/moby#36651](https://github.com/moby/moby/pull/36651)
- 修复以非 root 用户运行卷测试时出现的问题。 [moby/moby#36935](https://github.com/moby/moby/pull/36935)

### Swarm Mode

* RoleManager 将从集群成员中移除检测到的节点 [docker/swarmkit#2548](https://github.com/docker/swarmkit/pull/2548)
* Scheduler/TaskReaper: 处理标记为关闭但未分配的任务 [docker/swarmkit#2574](https://github.com/docker/swarmkit/pull/2574)
* 避免预定义的错误日志。 [docker/swarmkit#2561](https://github.com/docker/swarmkit/pull/2561)
* Task reaper 应删除已移除插槽但尚未分配的任务。 [docker/swarmkit#2557](https://github.com/docker/swarmkit/pull/2557)
* Agent 报告 FIPS 状态。 [docker/swarmkit#2587](https://github.com/docker/swarmkit/pull/2587)
- 修复: timeMutex 在临界区外执行临界操作。 [docker/swarmkit#2603](https://github.com/docker/swarmkit/pull/2603)
* 在引擎配置中公开 swarmkit 的 Raft 调优参数。 [moby/moby#36726](https://github.com/moby/moby/pull/36726)
* 使 internal/test/daemon.Daemon 具备 swarm 感知能力。 [moby/moby#36826](https://github.com/moby/moby/pull/36826)
