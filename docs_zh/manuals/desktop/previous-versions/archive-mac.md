---
description: Docker Desktop for Mac 旧版本的发行说明
keywords: Docker Desktop for Mac, 发行说明
title: 旧版本的发行说明
toc_min: 1
toc_max: 2
aliases:
- /desktop/mac/release-notes/archive/
sitemap: false
---

此页面包含 Docker Desktop for Mac 较旧版本的发行说明。

## 2018 年的稳定版本

### Docker Community Edition 18.06.1-ce-mac73 2018-08-29

* 升级
  - [Docker 18.06.1-ce](https://github.com/docker/docker-ce/releases/tag/v18.06.1-ce)

* Bug 修复和小改动
  - 修复容器内本地 DNS 解析失败的问题。

### Docker Community Edition 18.06.0-ce-mac70 2018-07-25

* 升级
  - [Docker 18.06.0-ce](https://github.com/docker/docker-ce/releases/tag/v18.06.0-ce)
  - [Docker Machine 0.15.0](https://github.com/docker/machine/releases/tag/v0.15.0)
  - [Docker Compose 1.22.0](https://github.com/docker/compose/releases/tag/1.22.0)
  - [LinuxKit v0.5](https://github.com/linuxkit/linuxkit/releases/tag/v0.5)
  - Linux Kernel 4.9.93，启用 CEPH、DRBD、RBD、MPLS_ROUTING 和 MPLS_IPTUNNEL

* 新增功能
  - Kubernetes 支持。现在可以从 Docker for Mac 偏好设置的“Kubernetes”面板运行单节点 Kubernetes 集群，并使用 kubectl 命令和 docker 命令。参见 [Kubernetes 部分](/manuals/desktop/use-desktop/kubernetes.md)
  - 添加实验性 SOCKS 服务器以允许访问容器网络，参见 [docker/for-mac#2670](https://github.com/docker/for-mac/issues/2670#issuecomment-372365274)。另见 [docker/for-mac#2721](https://github.com/docker/for-mac/issues/2721)
  - 为运行 macOS 10.13.4 及更高版本的用户重新启用 raw 作为默认磁盘格式。注意：此更改仅在“恢复出厂设置”或“删除所有数据”（从鲸鱼菜单 -> 偏好设置 -> 重置）后生效。相关问题：[docker/for-mac#2625](https://github.com/docker/for-mac/issues/2625)

* Bug 修复和小改动
  - Docker Desktop 中 AUFS 存储驱动已弃用，AUFS 支持将在下一个主要版本中移除。您可以在 Docker Desktop 18.06.x 中继续使用 AUFS，但在更新到下一个主要版本之前需要重置磁盘镜像（在偏好设置 > 重置菜单中）。您可以查看文档以[保存镜像](/reference/cli/docker/image/save/#examples)和[备份卷](/manuals/engine/storage/volumes.md#back-up-restore-or-migrate-data-volumes)
  - macOS El Captain 10.11 在 Docker Desktop 中已弃用。您将无法在 Docker Desktop 18.06.x 之后安装更新。我们建议升级到最新版本的 macOS。
  - 修复导致 VM 日志在某些情况下写入 RAM 而非磁盘以及 VM 挂起的错误。参见 [docker/for-mac#2984](https://github.com/docker/for-mac/issues/2984)
  - 修复由 haproxy TCP 健康检查触发的网络连接泄漏。[docker/for-mac#1132](https://github.com/docker/for-mac/issues/1132)
  - 当 vmnetd 被禁用时，提供更好的消息以重置它。参见 [docker/for-mac#3035](https://github.com/docker/for-mac/issues/3035)
  - 修复 VPNKit 内存泄漏。修复 [moby/vpnkit#371](https://github.com/moby/vpnkit/issues/371)
  - 虚拟机默认磁盘路径相对于 $HOME 存储。修复 [docker/for-mac#2928](https://github.com/docker/for-mac/issues/2928)、[docker/for-mac#1209](https://github.com/docker/for-mac/issues/1209)
  - 使用 Simple NTP 以最小化 VM 和主机之间的时钟漂移。修复 [docker/for-mac#2076](https://github.com/docker/for-mac/issues/2076)
  - 修复 stat 调用文件和 close 文件描述符引用该文件之间的竞争，这可能导致 stat 失败并返回 EBADF（通常显示为“文件未找到”）。修复 [docker/for-mac#2870](https://github.com/docker/for-mac/issues/2870)
  - 不允许在 macOS Yosemite 10.10 上安装 Docker for Mac，此版本自 Docker for Mac 17.09.0 起不再支持。
  - 修复重置对话框窗口中的按钮顺序。修复 [docker/for-mac#2827](https://github.com/docker/for-mac/issues/2827)
  - 修复从预 17.12 版本直接升级后 Docker for Mac 无法重启的问题。修复 [docker/for-mac#2739](https://github.com/docker/for-mac/issues/2739)
  - 为虚拟机内的 docker-ce 日志添加日志轮转。

### Docker Community Edition 18.03.1-ce-mac65 2018-04-30

* 升级
  - [Docker 18.03.1-ce](https://github.com/docker/docker-ce/releases/tag/v18.03.1-ce)
  - [Docker Compose 1.21.1](https://github.com/docker/compose/releases/tag/1.21.1)
  - [Notary 0.6.1](https://github.com/docker/notary/releases/tag/v0.6.1)

* Bug 修复和小改动
  - 修复由于套接字文件路径过长（通常是 HOME 文件夹路径过长）导致 Docker for Mac 无法启动的问题。修复 [docker/for-mac#2727](https://github.com/docker/for-mac/issues/2727)、[docker/for-mac#2731](https://github.com/docker/for-mac/issues/2731)。

### Docker Community Edition 18.03.1-ce-mac64 2018-04-26

* 升级
  - [Docker 18.03.1-ce](https://github.com/docker/docker-ce/releases/tag/v18.03.1-ce)
  - [Docker Compose 1.21.0](https://github.com/docker/compose/releases/tag/1.21.0)
  - [Notary 0.6.1](https://github.com/docker/notary/releases/tag/v0.6.1)

* Bug 修复和小改动
  - 修复由于套接字文件路径过长（通常是 HOME 文件夹路径过长）导致 Docker for Mac 无法启动的问题。修复 [docker/for-mac#2727](https://github.com/docker/for-mac/issues/2727)、[docker/for-mac#2731](https://github.com/docker/for-mac/issues/2731)。

### Docker Community Edition 18.03.0-ce-mac60 2018-03-30

* Bug 修复和小改动
  - 修复从 17.09 版本直接升级后 Docker for Mac 无法重启的问题。修复 [docker/for-mac#2739](https://github.com/docker/for-mac/issues/2739)

### Docker Community Edition 18.03.0-ce-mac59 2018-03-26

* 升级
  - [Docker 18.03.0-ce](https://github.com/docker/docker-ce/releases/tag/v18.03.0-ce)
  - [Docker Machine 0.14.0](https://github.com/docker/machine/releases/tag/v0.14.0)
  - [Docker Compose 1.20.1](https://github.com/docker/compose/releases/tag/1.20.1)
  - [Notary 0.6.0](https://github.com/docker/notary/releases/tag/v0.6.0)
  - Linux Kernel 4.9.87
  - AUFS 20180312

* 新增功能
  - VM 交换大小可以在设置中更改。参见 [docker/for-mac#2566](https://github.com/docker/for-mac/issues/2566)、[docker/for-mac#2389](https://github.com/docker/for-mac/issues/2389)
  - 新的菜单项用于重启 Docker。
  - 支持 NFS 卷共享。
  - 存储磁盘镜像的目录已重命名（从 `~/Library/Containers/com.docker.docker/Data/com.docker.driver.amd64-linux` 到 `~/Library/Containers/com.docker.docker/Data/vms/0`）。

* Bug 修复和小改动
  - 修复设置 TLS 相关选项时守护进程无法正确启动的问题。修复 [docker/for-mac#2663](https://github.com/docker/for-mac/issues/2663)
  - 容器内解析主机时应使用 DNS 名称 `host.docker.internal`。较旧的别名（仍然有效）已弃用，推荐使用此名称。（参见 https://tools.ietf.org/html/draft-west-let-localhost-be-localhost-06）
  - 修复使用“localhost”名称（例如 `host.docker.internal`）时 HTTP/S 透明代理的问题。
  - 修复偏好设置守护进程面板中错误添加的空注册表。修复 [docker/for-mac#2537](https://github.com/docker/for-mac/issues/2537)
  - 检测到不兼容的硬件时提供更清晰的错误消息。
  - 修复某些情况下在出错后选择“重置”无法正确重置的问题。
  - 修复 NTP 配置不正确的问题。修复 [docker/for-mac#2529](https://github.com/docker/for-mac/issues/2529)
  - Docker For Mac 安装程序中不再建议迁移 Docker Toolbox 镜像（仍可手动迁移 Toolbox 镜像）。

### Docker Community Edition 17.12.0-ce-mac55 2018-02-27

* Bug 修复和小改动
  - 将运行 macOS 10.13（High Sierra）的用户默认磁盘格式恢复为 qcow2。已确认使用 raw 格式在 APFS 上使用稀疏文件会导致文件损坏。注意：此更改仅在恢复出厂设置后生效（从鲸鱼菜单 -> 偏好设置 -> 重置）。相关问题：[docker/for-mac#2625](https://github.com/docker/for-mac/issues/2625)
  - 修复 vpnkit 代理 docker.for.mac.http.internal 的问题。

### Docker Community Edition 17.12.0-ce-mac49 2018-01-19

* Bug 修复和小改动
  - 修复在某些情况下调整/创建 Docker.raw 磁盘镜像时出错的问题。修复 [docker/for-mac#2383](https://github.com/docker/for-mac/issues/2383)、[docker/for-mac#2447](https://github.com/docker/for-mac/issues/2447)、[docker/for-mac#2453](https://github.com/docker/for-mac/issues/2453)、[docker/for-mac#2420](https://github.com/docker/for-mac/issues/2420)
  - 修复额外分配的磁盘空间在容器中不可用的问题。修复 [docker/for-mac#2449](https://github.com/docker/for-mac/issues/2449)
  - Vpnkit 端口最大空闲时间默认值恢复为 300 秒。修复 [docker/for-mac#2442](https://github.com/docker/for-mac/issues/2442)
  - 修复使用带身份验证的 HTTP 代理的问题。修复 [docker/for-mac#2386](https://github.com/docker/for-mac/issues/2386)
  - 允许 HTTP 代理排除列表写成 .docker.com 而不是 *.docker.com
  - 允许将单个 IP 地址添加到 HTTP 代理排除列表中。
  - 避免在查询 docker.for.mac.* 时，当上游 DNS 服务器缓慢或缺失时触发 DNS 超时。

### Docker Community Edition 17.12.0-ce-mac47 2018-01-12

* Bug 修复和小改动
  - 修复推送到不安全注册表的 `docker push` 问题。修复 [docker/for-mac#2392](https://github.com/docker/for-mac/issues/2392)
  - 分别使用内部端口代理 HTTP 和 HTTPS 内容。

### Docker Community Edition 17.12.0-ce-mac46 2018-01-09

* 升级
  - [Docker 17.12.0-ce](https://github.com/docker/docker-ce/releases/tag/v17.12.0-ce)
  - [Docker Compose 1.18.0](https://github.com/docker/compose/releases/tag/1.18.0)
  - [Docker Machine 0.13.0](https://github.com/docker/machine/releases/tag/v0.13.0)
  - Linux Kernel 4.9.60

* 新增功能
  - VM 完全使用 LinuxKit 构建
  - VM 磁盘大小可以在磁盘偏好设置中更改。（参见 [docker/for-mac#1037](https://github.com/docker/for-mac/issues/1037)）
  - 对于在 High Sierra 上运行 APFS 的系统，SSD 默认使用 `raw` 格式的 VM 磁盘。这提高了磁盘吞吐量（在 2015 年 MacBook Pro 上，`dd` 从 320MiB/sec 提升到 600MiB/sec）和磁盘空间处理。
    现有磁盘保持 qcow 格式，如果您想切换到 raw 格式，需要“删除所有数据”或“恢复出厂默认设置”。
  - 容器内解析主机时应使用 DNS 名称 `docker.for.mac.host.internal` 而不是 `docker.for.mac.localhost`（仍然有效），因为存在禁止使用 localhost 子域的 RFC。参见 https://tools.ietf.org/html/draft-west-let-localhost-be-localhost-06。

* Bug 修复和小改动
  - 在关于框中显示各种组件版本。
  - 更改主机代理设置时避免 VM 重启。
  - 不要通过外部代理转发容器间的 HTTP 流量，以免破坏流量。（参见 [docker/for-mac#981](https://github.com/docker/for-mac/issues/981)）
  - 文件共享设置现在存储在 settings.json 中。
  - 守护进程重启按钮已移至设置 / 重置选项卡。
  - 改进 VM 崩溃时的 VM 状态处理和错误消息。
  - 修复具有证书问题的私有仓库登录问题。（参见 [docker/for-mac#2201](https://github.com/docker/for-mac/issues/2201)）

## 2017 年的稳定版本

### Docker Community Edition 17.09.1-ce-mac42 2017-12-11

* 升级
  - [Docker 17.09.1-ce](https://github.com/docker/docker-ce/releases/tag/v17.09.1-ce)
  - [Docker Compose 1.17.1](https://github.com/docker/compose/releases/tag/1.17.1)
  - [Docker Machine 0.13.0](https://github.com/docker/machine/releases/tag/v0.13.0)

* Bug 修复和小改动
  - 修复在某些情况下无法移动 qcow 磁盘的错误。

### Docker Community Edition 17.09.0-ce-mac35 2017-10-06

* Bug 修复
  - 修复 Docker For Mac 无法启动的问题：移除了有时导致 vpnkit 进程死亡的 libgmp 使用。

### Docker Community Edition 17.09.0-ce-mac33 2017-10-03
  - 当存在现有 Docker For Mac 数据时，不显示 Toolbox 迁移助手。

### Docker Community Edition 17.09.0-ce-mac32 2017-10-02

* 升级
  - [Docker 17.09.0-ce](https://github.com/docker/docker-ce/releases/tag/v17.09.0-ce)
  - [Docker Compose 1.16.1](https://github.com/docker