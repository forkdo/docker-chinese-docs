---
title: 容器化 Java 应用
linkTitle: 容器化你的应用
weight: 10
keywords: java, containerize, initialize, maven, build
description: 学习如何容器化 Java 应用。
aliases:
  - /language/java/build-images/
  - /language/java/run-containers/
  - /language/java/containerize/
  - /guides/language/java/containerize/
---

## 前置条件

- 你已安装最新版本的 [Docker Desktop](/get-started/get-docker.md)。
  Docker 定期添加新功能，本指南中的某些部分可能仅在 Docker Desktop 最新版本中适用。

* 你已安装 [Git 客户端](https://git-scm.com/downloads)。本节示例使用基于命令行的 Git 客户端，但你可以使用任何客户端。

## 概述

本节将引导你完成容器化并运行 Java 应用的步骤。

## 获取示例应用

将你要使用的示例应用克隆到本地开发机器。在终端中运行以下命令克隆仓库。

```console
$ git clone https://github.com/spring-projects/spring-petclinic.git
```

示例应用是一个基于 Maven 构建的 Spring Boot 应用。更多详情，请参阅仓库中的 `readme.md`。

## 初始化 Docker 资产

现在你有了应用，可以创建必要的 Docker 资产来容器化你的应用。你可以使用 Docker Desktop 内置的 Docker Init 功能来简化流程，也可以手动创建这些资产。

{{< tabs >}}
{{< tab name="使用 Docker Init" >}}

在 `spring-petclinic` 目录中，运行 `docker init` 命令。`docker init` 提供一些默认配置，但你需要回答几个关于你的应用的问题。参考以下示例回答 `docker init` 的提示，并对你的提示使用相同的答案。

示例应用已包含 Docker 资产。系统会提示你覆盖现有的 Docker 资产。为继续本指南，选择 `y` 覆盖它们。

```console
$ docker init
Welcome to the Docker Init CLI!

This utility will walk you through creating the following files with sensible defaults for your project:
  - .dockerignore
  - Dockerfile
  - compose.yaml
  - README.Docker.md

Let's get started!

WARNING: The following Docker files already exist in this directory:
  - docker-compose.yml
? Do you want to overwrite them? Yes
? What application platform does your project use? Java
? What's the relative directory (with a leading .) for your app? ./src
? What version of Java do you want to use? 21
? What port does your server listen on? 8080
```

在前面的示例中，请注意 `WARNING`。`docker-compose.yaml` 已存在，因此 `docker init` 会覆盖该文件，而不是创建新的 `compose.yaml` 文件。这可以防止目录中有多个 Compose 文件。两个名称都受支持，但 Compose 更倾向于使用标准的 `compose.yaml`。

{{< /tab >}}
{{< tab name="手动创建资产" >}}

如果你未安装 Docker Desktop 或更喜欢手动创建资产，可以在项目目录中创建以下文件。

创建一个名为 `Dockerfile` 的文件，内容如下。

```dockerfile {collapse=true,title=Dockerfile}
# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

# Want to help us make this template better? Share your feedback here: https://forms.gle/ybq9Krt8jtBL3iCk7

################################################################################

# Create a stage for resolving and downloading dependencies.
FROM eclipse-temurin:21-jdk-jammy as deps

WORKDIR /build

# Copy the mvnw wrapper with executable permissions.
COPY --chmod=0755 mvnw mvnw
COPY .mvn/ .mvn/

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.m2 so that subsequent builds don't have to
# re-download packages.
RUN --mount=type=bind,source=pom.xml,target=pom.xml \
    --mount=type=cache,target=/root/.m2 ./mvnw dependency:go-offline -DskipTests

################################################################################

# Create a stage for building the application based on the stage with downloaded dependencies.
# This Dockerfile is optimized for Java applications that output an uber jar, which includes
# all the dependencies needed to run your app inside a JVM. If your app doesn't output an uber
# jar and instead relies on an application server like Apache Tomcat, you'll need to update this
# stage with the correct filename of your package and update the base image of the "final" stage
# use the relevant app server, e.g., using tomcat (https://hub.docker.com/_/tomcat/) as a base image.
FROM deps as package

WORKDIR /build

COPY ./src src/
RUN --mount=type=bind,source=pom.xml,target=pom.xml \
    --mount=type=cache,target=/root/.m2 \
    ./mvnw package -DskipTests && \
    mv target/$(./mvnw help:evaluate -Dexpression=project.artifactId -q -DforceStdout)-$(./mvnw help:evaluate -Dexpression=project.version -q -DforceStdout).jar target/app.jar

################################################################################

# Create a stage for extracting the application into separate layers.
# Take advantage of Spring Boot's layer tools and Docker's caching by extracting
# the packaged application into separate layers that can be copied into the final stage.
# See Spring's docs for reference:
# https://docs.spring.io/spring-boot/docs/current/reference/html/container-images.html
FROM package as extract

WORKDIR /build

RUN java -Djarmode=layertools -jar target/app.jar extract --destination target/extracted

################################################################################

# Create a new stage for running the application that contains the minimal
# runtime dependencies for the application. This often uses a different base
# image from the install or build stage where the necessary files are copied
# from the install stage.
#
# The example below uses eclipse-turmin's JRE image as the foundation for running the app.
# By specifying the "17-jre-jammy" tag, it will also use whatever happens to be the
# most recent version of that tag when you build your Dockerfile.
# If reproducibility is important, consider using a specific digest SHA, like
# eclipse-temurin@sha256:99cede493dfd88720b610eb8077c8688d3cca50003d76d1d539b0efc8cca72b4.
FROM eclipse-temurin:21-jre-jammy AS final

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser
USER appuser

# Copy the executable from the "package" stage.
COPY --from=extract build/target/extracted/dependencies/ ./
COPY --from=extract build/target/extracted/spring-boot-loader/ ./
COPY --from=extract build/target/extracted/snapshot-dependencies/ ./
COPY --from=extract build/target/extracted/application/ ./

EXPOSE 8080

ENTRYPOINT [ "java", "org.springframework.boot.loader.launch.JarLauncher" ]
```

示例中已包含一个 Compose 文件。为继续本指南，请覆盖此文件。将 `docker-compose.yaml` 更新为以下内容。

```yaml {collapse=true,title=docker-compose.yaml}
# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Docker Compose reference guide at
# https://docs.docker.com/go/compose-spec-reference/

# Here the instructions define your application as a service called "server".
# This service is built from the Dockerfile in the current directory.
# You can add other services your application可能依赖的服务，例如数据库或缓存。示例请参阅 Awesome Compose 仓库：
# https://github.com/docker/awesome-compose
services:
  server:
    build:
      context: .
    ports:
      - 8080:8080
# The commented out section below is an example of how to define a PostgreSQL
# database that your application can use. `depends_on` tells Docker Compose to
# start the database before your application. The `db-data` volume persists the
# database data between container restarts. The `db-password` secret is used
# to set the database password. You must创建 `db/password.txt` 并在其中添加
# 你选择的密码，然后运行 `docker compose up`。
#     depends_on:
#       db:
#         condition: service_healthy
#   db:
#     image: postgres:18
#     restart: always
#     user: postgres
#     secrets:
#       - db-password
#     volumes:
#       - db-data:/var/lib/postgresql
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

创建一个名为 `.dockerignore` 的文件，内容如下。

```text {collapse=true,title=".dockerignore"}
# Include any files or directories that you don't want to be copied to your
# container here (e.g., local build artifacts, temporary files, etc.).
#
# For more help, visit the .dockerignore file reference guide at
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
**/target
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

{{< /tab >}}
{{< /tabs >}}

现在你应该在 `spring-petclinic` 目录中有以下三个文件。

- [Dockerfile](/reference/dockerfile/)
- [.dockerignore](/reference/dockerfile/#dockerignore-file)
- [docker-compose.yaml](/reference/compose-file/_index.md)

## 运行应用

在 `spring-petclinic` 目录中，在终端中运行以下命令。

```console
$ docker compose up --build
```

首次构建和运行应用时，Docker 会下载依赖并构建应用。根据你的网络连接，这可能需要几分钟。

打开浏览器，在 [http://localhost:8080](http://localhost:8080) 查看应用。你应该会看到一个简单的宠物诊所应用。

在终端中，按 `ctrl`+`c` 停止应用。

### 在后台运行应用

你可以通过添加 `-d` 选项，在终端外以分离模式运行应用。在 `spring-petclinic` 目录中，在终端中运行以下命令。

```console
$ docker compose up --build -d
```

打开浏览器，在 [http://localhost:8080](http://localhost:8080) 查看应用。你应该会看到一个简单的宠物诊所应用。

在终端中，运行以下命令停止应用。

```console
$ docker compose down
```

有关 Compose 命令的更多信息，请参阅 [Compose CLI 参考](/reference/cli/docker/compose/_index.md)。

## 总结

在本节中，你学习了如何使用 Docker 容器化并运行 Java 应用。

相关信息：

- [docker init 参考](/reference/cli/docker/init/)

## 下一步

在下一节中，你将学习如何使用 Docker 容器开发你的应用。