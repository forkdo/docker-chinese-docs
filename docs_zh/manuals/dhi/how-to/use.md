---
title: 使用 Docker Hardened 镜像
linktitle: 使用镜像
description: 了解如何拉取、运行 Docker Hardened 镜像，并在 Dockerfile、CI 流水线和标准开发工作流中引用它们。
keywords: 使用加固镜像, docker pull 安全镜像, 非 root 容器, 多阶段 dockerfile, dev 镜像变体
weight: 30
---

你可以像使用 Docker Hub 上的任何其他镜像一样使用 Docker Hardened 镜像（DHI）。DHI 遵循相同的熟悉使用模式。使用 `docker pull` 拉取它们，在 Dockerfile 中引用它们，并使用 `docker run` 运行容器。

关键区别在于，DHI 专注于安全性，有意保持最小化以减少攻击面。这意味着某些变体不包含 shell 或包管理器，并且默认以非 root 用户身份运行。

> [!IMPORTANT]
>
> 你必须向 Docker Hardened Images 注册表 (`dhi.io`) 进行身份验证才能拉取镜像。使用你的 Docker ID 凭据（与你在 Docker Hub 上使用的相同用户名和密码）登录。如果你没有 Docker 账户，请[创建一个](../../accounts/create-account.md)免费账户。
>
> 运行 `docker login dhi.io` 进行身份验证。

## 采用 DHI 时的注意事项

Docker Hardened 镜像有意保持最小化以提高安全性。如果你正在更新现有的 Dockerfile 或框架以使用 DHI，请记住以下注意事项：

| 功能            | 详细信息                                                                                                                                                                                                                                               |
|--------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 无 shell 或包管理器 | 运行时镜像不包含 shell 或包管理器。在构建阶段使用 `-dev` 或 `-sdk` 变体来运行 shell 命令或安装包，然后将制品复制到最小的运行时镜像。                                         |
| 非 root 运行时    | 运行时 DHI 默认以非 root 用户身份运行。确保你的应用程序不需要特权访问，并且所有需要的文件对非 root 用户可读且可执行。                                                             |
| 端口               | 在旧版本的 Docker 或某些 Kubernetes 配置中，以非 root 用户身份运行的应用程序无法绑定到 1024 以下的端口。为兼容性使用 1024 以上的端口。                                             |
| 入口点         | DHI 可能不包含默认入口点，或者可能使用与你熟悉的原始镜像不同的入口点。检查镜像配置，并相应地更新你的 `CMD` 或 `ENTRYPOINT` 指令。                                        |
| 多阶段构建  | 对于框架，始终使用多阶段构建：在构建阶段使用 `-dev` 镜像，在最终阶段使用最小的运行时镜像。                                                                                                              |
| TLS 证书    | DHI 包含标准的 TLS 证书。你不需要手动安装 CA 证书。                                                                                                                                                               |

如果你正在迁移现有应用程序，请参阅 [将现有应用程序迁移到使用 Docker Hardened 镜像](../migration/_index.md)。

## 在 Dockerfile 中使用 DHI

要在容器中使用 DHI 作为基础镜像，请在 Dockerfile 的 `FROM` 指令中指定它：

```dockerfile
FROM dhi.io/<image>:<tag>
```

将镜像名称和标签替换为你想要使用的变体。例如，如果你在构建阶段需要 shell 或包管理器，请使用 `-dev` 标签：

```dockerfile
FROM dhi.io/python:3.13-dev AS build
```

要了解如何探索可用的变体，请参阅 [探索镜像](./explore.md)。

> [!TIP]
>
> 使用多阶段 Dockerfile 来分离构建和运行时阶段，在构建阶段使用 `-dev` 变体，在最终阶段使用最小的运行时镜像。

## 拉取 DHI

与任何其他镜像一样，你可以使用诸如 Docker CLI 或在 CI 流水线中等工具来拉取 DHI。

你可以根据需要从三个不同的位置拉取 Docker Hardened 镜像：

- 直接从 `dhi.io` 拉取
- 从 Docker Hub 上的镜像拉取
- 从第三方注册表上的镜像拉取

要了解哪种方法适合你的用例，请参阅 [镜像 Docker Hardened 镜像仓库](./mirror.md)。

以下部分展示了如何从每个位置拉取镜像。

### 直接从 dhi.io 拉取

在向 `dhi.io` 进行身份验证后，你可以使用标准 Docker 命令拉取镜像：

```console
$ docker login dhi.io
$ docker pull dhi.io/python:3.13
```

在 Dockerfile 中引用镜像：

```dockerfile
FROM dhi.io/python:3.13
COPY . /app
CMD ["python", "/app/main.py"]
```

### 从 Docker Hub 上的镜像拉取

一旦你将仓库镜像到 Docker Hub，你就可以从你的组织命名空间中拉取镜像：

```console
$ docker login
$ docker pull <your-namespace>/dhi-python:3.13
```

在 Dockerfile 中引用镜像的镜像：

```dockerfile
FROM <your-namespace>/dhi-python:3.13
COPY . /app
CMD ["python", "/app/main.py"]
```

要了解如何镜像仓库，请参阅 [将 DHI 仓库镜像到 Docker Hub](./mirror.md#mirror-a-dhi-repository-to-docker-hub)。

### 从第三方注册表上的镜像拉取

一旦你将仓库镜像到你的第三方注册表，你就可以拉取镜像：

```console
$ docker pull <your-registry>/<your-namespace>/python:3.13
```

在 Dockerfile 中引用第三方镜像：

```dockerfile
FROM <your-registry>/<your-namespace>/python:3.13
COPY . /app
CMD ["python", "/app/main.py"]
```

要了解更多信息，请参阅 [镜像到第三方注册表](./mirror.md#mirror-to-a-third-party-registry)。

## 运行 DHI

拉取镜像后，你可以使用 `docker run` 运行它。例如：

```console
$ docker run --rm dhi.io/python:3.13 python -c "print('Hello from DHI')"
```

## 在 CI/CD 流水线中使用 DHI

Docker Hardened 镜像在你的 CI/CD 流水线中的工作方式与任何其他镜像一样。
你可以在 Dockerfile 中引用它们，在流水线步骤中拉取它们，或者在构建和测试期间基于它们运行容器。

与典型的容器镜像不同，DHI 还包含已签名的[证明](../core-concepts/attestations.md)，如 SBOM 和出处元数据。如果你的工具支持，你可以将这些证明集成到你的流水线中，以支持供应链安全、策略检查或审计要求。

为了加强你的软件供应链，考虑在从 DHI 构建镜像时添加你自己的证明。这让你可以记录镜像是如何构建的，验证其完整性，并使用 Docker Scout 等工具启用下游验证和策略执行。

要了解如何在构建过程中附加证明，请参阅 [Docker 构建证明](/manuals/build/metadata/attestations.md)。

## 为编译的可执行文件使用静态镜像

Docker Hardened 镜像包含一个专门设计的 `static` 镜像仓库，用于在极小且安全的运行时中运行编译的可执行文件。

与非加固的 `FROM scratch` 镜像不同，DHI `static` 镜像包含验证其完整性并和出处所需的所有证明。尽管它是最小的，但它包含了安全运行容器所需的所有常用包，如 `ca-certificates`。

在早期阶段使用 `-dev` 或其他构建镜像来编译你的二进制文件，并将输出复制到 `static` 镜像中。

以下示例展示了一个多阶段 Dockerfile，它构建一个 Go 应用程序并在最小的静态镜像中运行：

```dockerfile
#syntax=docker/dockerfile:1

FROM dhi.io/golang:1.22-dev AS build
WORKDIR /app
COPY . .
RUN CGO_ENABLED=0 go build -o myapp

FROM dhi.io/static:20230311
COPY --from=build /app/myapp /myapp
ENTRYPOINT ["/myapp"]
```

这种模式确保了一个加固的运行时环境，没有任何不必要的组件，将攻击面减少到最小。

## 为基于框架的应用程序使用 dev 变体

如果你正在使用需要包管理器或构建工具的框架（如 Python、Node.js 或 Go）构建应用程序，请在开发或构建阶段使用 `-dev` 变体。这些变体包含支持本地迭代和 CI 工作流所需的基本工具，如 shell、编译器和包管理器。

在你的内部开发循环或隔离的 CI 阶段使用 `-dev` 镜像以最大化生产力。当你准备好为生产生成制品时，切换到更小的运行时变体以减少攻击面和镜像大小。

dev 变体通常配置为没有 `ENTRYPOINT`，并具有启动 shell 的默认 `CMD`（例如，["/bin/bash"]）。在这些情况下，不带额外参数运行容器默认会启动交互式 shell。

以下示例展示如何使用 `-dev` 变体构建 Python 应用程序并使用较小的运行时变体运行：

```dockerfile
#syntax=docker/dockerfile:1

FROM dhi.io/python:3.13-alpine3.21-dev AS builder

ENV LANG=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/venv/bin:$PATH"

WORKDIR /app

RUN python -m venv /app/venv
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

FROM dhi.io/python:3.13-alpine3.21

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PATH="/app/venv/bin:$PATH"

COPY image.py image.png ./
COPY --from=builder /app/venv /app/venv

ENTRYPOINT [ "python", "/app/image.py" ]
```

这种模式将构建环境与运行时环境分离，通过从最终镜像中移除不必要的工具来帮助减少镜像大小并提高安全性。

## 使用合规变体 {{< badge color="blue" text="DHI Enterprise" >}}

{{< summary-bar feature_name="Docker Hardened Images" >}}

当你拥有 Docker Hardened Images Enterprise 订阅时，你可以访问合规变体，如启用 FIPS 和符合 STIG 的镜像。这些变体有助于满足安全部署的监管和合规要求。

要使用合规变体，你必须首先[镜像](./mirror.md)仓库，然后从你的镜像仓库中拉取合规镜像。