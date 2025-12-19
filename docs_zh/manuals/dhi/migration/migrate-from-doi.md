---
title: 从 Alpine 或 Debian 迁移
description: 从 Docker 官方镜像迁移到 Docker Hardened 镜像的分步指南
weight: 20
keywords: docker official images, doi, migration, dhi, alpine, debian
---

Docker Hardened 镜像（DHI）提供基于 [Alpine 和 Debian 的变体](../explore/available.md)。在许多情况下，从基于这些发行版的其他镜像迁移，只需在 Dockerfile 中更改基础镜像即可。

本指南帮助你从现有的基于 Alpine 或 Debian 的 Docker 官方镜像（DOI）迁移到 DHI。

如果你当前使用的是基于 Debian 的 Docker 官方镜像，请迁移到基于 Debian 的 DHI 变体。如果你使用的是基于 Alpine 的镜像，请迁移到基于 Alpine 的 DHI 变体。这可以最大限度地减少迁移过程中包管理和依赖项的变化。

## 主要差异

从非加固镜像迁移到 DHI 时，请注意以下主要差异：

| 项目               | 非加固镜像                                                                                                                                                                                                                                                                                                         | Docker Hardened 镜像                                                                                                                                                                                                                                                                                                         |
|:-------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 包管理             | 包管理器通常在所有镜像中可用                                                                                                                                                                                                                                                                                                | 包管理器通常仅在带有 `dev` 标签的镜像中可用。运行时镜像不包含包管理器。使用多阶段构建，将必要的构件从构建阶段复制到运行时阶段。                                                                                                                                                                                                 |
| 非 root 用户       | 默认通常以 root 身份运行                                                                                                                                                                                                                                                                                                | 运行时变体默认以非 root 用户身份运行。确保必要的文件和目录对非 root 用户可访问。                                                                                                                                                                                                                                                                          |
| 多阶段构建         | 可选                                                                                                                                                                                                                                                                                                                       | 推荐。在构建阶段使用带有 `dev` 或 `sdk` 标签的镜像，在运行时使用非 dev 镜像。                                                                                                                                                                                                                           |
| TLS 证书           | 可能需要安装                                                                                                                                                                                                                                                                                                       | 默认包含标准 TLS 证书。无需安装 TLS 证书。                                                                                                                                                                                                                                   |
| 端口               | 以 root 身份运行时可以绑定到特权端口（低于 1024）                                                                                                                                                                                                                                                                 | 默认以非 root 用户身份运行。在 Kubernetes 中或在 Docker Engine 20.10 之前的版本中运行时，应用程序无法绑定到特权端口（低于 1024）。配置你的应用程序在容器内监听 1025 或更高的端口。                                                                                                                                                                                                        |
| 入口点             | 因镜像而异                                                                                                                                                                                                                                                                                                                | 可能与 Docker 官方镜像有不同的入口点。检查入口点，如有必要更新你的 Dockerfile。                                                                                                                                                                                                    |
| 无 Shell           | Shell 通常在所有镜像中可用                                                                                                                                                                                                                                                                                                  | 运行时镜像不包含 Shell。在构建阶段使用 `dev` 镜像运行 Shell 命令，然后将构件复制到运行时阶段。                                                                                                                                                                                      |

## 迁移步骤

### 步骤 1：更新 Dockerfile 中的基础镜像

在应用程序的 Dockerfile 中将基础镜像更新为加固镜像。这通常是带有 `dev` 或 `sdk` 标签的镜像，因为它具有安装包和依赖项所需的工具。

以下示例来自 Dockerfile 的差异片段，显示了旧基础镜像被新加固镜像替换：

> [!NOTE]
>
> 在拉取 Docker Hardened 镜像之前，你必须对 `dhi.io` 进行身份验证。
> 使用你的 Docker ID 凭据（与 Docker Hub 相同的用户名和密码）。如果你没有 Docker 账户，[免费创建一个](../../accounts/create-account.md)。
>
> 运行 `docker login dhi.io` 进行身份验证。

```diff
- ## 原始基础镜像
- FROM golang:1.25

+ ## 更新为使用加固基础镜像
+ FROM dhi.io/golang:1.25-debian12-dev
```

注意，DHI 没有 `latest` 标签，以促进镜像版本控制的最佳实践。确保你为镜像指定适当的版本标签。要找到正确的标签，请在 [DHI 目录](https://hub.docker.com/hardened-images/catalog/) 中探索可用的标签。此外，分发基础在标签中指定（例如，`-alpine3.22` 或 `-debian12`），因此请确保为你的应用程序选择正确的变体。

### 步骤 2：更新 Dockerfile 中的运行时镜像

> [!NOTE]
>
> 建议使用多阶段构建以保持最终镜像最小化和安全。单阶段构建受支持，但它们包含完整的 `dev` 镜像，因此会导致更大的镜像和更广泛的攻击面。

为确保你的最终镜像尽可能最小化，你应该使用[多阶段构建](/manuals/build/building/multi-stage.md)。Dockerfile 中的所有阶段都应使用加固镜像。虽然中间阶段通常使用带有 `dev` 或 `sdk` 标签的镜像，但你的最终运行时阶段应使用运行时镜像。

利用构建阶段编译你的应用程序，并将生成的构件复制到最终运行时阶段。这确保你的最终镜像是最小化和安全的。

以下示例显示了一个具有构建阶段和运行时阶段的多阶段 Dockerfile：

```dockerfile
# 构建阶段
FROM dhi.io/golang:1.25-debian12-dev AS builder
WORKDIR /app
COPY . .
RUN go build -o myapp

# 运行时阶段
FROM dhi.io/golang:1.25-debian12
WORKDIR /app
COPY --from=builder /app/myapp .
ENTRYPOINT ["/app/myapp"]
```

更新 Dockerfile 后，构建并测试你的应用程序。如果遇到问题，请参阅 [故障排除](/manuals/dhi/troubleshoot.md) 指南，了解常见问题和解决方案。

## 语言特定示例

请参阅示例部分，了解特定语言的迁移示例：

- [Go](examples/go.md)
- [Python](examples/python.md)
- [Node.js](examples/node.md)