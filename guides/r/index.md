# R 语言专项指南


R 语言专项指南将教你如何使用 Docker 容器化 R 应用。在本指南中，你将学会：

- 容器化并运行 R 应用
- 使用容器搭建本地环境来开发 R 应用

首先从容器化一个现有的 R 应用开始。

## Containerize a R application（容器化 R 应用）

### 前提条件

- 你已安装 [git 客户端](https://git-scm.com/downloads)。本节示例使用基于命令行的 git
  客户端，但你可以使用任意客户端。

### 概述

本节将带你完成 R 应用的容器化与运行。

### 获取示例应用

示例应用使用了流行的 [Shiny](https://shiny.posit.co/) 框架。

克隆本指南使用的示例应用。打开终端，切换到你想工作的目录，然后运行以下命令克隆仓库：

```console
$ git clone https://github.com/mfranzon/r-docker-dev.git && cd r-docker-dev
```

现在你的 `r-docker-dev` 目录中应该有以下内容。

```text
├── r-docker-dev/
│ ├── src/
│ │ └── app.R
│ ├── src_db/
│ │ └── app_db.R
│ ├── compose.yaml
│ ├── Dockerfile
│ └── README.md
```

要进一步了解仓库中的文件，请参阅：

- [Dockerfile](/reference/dockerfile.md)
- [.dockerignore](/reference/dockerfile.md#dockerignore-file)
- [compose.yaml](/reference/compose-file/_index.md)

### 运行应用

在 `r-docker-dev` 目录中，于终端运行以下命令。

```console
$ docker compose up --build
```

打开浏览器访问 [http://localhost:3838](http://localhost:3838) 查看应用。你应该会看到一个
简单的 Shiny 应用。

在终端中按 `ctrl`+`c` 停止应用。

#### 在后台运行应用

你可以加上 `-d` 选项，让应用与终端分离后运行。在 `r-docker-dev` 目录中，于终端运行以下命令。

```console
$ docker compose up --build -d
```

打开浏览器访问 [http://localhost:3838](http://localhost:3838) 查看应用。

你应该会看到一个简单的 Shiny 应用。

在终端中运行以下命令停止应用。

```console
$ docker compose down
```

有关 Compose 命令的更多信息，参阅 [Compose CLI
参考](/reference/cli/docker/compose/)。

## 使用容器进行 R 开发

### 前提条件

完成 [Containerize a R application](#containerize-a-r-application)。

### 概述

在本节中，你将学习如何为容器化应用搭建开发环境。这包括：

- 添加本地数据库并持久化数据
- 配置 Compose，使其在你编辑并保存代码时自动更新正在运行的 Compose 服务

### 获取示例应用

你需要克隆一个新仓库，以获得包含数据库连接逻辑的示例应用。

切换到你想克隆仓库的目录，然后运行以下命令。

```console
$ git clone https://github.com/mfranzon/r-docker-dev.git
```

### 配置应用以使用数据库

要试用 Shiny 应用与本地数据库之间的连接，你需要修改 `Dockerfile`，更改 `COPY` 指令：

```diff
-COPY src/ .
+COPY src_db/ .
```

### 添加本地数据库并持久化数据

你可以使用容器来搭建本地服务，例如数据库。在本节中，你将更新 `compose.yaml` 文件，
定义一个数据库服务以及一个用于持久化数据的卷。

在克隆下来的仓库目录中，用 IDE 或文本编辑器打开 `compose.yaml` 文件。

在 `compose.yaml` 文件中，你需要取消注释用于配置数据库的属性。你还必须挂载数据库密码
文件，并在 `shiny-app` 服务上设置一个环境变量，指向该文件在容器中的位置。

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
> 要进一步了解 Compose 文件中的各项指令，参阅 [Compose 文件
> 参考](/reference/compose-file/)。

在使用 Compose 运行应用之前，请注意这个 Compose 文件指定了一个 `password.txt` 文件来
保存数据库密码。你必须自行创建该文件，因为它并未包含在源码仓库中。

在克隆下来的仓库目录中，创建一个名为 `db` 的新目录，并在该目录中创建一个名为
`password.txt` 的文件，其中包含数据库密码。使用你喜欢的 IDE 或文本编辑器，把以下内容
添加到 `password.txt` 文件中。

```text
mysecretpassword
```

保存并关闭 `password.txt` 文件。

现在你的 `r-docker-dev` 目录中应该有以下内容。

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
│ └── README.md
```

现在运行以下 `docker compose up` 命令启动你的应用。

```console
$ docker compose up --build
```

然后打开浏览器测试数据库连接：

```console
http://localhost:3838
```

你应该会看到一条弹出消息：

```text
DB CONNECTED
```

在终端中按 `ctrl+c` 停止应用。

### 自动更新服务

使用 Compose Watch，在你编辑并保存代码时自动更新正在运行的 Compose 服务。有关
Compose Watch 的更多细节，参阅[使用 Compose
Watch](/manuals/compose/how-tos/file-watch.md)。

`compose.yaml` 文件中的第 15 到 18 行包含了一些属性，当当前工作目录中的文件发生变化时，
它们会触发 Docker 重新构建镜像：

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

运行以下命令，以 Compose Watch 方式运行你的应用。

```console
$ docker compose watch
```

现在，如果你修改 `app.R`，就能实时看到变化，而无需重新构建镜像！

在终端中按 `ctrl+c` 停止应用。

### 小结

在本节中，你了解了如何配置 Compose 文件以添加本地数据库并持久化数据。你还学习了如何使用
Compose Watch，在更新代码时自动重新构建并运行容器。

相关信息：

- [Compose 文件参考](/reference/compose-file/)
- [Compose file watch](/manuals/compose/how-tos/file-watch.md)
- [多阶段构建](/manuals/build/building/multi-stage.md)

