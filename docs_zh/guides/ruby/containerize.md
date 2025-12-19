---
title: 容器化 Ruby on Rails 应用
linkTitle: 容器化你的应用
weight: 10
keywords: ruby, flask, containerize, initialize
description: 学习如何容器化 Ruby on Rails 应用。
aliases:
  - /language/ruby/build-images/
  - /language/ruby/run-containers/
  - /language/ruby/containerize/
  - /guides/language/ruby/containerize/
---

## 前置条件

- 你已安装最新版本的 [Docker Desktop](/get-started/get-docker.md)。
- 你已安装 [Git 客户端](https://git-scm.com/downloads)。本节示例使用 Git CLI，但你可以使用任意客户端。

## 概述

本节将引导你完成容器化 [Ruby on Rails](https://rubyonrails.org/) 应用的全过程。

从 Rails 7.1 开始，[Docker 已原生支持](https://guides.rubyonrails.org/7_1_release_notes.html#generate-dockerfiles-for-new-rails-applications)。这意味着创建新 Rails 应用时，系统会自动生成 `Dockerfile`、`.dockerignore` 和 `bin/docker-entrypoint` 文件。

如果你已有 Rails 应用，则需要手动创建 Docker 资产。不幸的是，`docker init` 命令目前还不支持 Rails。这意味着如果你使用 Rails，需要从下方示例中手动复制 Dockerfile 和其他相关配置。

## 1. 初始化 Docker 资产

Rails 7.1 及以上版本默认生成多阶段 Dockerfile。以下是两种版本：一种使用 Docker Hardened Images (DHI)，另一种使用官方 Docker 镜像。

> [Docker Hardened Images (DHIs)](https://docs.docker.com/dhi/) 是由 Docker 维护的最小化、安全且可用于生产的容器基础镜像和应用镜像。

为提升安全性，建议在可能的情况下使用 DHI 镜像。它们旨在减少漏洞并简化合规性。

> 多阶段 Dockerfile 通过分离构建和运行时依赖，帮助创建更小、更高效的镜像，确保最终镜像仅包含必要组件。详见 [多阶段构建指南](/get-started/docker-concepts/building-images/multi-stage-builds/)。

虽然 Dockerfile 会自动生成，但理解其用途和功能很重要。强烈建议查看以下示例。

{{< tabs >}}
{{< tab name="使用 Docker Hardened Images" >}}

```dockerfile {title=Dockerfile}
# syntax=docker/dockerfile:1
# check=error=true

# 此 Dockerfile 专为生产环境设计，非开发环境。
# docker build -t app .
# docker run -d -p 80:80 -e RAILS_MASTER_KEY=<config/master.key 中的值> --name app app

# 如需容器化开发环境，请参阅 Dev Containers：https://guides.rubyonrails.org/getting_started_with_devcontainer.html

# 确保 RUBY_VERSION 与 .ruby-version 中的 Ruby 版本一致
ARG RUBY_VERSION=3.4.7
FROM <your-namespace>/dhi-ruby:$RUBY_VERSION-dev AS base

# Rails 应用位于此处
WORKDIR /rails

# 安装基础包
# 若使用 SQLite，请将 libpq-dev 替换为 sqlite3；若使用 MySQL，请替换为 libmysqlclient-dev
RUN apt-get update -qq && \
    apt-get install --no-install-recommends -y curl libjemalloc2 libvips libpq-dev && \
    rm -rf /var/lib/apt/lists /var/cache/apt/archives

# 设置生产环境
ENV RAILS_ENV="production" \
    BUNDLE_DEPLOYMENT="1" \
    BUNDLE_PATH="/usr/local/bundle" \
    BUNDLE_WITHOUT="development"

# 使用临时构建阶段以减少最终镜像大小
FROM base AS build

# 安装构建 gems 所需的包
RUN apt-get update -qq && \
    apt-get install --no-install-recommends -y build-essential curl git pkg-config libyaml-dev && \
    rm -rf /var/lib/apt/lists /var/cache/apt/archives

# 安装 JavaScript 依赖和 Node.js 以编译资源
#
# 若使用 NodeJS 编译资源，请取消注释以下行
#
# ARG NODE_VERSION=18.12.0
# ARG YARN_VERSION=1.22.19
# ENV PATH=/usr/local/node/bin:$PATH
# RUN curl -sL https://github.com/nodenv/node-build/archive/master.tar.gz | tar xz -C /tmp/ && \
#     /tmp/node-build-master/bin/node-build "${NODE_VERSION}" /usr/local/node && \
#     npm install -g yarn@$YARN_VERSION && \
#     npm install -g mjml && \
#     rm -rf /tmp/node-build-master

# 安装应用 gems
COPY Gemfile Gemfile.lock ./
RUN bundle install && \
    rm -rf ~/.bundle/ "${BUNDLE_PATH}"/ruby/*/cache "${BUNDLE_PATH}"/ruby/*/bundler/gems/*/.git && \
    bundle exec bootsnap precompile --gemfile

# 安装 node modules
#
# 若使用 NodeJS 编译资源，请取消注释以下行
#
# COPY package.json yarn.lock ./
# RUN --mount=type=cache,id=yarn,target=/rails/.cache/yarn YARN_CACHE_FOLDER=/rails/.cache/yarn \
#     yarn install --frozen-lockfile

# 复制应用代码
COPY . .

# 预编译 bootsnap 代码以提升启动速度
RUN bundle exec bootsnap precompile app/ lib/

# 无需密钥 RAILS_MASTER_KEY 即可预编译生产资源
RUN SECRET_KEY_BASE_DUMMY=1 ./bin/rails assets:precompile

# 应用镜像的最终阶段
FROM base

# 复制构建产物：gems 和应用
COPY --from=build "${BUNDLE_PATH}" "${BUNDLE_PATH}"
COPY --from=build /rails /rails

# 以非 root 用户运行并仅拥有运行时文件，提升安全性
RUN groupadd --system --gid 1000 rails && \
    useradd rails --uid 1000 --gid 1000 --create-home --shell /bin/bash && \
    chown -R rails:rails db log storage tmp
USER 1000:1000

# 入口脚本准备数据库
ENTRYPOINT ["/rails/bin/docker-entrypoint"]

# 默认通过 Thruster 启动服务器，运行时可覆盖
EXPOSE 80
CMD ["./bin/thrust", "./bin/rails", "server"]
```

{{< /tab >}}
{{< tab name="使用官方 Docker 镜像" >}}

```dockerfile {title=Dockerfile}
# syntax=docker/dockerfile:1
# check=error=true

# 此 Dockerfile 专为生产环境设计，非开发环境。
# docker build -t app .
# docker run -d -p 80:80 -e RAILS_MASTER_KEY=<config/master.key 中的值> --name app app

# 如需容器化开发环境，请参阅 Dev Containers：https://guides.rubyonrails.org/getting_started_with_devcontainer.html

# 确保 RUBY_VERSION 与 .ruby-version 中的 Ruby 版本一致
ARG RUBY_VERSION=3.4.7
FROM docker.io/library/ruby:$RUBY_VERSION-slim AS base

# Rails 应用位于此处
WORKDIR /rails

# 安装基础包
# 若使用 SQLite，请将 libpq-dev 替换为 sqlite3；若使用 MySQL，请替换为 libmysqlclient-dev
RUN apt-get update -qq && \
    apt-get install --no-install-recommends -y curl libjemalloc2 libvips libpq-dev && \
    rm -rf /var/lib/apt/lists /var/cache/apt/archives

# 设置生产环境
ENV RAILS_ENV="production" \
    BUNDLE_DEPLOYMENT="1" \
    BUNDLE_PATH="/usr/local/bundle" \
    BUNDLE_WITHOUT="development"

# 使用临时构建阶段以减少最终镜像大小
FROM base AS build

# 安装构建 gems 所需的包
RUN apt-get update -qq && \
    apt-get install --no-install-recommends -y build-essential curl git pkg-config libyaml-dev && \
    rm -rf /var/lib/apt/lists /var/cache/apt/archives

# 安装 JavaScript 依赖和 Node.js 以编译资源
#
# 若使用 NodeJS 编译资源，请取消注释以下行
#
# ARG NODE_VERSION=18.12.0
# ARG YARN_VERSION=1.22.19
# ENV PATH=/usr/local/node/bin:$PATH
# RUN curl -sL https://github.com/nodenv/node-build/archive/master.tar.gz | tar xz -C /tmp/ && \
#     /tmp/node-build-master/bin/node-build "${NODE_VERSION}" /usr/local/node && \
#     npm install -g yarn@$YARN_VERSION && \
#     npm install -g mjml && \
#     rm -rf /tmp/node-build-master

# 安装应用 gems
COPY Gemfile Gemfile.lock ./
RUN bundle install && \
    rm -rf ~/.bundle/ "${BUNDLE_PATH}"/ruby/*/cache "${BUNDLE_PATH}"/ruby/*/bundler/gems/*/.git && \
    bundle exec bootsnap precompile --gemfile

# 安装 node modules
#
# 若使用 NodeJS 编译资源，请取消注释以下行
#
# COPY package.json yarn.lock ./
# RUN --mount=type=cache,id=yarn,target=/rails/.cache/yarn YARN_CACHE_FOLDER=/rails/.cache/yarn \
#     yarn install --frozen-lockfile

# 复制应用代码
COPY . .

# 预编译 bootsnap 代码以提升启动速度
RUN bundle exec bootsnap precompile app/ lib/

# 无需密钥 RAILS_MASTER_KEY 即可预编译生产资源
RUN SECRET_KEY_BASE_DUMMY=1 ./bin/rails assets:precompile

# 应用镜像的最终阶段
FROM base

# 复制构建产物：gems 和应用
COPY --from=build "${BUNDLE_PATH}" "${BUNDLE_PATH}"
COPY --from=build /rails /rails

# 以非 root 用户运行并仅拥有运行时文件，提升安全性
RUN groupadd --system --gid 1000 rails && \
    useradd rails --uid 1000 --gid 1000 --create-home --shell /bin/bash && \
    chown -R rails:rails db log storage tmp
USER 1000:1000

# 入口脚本准备数据库
ENTRYPOINT ["/rails/bin/docker-entrypoint"]

# 默认通过 Thruster 启动服务器，运行时可覆盖
EXPOSE 80
CMD ["./bin/thrust", "./bin/rails", "server"]
```

{{< /tab >}}
{{< /tabs >}}

上述 Dockerfile 假设你将 Thruster 与 Puma 作为应用服务器一起使用。如果你使用其他服务器，可将最后三行替换为以下内容：

```dockerfile
# 启动应用服务器
EXPOSE 3000
CMD ["./bin/rails", "server"]
```

此 Dockerfile 使用 `./bin/docker-entrypoint` 脚本作为容器的入口点。该脚本准备数据库并运行应用服务器。以下是该脚本的示例。

```bash {title=docker-entrypoint}
#!/bin/bash -e

# 启用 jemalloc 以减少内存使用和延迟。
if [ -z "${LD_PRELOAD+x}" ]; then
    LD_PRELOAD=$(find /usr/lib -name libjemalloc.so.2 -print -quit)
    export LD_PRELOAD
fi

# 若运行 rails server，则创建或迁移现有数据库
if [ "${@: -2:1}" == "./bin/rails" ] && [ "${@: -1:1}" == "server" ]; then
  ./bin/rails db:prepare
fi

exec "${@}"
```

除了上述两个文件，你还需要 `.dockerignore` 文件。该文件用于排除构建上下文中的文件和目录。以下是 `.dockerignore` 文件的示例。

```text {collapse=true,title=".dockerignore"}
# 详见 https://docs.docker.com/engine/reference/builder/#dockerignore-file 了解忽略文件的更多信息。

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

# 忽略存储（开发中的上传文件和任何 SQLite 数据库）。
/storage/*
!/storage/.keep
/tmp/storage/*
!/tmp/storage/.keep

# 忽略资源。
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

最后一个可选文件是 `compose.yaml`，Docker Compose 使用它定义应用的各个服务。由于使用 SQLite 作为数据库，无需定义单独的数据库服务。唯一需要的服务是 Rails 应用本身。

```yaml {title=compose.yaml}
services:
  web:
    build: .
    environment:
      - RAILS_MASTER_KEY
    ports:
      - "3000:80"
```

现在你的应用文件夹中应包含以下文件：

- `.dockerignore`
- `compose.yaml`
- `Dockerfile`
- `bin/docker-entrypoint`

如需了解更多文件信息，请参阅：

- [Dockerfile](/reference/dockerfile)
- [.dockerignore](/reference/dockerfile#dockerignore-file)
- [compose.yaml](/reference/compose-file/_index.md)
- [docker-entrypoint](/reference/dockerfile/#entrypoint)

## 2. 运行应用

要在终端中运行应用，请在应用目录中执行以下命令。

```console
$ RAILS_MASTER_KEY=<master_key_value> docker compose up --build
```

在浏览器中访问 [http://localhost:3000](http://localhost:3000)。你应该能看到一个简单的 Ruby on Rails 应用。

在终端中按 `ctrl`+`c` 停止应用。

## 3. 在后台运行应用

添加 `-d` 选项可使应用在后台运行。在 `docker-ruby-on-rails` 目录中，于终端执行以下命令。

```console
$ docker compose up --build -d
```

在浏览器中访问 [http://localhost:3000](http://localhost:3000)。

你应该能看到一个简单的 Ruby on Rails 应用。

在终端中执行以下命令停止应用。

```console
$ docker compose down
```

更多 Compose 命令信息，请参阅 [Compose CLI 参考](/reference/cli/docker/compose/_index.md)。

## 小结

在本节中，你学会了如何使用 Docker 容器化并运行 Ruby 应用。

相关信息：

- [Docker Compose 概述](/manuals/compose/_index.md)

## 后续步骤

在下一节中，你将学习如何使用 GitHub Actions 设置 CI/CD 流水线。