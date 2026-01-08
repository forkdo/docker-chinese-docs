---
title: 使用容器进行 R 开发
linkTitle: 开发应用
weight: 20
keywords: R, local, development
description: 了解如何在本地开发 R 应用程序。
aliases:
- /language/r/develop/
- /guides/language/r/develop/
---

## 先决条件

完成 [容器化 R 应用程序](containerize.md)。

## 概述

在本节中，您将学习如何为容器化应用程序设置开发环境。这包括：

- 添加本地数据库并持久化数据
- 配置 Compose，以便在您编辑并保存代码时自动更新正在运行的 Compose 服务

## 获取示例应用程序

您需要克隆一个新仓库以获取包含连接数据库逻辑的示例应用程序。

切换到您想要克隆仓库的目录，然后运行以下命令。

```console
$ git clone https://github.com/mfranzon/r-docker-dev.git
```

## 配置应用程序以使用数据库

要尝试 Shiny 应用程序与本地数据库之间的连接，您必须修改 `Dockerfile`，更改 `COPY` 指令：

```diff
-COPY src/ .
+COPY src_db/ .
```

## 添加本地数据库并持久化数据

您可以使用容器来设置本地服务，例如数据库。在本节中，您将更新 `compose.yaml` 文件以定义数据库服务和用于持久化数据的卷。

在克隆的仓库目录中，使用 IDE 或文本编辑器打开 `compose.yaml` 文件。

在 `compose.yaml` 文件中，您需要取消注释用于配置数据库的属性。您还必须挂载数据库密码文件，并在 `shiny-app` 服务上设置一个环境变量，指向容器中该文件的位置。

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
> 要了解有关 Compose 文件中指令的更多信息，请参阅 [Compose 文件参考](/reference/compose-file/)。

在使用 Compose 运行应用程序之前，请注意此 Compose 文件指定了一个 `password.txt` 文件来保存数据库的密码。您必须创建此文件，因为它不包含在源仓库中。

在克隆的仓库目录中，创建一个名为 `db` 的新目录，并在该目录中创建一个名为 `password.txt` 的文件，该文件包含数据库的密码。使用您喜欢的 IDE 或文本编辑器，将以下内容添加到 `password.txt` 文件中。

```text
mysecretpassword
```

保存并关闭 `password.txt` 文件。

您现在应该在 `r-docker-dev` 目录中拥有以下内容。

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

现在，运行以下 `docker compose up` 命令来启动您的应用程序。

```console
$ docker compose up --build
```

现在，在浏览器中打开以下地址来测试您的数据库连接：

```console
http://localhost:3838
```

您应该会看到一个弹出消息：

```text
DB CONNECTED
```

在终端中按 `ctrl+c` 停止您的应用程序。

## 自动更新服务

使用 Compose Watch 在您编辑并保存代码时自动更新正在运行的 Compose 服务。有关 Compose Watch 的更多详细信息，请参阅 [使用 Compose Watch](/manuals/compose/how-tos/file-watch.md)。

`compose.yaml` 文件中的第 15 到 18 行包含一些属性，当当前工作目录中的文件发生更改时，这些属性会触发 Docker 重新构建镜像：

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

运行以下命令以使用 Compose Watch 运行您的应用程序。

```console
$ docker compose watch
```

现在，如果您修改您的 `app.R`，您将实时看到更改，而无需重新构建镜像！

在终端中按 `ctrl+c` 停止您的应用程序。

## 总结

在本节中，您了解了如何设置 Compose 文件以添加本地数据库并持久化数据。您还学习了如何使用 Compose Watch 在更新代码时自动重新构建和运行容器。

相关信息：

- [Compose 文件参考](/reference/compose-file/)
- [Compose 文件监视](/manuals/compose/how-tos/file-watch.md)
- [多阶段构建](/manuals/build/building/multi-stage.md)

## 下一步

在下一节中，您将了解如何使用 GitHub Actions 设置 CI/CD 管道。