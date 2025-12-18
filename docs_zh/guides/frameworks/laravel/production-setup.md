---
title: 使用 Docker Compose 搭建 Laravel 生产环境
description: 使用 Docker 和 Docker Compose 搭建生产就绪的 Laravel 环境。
weight: 20
---

本指南演示如何使用 Docker 和 Docker Compose 搭建生产就绪的 Laravel 环境。此配置旨在实现 Laravel 应用的简化、可扩展和安全的部署。

> [!NOTE]
> 如需体验现成的配置，请下载 [Laravel Docker 示例](https://github.com/dockersamples/laravel-docker-examples) 仓库。其中包含开发和生产环境的预配置设置。

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

此布局代表典型的 Laravel 项目，Docker 配置统一存储在 `docker` 目录中。你会看到 **两个** Compose 文件 —— `compose.dev.yaml`（用于开发）和 `compose.prod.yaml`（用于生产），以保持环境分离且易于管理。

## 为 PHP-FPM（生产环境）创建 Dockerfile

对于生产环境，`php-fpm` Dockerfile 创建一个优化的镜像，仅包含应用所需的 PHP 扩展和库。如 [GitHub 示例](https://github.com/dockersamples/laravel-docker-examples) 所示，使用多阶段构建的单个 Dockerfile 保持开发和生产环境的一致性，并减少重复。以下代码片段仅显示与生产相关的阶段：

```dockerfile
# 阶段 1：构建环境和 Composer 依赖
FROM php:8.4-fpm AS builder

# 安装系统依赖和 Laravel 所需的 PHP 扩展（支持 MySQL/PostgreSQL）
# 此阶段的依赖仅用于构建最终镜像
# Node.js 和资源构建在 Nginx 阶段处理，此处不涉及
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

# 设置容器内工作目录
WORKDIR /var/www

# 将整个 Laravel 应用代码复制到容器中
# -----------------------------------------------------------
# 在 Laravel 中，`composer install` 可能触发需要访问应用代码的脚本
# 例如，`post-autoload-dump` 事件可能执行
# Artisan 命令如 `php artisan package:discover`。如果应用代码（包括 `artisan` 文件）不存在，
# 这些命令将失败，导致构建错误
#
# 通过在运行 `composer install` 之前复制整个应用代码，我们确保所有必要文件都可用，
# 使这些脚本能够成功运行
# 在其他情况下，可以先复制 composer 文件，
# 以利用 Docker 的层缓存机制
# -----------------------------------------------------------
COPY . /var/www

# 安装 Composer 和依赖
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer \
    && composer install --no-dev --optimize-autoloader --no-interaction --no-progress --prefer-dist

# 阶段 2：生产环境
FROM php:8.4-fpm AS production

# 仅安装生产环境所需的运行时库
# libfcgi-bin 和 procps 是 php-fpm-healthcheck 脚本所需
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

# 复制初始存储结构
COPY ./storage /var/www/storage-init

# 从构建阶段复制 PHP 扩展和库
COPY --from=builder /usr/local/lib/php/extensions/ /usr/local/lib/php/extensions/
COPY --from=builder /usr/local/etc/php/conf.d/ /usr/local/etc/php/conf.d/
COPY --from=builder /usr/local/bin/docker-php-ext-* /usr/local/bin/

# 使用推荐的生产环境 PHP 配置
# -----------------------------------------------------------
# PHP 提供开发和生产配置
# 此处，我们将默认 php.ini 替换为生产版本，
# 以在生产环境中应用针对性能和安全性优化的设置
# -----------------------------------------------------------
RUN mv "$PHP_INI_DIR/php.ini-production" "$PHP_INI_DIR/php.ini"

# 通过 sed 修改 zz-docker.conf 启用 PHP-FPM 状态页面
RUN sed -i '/\[www\]/a pm.status_path = /status' /usr/local/etc/php-fpm.d/zz-docker.conf
# 更新 variables_order 以包含 E（用于 ENV）
#RUN sed -i 's/variables_order = "GPCS"/variables_order = "EGPCS"/' "$PHP_INI_DIR/php.ini"

# 从构建阶段复制应用代码和依赖
COPY --from=builder /var/www /var/www

# 设置工作目录
WORKDIR /var/www

# 确保正确的权限
RUN chown -R www-data:www-data /var/www

# 切换到非特权用户运行应用
USER www-data

# 更改默认命令以运行入口脚本
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

# 暴露端口 9000 并启动 php-fpm 服务器
EXPOSE 9000
CMD ["php-fpm"]
```

## 为 PHP-CLI（生产环境）创建 Dockerfile

在生产环境中，你通常需要一个独立容器来运行 Artisan 命令、迁移和其他 CLI 任务。在大多数情况下，你可以通过复用现有的 PHP-FPM 容器来运行这些命令：

```console
$ docker compose -f compose.prod.yaml exec php-fpm php artisan route:list
```

如果你需要一个具有不同扩展或严格关注点分离的独立 CLI 容器，可以考虑使用 php-cli Dockerfile：

```dockerfile
# 阶段 1：构建环境和 Composer 依赖
FROM php:8.4-cli AS builder

# 安装 Laravel 所需的系统依赖和 PHP 扩展（支持 MySQL/PostgreSQL）
# 某些依赖仅在构建阶段用于 PHP 扩展
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

# 设置容器内工作目录
WORKDIR /var/www

# 将整个 Laravel 应用代码复制到容器中
COPY . /var/www

# 安装 Composer 和依赖
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer \
    && composer install --no-dev --optimize-autoloader --no-interaction --no-progress --prefer-dist

# 阶段 2：生产环境
FROM php:8.4-cli

# 安装运行时所需的客户端库
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    libicu-dev \
    libzip-dev \
    && apt-get autoremove -y && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# 从构建阶段复制 PHP 扩展和库
COPY --from=builder /usr/local/lib/php/extensions/ /usr/local/lib/php/extensions/
COPY --from=builder /usr/local/etc/php/conf.d/ /usr/local/etc/php/conf.d/
COPY --from=builder /usr/local/bin/docker-php-ext-* /usr/local/bin/

# 使用默认的生产环境配置作为 PHP 运行时参数
RUN mv "$PHP_INI_DIR/php.ini-production" "$PHP_INI_DIR/php.ini"

# 从构建阶段复制应用代码和依赖
COPY --from=builder /var/www /var/www

# 设置工作目录
WORKDIR /var/www

# 确保正确的权限
RUN chown -R www-data:www-data /var/www

# 切换到非特权用户运行应用
USER www-data

# 默认命令：提供 bash shell 以允许运行任何命令
CMD ["bash"]
```

此 Dockerfile 与 PHP-FPM Dockerfile 类似，但使用 `php:8.4-cli` 镜像作为基础镜像，并为运行 CLI 命令设置容器。

## 为 Nginx（生产环境）创建 Dockerfile

Nginx 作为 Laravel 应用的 Web 服务器。你可以直接将静态资源包含到容器中。以下是 Nginx 的 Dockerfile 示例：

```dockerfile
# docker/nginx/Dockerfile
# 阶段 1：构建资源
FROM debian AS builder

# 安装 Node.js 和构建工具
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    nodejs \
    npm \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# 设置工作目录
WORKDIR /var/www

# 复制 Laravel 应用代码
COPY . /var/www

# 安装 Node.js 依赖并构建资源
RUN npm install && npm run build

# 阶段 2：Nginx 生产镜像
FROM nginx:alpine

# 复制自定义 Nginx 配置
# -----------------------------------------------------------
# 使用优化的自定义配置替换默认的 Nginx 配置，
# 以更好地服务 Laravel 应用
# -----------------------------------------------------------
COPY ./docker/nginx/nginx.conf /etc/nginx/nginx.conf

# 从构建阶段复制 Laravel 的公共资源
# -----------------------------------------------------------
# 我们只需要应用的 'public' 目录
# -----------------------------------------------------------
COPY --from=builder /var/www/public /var/www/public

# 将工作目录设置为公共文件夹
WORKDIR /var/www/public

# 暴露端口 80 并启动 Nginx
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

此 Dockerfile 使用多阶段构建将资源构建过程与最终的生产镜像分离。第一阶段安装 Node.js 并构建资源，第二阶段设置带有优化配置和构建资源的 Nginx 生产镜像。

## 为生产环境创建 Docker Compose 配置

为整合所有服务，创建 `compose.prod.yaml` 文件，定义生产环境的服务、卷和网络。以下为示例配置：

```yaml
services:
  web:
    build:
      context: .
      dockerfile: ./docker/production/nginx/Dockerfile
    restart: unless-stopped # 自动重启，除非服务被显式停止
    volumes:
      # 将 'laravel-storage-production' 卷挂载到容器内的 '/var/www/storage'
      # -----------------------------------------------------------
      # 此卷存储持久化数据，如上传文件和缓存
      # ':ro' 选项将其挂载为只读，因为 Nginx 只需读取这些文件
      # 'php-fpm' 服务将同一卷挂载为非只读以允许写入操作
      # -----------------------------------------------------------
      - laravel-storage-production:/var/www/storage:ro
    networks:
      - laravel-production
    ports:
      # 将容器内的端口 80 映射到主机上由 'NGINX_PORT' 指定的端口
      # -----------------------------------------------------------
      # 这允许从外部访问容器内运行的 Nginx Web 服务器
      # 例如，如果 'NGINX_PORT' 设置为 '8080'，访问 'http://localhost:8080' 即可到达应用
      # -----------------------------------------------------------
      - "${NGINX_PORT:-80}:80"
    depends_on:
      php-fpm:
        condition: service_healthy # 等待 php-fpm 健康检查

  php-fpm:
    # 对于 php-fpm 服务，我们将创建一个自定义镜像以安装必要的 PHP 扩展并设置正确权限
    build:
      context: .
      dockerfile: ./docker/common/php-fpm/Dockerfile
      target: production # 使用 Dockerfile 中的 'production' 阶段
    restart: unless-stopped
    volumes:
      - laravel-storage-production:/var/www/storage # 挂载存储卷
    env_file:
      - .env
    networks:
      - laravel-production
    healthcheck:
      test: ["CMD-SHELL", "php-fpm-healthcheck || exit 1"]
      interval: 10s
      timeout: 5s
      retries: 3
    # 'depends_on' 属性与 'condition: service_healthy' 确保此服务在 'postgres' 服务通过健康检查后才启动
    # 这防止应用尝试在数据库就绪前连接
    depends_on:
      postgres:
        condition: service_healthy

  # 'php-cli' 服务提供命令行接口，用于运行 Artisan 命令和其他 CLI 任务
  # -----------------------------------------------------------
  # 这对运行迁移、填充器或任何自定义脚本很有用
  # 它与 'php-fpm' 服务共享相同的代码库和环境
  # -----------------------------------------------------------
  php-cli:
    build:
      context: .
      dockerfile: ./docker/php-cli/Dockerfile
    tty: true # 启用交互式终端
    stdin_open: true # 为 'docker exec' 保持标准输入开启
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
    # 健康检查允许 Docker 确定服务是否运行正常
    # 'pg_isready' 命令检查 PostgreSQL 是否已准备好接受连接
    # 这防止依赖服务在数据库就绪前启动
    # -----------------------------------------------------------
    healthcheck:
      test: ["CMD", "pg_isready"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:alpine
    restart: unless-stopped # 自动重启，除非服务被显式停止
    networks:
      - laravel-production
    # Redis 健康检查
    # -----------------------------------------------------------
    # 检查 Redis 是否响应 'PING' 命令
    # 这确保服务不仅运行，而且可操作
    # -----------------------------------------------------------
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 3

networks:
  # 将服务附加到 'laravel-production' 网络
  # -----------------------------------------------------------
  # 此自定义网络允许其内所有服务使用服务名称作为主机名进行通信
  # 例如，'php-fpm' 可通过使用 'postgres' 作为主机名连接到 'postgres'
  # -----------------------------------------------------------
  laravel-production:

volumes:
  postgres-data-production:
  laravel-storage-production:
```

> [!NOTE]
> 确保 Laravel 项目根目录有 `.env` 文件，包含必要的配置（如数据库和 Xdebug 设置），以匹配 Docker Compose 设置。

## 运行你的生产环境

要启动生产环境，运行：

```console
$ docker compose -f compose.prod.yaml up --build -d
```

此命令将在分离模式下构建并启动所有服务，为你的 Laravel 应用提供可扩展且生产就绪的设置。

## 总结

通过为 Laravel 设置 Docker Compose 生产环境，你确保应用针对性能、可扩展性和安全性进行了优化。此设置使部署保持一致且更易于管理，减少了因环境差异导致错误的可能性。