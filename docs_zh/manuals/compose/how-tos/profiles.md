---
title: 使用 Compose 配置文件
linkTitle: 使用服务配置文件
weight: 20
description: 如何在 Docker Compose 中使用配置文件
keywords: cli, compose, profile, profiles 参考
aliases:
- /compose/profiles/
---

{{% include "compose/profiles.md" %}}

## 为服务分配配置文件

服务通过 [`profiles` 属性](/reference/compose-file/services.md#profiles) 与配置文件关联，该属性接收一个配置文件名称数组：

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

在此示例中，服务 `frontend` 和 `phpmyadmin` 分别被分配到 `frontend` 和 `debug` 配置文件，因此只有在启用相应配置文件时才会启动。

没有 `profiles` 属性的服务始终启用。在此情况下，运行 `docker compose up` 将仅启动 `backend` 和 `db` 服务。

有效的配置文件名称遵循正则表达式格式 `[a-zA-Z0-9][a-zA-Z0-9_.-]+`。

> [!TIP]
>
> 您应用程序的核心服务不应分配 `profiles`，以便它们始终启用并自动启动。

## 启动特定配置文件

要启动特定配置文件，请提供 `--profile` [命令行选项](/reference/cli/docker/compose.md) 或使用 [`COMPOSE_PROFILES` 环境变量](environment-variables/envvars.md#compose_profiles)：

```console
$ docker compose --profile debug up
```
```console
$ COMPOSE_PROFILES=debug docker compose up
```

这两个命令都会启用 `debug` 配置文件启动服务。在前面的 `compose.yaml` 文件中，这将启动服务 `db`、`backend` 和 `phpmyadmin`。

### 启动多个配置文件

您也可以启用多个配置文件，例如使用 `docker compose --profile frontend --profile debug up` 将启用 `frontend` 和 `debug` 配置文件。

可以通过传递多个 `--profile` 标志或为 `COMPOSE_PROFILES` 环境变量提供逗号分隔列表来指定多个配置文件：

```console
$ docker compose --profile frontend --profile debug up
```

```console
$ COMPOSE_PROFILES=frontend,debug docker compose up
```

如果您想同时启用所有配置文件，可以运行 `docker compose --profile "*"`。

## 自动启动配置文件和依赖解析

当您在命令行上明确指定一个服务，而该服务分配有一个或多个配置文件时，您无需手动启用配置文件，因为 Compose 会运行该服务，无论其配置文件是否已激活。这对于运行一次性服务或调试工具很有用。

只有被指定的服务（及其通过 `depends_on` 声明的依赖项）会被启动。与该服务共享相同配置文件的其他服务不会启动，除非：
- 它们也被明确指定，或
- 使用 `--profile` 或 `COMPOSE_PROFILES` 明确启用配置文件。

当分配了 `profiles` 的服务在命令行上被明确指定时，其配置文件会自动启动，因此您无需手动启动它们。这可用于一次性服务和调试工具。例如，考虑以下配置：

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
# 仅启动 backend 和 db（不涉及配置文件）
$ docker compose up -d

# 运行 db-migrations 服务，无需手动启用 'tools' 配置文件
$ docker compose run db-migrations
```

在此示例中，即使 `db-migrations` 被分配到 tools 配置文件，它也会运行，因为它是被明确指定的。`db` 服务也会自动启动，因为它在 `depends_on` 中列出。

如果被指定的服务有依赖项，而这些依赖项也受配置文件限制，您必须确保这些依赖项要么：
- 在同一配置文件中
- 单独启动
- 未分配到任何配置文件，因此始终启用

## 停止应用程序和具有特定配置文件的服务

与启动特定配置文件一样，您可以使用 `--profile` [命令行选项](/reference/cli/docker/compose.md#use--p-to-specify-a-project-name) 或使用 [`COMPOSE_PROFILES` 环境变量](environment-variables/envvars.md#compose_profiles)：

```console
$ docker compose --profile debug down
```
```console
$ COMPOSE_PROFILES=debug docker compose down
```

这两个命令都会停止并移除具有 `debug` 配置文件以及没有配置文件的服务。在以下 `compose.yaml` 文件中，这将停止服务 `db`、`backend` 和 `phpmyadmin`。

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

如果您只想停止 `phpmyadmin` 服务，可以运行：

```console 
$ docker compose down phpmyadmin
``` 
或
```console 
$ docker compose stop phpmyadmin
```

> [!NOTE]
>
> 运行 `docker compose down` 仅停止 `backend` 和 `db`。

## 参考信息

[`profiles`](/reference/compose-file/services.md#profiles)