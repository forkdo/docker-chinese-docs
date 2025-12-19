---
description: 了解 Docker Desktop 资源节省模式及其配置方法
keywords: Docker 仪表板, 资源节省, 管理, 容器, 图形界面, 仪表板, 用户手册
title: Docker Desktop 的资源节省模式
linkTitle: 资源节省模式
weight: 60
---

资源节省模式通过在没有容器运行一段时间后自动停止 Docker Desktop Linux 虚拟机，可显著降低主机上 Docker Desktop 的 CPU 和内存使用率，降幅可达 2 GB 或更多。默认时间为 5 分钟，但您可以根据需要进行调整。

在资源节省模式下，Docker Desktop 在空闲时使用最少的系统资源，从而帮助您延长笔记本电脑的电池续航时间并改善多任务处理体验。

## 配置资源节省模式

资源节省模式默认已启用，但您可以通过导航到**设置**中的**资源**选项卡来禁用它。您还可以按照下图所示配置空闲计时器。

![资源节省设置](../images/resource-saver-settings.webp)

如果提供的值无法满足您的需求，您可以将其重新配置为任何大于 30 秒的值，方法是更改 Docker Desktop 的 `settings-store.json` 文件（Docker Desktop 4.34 及更早版本为 `settings.json`）中的 `autoPauseTimeoutSeconds`：

  - Mac: `~/Library/Group Containers/group.com.docker/settings-store.json`
  - Windows: `C:\Users\[USERNAME]\AppData\Roaming\Docker\settings-store.json`
  - Linux: `~/.docker/desktop/settings-store.json`

重新配置后无需重启 Docker Desktop。

当 Docker Desktop 进入资源节省模式时：
- 月亮图标会显示在 Docker Desktop 状态栏以及系统托盘中的 Docker 图标上。
- 不运行容器的 Docker 命令（例如列出容器镜像或卷）不一定会触发退出资源节省模式，因为 Docker Desktop 可以在不唤醒 Linux 虚拟机的情况下处理这些命令。

> [!注意]
>
> 当需要时，Docker Desktop 会自动退出资源节省模式。
> 导致退出资源节省模式的命令执行时间会稍长一些（约 3 到 10 秒），因为 Docker Desktop 需要重启 Linux 虚拟机。
> 在 Mac 和 Linux 上通常更快，在 Windows 上使用 Hyper-V 时较慢。
> 一旦 Linux 虚拟机重启，后续的容器运行将立即照常进行。

## 资源节省模式与暂停模式的对比

资源节省模式的优先级高于较旧的[暂停](pause.md)功能，这意味着当 Docker Desktop 处于资源节省模式时，无法手动暂停 Docker Desktop（而且由于资源节省模式实际上会停止 Docker Desktop Linux 虚拟机，手动暂停也没有意义）。通常，我们建议保持资源节省模式启用，而不是禁用它并使用手动暂停功能，因为这样可以实现更好的 CPU 和内存节省效果。

## Windows 上的资源节省模式

在 Windows 上使用 WSL 时，资源节省模式的工作方式略有不同。它不会停止 WSL 虚拟机，而只是暂停 `docker-desktop` WSL 发行版内的 Docker 引擎。这是因为在 WSL 中，所有 WSL 发行版共享单个 Linux 虚拟机，因此 Docker Desktop 无法停止 Linux 虚拟机（即 WSL Linux 虚拟机不归 Docker Desktop 所有）。因此，资源节省模式会降低 WSL 上的 CPU 使用率，但不会降低 Docker 的内存使用率。

为了降低 WSL 上的内存使用率，我们建议用户启用 WSL 的 `autoMemoryReclaim` 功能，如 [Docker Desktop WSL 文档](/manuals/desktop/features/wsl/_index.md)中所述。最后，由于 Docker Desktop 在 WSL 上不会停止 Linux 虚拟机，因此退出资源节省模式是即时的（没有退出延迟）。