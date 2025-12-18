---
title: 扩展架构
linkTitle: 架构
description: Docker 扩展架构
keywords: Docker, extensions, sdk, metadata
aliases: 
 - /desktop/extensions-sdk/architecture/
weight: 50
---

扩展是运行在 Docker Desktop 内部的应用程序。它们被打包为 Docker 镜像，通过 Docker Hub 分发，并由用户通过 Docker Desktop 仪表板内的 Marketplace 或 Docker Extensions CLI 安装。

扩展可以由三个（可选的）组件组成：
- 前端（或用户界面）：在 Docker Desktop 仪表板的标签页中显示的 Web 应用
- 后端：一个或多个在 Docker Desktop 虚拟机中容器化的服务
- 可执行文件：Docker Desktop 在安装扩展时复制到主机上的 Shell 脚本或二进制文件

![扩展的三个组件概述](images/extensions-architecture.png?w=600h=400)

扩展不一定需要包含所有这些组件，而是根据扩展功能至少需要其中一个。Docker Desktop 使用 `metadata.json` 文件来配置和运行这些组件。更多详细信息，请参阅 [metadata](metadata) 部分。

## 前端

前端本质上是一个由 HTML、Javascript 和 CSS 构成的 Web 应用。它可以由一个简单的 HTML 文件、一些原生 Javascript 或任何前端框架（如 React 或 Vue.js）构建。

当 Docker Desktop 安装扩展时，它会从扩展镜像中提取 UI 文件夹，该文件夹由 `metadata.json` 中的 `ui` 部分定义。更多详细信息，请参阅 [ui metadata 部分](metadata.md#ui-section)。

每当用户点击 **Extensions** 标签时，Docker Desktop 都会初始化扩展的 UI，就像第一次一样。当他们导航离开该标签时，UI 本身及其启动的所有子进程（如果有）都会被终止。

前端可以通过 [Extensions SDK](https://www.npmjs.com/package/@docker/extension-api-client) 调用 `docker` 命令、与扩展后端通信或调用部署在主机上的扩展可执行文件。

> [!TIP]
>
> `docker extension init` 会生成一个基于 React 的扩展。但你仍然可以将其作为起点，使用任何其他前端框架，如 Vue、Angular、Svelte 等，甚至使用原生 Javascript。

了解更多关于为你的扩展 [构建前端](/manuals/extensions/extensions-sdk/build/frontend-extension-tutorial.md) 的信息。

## 后端

除了前端应用外，扩展还可以包含一个或多个后端服务。在大多数情况下，扩展不需要后端，功能可以通过 SDK 调用 docker 命令来实现。然而，在某些情况下，扩展需要后端服务，例如：
- 运行必须比前端存活时间更长的长时间运行进程
- 在本地数据库中存储数据并通过 REST API 提供服务
- 存储扩展状态，例如当按钮启动长时间运行的进程时，这样如果你导航离开扩展再回来，前端可以从离开的地方继续
- 访问 Docker Desktop VM 中的特定资源，例如通过 compose 文件挂载文件夹

> [!TIP]
>
> `docker extension init` 会生成一个 Go 后端。但你仍然可以将其作为起点，使用任何其他语言，如 Node.js、Python、Java、.Net 或任何其他语言和框架。

通常，后端由一个在 Docker Desktop VM 内运行的容器组成。在内部，Docker Desktop 创建一个 Docker Compose 项目，从 `metadata.json` 的 `vm` 部分的 `image` 选项创建容器，并将其附加到 Compose 项目。更多详细信息，请参阅 [ui metadata 部分](metadata.md#vm-section)。

在某些情况下，可以使用 `compose.yaml` 文件而不是 `image`。当后端容器需要更多特定选项时，这很有用，例如挂载卷或请求 [capabilities](https://docs.docker.com/engine/reference/run/#runtime-privilege-and-linux-capabilities)，这些无法仅通过 Docker 镜像表达。Compose 文件也可以用于添加扩展所需的多个容器，如数据库或消息代理。注意，如果 Compose 文件定义了许多服务，SDK 只能与其中第一个通信。

> [!NOTE]
>
> 在某些情况下，从后端与 Docker 引擎交互很有用。请参阅 [如何使用 Docker 套接字](../guides/use-docker-socket-from-backend.md)。

为了与后端通信，扩展 SDK 提供了 [函数](../dev/api/backend.md#get) 来从前端发出 `GET`、`POST`、`PUT`、`HEAD` 和 `DELETE` 请求。在底层，通信通过套接字或命名管道完成，具体取决于操作系统。如果后端监听端口，将很难防止与其他已在主机或容器中运行的应用程序发生冲突。此外，一些用户在受限环境中运行 Docker Desktop，他们无法在机器上打开端口。

![后端和前端通信](images/extensions-arch-2.png?w=500h=300)

最后，后端可以使用任何技术构建，只要它能在容器中运行并在套接字上监听。

了解更多关于为你的扩展 [添加后端](/manuals/extensions/extensions-sdk/build/backend-extension-tutorial.md) 的信息。

## 可执行文件

除了前端和后端外，扩展还可以包含可执行文件。可执行文件是在安装扩展时复制到主机上的二进制文件或 Shell 脚本。前端可以使用 [扩展 SDK](../dev/api/backend.md#invoke-an-extension-binary-on-the-host) 调用它们。

当扩展需要与第三方 CLI 工具（如 AWS、`kubectl` 等）交互时，这些可执行文件非常有用。将这些可执行文件随扩展一起分发，确保 CLI 工具始终在用户机器上可用，并且版本正确。

当 Docker Desktop 安装扩展时，它会根据 `metadata.json` 中的 `host` 部分将可执行文件复制到主机上。更多详细信息，请参阅 [ui metadata 部分](metadata.md#host-section)。

![可执行文件和前端通信](images/extensions-arch-3.png?w=250h=300)

然而，由于它们在用户机器上执行，因此必须对它们运行的平台可用。例如，如果你想分发 `kubectl` 可执行文件，你需要为 Windows、Mac 和 Linux 提供不同版本。多架构镜像也需要包含为正确架构（AMD / ARM）构建的二进制文件。

更多详细信息，请参阅 [host metadata 部分](metadata.md#host-section)。

了解如何 [调用主机二进制文件](../guides/invoke-host-binaries.md)。