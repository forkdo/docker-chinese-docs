---
title: 使用容器进行 PHP 开发
linkTitle: 开发你的应用
weight: 20
keywords: php, development
description: 学习如何在本地使用容器开发你的 PHP 应用。
aliases:
  - /language/php/develop/
  - /guides/language/php/develop/
---

## 前置条件

完成 [容器化 PHP 应用](containerize.md)。

## 概述

在本节中，你将学习如何为你的容器化应用设置开发环境。包括：

- 添加本地数据库并持久化数据
- 添加 phpMyAdmin 与数据库交互
- 配置 Compose 以在你编辑和保存代码时自动更新运行中的 Compose 服务
- 创建一个包含开发依赖的开发容器

## 添加本地数据库并持久化数据

你可以使用容器设置本地服务，例如数据库。为此，你需要执行以下操作：

- 更新 `Dockerfile` 以安装连接数据库的扩展
- 更新 `compose.yaml` 文件以添加数据库服务和持久化数据的卷

### 更新 Dockerfile 以安装扩展

要安装 PHP 扩展，你需要更新 `Dockerfile`。在 IDE 或文本编辑器中打开你的 Dockerfile，然后更新内容。以下 `Dockerfile` 包含一行新代码，用于安装 `pdo` 和 `pdo_mysql` 扩展。所有注释已被移除。

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

有关安装 PHP 扩展的更多详细信息，请参阅 [PHP 官方 Docker 镜像](https://hub.docker.com/_/php)。

### 更新 compose.yaml 文件以添加数据库并持久化数据

在 IDE 或文本编辑器中打开 `compose.yaml` 文件。你会注意到它已经包含 PostgreSQL 数据库和卷的注释指令。对于此应用，你将使用 MariaDB。有关 MariaDB 的更多详细信息，请参阅 [MariaDB 官方 Docker 镜像](https://hub.docker.com/_/mariadb)。

在 IDE 或文本编辑器中打开 `src/database.php` 文件。你会注意到它读取环境变量以连接到数据库。

在 `compose.yaml` 文件中，你需要更新以下内容：

1. 取消注释并更新数据库指令以使用 MariaDB。
2. 向服务器服务添加一个密钥以传入数据库密码。
3. 向服务器服务添加数据库连接环境变量。
4. 取消注释卷指令以持久化数据。

以下是更新后的 `compose.yaml` 文件。所有注释已被移除。

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
> 有关 Compose 文件中指令的更多信息，请参阅 [Compose 文件参考](/reference/compose-file/)。

在使用 Compose 运行应用之前，请注意此 Compose 文件使用 `secrets` 并指定 `password.txt` 文件来保存数据库密码。你必须创建此文件，因为它不包含在源代码仓库中。

在 `docker-php-sample` 目录中，创建一个名为 `db` 的新目录，并在该目录中创建一个名为 `password.txt` 的文件。在 IDE 或文本编辑器中打开 `password.txt`，添加以下密码。密码必须在单行中，文件中不能有额外的行。

```text
example
```

保存并关闭 `password.txt` 文件。

你现在应该在 `docker-php-sample` 目录中有以下内容。

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
│ ├── README.Docker.md
│ └── README.md
```

运行以下命令以启动你的应用。

```console
$ docker compose up --build
```

在浏览器中打开 [http://localhost:9000/database.php](http://localhost:9000/database.php) 查看应用。你应该看到一个带有文本和计数器的简单 Web 应用，每次刷新时计数器都会递增。

在终端中按 `ctrl+c` 停止你的应用。

## 验证数据在数据库中持久化

在终端中运行 `docker compose rm` 以删除容器，然后运行 `docker compose up` 再次运行你的应用。

```console
$ docker compose rm
$ docker compose up --build
```

在浏览器中刷新 [http://localhost:9000/database.php](http://localhost:9000/database.php) 并验证之前的计数仍然存在。如果没有卷，数据库数据在删除容器后将不会持久化。

在终端中按 `ctrl+c` 停止你的应用。

## 添加 phpMyAdmin 与数据库交互

你可以通过更新 `compose.yaml` 文件轻松为你的应用栈添加服务。

更新你的 `compose.yaml` 以添加 phpMyAdmin 的新服务。有关详细信息，请参阅 [phpMyAdmin 官方 Docker 镜像](https://hub.docker.com/_/phpmyadmin)。以下是更新后的 `compose.yaml` 文件。

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

在终端中运行 `docker compose up` 以再次运行你的应用。

```console
$ docker compose up --build
```

在浏览器中打开 [http://localhost:8080](http://localhost:8080) 以访问 phpMyAdmin。使用 `root` 作为用户名和 `example` 作为密码登录。你现在可以通过 phpMyAdmin 与数据库交互。

在终端中按 `ctrl+c` 停止你的应用。

## 自动更新服务

使用 Compose Watch 在你编辑和保存代码时自动更新你的运行中 Compose 服务。有关 Compose Watch 的更多详细信息，请参阅 [使用 Compose Watch](/manuals/compose/how-tos/file-watch.md)。

在 IDE 或文本编辑器中打开你的 `compose.yaml` 文件，然后添加 Compose Watch 指令。以下是更新后的 `compose.yaml` 文件。

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

运行以下命令以使用 Compose Watch 运行你的应用。

```console
$ docker compose watch
```

在浏览器中打开 [http://localhost:9000/hello.php](http://localhost:9000/hello.php) 验证应用正在运行。

你现在在本地机器上对应用源文件的任何更改都会立即反映在运行的容器中。

在 IDE 或文本编辑器中打开 `hello.php`，将字符串 `Hello, world!` 更新为 `Hello, Docker!`。

保存 `hello.php` 的更改，然后等待几秒钟让应用同步。在浏览器中刷新 [http://localhost:9000/hello.php](http://localhost:9000/hello.php) 并验证更新的文本已出现。

在终端中按 `ctrl+c` 停止 Compose Watch。在终端中运行 `docker compose down` 以停止应用。

## 创建开发容器

此时，当你运行容器化应用时，Composer 不会安装开发依赖。虽然这对于生产环境很好，但它缺少你在开发时可能需要的工具和依赖，并且不包含 `tests` 目录。你可以使用多阶段构建在同一 Dockerfile 中为开发和生产构建阶段。有关详细信息，请参阅 [多阶段构建](/manuals/build/building/multi-stage.md)。

在 `Dockerfile` 中，你需要更新以下内容：

1. 将 `deps` 阶段拆分为两个阶段。一个用于生产（`prod-deps`），另一个（`dev-deps`）用于安装开发依赖。
2. 创建一个通用的 `base` 阶段。
3. 为开发创建一个新的 `development` 阶段。
4. 更新 `final` 阶段以从新的 `prod-deps` 阶段复制依赖。

以下是更改前后的 `Dockerfile`。

{{< tabs >}}
{{< tab name="更改前" >}}

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

{{< /tab >}}
{{< tab name="更改后" >}}

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

{{< /tab >}}
{{< /tabs >}}

通过添加指令以目标开发阶段来更新你的 `compose.yaml` 文件。

以下是更新后的 `compose.yaml` 文件的部分内容。

```yaml {hl_lines=5}
services:
  server:
    build:
      context: .
      target: development
      # ...
```

你的容器化应用现在将安装开发依赖。

运行以下命令以启动你的应用。

```console
$ docker compose up --build
```

在浏览器中打开 [http://localhost:9000/hello.php](http://localhost:9000/hello.php) 查看应用。你应该仍然看到简单的 "Hello, Docker!" 应用。

在终端中按 `ctrl+c` 停止你的应用。

虽然应用看起来相同，你现在可以使用开发依赖。继续下一节以了解如何使用 Docker 运行测试。

## 总结

在本节中，你了解了如何设置你的 Compose 文件以添加本地数据库并持久化数据。你还学习了如何使用 Compose Watch 在你更新代码时自动同步你的应用。最后，你学习了如何创建一个包含开发所需依赖的开发容器。

相关信息：

- [Compose 文件参考](/reference/compose-file/)
- [Compose 文件监视](/manuals/compose/how-tos/file-watch.md)
- [Dockerfile 参考](/reference/dockerfile.md)
- [PHP 官方 Docker 镜像](https://hub.docker.com/_/php)

## 下一步

在下一节中，你将学习如何使用 Docker 运行单元测试。