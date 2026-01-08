---
description: 了解暂停 Docker Desktop Dashboard 的含义
keywords: Docker Desktop Dashboard, manage, containers, gui, dashboard, pause, user manual
title: 暂停 Docker Desktop
weight: 70
---

暂停 Docker Desktop 会暂时挂起运行 Docker Engine 的 Linux 虚拟机。这将保存所有容器在内存中的当前状态，并冻结所有正在运行的进程，显著降低 CPU 和内存使用率，有助于节省笔记本电脑的电池电量。

要暂停 Docker Desktop，请在 Docker Dashboard 底部左侧选择 **Pause** 图标。要手动恢复 Docker Desktop，请选择 Docker 菜单中的 **Resume** 选项，或运行任意 Docker CLI 命令。

当您手动暂停 Docker Desktop 时，Docker 菜单和 Docker Desktop Dashboard 上会显示暂停状态。您仍然可以访问 **Settings** 和 **Troubleshoot** 菜单。

> [!TIP]
>
> 资源节省器功能默认已启用，相比手动暂停功能可提供更好的 CPU 和内存节省效果。更多信息请参见 [Resource Saver mode](resource-saver.md)。