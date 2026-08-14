# .NET 语言专属指南


.NET 入门指南将教你如何使用 Docker 创建一个容器化的 .NET 应用。在本指南中，你将学习如何：

- 将 .NET 应用容器化并运行
- 搭建本地环境以使用容器开发 .NET 应用
- 使用容器为 .NET 应用运行测试

完成 .NET 入门模块后，你应该能够根据本指南中提供的示例和说明，将自己的 .NET 应用容器化。

首先，将一个现有的 .NET 应用容器化。

## 将 .NET 应用容器化

### 先决条件

- 你已安装最新版本的 [Docker Desktop](/get-started/get-docker.md)。
- 你有一个 [git 客户端](https://git-scm.com/downloads)。本节中的示例使用基于命令行的 git 客户端，但你可以使用任何客户端。

### 概述

本节将带你完成将一个 .NET 应用容器化并运行的过程。

### 获取示例应用

在本指南中，你将使用一个预先构建好的 .NET 应用。该应用类似于 Docker 博客文章 [使用 Docker Desktop 构建多容器 .NET 应用](https://www.docker.com/blog/building-multi-container-net-app-using-docker-desktop/) 中构建的应用。

打开终端，切换到你想工作的目录，并运行以下命令克隆仓库。

```console
$ git clone https://github.com/docker/docker-dotnet-sample
```

### 创建 Docker 资源

既然已经有了一个应用，你就可以创建将其容器化所需的 Docker 资源。你可以选择使用官方的 .NET 镜像，或者使用 Docker Hardened Images（DHI）。

> [!TIP]
>
> [Gordon](/ai/gordon/) 是 Docker 的 AI 助手，可以为你的项目生成 Docker 资源。让 Gordon 为你的应用创建 Dockerfile、Compose 文件和 `.dockerignore`。

> [Docker Hardened Images（DHI）](https://docs.docker.com/dhi/) 是由 Docker 维护的最小化、安全且可用于生产的基础镜像与应用镜像。建议使用 DHI 以获得更好的安全性——它们旨在减少漏洞并简化合规性。

**使用 Docker Hardened Images**



适用于 .NET 的 Docker Hardened Images（DHI）可在 [Docker Hardened Images 目录](https://hub.docker.com/hardened-images/catalog/dhi/aspnetcore) 中获取。Docker Hardened Images 对所有人免费提供，无需订阅。在登录到 DHI 镜像仓库后，你可以像使用其他任何 Docker 镜像一样拉取和使用它们。更多信息，请参阅 [DHI 快速入门](/dhi/get-started/) 指南。

1. 登录到 DHI 镜像仓库：

   ```console
   $ docker login dhi.io
   ```

2. 拉取 .NET SDK DHI（查看目录中可用的版本）：

   ```console
   $ docker pull dhi.io/dotnet:10-sdk
   ```

3. 拉取 ASP.NET Core 运行时 DHI（查看目录中可用的版本）：
   ```console
   $ docker pull dhi.io/aspnetcore:10
   ```

在你的 `docker-dotnet-sample` 目录中创建以下文件。

```dockerfile {collapse=true,title=Dockerfile}
# syntax=docker/dockerfile:1

FROM --platform=$BUILDPLATFORM dhi.io/dotnet:10-sdk AS build
ARG TARGETARCH
COPY . /source
WORKDIR /source/src
RUN --mount=type=cache,id=nuget,target=/root/.nuget/packages \
    dotnet publish -a ${TARGETARCH/amd64/x64} --use-current-runtime --self-contained false -o /app

FROM dhi.io/aspnetcore:10 AS final
WORKDIR /app
COPY --from=build /app .
ENTRYPOINT ["dotnet", "myWebApp.dll"]
```

> [!NOTE]
>
> DHI 运行时镜像已经以非 root 用户（`nonroot`，UID 65532）运行，因此无需在你的 Dockerfile 中创建用户或指定 `USER`。这减少了攻击面并简化了你的配置。

```yaml {collapse=true,title=compose.yaml}
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
      target: final
    ports:
      - 8080:8080

# The commented out section below is an example of how to define a PostgreSQL
# database that your application can use. `depends_on` tells Docker Compose to
# start the database before your application. The `db-data` volume persists the
# database data between container restarts. The `db-password` secret is used
# to set the database password. You must create `db/password.txt` and add
# a password of your choosing to it before running `docker compose up`.
#     depends_on:
#       db:
#         condition: service_healthy
#   db:
#     image: postgres
#     restart: always
#     user: postgres
#     secrets:
#       - db-password
#     volumes:
#       - db-data:/var/lib/postgresql/data
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

```text {collapse=true,title=".dockerignore"}
# Include any files or directories that you don't want to be copied to your
# container here (e.g., local build artifacts, temporary files, etc.).
#
# For more help, visit the .dockerignore file reference guide at
# https://docs.docker.com/go/build-context-dockerignore/

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

**使用官方 .NET 10 镜像**



在你的 `docker-dotnet-sample` 目录中创建以下文件。

```dockerfile {collapse=true,title=Dockerfile}
# syntax=docker/dockerfile:1

FROM --platform=$BUILDPLATFORM mcr.microsoft.com/dotnet/sdk:10.0-alpine AS build
ARG TARGETARCH
COPY . /source
WORKDIR /source/src
RUN --mount=type=cache,id=nuget,target=/root/.nuget/packages \
    dotnet publish -a ${TARGETARCH/amd64/x64} --use-current-runtime --self-contained false -o /app

FROM mcr.microsoft.com/dotnet/aspnet:10.0-alpine AS final
WORKDIR /app
COPY --from=build /app .
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser
USER appuser
ENTRYPOINT ["dotnet", "myWebApp.dll"]
```

```yaml {collapse=true,title=compose.yaml}
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
      target: final
    ports:
      - 8080:8080

# The commented out section below is an example of how to define a PostgreSQL
# database that your application can use. `depends_on` tells Docker Compose to
# start the database before your application. The `db-data` volume persists the
# database data between container restarts. The `db-password` secret is used
# to set the database password. You must create `db/password.txt` and add
# a password of your choosing to it before running `docker compose up`.
#     depends_on:
#       db:
#         condition: service_healthy
#   db:
#     image: postgres
#     restart: always
#     user: postgres
#     secrets:
#       - db-password
#     volumes:
#       - db-data:/var/lib/postgresql/data
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

```text {collapse=true,title=".dockerignore"}
# Include any files or directories that you don't want to be copied to your
# container here (e.g., local build artifacts, temporary files, etc.).
#
# For more help, visit the .dockerignore file reference guide at
# https://docs.docker.com/go/build-context-dockerignore/

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



现在你的 `docker-dotnet-sample` 目录中应当包含以下内容。

```text
├── docker-dotnet-sample/
│ ├── .git/
│ ├── src/
│ ├── .dockerignore
│ ├── compose.yaml
│ ├── Dockerfile
│ └── README.md
```

要了解这些文件的更多信息，请参阅以下内容：

- [Dockerfile](/reference/dockerfile.md)
- [.dockerignore](/reference/dockerfile.md#dockerignore-file)
- [compose.yaml](/reference/compose-file/_index.md)

### 运行应用

在 `docker-dotnet-sample` 目录中，在终端运行以下命令。

```console
$ docker compose up --build
```

打开浏览器，在 [http://localhost:8080](http://localhost:8080) 查看应用。你应该会看到一个简易的 Web 应用。

在终端中，按 `ctrl`+`c` 停止应用。

#### 在后台运行应用

你可以通过添加 `-d` 选项，让应用在终端分离（detached）模式下运行。在 `docker-dotnet-sample` 目录中，在终端运行以下命令。

```console
$ docker compose up --build -d
```

打开浏览器，在 [http://localhost:8080](http://localhost:8080) 查看应用。你应该会看到一个简易的 Web 应用。

在终端中，运行以下命令以停止应用。

```console
$ docker compose down
```

关于 Compose 命令的更多信息，请参阅 [Compose CLI 参考](/reference/cli/docker/compose/)。

## 使用容器进行 .NET 开发

### 先决条件

完成 [将 .NET 应用容器化](#containerize-a-net-application)。

### 概述

在本节中，你将学习如何为容器化的应用搭建开发环境。这包括：

- 添加本地数据库并持久化数据
- 配置 Compose，在你编辑并保存代码时自动更新正在运行的 Compose 服务
- 创建一个包含 .NET Core SDK 工具和依赖项的开发容器

### 更新应用

本节使用 `docker-dotnet-sample` 仓库的另一个分支，其中包含更新后的 .NET 应用。更新后的应用位于你在 [将 .NET 应用容器化](#containerize-a-net-application) 中克隆的仓库的 `add-db` 分支上。

要获取更新后的代码，你需要切换到 `add-db` 分支。对于你在 [将 .NET 应用容器化](#containerize-a-net-application) 中所做的改动，在本节中你可以用 stash 暂存它们。在终端中，于 `docker-dotnet-sample` 目录运行以下命令。

1. 暂存之前的所有改动。

   ```console
   $ git stash -u
   ```

2. 切换到包含更新后应用的新分支。

   ```console
   $ git checkout add-db
   ```

在 `add-db` 分支中，仅有 .NET 应用被更新。还没有任何 Docker 资源被更新。

现在你的 `docker-dotnet-sample` 目录中应当包含以下内容。

```text
├── docker-dotnet-sample/
│ ├── .git/
│ ├── src/
│ │ ├── Data/
│ │ ├── Models/
│ │ ├── Pages/
│ │ ├── Properties/
│ │ ├── wwwroot/
│ │ ├── appsettings.Development.json
│ │ ├── appsettings.json
│ │ ├── myWebApp.csproj
│ │ └── Program.cs
│ ├── tests/
│ │ ├── tests.csproj
│ │ ├── UnitTest1.cs
│ │ └── Usings.cs
│ ├── .dockerignore
│ ├── .gitignore
│ ├── compose.yaml
│ ├── Dockerfile
│ └── README.md
```

### 添加本地数据库并持久化数据

你可以使用容器来搭建本地服务，例如数据库。在本节中，你将更新 `compose.yaml` 文件，定义一个数据库服务以及一个用于持久化数据的卷。

在 IDE 或文本编辑器中打开 `compose.yaml` 文件。你会注意到它已经包含了一段关于 PostgreSQL 数据库和卷的注释说明。

在 IDE 或文本编辑器中打开 `docker-dotnet-sample/src/appsettings.json`。你会注意到包含全部数据库信息的连接字符串。`compose.yaml` 已经包含了这些信息，但它们处于注释状态。请取消 `compose.yaml` 文件中数据库相关说明的注释。

以下是更新后的 `compose.yaml` 文件。

```yaml {hl_lines="8-33"}
services:
  server:
    build:
      context: .
      target: final
    ports:
      - 8080:8080
    depends_on:
      db:
        condition: service_healthy
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
> 要了解 Compose 文件中这些说明的更多信息，请参阅 [Compose 文件参考](/reference/compose-file/)。

在使用 Compose 运行应用之前，请注意该 Compose 文件使用了 `secrets` 并指定了一个 `password.txt` 文件来保存数据库密码。你必须创建这个文件，因为它并未包含在源仓库中。

在 `docker-dotnet-sample` 目录中，创建一个名为 `db` 的新目录，并在该目录中创建一个名为 `password.txt` 的文件。在 IDE 或文本编辑器中打开 `password.txt`，并添加以下密码。密码必须位于单独的一行上，文件中不能有其他行。

```text
example
```

保存并关闭 `password.txt` 文件。

现在你的 `docker-dotnet-sample` 目录中应当包含以下内容。

```text
├── docker-dotnet-sample/
│ ├── .git/
│ ├── db/
│ │ └── password.txt
│ ├── src/
│ ├── tests/
│ ├── .dockerignore
│ ├── .gitignore
│ ├── compose.yaml
│ ├── Dockerfile
│ └── README.md
```

运行以下命令以启动你的应用。

```console
$ docker compose up --build
```

打开浏览器，在 [http://localhost:8080](http://localhost:8080) 查看应用。你应该会看到一个简易的 Web 应用，其中包含文本 `Student name is`。

该应用没有显示姓名，因为数据库是空的。对于这个应用，你需要访问数据库，然后添加记录。

### 向数据库添加记录

对于示例应用，你必须直接访问数据库来创建示例记录。

你可以使用 `docker exec` 命令在数据库容器内运行命令。在运行该命令之前，你必须获取数据库容器的 ID。打开一个新的终端窗口，运行以下命令列出所有正在运行的容器。

```console
$ docker container ls
```

你应该会看到类似以下的输出。

```console
CONTAINER ID   IMAGE                         COMMAND                  CREATED              STATUS                        PORTS                    NAMES
cb36e310aa7e   docker-dotnet-sample-server   "dotnet myWebApp.dll"    About a minute ago   Up About a minute             0.0.0.0:8080->8080/tcp   docker-dotnet-sample-server-1
39fdcf0aff7b   postgres:18                   "docker-entrypoint.s…"   About a minute ago   Up About a minute (healthy)   5432/tcp                 docker-dotnet-sample-db-1
```

在上例中，容器 ID 为 `39fdcf0aff7b`。运行以下命令连接到容器中的 postgres 数据库。请将容器 ID 替换为你自己的容器 ID。

```console
$ docker exec -it 39fdcf0aff7b psql -d example -U postgres
```

最后，向数据库中插入一条记录。

```console
example=# INSERT INTO "Students" ("ID", "LastName", "FirstMidName", "EnrollmentDate") VALUES (DEFAULT, 'Whale', 'Moby', '2013-03-20');
```

你应该会看到类似以下的输出。

```console
INSERT 0 1
```

通过运行 `exit` 关闭数据库连接并退出容器 shell。

```console
example=# exit
```

### 验证数据是否在数据库中持久化

打开浏览器，在 [http://localhost:8080](http://localhost:8080) 查看应用。你应该会看到一个简易的 Web 应用，其中包含文本 `Student name is Moby Whale`。

在终端中按 `ctrl+c` 停止你的应用。

在终端中运行 `docker compose rm` 移除你的容器，然后运行 `docker compose up` 再次运行你的应用。

```console
$ docker compose rm
$ docker compose up --build
```

在你的浏览器中刷新 [http://localhost:8080](http://localhost:8080)，并验证学生姓名已经持久化，即使在容器被移除并再次运行之后也是如此。

在终端中按 `ctrl+c` 停止你的应用。

### 自动更新服务

使用 Compose Watch，在你编辑并保存代码时自动更新正在运行的 Compose 服务。关于 Compose Watch 的更多详情，请参阅 [使用 Compose Watch](/manuals/compose/how-tos/file-watch.md)。

在 IDE 或文本编辑器中打开你的 `compose.yaml` 文件，然后添加 Compose Watch 说明。以下是更新后的 `compose.yaml` 文件。

```yaml {hl_lines="11-14"}
services:
  server:
    build:
      context: .
      target: final
    ports:
      - 8080:8080
    depends_on:
      db:
        condition: service_healthy
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

打开浏览器，确认应用在 [http://localhost:8080](http://localhost:8080) 运行。

现在，你本地机器上应用源文件的任何改动都会立即反映到运行中的容器中。

在 IDE 或文本编辑器中打开 `docker-dotnet-sample/src/Pages/Index.cshtml`，将第 13 行的学生姓名文本从 `Student name is` 更新为 `Student name:`。

```diff
-    <p>Student name is @Model.StudentName</p>
+    <p>Student name: @Model.StudentName</p>
```

保存对 `Index.cshtml` 的改动，然后等待几秒让应用重新构建。在你的浏览器中刷新 [http://localhost:8080](http://localhost:8080)，并确认更新后的文本已经出现。

在终端中按 `ctrl+c` 停止你的应用。

### 创建开发容器

此时，当你运行容器化的应用时，它使用的是 .NET 运行时镜像。虽然这个小镜像适合生产环境，但它缺少开发时可能需要的 SDK 工具和依赖项。此外，在开发期间，你可能不需要运行 `dotnet publish`。你可以使用多阶段构建，在同一个 Dockerfile 中为开发和生产构建各自的阶段。更多详情，请参阅 [多阶段构建](/manuals/build/building/multi-stage.md)。

向你的 Dockerfile 添加一个新的开发阶段，并更新你的 `compose.yaml` 文件以在本地开发中使用该阶段。

以下是更新后的 Dockerfile。

**使用 Docker Hardened Images**



```Dockerfile {hl_lines="10-13"}
# syntax=docker/dockerfile:1

FROM --platform=$BUILDPLATFORM dhi.io/dotnet:10-sdk AS build
ARG TARGETARCH
COPY . /source
WORKDIR /source/src
RUN --mount=type=cache,id=nuget,target=/root/.nuget/packages \
    dotnet publish -a ${TARGETARCH/amd64/x64} --use-current-runtime --self-contained false -o /app

FROM dhi.io/dotnet:10-sdk AS development
COPY . /source
WORKDIR /source/src
CMD dotnet run --no-launch-profile

FROM dhi.io/aspnetcore:10 AS final
WORKDIR /app
COPY --from=build /app .
ENTRYPOINT ["dotnet", "myWebApp.dll"]
```

**使用官方 .NET 10 镜像**



```Dockerfile {hl_lines="10-13"}
# syntax=docker/dockerfile:1

FROM --platform=$BUILDPLATFORM mcr.microsoft.com/dotnet/sdk:10.0-alpine AS build
ARG TARGETARCH
COPY . /source
WORKDIR /source/src
RUN --mount=type=cache,id=nuget,target=/root/.nuget/packages \
    dotnet publish -a ${TARGETARCH/amd64/x64} --use-current-runtime --self-contained false -o /app

FROM mcr.microsoft.com/dotnet/sdk:10.0-alpine AS development
COPY . /source
WORKDIR /source/src
CMD dotnet run --no-launch-profile

FROM mcr.microsoft.com/dotnet/aspnet:10.0-alpine AS final
WORKDIR /app
COPY --from=build /app .
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser
USER appuser
ENTRYPOINT ["dotnet", "myWebApp.dll"]
```



以下是更新后的 `compose.yaml` 文件。

```yaml {hl_lines=[5,15,16]}
services:
  server:
    build:
      context: .
      target: development
    ports:
      - 8080:8080
    depends_on:
      db:
        condition: service_healthy
    develop:
      watch:
        - action: rebuild
          path: .
    environment:
      - ASPNETCORE_ENVIRONMENT=Development
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

你的容器化应用现在将使用 SDK 镜像（DHI 为 `dhi.io/dotnet:10-sdk`，官方镜像为 `mcr.microsoft.com/dotnet/sdk:10.0-alpine`），其中包含了像 `dotnet test` 这样的开发工具。继续阅读下一节，了解如何运行 `dotnet test`。

## 在容器中运行 .NET 测试

### 先决条件

完成本指南此前所有小节，从 [将 .NET 应用容器化](#containerize-a-net-application) 开始。

### 概述

测试是现代软件开发中不可或缺的一部分。对不同开发团队而言，测试可能意味着很多事情。有单元测试、集成测试和端到端测试。在本指南中，你将了解在开发时和构建时如何在 Docker 中运行你的单元测试。

### 在本地开发时运行测试

示例应用已经在 `tests` 目录中包含一个 xUnit 测试。在本地开发时，你可以使用 Compose 来运行你的测试。

在 `docker-dotnet-sample` 目录中运行以下命令，以在容器内运行测试。

```console
$ docker compose run --build --rm server dotnet test /source/tests
```

你应该会看到包含以下内容的输出。

```console
Starting test execution, please wait...
A total of 1 test files matched the specified pattern.

Passed!  - Failed:     0, Passed:     1, Skipped:     0, Total:     1, Duration: < 1 ms - /source/tests/bin/Debug/net10.0/tests.dll (net10.0)
```

要了解该命令的更多信息，请参阅 [docker compose run](/reference/cli/docker/compose/run/)。

### 在构建时运行测试

要在构建时运行你的测试，你需要更新你的 Dockerfile。你可以创建一个运行测试的新测试阶段，或者在现有的构建阶段中运行测试。在本指南中，更新 Dockerfile 以在构建阶段中运行测试。

以下是更新后的 Dockerfile。

**使用 Docker Hardened Images**



```dockerfile {hl_lines="9"}
# syntax=docker/dockerfile:1

FROM --platform=$BUILDPLATFORM dhi.io/dotnet:10-sdk AS build
ARG TARGETARCH
COPY . /source
WORKDIR /source/src
RUN --mount=type=cache,id=nuget,target=/root/.nuget/packages \
    dotnet publish -a ${TARGETARCH/amd64/x64} --use-current-runtime --self-contained false -o /app
RUN dotnet test /source/tests

FROM dhi.io/dotnet:10-sdk AS development
COPY . /source
WORKDIR /source/src
CMD dotnet run --no-launch-profile

FROM dhi.io/aspnetcore:10 AS final
WORKDIR /app
COPY --from=build /app .
ENTRYPOINT ["dotnet", "myWebApp.dll"]
```

**使用官方 .NET 10 镜像**



```dockerfile {hl_lines="9"}
# syntax=docker/dockerfile:1

FROM --platform=$BUILDPLATFORM mcr.microsoft.com/dotnet/sdk:10.0-alpine AS build
ARG TARGETARCH
COPY . /source
WORKDIR /source/src
RUN --mount=type=cache,id=nuget,target=/root/.nuget/packages \
    dotnet publish -a ${TARGETARCH/amd64/x64} --use-current-runtime --self-contained false -o /app
RUN dotnet test /source/tests

FROM mcr.microsoft.com/dotnet/sdk:10.0-alpine AS development
COPY . /source
WORKDIR /source/src
CMD dotnet run --no-launch-profile

FROM mcr.microsoft.com/dotnet/aspnet:10.0-alpine AS final
WORKDIR /app
COPY --from=build /app .
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser
USER appuser
ENTRYPOINT ["dotnet", "myWebApp.dll"]
```



运行以下命令，以构建阶段为目标构建镜像并查看测试结果。包含 `--progress=plain` 以查看构建输出，`--no-cache` 以确保测试始终运行，`--target build` 以指定构建阶段为目标。

```console
$ docker build -t dotnet-docker-image-test --progress=plain --no-cache --target build .
```

你应该会看到包含以下内容的输出。

```console
#11 [build 5/5] RUN dotnet test /source/tests
#11 1.564   Determining projects to restore...
#11 3.421   Restored /source/src/myWebApp.csproj (in 1.02 sec).
#11 19.42   Restored /source/tests/tests.csproj (in 17.05 sec).
#11 27.91   myWebApp -> /source/src/bin/Debug/net10.0/myWebApp.dll
#11 28.47   tests -> /source/tests/bin/Debug/net10.0/tests.dll
#11 28.49 Test run for /source/tests/bin/Debug/net10.0/tests.dll (.NETCoreApp,Version=v10.0)
#11 28.67 Microsoft (R) Test Execution Command Line Tool Version 17.3.3 (x64)
#11 28.67 Copyright (c) Microsoft Corporation.  All rights reserved.
#11 28.68
#11 28.97 Starting test execution, please wait...
#11 29.03 A total of 1 test files matched the specified pattern.
#11 32.07
#11 32.08 Passed!  - Failed:     0, Passed:     1, Skipped:     0, Total:     1, Duration: < 1 ms - /source/tests/bin/Debug/net10.0/tests.dll (net10.0)
#11 DONE 32.2s
```

### 总结

在本节中，你学习了如何在本地开发时通过 Compose 运行测试，以及如何在构建镜像时运行测试。

相关信息：

- [docker compose run](/reference/cli/docker/compose/run/)

