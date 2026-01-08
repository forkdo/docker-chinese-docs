# Compose 中的网络

默认情况下，Compose 会为你的应用设置一个单独的
[network](/reference/cli/docker/network/create.md)。该服务的每个容器都会加入这个默认网络，既可以被该网络上的其他容器访问，也可以通过服务名称被其他容器发现。

> [!NOTE]
>
> 应用的网络名称是基于“项目名称”生成的，而项目名称又是基于该应用所在目录的名称。你可以通过 [`--project-name` 标志](/reference/cli/docker/compose.md)
> 或 [`COMPOSE_PROJECT_NAME` 环境变量](environment-variables/envvars.md#compose_project_name) 覆盖项目名称。

例如，假设你的应用位于一个名为 `myapp` 的目录中，你的 `compose.yaml` 文件如下所示：

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

当你运行 `docker compose up` 时，会发生以下情况：

1.  一个名为 `myapp_default` 的网络被创建。
2.  使用 `web` 的配置创建一个容器。它以 `web` 的名字加入网络
    `myapp_default`。
3.  使用 `db` 的配置创建一个容器。它以 `db` 的名字加入网络
    `myapp_default`。

现在，每个容器都可以查找服务名称 `web` 或 `db` 并
获得相应容器的 IP 地址。例如，`web` 的应用代码可以连接到 URL `postgres://db:5432` 并开始使用 Postgres 数据库。

重要的是要注意 `HOST_PORT` 和 `CONTAINER_PORT` 之间的区别。
在上面的例子中，对于 `db`，`HOST_PORT` 是 `8001`，而容器端口是
`5432`（postgres 默认端口）。网络化的服务到服务
通信使用 `CONTAINER_PORT`。当定义了 `HOST_PORT` 时，
该服务也可以在 swarm 外部被访问。

在 `web` 容器内，你连接到 `db` 的连接字符串看起来像
`postgres://db:5432`，而从主机机器来看，连接字符串看起来像
`postgres://{DOCKER_IP}:8001`，例如如果你的容器在本地运行，则是 `postgres://localhost:8001`。

## 更新网络上的容器

如果你更改了服务的配置并运行 `docker compose up` 来更新它，旧容器将被移除，新容器将以不同的 IP 地址但相同的名称加入网络。正在运行的容器可以查找该名称并连接到新地址，但旧地址将停止工作。

如果有任何容器与旧容器有打开的连接，这些连接将被关闭。检测这种情况、再次查找名称并重新连接是容器的责任。

> [!TIP]
>
> 尽可能通过名称而不是 IP 来引用容器。否则，你需要不断更新你使用的 IP 地址。

## 链接容器

Links 允许你定义额外的别名，通过这些别名，一个服务可以从另一个服务访问。它们不是启用服务通信所必需的。默认情况下，任何服务都可以通过该服务的名称访问任何其他服务。在下面的示例中，`db` 可以从 `web` 通过主机名 `db` 和 `database` 访问：

```yaml
services:
  web:
    build: .
    links:
      - "db:database"
  db:
    image: postgres:18
```

有关更多信息，请参阅 [links 参考](/reference/compose-file/services.md#links)。

## 多主机网络

当在启用了 [Swarm 模式](/manuals/engine/swarm/_index.md) 的 Docker Engine 上部署 Compose 应用时，
你可以利用内置的 `overlay` 驱动程序来启用多主机通信。

Overlay 网络始终创建为 `attachable`（可连接）。你可以选择将 [`attachable`](/reference/compose-file/networks.md#attachable) 属性设置为 `false`。

请参阅 [Swarm 模式部分](/manuals/engine/swarm/_index.md) 以了解如何设置
Swarm 集群，并参阅 [overlay 网络驱动程序文档](/manuals/engine/network/drivers/overlay.md)
以了解多主机 overlay 网络。

## 指定自定义网络

除了使用默认的应用网络外，你还可以使用顶级 `networks` 键指定你自己的网络。这允许你创建更复杂的拓扑结构并指定 [自定义网络驱动程序](/engine/extend/plugins_network/) 和选项。你也可以使用它将服务连接到不由 Compose 管理的外部创建的网络。

每个服务都可以使用服务级别的 `networks` 键指定要连接的网络，这是一个名称列表，引用顶级 `networks` 键下的条目。

以下示例显示了一个定义了两个自定义网络的 Compose 文件。`proxy` 服务与 `db` 服务是隔离的，因为它们没有共享网络。只有 `app` 可以与两者通信。

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
    # Specify driver options
    driver: bridge
    driver_opts:
      com.docker.network.bridge.host_binding_ipv4: "127.0.0.1"
  backend:
    # Use a custom driver
    driver: custom-driver
```

可以通过为每个连接的网络设置 [ipv4_address 和/或 ipv6_address](/reference/compose-file/services.md#ipv4_address-ipv6_address) 来为网络配置静态 IP 地址。

还可以为网络指定 [自定义名称](/reference/compose-file/networks.md#name)：

```yaml
services:
  # ...
networks:
  frontend:
    name: custom_frontend
    driver: custom-driver-1
```

## 配置默认网络

除了指定你自己的网络之外（或者作为替代），你还可以通过在 `networks` 下定义一个名为 `default` 的条目来更改应用范围默认网络的设置：

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
    # Use a custom driver
    driver: custom-driver-1
```

## 使用现有网络

如果你使用 `docker network create` 命令在 Compose 之外手动创建了一个桥接网络，你可以通过将该网络标记为 `external` 来将你的 Compose 服务连接到它。

如果你希望你的容器加入一个预先存在的网络，请使用 [`external` 选项](/reference/compose-file/networks.md#external)

```yaml
services:
  # ...
networks:
  network1:
    name: my-pre-existing-network
    external: true
```

Compose 不会尝试创建名为 `[projectname]_default` 的网络，而是查找名为 `my-pre-existing-network` 的网络并将你的应用容器连接到它。

## 更多参考信息

有关可用网络配置选项的完整详细信息，请参阅以下参考：

- [顶级 `networks` 元素](/reference/compose-file/networks.md)
- [服务级别 `networks` 属性](/reference/compose-file/services.md#networks)
