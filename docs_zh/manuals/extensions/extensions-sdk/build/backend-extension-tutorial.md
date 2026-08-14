---
title: 为你的扩展添加后端
description: 了解如何为你的扩展添加后端。
keywords: Docker, extensions, sdk, build
aliases:
 - /desktop/extensions-sdk/tutorials/minimal-backend-extension/
 - /desktop/extensions-sdk/build/minimal-backend-extension/
 - /desktop/extensions-sdk/build/set-up/backend-extension-tutorial/
 - /desktop/extensions-sdk/build/backend-extension-tutorial/
---

你的扩展可以附带一个后端部分，前端可以与之交互。本页提供关于为什么以及如何添加后端的信息。

在开始之前，请确保你已经安装了最新版本的 [Docker Desktop](https://www.docker.com/products/docker-desktop/)。

> Tip
>
> 查看 [快速入门指南](../quickstart.md) 和 `docker extension init <my-extension>`。它们为你的扩展提供了更好的基础，因为它们
> 更新且与你安装的 Docker Desktop 相关。

## 为什么要添加后端？（Why add a backend?）

得益于 Docker Extensions SDK，大多数情况下你应该能直接从 [前端](frontend-extension-tutorial.md#use-the-extension-apis-client)
通过 Docker CLI 完成你需要的操作。

尽管如此，有些情况下你可能需要为扩展添加后端。迄今为止，扩展开发者已使用后端来：
- 将数据存储在本地数据库中，并通过 REST API 提供。
- 存储扩展状态，例如当某个按钮启动一个长时间运行的进程时，这样如果你离开扩展用户界面再返回，前端可以从中断
  处继续。

有关扩展后端的更多信息，请参阅 [架构](../architecture/_index.md#the-backend)。

## 为扩展添加后端（Add a backend to the extension）

如果你使用 `docker extension init` 命令创建了扩展，你已经有了后端设置。否则，你必须先创建一个 `vm` 目录，
包含代码并更新 Dockerfile 以将其容器化。

以下是带后端的扩展文件夹结构：

```bash
.
├── Dockerfile # (1)
├── Makefile
├── metadata.json
├── ui
    └── index.html
└── vm # (2)
    ├── go.mod
    └── main.go
```

1. 包含构建后端并将其复制到扩展容器文件系统中所需的一切。
2. 包含扩展后端代码的源文件夹。

虽然你可以从空目录或 `vm-ui extension` [示例](https://github.com/docker/extensions-sdk/tree/main/samples) 开始，但强烈建议
你从 `docker extension init` 命令开始，并更改为满足你的需求。

> [!TIP]
>
> `docker extension init` 生成的是 Go 后端。但你仍可以将其作为你自己扩展的起点，并使用任何其他语言，如 Node.js、
> Python、Java、.Net 或任何其他语言和框架。

在本教程中，后端服务仅暴露一个路由，返回一条说 "Hello" 的 JSON 负载。

```json
{ "Message": "Hello" }
```

> [!IMPORTANT]
>
> 我们建议前端和后端通过套接字（在 Windows 上为命名管道）而非 HTTP 进行通信。这可以防止与主机上运行的任何其他
> 应用程序或容器发生端口冲突。此外，一些 Docker Desktop 用户运行在受限环境中，无法在机器上打开端口。为后端选择
> 语言和框架时，请确保它支持套接字连接。

{{< tabs group="lang" >}}
{{< tab name="Go" >}}

```go
package main

import (
	"flag"
	"log"
	"net"
	"net/http"
	"os"

	"github.com/labstack/echo"
	"github.com/sirupsen/logrus"
)

func main() {
	var socketPath string
	flag.StringVar(&socketPath, "socket", "/run/guest/volumes-service.sock", "Unix domain socket to listen on")
	flag.Parse()

	os.RemoveAll(socketPath)

	logrus.New().Infof("Starting listening on %s\n", socketPath)
	router := echo.New()
	router.HideBanner = true

	startURL := ""

	ln, err := listen(socketPath)
	if err != nil {
		log.Fatal(err)
	}
	router.Listener = ln

	router.GET("/hello", hello)

	log.Fatal(router.Start(startURL))
}

func listen(path string) (net.Listener, error) {
	return net.Listen("unix", path)
}

func hello(ctx echo.Context) error {
	return ctx.JSON(http.StatusOK, HTTPMessageBody{Message: "hello world"})
}

type HTTPMessageBody struct {
	Message string
}
```

{{< /tab >}}
{{< tab name="Node" >}}

> [!IMPORTANT]
>
> 我们目前还没有 Node 的可运行示例。[填写表单](https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&entry.25798127=Node)
> 让我们知道你是否想要 Node 的示例。

{{< /tab >}}
{{< tab name="Python" >}}

> [!IMPORTANT]
>
> 我们目前还没有 Python 的可运行示例。[填写表单](https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&entry.25798127=Python)
> 让我们知道你是否想要 Python 的示例。

{{< /tab >}}
{{< tab name="Java" >}}

> [!IMPORTANT]
>
> 我们目前还没有 Java 的可运行示例。[填写表单](https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&entry.25798127=Java)
> 让我们知道你是否想要 Java 的示例。

{{< /tab >}}
{{< tab name=".NET" >}}

> [!IMPORTANT]
>
> 我们目前还没有 .NET 的可运行示例。[填写表单](https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&entry.25798127=.Net)
> 让我们知道你是否想要 .NET 的示例。

{{< /tab >}}
{{< /tabs >}}

## 调整 Dockerfile（Adapt the Dockerfile）

> [!NOTE]
>
> 使用 `docker extension init` 时，它会创建一个已经包含 Go 后端所需内容的 `Dockerfile`。

{{< tabs group="lang" >}}
{{< tab name="Go" >}}

要在安装扩展时部署你的 Go 后端，你首先需要配置 `Dockerfile`，使其：
- 构建后端应用程序
- 将二进制文件复制到扩展的容器文件系统
- 在容器启动时启动二进制文件，监听扩展的套接字

> [!TIP]
>
> 为简化版本管理，你可以复用相同的镜像来构建前端、构建后端服务并打包扩展。

```dockerfile
# syntax=docker/dockerfile:1
FROM node:17.7-alpine3.14 AS client-builder
# ... build frontend application

# Build the Go backend
FROM golang:1.17-alpine AS builder
ENV CGO_ENABLED=0
WORKDIR /backend
RUN --mount=type=cache,target=/go/pkg/mod \
    --mount=type=cache,target=/root/.cache/go-build \
    --mount=type=bind,source=vm/.,target=. \
    go build -trimpath -ldflags="-s -w" -o bin/service

FROM alpine:3.15
# ... add labels and copy the frontend application

COPY --from=builder /backend/bin/service /
CMD /service -socket /run/guest-services/extension-allthethings-extension.sock
```

{{< /tab >}}
{{< tab name="Node" >}}

> [!IMPORTANT]
>
> 我们目前还没有 Node 的可运行 Dockerfile。[填写表单](https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&entry.25798127=Node)
> 让我们知道你是否想要 Node 的 Dockerfile。

{{< /tab >}}
{{< tab name="Python" >}}

> [!IMPORTANT]
>
> 我们目前还没有 Python 的可运行 Dockerfile。[填写表单](https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&entry.25798127=Python)
> 让我们知道你是否想要 Python 的 Dockerfile。

{{< /tab >}}
{{< tab name="Java" >}}

> [!IMPORTANT]
>
> 我们目前还没有 Java 的可运行 Dockerfile。[填写表单](https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&entry.25798127=Java)
> 让我们知道你是否想要 Java 的 Dockerfile。

{{< /tab >}}
{{< tab name=".NET" >}}

> [!IMPORTANT]
>
> 我们目前还没有 .Net 的可运行 Dockerfile。[填写表单](https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&entry.25798127=.Net)
> 让我们知道你是否想要 .Net 的 Dockerfile。

{{< /tab >}}
{{< /tabs >}}

## 配置元数据文件（Configure the metadata file）

要在 Docker Desktop 的 VM 中启动扩展的后端服务，你必须在 `metadata.json` 文件的 `vm` 段落中配置镜像名。

```json
{
  "vm": {
    "image": "${DESKTOP_PLUGIN_IMAGE}"
  },
  "icon": "docker.svg",
  "ui": {
    ...
  }
}
```

有关 `metadata.json` 的 `vm` 段落的更多信息，请参阅 [元数据](../architecture/metadata.md)。

> [!WARNING]
>
> 不要替换 `metadata.json` 文件中的 `${DESKTOP_PLUGIN_IMAGE}` 占位符。该占位符在安装扩展时会自动替换为正确的镜像名。

## 从前端调用扩展后端（Invoke the extension backend from your frontend）

使用 [高级前端扩展示例](frontend-extension-tutorial.md)，我们可以调用扩展后端。

使用 Docker Desktop Client 对象，然后通过 `ddClient.extension.vm.service.get` 调用后端服务的 `/hello` 路由，它返回
响应的主体。

{{< tabs group="framework" >}}
{{< tab name="React" >}}

用以下代码替换 `ui/src/App.tsx` 文件：

```tsx

// ui/src/App.tsx
import React, { useEffect, useState } from 'react';
import { createDockerDesktopClient } from "@docker/extension-api-client";

//obtain docker desktop extension client
const ddClient = createDockerDesktopClient();

export function App() {
  const [hello, setHello] = useState<string>();

  useEffect(() => {
    const getHello = async () => {
      const result = await ddClient.extension.vm?.service?.get('/hello');
      setHello(JSON.stringify(result));
    }
    getHello()
  }, []);

  return (
    <Typography>{hello}</Typography>
  );
}

```

{{< /tab >}}
{{< tab name="Vue" >}}

> [!IMPORTANT]
>
> 我们目前还没有 Vue 的示例。[填写表单](https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&entry.1333218187=Vue)
> 让我们知道你是否想要 Vue 的示例。

{{< /tab >}}
{{< tab name="Angular" >}}

> [!IMPORTANT]
>
> 我们目前还没有 Angular 的示例。[填写表单](https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&entry.1333218187=Angular)
> 让我们知道你是否想要 Angular 的示例。

{{< /tab >}}
{{< tab name="Svelte" >}}

> [!IMPORTANT]
>
> 我们目前还没有 Svelte 的示例。[填写表单](https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&entry.1333218187=Svelte)
> 让我们知道你是否想要 Svelte 的示例。

{{< /tab >}}
{{< /tabs >}}

## 重新构建扩展并更新它（Re-build the extension and update it）

由于你已修改了扩展的配置并在 Dockerfile 中添加了阶段，你必须重新构建扩展。

```bash
docker build --tag=awesome-inc/my-extension:latest .
```

构建完成后，你需要更新它，或者如果尚未安装则安装它。

```bash
docker extension update awesome-inc/my-extension:latest
```

现在你可以在 Docker Desktop 仪表盘的 **容器（Containers）** 视图中看到后端服务正在运行，并在需要调试时查看日志。

> [!TIP]
>
> 你可能需要打开 **设置（Settings）** 中的 **显示系统容器（Show system containers）** 选项才能看到后端容器在运行。
> 有关更多信息，请参阅 [显示扩展容器](../dev/test-debug.md#show-the-extension-containers)。

打开 Docker Desktop 仪表盘并选择 **容器（Containers）** 标签页。你应该会看到来自后端服务调用的响应显示出来。

## 接下来？（What's next?）

- 了解如何 [共享和发布你的扩展](../extensions/_index.md)。
- 了解更多关于扩展 [架构](../architecture/_index.md)。
