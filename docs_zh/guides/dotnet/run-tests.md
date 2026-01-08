---
title: 在容器中运行 .NET 测试
linkTitle: 运行测试
weight: 30
keywords: .NET, test
description: 了解如何在容器中运行 .NET 测试。
aliases:
- /language/dotnet/run-tests/
- /guides/language/dotnet/run-tests/
---

## 先决条件

完成本指南中从[容器化 .NET 应用程序](containerize.md)开始的所有先前部分。

## 概述

测试是现代软件开发的重要组成部分。对于不同的开发团队，测试可能意味着很多事情。有单元测试、集成测试和端到端测试。在本指南中，您将了解在开发和构建时使用 Docker 运行单元测试。

## 本地开发时运行测试

示例应用程序在 `tests` 目录中已经包含一个 xUnit 测试。在本地开发时，您可以使用 Compose 来运行测试。

在 `docker-dotnet-sample` 目录中运行以下命令，以在容器内运行测试。

```console
$ docker compose run --build --rm server dotnet test /source/tests
```

您应该看到包含以下内容的输出。

```console
Starting test execution, please wait...
A total of 1 test files matched the specified pattern.

Passed!  - Failed:     0, Passed:     1, Skipped:     0, Total:     1, Duration: < 1 ms - /source/tests/bin/Debug/net8.0/tests.dll (net8.0)
```

要了解有关该命令的更多信息，请参阅 [docker compose run](/reference/cli/docker/compose/run/)。

## 构建时运行测试

要在构建时运行测试，您需要更新 Dockerfile。您可以创建一个运行测试的新测试阶段，或在现有构建阶段中运行测试。对于本指南，请更新 Dockerfile 以在构建阶段中运行测试。

以下是更新后的 Dockerfile。

```dockerfile {hl_lines="9"}
# syntax=docker/dockerfile:1

FROM --platform=$BUILDPLATFORM mcr.microsoft.com/dotnet/sdk:8.0-alpine AS build
ARG TARGETARCH
COPY . /source
WORKDIR /source/src
RUN --mount=type=cache,id=nuget,target=/root/.nuget/packages \
    dotnet publish -a ${TARGETARCH/amd64/x64} --use-current-runtime --self-contained false -o /app
RUN dotnet test /source/tests

FROM mcr.microsoft.com/dotnet/sdk:8.0-alpine AS development
COPY . /source
WORKDIR /source/src
CMD dotnet run --no-launch-profile

FROM mcr.microsoft.com/dotnet/aspnet:8.0-alpine AS final
WORKDIR /app
COPY --from=build /app .
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser
USER appuser
ENTRYPOINT ["dotnet", "myWebApp.dll"]
```

运行以下命令，使用构建阶段作为目标构建镜像并查看测试结果。包含 `--progress=plain` 以查看构建输出，`--no-cache` 以确保测试始终运行，以及 `--target build` 以定位构建阶段。

```console
$ docker build -t dotnet-docker-image-test --progress=plain --no-cache --target build .
```

您应该看到包含以下内容的输出。

```console
#11 [build 5/5] RUN dotnet test /source/tests
#11 1.564   Determining projects to restore...
#11 3.421   Restored /source/src/myWebApp.csproj (in 1.02 sec).
#11 19.42   Restored /source/tests/tests.csproj (in 17.05 sec).
#11 27.91   myWebApp -> /source/src/bin/Debug/net8.0/myWebApp.dll
#11 28.47   tests -> /source/tests/bin/Debug/net8.0/tests.dll
#11 28.49 Test run for /source/tests/bin/Debug/net8.0/tests.dll (.NETCoreApp,Version=v8.0)
#11 28.67 Microsoft (R) Test Execution Command Line Tool Version 17.3.3 (x64)
#11 28.67 Copyright (c) Microsoft Corporation.  All rights reserved.
#11 28.68
#11 28.97 Starting test execution, please wait...
#11 29.03 A total of 1 test files matched the specified pattern.
#11 32.07
#11 32.08 Passed!  - Failed:     0, Passed:     1, Skipped:     0, Total:     1, Duration: < 1 ms - /source/tests/bin/Debug/net8.0/tests.dll (net8.0)
#11 DONE 32.2s
```

## 总结

在本节中，您学习了如何使用 Compose 在本地开发时运行测试，以及如何在构建镜像时运行测试。

相关信息：

- [docker compose run](/reference/cli/docker/compose/run/)

## 下一步

接下来，您将学习如何使用 GitHub Actions 设置 CI/CD 流水线。