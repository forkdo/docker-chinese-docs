# Docker Engine 17.12 发布说明

## 17.12.1-ce
2018-02-27

### Client
- 修复 `node-generic-resource` 拼写错误 [moby/moby#35970](https://github.com/moby/moby/pull/35970) 和 [moby/moby#36125](https://github.com/moby/moby/pull/36125)
* 在 stack deploy 配置创建/更新时，返回来自 daemon 的错误 [docker/cli#757](https://github.com/docker/cli/pull/757)

### Logging
- awslogs：修复大日志的批处理大小计算 [moby/moby#35726](https://github.com/moby/moby/pull/35726)
* 在 splunk 日志驱动中支持代理 [moby/moby#36220](https://github.com/moby/moby/pull/36220)

### Networking
- 修复从 17.09 升级到 17.12 时的 ingress 网络问题 [moby/moby#36003](https://github.com/moby/moby/pull/36003)
* 为部分 overlay ID 添加详细信息 [moby/moby#35989](https://github.com/moby/moby/pull/35989)
- 修复启用 live-restore 时 IPv6 网络被取消配置的问题 [docker/libnetwork#2043](https://github.com/docker/libnetwork/pull/2043)
- 修复 watchMiss 线程上下文 [docker/libnetwork#2051](https://github.com/docker/libnetwork/pull/2051)

### Packaging
- 在 docker.service 中设置 TasksMax [docker/docker-ce-packaging#78](https://github.com/docker/docker-ce-packaging/pull/78)

### Runtime
* Golang 升级至 1.9.4
* containerd 升级至 1.0.1
- 修复 dockerd 在 containerd 重启后无法重新连接的问题 [moby/moby#36173](https://github.com/moby/moby/pull/36173)
- 修复 containerd 事件被处理两次的问题 [moby/moby#35891](https://github.com/moby/moby/issues/35891)
- 修复 vfs 图形驱动因设置 fs 配额失败而无法初始化的问题 [moby/moby#35827](https://github.com/moby/moby/pull/35827)
- 修复健康检查不使用容器工作目录的回归问题 [moby/moby#35845](https://github.com/moby/moby/pull/35845)
- 在 containerd 1.0 中支持 `DOCKER_RAMDISK` [moby/moby#35957](https://github.com/moby/moby/pull/35957)
- 更新 runc 以修复启动和执行期间的挂起问题 [moby/moby#36097](https://github.com/moby/moby/pull/36097)
- Windows：引入 Microsoft/hcsshim @v.0.6.8 以部分修复导入层失败的问题 [moby/moby#35924](https://github.com/moby/moby/pull/35924)
* 不将图形驱动的主目录设为私有挂载点 [moby/moby#36047](https://github.com/moby/moby/pull/36047)
* 为来自 daemon 根目录的挂载使用 rslave 传播方式 [moby/moby#36055](https://github.com/moby/moby/pull/36055)
* 设置 daemon 根目录使用共享挂载传播 [moby/moby#36096](https://github.com/moby/moby/pull/36096)
* 在容器启动时验证挂载路径是否存在，而不仅仅是在创建时 [moby/moby#35833](https://github.com/moby/moby/pull/35833)
* 在 TaskState 中添加 `REMOVE` 和 `ORPHANED` [moby/moby#36146](https://github.com/moby/moby/pull/36146)
- 修复 network inspect 在 swarm 作用域中不显示网络创建时间的问题 [moby/moby#36095](https://github.com/moby/moby/pull/36095)
* 在释放时清空容器的读写层 [moby/moby#36130](https://github.com/moby/moby/pull/36160) 和 [moby/moby#36343](https://github.com/moby/moby/pull/36242)

### Swarm
* 从 swarm 模式中移除 watchMiss [docker/libnetwork#2047](https://github.com/docker/libnetwork/pull/2047)

### 已知问题
* 健康检查不再使用容器的工作目录 [moby/moby#35843](https://github.com/moby/moby/issues/35843)
* stack deploy 配置中未从客户端返回错误 [moby/moby#757](https://github.com/docker/cli/pull/757)
* 使用 systemd 选项时，Docker 无法使用内存限制 [moby/moby#35123](https://github.com/moby/moby/issues/35123)

## 17.12.0-ce
2017-12-27

### 已知问题
* AWS 日志批处理大小计算 [moby/moby#35726](https://github.com/moby/moby/pull/35726)
* 健康检查不再使用容器的工作目录 [moby/moby#35843](https://github.com/moby/moby/issues/35843)
* stack deploy 配置中未从客户端返回错误 [moby/moby#757](https://github.com/docker/cli/pull/757)
* 项目配额失败时 Daemon 异常终止 [moby/moby#35827](https://github.com/moby/moby/pull/35827)
* 使用 systemd 选项时，Docker 无法使用内存限制 [moby/moby#35123](https://github.com/moby/moby/issues/35123)

### Builder

- 修复损坏符号链接的构建缓存哈希 [moby/moby#34271](https://github.com/moby/moby/pull/34271)
- 修复长流同步问题 [moby/moby#35404](https://github.com/moby/moby/pull/35404)
- 修复 Dockerfile 解析器在处理长令牌时静默失败的问题 [moby/moby#35429](https://github.com/moby/moby/pull/35429)

### Client

* 在 cli/compose 中移除 secret/config 的重复定义 [docker/cli#671](https://github.com/docker/cli/pull/671)
* 为 `docker trust sign` 添加 `--local` 标志 [docker/cli#575](https://github.com/docker/cli/pull/575)
* 添加 `docker trust inspect` [docker/cli#694](https://github.com/docker/cli/pull/694)
+ 为 secrets 和 configs 添加 `name` 字段，以允许在 Compose 文件中进行插值 [docker/cli#668](https://github.com/docker/cli/pull/668)
+ 添加 `--isolation` 用于设置 swarm 服务隔离模式 [docker/cli#426](https://github.com/docker/cli/pull/426)
* 移除已弃用的 "daemon" 子命令 [docker/cli#689](https://github.com/docker/cli/pull/689)
- 修复 `rmi -f` 在遇到意外错误时的行为 [docker/cli#654](https://github.com/docker/cli/pull/654)
* 在 service create 中集成通用资源 [docker/cli#429](https://github.com/docker/cli/pull/429)
- 修复 stack 中的外部网络问题 [docker/cli#743](https://github.com/docker/cli/pull/743)
* 移除通过镜像短 ID 引用镜像的支持 [docker/cli#753](https://github.com/docker/cli/pull/753) 和 [moby/moby#35790](https://github.com/moby/moby/pull/35790)
* 为 containerd 使用 commit-sha 而非 tag [moby/moby#35770](https://github.com/moby/moby/pull/35770)

### Documentation

* 更新 1.35 版本的 API 历史 [moby/moby#35724](https://github.com/moby/moby/pull/35724)

### Logging

* Logentries 驱动 line-only=true []byte 输出修复 [moby/moby#35612](https://github.com/moby/moby/pull/35612)
* Logentries line-only 日志选项修复，以保持向后兼容性 [moby/moby#35628](https://github.com/moby/moby/pull/35628)
+ 为 docker logs 添加 `--until` 标志 [moby/moby#32914](https://github.com/moby/moby/pull/32914)
+ 为 Windows 构建添加 gelf 日志驱动插件 [moby/moby#35073](https://github.com/moby/moby/pull/35073)
* 为 splunk 批量发送设置超时 [moby/moby#35496](https://github.com/moby/moby/pull/35496)
* 更新 Graylog2/go-gelf [moby/moby#35765](https://github.com/moby/moby/pull/35765)

### Networking

* 将负载均衡器沙箱的创建/删除移至 libnetwork [moby/moby#35422](https://github.com/moby/moby/pull/35422)
* 仅在容器元数据内更改网络文件的所有者 [moby/moby#34224](https://github.com/moby/moby/pull/34224)
* 在 FindNetwork 中恢复错误类型 [moby/moby#35634](https://github.com/moby/moby/pull/35634)
- 修复 NetworkConnect 的 consumes MIME 类型 [moby/moby#35542](https://github.com/moby/moby/pull/35542)
+ 添加对持久化 Windows 网络驱动特定选项的支持 [moby/moby#35563](https://github.com/moby/moby/pull/35563)
- 修复 netlink 套接字超时和 watchMiss 泄漏问题 [moby/moby#35677](https://github.com/moby/moby/pull/35677)
+ 用于网络诊断的新 daemon 配置 [moby/moby#35677](https://github.com/moby/moby/pull/35677)
- 清理节点管理逻辑 [docker/libnetwork#2036](https://github.com/docker/libnetwork/pull/2036)
- 在端点恢复时分配 VIP [docker/swarmkit#2474](https://github.com/docker/swarmkit/pull/2474)

### Runtime

* 更新至 containerd v1.0.0 [moby/moby#35707](https://github.com/moby/moby/pull/35707)
* 让 VFS 图形驱动使用加速的内核内拷贝 [moby/moby#35537](https://github.com/moby/moby/pull/35537)
* 为 docker exec 引入 `workingdir` 选项 [moby/moby#35661](https://github.com/moby/moby/pull/35661)
* Golang 升级至 1.9.2 [moby/moby#33892](https://github.com/moby/moby/pull/33892) [docker/cli#716](https://github.com/docker/cli/pull/716)
* 使用 `--readonly` 标志时，`/dev` 不应为只读 [moby/moby#35344](https://github.com/moby/moby/pull/35344)
+ 添加自定义构建时图形驱动优先级列表 [moby/moby#35522](https://github.com/moby/moby/pull/35522)
* LCOW：CLI 更改以添加平台标志 - pull、run、create 和 build [docker/cli#474](https://github.com/docker/cli/pull/474)
* 修复 Windows 上 `docker exec` 的宽度/高度问题 [moby/moby#35631](https://github.com/moby/moby/pull/35631)
* 在 4.0 之前的内核上检测 overlay2 支持 [moby/moby#35527](https://github.com/moby/moby/pull/35527)
* Devicemapper：卸载后移除容器 rootfs 挂载路径 [moby/moby#34573](https://github.com/moby/moby/pull/34573)
* 禁止在 NFS 上使用 overlay/overlay2 [moby/moby#35483](https://github.com/moby/moby/pull/35483)
- 修复 plugin set 期间潜在的 panic [moby/moby#35632](https://github.com/moby/moby/pull/35632)
- 修复容器锁定的一些问题 [moby/moby#35501](https://github.com/moby/moby/pull/35501)
- 修复插件引用计数的一些问题 [moby/moby#35265](https://github.com/moby/moby/pull/35265)
+ 在 ProcessEvent 中添加缺失的锁 [moby/moby#35516](https://github.com/moby/moby/pull/35516)
+ 添加 vfs 配额支持 [moby/moby#35231](https://github.com/moby/moby/pull/35231)
* 在检测先前的图形驱动时跳过空目录 [moby/moby#35528](https://github.com/moby/moby/pull/35528)
* 在用户命名空间中运行时跳过 xfs 配额测试 [moby/moby#35526](https://github.com/moby/moby/pull/35526)
+ 在配置选项中添加 SubSecondPrecision [moby/moby#35529](https://github.com/moby/moby/pull/35529)
* 更新 fsnotify 以修复移除监视时的死锁问题 [moby/moby#35453](https://github.com/moby/moby/pull/35453)
- 修复使用 `--tmpfs /dev/shm` 时出现 "duplicate mount point" 的问题 [moby/moby#35467](https://github.com/moby/moby/pull/35467)
- 修复用户 `/dev/shm` 挂载不遵守 tmpfs-size 的问题 [moby/moby#35316](https://github.com/moby/moby/pull/35316)
- 修复在 overlayfs 和 v4.13+ 内核下的 EBUSY 错误 [moby/moby#34948](https://github.com/moby/moby/pull/34948)
* Container：保护健康监视器通道 [moby/moby#35482](https://github.com/moby/moby/pull/35482)
* Container：使用互斥锁保护健康状态 [moby/moby#35517](https://github.com/moby/moby/pull/35517)
* Container：更新实时资源 [moby/moby#33731](https://github.com/moby/moby/pull/33731)
* 仅在远程存在卷时创建标签 [moby/moby#34896](https://github.com/moby/moby/pull/34896)
- 修复容器/exec 状态泄漏问题 [moby/moby#35484](https://github.com/moby/moby/pull/35484)
* 禁止使用旧版 (v1) 注册表 [moby/moby#35751](https://github.com/moby/moby/pull/35751) 和 [docker/cli#747](https://github.com/docker/cli/pull/747)
- Windows：修复针对构建器缓存的不区分大小写的文件名匹配问题 [moby/moby#35793](https://github.com/moby/moby/pull/35793)
- 修复进程处理和错误检查周围的竞态条件 [moby/moby#35809](https://github.com/moby/moby/pull/35809)
* 确保在 daemon 启动时停止容器 [moby/moby#35805](https://github.com/moby/moby/pull/35805)
* 遵循 containerd 命名空间约定 [moby/moby#35812](https://github.com/moby/moby/pull/35812)

### Swarm Mode

+ 添加对 swarm 服务隔离模式的支持 [moby/moby#34424](https://github.com/moby/moby/pull/34424)
- 修复已完成任务的清理问题 [docker/swarmkit#2477](https://github.com/docker/swarmkit/pull/2477)

### Packaging

+ 为 Fedora 27 添加打包支持 [docker/docker-ce-packaging#59](https://github.com/docker/docker-ce-packaging/pull/59)
* 更改默认版本控制方案为 0.0.0-dev，除非为打包指定 [docker/docker-ce-packaging#67](https://github.com/docker/docker-ce-packaging/pull/67)
* 将版本传递给引擎静态构建 [docker/docker-ce-packaging#70](https://github.com/docker/docker-ce-packaging/pull/70)
+ 添加对 Debian (stretch/jessie) 和 Ubuntu Zesty 或更高版本上的 aarch64 支持 [docker/docker-ce-packaging#35](https://github.com/docker/docker-ce-packaging/pull/35)
