---
description: 扩展
keywords: Docker 扩展, Docker Desktop, Linux, Mac, Windows,
title: 非市场扩展
weight: 20
aliases:
 - /desktop/extensions/non-marketplace/
---

## 安装市场中不可用的扩展

> [!WARNING]
>
> 未在扩展市场中上架的扩展未经过 Docker 的审核流程。
> 扩展可以安装二进制文件、执行命令并访问您机器上的文件。安装这些扩展需自行承担风险。

扩展市场是通过 Docker Desktop 安装扩展的可信且官方的场所。这些扩展已通过 Docker 的审核流程。但是，如果您信任扩展作者，也可以在 Docker Desktop 中安装其他扩展。

鉴于 Docker 扩展的性质（即 Docker 镜像），您可能会在其他地方找到用户发布的扩展源代码。例如在 GitHub、GitLab，甚至托管在 DockerHub 或 GHCR 等镜像仓库中。
您可以安装由社区或公司内部同事开发的扩展。您不仅限于仅从市场安装扩展。

> [!NOTE]
>
> 确保 **仅允许通过 Docker 市场分发的扩展** 选项已禁用。否则，这会阻止安装任何未在市场中列出的扩展（通过扩展 SDK 工具）。
> 您可以在 **设置** 中更改此选项。

要安装市场中不存在的扩展，您可以使用 Docker Desktop 捆绑的扩展 CLI。

在终端中，输入 `docker extension install IMAGE[:TAG]` 通过镜像引用和可选的标签安装扩展。使用 `-f` 或 `--force` 标志可避免交互式确认。

转到 Docker Desktop 仪表板查看新安装的扩展。

## 列出已安装的扩展

无论扩展是从市场安装还是通过扩展 CLI 手动安装，您都可以使用 `docker extension ls` 命令显示已安装扩展的列表。
作为输出的一部分，您将看到扩展 ID、提供者、版本、标题以及它是否运行后端容器或已向主机部署二进制文件，例如：

```console
$ docker extension ls
ID                  PROVIDER            VERSION             UI                    VM                  HOST
john/my-extension   John                latest              1 tab(My-Extension)   Running(1)          -
```

转到 Docker Desktop 仪表板，选择 **添加扩展**，然后在 **管理** 选项卡中查看新安装的扩展。
请注意，会显示 `UNPUBLISHED`（未发布）标签，表示该扩展未从市场安装。

## 更新扩展

要更新市场中不存在的扩展，在终端中输入 `docker extension update IMAGE[:TAG]`，其中 `TAG` 应与已安装的扩展不同。

例如，如果您使用 `docker extension install john/my-extension:0.0.1` 安装了扩展，则可以通过运行 `docker extension update john/my-extension:0.0.2` 来更新它。
转到 Docker Desktop 仪表板查看更新后的扩展。

> [!NOTE]
>
> 未通过市场安装的扩展不会收到来自 Docker Desktop 的更新通知。

## 卸载扩展

要卸载市场中不存在的扩展，您可以通过以下两种方式操作：导航到市场中的 **管理** 选项卡并选择 **卸载** 按钮，或在终端中输入 `docker extension uninstall IMAGE[:TAG]`。