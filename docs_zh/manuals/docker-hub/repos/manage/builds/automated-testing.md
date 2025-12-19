---
description: 自动化测试
keywords: Automated, testing, repository
title: 自动化仓库测试
weight: 30
aliases:
- /docker-hub/builds/automated-testing/
---

> [!NOTE]
>
> 自动化构建需要 Docker Pro、Team 或 Business 订阅。

Docker Hub 可以使用容器自动测试源代码仓库的更改。您可以在任何 Docker Hub 仓库上启用 `Autotest`，以便在对源代码仓库的每个拉取请求上运行测试，从而创建持续集成测试服务。

启用 `Autotest` 会构建一个用于测试的镜像，但不会自动将构建的镜像推送到 Docker 仓库。如果您想将构建的镜像推送到您的 Docker Hub 仓库，请启用 [自动化构建](index.md)。

## 设置自动化测试文件

要设置自动化测试，请创建一个 `docker-compose.test.yml` 文件，该文件定义一个 `sut` 服务，用于列出要运行的测试。
`docker-compose.test.yml` 文件应位于包含用于构建镜像的 Dockerfile 的同一目录中。

例如：

```yaml
services:
  sut:
    build: .
    command: run_tests.sh
```

前面的示例构建仓库，并使用构建的镜像在容器内运行 `run_tests.sh` 文件。

您可以在此文件中定义任意数量的链接服务。唯一的要求是定义 `sut`。其返回代码决定测试是否通过。如果 `sut` 服务返回 `0`，则测试通过，否则失败。

> [!NOTE]
> 
> 只有 `sut` 服务和 [`depends_on`](/reference/compose-file/services.md#depends_on) 中列出的所有其他服务才会启动。如果您有轮询其他服务更改的服务，请确保将轮询服务包含在 [`depends_on`](/reference/compose-file/services.md#depends_on) 列表中，以确保所有服务都能启动。

如果需要，您可以定义多个 `docker-compose.test.yml` 文件。任何以 `.test.yml` 结尾的文件都将用于测试，并且测试会按顺序运行。您还可以使用 [自定义构建钩子](advanced.md#override-build-test-or-push-commands) 来进一步自定义测试行为。

> [!NOTE]
>
> 如果您启用了自动化构建，它们也会运行在 `test.yml` 文件中定义的任何测试。

## 在仓库上启用自动化测试

要在源代码仓库上启用测试，您必须首先在 Docker Hub 中创建一个关联的构建仓库。您的 `Autotest` 设置与 [自动化构建](index.md) 在同一页面上配置，但是您不需要启用自动构建即可使用自动测试。自动构建是按分支或标签启用的，您完全不需要启用它。

只有配置为使用自动构建的分支才会将镜像推送到 Docker 仓库，无论自动测试设置如何。

1. 登录 Docker Hub 并选择 **My Hub** > **Repositories**。

2. 选择您要启用 `Autotest` 的仓库。

3. 从仓库视图中，选择 **Builds** 选项卡。

4. 选择 **Configure automated builds**。

5. 按照 [自动化构建](index.md) 中的说明配置自动化构建设置。

    您至少必须配置：

    * 源代码仓库
    * 构建位置
    * 至少一条构建规则

6. 选择您的 **Autotest** 选项。

    以下选项可用：

    * `Off`：无额外的测试构建。仅当测试配置为自动化构建的一部分时才会运行。

    * `Internal pull requests`：为任何对匹配构建规则的分支的拉取请求运行测试构建，但仅当拉取请求来自同一源代码仓库时。

    * `Internal and external pull requests`：为任何对匹配构建规则的分支的拉取请求运行测试构建，包括当拉取请求源自外部源代码仓库时。

    > [!IMPORTANT]
    >
    >出于安全原因，公共仓库上的外部拉取请求的自动测试是有限的。不会拉取私有镜像，并且 Docker Hub 中定义的环境变量不可用。自动化构建继续按常规工作。

7. 选择 **Save** 以保存设置，或选择 **Save and build** 以保存并运行初始测试。

## 检查测试结果

从仓库的详细信息页面，选择 **Timeline**。

从此选项卡中，您可以查看仓库的任何待处理、进行中、成功和失败的构建及测试运行。

您可以选择任何时间线条目以查看每次测试运行的日志。