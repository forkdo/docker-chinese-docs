---
title: C++ Docker 镜像的供应链安全
linkTitle: 供应链安全
weight: 60
keywords: C++, 安全, 多阶段构建
description: 了解如何从 C++ Docker 镜像中提取软件物料清单（SBOM）。
aliases:
- /language/cpp/security/
- /guides/language/cpp/security/
---

## 前置条件

- 你已安装 [Git 客户端](https://git-scm.com/downloads)。本节示例使用基于命令行的 Git 客户端，但你可以使用任意客户端。
- 你已安装 Docker Desktop，并已启用 containerd 用于拉取和存储镜像（在 **Settings** > **General** 中勾选相应选项）。否则，如果你使用 Docker Engine：
  - 你已安装 [Docker SBOM CLI 插件](https://github.com/docker/sbom-cli-plugin)。在 Docker Engine 上安装该插件，请使用以下命令：

    ```bash
    $ curl -sSfL https://raw.githubusercontent.com/docker/sbom-cli-plugin/main/install.sh | sh -s --
    ```

  - 你已安装 [Docker Scout CLI 插件](https://docs.docker.com/scout/install/)。在 Docker Engine 上安装该插件，请使用以下命令：

    ```bash
    $ curl -sSfL https://raw.githubusercontent.com/docker/scout-cli/main/install.sh | sh -s --
    ```
    
  - 你已为 Docker Engine [启用 containerd](https://docs.docker.com/engine/storage/containerd/)。

## 概述

本节将指导你使用 Docker SBOM CLI 插件从 C++ Docker 镜像中提取软件物料清单（SBOM）。SBOM 提供了软件包中所有组件的详细列表，包括其版本和许可证信息。你可以使用 SBOM 来追踪软件的来源，确保其符合组织的安全和许可证策略。

## 生成 SBOM

此处我们将使用在 [为你的 C++ 应用创建多阶段构建](/guides/language/cpp/multistage/) 指南中构建的 Docker 镜像。如果你尚未构建该镜像，请先按照该指南中的步骤完成构建。
镜像名为 `hello`。要为 `hello` 镜像生成 SBOM，请运行以下命令：

```bash
$ docker sbom hello
```

命令将显示 "No packages discovered"（未发现包）。这是因为最终镜像是一个 scratch 镜像，不包含任何包。
让我们改用 Docker Scout 尝试：

```bash
$ docker scout sbom --format=list hello
```

此命令会告诉你同样的结果。

## 生成 SBOM 证明

SBOM 可以在构建过程中生成并"附加"到镜像上。这称为 SBOM 证明。
要为 `hello` 镜像生成 SBOM 证明，首先修改 Dockerfile：

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

第一行 `ARG BUILDKIT_SBOM_SCAN_STAGE=true` 在构建阶段启用了 SBOM 扫描。
现在，使用以下命令构建镜像：

```bash
$ docker buildx build --sbom=true -t hello:sbom .
```

此命令将构建镜像并生成 SBOM 证明。你可以通过运行以下命令验证 SBOM 已附加到镜像：

```bash
$ docker scout sbom --format=list hello:sbom
```

注意：普通的 `docker sbom` 命令无法加载 SBOM 证明。

## 总结

在本节中，你学会了如何在构建过程中为 C++ Docker 镜像生成 SBOM 证明。
普通的镜像扫描器无法从 scratch 镜像生成 SBOM。