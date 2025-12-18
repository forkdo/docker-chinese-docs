---
title: 覆盖容器默认配置
weight: 2
keywords: 概念, 构建, 镜像, 容器, docker desktop
description: 本概念页面将教您如何使用 `docker run` 命令覆盖容器默认配置。
aliases: 
 - /guides/docker-concepts/running-containers/overriding-container-defaults/
---

{{< youtube-embed PFszWK3BB8I >}}

## 说明

当 Docker 容器启动时，它会执行一个应用程序或命令。容器从其镜像的配置中获取此可执行文件（脚本或文件）。容器带有默认设置，通常这些设置运行良好，但您可以在需要时更改它们。这些调整有助于容器程序按照您的要求精确运行。

例如，如果您有一个在标准端口上监听的现有数据库容器，并且想要运行同一数据库容器的新实例，那么您可能希望更改新容器监听的端口设置，以避免与现有容器冲突。有时，如果程序需要更多资源来处理繁重的工作负载，您可能希望增加容器可用的内存，或者设置环境变量以提供程序正常运行所需的特定配置信息。

`docker run` 命令提供了一种强大的方式来覆盖这些默认值并定制容器的行为。该命令提供了几个标志，允许您动态自定义容器行为。

以下是几种实现方法：

### 覆盖网络端口

有时您可能希望为开发和测试目的使用单独的数据库实例。在相同端口上运行这些数据库实例可能会产生冲突。您可以使用 `docker run` 中的 `-p` 选项将容器端口映射到主机端口，从而在不冲突的情况下运行多个容器实例。

```console
$ docker run -d -p HOST_PORT:CONTAINER_PORT postgres
```

### 设置环境变量

此选项在容器内设置一个名为 `foo` 的环境变量，值为 `bar`。

```console
$ docker run -e foo=bar postgres env
```

您将看到如下输出：

```console
HOSTNAME=2042f2e6ebe4
foo=bar
```

> [!TIP]
>
> `.env` 文件是一种方便的方式，可以为 Docker 容器设置环境变量，而无需在命令行中使用大量 `-e` 标志。要使用 `.env` 文件，您可以在 `docker run` 命令中传递 `--env-file` 选项。
> ```console
> $ docker run --env-file .env postgres env
> ```

### 限制容器资源消耗

您可以将 `--memory` 和 `--cpus` 标志与 `docker run` 命令一起使用，以限制容器可以使用的 CPU 和内存。例如，您可以为 Python API 容器设置内存限制，防止它消耗主机上的过多资源。以下是命令：

```console
$ docker run -e POSTGRES_PASSWORD=secret --memory="512m" --cpus="0.5" postgres
 ```

此命令将容器内存使用限制为 512 MB，并将 CPU 配额定义为 0.5（半核）。

> **监控实时资源使用情况**
>
> 您可以使用 `docker stats` 命令监控正在运行的容器的实时资源使用情况。这有助于您了解分配的资源是否充足，或者是否需要调整。

通过有效使用这些 `docker run` 标志，您可以定制容器化应用程序的行为，使其符合您的特定需求。

## 动手尝试

在本实践指南中，您将了解如何使用 `docker run` 命令覆盖容器默认配置。

1. [下载并安装](/get-started/get-docker/) Docker Desktop。

### 运行多个 Postgres 数据库实例

1.  使用 [Postgres 镜像](https://hub.docker.com/_/postgres) 启动一个容器，命令如下：
    
    ```console
    $ docker run -d -e POSTGRES_PASSWORD=secret -p 5432:5432 postgres
    ```

    这将在后台启动 Postgres 数据库，监听标准容器端口 `5432`，并映射到主机的端口 `5432`。

2. 启动第二个映射到不同端口的 Postgres 容器。

    ```console
    $ docker run -d -e POSTGRES_PASSWORD=secret -p 5433:5432 postgres
    ```

    这将在后台启动另一个 Postgres 容器，监听容器内的标准 postgres 端口 `5432`，但映射到主机的端口 `5433`。您仅覆盖主机端口，以确保此新容器不会与现有运行的容器冲突。

3. 通过 Docker Desktop 仪表板的 **Containers** 视图验证两个容器是否都在运行。

    ![Docker Desktop 仪表板显示正在运行的 Postgres 容器实例的截图](images/running-postgres-containers.webp?border=true)

### 在受控网络中运行 Postgres 容器

默认情况下，当您运行容器时，它们会自动连接到一个特殊的网络，称为桥接网络。此桥接网络就像一个虚拟桥，允许同一主机上的容器相互通信，同时将它们与外部世界和其他主机隔离。这对于大多数容器交互来说是一个方便的起点。但是，对于特定场景，您可能希望对网络配置有更多控制。

这就是自定义网络的用武之地。您可以通过在 `docker run` 命令中传递 `--network` 标志来创建自定义网络。所有未指定 `--network` 的容器都会附加到默认桥接网络。

请按照以下步骤了解如何将 Postgres 容器连接到自定义网络。

1. 使用以下命令创建一个新的自定义网络：

    ```console
    $ docker network create mynetwork
    ```

2. 运行以下命令验证网络：

    ```console
    $ docker network ls
    ```

    此命令列出所有网络，包括新创建的 "mynetwork"。

3. 使用以下命令将 Postgres 连接到自定义网络：

    ```console
    $ docker run -d -e POSTGRES_PASSWORD=secret -p 5434:5432 --network mynetwork postgres
    ```

    这将在后台启动 Postgres 容器，映射到主机端口 5434，并附加到 `mynetwork` 网络。您传递了 `--network` 参数以覆盖容器默认配置，将容器连接到自定义 Docker 网络，以实现更好的隔离和与其他容器的通信。您可以使用 `docker network inspect` 命令检查容器是否已连接到此新桥接网络。

    > **默认桥接网络与自定义网络的关键区别**
    >
    > 1. DNS 解析：默认情况下，连接到默认桥接网络的容器可以通过 IP 地址相互通信，但无法通过名称解析（除非使用 `--link` 选项，这被认为是过时的）。由于各种[技术缺陷](/engine/network/drivers/bridge/#differences-between-user-defined-bridges-and-the-default-bridge)，不建议在生产环境中使用。在自定义网络上，容器可以通过名称或别名相互解析。
    > 2. 隔离：所有未指定 `--network` 的容器都会附加到默认桥接网络，因此可能存在风险，因为不相关的容器可以相互通信。使用自定义网络提供了一个作用域网络，只有附加到该网络的容器才能通信，从而提供更好的隔离。

### 管理资源

默认情况下，容器在资源使用方面不受限制。但是，在共享系统上，有效管理资源至关重要。重要的是不要让运行的容器消耗主机内存过多。

这就是 `docker run` 命令再次发挥作用的地方。它提供了 `--memory` 和 `--cpus` 标志来限制容器可以使用的 CPU 和内存。

```console
$ docker run -d -e POSTGRES_PASSWORD=secret --memory="512m" --cpus=".5" postgres
```

`--cpus` 标志指定容器的 CPU 配额。这里设置为半核 CPU（0.5），而 `--memory` 标志指定容器的内存限制。在这种情况下，设置为 512 MB。

### 在 Docker Compose 中覆盖默认 CMD 和 ENTRYPOINT

有时，您可能需要覆盖 Docker 镜像中定义的默认命令（`CMD`）或入口点（`ENTRYPOINT`），尤其是在使用 Docker Compose 时。

1. 创建一个 `compose.yml` 文件，内容如下：

    ```yaml
    services:
      postgres:
        image: postgres:18
        entrypoint: ["docker-entrypoint.sh", "postgres"]
        command: ["-h", "localhost", "-p", "5432"]
        environment:
          POSTGRES_PASSWORD: secret 
    ```

    该 Compose 文件定义了一个名为 `postgres` 的服务，使用官方 Postgres 镜像，设置入口点脚本，并使用密码身份验证启动容器。

2. 运行以下命令启动服务：

    ```console
    $ docker compose up -d
    ```

    此命令启动 Docker Compose 文件中定义的 Postgres 服务。

3. 使用 Docker Desktop 仪表板验证身份验证。

    打开 Docker Desktop 仪表板，选择 **Postgres** 容器，然后选择 **Exec** 进入容器 shell。您可以键入以下命令连接到 Postgres 数据库：

    ```console
    # psql -U postgres
    ```

    ![Docker Desktop 仪表板选择 Postgres 容器并使用 EXEC 按钮进入其 shell 的截图](images/exec-into-postgres-container.webp?border=true)

    > [!NOTE]
    > 
    > PostgreSQL 镜像在本地设置信任身份验证，因此您可能会注意到从 localhost（同一容器内）连接时不需要密码。但是，如果从不同主机/容器连接，则需要密码。

### 使用 `docker run` 覆盖默认 CMD 和 ENTRYPOINT

您也可以直接使用 `docker run` 命令覆盖默认值，命令如下：

```console 
$ docker run -e POSTGRES_PASSWORD=secret postgres docker-entrypoint.sh -h localhost -p 5432
```

此命令运行一个 Postgres 容器，设置环境变量进行密码身份验证，覆盖默认启动命令，并配置主机名和端口映射。

## 额外资源

* [使用 Compose 设置环境变量的方法](/compose/how-tos/environment-variables/set-environment-variables/)
* [什么是容器](/get-started/docker-concepts/the-basics/what-is-a-container/)

## 下一步

现在您已经了解了覆盖容器默认配置，接下来学习如何持久化容器数据。

{{< button text="持久化容器数据" url="persisting-container-data" >}}

