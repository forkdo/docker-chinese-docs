---
description: Docker Desktop for Mac 旧版本发行说明
keywords: Docker Desktop for Mac, 发行说明
title: 旧版本发行说明
toc_min: 1
toc_max: 2
aliases:
- /desktop/mac/release-notes/archive/
sitemap: false
---

本页包含 Docker Desktop for Mac 旧版本的发行说明。

## 2018 年稳定版

### Docker Community Edition 18.06.1-ce-mac73 2018-08-29

* 升级
  - [Docker 18.06.1-ce](https://github.com/docker/docker-ce/releases/tag/v18.06.1-ce)

* Bug 修复和微小改动
  - 修复容器内本地 DNS 解析失败的问题。

### Docker Community Edition 18.06.0-ce-mac70 2018-07-25

* 升级
  - [Docker 18.06.0-ce](https://github.com/docker/docker-ce/releases/tag/v18.06.0-ce)
  - [Docker Machine 0.15.0](https://github.com/docker/machine/releases/tag/v0.15.0)
  - [Docker compose 1.22.0](https://github.com/docker/compose/releases/tag/1.22.0)
  - [LinuxKit v0.5](https://github.com/linuxkit/linuxkit/releases/tag/v0.5)
  - Linux Kernel 4.9.93，启用了 CEPH、DRBD、RBD、MPLS_ROUTING 和 MPLS_IPTUNNEL

* 新增功能
  - Kubernetes 支持。您现在可以从 Docker for Mac 偏好设置中的 "Kubernetes" 面板运行单节点 Kubernetes 集群，并使用 kubectl 命令以及 docker 命令。请参阅 [Kubernetes 部分](/manuals/desktop/use-desktop/kubernetes.md)
  - 添加实验性 SOCKS 服务器以允许访问容器网络，请参阅 [docker/for-mac#2670](https://github.com/docker/for-mac/issues/2670#issuecomment-372365274)。另请参阅 [docker/for-mac#2721](https://github.com/docker/for-mac/issues/2721)
  - 为运行 macOS 10.13.4 及更高版本的用户重新启用 raw 作为默认磁盘格式。请注意，此更改仅在“恢复出厂默认设置”或“移除所有数据”（从鲸鱼菜单 -> 偏好设置 -> 重置）后生效。与 [docker/for-mac#2625](https://github.com/docker/for-mac/issues/2625) 相关

* Bug 修复和微小改动
  - AUFS 存储驱动在 Docker Desktop 中已弃用，AUFS 支持将在下一个主要版本中移除。您可以在 Docker Desktop 18.06.x 中继续使用 AUFS，但在更新到下一个主要版本之前需要重置磁盘映像（在偏好设置 > 重置菜单中）。您可以查阅文档以[保存映像](/reference/cli/docker/image/save/#examples)和[备份卷](/manuals/engine/storage/volumes.md#back-up-restore-or-migrate-data-volumes)
  - OS X El Captain 10.11 在 Docker Desktop 中已弃用。在 Docker Desktop 18.06.x 之后您将无法安装更新。我们建议升级到最新版本的 macOS。
  - 修复在某些情况下导致 VM 日志写入 RAM 而不是磁盘的错误，并导致 VM 挂起。请参阅 [docker/for-mac#2984](https://github.com/docker/for-mac/issues/2984)
  - 修复由 haproxy TCP 健康检查触发的网络连接泄漏 [docker/for-mac#1132](https://github.com/docker/for-mac/issues/1132)
  - 当 vmnetd 被禁用时提供更好的重置消息。请参阅 [docker/for-mac#3035](https://github.com/docker/for-mac/issues/3035)
  - 修复 VPNKit 内存泄漏。修复 [moby/vpnkit#371](https://github.com/moby/vpnkit/issues/371)
  - 虚拟机默认磁盘路径存储为相对于 $HOME 的路径。修复 [docker/for-mac#2928](https://github.com/docker/for-mac/issues/2928), [docker/for-mac#1209](https://github.com/docker/for-mac/issues/1209)
  - 使用 Simple NTP 以最小化 VM 和主机之间的时钟漂移。修复 [docker/for-mac#2076](https://github.com/docker/for-mac/issues/2076)
  - 修复在调用文件的 stat 和调用引用该文件的文件描述符的 close 之间的竞争条件，这可能导致 stat 失败并出现 EBADF 错误（通常显示为“文件未找到”）。修复 [docker/for-mac#2870](https://github.com/docker/for-mac/issues/2870)
  - 不允许在 macOS Yosemite 10.10 上安装 Docker for Mac，自 Docker for Mac 17.09.0 起已不再支持此版本。
  - 修复重置对话框窗口中的按钮顺序。修复 [docker/for-mac#2827](https://github.com/docker/for-mac/issues/2827)
  - 修复直接从 17.12 之前的版本升级的问题，其中 Docker for Mac 在升级执行后无法重启。修复 [docker/for-mac#2739](https://github.com/docker/for-mac/issues/2739)
  - 为虚拟机内的 docker-ce 日志添加了日志轮转。

### Docker Community Edition 18.03.1-ce-mac65 2018-04-30

* 升级
  - [Docker 18.03.1-ce](https://github.com/docker/docker-ce/releases/tag/v18.03.1-ce)
  - [Docker compose 1.21.1](https://github.com/docker/compose/releases/tag/1.21.1)
  - [Notary 0.6.1](https://github.com/docker/notary/releases/tag/v0.6.1)

* Bug 修复和微小改动
  - 修复因套接字文件路径过长（通常是 HOME 文件夹路径过长）导致 Docker for Mac 无法启动的问题。修复 [docker/for-mac#2727](https://github.com/docker/for-mac/issues/2727), [docker/for-mac#2731](https://github.com/docker/for-mac/issues/2731)。

### Docker Community Edition 18.03.1-ce-mac64 2018-04-26

* 升级
  - [Docker 18.03.1-ce](https://github.com/docker/docker-ce/releases/tag/v18.03.1-ce)
  - [Docker compose 1.21.0](https://github.com/docker/compose/releases/tag/1.21.0)
  - [Notary 0.6.1](https://github.com/docker/notary/releases/tag/v0.6.1)

* Bug 修复和微小改动
  - 修复因套接字文件路径过长（通常是 HOME 文件夹路径过长）导致 Docker for Mac 无法启动的问题。修复 [docker/for-mac#2727](https://github.com/docker/for-mac/issues/2727), [docker/for-mac#2731](https://github.com/docker/for-mac/issues/2731)。

### Docker Community Edition 18.03.0-ce-mac60 2018-03-30

* Bug 修复和微小改动
  - 修复直接从 17.09 版本升级的问题，其中 Docker for Mac 在升级执行后无法重启。修复 [docker/for-mac#2739](https://github.com/docker/for-mac/issues/2739)

### Docker Community Edition 18.03.0-ce-mac59 2018-03-26

* 升级
  - [Docker 18.03.0-ce](https://github.com/docker/docker-ce/releases/tag/v18.03.0-ce)
  - [Docker Machine 0.14.0](https://github.com/docker/machine/releases/tag/v0.14.0)
  - [Docker compose 1.20.1](https://github.com/docker/compose/releases/tag/1.20.1)
  - [Notary 0.6.0](https://github.com/docker/notary/releases/tag/v0.6.0)
  - Linux Kernel 4.9.87
  - AUFS 20180312

* 新增功能
  - 可以在设置中更改 VM 交换空间大小。请参阅 [docker/for-mac#2566](https://github.com/docker/for-mac/issues/2566), [docker/for-mac#2389](https://github.com/docker/for-mac/issues/2389)
  - 新增用于重启 Docker 的菜单项。
  - 支持 NFS 卷共享。
  - 保存磁盘映像的目录已重命名（从 `~/Library/Containers/com.docker.docker/Data/com.docker.driver.amd64-linux` 变为 ~/Library/Containers/com.docker.docker/Data/vms/0`）。

* Bug 修复和微小改动
  - 修复设置 TLS 相关选项时守护进程无法正常启动的问题。修复 [docker/for-mac#2663](https://github.com/docker/for-mac/issues/2663)
  - 应使用 DNS 名称 `host.docker.internal` 从容器解析主机。旧的别名（仍然有效）已弃用，建议使用此名称。（请参阅 https://tools.ietf.org/html/draft-west-let-localhost-be-localhost-06）。
  - 修复使用“localhost”名称（例如 `host.docker.internal`）时的 HTTP/S 透明代理问题。
  - 修复在某些情况下偏好设置守护进程面板中错误添加的空注册表。修复 [docker/for-mac#2537](https://github.com/docker/for-mac/issues/2537)
  - 检测到不兼容硬件时提供更清晰的错误消息。
  - 修复在某些情况下选择错误后“重置”无法正确重置的问题。
  - 修复不正确的 NTP 配置。修复 [docker/for-mac#2529](https://github.com/docker/for-mac/issues/2529)
  - Docker for Mac 安装程序中不再建议迁移 Docker Toolbox 映像（仍然可以手动迁移 Toolbox 映像）。

### Docker Community Edition 17.12.0-ce-mac55 2018-02-27

* Bug 修复和微小改动
  - 对于运行 macOS 10.13 (High Sierra) 的用户，将默认磁盘格式恢复为 qcow2。有确凿报告称，使用在 APFS 上使用稀疏文件的 raw 格式会导致文件损坏。请注意，此更改仅在恢复出厂默认设置（从鲸鱼菜单 -> 偏好设置 -> 重置）后生效。与 [docker/for-mac#2625](https://github.com/docker/for-mac/issues/2625) 相关
  - 修复 docker.for.mac.http.internal 的 VPNKit 代理。

### Docker Community Edition 17.12.0-ce-mac49 2018-01-19

* Bug 修复和微小改动
  - 修复在某些情况下调整大小/创建 Docker.raw 磁盘映像时的错误。修复 [docker/for-mac#2383](https://github.com/docker/for-mac/issues/2383), [docker/for-mac#2447](https://github.com/docker/for-mac/issues/2447), [docker/for-mac#2453], (https://github.com/docker/for-mac/issues/2453), [docker/for-mac#2420](https://github.com/docker/for-mac/issues/2420)
  - 修复容器中无法使用额外分配的磁盘空间的问题。修复 [docker/for-mac#2449](https://github.com/docker/for-mac/issues/2449)
  - Vpnkit 端口最大空闲时间默认值恢复为 300 秒。修复 [docker/for-mac#2442](https://github.com/docker/for-mac/issues/2442)
  - 修复使用带身份验证的 HTTP 代理的问题。修复 [docker/for-mac#2386](https://github.com/docker/for-mac/issues/2386)
  - 允许将 HTTP 代理排除项写为 .docker.com 以及 *.docker.com
  - 允许将单个 IP 地址添加到 HTTP 代理排除项。
  - 当上游 DNS 服务器响应慢或缺失时，避免查询 docker.for.mac.* 时遇到 DNS 超时。

### Docker Community Edition 17.12.0-ce-mac47 2018-01-12

* Bug 修复和微小改动
  - 修复 `docker push` 到不安全注册表的问题。修复 [docker/for-mac#2392](https://github.com/docker/for-mac/issues/2392)
  - 分离用于代理 HTTP 和 HTTPS 内容的内部端口。

### Docker Community Edition 17.12.0-ce-mac46 2018-01-09

* 升级
  - [Docker 17.12.0-ce](https://github.com/docker/docker-ce/releases/tag/v17.12.0-ce)
  - [Docker compose 1.18.0](https://github.com/docker/compose/releases/tag/1.18.0)
  - [Docker Machine 0.13.0](https://github.com/docker/machine/releases/tag/v0.13.0)
  - Linux Kernel 4.9.60

* 新增功能
  - VM 完全由 Linuxkit 构建
  - 可以在磁盘偏好设置中更改 VM 磁盘大小。（请参阅 [docker/for-mac#1037](https://github.com/docker/for-mac/issues/1037)）
  - 对于在 High Sierra 上的 SSD 运行 APFS 的系统，默认使用 `raw` 格式的 VM 磁盘。这提高了磁盘吞吐量（在 2015 MacBook Pro 上使用 `dd` 测试，从 320MiB/sec 提高到 600MiB/sec）和磁盘空间处理。
    现有磁盘仍保留为 qcow 格式，如果要切换到 raw 格式，需要“移除所有数据”或“恢复出厂默认设置”。
  - 应使用 DNS 名称 `docker.for.mac.host.internal` 而不是 `docker.for.mac.localhost`（仍然有效）从容器解析主机，因为有 RFC 禁止使用 localhost 的子域。请参阅 https://tools.ietf.org/html/draft-west-let-localhost-be-localhost-06。

* Bug 修复和微小改动
  - 在“关于”框中显示各种组件版本。
  - 更改主机代理设置时避免 VM 重启。
  - 不要通过外部代理转发容器之间的 HTTP 流量来破坏它们。（请参阅 [docker/for-mac#981](https://github.com/docker/for-mac/issues/981)）
  - 文件共享设置现在存储在 settings.json 中。
  - 守护进程重启按钮已移至设置 / 重置选项卡。
  - 更好的 VM 状态处理和 VM 崩溃时的错误消息。
  - 修复使用证书问题登录私有仓库的问题。（请参阅 [docker/for-mac#2201](https://github.com/docker/for-mac/issues/2201)）

## 2017 年稳定版

### Docker Community Edition 17.09.1-ce-mac42 2017-12-11

* 升级
  - [Docker 17.09.1-ce](https://github.com/docker/docker-ce/releases/tag/v17.09.1-ce)
  - [Docker compose 1.17.1](https://github.com/docker/compose/releases/tag/1.17.1)
  - [Docker Machine 0.13.0](https://github.com/docker/machine/releases/tag/v0.13.0)

* Bug 修复和微小改动
  - 修复在某些情况下不允许移动 qcow 磁盘的错误。

### Docker Community Edition 17.09.0-ce-mac35 2017-10-06

* Bug 修复
  - 修复在某些情况下 Docker For Mac 无法启动的问题：移除了有时导致 vpnkit 进程死亡的 libgmp 使用。

### Docker Community Edition 17.09.0-ce-mac33 2017-10-03
  - 当存在现有的 Docker For Mac 数据时，不显示 Toolbox 迁移助手。

### Docker Community Edition 17.09.0-ce-mac32 2017-10-02

* 升级
  - [Docker 17.09.0-ce](https://github.com/docker/docker-ce/releases/tag/v17.09.0-ce)
  - [Docker Compose 1.16.1](https://github.com/docker/compose/releases/tag/1.16.1)
  - [Docker Machine 0.12.2](https://github.com/docker/machine/releases/tag/v0.12.2)
  - [Docker Credential Helpers 0.6.0](https://github.com/docker/docker-credential-helpers/releases/tag/v0.6.0)
  - Linux Kernel 4.9.49
  - AUFS 20170911
  - DataKit 更新（修复 High Sierra 上的不稳定问题）

* 新增功能
  - 添加守护进程选项验证
  - VPNKit：添加对 ping 的支持！
  - VPNKit：添加 slirp/port-max-idle-timeout 以允许调整甚至禁用超时
  - VPNKit：桥接模式现在在所有地方都是默认模式
  - 透明代理直接使用 macOS 系统代理（如果已定义）
  - GUI 设置现在存储在 ~/Library/Group\ Containers/group.com.docker/settings.json 中。daemon.json 现在是 ~/.docker/ 中的一个文件
  - 您现在可以更改 Hyperkit 使用的默认 IP 地址，如果它与您的网络冲突

* Bug 修复和微小改动
  - 修复 High Sierra 上的不稳定问题 (docker/for-mac#2069, docker/for-mac#2062, docker/for-mac#2052, docker/for-mac#2029, docker/for-mac#2024)
  - 修复密码编码/解码问题 (docker/for-mac#2008, docker/for-mac#2016, docker/for-mac#1919, docker/for-mac#712, docker/for-mac#1220)。
  - 内核：启用 TASK_XACCT 和 TASK_IO_ACCOUNTING (docker/for-mac#1608)
  - 更频繁地轮转 VM 中的日志
  - VPNKit：更改协议以支持从服务器报告的错误消息
  - VPNKit：修复如果相应的 TCP 连接空闲超过 5 分钟会导致套接字泄漏的错误（与 [docker/for-mac#1374](https://github.com/docker/for-mac/issues/1374) 相关）
  - VPNKit：改进 Unix 域套接字连接周围的日志记录
  - VPNKit：自动修剪 int 或 bool 数据库键的空白
  - 诊断可以取消并改进帮助信息。修复 docker/for-mac#1134, docker/for-mac#1474
  - 支持 docker-cloud 仓库和组织的分页。修复 docker/for-mac#1538

### Docker Community Edition 17.06.2-ce-mac27 2017-09-06

**升级**

  - [Docker 17.06.2-ce](https://github.com/docker/docker-ce/releases/tag/v17.06.2-ce)
  - [Docker Machine 0.12.2](https://github.com/docker/machine/releases/tag/v0.12.2)

### Docker Community Edition 17.06.1-ce-mac24, 2017-08-21

**升级**

- [Docker 17.06.1-ce-rc1](https://github.com/docker/docker-ce/releases/tag/v17.06.1-ce-rc1)
- Linux Kernel 4.9.36
- AUFS 20170703

**Bug 修复和微小改动**

- DNS 修复。修复 [docker/for-mac#1763](https://github.com/docker/for-mac/issues/176), [docker/for-mac#1811](https://github.com/docker/for-mac/issues/1811), [docker/for-mac#1803](https://github.com/docker/for-mac/issues/1803)

- 避免不必要的 VM 重启（当更改代理排除项但未设置代理时）。修复 [docker/for-mac#1809](https://github.com/docker/for-mac/issues/1809), [docker/for-mac#1801](https://github.com/docker/for-mac/issues/1801)

### Docker Community Edition 17.06.0-ce-mac18, 2017-06-28s

**升级**

- [Docker 17.06.0-ce](https://github.com/docker/docker-ce/releases/tag/v17.06.0-ce)
- [Docker Credential Helpers 0.5.2](https://github.com/docker/docker-credential-helpers/releases/tag/v0.5.2)
- [Docker Machine 0.12.0](https://github.com/docker/machine/releases/tag/v0.12.0)
- [Docker compose 1.14.0](https://github.com/docker/compose/releases/tag/1.14.0)
- qcow-tool v0.10.0 (提高 `compact` 性能: mirage/ocaml-qcow#94)
- OSX Yosemite 10.10 标记为已弃用
- Linux Kernel 4.9.31

**新增功能**

- 与 Docker Cloud 集成：从本地 CLI 控制远程 Swarm 并查看您的仓库。
- GUI 选项以退出凭据存储
- GUI 选项以重置 Docker 数据而不丢失所有设置（修复 [docker/for-mac#1309](https://github.com/docker/for-mac/issues/1309)）
- 添加主机的实验性 DNS 名称：`docker.for.mac.localhost`
- 支持用于验证仓库访问的客户端（即“登录”）证书（修复 [docker/for-mac#1320](https://github.com/docker/for-mac/issues/1320)）
- OSXFS：支持 `cached` 挂载标志，以在不需要严格一致性时提高 macOS 挂载的性能

**Bug 修复和微小改动**

- 应用程序启动时重新同步 HTTP(S) 代理设置
- 正确解释 `localhost` 的系统代理设置（请参阅 [docker/for-mac#1511](https://github.com/docker/for-mac/issues/1511)）
- Docker for Mac 捆绑的所有 Docker 二进制文件现在都已签名
- 在鲸鱼菜单中显示所有 Docker Cloud 组织和仓库（修复 [docker/for-mac#1538](https://github.com/docker/for-mac/issues/1538)）
- OSXFS：许多常见操作（如读写）的延迟提高了约 25%
- 修复在选择文本表格视图并重新打开窗口时 GUI 崩溃的问题（修复 [docker/for-mac#1477](https://github.com/docker/for-mac/issues/1477)）
- 恢复默认设置/卸载时也移除 `config.json` 和 `osxkeychain` 凭据
- 更详细的 VirtualBox 卸载要求（ [docker/for-mac#1343](https://github.com/docker/for-mac/issues/1343)）
- 唤醒后请求时间同步以改进 [docker/for-mac#17](https://github.com/docker/for-mac/issues/17)
- VPNKit：改进 DNS 超时处理（修复 [docker/for-mac#202](https://github.com/docker/vpnkit/issues/202)）
- VPNKit：默认使用 DNSServiceRef API（仅在全新安装或恢复出厂设置后启用）
- 应用程序崩溃时添加恢复出厂默认设置的按钮
- Toolbox 导入对话框现在默认为“跳过”
- 当 Docker 客户端请求升级到原始流时，应正确处理缓冲数据
- 移除了与实验功能处理相关的输出错误消息
- 当用户主目录位于外部驱动器上时，`vmnetd` 不应崩溃
- 改进设置数据库模式处理
- 磁盘修剪应按预期工作
- 诊断现在包含更多设置数据

### Docker Community Edition 17.03.1-ce-mac12, 2017-05-12s

**升级**

- CVE-2017-7308 安全修复

### Docker Community Edition 17.03.1-ce-mac5, 2017-03-29s

**升级**

- [Docker Credential Helpers 0.4.2](https://github.com/docker/docker-credential-helpers/releases/tag/v0.4.2)


### Docker Community Edition 17.03.0-ce-mac1, 2017-03-02- 重命名为 Docker Community Edition

**新增功能**

- 与 Docker Cloud 集成：从本地 CLI 控制远程 Swarm 并查看您的仓库。此功能将逐步向所有用户推出
- Docker 现在会将您的 ID 安全地存储在 macOS 钥匙串中

**升级**

- [Docker 17.03.0-ce](https://github.com/docker/docker/releases/tag/v17.03.0-ce)
- [Docker Compose 1.11.2](https://github.com/docker/compose/releases/tag/1.11.2)
- [Docker Machine 0.10.0](https://github.com/docker/machine/releases/tag/v0.10.0)
- Linux kernel 4.9.12

**Bug 修复和微小改动**

- 允许通过高级子面板中的链接重置错误的 daemon.json
- 移动磁盘映像时提供更多选项
- 添加指向实验功能的链接
- 文件共享和守护进程表的空字段可编辑
- 隐藏设置窗口中的重启按钮
- 修复当应用程序未聚焦时更新窗口隐藏的错误
- 不要在 Linux VM 内使用端口 4222
- 将 page_poison=1 添加到启动参数
- 添加新的磁盘刷新选项
- DNS 转发器忽略来自故障服务器的响应 (docker/for-mac#1025)
- DNS 转发器并行发送所有查询，按顺序处理结果
- DNS 转发器在常规搜索中包含带区域的服务器 (docker/for-mac#997)
- 解析 /etc/hosts 中的别名 (docker/for-mac#983)
- 可以通过主机上 /etc/resolver 目录中列出的服务器解析 DNS 请求
- 将 vCPU 限制为 64
- 修复未挂载交换空间的问题
- 修复 aufs xattr 删除问题 (docker/docker#30245)
- osxfs：在读取非文件的扩展属性时捕获 EPERM
- VPNKit：修复包含指向标签指针的指针的 DNS 数据包的解组
- VPNKit：在来自缓存的 DNS 响应上设置“可用递归”位
- VPNKit：避免诊断捕获过多数据
- VPNKit：修复虚拟以太网链路上偶尔丢包（截断）的来源
- HyperKit：转储状态时从 VMCS 转储客户机物理和线性地址
- HyperKit：内核启动时带 panic=1 参数

### Docker for Mac 1.13.1, 2017-02-09s

**升级**

- [Docker 1.13.1](https://github.com/docker/docker/releases/tag/v1.13.1)
- [Docker Compose 1.11.1](https://github.com/docker/compose/releases/tag/1.11.1)
- Linux kernel 4.9.8

**Bug 修复和微小改动**

- 添加指向实验功能的链接
- 新的 1.13 可取消操作现在应由桌面 Docker 正确处理
- `daemon.json` 应在 UI 中良好呈现
- 允许通过高级子面板中的链接重置错误的 `daemon.json`

### Docker for Mac 1.13.0, 2017-01-19s

**升级**

- [Docker 1.13.0](https://github.com/docker/docker/releases/tag/v1.13.0)
- [Docker Compose 1.10](https://github.com/docker/compose/releases/tag/1.10.0)
- [Docker Machine 0.9.0](https://github.com/docker/machine/releases/tag/v0.9.0)
- [Notary 0.4.3](https://github.com/docker/notary/releases/tag/v0.4.3)
- Linux kernel 4.9.4
- qcow-tool 0.7.2

**新增功能**

- Linux 卷的存储位置现在可以移动
- 重启时回收磁盘空间
- 您现在可以编辑文件共享路径
- 内存可以以 256 MiB 为步长进行分配
- 代理现在可以完全禁用
- 使用 qemu 支持 arm、aarch64、ppc64le 架构
- 用于高级配置 docker 守护进程的专用偏好设置面板（编辑 `daemon.json`）
- Docker 实验模式可以切换
- 更好地支持拆分 DNS VPN 配置
- 使用更多 DNS 服务器，尊重顺序

**Bug 修复和微小改动**

- Docker 重启时无法编辑设置
- 在“关于”框中支持复制/粘贴
- 每 24 小时自动更新一次
- 内核启动时带 vsyscall=emulate 参数，Moby 中 CONFIG_LEGACY_VSYSCALL 设置为 NONE
- 修复重写负载下的 vsock 死锁
- 如果您选择退出分析，在发送错误报告之前会提示您批准
- 修复搜索域可能被读取为 `DomainName` 的错误
- 用于 HTTP 代理设置的专用偏好设置面板
- 用于 CPU 和内存计算资源的专用偏好设置面板
- 隐私设置移至常规偏好设置面板
- 修复当欢迎鲸鱼菜单关闭时偏好设置面板消失的问题
- HyperKit：代码清理和微小修复
- 改进日志记录和诊断
- osxfs：切换到 libev/kqueue 以提高延迟
- VPNKit：改进 DNS 处理
- VPNKit：改进诊断
- VPNKit：转发的 UDP 数据报应具有正确的源端口号
- VPNKit：添加 DNS 响应的本地缓存
- VPNKit：如果一个请求失败，允许其他并发请求成功。例如，即使 IPv6 损坏，这也能让 IPv4 服务器正常工作。
- VPNKit：修复可能导致连接跟踪低估活动连接数的错误

## 2016 年稳定版

### Docker for Mac 1.12.5, 2016-12-20s

**升级**

- Docker 1.12.5
- Docker Compose 1.9.0

### 跳过 Docker for Mac 1.12.4

我们没有分发 1.12.4 稳定版

### Docker for Mac 1.12.3, 2016-11-09s

**升级**

- Docker 1.12.3
- Linux Kernel 4.4.27
- Notary 0.4.2
- Docker Machine 0.8.2
- Docker Compose 1.8.1
- Kernel vsock driver v7
- aufs 20160912

**Bug 修复和微小改动**

**常规**

- 修复了设置更改期间鲸鱼动画不一致的问题

- 修复了某些窗口隐藏在另一个应用程序后面的问题

- 修复了 VM 正确启动后 Docker 状态继续显示为黄色/动画的问题

- 修复了 Docker for Mac 被错误报告为已更新的问题

- 频道现在显示在“关于”框中

- 崩溃报告通过 Bugsnag 而不是 HockeyApp 发送

- 修复了某些窗口未正确获取焦点的问题

- 添加了切换频道时的 UI，以防止用户丢失容器和设置

- 在 Toolbox 导入前检查磁盘容量

- 导入 `etc/ssl/certs/ca-certificates.crt` 中的证书

- 磁盘：使“刷新”行为可配置，适用于类似数据库的工作负载。这解决了 1.12.1 中的性能回归问题。

**网络**

- 代理：修复了在容器重启时应用系统或自定义代理设置的问题

- DNS：减少主机上消耗的 UDP 套接字数量

- VPNkit：改进连接限制代码，避免主机上的套接字耗尽

- UDP：处理大于 2035 的数据报，最高可达配置的 macOS 内核限制

- UDP：使转发更健壮；丢弃数据包并继续，而不是停止

**文件共享**

- osxfs：修复了在只读或模式 0 文件上禁止 chown 的问题（修复
  [docker/for-mac#117](https://github.com/docker/for-mac/issues/117),
  [docker/for-mac#263](https://github.com/docker/for-mac/issues/263),
  [docker/for-mac#633](https://github.com/docker/for-mac/issues/633)）

- osxfs：修复了导致某些读取永远运行的竞争条件

- osxfs：修复了同时卷挂载竞争，可能导致崩溃

**Moby**

- 增加默认的 ulimit for memlock（修复 [docker/for-mac#801](https://github.com/docker/for-mac/issues/801)）

### Docker for Mac 1.1