---
title: 杀毒软件与 Docker
description: 在 Docker 中使用杀毒软件的一般指南
keywords: antivirus, security
---

当杀毒软件扫描 Docker 使用的文件时，这些文件可能会以某种方式被锁定，从而导致 Docker 命令挂起。

减少这些问题的一种方法是将 Docker 数据目录（Linux 上为 `/var/lib/docker`，Windows Server 上为 `%ProgramData%\docker`，或 Mac 上为 `$HOME/Library/Containers/com.docker.docker/`）添加到杀毒软件的排除列表中。然而，这样做有一个权衡：Docker 镜像、容器的可写层或卷中的病毒或恶意软件将无法被检测到。如果您确实选择从后台病毒扫描中排除 Docker 数据目录，您可能需要安排一个定期任务来停止 Docker、扫描数据目录，然后重新启动 Docker。