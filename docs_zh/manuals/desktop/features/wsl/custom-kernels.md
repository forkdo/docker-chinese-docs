---
title: 在 WSL 上使用自定义内核
description: 在 WSL 2 上将自定义内核与 Docker Desktop 配合使用
keywords: wsl, docker desktop, custom kernel
tags: [最佳实践, 故障排除]
---

Docker Desktop 依赖于 Microsoft 分发的默认 WSL 2 Linux 内核中内置的若干内核特性。因此，在 WSL 2 上将自定义内核与 Docker Desktop 一起使用并未得到官方支持，并且可能导致 Docker Desktop 启动或运行时出现问题。

不过，在某些情况下可能需要运行自定义内核；Docker Desktop 不会阻止其使用，并且已有用户报告成功使用自定义内核的案例。

如果您选择使用自定义内核，建议从 Microsoft 从其[官方仓库](https://github.com/microsoft/WSL2-Linux-Kernel)分发的内核源码开始，然后在此基础上添加所需的特性。

此外，还建议您：
- 使用与最新 WSL2 版本分发的内核相同的内核版本。您可以在终端中运行 `wsl.exe --system uname -r` 来查找版本。
- 从 Microsoft 在其[仓库](https://github.com/microsoft/WSL2-Linux-Kernel)提供的默认内核配置开始，并在此基础上添加所需的特性。
- 确保您的内核构建环境包含 `pahole`，并且其版本在相应的内核配置（`CONFIG_PAHOLE_VERSION`）中正确反映。