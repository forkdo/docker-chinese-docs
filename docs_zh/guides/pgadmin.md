---
description: 使用 pgAdmin 可视化你的 PostgreSQL 数据库
keywords: pgadmin, container-supported development
title: 使用 pgAdmin 可视化你的 PostgreSQL 数据库
linktitle: 使用 pgAdmin 可视化你的 PostgreSQL 数据库
summary: |
  探索如何将 pgAdmin 添加到你的开发栈中，让你的团队成员能够更轻松地浏览和管理 PostgreSQL 数据库。
tags: [databases]
params:
  time: 10 minutes
---

许多应用程序在其技术栈中使用 PostgreSQL 数据库。然而，并非所有开发者都熟悉如何导航和操作 PostgreSQL 数据库。

幸运的是，当你在开发中使用容器时，可以轻松添加额外的服务来辅助故障排查和调试工作。

[pgAdmin](https://www.pgadmin.org/) 是一个流行的开源工具，专为管理和可视化 PostgreSQL 数据库而设计。

在本指南中，你将学习如何：

1. 将 pgAdmin 添加到你的应用栈中
2. 配置 pgAdmin 以自动连接到开发数据库



## 将 pgAdmin 添加到你的栈中

1. 在你的 `compose.yaml` 文件中，将 `pgadmin` 服务添加到现有的 `postgres` 服务旁边：

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

          # 登录后不需要“主密码”
          PGADMIN_CONFIG_MASTER_PASSWORD_REQUIRED: 'False'
    ```

2. 使用以下命令启动 Compose 栈：

    ```console
    $ docker compose up
    ```

    图像下载完成后，容器启动，你会看到类似以下的输出，表明 pgAdmin 已准备就绪：

    ```console
    pgadmin-1   | [2025-09-22 15:52:47 +0000] [1] [INFO] Starting gunicorn 23.0.0
    pgadmin-1   | [2025-09-22 15:52:47 +0000] [1] [INFO] Listening at: http://[::]:80 (1)
    pgadmin-1   | [2025-09-22 15:52:47 +0000] [1] [INFO] Using worker: gthread
    pgadmin-1   | [2025-09-22 15:52:47 +0000] [119] [INFO] Booting worker with pid: 119
    ```

3. 通过访问 http://localhost:5050 打开 pgAdmin。

4. 进入管理面板后，选择 **Add New Server** 链接来定义新服务器。输入以下详细信息：

    - **General** 选项卡：
        - **Name**: `postgres`
    - **Connection** 选项卡：
        - **Host name/address**: `postgres`
        - **Username**: `postgres`
        - **Password**: `secret`
        - 启用 **Save password?** 字段

    > [!IMPORTANT]
    >
    > 这些连接详细信息假设你使用的是前面的 Compose 文件片段。如果你使用的是现有的 Compose 文件，
    > 请根据需要调整连接详细信息。**Host name/address** 字段应与你的 postgres 服务名称匹配。

5. 选择 **Save** 按钮创建新数据库。

现在你已经设置好了 pgAdmin 并连接到你的容器化数据库。可以随意浏览、查看表并探索你的数据库。



## 配置 pgAdmin 自动连接到数据库

虽然你已经运行了 pgAdmin，但如果能直接打开应用而无需配置数据库连接就更好了。减少设置步骤是让团队成员更轻松地使用此工具的好方法。

幸运的是，pgAdmin 支持自动连接到数据库。

> [!WARNING]
    >
    > 为了实现自动连接，数据库凭据会通过明文文件共享。在本地开发中，这通常是可接受的，因为本地数据不是真实的客户数据。
    > 但是，如果你使用的是生产环境或敏感数据，强烈不建议这样做。

1. 首先，你需要定义 pgAdmin 使用 `servers.json` 文件来定义服务器。

    在你的 `compose.yaml` 文件中添加以下内容，为 `servers.json` 文件定义配置：

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

2. `servers.json` 文件定义了一个 `PassFile` 字段，它引用了 [PostgreSQL 密码文件](https://www.postgresql.org/docs/current/libpq-pgpass.html)。这些文件通常被称为 pgpass 文件。

    在你的 `compose.yaml` 文件中添加以下配置来定义 pgpass 文件：

    ```yaml
    config:
      pgadmin-pgpass:
        content: |
          postgres:5432:*:postgres:secret
    ```

    这表示任何连接到 `postgres:5432` 且使用用户名 `postgres` 的请求都应提供密码 `secret`。

3. 在你的 `compose.yaml` 中，更新 `pgadmin` 服务以注入配置文件：

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

4. 通过再次运行 `docker compose up` 更新应用栈：

    ```console
    $ docker compose up
    ```

5. 应用重启后，打开浏览器访问 http://localhost:5050。你应该无需登录或配置即可访问数据库。


## 结论

使用容器不仅便于运行应用程序的依赖项，还便于添加额外的工具来辅助故障排查和调试。

当你添加工具时，思考一下你的团队成员可能遇到的体验和摩擦，以及如何消除这些障碍。在本例中，你通过添加配置实现了数据库的自动配置和连接，为团队成员节省了宝贵的时间。