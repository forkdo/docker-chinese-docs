# Java


本示例展示如何将 Java 应用程序迁移到 Docker 强化镜像。

以下示例展示了迁移到 Docker 强化镜像前后的 Dockerfile。每个示例包含五种变体：

- 迁移前（Ubuntu）：使用基于 Ubuntu 的镜像的示例 Dockerfile，迁移到 DHI 之前
- 迁移前（Wolfi）：使用 Wolfi 发行版镜像的示例 Dockerfile，迁移到 DHI 之前
- 迁移前（DOI）：使用 Docker 官方镜像的示例 Dockerfile，迁移到 DHI 之前
- 迁移后（多阶段）：使用多阶段构建迁移到 DHI 后的示例 Dockerfile（推荐用于最小、安全的镜像）
- 迁移后（单阶段）：使用单阶段构建迁移到 DHI 后的示例 Dockerfile（更简单，但会导致镜像更大、攻击面更广）

> [!NOTE]
>
> 多阶段构建适用于大多数用例。单阶段构建出于简单性而受支持，但在大小和安全性方面存在权衡。
>
> 在拉取 Docker 强化镜像之前，您必须先向 `dhi.io` 进行身份验证。
> 使用您的 Docker ID 凭据（与您用于 Docker Hub 的用户名和密码相同）。如果您没有 Docker 账户，请[免费创建一个](../../../accounts/create-account.md)。
>
> 运行 `docker login dhi.io` 进行身份验证。

**Before (Ubuntu)**



```dockerfile
#syntax=docker/dockerfile:1

FROM ubuntu:24.04 AS builder

WORKDIR /app
COPY . ./

RUN apt-get update && apt-get install -y default-jdk maven --no-install-recommends && rm -rf /var/lib/apt/lists/*

RUN mvn -B package -DskipTests

FROM ubuntu:24.04

RUN apt-get update && apt-get install -y default-jre --no-install-recommends && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY --from=builder /app/target/app.jar /app/app.jar

ENTRYPOINT ["java", "-jar", "/app/app.jar"]
```

**Before (Wolfi)**



```dockerfile
#syntax=docker/dockerfile:1

FROM cgr.dev/chainguard/maven:latest-dev AS builder

WORKDIR /app
COPY . ./

# Install any additional packages if needed using apk
# RUN apk add --no-cache git

RUN mvn -B package -DskipTests

FROM cgr.dev/chainguard/jre:latest

WORKDIR /app
COPY --from=builder /app/target/app.jar /app/app.jar

ENTRYPOINT ["java", "-jar", "/app/app.jar"]
```

**Before (DOI)**



```dockerfile
#syntax=docker/dockerfile:1

FROM maven:3.9-eclipse-temurin-21 AS builder

WORKDIR /app
COPY . ./

# Install any additional packages if needed using apt
# RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

RUN mvn -B package -DskipTests

FROM eclipse-temurin:21-jre

WORKDIR /app
COPY --from=builder /app/target/app.jar /app/app.jar

ENTRYPOINT ["java", "-jar", "/app/app.jar"]
```

**After (multi-stage)**



```dockerfile
#syntax=docker/dockerfile:1

# === Build stage: Compile and package the Java application with Maven ===
FROM dhi.io/maven:3-jdk21-alpine3.22-dev AS builder

WORKDIR /app
COPY . ./

# Install any additional packages if needed using apk
# RUN apk add --no-cache git

RUN mvn -B package -DskipTests

# === Final stage: Create minimal runtime image ===
FROM dhi.io/eclipse-temurin:21-alpine3.22

WORKDIR /app
COPY --from=builder /app/target/app.jar /app/app.jar

ENTRYPOINT ["java", "-jar", "/app/app.jar"]
```

**After (single-stage)**



```dockerfile
#syntax=docker/dockerfile:1

FROM dhi.io/maven:3-jdk21-alpine3.22-dev

WORKDIR /app
COPY . ./

# Install any additional packages if needed using apk
# RUN apk add --no-cache git

RUN mvn -B package -DskipTests

ENTRYPOINT ["java", "-jar", "/app/target/app.jar"]
```



