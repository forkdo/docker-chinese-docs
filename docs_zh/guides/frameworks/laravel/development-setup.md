---
title: 使用 Docker Compose 进行 Laravel 开发环境设置
description: 使用 Docker Compose 设置 Laravel 开发环境。
weight: 30
---

本指南演示如何使用 Docker 和 Docker Compose 为 Laravel 应用程序配置**开发**环境。它在 PHP-FPM 的生产镜像**之上**构建，然后添加了面向开发人员的功能——例如 Xdebug——以简化调试。通过基于已知的生产镜像构建开发容器，您可以保持两个环境紧密一致。

此设置包括 PHP-FPM、Nginx 和 PostgreSQL 服务（尽管您可以轻松地将 PostgreSQL 替换为其他数据库，如 MySQL 或 MariaDB）。一切都在容器中运行，因此您可以在隔离环境中开发，而无需更改主机系统。

> [!NOTE]
> 要试用一个即用型配置，请下载 [Laravel Docker Examples](https://github.com/dockersamples/laravel-docker-examples) 仓库。它包含针对开发和生产的预配置设置。

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

此布局代表了一个典型的 Laravel 项目，Docker 配置存储在统一的 `docker` 目录中。您会发现**两个** Compose 文件——`compose.dev.yaml`（用于开发）和 `compose.prod.yaml`（用于生产）——以保持环境分离且易于管理。

环境包含一个 `workspace` 服务，这是一个辅助容器，用于执行诸如构建前端资源、运行 Artisan 命令以及项目可能需要的其他 CLI 工具等任务。虽然这个额外的容器看起来可能有些不寻常，但它是 **Laravel Sail** 和 **Laradock** 等解决方案中熟悉的模式。它还包含 **Xdebug** 以辅助调试。

## 为 PHP-FPM 创建 Dockerfile

此 Dockerfile 通过安装 Xdebug 并调整用户权限以简化本地开发，从而**扩展**了生产镜像。这样，您的开发环境与生产环境保持一致，同时仍提供额外的调试功能和改进的文件挂载。

```dockerfile
# 在生产镜像之上构建仅用于开发的层
FROM production AS development

# 使用 ARG 定义从 Docker 构建命令或 Docker Compose 传递的环境变量。
ARG XDEBUG_ENABLED=true
ARG XDEBUG_MODE=develop,coverage,debug,profile
ARG XDEBUG_HOST=host.docker.internal
ARG XDEBUG_IDE_KEY=DOCKER
ARG XDEBUG_LOG=/dev/stdout
ARG XDEBUG_LOG_LEVEL=0

USER root

# 如果启用则配置 Xdebug
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

# 添加用于同步权限的 ARG
ARG UID=1000
ARG GID=1000

# 使用指定的 UID 和 GID 创建新用户，如果 GID 已存在则重用现有组
RUN if getent group ${GID}; then \
      group_name=$(getent group ${GID} | cut -d: -f1); \
      useradd -m -u ${UID} -g ${GID} -s /bin/bash www; \
    else \
      groupadd -g ${GID} www && \
      useradd -m -u ${UID} -g www -s /bin/bash www; \
      group_name=www; \
    fi

# 动态更新 php-fpm 以使用新的用户和组
RUN sed -i "s/user = www-data/user = www/g" /usr/local/etc/php-fpm.d/www.conf && \
    sed -i "s/group = www-data/group = $group_name/g" /usr/local/etc/php-fpm.d/www.conf


# 设置工作目录
WORKDIR /var/www

# 复制入口点脚本
COPY ./docker/development/php-fpm/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# 切换回非特权用户以运行应用程序
USER www-data

# 更改默认命令以运行入口点脚本
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

# 暴露端口 9000 并启动 php-fpm 服务器
EXPOSE 9000
CMD ["php-fpm"]
```

## 为 Workspace 创建 Dockerfile

工作区容器提供了一个专用的 shell，用于资源编译、Artisan/Composer 命令和其他 CLI 任务。这种方法遵循 Laravel Sail 和 Laradock 的模式，将所有开发工具整合到一个容器中以方便使用。

```dockerfile
# docker/development/workspace/Dockerfile
# 使用官方的 PHP CLI 镜像作为基础
FROM php:8.4-cli

# 设置用户和组 ID 的环境变量
ARG UID=1000
ARG GID=1000
ARG NODE_VERSION=22.0.0

# 安装系统依赖和构建库
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
    && pecl install redis xdebug \
    && docker-php-ext-enable redis xdebug\
    && curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer \
    && apt-get autoremove -y && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# 使用 ARG 定义从 Docker 构建命令或 Docker Compose 传递的环境变量。
ARG XDEBUG_ENABLED
ARG XDEBUG_MODE
ARG XDEBUG_HOST
ARG XDEBUG_IDE_KEY
ARG XDEBUG_LOG
ARG XDEBUG_LOG_LEVEL

# 如果启用则配置 Xdebug
RUN if [ "${XDEBUG_ENABLED}" = "true" ]; then \
    docker-php-ext-enable xdebug && \
    echo "xdebug.mode=${XDEBUG_MODE}" >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini && \
    echo "xdebug.idekey=${XDEBUG_IDE_KEY}" >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini && \
    echo "xdebug.log=${XDEBUG_LOG}" >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini && \
    echo "xdebug.log_level=${XDEBUG_LOG_LEVEL}" >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini && \
    echo "xdebug.client_host=${XDEBUG_HOST}" >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini ; \
    echo "xdebug.start_with_request=yes" >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini ; \
fi

# 如果组已存在，则使用它；否则创建 'www' 组
RUN if getent group ${GID}; then \
      useradd -m -u ${UID} -g ${GID} -s /bin/bash www; \
    else \
      groupadd -g ${GID} www && \
      useradd -m -u ${UID} -g www -s /bin/bash www; \
    fi && \
    usermod -aG sudo www && \
    echo 'www ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

# 切换到非 root 用户以安装 NVM 和 Node.js
USER www

# 以 www 用户身份安装 NVM (Node Version Manager)
RUN export NVM_DIR="$HOME/.nvm" && \
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh | bash && \
    [ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh" && \
    nvm install ${NODE_VERSION} && \
    nvm alias default ${NODE_VERSION} && \
    nvm use default

# 确保 NVM 对所有未来的 shell 可用
RUN echo 'export NVM_DIR="$HOME/.nvm"' >> /home/www/.bashrc && \
    echo '[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"' >> /home/www/.bashrc && \
    echo '[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"' >> /home/www/.bashrc

# 设置工作目录
WORKDIR /var/www

# 覆盖入口点以避免默认的 php 入口点
ENTRYPOINT []

# 保持容器运行的默认命令
CMD ["bash"]
```

> [!NOTE]
> 如果您更喜欢**每个容器一个服务**的方法，只需省略工作区容器，并为每个任务运行单独的容器。例如，您可以使用专用的 `php-cli` 容器来运行 PHP 脚本，并使用 `node` 容器来处理资源构建。

## 为开发创建 Docker Compose 配置

以下是用于设置开发环境的 `compose.yaml` 文件：

```yaml
services:
  web:
    image: nginx:latest # 使用默认的 Nginx 镜像并自定义配置。
    volumes:
      # 挂载应用程序代码以实现实时更新
      - ./:/var/www
      # 挂载 Nginx 配置文件
      - ./docker/development/nginx/nginx.conf:/etc/nginx/nginx.conf:ro
    ports:
      # 将容器内的端口 80 映射到主机上由 'NGINX_PORT' 指定的端口
      - "80:80"
    environment:
      - NGINX_HOST=localhost
    networks:
      - laravel-development
    depends_on:
      php-fpm:
        condition: service_started # 等待 php-fpm 启动

  php-fpm:
    # 对于 php-fpm 服务，我们将使用我们通用的 PHP-FPM Dockerfile 并以 development 为目标
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
      # 从 Laravel 应用程序加载环境变量
      - .env
    user: "${UID:-1000}:${GID:-1000}"
    volumes:
      # 挂载应用程序代码以实现实时更新
      - ./:/var/www
    networks:
      - laravel-development
    depends_on:
      postgres:
        condition: service_started # 等待 postgres 启动

  workspace:
    # 对于工作区服务，我们也将创建一个自定义镜像来安装和设置所有必要的东西。
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
    tty: true # 启用交互式终端
    stdin_open: true # 保持标准输入打开以供 'docker exec' 使用
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
> 确保在 Laravel 项目的根目录下有一个包含必要配置的 `.env` 文件。您可以使用 `.env.example` 文件作为模板。

## 运行您的开发环境

要启动开发环境，请使用：

```console
$ docker compose -f compose.dev.yaml up --build -d
```

运行此命令以在分离模式下构建并启动开发环境。当容器完成初始化后，访问 [http://localhost/](http://localhost/) 以查看您的 Laravel 应用运行情况。

## 总结

通过在生产镜像之上构建并添加 Xdebug 等调试工具，您可以创建一个与生产环境非常相似的 Laravel 开发工作流程。可选的工作区容器简化了资源构建和运行 Artisan 命令等任务。如果您更喜欢为每个服务使用单独的容器（例如，专用的 `php-cli` 和 `node` 容器），则可以跳过工作区方法。无论哪种方式，Docker Compose 都提供了一种高效、一致的方式来开发您的 Laravel 项目。