---
title: 使用 Docker Compose 搭建 Laravel 生产环境
description: 使用 Docker Compose 为 Laravel 搭建可用于生产环境的环境。
weight: 20
---

本指南演示如何使用 Docker 和 Docker Compose 搭建可用于生产环境的 Laravel 环境。此配置专为简化、可扩展且安全的 Laravel 应用程序部署而设计。

> [!NOTE]
> 要试用可直接运行的配置，请下载 [Laravel Docker 示例](https://github.com/dockersamples/laravel-docker-examples) 仓库。该仓库包含预配置的开发和生产环境设置。

## 项目结构

```plaintext
my-laravel-app/
├── app/
├── bootstrap/
├── config/
├── database/
├── public/
├── docker/
│   ├── common/
│   │   └── php-fpm/
│   │       └── Dockerfile
│   ├── development/
│   ├── production/
│   │   ├── php-fpm/
│   │   │   └── entrypoint.sh
│   │   └── nginx
│   │       ├── Dockerfile
│   │       └── nginx.conf
├── compose.dev.yaml
├── compose.prod.yaml
├── .dockerignore
├── .env
├── vendor/
├── ...
```

此布局代表典型的 Laravel 项目，其中 Docker 配置存储在统一的 `docker` 目录中。您会看到**两个** Compose 文件 — `compose.dev.yaml`（用于开发）和 `compose.prod.yaml`（用于生产），以便将环境分开并便于管理。

## 为 PHP-FPM 创建 Dockerfile（生产环境）

对于生产环境，`php-fpm` Dockerfile 会创建一个优化镜像，仅包含应用程序所需的 PHP 扩展和库。如 [GitHub 示例](https://github.com/dockersamples/laravel-docker-examples) 所示，使用多阶段构建的单一 Dockerfile 可保持开发环境和生产环境的一致性并减少重复。以下代码片段仅显示与生产相关的阶段：

```dockerfile
# 阶段 1：构建环境和 Composer 依赖
FROM php:8.4-fpm AS builder

# 安装 Laravel 所需的系统依赖和 PHP 扩展（支持 MySQL/PostgreSQL）。
# 此阶段的依赖仅用于构建最终镜像。
# Node.js 和静态资源构建在 Nginx 阶段处理，不在此阶段。
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    unzip \
    libpq-dev \
    libonig-dev \
    libssl-dev \
    libxml2-dev \
    libcurl4-openssl-dev \
    libicu-dev \
    libzip-dev \
    && docker-php-ext-install -j$(nproc) \
    pdo_mysql \
    pdo_pgsql \
    pgsql \
    opcache \
    intl \
    zip \
    bcmath \
    soap \
    && pecl install redis \
    && docker-php-ext-enable redis \
    && apt-get autoremove -y && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# 设置容器内的工作目录
WORKDIR /var/www

# 将整个 Laravel 应用程序代码复制到容器中
# -----------------------------------------------------------
# 在 Laravel 中，`composer install` 可能触发需要访问应用程序代码的脚本。
# 例如，`post-autoload-dump` 事件可能执行类似 `php artisan package:discover` 的 Artisan 命令。
# 如果应用程序代码（包括 `artisan` 文件）不存在，这些命令将失败，导致构建错误。
#
# 通过在运行 `composer install` 之前复制整个应用程序代码，我们确保所有必要文件都可用，
# 从而允许这些脚本成功运行。在其他情况下，可以先复制 composer 文件，
# 以利用 Docker 的层缓存机制。
# -----------------------------------------------------------
COPY . /var/www

# 安装 Composer 和依赖
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer \
    && composer install --no-dev --optimize-autoloader --no-interaction --no-progress --prefer-dist

# 阶段 2：生产环境
FROM php:8.4-fpm AS production

# 仅安装生产环境所需的运行时库
# libfcgi-bin 和 procps 是 php-fpm-healthcheck 脚本所需的
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    libicu-dev \
    libzip-dev \
    libfcgi-bin \
    procps \
    && apt-get autoremove -y && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# 下载并安装 php-fpm 健康检查脚本
RUN curl -o /usr/local/bin/php-fpm-healthcheck \
    https://raw.githubusercontent.com/renatomefi/php-fpm-healthcheck/master/php-fpm-healthcheck \
    && chmod +x /usr/local/bin/php-fpm-healthcheck

# 复制初始化脚本
COPY ./docker/php-fpm/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# 复制初始 storage 结构
COPY ./storage /var/www/storage-init

# 从 builder 阶段复制 PHP 扩展和库
COPY --from=builder /usr/local/lib/php/extensions/ /usr/local/lib/php/extensions/
COPY --from=builder /usr/local/etc/php/conf.d/ /usr/local/etc/php/conf.d/
COPY --from=builder /usr/local/bin/docker-php-ext-* /usr/local/bin/

# 使用推荐的 PHP 生产环境配置
# -----------------------------------------------------------
# PHP 提供开发和生产环境配置。
# 在此，我们将默认的 php.ini 替换为生产版本，
# 以在 live 环境中应用针对性能和安全优化的设置。
# -----------------------------------------------------------
RUN mv "$PHP_INI_DIR/php.ini-production" "$PHP_INI_DIR/php.ini"

# 通过 sed 修改 zz-docker.conf 启用 PHP-FPM 状态页
RUN sed -i '/\[www\]/a pm.status_path = /status' /usr/local/etc/php-fpm.d/zz-docker.conf
# 更新 variables_order 以包含 E（用于 ENV）
#RUN sed -i 's/variables_order = "GPCS"/variables_order = "EGPCS"/' "$PHP_INI_DIR/php.ini"

# 从构建阶段复制应用程序代码和依赖
COPY --from=builder /var/www /var/www

# 设置工作目录
WORKDIR /var/www

# 确保权限正确
RUN chown -R www-data:www-data /var/www

# 切换到非特权用户运行应用程序
USER www-data

# 将默认命令更改为运行入口点脚本
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

# 暴露端口 9000 并启动 php-fpm 服务器
EXPOSE 9000
CMD ["php-fpm"]
```

## 为 PHP-CLI 创建 Dockerfile（生产环境）

对于生产环境，您通常需要一个单独的容器来运行 Artisan 命令、迁移和其他 CLI 任务。在大多数情况下，您可以通过重用现有的 PHP-FPM 容器来运行这些命令：

```console
$ docker compose -f compose.prod.yaml exec php-fpm php artisan route:list
```

如果您需要一个具有不同扩展或严格关注点分离的单独 CLI 容器，请考虑使用 php-cli Dockerfile：

```dockerfile
# 阶段 1：构建环境和 Composer 依赖
FROM php:8.4-cli AS builder

# 安装 Laravel + MySQL/PostgreSQL 支持所需的系统依赖和 PHP 扩展
# 某些依赖仅在构建阶段为 PHP 扩展所需
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    unzip \
    libpq-dev \
    libonig-dev \
    libssl-dev \
    libxml2-dev \
    libcurl4-openssl-dev \
    libicu-dev \
    libzip-dev \
    && docker-php-ext-install -j$(nproc) \
    pdo_mysql \
    pdo_pgsql \
    pgsql \
    opcache \
    intl \
    zip \
    bcmath \
    soap \
    && pecl install redis \
    && docker-php-ext-enable redis \
    && apt-get autoremove -y && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# 设置容器内的工作目录
WORKDIR /var/www

# 将整个 Laravel 应用程序代码复制到容器中
COPY . /var/www

# 安装 Composer 和依赖
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer \
    && composer install --no-dev --optimize-autoloader --no-interaction --no-progress --prefer-dist

# 阶段 2：生产环境
FROM php:8.4-cli

# 安装运行时 php 扩展所需的客户端库
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    libicu-dev \
    libzip-dev \
    && apt-get autoremove -y && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# 从 builder 阶段复制 PHP 扩展和库
COPY --from=builder /usr/local/lib/php/extensions/ /usr/local/lib/php/extensions/
COPY --from=builder /usr/local/etc/php/conf.d/ /usr/local/etc/php/conf.d/
COPY --from=builder /usr/local/bin/docker-php-ext-* /usr/local/bin/

# 使用 PHP 运行时参数的默认生产环境配置
RUN mv "$PHP_INI_DIR/php.ini-production" "$PHP_INI_DIR/php.ini"

# 从构建阶段复制应用程序代码和依赖
COPY --from=builder /var/www /var/www

# 设置工作目录
WORKDIR /var/www

# 确保权限正确
RUN chown -R www-data:www-data /var/www

# 切换到非特权用户运行应用程序
USER www-data

# 默认命令：提供 bash shell 以允许运行任何命令
CMD ["bash"]
```

此 Dockerfile 与 PHP-FPM Dockerfile 类似，但它使用 `php:8.4-cli` 镜像作为基础镜像，并设置容器以运行 CLI 命令。

## 为 Nginx 创建 Dockerfile（生产环境）

Nginx 作为 Laravel 应用程序的 Web 服务器。您可以将静态资源直接包含到容器中。以下是 Nginx 可能的 Dockerfile 示例：

```dockerfile
# docker/nginx/Dockerfile
# 阶段 1：构建静态资源
FROM debian AS builder

# 安装 Node.js 和构建工具
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    nodejs \
    npm \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# 设置工作目录
WORKDIR /var/www

# 复制 Laravel 应用程序代码
COPY . /var/www

# 安装 Node.js 依赖并构建静态资源
RUN npm install && npm run build

# 阶段 2：Nginx 生产镜像
FROM nginx:alpine

# 复制自定义 Nginx 配置
# -----------------------------------------------------------
# 用针对 Laravel 应用程序优化的自定义配置替换默认 Nginx 配置。
# -----------------------------------------------------------
COPY ./docker/nginx/nginx.conf /etc/nginx/nginx.conf

# 从 builder 阶段复制 Laravel 的公共静态资源
# -----------------------------------------------------------
# 我们只需要 Laravel 应用程序中的 'public' 目录。
# -----------------------------------------------------------
COPY --from=builder /var/www/public /var/www/public

# 将工作目录设置为 public 文件夹
WORKDIR /var/www/public

# 暴露端口 80 并启动 Nginx
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

此 Dockerfile 使用多阶段构建将静态资源构建过程与最终生产镜像分开。第一阶段安装 Node.js 并构建静态资源，而第二阶段设置带有优化配置和已构建静态资源的 Nginx 生产镜像。

## 为生产环境创建 Docker Compose 配置

要将所有服务整合在一起，请创建一个 `compose.prod.yaml` 文件，用于定义生产环境的服务、卷和网络。以下是配置示例：

```yaml
services:
  web:
    build:
      context: .
      dockerfile: ./docker/production/nginx/Dockerfile
    restart: unless-stopped # 除非服务被显式停止，否则自动重启
    volumes:
      # 将 'laravel-storage' 卷挂载到容器内的 '/var/www/storage'。
      # -----------------------------------------------------------
      # 此卷存储上传的文件和缓存等持久数据。
      # ':ro' 选项以只读方式在 'web' 服务中挂载它，因为 Nginx 只需要读取这些文件。
      # 'php-fpm' 服务挂载相同的卷时不使用 ':ro' 以允许写操作。
      # -----------------------------------------------------------
      - laravel-storage-production:/var/www/storage:ro
    networks:
      - laravel-production
    ports:
      # 将容器内的端口 80 映射到主机上由 'NGINX_PORT' 指定的端口。
      # -----------------------------------------------------------
      # 这允许外部访问容器内运行的 Nginx Web 服务器。
      # 例如，如果 'NGINX_PORT' 设置为 '8080'，访问 'http://localhost:8080' 将到达应用程序。
      # -----------------------------------------------------------
      - "${NGINX_PORT:-80}:80"
    depends_on:
      php-fpm:
        condition: service_healthy # 等待 php-fpm 健康检查

  php-fpm:
    # 对于 php-fpm 服务，我们将创建一个自定义镜像来安装必要的 PHP 扩展并设置正确的权限。
    build:
      context: .
      dockerfile: ./docker/common/php-fpm/Dockerfile
      target: production # 使用 Dockerfile 中的 'production' 阶段
    restart: unless-stopped
    volumes:
      - laravel-storage-production:/var/www/storage # 挂载 storage 卷
    env_file:
      - .env
    networks:
      - laravel-production
    healthcheck:
      test: ["CMD-SHELL", "php-fpm-healthcheck || exit 1"]
      interval: 10s
      timeout: 5s
      retries: 3
    # 'depends_on' 属性与 'condition: service_healthy' 确保此服务不会启动，
    # 直到 'postgres' 服务通过其健康检查。
    # 这防止应用程序在数据库准备好之前尝试连接数据库。
    depends_on:
      postgres:
        condition: service_healthy

  # 'php-cli' 服务提供命令行界面以运行 Artisan 命令和其他 CLI 任务。
  # -----------------------------------------------------------
  # 这对于运行迁移、填充器或任何自定义脚本很有用。
  # 它与 'php-fpm' 服务共享相同的代码库和环境。
  # -----------------------------------------------------------
  php-cli:
    build:
      context: .
      dockerfile: ./docker/php-cli/Dockerfile
    tty: true # 启用交互式终端
    stdin_open: true # 为 'docker exec' 保持标准输入打开
    env_file:
      - .env
    networks:
      - laravel

  postgres:
    image: postgres:18
    restart: unless-stopped
    user: postgres
    ports:
      - "${POSTGRES_PORT}:5432"
    environment:
      - POSTGRES_DB=${POSTGRES_DATABASE}
      - POSTGRES_USER=${POSTGRES_USERNAME}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    volumes:
      - postgres-data-production:/var/lib/postgresql
    networks:
      - laravel-production
    # PostgreSQL 健康检查
    # -----------------------------------------------------------
    # 健康检查允许 Docker 确定服务是否可操作。
    # 'pg_isready' 命令检查 PostgreSQL 是否准备好接受连接。
    # 这防止依赖服务在数据库准备好之前启动。
    # -----------------------------------------------------------
    healthcheck:
      test: ["CMD", "pg_isready"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:alpine
    restart: unless-stopped # 除非服务被显式停止，否则自动重启
    networks:
      - laravel-production
    # Redis 健康检查
    # -----------------------------------------------------------
    # 检查 Redis 是否响应 'PING' 命令。
    # 这确保服务不仅正在运行，而且可操作。
    # -----------------------------------------------------------
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 3

networks:
  # 将服务附加到 'laravel-production' 网络。
  # -----------------------------------------------------------
  # 此自定义网络允许其中所有服务使用其服务名称作为主机名进行通信。
  # 例如，'php-fpm' 可以使用 'postgres' 作为主机名连接到 'postgres'。
  # -----------------------------------------------------------
  laravel-production:

volumes:
  postgres-data-production:
  laravel-storage-production:
```

> [!NOTE]
> 确保在 Laravel 项目根目录有一个 `.env` 文件，其中包含必要的配置（例如数据库和 Xdebug 设置）以匹配 Docker Compose 设置。

## 运行生产环境

要启动生产环境，请运行：

```console
$ docker compose -f compose.prod.yaml up --build -d
```

此命令将以分离模式构建并启动所有服务，为您的 Laravel 应用程序提供可扩展且可用于生产环境的设置。

## 总结

通过为 Laravel 设置生产环境的 Docker Compose，您可以确保应用程序针对性能、可扩展性和安全性进行了优化。此设置使部署保持一致且更易于管理，减少了因环境差异而导致错误的可能性。