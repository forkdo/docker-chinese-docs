---
title: 容器化 Ruby on Rails 应用程序
linkTitle: 容器化您的应用
weight: 10
keywords: ruby, flask, containerize, initialize
description: 了解如何容器化 Ruby on Rails 应用程序。
aliases:
  - /language/ruby/build-images/
  - /language/ruby/run-containers/
  - /language/ruby/containerize/
  - /guides/language/ruby/containerize/
---

## 先决条件

- 您已安装最新版本的 [Docker Desktop](/get-started/get-docker.md)。
- 您拥有 [Git 客户端](https://git-scm.com/downloads)。本节中的示例展示了 Git CLI，但您可以使用任何客户端。

## 概述

本节将引导您完成容器化和运行 [Ruby on Rails](https://rubyonrails.org/) 应用程序的过程。

从 Rails 7.1 开始，[开箱即用支持 Docker](https://guides.rubyonrails.org/7_1_release_notes.html#generate-dockerfiles-for-new-rails-applications)。这意味着当您创建新的 Rails 应用程序时，将为您生成 `Dockerfile`、`.dockerignore` 和 `bin/docker-entrypoint` 文件。

如果您有一个现有的 Rails 应用程序，则需要手动创建 Docker 资产。不幸的是，`docker init` 命令尚不支持 Rails。这意味着如果您使用 Rails，则需要从下面的示例中手动复制 Dockerfile 和其他相关配置。

## 1. 初始化 Docker 资产

Rails 7.1 及更新版本会开箱即用地生成多阶段 Dockerfile。以下是此类文件的两个版本：一个使用 Docker 硬化镜像 (DHIs)，另一个使用 Docker 官方镜像 (DOIs)。尽管 Dockerfile 是自动生成的，但了解其目的和功能非常重要。强烈建议查看以下示例。

[Docker 硬化镜像 (DHIs)](https://docs.docker.com/dhi/) 是由 Docker 维护的最小、安全且可用于生产的容器基础镜像和应用程序镜像。只要可能，都建议使用 DHIs 以获得更好的安全性。它们旨在减少漏洞并简化合规性，对所有人免费提供，无需订阅，没有使用限制，也没有供应商锁定。

多阶段 Dockerfile 通过分离构建和运行时依赖项，有助于创建更小、更高效的镜像，确保最终镜像中仅包含必要的组件。请在[多阶段构建指南](/get-started/docker-concepts/building-images/multi-stage-builds/)中阅读更多内容。

{{< tabs >}}
{{< tab name="使用 DHIs" >}}

您必须先向 `dhi.io` 进行身份验证，然后才能拉取 Docker 硬化镜像。运行 `docker login dhi.io` 进行身份验证。

```dockerfile {title=Dockerfile}
# syntax=docker/dockerfile:1
# check=error=true

# 此 Dockerfile 专为生产环境设计，而非开发环境。
# docker build -t app .
# docker run -d -p 80:80 -e RAILS_MASTER_KEY=<config/master.key 中的值> --name app app

# 有关容器化开发环境，请参阅开发容器：https://guides.rubyonrails.org/getting_started_with_devcontainer.html

# 确保 RUBY_VERSION 与 .ruby-version 中的 Ruby 版本匹配
ARG RUBY_VERSION=3.4.8
FROM dhi.io/ruby:$RUBY_VERSION-dev AS base

# Rails 应用程序位于此处
WORKDIR /rails

# 安装基础软件包
# 如果使用 SQLite，请将 libpq-dev 替换为 sqlite3；如果使用 MySQL，则替换为 libmysqlclient-dev
RUN apt-get update -qq && \
    apt-get install --no-install-recommends -y curl libjemalloc2 libvips libpq-dev && \
    rm -rf /var/lib/apt/lists /var/cache/apt/archives

# 设置生产环境
ENV RAILS_ENV="production" \
    BUNDLE_DEPLOYMENT="1" \
    BUNDLE_PATH="/usr/local/bundle" \
    BUNDLE_WITHOUT="development"

# 用于减小最终镜像大小的临时构建阶段
FROM base AS build

# 安装构建 gems 所需的软件包
RUN apt-get update -qq && \
    apt-get install --no-install-recommends -y build-essential curl git pkg-config libyaml-dev && \
    rm -rf /var/lib/apt/lists /var/cache/apt/archives

# 安装 JavaScript 依赖项和 Node.js 以编译资产
#
# 如果您使用 NodeJS 需要编译资产，请取消注释以下几行
#
# ARG NODE_VERSION=18.12.0
# ARG YARN_VERSION=1.22.19
# ENV PATH=/usr/local/node/bin:$PATH
# RUN curl -sL https://github.com/nodenv/node-build/archive/master.tar.gz | tar xz -C /tmp/ && \
#     /tmp/node-build-master/bin/node-build "${NODE_VERSION}" /usr/local/node && \
#     npm install -g yarn@$YARN_VERSION && \
#     npm install -g mjml && \
#     rm -rf /tmp/node-build-master

# 安装应用程序 gems
COPY Gemfile Gemfile.lock ./
RUN bundle install && \
    rm -rf ~/.bundle/ "${BUNDLE_PATH}"/ruby/*/cache "${BUNDLE_PATH}"/ruby/*/bundler/gems/*/.git && \
    bundle exec bootsnap precompile --gemfile

# 安装 node 模块
#
# 如果您使用 NodeJS 需要编译资产，请取消注释以下几行
#
# COPY package.json yarn.lock ./
# RUN --mount=type=cache,id=yarn,target=/rails/.cache/yarn YARN_CACHE_FOLDER=/rails/.cache/yarn \
#     yarn install --frozen-lockfile

# 复制应用程序代码
COPY . .

# 预编译 bootsnap 代码以加快启动时间
RUN bundle exec bootsnap precompile app/ lib/

# 预编译生产环境资产，无需 RAILS_MASTER_KEY 密钥
RUN SECRET_KEY_BASE_DUMMY=1 ./bin/rails assets:precompile

# 应用程序镜像的最终阶段
FROM base

# 复制构建的工件：gems、应用程序
COPY --from=build "${BUNDLE_PATH}" "${BUNDLE_PATH}"
COPY --from=build /rails /rails

# 作为非 root 用户运行并仅拥有运行时文件的所有权，以确保安全
RUN groupadd --system --gid 1000 rails && \
    useradd rails --uid 1000 --gid 1000 --create-home --shell /bin/bash && \
    chown -R rails:rails db log storage tmp
USER 1000:1000

# 入口点用于准备数据库。
ENTRYPOINT ["/rails/bin/docker-entrypoint"]

# 默认通过 Thruster 启动服务器，这可以在运行时被覆盖
EXPOSE 80
CMD ["./bin/thrust", "./bin/rails", "server"]
```

{{< /tab >}}
{{< tab name="使用 DOIs" >}}

```dockerfile {title=Dockerfile}
# syntax=docker/dockerfile:1
# check=error=true

# 此 Dockerfile 专为生产环境设计，而非开发环境。
# docker build -t app .
# docker run -d -p 80:80 -e RAILS_MASTER_KEY=<config/master.key 中的值> --name app app

# 有关容器化开发环境，请参阅开发容器：https://guides.rubyonrails.org/getting_started_with_devcontainer.html

# 确保 RUBY_VERSION 与 .ruby-version 中的 Ruby 版本匹配
ARG RUBY_VERSION=3.4.8
FROM docker.io/library/ruby:$RUBY_VERSION-slim AS base

# Rails 应用程序位于此处
WORKDIR /rails

# 安装基础软件包
# 如果使用 SQLite，请将 libpq-dev 替换为 sqlite3；如果使用 MySQL，则替换为 libmysqlclient-dev
RUN apt-get update -qq && \
    apt-get install --no-install-recommends -y curl libjemalloc2 libvips libpq-dev && \
    rm -rf /var/lib/apt/lists /var/cache/apt/archives

# 设置生产环境
ENV RAILS_ENV="production" \
    BUNDLE_DEPLOYMENT="1" \
    BUNDLE_PATH="/usr/local/bundle" \
    BUNDLE_WITHOUT="development"

# 用于减小最终镜像大小的临时构建阶段
FROM base AS build

# 安装构建 gems 所需的软件包
RUN apt-get update -qq && \
    apt-get install --no-install-recommends -y build-essential curl git pkg-config libyaml-dev && \
    rm -rf /var/lib/apt/lists /var/cache/apt/archives

# 安装 JavaScript 依赖项和 Node.js 以编译资产
#
# 如果您使用 NodeJS 需要编译资产，请取消注释以下几行
#
# ARG NODE_VERSION=18.12.0
# ARG YARN_VERSION=1.22.19
# ENV PATH=/usr/local/node/bin:$PATH
# RUN curl -sL https://github.com/nodenv/node-build/archive/master.tar.gz | tar xz -C /tmp/ && \
#     /tmp/node-build-master/bin/node-build "${NODE_VERSION}" /usr/local/node && \
#     npm install -g yarn@$YARN_VERSION && \
#     npm install -g mjml && \
#     rm -rf /tmp/node-build-master

# 安装应用程序 gems
COPY Gemfile Gemfile.lock ./
RUN bundle install && \
    rm -rf ~/.bundle/ "${BUNDLE_PATH}"/ruby/*/cache "${BUNDLE_PATH}"/ruby/*/bundler/gems/*/.git && \
    bundle exec bootsnap precompile --gemfile

# 安装 node 模块
#
# 如果您使用 NodeJS 需要编译资产，请取消注释以下几行
#
# COPY package.json yarn.lock ./
# RUN --mount=type=cache,id=yarn,target=/rails/.cache/yarn YARN_CACHE_FOLDER=/rails/.cache/yarn \
#     yarn install --frozen-lockfile

# 复制应用程序代码
COPY . .

# 预编译 bootsnap 代码以加快启动时间
RUN bundle exec bootsnap precompile app/ lib/

# 预编译生产环境资产，无需 RAILS_MASTER_KEY 密钥
RUN SECRET_KEY_BASE_DUMMY=1 ./bin/rails assets:precompile

# 应用程序镜像的最终阶段
FROM base

# 复制构建的工件：gems、应用程序
COPY --from=build "${BUNDLE_PATH}" "${BUNDLE_PATH}"
COPY --from=build /rails /rails

# 作为非 root 用户运行并仅拥有运行时文件的所有权，以确保安全
RUN groupadd --system --gid 1000 rails && \
    useradd rails --uid 1000 --gid 1000 --create-home --shell /bin/bash && \
    chown -R rails:rails db log storage tmp
USER 1000:1000

# 入口点用于准备数据库。
ENTRYPOINT ["/rails/bin/docker-entrypoint"]

# 默认通过 Thruster 启动服务器，这可以在运行时被覆盖
EXPOSE 80
CMD ["./bin/thrust", "./bin/rails", "server"]
```

{{< /tab >}}
{{< /tabs >}}

上面的 Dockerfile 假设您将 Thruster 与 Puma 一起用作应用程序服务器。如果您使用任何其他服务器，可以用以下内容替换最后三行：

```dockerfile
# 启动应用程序服务器
EXPOSE 3000
CMD ["./bin/rails", "server"]
```

此 Dockerfile 使用 `./bin/docker-entrypoint` 处的脚本作为容器的入口点。该脚本用于准备数据库并运行应用程序服务器。以下是此类脚本的示例。

```bash {title=docker-entrypoint}
#!/bin/bash -e

# 启用 jemalloc 以减少内存使用和延迟。
if [ -z "${LD_PRELOAD+x}" ]; then
    LD_PRELOAD=$(find /usr/lib -name libjemalloc.so.2 -print -quit)
    export LD_PRELOAD
fi

# 如果运行 rails 服务器，则创建或迁移现有数据库
if [ "${@: -2:1}" == "./bin/rails" ] && [ "${@: -1:1}" == "server" ]; then
  ./bin/rails db:prepare
fi

exec "${@}"
```

除了上面的两个文件，您还需要一个 `.dockerignore` 文件。此文件用于从构建上下文中排除文件和目录。以下是 `.dockerignore` 文件的示例。

```text {collapse=true,title=".dockerignore"}
# 有关忽略文件的更多信息，请参阅 https://docs.docker.com/engine/reference/builder/#dockerignore-file。

# 忽略 git 目录。
/.git/
/.gitignore

# 忽略 bundler 配置。
/.bundle

# 忽略所有环境文件。
/.env*

# 忽略所有默认密钥文件。
/config/master.key
/config/credentials/*.key

# 忽略所有日志文件和临时文件。
/log/*
/tmp/*
!/log/.keep
!/tmp/.keep

# 忽略 pid 文件，但保留目录。
/tmp/pids/*
!/tmp/pids/.keep

# 忽略存储（开发中上传的文件和任何 SQLite 数据库）。
/storage/*
!/storage/.keep
/tmp/storage/*
!/tmp/storage/.keep

# 忽略资产。
/node_modules/
/app/assets/builds/*
!/app/assets/builds/.keep
/public/assets

# 忽略 CI 服务文件。
/.github

# 忽略开发文件
/.devcontainer

# 忽略 Docker 相关文件
/.dockerignore
/Dockerfile*
```

您可能需要的最后一个可选文件是 `compose.yaml` 文件，Docker Compose 使用它来定义构成应用程序的服务。由于使用 SQLite 作为数据库，因此无需为数据库定义单独的服务。唯一需要的服务是 Rails 应用程序本身。

```yaml {title=compose.yaml}
services:
  web:
    build: .
    environment:
      - RAILS_MASTER_KEY
    ports:
      - "3000:80"
```

您现在应该在您的应用程序文件夹中拥有以下文件：

- `.dockerignore`
- `compose.yaml`
- `Dockerfile`
- `bin/docker-entrypoint`

要了解有关这些文件的更多信息，请参阅以下内容：

- [Dockerfile](/reference/dockerfile)
- [.dockerignore](/reference/dockerfile#dockerignore-file)
- [compose.yaml](/reference/compose-file/_index.md)
- [docker-entrypoint](/reference/dockerfile/#entrypoint)

## 2. 运行应用程序

要在应用程序的目录中运行应用程序，请在终端中运行以下命令。

```console
$ RAILS_MASTER_KEY=<master_key_value> docker compose up --build
```

打开浏览器并访问 [http://localhost:3000](http://localhost:3000) 查看应用程序。您应该会看到一个简单的 Ruby on Rails 应用程序。

在终端中，按 `ctrl`+`c` 停止应用程序。

## 3. 在后台运行应用程序

您可以通过添加 `-d` 选项在终端中分离运行应用程序。在 `docker-ruby-on-rails` 目录中，在终端中运行以下命令。

```console
$ docker compose up --build -d
```

打开浏览器并访问 [http://localhost:3000](http://localhost:3000) 查看应用程序。

您应该会看到一个简单的 Ruby on Rails 应用程序。

在终端中，运行以下命令停止应用程序。

```console
$ docker compose down
```

有关 Compose 命令的更多信息，请参阅 [Compose CLI 参考](/reference/cli/docker/compose/_index.md)。

## 总结

在本节中，您学习了如何使用 Docker 容器化和运行您的 Ruby 应用程序。

相关信息：

- [Docker Compose 概述](/manuals/compose/_index.md)

## 下一步

在下一节中，您将了解如何使用 GitHub Actions 设置 CI/CD 管道。