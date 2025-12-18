---
description: Docker Desktop for Windows 旧版本的发布说明
keywords: Docker Desktop for Windows, 发布说明
title: 早期版本的发布说明
toc_min: 1
toc_max: 2
aliases:
- /desktop/windows/release-notes/archive/
sitemap: false
---

本页面包含 Docker Desktop for Windows 较旧版本的发布说明。

## 2018 年的稳定版本

### Docker Community Edition 18.06.1-ce-win73 2018-08-29

* 升级
  - [Docker 18.06.1-ce](https://github.com/docker/docker-ce/releases/tag/v18.06.1-ce)

* 错误修复和小改动
  - 修复了 VM 活动检测中的错误，导致 Docker Desktop 无法启动。修复 [docker/for-win#2404](https://github.com/docker/for-win/issues/2404)
  - 修复了 Windows 服务未运行时的检测错误，并建议重启服务。
  - 修复了容器内本地 DNS 解析失败的问题。修复 [docker/for-win#2301](https://github.com/docker/for-win/issues/2301)、[docker/for-win#2304](https://github.com/docker/for-win/issues/2304)
  - 修复重置为出厂默认设置后 Kubernetes 状态显示的问题
  - 修复了在某些情况下 `host.docker.internal` 无法解析的错误。修复 [docker/for-win#2402](https://github.com/docker/for-win/issues/2402)
  - 使用 1MB 的 vhdx 块大小，而不是默认的 32MB。参见 [docker/for-win#244](https://github.com/docker/for-win/issues/244)。另见 [Microsoft 在 Hyper-V 上运行 Linux 的最佳实践](https://docs.microsoft.com/en-us/windows-server/virtualization/hyper-v/best-practices-for-running-linux-on-hyper-v)
  - 在 Windows 服务未启动的特定情况下改进诊断。
  - 更改了 samba 的默认文件权限，以避免权限过宽的问题。修复 [docker/for-win#2170](https://github.com/docker/for-win/issues/2170)
  - 在 RS5 预览版中，修复了错误检测缺少 "Containers" 功能的问题，不再需要安装该功能后重启。

### Docker Community Edition 18.06.0-ce-win72 2018-07-26

* 新增
  - 更新了签名证书。安装程序可能会显示 Windows Defender 弹窗，直到更新的证书被加入白名单。点击 "更多信息" 查看应用发布者为 "Docker Inc"，然后运行。

* 错误修复和小改动
  - 修复了在启动 Docker Desktop 时，如果 Windows 功能 "Hyper-V" 和 "Containers" 未启用，自动启用功能的错误。

### Docker Community Edition 18.06.0-ce-win70 2018-07-25

* 升级
  - [Docker 18.06.0-ce](https://github.com/docker/docker-ce/releases/tag/v18.06.0-ce)
  - [Docker Machine 0.15.0](https://github.com/docker/machine/releases/tag/v0.15.0)
  - [Docker Compose 1.22.0](https://github.com/docker/compose/releases/tag/1.22.0)
  - [LinuxKit v0.4](https://github.com/linuxkit/linuxkit/releases/tag/v0.4)
  - Linux Kernel 4.9.93，启用 CEPH、DRBD、RBD、MPLS_ROUTING 和 MPLS_IPTUNNEL

* 新增
  - Kubernetes 支持。现在可以从 Docker for Windows 设置中的 "Kubernetes" 窗格运行单节点 Kubernetes 集群，并使用 kubectl 命令和 Docker 命令。参见 [Kubernetes 部分](/manuals/desktop/use-desktop/kubernetes.md)

* 错误修复和小改动
  - Docker Desktop 中 AUFS 存储驱动已弃用，将在下一个主要版本中移除 AUFS 支持。您可以在 Docker Desktop 18.06.x 中继续使用 AUFS，但在更新到下一个主要版本之前需要重置磁盘映像（在设置 > 重置菜单中）。您可以查看文档以[保存镜像](/reference/cli/docker/image/save/#examples)和[备份卷](/manuals/engine/storage/volumes.md#back-up-restore-or-migrate-data-volumes)
  - 修复了在某些情况下会导致虚拟机日志写入 RAM 而非磁盘，以及虚拟机挂起的错误。
  - 修复了 docker 服务命名管道连接的安全问题。
  - 修复了 VPNKit 内存泄漏。修复 [docker/for-win#2087](https://github.com/docker/for-win/issues/2087)、[moby/vpnkit#371](https://github.com/moby/vpnkit/issues/371)
  - 修复了在最新的 1709 Windows 更新上使用 Windows 快速启动时的重启问题。修复 [docker/for-win#1741](https://github.com/docker/for-win/issues/1741)、[docker/for-win#1741](https://github.com/docker/for-win/issues/1741)
  - DNS 名称 `host.docker.internal` 现在可用于从 Windows 容器解析主机。修复 [docker/for-win#1976](https://github.com/docker/for-win/issues/1976)
  - 修复了诊断窗口中的断开链接。
  - 为虚拟机内的 docker-ce 日志添加了日志轮转。
  - 更改了 smb 权

[Response interrupted by a subsequent message. Only one message may be generated at a time.]