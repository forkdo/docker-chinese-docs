# Python 语言专项指南


> **致谢**
>
> 本指南由社区贡献。Docker 在此感谢
> [Esteban Maya](https://www.linkedin.com/in/esteban-x64/) 和 [Igor Aleksandrov](https://www.linkedin.com/in/igor-aleksandrov/) 对本指南的贡献。

Python 语言专项指南将教你如何使用 Docker 容器化一个 Python 应用。在本指南中，你将学习如何：

- 容器化并运行一个 Python 应用
- 搭建本地环境，使用容器开发 Python 应用
- 代码检查（lint）、格式化、类型检查与最佳实践

首先从容器化一个已有的 Python 应用开始。

## Containerize a Python application

### 先决条件

- 你已安装最新版本的 [Docker Desktop](/get-started/get-docker.md)。

### 概述

容器化你的应用，意味着将应用与其依赖、配置和运行时一起打包成一个可移植的单元，称为容器镜像。运行该镜像会创建一个容器——一个隔离的进程，无论在你的笔记本、CI 运行器还是生产服务器上，其行为都保持一致。

在本节中，你将容器化一个简单的 [FastAPI](https://fastapi.tiangolo.com) Web 应用。你将编写一个 `Dockerfile` 来描述如何构建镜像，添加一个 `compose.yaml` 文件来定义 Docker 如何运行你的容器，然后用一条命令构建并启动应用。

你将使用 [Docker Hardened Images](/dhi/) 作为基础镜像。这些是由 Docker 维护的最小、安全的 Python 镜像。

### 创建应用

示例应用是一个极简的 FastAPI 服务，只有一个返回 JSON 问候语的端点。在一个新的 `python-docker-example` 目录中创建以下文件。若要一次性创建所有文件，可切换到文件浏览器中的 **Scaffold script（脚手架脚本）** 选项卡并复制 shell 命令。

**`python-docker-example/`**

`app.py` (new):

```python
# A minimal FastAPI application.
# The root endpoint (GET /) returns a JSON "Hello World" response.
# See https://fastapi.tiangolo.com/ for the framework reference.

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}
```

`requirements.txt` (new):

```text
# Python package dependencies for the application, pinned for reproducible builds.
# See https://pip.pypa.io/en/stable/reference/requirements-file-format/

fastapi==0.115.12
uvicorn==0.34.3
```

`.gitignore` (new):

```text
# Files and directories that Git should ignore. This is the standard Python
# template covering bytecode, build artifacts, virtual environments, and IDE
# settings. See https://git-scm.com/docs/gitignore for syntax reference.

# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
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

# Unit test / coverage reports
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

# PEP 582; used by e.g. github.com/David-OConnor/pyflow and github.com/pdm-project/pdm
__pypackages__/

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Secrets
db/password.txt
```



如果你已经安装了 Python，并想在容器化之前验证应用是否正常工作，可以在本地运行它：

```console
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
$ uvicorn app:app --reload
```

> [!NOTE]
>
> 在 Windows 上，请使用 `.venv\Scripts\activate` 激活虚拟环境，而不是 `source .venv/bin/activate`。

如果你没有安装 Python，请跳到下一节。后续步骤将在容器中运行应用，无需本地安装 Python。

### 创建 Docker 相关文件

登录 DHI 镜像仓库，以便 Docker 在构建过程中能拉取 Python 基础镜像。可用的 Python 镜像列在
[catalog](https://hub.docker.com/hardened-images/catalog/dhi/python) 中。

```console
$ docker login dhi.io
```

将以下三个文件添加到你的 `python-docker-example` 目录。`Dockerfile` 描述如何构建镜像，`compose.yaml` 定义 Docker 如何运行容器，`.dockerignore` 用于防止不需要的文件进入构建上下文。

> [!TIP]
>
> [Gordon](/ai/gordon/)，Docker 的 AI 助手，可以为你的项目生成 Docker 相关文件。让 Gordon 创建专为你的应用定制的 Dockerfile、Compose 文件以及 `.dockerignore`。

**`python-docker-example/`**

`app.py`:

```python
# A minimal FastAPI application.
# The root endpoint (GET /) returns a JSON "Hello World" response.
# See https://fastapi.tiangolo.com/ for the framework reference.

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}
```

`requirements.txt`:

```text
# Python package dependencies for the application, pinned for reproducible builds.
# See https://pip.pypa.io/en/stable/reference/requirements-file-format/

fastapi==0.115.12
uvicorn==0.34.3
```

`Dockerfile` (new):

```dockerfile
# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

# This Dockerfile uses Docker Hardened Images (DHI) for enhanced security.
# For more information, see https://docs.docker.com/dhi/

# Use the dev image to build and install dependencies.
FROM dhi.io/python:3.12-dev AS builder

WORKDIR /app

RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# this layer.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    pip install -r requirements.txt

# Use the minimal runtime image. It runs as nonroot by default.
FROM dhi.io/python:3.12

WORKDIR /app

COPY --from=builder /venv /venv
ENV PATH="/venv/bin:$PATH"

# Copy the source code into the container.
COPY . .

# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
CMD ["/venv/bin/python3", "-m", "uvicorn", "app:app", "--host=0.0.0.0", "--port=8000"]
```

`compose.yaml` (new):

```yaml
# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Docker Compose reference guide at
# https://docs.docker.com/go/compose-spec-reference/

# Here the instructions define your application as a service called "server".
# This service is built from the Dockerfile in the current directory.
# You can add other services your application may depend on here, such as a
# database or a cache. For examples, see the Awesome Compose repository:
# https://github.com/docker/awesome-compose
services:
  server:
    build:
      context: .
    ports:
      - 8000:8000
```

`.dockerignore` (new):

```text
# Include any files or directories that you don't want to be copied to your
# container here (e.g., local build artifacts, temporary files, etc.).
#
# For more help, visit the .dockerignore file reference guide at
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

`.gitignore`:

```text
# Files and directories that Git should ignore. This is the standard Python
# template covering bytecode, build artifacts, virtual environments, and IDE
# settings. See https://git-scm.com/docs/gitignore for syntax reference.

# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
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

# Unit test / coverage reports
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

# PEP 582; used by e.g. github.com/David-OConnor/pyflow and github.com/pdm-project/pdm
__pypackages__/

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Secrets
db/password.txt
```



要了解每个文件的更多信息，请参阅以下内容：

- [Dockerfile](/reference/dockerfile.md)
- [.dockerignore](/reference/dockerfile.md#dockerignore-file)
- [compose.yaml](/reference/compose-file/_index.md)

### 运行应用

在 `python-docker-example` 目录中，在终端运行以下命令。

```console
$ docker compose up --build
```

打开浏览器，在 [http://localhost:8000](http://localhost:8000) 查看应用。你应该会看到一个简易的 FastAPI 应用。

在终端中，按 `ctrl`+`c` 停止应用。

#### 在后台运行应用

你可以通过添加 `-d` 选项，让应用在终端之外以分离（detached）模式运行。在 `python-docker-example` 目录中，在终端运行以下命令。

```console
$ docker compose up --build -d
```

打开浏览器，在 [http://localhost:8000](http://localhost:8000) 查看应用。

要查看 OpenAPI 文档，可以访问 [http://localhost:8000/docs](http://localhost:8000/docs)。

你应该会看到一个简易的 FastAPI 应用。

在终端中，运行以下命令以停止应用。

```console
$ docker compose down
```

有关 Compose 命令的更多信息，请参阅 [Compose CLI
reference](/reference/cli/docker/compose/)。

## Use containers for Python development

### 先决条件

完成 [Containerize a Python application](#containerize-a-python-application)。

### 概述

一旦你的应用在容器中运行，下一步就是让容器化的开发循环成为你日常开发工作流的一部分。代码变更应当快速生效，而应用依赖的服务（例如数据库）应当与它一同运行。

在本节中，你将扩展上一节的项目：向 `compose.yaml` 中添加一个 PostgreSQL 数据库服务，将数据库数据持久化到命名卷（named volume），并启用 Compose Watch，使你保存在编辑器中的修改无需手动重建即可被运行中的容器获取。

### 更新应用

你将更新应用以连接 PostgreSQL 数据库。继续在 `python-docker-example` 目录中工作。

替换 `app.py` 和 `requirements.txt`，并添加一个包含以下内容的新的 `config.py` 文件。

> [!NOTE]
>
> 完成此步骤后，应用还无法运行。它尝试连接一个尚不存在的 PostgreSQL 数据库。接下来两节将添加数据库服务以及驱动所有内容一起运行所需的 Docker 配置。

**`python-docker-example/`**

`app.py` (modified):

```python
# FastAPI application backed by a PostgreSQL database via SQLModel.
# The FastAPI lifespan handler creates database tables at startup.
# Endpoints: GET / (greeting), POST /heroes/ (create), GET /heroes/ (list).
# See https://fastapi.tiangolo.com/ and https://sqlmodel.tiangolo.com/

from collections.abc import AsyncGenerator, Sequence
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select

from config import settings


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)


engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def hello() -> str:
    return "Hello, Docker!"


@app.post("/heroes/")
def create_hero(hero: Hero) -> Hero:
    with Session(engine) as session:
        session.add(hero)
        session.commit()
        session.refresh(hero)
        return hero


@app.get("/heroes/")
def read_heroes() -> Sequence[Hero]:
    with Session(engine) as session:
        heroes = session.exec(select(Hero)).all()
        return heroes
```

`config.py` (new):

```python
# Pydantic settings that read PostgreSQL connection details from the
# environment. Supports a password file (Docker secrets) via
# POSTGRES_PASSWORD_FILE in addition to POSTGRES_PASSWORD.
# See https://docs.pydantic.dev/latest/concepts/pydantic_settings/

import os
from typing import Any

from pydantic import (
    PostgresDsn,
    computed_field,
    field_validator,
    model_validator,
)
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str | None = None
    POSTGRES_PASSWORD_FILE: str | None = None
    POSTGRES_DB: str

    @model_validator(mode="before")
    @classmethod
    def check_postgres_password(cls, data: Any) -> Any:
        """Validate that either POSTGRES_PASSWORD or POSTGRES_PASSWORD_FILE is set."""
        if isinstance(data, dict):
            password_file: str | None = data.get("POSTGRES_PASSWORD_FILE")  # type: ignore
            password: str | None = data.get("POSTGRES_PASSWORD")  # type: ignore
            if password_file is None and password is None:
                raise ValueError(
                    "At least one of POSTGRES_PASSWORD_FILE and POSTGRES_PASSWORD must be set."
                )
        return data  # type: ignore

    @field_validator("POSTGRES_PASSWORD_FILE", mode="before")
    @classmethod
    def read_password_from_file(cls, v: str | None) -> str | None:
        if v is not None:
            file_path = v
            if os.path.exists(file_path):
                with open(file_path) as file:
                    return file.read().strip()
            raise ValueError(f"Password file {file_path} does not exist.")
        return v

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        url = MultiHostUrl.build(
            scheme="postgresql+psycopg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD
            if self.POSTGRES_PASSWORD
            else self.POSTGRES_PASSWORD_FILE,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )
        return PostgresDsn(url)


settings = Settings()  # type: ignore
```

`requirements.txt` (modified):

```text
# Python package dependencies for the application, pinned for reproducible builds.
# See https://pip.pypa.io/en/stable/reference/requirements-file-format/

fastapi==0.115.12
sqlmodel==0.0.24
psycopg[binary]==3.2.9
pydantic-settings==2.9.1
uvicorn==0.34.3
```

`Dockerfile`:

```dockerfile
# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

# This Dockerfile uses Docker Hardened Images (DHI) for enhanced security.
# For more information, see https://docs.docker.com/dhi/

# Use the dev image to build and install dependencies.
FROM dhi.io/python:3.12-dev AS builder

WORKDIR /app

RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# this layer.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    pip install -r requirements.txt

# Use the minimal runtime image. It runs as nonroot by default.
FROM dhi.io/python:3.12

WORKDIR /app

COPY --from=builder /venv /venv
ENV PATH="/venv/bin:$PATH"

# Copy the source code into the container.
COPY . .

# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
CMD ["/venv/bin/python3", "-m", "uvicorn", "app:app", "--host=0.0.0.0", "--port=8000"]
```

`compose.yaml`:

```yaml
# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Docker Compose reference guide at
# https://docs.docker.com/go/compose-spec-reference/

# Here the instructions define your application as a service called "server".
# This service is built from the Dockerfile in the current directory.
# You can add other services your application may depend on here, such as a
# database or a cache. For examples, see the Awesome Compose repository:
# https://github.com/docker/awesome-compose
services:
  server:
    build:
      context: .
    ports:
      - 8000:8000
```

`.dockerignore`:

```text
# Include any files or directories that you don't want to be copied to your
# container here (e.g., local build artifacts, temporary files, etc.).
#
# For more help, visit the .dockerignore file reference guide at
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

`.gitignore`:

```text
# Files and directories that Git should ignore. This is the standard Python
# template covering bytecode, build artifacts, virtual environments, and IDE
# settings. See https://git-scm.com/docs/gitignore for syntax reference.

# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
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

# Unit test / coverage reports
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

# PEP 582; used by e.g. github.com/David-OConnor/pyflow and github.com/pdm-project/pdm
__pypackages__/

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Secrets
db/password.txt
```



### 更新 Docker 相关文件

将 `Dockerfile` 和 `compose.yaml` 替换为以下内容。

**`python-docker-example/`**

`app.py`:

```python
# FastAPI application backed by a PostgreSQL database via SQLModel.
# The FastAPI lifespan handler creates database tables at startup.
# Endpoints: GET / (greeting), POST /heroes/ (create), GET /heroes/ (list).
# See https://fastapi.tiangolo.com/ and https://sqlmodel.tiangolo.com/

from collections.abc import AsyncGenerator, Sequence
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select

from config import settings


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)


engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def hello() -> str:
    return "Hello, Docker!"


@app.post("/heroes/")
def create_hero(hero: Hero) -> Hero:
    with Session(engine) as session:
        session.add(hero)
        session.commit()
        session.refresh(hero)
        return hero


@app.get("/heroes/")
def read_heroes() -> Sequence[Hero]:
    with Session(engine) as session:
        heroes = session.exec(select(Hero)).all()
        return heroes
```

`config.py`:

```python
# Pydantic settings that read PostgreSQL connection details from the
# environment. Supports a password file (Docker secrets) via
# POSTGRES_PASSWORD_FILE in addition to POSTGRES_PASSWORD.
# See https://docs.pydantic.dev/latest/concepts/pydantic_settings/

import os
from typing import Any

from pydantic import (
    PostgresDsn,
    computed_field,
    field_validator,
    model_validator,
)
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str | None = None
    POSTGRES_PASSWORD_FILE: str | None = None
    POSTGRES_DB: str

    @model_validator(mode="before")
    @classmethod
    def check_postgres_password(cls, data: Any) -> Any:
        """Validate that either POSTGRES_PASSWORD or POSTGRES_PASSWORD_FILE is set."""
        if isinstance(data, dict):
            password_file: str | None = data.get("POSTGRES_PASSWORD_FILE")  # type: ignore
            password: str | None = data.get("POSTGRES_PASSWORD")  # type: ignore
            if password_file is None and password is None:
                raise ValueError(
                    "At least one of POSTGRES_PASSWORD_FILE and POSTGRES_PASSWORD must be set."
                )
        return data  # type: ignore

    @field_validator("POSTGRES_PASSWORD_FILE", mode="before")
    @classmethod
    def read_password_from_file(cls, v: str | None) -> str | None:
        if v is not None:
            file_path = v
            if os.path.exists(file_path):
                with open(file_path) as file:
                    return file.read().strip()
            raise ValueError(f"Password file {file_path} does not exist.")
        return v

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        url = MultiHostUrl.build(
            scheme="postgresql+psycopg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD
            if self.POSTGRES_PASSWORD
            else self.POSTGRES_PASSWORD_FILE,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )
        return PostgresDsn(url)


settings = Settings()  # type: ignore
```

`requirements.txt`:

```text
# Python package dependencies for the application, pinned for reproducible builds.
# See https://pip.pypa.io/en/stable/reference/requirements-file-format/

fastapi==0.115.12
sqlmodel==0.0.24
psycopg[binary]==3.2.9
pydantic-settings==2.9.1
uvicorn==0.34.3
```

`Dockerfile` (modified):

```dockerfile
# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

# This Dockerfile uses Docker Hardened Images (DHI) for enhanced security.
# For more information, see https://docs.docker.com/dhi/

# Use the dev image to build and install dependencies.
# The builder stage is also used directly in development (see compose.yaml).
FROM dhi.io/python:3.12-dev AS builder

WORKDIR /app

RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them
# into this layer.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    pip install -r requirements.txt

# Copy the source code into the container.
COPY . .

# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
CMD ["/venv/bin/python3", "-m", "uvicorn", "app:app", "--host=0.0.0.0", "--port=8000"]


# Use the minimal runtime image for production. It runs as nonroot by default.
FROM dhi.io/python:3.12

WORKDIR /app

COPY --from=builder /venv /venv
ENV PATH="/venv/bin:$PATH"

COPY --from=builder /app .

EXPOSE 8000

CMD ["/venv/bin/python3", "-m", "uvicorn", "app:app", "--host=0.0.0.0", "--port=8000"]
```

`compose.yaml` (modified):

```yaml
services:
  # Application service. The `target: builder` line builds the development
  # image (includes a shell and tools); the production stage of the
  # Dockerfile is unused in development.
  server:
    build:
      context: .
      target: builder
    ports:
      - 8000:8000
```

`.dockerignore`:

```text
# Include any files or directories that you don't want to be copied to your
# container here (e.g., local build artifacts, temporary files, etc.).
#
# For more help, visit the .dockerignore file reference guide at
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

`.gitignore`:

```text
# Files and directories that Git should ignore. This is the standard Python
# template covering bytecode, build artifacts, virtual environments, and IDE
# settings. See https://git-scm.com/docs/gitignore for syntax reference.

# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
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

# Unit test / coverage reports
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

# PEP 582; used by e.g. github.com/David-OConnor/pyflow and github.com/pdm-project/pdm
__pypackages__/

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Secrets
db/password.txt
```



#### 关于这些改动

`Dockerfile` 的构建（builder）阶段现在包含了 `COPY . .` 和 `CMD` 指令，使其可以直接运行。这让 Compose 在开发期间直接以构建阶段为目标，而无需重建生产阶段。底部的生产阶段保持不变，仍然生成一个最小、以 nonroot 身份运行的运行时镜像用于发布。

在 `compose.yaml` 中，新增的 `target: builder` 行告诉 Compose 在开发期间构建并运行 Dockerfile 的构建阶段。与生产用的精简镜像不同，开发镜像包含 shell 和额外的工具，便于调试。如果你需要在运行中的生产容器中获取 shell，请改用 [Docker Debug](/reference/cli/docker/debug/)。

### 添加本地数据库并持久化数据

你可以使用容器来搭建本地服务，例如数据库。在本节中，你将更新 `compose.yaml` 文件以定义一个数据库服务和一个用于持久化数据的卷，并添加一个保存数据库密码的 `db/password.txt` 文件。

**`python-docker-example/`**

`app.py`:

```python
# FastAPI application backed by a PostgreSQL database via SQLModel.
# The FastAPI lifespan handler creates database tables at startup.
# Endpoints: GET / (greeting), POST /heroes/ (create), GET /heroes/ (list).
# See https://fastapi.tiangolo.com/ and https://sqlmodel.tiangolo.com/

from collections.abc import AsyncGenerator, Sequence
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select

from config import settings


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)


engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def hello() -> str:
    return "Hello, Docker!"


@app.post("/heroes/")
def create_hero(hero: Hero) -> Hero:
    with Session(engine) as session:
        session.add(hero)
        session.commit()
        session.refresh(hero)
        return hero


@app.get("/heroes/")
def read_heroes() -> Sequence[Hero]:
    with Session(engine) as session:
        heroes = session.exec(select(Hero)).all()
        return heroes
```

`config.py`:

```python
# Pydantic settings that read PostgreSQL connection details from the
# environment. Supports a password file (Docker secrets) via
# POSTGRES_PASSWORD_FILE in addition to POSTGRES_PASSWORD.
# See https://docs.pydantic.dev/latest/concepts/pydantic_settings/

import os
from typing import Any

from pydantic import (
    PostgresDsn,
    computed_field,
    field_validator,
    model_validator,
)
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str | None = None
    POSTGRES_PASSWORD_FILE: str | None = None
    POSTGRES_DB: str

    @model_validator(mode="before")
    @classmethod
    def check_postgres_password(cls, data: Any) -> Any:
        """Validate that either POSTGRES_PASSWORD or POSTGRES_PASSWORD_FILE is set."""
        if isinstance(data, dict):
            password_file: str | None = data.get("POSTGRES_PASSWORD_FILE")  # type: ignore
            password: str | None = data.get("POSTGRES_PASSWORD")  # type: ignore
            if password_file is None and password is None:
                raise ValueError(
                    "At least one of POSTGRES_PASSWORD_FILE and POSTGRES_PASSWORD must be set."
                )
        return data  # type: ignore

    @field_validator("POSTGRES_PASSWORD_FILE", mode="before")
    @classmethod
    def read_password_from_file(cls, v: str | None) -> str | None:
        if v is not None:
            file_path = v
            if os.path.exists(file_path):
                with open(file_path) as file:
                    return file.read().strip()
            raise ValueError(f"Password file {file_path} does not exist.")
        return v

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        url = MultiHostUrl.build(
            scheme="postgresql+psycopg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD
            if self.POSTGRES_PASSWORD
            else self.POSTGRES_PASSWORD_FILE,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )
        return PostgresDsn(url)


settings = Settings()  # type: ignore
```

`requirements.txt`:

```text
# Python package dependencies for the application, pinned for reproducible builds.
# See https://pip.pypaia/en/stable/reference/requirements-file-format/

fastapi==0.115.12
sqlmodel==0.0.24
psycopg[binary]==3.2.9
pydantic-settings==2.9.1
uvicorn==0.34.3
```

`Dockerfile`:

```dockerfile
# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

# This Dockerfile uses Docker Hardened Images (DHI) for enhanced security.
# For more information, see https://docs.docker.com/dhi/

# Use the dev image to build and install dependencies.
# The builder stage is also used directly in development (see compose.yaml).
FROM dhi.io/python:3.12-dev AS builder

WORKDIR /app

RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them
# into this layer.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    pip install -r requirements.txt

# Copy the source code into the container.
COPY . .

# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
CMD ["/venv/bin/python3", "-m", "uvicorn", "app:app", "--host=0.0.0.0", "--port=8000"]


# Use the minimal runtime image for production. It runs as nonroot by default.
FROM dhi.io/python:3.12

WORKDIR /app

COPY --from=builder /venv /venv
ENV PATH="/venv/bin:$PATH"

COPY --from=builder /app .

EXPOSE 8000

CMD ["/venv/bin/python3", "-m", "uvicorn", "app:app", "--host=0.0.0.0", "--port=8000"]
```

`compose.yaml` (modified):

```yaml
services:
  # Application service. The `target: builder` line builds the development
  # image (includes a shell and tools); the production stage of the
  # Dockerfile is unused in development.
  server:
    build:
      context: .
      target: builder
    ports:
      - 8000:8000
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
  # Database service. Reads the password from a Docker secret mounted at
  # /run/secrets/db-password. Compose waits for the healthcheck to pass
  # before starting the server, via the server's depends_on.
  db:
    image: dhi.io/postgres:18
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

`db/password.txt` (new):

```text
mysecretpassword
```

`.dockerignore`:

```text
# Include any files or directories that you don't want to be copied to your
# container here (e.g., local build artifacts, temporary files, etc.).
#
# For more help, visit the .dockerignore file reference guide at
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

`.gitignore`:

```text
# Files and directories that Git should ignore. This is the standard Python
# template covering bytecode, build artifacts, virtual environments, and IDE
# settings. See https://git-scm.com/docs/gitignore for syntax reference.

# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
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

# Unit test / coverage reports
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

# PEP 582; used by e.g. github.com/David-OConnor/pyflow and github.com/pdm-project/pdm
__pypackages__/

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Secrets
db/password.txt
```



> [!NOTE]
>
> 要了解 Compose 文件中各指令的更多信息，请参阅 [Compose file
> reference](/reference/compose-file/)。

现在，运行以下 `docker compose up` 命令来启动你的应用。

```console
$ docker compose up --build
```

现在测试你的 API 端点。打开一个新终端，使用 curl 命令向服务器发起请求：

用 POST 请求创建一个对象：

```console
$ curl -X 'POST' \
  'http://localhost:8000/heroes/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "id": 1,
  "name": "my hero",
  "secret_name": "austing",
  "age": 12
}'
```

你应该会收到以下响应：

```json
{
  "age": 12,
  "id": 1,
  "name": "my hero",
  "secret_name": "austing"
}
```

现在发起一个 GET 请求：

```console
$ curl -X 'GET' \
  'http://localhost:8000/heroes/' \
  -H 'accept: application/json'
```

你应该会收到与上面相同的响应，因为数据库中只有这一个对象。

```json
{
  "age": 12,
  "id": 1,
  "name": "my hero",
  "secret_name": "austing"
}
```

在终端中按 `ctrl+c` 停止你的应用。

### 自动更新服务

使用 Compose Watch 在你编辑并保存代码时自动更新运行中的 Compose 服务。有关 Compose Watch 的更多细节，请参阅 [Use Compose
Watch](/manuals/compose/how-tos/file-watch.md)。

在 IDE 或文本编辑器中打开你的 `compose.yaml` 文件，并添加高亮的 Compose Watch 指令。

**`python-docker-example/`**

`app.py`:

```python
# FastAPI application backed by a PostgreSQL database via SQLModel.
# The FastAPI lifespan handler creates database tables at startup.
# Endpoints: GET / (greeting), POST /heroes/ (create), GET /heroes/ (list).
# See https://fastapi.tiangolo.com/ and https://sqlmodel.tiangolo.com/

from collections.abc import AsyncGenerator, Sequence
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select

from config import settings


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)


engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def hello() -> str:
    return "Hello, Docker!"


@app.post("/heroes/")
def create_hero(hero: Hero) -> Hero:
    with Session(engine) as session:
        session.add(hero)
        session.commit()
        session.refresh(hero)
        return hero


@app.get("/heroes/")
def read_heroes() -> Sequence[Hero]:
    with Session(engine) as session:
        heroes = session.exec(select(Hero)).all()
        return heroes
```

`config.py`:

```python
# Pydantic settings that read PostgreSQL connection details from the
# environment. Supports a password file (Docker secrets) via
# POSTGRES_PASSWORD_FILE in addition to POSTGRES_PASSWORD.
# See https://docs.pydantic.dev/latest/concepts/pydantic_settings/

import os
from typing import Any

from pydantic import (
    PostgresDsn,
    computed_field,
    field_validator,
    model_validator,
)
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str | None = None
    POSTGRES_PASSWORD_FILE: str | None = None
    POSTGRES_DB: str

    @model_validator(mode="before")
    @classmethod
    def check_postgres_password(cls, data: Any) -> Any:
        """Validate that either POSTGRES_PASSWORD or POSTGRES_PASSWORD_FILE is set."""
        if isinstance(data, dict):
            password_file: str | None = data.get("POSTGRES_PASSWORD_FILE")  # type: ignore
            password: str | None = data.get("POSTGRES_PASSWORD")  # type: ignore
            if password_file is None and password is None:
                raise ValueError(
                    "At least one of POSTGRES_PASSWORD_FILE and POSTGRES_PASSWORD must be set."
                )
        return data  # type: ignore

    @field_validator("POSTGRES_PASSWORD_FILE", mode="before")
    @classmethod
    def read_password_from_file(cls, v: str | None) -> str | None:
        if v is not None:
            file_path = v
            if os.path.exists(file_path):
                with open(file_path) as file:
                    return file.read().strip()
            raise ValueError(f"Password file {file_path} does not exist.")
        return v

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        url = MultiHostUrl.build(
            scheme="postgresql+psycopg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD
            if self.POSTGRES_PASSWORD
            else self.POSTGRES_PASSWORD_FILE,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )
        return PostgresDsn(url)


settings = Settings()  # type: ignore
```

`requirements.txt`:

```text
# Python package dependencies for the application, pinned for reproducible builds.
# See https://pip.pypa.io/en/stable/reference/requirements-file-format/

fastapi==0.115.12
sqlmodel==0.0.24
psycopg[binary]==3.2.9
pydantic-settings==2.9.1
uvicorn==0.34.3
```

`Dockerfile`:

```dockerfile
# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

# This Dockerfile uses Docker Hardened Images (DHI) for enhanced security.
# For more information, see https://docs.docker.com/dhi/

# Use the dev image to build and install dependencies.
# The builder stage is also used directly in development (see compose.yaml).
FROM dhi.io/python:3.12-dev AS builder

WORKDIR /app

RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them
# into this layer.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    pip install -r requirements.txt

# Copy the source code into the container.
COPY . .

# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
CMD ["/venv/bin/python3", "-m", "uvicorn", "app:app", "--host=0.0.0.0", "--port=8000"]


# Use the minimal runtime image for production. It runs as nonroot by default.
FROM dhi.io/python:3.12

WORKDIR /app

COPY --from=builder /venv /venv
ENV PATH="/venv/bin:$PATH"

COPY --from=builder /app .

EXPOSE 8000

CMD ["/venv/bin/python3", "-m", "uvicorn", "app:app", "--host=0.0.0.0", "--port=8000"]
```

`compose.yaml` (modified):

```yaml
services:
  # Application service. The `target: builder` line builds the development
  # image (includes a shell and tools); the production stage of the
  # Dockerfile is unused in development.
  server:
    build:
      context: .
      target: builder
    ports:
      - 8000:8000
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
    image: dhi.io/postgres:18
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

`db/password.txt`:

```text
mysecretpassword
```

`.dockerignore`:

```text
# Include any files or directories that you don't want to be copied to your
# container here (e.g., local build artifacts, temporary files, etc.).
#
# For more help, visit the .dockerignore file reference guide at
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

`.gitignore`:

```text
# Files and directories that Git should ignore. This is the standard Python
# template covering bytecode, build artifacts, virtual environments, and IDE
# settings. See https://git-scm.com/docs/gitignore for syntax reference.

# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
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

# Unit test / coverage reports
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

# PEP 582; used by e.g. github.com/David-OConnor/pyflow and github.com/pdm-project/pdm
__pypackages__/

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Secrets
db/password.txt
```



在终端中运行以下命令，使用 Compose Watch 运行你的应用。

```console
$ docker compose watch
```

在终端中，用 curl 访问应用以获取响应。

```console
$ curl http://localhost:8000
Hello, Docker!
```

现在，你在本地机器上对应用源文件所做的任何修改都会立即反映到运行中的容器中。

在 IDE 或文本编辑器中打开 `python-docker-example/app.py`，通过多加几个感叹号来更新 `Hello, Docker!` 字符串。

```diff
-    return 'Hello, Docker!'
+    return 'Hello, Docker!!!'
```

将改动保存到 `app.py`，然后等待几秒让应用重新构建。再次用 curl 访问应用，确认更新后的文本已出现。

```console
$ curl http://localhost:8000
Hello, Docker!!!
```

在终端中按 `ctrl+c` 停止你的应用。

## Linting, formatting, and type checking for Python

### 先决条件

完成 [Develop your app](#use-containers-for-python-development)。本主题需要本地安装 Python，因为这里介绍的工具和 Git 钩子都运行在你的主机上。如果你不想在本地安装 Python，可以跳过本主题，也可以在 CI 中运行相同的检查。

### 概述

代码检查（linting）、格式化和类型检查是在代码运行前自动捕获 bug、强制执行代码风格并发现类型错误的手段。在每次提交、CI 以及编辑器中运行它们，可以在问题还容易修复时就尽早发现。

在本节中，你将为自己的 Python 应用配置三个工具。Ruff 在单次快速的传递中完成代码检查和格式化。Pyright 静态地检查代码中的类型错误。Pre-commit 钩子会在每次 Git 提交前自动运行这两者，从而在你提交之前就在本地捕获问题。

### 使用 Ruff 进行代码检查与格式化

Ruff 是一个用 Rust 编写的极快的 Python 代码检查器和格式化器。它用一个统一的工具替代了 flake8、isort 和 black 等多个工具。

在你的 `python-docker-example` 目录中创建一个 `pyproject.toml` 文件：

**`python-docker-example/`**

`pyproject.toml` (new):

```toml
# Configuration for code-quality tools.
# - [tool.ruff]: linting and formatting (https://docs.astral.sh/ruff/)
# - [tool.pyright]: static type checking (https://microsoft.github.io/pyright/)

[tool.ruff]
target-version = "py312"

[tool.ruff.lint]
select = [
    "E",  # pycodestyle errors
    "W",  # pycodestyle warnings
    "F",  # pyflakes
    "I",  # isort
    "B",  # flake8-bugbear
    "C4",  # flake8-comprehensions
    "UP",  # pyupgrade
    "ARG001", # unused arguments in functions
]
ignore = [
    "E501",  # line too long, handled by black
    "B008",  # do not perform function calls in argument defaults
    "W191",  # indentation contains tabs
    "B904",  # Allow raising exceptions without from e, for HTTPException
]
```



安装 Ruff：

```console
$ pip install ruff
```

如果你正在使用虚拟环境，请确保其已激活，以便 `ruff` 命令可用。

运行以下命令来检查并格式化你的代码：

```console
# Check for errors
$ ruff check .

# Automatically fix fixable errors
$ ruff check --fix .

# Format code
$ ruff format .
```

### 使用 Pyright 进行类型检查

Pyright 是一个快速的 Python 静态类型检查器，能很好地支持现代 Python 特性。

更新 `pyproject.toml`，在底部添加 Pyright 配置。

**`python-docker-example/`**

`pyproject.toml` (modified):

```toml
# Configuration for code-quality tools.
# - [tool.ruff]: linting and formatting (https://docs.astral.sh/ruff/)
# - [tool.pyright]: static type checking (https://microsoft.github.io/pyright/)

[tool.ruff]
target-version = "py312"

[tool.ruff.lint]
select = [
    "E",  # pycodestyle errors
    "W",  # pycodestyle warnings
    "F",  # pyflakes
    "I",  # isort
    "B",  # flake8-bugbear
    "C4",  # flake8-comprehensions
    "UP",  # pyupgrade
    "ARG001", # unused arguments in functions
]
ignore = [
    "E501",  # line too long, handled by black
    "B008",  # do not perform function calls in argument defaults
    "W191",  # indentation contains tabs
    "B904",  # Allow raising exceptions without from e, for HTTPException
]

[tool.pyright]
typeCheckingMode = "strict"
pythonVersion = "3.12"
exclude = [".venv"]
```



安装 Pyright 并运行它：

```console
$ pip install pyright
$ pyright
```

### 配置 pre-commit 钩子

Pre-commit 钩子会在你本地机器上每次提交前自动运行检查。在你的 `python-docker-example` 目录中创建一个 `.pre-commit-config.yaml` 文件来配置 Ruff 钩子：

**`python-docker-example/`**

`.pre-commit-config.yaml` (new):

```yaml
# Pre-commit hook configuration. Runs Ruff (lint + format) on every
# `git commit`. See https://pre-commit.com/

repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.15.15
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```



安装与使用方法：

```console
$ pip install pre-commit
$ pre-commit install
$ git commit -m "Test commit"  # Automatically runs checks
```

### 小结

在本节中，你学习了如何：

- 配置并使用 Ruff 进行代码检查与格式化
- 搭建 Pyright 进行静态类型检查
- 用 pre-commit 钩子自动化检查

这些工具有助于在开发早期保持代码质量并捕获错误。

相关信息：

- [Ruff 文档](https://docs.astral.sh/ruff/)
- [Pyright 文档](https://microsoft.github.io/pyright/)
- [pre-commit 框架](https://pre-commit.com/)

### 下一步

- 自定义代码检查规则以匹配你团队的风格偏好
- 探索进阶的类型检查功能

