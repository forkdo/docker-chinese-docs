---
title: 在开发环境中启动时使用架构和数据预填充数据库
linktitle: 预填充数据库  
description: &desc 在开发环境中启动时使用架构和数据预填充数据库
keywords: 预填充, 数据库, postgres, 容器支持的开发
summary: *desc
tags: [app-dev, databases]
params:
  time: 20 分钟
---

在本地开发过程中，使用必要的数据和架构预填充数据库是增强开发和测试工作流的常见做法。通过模拟真实场景，这种做法有助于及早发现前端问题，确保数据库管理员和软件工程师之间的协调一致，并促进更顺畅的协作。预填充提供了诸如自信部署、跨环境一致性以及及早发现问题等好处，最终改进了整个开发过程。

在本指南中，您将学习如何：

- 使用 Docker 启动 Postgres 容器
- 使用 SQL 脚本预填充 Postgres
- 通过将 SQL 文件复制到 Docker 镜像中来预填充 Postgres
- 使用 JavaScript 代码预填充 Postgres

## 使用 Docker 运行 Postgres

[Postgres 的官方 Docker 镜像](https://hub.docker.com/_/postgres) 提供了一种在开发机器上运行 Postgres 数据库的便捷方式。Postgres Docker 镜像是一个预配置的环境，封装了 PostgreSQL 数据库系统。它是一个独立的单元，可以在 Docker 容器中运行。使用此镜像，您可以快速轻松地设置 Postgres 实例，而无需手动配置。

## 先决条件

要遵循本操作指南，需要满足以下先决条件：

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)

## 启动 Postgres

通过以下步骤启动一个快速的 Postgres 演示：

1. 打开终端并运行以下命令来启动 Postgres 容器。

   此示例将启动一个 Postgres 容器，并将端口 `5432` 暴露给主机，以便本机运行的应用程序可以使用密码 `mysecretpassword` 连接到它。

   ```console
   $ docker run -d --name postgres -p 5432:5432 -e POSTGRES_PASSWORD=mysecretpassword postgres
   ```

2. 通过选择容器并在 Docker 仪表板上检查日志来验证 Postgres 是否已启动并正在运行。

   ```plaintext
   PostgreSQL Database directory appears to contain a database; Skipping initialization
 
   2024-09-08 09:09:47.136 UTC [1] LOG:  starting PostgreSQL 16.4 (Debian 16.4-1.pgdg120+1) on aarch64-unknown-linux-gnu, compiled by gcc (Debian 12.2.0-14) 12.2.0, 64-bit
   2024-09-08 09:09:47.137 UTC [1] LOG:  listening on IPv4 address "0.0.0.0", port 5432
   2024-09-08 09:09:47.137 UTC [1] LOG:  listening on IPv6 address "::", port 5432
   2024-09-08 09:09:47.139 UTC [1] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
   2024-09-08 09:09:47.142 UTC [29] LOG:  database system was shut down at 2024-09-08 09:07:09 UTC
   2024-09-08 09:09:47.148 UTC [1] LOG:  database system is ready to accept connections
   ```

3. 从本地系统连接到 Postgres。

   `psql` 是 PostgreSQL 交互式 shell，用于连接到 Postgres 数据库并让您开始执行 SQL 命令。假设您已经在本地系统上安装了 `psql` 实用程序，现在是时候连接到 Postgres 数据库了。在本地终端上运行以下命令：

   ```console
   $ docker exec -it postgres psql -h localhost -U postgres
   ```

   您现在可以在 `psql` 提示符下执行任何所需的 SQL 查询或命令。

   使用 `\q` 或 `\quit` 退出 Postgres 交互式 shell。

## 使用 SQL 脚本预填充 Postgres 数据库

现在您已经熟悉了 Postgres，是时候看看如何使用示例数据对其进行预填充了。在此演示中，您将首先创建一个包含 SQL 命令的脚本。该脚本定义了数据库和表结构，并插入示例数据。然后您将连接数据库以验证数据。

假设您已经有一个正在运行的现有 Postgres 数据库实例，请按照以下步骤填充数据库。

1. 创建一个名为 `seed.sql` 的空文件，并添加以下内容。

   ```sql
   CREATE DATABASE sampledb;

   \c sampledb

   CREATE TABLE users (
     id SERIAL PRIMARY KEY,
     name VARCHAR(50),
     email VARCHAR(100) UNIQUE
   );

   INSERT INTO users (name, email) VALUES
     ('Alpha', 'alpha@example.com'),
     ('Beta', 'beta@example.com'),
     ('Gamma', 'gamma@example.com');  
   ```

   SQL 脚本创建一个名为 `sampledb` 的新数据库，连接到它，并创建一个 `users` 表。该表包括一个自动递增的 `id` 作为主键，一个最大长度为 50 个字符的 `name` 字段，以及一个唯一的、最多 100 个字符的 `email` 字段。

   创建表后，`INSERT` 命令将三个用户插入到 `users` 表中，并附上他们各自的姓名和电子邮件。此设置形成了一个基本的数据库结构，用于存储具有唯一电子邮件地址的用户信息。

2. 填充数据库。

   现在是时候使用 `<` 运算符将 `seed.sql` 的内容直接输入数据库了。该命令用于针对名为 `sampledb` 的 Postgres 数据库执行名为 `seed.sql` 的 SQL 脚本。

   ```console
   $ cat seed.sql | docker exec -i postgres psql -h localhost -U postgres -f-
   ```

   查询执行后，您将看到以下结果：

   ```plaintext
   CREATE DATABASE
   You are now connected to database "sampledb" as user "postgres".
   CREATE TABLE
   INSERT 0 3
   ```

3. 运行以下 `psql` 命令，验证名为 users 的表是否已在 `sampledb` 数据库中填充。

   ```console
   $ docker exec -it postgres psql -h localhost -U postgres sampledb
   ```

   您现在可以在 `psql` shell 中运行 `\l` 来列出 Postgres 服务器上的所有数据库。

   ```console
   sampledb=# \l
                                                List of databases
   Name    |  Owner   | Encoding |  Collate   |   Ctype    | ICU Locale | Locale Provider |   Access privileges
   -----------+----------+----------+------------+------------+------------+-----------------+-----------------------
   postgres  | postgres | UTF8     | en_US.utf8 | en_US.utf8 |            | libc            |
   sampledb  | postgres | UTF8     | en_US.utf8 | en_US.utf8 |            | libc            |
   template0 | postgres | UTF8     | en_US.utf8 | en_US.utf8 |            | libc            | =c/postgres          +
             |          |          |            |            |            |                 | postgres=CTc/postgres
   template1 | postgres | UTF8     | en_US.utf8 | en_US.utf8 |            | libc            | =c/postgres          +
             |          |          |            |            |            |                 | postgres=CTc/postgres
   (4 rows)
   ```

   要从 users 表中检索所有数据，请输入以下查询：

   ```console
   sampledb=# SELECT * FROM users;
   id | name  |       email
   ----+-------+-------------------
    1 | Alpha | alpha@example.com
    2 | Beta  | beta@example.com
    3 | Gamma | gamma@example.com
   (3 rows)
   ```
  
   使用 `\q` 或 `\quit` 退出 Postgres 交互式 shell。

## 通过绑定挂载 SQL 脚本预填充数据库

在 Docker 中，挂载指的是使来自主机系统的文件或目录在容器内可访问。这使您能够在主机和容器之间共享数据或配置文件，从而实现更大的灵活性和持久性。

现在您已经学习了如何启动 Postgres 并使用 SQL 脚本预填充数据库，接下来学习如何将 SQL 文件直接挂载到 Postgres 容器的初始化目录 (`/docker-entrypoint-initdb.d`) 中。`/docker-entrypoint-initdb.d` 是 PostgreSQL Docker 容器中的一个特殊目录，用于在容器首次启动时初始化数据库。

在执行以下步骤之前，请确保停止任何正在运行的 Postgres 容器（以及卷），以防止端口冲突：

```console
$ docker container stop postgres
```

1. 使用以下条目修改 `seed.sql`：

   ```sql
   CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    email VARCHAR(100) UNIQUE
   );

   INSERT INTO users (name, email) VALUES
    ('Alpha', 'alpha@example.com'),
    ('Beta', 'beta@example.com'),
    ('Gamma', 'gamma@example.com')
   ON CONFLICT (email) DO NOTHING;
   ```
   
2. 创建一个名为 `Dockerfile` 的文本文件并复制以下内容。

   ```plaintext
   # syntax=docker/dockerfile:1
   FROM postgres:18
   COPY seed.sql /docker-entrypoint-initdb.d/
   ```

   此 Dockerfile 将 `seed.sql` 脚本直接复制到 PostgreSQL 容器的初始化目录中。
   

3. 使用 Docker Compose。
   
   使用 Docker Compose 可以更轻松地管理和部署带有预填充数据库的 PostgreSQL 容器。此 compose.yml 文件定义了一个名为 `db` 的 Postgres 服务，使用最新的 Postgres 镜像，该镜像设置了一个名为 `sampledb` 的数据库，以及一个用户 `postgres` 和密码 `mysecretpassword`。

   ```yaml
   services:
     db:
       build:
         context: .
         dockerfile: Dockerfile
       container_name: my_postgres_db
       environment:
         POSTGRES_USER: postgres
         POSTGRES_PASSWORD: mysecretpassword
         POSTGRES_DB: sampledb
       ports:
         - "5432:5432"
       volumes:
         - data_sql:/var/lib/postgresql   # 持久化数据存储

   volumes:
     data_sql:
    ```
  
    它将主机上的端口 `5432` 映射到容器的 `5432`，让您可以从容器外部访问 Postgres 数据库。它还定义了 `data_sql` 用于持久化数据库数据，确保在容器停止时数据不会丢失。

    需要注意的是，到主机的端口映射仅在您想从非容器化程序连接到数据库时才需要。如果您将连接到 DB 的服务容器化，则应通过自定义桥接网络连接到数据库。

4. 启动 Compose 服务。

    假设您已将 `seed.sql` 文件与 Dockerfile 放在同一目录中，请执行以下命令：

    ```console
    $ docker compose up -d --build
    ```

5. 现在是时候验证 `users` 表是否已填充数据了。

    ```console
    $ docker exec -it my_postgres_db psql -h localhost -U postgres sampledb
    ```

    ```sql 
    sampledb=# SELECT * FROM users;
      id | name  |       email
    ----+-------+-------------------
       1 | Alpha | alpha@example.com
       2 | Beta  | beta@example.com
       3 | Gamma | gamma@example.com
     (3 rows)

    sampledb=#
    ```


## 使用 JavaScript 代码预填充数据库


现在您已经学习了如何使用各种方法（如 SQL 脚本、挂载卷等）填充数据库，是时候尝试使用 JavaScript 代码来实现它了。

1. 创建一个包含以下内容的 .env 文件：

   ```plaintext
   POSTGRES_USER=postgres
   POSTGRES_DB_HOST=localhost
   POSTGRES_DB=sampledb
   POSTGRES_PASSWORD=mysecretpassword
   POSTGRES_PORT=5432
   ```

2. 创建一个名为 seed.js 的新 JavaScript 文件，内容如下：

   以下 JavaScript 代码导入 `dotenv` 包，该包用于从 `.env` 文件加载环境变量。`.config()` 方法读取 `.env` 文件并将环境变量设置为 `process.env` 对象的属性。这使您能够安全地将数据库凭据等敏感信息存储在代码之外。

   然后，它从 pg 库创建一个新的 Pool 实例，该实例为高效的数据库交互提供连接池。定义了 `seedData` 函数来执行数据库填充操作。
   它在脚本末尾被调用以启动填充过程。使用 try...catch...finally 块进行错误处理。

   ```plaintext
   require('dotenv').config();  // 从 .env 文件加载环境变量
   const { Pool } = require('pg');

   // 使用环境变量创建一个新的池
   const pool = new Pool({
     user: process.env.POSTGRES_USER,
     host: process.env.POSTGRES_DB_HOST,
     database: process.env.POSTGRES_DB,
     port: process.env.POSTGRES_PORT,
     password: process.env.POSTGRES_PASSWORD,
   });

   const seedData = async () => {
     try {
        // 如果表已存在则删除（可选）
        await pool.query(`DROP TABLE IF EXISTS todos;`);

        // 使用正确的结构创建表
        await pool.query(`
          CREATE TABLE todos (
            id SERIAL PRIMARY KEY,
            task VARCHAR(255) NOT NULL,
            completed BOOLEAN DEFAULT false
              );
        `   );

        // 插入种子数据
        await pool.query(`
          INSERT INTO todos (task, completed) VALUES
          ('Watch netflix', false),
          ('Finish podcast', false),
          ('Pick up kid', false);
          `);
          console.log('Database seeded successfully!');
        } catch (err) {
          console.error('Error seeding the database', err);
        } finally {
          pool.end();
       }
     };

     // 调用 seedData 函数运行脚本
     seedData();
     ```

3. 启动填充过程

    ```console
    $ node seed.js
    ```

    您应该看到以下命令：

    ```plaintext
    Database seeded successfully!
    ```

4. 验证数据库是否正确填充：

    ```console
    $ docker exec -it postgres psql -h localhost -U postgres sampledb
    ```

    ```console
    sampledb=# SELECT * FROM todos;
    id |      task      | completed
    ----+----------------+-----------
    1 | Watch netflix  | f
    2 | Finish podcast | f
    3 | Pick up kid    | f
    (3 rows)  
    ```

## 总结

在启动时使用架构和数据预填充数据库对于创建一致且真实的测试环境至关重要，这有助于在开发早期发现问题并协调前端和后端工作。本指南使您掌握了使用各种方法实现预填充的知识和实践步骤，包括 SQL 脚本、Docker 集成和 JavaScript 代码。