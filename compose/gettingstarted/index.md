# Docker Compose 快速入门


本教程旨在通过引导您开发一个基本的 Python Web 应用程序，来介绍 Docker Compose 的基本概念。

使用 Flask 框架，该应用程序在 Redis 中实现了一个访问计数器，提供了一个如何在 Web 开发场景中应用 Docker Compose 的实际示例。即使您不熟悉 Python，也应该能够理解这里演示的概念。

## 先决条件

请确保您已经：

- [安装了最新版本的 Docker Compose](/manuals/compose/install/_index.md)
- 对 Docker 概念和 Docker 的工作原理有基本的了解

## 步骤 1：设置项目

1. 为项目创建一个目录：

   ```console
   $ mkdir compose-demo
   $ cd compose-demo
   ```

2. 在项目目录中创建 `app.py` 并添加以下内容：

   ```python
   import os
   import redis
   from flask import Flask

   app = Flask(__name__)
   cache = redis.Redis(
       host=os.getenv("REDIS_HOST", "redis"),
       port=int(os.getenv("REDIS_PORT", "6379")),
   )

   @app.route("/")
   def hello():
       count = cache.incr("hits")
       return f"Hello from Docker! I have been seen {count} time(s).\n"
   ```

   该应用从环境变量读取其 Redis 连接信息，并带有合理的默认值，因此可以开箱即用。

3. 在项目目录中创建 `requirements.txt` 并添加以下内容：

   ```text
   flask
   redis
   ```

4. 创建一个 `Dockerfile`：

   ```dockerfile
   # syntax=docker/dockerfile:1

   # Build an image with the Python 3.12 image
   FROM python:3.12-alpine

   # Set the working directory to `/code`
   WORKDIR /code

   # Set environment variables used by the `flask` command
   ENV FLASK_APP=app.py
   ENV FLASK_RUN_HOST=0.0.0.0

   # Install `gcc` and other dependencies
   RUN apk add --no-cache gcc musl-dev linux-headers

   # Copy `requirements.txt`
   COPY requirements.txt .

   # Install the Python dependencies
   RUN pip install -r requirements.txt

   # Copy the current directory `.` in the project to the workdir `.` in the image
   COPY . .

   EXPOSE 5000

   # Set the default command for the container to `flask run --debug`
   CMD ["flask", "run", "--debug"]
   ```

   > [!IMPORTANT]
   >
   > 确保该文件名为 `Dockerfile`，没有扩展名。某些编辑器会自动添加 `.txt` 扩展名，这会导致构建失败。

   有关如何编写 Dockerfile 的更多信息，请参阅 [Dockerfile 参考](/reference/dockerfile/)。

5. 创建一个 `.env` 文件来保存配置值：

   ```text
   APP_PORT=8000
   REDIS_HOST=redis
   REDIS_PORT=6379
   ```

   Compose 会自动读取 `.env`，并使这些值可用于你的 `compose.yaml` 中的插值。对于这个示例来说收益不大，但在实践中，将配置保留在 Compose 文件之外可以更轻松地：
   - 跨环境更改值而无需编辑 YAML
   - 避免将密钥提交到版本控制
   - 在多个服务之间复用值

6. 创建一个 `.dockerignore` 文件，将不必要的文件排除在你的构建上下文之外：

   ```text
   .env
   *.pyc
   __pycache__
   redis-data
   ```

   Docker 在构建镜像时会将项目目录中的所有内容发送到守护进程。没有 `.dockerignore`，这会包括你的 `.env` 文件（可能包含密钥）以及任何缓存的 Python 字节码。排除它们可以保持构建快速，并避免将敏感值意外烘焙进镜像层。

## 步骤 2：定义并启动你的服务

Compose 简化了对整个应用堆栈的控制，使您能够轻松管理单个 YAML 配置文件中的服务、网络和卷。

1. 在项目目录中创建 `compose.yaml` 并粘贴以下内容：

   ```yaml
   services:
     web:
       build: .
       ports:
         - "${APP_PORT}:5000"
       environment:
         - REDIS_HOST=${REDIS_HOST}
         - REDIS_PORT=${REDIS_PORT}

     redis:
       image: redis:alpine
   ```

   这个 Compose 文件定义了两个服务：

   - `web` 服务使用从当前目录的 `Dockerfile` 构建的镜像。它将主机上的端口 `8000` 映射到 Flask 默认监听的容器端口 `5000`。

   - `redis` 服务使用从 Docker Hub 注册表拉取的公共 [Redis](https://registry.hub.docker.com/_/redis/) 镜像。

   有关 `compose.yaml` 文件的更多信息，请参阅 [Compose 的工作原理](compose-application-model.md)。

2. 启动你的应用：

   ```console
   $ docker compose up
   ```

   使用单个命令，您可以从配置文件中创建并启动所有服务。Compose 构建你的 web 镜像、拉取 Redis 镜像，并启动两个容器。

3. 打开 `http://localhost:8000`。你应该看到：

   ```text
   Hello from Docker! I have been seen 1 time(s).
   ```

   刷新页面——计数器会在每次访问时递增。

   这个最小设置可以工作，但它有两个你在接下来的步骤中会修复的问题：

   - 启动竞态：`web` 与 `redis` 同时启动。如果 Redis 尚未就绪，Flask 应用会连接失败并崩溃。
   - 无持久化：如果你运行 `docker compose down` 然后运行 `docker compose up`，计数器会重置为零。`docker compose down` 会移除容器，以及容器可写层中写入的任何数据。`docker compose stop` 会保留容器，因此数据会存活，但在容器经常被替换的生产环境中你不能依赖它。

4. 在继续之前停止该堆栈：

   ```console
   $ docker compose down
   ```

## 步骤 3：用健康检查修复启动竞态

为了修复启动竞态，Compose 需要在启动 `web` 之前等待 `redis` 被确认健康。

1. 更新 `compose.yaml`：

   ```yaml
   services:
     web:
       build: .
       ports:
         - "${APP_PORT}:5000"
       environment:
         - REDIS_HOST=${REDIS_HOST}
         - REDIS_PORT=${REDIS_PORT}
       depends_on:
         redis:
           condition: service_healthy

     redis:
       image: redis:alpine
       healthcheck:
         test: ["CMD", "redis-cli", "ping"]
         interval: 5s
         timeout: 3s
         retries: 5
         start_period: 10s
   ```

   `healthcheck` 块告诉 Compose 如何测试 Redis 是否就绪：

   - `test` 是 Compose 在容器内运行以检查其健康状态的命令。`redis-cli ping` 连接到 Redis 并期望得到 `PONG` 响应——如果得到，则容器是健康的。
   - `start_period` 给 Redis 10 秒的初始化时间，之后才开始健康检查。此窗口内的任何失败都不计入重试限制。
   - `interval` 在启动周期结束后每 5 秒运行一次检查。
   - `timeout` 给每次检查 3 秒的响应时间，超过则视为失败。
   - `retries` 设置 Compose 将容器标记为不健康之前允许的连续失败次数。在 `interval: 5s` 和 `retries: 5` 下，Compose 最多会等待 25 秒才放弃。

2. 启动堆栈以确认顺序已修复：

   ```console
   $ docker compose up
   ```

   你应该看到类似以下内容：

   ```text
   [+] Running 2/2
   ✔ Container compose-demo-redis-1  Healthy                       0.0s
   ```

3. 打开 `http://localhost:8000` 确认应用仍在工作，然后在继续之前停止堆栈：

   ```console
   $ docker compose down
   ```

## 步骤 4：启用 Compose Watch 进行实时更新

没有 Compose Watch，每次代码更改都需要你停止堆栈、重建镜像并重启容器。Compose Watch 通过在保存文件时自动将更改同步到运行中的容器来消除这个循环。

1. 更新 `compose.yaml`，向 `web` 服务添加 `develop.watch` 块：

   ```yaml
   services:
     web:
       build: .
       ports:
         - "${APP_PORT}:5000"
       environment:
         - REDIS_HOST=${REDIS_HOST}
         - REDIS_PORT=${REDIS_PORT}
       depends_on:
         redis:
           condition: service_healthy
       develop:
         watch:
           - action: sync+restart
             path: .
             target: /code
           - action: rebuild
             path: requirements.txt

     redis:
       image: redis:alpine
       healthcheck:
         test: ["CMD", "redis-cli", "ping"]
         interval: 5s
         timeout: 3s
         retries: 5
         start_period: 10s
   ```

   `watch` 块定义了两条规则：
   - `sync+restart` 动作监视主机上的项目目录（`.`）。当文件发生变化时，Compose 将任何更改的文件复制到运行中的容器内的 `/code`，然后重启容器。因为容器在更新后的文件已经就位的情况下重启，Flask 启动时直接读取新代码——无需手动重建或重启。
   - 对 `requirements.txt` 的 `rebuild` 动作会在你添加新依赖时触发完整的镜像重建，因为安装包需要重建镜像，而不仅仅是同步文件。

2. 在启用 Watch 的情况下启动堆栈：

   ```console
   $ docker compose up --watch
   ```

3. 进行实时更改。打开 `app.py` 并更新问候语：

   ```python
   return f"Hello from Compose Watch! I have been seen {count} time(s).\n"
   ```

4. 保存文件。Compose Watch 检测到更改并立即同步：

   ```text
   Syncing service "web" after changes were detected
   ```

5. 刷新 `http://localhost:8000`。更新后的问候语会出现，无需任何重启，计数器应该仍在递增。

6. 在继续之前停止堆栈：

   ```console
   $ docker compose down
   ```

   有关 Compose Watch 如何工作的更多信息，请参阅 [使用 Compose Watch](/manuals/compose/how-tos/file-watch.md)。

## 步骤 5：用命名卷持久化数据

每次你停止并重启堆栈，访问计数器都会重置为零。Redis 数据位于容器内部，因此在容器被移除时它会消失。命名卷通过将数据存储在宿主机上、在容器生命周期之外来修复这个问题。

1. 更新 `compose.yaml`：

   ```yaml
   services:
     web:
       build: .
       ports:
         - "${APP_PORT}:5000"
       environment:
         - REDIS_HOST=${REDIS_HOST}
         - REDIS_PORT=${REDIS_PORT}
       depends_on:
         redis:
           condition: service_healthy
       develop:
         watch:
           - action: sync+restart
             path: .
             target: /code
           - action: rebuild
             path: requirements.txt

     redis:
       image: redis:alpine
       volumes:
         - redis-data:/data
       healthcheck:
         test: ["CMD", "redis-cli", "ping"]
         interval: 5s
         timeout: 3s
         retries: 5
         start_period: 10s

   volumes:
     redis-data:
   ```

   `redis.volumes` 下的 `redis-data:/data` 条目将命名卷挂载到 `/data`，即 Redis 写入其数据文件的路径。顶级的 `volumes` 键将其注册到 Docker，使其在 `compose down` 和 `compose up` 周期之间持久保留。

2. 用 `docker compose up --watch` 启动堆栈，并刷新 `http://localhost:8000` 几次以累积计数。

3. 用 `docker compose down` 拆除堆栈，然后用 `docker compose up --watch` 再次启动它。

4. 打开 `http://localhost:8000`——计数器会从上次离开的地方继续。

5. 现在用 `docker compose down -v` 重置计数器。

   `-v` 标志会连同容器一起移除命名卷。请有意使用——它会永久删除存储的数据。

## 步骤 6：用多个 Compose 文件组织你的项目

随着应用的增长，单个 `compose.yaml` 变得更难维护。`include` 顶级元素让你可以将服务拆分到多个文件中，同时保持它们是同一个应用的一部分。

当不同团队拥有堆栈的不同部分，或你想在多个项目之间复用基础设施定义时，这尤其有用。

1. 在项目目录中创建一个名为 `infra.yaml` 的新文件，并将 Redis 服务和卷移入其中：

   ```yaml
   services:
     redis:
       image: redis:alpine
       volumes:
         - redis-data:/data
       healthcheck:
         test: ["CMD", "redis-cli", "ping"]
         interval: 5s
         timeout: 3s
         retries: 5
         start_period: 10s

   volumes:
     redis-data:
   ```

2. 更新 `compose.yaml` 以包含 `infra.yaml`：

   ```yaml
   include:
     - path: ./infra.yaml
   services:
     web:
       build: .
       ports:
         - "${APP_PORT}:5000"
       environment:
         - REDIS_HOST=${REDIS_HOST}
         - REDIS_PORT=${REDIS_PORT}
       depends_on:
         redis:
           condition: service_healthy
       develop:
         watch:
           - action: sync+restart
             path: .
             target: /code
           - action: rebuild
             path: requirements.txt
   ```

3. 运行应用以确认一切仍正常工作：

   ```console
   $ docker compose up --watch
   ```

   Compose 在启动时合并两个文件。`web` 服务仍然可以通过名称引用 `redis`，因为所有包含的服务共享同一个默认网络。

   这是一个简化的示例，但它演示了 `include` 的基本原理，以及它如何使将复杂应用模块化到子 Compose 文件中变得更加容易。有关 `include` 和使用多个 Compose 文件的更多信息，请参阅 [使用多个 Compose 文件](/manuals/compose/how-tos/multiple-compose-files/_index.md)。

4. 在继续之前停止堆栈：

   ```console
   $ docker compose down
   ```

## 步骤 7：检查并调试你运行的堆栈

有了完整配置的堆栈，你可以在不停止任何东西的情况下观察容器内部发生的情况。这一步涵盖检查已解析配置、流式传输日志以及在运行中的容器内运行命令的核心命令。

在启动堆栈之前，验证 Compose 是否已解析你的 `.env` 变量并正确合并了所有文件：

```console
$ docker compose config
```

`docker compose config` 不需要堆栈在运行——它纯粹根据你的文件工作。输出中值得注意的几点：

- `${APP_PORT}`、`${REDIS_HOST}` 和 `${REDIS_PORT}` 都已被你的 `.env` 文件中的值替换。
- 短格式的端口表示法（`"8000:5000"`）被扩展为其规范字段（`target`、`published`、`protocol`）。
- 默认网络和卷名被显式化，并以前缀项目名 `compose-demo` 开头。
- 输出是完全解析的配置，通过 `include` 引入的任何文件都合并到单个视图中。

当你想确认 Compose 实际会应用什么时，请使用 `docker compose config`，尤其是在调试变量替换或使用多个 Compose 文件时。

现在以分离模式启动堆栈，以便终端保持空闲以供后续命令使用：

```console
$ docker compose up -d
```

### 从所有服务流式传输日志

```console
$ docker compose logs -f
```

`-f` 标志实时跟踪日志流，交错来自两个容器的输出，并带有彩色编码的服务名前缀。刷新 `http://localhost:8000` 几次，并观察 Flask 请求日志出现。要跟踪单个服务的日志，传入其名称：

```console
$ docker compose logs -f web
```

按 `Ctrl+C` 停止跟踪日志。容器继续运行。

### 在运行中的容器内运行命令

`docker compose exec` 在已经运行的容器内运行命令，而不启动新容器。这是实时调试的主要工具。

#### 验证环境变量是否正确设置

```console
$ docker compose exec web env | grep REDIS
```

```text
REDIS_HOST=redis
REDIS_PORT=6379
```

#### 测试 `web` 容器能否使用服务名作为主机名到达 Redis

```console
$ docker compose exec web python -c "import redis; r = redis.Redis(host='redis'); print(r.ping())"
```

```text
True
```

这使用了你的应用使用的相同 `redis` 库，因此 `True` 响应确认了服务发现、网络以及 Redis 连接端到端都在工作。

#### 检查 Redis 中访问计数器的实时值

```console
$ docker compose exec redis redis-cli GET hits
```

## 接下来去哪里

- [探索完整的 Compose 命令列表](/reference/cli/docker/compose/)
- [探索 Compose 文件参考](/reference/compose-file/_index.md)
- [查看 LinkedIn Learning 上的 Learning Docker Compose 视频](https://www.linkedin.com/learning/learning-docker-compose/)
- [了解如何在 Compose 中设置环境变量](/compose/how-tos/environment-variables/set-environment-variables/)
- [了解如何打包和分发你的 Compose 应用](/compose/how-tos/oci-artifact/)
