---
description: 关于 Docker Engine 在 SLES 上的可用性信息。Docker 软件包不再适用于 SLES s390x 架构。
keywords: sles, 安装, 卸载, 升级, 更新, s390x, ibm-z, 不支持, 不可用
title: Docker Engine 在 SLES (s390x) 上
linkTitle: SLES (s390x)
weight: 70
toc_max: 4
aliases:
- /ee/docker-ee/sles/
- /ee/docker-ee/suse/
- /engine/installation/linux/docker-ce/sles/
- /engine/installation/linux/docker-ee/sles/
- /engine/installation/linux/docker-ee/suse/
- /engine/installation/linux/sles/
- /engine/installation/linux/SUSE/
- /engine/installation/linux/suse/
- /engine/installation/sles/
- /engine/installation/SUSE/
- /install/linux/docker-ce/sles/
- /install/linux/docker-ee/sles/
- /install/linux/docker-ee/suse/
- /install/linux/sles/
- /installation/sles/
---

## Docker Engine 不再适用于 SLES

> [!IMPORTANT]
>
> Docker Engine 软件包已**不再提供**给 **s390x** 架构（IBM Z）上的 SUSE Linux Enterprise Server (SLES)。

IBM 已决定停止为 SLES s390x 系统构建和提供 Docker Engine 软件包。Docker Inc. 从未直接构建这些软件包，仅参与了其部署工作。

## 这意味着什么

- 无法为 SLES s390x 安装新的 Docker Engine
- 现有安装将继续工作，但不会收到更新
- 将不再提供新版本或安全更新
- 面向 SLES s390x 的 Docker 软件包仓库已不再维护

## 如果您当前安装了 Docker

如果您当前在 SLES s390x 系统上安装了 Docker Engine：

- 您现有的 Docker 安装将继续正常运行
- 将无法获得自动更新
- 您应相应地规划您的容器化需求
- 请考虑运行无更新软件所带来的安全影响

## 后续步骤

如对此决定或替代方案有疑问，请联系 IBM 支持。