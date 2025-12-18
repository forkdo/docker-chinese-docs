---
title: 从 Wolfi 迁移
description: 从基于 Wolfi 的镜像迁移到 Docker Hardened Images 的分步指南
weight: 30
keywords: wolfi, chainguard, 迁移, dhi
---

本指南帮助你将基于 Wolfi 的镜像迁移到 Docker Hardened Images（DHI）。通常，迁移过程非常直接，因为 Wolfi 类似 Alpine，而 DHI 提供基于 Alpine 的加固镜像。

与其他加固镜像一样，DHI 提供全面的[证明](/dhi/core概念/attestations/)，包括 SBOM 和来源信息，允许你[验证](/manuals/dhi/how-to/verify.md)镜像签名并[扫描](/manuals/dhi/how-to/scan.md)漏洞，以确保镜像的安全性和完整性。

## 迁移步骤

以下示例演示如何将 Dockerfile 从基于 Wolfi 的镜像迁移到基于 Alpine 的 Docker Hardened Image。

### 步骤 1：更新 Dockerfile 中的基础镜像

在应用程序的 Dockerfile 中将基础镜像更新为加固镜像。这通常是标记为 `dev` 或 `sdk` 的镜像，因为它包含安装包和依赖项所需的工具。

以下来自 Dockerfile 的示例差异片段显示了旧的基础镜像被新加固镜像替换。

> [!NOTE]
>
> 在拉取 Docker Hardened Images 之前，你必须先对 `dhi.io` 进行身份验证。
> 使用你的 Docker ID 凭据（与 Docker Hub 相同的用户名和密码）。如果你没有 Docker 账户，请[创建一个](../../accounts/create-account.md)免费账户。
>
> 运行 `docker login dhi.io` 进行身份验证。

```diff
- ## 原始基础镜像
- FROM cgr.dev/chainguard/go:latest-dev

+ ## 更新为使用加固基础镜像
+ FROM dhi.io/golang:1.25-alpine3.22-dev
```

请注意，DHI 没有 `latest` 标签，以促进镜像版本控制的最佳实践。确保你为镜像指定适当的版本标签。要找到正确的标签，请在 [DHI 目录](https://hub.docker.com/hardened-images/catalog/) 中探索可用的标签。

### 步骤 2：更新 Dockerfile 中的运行时镜像

> [!NOTE]
>
> 建议使用多阶段构建以保持最终镜像最小化和安全。单阶段构建受支持，但它们包含完整的 `dev` 镜像，因此会导致更大的镜像和更广泛的攻击面。

为确保最终镜像尽可能最小化，你应该使用[多阶段构建](/manuals/build/building/multi-stage.md)。Dockerfile 中的所有阶段都应使用加固镜像。虽然中间阶段通常使用标记为 `dev` 或 `sdk` 的镜像，但你的最终运行时阶段应使用运行时镜像。

利用构建阶段编译你的应用程序，并将生成的构件复制到最终运行时阶段。这确保你的最终镜像最小化且安全。

以下示例显示了一个具有构建阶段和运行时阶段的多阶段 Dockerfile：

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

更新 Dockerfile 后，构建并测试你的应用程序。如果遇到问题，请参阅[故障排除](/manuals/dhi/troubleshoot.md)指南，了解常见问题和解决方案。

## 语言特定示例

请参阅示例部分，了解特定语言的迁移示例：

- [Go](examples/go.md)
- [Python](examples/python.md)
- [Node.js](examples/node.md)