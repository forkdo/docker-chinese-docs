---
description: 有关 SLES 上 Docker Engine 可用性的信息。Docker 软件包不再适用于 SLES s390x 架构。
keywords: sles, install, uninstall, upgrade, update, s390x, ibm-z, not supported, unavailable
title: SLES (s390x) 上的 Docker Engine
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
> Docker Engine 软件包 **不再提供** 用于 **s390x** 架构（IBM Z）上的 SUSE Linux Enterprise Server (SLES)。

IBM 已决定停止构建和提供适用于 SLES s390x 系统的 Docker Engine 软件包。Docker Inc. 从未直接构建这些软件包，仅参与其部署。

## 这意味着什么

- SLES s390x 不再提供新的 Docker Engine 安装
- 现有安装将继续运行，但不会收到更新
- 不再提供新版本或安全更新
- SLES s390x 的 Docker 软件包仓库不再维护

## 如果您当前已安装 Docker

如果您当前已在 SLES s390x 系统上安装了 Docker Engine：

- 您现有的 Docker 安装将继续运行
- 不再提供自动更新
- 您应为容器化需求做好相应规划
- 请考虑运行无更新软件的安全影响

## 后续步骤

如需了解此决定或替代解决方案的问题，请联系 IBM 支持。