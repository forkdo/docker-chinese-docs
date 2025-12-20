# Docker Engine 18.01 发布说明

## 18.01.0-ce
2018-01-10

### 构建器

* 修复启用用户命名空间时文件未被删除的问题 [moby/moby#35822](https://github.com/moby/moby/pull/35822)
- 增加对 `docker commit --change ...` 中展开环境变量的支持 [moby/moby#35582](https://github.com/moby/moby/pull/35582)

### 客户端

* 在堆栈部署配置中返回客户端错误 [docker/cli#757](https://github.com/docker/cli/pull/757)
- 修复清理命令中过滤器标志的描述 [docker/cli#774](https://github.com/docker/cli/pull/774)
+ 将 "pid" 添加到不支持的选项列表 [docker/cli#768](https://github.com/docker/cli/pull/768)
+ 增加对实验性 Cli 配置的支持 [docker/cli#758](https://github.com/docker/cli/pull/758)
+ 增加对 bash 补全中泛用资源的支持 [docker/cli#749](https://github.com/docker/cli/pull/749)
- 修复 zsh 补全脚本中 docker exec 的错误 [docker/cli#751](https://github.com/docker/cli/pull/751)
+ 在客户端关闭 websocket 附加连接时添加调试消息 [moby/moby#35720](https://github.com/moby/moby/pull/35720)
- 修复 `"docker swarm"` 的 bash 补全 [docker/cli#772](https://github.com/docker/cli/pull/772)


### 文档
* 纠正文档中对 `--publish` 长格式的引用 [docker/cli#746](https://github.com/docker/cli/pull/746)
* 纠正 MAC_ADMIN 和 MAC_OVERRIDE 的描述 [docker/cli#761](https://github.com/docker/cli/pull/761)
* 更新开发者文档以解释外部 CLI [moby/moby#35681](https://github.com/moby/moby/pull/35681)
- 修复 `"on-failure"` 重启策略被记录为 "failure" 的问题 [docker/cli#754](https://github.com/docker/cli/pull/754)
- 修复 "存储驱动选项" 的锚点链接 [docker/cli#748](https://github.com/docker/cli/pull/748)

### 实验性功能

+ 在 `docker stack` 命令中增加对 kubernetes 的支持 [docker/cli#721](https://github.com/docker/cli/pull/721)
* 不再将容器 id 附加到自定义目录检查点 [moby/moby#35694](https://github.com/moby/moby/pull/35694)

### 日志

* 修复当 GELF 服务器关闭时，使用 TCP 上的 GELF 日志驱动时守护进程崩溃的问题 [moby/moby#35765](https://github.com/moby/moby/pull/35765)
- 修复 awslogs 对大型日志的批处理大小计算 [moby/moby#35726](https://github.com/moby/moby/pull/35726)

### 网络

- Windows：修复允许 docker 服务在 Windows VM 上启动 [docker/libnetwork#1916](https://github.com/docker/libnetwork/pull/1916)
- 修复 docker 在 ICS 网络上拦截 DNS 请求的问题 [docker/libnetwork#2014](https://github.com/docker/libnetwork/pull/2014)
+ Windows：添加新的网络创建驱动选项 [docker/libnetwork#2021](https://github.com/docker/libnetwork/pull/2021)


### 运行时

* 验证容器启动时的挂载规范以防止主机路径缺失 [moby/moby#35833](https://github.com/moby/moby/pull/35833)
- 修复用户命名空间内的 overlay2 存储驱动 [moby/moby#35794](https://github.com/moby/moby/pull/35794)
* Zfs：修复容器停止时的忙碌错误 [moby/moby#35674](https://github.com/moby/moby/pull/35674)
- 修复健康检查未使用容器工作目录的问题 [moby/moby#35845](https://github.com/moby/moby/pull/35845)
- 修复 VFS 图驱动因设置文件系统配额失败而无法初始化的问题 [moby/moby#35827](https://github.com/moby/moby/pull/35827)
- 修复 containerd 事件被处理两次的问题 [moby/moby#35896](https://github.com/moby/moby/pull/35896)

### Swarm 模式

- 修复如果服务具有相同数量的主机模式发布的端口且 Published Port 为 0 时，发布的端口未更新的问题 [docker/swarmkit#2376](https://github.com/docker/swarmkit/pull/2376)
* 使任务终止顺序确定化 [docker/swarmkit#2265](https://github.com/docker/swarmkit/pull/2265)
