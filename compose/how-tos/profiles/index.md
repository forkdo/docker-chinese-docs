# 在 Compose 中使用配置集



配置文件（Profiles）可帮助您根据不同的环境或用例调整 Compose 应用程序，方法是选择性地激活服务。服务可以分配到一个或多个配置文件；未分配的服务默认启动/停止，而已分配的服务仅在其配置文件处于活动状态时才会启动/停止。通过这种设置，特定服务（例如用于调试或开发的服务）可以包含在单个 `compose.yml` 文件中，并仅在需要时激活。

## 为服务分配配置集

服务通过 [`profiles` 属性](/reference/compose-file/services.md#profiles) 与配置集关联，该属性接收一个配置集名称的数组：

```yaml
services:
  frontend:
    image: frontend
    profiles: [frontend]

  phpmyadmin:
    image: phpmyadmin
    depends_on: [db]
    profiles: [debug]

  backend:
    image: backend

  db:
    image: mysql
```

在此示例中，服务 `frontend` 和 `phpmyadmin` 分别被分配到 `frontend` 和 `debug` 配置集，因此只有在启用各自配置集时才会启动。

没有 `profiles` 属性的服务始终处于启用状态。在这种情况下，运行 `docker compose up` 将只启动 `backend` 和 `db`。

有效的配置集名称遵循正则表达式格式 `[a-zA-Z0-9][a-zA-Z0-9_.-]+`。

> [!TIP]
>
> 应用程序的核心服务不应分配 `profiles`，以便它们始终启用并自动启动。

## 启动特定配置集

要启动特定配置集，请提供 `--profile` [命令行选项](/reference/cli/docker/compose.md) 或使用 [`COMPOSE_PROFILES` 环境变量](environment-variables/envvars.md#compose_profiles)：

```console
$ docker compose --profile debug up
```
```console
$ COMPOSE_PROFILES=debug docker compose up
```

这两个命令都会启动启用了 `debug` 配置集的服务。在前面的 `compose.yaml` 文件中，这将启动 `db`、`backend` 和 `phpmyadmin` 服务。

### 启动多个配置集

您也可以启用多个配置集，例如使用 `docker compose --profile frontend --profile debug up` 将启用 `frontend` 和 `debug` 配置集。

可以通过传递多个 `--profile` 标志或为 `COMPOSE_PROFILES` 环境变量提供逗号分隔的列表来指定多个配置集：

```console
$ docker compose --profile frontend --profile debug up
```

```console
$ COMPOSE_PROFILES=frontend,debug docker compose up
```

如果要同时启用所有配置集，可以运行 `docker compose --profile "*"`。

## 自动启动配置集和依赖解析

当您在命令行中明确指定一个分配了一个或多个配置集的服务时，您不需要手动启用配置集，因为 Compose 会运行该服务，无论其配置集是否已激活。这对于运行一次性服务或调试工具非常有用。

只启动目标服务（及其通过 `depends_on` 声明的任何依赖项）。共享相同配置集的其他服务不会启动，除非：
- 它们也被明确指定，或者
- 使用 `--profile` 或 `COMPOSE_PROFILES` 显式启用了配置集。

当在命令行中明确指定分配了 `profiles` 的服务时，其配置集会自动启动，因此您无需手动启动它们。这可用于一次性服务和调试工具。
例如，考虑以下配置：

```yaml
services:
  backend:
    image: backend

  db:
    image: mysql

  db-migrations:
    image: backend
    command: myapp migrate
    depends_on:
      - db
    profiles:
      - tools
```

```sh
# 仅启动 backend 和 db（不涉及配置集）
$ docker compose up -d

# 运行 db-migrations 服务，无需手动启用 'tools' 配置集
$ docker compose run db-migrations
```

在此示例中，即使 `db-migrations` 被分配到 tools 配置集，它也会运行，因为它被明确指定。`db` 服务也会自动启动，因为它被列在 `depends_on` 中。

如果目标服务的依赖项也受配置集限制，您必须确保这些依赖项满足以下条件之一：
 - 位于同一配置集中
 - 单独启动
 - 未分配给任何配置集，因此始终启用

## 停止应用程序和具有特定配置集的服务

与启动特定配置集类似，您可以使用 `--profile` [命令行选项](/reference/cli/docker/compose.md#use--p-to-specify-a-project-name) 或使用 [`COMPOSE_PROFILES` 环境变量](environment-variables/envvars.md#compose_profiles)：

```console
$ docker compose --profile debug down
```
```console
$ COMPOSE_PROFILES=debug docker compose down
```

这两个命令都会停止并移除具有 `debug` 配置集的服务以及没有配置集的服务。在以下 `compose.yaml` 文件中，这将停止 `db`、`backend` 和 `phpmyadmin` 服务。

```yaml
services:
  frontend:
    image: frontend
    profiles: [frontend]

  phpmyadmin:
    image: phpmyadmin
    depends_on: [db]
    profiles: [debug]

  backend:
    image: backend

  db:
    image: mysql
```

如果您只想停止 `phpmyadmin` 服务，可以运行

```console 
$ docker compose down phpmyadmin
``` 
或 
```console 
$ docker compose stop phpmyadmin
```

> [!NOTE]
>
> 运行 `docker compose down` 只会停止 `backend` 和 `db`。

## 参考信息

[`profiles`](/reference/compose-file/services.md#profiles)
