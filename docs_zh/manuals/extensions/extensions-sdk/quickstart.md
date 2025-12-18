---
title: 快速开始
description: 快速构建扩展的指南
keywords: 快速开始, 扩展
aliases:
 - desktop/extensions-sdk/tutorials/initialize/
 - /desktop/extensions-sdk/quickstart/
weight: 20
---

请按照本指南开始创建一个基本的 Docker 扩展。快速开始指南会自动为您生成样板文件。

## 前置条件

- [Docker Desktop](/manuals/desktop/release-notes.md)
- [NodeJS](https://nodejs.org/)
- [Go](https://go.dev/dl/)

> [!NOTE]
>
> NodeJS 和 Go 仅在您按照快速开始指南创建扩展时需要。它使用 `docker extension init` 命令自动生成样板文件。此命令使用基于 ReactJS 和 Go 应用程序的模板。

在 Docker Desktop 设置中，确保您可以安装正在开发的扩展。您可能需要导航到 Docker Desktop 设置中的 **Extensions** 选项卡，并取消选中 **Allow only extensions distributed through the Docker Marketplace**。

## 步骤一：设置目录

要设置目录，请使用 `init` 子命令并提供扩展的名称。

```console
$ docker extension init <my-extension>
```

该命令会询问您关于扩展的一系列问题，例如其名称、描述以及您的 Hub 仓库名称。这有助于 CLI 为您生成一组样板文件。它将样板文件存储在 `my-extension` 目录中。

自动生成的扩展包含：

- `backend` 文件夹中的 Go 后端服务，监听套接字。它有一个端点 `/hello` 返回 JSON 负载。
- `frontend` 文件夹中的 React 前端，可以调用后端并输出后端的响应。

有关构建 UI 的更多信息和指南，请参阅 [Design and UI styling 部分](design/design-guidelines.md)。

## 步骤二：构建扩展

要构建扩展，请移至新创建的目录并运行：

```console
$ docker build -t <name-of-your-extension> .
```

`docker build` 构建扩展并生成一个图像，图像名称与所选的 hub 仓库相同。例如，如果您在回答以下问题时输入了 `john/my-extension`：

```console
? Hub repository (eg. namespace/repository on hub): john/my-extension`
```

`docker build` 会生成一个名为 `john/my-extension` 的图像。

## 步骤三：安装并预览扩展

要在 Docker Desktop 中安装扩展，请运行：

```console
$ docker extension install <name-of-your-extension>
```

要在 Docker Desktop 中预览扩展，安装完成后，您应该在 **Extensions** 菜单下看到一个 **Quickstart** 项。选择此项会打开扩展的前端。

> [!TIP]
>
> 在 UI 开发期间，使用热重载来测试您的更改而不必重新构建整个扩展会很有帮助。更多信息请参阅 [Preview whilst developing the UI](dev/test-debug.md#hot-reloading-whilst-developing-the-ui)。

您可能还想检查属于扩展的容器。默认情况下，扩展容器在 Docker Dashboard 中是隐藏的。您可以在 **Settings** 中更改此设置，更多信息请参阅 [how to show extension containers](dev/test-debug.md#show-the-extension-containers)。

## 步骤四：提交并发布您的扩展到 Marketplace

如果您希望所有 Docker Desktop 用户都能使用您的扩展，您可以提交它以在 Marketplace 中发布。更多信息请参阅 [Publish](extensions/_index.md)。

## 清理

要删除扩展，请运行：

```console
$ docker extension rm <name-of-your-extension>
```

## 接下来

- 为您的扩展构建更高级的 [前端](build/frontend-extension-tutorial.md)。
- 了解如何 [测试和调试](dev/test-debug.md) 您的扩展。
- 了解如何为您的扩展 [设置 CI](dev/continuous-integration.md)。
- 了解有关扩展 [架构](architecture/_index.md) 的更多信息。
- 了解有关 [设计 UI](design/design-guidelines.md) 的更多信息。