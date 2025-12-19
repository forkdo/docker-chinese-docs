---
title: 使用 Docker Hardened Image
linktitle: 使用镜像
description: 了解如何在 Dockerfile、CI 流程和标准开发工作流中拉取、运行和引用 Docker Hardened Image。
keywords: 使用加固镜像, docker 拉取安全镜像, 非 root 容器, 多阶段 Dockerfile, 开发镜像变体
weight: 30
---

您可以像使用 Docker Hub 上的任何其他镜像一样使用 Docker Hardened Image (DHI)。DHI 遵循相同的常用使用模式。使用 `docker pull` 拉取它们，在 Dockerfile 中引用它们，并使用 `docker run` 运行容器。

关键区别在于，DHI 专注于安全性，并且有意设计得极为精简，以减少攻击面。这意味着某些变体不包含 shell 或包管理器，并且默认可能以非 root 用户身份运行。

> [!IMPORTANT]
>
> 您必须向 Docker Hardened Images 仓库 (`dhi.io`) 进行身份验证才能拉取镜像。登录时请使用您的 Docker ID 凭据（与您用于 Docker Hub 的用户名和密码相同）。如果您没有 Docker 账户，可以[免费创建一个](../../accounts/create-account.md)。
>
> 运行 `docker login dhi.io` 进行身份验证。

## 采用 DHI 时的注意事项

Docker Hardened Images 有意设计得极为精简以提高安全性。如果您正在更新现有的 Dockerfile 或框架以使用 DHI，请牢记以下注意事项：

| 功能 | 详情 |
|--------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 无 shell 或包管理器 | 运行时镜像不包含 shell 或包管理器。在构建阶段使用 `-dev` 或 `-sdk` 变体来运行 shell 命令或安装包，然后将构建产物复制到精简的运行时镜像中。 |
| 非 root 运行时 | 运行时 DHI 默认以非 root 用户身份运行。确保您的应用程序不需要特权访问，并且所有需要的文件都对非 root 用户可读且可执行。 |
| 端口 | 以非 root 用户身份运行的应用程序在旧版本的 Docker 或某些 Kubernetes 配置中无法绑定到 1024 以下的端口。为确保兼容性，请使用 1024 以上的端口。 |
| 入口点 (Entry point) | DHI 可能不包含默认入口点，或者可能使用与您熟悉的原始镜像不同的入口点。请检查镜像配置，并相应地更新您的 `CMD` 或 `ENTRYPOINT` 指令。 |
| 多阶段构建 | 始终为框架使用多阶段构建：使用 `-dev` 镜像进行构建或安装依赖项，并在最后阶段使用精简的运行时镜像。 |
| TLS 证书 | DHI 包含标准 TLS 证书。您无需手动安装 CA 证书。 |

如果您正在迁移现有应用程序，请参阅[将现有应用程序迁移到使用 Docker Hardened Images](../migration/_index.md)。

## 在 Dockerfile 中使用 DHI

要将 DHI 用作容器的基础镜像，请在 Dockerfile 的 `FROM` 指令中指定它：

```dockerfile
FROM dhi.io/<image>:<tag>
```

将镜像名称和标签替换为您要使用的变体。例如，如果您在构建阶段需要 shell 或包管理器，请使用 `-dev` 标签：

```dockerfile
FROM dhi.io/python:3.13-dev AS build
```

要了解如何探索可用的变体，请参阅[探索镜像](./explore.md)。

> [!TIP]
>
> 使用多阶段 Dockerfile 将构建阶段和运行时阶段分开，在构建阶段使用 `-dev` 变体，在最后阶段使用精简的运行时镜像。

## 拉取 DHI

就像任何其他镜像一样，您可以使用 Docker CLI 等工具或在 CI 流程中拉取 DHI。

根据您的需求，您可以从三个不同的位置拉取 Docker Hardened Images：

- 直接从 `dhi.io`
- 从 Docker Hub 上的镜像
- 从第三方仓库上的镜像

要了解哪种方法适合您的用例，请参阅[镜像 Docker Hardened Image 仓库](./mirror.md)。

以下部分展示了如何从每个位置拉取镜像。

### 直接从 dhi.io 拉取

向 `dhi.io` 进行身份验证后，您可以使用标准 Docker 命令拉取镜像：

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

将仓库镜像到 Docker Hub 后，您可以从您的组织命名空间拉取镜像：

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

要了解如何镜像仓库，请参阅[将 DHI 仓库镜像到 Docker Hub](./mirror.md#mirror-a-dhi-repository-to-docker-hub)。

### 从第三方仓库上的镜像拉取

将仓库镜像到您的第三方仓库后，您可以拉取镜像：

```console
$ docker pull <your-registry>/<your-namespace>/python:3.13
```

在 Dockerfile 中引用第三方镜像的镜像：

```dockerfile
FROM <your-registry>/<your-namespace>/python:3.13
COPY . /app
CMD ["python", "/app/main.py"]
```

要了解更多信息，请参阅[镜像到第三方仓库](./mirror.md#mirror-to-a-third-party-registry)。

## 运行 DHI

拉取镜像后，您可以使用 `docker run` 运行它。例如：

```console
$ docker run --rm dhi.io/python:3.13 python -c "print('Hello from DHI')"
```

## 在 CI/CD 流程中使用 DHI

Docker Hardened Images 在您的 CI/CD 流程中就像任何其他镜像一样工作。
您可以在 Dockerfile 中引用它们，作为流程步骤的一部分拉取它们，或者在构建和测试期间运行基于它们的容器。

与典型的容器镜像不同，DHI 还包含签名的[证明](../core-concepts/attestations.md)，例如 SBOM 和来源元数据。如果您的工具支持，您可以将这些纳入您的流程中，以支持供应链安全、策略检查或审计要求。

为了加强您的软件供应链，考虑在从 DHI 构建镜像时添加您自己的证明。这可以让您记录镜像的构建方式，验证其完整性，并使用 Docker Scout 等工具实现下游验证和策略执行。

要了解如何在构建过程中附加证明，请参阅[Docker Build 证明](/manuals/build/metadata/attestations.md)。

## 为编译后的可执行文件使用静态镜像

Docker Hardened Images 包含一个专门设计的 `static` 镜像仓库，用于在极其精简和安全的运行时中运行编译后的可执行文件。

与非加固的 `FROM scratch` 镜像不同，DHI `static` 镜像包含验证其完整性和来源所需的所有证明。虽然它很精简，但它包含安全运行容器所需的常用软件包，例如 `ca-certificates`。

在早期阶段使用 `-dev` 或其他构建器镜像来编译您的二进制文件，并将输出复制到 `static` 镜像中。

以下示例展示了一个多阶段 Dockerfile，它构建一个 Go 应用程序并在精简的静态镜像中运行它：

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

这种模式确保了加固的运行时环境，没有不必要的组件，将攻击面降至最低。

## 为基于框架的应用程序使用开发变体

如果您正在构建需要包管理器或构建工具（如 Python、Node.js 或 Go）的应用程序，请在开发或构建阶段使用 `-dev` 变体。这些变体包含基本的实用程序，如 shell、编译器和包管理器，以支持本地迭代和 CI 工作流。

在内部开发循环或隔离的 CI 阶段中使用 `-dev` 镜像，以最大化生产力。一旦您准备好为生产环境生成工件，请切换到更小的运行时变体，以减少攻击面和镜像大小。

开发变体通常配置为没有 `ENTRYPOINT`，并且默认 `CMD` 是启动 shell（例如 ["/bin/bash"]）。在这些情况下，运行容器而不带附加参数会默认启动一个交互式 shell。

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

这种模式将构建环境与运行时环境分开，有助于减少镜像大小，并通过从最终镜像中删除不必要的工具来提高安全性。

## 使用合规变体 {{< badge color="blue" text="DHI Enterprise" >}}

{{< summary-bar feature_name="Docker Hardened Images" >}}

当您拥有 Docker Hardened Images Enterprise 订阅时，您可以访问合规变体，例如启用 FIPS 和准备 STIG 的镜像。这些变体有助于满足安全部署的监管和合规要求。

要使用合规变体，您必须首先[镜像](./mirror.md)仓库，然后从您的镜像仓库中拉取合规镜像。