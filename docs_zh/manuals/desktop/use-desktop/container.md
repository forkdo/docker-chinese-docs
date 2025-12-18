---
description: 了解如何使用 Docker Dashboard 上的 Containers 视图
keywords: Docker Dashboard, 管理, 容器, GUI, 仪表板, 镜像, 用户手册
title: 探索 Docker Desktop 中的 Containers 视图
linkTitle: 容器
weight: 10
---

**Containers** 视图列出了所有运行中和已停止的容器及应用程序。它提供了一个清晰的界面，用于管理容器的生命周期、与运行中的应用程序交互，以及检查 Docker 对象（包括 Docker Compose 应用）。

## 容器操作

使用 **Search** 字段可以通过名称查找特定容器。

在 **Containers** 视图中，您可以：
- 启动、停止、暂停、恢复或重启容器
- 查看镜像包和 CVE 信息
- 删除容器
- 在 VS Code 中打开应用程序
- 在浏览器中打开容器暴露的端口
- 复制 `docker run` 命令以供重用或修改
- 使用 [Docker Debug](#execdebug)

## 资源使用情况

在 **Containers** 视图中，您可以监控容器随时间的 CPU 和内存使用情况。这有助于您判断容器是否存在问题，或是否需要分配更多资源。

当您[检查容器](#inspect-a-container)时，**Stats** 选项卡会显示容器资源利用情况的详细信息。您可以查看容器随时间推移使用的 CPU、内存、网络和磁盘空间。

## 检查容器

选择容器后，您可以获取其详细信息。

在这里，您可以使用快速操作按钮执行各种操作，如暂停、恢复、启动或停止，或浏览 **Logs**、**Inspect**、**Bind mounts**、**Debug**、**Files** 和 **Stats** 选项卡。

### 日志

选择 **Logs** 可实时查看容器输出。查看日志时，您可以：
- 使用 `Cmd + f`/`Ctrl + f` 打开搜索栏，查找特定条目。搜索匹配项会以黄色高亮显示。
- 按 `Enter` 或 `Shift + Enter` 分别跳到下一个或上一个搜索匹配项。
- 使用右上角的 **Copy** 图标将所有日志复制到剪贴板。
- 显示时间戳
- 使用右上角的 **Clear terminal** 图标清除日志终端。
- 选择并查看日志中可能存在的外部链接。

您可以通过以下方式优化视图：
- 过滤特定容器的日志，如果您运行的是多容器应用程序。
- 使用正则表达式或精确匹配搜索词

### 检查

选择 **Inspect** 可查看容器的底层信息。它显示本地路径、镜像版本号、SHA-256、端口映射等详细信息。

### 执行/调试

如果未在设置中启用 Docker Debug，将显示 **Exec** 选项卡。它允许您快速在运行中的容器内执行命令。

使用 **Exec** 选项卡等同于运行以下命令之一：
- `docker exec -it <container-id> /bin/sh`
- 访问 Windows 容器时：`docker exec -it <container-id> cmd.exe`

详细信息请参阅 [`docker exec` CLI 参考](/reference/cli/docker/exec/)。

如果已在设置中启用 Docker Debug，或在选项卡右侧切换了 **Debug mode**，将显示 **Debug** 选项卡。

调试模式具有多个优势，例如：
- 可自定义的工具箱。工具箱预装了许多标准 Linux 工具，如 `vim`、`nano`、`htop` 和 `curl`。详细信息请参阅 [`docker debug` CLI 参考](/reference/cli/docker/debug/)。
- 可访问没有 shell 的容器，例如精简或无发行版容器。

使用调试模式的方法：
- 将鼠标悬停在运行中的容器上，在 **Actions** 列中选择 **Show container actions** 菜单。从下拉菜单中选择 **Use Docker Debug**。
- 或选择容器，然后选择 **Debug** 选项卡。

要默认使用调试模式，请导航到 **Settings** 的 **General** 选项卡，选择 **Enable Docker Debug by default** 选项。

### 文件

选择 **Files** 可浏览运行中或已停止容器的文件系统。您还可以：
- 查看最近添加、修改或删除的文件
- 直接在内置编辑器中编辑文件
- 在主机和容器之间拖放文件和文件夹
- 右键单击文件删除不需要的文件
- 直接从容器下载文件和文件夹到主机

## 附加资源

- [什么是容器](/get-started/docker-concepts/the-basics/what-is-a-container.md)
- [运行多容器应用程序](/get-started/docker-concepts/running-containers/multi-container-applications.md)