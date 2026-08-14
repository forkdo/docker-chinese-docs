---
title: .NET
description: 将 .NET 应用程序迁移到 Docker Hardened Images
weight: 40
keywords: dotnet, .net, csharp, aspnet, migration, dhi
---

本示例展示如何将 .NET 应用程序迁移到 Docker 安全加固镜像。

以下示例展示了迁移到 Docker 安全加固镜像之前和之后的 Dockerfile。每个示例包含四种变体：

- 之前（Wolfi）：使用 Wolfi 发行版镜像的示例 Dockerfile，迁移到 DHI 之前
- 之前（DOI）：使用 Docker 官方镜像的示例 Dockerfile，迁移到 DHI 之前
- 之后（多阶段）：迁移到 DHI 后使用多阶段构建的示例 Dockerfile（推荐用于最小化、安全的镜像）
- 之后（单阶段）：迁移到 DHI 后使用单阶段构建的示例 Dockerfile（更简单，但会导致更大的镜像和更广的攻击面）

> [!NOTE]
>
> 大多数使用场景推荐使用多阶段构建。单阶段构建受支持是为了简化，但在大小和安全性方面存在权衡。
>
> 在拉取 Docker 安全加固镜像之前，您必须对 `dhi.io` 进行身份验证。使用您的 Docker ID 凭据（即用于 Docker Hub 的相同用户名和密码）。如果您没有 Docker 账户，请[免费创建一个](../../../accounts/create-account.md)。
>
> 运行 `docker login dhi.io` 进行身份验证。

{{< tabs >}}
{{< tab name="之前（Wolfi）" >}}

```dockerfile
#syntax=docker/dockerfile:1

FROM cgr.dev/chainguard/dotnet-sdk:latest-dev AS builder

WORKDIR /src
COPY . ./

# 如果需要，使用 apk 安装任何其他包
# RUN apk add --no-cache git

RUN dotnet restore
RUN dotnet publish -c Release -o /src/out --no-restore

FROM cgr.dev/chainguard/aspnet-runtime:latest

WORKDIR /app
COPY --from=builder /src/out ./

ENTRYPOINT ["dotnet", "app.dll"]
```

{{< /tab >}}
{{< tab name="之前（DOI）" >}}

```dockerfile
#syntax=docker/dockerfile:1

FROM mcr.microsoft.com/dotnet/sdk:8.0 AS builder

WORKDIR /src
COPY . ./

# 如果需要，使用 apt 安装任何其他包
# RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

RUN dotnet restore
RUN dotnet publish -c Release -o /app --no-restore

FROM mcr.microsoft.com/dotnet/aspnet:8.0

WORKDIR /app
COPY --from=builder /app ./

ENTRYPOINT ["dotnet", "app.dll"]
```

{{< /tab >}}
{{< tab name="之后（多阶段）" >}}

```dockerfile
#syntax=docker/dockerfile:1

# === 构建阶段：还原、构建并发布 .NET 应用程序 ===
FROM dhi.io/dotnet:8-sdk-alpine3.22 AS builder

WORKDIR /src
COPY . ./

# 如果需要，使用 apk 安装任何其他包
# RUN apk add --no-cache git

RUN dotnet restore
RUN dotnet publish -c Release -o /app --no-restore

# === 最终阶段：创建最小化运行时镜像 ===
FROM dhi.io/aspnetcore:8-alpine3.22

WORKDIR /app
COPY --from=builder /app ./

ENTRYPOINT ["dotnet", "app.dll"]
```

{{< /tab >}}
{{< tab name="之后（单阶段）" >}}

```dockerfile
#syntax=docker/dockerfile:1

FROM dhi.io/dotnet:8-sdk-alpine3.22

WORKDIR /src
COPY . ./

# 如果需要，使用 apk 安装任何其他包
# RUN apk add --no-cache git

RUN dotnet restore
RUN dotnet publish -c Release -o /app --no-restore

WORKDIR /app

ENTRYPOINT ["dotnet", "/app/app.dll"]
```

{{< /tab >}}
{{< /tabs >}}
