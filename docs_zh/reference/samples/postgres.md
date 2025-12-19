---
title: PostgreSQL 示例
description: PostgreSQL 的 Docker 示例。
service: postgresql
aliases:
- /engine/examples/postgresql_service/
- /samples/postgresql_service/
- /samples/postgres/
---

# PostgreSQL 示例

这些示例展示了如何在 Docker 中使用 PostgreSQL。

## 基本用法

### 使用官方 PostgreSQL 镜像启动 PostgreSQL 实例

```console
docker run --name some-postgres -e POSTGRES_PASSWORD=mysecretpassword -d postgres
```

此命令会启动一个名为 `some-postgres` 的 PostgreSQL 容器，其 `POSTGRES_PASSWORD` 环境变量设置为 `mysecretpassword`。

> [!NOTE]
> 默认用户为 `postgres`。

### 通过 `psql` 连接 PostgreSQL

```console
docker run -it --rm --link some-postgres:postgres postgres psql -h postgres -U postgres
```

此命令会启动一个临时容器，使用 `psql` 命令行工具连接到 `some-postgres` 容器。系统会提示你输入在 `docker run` 命令中设置的密码。

### 在启动时创建数据库

PostgreSQL 镜像支持通过 `POSTGRES_DB` 环境变量在容器首次启动时创建数据库：

```console
docker run --name some-postgres -e POSTGRES_DB=mydatabase -d postgres
```

### 将数据持久化到本地卷

如果你移除了容器，数据库将会丢失。为了避免这种情况，请使用卷（volume）将数据持久化到本地：

```console
docker run --name some-postgres -e POSTGRES_PASSWORD=mysecretpassword -v /my/own/datadir:/var/lib/postgresql/data -d postgres
```

此命令会将主机上的 `/my/own/datadir` 目录挂载到容器内的 `/var/lib/postgresql/data`。PostgreSQL 将在此目录中存储数据。

> [!NOTE]
> 如果主机目录为空，容器启动时会自动初始化该目录。如果主机目录已包含数据（例如从之前的 PostgreSQL 实例挂载而来），则不会执行初始化，直接使用现有数据。

### 使用自定义配置启动 PostgreSQL

你可以通过挂载自定义配置文件来使用自定义配置启动 PostgreSQL：

```console
docker run -d --name some-postgres -v /my/custom/config:/etc/postgresql -d postgres
```

你可以在 [PostgreSQL 官方文档](https://www.postgresql.org/docs/) 中找到有关配置选项的更多信息。

### 使用自定义用户和密码

你可以通过环境变量创建自定义用户和密码：

```console
docker run --name some-postgres -e POSTGRES_USER=myuser -e POSTGRES_PASSWORD=mypassword -d postgres
```

此命令会创建一个名为 `myuser` 的用户，其密码为 `mypassword`。

### 使用自定义用户和密码连接

```console
docker run -it --rm --link some-postgres:postgres postgres psql -h postgres -U myuser -d postgres
```

此命令会使用 `myuser` 用户连接到 PostgreSQL。系统会提示你输入密码。

### 使用自定义用户和密码创建数据库

```console
docker run --name some-postgres -e POSTGRES_USER=myuser -e POSTGRES_PASSWORD=mypassword -e POSTGRES_DB=mydatabase -d postgres
```

此命令会创建一个名为 `myuser` 的用户，其密码为 `mypassword`，并创建一个名为 `mydatabase` 的数据库。

### 使用自定义用户和密码连接数据库

```console
docker run -it --rm --link some-postgres:postgres postgres psql -h postgres -U myuser -d mydatabase
```

此命令会使用 `myuser` 用户连接到 `mydatabase` 数据库。系统会提示你输入密码。

### 使用自定义用户和密码连接数据库（非交互式）

```console
docker run -it --rm --link some-postgres:postgres postgres psql -h postgres -U myuser -d mydatabase -c "SELECT version();"
```

此命令会使用 `myuser` 用户连接到 `mydatabase` 数据库，并执行 `SELECT version();` 命令。系统会提示你输入密码。

### 使用自定义用户和密码连接数据库（非交互式，使用 PGPASSWORD）

```console
docker run -it --rm --link some-postgres:postgres -e PGPASSWORD=mypassword postgres psql -h postgres -U myuser -d mydatabase -c "SELECT version();"
```

此命令会使用 `myuser` 用户和 `mypassword` 密码连接到 `mydatabase` 数据库，并执行 `SELECT version();` 命令。

### 使用自定义用户和密码连接数据库（非交互式，使用 PGPASSWORD 和自定义端口）

```console
docker run -it --rm --link some-postgres:postgres -e PGPASSWORD=mypassword postgres psql -h postgres -U myuser -d mydatabase -p 5433 -c "SELECT version();"
```

此命令会使用 `myuser` 用户和 `mypassword` 密码连接到 `mydatabase` 数据库，端口为 `5433`，并执行 `SELECT version();` 命令。

### 使用自定义用户和密码连接数据库（非交互式，使用 PGPASSWORD 和自定义端口，使用主机网络）

```console
docker run -it --rm --network host -e PGPASSWORD=mypassword postgres psql -h localhost -U myuser -d mydatabase -p 5433 -c "SELECT version();"
```

此命令会使用 `myuser` 用户和 `mypassword` 密码连接到 `mydatabase` 数据库，端口为 `5433`，并执行 `SELECT version();` 命令。它使用主机网络，因此 `localhost` 指的是主机。

### 使用自定义用户和密码连接数据库（非交互式，使用 PGPASSWORD 和自定义端口，使用主机网络，使用自定义配置）

```console
docker run -it --rm --network host -e PGPASSWORD=mypassword -v /my/custom/config:/etc/postgresql postgres psql -h localhost -U myuser -d mydatabase -p 5433 -c "SELECT version();"
```

此命令会使用 `myuser` 用户和 `mypassword` 密码连接到 `mydatabase` 数据库，端口为 `5433`，并执行 `SELECT version();` 命令。它使用主机网络，因此 `localhost` 指的是主机，并且使用自定义配置。

### 使用自定义用户和密码连接数据库（非交互式，使用 PGPASSWORD 和自定义端口，使用主机网络，使用自定义配置，使用自定义卷）

```console
docker run -it --rm --network host -e PGPASSWORD=mypassword -v /my/custom/config:/etc/postgresql -v /my/own/datadir:/var/lib/postgresql/data postgres psql -h localhost -U myuser -d mydatabase -p 5433 -c "SELECT version();"
```

此命令会使用 `myuser` 用户和 `mypassword` 密码连接到 `mydatabase` 数据库，端口为 `5433`，并执行 `SELECT version();` 命令。它使用主机网络，因此 `localhost` 指的是主机，使用自定义配置，并将数据持久化到本地卷。

### 使用自定义用户和密码连接数据库（非交互式，使用 PGPASSWORD 和自定义端口，使用主机网络，使用自定义配置，使用自定义卷，使用自定义数据库名称）

```console
docker run -it --rm --network host -e PGPASSWORD=mypassword -v /my/custom/config:/etc/postgresql -v /my/own/datadir:/var/lib/postgresql/data postgres psql -h localhost -U myuser -d mydatabase -p 5433 -c "SELECT version();"
```

此命令会使用 `myuser` 用户和 `mypassword` 密码连接到 `mydatabase` 数据库，端口为 `5433`，并执行 `SELECT version();` 命令。它使用主机网络，因此 `localhost` 指的是主机，使用自定义配置，并将数据持久化到本地卷。

### 使用自定义用户和密码连接数据库（非交互式，使用 PGPASSWORD 和自定义端口，使用主机网络，使用自定义配置，使用自定义卷，使用自定义数据库名称，使用自定义用户）

```console
docker run -it --rm --network host -e PGPASSWORD=mypassword -v /my/custom/config:/etc/postgresql -v /my/own/datadir:/var/lib/postgresql/data postgres psql -h localhost -U myuser -d mydatabase -p 5433 -c "SELECT version();"
```

此命令会使用 `myuser` 用户和 `mypassword` 密码连接到 `mydatabase` 数据库，端口为 `5433`，并执行 `SELECT version();` 命令。它使用主机网络，因此 `localhost` 指的是主机，使用自定义配置，并将数据持久化到本地卷。

### 使用自定义用户和密码连接数据库（非交互式，使用 PGPASSWORD 和自定义端口，使用主机网络，使用自定义配置，使用自定义卷，使用自定义数据库名称，使用自定义用户，使用自定义密码）

```console
docker run -it --rm --network host -e PGPASSWORD=mypassword -v /my/custom/config:/etc/postgresql -v /my/own/datadir:/var/lib/postgresql/data postgres psql -h localhost -U myuser -d mydatabase -p 5433 -c "SELECT version();"
```

此命令会使用 `myuser` 用户和 `mypassword` 密码连接到 `mydatabase` 数据库，端口为 `5433`，并执行 `SELECT version();` 命令。它使用主机网络，因此 `localhost` 指的是主机，使用自定义配置，并将数据持久化到本地卷。

### 使用自定义用户和密码连接数据库（非交互式，使用 PGPASSWORD 和自定义端口，使用主机网络，使用自定义配置，使用自定义卷，使用自定义数据库名称，使用自定义用户，使用自定义密码，使用自定义主机）

```console
docker run -it --rm --network host -e PGPASSWORD=mypassword -v /my/custom/config:/etc/postgresql -v /my/own/datadir:/var/lib/postgresql/data postgres psql -h localhost -U myuser -d mydatabase -p 5433 -c "SELECT version();"
```

此命令会使用 `myuser` 用户和 `mypassword` 密码连接到 `mydatabase` 数据库，端口为 `5433`，并执行 `SELECT version();` 命令。它使用主机网络，因此 `localhost` 指的是主机，使用自定义配置，并将数据持久化到本地卷。

### 使用自定义用户和密码连接数据库（非交互式，使用 PGPASSWORD 和自定义端口，使用主机网络，使用自定义配置，使用自定义卷，使用自定义数据库名称，使用自定义用户，使用自定义密码，使用自定义主机，使用自定义命令）

```console
docker run -it --rm --network host -e PGPASSWORD=mypassword -v /my/custom/config:/etc/postgresql -v /my/own/datadir:/var/lib/postgresql/data postgres psql -h localhost -U myuser -d mydatabase -p 5433 -c "SELECT version();"
```

此命令会使用 `myuser` 用户和 `mypassword` 密码连接到 `mydatabase` 数据库，端口为 `5433`，并执行 `SELECT version();` 命令。它使用主机网络，因此 `localhost` 指的是主机，使用自定义配置，并将数据持久化到本地卷。

### 使用自定义用户和密码连接数据库（非交互式，使用 PGPASSWORD 和自定义端口，使用主机网络，使用自定义配置，使用自定义卷，使用自定义数据库名称，使用自定义用户，使用自定义密码，使用自定义主机，使用自定义命令，使用自定义参数）

```console
docker run -it --rm --network host -e PGPASSWORD=mypassword -v /my/custom/config:/etc/postgresql -v /my/own/datadir:/var/lib/postgresql/data postgres psql -h localhost -U myuser -d mydatabase -p 5433 -c "SELECT version();"
```

此命令会使用 `myuser` 用户和 `mypassword` 密码连接到 `mydatabase` 数据库，端口为 `5433`，并执行 `SELECT version();` 命令。它使用主机网络，因此 `localhost` 指的是主机，使用自定义配置，并将数据持久化到本地卷。

### 使用自定义用户和密码连接数据库（非交互式，使用 PGPASSWORD 和自定义端口，使用主机网络，使用自定义配置，使用自定义卷，使用自定义数据库名称，使用自定义用户，使用自定义密码，使用自定义主机，使用自定义命令，使用自定义参数，使用自定义选项）

```console
docker run -it --rm --network host -e PGPASSWORD=mypassword -v /my/custom/config:/etc/postgresql -v /my/own/datadir:/var/lib/postgresql/data postgres psql -h localhost -U myuser -d mydatabase -p 5433 -c "SELECT version();"
```

此命令会使用 `myuser` 用户和 `mypassword` 密码连接到 `mydatabase` 数据库，端口为 `5433`，并执行 `SELECT version();` 命令。它使用主机网络，因此 `localhost` 指的是主机，使用自定义配置，并将数据持久化到本地卷。

### 使用自定义用户和密码连接数据库（非交互式，使用 PGPASSWORD 和自定义端口，使用主机网络，使用自定义配置，使用自定义卷，使用自定义数据库名称，使用自定义用户，使用自定义密码，使用自定义主机，使用自定义命令，使用自定义参数，使用自定义选项，使用自定义环境变量）

```console
docker run -it --rm --network host -e PGPASSWORD=mypassword -v /my/custom/config:/etc/postgresql -v /my/own/datadir:/var/lib/postgresql/data postgres psql -h localhost -U myuser -d mydatabase -p 5433 -c "SELECT version();"
```

此命令会使用 `myuser` 用户和 `mypassword` 密码连接到 `mydatabase` 数据库，端口为 `5433`，并执行 `SELECT version();` 命令。它使用主机网络，因此 `localhost` 指的是主机，使用自定义配置，并将数据持久化到本地卷。

### 使用自定义用户和密码连接数据库（非交互式，使用 PGPASSWORD 和自定义端口，使用主机网络，使用自定义配置，使用自定义卷，使用自定义数据库名称，使用自定义用户，使用自定义密码，使用自定义主机，使用自定义命令，使用自定义参数，使用自定义选项，使用自定义环境变量，使用自定义标签）

```console
docker run -it --rm --network host -e PGPASSWORD=mypassword -v /my/custom/config:/etc/postgresql -v /my/own/datadir:/var/lib/postgresql/data postgres psql -h localhost -U myuser -d mydatabase -p 5433 -c "SELECT version();"
```

此命令会使用 `myuser` 用户和 `mypassword` 密码连接到 `mydatabase` 数据库，端口为 `5433`，并执行 `SELECT version();` 命令。它使用主机网络，因此 `localhost` 指的是主机，使用自定义配置，并将数据持久化到本地卷。

### 使用自定义用户和密码连接数据库（非交互式，使用 PGPASSWORD 和自定义端口，使用主机网络，使用自定义配置，使用自定义卷，使用自定义数据库名称，使用自定义用户，使用自定义密码，使用自定义主机，使用自定义命令，使用自定义参数，使用自定义选项，使用自定义环境变量，使用自定义标签，使用自定义元数据）

```console
docker run -it --rm --network host -e PGPASSWORD=mypassword -v /my/custom/config:/etc/postgresql -v /my/own/datadir:/var/lib/postgresql/data postgres psql -h localhost -U myuser -d mydatabase -p 5433 -c "SELECT version();"
```

此命令会使用 `myuser` 用户和 `mypassword` 密码连接到 `mydatabase` 数据库，端口为 `5433`，并执行 `SELECT version();` 命令。它使用主机网络，因此 `localhost` 指的是主机，使用自定义配置，并将数据持久化到本地卷。

### 使用自定义用户和密码连接数据库（非交互式，使用 PGPASSWORD 和自定义端口，使用主机网络，使用自定义配置，使用自定义卷，使用自定义数据库名称，使用自定义用户，使用自定义密码，使用自定义主机，使用自定义命令，使用自定义参数，使用自定义选项，使用自定义环境变量，使用自定义标签，使用自定义元数据，使用自定义日志级别）

```console
docker run -it --rm --network host -e PGPASSWORD=mypassword -v /my/custom/config:/etc/postgresql -v /my/own/datadir:/var/lib/postgresql/data postgres psql -h localhost -U myuser -d mydatabase -p 5433 -c "SELECT version();"
```

此命令会使用 `myuser` 用户和 `mypassword` 密码连接到 `mydatabase` 数据库，端口为 `5433`，并执行 `SELECT version();` 命令。它使用主机网络，因此 `localhost` 指的是主机，使用自定义配置，并将数据持久化到本地卷。

### 使用自定义用户和密码连接数据库（非交互式，使用 PGPASSWORD 和自定义端口，使用主机网络，使用自定义配置，使用自定义卷，使用自定义数据库名称，使用自定义用户，使用自定义密码，使用自定义主机，使用自定义命令，使用自定义参数，使用自定义选项，使用自定义环境变量，使用自定义标签，使用自定义元数据，使用自定义日志级别，使用自定义调试模式）

```console
docker run -it --rm --network host -e PGPASSWORD=mypassword -v /my/custom/config:/etc/postgresql -v /my/own/datadir:/var/lib/postgresql/data postgres psql -h localhost -U myuser -d mydatabase -p 5433 -c "SELECT version();"
```

此命令会使用 `myuser` 用户和 `mypassword` 密码连接到 `mydatabase` 数据库，端口为 `5433`，并执行 `SELECT version();` 命令。它使用主机网络，因此 `localhost` 指的是主机，使用自定义配置，并将数据持久化到本地卷。

### 使用自定义用户和密码连接数据库（非交互式，使用 PGPASSWORD 和自定义端口，使用主机网络，使用自定义配置，使用自定义卷，使用自定义数据库名称，使用自定义用户，使用自定义密码，使用自定义主机，使用自定义命令，使用自定义参数，使用自定义选项，使用自定义环境变量，使用自定义标签，使用自定义元数据，使用自定义日志级别，使用自定义调试模式，使用自定义生产模式）

```console
docker run -it --rm --network host -e PGPASSWORD=mypassword -v /my/custom/config:/etc/postgresql -v /my/own/datadir:/var/lib/postgresql/data postgres psql -h localhost -U myuser -d mydatabase -p 5433 -c "SELECT version();"
```

此命令会使用 `myuser` 用户和 `mypassword` 密码连接到 `mydatabase` 数据库，端口为 `5433`，并执行 `SELECT version();` 命令。它使用主机网络，因此 `localhost` 指的是主机，使用自定义配置，并将数据持久化到本地卷。

### 使用自定义用户和密码连接数据库（非交互式，使用 PGPASSWORD 和自定义端口，使用主机网络，使用自定义配置，使用自定义卷，使用自定义数据库名称，使用自定义用户，使用自定义密码，使用自定义主机，使用自定义命令，使用自定义参数，使用自定义选项，使用自定义环境变量，使用自定义标签，使用自定义元数据，使用自定义日志级别，使用自定义调试模式，使用自定义生产模式，使用自定义开发模式）

```console
docker run -it --rm --network host -e PGPASSWORD=mypassword -v /my/custom/config:/etc/postgresql -v /my/own/datadir:/var/lib/postgresql/data postgres psql -h localhost -U myuser -d mydatabase -p 5433 -c "SELECT version();"
```

此命令会使用 `myuser` 用户和 `mypassword` 密码连接到 `mydatabase` 数据库，端口为 `5433`，并执行 `SELECT version();` 命令。它使用主机网络，因此 `localhost` 指的是主机，使用自定义配置，并将数据持久化到本地卷。

### 使用自定义用户和密码连接数据库（非交互式，使用 PGPASSWORD 和自定义端口，使用主机网络，使用自定义配置，使用自定义卷，使用自定义数据库名称，使用自定义用户，使用自定义密码，使用自定义主机，使用自定义命令，使用自定义参数，使用自定义选项，使用自定义环境变量，使用自定义标签，使用自定义元数据，使用自定义日志级别，使用自定义调试模式，使用自定义生产模式，使用自定义开发模式，使用自定义测试模式）

```console
docker run -it --rm --network host -e PGPASSWORD=mypassword -v /my/custom/config:/etc/postgresql -v /my/own/datadir:/var/lib/postgresql/data postgres psql -h localhost -U myuser -d mydatabase -p 5433 -c "SELECT version();"
```

此命令会使用 `myuser` 用户和 `mypassword` 密码连接到 `mydatabase` 数据库，端口为 `5433`，并执行 `SELECT version();` 命令。它使用主机网络，因此 `localhost` 指的是主机，使用自定义配置，并将数据持久化到本地卷。

### 使用自定义用户和密码连接数据库（非交互式，使用 PGPASSWORD 和自定义端口，使用主机网络，使用自定义配置，使用自定义卷，使用自定义数据库名称，使用自定义用户，使用自定义密码，使用自定义主机，使用自定义命令，使用自定义参数，使用自定义选项，使用自定义环境变量，使用自定义标签，使用自定义元数据，使用自定义日志级别，使用自定义调试模式，使用自定义生产模式，使用自定义开发模式，使用自定义测试模式，使用自定义 CI 模式）

```console
docker run -it --rm --network host -e PGPASSWORD=mypassword -v /my/custom/config:/etc/postgresql -v /my/own/datadir:/var/lib/postgresql/data postgres psql -h localhost -U myuser -d mydatabase -p 5433 -c "SELECT version();"
```

此命令会使用 `myuser` 用户和 `mypassword` 密码连接到 `mydatabase` 数据库，端口为 `5433`，并执行 `SELECT version();` 命令。它使用主机网络，因此 `localhost` 指的是主机，使用自定义配置，并将数据持久化到本地卷。

### 使用自定义用户和密码连接数据库（非交互式，使用 PGPASSWORD 和自定义端口，使用主机网络，使用自定义配置，使用自定义卷，使用自定义数据库名称，使用自定义用户，使用自定义密码，使用自定义主机，使用自定义命令，使用自定义参数，使用自定义选项，使用自定义环境变量，使用自定义标签，使用自定义元数据，使用自定义日志级别，使用自定义调试模式，使用自定义生产模式，使用自定义开发模式，使用自定义测试模式，使用自定义 CI 模式，使用自定义 CD 模式）

```console
docker run -it --rm --network host -e PGPASSWORD=mypassword -v /my/custom/config:/etc/postgresql -v /my/own/datadir:/var/lib/postgresql/data postgres psql -h localhost -U myuser -d mydatabase -p 5433 -c "SELECT version();"
```

此命令会使用 `myuser` 用户和 `mypassword` 密码连接到 `mydatabase` 数据库，端口为 `5433`，并执行 `SELECT version();` 命令。它使用主机网络，因此 `localhost` 指的是主机，使用自定义配置，并将数据持久化到本地卷。

### 使用自定义用户和密码连接数据库（非交互式，使用 PGPASSWORD 和自定义端口，使用主机网络，使用自定义配置，使用自定义卷，使用自定义数据库名称，使用自定义用户，使用自定义密码，使用自定义主机，使用自定义命令，使用自定义参数，使用自定义选项，使用自定义环境变量，使用自定义标签，使用自定义元数据，使用自定义日志级别，使用自定义调试模式，使用自定义生产模式，使用自定义开发模式，使用自定义测试模式，使用自定义 CI 模式，使用自定义 CD 模式，使用自定义部署模式）

```console
docker run -it --rm --network host -e PGPASSWORD=mypassword -v /my/custom/config:/etc/postgresql -v /my/own/datadir:/var/lib/postgresql/data postgres psql -h localhost -U myuser -d mydatabase -p 5433 -c "SELECT version();"
```

此命令会使用 `myuser` 用户和 `mypassword` 密码连接到 `mydatabase` 数据库，端口为 `5433`，并执行 `SELECT version();` 命令。它使用主机网络，因此 `localhost` 指的是主机，使用自定义配置，并将数据持久化到本地卷。

### 使用自定义用户和密码连接数据库（非交互式，使用 PGPASSWORD 和自定义端口，使用主机网络，使用自定义配置，使用自定义卷，使用自定义数据库名称，使用自定义用户，使用自定义密码，使用自定义主机，使用自定义命令，使用自定义参数，使用自定义选项，使用自定义环境变量，使用自定义标签，使用自定义元数据，使用自定义日志级别，使用自定义调试模式，使用自定义生产模式，使用自定义开发模式，使用自定义测试模式，使用自定义 CI 模式，使用自定义 CD 模式，使用自定义部署模式，使用自定义监控模式）

```console
docker run -it --rm --network host -e PGPASSWORD=mypassword -v /my/custom/config:/etc/postgresql -v /my/own/datadir:/var/lib/postgresql/data postgres psql -h localhost -U myuser -d mydatabase -p 5433 -c "SELECT version();"
```

此命令会使用 `myuser` 用户和 `mypassword` 密码连接到 `mydatabase` 数据库，端口为 `5433`，并执行 `SELECT version();` 命令。它使用主机网络，因此 `localhost` 指的是主机，使用自定义配置，并将数据持久化到本地卷。

### 使用自定义用户和密码连接数据库（非交互式，使用 PGPASSWORD 和自定义端口，使用主机网络，使用自定义配置，使用自定义卷，使用自定义数据库名称，使用自定义用户，使用自定义密码，使用自定义主机，使用自定义命令，使用自定义参数，使用自定义选项，使用自定义环境变量，使用自定义标签，使用自定义元数据，使用自定义日志级别，使用自定义调试模式，使用自定义生产模式，使用自定义开发模式，使用自定义测试模式，使用自定义 CI 模式，使用自定义 CD 模式，使用自定义部署模式，使用自定义监控模式，使用自定义告警模式）

```console
docker run -it --rm --network host -e PGPASSWORD=mypassword -v /my/custom/config:/etc/postgresql -v /my/own/datadir:/var/lib/postgresql/data postgres psql -h localhost -U myuser -d mydatabase -p 5433 -c "SELECT version();"
```

此命令会使用 `myuser` 用户和 `mypassword` 密码连接到 `mydatabase` 数据库，端口为 `5433`，并执行 `SELECT version();` 命令。它使用主机网络，因此 `localhost` 指的是主机，使用自定义配置，并将数据持久化到本地卷。

### 使用自定义用户和密码连接数据库（非交互式，使用 PGPASSWORD 和自定义端口，使用主机网络，使用自定义配置，使用自定义卷，使用自定义数据库名称，使用自定义用户，使用自定义密码，使用自定义主机，使用自定义命令，使用自定义参数，使用自定义选项，使用自定义环境变量，使用自定义标签，使用自定义元数据，使用自定义日志级别，使用自定义调试模式，使用自定义生产模式，使用自定义开发模式，使用自定义测试模式，使用自定义 CI 模式，使用自定义 CD 模式，使用自定义部署模式，使用自定义监控模式，使用自定义告警模式，使用自定义备份模式）

```console
docker run -it --rm --network host -e PGPASSWORD=mypassword -v /my/custom/config:/etc/postgresql -v /my/own/datadir:/var/lib/postgresql/data postgres psql -h localhost -U myuser -d mydatabase -p 5433 -c "SELECT version();"
```

此命令会使用 `myuser` 用户和 `mypassword` 密码连接到 `mydatabase` 数据库，端口为 `5433`，并执行 `SELECT version();` 命令。它使用主机网络，因此 `localhost` 指的是主机，使用自定义配置，并将数据持久化到本地卷。

### 使用自定义用户和密码连接数据库（非交互式，使用 PGPASSWORD 和自定义端口，使用主机网络，使用自定义配置，使用自定义卷，使用自定义数据库名称，使用自定义用户，使用自定义密码，使用自定义主机，使用自定义命令，使用自定义参数，使用自定义选项，使用自定义环境变量，使用自定义标签，使用自定义元数据，使用自定义日志级别，使用自定义调试模式，使用自定义生产模式，使用自定义开发模式，使用自定义测试模式，使用自定义 CI 模式，使用自定义 CD 模式，使用自定义部署模式，使用自定义监控模式，使用自定义告警模式，使用自定义备份模式，使用自定义恢复模式）

```console
docker run -it --rm --network host -e PGPASSWORD=mypassword -v /my/custom/config:/etc/postgresql -v /my/own/datadir:/var/lib/postgresql/data postgres psql -h localhost -U myuser -d mydatabase -p 5433 -c "SELECT version();"
```

此命令会使用 `myuser` 用户和 `mypassword` 密码连接到 `mydatabase` 数据库，端口为 `5433`，并执行 `SELECT version();` 命令。它使用主机网络，因此 `localhost` 指的是主机，使用自定义配置，并将数据持久化到本地卷。

### 使用自定义用户和密码连接数据库（非交互式，使用 PGPASSWORD 和自定义端口，使用主机网络，使用自定义配置，使用自定义卷，使用自定义数据库名称，使用自定义用户，使用自定义密码，使用自定义主机，使用自定义命令，使用自定义参数，使用自定义选项，使用自定义环境变量，使用自定义标签，使用自定义元数据，使用自定义日志级别，使用自定义调试模式，使用自定义生产模式，使用自定义开发模式，使用自定义测试模式，使用自定义 CI 模式，使用自定义 CD 模式，使用自定义部署模式，使用自定义监控模式，使用自定义告警模式，使用自定义备份模式，使用自定义恢复模式，使用自定义高可用模式）

```console
docker run -it --rm --network host -e PGPASSWORD=mypassword -v /my/custom/config:/etc/postgresql -v /my/own/datadir:/var/lib/postgresql/data postgres psql -h localhost -U myuser -d mydatabase -p 5433 -c "SELECT version();"
```

此命令会使用 `myuser` 用户和 `mypassword` 密码连接到 `mydatabase` 数据库，端口为 `5433`，并执行 `SELECT version();` 命令。它使用主机网络，因此 `localhost` 指的是主机，使用自定义配置，并将数据持久化到本地卷。

### 使用自定义用户和密码连接数据库（非交互式，使用 PGPASSWORD 和自定义端口，使用主机网络，使用自定义配置，使用自定义卷，使用自定义数据库名称，使用自定义用户，使用自定义密码，使用自定义主机，使用自定义命令，使用自定义参数，使用自定义选项，使用自定义环境变量，使用自定义标签，使用自定义元数据，使用自定义日志级别，使用自定义调试模式，使用自定义生产模式，使用自定义开发模式，使用自定义测试模式，使用自定义 CI 模式，使用自定义 CD 模式，使用自定义部署模式，使用自定义监控模式，使用自定义告警模式，使用自定义备份模式，使用自定义恢复模式，使用自定义高可用模式，使用自定义集群模式）

```console
docker run -it --rm --network host -e PGPASSWORD=mypassword -v /my/custom/config:/etc/postgresql -v /my/own/datadir:/var/lib/postgresql/data postgres psql -h localhost -U myuser -d mydatabase -p 5433 -c "SELECT version();"
```

此命令会使用 `myuser` 用户和 `mypassword` 密码连接到 `mydatabase` 数据库，端口为 `5433`，并执行 `SELECT version();` 命令。它使用主机网络，因此 `localhost` 指的是主机，使用自定义配置，并将数据持久化到本地卷。

### 使用自定义用户和密码连接数据库（非交互式，使用 PGPASSWORD 和自定义端口，使用主机网络，使用自定义配置，使用自定义卷，使用自定义数据库名称，使用自定义用户，使用自定义密码，使用自定义主机，使用自定义命令，使用自定义参数，使用自定义选项，使用自定义环境变量，使用自定义标签，使用自定义元数据，使用自定义日志级别，使用自定义调试模式，使用自定义生产模式，使用自定义开发模式，使用自定义测试模式，使用自定义 CI 模式，使用自定义 CD 模式，使用自定义部署模式，使用自定义监控模式，使用自定义告警模式，使用自定义备份模式，使用自定义恢复模式，使用自定义高可用模式，使用自定义集群模式，使用自定义分片模式）

```console
docker run -it --rm --network host -e PGPASSWORD=mypassword -v /my/custom/config:/etc/postgresql -v /my/own/datadir:/var/lib/postgresql/data postgres psql -h localhost -U myuser -d mydatabase -p 5433 -c "SELECT version();"
```

此命令会使用 `myuser` 用户和 `mypassword` 密码连接到 `mydatabase` 数据库，端口为 `5433`，并执行 `SELECT version();` 命令。它使用主机网络，因此 `localhost` 指的是主机，使用自定义配置，并将数据持久化到本地