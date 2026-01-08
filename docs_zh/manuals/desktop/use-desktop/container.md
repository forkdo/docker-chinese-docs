---
description: 通过 Docker Dashboard 的“容器”视图了解您可以执行的操作
keywords: Docker Dashboard, manage, containers, gui, dashboard, images, user manual
title: 探索 Docker Desktop 中的“容器”视图
linkTitle: 容器
weight: 10
---

“容器”视图列出了所有正在运行和已停止的容器和应用程序。它提供了一个简洁的界面来管理容器的生命周期、与运行中的应用程序交互以及检查 Docker 对象（包括 Docker Compose 应用程序）。

## 容器操作

使用**搜索**字段按名称查找特定容器。

在**容器**视图中，您可以：
- 启动、停止、暂停、恢复或重启容器
- 查看镜像包和 CVEs
- 删除容器
- 在 VS Code 中打开应用程序
- 在浏览器中打开容器暴露的端口
- 复制 `docker run` 命令以便重复使用或修改
- 使用 [Docker Debug](#execdebug)

## 资源使用情况

在**容器**视图中，您可以监控您的容器随时间变化的 CPU 和内存使用情况。这可以帮助您了解容器是否存在问题或是否需要分配额外资源。

当您[检查一个容器](#inspect-a-container)时，**统计**选项卡会显示更多关于容器资源利用情况的信息。您可以查看您的容器随时间推移使用了多少 CPU、内存、网络和磁盘空间。

## 检查容器

当您选择一个容器时，可以获取其详细信息。

在这里，您可以使用快捷操作按钮来执行各种操作，例如暂停、恢复、启动或停止，或者探索**日志**、**检查**、**绑定挂载**、**调试**、**文件**和**统计**选项卡。

### 日志

选择**日志**以实时查看容器的输出。查看日志时，您可以：

- 使用 `Cmd + f`/`Ctrl + f` 打开搜索栏并查找特定条目。
  匹配的搜索结果会以黄色高亮显示。
- 按 `Enter` 或 `Shift + Enter` 可分别跳转到下一个或上一个搜索匹配项。
- 使用右上角的**复制**图标将所有日志复制到您的剪贴板。
- 显示时间戳
- 使用右上角的**清空终端**图标清空日志终端。
- 选择并查看日志中可能存在的外部链接。

您可以通过以下方式优化视图：

- 如果您正在运行多容器应用程序，可以筛选特定容器的日志。
- 使用正则表达式或精确匹配的搜索词

### 检查

选择**检查**以查看有关容器的底层信息。它会显示本地路径、镜像版本号、SHA-256、端口映射以及其他详细信息。

### Exec/调试

如果您尚未在设置中启用 Docker Debug，则会显示 **Exec** 选项卡。它允许您在正在运行的容器中快速运行命令。

使用 **Exec** 选项卡等同于运行以下命令之一：

- `docker exec -it <container-id> /bin/sh`
- 访问 Windows 容器时使用 `docker exec -it <container-id> cmd.exe`

更多详情，请参阅 [`docker exec` CLI 参考文档](/reference/cli/docker/exec/)。

如果您已在设置中启用 Docker Debug，或已开启选项卡右侧的**调试模式**，则会显示**调试**选项卡。

调试模式具有多项优势，例如：

- 一个可定制的工具箱。该工具箱预装了许多标准 Linux 工具，例如 `vim`、`nano`、`htop` 和 `curl`。更多详情，请参阅 [`docker debug` CLI 参考文档](/reference/cli/docker/debug/)。
- 能够访问没有 Shell 的容器，例如 slim 或 distroless 容器。

要使用调试模式：

- 将鼠标悬停在正在运行的容器上，在**操作**列中选择**显示容器操作**菜单。从下拉菜单中，选择**使用 Docker Debug**。
- 或者，选择容器，然后选择**调试**选项卡。

要默认使用调试模式，请导航到**设置**中的**通用**选项卡，然后选择**默认启用 Docker Debug**选项。

### 文件

选择**文件**以探索正在运行或已停止容器的文件系统。您还可以：

- 查看最近添加、修改或删除的文件
- 直接通过内置编辑器编辑文件
- 在主机和容器之间拖放文件和文件夹
- 右键单击文件时删除不必要的文件
- 直接将文件和文件夹从容器下载到主机

## 其他资源

- [什么是容器](/get-started/docker-concepts/the-basics/what-is-a-container.md)
- [运行多容器应用程序](/get-started/docker-concepts/running-containers/multi-container-applications.md)