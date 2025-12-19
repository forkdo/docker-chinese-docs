---
description: 扩展
keywords: Docker Extensions, Docker Desktop, Linux, Mac, Windows,
title: 非 Marketplace 扩展
weight: 20
aliases:
 - /desktop/extensions/non-marketplace/
---

## 安装未在 Marketplace 中提供的扩展

> [!WARNING]
>
> 未在 Marketplace 中的 Docker Extensions 未经过 Docker 的审核流程。
> 扩展可以安装二进制文件、执行命令并访问您机器上的文件。安装这些扩展需自行承担风险。

扩展 Marketplace 是在 Docker Desktop 内安装扩展的可信且官方的场所。这些扩展已通过 Docker 的审核流程。但是，如果您信任扩展作者，也可以在 Docker Desktop 中安装其他扩展。

鉴于 Docker Extension 的本质（即 Docker 镜像），您可以在其他地方找到用户发布的扩展源代码。例如在 GitHub、GitLab，甚至托管在 DockerHub 或 GHCR 等镜像仓库中。
您可以安装由社区或公司内部同事开发的扩展。您并不局限于仅从 Marketplace 安装扩展。

> [!NOTE]
>
> 确保 **仅允许通过 Docker Marketplace 分发的扩展** 选项已禁用。否则，将阻止安装任何未在 Marketplace 中列出的扩展，即使通过 Extension SDK 工具也无法安装。
> 您可以在 **设置** 中更改此选项。

要安装未在 Marketplace 中提供的扩展，您可以使用 Docker Desktop 自带的 Extensions CLI。

在终端中，输入 `docker extension install IMAGE[:TAG]` 以镜像引用和可选的标签安装扩展。使用 `-f` 或 `--force` 标志可避免交互式确认。

转到 Docker Desktop 仪表板查看新安装的扩展。

## 列出已安装的扩展

无论扩展是从 Marketplace 安装还是通过 Extensions CLI 手动安装，您都可以使用 `docker extension ls` 命令显示已安装扩展的列表。
作为输出的一部分，您将看到扩展 ID、提供者、版本、标题，以及它是否运行后端容器或已向主机部署二进制文件，例如：

```console
$ docker extension ls
ID                  PROVIDER            VERSION             UI                    VM                  HOST
john/my-extension   John                latest              1 tab(My-Extension)   Running(1)          -
```

转到 Docker Desktop 仪表板，选择 **添加扩展**，然后在 **管理** 选项卡中查看新安装的扩展。
请注意，会显示 `UNPUBLISHED` 标签，表示该扩展未从 Marketplace 安装。

## 更新扩展

要更新未在 Marketplace 中提供的扩展，在终端中输入 `docker extension update IMAGE[:TAG]`，其中 `TAG` 应与已安装的扩展不同。

例如，如果您使用 `docker extension install john/my-extension:0.0.1` 安装了扩展，则可以通过运行 `docker extension update john/my-extension:0.0.2` 来更新它。
转到 Docker Desktop 仪表板查看更新后的扩展。

> [!NOTE]
>
> 未通过 Marketplace 安装的扩展不会收到来自 Docker Desktop 的更新通知。

## 卸载扩展

要卸载未在 Marketplace 中提供的扩展，您可以导航到 Marketplace 中的 **管理** 选项卡并选择 **卸载** 按钮，或者在终端中输入 `docker extension uninstall IMAGE[:TAG]`。