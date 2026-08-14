# Compose 中的网络


Compose 默认会为你处理网络，但当你需要时也能提供精细的控制。本页讲解默认网络的工作原理以及容器如何通过名称相互发现，还涵盖了何时以及如何定义自定义网络、跨独立的 Compose 项目连接服务、映射自定义主机名，以及排查连接问题。

## 默认网络与服务发现

默认情况下，Compose 会为你的应用设置一个单独的 [network](/reference/cli/docker/network/create/)。该服务的每个容器都会加入这个默认网络，既可以被该网络上的其他容器访问，也可以通过其服务名称被发现。该网络使用 `bridge` 驱动。要了解何时需要使用不同的驱动，请参阅 [网络驱动：bridge 与 host](#change-the-network-mode)。

对于大多数开发场景，默认网络已经足够。当你运行 `docker compose up` 时，Compose 会创建一个名为 `<project-name>_default` 的网络，并将所有服务连接到它。每个服务都会向内部 DNS 服务器注册自己的名称，因此容器可以直接使用服务名称相互访问，无需 IP 地址或手动配置。

例如，假设你的应用位于一个名为 `myapp` 的目录中，你的 `compose.yaml` 文件如下所示：

```yaml
services:
  web:
    build: .
    ports:
      - "8000:8000"
  db:
    image: postgres:latest
    ports:
      - "8001:5432"
```

Compose 会自动将所有服务连接到默认网络，因此你无需在 Compose 文件中显式定义 `networks`。

当你运行 `docker compose up` 时，会发生以下情况：

1. 创建一个名为 `myapp_default` 的网络。
2. 使用 `web` 的配置创建一个容器。它以 `web` 的名称加入 `myapp_default`。
3. 使用 `db` 的配置创建一个容器。它以 `db` 的名称加入 `myapp_default`。

现在，每个容器都可以查找服务名称 `web` 或 `db` 并获取对应容器的 IP 地址。`web` 服务可以连接到 `postgres://db:5432` 处的数据库。如果你的容器在本地运行，从主机来看，同一个数据库可以通过 `postgres://localhost:8001` 访问。

> [!TIP]
>
> Docker 每次容器启动时都会从网络的子网中动态分配容器 IP 地址，因此它们在重启或重建后不会持久化。这意味着你应该始终通过名称而非 IP 地址来引用服务。当容器被重建时（例如配置变更后），它们会获得新的 IP 地址，而服务名称保持不变。

你的应用的网络名称是基于“项目名称”生成的，而项目名称取自该应用所在目录的名称。你可以通过 [`--project-name` 标志](/reference/cli/docker/compose/) 或 [`COMPOSE_PROJECT_NAME` 环境变量](environment-variables/envvars.md#compose_project_name) 覆盖项目名称。

`HOST_PORT` 和 `CONTAINER_PORT` 用途不同。在上面的例子中，对于 `db`，`HOST_PORT` 是 `8001`，容器端口是 `5432`（Postgres 默认值）。网络化的服务到服务通信使用 `CONTAINER_PORT`。主机端口仅用于在从网络外部访问服务时使用。

### 更新网络上的容器

如果你更改了服务的配置并运行 `docker compose up` 来更新它，旧容器将被移除，新容器将以不同的 IP 地址但相同的名称加入网络。正在运行的容器可以查找该名称并连接到新地址，但旧地址将停止工作。

如果有任何容器与旧容器有打开的连接，这些连接将被关闭。检测这种情况、再次查找名称并重新连接是每个容器的责任。

## 更改网络模式

默认情况下，每个服务都会加入项目的 bridge 网络。这是最安全的网络模式。如果你没有指定 [`network_mode`](/reference/compose-file/services.md#network_mode)，你创建的就是这种类型的网络。

你可以在每个服务的基础上覆盖网络模式。`network_mode` 选项接受以下值：

- `host`：容器共享主机的网络栈。不需要也不支持端口映射，且服务名称的 DNS 解析不起作用。适用于需要直接访问主机接口的系统级工具（如网络监视器）。使用 `network_mode: host` 的容器可以访问主机的所有端口，并能观察到主机上的所有网络流量。仅在确实必要时使用。
- `none`：关闭所有容器网络。
- `service:{name}`：通过引用其服务名称，让容器能够访问指定的容器。
- `container:{name}`：通过引用其容器 ID，让容器能够访问指定的容器。

你可以在单个项目中混合使用不同的模式：

```yaml
services:
  app:
    image: myapp
    networks:
      - isolated
    ports:
      - "3000:3000"

  monitoring:
    image: netdata/netdata
    network_mode: host   # 可以监视主机系统和所有主机端口

networks:
  isolated:
    driver: bridge
```

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
    image: postgres:latest
    networks:
      - backend

networks:
  frontend:
    driver: bridge   # Specify driver options
    driver_opts:
      com.docker.network.bridge.host_binding_ipv4: "127.0.0.1"
  backend:
    driver: custom-driver  # Use a custom driver
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

### 内部网络

在网络上设置 `internal: true` 会创建一个没有连接到主机网络接口的网络。它没有用于外部连接的默认网关。这对于像数据库这样应该完全无法从容器网络外部访问的服务非常有用：

```yaml
services:
  cache:
    image: redis
    networks:
      - isolated

  worker:
    image: myworker
    networks:
      - isolated
      - public

networks:
  isolated:
    internal: true   # 无外部连接
  public:   # 标准 bridge 网络，在 docker compose up 时由 Compose 创建
```

注意，同时连接到内部网络和非内部网络（如上例中的 `worker`）的服务，仍然可以通过非内部网络 `public` 访问互联网。

### 配置默认网络

除了指定你自己的网络之外（或者作为替代），你还可以通过在 `networks` 下定义一个名为 `default` 的条目来更改应用范围默认网络的设置：

```yaml
services:
  web:
    build: .
    ports:
      - "8000:8000"
  db:
    image: postgres:latest

networks:
  default:
    driver: custom-driver-1   # Use a custom driver
```

## 使用已有的外部网络

如果你使用 `docker network create` 手动创建了一个桥接网络，你可以通过将其标记为 [`external`](/reference/compose-file/networks.md#external) 来将你的 Compose 服务连接到它：

```yaml
services:
  # ...
networks:
  network1:
    name: my-pre-existing-network
    external: true
```

Compose 不会尝试创建 `<project-name>_default`，而是查找名为 `my-pre-existing-network` 的网络并将你的容器连接到它。

### 连接多个 Compose 项目

当独立的 Compose 项目中的服务需要通信时，外部网络特别有用。先创建一个共享网络，然后在每个项目中将其作为外部网络引用：

```bash
docker network create inter-project
```

backend-compose.yaml：

```yaml
services:
  api:
    image: myapi:latest
    networks:
      - shared
      - default   # 同时保留项目内部网络

networks:
  shared:
    external: true
    name: inter-project
```

frontend-compose.yaml：

```yaml
services:
  web:
    image: myfrontend:latest
    environment:
      API_URL: http://api:8080   # 通过服务名称引用
    networks:
      - shared

networks:
  shared:
    external: true
    name: inter-project
```

同一外部网络上的服务可以通过服务名称相互访问，就像单个项目内的服务一样。

> [!IMPORTANT]
>
> 外部网络必须在你运行 `docker compose up` 之前已经存在。如果不存在，Compose 会失败并报 `Network not found` 错误。请始终先使用 `docker network create` 创建它。

## 混合网络（Hybrid networking）

一个服务可以同时属于一个外部共享网络和它自己的项目内部网络。这让你只暴露那些需要被其他项目访问的服务，同时将数据库等其他一切内容完全隔离：

```yaml
services:
  api:
    image: myapp-api
    networks:
      - shared     # 可被其他项目访问
      - internal   # 也可以访问数据库

  database:
    image: postgres:latest
    networks:
      - internal   # 不在共享网络上暴露

networks:
  shared:
    name: inter-project
    external: true
  internal: {}     # 项目专属，隔离
```

## 使用 `extra_hosts` 自定义 DNS

你可以使用 [`extra_hosts`](/reference/compose-file/services.md#extra_hosts) 向容器的 `/etc/hosts` 文件添加自定义的主机名到 IP 的映射。当一个服务需要解析一个未在 Docker 内部 DNS 中注册的主机名时（例如固定 IP 的依赖项或预发环境端点），这很有用：

```yaml
services:
  app:
    image: myapp
    extra_hosts:
      - "api.staging:192.168.1.100"
      - "cache.internal:192.168.1.101"
```

要将主机名动态映射到主机的 IP，请使用特殊的 `host-gateway` 值：

```yaml
services:
  app:
    image: myapp
    extra_hosts:
      - "host.docker.internal:host-gateway"
```

在 Linux 上，`host-gateway` 解析为默认 bridge 网络上主机的 IP。在 Mac 和 Windows 上，Docker 会自动提供此功能，`host-gateway` 解析为与 `host.docker.internal` 相同的内部 IP 地址。

你也可以通过环境变量来驱动 `extra_hosts`，这样便于在不同环境下将服务指向不同的目标：

```yaml
services:
  app:
    image: myapp
    extra_hosts:
      - "api.service:${API_HOST:-127.0.0.1}"
      - "auth.service:${AUTH_HOST:-127.0.0.1}"
```

其中 `.env.development` 可能设置 `API_HOST=localhost`，而生产环境文件可能设置 `API_HOST=10.0.1.50`。

要验证注入了什么内容，可以在容器内检查 hosts 文件：

```bash
$ docker compose exec app cat /etc/hosts
```

## 多主机网络

当在启用了 [Swarm 模式](/manuals/engine/swarm/_index.md) 的 Docker Engine 上部署 Compose 应用时，你可以使用内置的 `overlay` 驱动来启用多主机通信。Overlay 网络始终创建为 `attachable`。你可以选择将 [`attachable`](/reference/compose-file/networks.md#attachable) 属性设置为 `false`。

要了解更多信息，请参阅 [overlay 网络驱动程序文档](/manuals/engine/network/drivers/overlay.md)。

## 链接容器

Links 允许你定义额外的别名，通过这些别名，一个服务可以从另一个服务访问。它们不是基本的服务到服务通信所必需的。默认情况下，任何服务都可以通过该服务的名称访问任何其他服务。在下面的示例中，`db` 可以通过主机名 `db` 和 `database` 两个名称从 `web` 访问：

```yaml
services:
  web:
    build: .
    links:
      - "db:database"
  db:
    image: postgres:latest
```

有关更多信息，请参阅 [links 参考](/reference/compose-file/services.md#links)。

## 调试

当一个服务无法访问另一个服务时，请按以下顺序逐步排查：先确认网络配置看起来正确，再确认容器确实已连接，最后测试实际连通性。

### 检查端口映射

要查明哪个主机端口映射到容器端口，可以使用 `docker compose port`：

```bash
# db 上容器端口 5432 映射到哪个主机端口？
$ docker compose port db 5432
# 输出：0.0.0.0:8001
```

这在使用动态端口映射时尤其有用，因为每次 `docker compose up` 时主机端口都会变化：

```yaml
services:
  web:
    image: nginx
    ports:
      - "80"   # Docker 动态分配主机端口
```

```bash
$ docker compose port web 80
# 输出：0.0.0.0:55432
```

当你扩展服务时，每个副本都会获得自己的动态端口。使用 `--index` 查询特定的副本：

```bash
$ docker compose up -d --scale web=3

$ docker compose port --index=1 web 80   # 输出：0.0.0.0:55001
$ docker compose port --index=2 web 80   # 输出：0.0.0.0:55002
$ docker compose port --index=3 web 80   # 输出：0.0.0.0:55003
```

默认情况下，`docker compose port` 查找 TCP 映射。如果一个服务在同一端口上同时暴露 TCP 和 UDP，请使用 `--protocol`：

```bash
$ docker compose port --protocol=udp myservice 53
```

### 验证网络成员关系

要检查哪些容器连接到了某个网络（在排查跨外部或自定义网络的连通性问题时很有用）：

```bash
$ docker network inspect <network-name>
```

### 检查连通性

如果网络成员关系看起来正确，但服务之间仍然无法相互访问，可以使用 `docker compose exec` 从运行中的容器内部测试连通性。

## 更多参考信息

有关可用网络配置选项的完整详细信息，请参阅以下参考：

- [顶级 `networks` 元素](/reference/compose-file/networks.md)
- [服务级别 `networks` 属性](/reference/compose-file/services.md#networks)

