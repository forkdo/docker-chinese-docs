---
title: 容器安全常见问题
linkTitle: Container
description: 关于 Docker 容器安全性和隔离性的常见问题
keywords: container security, docker desktop isolation, enhanced container isolation, file sharing
weight: 20
tags:
- FAQ
aliases:
- /faq/security/containers/
---

## Docker Desktop 中的容器如何与主机隔离？

Docker Desktop 在定制的 Linux 虚拟机中运行所有容器（原生 Windows 容器除外）。这为容器与主机之间提供了强大的隔离，即使容器以 root 身份运行也是如此。

需要注意的重要事项包括：

- 容器可以通过 Docker Desktop 设置访问配置为文件共享的主机文件
- 默认情况下，容器在 Docker Desktop VM 内以 root 身份运行，但权限受限
- 特权容器（`--privileged`、`--pid=host`、`--cap-add`）在 VM 内以提升的权限运行，从而可以访问 VM 内部和 Docker Engine

启用增强容器隔离（Enhanced Container Isolation）后，每个容器在 Docker Desktop VM 内的专用 Linux 用户命名空间中运行。即使是特权容器，其权限也仅限于容器边界内，而非整个 VM。ECI 采用先进技术防止容器突破 Docker Desktop VM 和 Docker Engine。

## 容器可以访问主机文件系统的哪些部分？

容器只能访问以下主机文件：

1. 使用 Docker Desktop 设置共享的文件
2. 明确绑定挂载到容器中的文件（例如 `docker run -v /path/to/host/file:/mnt`）

## 以 root 身份运行的容器能否访问主机上管理员拥有的文件？

不能。主机文件共享使用用户空间文件服务器（以 Docker Desktop 用户身份在 `com.docker.backend` 中运行），因此容器只能访问 Docker Desktop 用户已有权限访问的文件。