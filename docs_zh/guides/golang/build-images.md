---
title: 构建你的 Go 镜像
linkTitle: 构建镜像
weight: 5
keywords: 容器, 镜像, go, golang, dockerfiles, 编码, 构建, 推送, 运行
description: 学习如何通过编写 Dockerfile 来构建你的第一个 Docker 镜像
aliases:
  - /get-started/golang/build-images/
  - /language/golang/build-images/
  - /guides/language/golang/build-images/
---

## 概述

在本节中，你将构建一个容器镜像。该镜像包含运行应用程序所需的一切——编译后的应用程序二进制文件、运行时、库以及应用程序所需的所有其他资源。

## 必备软件

要完成本教程，你需要以下内容：

- 本地运行的 Docker。请按照[下载和安装 Docker 的说明](/manuals/desktop/_index.md)操作。
- 一个 IDE 或文本编辑器来编辑文件。[Visual Studio Code](https://code.visualstudio.com/) 是一个免费且受欢迎的选择，但你可以使用任何你熟悉的工具。
- 一个 Git 客户端。本指南使用基于命令行的 `git` 客户端，但你可以使用任何适合你的工具。
- 一个命令行终端应用程序。本模块中的示例来自 Linux shell，但它们在 PowerShell、Windows 命令提示符或 OS X 终端中应该也能运行，只需最少的修改（如果需要的话）。

## 认识示例应用程序

示例应用程序是一个微服务的简化版本。它故意设计得很简单，以便将重点放在学习 Go 应用程序容器化的基础上。

该应用程序提供两个 HTTP 端点：

- 对于请求 `/`，它返回一个包含心形符号 (`<3`) 的字符串。
- 对于请求 `/health`，它返回 JSON `{"Status" : "OK"}`。
- 对于任何其他请求，它返回 HTTP 错误 404。

应用程序在由环境变量 `PORT` 定义的 TCP 端口上监听。默认值为 `8080`。

该应用程序是无状态的。

应用程序的完整源代码位于 GitHub：[github.com/docker/docker-gs-ping](https://github.com/docker/docker-gs-ping)。鼓励你 fork 它并随意实验。

要继续，请将应用程序仓库克隆到你的本地机器：

```console
$ git clone https://github.com/docker/docker-gs-ping
```

如果你熟悉 Go，应用程序的 `main.go` 文件很简单：

```go
package main

import (
	"net/http"
	"os"

	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
)

func main() {

	e := echo.New()

	e.Use(middleware.Logger())
	e.Use(middleware.Recover())

	e.GET("/", func(c echo.Context) error {
		return c.HTML(http.StatusOK, "Hello, Docker! <3")
	})

	e.GET("/health", func(c echo.Context) error {
		return c.JSON(http.StatusOK, struct{ Status string }{Status: "OK"})
	})

	httpPort := os.Getenv("PORT")
	if httpPort == "" {
		httpPort = "8080"
	}

	e.Logger.Fatal(e.Start(":" + httpPort))
}

// 简单的整数最小值实现
// 改编自：https://gobyexample.com/testing-and-benchmarking
func IntMin(a, b int) int {
	if a < b {
		return a
	}
	return b
}
```

## 为应用程序创建 Dockerfile

要使用 Docker 构建容器镜像，需要一个包含构建指令的 `Dockerfile`。

以（可选的）解析器指令行开始你的 `Dockerfile`，它指示 BuildKit 根据指定版本的语法语法规则来解释你的文件。

然后告诉 Docker 你希望为应用程序使用什么基础镜像：

```dockerfile
# syntax=docker/dockerfile:1

FROM golang:1.19
```

Docker 镜像可以从其他镜像继承。因此，你可以使用官方 Go 镜像，它已经包含了编译和运行 Go 应用程序所需的所有工具和库，而不需要从头创建自己的基础镜像。

> [!NOTE]
>
> 如果你对创建自己的基础镜像感兴趣，可以查看本指南的以下部分：[创建基础镜像](/manuals/build/building/base-images.md#create-a-base-image)。
> 但请注意，这对你的当前任务来说不是必需的。

现在你已经为即将构建的容器镜像定义了基础镜像，可以开始在其之上构建了。

为了在运行其余命令时更方便，创建一个位于正在构建的镜像内部的目录。这也指示 Docker 将此目录用作所有后续命令的默认目标目录。这样你就不必在 `Dockerfile` 中键入完整的文件路径，相对路径将基于此目录。

```dockerfile
WORKDIR /app
```

通常，一旦你下载了一个用 Go 编写的项目，你要做的第一件事就是安装编译它所需的模块。注意，基础镜像已经有了工具链，但你的源代码还没有。

因此，在你可以在镜像内运行 `go mod download` 之前，你需要将 `go.mod` 和 `go.sum` 文件复制到镜像中。使用 `COPY` 命令来实现这一点。

在最简单的形式中，`COPY` 命令接受两个参数。第一个参数告诉 Docker 你想要将哪些文件复制到镜像中。最后一个参数告诉 Docker 你想要将该文件复制到哪里。

将 `go.mod` 和 `go.sum` 文件复制到你的项目目录 `/app`，由于使用了 `WORKDIR`，这是镜像内的当前目录 (`./`)。与一些现代 shell 对尾部斜杠 (`/`) 似乎漠不关心（并且可以弄清楚用户的意思（大多数时候））不同，Docker 的 `COPY` 命令对尾部斜杠的解释非常敏感。

```dockerfile
COPY go.mod go.sum ./
```

> [!NOTE]
>
> 如果你想熟悉 `COPY` 命令对尾部斜杠的处理，请参阅 [Dockerfile 参考](/reference/dockerfile.md#copy)。这个尾部斜杠可能会引起比你想象中更多的问题。

现在你已经将模块文件复制到正在构建的 Docker 镜像中，你可以使用 `RUN` 命令也在那里运行 `go mod download` 命令。这与你在本地机器上运行 `go` 完全相同，但这次这些 Go 模块将安装到镜像内的目录中。

```dockerfile
RUN go mod download
```

此时，你有了一个 Go 工具链版本 1.19.x 和所有 Go 依赖项，它们都安装在正在构建的镜像中。

接下来要做的就是将你的源代码复制到镜像中。你将像之前复制模块文件一样使用 `COPY` 命令。

```dockerfile
COPY *.go ./
```

这个 `COPY` 命令使用通配符将当前目录（`Dockerfile` 所在的目录）中所有扩展名为 `.go` 的文件复制到镜像内的当前目录。

现在，要编译你的应用程序，使用熟悉的 `RUN` 命令：

```dockerfile
RUN CGO_ENABLED=0 GOOS=linux go build -o /docker-gs-ping
```

这应该很熟悉。该命令的结果将是一个静态应用程序二进制文件，名为 `docker-gs-ping`，位于正在构建的镜像文件系统的根目录中。你可以将二进制文件放在该镜像内的任何其他地方，根目录在这里没有特殊含义。只是使用它来保持文件路径简短，以提高可读性。

现在，剩下的就是告诉 Docker 当你的镜像用于启动容器时运行什么命令。

你使用 `CMD` 命令来实现这一点：

```dockerfile
CMD ["/docker-gs-ping"]
```

这是完整的 `Dockerfile`：

```dockerfile
# syntax=docker/dockerfile:1

FROM golang:1.19

# Set destination for COPY
WORKDIR /app

# Download Go modules
COPY go.mod go.sum ./
RUN go mod download

# Copy the source code. Note the slash at the end, as explained in
# https://docs.docker.com/reference/dockerfile/#copy
COPY *.go ./

# Build
RUN CGO_ENABLED=0 GOOS=linux go build -o /docker-gs-ping

# Optional:
# To bind to a TCP port, runtime parameters must be supplied to the docker command.
# But we can document in the Dockerfile what ports
# the application is going to listen on by default.
# https://docs.docker.com/reference/dockerfile/#expose
EXPOSE 8080

# Run
CMD ["/docker-gs-ping"]
```

`Dockerfile` 也可以包含注释。它们总是以 `#` 符号开始，并且必须在行的开头。注释是为了方便你记录 `Dockerfile`。

还有一个 Dockerfile 指令的概念，比如你添加的 `syntax` 指令。指令必须始终位于 `Dockerfile` 的最顶部，因此在添加注释时，请确保注释跟在你可能使用的任何指令之后：

```dockerfile
# syntax=docker/dockerfile:1
# A sample microservice in Go packaged into a container image.

FROM golang:1.19

# ...
```

## 构建镜像

现在你已经创建了 `Dockerfile`，从它构建一个镜像。`docker build` 命令从 `Dockerfile` 和上下文创建 Docker 镜像。构建上下文是位于指定路径或 URL 中的文件集。Docker 构建过程可以访问上下文中任何文件。

构建命令可选地接受一个 `--tag` 标志。此标志用于用人类易于阅读和识别的字符串值标记镜像。如果你不传递 `--tag`，Docker 将使用 `latest` 作为默认值。

构建你的第一个 Docker 镜像。

```console
$ docker build --tag docker-gs-ping .
```

构建过程将在执行构建步骤时打印一些诊断消息。以下是这些消息可能看起来像什么的示例。

```console
[+] Building 2.2s (15/15) FINISHED
 => [internal] load build definition from Dockerfile                                                                                       0.0s
 => => transferring dockerfile: 701B                                                                                                       0.0s
 => [internal] load .dockerignore                                                                                                          0.0s
 => => transferring context: 2B                                                                                                            0.0s
 => resolve image config for docker.io/docker/dockerfile:1                                                                                 1.1s
 => CACHED docker-image://docker.io/docker/dockerfile:1@sha256:39b85bbfa7536a5feceb7372a0817649ecb2724562a38360f4d6a7782a409b14            0.0s
 => [internal] load build definition from Dockerfile                                                                                       0.0s
 => [internal] load .dockerignore                                                                                                          0.0s
 => [internal] load metadata for docker.io/library/golang:1.19                                                                             0.7s
 => [1/6] FROM docker.io/library/golang:1.19@sha256:5d947843dde82ba1df5ac1b2ebb70b203d106f0423bf5183df3dc96f6bc5a705                       0.0s
 => [internal] load build context                                                                                                          0.0s
 => => transferring context: 6.08kB                                                                                                        0.0s
 => CACHED [2/6] WORKDIR /app                                                                                                              0.0s
 => CACHED [3/6] COPY go.mod go.sum ./                                                                                                     0.0s
 => CACHED [4/6] RUN go mod download                                                                                                       0.0s
 => CACHED [5/6] COPY *.go ./                                                                                                              0.0s
 => CACHED [6/6] RUN CGO_ENABLED=0 GOOS=linux go build -o /docker-gs-ping                                                                  0.0s
 => exporting to image                                                                                                                     0.0s
 => => exporting layers                                                                                                                    0.0s
 => => writing image sha256:ede8ff889a0d9bc33f7a8da0673763c887a258eb53837dd52445cdca7b7df7e3                                               0.0s
 => => naming to docker.io/library/docker-gs-ping                                                                                          0.0s
```

你的确切输出会有所不同，但只要没有错误，你应该在第一行输出中看到 `FINISHED`。这意味着 Docker 已成功构建了名为 `docker-gs-ping` 的镜像。

## 查看本地镜像

要在本地机器上查看镜像列表，你有两个选择。一种是使用 CLI，另一种是使用 [Docker Desktop](/manuals/desktop/_index.md)。既然你现在正在终端中工作，那就看看如何使用 CLI 列出镜像。

要列出镜像，运行 `docker image ls` 命令（或 `docker images` 缩写）：

```console
$ docker image ls

REPOSITORY                       TAG       IMAGE ID       CREATED         SIZE
docker-gs-ping                   latest    7f153fbcc0a8   2 minutes ago   1.11GB
...
```

你的确切输出可能有所不同，但你应该看到带有 `latest` 标签的 `docker-gs-ping` 镜像。因为你没有在构建镜像时指定自定义标签，Docker 假定标签将是 `latest`，这是一个特殊值。

## 标记镜像

镜像名称由斜杠分隔的名称组件组成。名称组件可能包含小写字母、数字和分隔符。分隔符定义为句点、一个或两个下划线，或一个或多个破折号。名称组件不能以分隔符开头或结尾。

镜像由清单和图层列表组成。简单来说，标签指向这些工件的组合。你可以为镜像有多个标签，事实上，大多数镜像都有多个标签。为构建的镜像创建第二个标签，然后查看其图层。

使用 `docker image tag` 命令（或 `docker tag` 缩写）为镜像创建新标签。此命令接受两个参数；第一个参数是源镜像，第二个是新标签。以下命令为构建的 `docker-gs-ping:latest` 创建新的 `docker-gs-ping:v1.0` 标签：

```console
$ docker image tag docker-gs-ping:latest docker-gs-ping:v1.0
```

Docker `tag` 命令为镜像创建新标签。它不会创建新镜像。标签指向同一镜像，只是引用镜像的另一种方式。

现在再次运行 `docker image ls` 命令以查看更新的本地镜像列表：

```console
$ docker image ls

REPOSITORY                       TAG       IMAGE ID       CREATED         SIZE
docker-gs-ping                   latest    7f153fbcc0a8   6 minutes ago   1.11GB
docker-gs-ping                   v1.0      7f153fbcc0a8   6 minutes ago   1.11GB
...
```

你可以看到你有两个以 `docker-gs-ping` 开头的镜像。如果你查看 `IMAGE ID` 列，可以看到两个镜像的值相同。这个值是 Docker 用于标识镜像的唯一标识符。

删除刚刚创建的标签。为此，你将使用 `docker image rm` 命令，或缩写 `docker rmi`（代表 "remove image"）：

```console
$ docker image rm docker-gs-ping:v1.0
Untagged: docker-gs-ping:v1.0
```

注意，Docker 的响应告诉你镜像没有被删除，只是被取消了标签。

通过运行以下命令验证这一点：

```console
$ docker image ls
```

你会看到 `v1.0` 标签不再在 Docker 实例维护的镜像列表中。

```text
REPOSITORY                       TAG       IMAGE ID       CREATED         SIZE
docker-gs-ping                   latest    7f153fbcc0a8   7 minutes ago   1.11GB
...
```

标签 `v1.0` 已被删除，但你仍然在机器上有 `docker-gs-ping:latest` 标签，所以镜像还在那里。

## 多阶段构建

你可能已经注意到你的 `docker-gs-ping` 镜像重量超过一吉字节，这对于一个小型编译的 Go 应用程序来说是很大的。你也可能在想，构建镜像后，完整的 Go 工具套件（包括编译器）发生了什么。

答案是完整的工具链仍然在那里，在容器镜像中。这不仅因为大文件大小而不方便，而且当容器部署时也可能带来安全风险。

这两个问题可以通过使用[多阶段构建](/manuals/build/building/multi-stage.md)来解决。

简而言之，多阶段构建可以将一个构建阶段的工件携带到另一个阶段，每个构建阶段都可以从不同的基础镜像实例化。

因此，在以下示例中，你将使用一个全功能的官方 Go 镜像来构建你的应用程序。然后你将应用程序二进制文件复制到另一个基础非常精简且不包含 Go 工具链或其他可选组件的镜像中。

示例应用程序仓库中的 `Dockerfile.multistage` 包含以下内容：

```dockerfile
# syntax=docker/dockerfile:1

# Build the application from source
FROM golang:1.19 AS build-stage

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY *.go ./

RUN CGO_ENABLED=0 GOOS=linux go build -o /docker-gs-ping

# Run the tests in the container
FROM build-stage AS run-test-stage
RUN go test -v ./...

# Deploy the application binary into a lean image
FROM gcr.io/distroless/base-debian11 AS build-release-stage

WORKDIR /

COPY --from=build-stage /docker-gs