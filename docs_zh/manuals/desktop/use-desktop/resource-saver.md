---
description: 了解 Docker Desktop 资源节省模式的原理及其配置方法
keywords: Docker Dashboard, resource saver, 管理, 容器, gui, 仪表板, 用户手册
title: Docker Desktop 的资源节省模式
linkTitle: 资源节省模式
weight: 60
---

资源节省模式通过在 Linux VM 闲置一段时间后自动停止 Docker Desktop 的 Linux VM，显著降低了 Docker Desktop 在主机上的 CPU 和内存使用量，通常可节省 2 GB 或更多的资源。默认时间设置为 5 分钟，但您可以根据需要调整此时间。

启用资源节省模式后，Docker Desktop 在空闲时使用最少的系统资源，从而帮助您节省笔记本电脑的电池电量，并改善您的多任务处理体验。

## 配置资源节省模式

资源节省模式默认启用，但您可以通过导航到 **Settings** 中的 **Resources** 选项卡来禁用它。您也可以按如下所示配置空闲计时器。

![资源节省模式设置](../images/resource-saver-settings.webp)

如果可用的选项值无法满足您的需求，您可以通过修改 Docker Desktop 的 `settings-store.json` 文件（Docker Desktop 4.34 及更早版本为 `settings.json`）中的 `autoPauseTimeoutSeconds`，将超时时间重新配置为任意值，只要该值大于 30 秒即可：

  - Mac: `~/Library/Group Containers/group.com.docker/settings-store.json`
  - Windows: `C:\Users\[USERNAME]\AppData\Roaming\Docker\settings-store.json`
  - Linux: `~/.docker/desktop/settings-store.json`

重新配置后无需重启 Docker Desktop。

当 Docker Desktop 进入资源节省模式时：
- Docker Desktop 状态栏以及系统托盘中的 Docker 图标上会显示一个月亮图标。
- 不运行容器的 Docker 命令（例如列出容器镜像或卷）不会触发退出资源节省模式，因为 Docker Desktop 可以在不唤醒 Linux VM 的情况下响应此类命令。

> [!NOTE]
>
> Docker Desktop 在需要时会自动退出资源节省模式。
> 触发退出资源节省模式的命令执行时间会稍长一些（大约 3 到 10 秒），因为 Docker Desktop 需要重启 Linux VM。
> 在 Mac 和 Linux 上通常更快，在 Windows 的 Hyper-V 上则较慢。
> Linux VM 重启后，后续的容器运行将立即正常执行。

## 资源节省模式与暂停功能的对比

资源节省模式比旧的 [暂停](pause.md) 功能具有更高的优先级，这意味着当 Docker Desktop 处于资源节省模式时，无法手动暂停 Docker Desktop（也没有必要，因为资源节省模式实际上已经停止了 Docker Desktop 的 Linux VM）。通常，我们建议保持启用资源节省模式，而不是禁用它并使用手动暂停功能，因为资源节省模式在 CPU 和内存节省方面效果更好。

## Windows 上的资源节省模式

在使用 WSL 的 Windows 上，资源节省模式的工作方式略有不同。它不会停止 WSL VM，而只是暂停 `docker-desktop` WSL 发行版内的 Docker Engine。这是因为 WSL 中有一个由所有 WSL 发行版共享的单一 Linux VM，因此 Docker Desktop 无法停止 Linux VM（即 WSL Linux VM 不归 Docker Desktop 管理）。因此，资源节省模式在 WSL 上可以降低 CPU 使用率，但不会降低 Docker 的内存使用率。

为了减少 WSL 上的内存使用，我们建议用户启用 WSL 的 `autoMemoryReclaim` 功能，具体说明请参阅 [Docker Desktop WSL 文档](/manuals/desktop/features/wsl/_index.md)。最后，由于 Docker Desktop 在 WSL 上不会停止 Linux VM，因此退出资源节省模式是即时的（没有退出延迟）。