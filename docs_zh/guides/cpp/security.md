---
title: C++ Docker 镜像的供应链安全
linkTitle: 供应链安全
weight: 60
keywords: C++, security, multi-stage
description: 了解如何从 C++ Docker 镜像中提取 SBOM。
aliases:
- /language/cpp/security/
- /guides/language/cpp/security/
---

## 先决条件

- 您已安装 [Git 客户端](https://git-scm.com/downloads)。本节示例使用的是基于命令行的 Git 客户端，但您也可以使用任何其他客户端。
- 您已安装 Docker Desktop，并启用了 containerd 以用于拉取和存储镜像（在 **设置** > **常规** 中有一个复选框）。否则，如果您使用的是 Docker Engine：
  - 您已安装 [Docker SBOM CLI 插件](https://github.com/docker/sbom-cli-plugin)。要在 Docker Engine 上安装该插件，请使用以下命令：

    ```bash
    $ curl -sSfL https://raw.githubusercontent.com/docker/sbom-cli-plugin/main/install.sh | sh -s --
    ```

  - 您已安装 [Docker Scout CLI 插件](https://docs.docker.com/scout/install/)。要在 Docker Engine 上安装该插件，请使用以下命令：

    ```bash
    $ curl -sSfL https://raw.githubusercontent.com/docker/scout-cli/main/install.sh | sh -s --
    ```
    
  - 您已为 Docker Engine [启用 containerd](https://docs.docker.com/engine/storage/containerd/)。

## 概述

本节将指导您使用 Docker SBOM CLI 插件从 C++ Docker 镜像中提取软件物料清单 (SBOM)。SBOM 提供了软件包中所有组件的详细列表，包括其版本和许可证信息。您可以使用 SBOM 来跟踪软件的来源，并确保其符合组织的安全和许可策略。

## 生成 SBOM

这里我们将使用在 [为您的 C++ 应用程序创建多阶段构建](/guides/language/cpp/multistage/) 指南中构建的 Docker 镜像。如果您尚未构建该镜像，请按照该指南中的步骤构建镜像。
该镜像名为 `hello`。要为 `hello` 镜像生成 SBOM，请运行以下命令：

```bash
$ docker sbom hello
```

该命令会显示“未发现任何软件包”。这是因为最终镜像是 scratch 镜像，不包含任何软件包。
让我们再尝试使用 Docker Scout：

```bash
$ docker scout sbom --format=list hello
```

此命令会告诉您相同的信息。

## 生成 SBOM 证明

SBOM 可以在构建过程中生成并“附加”到镜像上。这称为 SBOM 证明。
要为 `hello` 镜像生成 SBOM 证明，首先让我们修改 Dockerfile：

```Dockerfile
ARG BUILDKIT_SBOM_SCAN_STAGE=true

FROM ubuntu:latest AS build

RUN apt-get update && apt-get install -y build-essential

WORKDIR /app

COPY hello.cpp .

RUN g++ -o hello hello.cpp -static

# --------------------
FROM scratch

COPY --from=build /app/hello /hello

CMD ["/hello"]
```

第一行 `ARG BUILDKIT_SBOM_SCAN_STAGE=true` 启用了构建阶段的 SBOM 扫描。
现在，使用以下命令构建镜像：

```bash
$ docker buildx build --sbom=true -t hello:sbom .
```

此命令将构建镜像并生成 SBOM 证明。您可以通过运行以下命令验证 SBOM 是否已附加到镜像：

```bash
$ docker scout sbom --format=list hello:sbom
```

请注意，普通的 `docker sbom` 命令不会加载 SBOM 证明。

## 总结

在本节中，您学习了如何在构建过程中为 C++ Docker 镜像生成 SBOM 证明。
普通的镜像扫描器无法从 scratch 镜像生成 SBOM。