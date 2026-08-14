# Ruby on Rails 语言专项指南


Ruby 语言专项指南将教你如何使用 Docker 容器化一个 Ruby on Rails 应用。在本指南中，你将学习如何：

- 容器化并运行 Ruby on Rails 应用
- 使用容器搭建本地开发环境来开发 Ruby on Rails 应用

首先从容器化一个现有的 Ruby on Rails 应用开始。

## Containerize a Ruby on Rails application（容器化 Ruby on Rails 应用）

### 前提条件

- 你已安装最新版本的 [Docker Desktop](/get-started/get-docker.md)。
- 你拥有一个 [Git 客户端](https://git-scm.com/downloads)。本节示例展示的是 Git CLI，但你可以使用任意客户端。

### 概述

本节将带你完成 [Ruby on Rails](https://rubyonrails.org/) 应用的容器化和运行。

从 Rails 7.1 开始，[Docker 已获得开箱即用的支持](https://guides.rubyonrails.org/7_1_release_notes.html#generate-dockerfiles-for-new-rails-applications)。这意味着在创建新的 Rails 应用时，系统会为你自动生成 `Dockerfile`、`.dockerignore` 以及 `bin/docker-entrypoint` 文件。

如果你已有一个现成的 Rails 应用，则需要参照下面的示例手动创建这些 Docker 资产文件。

### 1. 创建 Docker 资产文件

> [!TIP]
>
> Docker 的 AI 助手 [Gordon](/ai/gordon/) 可以为你的项目生成 Docker 资产文件。你可以让 Gordon 创建适配你应用的 Dockerfile、Compose 文件和 `.dockerignore`。

Rails 7.1 及更新版本会开箱即用地生成多阶段 Dockerfile。下面是该文件的两个版本：一个使用 Docker Hardened Images (DHIs)，另一个使用 Docker 官方镜像 (DOIs)。虽然 Dockerfile 是自动生成的，但理解其用途和工作方式很重要。强烈建议你仔细阅读以下示例。

[Docker Hardened Images (DHIs)](https://docs.docker.com/dhi/) 是由 Docker 维护的精简、安全、可用于生产的容器基础镜像和应用镜像。在可能的情况下推荐使用 DHIs 以获得更好的安全性。它们旨在减少漏洞并简化合规工作，对所有人免费开放，无需订阅、无使用限制、无厂商锁定。

多阶段 Dockerfile 通过分离构建期依赖和运行期依赖，帮助创建更小、更高效的镜像，确保最终镜像中只包含必要的组件。更多内容请参阅[多阶段构建指南](/get-started/docker-concepts/building-images/multi-stage-builds/)。

**Using DHIs**



在拉取 Docker Hardened Images 之前，你必须先向 `dhi.io` 完成认证。运行 `docker login dhi.io` 进行认证。

```dockerfile {title=Dockerfile}
# syntax=docker/dockerfile:1
# check=error=true

# This Dockerfile is designed for production, not development.
# docker build -t app .
# docker run -d -p 80:80 -e RAILS_MASTER_KEY=<value from config/master.key> --name app app

# For a containerized dev environment, see Dev Containers: https://guides.rubyonrails.org/getting_started_with_devcontainer.html

# Make sure RUBY_VERSION matches the Ruby version in .ruby-version
ARG RUBY_VERSION=3.4.8
FROM dhi.io/ruby:$RUBY_VERSION-dev AS base

# Rails app lives here
WORKDIR /rails

# Install base packages
# Replace libpq-dev with sqlite3 if using SQLite, or libmysqlclient-dev if using MySQL
RUN apt-get update -qq && \
    apt-get install --no-install-recommends -y curl libjemalloc2 libvips libpq-dev && \
    rm -rf /var/lib/apt/lists /var/cache/apt/archives

# Set production environment
ENV RAILS_ENV="production" \
    BUNDLE_DEPLOYMENT="1" \
    BUNDLE_PATH="/usr/local/bundle" \
    BUNDLE_WITHOUT="development"

# Throw-away build stage to reduce size of final image
FROM base AS build

# Install packages needed to build gems
RUN apt-get update -qq && \
    apt-get install --no-install-recommends -y build-essential curl git pkg-config libyaml-dev && \
    rm -rf /var/lib/apt/lists /var/cache/apt/archives

# Install JavaScript dependencies and Node.js for asset compilation
#
# Uncomment the following lines if you are using NodeJS need to compile assets
#
# ARG NODE_VERSION=18.12.0
# ARG YARN_VERSION=1.22.19
# ENV PATH=/usr/local/node/bin:$PATH
# RUN curl -sL https://github.com/nodenv/node-build/archive/master.tar.gz | tar xz -C /tmp/ && \
#     /tmp/node-build-master/bin/node-build "${NODE_VERSION}" /usr/local/node && \
#     npm install -g yarn@$YARN_VERSION && \
#     npm install -g mjml && \
#     rm -rf /tmp/node-build-master

# Install application gems
COPY Gemfile Gemfile.lock ./
RUN bundle install && \
    rm -rf ~/.bundle/ "${BUNDLE_PATH}"/ruby/*/cache "${BUNDLE_PATH}"/ruby/*/bundler/gems/*/.git && \
    bundle exec bootsnap precompile --gemfile

# Install node modules
#
# Uncomment the following lines if you are using NodeJS need to compile assets
#
# COPY package.json yarn.lock ./
# RUN --mount=type=cache,id=yarn,target=/rails/.cache/yarn YARN_CACHE_FOLDER=/rails/.cache/yarn \
#     yarn install --frozen-lockfile

# Copy application code
COPY . .

# Precompile bootsnap code for faster boot times
RUN bundle exec bootsnap precompile app/ lib/

# Precompiling assets for production without requiring secret RAILS_MASTER_KEY
RUN SECRET_KEY_BASE_DUMMY=1 ./bin/rails assets:precompile

# Final stage for app image
FROM base

# Copy built artifacts: gems, application
COPY --from=build "${BUNDLE_PATH}" "${BUNDLE_PATH}"
COPY --from=build /rails /rails

# Run and own only the runtime files as a non-root user for security
RUN groupadd --system --gid 1000 rails && \
    useradd rails --uid 1000 --gid 1000 --create-home --shell /bin/bash && \
    chown -R rails:rails db log storage tmp
USER 1000:1000

# Entrypoint prepares the database.
ENTRYPOINT ["/rails/bin/docker-entrypoint"]

# Start server via Thruster by default, this can be overwritten at runtime
EXPOSE 80
CMD ["./bin/thrust", "./bin/rails", "server"]
```

**Using DOIs**



```dockerfile {title=Dockerfile}
# syntax=docker/dockerfile:1
# check=error=true

# This Dockerfile is designed for production, not development.
# docker build -t app .
# docker run -d -p 80:80 -e RAILS_MASTER_KEY=<value from config/master.key> --name app app

# For a containerized dev environment, see Dev Containers: https://guides.rubyonrails.org/getting_started_with_devcontainer.html

# Make sure RUBY_VERSION matches the Ruby version in .ruby-version
ARG RUBY_VERSION=3.4.8
FROM docker.io/library/ruby:$RUBY_VERSION-slim AS base

# Rails app lives here
WORKDIR /rails

# Install base packages
# Replace libpq-dev with sqlite3 if using SQLite, or libmysqlclient-dev if using MySQL
RUN apt-get update -qq && \
    apt-get install --no-install-recommends -y curl libjemalloc2 libvips libpq-dev && \
    rm -rf /var/lib/apt/lists /var/cache/apt/archives

# Set production environment
ENV RAILS_ENV="production" \
    BUNDLE_DEPLOYMENT="1" \
    BUNDLE_PATH="/usr/local/bundle" \
    BUNDLE_WITHOUT="development"

# Throw-away build stage to reduce size of final image
FROM base AS build

# Install packages needed to build gems
RUN apt-get update -qq && \
    apt-get install --no-install-recommends -y build-essential curl git pkg-config libyaml-dev && \
    rm -rf /var/lib/apt/lists /var/cache/apt/archives

# Install JavaScript dependencies and Node.js for asset compilation
#
# Uncomment the following lines if you are using NodeJS need to compile assets
#
# ARG NODE_VERSION=18.12.0
# ARG YARN_VERSION=1.22.19
# ENV PATH=/usr/local/node/bin:$PATH
# RUN curl -sL https://github.com/nodenv/node-build/archive/master.tar.gz | tar xz -C /tmp/ && \
#     /tmp/node-build-master/bin/node-build "${NODE_VERSION}" /usr/local/node && \
#     npm install -g yarn@$YARN_VERSION && \
#     npm install -g mjml && \
#     rm -rf /tmp/node-build-master

# Install application gems
COPY Gemfile Gemfile.lock ./
RUN bundle install && \
    rm -rf ~/.bundle/ "${BUNDLE_PATH}"/ruby/*/cache "${BUNDLE_PATH}"/ruby/*/bundler/gems/*/.git && \
    bundle exec bootsnap precompile --gemfile

# Install node modules
#
# Uncomment the following lines if you are using NodeJS need to compile assets
#
# COPY package.json yarn.lock ./
# RUN --mount=type=cache,id=yarn,target=/rails/.cache/yarn YARN_CACHE_FOLDER=/rails/.cache/yarn \
#     yarn install --frozen-lockfile

# Copy application code
COPY . .

# Precompile bootsnap code for faster boot times
RUN bundle exec bootsnap precompile app/ lib/

# Precompiling assets for production without requiring secret RAILS_MASTER_KEY
RUN SECRET_KEY_BASE_DUMMY=1 ./bin/rails assets:precompile

# Final stage for app image
FROM base

# Copy built artifacts: gems, application
COPY --from=build "${BUNDLE_PATH}" "${BUNDLE_PATH}"
COPY --from=build /rails /rails

# Run and own only the runtime files as a non-root user for security
RUN groupadd --system --gid 1000 rails && \
    useradd rails --uid 1000 --gid 1000 --create-home --shell /bin/bash && \
    chown -R rails:rails db log storage tmp
USER 1000:1000

# Entrypoint prepares the database.
ENTRYPOINT ["/rails/bin/docker-entrypoint"]

# Start server via Thruster by default, this can be overwritten at runtime
EXPOSE 80
CMD ["./bin/thrust", "./bin/rails", "server"]
```



上面的 Dockerfile 假定你将 Thruster 与 Puma 一起作为应用服务器使用。如果你使用其他服务器，可以将最后三行替换为以下内容：

```dockerfile
# Start the application server
EXPOSE 3000
CMD ["./bin/rails", "server"]
```

该 Dockerfile 使用 `./bin/docker-entrypoint` 脚本作为容器的入口点。这个脚本负责准备数据库并启动应用服务器。下面是这样一个脚本的示例。

```bash {title=docker-entrypoint}
#!/bin/bash -e

# Enable jemalloc for reduced memory usage and latency.
if [ -z "${LD_PRELOAD+x}" ]; then
    LD_PRELOAD=$(find /usr/lib -name libjemalloc.so.2 -print -quit)
    export LD_PRELOAD
fi

# If running the rails server then create or migrate existing database
if [ "${@: -2:1}" == "./bin/rails" ] && [ "${@: -1:1}" == "server" ]; then
  ./bin/rails db:prepare
fi

exec "${@}"
```

除了上面两个文件之外，你还需要一个 `.dockerignore` 文件。该文件用于将某些文件和目录从构建上下文中排除。下面是一个 `.dockerignore` 文件的示例。

```text {collapse=true,title=".dockerignore"}
# See https://docs.docker.com/engine/reference/builder/#dockerignore-file for more about ignoring files.

# Ignore git directory.
/.git/
/.gitignore

# Ignore bundler config.
/.bundle

# Ignore all environment files.
/.env*

# Ignore all default key files.
/config/master.key
/config/credentials/*.key

# Ignore all logfiles and tempfiles.
/log/*
/tmp/*
!/log/.keep
!/tmp/.keep

# Ignore pidfiles, but keep the directory.
/tmp/pids/*
!/tmp/pids/.keep

# Ignore storage (uploaded files in development and any SQLite databases).
/storage/*
!/storage/.keep
/tmp/storage/*
!/tmp/storage/.keep

# Ignore assets.
/node_modules/
/app/assets/builds/*
!/app/assets/builds/.keep
/public/assets

# Ignore CI service files.
/.github

# Ignore development files
/.devcontainer

# Ignore Docker-related files
/.dockerignore
/Dockerfile*
```

最后一个可选文件是 `compose.yaml`，Docker Compose 用它来定义组成应用的各个服务。由于这里使用 SQLite 作为数据库，因此无需为数据库定义单独的服务。唯一需要的服务就是 Rails 应用本身。

```yaml {title=compose.yaml}
services:
  web:
    build: .
    environment:
      - RAILS_MASTER_KEY
    ports:
      - "3000:80"
```

现在你的应用目录中应该有以下文件：

- `.dockerignore`
- `compose.yaml`
- `Dockerfile`
- `bin/docker-entrypoint`

要了解更多关于这些文件的信息，请参阅：

- [Dockerfile](/reference/dockerfile)
- [.dockerignore](/reference/dockerfile#dockerignore-file)
- [compose.yaml](/reference/compose-file/_index.md)
- [docker-entrypoint](/reference/dockerfile/#entrypoint)

### 2. 运行应用

要运行应用，请在应用目录内的终端中执行以下命令。

```console
$ RAILS_MASTER_KEY=<master_key_value> docker compose up --build
```

打开浏览器访问 [http://localhost:3000](http://localhost:3000) 查看应用。你应该会看到一个简单的 Ruby on Rails 应用。

在终端中按 `ctrl`+`c` 停止应用。

### 3. 在后台运行应用

你可以通过添加 `-d` 选项让应用脱离终端在后台运行。在 `docker-ruby-on-rails` 目录中，于终端执行以下命令。

```console
$ docker compose up --build -d
```

打开浏览器访问 [http://localhost:3000](http://localhost:3000) 查看应用。

你应该会看到一个简单的 Ruby on Rails 应用。

在终端中执行以下命令停止应用。

```console
$ docker compose down
```

有关 Compose 命令的更多信息，请参阅 [Compose CLI 参考](/reference/cli/docker/compose/)。

## 使用容器进行 Ruby on Rails 开发

### 前提条件

完成[容器化 Ruby on Rails 应用](#containerize-a-ruby-on-rails-application)。

### 概述

在本节中，你将学习如何为容器化应用搭建开发环境。这包括：

- 添加本地数据库并持久化数据
- 配置 Compose，使其在你编辑并保存代码时自动更新正在运行的 Compose 服务

### 添加本地数据库并持久化数据

你可以使用容器来搭建本地服务，例如数据库。在本节中，你将更新 `compose.yaml` 文件以定义一个数据库服务和一个用于持久化数据的卷。

在克隆仓库的目录中，用 IDE 或文本编辑器打开 `compose.yaml` 文件。你需要将数据库密码文件作为环境变量添加到 server 服务中，并指定要使用的 secret 文件。

以下是更新后的 `compose.yaml` 文件。

```yaml {hl_lines="07-25"}
services:
  web:
    build: .
    command: bundle exec rails s -b '0.0.0.0'
    ports:
      - "3000:3000"
    depends_on:
      - db
    environment:
      - RAILS_ENV=test
    env_file: "webapp.env"
  db:
    image: postgres:18
    secrets:
      - db-password
    environment:
      - POSTGRES_PASSWORD_FILE=/run/secrets/db-password
    volumes:
      - postgres_data:/var/lib/postgresql

volumes:
  postgres_data:
secrets:
  db-password:
    file: db/password.txt
```

> [!NOTE]
>
> 要了解 Compose 文件中各指令的更多信息，请参阅 [Compose 文件参考](/reference/compose-file/)。

在使用 Compose 运行应用之前，请注意该 Compose 文件指定了一个 `password.txt` 文件来存放数据库密码。由于源仓库中并不包含此文件，你必须自行创建。

在克隆仓库的目录中，创建一个名为 `db` 的新目录，并在该目录中创建一个名为 `password.txt` 的文件用于存放数据库密码。使用你喜欢的 IDE 或文本编辑器，将以下内容添加到 `password.txt` 文件中。

```text
mysecretpassword
```

保存并关闭 `password.txt` 文件。此外，你还可以在 `webapp.env` 文件中修改连接数据库所用的密码。

现在，你的 `docker-ruby-on-rails` 目录中应该包含以下内容。

```text
.
├── Dockerfile
├── Gemfile
├── Gemfile.lock
├── README.md
├── Rakefile
├── app/
├── bin/
├── compose.yaml
├── config/
├── config.ru
├── db/
│   ├── development.sqlite3
│   ├── migrate
│   ├── password.txt
│   ├── schema.rb
│   └── seeds.rb
├── lib/
├── log/
├── public/
├── storage/
├── test/
├── tmp/
└── vendor
```

现在，运行以下 `docker compose up` 命令来启动你的应用。

```console
$ docker compose up --build
```

在 Ruby on Rails 中，`db:migrate` 是一个用于对数据库执行迁移的 Rake 任务。迁移是一种以一致且简便的方式随时间演进数据库 schema 结构的手段。

```console
$ docker exec -it docker-ruby-on-rails-web-1 rake db:migrate RAILS_ENV=test
```

你会看到类似下面的信息：

```console
== 20240710193146 CreateWhales: migrating =====================================
-- create_table(:whales)
   -> 0.0126s
== 20240710193146 CreateWhales: migrated (0.0127s) ============================
```

在浏览器中刷新 <http://localhost:3000>，然后添加鲸鱼记录。

在终端中按 `ctrl+c` 停止应用，再次运行 `docker compose up`，可以看到鲸鱼记录已被持久化保存。

### 自动更新服务

使用 Compose Watch，在你编辑并保存代码时自动更新正在运行的 Compose 服务。有关 Compose Watch 的更多细节，请参阅[使用 Compose Watch](/manuals/compose/how-tos/file-watch.md)。

用 IDE 或文本编辑器打开 `compose.yaml` 文件，然后添加 Compose Watch 相关指令。以下是更新后的 `compose.yaml` 文件。

```yaml {hl_lines="13-16"}
services:
  web:
    build: .
    command: bundle exec rails s -b '0.0.0.0'
    ports:
      - "3000:3000"
    depends_on:
      - db
    environment:
      - RAILS_ENV=test
    env_file: "webapp.env"

    develop:
      watch:
        - action: rebuild
          path: .
  db:
    image: postgres:18
    secrets:
      - db-password
    environment:
      - POSTGRES_PASSWORD_FILE=/run/secrets/db-password
    volumes:
      - postgres_data:/var/lib/postgresql

volumes:
  postgres_data:
secrets:
  db-password:
    file: db/password.txt
```

运行以下命令，使用 Compose Watch 运行你的应用。

```console
$ docker compose watch
```

现在，你在本机上对应用源文件所做的任何更改都会立即反映到正在运行的容器中。

用 IDE 或文本编辑器打开 `docker-ruby-on-rails/app/views/whales/index.html.erb`，为 `Whales` 字符串添加一个感叹号。

```diff
-    <h1>Whales</h1>
+    <h1>Whales!</h1>
```

保存对 `index.html.erb` 的修改，然后等待几秒钟让应用重新构建。再次访问应用，确认更新后的文本已出现。

在终端中按 `ctrl+c` 停止应用。

### 小结

在本节中，你了解了如何配置 Compose 文件以添加本地数据库并持久化数据。你还学习了如何使用 Compose Watch，在更新代码时自动重新构建并运行容器。

相关信息：

- [Compose 文件参考](/reference/compose-file/)
- [Compose 文件监视](/manuals/compose/how-tos/file-watch.md)
- [多阶段构建](/manuals/build/building/multi-stage.md)

