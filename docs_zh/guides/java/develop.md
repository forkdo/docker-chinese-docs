---
title: 为 Java 开发使用容器
linkTitle: 开发你的应用
weight: 20
keywords: Java, 本地, 开发, 运行,
description: 了解如何在本地开发你的应用程序。
aliases:
  - /language/java/develop/
  - /guides/language/java/develop/
---

## 前置条件

完成[容器化你的应用](containerize.md)中的步骤。

## 概述

在本节中，你将学习如何为上一节中容器化的应用程序设置本地开发环境。包括：

- 添加本地数据库并持久化数据
- 创建一个开发容器以连接调试器
- 配置 Compose，使你在编辑和保存代码时自动更新正在运行的 Compose 服务

## 添加本地数据库并持久化数据

你可以使用容器设置本地服务，比如数据库。在本节中，你将更新 `docker-compose.yaml` 文件，定义数据库服务和持久化数据的卷。此外，此特定应用程序使用系统属性定义数据库类型，因此你需要更新 `Dockerfile`，在启动应用时传入系统属性。

在克隆的仓库目录中，使用 IDE 或文本编辑器打开 `docker-compose.yaml` 文件。你的 Compose 文件中已有一个示例数据库服务，但需要进行一些修改以适配你的独特应用。

在 `docker-compose.yaml` 文件中，你需要执行以下操作：

- 取消注释所有数据库指令。现在你将使用数据库服务而不是本地存储数据。
- 删除顶级 `secrets` 元素以及 `db` 服务内的元素。此示例使用环境变量而非密钥存储密码。
- 删除 `db` 服务中的 `user` 元素。此示例在环境变量中指定用户。
- 更新数据库环境变量。这些变量由 Postgres 镜像定义。更多详细信息，请参阅
  [Postgres 官方 Docker 镜像](https://hub.docker.com/_/postgres)。
- 更新 `db` 服务的健康检查测试并指定用户。默认情况下，健康检查使用 root 用户而不是你定义的 `petclinic` 用户。
- 在 `server` 服务中添加数据库 URL 作为环境变量。这会覆盖在
  `spring-petclinic/src/main/resources/application-postgres.properties`
  中定义的默认值。

以下是更新后的 `docker-compose.yaml` 文件。所有注释已被移除。

```yaml {hl_lines="7-29"}
services:
  server:
    build:
      context: .
    ports:
      - 8080:8080
    depends_on:
      db:
        condition: service_healthy
    environment:
      - POSTGRES_URL=jdbc:postgresql://db:5432/petclinic
  db:
    image: postgres:18
    restart: always
    volumes:
      - db-data:/var/lib/postgresql
    environment:
      - POSTGRES_DB=petclinic
      - POSTGRES_USER=petclinic
      - POSTGRES_PASSWORD=petclinic
    ports:
      - 5432:5432
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "petclinic"]
      interval: 10s
      timeout: 5s
      retries: 5
volumes:
  db-data:
```

使用 IDE 或文本编辑器打开 `Dockerfile`。在 `ENTRYPOINT` 指令中，更新指令以传入系统属性，如
`spring-petclinic/src/resources/db/postgres/petclinic_db_setup_postgres.txt`
文件中所指定。

```diff
- ENTRYPOINT [ "java", "org.springframework.boot.loader.launch.JarLauncher" ]
+ ENTRYPOINT [ "java", "-Dspring.profiles.active=postgres", "org.springframework.boot.loader.launch.JarLauncher" ]
```

保存并关闭所有文件。

现在，运行以下 `docker compose up` 命令启动你的应用程序。

```console
$ docker compose up --build
```

打开浏览器，在 [http://localhost:8080](http://localhost:8080) 查看应用程序。你应该能看到一个简单的宠物诊所应用。浏览应用。导航到 **Veterinarians**，通过能够列出兽医来验证应用已连接到数据库。

在终端中，按 `ctrl`+`c` 停止应用。

## 开发用 Dockerfile

你现在拥有的 Dockerfile 很适合生产环境，它是一个小巧、安全的镜像，只包含运行应用所需的组件。开发时，你可能需要一个具有不同环境的镜像。

例如，在开发镜像中，你可能希望配置镜像以启动应用，以便你可以将调试器连接到正在运行的 Java 进程。

与其管理多个 Dockerfile，不如添加一个新阶段。你的 Dockerfile 可以同时生成准备用于生产的最终镜像和开发镜像。

使用以下内容替换你的 Dockerfile 内容。

```dockerfile {hl_lines="22-29"}
# syntax=docker/dockerfile:1

FROM eclipse-temurin:21-jdk-jammy as deps
WORKDIR /build
COPY --chmod=0755 mvnw mvnw
COPY .mvn/ .mvn/
RUN --mount=type=bind,source=pom.xml,target=pom.xml \
    --mount=type=cache,target=/root/.m2 ./mvnw dependency:go-offline -DskipTests

FROM deps as package
WORKDIR /build
COPY ./src src/
RUN --mount=type=bind,source=pom.xml,target=pom.xml \
    --mount=type=cache,target=/root/.m2 \
    ./mvnw package -DskipTests && \
    mv target/$(./mvnw help:evaluate -Dexpression=project.artifactId -q -DforceStdout)-$(./mvnw help:evaluate -Dexpression=project.version -q -DforceStdout).jar target/app.jar

FROM package as extract
WORKDIR /build
RUN java -Djarmode=layertools -jar target/app.jar extract --destination target/extracted

FROM extract as development
WORKDIR /build
RUN cp -r /build/target/extracted/dependencies/. ./
RUN cp -r /build/target/extracted/spring-boot-loader/. ./
RUN cp -r /build/target/extracted/snapshot-dependencies/. ./
RUN cp -r /build/target/extracted/application/. ./
ENV JAVA_TOOL_OPTIONS -agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:8000
CMD [ "java", "-Dspring.profiles.active=postgres", "org.springframework.boot.loader.launch.JarLauncher" ]

FROM eclipse-temurin:21-jre-jammy AS final
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
COPY --from=extract build/target/extracted/dependencies/ ./
COPY --from=extract build/target/extracted/spring-boot-loader/ ./
COPY --from=extract build/target/extracted/snapshot-dependencies/ ./
COPY --from=extract build/target/extracted/application/ ./
EXPOSE 8080
ENTRYPOINT [ "java", "-Dspring.profiles.active=postgres", "org.springframework.boot.loader.launch.JarLauncher" ]
```

保存并关闭 `Dockerfile`。

在 `Dockerfile` 中，你添加了一个基于 `extract` 阶段的新阶段，标记为 `development`。在此阶段中，你将提取的文件复制到公共目录，然后运行启动应用的命令。在命令中，你暴露端口 8000 并声明 JVM 的调试配置，以便你可以附加调试器。

## 使用 Compose 进行本地开发

当前的 Compose 文件不会启动你的开发容器。为此，你必须更新 Compose 文件以定位开发阶段。同时，更新服务器服务的端口映射以提供调试器访问。

打开 `docker-compose.yaml` 并在文件中添加以下指令。

```yaml {hl_lines=["5","8"]}
services:
  server:
    build:
      context: .
      target: development
    ports:
      - 8080:8080
      - 8000:8000
    depends_on:
      db:
        condition: service_healthy
    environment:
      - POSTGRES_URL=jdbc:postgresql://db:5432/petclinic
  db:
    image: postgres:18
    restart: always
    volumes:
      - db-data:/var/lib/postgresql
    environment:
      - POSTGRES_DB=petclinic
      - POSTGRES_USER=petclinic
      - POSTGRES_PASSWORD=petclinic
    ports:
      - 5432:5432
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "petclinic"]
      interval: 10s
      timeout: 5s
      retries: 5
volumes:
  db-data:
```

现在，启动你的应用并确认它正在运行。

```console
$ docker compose up --build
```

最后，测试你的 API 端点。运行以下 curl 命令：

```console
$ curl  --request GET \
  --url http://localhost:8080/vets \
  --header 'content-type: application/json'
```

你应该收到以下响应：

```json
{
  "vetList": [
    {
      "id": 1,
      "firstName": "James",
      "lastName": "Carter",
      "specialties": [],
      "nrOfSpecialties": 0,
      "new": false
    },
    {
      "id": 2,
      "firstName": "Helen",
      "lastName": "Leary",
      "specialties": [{ "id": 1, "name": "radiology", "new": false }],
      "nrOfSpecialties": 1,
      "new": false
    },
    {
      "id": 3,
      "firstName": "Linda",
      "lastName": "Douglas",
      "specialties": [
        { "id": 3, "name": "dentistry", "new": false },
        { "id": 2, "name": "surgery", "new": false }
      ],
      "nrOfSpecialties": 2,
      "new": false
    },
    {
      "id": 4,
      "firstName": "Rafael",
      "lastName": "Ortega",
      "specialties": [{ "id": 2, "name": "surgery", "new": false }],
      "nrOfSpecialties": 1,
      "new": false
    },
    {
      "id": 5,
      "firstName": "Henry",
      "lastName": "Stevens",
      "specialties": [{ "id": 1, "name": "radiology", "new": false }],
      "nrOfSpecialties": 1,
      "new": false
    },
    {
      "id": 6,
      "firstName": "Sharon",
      "lastName": "Jenkins",
      "specialties": [],
      "nrOfSpecialties": 0,
      "new": false
    }
  ]
}
```

## 连接调试器

你将使用 IntelliJ IDEA 自带的调试器。你可以使用此 IDE 的社区版。在 IntelliJ IDEA 中打开你的项目，进入 **Run** 菜单，然后选择 **Edit Configuration**。添加一个新的 Remote JVM Debug 配置，类似于以下内容：

![Java 连接调试器](images/connect-debugger.webp)

设置断点。

打开 `src/main/java/org/springframework/samples/petclinic/vet/VetController.java` 并在 `showResourcesVetList` 函数内添加一个断点。

要开始调试会话，选择 **Run** 菜单，然后选择 **Debug _NameOfYourConfiguration_**。

![调试菜单](images/debug-menu.webp?w=300)

你现在应该能在 Compose 应用的日志中看到连接。

![Compose 日志文件 ](images/compose-logs.webp)

你现在可以调用服务器端点。

```console
$ curl --request GET --url http://localhost:8080/vets
```

你应该看到代码在标记的行上中断，现在你可以像平常一样使用调试器。你还可以检查和监视变量，设置条件断点，查看堆栈跟踪等。

![调试器代码断点](images/debugger-breakpoint.webp)

在终端中按 `ctrl+c` 停止你的应用。

## 自动更新服务

使用 Compose Watch 在你编辑和保存代码时自动更新正在运行的 Compose 服务。有关 Compose Watch 的更多详细信息，请参阅
[使用 Compose Watch](/manuals/compose/how-tos/file-watch.md)。

在 IDE 或文本编辑器中打开 `docker-compose.yaml` 文件，然后添加
Compose Watch 指令。以下是更新后的 `docker-compose.yaml`
文件。

```yaml {hl_lines="14-17"}
services:
  server:
    build:
      context: .
      target: development
    ports:
      - 8080:8080
      - 8000:8000
    depends_on:
      db:
        condition: service_healthy
    environment:
      - POSTGRES_URL=jdbc:postgresql://db:5432/petclinic
    develop:
      watch:
        - action: rebuild
          path: .
  db:
    image: postgres:18
    restart: always
    volumes:
      - db-data:/var/lib/postgresql
    environment:
      - POSTGRES_DB=petclinic
      - POSTGRES_USER=petclinic
      - POSTGRES_PASSWORD=petclinic
    ports:
      - 5432:5432
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "petclinic"]
      interval: 10s
      timeout: 5s
      retries: 5
volumes:
  db-data:
```

运行以下命令，使用 Compose Watch 运行你的应用。

```console
$ docker compose watch
```

打开浏览器，在 [http://localhost:8080](http://localhost:8080) 查看应用。你应该看到 Spring 宠物诊所的主页。

现在，应用源文件在你本地机器上的任何更改都会自动反映在运行的容器中。

在 IDE 或文本编辑器中打开 `spring-petclinic/src/main/resources/templates/fragments/layout.html`，通过添加感叹号更新 `Home` 导航字符串。

```diff
-   <li th:replace="~{::menuItem ('/','home','home page','home','Home')}">
+   <li th:replace="~{::menuItem ('/','home','home page','home','Home!')}">

```

保存 `layout.html` 的更改，然后你可以继续开发，容器会自动重建。

容器重建并运行后，刷新 [http://localhost:8080](http://localhost:8080)，然后验证 **Home!** 现在出现在菜单中。

在终端中按 `ctrl+c` 停止 Compose Watch。

## 总结

在本节中，你了解了如何运行本地数据库并持久化数据。你还创建了一个包含 JDK 的开发镜像，允许你附加调试器。最后，你设置了 Compose 文件以暴露调试端口，并配置 Compose Watch 实现热重载。

相关信息：

- [Compose 文件参考](/reference/compose-file/)
- [Compose Watch](/manuals/compose/how-tos/file-watch.md)
- [Dockerfile 参考](/reference/dockerfile/)

## 下一步

在下一节中，你将了解如何在 Docker 中运行单元测试。