# Docker Engine 19.03 发行说明

## 19.03.15
2021-02-01

### 安全

* [CVE-2021-21285](https://github.com/moby/moby/security/advisories/GHSA-6fj5-m822-rqx8) 防止无效镜像导致 Docker 守护进程崩溃
* [CVE-2021-21284](https://github.com/moby/moby/security/advisories/GHSA-7452-xqpj-6rpc) 锁定文件权限，防止重新映射的 root 用户访问 Docker 状态
* 确保在使用 BuildKit 构建时应用 AppArmor 和 SELinux 配置文件

### 客户端

* 在导入上下文之前检查上下文，以降低提取文件逃逸上下文存储的风险

## 19.03.14
2020-12-01

### 安全

- [CVE-2020-15257](http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2020-15257):
  将捆绑的 containerd 静态二进制文件更新至 v1.3.9 [moby/moby#41731](https://github.com/moby/moby/pull/41731)。
  包管理器应更新 containerd.io 包。

### 构建器

- 现在可以正确解析 AppArmor 的测试版，防止构建失败 [moby/moby#41542](https://github.com/moby/moby/pull/41542)

### 网络

- 修复 swarmkit 服务持续启动失败时的 panic 问题 [moby/moby#41635](https://github.com/moby/moby/pull/41635)

### 运行时

- 返回正确的错误，而不是虚假的 -EINVAL [moby/moby#41293](https://github.com/moby/moby/pull/41293)

### 无根模式

- 锁定状态目录以防止 systemd-tmpfiles 自动清理 [moby/moby#41635](https://github.com/moby/moby/pull/41635)
- dockerd-rootless.sh: 支持新的 containerd shim 套接字路径约定 [moby/moby#41557](https://github.com/moby/moby/pull/41557)

### 日志

- gcplogs: 修复内存/连接泄漏 [moby/moby#41522](https://github.com/moby/moby/pull/41522)
- awslogs: 支持 AWS imdsv2 [moby/moby#41494](https://github.com/moby/moby/pull/41494)

## 19.03.13
2020-09-16

### 构建器

- buildkit: 修复缓存逻辑中的空指针解引用 [moby/moby#41279](https://github.com/moby/moby/pull/41279)
- buildkit: 在 COPY/ADD 期间将 Unix 套接字视为常规文件 [moby/moby#41269](https://github.com/moby/moby/pull/41269)
- buildkit: 在计算中忽略系统和安全扩展属性，以确保在 SELinux 环境中 COPY 缓存的一致性 [moby/moby#41222](https://github.com/moby/moby/pull/41222)
- buildkit: 使 `--cache-from` 行为更可靠 [moby/moby#41222](https://github.com/moby/moby/pull/41222)
- buildkit: 修复导出缓存时的无限循环导致 CPU 占用过高 [moby/moby#41185](https://github.com/moby/moby/pull/41185)

### 客户端

- 升级 Golang 至 1.13.15 [docker/cli#2674](https://github.com/docker/cli/pull/2674)
- 修复配置文件权限问题 (~/.docker/config.json) [docker/cli#2631](https://github.com/docker/cli/pull/2631)
- build: 修复在高度为零的终端上发生 panic 的问题 [docker/cli#2719](https://github.com/docker/cli/pull/2719)
- windows: 修复控制台中换行符的潜在问题 [docker/cli#2623](https://github.com/docker/cli/pull/2623)

### 网络

- 在失败时清理网络沙箱 [moby/moby#41081](https://github.com/moby/moby/pull/41081)
- 通过将截止时间相关错误转发给用户来修复浅层错误消息 [moby/moby#41312](https://github.com/moby/moby/pull/41312)
- 修复 netns 文件描述符泄漏 [moby/moby#41287](https://github.com/moby/moby/41287)

### 无根模式

- 修复端口转发器资源泄漏 [moby/moby#41277](https://github.com/moby/moby/pull/41277)

### 运行时

- 升级 Golang 至 1.13.15 [moby/moby#41334](https://github.com/moby/moby/pull/41334)
- 更新 containerd 至 1.3.7 [moby/moby#40408](https://github.com/moby/moby/pull/40408)

### Windows

- 修复使用 servercore 镜像时 Windows 容器启动缓慢的问题 [moby/moby#41192](https://github.com/moby/moby/pull/41192)

## 19.03.12
2020-06-18

### 客户端

- 修复在使用多个配置文件时（例如在 Docker Desktop 中使用 Windows 和 WSL2）无法从注册表注销的错误 [docker/cli#2592](https://github.com/docker/cli/pull/2592)
- 修复阻止读取上下文元数据的回归问题 [docker/cli#2586](https://github.com/docker/cli/pull/2586)
- 升级 Golang 至 1.13.12 [docker/cli#2575](https://github.com/docker/cli/pull/2575)

### 网络

- 修复在 systemd-nspawn 环境中守护进程无法启动的回归问题 [moby/moby#41124](https://github.com/moby/moby/pull/41124) [moby/libnetwork#2567](https://github.com/moby/libnetwork/pull/2567)
- 修复在 swarm 中创建覆盖网络的重试逻辑 [moby/moby#41124](https://github.com/moby/moby/pull/41124) [moby/libnetwork#2565](https://github.com/moby/libnetwork/pull/2565)

### 运行时

- 升级 Golang 至 1.13.12 [moby/moby#41082](https://github.com/moby/moby/pull/41082)

## 19.03.11
2020-06-01

### 网络

禁用 IPv6 路由通告以防止地址欺骗。 [CVE-2020-13401](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2020-13401)

**描述**

在 Docker 默认配置中，容器网络接口是连接到主机的虚拟以太网链路（veth 接口）。
在此配置中，能够在容器中以 root 身份运行进程的攻击者可以使用 `CAP_NET_RAW` 功能（在默认配置中存在）向主机发送和接收任意数据包。

如果主机上没有完全禁用 IPv6（通过内核命令行中的 `ipv6.disable=1`），它将未配置或在某些接口上配置，但很可能 IPv6 转发被禁用，即 `/proc/sys/net/ipv6/conf//forwarding == 0`。同样默认情况下，`/proc/sys/net/ipv6/conf//accept_ra == 1`。这两个 sysctl 的组合意味着主机接受路由器通告并使用它们配置 IPv6 堆栈。

通过从容器发送“恶意”路由器通告，攻击者可以重新配置主机以将主机的部分或全部 IPv6 流量重定向到攻击者控制的容器。

即使之前没有 IPv6 流量，如果 DNS 返回 A（IPv4）和 AAAA（IPv6）记录，许多 HTTP 库将首先尝试通过 IPv6 连接，然后回退到 IPv4，这为攻击者提供了响应的机会。
如果主机碰巧存在漏洞，例如去年 apt 中的 RCE（CVE-2019-3462），攻击者现在可以升级到主机。

由于 `CAP_NET_ADMIN` 默认情况下不存在于 Docker 容器中，攻击者无法配置他们想要进行中间人攻击的 IP，他们无法使用 iptables 进行 NAT 或重定向流量，也无法使用 `IP_TRANSPARENT`。
然而，攻击者仍然可以使用 `CAP_NET_RAW` 并在用户空间中实现 tcp/ip 堆栈。

参见 [kubernetes/kubernetes#91507](https://github.com/kubernetes/kubernetes/issues/91507) 了解相关问题。

## 19.03.10
2020-05-29

### 客户端
- 修复与旧版引擎的版本协商问题。 [docker/cli#2538](https://github.com/docker/cli/pull/2538)
- 避免通过主机名设置 SSH 标志。 [docker/cli#2560](https://github.com/docker/cli/pull/2560)
- 修复 DOCKER_CLI_EXPERIMENTAL 无效时发生 panic 的问题。 [docker/cli#2558](https://github.com/docker/cli/pull/2558)
- 通过将 Go 升级到 1.13.11，避免在 s390x 上发生潜在的 panic。 [docker/cli#2532](https://github.com/docker/cli/pull/2532)

### 网络
- 修复 DNS 回退回归问题。 [moby/moby#41009](https://github.com/moby/moby/pull/41009)

### 运行时
- 通过将 Go 升级到 1.13.11，避免在 s390x 上发生潜在的 panic。 [moby/moby#40978](https://github.com/moby/moby/pull/40978)

### 打包
- 修复在 ARM64 上的 ARM 构建问题。 [moby/moby#41027](https://github.com/moby/moby/pull/41027)

## 19.03.9
2020-05-14

### 构建器
- buildkit: 修复并行构建多个镜像时的并发映写 panic 问题。 [moby/moby#40780](https://github.com/moby/moby/pull/40780)
- buildkit: 修复在使用 userns 时无法在阶段之间更改非 root 拥有文件所有权的问题。 [moby/moby#40955](https://github.com/moby/moby/pull/40955)
- 避免在 Windows 上创建无关的临时文件。 [moby/moby#40877](https://github.com/moby/moby/pull/40877)

### 客户端
- 修复单字符卷上的 panic 问题。 [docker/cli#2471](https://github.com/docker/cli/pull/2471)
- 懒惰检测守护进程功能，以避免简单命令的长时间超时。 [docker/cli#2442](https://github.com/docker/cli/pull/2442)
- Windows 上的 `docker context inspect` 现在更快。 [docker/cli#2516](https://github.com/docker/cli/pull/2516)
- 升级 Golang 至 1.13.10。 [docker/cli#2431](https://github.com/docker/cli/pull/2431)
- 升级 gopkg.in/yaml.v2 至 v2.2.8。 [docker/cli#2470](https://github.com/docker/cli/pull/2470)

### 日志
- 避免因关闭已关闭的日志文件而导致容器日志无法轮转的情况。 [moby/moby#40921](https://github.com/moby/moby/pull/40921)

### 网络
- 修复重启时潜在的 panic 问题。 [moby/moby#40809](https://github.com/moby/moby/pull/40809)
- 为默认桥接子网字段分配正确的网络值。 [moby/moby#40565](https://github.com/moby/moby/pull/40565)

### 运行时
- 修复在 /etc/subuid 和 /etc/subgid 中使用 UID 创建命名空间时 Docker 崩溃的问题。 [moby/moby#40562](https://github.com/moby/moby/pull/40562)
- 改进 ARM 平台匹配。 [moby/moby#40758](https://github.com/moby/moby/pull/40758)
- overlay2: 显示后端文件系统。 [moby/moby#40652](https://github.com/moby/moby/pull/40652)
- 更新 CRIU 至 v3.13 "Silicon Willet"。 [moby/moby#40850](https://github.com/moby/moby/pull/40850)
- 仅在成功回退时显示注册表 v2 schema1 弃用警告，而不是针对任何注册表错误。 [moby/moby#40681](https://github.com/moby/moby/pull/40681)
- 在 Windows 上为日志文件使用 FILE_SHARE_DELETE。 [moby/moby#40563](https://github.com/moby/moby/pull/40563)
- 升级 Golang 至 1.13.10。 [moby/moby#40803](https://github.com/moby/moby/pull/40803)

### 无根模式
- 现在 rootlesskit-docker-proxy 在暴露特权端口时返回详细的错误消息。 [moby/moby#40863](https://github.com/moby/moby/pull/40863)
- 支持 /etc/subuid 和 /etc/subgid 中的数字 ID。 [moby/moby#40951](https://github.com/moby/moby/pull/40951)

### 安全
- apparmor: 为 userns 添加缺失的规则。 [moby/moby#40564](https://github.com/moby/moby/pull/40564)
- SElinux: 修复重新标记时未检测到 ENOTSUP 错误的问题。 [moby/moby#40946](https://github.com/moby/moby/pull/40946)

### Swarm
- 增加记录器的补充速率，以避免在服务日志上挂起。 [moby/moby#40628](https://github.com/moby/moby/pull/40628)
- 修复单个 swarm 管理器在重启后卡在 Down 状态的问题。 [moby/moby#40831](https://github.com/moby/moby/pull/40831)
- tasks.db 不再无限增长。 [moby/moby#40831](https://github.com/moby/moby/pull/40831)

## 19.03.8
2020-03-10

### 运行时

- 改进对 [CVE-2019-14271](https://nvd.nist.gov/vuln/detail/CVE-2019-14271) 的缓解措施，适用于某些 nscd 配置。

## 19.03.7
2020-03-03

### 构建器

- builder-next: 修复边缘情况下的死锁问题。 [moby/moby#40557](https://github.com/moby/moby/pull/40557)

### 运行时

* overlay: 移除 modprobe execs。 [moby/moby#40462](https://github.com/moby/moby/pull/40462)
* selinux: 在设置文件标签时显示更好的错误消息。 [moby/moby#40547](https://github.com/moby/moby/pull/40547)
* 加快初始统计信息收集速度。 [moby/moby#40549](https://github.com/moby/moby/pull/40549)
- rootless: 使用来自 XDG_CONFIG_HOME 的 certs.d。 [moby/moby#40461](https://github.com/moby/moby/pull/40461)
- 升级 Golang 至 1.12.17。 [moby/moby#40533](https://github.com/moby/moby/pull/40533)
- 升级 google.golang.org/grpc 至 v1.23.1。 [moby/moby#40566](https://github.com/moby/moby/pull/40566)
- 更新 containerd 二进制文件至 v1.2.13。 [moby/moby#40540](https://github.com/moby/moby/pull/40540)
- 防止在边缘情况下将已停止的容器显示为正在运行。 [moby/moby#40555](https://github.com/moby/moby/pull/40555)
- 防止潜在的锁。 [moby/moby#40604](https://github.com/moby/moby/pull/40604)

### 客户端

- 升级 Golang 至 1.12.17。 [docker/cli#2342](https://github.com/docker/cli/pull/2342)
- 升级 google.golang.org/grpc 至 v1.23.1。 [docker/cli#1884](https://github.com/docker/cli/pull/1884) [docker/cli#2373](https://github.com/docker/cli/pull/2373)

## 19.03.6
2020-02-12

### 构建器

- builder-next: 允许用于 SSH 转发的现代签名哈希。 [docker/engine#453](https://github.com/docker/engine/pull/453)
- builder-next: 触发后清除 onbuild 规则。 [docker/engine#453](https://github.com/docker/engine/pull/453)
- builder-next: 修复启用用户名称空间时的目录权限问题。 [moby/moby#40440](https://github.com/moby/moby/pull/40440)
- 升级 hcsshim 以修复在 Windows 1903 上 docker build 失败的问题。 [docker/engine#429](https://github.com/docker/engine/pull/429)

### 网络

- 缩短 exec-root 中的控制器 ID 以避免达到 UNIX_PATH_MAX。 [docker/engine#424](https://github.com/docker/engine/pull/424)
- 修复 drivers/overlay/encryption.go 中的 panic 问题。 [docker/engine#424](https://github.com/docker/engine/pull/424)
- 修复 hwaddr 设置与 udev 之间的竞争条件。 [docker/engine#439](https://github.com/docker/engine/pull/439)

### 运行时

* 升级 Golang 至 1.12.16。 [moby/moby#40433](https://github.com/moby/moby/pull/40433)
* 更新 containerd 二进制文件至 v1.2.12。 [moby/moby#40433](https://github.com/moby/moby/pull/40453)
* 更新至 runc v1.0.0-rc10。 [moby/moby#40433](https://github.com/moby/moby/pull/40453)
- 修复 Lgetxattr 中可能的运行时 panic。 [docker/engine#454](https://github.com/docker/engine/pull/454)
- rootless: 修复代理 UDP 数据包的问题。 [docker/engine#434](https://github.com/docker/engine/pull/434)

## 19.03.5
2019-11-14

### 构建器

* builder-next: 在构建器配置中添加了 `entitlements`。 [docker/engine#412](https://github.com/docker/engine/pull/412)
* 修复 builder-next: 在使用 userns-remap 时使用构建秘密或 SSH 转发的权限错误。 [docker/engine#420](https://github.com/docker/engine/pull/420)
* 修复 builder-next: 在已复制的目录内复制符号链接。 [docker/engine#420](https://github.com/docker/engine/pull/420)

### 打包

* 支持 RHEL 8 软件包

### 运行时

* 升级 Golang 至 1.12.12。 [docker/engine#418](https://github.com/docker/engine/pull/418)
* 更新 RootlessKit 至 v0.7.0，以通过挂载命名空间和 seccomp 来加固 slirp4netns。 [docker/engine#397](https://github.com/docker/engine/pull/397)
* 修复从事件处理器传播 GetContainer 错误的问题。 [docker/engine#407](https://github.com/docker/engine/pull/407)
* 修复 OCI 镜像的推送问题。 [docker/engine#405](https://github.com/docker/engine/pull/405)

## 19.03.4
2019-10-17

### 网络

* 回滚 libnetwork 更改以修复 `DOCKER-USER` iptables 链问题。 [docker/engine#404](https://github.com/docker/engine/pull/404)

### 已知问题

#### 现有

* 在某些大型集群情况下，Docker 信息可能会在 Swarm 部分包含错误 `code = ResourceExhausted desc = grpc: received message larger than max (5351376 vs. 4194304)`。这并不表示用户有任何失败或配置错误，无需响应。
* 当重新部署所有服务为新服务时，可能会发生编排器端口冲突。由于短时间内收到大量 Swarm 管理器请求，某些服务在部署后无法接收流量并导致 `404` 错误。
     - **解决方法：** 通过 `docker service update --force` 重启所有任务。
* [CVE-2018-15664](https://nvd.nist.gov/vuln/detail/CVE-2018-15664) 符号链接交换攻击伴随目录遍历。在即将发布的补丁版本中提供适当修复之前的解决方法：在执行文件操作之前 `docker pause` 容器。 [moby/moby#39252](https://github.com/moby/moby/pull/39252)
* 由于 CVE 缓解措施导致的 `docker cp` 回归。当 `docker cp` 的源设置为 `/` 时会产生错误。

## 19.03.3
2019-10-08

### 安全

* 修补了 containerd 中的 `runc`。 [CVE-2017-18367](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-18367)

### 构建器

* 修复 builder-next: 解析第三方注册表的摘要。 [docker/engine#339](https://github.com/docker/engine/pull/339)

* 修复 builder-next: 当守护进程通过套接字激活启动时的用户命名空间构建。 [docker/engine#373](https://github.com/docker/engine/pull/373)

* 修复 builder-next; session: 每个连接释放转发的 SSH 套接字连接。 [docker/engine#373](https://github.com/docker/engine/pull/373)

* 修复 build-next: llbsolver: 多个缓存导入器的错误。 [docker/engine#373](https://github.com/docker/engine/pull/373)

### 客户端

* 添加了对 Docker Template 0.1.6 的支持。

* 减轻具有过多别名的 YAML 文件的影响。 [docker/cli#2119](https://github.com/docker/cli/pull/2119)

### 运行时

* 升级 Golang 至 1.12.10。 [docker/engine#387](https://github.com/docker/engine/pull/387)

* 升级 containerd 至 1.2.10。 [docker/engine#385](https://github.com/docker/engine/pull/385)

* 分发：修改拉取 v2 schema1 清单时的警告逻辑。 [docker/engine#368](https://github.com/docker/engine/pull/368)

* 修复在提供不正确的平台选项时 `POST /images/create` 返回 500 状态码的问题。 [docker/engine#365](https://github.com/docker/engine/pull/365)

* 修复在提供不正确的平台选项时 `POST /build` 返回 500 状态码的问题。 [docker/engine#365](https://github.com/docker/engine/pull/365)

* 修复在 32 位 ARMv7 上由结构体成员未对齐引起的 panic。 [docker/engine#363](https://github.com/docker/engine/pull/363)

* 修复在链接到不存在的容器时返回“无效参数”的问题。 [docker/engine#352](https://github.com/docker/engine/pull/352)

* 修复 overlay2: 在使用内核 >= 5.2 时挂载时出现 busy 错误的问题。 [docker/engine#332](https://github.com/docker/engine/pull/332)

* 修复 `docker rmi` 在某些配置错误的系统（例如死 NFS 共享）中卡住的问题。 [docker/engine#335](https://github.com/docker/engine/pull/335)

* 修复 exec 进程的阻塞 I/O 处理。 [docker/engine#296](https://github.com/docker/engine/pull/296)

* 修复 jsonfile 记录器：当设置了 `max-size` 且 `max-file=1` 时，日志跟随卡住的问题。 [docker/engine#378](https://github.com/docker/engine/pull/378)

### 已知问题

#### 新增

* `DOCKER-USER` iptables 链缺失：[docker/for-linux#810](https://github.com/docker/for-linux/issues/810)。
  用户无法在此 iptables 链之上执行额外的容器网络流量过滤。如果您没有在 `DOCKER-USER` 之上自定义 iptable 链，则不受此问题影响。
     - **解决方法：** 在 docker 守护进程启动后插入 iptables 链。
       例如：
       ```
       iptables -N DOCKER-USER
       iptables -I FORWARD -j DOCKER-USER
       iptables -A DOCKER-USER -j RETURN
       ```

#### 现有

* 在某些大型集群情况下，Docker 信息可能会在 Swarm 部分包含错误 `code = ResourceExhausted desc = grpc: received message larger than max (5351376 vs. 4194304)`。这并不表示用户有任何失败或配置错误，无需响应。
* 当重新部署所有服务为新服务时，可能会发生编排器端口冲突。由于短时间内收到大量 Swarm 管理器请求，某些服务在部署后无法接收流量并导致 `404` 错误。
     - **解决方法：** 通过 `docker service update --force` 重启所有任务。
* [CVE-2018-15664](https://nvd.nist.gov/vuln/detail/CVE-2018-15664) 符号链接交换攻击伴随目录遍历。在即将发布的补丁版本中提供适当修复之前的解决方法：在执行文件操作之前 `docker pause` 容器。 [moby/moby#39252](https://github.com/moby/moby/pull/39252)
* 由于 CVE 缓解措施导致的 `docker cp` 回归。当 `docker cp` 的源设置为 `/` 时会产生错误。

## 19.03.2
2019-09-03

### 构建器

* 修复在 Windows 上 `COPY --from` 到不存在目录的问题。 [moby/moby#39695](https://github.com/moby/moby/pull/39695)

* 修复 builder-next: 元数据命令在历史记录中没有创建时间的问题。 [moby/moby#39456](https://github.com/moby/moby/issues/39456)

* 修复 builder-next: 在层导出错误时关闭进度。 [moby/moby#39782](https://github.com/moby/moby/pull/39782)

* 更新 buildkit 至 588c73e1e4。 [moby/moby#39781](https://github.com/moby/moby/pull/39781)

### 客户端

* 修复在非 Windows 系统上检测 Windows 绝对路径的问题 [docker/cli#1990](https://github.com/docker/cli/pull/1990)

* 修复 `docker login --username` 的 zsh 补全脚本。

* 修复上下文：在 `context create` 上产生一致的输出。 [docker/cli#1985](https://github.com/docker/cli/pull/1874)

* 修复对 HTTP 代理环境变量的支持。 [docker/cli#2059](https://github.com/docker/cli/pull/2059)

### 日志

* 修复读取 journald 日志的问题。 [moby/moby#37819](https://github.com/moby/moby/pull/37819) [moby/moby#38859](https://github.com/moby/moby/pull/38859)

### 网络

* 防止在连接到禁用网络的容器的网络上发生 panic。 [moby/moby#39589](https://github.com/moby/moby/pull/39589)

### 运行时

* 升级 Golang 至 1.12.8。

* 修复在为容器使用 XFS 磁盘配额时引擎可能发生的 panic。 [moby/moby#39644](https://github.com/moby/moby/pull/39644)

### Swarm

* 修复具有多个任务的节点无法被移除的问题。 [docker/swarmkit#2867](https://github.com/docker/swarmkit/pull/2867)

### 已知问题

* 在某些大型集群情况下，Docker 信息可能会在 Swarm 部分包含错误 `code = ResourceExhausted desc = grpc: received message larger than max (5351376 vs. 4194304)`。这并不表示用户有任何失败或配置错误，无需响应。
* 当重新部署所有服务为新服务时，可能会发生编排器端口冲突。由于短时间内收到大量 Swarm 管理器请求，某些服务在部署后无法接收流量并导致 `404` 错误。
     - 解决方法：通过 `docker service update --force` 重启所有任务。

* 由于 FORWARD 链中缺少 Iptables 规则，流量无法从主机流出
  缺失的规则是：
     ```
     /sbin/iptables --wait -C FORWARD -o docker_gwbridge -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
     /sbin/iptables --wait -C FORWARD -o docker0 -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
     ```
     - 解决方法：使用脚本和 cron 定义将这些规则添加回来。脚本必须包含 '-C' 命令以检查规则是否存在，以及 '-A' 命令以将规则添加回来。在 cron 上定期运行该脚本，例如每 <x> 分钟。
     - 受影响的版本：18.09.1, 19.03.0
* [CVE-2018-15664](https://nvd.nist.gov/vuln/detail/CVE-2018-15664) 符号链接交换攻击伴随目录遍历。在即将发布的补丁版本中提供适当修复之前的解决方法：在执行文件操作之前 `docker pause` 容器。 [moby/moby#39252](https://github.com/moby/moby/pull/39252)
* 由于 CVE 缓解措施导致的 `docker cp` 回归。当 `docker cp` 的源设置为 `/` 时会产生错误。

## 19.03.1
2019-07-25

### 安全

 * 修复了在 Glibc 下 chroot 内加载基于 nsswitch 的配置的问题。 [CVE-2019-14271](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2019-14271)

### 已知问题

 * 在某些情况下，在大型集群中，Docker 信息可能会在 Swarm 部分包含错误 `code = ResourceExhausted desc = grpc: received message larger than max (5351376 vs. 4194304
