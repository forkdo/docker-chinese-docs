---
title: 容器安全常见问题
linkTitle: 容器
description: 关于 Docker 容器安全和隔离的常见问题
keywords: 容器安全, docker desktop 隔离, 增强容器隔离, 文件共享
weight: 20
tags: [FAQ]
aliases:
- /faq/security/containers/
---

## Docker Desktop 中容器如何与主机隔离？

Docker Desktop 在一个定制的 Linux 虚拟机内运行所有容器（原生 Windows 容器除外）。这在容器与主机之间提供了强大的隔离性，即使容器以 root 身份运行也是如此。

需要考虑的重要因素包括：

- 容器只能访问通过 Docker Desktop 设置配置为文件共享的主机文件
- 容器默认在 Docker Desktop VM 内以 root 身份运行，但权限受限
- 特权容器（`--privileged`、`--pid=host`、`--cap-add`）在 VM 内以提升的权限运行，使其能够访问 VM 内部和 Docker Engine

启用增强容器隔离（Enhanced Container Isolation）后，每个容器在 Docker Desktop VM 内的专用 Linux 用户命名空间中运行。即使特权容器也仅在其容器边界内拥有特权，而无法访问 VM。ECI 使用先进技术防止容器突破 Docker Desktop VM 和 Docker Engine。

## 容器可以访问主机文件系统的哪些部分？

容器只能访问以下主机文件：

1. 通过 Docker Desktop 设置共享的文件
1. 显式绑定挂载到容器中的文件（例如 `docker run -v /path/to/host/file:/mnt`）

## 以 root 身份运行的容器能否访问主机上管理员拥有的文件？

不能。主机文件共享使用用户空间文件服务器（在 `com.docker.backend` 中以 Docker Desktop 用户身份运行），因此容器只能访问 Docker Desktop 用户已有权限访问的文件。