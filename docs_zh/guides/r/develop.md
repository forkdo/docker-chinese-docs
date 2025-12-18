---
title: 使用容器进行 R 开发
linkTitle: 开发你的应用
weight: 20
keywords: R, 本地, 开发
description: 了解如何在本地开发你的 R 应用。
aliases:
  - /language/r/develop/
  - /guides/language/r/develop/
---

## 前置条件

完成 [容器化 R 应用](containerize.md)。

## 概述

在本节中，你将学习如何为你的容器化应用设置开发环境。这包括：

- 添加本地数据库并持久化数据
- 配置 Compose，使你在编辑和保存代码时自动更新正在运行的 Compose 服务

## 获取示例应用

你需要克隆一个新的仓库，以获取包含连接数据库逻辑的示例应用。

切换到你想克隆仓库的目录，运行以下命令。

```console
$ git clone https://github.com/mfranzon/r-docker-dev.git
```

## 配置应用使用数据库

要测试 Shiny 应用与本地数据库的连接，你需要修改 `Dockerfile`，更改 `COPY` 指令：

```diff
-COPY src/ .
+COPY src_db/ .
```

## 添加本地数据库并持久化数据

你可以使用容器设置本地服务，比如数据库。在本节中，你将更新 `compose.yaml` 文件，定义数据库服务和持久化数据的卷。

在克隆的仓库目录中，使用 IDE 或文本编辑器打开 `compose.yaml` 文件。

在 `compose.yaml` 文件中，你需要取消注释配置数据库的属性。你还必须挂载数据库密码文件，并在 `shiny-app` 服务上设置环境变量，指向容器中文件的位置。

以下是更新后的 `compose.yaml` 文件。

```yaml
services:
  shiny-app:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - 3838:3838
    environment:
      - POSTGRES_PASSWORD_FILE=/run/secrets/db-password
    depends_on:
      db:
        condition: service_healthy
    secrets:
      - db-password
  db:
    image: postgres:18
    restart: always
    user: postgres
    secrets:
      - db-password
    volumes:
      - db-data:/var/lib/postgresql
    environment:
      - POSTGRES_DB=example
      - POSTGRES_PASSWORD_FILE=/run/secrets/db-password
    expose:
      - 5432
    healthcheck:
      test: ["CMD", "pg_isready"]
      interval: 10s
      timeout: 5s
      retries: 5
volumes:
  db-data:
secrets:
  db-password:
    file: db/password.txt
```

> [!NOTE]
>
> 要了解 Compose 文件中指令的更多信息，请参阅 [Compose 文件参考](/reference/compose-file/)。

在使用 Compose 运行应用之前，请注意此 Compose 文件指定使用 `password.txt` 文件存储数据库密码。你必须创建此文件，因为它不包含在源仓库中。

在克隆的仓库目录中，创建一个名为 `db` 的新目录，并在该目录内创建一个名为 `password.txt` 的文件，用于存储数据库密码。使用你喜欢的 IDE 或文本编辑器，将以下内容添加到 `password.txt` 文件中。

```text
mysecretpassword
```

保存并关闭 `password.txt` 文件。

现在你的 `r-docker-dev` 目录中应包含以下内容。

```text
├── r-docker-dev/
│ ├── db/
│ │ └── password.txt
│ ├── src/
│ │ └── app.R
│ ├── src_db/
│ │ └── app_db.R
│ ├── requirements.txt
│ ├── .dockerignore
│ ├── compose.yaml
│ ├── Dockerfile
│ ├── README.Docker.md
│ └── README.md
```

现在，运行以下 `docker compose up` 命令启动你的应用。

```console
$ docker compose up --build
```

现在通过在浏览器中打开以下地址测试你的数据库连接：

```console
http://localhost:3838
```

你应该看到一个弹窗消息：

```text
DB CONNECTED
```

在终端中按 `ctrl+c` 停止你的应用。

## 自动更新服务

使用 Compose Watch 在你编辑和保存代码时自动更新正在运行的 Compose 服务。有关 Compose Watch 的更多详细信息，请参阅 [使用 Compose Watch](/manuals/compose/how-tos/file-watch.md)。

`compose.yaml` 文件中的第 15 到 18 行包含触发 Docker 在当前工作目录中的文件更改时重建镜像的属性：

```yaml {hl_lines="15-18",linenos=true}
services:
  shiny-app:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - 3838:3838
    environment:
      - POSTGRES_PASSWORD_FILE=/run/secrets/db-password
    depends_on:
      db:
        condition: service_healthy
    secrets:
      - db-password
    develop:
      watch:
        - action: rebuild
          path: .
  db:
    image: postgres:18
    restart: always
    user: postgres
    secrets:
      - db-password
    volumes:
      - db-data:/var/lib/postgresql
    environment:
      - POSTGRES_DB=example
      - POSTGRES_PASSWORD_FILE=/run/secrets/db-password
    expose:
      - 5432
    healthcheck:
      test: ["CMD", "pg_isready"]
      interval: 10s
      timeout: 5s
      retries: 5
volumes:
  db-data:
secrets:
  db-password:
    file: db/password.txt
```

运行以下命令，使用 Compose Watch 运行你的应用。

```console
$ docker compose watch
```

现在，如果你修改 `app.R`，你将实时看到更改，而无需重建镜像！

在终端中按 `ctrl+c` 停止你的应用。

## 总结

在本节中，你了解了如何设置 Compose 文件以添加本地数据库并持久化数据。你还学习了如何使用 Compose Watch 在更新代码时自动重建和运行容器。

相关信息：

- [Compose 文件参考](/reference/compose-file/)
- [Compose 文件监视](/manuals/compose/how-tos/file-watch.md)
- [多阶段构建](/manuals/build/building/multi-stage.md)

## 下一步

在下一节中，你将了解如何使用 GitHub Actions 设置 CI/CD 流水线。