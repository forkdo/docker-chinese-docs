---
description: 使用 pgAdmin 可视化您的 PostgreSQL 数据库
keywords: pgadmin, container-supported development
title: 使用 pgAdmin 可视化您的 PostgreSQL 数据库
linktitle: 使用 pgAdmin 可视化您的 PostgreSQL 数据库
summary: |
  探索如何将 pgAdmin 添加到您的开发堆栈中，并尽可能让您的队友轻松浏览 PostgreSQL 数据库。
tags: [databases]
params:
  time: 10 minutes
---

许多应用程序在应用堆栈中使用 PostgreSQL 数据库。然而，并非所有开发人员都精通导航和操作 PostgreSQL 数据库。

幸运的是，当您在开发中使用容器时，可以轻松添加额外的服务来帮助进行故障排除和调试。

[pgAdmin](https://www.pgadmin.org/) 工具是一个流行的开源工具，旨在帮助管理和可视化 PostgreSQL 数据库。

在本指南中，您将学习如何：

1. 将 pgAdmin 添加到您的应用堆栈中
2. 配置 pgAdmin 以自动连接到开发数据库



## 将 pgAdmin 添加到您的堆栈

1. 在您的 `compose.yaml` 文件中，在现有的 `postgres` 服务旁边添加 `pgadmin` 服务：

    ```yaml
    services:
      postgres:
        image: postgres:18
        environment:
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: secret
          POSTGRES_DB: demo

      pgadmin:
        image: dpage/pgadmin4:9.8
        ports:
          - 5050:80
        environment:
          # pgAdmin 所需
          PGADMIN_DEFAULT_EMAIL: demo@example.com
          PGADMIN_DEFAULT_PASSWORD: secret

          # 不要求用户登录
          PGADMIN_CONFIG_SERVER_MODE: 'False'

          # 登录后不需要“主”密码
          PGADMIN_CONFIG_MASTER_PASSWORD_REQUIRED: 'False'
    ```

2. 使用以下命令启动 Compose 堆栈：

    ```console
    $ docker compose up
    ```

    镜像下载并启动容器后，您将看到类似以下的输出，表明 pgAdmin 已准备就绪：

    ```console
    pgadmin-1   | [2025-09-22 15:52:47 +0000] [1] [INFO] Starting gunicorn 23.0.0
    pgadmin-1   | [2025-09-22 15:52:47 +0000] [1] [INFO] Listening at: http://[::]:80 (1)
    pgadmin-1   | [2025-09-22 15:52:47 +0000] [1] [INFO] Using worker: gthread
    pgadmin-1   | [2025-09-22 15:52:47 +0000] [119] [INFO] Booting worker with pid: 119
    ```

3. 访问 http://localhost:5050 打开 pgAdmin。

4. 进入管理面板后，选择 **Add New Server** 链接以定义新服务器。输入以下详细信息：

    - **General** 选项卡：
        - **Name**: `postgres`
    - **Connection** 选项卡：
        - **Host name/address**: `postgres`
        - **Username**: `postgres`
        - **Password**: `secret`
        - 启用 **Save password?** 字段

    > [!IMPORTANT]
    >
    > 这些连接详细信息假设您使用的是前面的 Compose 文件片段。如果您使用现有的 Compose 文件，请根据需要调整连接详细信息。**Host name/address** 字段应与您的 postgres 服务名称匹配。

5. 选择 **Save** 按钮创建新数据库。

您现在已设置好 pgAdmin 并连接到您的容器化数据库。可以随意浏览、查看表并探索您的数据库。



## 配置 pgAdmin 以自动连接到数据库

虽然您已经运行了 pgAdmin，但如果能直接打开应用程序而无需配置数据库连接会更好。减少设置步骤是让队友更容易从此工具中获益的好方法。

幸运的是，有一种自动连接到数据库的方法。

> [!WARNING]
>
> 为了实现自动连接，数据库凭证是使用纯文本文件共享的。在本地开发期间，这通常是可接受的，因为本地数据不是真实的客户数据。
> 但是，如果您使用的是生产数据或敏感数据，则强烈不建议这种做法。

1. 首先，您需要定义服务器本身，pgAdmin 使用 `servers.json` 文件来完成此操作。

    将以下内容添加到您的 `compose.yaml` 文件中，以定义 `servers.json` 文件的配置文件：

    ```yaml
    configs:
      pgadmin-servers:
        content: |
          {
            "Servers": {
              "1": {
                "Name": "Local Postgres",
                "Group": "Servers",
                "Host": "postgres",
                "Port": 5432,
                "MaintenanceDB": "postgres",
                "Username": "postgres",
                "PassFile": "/config/pgpass"
              }
            }
          }
    ```

2. `servers.json` 文件定义了一个 `PassFile` 字段，该字段引用了 [postgreSQL 密码文件](https://www.postgresql.org/docs/current/libpq-pgpass.html)。这些通常被称为 pgpass 文件。

    将以下配置添加到您的 `compose.yaml` 文件中以定义 pgpass 文件：

    ```yaml
    config:
      pgadmin-pgpass:
        content: |
          postgres:5432:*:postgres:secret
    ```

    这将指示任何连接到 `postgres:5432` 且使用用户名 `postgres` 的请求都应提供密码 `secret`。

3. 在您的 `compose.yaml` 中，更新 `pgadmin` 服务以注入配置文件：

    ```yaml
    services:
      pgadmin:
        ...
        configs:
          - source: pgadmin-pgpass
            target: /config/pgpass
            uid: "5050"
            gid: "5050"
            mode: 0400
          - source: pgadmin-servers
            target: /pgadmin4/servers.json
            mode: 0444
    ```

4. 通过再次运行 `docker compose up` 更新应用堆栈：

    ```console
    $ docker compose up
    ```

5. 应用程序重新启动后，在浏览器中打开 http://localhost:5050。您应该无需任何登录或配置即可访问数据库。


## 结论

使用容器不仅可以轻松运行应用程序的依赖项，还可以轻松运行有助于故障排除和调试的附加工具。

在添加工具时，请考虑队友可能遇到的体验和潜在障碍，以及如何消除这些障碍。在这种情况下，您能够采取额外的步骤来添加配置，以自动配置和连接数据库，从而为队友节省宝贵的时间。