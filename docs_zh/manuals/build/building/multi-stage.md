---
title: 多阶段构建
linkTitle: 多阶段
weight: 10
description: |
  了解多阶段构建，以及如何利用它们改进构建并获得更小的镜像
keywords: build, best practices
aliases:
- /engine/userguide/eng-image/multistage-build/
- /develop/develop-images/multistage-build/
---

多阶段构建对任何曾努力优化 Dockerfile 同时又想保持其易读、易维护的人都有用。

## 使用多阶段构建（Use multi-stage builds）

使用多阶段构建时，你在 Dockerfile 中使用多个 `FROM` 语句。每条 `FROM` 指令可以使用不同的基础
镜像，并且每条都开始构建的一个新阶段。你可以有选择地将制品从一个阶段复制到另一个阶段，将你不想要
留在最终镜像中的一切留在后面。

以下 Dockerfile 有两个独立的阶段：一个用于构建二进制文件，另一个将二进制文件从第一阶段复制到下一
阶段。

```dockerfile
# syntax=docker/dockerfile:1
FROM golang:{{% param "example_go_version" %}}
WORKDIR /src
COPY <<EOF ./main.go
package main

import "fmt"

func main() {
  fmt.Println("hello, world")
}
EOF
RUN go build -o /bin/hello ./main.go

FROM scratch
COPY --from=0 /bin/hello /bin/hello
CMD ["/bin/hello"]
```

你只需要这一个 Dockerfile。无需单独的构建脚本。直接运行 `docker build`。

```console
$ docker build -t hello .
```

最终结果是一个微小的生产镜像，里面除了二进制文件别无他物。构建应用程序所需的任何构建工具都不包含在
结果镜像中。

它是如何工作的？第二条 `FROM` 指令以 `scratch` 镜像为基础开始一个新的构建阶段。`COPY --from=0` 行
仅将之前阶段构建好的制品复制到这个新阶段。Go SDK 和任何中间制品都被留在后面，不会保存到最终镜像中。

## 为构建阶段命名（Name your build stages）

默认情况下，阶段没有名称，你用整数编号引用它们，第一条 `FROM` 指令从 0 开始。不过，你可以通过在
`FROM` 指令中添加 `AS <NAME>` 来为阶段命名。此示例通过为阶段命名并在 `COPY` 指令中使用该名称，改进了
前一个示例。这意味着即使你的 Dockerfile 中的指令之后被重新排序，`COPY` 也不会出错。

```dockerfile
# syntax=docker/dockerfile:1
FROM golang:{{% param "example_go_version" %}} AS build
WORKDIR /src
COPY <<EOF /src/main.go
package main

import "fmt"

func main() {
  fmt.Println("hello, world")
}
EOF
RUN go build -o /bin/hello ./main.go

FROM scratch
COPY --from=build /bin/hello /bin/hello
CMD ["/bin/hello"]
```

## 停在特定的构建阶段（Stop at a specific build stage）

构建镜像时，你不一定需要构建包括每个阶段在内的整个 Dockerfile。你可以指定一个目标构建阶段。以下命令
假设你使用的是之前的 `Dockerfile`，但停在名为 `build` 的阶段：

```console
$ docker build --target build -t hello .
```

这可能有用的几种场景是：

- 调试特定的构建阶段
- 使用一个启用了所有调试符号或工具的 `debug` 阶段，以及一个精简的 `production` 阶段
- 使用一个 `testing` 阶段，其中你的应用被填充了测试数据，但使用真实数据通过不同的阶段进行生产构建

## 使用外部镜像作为阶段（Use an external image as a stage）

使用多阶段构建时，你并不局限于从 Dockerfile 中之前创建的阶段复制。你可以使用 `COPY --from` 指令从
单独的镜像复制，既可以使用本地镜像名、本地或 Docker 仓库上可用的标签，也可以使用标签 ID。Docker 客户端
会在必要时拉取该镜像并从那里复制制品。语法如下：

```dockerfile
COPY --from=nginx:latest /etc/nginx/nginx.conf /nginx.conf
```

## 将之前的阶段作为新阶段（Use a previous stage as a new stage）

你可以通过在使用 `FROM` 指令时引用它，从上一个阶段结束的地方继续。例如：

```dockerfile
# syntax=docker/dockerfile:1

FROM alpine:latest AS builder
RUN apk --no-cache add build-base

FROM builder AS build1
COPY source1.cpp source.cpp
RUN g++ -o /binary source.cpp

FROM builder AS build2
COPY source2.cpp source.cpp
RUN g++ -o /binary source.cpp
```

## 传统构建器与 BuildKit 的区别（Differences between legacy builder and BuildKit）

传统的 Docker Engine 构建器会处理 Dockerfile 中直到所选 `--target` 的所有阶段。即使所选目标不依赖该
阶段，它也会构建该阶段。

[BuildKit](../buildkit/_index.md) 只构建目标阶段所依赖的阶段。

例如，给定以下 Dockerfile：

```dockerfile
# syntax=docker/dockerfile:1
FROM ubuntu AS base
RUN echo "base"

FROM base AS stage1
RUN echo "stage1"

FROM base AS stage2
RUN echo "stage2"
```

在 [启用 BuildKit](../buildkit/_index.md#getting-started) 的情况下，构建该 Dockerfile 的 `stage2` 目标意味着
只处理 `base` 和 `stage2`。不依赖 `stage1`，因此跳过它。

```console
$ DOCKER_BUILDKIT=1 docker build --no-cache -f Dockerfile --target stage2 .
[+] Building 0.4s (7/7) FINISHED                                                                    
 => [internal] load build definition from Dockerfile                                            0.0s
 => => transferring dockerfile: 36B                                                             0.0s
 => [internal] load .dockerignore                                                               0.0s
 => => transferring context: 2B                                                                 0.0s
 => [internal] load metadata for docker.io/library/ubuntu:latest                                0.0s
 => CACHED [base 1/2] FROM docker.io/library/ubuntu                                             0.0s
 => [base 2/2] RUN echo "base"                                                                  0.1s
 => [stage2 1/1] RUN echo "stage2"                                                              0.2s
 => exporting to image                                                                          0.0s
 => => exporting layers                                                                         0.0s
 => => writing image sha256:f55003b607cef37614f607f0728e6fd4d113a4bf7ef12210da338c716f2cfd15    0.0s
```

另一方面，在没有 BuildKit 的情况下构建相同的目标会导致所有阶段都被处理：

```console
$ DOCKER_BUILDKIT=0 docker build --no-cache -f Dockerfile --target stage2 .
Sending build context to Docker daemon  219.1kB
Step 1/6 : FROM ubuntu AS base
 ---> a7870fd478f4
Step 2/6 : RUN echo "base"
 ---> Running in e850d0e42eca
base
Removing intermediate container e850d0e42eca
 ---> d9f69f23cac8
Step 3/6 : FROM base AS stage1
 ---> d9f69f23cac8
Step 4/6 : RUN echo "stage1"
 ---> Running in 758ba6c1a9a3
stage1
Removing intermediate container 758ba6c1a9a3
 ---> 396baa55b8c3
Step 5/6 : FROM base AS stage2
 ---> d9f69f23cac8
Step 6/6 : RUN echo "stage2"
 ---> Running in bbc025b93175
stage2
Removing intermediate container bbc025b93175
 ---> 09fc3770a9c4
Successfully built 09fc3770a9c4
```

传统构建器会处理 `stage1`，即使 `stage2` 并不依赖它。
