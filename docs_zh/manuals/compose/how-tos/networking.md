---
description: Docker Compose 如何在容器之间设置网络连接
keywords: 文档, 文档, docker, compose, 编排, 容器, 网络
title: Compose 中的网络
linkTitle: 网络
weight: 70
aliases:
  - /compose/networking/
---

{{% include "compose-eol.md" %}}

默认情况下，Compose 为您的应用设置一个 [网络](/reference/cli/docker/network/create.md)。每个服务的容器都会加入该默认网络，并且可以被该网络上的其他容器访问，同时也可以通过服务名称被发现。

> [!NOTE]
>
> 您应用的网络会基于“项目名称”被赋予一个名称，项目名称又基于它所在目录的名称。您可以通过 [`--project-name` 标志](/reference/cli/docker/compose.md) 或 [`COMPOSE_PROJECT_NAME` 环境变量](environment-variables/envvars.md#compose_project_name) 来覆盖项目名称。

例如，假设您的应用位于名为 `myapp` 的目录中，您的 `compose.yaml` 看起来像这样：

```yaml
services:
  web:
    build: .
    ports:
      - "8000:8000"
  db:
    image: postgres:18
    ports:
      - "8001:5432"
```

当您运行 `docker compose up` 时，会发生以下情况：

1.  创建一个名为 `myapp_default` 的网络。
2.  使用 `web` 的配置创建一个容器。它以名称 `web` 加入网络 `myapp_default`。
3.  使用 `db` 的配置创建一个容器。它以名称 `db` 加入网络 `myapp_default`。

现在，每个容器都可以查找服务名称 `web` 或 `db`，并获取相应容器的 IP 地址。例如，`web` 的应用代码可以连接到 URL `postgres://db:5432` 并开始使用 Postgres 数据库。

重要的是要注意 `HOST_PORT` 和 `CONTAINER_PORT` 之间的区别。在上面的例子中，对于 `db`，`HOST_PORT` 是 `8001`，容器端口是 `5432`（postgres 默认端口）。网络化的服务到服务通信使用 `CONTAINER_PORT`。当定义了 `HOST_PORT` 时，该服务在集群外部也是可访问的。

在 `web` 容器内，您到 `db` 的连接字符串看起来像 `postgres://db:5432`，而在主机机器上，连接字符串看起来像 `postgres://{DOCKER_IP}:8001`，例如，如果您的容器在本地运行，则为 `postgres://localhost:8001`。

## 更新网络上的容器

如果您对服务进行了配置更改并运行 `docker compose up` 来更新它，旧容器将被移除，新容器以不同的 IP 地址但相同的名称加入网络。正在运行的容器可以查找该名称并连接到新地址，但旧地址将停止工作。

如果有任何容器与旧容器保持连接，这些连接将被关闭。容器有责任检测这种情况，再次查找名称并重新连接。

> [!TIP]
>
> 只要可能，就通过名称而不是 IP 引用容器。否则您需要不断更新您使用的 IP 地址。

## 链接容器

链接允许您定义额外的别名，使一个服务可以从另一个服务访问。它们不是启用服务通信所必需的。默认情况下，任何服务都可以通过该服务的名称访问任何其他服务。在以下示例中，`db` 可以从 `web` 通过主机名 `db` 和 `database` 访问：

```yaml
services:
  web:
    build: .
    links:
      - "db:database"
  db:
    image: postgres:18
```

请参阅 [links 引用](/reference/compose-file/services.md#links) 了解更多信息。

## 多主机网络

当在启用了 [Swarm 模式](/manuals/engine/swarm/_index.md) 的 Docker Engine 上部署 Compose 应用时，您可以使用内置的 `overlay` 驱动程序来启用多主机通信。

覆盖网络总是作为 `attachable` 创建。您也可以选择将 [`attachable`](/reference/compose-file/networks.md#attachable) 属性设置为 `false`。

请查阅 [Swarm 模式部分](/manuals/engine/swarm/_index.md) 了解如何设置 Swarm 集群，以及 [覆盖网络驱动程序文档](/manuals/engine/network/drivers/overlay.md) 了解多主机覆盖网络。

## 指定自定义网络

除了仅使用默认应用网络外，您还可以使用顶级 `networks` 键指定自己的网络。这使您可以创建更复杂的拓扑结构，指定 [自定义网络驱动程序](/engine/extend/plugins_network/) 和选项。您也可以使用它将服务连接到外部创建的、不由 Compose 管理的网络。

每个服务都可以通过服务级 `networks` 键指定要连接到哪些网络，该键是一个列表，引用顶级 `networks` 键下的条目。

以下示例显示了一个定义两个自定义网络的 Compose 文件。`proxy` 服务与 `db` 服务隔离，因为它们没有共享共同的网络。只有 `app` 可以同时与两者通信。

```yaml
services:
  proxy:
    build: ./proxy
    networks:
      - frontend
  app:
    build: ./app
    networks:
      - frontend
      - backend
  db:
    image: postgres:18
    networks:
      - backend

networks:
  frontend:
    # 指定驱动程序选项
    driver: bridge
    driver_opts:
      com.docker.network.bridge.host_binding_ipv4: "127.0.0.1"
  backend:
    # 使用自定义驱动程序
    driver: custom-driver
```

网络可以通过为每个连接的网络设置 [ipv4_address 和/或 ipv6_address](/reference/compose-file/services.md#ipv4_address-ipv6_address) 来配置静态 IP 地址。

网络也可以被赋予 [自定义名称](/reference/compose-file/networks.md#name)：

```yaml
services:
  # ...
networks:
  frontend:
    name: custom_frontend
    driver: custom-driver-1
```

## 配置默认网络

除了指定您自己的网络外，您还可以通过定义一个名为 `default` 的顶级 `networks` 条目来更改应用范围默认网络的设置：

```yaml
services:
  web:
    build: .
    ports:
      - "8000:8000"
  db:
    image: postgres:18

networks:
  default:
    # 使用自定义驱动程序
    driver: custom-driver-1
```

## 使用现有网络

如果您在 Compose 外部使用 `docker network create` 命令手动创建了一个桥接网络，您可以通过将网络标记为 `external` 来让您的 Compose 服务连接到它。

如果您希望您的容器加入一个预先存在的网络，请使用 [`external` 选项](/reference/compose-file/networks.md#external)

```yaml
services:
  # ...
networks:
  network1:
    name: my-pre-existing-network
    external: true
```

Compose 不会尝试创建一个名为 `[projectname]_default` 的网络，而是查找名为 `my-pre-existing-network` 的网络，并将您应用的容器连接到它。