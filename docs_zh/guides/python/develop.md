---
title: 使用容器进行 Python 开发
linkTitle: 开发应用
weight: 15
keywords: python, local, development
description: 了解如何在本地开发 Python 应用程序。
aliases:
- /language/python/develop/
- /guides/language/python/develop/
---

## 先决条件

完成[容器化 Python 应用程序](containerize.md)。

## 概述

在本节中，您将学习如何为容器化应用程序设置开发环境。这包括：

- 添加本地数据库并持久化数据
- 配置 Compose 以在您编辑和保存代码时自动更新正在运行的 Compose 服务

## 获取示例应用程序

您需要克隆一个新的仓库来获取包含连接数据库逻辑的示例应用程序。

1. 切换到您要克隆仓库的目录，然后运行以下命令。

   ```console
   $ git clone https://github.com/estebanx64/python-docker-dev-example
   ```

2. 在克隆的仓库目录中，手动创建 Docker 资产或运行 `docker init` 来创建必要的 Docker 资产。

   {{< tabs >}}
   {{< tab name="使用 Docker Init" >}}

   在克隆的仓库目录中，运行 `docker init`。参考以下示例来回答 `docker init` 的提示。

   ```console
   $ docker init
   欢迎使用 Docker Init CLI！

   此工具将引导您创建以下文件，并为您的项目设置合理的默认值：
     - .dockerignore
     - Dockerfile
     - compose.yaml
     - README.Docker.md

   让我们开始吧！

   ? 您的项目使用什么应用程序平台？Python
   ? 您想使用哪个版本的 Python？3.12
   ? 您希望应用程序监听哪个端口？8001
   ? 运行应用程序的命令是什么？python3 -m uvicorn app:app --host=0.0.0.0 --port=8001
   ```

   创建一个名为 `.gitignore` 的文件，内容如下。

   ```text {collapse=true,title=".gitignore"}
   # 字节编译/优化/DLL 文件
   __pycache__/
   *.py[cod]
   *$py.class

   # C 扩展
   *.so

   # 分发/打包
   .Python
   build/
   develop-eggs/
   dist/
   downloads/
   eggs/
   .eggs/
   lib/
   lib64/
   parts/
   sdist/
   var/
   wheels/
   share/python-wheels/
   *.egg-info/
   .installed.cfg
   *.egg
   MANIFEST

   # 单元测试/覆盖率报告
   htmlcov/
   .tox/
   .nox/
   .coverage
   .coverage.*
   .cache
   nosetests.xml
   coverage.xml
   *.cover
   *.py,cover
   .hypothesis/
   .pytest_cache/
   cover/

   # PEP 582；例如被 github.com/David-OConnor/pyflow 和 github.com/pdm-project/pdm 使用
   __pypackages__/

   # 环境
   .env
   .venv
   env/
   venv/
   ENV/
   env.bak/
   venv.bak/
   ```

   {{< /tab >}}
   {{< tab name="手动创建资产" >}}

   如果您没有安装 Docker Desktop 或更喜欢手动创建资产，您可以在项目目录中创建以下文件。

   创建一个名为 `Dockerfile` 的文件，内容如下。

   ```dockerfile {collapse=true,title=Dockerfile}
   # syntax=docker/dockerfile:1

   # 此文件中提供了注释以帮助您入门。
   # 如果您需要更多帮助，请访问 Dockerfile 参考指南：
   # https://docs.docker.com/go/dockerfile-reference/

   # 想帮助我们改进此模板？在此分享您的反馈：https://   forms.gle/ybq9Krt8jtBL3iCk7

   ARG PYTHON_VERSION=3.12
   FROM python:${PYTHON_VERSION}-slim

   # 防止 Python 写入 pyc 文件。
   ENV PYTHONDONTWRITEBYTECODE=1

   # 防止 Python 缓冲 stdout 和 stderr，以避免由于缓冲而导致应用程序崩溃时没有发出任何日志的情况。
   ENV PYTHONUNBUFFERED=1

   WORKDIR /app

   # 创建一个非特权用户，应用程序将以此用户身份运行。
   # 参见 https://docs.docker.com/go/dockerfile-user-best-practices/
   ARG UID=10001
   RUN adduser \
       --disabled-password \
       --gecos "" \
       --home "/nonexistent" \
       --shell "/sbin/nologin" \
       --no-create-home \
       --uid "${UID}" \
       appuser

   # 将下载依赖项作为单独的步骤，以利用 Docker 的缓存。
   # 利用缓存挂载到 /root/.cache/pip 以加速后续构建。
   # 利用绑定挂载到 requirements.txt 以避免必须将它们复制到此层中。
   RUN --mount=type=cache,target=/root/.cache/pip \
       --mount=type=bind,source=requirements.txt,target=requirements.txt \
       python -m pip install -r requirements.txt

   # 切换到非特权用户以运行应用程序。
   USER appuser

   # 将源代码复制到容器中。
   COPY . .

   # 暴露应用程序监听的端口。
   EXPOSE 8001

   # 运行应用程序。
   CMD ["python3", "-m", "uvicorn", "app:app", "--host=0.0.0.0", "--port=8001"]
   ```

   创建一个名为 `compose.yaml` 的文件，内容如下。

   ```yaml {collapse=true,title=compose.yaml}
   # 此文件中提供了注释以帮助您入门。
   # 如果您需要更多帮助，请访问 Compose 参考指南：
   # https://docs.docker.com/go/compose-spec-reference/

   # 这里的指令将您的应用程序定义为一个名为 "server" 的服务。
   # 此服务从当前目录中的 Dockerfile 构建。
   # 您可以在此处添加您的应用程序可能依赖的其他服务，例如数据库或缓存。有关示例，请参阅 Awesome Compose 仓库：
   # https://github.com/docker/awesome-compose
   services:
     server:
       build:
         context: .
       ports:
         - 8001:8001
   # 下面的注释部分是定义您的应用程序可以使用的 PostgreSQL 数据库的示例。`depends_on` 告诉 Docker Compose 在您的应用程序之前启动数据库。`db-data` 卷在容器重启之间保持数据库数据。`db-password` 秘密用于设置数据库密码。您必须在运行 `docker compose up` 之前创建 `db/password.txt` 并向其中添加您选择的密码。
   #     depends_on:
   #       db:
   #         condition: service_healthy
   #   db:
   #     image: postgres:18
   #     restart: always
   #     user: postgres
   #     secrets:
   #       - db-password
   #     volumes:
   #       - db-data:/var/lib/postgresql
   #     environment:
   #       - POSTGRES_DB=example
   #       - POSTGRES_PASSWORD_FILE=/run/secrets/db-password
   #     expose:
   #       - 5432
   #     healthcheck:
   #       test: [ "CMD", "pg_isready" ]
   #       interval: 10s
   #       timeout: 5s
   #       retries: 5
   # volumes:
   #   db-data:
   # secrets:
   #   db-password:
   #     file: db/password.txt
   ```

   创建一个名为 `.dockerignore` 的文件，内容如下。

   ```text {collapse=true,title=".dockerignore"}
   # 在此处包含您不希望复制到容器的任何文件或目录（例如，本地构建工件、临时文件等）。
   #
   # 有关更多帮助，请访问 .dockerignore 文件参考指南：
   # https://docs.docker.com/go/build-context-dockerignore/

   **/.DS_Store
   **/__pycache__
   **/.venv
   **/.classpath
   **/.dockerignore
   **/.env
   **/.git
   **/.gitignore
   **/.project
   **/.settings
   **/.toolstarget
   **/.vs
   **/.vscode
   **/*.*proj.user
   **/*.dbmdl
   **/*.jfm
   **/bin
   **/charts
   **/docker-compose*
   **/compose.y*ml
   **/Dockerfile*
   **/node_modules
   **/npm-debug.log
   **/obj
   **/secrets.dev.yaml
   **/values.dev.yaml
   LICENSE
   README.md
   ```

   创建一个名为 `.gitignore` 的文件，内容如下。

   ```text {collapse=true,title=".gitignore"}
   # 字节编译/优化/DLL 文件
   __pycache__/
   *.py[cod]
   *$py.class

   # C 扩展
   *.so

   # 分发/打包
   .Python
   build/
   develop-eggs/
   dist/
   downloads/
   eggs/
   .eggs/
   lib/
   lib64/
   parts/
   sdist/
   var/
   wheels/
   share/python-wheels/
   *.egg-info/
   .installed.cfg
   *.egg
   MANIFEST

   # 单元测试/覆盖率报告
   htmlcov/
   .tox/
   .nox/
   .coverage
   .coverage.*
   .cache
   nosetests.xml
   coverage.xml
   *.cover
   *.py,cover
   .hypothesis/
   .pytest_cache/
   cover/

   # PEP 582；例如被 github.com/David-OConnor/pyflow 和 github.com/pdm-project/pdm 使用
   __pypackages__/

   # 环境
   .env
   .venv
   env/
   venv/
   ENV/
   env.bak/
   venv.bak/
   ```

   {{< /tab >}}
   {{< /tabs >}}

## 添加本地数据库并持久化数据

您可以使用容器来设置本地服务，如数据库。在本节中，您将更新 `compose.yaml` 文件以定义数据库服务和持久化数据的卷。

在克隆的仓库目录中，在 IDE 或文本编辑器中打开 `compose.yaml` 文件。`docker init` 处理了创建大部分指令，但您需要根据您的独特应用程序进行更新。

在 `compose.yaml` 文件中，您需要取消注释所有数据库指令。此外，您需要将数据库密码文件作为环境变量添加到服务器服务，并指定要使用的秘密文件。

以下是更新后的 `compose.yaml` 文件。

```yaml {hl_lines="7-43"}
services:
  server:
    build:
      context: .
    ports:
      - 8001:8001
    environment:
      - POSTGRES_SERVER=db
      - POSTGRES_USER=postgres
      - POSTGRES_DB=example
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
> 要了解 Compose 文件中的指令，请参阅 [Compose 文件参考](/reference/compose-file/)。

在运行应用程序之前，请注意此 Compose 文件指定了一个 `password.txt` 文件来保存数据库的密码。您必须创建此文件，因为它不包含在源仓库中。

在克隆的仓库目录中，创建一个名为 `db` 的新目录，并在该目录中创建一个名为 `password.txt` 的文件，其中包含数据库的密码。使用您喜欢的 IDE 或文本编辑器，将以下内容添加到 `password.txt` 文件中。

```text
mysecretpassword
```

保存并关闭 `password.txt` 文件。

现在，您的 `python-docker-dev-example` 目录中应该有以下内容。

```text
├── python-docker-dev-example/
│ ├── db/
│ │ └── password.txt
│ ├── app.py
│ ├── config.py
│ ├── requirements.txt
│ ├── .dockerignore
│ ├── .gitignore
│ ├── compose.yaml
│ ├── Dockerfile
│ ├── README.Docker.md
│ └── README.md
```

现在，运行以下 `docker compose up` 命令来启动您的应用程序。

```console
$ docker compose up --build
```

现在测试您的 API 端点。打开一个新的终端，然后使用 curl 命令向服务器发出请求：

让我们使用 post 方法创建一个对象

```console
$ curl -X 'POST' \
  'http://localhost:8001/heroes/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "id": 1,
  "name": "my hero",
  "secret_name": "austing",
  "age": 12
}'
```

您应该会收到以下响应：

```json
{
  "age": 12,
  "id": 1,
  "name": "my hero",
  "secret_name": "austing"
}
```

让我们使用下一个 curl 命令进行 get 请求：

```console
curl -X 'GET' \
  'http://localhost:8001/heroes/' \
  -H 'accept: application/json'
```

您应该会收到与上面相同的响应，因为它是数据库中唯一的对象。

```json
{
  "age": 12,
  "id": 1,
  "name": "my hero",
  "secret_name": "austing"
}
```

在终端中按 `ctrl+c` 停止您的应用程序。

## 自动更新服务

使用 Compose Watch 在您编辑和保存代码时自动更新正在运行的 Compose 服务。有关 Compose Watch 的更多详细信息，请参阅[使用 Compose Watch](/manuals/compose/how-tos/file-watch.md)。

在 IDE 或文本编辑器中打开您的 `compose.yaml` 文件，然后添加 Compose Watch 指令。以下是更新后的 `compose.yaml` 文件。

```yaml {hl_lines="17-20"}
services:
  server:
    build:
      context: .
    ports:
      - 8001:8001
    environment:
      - POSTGRES_SERVER=db
      - POSTGRES_USER=postgres
      - POSTGRES_DB=example
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

在终端中，curl 应用程序以获取响应。

```console
$ curl http://localhost:8001
Hello, Docker!
```

现在，您在本地机器上对应用程序源文件所做的任何更改都会立即反映在正在运行的容器中。

在 IDE 或文本编辑器中打开 `python-docker-dev-example/app.py` 并更新 `Hello, Docker!` 字符串，添加几个感叹号。

```diff
-    return 'Hello, Docker!'
+    return 'Hello, Docker!!!'
```

保存对 `app.py` 的更改，然后等待几秒钟让应用程序重新构建。再次 curl 应用程序并验证更新的文本是否出现。

```console
$ curl http://localhost:8001
Hello, Docker!!!
```

在终端中按 `ctrl+c` 停止您的应用程序。

## 总结

在本节中，您查看了如何设置 Compose 文件以添加本地数据库并持久化数据。您还学习了如何使用 Compose Watch 在更新代码时自动重新构建和运行容器。

相关信息：

- [Compose 文件参考](/reference/compose-file/)
- [Compose 文件 watch](/manuals/compose/how-tos/file-watch.md)
- [多阶段构建](/manuals/build/building/multi-stage.md)

## 下一步

在下一节中，您将学习如何设置 linting、格式化和类型检查以遵循 python 应用程序的最佳实践。