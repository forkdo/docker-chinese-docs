# 构建您的 Go 镜像

## 概述

在本节中，您将构建一个容器镜像。该镜像包含了运行应用程序所需的一切——编译后的应用程序二进制文件、运行时、库以及应用程序所需的所有其他资源。

## 所需软件

要完成本教程，您需要以下内容：

- 本地运行的 Docker。请遵循[下载并安装 Docker 的说明](/manuals/desktop/_index.md)。
- 用于编辑文件的 IDE 或文本编辑器。[Visual Studio Code](https://code.visualstudio.com/) 是一个免费且流行的选择，但您可以使用任何您觉得顺手的工具。
- Git 客户端。本指南使用基于命令行的 `git` 客户端，但您可以自由使用任何适合您的工具。
- 命令行终端应用程序。本模块中显示的示例来自 Linux shell，但只需极少的修改（如果需要的话），它们就可以在 PowerShell、Windows 命令提示符或 OS X 终端中工作。

## 认识示例应用程序

示例应用程序是一个微服务的夸张简化版。它的目的是保持简单，以便专注于学习 Go 应用程序容器化的基础知识。

该应用程序提供两个 HTTP 端点：

- 对 `/` 的请求会响应一个包含心形符号 (`<3`) 的字符串。
- 对 `/health` 的请求会响应 `{"Status" : "OK"}` JSON。

它对任何其他请求响应 HTTP 错误 404。

该应用程序监听由环境变量 `PORT` 的值定义的 TCP 端口。默认值为 `8080`。

该应用程序是无状态的。

应用程序的完整源代码在 GitHub 上：[github.com/docker/docker-gs-ping](https://github.com/docker/docker-gs-ping)。鼓励您将其 Fork 并随意进行实验。

要继续，请将应用程序仓库克隆到您的本地机器：

```console
$ git clone https://github.com/docker/docker-gs-ping
```

如果您熟悉 Go，应用程序的 `main.go` 文件非常直观：

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

// 整数最小值的简单实现
// 改编自: https://gobyexample.com/testing-and-benchmarking
func IntMin(a, b int) int {
	if a < b {
		return a
	}
	return b
}
```

## 为应用程序创建 Dockerfile

要使用 Docker 构建容器镜像，需要一个包含构建指令的 `Dockerfile`。

在您的 `Dockerfile` 开头使用（可选的）解析器指令行，指示 BuildKit 根据指定版本的语法的语法规则来解释您的文件。

然后告诉 Docker 您希望为您的应用程序使用什么基础镜像：

```dockerfile
# syntax=docker/dockerfile:1

FROM golang:1.19
```

Docker 镜像可以从其他镜像继承。因此，您可以使用官方的 Go 镜像，而不是从头开始创建自己的基础镜像，该镜像已经包含了编译和运行 Go 应用程序所需的所有工具和库。

> [!NOTE]
>
> 如果您对创建自己的基础镜像感到好奇，可以查看本指南的以下部分：[创建基础镜像](/manuals/build/building/base-images.md#create-a-base-image)。
> 但是请注意，继续完成手头的任务并不需要这样做。

现在您已经为即将构建的容器镜像定义了基础镜像，您可以开始在其基础上进行构建。

为了在运行其余命令时更轻松，请在您正在构建的镜像中创建一个目录。这也会指示 Docker 将此目录用作所有后续命令的默认目标位置。这样您就不必在 `Dockerfile` 中键入完整的文件路径，相对路径将基于此目录。

```dockerfile
WORKDIR /app
```

通常，下载用 Go 编写的项目后，首先要做的就是安装编译所需的模块。请注意，基础镜像已经包含了工具链，但您的源代码尚未在其中。

因此，在镜像内部运行 `go mod download` 之前，您需要将 `go.mod` 和 `go.sum` 文件复制到其中。使用 `COPY` 命令来完成此操作。

最简单的形式下，`COPY` 命令接受两个参数。第一个参数告诉 Docker 您想要将哪些文件复制到镜像中。最后一个参数告诉 Docker 您希望将该文件复制到哪里。

将 `go.mod` 和 `go.sum` 文件复制到您的项目目录 `/app` 中，由于您使用了 `WORKDIR`，该目录是镜像中的当前目录 (`./`)。与一些对使用尾部斜杠 (`/`) 似乎无所谓的现代 shell 不同，Docker 的 `COPY` 命令在解释尾部斜杠时相当敏感。

```dockerfile
COPY go.mod go.sum ./
```

> [!NOTE]
>
> 如果您想熟悉 `COPY` 命令对尾部斜杠的处理，请参阅 [Dockerfile 参考](/reference/dockerfile.md#copy)。这个尾部斜杠可能以您无法想象的方式导致问题。

现在您已经将模块文件放入正在构建的 Docker 镜像中，您可以使用 `RUN` 命令在其中运行 `go mod download` 命令。这与在本地机器上运行 `go` 完全相同，但这次这些 Go 模块将被安装到镜像内的一个目录中。

```dockerfile
RUN go mod download
```

此时，您的镜像中已经安装了 Go 工具链版本 1.19.x 和所有 Go 依赖项。

接下来要做的是将您的源代码复制到镜像中。您将像之前处理模块文件一样使用 `COPY` 命令。

```dockerfile
COPY *.go ./
```

此 `COPY` 命令使用通配符将主机上当前目录（`Dockerfile` 所在的目录）中所有扩展名为 `.go` 的文件复制到镜像中的当前目录。

现在，要编译您的应用程序，请使用熟悉的 `RUN` 命令：

```dockerfile
RUN CGO_ENABLED=0 GOOS=linux go build -o /docker-gs-ping
```

这应该很熟悉。该命令的结果将是一个名为 `docker-gs-ping` 的静态应用程序二进制文件，位于您正在构建的镜像的文件系统根目录中。您可以将二进制文件放入该镜像中您想要的任何其他位置，根目录在这方面没有特殊含义。使用它只是为了方便地保持文件路径简短，以提高可读性。

现在，剩下要做的就是告诉 Docker 在使用您的镜像启动容器时要运行什么命令。

您使用 `CMD` 命令来完成此操作：

```dockerfile
CMD ["/docker-gs-ping"]
```

以下是完整的 `Dockerfile`：

```dockerfile
# syntax=docker/dockerfile:1

FROM golang:1.19

# 设置 COPY 的目标目录
WORKDIR /app

# 下载 Go 模块
COPY go.mod go.sum ./
RUN go mod download

# 复制源代码。注意末尾的斜杠，如 https://docs.docker.com/reference/dockerfile/#copy 中所述
COPY *.go ./

# 构建
RUN CGO_ENABLED=0 GOOS=linux go build -o /docker-gs-ping

# 可选：
# 要绑定到 TCP 端口，必须向 docker 命令提供运行时参数。
# 但我们可以在 Dockerfile 中记录应用程序默认监听的端口。
# https://docs.docker.com/reference/dockerfile/#expose
EXPOSE 8080

# 运行
CMD ["/docker-gs-ping"]
```

`Dockerfile` 也可以包含注释。它们总是以 `#` 符号开头，并且必须位于行的开头。注释是为了方便您，允许您记录您的 `Dockerfile`。

还有 Dockerfile 指令的概念，例如您添加的 `syntax` 指令。指令必须始终位于 `Dockerfile` 的最顶部，因此在添加注释时，请确保注释位于您可能使用的任何指令之后：

```dockerfile
# syntax=docker/dockerfile:1
# 一个打包到容器镜像中的 Go 示例微服务。

FROM golang:1.19

# ...
```

## 构建镜像

现在您已经创建了 `Dockerfile`，请从中构建一个镜像。`docker build` 命令从 `Dockerfile` 和一个上下文创建 Docker 镜像。构建上下文是位于指定路径或 URL 中的一组文件。Docker 构建过程可以访问上下文中的任何文件。

构建命令可选择接受 `--tag` 标志。此标志用于用字符串值标记镜像，该值易于人类阅读和识别。如果您不传递 `--tag`，Docker 将使用 `latest` 作为默认值。

构建您的第一个 Docker 镜像。

```console
$ docker build --tag docker-gs-ping .
```

构建过程将在经历构建步骤时打印一些诊断消息。以下只是这些消息可能看起来的样子的示例。

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

您的确切输出会有所不同，但如果没有错误，您应该在输出的第一行看到 `FINISHED` 这个词。这意味着 Docker 已成功构建名为 `docker-gs-ping` 的镜像。

## 查看本地镜像

要查看本地机器上的镜像列表，您有两个选择。一种是使用 CLI，另一种是使用 [Docker Desktop](/manuals/desktop/_index.md)。由于您当前正在终端中工作，我们来看一下如何使用 CLI 列出镜像。

要列出镜像，请运行 `docker image ls` 命令（或简写 `docker images`）：

```console
$ docker image ls

REPOSITORY                       TAG       IMAGE ID       CREATED         SIZE
docker-gs-ping                   latest    7f153fbcc0a8   2 minutes ago   1.11GB
...
```

您的确切输出可能有所不同，但您应该会看到带有 `latest` 标签的 `docker-gs-ping` 镜像。因为您在构建镜像时没有指定自定义标签，所以 Docker 假定标签为 `latest`，这是一个特殊值。

## 标记镜像

镜像名称由斜杠分隔的名称组件组成。名称组件可以包含小写字母、数字和分隔符。分隔符定义为句点、一个或两个下划线或一个或多个破折号。名称组件不能以分隔符开头或结尾。

镜像由清单和层列表组成。简而言之，标签指向这些工件的组合。您可以为镜像设置多个标签，事实上，大多数镜像都有多个标签。为您构建的镜像创建第二个标签，并查看其层。

使用 `docker image tag`（或简写 `docker tag`）命令为您的镜像创建一个新标签。此命令接受两个参数；第一个参数是源镜像，第二个是要创建的新标签。以下命令为构建的 `docker-gs-ping:latest` 创建一个新的 `docker-gs-ping:v1.0` 标签：

```console
$ docker image tag docker-gs-ping:latest docker-gs-ping:v1.0
```

Docker `tag` 命令为镜像创建一个新标签。它不会创建新镜像。该标签指向同一个镜像，只是引用镜像的另一种方式。

现在再次运行 `docker image ls` 命令以查看更新后的本地镜像列表：

```console
$ docker image ls

REPOSITORY                       TAG       IMAGE ID       CREATED         SIZE
docker-gs-ping                   latest    7f153fbcc0a8   6 minutes ago   1.11GB
docker-gs-ping                   v1.0      7f153fbcc0a8   6 minutes ago   1.11GB
...
```

您可以看到有两个以 `docker-gs-ping` 开头的镜像。您知道它们是同一个镜像，因为如果您查看 `IMAGE ID` 列，您会看到两个镜像的值是相同的。此值是 Docker 内部用于标识镜像的唯一标识符。

删除您刚刚创建的标签。为此，您将使用 `docker image rm` 命令，或简写 `docker rmi`（代表 "remove image"）：

```console
$ docker image rm docker-gs-ping:v1.0
Untagged: docker-gs-ping:v1.0
``请注意，Docker 的响应告诉您镜像并未被删除，只是被取消了标记。

通过运行以下命令进行验证：

```console
$ docker image ls
```

您将看到标签 `v1.0` 不再在 Docker 实例保存的镜像列表中。

```text
REPOSITORY                       TAG       IMAGE ID       CREATED         SIZE
docker-gs-ping                   latest    7f153fbcc0a8   7 minutes ago   1.11GB
...
```

标签 `v1.0` 已被移除，但您的机器上仍然有 `docker-gs-ping:latest` 标签可用，所以镜像还在那里。

## 多阶段构建

您可能已经注意到您的 `docker-gs-ping` 镜像重达一千兆字节以上，对于一个微小的编译好的 Go 应用程序来说，这太大了。您可能也想知道在构建镜像后，包括编译器在内的全套 Go 工具发生了什么。

答案是完整的工具链仍然在容器镜像中。这不仅因为文件过大而不方便，而且在部署容器时也可能带来安全风险。

这两个问题可以通过使用[多阶段构建](/manuals/build/building/multi-stage.md)来解决。

简而言之，多阶段构建可以将工件从一个构建阶段传递到另一个阶段，并且每个构建阶段都可以从不同的基础镜像实例化。

因此，在下面的示例中，您将使用一个全功能的官方 Go 镜像来构建您的应用程序。然后您将应用程序二进制文件复制到另一个基础非常精简、不包含 Go 工具链或其他可选组件的镜像中。

示例应用程序仓库中的 `Dockerfile.multistage` 包含以下内容：

```dockerfile
# syntax=docker/dockerfile:1

# 从源代码构建应用程序
FROM golang:1.19 AS build-stage

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY *.go ./

RUN CGO_ENABLED=0 GOOS=linux go build -o /docker-gs-ping

# 在容器中运行测试
FROM build-stage AS run-test-stage
RUN go test -v ./...

# 将应用程序二进制文件部署到精简镜像中
FROM gcr.io/distroless/base-debian11 AS build-release-stage

WORKDIR /

COPY --from=build-stage /docker-gs-ping /docker-gs-ping

EXPOSE 8080

USER nonroot:nonroot

ENTRYPOINT ["/docker-gs-ping"]
```

由于您现在有两个 Dockerfile，您必须告诉 Docker 您想使用哪个 Dockerfile 来构建镜像。用 `multistage` 标记新镜像。这个标签（像除 `latest` 之外的任何其他标签一样）对 Docker 没有特殊含义，它只是您选择的东西。

```console
$ docker build -t docker-gs-ping:multistage -f Dockerfile.multistage .
```

比较 `docker-gs-ping:multistage` 和 `docker-gs-ping:latest` 的大小，您会看到几个数量级的差异。

```console
$ docker image ls
REPOSITORY       TAG          IMAGE ID       CREATED              SIZE
docker-gs-ping   multistage   e3fdde09f172   About a minute ago   28.1MB
docker-gs-ping   latest       336a3f164d0f   About an hour ago    1.11GB
```

之所以如此，是因为您在构建的第二阶段使用的 ["distroless"](https://github.com/GoogleContainerTools/distroless) 基础镜像非常精简，专为静态二进制文件的精简部署而设计。

多阶段构建还有更多内容，包括多架构构建的可能性，所以请随时查看[多阶段构建](/manuals/build/building/multi-stage.md)。然而，这对于您在此处的进展并不是必需的。

## 下一步

在本模块中，您认识了示例应用程序并为其构建了容器镜像。

在下一个模块中，您将了解如何将镜像作为容器运行。
