<!-- FILE: guides/testcontainers-java-service-configuration.md -->

---
title: 配置在容器中运行的服务
linkTitle: 服务配置（Java）
description: 了解如何通过复制文件以及在容器内执行命令来配置 Testcontainers 中运行的服务。
keywords: testcontainers, java, testing, postgresql, localstack, container configuration
summary: |
  了解如何通过向容器复制文件以及在容器内执行命令，来初始化并配置用于测试的
  Docker 容器。
aliases:
  - /guides/testcontainers-java-service-configuration/copy-files/
  - /guides/testcontainers-java-service-configuration/exec-in-container/
params:
  tags: [testing]
  time: 15 minutes
---


<!-- Source: https://github.com/testcontainers/tc-guide-configuration-of-services-running-in-container -->

在本指南中，你将学习如何：

- 通过向容器复制文件来初始化容器
- 使用 `execInContainer()` 在运行中的容器内执行命令
- 使用 SQL 脚本搭建 PostgreSQL 数据库
- 在 LocalStack 容器中创建 AWS S3 存储桶

## 先决条件

- Java 17+
- 你偏好的 IDE
- 一个受 Testcontainers 支持的 Docker 环境

> [!NOTE]
> 如果你刚接触 Testcontainers，请访问
> [Testcontainers 概览](https://testcontainers.com/getting-started/) 了解
> Testcontainers 及其使用优势。

## 向容器复制文件

有时你需要将文件放到特定位置来初始化容器。例如，PostgreSQL 会在容器启动时从
`/docker-entrypoint-initdb.d/` 目录运行 SQL 脚本。

### 创建初始化脚本

创建 `src/test/resources/init-db.sql`：

```sql
create table customers (
     id bigint not null,
     name varchar not null,
     primary key (id)
);
```

### 将文件复制到容器

使用 `withCopyFileToContainer()` 将 SQL 脚本复制到容器的初始化目录：

```java
package com.testcontainers.demo;

import static org.junit.jupiter.api.Assertions.assertFalse;

import java.util.List;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.testcontainers.postgresql.PostgreSQLContainer;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;
import org.testcontainers.utility.MountableFile;

@Testcontainers
class CustomerServiceTest {

  @Container
  static PostgreSQLContainer postgres = new PostgreSQLContainer(
    "postgres:16-alpine"
  )
    .withCopyFileToContainer(
      MountableFile.forClasspathResource("init-db.sql"),
      "/docker-entrypoint-initdb.d/"
    );

  CustomerService customerService;

  @BeforeEach
  void setUp() {
    customerService =
    new CustomerService(
      postgres.getJdbcUrl(),
      postgres.getUsername(),
      postgres.getPassword()
    );
  }

  @Test
  void shouldGetCustomers() {
    customerService.createCustomer(new Customer(1L, "George"));
    customerService.createCustomer(new Customer(2L, "John"));

    List<Customer> customers = customerService.getAllCustomers();
    assertFalse(customers.isEmpty());
  }
}
```

`withCopyFileToContainer(MountableFile, String)` 方法将 `init-db.sql` 从 classpath 复制到
容器内的 `/docker-entrypoint-initdb.d/`。PostgreSQL 会在启动时自动执行该目录下的脚本。

你也可以从宿主机的任意路径复制文件：

```java
.withCopyFileToContainer(
    MountableFile.forHostPath("/host/path/to/init-db.sql"),
    "/docker-entrypoint-initdb.d/"
);
```

## 在容器内执行命令

一些 Docker 容器提供了用于执行操作的 CLI 工具。你可以使用
`container.execInContainer(String...)` 在运行中的容器内执行任何可用的命令。

### 示例：在 LocalStack 中创建 S3 存储桶

[LocalStack](https://localstack.cloud/) 模块用于模拟 AWS 服务。要测试 S3 文件上传，可
在运行测试之前创建一个存储桶：

```java
package com.testcontainers.demo;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.testcontainers.containers.localstack.LocalStackContainer.Service.S3;

import java.io.IOException;
import java.net.URI;
import java.util.List;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;
import org.testcontainers.containers.localstack.LocalStackContainer;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;
import org.testcontainers.utility.DockerImageName;
import software.amazon.awssdk.auth.credentials.AwsBasicCredentials;
import software.amazon.awssdk.auth.credentials.StaticCredentialsProvider;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.s3.S3Client;
import software.amazon.awssdk.services.s3.model.Bucket;

@Testcontainers
class LocalStackTest {

  static final String bucketName = "mybucket";

  @Container
  static LocalStackContainer localStack = new LocalStackContainer(
    DockerImageName.parse("localstack/localstack:3.4.0")
  );

  @BeforeAll
  static void beforeAll() throws IOException, InterruptedException {
    localStack.execInContainer("awslocal", "s3", "mb", "s3://" + bucketName);

    org.testcontainers.containers.Container.ExecResult execResult =
      localStack.execInContainer("awslocal", "s3", "ls");
    String stdout = execResult.getStdout();
    int exitCode = execResult.getExitCode();
    assertTrue(stdout.contains(bucketName));
    assertEquals(0, exitCode);
  }

  @Test
  void shouldListBuckets() {
    URI s3Endpoint = localStack.getEndpointOverride(S3);
    StaticCredentialsProvider credentialsProvider =
      StaticCredentialsProvider.create(
        AwsBasicCredentials.create(
          localStack.getAccessKey(),
          localStack.getSecretKey()
        )
      );
    S3Client s3 = S3Client
      .builder()
      .endpointOverride(s3Endpoint)
      .credentialsProvider(credentialsProvider)
      .region(Region.of(localStack.getRegion()))
      .build();

    List<String> s3Buckets = s3
      .listBuckets()
      .buckets()
      .stream()
      .map(Bucket::name)
      .toList();

    assertTrue(s3Buckets.contains(bucketName));
  }
}
```

`execInContainer("awslocal", "s3", "mb", "s3://mybucket")` 调用会运行 `awslocal` CLI 工具
（由 LocalStack 镜像提供）来创建一个 S3 存储桶。

你可以捕获任何命令的输出和退出码：

```java
Container.ExecResult execResult =
    localStack.execInContainer("awslocal", "s3", "ls");
String stdout = execResult.getStdout();
int exitCode = execResult.getExitCode();
```

> [!NOTE]
> `withCopyFileToContainer()` 和 `execInContainer()` 方法继承自 `GenericContainer`，因此它们
> 对所有 Testcontainers 模块都可用。

### 小结

- 使用 `withCopyFileToContainer()` 在容器启动前将初始化文件放入其中。
- 使用 `execInContainer()` 在运行中的容器内执行命令，完成创建存储桶、主题或队列等初始化
  任务。

### 延伸阅读

- [Java Testcontainers 入门](/guides/testcontainers-java-getting-started/)
- [Testcontainers Postgres 模块](https://java.testcontainers.org/modules/databases/postgres/)
- [Testcontainers LocalStack 模块](https://java.testcontainers.org/modules/localstack/)
