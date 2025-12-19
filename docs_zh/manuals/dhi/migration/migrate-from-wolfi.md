---
title: 从 Wolfi 迁移
description: 从 Wolfi 发行版镜像迁移到 Docker 加固镜像的分步指南
weight: 30
keywords: wolfi, chainguard, migration, dhi
---

本指南帮助您从基于 Wolfi 的镜像迁移到 Docker 加固镜像 (DHI)。通常来说，迁移过程非常简单，因为 Wolfi 与 Alpine 类似，而 DHI 提供基于 Alpine 的加固镜像。

与其他加固镜像一样，DHI 提供全面的[证明](/dhi/core-concepts/attestations/)，包括 SBOM 和来源信息，使您能够[验证](/manuals/dhi/how-to/verify.md)镜像签名并[扫描](/manuals/dhi/how-to/scan.md)漏洞，以确保镜像的安全性和完整性。

## 迁移步骤

以下示例演示如何将 Dockerfile 从基于 Wolfi 的镜像迁移到基于 Alpine 的 Docker 加固镜像。

### 步骤 1：更新 Dockerfile 中的基础镜像

将应用程序 Dockerfile 中的基础镜像更新为加固镜像。通常，这将是标记为 `dev` 或 `sdk` 的镜像，因为它包含安装软件包和依赖项所需的工具。

以下 Dockerfile 的 diff 片段示例展示了旧基础镜像被新的加固镜像替换的过程。

> [!注意]
>
> 在拉取 Docker 加固镜像之前，您必须向 `dhi.io` 进行身份验证。
> 使用您的 Docker ID 凭据（与 Docker Hub 相同的用户名和密码）。如果您没有 Docker 账户，请免费[创建一个](../../accounts/create-account.md)。
>
> 运行 `docker login dhi.io` 进行身份验证。

```diff
- ## 原始基础镜像
- FROM cgr.dev/chainguard/go:latest-dev

+ ## 更新为使用加固基础镜像
+ FROM dhi.io/golang:1.25-alpine3.22-dev
```

请注意，DHI 没有 `latest` 标签，以促进镜像版本控制的最佳实践。请确保为您的镜像指定适当的版本标签。要找到正确的标签，请浏览 [DHI 目录](https://hub.docker.com/hardened-images/catalog/) 中的可用标签。

### 步骤 2：更新 Dockerfile 中的运行时镜像

> [!注意]
>
> 建议采用多阶段构建，以保持最终镜像的最小化和安全性。支持单阶段构建，但它们包含完整的 `dev` 镜像，因此会导致镜像更大，攻击面更广。

为了确保最终镜像尽可能最小化，您应该使用[多阶段构建](/manuals/build/building/multi-stage.md)。Dockerfile 中的所有阶段都应使用加固镜像。虽然中间阶段通常使用标记为 `dev` 或 `sdk` 的镜像，但最终运行时阶段应使用运行时镜像。

利用构建阶段编译您的应用程序，并将生成的制品复制到最终运行时阶段。这可确保您的最终镜像最小化且安全。

以下示例展示了具有构建阶段和运行时阶段的多阶段 Dockerfile：

```dockerfile
# 构建阶段
FROM dhi.io/golang:1.25-alpine3.22-dev AS builder
WORKDIR /app
COPY . .
RUN go build -o myapp

# 运行时阶段
FROM dhi.io/golang:1.25-alpine3.22
WORKDIR /app
COPY --from=builder /app/myapp .
ENTRYPOINT ["/app/myapp"]
```

更新 Dockerfile 后，构建并测试您的应用程序。如果遇到问题，请参阅[故障排除](/manuals/dhi/troubleshoot.md)指南，了解常见问题及其解决方案。

## 语言特定示例

请参阅示例部分，了解语言特定的迁移示例：

- [Go](examples/go.md)
- [Python](examples/python.md)
- [Node.js](examples/node.md)