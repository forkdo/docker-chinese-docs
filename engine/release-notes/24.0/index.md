# Docker Engine 24.0 发行说明

本页面描述了 Docker Engine 24.0 版本的最新变更、新增功能、已知问题和修复。

有关以下内容的更多信息：

- 已弃用和已移除的功能，请参阅 [已弃用的 Engine 功能](../deprecated.md)。
- Engine API 的变更，请参阅 [Engine API 版本历史](/reference/api/engine/version-history/)。

## 24.0.9

<em class="text-gray-400 italic dark:text-gray-500">2024-01-31</em>


有关此版本中拉取请求和变更的完整列表，请参阅相关的 GitHub 里程碑：

- [docker/cli, 24.0.9 里程碑](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A24.0.9)
- [moby/moby, 24.0.9 里程碑](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A24.0.9)

## 安全

此版本包含针对以下影响 Docker Engine 及其组件的 CVE 的安全修复。

| CVE                                                         | 组件            | 修复版本 | 严重性             |
| ----------------------------------------------------------- | -------------- | -------- | ---------------- |
| [CVE-2024-21626](https://scout.docker.com/v/CVE-2024-21626) | runc           | 1.1.12   | 高, CVSS 8.6      |
| [CVE-2024-24557](https://scout.docker.com/v/CVE-2024-24557) | Docker Engine  | 24.0.9   | 中, CVSS 6.9      |

> [!IMPORTANT]
>
> 请注意，此版本的 Docker Engine 不包含针对以下 BuildKit 中已知漏洞的修复：
>
> - [CVE-2024-23651](https://scout.docker.com/v/CVE-2024-23651)
> - [CVE-2024-23652](https://scout.docker.com/v/CVE-2024-23652)
> - [CVE-2024-23653](https://scout.docker.com/v/CVE-2024-23653)
> - [CVE-2024-23650](https://scout.docker.com/v/CVE-2024-23650)
>
> 要解决这些漏洞，请升级到 [Docker Engine v25.0.2](./25.0.md#2502)。

有关此版本中已解决的安全问题以及 BuildKit 中未解决的漏洞的更多信息，请参阅 [博客文章](https://www.docker.com/blog/docker-security-advisory-multiple-vulnerabilities-in-runc-buildkit-and-moby/)。

有关每个漏洞的详细信息，请参阅相关的安全公告：

- [CVE-2024-21626](https://github.com/opencontainers/runc/security/advisories/GHSA-xr7r-f8xq-vfvv)
- [CVE-2024-24557](https://github.com/moby/moby/security/advisories/GHSA-xw73-rw38-6vjc)

### 打包更新

- 将 runc 升级到 [v1.1.12](https://github.com/opencontainers/runc/releases/tag/v1.1.12)。 [moby/moby#47269](https://github.com/moby/moby/pull/47269)
- 将 containerd 升级到 [v1.7.13](https://github.com/containerd/containerd/releases/tag/v1.7.13)（仅限静态二进制文件）。 [moby/moby#47280](https://github.com/moby/moby/pull/47280)

## 24.0.8

<em class="text-gray-400 italic dark:text-gray-500">2024-01-25</em>


有关此版本中拉取请求和变更的完整列表，请参阅相关的 GitHub 里程碑：

- [docker/cli, 24.0.8 里程碑](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A24.0.8)
- [moby/moby, 24.0.8 里程碑](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A24.0.8)

### 错误修复和增强功能
* 实时恢复：具有自动移除功能的容器（`docker run --rm`）在引擎重启时不再被强制移除。 [moby/moby#46857](https://github.com/moby/moby/pull/46869)

### 打包更新
* 将 Go 升级到 `go1.20.13`。 [moby/moby#47054](https://github.com/moby/moby/pull/47054), [docker/cli#4826](https://github.com/docker/cli/pull/4826), [docker/docker-ce-packaging#975](https://github.com/docker/docker-ce-packaging/pull/975)
* 将 containerd（仅限静态二进制文件）升级到 [v1.7.12](https://github.com/containerd/containerd/releases/tag/v1.7.12) [moby/moby#47096](https://github.com/moby/moby/pull/47096)
* 将 runc 升级到 v1.1.11。 [moby/moby#47010](https://github.com/moby/moby/pull/47010)

## 24.0.7

<em class="text-gray-400 italic dark:text-gray-500">2023-10-27</em>


有关此版本中拉取请求和变更的完整列表，请参阅相关的 GitHub 里程碑：

- [docker/cli, 24.0.7 里程碑](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A24.0.7)
- [moby/moby, 24.0.7 里程碑](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A24.0.7)

### 错误修复和增强功能

* 原子写入 overlay2 层元数据。 [moby/moby#46703](https://github.com/moby/moby/pull/46703)
* 修复在 systemd 250 及更高版本上运行“根用户模式下的无根” Docker-in-Docker 的问题。 [moby/moby#46626](https://github.com/moby/moby/pull/46626)
* 修复当用户名包含反斜杠时 `dockerd-rootless-setuptools.sh` 的问题。 [moby/moby#46407](https://github.com/moby/moby/pull/46407)
* 修复在停止没有网络连接的容器且使用 `dockerd --bridge=none` 时，网络沙箱无法完全删除的错误。 [moby/moby#46702](https://github.com/moby/moby/pull/46702)
* 修复取消 API 请求可能中断容器重启的错误。 [moby/moby#46697](https://github.com/moby/moby/pull/46697)
* 修复当提供大于子网的 `--ip-range` 范围时容器无法启动的问题。 [docker/for-mac#6870](https://github.com/docker/for-mac/issues/6870)
* 修复 zstd 输出的数据损坏问题。 [moby/moby#46709](https://github.com/moby/moby/pull/46709)
* 修复应用容器 MAC 地址的条件。 [moby/moby#46478](https://github.com/moby/moby/pull/46478)
* 提高统计信息收集器的性能。 [moby/moby#46448](https://github.com/moby/moby/pull/46448)
* 修复源策略规则最终顺序错误的问题。 [moby/moby#46441](https://github.com/moby/moby/pull/46441)

### 打包更新

* 添加对 Fedora 39 和 Ubuntu 23.10 的支持。 [docker/docker-ce-packaging#940](https://github.com/docker/docker-ce-packaging/pull/940), [docker/docker-ce-packaging#955](https://github.com/docker/docker-ce-packaging/pull/955)
* 修复卸载 `docker-ce` RPM 包时 `docker.socket` 未被禁用的问题。 [docker/docker-ce-packaging#852](https://github.com/docker/docker-ce-packaging/pull/852)
* 将 Go 升级到 `go1.20.10`。 [docker/docker-ce-packaging#951](https://github.com/docker/docker-ce-packaging/pull/951)
* 将 containerd 升级到 `v1.7.6`（仅限静态二进制文件）。 [moby/moby#46103](https://github.com/moby/moby/pull/46103)
* 将 `containerd.io` 包升级到 [`v1.6.24`](https://github.com/containerd/containerd/releases/tag/v1.6.24)。

### 安全

* 默认情况下拒绝容器访问 `/sys/devices/virtual/powercap`。此变更增强了对以下漏洞的防护：
  [CVE-2020-8694](https://scout.docker.com/v/CVE-2020-8694),
  [CVE-2020-8695](https://scout.docker.com/v/CVE-2020-8695), 以及
  [CVE-2020-12912](https://scout.docker.com/v/CVE-2020-12912),
  以及一种称为 [PLATYPUS 攻击](https://platypusattack.com/) 的攻击。

  更多详情，请参阅
  [公告](https://github.com/moby/moby/security/advisories/GHSA-jq35-85cj-fj4p),
  [提交](https://github.com/moby/moby/commit/c9ccbfad11a60e703e91b6cca4f48927828c7e35)。

## 24.0.6

<em class="text-gray-400 italic dark:text-gray-500">2023-09-05</em>


有关此版本中拉取请求和变更的完整列表，请参阅相关的 GitHub 里程碑：

- [docker/cli, 24.0.6 里程碑](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A24.0.6)
- [moby/moby, 24.0.6 里程碑](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A24.0.6)

### 错误修复和增强功能

* containerd 存储后端：修复当容器镜像不再存在于内容存储中时 `docker ps` 失败的问题。 [moby/moby#46095](https://github.com/moby/moby/pull/46095)
* containerd 存储后端：修复当容器镜像配置不再存在于内容存储中时 `docker ps -s -a` 和 `docker container prune` 失败的问题。 [moby/moby#46097](https://github.com/moby/moby/pull/46097)
* containerd 存储后端：修复当容器镜像配置不再（或从未）存在于内容存储中时 `docker inspect` 失败的问题。 [moby/moby#46244](https://github.com/moby/moby/pull/46244)
* containerd 存储后端：通过使用引用计数的 rootfs 挂载，修复使用 `overlayfs` 快照器的差异和导出问题。 [moby/moby#46266](https://github.com/moby/moby/pull/46266)
* containerd 存储后端：修复当本地可用的镜像平台与所需平台不匹配时的误导性错误消息。 [moby/moby#46300](https://github.com/moby/moby/pull/46300)
* containerd 存储后端：修复经典构建器使用 `FROM scratch` Dockerfile 指令的问题。 [moby/moby#46302](https://github.com/moby/moby/pull/46302)
* containerd 存储后端：修复经典构建器出现 `mismatched image rootfs and manifest layers` 错误的问题。 [moby/moby#46310](https://github.com/moby/moby/pull/46310)
* 从所有注册表拉取 Docker 镜像格式 v1 和 Docker 镜像清单版本 2、模式 1 的镜像时发出警告。 [moby/moby#46290](https://github.com/moby/moby/pull/46290)
* 修复具有自定义卷选项的卷的实时恢复。 [moby/moby#46366](https://github.com/moby/moby/pull/46366)
* 修复以非 root 用户运行容器时错误地丢弃能力位的问题（注意：由于回归，此更改实际上已经存在）。 [moby/moby#46221](https://github.com/moby/moby/pull/46221)
* 修复网络隔离 iptables 规则阻止容器之间交换 IPv6 邻居请求数据包的问题。 [moby/moby#46214](https://github.com/moby/moby/pull/46214)
* 修复当二进制文件在 Windows 的当前目录中时 `docked.exe --register-service` 不工作的问题。 [moby/moby#46215](https://github.com/moby/moby/pull/46215)
* 为针对 Docker Hub 的 `docker login` 添加建议使用 PAT（个人访问令牌）的提示。 [docker/cli#4500](https://github.com/docker/cli/pull/4500)
* 为使用 CLI 的 Bash 自动补全的用户改善 shell 启动时间。 [docker/cli#4517](https://github.com/docker/cli/pull/4517)
* 通过在可能的情况下跳过 `GET /_ping` 来提高某些命令的速度。 [docker/cli#4508](https://github.com/docker/cli/pull/4508)
* 修复使用 PAT 对 Docker Hub 上的镜像进行 `docker manifest inspect` 时的凭证范围问题。 [docker/cli#4512](https://github.com/docker/cli/pull/4512)
* 修复 `docker events` 不支持 `--format=json` 的问题。 [docker/cli#4544](https://github.com/docker/cli/pull/4544)

### 打包更新

* 将 Go 升级到 `go1.20.7`。 [moby/moby#46140](https://github.com/moby/moby/pull/46140), [docker/cli#4476](https://github.com/docker/cli/pull/4476), [docker/docker-ce-packaging#932](https://github.com/docker/docker-ce-packaging/pull/932)
* 将 containerd 升级到 `v1.7.3`（仅限静态二进制文件）。 [moby/moby#46103](https://github.com/moby/moby/pull/46103)
* 将 Compose 升级到 `v2.21.0`。 [docker/docker-ce-packaging#936](https://github.com/docker/docker-ce-packaging/pull/936)

## 24.0.5

<em class="text-gray-400 italic dark:text-gray-500">2023-07-24</em>


有关此版本中拉取请求和变更的完整列表，请参阅相关的 GitHub 里程碑：

- [docker/cli, 24.0.5 里程碑](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A24.0.5)
- [moby/moby, 24.0.5 里程碑](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A24.0.5)

### 错误修复和增强功能

* Go 客户端现在避免在 HTTP `Host:` 头中使用 UNIX 套接字路径，以便与 `go1.20.6` 中引入的更改兼容。 [moby/moby#45962](https://github.com/moby/moby/pull/45962), [moby/moby#45990](https://github.com/moby/moby/pull/45990)
* containerd 存储后端：修复 `Variant` 未包含在 `docker image inspect` 和 `GET /images/{name}/json` 中的问题。 [moby/moby#46025](https://github.com/moby/moby/pull/46025)
* containerd 存储后端：防止在镜像导出期间对内容进行潜在的垃圾回收。 [moby/moby#46021](https://github.com/moby/moby/pull/46021)
* containerd 存储后端：防止 `RepoDigests` 中出现重复的摘要条目。 [moby/moby#46014](https://github.com/moby/moby/pull/46014)
* containerd 存储后端：修复当处理通过标签和摘要引用的镜像时，操作针对错误标签进行的问题。 [moby/moby#46013](https://github.com/moby/moby/pull/46013)
* containerd 存储后端：修复使用传统构建器构建容器时 `EXPOSE` 导致的 panic。 [moby/moby#45921](https://github.com/moby/moby/pull/45921)
* 修复在非 Swarm 节点上尝试创建 `overlay` 网络时导致返回非直观错误的回归问题。 [moby/moby#45974](https://github.com/moby/moby/pull/45974)
* 正确报告从命令行解析卷规范时的错误。 [docker/cli#4423](https://github.com/docker/cli/pull/4423)
* 修复当 CLI 配置文件中找到 `auths: null` 时导致的 panic。 [docker/cli#4450](https://github.com/docker/cli/pull/4450)

### 打包更新

* 使用 moby/moby `contrib/init` 中提供的初始化脚本。 [docker/docker-ce-packaging#914](https://github.com/docker/docker-ce-packaging/pull/914), [docker/docker-ce-packaging#926](https://github.com/docker/docker-ce-packaging/pull/926)
* 从 `contrib/init` 中移除 Upstart。 [moby/moby#46044](https://github.com/moby/moby/pull/46044)
* 将 Go 升级到 `go1.20.6`。 [docker/cli#4428](https://github.com/docker/cli/pull/4428), [moby/moby#45970](https://github.com/moby/moby/pull/45970), [docker/docker-ce-packaging#921](https://github.com/docker/docker-ce-packaging/pull/921)
* 将 Compose 升级到 `v2.20.2`。 [docker/docker-ce-packaging#924](https://github.com/docker/docker-ce-packaging/pull/924)
* 将 buildx 升级到 `v0.11.2`。 [docker/docker-ce-packaging#922](https://github.com/docker/docker-ce-packaging/pull/922)


## 24.0.4

<em class="text-gray-400 italic dark:text-gray-500">2023-07-07</em>


有关此版本中拉取请求和变更的完整列表，请参阅相关的 GitHub 里程碑：

- [docker/cli, 24.0.4 里程碑](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A24.0.4)
- [moby/moby, 24.0.4 里程碑](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A24.0.4)

### 错误修复和增强功能

* 修复在 24.0.3 期间引入的回归问题，该问题导致在具有绑定挂载的容器实时恢复期间发生 panic。 [moby/moby#45903](https://github.com/moby/moby/pull/45903)


## 24.0.3

<em class="text-gray-400 italic dark:text-gray-500">2023-07-06</em>


有关此版本中拉取请求和变更的完整列表，请参阅相关的 GitHub 里程碑：

- [docker/cli, 24.0.3 里程碑](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A24.0.3)
- [moby/moby, 24.0.3 里程碑](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A24.0.3)

### 错误修复和增强功能

* containerd 镜像存储：修复不包含默认平台清单的多平台镜像无法交互的问题。 [moby/moby#45849](https://github.com/moby/moby/pull/45849)
* containerd 镜像存储：修复在容器构建中尝试缓存 `FROM scratch` 的问题。 [moby/moby#45822](https://github.com/moby/moby/pull/45822)
* containerd 镜像存储：修复 `docker cp` 与无法多次挂载相同内容的快照器一起使用的问题。 [moby/moby#45780](https://github.com/moby/moby/pull/45780), [moby/moby#45786](https://github.com/moby/moby/pull/45786)
* containerd 镜像存储：修复使用 `type=image` 的构建未正确解包/存储的问题。 [moby/moby#45692](https://github.com/moby/moby/pull/45692)
* containerd 镜像存储：修复在 `docker load` 中错误地尝试解包伪镜像（包括证明）的问题。 [moby/moby#45688](https://github.com/moby/moby/pull/45688)
* containerd 镜像存储：正确设置用户代理，并在与注册表交互时包含快照器等附加信息。 [moby/moby#45671](https://github.com/moby/moby/pull/45671), [moby/moby#45684](https://github.com/moby/moby/pull/45684)
* containerd 镜像存储：修复在快照器之间切换后无法解包已拉取内容的问题。 [moby/moby#45678](https://github.com/moby/moby/pull/45678)
* containerd 镜像存储：修复已被重新标记或所有标签均被移除的镜像在仍在使用时被修剪的问题。 [moby/moby#45857](https://github.com/moby/moby/pull/45857)
* 修复 Swarm CSI 问题，其中拓扑字段未传播到 NodeCSIInfo。 [moby/moby#45810](https://github.com/moby/moby/pull/45810)
* 修复由于非常大的 Raft 日志导致添加新的 Swarm 管理节点失败的问题。 [moby/moby#45703](https://github.com/moby/moby/pull/45703), [moby/swarmkit#3122](https://github.com/moby/swarmkit/pull/3122), [moby/swarmkit#3128](https://github.com/moby/swarmkit/pull/3128)
* `name_to_handle_at(2)` 现在在默认 seccomp 配置文件中始终被允许。 [moby/moby#45833](https://github.com/moby/moby/pull/45833)
* 修复加密的 Swarm 覆盖网络在非默认端口（4789）上无法工作的问题。 [moby/moby#45637](https://github.com/moby/moby/pull/45637)
* 修复在实时恢复期间无法恢复挂载引用计数的问题。 [moby/moby#45824](https://github.com/moby/moby/pull/45824)
* 修复实时恢复期间各种与网络相关的故障。 [moby/moby#45658](https://github.com/moby/moby/pull/45658), [moby/moby#45659](https://github.com/moby/moby/pull/45659)
* 修复当守护进程意外终止时，正在运行的容器以零（成功）退出状态恢复的问题。 [moby/moby#45801](https://github.com/moby/moby/pull/45801)
* 修复在执行健康检查探测期间可能出现的 panic。 [moby/moby#45798](https://github.com/moby/moby/pull/45798)
* 修复容器 exec 启动中的竞争条件导致的 panic。 [moby/moby#45794](https://github.com/moby/moby/pull/45794)
* 修复将终端附加到具有不存在命令的 exec 时导致的异常。 [moby/moby#45643](https://github.com/moby/moby/pull/45643)
* 通过将 IP 作为标签传递来修复 BuildKit 的 `host-gateway` 问题（还需要 [docker/buildx#1894](https://github.com/docker/buildx/pull/1894)）。 [moby/moby#45790](https://github.com/moby/moby/pull/45790)
* 修复当请求被取消时 `POST /containers/{id}/stop` 会强制终止容器，而不是等待指定的超时时间以进行“优雅”停止的问题。 [moby/moby#45774](https://github.com/moby/moby/pull/45774)
* 修复从根目录 (`/`) 执行 `docker cp -a` 会失败的问题。 [moby/moby#45748](https://github.com/moby/moby/pull/45748)
* 通过在 OCI 配置中更正确地设置资源约束参数，提高与非 runc 容器运行时的兼容性。 [moby/moby#45746](https://github.com/moby/moby/pull/45746)
* 修复在无根模式下某些配置（例如 LDAP）中 subuid/subgid 范围重叠导致的问题。 [moby/moby#45747](https://github.com/moby/moby/pull/45747), [rootless-containers/rootlesskit#369](https://github.com/rootless-containers/rootlesskit/pull/369)
* 在填充 `GET /info` 的调试部分时，大大减少 CPU 和内存使用量。 [moby/moby#45856](https://github.com/moby/moby/pull/45856)
* 修复当仅客户端处于调试模式时，`docker info` 期间未正确打印调试信息的问题。 [docker/cli#4393](https://github.com/docker/cli/pull/4393)
* 修复通过 SSH 连接连接到主机时的挂起连接问题。 [docker/cli#4395](https://github.com/docker/cli/pull/4395)

### 打包更新

* 将 Go 升级到 `go1.20.5`。 [moby/moby#45745](https://github.com/moby/moby/pull/45745), [docker/cli#4351](https://github.com/docker/cli/pull/4351), [docker/docker-ce-packaging#904](https://github.com/docker/docker-ce-packaging/pull/904)
* 将 Compose 升级到 `v2.19.1`。 [docker/docker-ce-packaging#916](https://github.com/docker/docker-ce-packaging/pull/916)
* 将 buildx 升级到 `v0.11.1`。 [docker/docker-ce-packaging#918](https://github.com/docker/docker-ce-packaging/pull/918)


## 24.0.2

<em class="text-gray-400 italic dark:text-gray-500">2023-05-26</em>


有关此版本中拉取请求和变更的完整列表，请参阅相关的 GitHub 里程碑：

- [docker/cli, 24.0.2 里程碑](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A24.0.2)
- [moby/moby, 24.0.2 里程碑](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A24.0.2)

### 错误修复和增强功能

* 修复在构建期间引用本地标记镜像时发生的 panic。 [moby/buildkit#3899](https://github.com/moby/buildkit/pull/3899), [moby/moby#45582](https://github.com/moby/moby/pull/45582)
* 修复在执行许多并发构建阶段时可能因 `exit code: 4294967295` 而导致构建失败的问题。 [moby/moby#45620](https://github.com/moby/moby/pull/45620)
* 修复 Windows 上的 DNS 解析忽略 `etc/hosts`（`%WINDIR%\System32\Drivers\etc\hosts`），包括 `localhost` 的解析。 [moby/moby#45562](https://github.com/moby/moby/pull/45562)
* 应用针对 containerd 错误的解决方法，该错误导致并发的 `docker exec` 命令花费的时间比预期长得多。 [moby/moby#45625](https://github.com/moby/moby/pull/45625)
* containerd 镜像存储：修复镜像 `Created` 字段包含错误值的问题。 [moby/moby#45623](https://github.com/moby/moby/pull/45623)
* containerd 镜像存储：调整镜像拉取进度的输出，使无论是否启用容器镜像存储，输出格式都相同。 [moby/moby#45602](https://github.com/moby/moby/pull/45602)
* containerd 镜像存储：在默认镜像存储和容器镜像存储之间切换现在需要重启守护进程。 [moby/moby#45616](https://github.com/moby/moby/pull/45616)

### 打包更新

* 将 Buildx 升级到 `v0.10.5`。 [docker/docker-ce-packaging#900](https://github.com/docker/docker-ce-packaging/pull/900)


## 24.0.1

<em class="text-gray-400 italic dark:text-gray-500">2023-05-19</em>


有关此版本中拉取请求和变更的完整列表，请参阅相关的 GitHub 里程碑：

- [docker/cli, 24.0.1 里程碑](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A24.0.1)
- [moby/moby, 24.0.1 里程碑](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A24.0.1)

### 已移除

* 移除了 24.0 主要版本中已移除的存储驱动的 CLI 自动补全。 [docker/cli#4302](https://github.com/docker/cli/pull/4302)

### 错误修复和增强功能

* 修复来自外部服务器的 DNS 查询 NXDOMAIN 回复被作为 SERVFAIL 转发给客户端的问题。 [moby/moby#45573](https://github.com/moby/moby/pull/45573)
* 修复 `docker pull --platform` 会针对指向同一镜像的另一个标签报告 `No such image` 的问题。 [moby/moby#45562](https://github.com/moby/moby/pull/45562)
* 修复不安全的注册表配置在配置重新加载期间被遗忘的问题。 [moby/moby#45571](https://github.com/moby/moby/pull/45571)
* containerd 镜像存储：修复没有层的镜像不会在 `docker images -a` 中列出的问题。 [moby/moby#45588](https://github.com/moby/moby/pull/45588)
* API：修复 `GET /images/{id}/json` 返回 `null` 而不是空的 `RepoTags` 和 `RepoDigests` 的问题。 [moby/moby#45564](https://github.com/moby/moby/pull/45564)
* API：修复 `POST /commit` 不接受空请求正文的问题。 [moby/moby#45568](https://github.com/moby/moby/pull/45568)

### 打包更新

* 将 Compose 升级到 `v2.18.1`。 [docker/docker-ce-packaging#896](https://github.com/docker/docker-ce-packaging/pull/896)


## 24.0.0

<em class="text-gray-400 italic dark:text-gray-500">2023-05-16</em>


有关此版本中拉取请求和变更的完整列表，请参阅相关的 GitHub 里程碑：

- [docker/cli, 24.0.0 里程碑](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A24.0.0)
- [moby/moby, 24.0.0 里程碑](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3
