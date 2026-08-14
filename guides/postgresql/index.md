# PostgreSQL 专项指南



## 快速搭建与数据持久化

本指南让您在五分钟内从零开始运行一个 PostgreSQL 容器，然后解释如何在容器重启和移除时保护您的数据。

### 概述

在 Docker 中运行 PostgreSQL 需要理解一个关键概念：容器是临时的，但您的数据不应该是。本指南涵盖：

- 用一条命令启动 PostgreSQL
- 理解为什么容器默认会丢失数据
- 配置卷以实现持久化存储
- 将您的配置转换为 Docker Compose

### 快速开始（最小可用容器）

> [!NOTE]
>
> [Docker Hardened Images (DHIs)](https://docs.docker.com/dhi/) 是由 Docker 维护的最小、安全且生产就绪的容器基础镜像和应用镜像。只要条件允许，都推荐使用 DHI 以提升安全性。它们旨在减少漏洞并简化合规，对所有人免费提供，无需订阅、无使用限制、无供应商锁定。

用这一条命令立即运行 PostgreSQL：

**使用 DHIs**



在拉取 Docker Hardened Images 之前，您必须对 dhi.io 进行身份验证。运行 `docker login dhi.io` 进行身份验证。

```console
docker run --rm --name postgres-dev \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -p 5432:5432 \
  -d dhi.io/postgres:18
```

**使用 DOIs**



```console
$ docker run --rm --name postgres-dev \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -p 5432:5432 \
  -d postgres:18
```



#### 理解各选项

| 选项 | 用途 |
|------|---------|
| `--rm` | 容器停止时自动移除 |
| `--name postgres-dev` | 分配一个易记的名称，而非随机字符串 |
| `-e POSTGRES_PASSWORD=...` | 设置超级用户密码（必填） |
| `-p 5432:5432` | 将主机端口 5432 映射到容器端口 5432 |
| `-d` | 在后台运行容器（分离模式） |

验证容器正在运行：

```console
$ docker ps --filter name=postgres-dev
CONTAINER ID   IMAGE         COMMAND                  STATUS         PORTS                    NAMES
a1b2c3d4e5f6   postgres:18   "docker-entrypoint.s…"   Up 2 seconds   0.0.0.0:5432->5432/tcp   postgres-dev
```

使用容器内的 `psql` 进行连接：

```console
$ docker exec -it postgres-dev psql -U postgres
psql (18.0)
Type "help" for help.

postgres=#
```

现在您已经有了一个可用的 PostgreSQL 实例。但有个问题——停止这个容器，您的数据就会消失。

### 数据持久化问题

容器使用临时文件系统。当容器被移除时，其中的所有内容（包括您的数据库文件）都会被删除。

亲自验证一下：

**使用 DHIs**



```console
$ docker exec postgres-dev psql -U postgres -c "CREATE DATABASE testdb;"
CREATE DATABASE

$ docker exec postgres-dev psql -U postgres -c "\l" | grep testdb
 testdb    | postgres | UTF8     | libc            | en_US.utf8 | en_US.utf8 |            |           |

$ docker stop postgres-dev
postgres-dev

$ docker run --rm --name postgres-dev \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -p 5432:5432 \
  -d dhi.io/postgres:18

$ docker exec postgres-dev psql -U postgres -c "\l" | grep testdb
(no output - database is gone)
```

**使用 DOIs**



```console
$ docker exec postgres-dev psql -U postgres -c "CREATE DATABASE testdb;"
CREATE DATABASE

$ docker exec postgres-dev psql -U postgres -c "\l" | grep testdb
 testdb    | postgres | UTF8     | libc            | en_US.utf8 | en_US.utf8 |            |           |

$ docker stop postgres-dev
postgres-dev

$ docker run --rm --name postgres-dev \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -p 5432:5432 \
  -d postgres:18

$ docker exec postgres-dev psql -U postgres -c "\l" | grep testdb
(no output - database is gone)
```



您的 `testdb` 数据库消失了，因为新容器以全新的文件系统启动。这是预期行为——也正是卷存在的原因。

### 命名卷

命名卷是由 Docker 管理的存储位置，独立于容器而持久存在。Docker 负责处理文件系统位置、权限和生命周期。

创建一个带有命名卷的容器：

**使用 DHIs**



在拉取 Docker Hardened Images 之前，您必须对 dhi.io 进行身份验证。运行 `docker login dhi.io` 进行身份验证。

```console
$ docker run --rm --name postgres-dev \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -p 5432:5432 \
  -v postgres_data:/var/lib/postgresql \
  -d dhi.io/postgres:18
```

**使用 DOIs**



```console
$ docker run --rm --name postgres-dev \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -p 5432:5432 \
  -v postgres_data:/var/lib/postgresql \
  -d postgres:18
```




`-v postgres_data:/var/lib/postgresql` 选项将一个名为 `postgres_data` 的命名卷挂载到 PostgreSQL 的数据目录。如果该卷不存在，Docker 会自动创建它。

> [!NOTE]
>
> PostgreSQL 18+ 将数据存储在 `/var/lib/postgresql` 下特定于版本的子目录中。在此层级（而非 `/var/lib/postgresql/data`）挂载，便于使用 `pg_upgrade --link` 进行更轻松的升级。

#### 验证持久化是否生效

要验证数据持久化，请重复之前的测试，但这次挂载命名卷。

**使用 DHIs**



```console
$ docker exec postgres-dev psql -U postgres -c "CREATE DATABASE testdb;"
CREATE DATABASE

$ docker stop postgres-dev
postgres-dev

$ docker run --rm --name postgres-dev \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -p 5432:5432 \
  -v postgres_data:/var/lib/postgresql \
  -d dhi.io/postgres:18

$ docker exec postgres-dev psql -U postgres -c "\l" | grep testdb
 testdb    | postgres | UTF8     | libc            | en_US.utf8 | en_US.utf8 |            |           |
```

**使用 DOIs**



```console
$ docker exec postgres-dev psql -U postgres -c "CREATE DATABASE testdb;"
CREATE DATABASE

$ docker stop postgres-dev
postgres-dev

$ docker run --rm --name postgres-dev \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -p 5432:5432 \
  -v postgres_data:/var/lib/postgresql \
  -d postgres:18

$ docker exec postgres-dev psql -U postgres -c "\l" | grep testdb
 testdb    | postgres | UTF8     | libc            | en_US.utf8 | en_US.utf8 |            |           |
```



如果您在输出中看到 `testdb`，说明持久化生效了：数据库之所以能够存活，是因为卷保留了数据目录。

#### 管理卷

列出所有卷：

```console
$ docker volume ls --filter name=postgres_data
DRIVER    VOLUME NAME
local     postgres_data
```

检查某个卷以查看其详情：

```console
$ docker volume inspect postgres_data
[
    {
        "CreatedAt": "2025-01-05T10:30:00Z",
        "Driver": "local",
        "Labels": null,
        "Mountpoint": "/var/lib/docker/volumes/postgres_data/_data",
        "Name": "postgres_data",
        "Options": null,
        "Scope": "local"
    }
]
```

移除一个未使用的卷（警告：这会删除所有数据）：

```console
$ docker volume rm postgres_data
```

### 绑定挂载（替代方案）

绑定挂载将特定的主机目录映射到容器路径。与命名卷不同，您完全控制数据在主机文件系统中的确切位置。

在您的主机上创建一个目录来存储 Postgres 数据。

**使用 DHIs**



```console
mkdir -p ~/postgres-data && sudo chown -R 999:999 ~/postgres-data
```

使用绑定挂载运行 Postgres。

```console
docker run --rm --name postgres-dev \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -p 5432:5432 \
  -v ~/postgres-data:/var/lib/postgresql \
  -d dhi.io/postgres:18
```

**使用 DOIs**



```console
$ mkdir -p ~/postgres-data
```

使用绑定挂载运行 Postgres。

```console
$ docker run --rm --name postgres-dev \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -p 5432:5432 \
  -v ~/postgres-data:/var/lib/postgresql \
  -d postgres:18
```



#### 何时使用绑定挂载

当您需要直接通过文件系统访问数据目录（用于直接读取文件的备份脚本）、与主机级监控工具集成、或存在特定权限要求时，绑定挂载很有用。对于大多数开发和生产场景，命名卷更简单且更不容易出错。

#### 常见的绑定挂载问题

权限错误是绑定挂载最频繁的问题。PostgreSQL 在容器内以用户 `postgres`（UID 999）运行。如果您的主机目录权限受限，容器将无法启动。

如果容器立即退出，请检查日志：

```console
$ docker logs postgres-dev
```

### Docker Compose 配置

Docker Compose 将您的整个配置保存在文件中，使设置在复杂度增长时具有可复现性且更易于管理。

创建一个 `compose.yaml` 文件：

```yaml
services:
  db:
    image: postgres:18
    container_name: postgres-dev
    environment:
      POSTGRES_PASSWORD: mysecretpassword
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql

volumes:
  postgres_data:
```

启动数据库：

```console
$ docker compose up -d
```

停止并移除容器（卷持久存在）：

```console
$ docker compose down
```

或者，您可以停止、移除容器并删除卷：

```console
$ docker compose down -v
```

这个 compose 文件成为添加初始化脚本、性能调优以及后续指南中涉及的配套服务的基础。

#### 环境变量参考

官方 PostgreSQL 镜像支持以下环境变量：

| 变量 | 必填 | 描述 |
|----------|----------|-------------|
| `POSTGRES_PASSWORD` | 是 | 超级用户密码 |
| `POSTGRES_USER` | 否 | 超级用户名（默认：`postgres`） |
| `POSTGRES_DB` | 否 | 默认数据库名（默认：与 `POSTGRES_USER` 相同） |

### 下一步

配置好持久化存储后，您就可以进一步自定义 PostgreSQL 了。本指南的下一章涵盖：

- 使用初始化脚本自动创建 schema
- 针对容器化工作负载的性能调优
- 时区和区域设置配置

## 高级配置与初始化

上一节配置了持久化存储，现在您可以为实际用途自定义 PostgreSQL 了。本指南涵盖在 Docker 容器中运行 PostgreSQL 的高级配置技术，包括自动数据库初始化、性能调优和时区配置。

### 概述

虽然 PostgreSQL 容器可以使用默认设置快速启动，但生产环境需要自定义配置。本指南解释如何：

- 在容器启动时自动创建数据库、schema 和用户
- 针对容器化工作负载调优 PostgreSQL 性能参数
- 配置时区和区域设置

### 初始化脚本

官方 PostgreSQL Docker 镜像支持在容器首次启动时自动运行初始化脚本。放置在 `/docker-entrypoint-initdb.d/` 目录中的任何文件都会按字母顺序执行。

#### 初始化工作原理

当容器启动时，它会检查 PostgreSQL 数据目录是否为空。如果该目录已包含数据，PostgreSQL 会立即启动，不运行任何初始化。如果目录为空，容器会运行 `initdb` 创建一个新的数据库集群，然后在启动 PostgreSQL 之前，按字母顺序执行 `/docker-entrypoint-initdb.d/` 中的所有脚本。

#### 支持的文件格式

| 格式 | 描述 |
|--------|-------------|
| `.sql` | 直接执行的 SQL 命令 |
| `.sql.gz` | Gzip 压缩的 SQL 文件 |
| `.sh` | 使用 bash 执行的 Shell 脚本 |

> [!IMPORTANT]
>
> 初始化脚本仅在 PostgreSQL 数据目录（`/var/lib/postgresql/data`）为空时运行。如果您挂载了包含现有数据的卷，初始化会被跳过。此行为防止覆盖现有数据库。

### 挂载初始化脚本

使用 Docker Compose 将初始化脚本挂载到容器中。首先，创建一个项目目录：

```console
$ mkdir -p postgres-project/init-db
$ cd postgres-project
```

创建一个 `compose.yaml` 文件：

```yaml
services:
  db:
    image: postgres:18
    volumes:
      - ./init-db:/docker-entrypoint-initdb.d
      - postgres_data:/var/lib/postgresql
    environment:
      POSTGRES_PASSWORD: mysecretpassword

volumes:
  postgres_data:
```

`init-db` 目录中的所有脚本在容器首次启动时执行。这非常适合引导数据库。

### 初始化脚本示例

在您的 `init-db` 目录中创建一个名为 `init.sql` 的文件：

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

该脚本在容器首次启动时自动运行，创建您的初始数据库 schema。

> [!NOTE]
>
> 确保初始化脚本具有正确的读取权限。如果遇到 "Permission denied" 错误，请运行 `chmod 644 init-db/*.sql`，使文件可被容器读取。

### 性能调优

默认的 PostgreSQL 设置较为保守，以在资源有限的系统上工作。对于生产工作负载，您应根据容器分配的资源来调优这些参数。

#### 方法 1：自定义配置文件

为了完全控制，请挂载一个自定义的 `postgresql.conf` 文件。首先，提取默认配置：

```console
$ docker run -i --rm postgres:18 cat /usr/share/postgresql/postgresql.conf.sample > my-postgres.conf
```

用您想要的设置编辑 `my-postgres.conf`，然后将其挂载到您的 Compose 文件中：

```yaml
services:
  db:
    image: postgres:18
    volumes:
      - ./my-postgres.conf:/etc/postgresql/postgresql.conf
      - ./init-db:/docker-entrypoint-initdb.d
      - postgres_data:/var/lib/postgresql
    command: postgres -c config_file=/etc/postgresql/postgresql.conf
    environment:
      POSTGRES_PASSWORD: mysecretpassword

volumes:
  postgres_data:
```

### 关键配置参数

下表列出了容器化 PostgreSQL 部署中重要的 `postgresql.conf` 参数。

#### 连接设置

| 参数 | 描述 | 默认值 |
|-----------|-------------|---------|
| `listen_addresses` | 监听的 IP 地址 | `localhost` |
| `port` | TCP 端口号 | `5432` |
| `max_connections` | 最大并发连接数 | `100` |

#### 内存设置

| 参数 | 描述 | 推荐的起始值 |
|-----------|-------------|---------------------------|
| `shared_buffers` | 用于缓存的共享内存 | 容器内存的 25% |
| `work_mem` | 每次查询操作的内存 | 4MB - 64MB |
| `maintenance_work_mem` | 用于 VACUUM、CREATE INDEX 的内存 | 64MB - 256MB |
| `effective_cache_size` | 规划器对缓存大小的估计 | 容器内存的 50-75% |

##### Docker 内存限制

调优内存参数时，请使用 Compose 中的 `deploy.resources.limits.memory` 或 `docker run` 的 `--memory` 为容器设置明确的内存限制。如果不设置限制，PostgreSQL 会看到主机的总 RAM，并可能分配超出预期的内存。例如，如果您的容器最多应使用 4GB，请将 `shared_buffers` 设置为约 1GB（25%）。

#### I/O 设置

| 参数 | 描述 | 推荐的起始值 |
|-----------|-------------|---------------------------|
| `effective_io_concurrency` | 并发磁盘 I/O 操作数 | SSD 为 `200`，HDD 为 `2` |

#### 超时设置

| 参数 | 描述 | 默认值 |
|-----------|-------------|---------|
| `statement_timeout` | 任何语句的最大执行时间 | `0`（禁用） |
| `lock_timeout` | 等待锁的最大时间 | `0`（禁用） |
| `deadlock_timeout` | 检查死锁前的等待时间 | `1s` |
| `transaction_timeout` | 事务的最大持续时间 | `0`（禁用） |

> [!NOTE]
>
> 在容器中将 `shared_buffers` 设置得过高可能超出内核的共享内存限制。使用不超过容器内存限制的 25-30%。

### 时区和区域设置配置

正确的本地化可确保时间戳和排序对应用用户表现正确。

```yaml
services:
  db:
    image: postgres:18
    volumes:
      - postgres_data:/var/lib/postgresql
      - /etc/localtime:/etc/localtime:ro
      - /etc/timezone:/etc/timezone:ro
    environment:
      POSTGRES_PASSWORD: mysecretpassword
      TZ: America/New_York

volumes:
  postgres_data:
```

或者，使用 PostgreSQL 命令行参数设置时区：

```yaml
services:
  db:
    image: postgres:18
    command: ["postgres", "-c", "timezone=America/New_York"]
    environment:
      POSTGRES_PASSWORD: mysecretpassword
```

#### 设置区域

在数据库初始化期间，使用 `POSTGRES_INITDB_ARGS` 环境变量指定区域设置：

```yaml
services:
  db:
    image: postgres:18
    volumes:
      - postgres_data:/var/lib/postgresql
    environment:
      POSTGRES_PASSWORD: mysecretpassword
      POSTGRES_INITDB_ARGS: "--encoding=UTF8 --lc-collate=en_US.UTF-8 --lc-ctype=en_US.UTF-8"

volumes:
  postgres_data:
```

这会影响排序（collation）和字符处理行为。在数据库创建后更改此变量无效——它仅在数据目录初始化时的首次运行中适用。

### 连接到数据库

即使您的主机没有安装 `psql`，也可以与容器中运行的 PostgreSQL 交互。

#### 交互式 shell

在容器内打开一个 `psql` 会话：

```console
$ docker exec -it postgres-container psql -U postgres
```

连接到特定数据库：

```console
$ docker exec -it postgres-container psql -U postgres -d mydb
```

## 网络与连接

本指南涵盖两种连接到 Docker 中运行的 PostgreSQL 的常见方式：

- 容器到容器：通过私有 Docker 网络从您的应用容器连接到 PostgreSQL。无需向主机暴露端口。
- 主机到容器：使用 `localhost` 和发布端口从您的笔记本或开发机连接。

先决条件：本指南假设您已运行带有持久化存储的 PostgreSQL。如果没有，请先遵循 [快速搭建与数据持久化](/guides/postgresql/immediate-setup-and-data-persistence/) 指南。

### 内部网络访问（容器到容器）

当您的应用在另一个容器中运行时，通过用户定义的桥接网络连接 PostgreSQL 是推荐方法。这种设置提供自动 DNS 解析，因此您的应用可以使用容器名称作为主机名连接到 PostgreSQL，而无需跟踪 IP 地址。

> [!NOTE]
> 为什么不使用默认的桥接网络？虽然默认桥接网络上的容器可以通信，但它们只能通过 IP 地址通信。由于容器 IP 地址在容器重启时会变化，这将需要您每次都更新 PostgreSQL 连接字符串。用户定义的桥接网络通过提供自动 DNS 解析解决了这个问题，确保即使容器重启并获得新的 IP 地址，您的 PostgreSQL 连接字符串也保持稳定。

下面是一个快速对比：

> [!NOTE]
>
> 以下示例展示了方法上的差异。要实际测试，请先按照本指南中的步骤在适当的网络上设置容器。

使用默认桥接网络，您需要先找到 IP 地址：
```bash
# 获取容器的 IP 地址（重启时变化）
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' postgres-dev
# 输出：172.17.0.2

# 然后从另一个容器使用该 IP 地址连接
# （无需 --network 标志 - 容器默认使用桥接网络）
docker run --rm -it \
  -e PGPASSWORD=mysecretpassword \
  postgres:18 \
  psql -h 172.17.0.2 -U postgres
```

使用用户定义的网络，您只需使用容器名称：
```bash
# 容器名称可直接使用 - 无需查找 IP
docker run --rm -it \
  --network my-app-net \
  -e PGPASSWORD=mysecretpassword \
  postgres:18 \
  psql -h postgres-dev -U postgres
```

#### 第 1 步：创建用户定义的网络

```bash
docker network create my-app-net

# 示例输出
ab7f984be43a0ca15534a9ee568716ddbe869a5875077fad3ef3192e3af7d288

docker network ls
# 输出
ab7f984be43a   my-app-net    bridge    local


```

#### 第 2 步：在该网络上运行 PostgreSQL（不发布端口）

注意这里没有 `-p 5432:5432`。这使 PostgreSQL 保留在 Docker 内部，无法从主机访问，对于生产环境更安全。

```bash
docker run -d --name postgres-dev \
  --network my-app-net \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -v postgres_data:/var/lib/postgresql \
  postgres:18

  # 输出
CONTAINER ID  IMAGE        COMMAND                 CREATED         STATUS        PORTS     NAMES
6d351ed89efc  postgres:18  "docker-entrypoint.s…"  9 seconds ago   Up 8 seconds  5432/tcp  postgres-dev

```

#### 第 3 步：使用 Postgres 容器名称从另一个容器连接

您可以使用一个临时的 `psql` 客户端容器测试连接：

```bash
docker run --rm -it \
  --network my-app-net \
  -e PGPASSWORD=mysecretpassword \
  postgres:18 \
  psql -h postgres-dev -U postgres
```

关键点：`-h postgres-dev` 之所以有效，是因为 Docker DNS 在用户定义的网络上解析容器名称。容器名称充当主机名。

#### 连接字符串示例

从您的应用容器连接时，请使用以下 PostgreSQL 连接字符串：

- PostgreSQL URI 格式：
  这是标准的 PostgreSQL 连接 URI 格式，将所有连接参数组合为一个字符串，受到 PostgreSQL 客户端和库的广泛支持。

  ```bash
  postgresql://postgres:mysecretpassword@postgres-dev:5432/postgres
  ```

  此命令演示了将 PostgreSQL URI 连接字符串作为环境变量传递给容器，您的应用随后可以读取它以连接到数据库。

  Docker run 命令中的示例用法：
  ```bash
  docker run --rm -it \
    --network my-app-net \
    -e DATABASE_URL="postgresql://postgres:mysecretpassword@postgres-dev:5432/postgres" \
    alpine:latest \
    sh -c 'echo "DATABASE_URL is set to: $DATABASE_URL"'
  ```


- PostgreSQL 连接参数：
  此格式使用以空格分隔的键值对，许多 PostgreSQL 客户端库将其作为 URI 格式的替代方案。
  ```bash
  host=postgres-dev
  port=5432
  user=postgres
  password=mysecretpassword
  dbname=postgres
  ```

  应用代码中的示例用法（使用 psycopg2 的 Python）：
  ```python
  conn = psycopg2.connect(
      host="postgres-dev",
      port=5432,
      user="postgres",
      password="mysecretpassword",
      dbname="postgres"
  )
  ```

- 连接到特定数据库：
  将连接字符串中的数据库名替换为要连接的特定数据库，而不是默认的 `postgres` 数据库。
  如果您创建了自定义数据库（例如 `testdb`），请使用：
  ```bash
  postgresql://postgres:mysecretpassword@postgres-dev:5432/testdb
  ```

  禁用 SSL 的示例（在 Docker 网络中常见）：
  在不需要 SSL 加密的私有 Docker 网络内连接时，向连接字符串添加 `?sslmode=disable`。
  ```bash
  postgresql://postgres:mysecretpassword@postgres-dev:5432/testdb?sslmode=disable
  ```

> [!NOTE]
>
> 这些示例使用默认端口 `5432`。如果您连接的是不同的 PostgreSQL 实例或更改了端口，请相应地更新连接字符串。容器名称（`postgres-dev`）由 Docker DNS 解析为该网络上容器的 IP 地址。

### 从主机连接（外部访问）

要使用 `psql`、`pgAdmin`、`DBeaver` 或数据库管理脚本等工具从主机连接到 PostgreSQL，您需要向主机发布 PostgreSQL 的端口（`5432`）。这允许外部工具访问 PostgreSQL 容器。

#### 仅暴露 Postgres 到 localhost（推荐用于开发）

这绑定到 `127.0.0.1`，因此只能从您的本地机器访问，而不能从网络上的其他设备访问。这是开发中最安全的选项。

```bash
docker run -d --name postgres-dev \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -p 127.0.0.1:5432:5432 \
  -v postgres_data:/var/lib/postgresql \
  postgres:18
```

现在从您的主机连接：

- 主机：`localhost` 或 `127.0.0.1`
- 端口：`5432`

如果您的主机安装了 `psql`：
```bash
psql -h localhost -p 5432 -U postgres
```

系统会提示您输入密码。或者，您可以使用 `PGPASSWORD` 环境变量：
```bash
PGPASSWORD=mysecretpassword psql -h localhost -p 5432 -U postgres
```

#### 使用 PostgreSQL GUI 工具连接

流行的 PostgreSQL GUI 工具可以使用这些通用连接详细信息进行连接：主机：`localhost`，端口：`5432`，用户：`postgres`，数据库：`postgres`（或您的数据库名）。

- pgAdmin：基于 Web 的 PostgreSQL 管理和开发平台
- DBeaver：支持 PostgreSQL 和许多其他数据库的通用数据库工具。选择 PostgreSQL 作为连接类型
- TablePlus：适用于 macOS 和 Windows 的现代原生数据库管理工具，界面简洁

所有工具都会提示您输入使用 `POSTGRES_PASSWORD` 设置的密码。

#### 暴露 Postgres 到所有网络接口（谨慎使用）

要允许来自网络上其他设备的连接，请使用 `-p 5432:5432` 而不是 `-p 127.0.0.1:5432:5432`。这会将 PostgreSQL 绑定到主机上的所有网络接口，使其可从任何能访问您主机的设备访问，而不仅仅是 localhost。

```bash
docker run -d --name postgres-dev \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -p 5432:5432 \
  -v postgres_data:/var/lib/postgresql \
  postgres:18
```

> [!WARNING]
>
> 将 PostgreSQL 暴露给所有网络接口（`0.0.0.0:5432`）会使任何能访问您主机的设备都可以连接它。仅在受信任的网络环境或防火墙后面使用此方式。对于生产环境，请考虑改用反向代理或 VPN。

#### 外部访问的 PostgreSQL 安全注意事项

暴露 PostgreSQL 进行外部访问时，请遵循以下 PostgreSQL 特定的安全实践：

- 避免使用 `postgres` 超级用户：默认的 `postgres` 用户拥有完整的数据库权限。请创建仅具有应用所需权限的专用用户。
- 使用强密码：PostgreSQL 密码应当复杂。考虑使用环境变量或机密管理，而不是 `硬编码` 密码。
- 限制网络暴露：绑定到 `127.0.0.1`（仅 localhost）比暴露给所有接口（`0.0.0.0`）更安全。
- 考虑 SSL/TLS：对于生产环境，请将 PostgreSQL 配置为要求 SSL 连接。[高级配置与初始化](/guides/postgresql/advanced-configuration-and-initialization/) 指南展示了如何配置 PostgreSQL 设置。
- 创建特定于应用的用户：使用初始化脚本创建权限有限的用户。例如，用于报告的只读用户，或只能访问特定数据库的用户。

[高级配置与初始化](/guides/postgresql/advanced-configuration-and-initialization/) 指南展示了如何使用初始化脚本自动创建用户和角色。

### 使用 Docker Compose 进行网络配置

Docker Compose 会自动为您的服务创建一个网络，使网络配置更简单。以下是一个结合了内部和外部访问的示例：

```yaml
services:
  db:
    image: postgres:18
    container_name: postgres-dev
    environment:
      POSTGRES_PASSWORD: mysecretpassword
    volumes:
      - postgres_data:/var/lib/postgresql
    ports:
      - "127.0.0.1:5432:5432"  # 仅暴露到 localhost
    networks:
      - app-network

  app:
    build: ./my-app
    environment:
      DATABASE_URL: postgresql://postgres:mysecretpassword@db:5432/mydb
    networks:
      - app-network
    depends_on:
      - db

volumes:
  postgres_data:

networks:
  app-network:
    driver: bridge
```

在这个以 PostgreSQL 为中心的设置中：
- `app` 服务在连接字符串中使用服务名（`db`）作为主机名连接到 PostgreSQL
- PostgreSQL 可从您主机上的 `localhost:5432` 访问，供外部工具使用
- 两个服务都隔离在自定义网络上，提供网络级安全性
- `depends_on` 指令确保 PostgreSQL 在您的应用之前启动

应用服务的 PostgreSQL 连接详细信息：
- 主机名：`db`（由 Docker DNS 解析）
- 端口：`5432`（PostgreSQL 默认端口）
- 数据库：`mydb`（如连接字符串中所指定）
- 用户：`postgres`（或您创建的自定义用户）

> [!NOTE]
>
> Docker Compose 会自动为您的项目创建一个网络。服务无需显式网络配置即可通过服务名相互访问，但定义自定义网络能让您有更多控制权。对于 PostgreSQL，这意味着无论容器重启还是 IP 变化，您的应用始终可以使用服务名连接。

### 故障排查

本节涵盖使用 Docker 网络时常见的 PostgreSQL 连接问题及其解决方案。

#### "Could not translate host name postgres-dev"（无法解析主机名 postgres-dev）

- 两个容器必须位于同一个 Docker 网络（`my-app-net`）上。
- 验证网络是否存在：`docker network ls`
- 检查容器位于哪个网络：`docker inspect postgres-dev | grep NetworkMode`
- 确保您使用的是用户定义的网络，而不是默认桥接网络

#### "Connection refused"（连接被拒绝）或 "could not connect to server"（无法连接到服务器）

- PostgreSQL 可能仍在初始化：PostgreSQL 需要几秒钟来启动并初始化数据库集群。容器启动后等待 5-10 秒再重试。
- 检查 PostgreSQL 容器是否正在运行：

  ```bash
  docker ps --filter name=postgres-dev
  ```

- 检查 PostgreSQL 日志以查找初始化或连接错误：

  ```bash
  docker logs postgres-dev
  ```

  查找类似 "database system is ready to accept connections" 的消息，以确认 PostgreSQL 已完全启动。

- 验证端口映射是否正确：

  ```bash
  docker port postgres-dev
  ```

  这应显示 `5432/tcp -> 127.0.0.1:5432`（或如果绑定到所有接口则为 `0.0.0.0:5432`）。

- 从容器内测试 PostgreSQL 连接：

  ```bash
  docker exec -it postgres-dev psql -U postgres -c "SELECT version();"
  ```

  如果这样可行但外部连接失败，问题出在端口发布上，而不是 PostgreSQL 本身。

#### "Password authentication failed"（密码验证失败）或 "FATAL: password authentication failed for user"（用户密码验证失败）

- 确认密码：验证您使用的是启动容器时在 `POSTGRES_PASSWORD` 中设置的相同密码。
- 包含旧凭据的现有卷：如果您复用了现有卷，原始初始化时的密码仍然有效。`POSTGRES_PASSWORD` 环境变量仅在首次数据库初始化时设置密码。要重置：
  - 移除卷：`docker volume rm postgres_data`
  - 或使用旧密码连接
  - 或在连接后更改密码：`ALTER USER postgres WITH PASSWORD 'newpassword';`
- 尝试使用密码提示连接：`psql -h localhost -U postgres -W`（`-W` 标志强制提示输入密码）
- 使用 PGPASSWORD 环境变量：`PGPASSWORD=mysecretpassword psql -h localhost -U postgres`
- 检查 PostgreSQL 身份验证配置：如果您自定义了 `pg_hba.conf`，请验证身份验证方法允许密码验证

#### "Network not found"（找不到网络）

- 在启动容器之前确保网络存在：`docker network create my-app-net`
- 如果使用 Docker Compose，网络在您运行 `docker compose up` 时会自动创建

## PostgreSQL 的配套工具

### PostgreSQL 生态配套：pgAdmin、PgBouncer 与性能测试

运行一个独立的 PostgreSQL 容器通常只是开始。当数千个连接到达，或者您需要一个可视化界面来管理数据库时，会发生什么？

这就是**配套工具**发挥作用的地方。这些应用扩展了 PostgreSQL 核心数据库引擎本身不原生提供的能力：可视化管理、连接池和性能基准测试。本指南涵盖如何在 Docker 中部署 pgAdmin 4、PgBouncer、Pgpool-II 和 `pgbench`，何时使用每种工具，以及展示其性能影响的真实基准测试结果。

### pgAdmin 4：可视化管理平台

pgAdmin 4 是 PostgreSQL 行业标准的开源管理工具。在 Docker 中部署时，它通常运行在**服务器模式**（Server Mode），提供多用户 Web 界面来管理一个或多个数据库实例。

虽然您可以使用 `psql` 在命令行完成所有操作，但可视化界面显著简化了编写复杂查询、可视化表结构和探索数据库对象。

#### 关键注意事项

在 Docker 中运行 pgAdmin 时，请牢记以下几点：

- **镜像**：使用官方的 `dpage/pgadmin4` 镜像
- **网络**：在 Docker Compose 环境中，pgAdmin 使用内部服务名（例如 `db:5432`）而不是 `localhost` 连接到数据库

#### Docker Compose 配置

要快速部署 pgAdmin：

```yaml
pgadmin:
  image: dpage/pgadmin4:8.14
  environment:
    PGADMIN_DEFAULT_EMAIL: admin@example.com
    PGADMIN_DEFAULT_PASSWORD: secure_password
  volumes:
    - pgadmin_data:/var/lib/pgadmin
  ports:
    - "8080:80"
```

使用此配置，可在 `http://localhost:8080` 访问 pgAdmin 界面。使用环境变量中指定的电子邮件和密码进行初始登录。

> [!IMPORTANT]
>
> 在生产环境中，请将 `PGADMIN_DEFAULT_PASSWORD` 作为外部环境变量传递或使用 Docker 机密。在 `docker-compose.yml` 中以明文存储密码会带来安全风险。

现在您已经有了可视化数据库管理，生产环境中的下一个挑战是处理连接负载。下一节解释如何管理大容量的数据库流量。

### PgBouncer：轻量级连接池

PostgreSQL 为每个客户端连接创建一个新的进程，这会消耗大量 RAM。当您有 1,000 个并发用户时会发生什么？PgBouncer 正是解决这个问题。

PgBouncer 是一个轻量级代理，用于池化连接，允许数千个应用共享少量实际的数据库后端。可以将其想象为交通管制员：每个人都想同时通过，但管制员调节流量以防止拥堵。

#### 池化模式

PgBouncer 提供三种不同的池化模式：

| 模式 | 描述 | 使用场景 |
|------|-------------|----------|
| **Session** | 在整个会话期间分配连接 | 长连接、会话变量 |
| **Transaction** | 每次事务结束后归还连接 | Web 应用、微服务（最常见） |
| **Statement** | 每条 SQL 语句后归还连接 | 简单查询、无多语句事务 |

#### 何时使用 PgBouncer

当您遇到以下情况时，PgBouncer 变得必不可少：

- "too many connections"（连接过多）错误
- 连接开销导致的高内存消耗
- 许多短连接（Web 应用、无服务器函数）
- 需要用有限的数据库连接为数千个客户端提供服务

#### 完整的 Docker Compose 设置

要一起运行 PostgreSQL 和 PgBouncer，您需要三个文件：`docker-compose.yml`、`pgbouncer.ini` 和 `userlist.txt`。

首先，创建 PgBouncer 配置文件（`pgbouncer.ini`）：

```bash
[databases]
benchmark = host=postgres port=5432 dbname=benchmark user=postgres

[pgbouncer]
listen_addr = 0.0.0.0
listen_port = 6432
auth_type = trust
auth_file = /etc/pgbouncer/userlist.txt
admin_users = postgres
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 50
min_pool_size = 10
reserve_pool_size = 10
max_db_connections = 100
```

接下来，创建用户身份验证文件（`userlist.txt`）：

```bash
"postgres" "postgres"
```

最后，创建 Docker Compose 文件（`docker-compose.yml`）：

```yaml
services:
  postgres:
    image: postgres:18
    container_name: postgres
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: benchmark
      POSTGRES_HOST_AUTH_METHOD: trust
    volumes:
      - postgres_data:/var/lib/postgresql
    ports:
      - "5432:5432"
    networks:
      - pgnet
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

  pgbouncer:
    image: percona/percona-pgbouncer:1.25.0
    container_name: pgbouncer
    volumes:
      - ./pgbouncer.ini:/etc/pgbouncer/pgbouncer.ini
      - ./userlist.txt:/etc/pgbouncer/userlist.txt
    ports:
      - "6432:6432"
    networks:
      - pgnet
    depends_on:
      postgres:
        condition: service_healthy

volumes:
  postgres_data:

networks:
  pgnet:
    driver: bridge
```

关键配置说明：

- `PgBouncer` 监听端口 **6432**，避免与端口 5432 上的直接 PostgreSQL 连接混淆
- 带有 `service_healthy` 条件的 `depends_on` 指令确保 PgBouncer 仅在 PostgreSQL 就绪后启动
- `pool_mode = transaction` 是大多数 Web 应用的最佳选择
- [Percona PgBouncer 镜像](https://hub.docker.com/r/percona/percona-pgbouncer) 需要挂载配置文件（不带 `:ro` 标志，因为入口点脚本需要修改它们）
- 为简单起见，本示例使用 `trust` 身份验证。在生产环境中，请配置适当的 SCRAM-SHA-256 身份验证

> [!NOTE]
>
> `Percona PgBouncer` 入口点脚本在启动时处理配置文件。挂载它们时不要使用只读标志，以避免权限错误。

### `pgbench`：性能基准测试

`pgbench` 是官方 PostgreSQL 镜像附带的基准测试实用程序。它允许您模拟繁重的工作负载，并验证您的 Docker 配置在压力下的表现。

#### 初始化基准测试表

首先，创建测试表。`-s`（scale）参数决定数据大小——比例因子 50 大约创建 500 万行：

```bash
docker exec postgres pgbench -i -s 50 -U postgres benchmark
```

#### 运行压力测试

关键参数：

- `-c`：模拟的客户端数量
- `-j`：线程数
- `-T`：持续时间（秒）

使用直接 PostgreSQL 连接进行测试：

```bash
docker exec postgres pgbench -h localhost -U postgres -c 50 -j 4 -T 60 benchmark
```

通过 PgBouncer 进行测试：

```bash
docker exec postgres pgbench -h pgbouncer -p 6432 -U postgres -c 50 -j 4 -T 60 benchmark
```

### 理解基准测试结果

PgBouncer 真的有差别吗？自己运行基准测试来找出答案。您的结果会根据您的硬件、Docker 配置、网络设置和系统负载而有所不同。

#### 预期结果

当您运行这些基准测试时，您会观察到模式而不是具体数字。可以将其想象为比较两条不同的上班路线："更快"的路线取决于交通状况、一天中的时间和您的交通工具。

#### 关键观察

比较直接连接与 PgBouncer 时，您通常会注意到：

##### 1. 连接开销差异显著

直接连接要求 PostgreSQL 为每个客户端生成新进程。PgBouncer 重用现有连接。观察结果中的"初始连接时间"指标——PgBouncer 通常显示明显更快的连接建立。

##### 2. 压力下的行为揭示了真正的差异

尝试逐渐增加客户端数量（`-c` 参数）：50、100、150、200。在某些时候，直接连接将因 "too many clients already" 而失败，而 PgBouncer 继续处理请求。这是 PgBouncer 的主要价值：**它防止连接耗尽**。

##### 3. 吞吐量因环境而异

在某些系统上，直接连接在低并发下显示更高的每秒事务数（TPS）。在其他系统上，即使客户端很少，PgBouncer 也胜出。差异取决于：
- 可用的 CPU 和内存
- Docker 网络开销
- 磁盘 I/O 速度
- 连接是否被快速打开和关闭
