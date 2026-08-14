# Go 语言专属指南


本指南将向你展示如何使用 Docker 创建、测试和部署容器化的 Go 应用。

> **致谢**
>
> Docker 感谢 [Oliver Frolovs](https://www.linkedin.com/in/ofr/) 对本指南的贡献。

## 你将学到什么？

在本指南中，你将学习如何：

- 创建一个 `Dockerfile`，其中包含为用 Go 编写的程序构建容器镜像的指令。
- 在本地 Docker 实例中将镜像作为容器运行，并管理容器的生命周期。
- 使用多阶段构建高效地构建小镜像，同时保持 Dockerfile 易于阅读和维护。
- 使用 Docker Compose 在开发环境中编排多个相关容器的协同运行。

## 先决条件

假定你已对 Go 及其工具链有基本的了解。这不是一篇 Go 教程。如果你是 : languages: 新手，[Go 官网](https://golang.org/) 是一个很好的探索起点，所以 _go_（双关语）去看看吧！

你还必须了解一些基本的 [Docker 概念](/get-started/docker-concepts/the-basics/what-is-a-container.md)，并且至少要模糊地熟悉 [Dockerfile 格式](/manuals/build/concepts/dockerfile.md)。

你的 Docker 设置必须启用 BuildKit。BuildKit 在 [Docker Desktop](/manuals/desktop/_index.md) 上对所有用户默认启用。如果你已安装 Docker Desktop，则无需手动启用 BuildKit。如果你在 Linux 上运行 Docker，请查看 BuildKit 的 [入门](/manuals/build/buildkit/_index.md#getting-started) 页面。

也期望你对命令行有一定熟悉。

## 后续步骤

本指南旨在提供足够的示例和说明，让你能够将自己的 Go 应用容器化并部署到云端。

首先构建你的第一个 Go 镜像。

## 构建你的 Go 镜像

### 概述

在本节中，你将构建一个容器镜像。该镜像包含运行你的应用所需的一切——编译好的应用二进制文件、运行时、库以及应用所需的所有其他资源。

### 所需软件

要完成本教程，你需要以下内容：

- 本地运行的 Docker。请按照 [下载并安装 Docker 的说明](/manuals/desktop/_index.md) 操作。
- 一个用于编辑文件的 IDE 或文本编辑器。[Visual Studio Code](https://code.visualstudio.com/) 是一个免费且受欢迎的选择，但你可以使用任何你感到舒适的编辑器。
- 一个 Git 客户端。本指南使用基于命令行的 `git` 客户端，但你完全可以使用适合你的任何工具。
- 一个命令行终端应用。本模块中展示的示例来自 Linux shell，但它们在 PowerShell、Windows 命令提示符或 OS X Terminal 中应该也能工作，几乎（即使有）不需要修改。

### 认识示例应用

示例应用是一个微服务的漫画式写照。它故意做得微不足道，以便让你专注于学习 Go 应用容器化的基础知识。

该应用提供两个 HTTP 端点：

- 对 `/` 的请求，它会以包含心形符号（`<3`）的字符串作为响应。
- 对 `/health` 的请求，它会以 `{"Status" : "OK"}` 的 JSON 作为响应。

对于任何其他请求，它会以 HTTP 错误 404 作为响应。

该应用监听由环境变量 `PORT` 的值定义的 TCP 端口。默认值为 `8080`。

该应用是无状态的。

该应用的完整源代码在 GitHub 上：[github.com/docker/docker-gs-ping](https://github.com/docker/docker-gs-ping)。我们鼓励你 fork 它并随意试验。

要继续，请将应用仓库克隆到你的本地机器：

```console
$ git clone https://github.com/docker/docker-gs-ping
```

如果你熟悉 Go，该应用的 `main.go` 文件很简单：

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

// Simple implementation of an integer minimum
// Adapted from: https://gobyexample.com/testing-and-benchmarking
func IntMin(a, b int) int {
	if a < b {
		return a
	}
	return b
}
```

### 为应用创建 Dockerfile

要使用 Docker 构建容器镜像，需要一个包含构建指令的 `Dockerfile`。

以（可选的）解析器指令行开始你的 `Dockerfile`，该指令指示 BuildKit 根据指定版本语法的语法规则来解释你的文件。

然后告诉 Docker 你希望为你的应用使用什么基础镜像：

```dockerfile
# syntax=docker/dockerfile:1

FROM golang:1.19
```

Docker 镜像可以继承自其他镜像。因此，你无需从头创建自己的基础镜像，而是可以使用官方的 Go 镜像，它已经拥有编译和运行 Go 应用所需的全部工具和库。

> [!NOTE]
>
> 如果你对创建自己的基础镜像感到好奇，可以查看本指南的以下章节：[创建基础镜像](/manuals/build/building/base-images.md#create-a-base-image)。不过请注意，要完成你手头的任务，这并非必要。

现在你已经为即将构建的容器镜像定义了基础镜像，你可以开始在其上构建。

为了让后续命令的运行更方便，在正在构建的镜像内创建一个目录。这也指示 Docker 将该目录作为所有后续命令的默认目标位置。这样你就无需在 `Dockerfile` 中输入完整的文件路径，相对路径将基于此目录。

```dockerfile
WORKDIR /app
```

通常，一旦下载了一个用 Go 编写的项目，你要做的第一件事就是安装编译它所需的模块。请注意，基础镜像已经拥有工具链，但你的源代码还不在其中。

因此，在你可以在镜像内运行 `go mod download` 之前，你需要将 `go.mod` 和 `go.sum` 文件复制到镜像中。使用 `COPY` 命令来完成。

`COPY` 命令最简单的形式有两个参数。第一个参数告诉 Docker 你想将哪些文件复制进镜像。最后一个参数告诉 Docker 你想将这些文件复制到哪里。

将 `go.mod` 和 `go.sum` 文件复制到你的项目目录 `/app`，由于你使用了 `WORKDIR`，该目录在镜像内就是当前目录（`./`）。与一些现代 shell 似乎对尾斜杠（`/`）的使用漠不关心，并且（在大多数情况下）能够推断出用户的意图不同，Docker 的 `COPY` 命令在解释尾斜杠时相当敏感。

```dockerfile
COPY go.mod go.sum ./
```

> [!NOTE]
>
> 如果你想熟悉 `COPY` 命令对尾斜杠的处理方式，请参阅 [Dockerfile 参考](/reference/dockerfile.md#copy)。这个尾斜杠可能以你无法想象的方式引发问题。

既然你正在构建的 Docker 镜像中已经包含了模块文件，你就可以使用 `RUN` 命令来在那里运行 `go mod download` 命令。这与你在本机本地运行 `go` 完全一样，但这一次这些 Go 模块将被安装到镜像内的一个目录中。

```dockerfile
RUN go mod download
```

此时，你已经拥有一个 Go 工具链 1.19.x 版本以及全部 Go 依赖项，它们都安装在镜像内。

接下来你需要做的是将你的源代码复制到镜像中。你将使用 `COPY` 命令，就像之前处理模块文件那样。

```dockerfile
COPY *.go ./
```

这个 `COPY` 命令使用通配符，将位于主机当前目录（即 `Dockerfile` 所在目录）中所有扩展名为 `.go` 的文件复制到镜像内的当前目录。

现在，要编译你的应用，使用熟悉的 `RUN` 命令：

```dockerfile
RUN CGO_ENABLED=0 GOOS=linux go build -o /docker-gs-ping
```

这应该很熟悉。该命令的结果将是一个名为 `docker-gs-ping` 的静态应用二进制文件，位于你正在构建的镜像的文件系统根目录下。你可以把它放在该镜像内任何你希望的其他位置，根目录在这方面没有特殊含义。使用根目录是为了让文件路径保持简短以提高可读性，这样做很方便。

现在，剩下要做的就是在你的镜像被用于启动容器时，告诉 Docker 要运行什么命令。

你使用 `CMD` 命令来完成：

```dockerfile
CMD ["/docker-gs-ping"]
```

以下是完整的 `Dockerfile`：

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

`Dockerfile` 也可以包含注释。它们总是以 `#` 符号开头，并且必须在一行的开始处。注释是为你方便而存在的，用于记录你的 `Dockerfile`。

还有一个 Dockerfile 指令（directive）的概念，比如你添加的 `syntax` 指令。指令必须始终位于 `Dockerfile` 的最顶部，所以在添加注释时，请确保注释位于你可能使用的任何指令之后：

```dockerfile
# syntax=docker/dockerfile:1
# A sample microservice in Go packaged into a container image.

FROM golang:1.19

# ...
```

### 构建镜像

既然你已经创建了 `Dockerfile`，就从它构建一个镜像。`docker build` 命令从 `Dockerfile` 和构建上下文（context）创建 Docker 镜像。构建上下文是位于指定路径或 URL 下的一组文件。Docker 构建过程可以访问上下文中位于任何位置的任何文件。

`build` 命令可选地接受一个 `--tag` 标志。该标志用于用一个易于人类阅读和识别的字符串值来标记镜像。如果你不传递 `--tag`，Docker 将使用 `latest` 作为默认值。

构建你的第一个 Docker 镜像。

```console
$ docker build --tag docker-gs-ping .
```

构建过程会在经过各个构建步骤时打印一些诊断消息。以下是这些消息可能的样子示例。

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

你的确切输出会有所不同，但如果没有任何错误，你应该会在输出的第一行看到 `FINISHED` 这个词。这意味着 Docker 已成功构建了名为 `docker-gs-ping` 的镜像。

### 查看本地镜像

要查看你本地机器上的镜像列表，你有两种选择。一种是使用 CLI，另一种是使用 [Docker Desktop](/manuals/desktop/_index.md)。既然你在终端中工作，那就用 CLI 来看看列出镜像。

要列出镜像，运行 `docker image ls` 命令（或简写 `docker images`）：

```console
$ docker image ls

REPOSITORY                       TAG       IMAGE ID       CREATED         SIZE
docker-gs-ping                   latest    7f153fbcc0a8   2 minutes ago   1.11GB
...
```

你的确切输出可能有所不同，但你应该能看到带有 `latest` 标签的 `docker-gs-ping` 镜像。因为你在构建镜像时没有指定自定义标签，Docker 假定标签为 `latest`，这是一个特殊值。

### 标记镜像

镜像名称由以斜杠分隔的名称组件组成。名称组件可以包含小写字母、数字和分隔符。分隔符定义为一个句号、一个或两个下划线，或一个以上的破折号。名称组件不能以分隔符开头或结尾。

一个镜像由一个清单（manifest）和一组层（layer）组成。简单来说，一个标签（tag）指向这些制品的组合。你可以为镜像拥有多个标签，事实上，大多数镜像都有多个标签。为你构建的镜像创建第二个标签，并查看它的层。

使用 `docker image tag`（或简写 `docker tag`）命令为你的镜像创建一个新标签。该命令接受两个参数；第一个参数是源镜像，第二个是要创建的新标签。以下命令为你构建的 `docker-gs-ping:latest` 创建了一个新的 `docker-gs-ping:v1.0` 标签：

```console
$ docker image tag docker-gs-ping:latest docker-gs-ping:v1.0
```

Docker 的 `tag` 命令为镜像创建一个新标签。它不会创建一个新镜像。该标签指向同一个镜像，是引用该镜像的另一种方式。

现在再次运行 `docker image ls` 命令，查看更新后的本地镜像列表：

```console
$ docker image ls

REPOSITORY                       TAG       IMAGE ID       CREATED         SIZE
docker-gs-ping                   latest    7f153fbcc0a8   6 minutes ago   1.11GB
docker-gs-ping                   v1.0      7f153fbcc0a8   6 minutes ago   1.11GB
...
```

你可以看到你有两个以 `docker-gs-ping` 开头的镜像。你知道它们是同一个镜像，因为如果你查看 `IMAGE ID` 列，你会发现两个镜像的值相同。这个值是 Docker 在内部用于识别镜像的唯一标识符。

移除你刚刚创建的标签。为此，你将使用 `docker image rm` 命令，或简写 `docker rmi`（代表 "remove image"）：

```console
$ docker image rm docker-gs-ping:v1.0
Untagged: docker-gs-ping:v1.0
```

请注意，Docker 的响应告诉你镜像没有被移除，只是被取消了标签。

通过运行以下命令来验证：

```console
$ docker image ls
```

你将看到标签 `v1.0` 不再位于你的 Docker 实例保留的镜像列表中。

```text
REPOSITORY                       TAG       IMAGE ID       CREATED         SIZE
docker-gs-ping                   latest    7f153fbcc0a8   7 minutes ago   1.11GB
...
```

标签 `v1.0` 已被移除，但你的机器上仍有 `docker-gs-ping:latest` 标签可用，所以镜像还在。

### 多阶段构建

你可能已经注意到，你的 `docker-gs-ping` 镜像超过一吉字节，这对于一个小小的编译型 Go 应用来说相当大。你可能还在好奇，在你构建完镜像之后，包括编译器在内的全套 Go 工具都去哪了。

答案是，完整的工具链仍在容器镜像中。这不仅因为文件体积巨大而带来不便，而且在容器被部署时还可能带来安全风险。

这两个问题都可以通过使用 [多阶段构建](/manuals/build/building/multi-stage.md) 来解决。

简而言之，多阶段构建可以将构建产物从一个构建阶段带入另一个阶段，并且每个构建阶段都可以从不同的基础镜像实例化。

因此，在下面的示例中，你将使用全功能的官方 Go 镜像来构建你的应用。然后你将应用二进制文件复制到另一个基础非常精简、不包含 Go 工具链或其他可选组件的镜像中。

示例应用仓库中的 `Dockerfile.multistage` 包含以下内容：

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

COPY --from=build-stage /docker-gs-ping /docker-gs-ping

EXPOSE 8080

USER nonroot:nonroot

ENTRYPOINT ["/docker-gs-ping"]
```

既然你现在有了两个 Dockerfile，你必须告诉 Docker 你想使用哪个 Dockerfile 来构建镜像。用 `multistage` 标记这个新镜像。这个标签（与 `latest` 之外的任何其他标签一样）对 Docker 没有特殊含义，它是你自行选择的。

```console
$ docker build -t docker-gs-ping:multistage -f Dockerfile.multistage .
```

比较 `docker-gs-ping:multistage` 和 `docker-gs-ping:latest` 的大小，你会发现几个数量级的差异。

```console
$ docker image ls
REPOSITORY       TAG          IMAGE ID       CREATED              SIZE
docker-gs-ping   multistage   e3fdde09f172   About a minute ago   28.1MB
docker-gs-ping   latest       336a3f164d0f   About an hour ago    1.11GB
```

这是因为你在构建的第二阶段使用的 ["distroless"](https://github.com/GoogleContainerTools/distroless) 基础镜像非常精简，专为静态二进制文件的精简部署而设计。

多阶段构建还有很多内容，包括多架构构建的可能性，所以请随意查看 [多阶段构建](/manuals/build/building/multi-stage.md)。不过，这对于你在这里的进展并非必要。

## 将你的 Go 镜像作为容器运行

### 先决条件

完成 [构建你的 Go 镜像](#build-your-go-image) 中将 Go 应用容器化的步骤。

### 概述

在上一模块中，你为示例应用创建了一个 `Dockerfile`，然后使用 `docker build` 命令创建了你的 Docker 镜像。既然你已经有了镜像，你就可以运行该镜像，看看你的应用是否运行正常。

容器是一个普通的操系统进程，只不过这个进程是隔离的，并且拥有自己的文件系统、自己的网络，以及独立于主机的、隔离的进程树。

要在容器内运行一个镜像，你使用 `docker run` 命令。它需要一个参数，那就是镜像名称。启动你的镜像并确保它运行正常。在终端中运行以下命令。

```console
$ docker run docker-gs-ping
```

```text
   ____    __
  / __/___/ /  ___
 / _// __/ _ \/ _ \
/___/\__/_//_/\___/ v4.10.2
High performance, minimalist Go web framework
https://echo.labstack.com
____________________________________O/_______
                                    O\
⇨ http server started on [::]:8080
```

当你运行此命令时，你会注意到你没有返回到命令提示符。这是因为你的应用是一个 REST 服务器，它将在一个循环中运行，等待传入的请求，直到你停止容器，才会将控制权交还给操作系统。

使用 curl 命令向服务器发送一个 GET 请求。

```console
$ curl http://localhost:8080/
curl: (7) Failed to connect to localhost port 8080: Connection refused
```

你的 curl 命令失败了，因为与服务器的连接被拒绝。这意味着你无法连接到 localhost 的 8080 端口。这是预料之中的，因为你的容器在隔离中运行，包括网络。停止容器，并用在你的本地网络上发布的 8080 端口重新启动。

要停止容器，按 ctrl-c。这将使你返回到终端提示符。

要为你的容器发布一个端口，你将在 `docker run` 命令上使用 `--publish` 标志（简写为 `-p`）。`--publish` 命令的格式为 `[host_port]:[container_port]`。所以如果你想将容器内部的 8080 端口暴露到容器外部的 3000 端口，你将向 `--publish` 标志传递 `3000:8080`。

启动容器并将 8080 端口暴露到主机的 8080 端口。

```console
$ docker run --publish 8080:8080 docker-gs-ping
```

现在，重新运行 curl 命令。

```console
$ curl http://localhost:8080/
Hello, Docker! <3
```

成功！你能够连接到运行在容器内、端口 8080 上的应用。切换回你的容器运行的终端，你应该会看到 `GET` 请求被记录到控制台。

按 `ctrl-c` 停止容器。

### 以分离模式运行

到目前为止这很棒，但你的示例应用是一个 Web 服务器，你不应该让终端连接到容器。Docker 可以在后台以分离模式运行你的容器。为此，你可以使用 `--detach` 或简写为 `-d`。Docker 会像之前一样启动你的容器，但这次会与你分离并返回到终端提示符。

```console
$ docker run -d -p 8080:8080 docker-gs-ping
d75e61fcad1e0c0eca69a3f767be6ba28a66625ce4dc42201a8a323e8313c14e
```

Docker 在后台启动了你的容器，并在终端上打印了容器 ID。

再次确保容器正在运行。运行相同的 `curl` 命令：

```console
$ curl http://localhost:8080/
Hello, Docker! <3
```

### 列出容器

由于你在后台运行了容器，你怎么知道容器是否正在运行，或者你的机器上还运行着哪些其他容器？嗯，要查看机器上运行的容器列表，运行 `docker ps`。这类似于在 Linux 机器上使用 ps 命令来查看进程列表。

```console
$ docker ps

CONTAINER ID   IMAGE            COMMAND             CREATED          STATUS          PORTS                    NAMES
d75e61fcad1e   docker-gs-ping   "/docker-gs-ping"   41 seconds ago   Up 40 seconds   0.0.0.0:8080->8080/tcp   inspiring_ishizaka
```

`ps` 命令告诉你关于正在运行的容器的一些信息。你可以看到容器 ID、容器内部运行的镜像、用于启动容器的命令、创建时间、状态、暴露的端口以及容器的名称。

你可能在想你的容器名称是从哪里来的。由于你在启动容器时没有为它提供名称，Docker 生成了一个随机名称。你马上会修复这个问题，但首先你需要停止容器。要停止容器，运行 `docker stop` 命令，传入容器的名称或 ID。

```console
$ docker stop inspiring_ishizaka
inspiring_ishizaka
```

现在重新运行 `docker ps` 命令以查看正在运行的容器列表。

```console
$ docker ps

CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

### 停止、启动和命名容器

Docker 容器可以被启动、停止和重启。当你停止一个容器时，它不会被移除，但其状态会更改为已停止，并且容器内的进程被停止。当你运行 `docker ps` 命令时，默认输出只显示正在运行的容器。如果你传入 `--all`（或简写为 `-a`），你将看到系统上的所有容器，包括已停止的容器和正在运行的容器。

```console
$ docker ps --all

CONTAINER ID   IMAGE            COMMAND                  CREATED              STATUS                      PORTS     NAMES
d75e61fcad1e   docker-gs-ping   "/docker-gs-ping"        About a minute ago   Exited (2) 23 seconds ago             inspiring_ishizaka
f65dbbb9a548   docker-gs-ping   "/docker-gs-ping"        3 minutes ago        Exited (2) 2 minutes ago              wizardly_joliot
aade1bf3d330   docker-gs-ping   "/docker-gs-ping"        3 minutes ago        Exited (2) 3 minutes ago              magical_carson
52d5ce3c15f0   docker-gs-ping   "/docker-gs-ping"        9 minutes ago        Exited (2) 3 minutes ago              gifted_mestorf
```

如果你一直在跟着操作，你应该会看到列出的几个容器。这些是你启动并停止但还没有移除的容器。

重启你刚刚停止的容器。找到容器的名称，并在下面的 `restart` 命令中替换该名称：

```console
$ docker restart inspiring_ishizaka
```

现在，使用 `ps` 命令再次列出所有容器：

```console
$ docker ps -a

CONTAINER ID   IMAGE            COMMAND                  CREATED          STATUS                     PORTS                    NAMES
d75e61fcad1e   docker-gs-ping   "/docker-gs-ping"        2 minutes ago    Up 5 seconds               0.0.0.0:8080->8080/tcp   inspiring_ishizaka
f65dbbb9a548   docker-gs-ping   "/docker-gs-ping"        4 minutes ago    Exited (2) 2 minutes ago                            wizardly_joliot
aade1bf3d330   docker-gs-ping   "/docker-gs-ping"        4 minutes ago    Exited (2) 4 minutes ago                            magical_carson
52d5ce3c15f0   docker-gs-ping   "/docker-gs-ping"        10 minutes ago   Exited (2) 4 minutes ago                            gifted_mestorf
```

请注意，你刚刚重启的容器已以分离模式启动，并且暴露了 `8080` 端口。另外，请注意容器的状态是 `Up X seconds`。当你重启一个容器时，它将以最初启动时所使用的相同标志或命令来启动。

停止并移除你的所有容器，然后来看看如何解决随机命名的问题。

停止你刚刚启动的容器。找到你正在运行的容器的名称，并在以下命令中将该名称替换为你系统上的容器名称：

```console
$ docker stop inspiring_ishizaka
inspiring_ishizaka
```

既然你所有的容器都已停止，移除它们。当一个容器被移除时，它不再运行，也不处于已停止状态。相反，容器内的进程被终止，容器的元数据被移除。

要移除一个容器，运行 `docker rm` 命令并传入容器名称。你可以在一条命令中向该命令传入多个容器名称。

同样，请确保将以下命令中的容器名称替换为你系统上的容器名称：

```console
$ docker rm inspiring_ishizaka wizardly_joliot magical_carson gifted_mestorf

inspiring_ishizaka
wizardly_joliot
magical_carson
gifted_mestorf
```

再次运行 `docker ps --all` 命令以验证所有容器都已消失。

现在，来解决烦人的随机命名问题。标准做法是给你的容器命名，原因很简单：这样更容易识别容器中运行的是什么，以及它与哪个应用或服务相关联。就像在你的代码中为变量使用良好的命名约定能让代码更易读一样，为你的容器命名也是如此。

要为一个容器命名，你必须在 `run` 命令上传递 `--name` 标志：

```console
$ docker run -d -p 8080:8080 --name rest-server docker-gs-ping
3bbc6a3102ea368c8b966e1878a5ea9b1fc61187afaac1276c41db22e4b7f48f
```

```console
$ docker ps

CONTAINER ID   IMAGE            COMMAND             CREATED          STATUS          PORTS                    NAMES
3bbc6a3102ea   docker-gs-ping   "/docker-gs-ping"   25 seconds ago   Up 24 seconds   0.0.0.0:8080->8080/tcp   rest-server
```

现在，你可以根据名称轻松识别你的容器。

## 使用容器进行 Go 开发

### 先决条件

完成 [将你的镜像作为容器运行](#run-your-go-image-as-a-container) 模块中的步骤，以学习如何管理容器的生命周期。

### 简介

在本模块中，你将了解如何在容器中运行数据库引擎，并将其连接到示例应用的扩展版本。你将看到一些用于保持持久化数据以及将容器连接在一起相互通信的选项。最后，你将学习如何使用 Docker Compose 有效地管理此类多容器本地开发环境。

### 本地数据库与容器

你将使用的数据库引擎称为 [CockroachDB](https://www.cockroachlabs.com/product/)。它是一个现代的、云原生的分布式 SQL 数据库。

与使用从源代码编译 CockroachDB 或使用操作系统的原生包管理器来安装 CockroachDB 不同，你将使用 [CockroachDB 的 Docker 镜像](https://hub.docker.com/r/cockroachdb/cockroach) 并在容器中运行它。

CockroachDB 在相当程度上与 PostgreSQL 兼容，并与后者共享许多约定，特别是环境变量的默认名称。所以，如果你熟悉 Postgres，看到一些熟悉的环境变量名时不要感到惊讶。与 Postgres 配合使用的 Go 模块，如 [pgx](https://pkg.go.dev/github.com/jackc/pgx)、[pq](https://pkg.go.dev/github.com/lib/pq)、[GORM](https://gorm.io/index.html) 和 [upper/db](https://upper.io/v4/) 也能与 CockroachDB 配合使用。

有关 Go 与 CockroachDB 之间关系的更多信息，请参阅 [CockroachDB 文档](https://www.cockroachlabs.com/docs/v20.2/build-a-go-app-with-cockroachdb.html)，不过要继续本指南，这并不是必要的。

#### 存储

数据库的意义在于拥有一个持久化的数据存储。[卷（Volumes）](/manuals/engine/storage/volumes.md) 是持久化由 Docker 容器生成和使用的数据的首选机制。因此，在你启动 CockroachDB 之前，为它创建卷。

要创建一个受管卷，运行：

```console
$ docker volume create roach
roach
```

你可以用以下命令查看 Docker 实例中所有受管卷的列表：

```console
$ docker volume list
DRIVER    VOLUME NAME
local     roach
```

#### 网络

示例应用和数据库引擎将通过网络彼此通信。可能有不同种类的网络配置，你将使用所谓的用户定义桥接网络（user-defined bridge network）。它将为你提供 DNS 查找服务，这样你就可以通过主机名来引用你的数据库引擎容器。

以下命令创建了一个名为 `mynet` 的新桥接网络：

```console
$ docker network create -d bridge mynet
51344edd6430b5acd121822cacc99f8bc39be63dd125a3b3cd517b6485ab7709
```

与受管卷的情况一样，有一个命令可以列出 Docker 实例中设置的所有网络：

```console
$ docker network list
NETWORK ID     NAME          DRIVER    SCOPE
0ac2b1819fa4   bridge        bridge    local
51344edd6430   mynet         bridge    local
daed20bbecce   host          host      local
6aee44f40a39   none          null      local
```

你的桥接网络 `mynet` 已成功创建。其他三个名为 `bridge`、`host` 和 `none` 的网络是默认网络，它们由 Docker 自身创建。虽然这与本指南无关，但你可以在 [网络概述](/manuals/engine/network/_index.md) 章节中了解更多关于 Docker 网络的内容。

#### 为卷和网络选择好的名称

俗话说，计算机科学中只有两件难事：缓存失效和命名。还有少一错误（off-by-one errors）。

在为网络或受管卷选择名称时，最好选择一个能表明预期用途的名称。本指南力求简洁，所以使用了简短、通用的名称。

#### 启动数据库引擎

既然杂务已处理完毕，你可以运行 CockroachDB 容器，并将其附加到你刚刚创建的卷和网络。当你运行以下命令时，Docker 将从 Docker Hub 拉取镜像并在本地为你运行它：

```console
$ docker run -d \
  --name roach \
  --hostname db \
  --network mynet \
  -p 26257:26257 \
  -p 8080:8080 \
  -v roach:/cockroach/cockroach-data \
  cockroachdb/cockroach:latest-v25.4 start-single-node \
  --insecure

# ... output omitted ...
```

请注意巧妙地使用了标签 `latest-v25.4` 来确保你拉取的是 25.4 的最新补丁版本。可用标签的多样性取决于镜像维护者。在这里，你的意图是拥有 CockroachDB 的最新补丁版本，同时随着时间的推移不要太偏离已知可用的版本。要查看 CockroachDB 镜像可用的标签，你可以前往 [Docker Hub 上的 CockroachDB 页面](https://hub.docker.com/r/cockroachdb/cockroach/tags)。

#### 配置数据库引擎

既然数据库引擎已启动，在应用可以使用它之前，还需要进行一些配置。幸运的是，这并不多。你必须：

1. 创建一个空白数据库。
2. 在数据库引擎中注册一个新的用户账户。
3. 授予该新用户对该数据库的访问权限。

你可以借助 CockroachDB 内置的 SQL shell 来完成。要在数据库引擎运行的同一容器中启动 SQL shell，输入：

```console
$ docker exec -it roach ./cockroach sql --insecure
```

1. 在 SQL shell 中，创建示例应用将要使用的数据库：

   ```sql
   CREATE DATABASE mydb;
   ```

2. 在数据库引擎中注册一个新的 SQL 用户账户。使用用户名 `totoro`。

   ```sql
   CREATE USER totoro;
   ```

3. 授予新用户必要的权限：

   ```sql
   GRANT ALL ON DATABASE mydb TO totoro;
   ```

4. 输入 `quit` 退出 shell。

以下是与 SQL shell 交互的示例。

```console
$ sudo docker exec -it roach ./cockroach sql --insecure
#
# Welcome to the CockroachDB SQL shell.
# All statements must be terminated by a semicolon.
# To exit, type: \q.
#
# Server version: CockroachDB CCL v20.1.15 (x86_64-unknown-linux-gnu, built 2021/04/26 16:11:58, go1.13.9) (same version as client)
# Cluster ID: 7f43a490-ccd6-4c2a-9534-21f393ca80ce
#
# Enter \? for a brief introduction.
#
root@:26257/defaultdb> CREATE DATABASE mydb;
CREATE DATABASE

Time: 22.985478ms

root@:26257/defaultdb> CREATE USER totoro;
CREATE ROLE

Time: 13.921659ms

root@:26257/defaultdb> GRANT ALL ON DATABASE mydb TO totoro;
GRANT

Time: 14.217559ms

root@:26257/defaultdb> quit
oliver@hki:~$
```

#### 认识示例应用

既然你已经启动并配置了数据库引擎，你可以将注意力转向应用。

本模块的示例应用是你在前面模块中使用的 `docker-gs-ping` 应用的扩展版本。你有两个选择：

- 你可以更新你本地的 `docker-gs-ping` 副本，使其与本章所呈现的新扩展版本相匹配；或者
- 你可以克隆 [docker/docker-gs-ping-dev](https://github.com/docker/docker-gs-ping-dev) 仓库。推荐采用后一种方法。

要检出示例应用，运行：

```console
$ git clone https://github.com/docker/docker-gs-ping-dev.git
# ... output omitted ...
```

应用的 `main.go` 现在包含了数据库初始化代码，以及实现新的业务需求的代码：

- 一个向 `/send` 发送的 HTTP `POST` 请求，包含 `{ "value" : string }` 的 JSON，必须将值保存到数据库中。

你还有一个针对另一个业务需求的更新。该需求是：

- 应用对 `/` 的请求以包含心形符号（"`<3`"）的文本消息作为响应。

现在它将是：

- 应用以包含数据库中存储消息计数的字符串作为响应，该计数用括号括起来。

  示例输出：`Hello, Docker! (7)`

以下是 `main.go` 的完整源代码清单。

```go
package main

import (
	"context"
	"database/sql"
	"fmt"
	"log"
	"net/http"
	"os"

	"github.com/cenkalti/backoff/v4"
	"github.com/cockroachdb/cockroach-go/v2/crdb"
	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
)

func main() {

	e := echo.New()

	e.Use(middleware.Logger())
	e.Use(middleware.Recover())

	db, err := initStore()
	if err != nil {
		log.Fatalf("failed to initialize the store: %s", err)
	}
	defer db.Close()

	e.GET("/", func(c echo.Context) error {
		return rootHandler(db, c)
	})

	e.GET("/ping", func(c echo.Context) error {
		return c.JSON(http.StatusOK, struct{ Status string }{Status: "OK"})
	})

	e.POST("/send", func(c echo.Context) error {
		return sendHandler(db, c)
	})

	httpPort := os.Getenv("HTTP_PORT")
	if httpPort == "" {
		httpPort = "8080"
	}

	e.Logger.Fatal(e.Start(":" + httpPort))
}

type Message struct {
	Value string `json:"value"`
}

func initStore() (*sql.DB, error) {

	pgConnString := fmt.Sprintf("host=%s port=%s dbname=%s user=%s password=%s sslmode=disable",
		os.Getenv("PGHOST"),
		os.Getenv("PGPORT"),
		os.Getenv("PGDATABASE"),
		os.Getenv("PGUSER"),
		os.Getenv("PGPASSWORD"),
	)

	var (
		db  *sql.DB
		err error
	)
	openDB := func() error {
		db, err = sql.Open("postgres", pgConnString)
		return err
	}

	err = backoff.Retry(openDB, backoff.NewExponentialBackOff())
	if err != nil {
		return nil, err
	}

	if _, err := db.Exec(
		"CREATE TABLE IF NOT EXISTS message (value TEXT PRIMARY KEY)"); err != nil {
		return nil, err
	}

	return db, nil
}

func rootHandler(db *sql.DB, c echo.Context) error {
	r, err := countRecords(db)
	if err != nil {
		return c.HTML(http.StatusInternalServerError, err.Error())
	}
	return c.HTML(http.StatusOK, fmt.Sprintf("Hello, Docker! (%d)\n", r))
}

func sendHandler(db *sql.DB, c echo.Context) error {

	m := &Message{}

	if err := c.Bind(m); err != nil {
		return c.JSON(http.StatusInternalServerError, err)
	}

	err := crdb.ExecuteTx(context.Background(), db, nil,
		func(tx *sql.Tx) error {
			_, err := tx.Exec(
				"INSERT INTO message (value) VALUES ($1) ON CONFLICT (value) DO UPDATE SET value = excluded.value",
				m.Value,
			)
			if err != nil {
				return c.JSON(http.StatusInternalServerError, err)
			}
			return nil
		})

	if err != nil {
		return c.JSON(http.StatusInternalServerError, err)
	}

	return c.JSON(http.StatusOK, m)
}

func countRecords(db *sql.DB) (int, error) {

	rows, err := db.Query("SELECT COUNT(*) FROM message")
	if err != nil {
		return 0, err
	}
	defer rows.Close()

	count := 0
	for rows.Next() {
		if err := rows.Scan(&count); err != nil {
			return 0, err
		}
		rows.Close()
	}

	return count, nil
}
```

该仓库还包含 `Dockerfile`，它几乎与前面模块中介绍的多阶段 `Dockerfile` 完全相同。它使用官方的 Docker Go 镜像来构建应用，然后通过将编译好的二进制文件放入更精简的 distroless 镜像中来构建最终的镜像。

无论你是更新了旧的示例应用，还是检出了新的示例应用，都必须构建这个新的 Docker 镜像以反映对应用源代码的更改。

#### 构建应用

你可以用熟悉的 `build` 命令来构建镜像：

```console
$ docker build --tag docker-gs-ping-roach .
```

#### 运行应用

现在，运行你的容器。这一次你需要设置一些环境变量，以便你的应用知道如何访问数据库。目前，你将在 `docker run` 命令中直接完成。稍后你会看到使用 Docker Compose 的更方便的方法。

> [!NOTE]
>
> 由于你在以不安全模式运行 CockroachDB 集群，密码的值可以是任意值。
>
> 在生产环境中，不要以不安全模式运行。

```console
$ docker run -it --rm -d \
  --network mynet \
  --name rest-server \
  -p 80:8080 \
  -e PGUSER=totoro \
  -e PGPASSWORD=myfriend \
  -e PGHOST=db \
  -e PGPORT=26257 \
  -e PGDATABASE=mydb \
  docker-gs-ping-roach
```

关于这个命令有几点需要注意。

- 这次你将容器端口 `8080` 映射到主机端口 `80`。因此，对于 `GET` 请求，你可以直接使用 `curl localhost`：

  ```console
  $ curl localhost
  Hello, Docker! (0)
  ```

  或者，如果你愿意，使用完整的 URL 也同样有效：

  ```console
  $ curl http://localhost/
  Hello, Docker! (0)
  ```

- 目前存储的消息总数为 `0`。这没问题，因为你还没有向你的应用发布任何内容。
- 你通过数据库容器的主机名（即 `db`）来引用它。这就是你在启动数据库容器时使用 `--hostname db` 的原因。

- 实际的密码无关紧要，但必须设置为某个值，以免让示例应用感到困惑。
- 你刚刚运行的容器名为 `rest-server`。这些名称对于管理容器生命周期很有用：

  ```console
  # Don't do this just yet, it's only an example:
  $ docker container rm --force rest-server
  ```

#### 测试应用

在上一节中，你已经通过 `GET` 测试了查询你的应用，它返回了存储消息计数器的值为零。现在，向它发布一些消息：

```console
$ curl --request POST \
  --url http://localhost/send \
  --header 'content-type: application/json' \
  --data '{"value": "Hello, Docker!"}'
```

应用以消息内容作为响应，这意味着它已保存到数据库中：

```json
{ "value": "Hello, Docker!" }
```

发送另一条消息：

```console
$ curl --request POST \
  --url http://localhost/send \
  --header 'content-type: application/json' \
  --data '{"value": "Hello, Oliver!"}'
```

同样，你取回了消息的值：

```json
{ "value": "Hello, Oliver!" }
```

运行 curl 并看看消息计数器显示了什么：

```console
$ curl localhost
Hello, Docker! (2)
```

在此示例中，你发送了两条消息，数据库将它们保留了。是这样吗？停止并移除你的所有容器，但不要移除卷，然后再试一次。

首先，停止容器：

```console
$ docker container stop rest-server roach
rest-server
roach
```

然后，移除它们：

```console
$ docker container rm rest-server roach
rest-server
roach
```

验证它们已消失：

```console
$ docker container list --all
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

重新启动它们，先启动数据库：

```console
$ docker run -d \
  --name roach \
  --hostname db \
  --network mynet \
  -p 26257:26257 \
  -p 8080:8080 \
  -v roach:/cockroach/cockroach-data \
  cockroachdb/cockroach:latest-v25.4 start-single-node \
  --insecure
```

然后是服务：

```console
$ docker run -it --rm -d \
  --network mynet \
  --name rest-server \
  -p 80:8080 \
  -e PGUSER=totoro \
  -e PGPASSWORD=myfriend \
  -e PGHOST=db \
  -e PGPORT=26257 \
  -e PGDATABASE=mydb \
  docker-gs-ping-roach
```

最后，查询你的服务：

```console
$ curl localhost
Hello, Docker! (2)
```

太好了！来自数据库的记录计数是正确的，尽管你不仅停止了容器，而且在启动新实例之前还移除了它们。区别在于你复用了 CockroachDB 的受管卷。新的 CockroachDB 容器从磁盘读取了数据库文件，就像它通常在容器外部运行时那样。

#### 收尾一切

请记住，你是以不安全模式运行 CockroachDB。既然你已经构建并测试了你的应用，在继续之前是时候收尾一切了。你可以用 `list` 命令列出你正在运行的容器：

```console
$ docker container list
```

既然你知道了容器 ID，你就可以使用 `docker container stop` 和 `docker container rm`，如前面模块中所示。

在继续之前，停止 CockroachDB 和 `docker-gs-ping-roach` 容器。

### 使用 Docker Compose 提升生产力

此时，你可能想知道是否有办法避免不得不处理 `docker` 命令那一长串参数。本系列中使用的玩具示例需要五个环境变量来定义与数据库的连接。一个真实的应用可能需要更多、更多的环境变量。此外还有依赖关系的问题。理想情况下，你希望确保数据库在你的应用运行之前启动。而启动数据库实例可能需要另一个带有很多选项的 Docker 命令。但对于本地开发目的，有更好的方法来编排这些部署。

在本节中，你将创建一个 Docker Compose 文件，用一条命令启动你的 `docker-gs-ping-roach` 应用和 CockroachDB 数据库引擎。

#### 配置 Docker Compose

在你的应用目录中，创建一个名为 `compose.yaml` 的新文本文件，内容如下。

```yaml
services:
  docker-gs-ping-roach:
    depends_on:
      - roach
    build:
      context: .
    container_name: rest-server
    hostname: rest-server
    networks:
      - mynet
    ports:
      - 80:8080
    environment:
      - PGUSER=${PGUSER:-totoro}
      - PGPASSWORD=${PGPASSWORD:?database password not set}
      - PGHOST=${PGHOST:-db}
      - PGPORT=${PGPORT:-26257}
      - PGDATABASE=${PGDATABASE:-mydb}
    deploy:
      restart_policy:
        condition: on-failure
  roach:
    image: cockroachdb/cockroach:latest-v25.4
    container_name: roach
    hostname: db
    networks:
      - mynet
    ports:
      - 26257:26257
      - 8080:8080
    volumes:
      - roach:/cockroach/cockroach-data
    command: start-single-node --insecure

volumes:
  roach:

networks:
  mynet:
    driver: bridge
```

这个 Docker Compose 配置非常方便，因为你无需键入所有要传递给 `docker run` 命令的参数。你可以在 Docker Compose 文件中以声明式的方式完成。 [Docker Compose 文档页面](/manuals/compose/_index.md) 相当广泛，并包含 Docker Compose 文件格式的完整参考。

#### `.env` 文件

如果有 `.env` 文件可用，Docker Compose 会自动从中读取环境变量。由于你的 Compose 文件要求设置 `PGPASSWORD`，请将以下内容添加到 `.env` 文件中：

```bash
PGPASSWORD=whatever
```

对于这个示例，确切的值并不重要，因为你以不安全模式运行 CockroachDB。请确保将该变量设置为某个值，以避免出错。

#### 合并 Compose 文件

文件名 `compose.yaml` 是 `docker compose` 命令在不提供 `-f` 标志时识别的默认文件名。这意味着如果你的环境有这样的需求，你可以拥有多个 Docker Compose 文件。此外，Docker Compose 文件是可组合的（composable），因此可以在命令行上指定多个文件，以将配置的各个部分合并在一起。以下列表展示了一几个此类功能可能有用的场景示例：

- 在本地开发时对源代码使用绑定挂载（bind mount），但在运行 CI 测试时不使用；
- 在为某个 API 应用使用前端预构建镜像与为源代码创建绑定挂载之间切换；
- 为集成测试添加额外的服务；
- 以及更多……

你在这里不会涉及这些高级用例。

#### Docker Compose 中的变量替换

Docker Compose 的一个非常酷的特性是 [变量替换](/reference/compose-file/interpolation.md)。你可以在 Compose 文件的 `environment` 部分看到一些示例。举例来说：

- `PGUSER=${PGUSER:-totoro}` 意味着在容器内部，环境变量 `PGUSER` 应被设置为与运行 Docker Compose 的主机机器上相同的值。如果主机机器上没有这个名称的环境变量，容器内的变量将获得默认值 `totoro`。
- `PGPASSWORD=${PGPASSWORD:?database password not set}` 意味着如果主机上没有设置环境变量 `PGPASSWORD`，Docker Compose 将显示错误。这没问题，因为你不想为密码硬编码默认值。你在 `.env` 文件中设置密码值，它只存在于你的本地机器上。始终将 `.env` 添加到 `.gitignore` 中以避免密钥被提交到版本控制中是一个好习惯。

处理未定义或空值的其他方式也存在，如 Docker 文档的 [变量替换](/reference/compose-file/interpolation.md) 章节中所述。

#### 验证 Docker Compose 配置

在应用对 Compose 配置文件所做的更改之前，有机会通过以下命令验证配置文件的内容：

```console
$ docker compose config
```

当运行此命令时，Docker Compose 读取 `compose.yaml` 文件，将其解析为内存中的数据结构，在可能的情况下进行验证，并把从其内部表示重建出的配置文件打印回来。如果由于错误而无法做到这一点，Docker 会打印一条错误消息。

#### 使用 Docker Compose 构建并运行应用

启动你的应用并确认它正在运行。

```console
$ docker compose up --build
```

你传递了 `--build` 标志，所以 Docker 会编译你的镜像，然后启动它。

> [!NOTE]
>
> Docker Compose 是一个有用的工具，但它有自己的怪癖。例如，除非提供 `--build` 标志，否则源代码更新不会触发重建。编辑自己的源代码，然后在运行 `docker compose up` 时忘记使用 `--build` 标志，这是一个非常常见的陷阱。

由于你的设置现在由 Docker Compose 运行，它为其分配了一个项目名称，因此你会为你的 CockroachDB 实例获得一个新的卷。这意味着你的应用将连接数据库失败，因为该数据库在这个新卷中不存在。终端显示了一个针对该数据库的认证错误：

```text
# ... omitted output ...
rest-server             | 2021/05/10 00:54:25 failed to initialise the store: pq: password authentication failed for user totoro
roach                   | *
roach                   | * INFO: Replication was disabled for this cluster.
roach                   | * When/if adding nodes in the future, update zone configurations to increase the replication factor.
roach                   | *
roach                   | CockroachDB node starting at 2021-05-10 00:54:26.398177 +0000 UTC (took 3.0s)
roach                   | build:               CCL v20.1.15 @ 2021/04/26 16:11:58 (go1.13.9)
roach                   | webui:               http://db:8080
roach                   | sql:                 postgresql://root@db:26257?sslmode=disable
roach                   | RPC client flags:    /cockroach/cockroach <client cmd> --host=db:26257 --insecure
roach                   | logs:                /cockroach/cockroach-data/logs
roach                   | temp dir:            /cockroach/cockroach-data/cockroach-temp349434348
roach                   | external I/O path:   /cockroach/cockroach-data/extern
roach                   | store[0]:            path=/cockroach/cockroach-data
roach                   | storage engine:      rocksdb
roach                   | status:              initialized new cluster
roach                   | clusterID:           b7b1cb93-558f-4058-b77e-8a4ddb329a88
roach                   | nodeID:              1
rest-server exited with code 0
rest-server             | 2021/05/10 00:54:25 failed to initialise the store: pq: password authentication failed for user totoro
rest-server             | 2021/05/10 00:54:26 failed to initialise the store: pq: password authentication failed for user totoro
rest-server             | 2021/05/10 00:54:29 failed to initialise the store: pq: password authentication failed for user totoro
rest-server             | 2021/05/10 00:54:25 failed to initialise the store: pq: password authentication failed for user totoro
rest-server             | 2021/05/10 00:54:26 failed to initialise the store: pq: password authentication failed for user totoro
rest-server             | 2021/05/10 00:54:29 failed to initialise the store: pq: password authentication failed for user totoro
rest-server exited with code 1
# ... omitted output ...
```

由于你设置部署的方式使用了 `restart_policy`，失败的容器每 20 秒被重启一次。所以，为了修复问题，你需要登录数据库引擎并创建用户。你之前在 [配置数据库引擎](#configure-the-database-engine) 中已经做过。

这没什么大不了的。你所要做的就是连接到 CockroachDB 实例，并运行创建数据库和用户的三条 SQL 命令，如 [配置数据库引擎](#configure-the-database-engine) 中所述。

所以，从另一个终端登录数据库引擎：

```console
$ docker exec -it roach ./cockroach sql --insecure
```

并运行与之前相同的命令来创建数据库 `mydb`、用户 `totoro`，并授予该用户必要的权限。一旦你完成了这些（并且示例应用容器自动重启），`rest-service` 就会停止失败和重启，控制台也会恢复安静。

本可以连接你之前使用的卷，但就本示例而言，这样做的麻烦大于其价值，而且它还提供了一个机会来展示如何通过 `restart_policy` 这个 Compose 文件特性将弹性引入你的部署。

#### 测试应用

现在，测试你的 API 端点。在新终端中，运行以下命令：

```console
$ curl http://localhost/
```

你应该收到以下响应：

```json
Hello, Docker! (0)
```

#### 关闭

要停止由 Docker Compose 启动的容器，在运行了 `docker compose up` 的终端中按 `ctrl+c`。要在它们停止后移除这些容器，运行 `docker compose down`。

#### 分离模式

你可以以分离模式运行由 `docker compose` 命令启动的容器，就像你对 `docker` 命令所做的那样，只需使用 `-d` 标志。

要以分离模式启动由 Compose 文件定义的栈，运行：

```console
$ docker compose up --build -d
```

然后，你可以使用 `docker compose stop` 停止容器，并使用 `docker compose down` 移除它们。

### 进一步探索

你可以运行 `docker compose` 来查看还有哪些命令可用。

### 总结

有一些相关的、但有趣的点被刻意排除在本章之外。对于更具探索精神的读者，本节提供了一些进一步学习的指引。

#### 持久化存储

受管卷并不是为容器提供持久化存储的唯一方法。强烈建议熟悉可用的存储选项及其用例，这些都在 [在 Docker 中管理数据](/manuals/engine/storage/_index.md) 中有所涵盖。

#### CockroachDB 集群

你运行了 CockroachDB 的单实例，这对本示例来说已经足够。但是，运行由多个 CockroachDB 实例组成的 CockroachDB 集群是可能的，每个实例运行在它自己的容器中。由于 CockroachDB 引擎本身就是为分布式而设计的，要运行一个多节点的集群，对你的流程所需的改动会小得惊人。

这种分布式设置为你提供了有趣的可能性，例如应用混沌工程（Chaos Engineering）技术来模拟集群的部分故障，并评估你的应用应对此类故障的能力。

如果你有兴趣试验 CockroachDB 集群，请查看：

- [在 Docker 中启动 CockroachDB 集群](https://www.cockroachlabs.com/docs/v20.2/start-a-local-cluster-in-docker-mac.html) 一文；以及
- Docker Compose 关键字 [`deploy`](/reference/compose-file/legacy-versions.md) 和 [`replicas`](/reference/compose-file/legacy-versions.md) 的文档。

#### 其他数据库

既然你没有运行 CockroachDB 实例的集群，你可能想知道是否可以使用非分布式数据库引擎。答案是"可以"，如果你选择更传统的 SQL 数据库，例如 [PostgreSQL](https://www.postgresql.org/)，本章描述的流程将非常相似。

## 使用 Go test 运行你的测试

### 先决条件

完成本指南的 [构建你的 Go 镜像](#build-your-go-image) 部分。

### 概述

测试是现代软件开发中不可或缺的一部分。对不同开发团队而言，测试可能意味着很多事情。有单元测试、集成测试和端到端测试。在本指南中，你将了解在构建时在 Docker 中运行你的单元测试。

对于本节，使用你在 [构建你的 Go 镜像](#build-your-go-image) 中克隆的 `docker-gs-ping` 项目。

### 在构建时运行测试

要在构建时运行你的测试，你需要向 `Dockerfile.multistage` 添加一个测试阶段。示例应用仓库中的 `Dockerfile.multistage` 已经包含以下内容：

```dockerfile {hl_lines="15-17"}
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

COPY --from=build-stage /docker-gs-ping /docker-gs-ping

EXPOSE 8080

USER nonroot:nonroot

ENTRYPOINT ["/docker-gs-ping"]
```

运行以下命令，以 `run-test-stage` 阶段为目标构建镜像并查看测试结果。包含 `--progress plain` 以查看构建输出，`--no-cache` 以确保测试始终运行，以及 `--target run-test-stage` 以指定测试阶段为目标。

```console
$ docker build -f Dockerfile.multistage -t docker-gs-ping-test --progress plain --no-cache --target run-test-stage .
```

你应该看到包含以下内容的输出。

```text
#13 [run-test-stage 1/1] RUN go test -v ./...
#13 4.915 === RUN   TestIntMinBasic
#13 4.915 --- PASS: TestIntMinBasic (0.00s)
#13 4.915 === RUN   TestIntMinTableDriven
#13 4.915 === RUN   TestIntMinTableDriven/0,1
#13 4.915 === RUN   TestIntMinTableDriven/1,0
#13 4.915 === RUN   TestIntMinTableDriven/2,-2
#13 4.915 === RUN   TestIntMinTableDriven/0,-1
#13 4.915 === RUN   TestIntMinTableDriven/-1,0
#13 4.915 --- PASS: TestIntMinTableDriven (0.00s)
#13 4.915     --- PASS: TestIntMinTableDriven/0,1 (0.00s)
#13 4.915     --- PASS: TestIntMinTableDriven/1,0 (0.00s)
#13 4.915     --- PASS: TestIntMinTableDriven/2,-2 (0.00s)
#13 4.915     --- PASS: TestIntMinTableDriven/0,-1 (0.00s)
#13 4.915     --- PASS: TestIntMinTableDriven/-1,0 (0.00s)
#13 4.915 PASS
```

