---
title: 在 WSL 上使用自定义内核
description: 在 WSL 2 上使用 Docker Desktop 的自定义内核
keywords: wsl, docker desktop, custom kernel
tags: [最佳实践, 故障排除]
---

Docker Desktop 依赖于 Microsoft 分发的默认 WSL 2 Linux 内核中内置的多个内核功能。因此，在 WSL 2 上为 Docker Desktop 使用自定义内核并未得到官方支持，可能会导致 Docker Desktop 启动或运行时出现问题。

但是，在某些情况下，使用自定义内核可能是必要的；Docker Desktop 不会阻止其使用，一些用户报告称使用自定义内核取得了成功。

如果您选择使用自定义内核，建议您从 Microsoft 官方 [仓库](https://github.com/microsoft/WSL2-Linux-Kernel) 分发的内核树开始，然后在该基础上添加您需要的功能。

同时建议您：
- 使用与最新 WSL2 发行版分发的相同内核版本。您可以通过在终端中运行 `wsl.exe --system uname -r` 来查找版本。
- 从 Microsoft [仓库](https://github.com/microsoft/WSL2-Linux-Kernel) 提供的默认内核配置开始，在此基础上添加您需要的功能。
- 确保您的内核构建环境中包含 `pahole`，并且其版本在相应的内核配置（`CONFIG_PAHOLE_VERSION`）中得到正确反映。