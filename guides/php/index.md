# PHP 语言专项指南


PHP 语言专项指南教您如何使用 Docker 创建容器化的 PHP 应用。在本指南中，您将学习如何：

- 容器化并运行 PHP 应用
- 使用容器搭建本地环境以开发 PHP 应用
- 在容器内运行 PHP 应用的测试

完成 PHP 语言专项指南后，您应该能够根据本指南提供的示例和说明容器化您自己的 PHP 应用。

首先从容器化一个已有的 PHP 应用开始。

## 容器化一个 PHP 应用

### 前提条件

- 您已安装最新版本的 [Docker Desktop](/get-started/get-docker.md)。
- 您拥有 [git 客户端](https://git-scm.com/downloads)。本节示例使用基于命令行的 git 客户端，但您可以使用任何客户端。

### 概述

本节将引导您容器化并运行一个 PHP 应用。

### 获取示例应用

在本指南中，您将使用一个预构建的 PHP 应用。该应用使用 Composer 进行库依赖管理。您将通过 Apache Web 服务器提供该应用。

打开终端，切换到您想工作的目录，然后运行以下命令克隆仓库。

```console
$ git clone https://github.com/docker/docker-php-sample
```

该示例应用是一个基本的 hello world 应用以及一个在数据库中递增计数器的应用。此外，该应用使用 PHPUnit 进行测试。

### 创建 Docker 资产

现在您已经有一个应用，可以创建必要的 Docker 资产来将其容器化。

> [!TIP]
>
> [Gordon](/ai/gordon/)（Docker 的 AI 助手）可以为您的项目生成 Docker 资产。请 Gordon 为您创建适配您应用的 Dockerfile、Compose 文件和 `.dockerignore`。

在您的 `docker-php-sample` 目录中创建以下文件。

```dockerfile {collapse=true,title=Dockerfile}
# syntax=docker/dockerfile:1

# 本文件中的注释可帮助您入门。
# 如需更多帮助，请访问 Dockerfile 参考指南：
# https://docs.docker.com/go/dockerfile-reference/

################################################################################

# 创建一个用于安装 Composer 中定义的应用依赖的阶段。
FROM composer:lts as deps

WORKDIR /app

# 如果您的 composer.json 文件定义了在依赖安装期间运行且
# 引用了应用源文件的脚本，请取消下面一行的注释，将所有文件
# 复制到此层中。
# COPY . .

# 将下载依赖作为单独的步骤，以利用 Docker 的缓存。
# 利用到 composer.json 和 composer.lock 的绑定挂载，避免将它们
# 复制到此层中。
# 利用到 /tmp/cache 的缓存挂载，以便后续构建无需重新下载包。
RUN --mount=type=bind,source=composer.json,target=composer.json \
    --mount=type=bind,source=composer.lock,target=composer.lock \
    --mount=type=cache,target=/tmp/cache \
    composer install --no-dev --no-interaction

################################################################################

# 创建一个用于运行应用的新阶段，其中包含应用所需的最小运行时依赖。
# 这通常使用与安装或构建阶段不同的基础镜像，必要文件从安装阶段复制过来。
#
# 下面的示例使用 PHP Apache 镜像作为运行应用的基础。
# 通过指定 "8.2-apache" 标签，它还会使用构建 Dockerfile 时该标签最新的版本。
# 如果可复现性很重要，请考虑使用特定的摘要 SHA，例如
# php@sha256:99cede493dfd88720b610eb8077c8688d3cca50003d76d1d539b0efc8cca72b4。
FROM php:8.2-apache as final

# 您的 PHP 应用可能需要手动安装额外的 PHP 扩展。
# 有关安装扩展的详细说明，请参见
# https://github.com/docker-library/docs/tree/master/php#how-to-install-more-php-extensions
# 下面的代码块提供了您可以编辑和使用的示例。
#
# 添加核心 PHP 扩展，参见
# https://github.com/docker-library/docs/tree/master/php#php-core-extensions
# 本示例添加了 'gd' 扩展依赖的 apt 包，然后安装 'gd' 扩展。
# 有关运行 apt-get 的更多提示，请参见
# https://docs.docker.com/go/dockerfile-aptget-best-practices/
# RUN apt-get update && apt-get install -y \
#     libfreetype-dev \
#     libjpeg62-turbo-dev \
#     libpng-dev \
# && rm -rf /var/lib/apt/lists/* \
#     && docker-php-ext-configure gd --with-freetype --with-jpeg \
#     && docker-php-ext-install -j$(nproc) gd
#
# 添加 PECL 扩展，参见
# https://github.com/docker-library/docs/tree/master/php#pecl-extensions
# 本示例添加了 'redis' 和 'xdebug' 扩展。
# RUN pecl install redis-5.3.7 \
#    && pecl install xdebug-3.2.1 \
#    && docker-php-ext-enable redis xdebug

# 使用 PHP 运行时参数的默认生产配置，参见
# https://github.com/docker-library/docs/tree/master/php#configuration
RUN mv "$PHP_INI_DIR/php.ini-production" "$PHP_INI_DIR/php.ini"

# 从上一安装阶段复制应用依赖。
COPY --from=deps app/vendor/ /var/www/html/vendor
# 从应用目录复制应用文件。
COPY ./src /var/www/html

# 切换到应用将以其运行的、非特权用户（在基础镜像中定义）。
# 参见 https://docs.docker.com/go/dockerfile-user-best-practices/
USER www-data
```

```yaml {collapse=true,title=compose.yaml}
# 本文件中的注释可帮助您入门。
# 如需更多帮助，请访问 Docker Compose 参考指南：
# https://docs.docker.com/go/compose-spec-reference/

# 这里的指令将您的应用定义为名为 "server" 的服务。
# 该服务从当前目录中的 Dockerfile 构建。
# 您可以在此处添加应用可能依赖的其他服务，如数据库或缓存。
# 示例见 Awesome Compose 仓库：
# https://github.com/docker/awesome-compose
services:
  server:
    build:
      context: .
    ports:
      - 9000:80

# 下面注释掉的部分是如何定义应用可使用的 PostgreSQL
# 数据库的示例。`depends_on` 告诉 Docker Compose 在您的应用之前
# 启动数据库。`db-data` 卷在容器重启之间持久化数据库数据。
# `db-password` secret 用于设置数据库密码。您必须创建 `db/password.txt`
# 并向其中添加您选择的密码，然后才能运行 `docker compose up`。
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
# 在此处包含您不希望被复制到容器中的任何文件或目录
# （例如本地构建产物、临时文件等）。
#
# 如需更多帮助，请访问 .dockerignore 文件参考指南：
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
**/.next
**/.cache
**/*.*proj.user
**/*.dbmdl
**/*.jfm
**/charts
**/docker-compose*
**/compose.y*ml
!**/composer.json
!**/composer.lock
**/Dockerfile*
**/node_modules
**/npm-debug.log
**/obj
**/secrets.dev.yaml
**/values.dev.yaml
**/vendor
LICENSE
README.md
```

现在您的 `docker-php-sample` 目录中应包含以下内容。

```text
├── docker-php-sample/
│ ├── .git/
│ ├── src/
│ ├── tests/
│ ├── .dockerignore
│ ├── .gitignore
│ ├── compose.yaml
│ ├── composer.json
│ ├── composer.lock
│ ├── Dockerfile
│ └── README.md
```

要了解这些文件的更多信息，请参阅以下内容：

- [Dockerfile](/reference/dockerfile.md)
- [.dockerignore](/reference/dockerfile.md#dockerignore-file)
- [compose.yaml](/reference/compose-file/_index.md)

### 运行应用

在 `docker-php-sample` 目录中，在终端运行以下命令。

```console
$ docker compose up --build
```

打开浏览器，在 [http://localhost:9000/hello.php](http://localhost:9000/hello.php) 查看应用。您应该会看到一个简单的 hello world 应用。

在终端中按 `ctrl`+`c` 停止应用。

#### 在后台运行应用

您可以通过添加 `-d` 选项使应用脱离终端运行。在 `docker-php-sample` 目录中，在终端运行以下命令。

```console
$ docker compose up --build -d
```

打开浏览器，在 [http://localhost:9000/hello.php](http://localhost:9000/hello.php) 查看应用。您应该会看到一个简单的 hello world 应用。

在终端中运行以下命令停止应用。

```console
$ docker compose down
```

有关 Compose 命令的更多信息，请参阅 [Compose CLI 参考](/reference/cli/docker/compose/)。

## 使用容器进行 PHP 开发

### 前提条件

完成 [容器化一个 PHP 应用](#containerize-a-php-application)。

### 概述

在本节中，您将学习如何为容器化的应用搭建开发环境。这包括：

- 添加本地数据库并持久化数据
- 添加 phpMyAdmin 以与数据库交互
- 配置 Compose 以在您编辑并保存代码时自动更新运行中的 Compose 服务
- 创建一个包含开发依赖的开发容器

### 添加本地数据库并持久化数据

您可以使用容器来搭建本地服务，如数据库。对于示例应用，您需要执行以下操作：

- 更新 `Dockerfile` 以安装连接到数据库的扩展
- 更新 `compose.yaml` 文件以添加数据库服务和用于持久化数据的卷

#### 更新 Dockerfile 以安装扩展

要安装 PHP 扩展，您需要更新 `Dockerfile`。在 IDE 或文本编辑器中打开您的 Dockerfile，然后更新内容。以下 `Dockerfile` 包含一行新内容，用于安装 `pdo` 和 `pdo_mysql` 扩展。所有注释已移除。

```dockerfile {hl_lines=11}
# syntax=docker/dockerfile:1

FROM composer:lts as deps
WORKDIR /app
RUN --mount=type=bind,source=composer.json,target=composer.json \
    --mount=type=bind,source=composer.lock,target=composer.lock \
    --mount=type=cache,target=/tmp/cache \
    composer install --no-dev --no-interaction

FROM php:8.2-apache as final
RUN docker-php-ext-install pdo pdo_mysql
RUN mv "$PHP_INI_DIR/php.ini-production" "$PHP_INI_DIR/php.ini"
COPY --from=deps app/vendor/ /var/www/html/vendor
COPY ./src /var/www/html
USER www-data
```

有关安装 PHP 扩展的更多详情，请参阅 [PHP 官方 Docker 镜像](https://hub.docker.com/_/php)。

#### 更新 compose.yaml 文件以添加数据库并持久化数据

在 IDE 或文本编辑器中打开 `compose.yaml` 文件。您会注意到它已经包含针对 PostgreSQL 数据库和卷的注释掉的指令。对于此应用，您将使用 MariaDB。有关 MariaDB 的更多详情，请参阅 [MariaDB 官方 Docker 镜像](https://hub.docker.com/_/mariadb)。

在 IDE 或文本编辑器中打开 `src/database.php` 文件。您会注意到它读取环境变量以连接到数据库。

在 `compose.yaml` 文件中，您需要更新以下内容：

1. 取消注释并更新 MariaDB 的数据库指令。
2. 向 server 服务添加一个 secret 以传入数据库密码。
3. 向 server 服务添加数据库连接环境变量。
4. 取消注释卷指令以持久化数据。

以下是更新后的 `compose.yaml` 文件。所有注释已移除。

```yaml
services:
  server:
    build:
      context: .
    ports:
      - 9000:80
    depends_on:
      db:
        condition: service_healthy
    secrets:
      - db-password
    environment:
      - PASSWORD_FILE_PATH=/run/secrets/db-password
      - DB_HOST=db
      - DB_NAME=example
      - DB_USER=root
  db:
    image: mariadb
    restart: always
    user: root
    secrets:
      - db-password
    volumes:
      - db-data:/var/lib/mysql
    environment:
      - MARIADB_ROOT_PASSWORD_FILE=/run/secrets/db-password
      - MARIADB_DATABASE=example
    expose:
      - 3306
    healthcheck:
      test:
        [
          "CMD",
          "/usr/local/bin/healthcheck.sh",
          "--su-mysql",
          "--connect",
          "--innodb_initialized",
        ]
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

在使用 Compose 运行应用之前，请注意此 Compose 文件使用了 `secrets` 并指定了一个 `password.txt` 文件来保存数据库密码。您必须创建此文件，因为它未包含在源仓库中。

在 `docker-php-sample` 目录中，创建一个名为 `db` 的新目录，并在该目录中创建一个名为 `password.txt` 的文件。在 IDE 或文本编辑器中打开 `password.txt` 并添加以下密码。密码必须位于单行，文件中不能有其他行。

```text
example
```

保存并关闭 `password.txt` 文件。

现在您的 `docker-php-sample` 目录中应包含以下内容。

```text
├── docker-php-sample/
│ ├── .git/
│ ├── db/
│ │ └── password.txt
│ ├── src/
│ ├── tests/
│ ├── .dockerignore
│ ├── .gitignore
│ ├── compose.yaml
│ ├── composer.json
│ ├── composer.lock
│ ├── Dockerfile
│ └── README.md
```

运行以下命令启动应用。

```console
$ docker compose up --build
```

打开浏览器，在 [http://localhost:9000/database.php](http://localhost:9000/database.php) 查看应用。您应该会看到一个带有文本和计数器的简单 Web 应用，每次刷新时计数器都会递增。

在终端中按 `ctrl+c` 停止应用。

### 验证数据是否在数据库中持久化

在终端中，运行 `docker compose rm` 移除容器，然后运行 `docker compose up` 再次运行应用。

```console
$ docker compose rm
$ docker compose up --build
```

在浏览器中刷新 [http://localhost:9000/database.php](http://localhost:9000/database.php)，并验证之前的计数仍然存在。如果没有卷，数据库数据在您移除容器后将不会持久化。

在终端中按 `ctrl+c` 停止应用。

### 添加 phpMyAdmin 以与数据库交互

您可以通过更新 `compose.yaml` 文件轻松地向应用栈添加服务。

更新您的 `compose.yaml` 以添加 phpMyAdmin 的新服务。更多详情请参阅 [phpMyAdmin 官方 Docker 镜像](https://hub.docker.com/_/phpmyadmin)。以下是更新后的 `compose.yaml` 文件。

```yaml {hl_lines="42-49"}
services:
  server:
    build:
      context: .
    ports:
      - 9000:80
    depends_on:
      db:
        condition: service_healthy
    secrets:
      - db-password
    environment:
      - PASSWORD_FILE_PATH=/run/secrets/db-password
      - DB_HOST=db
      - DB_NAME=example
      - DB_USER=root
  db:
    image: mariadb
    restart: always
    user: root
    secrets:
      - db-password
    volumes:
      - db-data:/var/lib/mysql
    environment:
      - MARIADB_ROOT_PASSWORD_FILE=/run/secrets/db-password
      - MARIADB_DATABASE=example
    expose:
      - 3306
    healthcheck:
      test:
        [
          "CMD",
          "/usr/local/bin/healthcheck.sh",
          "--su-mysql",
          "--connect",
          "--innodb_initialized",
        ]
      interval: 10s
      timeout: 5s
      retries: 5
  phpmyadmin:
    image: phpmyadmin
    ports:
      - 8080:80
    depends_on:
      - db
    environment:
      - PMA_HOST=db
volumes:
  db-data:
secrets:
  db-password:
    file: db/password.txt
```

在终端中，运行 `docker compose up` 再次运行应用。

```console
$ docker compose up --build
```

在浏览器中打开 [http://localhost:8080](http://localhost:8080) 访问 phpMyAdmin。使用 `root` 作为用户名、`example` 作为密码登录。您现在可以通过 phpMyAdmin 与数据库交互。

在终端中按 `ctrl+c` 停止应用。

### 自动更新服务

使用 Compose Watch 在您编辑并保存代码时自动更新运行中的 Compose 服务。有关 Compose Watch 的更多详情，请参阅 [使用 Compose Watch](/manuals/compose/how-tos/file-watch.md)。

在 IDE 或文本编辑器中打开您的 `compose.yaml` 文件，然后添加 Compose Watch 指令。以下是更新后的 `compose.yaml` 文件。

```yaml {hl_lines="17-21"}
services:
  server:
    build:
      context: .
    ports:
      - 9000:80
    depends_on:
      db:
        condition: service_healthy
    secrets:
      - db-password
    environment:
      - PASSWORD_FILE_PATH=/run/secrets/db-password
      - DB_HOST=db
      - DB_NAME=example
      - DB_USER=root
    develop:
      watch:
        - action: sync
          path: ./src
          target: /var/www/html
  db:
    image: mariadb
    restart: always
    user: root
    secrets:
      - db-password
    volumes:
      - db-data:/var/lib/mysql
    environment:
      - MARIADB_ROOT_PASSWORD_FILE=/run/secrets/db-password
      - MARIADB_DATABASE=example
    expose:
      - 3306
    healthcheck:
      test:
        [
          "CMD",
          "/usr/local/bin/healthcheck.sh",
          "--su-mysql",
          "--connect",
          "--innodb_initialized",
        ]
      interval: 10s
      timeout: 5s
      retries: 5
  phpmyadmin:
    image: phpmyadmin
    ports:
      - 8080:80
    depends_on:
      - db
    environment:
      - PMA_HOST=db
volumes:
  db-data:
secrets:
  db-password:
    file: db/password.txt
```

运行以下命令以使用 Compose Watch 运行应用。

```console
$ docker compose watch
```

打开浏览器，验证应用在 [http://localhost:9000/hello.php](http://localhost:9000/hello.php) 运行。

您本地机器上对应用源文件的任何更改现在都会立即反映到运行中的容器中。

在 IDE 或文本编辑器中打开 `hello.php`，并将字符串 `Hello, world!` 更新为 `Hello, Docker!`。

保存对 `hello.php` 的更改，然后等待几秒钟让应用同步。在浏览器中刷新 [http://localhost:9000/hello.php](http://localhost:9000/hello.php)，并验证更新后的文本是否出现。

在终端中按 `ctrl+c` 停止 Compose Watch。在终端中运行 `docker compose down` 停止应用。

### 创建开发容器

此时，当您运行容器化的应用时，Composer 并未安装开发依赖。虽然这个较小的镜像适合生产，但它缺少开发时可能需要的工具和依赖，并且不包含 `tests` 目录。您可以使用多阶段构建在同一 Dockerfile 中构建开发和生产阶段。更多详情请参阅 [多阶段构建](/manuals/build/building/multi-stage.md)。

在 `Dockerfile` 中，您需要更新以下内容：

1. 将 `deps` 阶段拆分为两个阶段。一个用于生产（`prod-deps`），一个（`dev-deps`）用于安装开发依赖。
2. 创建一个公共的 `base` 阶段。
3. 创建一个新的 `development` 阶段用于开发。
4. 更新 `final` 阶段以从新的 `prod-deps` 阶段复制依赖。

以下是更改前后的 `Dockerfile`。

**更改前**



```dockerfile
# syntax=docker/dockerfile:1

FROM composer:lts as deps
WORKDIR /app
RUN --mount=type=bind,source=composer.json,target=composer.json \
    --mount=type=bind,source=composer.lock,target=composer.lock \
    --mount=type=cache,target=/tmp/cache \
    composer install --no-dev --no-interaction

FROM php:8.2-apache as final
RUN docker-php-ext-install pdo pdo_mysql
RUN mv "$PHP_INI_DIR/php.ini-production" "$PHP_INI_DIR/php.ini"
COPY --from=deps app/vendor/ /var/www/html/vendor
COPY ./src /var/www/html
USER www-data
```

**更改后**



```dockerfile
# syntax=docker/dockerfile:1

FROM composer:lts as prod-deps
WORKDIR /app
RUN --mount=type=bind,source=./composer.json,target=composer.json \
    --mount=type=bind,source=./composer.lock,target=composer.lock \
    --mount=type=cache,target=/tmp/cache \
    composer install --no-dev --no-interaction

FROM composer:lts as dev-deps
WORKDIR /app
RUN --mount=type=bind,source=./composer.json,target=composer.json \
    --mount=type=bind,source=./composer.lock,target=composer.lock \
    --mount=type=cache,target=/tmp/cache \
    composer install --no-interaction

FROM php:8.2-apache as base
RUN docker-php-ext-install pdo pdo_mysql
COPY ./src /var/www/html

FROM base as development
COPY ./tests /var/www/html/tests
RUN mv "$PHP_INI_DIR/php.ini-development" "$PHP_INI_DIR/php.ini"
COPY --from=dev-deps app/vendor/ /var/www/html/vendor

FROM base as final
RUN mv "$PHP_INI_DIR/php.ini-production" "$PHP_INI_DIR/php.ini"
COPY --from=prod-deps app/vendor/ /var/www/html/vendor
USER www-data
```



通过添加一条指向开发阶段的指令来更新您的 `compose.yaml` 文件。

以下是 `compose.yaml` 文件中更新后的部分。

```yaml {hl_lines=5}
services:
  server:
    build:
      context: .
      target: development
      # ...
```

您的容器化应用现在将安装开发依赖。

运行以下命令启动应用。

```console
$ docker compose up --build
```

打开浏览器，在 [http://localhost:9000/hello.php](http://localhost:9000/hello.php) 查看应用。您应该仍会看到简单的 "Hello, Docker!" 应用。

在终端中按 `ctrl+c` 停止应用。

虽然应用看起来相同，但您现在可以使用开发依赖了。继续阅读下一节，了解如何使用 Docker 运行测试。

## 在容器中运行 PHP 测试

### 前提条件

完成本指南的所有前面章节，从 [容器化一个 PHP 应用](#containerize-a-php-application) 开始。

### 概述

测试是现代软件开发的重要组成部分。对于不同的开发团队，测试可能意味着很多东西。有单元测试、集成测试和端到端测试。在本指南中，您将了解在开发和构建时使用 Docker 运行单元测试。

### 在本地开发时运行测试

示例应用已经在 `tests` 目录中包含一个 PHPUnit 测试。在本地开发时，您可以使用 Compose 运行测试。

在 `docker-php-sample` 目录中运行以下命令以在容器内运行测试。

```console
$ docker compose run --build --rm server ./vendor/bin/phpunit tests/HelloWorldTest.php
```

您应该会看到包含以下内容的输出。

```console
Hello, Docker!PHPUnit 9.6.13 by Sebastian Bergmann and contributors.

.                                                                   1 / 1 (100%)

Time: 00:00.003, Memory: 4.00 MB

OK (1 test, 1 assertion)
```

要了解该命令的更多信息，请参阅 [docker compose run](/reference/cli/docker/compose/run/)。

### 在构建时运行测试

要在构建时运行测试，您需要更新 Dockerfile。创建一个运行测试的新 test 阶段。

以下是更新后的 Dockerfile。

```dockerfile {hl_lines="26-28"}
# syntax=docker/dockerfile:1

FROM composer:lts as prod-deps
WORKDIR /app
RUN --mount=type=bind,source=./composer.json,target=composer.json \
    --mount=type=bind,source=./composer.lock,target=composer.lock \
    --mount=type=cache,target=/tmp/cache \
    composer install --no-dev --no-interaction

FROM composer:lts as dev-deps
WORKDIR /app
RUN --mount=type=bind,source=./composer.json,target=composer.json \
    --mount=type=bind,source=./composer.lock,target=composer.lock \
    --mount=type=cache,target=/tmp/cache \
    composer install --no-interaction

FROM php:8.2-apache as base
RUN docker-php-ext-install pdo pdo_mysql
COPY ./src /var/www/html

FROM base as development
COPY ./tests /var/www/html/tests
RUN mv "$PHP_INI_DIR/php.ini-development" "$PHP_INI_DIR/php.ini"
COPY --from=dev-deps app/vendor/ /var/www/html/vendor

FROM development as test
WORKDIR /var/www/html
RUN ./vendor/bin/phpunit tests/HelloWorldTest.php

FROM base as final
RUN mv "$PHP_INI_DIR/php.ini-production" "$PHP_INI_DIR/php.ini"
COPY --from=prod-deps app/vendor/ /var/www/html/vendor
USER www-data
```

运行以下命令以使用 test 阶段作为目标构建镜像并查看测试结果。包含 `--progress plain` 以查看构建输出，`--no-cache` 以确保测试始终运行，`--target test` 以指定 test 阶段。

```console
$ docker build -t php-docker-image-test --progress plain --no-cache --target test .
```

您应该会看到包含以下内容的输出。

```console
#18 [test 2/2] RUN ./vendor/bin/phpunit tests/HelloWorldTest.php
#18 0.385 Hello, Docker!PHPUnit 9.6.13 by Sebastian Bergmann and contributors.
#18 0.392
#18 0.394 .                                                                   1 / 1 (100%)
#18 0.395
#18 0.395 Time: 00:00.003, Memory: 4.00 MB
#18 0.395
#18 0.395 OK (1 test, 1 assertion)
```

### 总结

在本节中，您学习了如何在本地开发时使用 Compose 运行测试，以及如何在构建镜像时运行测试。

相关信息：

- [docker compose run](/reference/cli/docker/compose/run/)
