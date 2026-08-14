# 将 Django 应用容器化


## 先决条件

- 你已安装最新版本的 [Docker Desktop](/get-started/get-docker.md)。
- 你已安装 [uv](https://docs.astral.sh/uv/)，或者你可以借助 Docker，在无需本地 Python 或 uv 安装的情况下搭建项目。

> [!TIP]
>
> 如果你是 Docker 新手，请先从 [Docker 基础](/get-started/docker-concepts/the-basics/what-is-a-container.md) 指南开始，熟悉镜像、容器和 Dockerfile 等关键概念。

---

## 概述

本指南将带你通过 Docker 将 Django 应用容器化。完成之后，你将能够：

- 使用 uv 在本地或在 Docker Hardened Image 容器中初始化一个 Django 项目。
- 使用 [Docker Hardened Images（DHI）](/dhi/) 创建一个可用于生产的 Dockerfile。
- 向你的 Dockerfile 添加一个 `development`（开发）阶段，并配置 Compose Watch 以实现自动代码同步。

---

## 创建 Django 项目

你可以使用本地的 uv 安装来引导项目，也可以完全在容器中使用与 Dockerfile 相同的 DHI 镜像来完成，无需本地 Python。

**Local (uv)**



1. 初始化项目并固定到 Python 3.14，然后进入该项目目录：

   ```console
   $ uv init --python 3.14 django-docker
   $ cd django-docker
   ```

2. 添加 Django 和 Gunicorn，然后搭建 Django 项目骨架：

   ```console
   $ uv add django gunicorn
   $ uv run django-admin startproject myapp .
   ```

**Container (DHI)**



DHI dev 镜像已经包含 Python 3.14，因此搭建出的项目会与 Dockerfile 完全一致。

1. 创建项目目录并进入：

   ```console
   $ mkdir django-docker && cd django-docker
   ```

2. 初始化项目、添加依赖并搭建骨架。全部在一次性容器运行中完成：

   ```console
   $ docker run --rm -v $PWD:$PWD -w $PWD \
     -e UV_LINK_MODE=copy \
     dhi.io/python:3.14-alpine3.23-dev \
     sh -c "pip install --quiet --root-user-action=ignore uv && uv init --name django-docker --python 3.14 . && uv add django gunicorn && uv run django-admin startproject myapp ."
   ```

   > [!NOTE]
   >
   > 上述命令使用了 Mac/Linux shell 语法。在 Windows 上，需要调整路径：PowerShell 使用 `${PWD}`，命令提示符使用 `%cd%`，Git Bash 需要配合 `MSYS_NO_PATHCONV=1` 与 `$(pwd -W)`。



你的目录现在应当包含以下文件：

```text
├── .python-version
├── main.py
├── manage.py
├── myapp/
│ ├── __init__.py
│ ├── asgi.py
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
├── pyproject.toml
├── uv.lock
└── README.md
```

---

## 创建生产用 Dockerfile

Docker Hardened Images 是由 Docker 维护的、可用于生产的基础镜像，能够最大程度地减小攻击面。更多详情，请参阅 [Docker Hardened Images](/dhi/)。

1. 登录到 DHI 镜像仓库：

   ```console
   $ docker login dhi.io
   ```

2. 创建一个 `.dockerignore` 文件，将本地构建产物排除在构建上下文之外：

   ```text {title=".dockerignore"}
   .venv/
   __pycache__/
   *.pyc
   .git/
   ```

3. 创建一个包含以下内容的 `Dockerfile`：

   ```dockerfile {title="Dockerfile"}
   # syntax=docker/dockerfile:1

   # Build stage: the -dev image includes tools needed to install packages.
   FROM dhi.io/python:3.14-alpine3.23-dev AS builder

   # Prevent Python from writing .pyc files to disk.
   ENV PYTHONDONTWRITEBYTECODE=1
   # Prevent Python from buffering stdout/stderr so logs appear immediately.
   ENV PYTHONUNBUFFERED=1

   RUN pip install --quiet --root-user-action=ignore uv
   # Use copy mode since the cache and build filesystem are on different volumes.
   ENV UV_LINK_MODE=copy

   WORKDIR /app

   # Install dependencies into a virtual environment using cache and bind mounts
   # so neither uv nor the lock files need to be copied into the image.
   RUN --mount=type=cache,target=/root/.cache/uv \
       --mount=type=bind,source=uv.lock,target=uv.lock \
       --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
       uv sync --frozen --no-install-project

   # Runtime stage: minimal DHI image with no shell or package manager,
   # already runs as the nonroot user.
   FROM dhi.io/python:3.14-alpine3.23

   # Prevent Python from buffering stdout/stderr so logs appear immediately.
   ENV PYTHONUNBUFFERED=1
   # Activate the virtual environment copied from the build stage.
   ENV PATH="/app/.venv/bin:$PATH"

   WORKDIR /app

   # Copy the pre-built virtual environment and application source code.
   COPY --from=builder /app/.venv /app/.venv
   COPY . .

   EXPOSE 8000

   # Run Gunicorn as the production WSGI server.
   CMD ["gunicorn", "myapp.wsgi:application", "--bind", "0.0.0.0:8000"]
   ```

4. 创建一个 `compose.yaml` 文件：

   ```yaml {title="compose.yaml"}
   services:
     web:
       build: .
       ports:
         - "8000:8000"
   ```

### 运行应用

在 `django-docker` 目录中运行：

```console
$ docker compose up --build
```

打开浏览器并访问 [http://localhost:8000](http://localhost:8000)。你应该会看到 Django 的欢迎页面。

按 `ctrl`+`c` 停止应用。

---

## 搭建开发环境

生产环境使用 Gunicorn，并且需要完整重建镜像才能获取代码改动。对于开发，你可以向 Dockerfile 添加一个 `development` 阶段，使用 Django 内置的服务器，并配置 Compose Watch 以在无需重建的情况下自动将代码改动同步到运行中的容器里。

### 更新 Dockerfile

将你的 `Dockerfile` 替换为多阶段版本，在 `production` 之外再添加一个 `development` 阶段：

```dockerfile {title="Dockerfile"}
# syntax=docker/dockerfile:1

# Build stage: the -dev image includes tools needed to install packages.
FROM dhi.io/python:3.14-alpine3.23-dev AS builder

# Prevent Python from writing .pyc files to disk.
ENV PYTHONDONTWRITEBYTECODE=1
# Prevent Python from buffering stdout/stderr so logs appear immediately.
ENV PYTHONUNBUFFERED=1

RUN pip install --quiet --root-user-action=ignore uv
# Use copy mode since the cache and build filesystem are on different volumes.
ENV UV_LINK_MODE=copy

WORKDIR /app

# Install dependencies into a virtual environment using cache and bind mounts
# so neither uv nor the lock files need to be copied into the image.
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

# The development stage inherits the -dev image and virtual environment from
# the builder. Django's built-in server reloads when Compose Watch syncs files.
FROM builder AS development

ENV PATH="/app/.venv/bin:$PATH"

COPY . .
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# The production stage uses the minimal runtime image, which has no shell,
# no package manager, and already runs as the nonroot user.
FROM dhi.io/python:3.14-alpine3.23 AS production

# Prevent Python from buffering stdout/stderr so logs appear immediately.
ENV PYTHONUNBUFFERED=1
# Activate the virtual environment copied from the build stage.
ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Copy only the pre-built virtual environment and application source code.
COPY --from=builder /app/.venv /app/.venv
COPY . .

EXPOSE 8000

# Run Gunicorn as the production WSGI server.
CMD ["gunicorn", "myapp.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### 更新 Compose 文件

将你的 `compose.yaml` 替换为以下内容。它针对 `development` 阶段，添加了一个 PostgreSQL 数据库，并配置了 Compose Watch：

```yaml {title="compose.yaml"}
services:
  web:
    build:
      context: .
      # Build the development stage from the multi-stage Dockerfile.
      target: development
    ports:
      - "8000:8000"
    environment:
      # Enable Django's verbose debug error pages (the dev server always auto-reloads).
      - DEBUG=1
      # Database connection settings passed to Django via environment variables.
      - POSTGRES_DB=myapp
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
      - POSTGRES_HOST=db
      - POSTGRES_PORT=5432
    # Wait for the database to pass its healthcheck before starting the web service.
    depends_on:
      db:
        condition: service_healthy
    develop:
      watch:
        # Sync source file changes directly into the container so Django's
        # dev server can reload them without a full image rebuild.
        - action: sync
          path: .
          target: /app
          ignore:
            - __pycache__/
            - "*.pyc"
            - .git/
            - .venv/
        # Rebuild the image when dependencies change.
        - action: rebuild
          path: pyproject.toml
        - action: rebuild
          path: uv.lock
  db:
    image: dhi.io/postgres:18
    restart: always
    volumes:
      # Persist database data across container restarts.
      - db-data:/var/lib/postgresql
    environment:
      - POSTGRES_DB=myapp
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    # Expose the port only to other services on the Compose network,
    # not to the host machine.
    expose:
      - 5432
    # Only report healthy once PostgreSQL is ready to accept connections,
    # so the web service doesn't start before the database is available.
    healthcheck:
      test: ["CMD", "pg_isready"]
      interval: 10s
      timeout: 5s
      retries: 5
volumes:
  db-data:
```

`sync` 动作会将文件改动直接推送进运行中的容器，以便 Django 的开发服务器自动重新加载它们。对 `pyproject.toml` 或 `uv.lock` 的改动则改为触发一次完整的镜像重建。

> [!NOTE]
>
> 要了解更多关于 Compose Watch 的内容，请参阅 [使用 Compose Watch](/manuals/compose/how-tos/file-watch.md)。

### 添加 PostgreSQL 驱动

将 `psycopg` 适配器添加到你的项目中：

**Local (uv)**



```console
$ uv add 'psycopg[binary]'
```

**Container (DHI)**



```console
$ docker run --rm -v $PWD:$PWD -w $PWD \
  -e UV_LINK_MODE=copy \
  dhi.io/python:3.14-alpine3.23-dev \
  sh -c "pip install --quiet --root-user-action=ignore uv && uv add 'psycopg[binary]'"
```



然后更新 `myapp/settings.py`，以从环境变量中读取 `DEBUG` 和 `DATABASES`：

```python {title="myapp/settings.py"}
import os

DEBUG = os.environ.get('DEBUG', '0') == '1'

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", "myapp"),
        "USER": os.environ.get("POSTGRES_USER", "postgres"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "password"),
        "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
    }
}
```

### 使用 Compose Watch 运行

启动开发栈：

```console
$ docker compose watch
```

打开浏览器并访问 [http://localhost:8000](http://localhost:8000)。

尝试编辑一个文件，例如向 `myapp/views.py` 添加一个视图。Compose Watch 会将改动同步进容器，Django 开发服务器会自动重新加载。如果你更新了 `pyproject.toml` 或 `uv.lock`，Compose Watch 会触发一次完整的镜像重建。

按 `ctrl`+`c` 停止。

---

## 总结

在本指南中，你：

- 使用 uv 引导了一个 Django 项目，提供了本地和容器化两种搭建方式。
- 使用 Docker Hardened Images 和 uv（用于依赖管理）创建了一个可用于生产的 Dockerfile。
- 向 `Dockerfile` 添加了一个 `development` 阶段，并配置了 Compose Watch，配合 PostgreSQL 数据库实现快速迭代开发。

相关信息：

- [Dockerfile 参考](/reference/dockerfile.md)
- [Compose 文件参考](/reference/compose-file/_index.md)
- [使用 Compose Watch](/manuals/compose/how-tos/file-watch.md)
- [Docker Hardened Images](/dhi/)
- [多阶段构建](/manuals/build/building/multi-stage.md)
- [uv 文档](https://docs.astral.sh/uv/)

