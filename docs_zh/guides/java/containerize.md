---
title: 容器化 Java 应用程序
linkTitle: 容器化您的应用
weight: 10
description: 学习如何将 Java 应用程序容器化。
keywords: java, containerize, initialize, maven, build
aliases:
- /language/java/build-images/
- /language/java/run-containers/
- /language/java/containerize/
- /guides/language/java/containerize/
---
## 先决条件

- 您已安装最新版本的 [Docker Desktop](/get-started/get-docker.md)。
  Docker 会定期添加新功能，本指南的部分内容可能仅适用于最新版本的 Docker Desktop。

* 您已安装 [Git 客户端](https://git-scm.com/downloads)。本节示例使用基于命令行的 Git 客户端，但您可以使用任何客户端。

## 概述

本节将引导您完成容器化和运行 Java 应用程序的过程。

## 获取示例应用程序

将您要使用的示例应用程序克隆到本地开发机器。在终端中运行以下命令以克隆仓库。

```console
$ git clone https://github.com/spring-projects/spring-petclinic.git
```

示例应用程序是一个使用 Maven 构建的 Spring Boot 应用程序。有关更多详细信息，请参阅仓库中的 `readme.md`。

## 初始化 Docker 资源

现在您已有一个应用程序，可以创建必要的 Docker 资源来容器化您的应用程序。您可以使用 Docker Desktop 内置的 Docker Init 功能来帮助简化流程，也可以手动创建这些资源。

{{< tabs >}}
{{< tab name="使用 Docker Init" >}}

在 `spring-petclinic` 目录中，运行 `docker init` 命令。`docker init` 会提供一些默认配置，但您需要回答一些关于应用程序的问题。参考以下示例回答 `docker init` 的提示，并为您的提示使用相同的答案。

示例应用程序已包含 Docker 资源。系统会提示您覆盖现有的 Docker 资源。要继续本指南，请选择 `y` 以覆盖它们。

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

在上面的示例中，请注意 `WARNING`。`docker-compose.yaml` 已存在，因此 `docker init` 会覆盖该文件，而不是创建新的 `compose.yaml` 文件。这样可以防止目录中出现多个 Compose 文件。两种名称都受支持，但 Compose 首选标准名称 `compose.yaml`。

{{< /tab >}}
{{< tab name="手动创建资源" >}}

如果您未安装 Docker Desktop 或更喜欢手动创建资源，可以在项目目录中创建以下文件。

创建一个名为 `Dockerfile` 的文件，内容如下。

```dockerfile {collapse=true,title=Dockerfile}
# syntax=docker/dockerfile:1

# 本文件各处提供了注释，帮助您入门。
# 如果您需要更多帮助，请访问 Dockerfile 参考指南：
# https://docs.docker.com/go/dockerfile-reference/

# 想帮助我们改进此模板？请在此处分享您的反馈：https://forms.gle/ybq9Krt8jtBL3iCk7

################################################################################

# 创建一个用于解析和下载依赖项的阶段。
FROM eclipse-temurin:21-jdk-jammy as deps

WORKDIR /build

# 复制具有可执行权限的 mvnw 包装器。
COPY --chmod=0755 mvnw mvnw
COPY .mvn/ .mvn/

# 将下载依赖项作为单独步骤，以利用 Docker 的缓存。
# 利用缓存挂载到 /root/.m2，以便后续构建无需重新下载包。
RUN --mount=type=bind,source=pom.xml,target=pom.xml \
    --mount=type=cache,target=/root/.m2 ./mvnw dependency:go-offline -DskipTests

################################################################################

# 创建一个基于已下载依赖项阶段的构建应用程序阶段。
# 此 Dockerfile 针对输出 uber jar 的 Java 应用程序进行了优化，uber jar 包含在 JVM 中运行应用所需的所有依赖项。
# 如果您的应用不输出 uber jar，而是依赖 Apache Tomcat 等应用服务器，则需要更新此阶段的包文件名，
# 并更新 "final" 阶段的基础镜像以使用相关应用服务器，例如使用 tomcat（https://hub.docker.com/_/tomcat/）作为基础镜像。
FROM deps as package

WORKDIR /build

COPY ./src src/
RUN --mount=type=bind,source=pom.xml,target=pom.xml \
    --mount=type=cache,target=/root/.m2 \
    ./mvnw package -DskipTests && \
    mv target/$(./mvnw help:evaluate -Dexpression=project.artifactId -q -DforceStdout)-$(./mvnw help:evaluate -Dexpression=project.version -q -DforceStdout).jar target/app.jar

################################################################################

# 创建一个用于将应用程序提取到单独层的阶段。
# 利用 Spring Boot 的层工具和 Docker 的缓存，将打包的应用程序提取到可复制到最终阶段的单独层中。
# 参考 Spring 文档：
# https://docs.spring.io/spring-boot/docs/current/reference/html/container-images.html
FROM package as extract

WORKDIR /build

RUN java -Djarmode=layertools -jar target/app.jar extract --destination target/extracted

################################################################################

# 创建一个新的运行应用程序阶段，该阶段包含应用程序的最小运行时依赖项。
# 此阶段通常使用与安装或构建阶段不同的基础镜像，必要文件从安装阶段复制。
#
# 以下示例使用 eclipse-turmin 的 JRE 镜像作为运行应用的基础。
# 通过指定 "17-jre-jammy" 标签，它还会使用构建 Dockerfile 时该标签的最新版本。
# 如果可重现性很重要，请考虑使用特定的摘要 SHA，例如
# eclipse-temurin@sha256:99cede493dfd88720b610eb8077c8688d3cca50003d76d1d539b0efc8cca72b4。
FROM eclipse-temurin:21-jre-jammy AS final

# 创建一个应用将以其身份运行的非特权用户。
# 参见 https://docs.docker.com/go/dockerfile-user-best-practices/
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

# 从 "package" 阶段复制可执行文件。
COPY --from=extract build/target/extracted/dependencies/ ./
COPY --from=extract build/target/extracted/spring-boot-loader/ ./
COPY --from=extract build/target/extracted/snapshot-dependencies/ ./
COPY --from=extract build/target/extracted/application/ ./

EXPOSE 8080

ENTRYPOINT [ "java", "org.springframework.boot.loader.launch.JarLauncher" ]
```

示例已包含 Compose 文件。覆盖此文件以继续本指南。使用以下内容更新 `docker-compose.yaml`。

```yaml {collapse=true,title=docker-compose.yaml}
# 本文件各处提供了注释，帮助您入门。
# 如果您需要更多帮助，请访问 Docker Compose 参考指南：
# https://docs.docker.com/go/compose-spec-reference/

# 此处指令将您的应用程序定义为名为 "server" 的服务。
# 此服务从当前目录的 Dockerfile 构建。
# 您可以在此处添加应用程序可能依赖的其他服务，例如数据库或缓存。有关示例，请参阅 Awesome Compose 仓库：
# https://github.com/docker/awesome-compose
services:
  server:
    build:
      context: .
    ports:
      - 8080:8080
# 以下注释部分是定义 PostgreSQL 数据库的示例，您的应用程序可以使用。
# `depends_on` 告诉 Docker Compose 在应用程序之前启动数据库。
# `db-data` 卷在容器重启之间持久化数据库数据。
# `db-password` 密钥用于设置数据库密码。在运行 `docker compose up` 之前，
# 您必须创建 `db/password.txt` 并向其中添加您选择的密码。
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
# 在此处包含您不希望复制到容器中的任何文件或目录（例如，本地构建产物、临时文件等）。
#
# 如需更多帮助，请访问 .dockerignore 文件参考指南：
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

现在您的 `spring-petclinic` 目录中应包含以下三个文件。

- [Dockerfile](/reference/dockerfile/)
- [.dockerignore](/reference/dockerfile/#dockerignore-file)
- [docker-compose.yaml](/reference/compose-file/_index.md)

## 运行应用程序

在 `spring-petclinic` 目录中，在终端中运行以下命令。

```console
$ docker compose up --build
```

首次构建和运行应用时，Docker 会下载依赖项并构建应用。根据您的网络连接，可能需要几分钟时间。

打开浏览器并访问 [http://localhost:8080](http://localhost:8080) 查看应用程序。您应该能看到一个简单的宠物诊所应用。

在终端中按 `ctrl`+`c` 停止应用程序。

### 在后台运行应用程序

您可以通过添加 `-d` 选项在终端后台运行应用程序。在 `spring-petclinic` 目录中，在终端中运行以下命令。

```console
$ docker compose up --build -d
```

打开浏览器并访问 [http://localhost:8080](http://localhost:8080) 查看应用程序。您应该能看到一个简单的宠物诊所应用。

在终端中运行以下命令以停止应用程序。

```console
$ docker compose down
```

有关 Compose 命令的更多信息，请参阅
[Compose CLI 参考](/reference/cli/docker/compose/_index.md)。

## 总结

在本节中，您学习了如何使用 Docker 容器化和运行 Java 应用程序。

相关信息：

- [docker init 参考](/reference/cli/docker/init/)

## 下一步

在下一节中，您将学习如何使用 Docker 容器开发您的应用程序。