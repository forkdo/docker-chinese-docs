# Docker Engine 17.10 发布说明

## 17.10.0-ce
2017-10-17

> [!IMPORTANT]: 从本版本开始，`docker service create`、`docker service update`、`docker service scale` 和 `docker service rollback` 默认使用非分离模式，使用 `--detach` 可保持旧行为。

### Builder

* 在上传的构建上下文中将 uid/gid 重置为 0，以便与其他客户端共享构建缓存 [docker/cli#513](https://github.com/docker/cli/pull/513)
+ 添加对无子路径的 `ADD` URL 的支持 [moby/moby#34217](https://github.com/moby/moby/pull/34217)

### Client

* 将 `docker stack rm` 的输出移至 stdout [docker/cli#491](https://github.com/docker/cli/pull/491)
* 在 cli 中对 secrets 和 configs 使用自然排序 [docker/cli#307](https://github.com/docker/cli/pull/307)
* 为 `docker service` 命令默认使用非分离模式 [docker/cli#525](https://github.com/docker/cli/pull/525)
* 即使在 Ping 失败时也在客户端设置 APIVersion [docker/cli#546](https://github.com/docker/cli/pull/546)
- 修复 `docker stack deploy` 中不同构建语法的加载器错误 [docker/cli#544](https://github.com/docker/cli/pull/544)
* 将 `docker container stats` 的默认输出格式更改为显示 `CONTAINER ID` 和 `NAME` [docker/cli#565](https://github.com/docker/cli/pull/565)
+ 为 `docker container stats` 添加 `--no-trunc` 标志 [docker/cli#565](https://github.com/docker/cli/pull/565)
+ 添加实验性的 `docker trust`：`view`、`revoke`、`sign` 子命令 [docker/cli#472](https://github.com/docker/cli/pull/472)
- 各种文档和 shell 补全修复 [docker/cli#610](https://github.com/docker/cli/pull/610) [docker/cli#611](https://github.com/docker/cli/pull/611) [docker/cli#618](https://github.com/docker/cli/pull/618) [docker/cli#580](https://github.com/docker/cli/pull/580) [docker/cli#598](https://github.com/docker/cli/pull/598) [docker/cli#603](https://github.com/docker/cli/pull/603)

### Networking

* 在 Windows 上使用每节点、每网络的 LB 端点启用 ILB/ELB [moby/moby#34674](https://github.com/moby/moby/pull/34674)
* 用于瞬态 IP 重用的 Overlay 修复 [docker/libnetwork#1935](https://github.com/docker/libnetwork/pull/1935)
* 序列化 bitseq 分配 [docker/libnetwork#1788](https://github.com/docker/libnetwork/pull/1788)
- 在链存在检查时禁用主机名查找 [docker/libnetwork#1974](https://github.com/docker/libnetwork/pull/1974)

### Runtime

* LCOW：在拆卸前获取日志以增强 UVM 可调试性 [moby/moby#34846](https://github.com/moby/moby/pull/34846)
* LCOW：为绑定挂载做准备 [moby/moby#34258](https://github.com/moby/moby/pull/34258)
* LCOW：支持 docker cp、构建中的 ADD/COPY [moby/moby#34252](https://github.com/moby/moby/pull/34252)
* LCOW：VHDX 启动为只读 [moby/moby#34754](https://github.com/moby/moby/pull/34754)
* Volume：在重新标记挂载源之前评估符号链接 [moby/moby#34792](https://github.com/moby/moby/pull/34792)
- 修复 'docker cp' 以允许在主机符号链接目录中使用新的目标文件名 [moby/moby#31993](https://github.com/moby/moby/pull/31993)
+ 添加对拉取时 Windows 版本过滤的支持 [moby/moby#35090](https://github.com/moby/moby/pull/35090)

### Swarm mode

* 如果在工作节点上执行 `docker swarm init --force-new-cluster` 则产生错误 [moby/moby#34881](https://github.com/moby/moby/pull/34881)
+ 添加对 swarm 服务中 `.Node.Hostname` 模板化的支持 [moby/moby#34686](https://github.com/moby/moby/pull/34686)
* 将发送快照的 gRPC 请求超时增加到 20 秒 [docker/swarmkit#2391](https://github.com/docker/swarmkit/pull/2391)
- 如果日志驱动设置为 `none` 则不过滤节点 [docker/swarmkit#2396](https://github.com/docker/swarmkit/pull/2396)
+ 向 ipam 驱动程序请求添加 ipam 选项 [docker/swarmkit#2324](https://github.com/docker/swarmkit/pull/2324)
