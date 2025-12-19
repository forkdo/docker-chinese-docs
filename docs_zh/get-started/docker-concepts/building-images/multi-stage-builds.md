---
title: 多阶段构建
keywords: 概念, 构建, 镜像, 容器, docker desktop
description: 本概念页面将为您介绍多阶段构建的目的及其优势
summary: |
  通过将构建环境与最终运行环境分离，您可以显著减小镜像体积并缩小攻击面。在本指南中，您将掌握多阶段构建的强大功能，以创建精简高效的 Docker 镜像，这对于最小化开销和增强生产环境中的部署至关重要。
weight: 5
aliases: 
 - /guides/docker-concepts/building-images/multi-stage-builds/
---

{{< youtube-embed vR185cjwxZ8 >}}

## 解释

在传统构建中，所有构建指令都在单个构建容器中按顺序执行：下载依赖项、编译代码以及打包应用程序。所有这些层最终都会进入您的最终镜像。这种方法可行，但它会导致镜像臃肿，携带不必要的重量，并增加您的安全风险。这就是多阶段构建的用武之地。

多阶段构建在您的 Dockerfile 中引入了多个阶段，每个阶段都有特定的用途。可以将其视为能够在多个不同的环境中并发运行构建的不同部分的能力。通过将构建环境与最终运行环境分离，您可以显著减小镜像体积并缩小攻击面。这对于具有大型构建依赖项的应用程序尤其有益。

多阶段构建适用于所有类型的应用程序。

- 对于解释型语言，如 JavaScript、Ruby 或 Python，您可以在一个阶段构建和压缩代码，然后将生产就绪的文件复制到更小的运行时镜像中。这可以优化您的镜像以进行部署。
- 对于编译型语言，如 C、Go 或 Rust，多阶段构建让您可以在一个阶段进行编译，并将编译后的二进制文件复制到最终的运行时镜像中。无需在最终镜像中捆绑整个编译器。

以下是一个使用伪代码的多阶段构建结构的简化示例。请注意，这里有多个 `FROM` 语句和一个新的 `AS <stage-name>`。此外，第二阶段的 `COPY` 语句正在从之前的阶段 `--from` 复制。

```dockerfile
# 阶段 1: 构建环境
FROM builder-image AS build-stage 
# 安装构建工具 (例如, Maven, Gradle)
# 复制源代码
# 构建命令 (例如, 编译, 打包)

# 阶段 2: 运行时环境
FROM runtime-image AS final-stage  
# 从构建阶段复制应用程序构件 (例如, JAR 文件)
COPY --from=build-stage /path/in/build/stage /path/to/place/in/final/stage
# 定义运行时配置 (例如, CMD, ENTRYPOINT) 
```

这个 Dockerfile 使用了两个阶段：

- 构建阶段使用一个包含编译应用程序所需构建工具的基础镜像。它包括安装构建工具、复制源代码和执行构建命令的指令。
- 最终阶段使用一个适合运行您应用程序的更小的基础镜像。它从构建阶段复制编译后的构件（例如 JAR 文件）。最后，它定义了启动应用程序的运行时配置（使用 `CMD` 或 `ENTRYPOINT`）。

## 动手尝试

在这篇实践指南中，您将掌握多阶段构建的强大功能，为一个示例 Java 应用程序创建精简高效的 Docker 镜像。您将使用一个简单的基于 Spring Boot 的 "Hello World" 应用程序（使用 Maven 构建）作为示例。

1. [下载并安装](https://www.docker.com/products/docker-desktop/) Docker Desktop。

2. 打开这个[预初始化的项目](https://start.spring.io/#!type=maven-project&language=java&platformVersion=3.4.0-M3&packaging=jar&jvmVersion=21&groupId=com.example&artifactId=spring-boot-docker&name=spring-boot-docker&description=Demo%20project%20for%20Spring%20Boot&packageName=com.example.spring-boot-docker&dependencies=web)以生成一个 ZIP 文件。如下图所示：


    ![一张 Spring Initializr 工具的截图，已选择 Java 21、Spring Web 和 Spring Boot 3.4.0](images/multi-stage-builds-spring-initializer.webp?border=true)


    [Spring Initializr](https://start.spring.io/) 是一个用于 Spring 项目的快速启动生成器。它提供了一个可扩展的 API 来生成基于 JVM 的项目，并为几种常见概念提供实现——例如 Java、Kotlin 和 Groovy 的基本语言生成。

    选择 **Generate** 来创建并下载此项目的 zip 文件。

    在此演示中，您已将 Maven 构建自动化与 Java、Spring Web 依赖项以及用于元数据的 Java 21 配对。

3. 浏览项目目录。解压文件后，您将看到以下项目目录结构：

    ```plaintext
    spring-boot-docker
    ├── HELP.md
    ├── mvnw
    ├── mvnw.cmd
    ├── pom.xml
    └── src
        ├── main
        │   ├── java
        │   │   └── com
        │   │       └── example
        │   │           └── spring_boot_docker
        │   │               └── SpringBootDockerApplication.java
        │   └── resources
        │       ├── application.properties
        │       ├── static
        │       └── templates
        └── test
            └── java
                └── com
                    └── example
                        └── spring_boot_docker
                            └── SpringBootDockerApplicationTests.java
    
    15 directories, 7 files
    ```

   `src/main/java` 目录包含您项目的源代码，`src/test/java` 目录包含测试源代码，而 `pom.xml` 文件是您的项目对象模型 (POM)。

   `pom.xml` 文件是 Maven 项目配置的核心。它是一个单一的配置文件，包含构建定制项目所需的大部分信息。POM 很庞大，可能看起来令人生畏。幸运的是，您还不需要理解每一个细节就能有效地使用它。

4. 创建一个显示 "Hello World!" 的 RESTful Web 服务。

    
    在 `src/main/java/com/example/spring_boot_docker/` 目录下，您可以使用以下内容修改您的 `SpringBootDockerApplication.java` 文件：

    ```java
    package com.example.spring_boot_docker;

    import org.springframework.boot.SpringApplication;
    import org.springframework.boot.autoconfigure.SpringBootApplication;
    import org.springframework.web.bind.annotation.RequestMapping;
    import org.springframework.web.bind.annotation.RestController;


    @RestController
    @SpringBootApplication
    public class SpringBootDockerApplication {

        @RequestMapping("/")
            public String home() {
            return "Hello World";
        }

    	public static void main(String[] args) {
    		SpringApplication.run(SpringBootDockerApplication.class, args);
    	}

    }
    ```

    `SpringbootDockerApplication.java` 文件首先声明您的 `com.example.spring_boot_docker` 包并导入必要的 Spring 框架。这个 Java 文件创建了一个简单的 Spring Boot Web 应用程序，当用户访问其主页时会响应 "Hello World"。

### 创建 Dockerfile

现在您有了项目，就可以创建 `Dockerfile` 了。

 1. 在包含所有其他文件夹和文件（如 src、pom.xml 等）的同一文件夹中创建一个名为 `Dockerfile` 的文件。

 2. 在 `Dockerfile` 中，通过添加以下行来定义您的基础镜像：

     ```dockerfile
     FROM eclipse-temurin:21.0.8_9-jdk-jammy
     ```

 3. 现在，使用 `WORKDIR` 指令定义工作目录。这将指定未来命令运行的位置以及文件将被复制到容器镜像中的目录。

     ```dockerfile
     WORKDIR /app
     ```

 4. 将 Maven 包装器脚本和您项目的 `pom.xml` 文件复制到 Docker 容器内的当前工作目录 `/app` 中。

     ```dockerfile
     COPY .mvn/ .mvn
     COPY mvnw pom.xml ./
     ```

 5. 在容器内执行一个命令。它运行 `./mvnw dependency:go-offline` 命令，该命令使用 Maven 包装器 (`./mvnw`) 下载项目的所有依赖项，而不构建最终的 JAR 文件（对于更快的构建很有用）。

     ```dockerfile
     RUN ./mvnw dependency:go-offline
     ```

 6. 将主机上的 `src` 目录复制到容器内的 `/app` 目录中。

     ```dockerfile
     COPY src ./src
     ```

 7. 设置容器启动时要执行的默认命令。此命令指示容器使用 `spring-boot:run` 目标运行 Maven 包装器 (`./mvnw`)，这将构建并执行您的 Spring Boot 应用程序。

     ```dockerfile
     CMD ["./mvnw", "spring-boot:run"]
     ```

    完成以上步骤后，您应该得到以下 Dockerfile：

    ```dockerfile 
    FROM eclipse-temurin:21.0.8_9-jdk-jammy
    WORKDIR /app
    COPY .mvn/ .mvn
    COPY mvnw pom.xml ./
    RUN ./mvnw dependency:go-offline
    COPY src ./src
    CMD ["./mvnw", "spring-boot:run"]
    ```

### 构建容器镜像

 1. 执行以下命令来构建 Docker 镜像：

    ```console
    $ docker build -t spring-helloworld .
    ```

 2. 使用 `docker images` 命令检查 Docker 镜像的大小：

    ```console
    $ docker images
    ```

    这样做将产生类似以下的输出：

    ```console
    REPOSITORY          TAG       IMAGE ID       CREATED          SIZE
    spring-helloworld   latest    ff708d5ee194   3 minutes ago    880MB
    ```

    此输出显示您的镜像大小为 880MB。它包含了完整的 JDK、Maven 工具链等。在生产环境中，您的最终镜像中不需要这些。

### 运行 Spring Boot 应用程序

1. 现在您已经有了构建好的镜像，是时候运行容器了。

    ```console
    $ docker run -p 8080:8080 spring-helloworld
    ```

    然后您将在容器日志中看到类似以下的输出：

    ```plaintext
    [INFO] --- spring-boot:3.3.4:run (default-cli) @ spring-boot-docker ---
    [INFO] Attaching agents: []
    
         .   ____          _            __ _ _
        /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
       ( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
        \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
         '  |____| .__|_| |_|_| |_\__, | / / / /
        =========|_|==============|___/=/_/_/_/
    
        :: Spring Boot ::                (v3.3.4)
    
    2024-09-29T23:54:07.157Z  INFO 159 --- [spring-boot-docker] [           main]
    c.e.s.SpringBootDockerApplication        : Starting SpringBootDockerApplication using Java
    21.0.2 with PID 159 (/app/target/classes started by root in /app)
     ….
     ```

2. 通过您的 Web 浏览器访问您的 "Hello World" 页面，地址为 [http://localhost:8080](http://localhost:8080)，或通过以下 curl 命令访问：

    ```console
    $ curl localhost:8080
    Hello World
    ```

### 使用多阶段构建

1. 考虑以下 Dockerfile：

    ```dockerfile
    FROM eclipse-temurin:21.0.8_9-jdk-jammy AS builder
    WORKDIR /opt/app
    COPY .mvn/ .mvn
    COPY mvnw pom.xml ./
    RUN ./mvnw dependency:go-offline
    COPY ./src ./src
    RUN ./mvnw clean install

    FROM eclipse-temurin:21.0.8_9-jre-jammy AS final
    WORKDIR /opt/app
    EXPOSE 8080
    COPY --from=builder /opt/app/target/*.jar /opt/app/*.jar
    ENTRYPOINT ["java", "-jar", "/opt/app/*.jar"]
    ```

    请注意，此 Dockerfile 已被拆分为两个阶段。

    - 第一阶段与之前的 Dockerfile 保持一致，为构建应用程序提供 Java 开发工具包 (JDK) 环境。此阶段被命名为 builder。

    - 第二阶段是一个名为 `final` 的新阶段。它使用更精简的 `eclipse-temurin:21.0.2_13-jre-jammy` 镜像，仅包含运行应用程序所需的 Java 运行时环境 (JRE)。此镜像提供了一个 Java 运行时环境 (JRE)，足以运行编译后的应用程序（JAR 文件）。

    
   > 对于生产使用，强烈建议您使用 jlink 生成自定义的 JRE 类运行时。所有版本的 Eclipse Temurin 都提供 JRE 镜像，但 `jlink` 允许您创建一个仅包含应用程序所需必要 Java 模块的最小运行时。这可以显著减小最终镜像的大小并提高其安全性。[请参阅此页面](https://hub.docker.com/_/eclipse-temurin) 以获取更多信息。

   通过多阶段构建，Docker 构建使用一个基础镜像进行编译、打包和单元测试，然后使用另一个单独的镜像用于应用程序运行时。因此，最终镜像的体积更小，因为它不包含任何开发或调试工具。通过将构建环境与最终运行环境分离，您可以显著减小镜像体积并提高最终镜像的安全性。

 2. 现在，重新构建您的镜像并运行您准备使用的生产构建。

    ```console
    $ docker build -t spring-helloworld-builder .
    ```

    此命令使用您当前目录中 `Dockerfile` 文件的最终阶段构建一个名为 `spring-helloworld-builder` 的 Docker 镜像。

     > [!NOTE]
     >
     > 在您的多阶段 Dockerfile 中，最终阶段 (final) 是构建的默认目标。这意味着如果您没有在 `docker build` 命令中使用 `--target` 标志明确指定目标阶段，Docker 将默认构建最后一个阶段。您可以使用 `docker build -t spring-helloworld-builder --target builder .` 来仅构建包含 JDK 环境的 builder 阶段。

 3. 使用 `docker images` 命令查看镜像大小的差异：

    ```console
    $ docker images
    ```

    您将得到类似以下的输出：

    ```console
    spring-helloworld-builder latest    c5c76cb815c0   24 minutes ago      428MB
    spring-helloworld         latest    ff708d5ee194   About an hour ago   880MB
    ```

    您的最终镜像只有 428 MB，而原始构建大小为 880 MB。

    通过优化每个阶段并仅包含必要的内容，您能够在实现相同功能的同时显著减小整体镜像体积。这不仅提高了性能，还使您的 Docker 镜像更轻量、更安全、更易于管理。

## 其他资源

* [多阶段构建](/build/building/multi-stage/)
* [Dockerfile 最佳实践](/develop/develop-images/dockerfile_best-practices/)
* [基础镜像](/build/building/base-images/)
* [Spring Boot Docker](https://spring.io/guides/topicals/spring-boot-docker)