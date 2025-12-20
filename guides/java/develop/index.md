# 使用容器进行 Java 开发
## 先决条件

请先完成[容器化您的应用](containerize.md)中的步骤，将您的应用容器化。

## 概述

在本节中，您将为上一节中容器化的应用搭建本地开发环境。这包括：

- 添加本地数据库并持久化数据
- 创建开发容器以连接调试器
- 配置 Compose，以便在您编辑并保存代码时自动更新正在运行的 Compose 服务

## 添加本地数据库并持久化数据

您可以使用容器来搭建本地服务，例如数据库。在本节中，您将更新 `docker-compose.yaml` 文件以定义数据库服务和用于持久化数据的卷。此外，这个特定的应用程序使用系统属性来定义数据库类型，因此您需要更新 `Dockerfile` 以便在启动应用时传入该系统属性。

在克隆的仓库目录中，使用 IDE 或文本编辑器打开 `docker-compose.yaml` 文件。您的 Compose 文件中有一个示例数据库服务，但需要根据您独特的应用进行一些更改。

在 `docker-compose.yaml` 文件中，您需要执行以下操作：

- 取消注释所有数据库指令。您现在将使用数据库服务，而不是本地存储来保存数据。
- 移除顶层的 `secrets` 元素以及 `db` 服务内的元素。此示例使用环境变量来设置密码，而不是 secrets。
- 移除 `db` 服务中的 `user` 元素。此示例在环境变量中指定用户。
- 更新数据库环境变量。这些由 Postgres 镜像定义。更多详情，请参阅 [Postgres 官方 Docker 镜像](https://hub.docker.com/_/postgres)。
- 更新 `db` 服务的 healthcheck 测试并指定用户。默认情况下，healthcheck 使用 root 用户，而不是您定义的 `petclinic` 用户。
- 将数据库 URL 作为环境变量添加到 `server` 服务中。这将覆盖 `spring-petclinic/src/main/resources/application-postgres.properties` 中定义的默认值。

以下是更新后的 `docker-compose.yaml` 文件。所有注释均已移除。

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

使用 IDE 或文本编辑器打开 `Dockerfile`。在 `ENTRYPOINT` 指令中，更新该指令以传入 `spring-petclinic/src/resources/db/postgres/petclinic_db_setup_postgres.txt` 文件中指定的系统属性。

```diff
- ENTRYPOINT [ "java", "org.springframework.boot.loader.launch.JarLauncher" ]
+ ENTRYPOINT [ "java", "-Dspring.profiles.active=postgres", "org.springframework.boot.loader.launch.JarLauncher" ]
```

保存并关闭所有文件。

现在，运行以下 `docker compose up` 命令来启动您的应用程序。

```console
$ docker compose up --build
```

打开浏览器，访问 [http://localhost:8080](http://localhost:8080) 查看应用程序。您应该会看到一个简单的宠物诊所应用。浏览该应用程序。导航到 **Veterinarians**（兽医），通过能否列出兽医来验证应用程序是否已连接到数据库。

在终端中，按 `ctrl`+`c` 停止应用程序。

## 用于开发的 Dockerfile

您现在的 Dockerfile 非常适合生成一个小巧、安全的生产镜像，其中仅包含运行应用程序所需的组件。在开发时，您可能需要一个具有不同环境的不同镜像。

例如，在开发镜像中，您可能希望设置镜像以启动应用程序，这样您就可以将调试器连接到正在运行的 Java 进程。

与其管理多个 Dockerfile，您可以添加一个新的构建阶段。这样，您的 Dockerfile 就可以生成一个可用于生产的最终镜像，以及一个开发镜像。

用以下内容替换您的 Dockerfile 内容。

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

在 `Dockerfile` 中，您添加了一个基于 `extract` 阶段的、名为 `development` 的新阶段。在此阶段，您将提取的文件复制到一个公共目录，然后运行一个命令来启动应用程序。在该命令中，您暴露了端口 8000，并声明了 JVM 的调试配置，以便您可以附加调试器。

## 使用 Compose 进行本地开发

当前的 Compose 文件不会启动您的开发容器。为此，您必须更新您的 Compose 文件以定位开发阶段。此外，更新服务器服务的端口映射，以便为调试器提供访问权限。

打开 `docker-compose.yaml` 并将以下指令添加到文件中。

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

现在，启动您的应用程序并确认它正在运行。

```console
$ docker compose up --build
```

最后，测试您的 API 端点。运行以下 curl 命令：

```console
$ curl  --request GET \
  --url http://localhost:8080/vets \
  --header 'content-type: application/json'
```

您应该会收到以下响应：

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

您将使用 IntelliJ IDEA 自带的调试器。您可以使用此 IDE 的社区版。在 IntelliJ IDEA 中打开您的项目，转到 **Run** 菜单，然后选择 **Edit Configuration**。添加一个新的 Remote JVM Debug 配置，类似于以下内容：

![Java 连接调试器](images/connect-debugger.webp)

设置一个断点。

打开 `src/main/java/org/springframework/samples/petclinic/vet/VetController.java`，并在 `showResourcesVetList` 函数内部添加一个断点。

要开始调试会话，请选择 **Run** 菜单，然后选择 **Debug _您的配置名称_**。

![调试菜单](images/debug-menu.webp?w=300)

您现在应该在 Compose 应用程序的日志中看到连接。

![Compose 日志文件](images/compose-logs.webp)

您现在可以调用服务器端点。

```console
$ curl --request GET --url http://localhost:8080/vets
```

您应该看到代码在标记行处中断，现在您可以像往常一样使用调试器了。您还可以检查和监视变量、设置条件断点、查看堆栈跟踪以及执行许多其他操作。

![调试器代码断点](images/debugger-breakpoint.webp)

在终端中按 `ctrl+c` 停止您的应用程序。

## 自动更新服务

使用 Compose Watch 在您编辑并保存代码时自动更新正在运行的 Compose 服务。有关 Compose Watch 的更多详情，请参阅 [使用 Compose Watch](/manuals/compose/how-tos/file-watch.md)。

使用 IDE 或文本编辑器打开您的 `docker-compose.yaml` 文件，然后添加 Compose Watch 指令。以下是更新后的 `docker-compose.yaml` 文件。

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

运行以下命令，使用 Compose Watch 运行您的应用程序。

```console
$ docker compose watch
```

打开 Web 浏览器，访问 [http://localhost:8080](http://localhost:8080) 查看应用程序。您应该会看到 Spring Pet Clinic 主页。

现在，对本地计算机上应用程序源文件的任何更改都将自动反映在正在运行的容器中。

使用 IDE 或文本编辑器打开 `spring-petclinic/src/main/resources/templates/fragments/layout.html`，通过添加一个感叹号来更新 `Home` 导航字符串。

```diff
-   <li th:replace="~{::menuItem ('/','home','home page','home','Home')}">
+   <li th:replace="~{::menuItem ('/','home','home page','home','Home!')}">

```

保存对 `layout.html` 的更改，然后您可以继续开发，同时容器会自动重建。

容器重建并运行后，刷新 [http://localhost:8080](http://localhost:8080)，然后验证菜单中是否出现了 **Home!**。

在终端中按 `ctrl+c` 停止 Compose Watch。

## 总结

在本节中，您了解了如何在本地运行数据库并持久化数据。您还创建了一个包含 JDK 并允许您附加调试器的开发镜像。最后，您设置了 Compose 文件以暴露调试端口，并配置了 Compose Watch 以实时重新加载您的更改。

相关信息：

- [Compose 文件参考](/reference/compose-file/)
- [Compose Watch](/manuals/compose/how-tos/file-watch.md)
- [Dockerfile 参考](/reference/dockerfile/)

## 下一步

在下一节中，您将了解如何在 Docker 中运行单元测试。
