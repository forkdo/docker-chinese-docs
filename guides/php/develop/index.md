# 使用容器进行 PHP 开发

## 先决条件

已完成[容器化 PHP 应用程序](containerize.md)。

## 概述

在本节中，您将学习如何为容器化应用程序设置开发环境。这包括：

- 添加本地数据库并持久化数据
- 添加 phpMyAdmin 以与数据库交互
- 配置 Compose，以便在您编辑并保存代码时自动更新正在运行的 Compose 服务
- 创建包含开发依赖项的开发容器

## 添加本地数据库并持久化数据

您可以使用容器来设置本地服务，例如数据库。
要对示例应用程序执行此操作，您需要执行以下操作：

- 更新 `Dockerfile` 以安装连接数据库所需的扩展
- 更新 `compose.yaml` 文件以添加数据库服务和用于持久化数据的卷

### 更新 Dockerfile 以安装扩展

要安装 PHP 扩展，您需要更新 `Dockerfile`。在 IDE 或文本编辑器中打开您的 Dockerfile，然后更新内容。以下 `Dockerfile` 包含一行新内容，用于安装 `pdo` 和 `pdo_mysql` 扩展。所有注释均已移除。

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

有关安装 PHP 扩展的更多详细信息，请参阅 [PHP 的官方 Docker 镜像](https://hub.docker.com/_/php)。

### 更新 compose.yaml 文件以添加数据库并持久化数据

在 IDE 或文本编辑器中打开 `compose.yaml` 文件。您会注意到它已经包含注释掉的 PostgreSQL 数据库和卷的说明。对于此应用程序，您将使用 MariaDB。有关 MariaDB 的更多详细信息，请参阅 [MariaDB 官方 Docker 镜像](https://hub.docker.com/_/mariadb)。

在 IDE 或文本编辑器中打开 `src/database.php` 文件。您会注意到它读取环境变量以连接到数据库。

在 `compose.yaml` 文件中，您需要更新以下内容：

1. 取消注释并更新 MariaDB 的数据库说明。
2. 向服务器服务添加一个 secret 以传入数据库密码。
3. 向服务器服务添加数据库连接环境变量。
4. 取消注释卷说明以持久化数据。

以下是更新后的 `compose.yaml` 文件。所有注释均已移除。

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
> 要了解有关 Compose 文件中指令的更多信息，请参阅 [Compose 文件参考](/reference/compose-file/)。

在使用 Compose 运行应用程序之前，请注意此 Compose 文件使用 `secrets` 并指定一个 `password.txt` 文件来保存数据库密码。您必须创建此文件，因为它不包含在源代码仓库中。

在 `docker-php-sample` 目录中，创建一个名为 `db` 的新目录，并在该目录中创建一个名为 `password.txt` 的文件。在 IDE 或文本编辑器中打开 `password.txt` 并添加以下密码。密码必须位于单行上，文件中不能有其他行。

```text
example
```

保存并关闭 `password.txt` 文件。

您现在应该在 `docker-php-sample` 目录中拥有以下内容。

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

运行以下命令以启动您的应用程序。

```console
$ docker compose up --build
```

打开浏览器并访问 [http://localhost:9000/database.php](http://localhost:9000/database.php) 查看应用程序。您应该会看到一个简单的 Web 应用程序，其中包含文本和一个计数器，每次刷新时计数器都会递增。

在终端中按 `ctrl+c` 停止您的应用程序。

## 验证数据是否在数据库中持久化

在终端中，运行 `docker compose rm` 以移除您的容器，然后运行 `docker compose up` 再次运行您的应用程序。

```console
$ docker compose rm
$ docker compose up --build
```

在浏览器中刷新 [http://localhost:9000/database.php](http://localhost:9000/database.php)，并验证之前的计数是否仍然存在。如果没有卷，数据库数据在移除容器后将不会持久保存。

在终端中按 `ctrl+c` 停止您的应用程序。

## 添加 phpMyAdmin 以与数据库交互

您可以通过更新 `compose.yaml` 文件轻松地将服务添加到您的应用程序堆栈中。

更新您的 `compose.yaml` 以添加一个新的 phpMyAdmin 服务。有关更多详细信息，请参阅 [phpMyAdmin 官方 Docker 镜像](https://hub.docker.com/_/phpmyadmin)。以下是更新后的 `compose.yaml` 文件。

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

在终端中，运行 `docker compose up` 再次运行您的应用程序。

```console
$ docker compose up --build
```

在浏览器中打开 [http://localhost:8080](http://localhost:8080) 以访问 phpMyAdmin。使用 `root` 作为用户名，`example` 作为密码登录。您现在可以通过 phpMyAdmin 与数据库交互。

在终端中按 `ctrl+c` 停止您的应用程序。

## 自动更新服务

使用 Compose Watch 在您编辑并保存代码时自动更新正在运行的 Compose 服务。有关 Compose Watch 的更多详细信息，请参阅[使用 Compose Watch](/manuals/compose/how-tos/file-watch.md)。

在 IDE 或文本编辑器中打开您的 `compose.yaml` 文件，然后添加 Compose Watch 说明。以下是更新后的 `compose.yaml` 文件。

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

运行以下命令以使用 Compose Watch 运行您的应用程序。

```console
$ docker compose watch
```

打开浏览器并验证应用程序是否正在运行于 [http://localhost:9000/hello.php](http://localhost:9000/hello.php)。

现在，您本地机器上对应用程序源文件的任何更改都将立即反映在正在运行的容器中。

在 IDE 或文本编辑器中打开 `hello.php`，并将字符串 `Hello, world!` 更新为 `Hello, Docker!`。

保存对 `hello.php` 的更改，然后等待几秒钟让应用程序同步。在浏览器中刷新 [http://localhost:9000/hello.php](http://localhost:9000/hello.php)，并验证是否出现了更新后的文本。

在终端中按 `ctrl+c` 停止 Compose Watch。在终端中运行 `docker compose down` 以停止应用程序。

## 创建开发容器

此时，当您运行容器化应用程序时，Composer 不会安装开发依赖项。虽然这个小镜像适合生产环境，但它缺少开发时可能需要的工具和依赖项，并且不包含 `tests` 目录。您可以使用多阶段构建在同一个 Dockerfile 中为开发和生产构建阶段。有关更多详细信息，请参阅[多阶段构建](/manuals/build/building/multi-stage.md)。

在 `Dockerfile` 中，您需要更新以下内容：

1. 将 `deps` 阶段拆分为两个阶段。一个用于生产 (`prod-deps`)，另一个 (`dev-deps`) 用于安装开发依赖项。
2. 创建一个通用的 `base` 阶段。
3. 为开发创建一个新的 `development` 阶段。
4. 更新 `final` 阶段以从新的 `prod-deps` 阶段复制依赖项。

以下是更改前后的 `Dockerfile`。








<div
  class="tabs"
  
    x-data="{ selected: '%E6%9B%B4%E6%94%B9%E5%89%8D' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === '%E6%9B%B4%E6%94%B9%E5%89%8D' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = '%E6%9B%B4%E6%94%B9%E5%89%8D'"
        
      >
        更改前
      </button>
    
      <button
        class="tab-item"
        :class="selected === '%E6%9B%B4%E6%94%B9%E5%90%8E' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = '%E6%9B%B4%E6%94%B9%E5%90%8E'"
        
      >
        更改后
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== '%E6%9B%B4%E6%94%B9%E5%89%8D' && 'hidden'"
      >
        <div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'IyBzeW50YXg9ZG9ja2VyL2RvY2tlcmZpbGU6MQoKRlJPTSBjb21wb3NlcjpsdHMgYXMgZGVwcwpXT1JLRElSIC9hcHAKUlVOIC0tbW91bnQ9dHlwZT1iaW5kLHNvdXJjZT1jb21wb3Nlci5qc29uLHRhcmdldD1jb21wb3Nlci5qc29uIFwKICAgIC0tbW91bnQ9dHlwZT1iaW5kLHNvdXJjZT1jb21wb3Nlci5sb2NrLHRhcmdldD1jb21wb3Nlci5sb2NrIFwKICAgIC0tbW91bnQ9dHlwZT1jYWNoZSx0YXJnZXQ9L3RtcC9jYWNoZSBcCiAgICBjb21wb3NlciBpbnN0YWxsIC0tbm8tZGV2IC0tbm8taW50ZXJhY3Rpb24KCkZST00gcGhwOjguMi1hcGFjaGUgYXMgZmluYWwKUlVOIGRvY2tlci1waHAtZXh0LWluc3RhbGwgcGRvIHBkb19teXNxbApSVU4gbXYgIiRQSFBfSU5JX0RJUi9waHAuaW5pLXByb2R1Y3Rpb24iICIkUEhQX0lOSV9ESVIvcGhwLmluaSIKQ09QWSAtLWZyb209ZGVwcyBhcHAvdmVuZG9yLyAvdmFyL3d3dy9odG1sL3ZlbmRvcgpDT1BZIC4vc3JjIC92YXIvd3d3L2h0bWwKVVNFUiB3d3ctZGF0YQ==', copying: false }"
        class="
          top-1
         absolute right-2 z-10 text-gray-300 dark:text-gray-500"
        title="copy"
        @click="window.navigator.clipboard.writeText(atob(code).replaceAll(/^[\$>]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);"
      >
        <span
          :class="{ 'group-hover:block' : !copying }"
          class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M300-200q-24 0-42-18t-18-42v-560q0-24 18-42t42-18h440q24 0 42 18t18 42v560q0 24-18 42t-42 18H300ZM180-80q-24 0-42-18t-18-42v-590q0-13 8.5-21.5T150-760q13 0 21.5 8.5T180-730v590h470q13 0 21.5 8.5T680-110q0 13-8.5 21.5T650-80H180Z"/></svg></span
        >
        <span :class="{ 'group-hover:block' : copying }" class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="m421-389-98-98q-9-9-22-9t-23 10q-9 9-9 22t9 22l122 123q9 9 21 9t21-9l239-239q10-10 10-23t-10-23q-10-9-23.5-8.5T635-603L421-389Zm59 309q-82 0-155-31.5t-127.5-86Q143-252 111.5-325T80-480q0-83 31.5-156t86-127Q252-817 325-848.5T480-880q83 0 156 31.5T763-763q54 54 85.5 127T880-480q0 82-31.5 155T763-197.5q-54 54.5-127 86T480-80Z"/></svg></span
        >
      </button>
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-dockerfile" data-lang="dockerfile"><span class="line"><span class="cl"><span class="c"># syntax=docker/dockerfile:1</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">FROM</span><span class="w"> </span><span class="s">composer:lts</span><span class="w"> </span><span class="k">as</span><span class="w"> </span><span class="s">deps</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">WORKDIR</span><span class="w"> </span><span class="s">/app</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">RUN</span> --mount<span class="o">=</span><span class="nv">type</span><span class="o">=</span>bind,source<span class="o">=</span>composer.json,target<span class="o">=</span>composer.json <span class="se">\
</span></span></span><span class="line"><span class="cl">    --mount<span class="o">=</span><span class="nv">type</span><span class="o">=</span>bind,source<span class="o">=</span>composer.lock,target<span class="o">=</span>composer.lock <span class="se">\
</span></span></span><span class="line"><span class="cl">    --mount<span class="o">=</span><span class="nv">type</span><span class="o">=</span>cache,target<span class="o">=</span>/tmp/cache <span class="se">\
</span></span></span><span class="line"><span class="cl">    composer install --no-dev --no-interaction<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">FROM</span><span class="w"> </span><span class="s">php:8.2-apache</span><span class="w"> </span><span class="k">as</span><span class="w"> </span><span class="s">final</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">RUN</span> docker-php-ext-install pdo pdo_mysql<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">RUN</span> mv <span class="s2">&#34;</span><span class="nv">$PHP_INI_DIR</span><span class="s2">/php.ini-production&#34;</span> <span class="s2">&#34;</span><span class="nv">$PHP_INI_DIR</span><span class="s2">/php.ini&#34;</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">COPY</span> --from<span class="o">=</span>deps app/vendor/ /var/www/html/vendor<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">COPY</span> ./src /var/www/html<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">USER</span><span class="w"> </span><span class="s">www-data</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== '%E6%9B%B4%E6%94%B9%E5%90%8E' && 'hidden'"
      >
        <div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'IyBzeW50YXg9ZG9ja2VyL2RvY2tlcmZpbGU6MQoKRlJPTSBjb21wb3NlcjpsdHMgYXMgcHJvZC1kZXBzCldPUktESVIgL2FwcApSVU4gLS1tb3VudD10eXBlPWJpbmQsc291cmNlPS4vY29tcG9zZXIuanNvbix0YXJnZXQ9Y29tcG9zZXIuanNvbiBcCiAgICAtLW1vdW50PXR5cGU9YmluZCxzb3VyY2U9Li9jb21wb3Nlci5sb2NrLHRhcmdldD1jb21wb3Nlci5sb2NrIFwKICAgIC0tbW91bnQ9dHlwZT1jYWNoZSx0YXJnZXQ9L3RtcC9jYWNoZSBcCiAgICBjb21wb3NlciBpbnN0YWxsIC0tbm8tZGV2IC0tbm8taW50ZXJhY3Rpb24KCkZST00gY29tcG9zZXI6bHRzIGFzIGRldi1kZXBzCldPUktESVIgL2FwcApSVU4gLS1tb3VudD10eXBlPWJpbmQsc291cmNlPS4vY29tcG9zZXIuanNvbix0YXJnZXQ9Y29tcG9zZXIuanNvbiBcCiAgICAtLW1vdW50PXR5cGU9YmluZCxzb3VyY2U9Li9jb21wb3Nlci5sb2NrLHRhcmdldD1jb21wb3Nlci5sb2NrIFwKICAgIC0tbW91bnQ9dHlwZT1jYWNoZSx0YXJnZXQ9L3RtcC9jYWNoZSBcCiAgICBjb21wb3NlciBpbnN0YWxsIC0tbm8taW50ZXJhY3Rpb24KCkZST00gcGhwOjguMi1hcGFjaGUgYXMgYmFzZQpSVU4gZG9ja2VyLXBocC1leHQtaW5zdGFsbCBwZG8gcGRvX215c3FsCkNPUFkgLi9zcmMgL3Zhci93d3cvaHRtbAoKRlJPTSBiYXNlIGFzIGRldmVsb3BtZW50CkNPUFkgLi90ZXN0cyAvdmFyL3d3dy9odG1sL3Rlc3RzClJVTiBtdiAiJFBIUF9JTklfRElSL3BocC5pbmktZGV2ZWxvcG1lbnQiICIkUEhQX0lOSV9ESVIvcGhwLmluaSIKQ09QWSAtLWZyb209ZGV2LWRlcHMgYXBwL3ZlbmRvci8gL3Zhci93d3cvaHRtbC92ZW5kb3IKCkZST00gYmFzZSBhcyBmaW5hbApSVU4gbXYgIiRQSFBfSU5JX0RJUi9waHAuaW5pLXByb2R1Y3Rpb24iICIkUEhQX0lOSV9ESVIvcGhwLmluaSIKQ09QWSAtLWZyb209cHJvZC1kZXBzIGFwcC92ZW5kb3IvIC92YXIvd3d3L2h0bWwvdmVuZG9yClVTRVIgd3d3LWRhdGE=', copying: false }"
        class="
          top-1
         absolute right-2 z-10 text-gray-300 dark:text-gray-500"
        title="copy"
        @click="window.navigator.clipboard.writeText(atob(code).replaceAll(/^[\$>]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);"
      >
        <span
          :class="{ 'group-hover:block' : !copying }"
          class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M300-200q-24 0-42-18t-18-42v-560q0-24 18-42t42-18h440q24 0 42 18t18 42v560q0 24-18 42t-42 18H300ZM180-80q-24 0-42-18t-18-42v-590q0-13 8.5-21.5T150-760q13 0 21.5 8.5T180-730v590h470q13 0 21.5 8.5T680-110q0 13-8.5 21.5T650-80H180Z"/></svg></span
        >
        <span :class="{ 'group-hover:block' : copying }" class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="m421-389-98-98q-9-9-22-9t-23 10q-9 9-9 22t9 22l122 123q9 9 21 9t21-9l239-239q10-10 10-23t-10-23q-10-9-23.5-8.5T635-603L421-389Zm59 309q-82 0-155-31.5t-127.5-86Q143-252 111.5-325T80-480q0-83 31.5-156t86-127Q252-817 325-848.5T480-880q83 0 156 31.5T763-763q54 54 85.5 127T880-480q0 82-31.5 155T763-197.5q-54 54.5-127 86T480-80Z"/></svg></span
        >
      </button>
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-dockerfile" data-lang="dockerfile"><span class="line"><span class="cl"><span class="c"># syntax=docker/dockerfile:1</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">FROM</span><span class="w"> </span><span class="s">composer:lts</span><span class="w"> </span><span class="k">as</span><span class="w"> </span><span class="s">prod-deps</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">WORKDIR</span><span class="w"> </span><span class="s">/app</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">RUN</span> --mount<span class="o">=</span><span class="nv">type</span><span class="o">=</span>bind,source<span class="o">=</span>./composer.json,target<span class="o">=</span>composer.json <span class="se">\
</span></span></span><span class="line"><span class="cl">    --mount<span class="o">=</span><span class="nv">type</span><span class="o">=</span>bind,source<span class="o">=</span>./composer.lock,target<span class="o">=</span>composer.lock <span class="se">\
</span></span></span><span class="line"><span class="cl">    --mount<span class="o">=</span><span class="nv">type</span><span class="o">=</span>cache,target<span class="o">=</span>/tmp/cache <span class="se">\
</span></span></span><span class="line"><span class="cl">    composer install --no-dev --no-interaction<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">FROM</span><span class="w"> </span><span class="s">composer:lts</span><span class="w"> </span><span class="k">as</span><span class="w"> </span><span class="s">dev-deps</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">WORKDIR</span><span class="w"> </span><span class="s">/app</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">RUN</span> --mount<span class="o">=</span><span class="nv">type</span><span class="o">=</span>bind,source<span class="o">=</span>./composer.json,target<span class="o">=</span>composer.json <span class="se">\
</span></span></span><span class="line"><span class="cl">    --mount<span class="o">=</span><span class="nv">type</span><span class="o">=</span>bind,source<span class="o">=</span>./composer.lock,target<span class="o">=</span>composer.lock <span class="se">\
</span></span></span><span class="line"><span class="cl">    --mount<span class="o">=</span><span class="nv">type</span><span class="o">=</span>cache,target<span class="o">=</span>/tmp/cache <span class="se">\
</span></span></span><span class="line"><span class="cl">    composer install --no-interaction<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">FROM</span><span class="w"> </span><span class="s">php:8.2-apache</span><span class="w"> </span><span class="k">as</span><span class="w"> </span><span class="s">base</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">RUN</span> docker-php-ext-install pdo pdo_mysql<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">COPY</span> ./src /var/www/html<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">FROM</span><span class="w"> </span><span class="s">base</span><span class="w"> </span><span class="k">as</span><span class="w"> </span><span class="s">development</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">COPY</span> ./tests /var/www/html/tests<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">RUN</span> mv <span class="s2">&#34;</span><span class="nv">$PHP_INI_DIR</span><span class="s2">/php.ini-development&#34;</span> <span class="s2">&#34;</span><span class="nv">$PHP_INI_DIR</span><span class="s2">/php.ini&#34;</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">COPY</span> --from<span class="o">=</span>dev-deps app/vendor/ /var/www/html/vendor<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">FROM</span><span class="w"> </span><span class="s">base</span><span class="w"> </span><span class="k">as</span><span class="w"> </span><span class="s">final</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">RUN</span> mv <span class="s2">&#34;</span><span class="nv">$PHP_INI_DIR</span><span class="s2">/php.ini-production&#34;</span> <span class="s2">&#34;</span><span class="nv">$PHP_INI_DIR</span><span class="s2">/php.ini&#34;</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">COPY</span> --from<span class="o">=</span>prod-deps app/vendor/ /var/www/html/vendor<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">USER</span><span class="w"> </span><span class="s">www-data</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
  </div>
</div>


更新您的 `compose.yaml` 文件，添加一个指令以定位开发阶段。

以下是 `compose.yaml` 文件的更新部分。

```yaml {hl_lines=5}
services:
  server:
    build:
      context: .
      target: development
      # ...
```

您的容器化应用程序现在将安装开发依赖项。

运行以下命令以启动您的应用程序。

```console
$ docker compose up --build
```

打开浏览器并访问 [http://localhost:9000/hello.php](http://localhost:9000/hello.php) 查看应用程序。您应该仍然会看到简单的 "Hello, Docker!" 应用程序。

在终端中按 `ctrl+c` 停止您的应用程序。

虽然应用程序看起来相同，但您现在可以利用开发依赖项了。继续下一节，了解如何使用 Docker 运行测试。

## 总结

在本节中，您了解了如何设置 Compose 文件以添加本地数据库并持久化数据。您还学习了如何使用 Compose Watch 在更新代码时自动同步应用程序。最后，您学习了如何创建包含开发所需依赖项的开发容器。

相关信息：

- [Compose 文件参考](/reference/compose-file/)
- [Compose 文件监视](/manuals/compose/how-tos/file-watch.md)
- [Dockerfile 参考](/reference/dockerfile.md)
- [PHP 的官方 Docker 镜像](https://hub.docker.com/_/php)

## 下一步

在下一节中，您将学习如何使用 Docker 运行单元测试。
