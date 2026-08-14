---
title: 使用 Docker Compose 开发和部署 Laravel 应用
linkTitle: Laravel
summary: 学习如何使用 Docker Compose 高效地搭建 Laravel 开发和生产环境。
description: 一份关于使用 Docker Compose 管理 Laravel 应用的开发和生产环境的指南，涵盖容器配置与服务管理。
keywords: laravel, php, docker compose, web framework, development, production
aliases:
  - /frameworks/laravel/
  - /guides/frameworks/laravel/
  - /guides/frameworks/laravel/common-questions/
  - /guides/frameworks/laravel/development-setup/
  - /guides/frameworks/laravel/prerequisites/
  - /guides/frameworks/laravel/production-setup/
params:
  tags: [languages]
  time: 30 minutes
---


Laravel 是一个流行的 PHP 框架，可以让开发者快速而高效地构建 Web 应用。Docker Compose 通过在单个 YAML 文件中定义必要的服务（如 PHP、Web 服务器和数据库），简化了开发和生产环境的管理。本指南提供了一种简洁的方法，使用 Docker Compose 搭建健壮的 Laravel 环境，重点关注简单性和效率。

> **致谢**
>
> Docker 感谢 [Sergei Shitikov](https://github.com/rw4lll) 对本指南的贡献。

演示示例可以在[这个 GitHub 仓库](https://github.com/dockersamples/laravel-docker-examples)中找到。Docker Compose 为 Laravel 连接多个容器提供了一种简单直接的方法，尽管类似的设置也可以通过 Docker Swarm、Kubernetes 或单独的 Docker 容器来实现。

本指南仅供学习之用，帮助开发者针对其具体用例调整和优化配置。此外，已经有一些工具支持在容器中运行 Laravel：

- [Laravel Sail](https://laravel.com/docs/12.x/sail)：一个用于轻松在 Docker 中启动 Laravel 的官方包。
- [Laradock](https://github.com/laradock/laradock)：一个帮助在 Docker 中运行 Laravel 应用的社区项目。

## 你将学到什么（What you’ll learn）

- 如何使用 Docker Compose 搭建 Laravel 开发和生产环境。
- 定义让 Laravel 开发更轻松的服务，包括 PHP-FPM、Nginx 和数据库容器。
- 使用容器化管理 Laravel 环境的最佳实践。

## 面向谁（Who’s this for?）

- 使用 Laravel 并希望简化环境管理的开发者。
- 寻求高效管理和部署 Laravel 应用的 DevOps 工程师。

## 使用 Docker Compose 搭建 Laravel 的先决条件

在开始使用 Docker Compose 搭建 Laravel 之前，请确保满足以下先决条件：

### Docker 和 Docker Compose

你需要在系统上安装 Docker 和 Docker Compose。Docker 让你可以将应用容器化，而 Docker Compose 帮助你管理多容器应用。

- Docker：确保在你的机器上已安装并运行 Docker。请参考 [Docker 安装指南](/get-docker/) 安装 Docker。
- Docker Compose：Docker Compose 已包含在 Docker Desktop 中，但如有需要，你也可以按照 [Docker Compose 安装指南](/compose/install/) 进行安装。

### Docker 和容器的基础知识

对 Docker 及容器工作原理有基本了解会很有帮助。如果你是 Docker 新手，建议先阅读 [Docker 概览](/get-started/overview/) 以熟悉容器化的概念。

### Laravel 基础知识

本指南假设你对 Laravel 和 PHP 有基本了解。熟悉 Laravel 的命令行工具（如 [Artisan](https://laravel.com/docs/12.x/artisan)）及其项目结构，对于跟随本指南的说明非常重要。

- Laravel CLI：你应该能够自如地使用 Laravel 的命令行工具（`artisan`）。
- Laravel 项目结构：熟悉 Laravel 的文件夹结构（`app`、`config`、`routes`、`tests` 等）。

## 使用 Docker Compose 搭建 Laravel 生产环境

本指南演示如何使用 Docker 和 Docker Compose 搭建生产就绪的 Laravel 环境。该配置专为简化、可扩展且安全的 Laravel 应用部署而设计。

> [!NOTE]
> 如果想试用一个即开即用的配置，请下载 [Laravel Docker Examples](https://github.com/dockersamples/laravel-docker-examples) 仓库。它包含了针对开发和生产预先配置好的设置。

### 项目结构

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
│   │       ├── Dockerfile
│   │       └── conf.d/
│   │           └── 20-status-path.conf
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

这种布局代表了一个典型的 Laravel 项目，Docker 配置统一存放在 `docker` 目录中。你会看到**两个** Compose 文件——`compose.dev.yaml`（用于开发）和 `compose.prod.yaml`（用于生产）——以便将你的环境分隔开并便于管理。

### 为 PHP-FPM 创建 Dockerfile（生产环境）

对于生产环境，php-fpm 的 Dockerfile 会创建一个经过优化的镜像，只包含你的应用所需的 PHP 扩展和库。正如 [GitHub 示例](https://github.com/dockersamples/laravel-docker-examples) 所示，一个采用多阶段构建的 Dockerfile 可以在开发和生产之间保持一致性并减少重复。以下片段仅展示了与生产相关的阶段：

```dockerfile
# Stage 1: Build environment and Composer dependencies
FROM php:8.5-fpm AS builder

# Install system dependencies and PHP extensions for Laravel with MySQL/PostgreSQL support.
# Dependencies in this stage are only required for building the final image.
# Node.js and asset building are handled in the Nginx stage, not here.
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
    intl \
    zip \
    bcmath \
    soap \
    && pecl install redis \
    && docker-php-ext-enable redis \
    && apt-get autoremove -y && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Set the working directory inside the container
WORKDIR /var/www

# Copy the entire Laravel application code into the container
# -----------------------------------------------------------
# In Laravel, `composer install` may trigger scripts
# needing access to application code.
# For example, the `post-autoload-dump` event might execute
# Artisan commands like `php artisan package:discover`. If the
# application code (including the `artisan` file) is not
# present, these commands will fail, leading to build errors.
#
# By copying the entire application code before running
# `composer install`, we ensure that all necessary files are
# available, allowing these scripts to run successfully.
# In other cases, it would be possible to copy composer files
# first, to leverage Docker's layer caching mechanism.
# -----------------------------------------------------------
COPY . /var/www

# Install Composer and dependencies
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer \
    && composer install --no-dev --optimize-autoloader --no-interaction --no-progress --prefer-dist

# Stage 2: Production environment
FROM php:8.5-fpm AS production

# Install only runtime libraries needed in production
# libfcgi-bin and procps are required for the php-fpm-healthcheck script
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    libicu-dev \
    libzip-dev \
    libfcgi-bin \
    procps \
    && apt-get autoremove -y && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Download and install php-fpm health check script
RUN curl -o /usr/local/bin/php-fpm-healthcheck \
    https://raw.githubusercontent.com/renatomefi/php-fpm-healthcheck/master/php-fpm-healthcheck \
    && chmod +x /usr/local/bin/php-fpm-healthcheck

# Copy the initialization script
COPY ./docker/php-fpm/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Copy the initial storage structure
COPY ./storage /var/www/storage-init

# Copy PHP extensions and libraries from the builder stage
COPY --from=builder /usr/local/lib/php/extensions/ /usr/local/lib/php/extensions/
COPY --from=builder /usr/local/etc/php/conf.d/ /usr/local/etc/php/conf.d/
COPY --from=builder /usr/local/bin/docker-php-ext-* /usr/local/bin/

# Use the recommended production PHP configuration
# -----------------------------------------------------------
# PHP provides development and production configurations.
# Here, we replace the default php.ini with the production
# version to apply settings optimized for performance and
# security in a live environment.
# -----------------------------------------------------------
RUN mv "$PHP_INI_DIR/php.ini-production" "$PHP_INI_DIR/php.ini"

# Keep the image-provided FPM global config intact and add pool overrides separately
COPY ./docker/common/php-fpm/conf.d/*.conf /usr/local/etc/php-fpm.d/
# Update the variables_order to include E (for ENV)
#RUN sed -i 's/variables_order = "GPCS"/variables_order = "EGPCS"/' "$PHP_INI_DIR/php.ini"

# Copy the application code and dependencies from the build stage
COPY --from=builder /var/www /var/www

# Set working directory
WORKDIR /var/www

# Ensure correct permissions
RUN chown -R www-data:www-data /var/www

# Switch to the non-privileged user to run the application
USER www-data

# Change the default command to run the entrypoint script
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

# Expose port 9000 and start php-fpm server
EXPOSE 9000
CMD ["php-fpm"]
```

### 为 PHP-CLI 创建 Dockerfile（生产环境）

对于生产环境，你通常需要一个单独的容器来运行 Artisan 命令、迁移以及其他 CLI 任务。在大多数情况下，你可以通过复用现有的 PHP-FPM 容器来运行这些命令：

```console
$ docker compose -f compose.prod.yaml exec php-fpm php artisan route:list
```

如果你需要一个具有不同扩展或严格关注点分离的单独 CLI 容器，可以考虑使用 php-cli 的 Dockerfile：

```dockerfile
# Stage 1: Build environment and Composer dependencies
FROM php:8.5-cli AS builder

# Install system dependencies and PHP extensions required for Laravel + MySQL/PostgreSQL support
# Some dependencies are required for PHP extensions only in the build stage
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
    intl \
    zip \
    bcmath \
    soap \
    && pecl install redis \
    && docker-php-ext-enable redis \
    && apt-get autoremove -y && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Set the working directory inside the container
WORKDIR /var/www

# Copy the entire Laravel application code into the container
COPY . /var/www

# Install Composer and dependencies
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer \
    && composer install --no-dev --optimize-autoloader --no-interaction --no-progress --prefer-dist

# Stage 2: Production environment
FROM php:8.5-cli

# Install client libraries required for php extensions in runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    libicu-dev \
    libzip-dev \
    && apt-get autoremove -y && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Copy PHP extensions and libraries from the builder stage
COPY --from=builder /usr/local/lib/php/extensions/ /usr/local/lib/php/extensions/
COPY --from=builder /usr/local/etc/php/conf.d/ /usr/local/etc/php/conf.d/
COPY --from=builder /usr/local/bin/docker-php-ext-* /usr/local/bin/

# Use the default production configuration for PHP runtime arguments
RUN mv "$PHP_INI_DIR/php.ini-production" "$PHP_INI_DIR/php.ini"

# Copy the application code and dependencies from the build stage
COPY --from=builder /var/www /var/www

# Set working directory
WORKDIR /var/www

# Ensure correct permissions
RUN chown -R www-data:www-data /var/www

# Switch to the non-privileged user to run the application
USER www-data

# Default command: Provide a bash shell to allow running any command
CMD ["bash"]
```

这个 Dockerfile 与 PHP-FPM 的 Dockerfile 类似，但它使用 `php:8.5-cli` 镜像作为基础镜像，并将容器配置为运行 CLI 命令。

### 为 Nginx 创建 Dockerfile（生产环境）

Nginx 作为 Laravel 应用的 Web 服务器。你可以将静态资源直接包含到容器中。以下是一个可能的 Nginx Dockerfile 示例：

```dockerfile
# docker/nginx/Dockerfile
# Stage 1: Build assets
FROM debian AS builder

# Install Node.js and build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    nodejs \
    npm \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Set working directory
WORKDIR /var/www

# Copy Laravel application code
COPY . /var/www

# Install Node.js dependencies and build assets
RUN npm install && npm run build

# Stage 2: Nginx production image
FROM nginx:alpine

# Copy custom Nginx configuration
# -----------------------------------------------------------
# Replace the default Nginx configuration with our custom one
# that is optimized for serving a Laravel application.
# -----------------------------------------------------------
COPY ./docker/nginx/nginx.conf /etc/nginx/nginx.conf

# Copy Laravel's public assets from the builder stage
# -----------------------------------------------------------
# We only need the 'public' directory from our Laravel app.
# -----------------------------------------------------------
COPY --from=builder /var/www/public /var/www/public

# Set the working directory to the public folder
WORKDIR /var/www/public

# Expose port 80 and start Nginx
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

这个 Dockerfile 使用多阶段构建，将资源构建过程与最终的生产镜像分离开来。第一阶段安装 Node.js 并构建资源，而第二阶段则使用优化配置和构建好的资源来设置 Nginx 生产镜像。

### 为生产环境创建 Docker Compose 配置

为了将所有服务整合在一起，创建一个 `compose.prod.yaml` 文件，定义生产环境的服务、卷和网络。以下是一个示例配置：

```yaml
services:
  web:
    build:
      context: .
      dockerfile: ./docker/production/nginx/Dockerfile
    restart: unless-stopped # Automatically restart unless the service is explicitly stopped
    volumes:
      # Mount the 'laravel-storage' volume to '/var/www/storage' inside the container.
      # -----------------------------------------------------------
      # This volume stores persistent data like uploaded files and cache.
      # The ':ro' option mounts it as read-only in the 'web' service because Nginx only needs to read these files.
      # The 'php-fpm' service mounts the same volume without ':ro' to allow write operations.
      # -----------------------------------------------------------
      - laravel-storage-production:/var/www/storage:ro
    networks:
      - laravel-production
    ports:
      # Map port 80 inside the container to the port specified by 'NGINX_PORT' on the host machine.
      # -----------------------------------------------------------
      # This allows external access to the Nginx web server running inside the container.
      # For example, if 'NGINX_PORT' is set to '8080', accessing 'http://localhost:8080' will reach the application.
      # -----------------------------------------------------------
      - "${NGINX_PORT:-80}:80"
    depends_on:
      php-fpm:
        condition: service_healthy # Wait for php-fpm health check

  php-fpm:
    # For the php-fpm service, we will create a custom image to install the necessary PHP extensions and setup proper permissions.
    build:
      context: .
      dockerfile: ./docker/common/php-fpm/Dockerfile
      target: production # Use the 'production' stage in the Dockerfile
    restart: unless-stopped
    volumes:
      - laravel-storage-production:/var/www/storage # Mount the storage volume
    env_file:
      - .env
    networks:
      - laravel-production
    healthcheck:
      test: ["CMD-SHELL", "php-fpm-healthcheck || exit 1"]
      interval: 10s
      timeout: 5s
      retries: 3
    # The 'depends_on' attribute with 'condition: service_healthy' ensures that
    # this service will not start until the 'postgres' service passes its health check.
    # This prevents the application from trying to connect to the database before it's ready.
    depends_on:
      postgres:
        condition: service_healthy

  # The 'php-cli' service provides a command-line interface for running Artisan commands and other CLI tasks.
  # -----------------------------------------------------------
  # This is useful for running migrations, seeders, or any custom scripts.
  # It shares the same codebase and environment as the 'php-fpm' service.
  # -----------------------------------------------------------
  php-cli:
    build:
      context: .
      dockerfile: ./docker/php-cli/Dockerfile
    tty: true # Enables an interactive terminal
    stdin_open: true # Keeps standard input open for 'docker exec'
    env_file:
      - .env
    networks:
      - laravel-production

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
    # Health check for PostgreSQL
    # -----------------------------------------------------------
    # Health checks allow Docker to determine if a service is operational.
    # The 'pg_isready' command checks if PostgreSQL is ready to accept connections.
    # This prevents dependent services from starting before the database is ready.
    # -----------------------------------------------------------
    healthcheck:
      test: ["CMD", "pg_isready"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:alpine
    restart: unless-stopped # Automatically restart unless the service is explicitly stopped
    networks:
      - laravel-production
    # Health check for Redis
    # -----------------------------------------------------------
    # Checks if Redis is responding to the 'PING' command.
    # This ensures that the service is not only running but also operational.
    # -----------------------------------------------------------
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 3

networks:
  # Attach the service to the 'laravel-production' network.
  # -----------------------------------------------------------
  # This custom network allows all services within it to communicate using their service names as hostnames.
  # For example, 'php-fpm' can connect to 'postgres' by using 'postgres' as the hostname.
  # -----------------------------------------------------------
  laravel-production:

volumes:
  postgres-data-production:
  laravel-storage-production:
```

> [!NOTE]
> 请确保你的 Laravel 项目根目录下有一个 `.env` 文件，其中包含与 Docker Compose 配置相匹配的必要设置。

### 运行你的生产环境

要启动生产环境，请运行：

```console
$ docker compose -f compose.prod.yaml up --build -d
```

该命令会以分离（detached）模式构建并启动所有服务，为你的 Laravel 应用提供一个可扩展且生产就绪的设置。

### 小结

通过为 Laravel 搭建 Docker Compose 生产环境，你可以确保应用针对性能、可扩展性和安全性进行了优化。这种设置使部署保持一致且更易于管理，减少了因环境差异导致错误的可能性。

## 使用 Docker Compose 搭建 Laravel 开发环境

本指南演示如何使用 Docker 和 Docker Compose 为 Laravel 应用配置**开发**环境。它在 PHP-FPM 的生产镜像**之上**构建，然后添加以开发者为中心的功能——例如 Xdebug——以简化调试。通过让开发容器基于已知的生产镜像，你可以让两个环境保持高度一致。

这个设置包含 PHP-FPM、Nginx 和 PostgreSQL 服务（尽管你可以轻松地将 PostgreSQL 换成另一个数据库，如 MySQL 或 MariaDB）。所有内容都在容器中运行，因此你可以隔离开发，而无需改动你的宿主机系统。

> [!NOTE]
> 如果想试用一个即开即用的配置，请下载 [Laravel Docker Examples](https://github.com/dockersamples/laravel-docker-examples) 仓库。它包含了针对开发和生产预先配置好的设置。

### 项目结构

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
│   │   ├── php-fpm/
│   │   │   └── entrypoint.sh
│   │   ├── workspace/
│   │   │   └── Dockerfile
│   │   └── nginx
│   │       ├── Dockerfile
│   │       └── nginx.conf
│   └── production/
├── compose.dev.yaml
├── compose.prod.yaml
├── .dockerignore
├── .env
├── vendor/
├── ...
```

这种布局代表了一个典型的 Laravel 项目，Docker 配置统一存放在 `docker` 目录中。你会看到**两个** Compose 文件——`compose.dev.yaml`（用于开发）和 `compose.prod.yaml`（用于生产）——以便将你的环境分隔开并便于管理。

该环境包含一个 `workspace` 服务，这是一个用于构建前端资源、运行 Artisan 命令以及你的项目可能需要的其他 CLI 工具的 sidecar（边车）容器。虽然这个额外的容器看起来有些不寻常，但它在 **Laravel Sail** 和 **Laradock** 等方案中是一种常见模式。它还包含了 **Xdebug** 以辅助调试。

### 为 PHP-FPM 创建 Dockerfile

这个 Dockerfile 通过安装 Xdebug 并调整用户权限来简化本地开发，从而**扩展**了生产镜像。这样一来，你的开发环境在与生产环境保持一致的同时，还提供了额外的调试功能和更好的文件挂载体验。

```dockerfile
# Builds a dev-only layer on top of the production image
FROM production AS development

# Use ARGs to define environment variables passed from the Docker build command or Docker Compose.
ARG XDEBUG_ENABLED=true
ARG XDEBUG_MODE=develop,coverage,debug,profile
ARG XDEBUG_HOST=host.docker.internal
ARG XDEBUG_IDE_KEY=DOCKER
ARG XDEBUG_LOG=/dev/stdout
ARG XDEBUG_LOG_LEVEL=0

USER root

# Configure Xdebug if enabled
RUN if [ "${XDEBUG_ENABLED}" = "true" ]; then \
    pecl install xdebug && \
    docker-php-ext-enable xdebug && \
    echo "xdebug.mode=${XDEBUG_MODE}" >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini && \
    echo "xdebug.idekey=${XDEBUG_IDE_KEY}" >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini && \
    echo "xdebug.log=${XDEBUG_LOG}" >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini && \
    echo "xdebug.log_level=${XDEBUG_LOG_LEVEL}" >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini && \
    echo "xdebug.client_host=${XDEBUG_HOST}" >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini ; \
    echo "xdebug.start_with_request=yes" >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini ; \
    fi

# Add ARGs for syncing permissions
ARG UID=1000
ARG GID=1000

# Create a new user with the specified UID and GID, reusing an existing group if GID exists
RUN if getent group ${GID}; then \
      group_name=$(getent group ${GID} | cut -d: -f1); \
      useradd -m -u ${UID} -g ${GID} -s /bin/bash www; \
    else \
      groupadd -g ${GID} www && \
      useradd -m -u ${UID} -g www -s /bin/bash www; \
      group_name=www; \
    fi

# Dynamically update php-fpm to use the new user and group
RUN sed -i "s/user = www-data/user = www/g" /usr/local/etc/php-fpm.d/www.conf && \
    sed -i "s/group = www-data/group = $group_name/g" /usr/local/etc/php-fpm.d/www.conf


# Set the working directory
WORKDIR /var/www

# Copy the entrypoint script
COPY ./docker/development/php-fpm/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Switch back to the non-privileged user to run the application
USER www-data

# Change the default command to run the entrypoint script
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

# Expose port 9000 and start php-fpm server
EXPOSE 9000
CMD ["php-fpm"]
```

### 为 Workspace 创建 Dockerfile

一个 workspace 容器提供了一个专用的 shell，用于构建资源、运行 Artisan/Composer 命令以及其他 CLI 任务。这种方式遵循了 Laravel Sail 和 Laradock 的模式，将所有开发工具整合到一个容器中，方便使用。

```dockerfile
# docker/development/workspace/Dockerfile
# Use the official PHP CLI image as the base
FROM php:8.5-cli

# Set environment variables for user and group ID
ARG UID=1000
ARG GID=1000
ARG NODE_VERSION=22.0.0

# Install system dependencies and build libraries
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
    intl \
    zip \
    bcmath \
    soap \
    && pecl install redis \
    && docker-php-ext-enable redis \
    && curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer \
    && apt-get autoremove -y && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Use ARG to define environment variables passed from the Docker build command or Docker Compose.
ARG XDEBUG_ENABLED
ARG XDEBUG_MODE
ARG XDEBUG_HOST
ARG XDEBUG_IDE_KEY
ARG XDEBUG_LOG
ARG XDEBUG_LOG_LEVEL

# Configure Xdebug if enabled
RUN if [ "${XDEBUG_ENABLED}" = "true" ]; then \
    pecl install xdebug && \
    docker-php-ext-enable xdebug && \
    echo "xdebug.mode=${XDEBUG_MODE}" >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini && \
    echo "xdebug.idekey=${XDEBUG_IDE_KEY}" >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini && \
    echo "xdebug.log=${XDEBUG_LOG}" >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini && \
    echo "xdebug.log_level=${XDEBUG_LOG_LEVEL}" >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini && \
    echo "xdebug.client_host=${XDEBUG_HOST}" >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini ; \
    echo "xdebug.start_with_request=yes" >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini ; \
    fi

# If the group already exists, use it; otherwise, create the 'www' group
RUN if getent group ${GID}; then \
      useradd -m -u ${UID} -g ${GID} -s /bin/bash www; \
    else \
      groupadd -g ${GID} www && \
      useradd -m -u ${UID} -g www -s /bin/bash www; \
    fi && \
    usermod -aG sudo www && \
    echo 'www ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

# Switch to the non-root user to install NVM and Node.js
USER www

# Install NVM (Node Version Manager) as the www user
RUN export NVM_DIR="$HOME/.nvm" && \
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh | bash && \
    [ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh" && \
    nvm install ${NODE_VERSION} && \
    nvm alias default ${NODE_VERSION} && \
    nvm use default

# Ensure NVM is available for all future shells
RUN echo 'export NVM_DIR="$HOME/.nvm"' >> /home/www/.bashrc && \
    echo '[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"' >> /home/www/.bashrc && \
    echo '[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"' >> /home/www/.bashrc

# Set the working directory
WORKDIR /var/www

# Override the entrypoint to avoid the default php entrypoint
ENTRYPOINT []

# Default command to keep the container running
CMD ["bash"]
```

> [!NOTE]
> 如果你更喜欢**一个容器一个服务**的方式，只需省略 workspace 容器，并为每个任务运行单独的容器即可。例如，你可以使用一个专用的 `php-cli` 容器来运行 PHP 脚本，以及一个 `node` 容器来处理资源构建。

### 为开发环境创建 Docker Compose 配置

以下是用于搭建开发环境的 `compose.yaml` 文件：

```yaml
services:
  web:
    image: nginx:latest # Using the default Nginx image with custom configuration.
    volumes:
      # Mount the application code for live updates
      - ./:/var/www
      # Mount the Nginx configuration file
      - ./docker/development/nginx/nginx.conf:/etc/nginx/nginx.conf:ro
    ports:
      # Map port 80 inside the container to the port specified by 'NGINX_PORT' on the host machine
      - "80:80"
    environment:
      - NGINX_HOST=localhost
    networks:
      - laravel-development
    depends_on:
      php-fpm:
        condition: service_started # Wait for php-fpm to start

  php-fpm:
    # For the php-fpm service, we will use our common PHP-FPM Dockerfile with the development target
    build:
      context: .
      dockerfile: ./docker/common/php-fpm/Dockerfile
      target: development
      args:
        UID: ${UID:-1000}
        GID: ${GID:-1000}
        XDEBUG_ENABLED: ${XDEBUG_ENABLED:-true}
        XDEBUG_MODE: develop,coverage,debug,profile
        XDEBUG_HOST: ${XDEBUG_HOST:-host.docker.internal}
        XDEBUG_IDE_KEY: ${XDEBUG_IDE_KEY:-DOCKER}
        XDEBUG_LOG: /dev/stdout
        XDEBUG_LOG_LEVEL: 0
    env_file:
      # Load the environment variables from the Laravel application
      - .env
    user: "${UID:-1000}:${GID:-1000}"
    volumes:
      # Mount the application code for live updates
      - ./:/var/www
    networks:
      - laravel-development
    depends_on:
      postgres:
        condition: service_started # Wait for postgres to start

  workspace:
    # For the workspace service, we will also create a custom image to install and setup all the necessary stuff.
    build:
      context: .
      dockerfile: ./docker/development/workspace/Dockerfile
      args:
        UID: ${UID:-1000}
        GID: ${GID:-1000}
        XDEBUG_ENABLED: ${XDEBUG_ENABLED:-true}
        XDEBUG_MODE: develop,coverage,debug,profile
        XDEBUG_HOST: ${XDEBUG_HOST:-host.docker.internal}
        XDEBUG_IDE_KEY: ${XDEBUG_IDE_KEY:-DOCKER}
        XDEBUG_LOG: /dev/stdout
        XDEBUG_LOG_LEVEL: 0
    tty: true # Enables an interactive terminal
    stdin_open: true # Keeps standard input open for 'docker exec'
    env_file:
      - .env
    volumes:
      - ./:/var/www
    networks:
      - laravel-development

  postgres:
    image: postgres:18
    ports:
      - "${POSTGRES_PORT:-5432}:5432"
    environment:
      - POSTGRES_DB=app
      - POSTGRES_USER=laravel
      - POSTGRES_PASSWORD=secret
    volumes:
      - postgres-data-development:/var/lib/postgresql
    networks:
      - laravel-development

  redis:
    image: redis:alpine
    networks:
      - laravel-development

networks:
  laravel-development:

volumes:
  postgres-data-development:
```

> [!NOTE]
> 请确保你的 Laravel 项目根目录下有一个包含必要配置的 `.env` 文件。你可以以 `.env.example` 文件作为模板。

### 运行你的开发环境

要启动开发环境，请使用：

```console
$ docker compose -f compose.dev.yaml up --build -d
```

运行此命令以分离模式构建并启动开发环境。当容器完成初始化后，访问 [http://localhost/](http://localhost/) 即可看到你的 Laravel 应用运行起来。

### 小结

通过在生产镜像之上构建并添加 Xdebug 等调试工具，你可以创建一个与生产环境高度一致的 Laravel 开发工作流。可选的 workspace 容器简化了资源构建和运行 Artisan 命令等任务。如果你希望为每个服务使用单独的容器（例如专用的 `php-cli` 和 `node` 容器），也可以不使用 workspace 方案。无论采用哪种方式，Docker Compose 都为你开发 Laravel 项目提供了一种高效、一致的方法。

## 使用 Laravel 与 Docker 的常见问题

<!-- vale Docker.HeadingLength = NO -->

### 1. 为什么我应该使用 Docker Compose 来运行 Laravel？

Docker Compose 是管理多容器环境的强大工具，尤其是在开发环境中，因其简单性而备受青睐。借助 Docker Compose，你可以在单个配置（`compose.*.yaml`）中定义并连接 Laravel 所需的全部服务，例如 PHP、Nginx 和数据库。这种设置确保了开发、测试和生产环境之间的一致性，简化了上手过程，并减少了本地与服务器配置之间的差异。

虽然 Docker Compose 是开发环境的绝佳选择，但像 **Docker Swarm** 或 **Kubernetes** 这样的工具提供了更高级的扩展和编排功能，可能对复杂的生产部署更为有利。

### 2. 如何使用 Docker Compose 调试我的 Laravel 应用？

要在 Docker 环境中调试你的 Laravel 应用，请使用 **Xdebug**。在开发环境设置中，Xdebug 被安装在 `php-fpm` 容器中以启用调试功能。请确保在你的 `compose.dev.yaml` 文件中通过将环境变量 `XDEBUG_ENABLED=true` 来启用 Xdebug，并配置你的 IDE（例如 Visual Studio Code 或 PHPStorm）以连接到远程容器进行调试。

### 3. 我可以将 Docker Compose 用于 PostgreSQL 以外的数据库吗？

可以，Docker Compose 支持 Laravel 的多种数据库服务。虽然示例中使用了 PostgreSQL，但你可以轻松替换为 **MySQL**、**MariaDB**，甚至是 **SQLite**。更新 `compose.*.yaml` 文件以指定所需的 Docker 镜像，并调整你的 `.env` 文件以反映新的数据库配置。

### 4. 我该如何在开发和生产环境中持久化数据？

在开发和生产环境中，都使用 Docker 卷来持久化数据。例如，在 `compose.*.yaml` 文件中，`postgres-data-*` 卷用于存储 PostgreSQL 数据，确保即使容器重启，数据也能保留。你也可以为其他需要数据持久化的服务定义命名卷。

### 5. 开发环境和生产环境的 Docker 配置有什么区别？

在开发环境中，Docker 配置包含简化编码和调试的工具，例如用于调试的 Xdebug，以及用于在不重新构建镜像的情况下实现实时代码更新的卷挂载。

在生产环境中，配置针对性能、安全性和效率进行了优化。这种设置使用多阶段构建来保持镜像轻量，并且只包含必要的工具、包和库。

建议在生产环境中使用基于 `alpine` 的镜像，以获得更小的镜像体积，从而提升部署速度和安全性。

此外，考虑使用 [Docker Scout](/manuals/scout/_index.md) 来检测和分析漏洞，尤其是在生产环境中。

有关在生产环境中使用 Docker Compose 的更多信息，请参阅 [本指南](/compose/how-tos/production/)。
