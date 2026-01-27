---
title: 使用 Docker 加固镜像
linktitle: 使用镜像
description: 了解如何在 Dockerfile、CI 流水线以及标准开发工作流中拉取、运行和引用 Docker 加固镜像。
keywords: use hardened image, docker pull secure image, non-root containers, multi-stage dockerfile, dev image variant
weight: 30
---

你可以像使用 Docker Hub 上的任何其他镜像一样使用 Docker 加固镜像（DHI）。DHI 遵循相同的熟悉使用模式：使用 `docker pull` 拉取镜像，在 Dockerfile 中引用它们，并使用 `docker run` 运行容器。

关键区别在于，DHI 专注于安全性，并且有意保持最小化以减少攻击面。这意味着某些变体默认不包含 shell 或包管理器，并且可能以非 root 用户身份运行。

> [!重要]
>
> 你必须向 Docker 加固镜像注册表 (`dhi.io`) 进行身份验证才能拉取镜像。登录时请使用你的 Docker ID 凭据（即你在 Docker Hub 上使用的相同用户名和密码）。如果你没有 Docker 账户，请[免费创建一个](../../accounts/create-account.md)。
>
> 运行 `docker login dhi.io` 进行身份验证。

## 采用 DHI 时的注意事项

Docker 加固镜像有意保持最小化以提高安全性。如果你正在更新现有的 Dockerfile 或框架以使用 DHI，请牢记以下注意事项：

| 功能 | 详情 |
|--------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 无 shell 或包管理器 | 运行时镜像不包含 shell 或包管理器。在构建阶段使用 `-dev` 或 `-sdk` 变体来运行 shell 命令或安装包，然后将构建产物复制到最小化的运行时镜像中。 |
| 非 root 运行时 | 运行时 DHI 默认以非 root 用户身份运行。确保你的应用程序不需要特权访问权限，并且所有必需的文件都可被非 root 用户读取和执行。 |
| 端口 | 在旧版本 Docker 或某些 Kubernetes 配置中，以非 root 用户身份运行的应用程序无法绑定到 1024 以下的端口。为了兼容性，请使用 1024 以上的端口。 |
| 入口点 | DHI 可能不包含默认入口点，或者其入口点与你熟悉的原始镜像不同。请检查镜像配置，并相应地更新你的 `CMD` 或 `ENTRYPOINT` 指令。 |
| 多阶段构建 | 对于框架，始终使用多阶段构建：在构建阶段使用 `-dev` 镜像，在最终阶段使用最小化的运行时镜像。 |
| TLS 证书 | DHI 包含标准 TLS 证书。你无需手动安装 CA 证书。 |

如果你正在迁移现有应用程序，请参阅[将现有应用程序迁移以使用 Docker 加固镜像](../migration/_index.md)。

## 在 Dockerfile 中使用 DHI

要将 DHI 用作容器的基础镜像，请在 Dockerfile 的 `FROM` 指令中指定它：

```dockerfile
FROM dhi.io/<image>:<tag>
```

将镜像名称和标签替换为你要使用的变体。例如，如果你在构建阶段需要 shell 或包管理器，请使用 `-dev` 标签：

```dockerfile
FROM dhi.io/python:3.13-dev AS build
```

要了解如何探索可用的变体，请参阅[探索镜像](./explore.md)。

> [!提示]
>
> 使用多阶段 Dockerfile 来分离构建和运行时阶段：在构建阶段使用 `-dev` 变体，在最终阶段使用最小化的运行时镜像。

## 拉取 DHI

与任何其他镜像一样，你可以使用 Docker CLI 等工具或在 CI 流水线中拉取 DHI。

你可以根据需求从三个不同位置拉取 Docker 加固镜像：

- 直接从 `dhi.io`
- 从 Docker Hub 上的镜像仓库
- 从第三方注册表上的镜像仓库

要了解哪种方法适合你的使用场景，请参阅[镜像 Docker 加固镜像仓库](./mirror.md)。

以下章节展示了如何从每个位置拉取镜像。

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

### 从 Docker Hub 上的镜像仓库拉取

一旦将仓库镜像到 Docker Hub，你就可以从你的组织命名空间中拉取镜像：

```console
$ docker login
$ docker pull <your-namespace>/dhi-python:3.13
```

在 Dockerfile 中引用镜像化的镜像：

```dockerfile
FROM <your-namespace>/dhi-python:3.13
COPY . /app
CMD ["python", "/app/main.py"]
```

要了解如何镜像仓库，请参阅[将 DHI 仓库镜像到 Docker Hub](./mirror.md#mirror-a-dhi-repository-to-docker-hub)。

### 从第三方注册表上的镜像仓库拉取

一旦将仓库镜像到你的第三方注册表，你就可以拉取镜像：

```console
$ docker pull <your-registry>/<your-namespace>/python:3.13
```

在 Dockerfile 中引用第三方镜像化的镜像：

```dockerfile
FROM <your-registry>/<your-namespace>/python:3.13
COPY . /app
CMD ["python", "/app/main.py"]
```

要了解详细信息，请参阅[镜像到第三方注册表](./mirror.md#mirror-to-a-third-party-registry)。

## 运行 DHI

拉取镜像后，你可以使用 `docker run` 运行它。例如：

```console
$ docker run --rm dhi.io/python:3.13 python -c "print('Hello from DHI')"
```

## 在 CI/CD 流水线中使用 DHI

Docker 加固镜像在你的 CI/CD 流水线中的使用方式与其他任何镜像相同。你可以在 Dockerfile 中引用它们，在流水线步骤中拉取它们，或在构建和测试期间基于它们运行容器。

与典型的容器镜像不同，DHI 还包含已签名的[证明](../core-concepts/attestations.md)，例如 SBOM 和来源元数据。如果你的工具支持，你可以将这些证明集成到流水线中，以支持供应链安全、策略检查或审计要求。

为了加强你的软件供应链，请考虑在使用 DHI 构建镜像时添加你自己的证明。这使你能够记录镜像的构建方式、验证其完整性，并使用 Docker Scout 等工具实现下游验证和策略执行。

要了解如何在构建过程中附加证明，请参阅 [Docker Build 证明](/manuals/build/metadata/attestations.md)。

## 为编译后的可执行文件使用静态镜像

Docker 加固镜像包含一个专门设计用于在极其最小化和安全的运行时中运行编译后可执行文件的 `static` 镜像仓库。

与未加固的 `FROM scratch` 镜像不同，DHI `static` 镜像包含验证其完整性和来源所需的所有证明。尽管它是最小化的，但它包含了安全运行容器所需的通用包，例如 `ca-certificates`。

在早期阶段使用 `-dev` 或其他构建器镜像来编译你的二进制文件，并将输出复制到 `static` 镜像中。

以下示例展示了一个多阶段 Dockerfile，它构建了一个 Go 应用程序并在最小化的静态镜像中运行它：

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

这种模式确保了强化的运行时环境，不包含任何不必要的组件，从而将攻击面降至最低。

## 对基于框架的应用程序使用 dev 变体

如果您正在使用需要包管理器或构建工具（如 Python、Node.js 或 Go）的框架构建应用程序，请在开发或构建阶段使用 `-dev` 变体。这些变体包含 shell、编译器和包管理器等必要工具，以支持本地迭代和 CI 工作流。

在内部开发循环或隔离的 CI 阶段使用 `-dev` 镜像，以最大限度地提高生产力。当您准备好为生产环境生成制品时，请切换到更小的运行时变体，以减少攻击面和镜像大小。

Dev 变体通常配置为没有 `ENTRYPOINT`，并设置一个默认的 `CMD` 来启动 shell（例如 ["/bin/bash"]）。在这种情况下，运行容器时若不添加额外参数，默认会启动交互式 shell。

以下示例展示了如何使用 `-dev` 变体构建 Python 应用程序，并使用更小的运行时变体运行它：

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

这种模式将构建环境与运行时环境分离，有助于减小镜像大小，并通过从最终镜像中移除不必要的工具来提高安全性。

## 使用合规变体 {tier="DHI Enterprise"}

{{< summary-bar feature_name="Docker Hardened Images" >}}

当您拥有 Docker Hardened Images Enterprise 订阅时，可以访问合规变体，例如启用 FIPS 和符合 STIG 要求的镜像。这些变体有助于满足安全部署的监管和合规要求。

要使用合规变体，您必须首先[镜像](./mirror.md)仓库，然后从镜像仓库中拉取合规镜像。