---
description: 了解暂停 Docker Desktop 仪表板的含义
keywords: Docker Desktop Dashboard, 管理, 容器, GUI, 仪表板, 暂停, 用户手册
title: 暂停 Docker Desktop
weight: 70
---

暂停 Docker Desktop 会临时挂起运行 Docker Engine 的 Linux 虚拟机。这会将所有容器的当前状态保存在内存中，并冻结所有正在运行的进程，显著降低 CPU 和内存使用量，有助于节省笔记本电脑的电池电量。

要暂停 Docker Desktop，请在 Docker 仪表板的页脚左侧选择 **暂停** 图标。要手动恢复 Docker Desktop，可选择 Docker 菜单中的 **恢复** 选项，或运行任何 Docker CLI 命令。

当你手动暂停 Docker Desktop 时，Docker 菜单和 Docker Desktop 仪表板上会显示暂停状态。你仍然可以访问 **设置** 和 **故障排除** 菜单。

> [!TIP]
>
> Resource Saver 功能默认启用，相比手动暂停功能，能提供更好的 CPU 和内存节省效果。更多信息请参阅 [Resource Saver 模式](resource-saver.md)。