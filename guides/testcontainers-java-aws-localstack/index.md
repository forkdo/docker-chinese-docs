# 使用 LocalStack 测试 AWS 服务集成



<!-- Source: https://github.com/testcontainers/tc-guide-testing-aws-service-integrations-using-localstack -->

在本指南中，你将学习如何：

- 创建一个集成 Spring Cloud AWS 的 Spring Boot 应用
- 使用 AWS S3 和 SQS 服务
- 使用 Testcontainers 和 LocalStack 测试该应用

## 先决条件

- Java 17+
- Maven 或 Gradle
- Testcontainers 支持的 Docker 环境

> [!NOTE]
> 如果你是 Testcontainers 的新手，请访问
> [Testcontainers 概览](https://testcontainers.com/getting-started/) 以了解更多关于
> Testcontainers 及其优势的信息。

## 创建 Spring Boot 项目

### 设置项目

从 [Spring Initializr](https://start.spring.io) 创建一个 Spring Boot 项目，选择 **Testcontainers** starter。Spring Cloud AWS starter 在 Spring Initializr 上不可用，因此你需要手动添加它们。

或者，克隆
[指南仓库](https://github.com/testcontainers/tc-guide-testing-aws-service-integrations-using-localstack)。

将 Spring Cloud AWS BOM 添加到依赖管理，并将 S3、SQS starter 作为依赖添加。Testcontainers 提供了一个用于测试 AWS 服务集成的
[LocalStack 模块](https://testcontainers.com/modules/localstack/)。你还需要
[Awaitility](http://www.awaitility.org/) 来测试异步的 SQS 处理。

`pom.xml` 中的关键依赖如下：

```xml
<properties>
    <java.version>17</java.version>
    <testcontainers.version>2.0.4</testcontainers.version>
    <awspring.version>3.0.3</awspring.version>
</properties>

<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
    <dependency>
        <groupId>io.awspring.cloud</groupId>
        <artifactId>spring-cloud-aws-starter-s3</artifactId>
    </dependency>
    <dependency>
        <groupId>io.awspring.cloud</groupId>
        <artifactId>spring-cloud-aws-starter-sqs</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-test</artifactId>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-testcontainers</artifactId>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.testcontainers</groupId>
        <artifactId>testcontainers-junit-jupiter</artifactId>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.testcontainers</groupId>
        <artifactId>testcontainers-localstack</artifactId>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.awaitility</groupId>
        <artifactId>awaitility</artifactId>
        <scope>test</scope>
    </dependency>
</dependencies>

<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>io.awspring.cloud</groupId>
            <artifactId>spring-cloud-aws-dependencies</artifactId>
            <version>${awspring.version}</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>
```

### 创建配置属性

为了让 SQS 队列和 S3 桶名称可配置，创建一个 `ApplicationProperties` 记录：

```java
package com.testcontainers.demo;

import org.springframework.boot.context.properties.ConfigurationProperties;

@ConfigurationProperties(prefix = "app")
public record ApplicationProperties(String queue, String bucket) {}
```

然后向主应用类添加 `@ConfigurationPropertiesScan`，以便 Spring 自动扫描带有 `@ConfigurationProperties` 注解的类并将其注册为 bean：

```java
package com.testcontainers.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.context.properties.ConfigurationPropertiesScan;

@SpringBootApplication
@ConfigurationPropertiesScan
public class Application {

  public static void main(String[] args) {
    SpringApplication.run(Application.class, args);
  }
}
```

### 为 S3 实现 StorageService

Spring Cloud AWS 提供了更高层次的抽象，例如带有上传和下载文件便捷方法的 `S3Template`。创建一个 `StorageService` 类：

```java
package com.testcontainers.demo;

import io.awspring.cloud.s3.S3Template;
import java.io.IOException;
import java.io.InputStream;
import org.springframework.stereotype.Service;

@Service
public class StorageService {

  private final S3Template s3Template;

  public StorageService(S3Template s3Template) {
    this.s3Template = s3Template;
  }

  public void upload(String bucketName, String key, InputStream stream) {
    this.s3Template.upload(bucketName, key, stream);
  }

  public InputStream download(String bucketName, String key)
    throws IOException {
    return this.s3Template.download(bucketName, key).getInputStream();
  }

  public String downloadAsString(String bucketName, String key)
    throws IOException {
    try (InputStream is = this.download(bucketName, key)) {
      return new String(is.readAllBytes());
    }
  }
}
```

### 创建 SQS 消息模型

创建一个 `Message` 记录，表示你发送到 SQS 队列的负载：

```java
package com.testcontainers.demo;

import java.util.UUID;

public record Message(UUID uuid, String content) {}
```

### 实现消息发送者

创建 `MessageSender`，它使用 `SqsTemplate` 发布消息：

```java
package com.testcontainers.demo;

import io.awspring.cloud.sqs.operations.SqsTemplate;
import org.springframework.stereotype.Service;

@Service
public class MessageSender {

  private final SqsTemplate sqsTemplate;

  public MessageSender(SqsTemplate sqsTemplate) {
    this.sqsTemplate = sqsTemplate;
  }

  public void publish(String queueName, Message message) {
    sqsTemplate.send(to -> to.queue(queueName).payload(message));
  }
}
```

### 实现消息监听器

创建带有 `@SqsListener` 注解的处理方法的 `MessageListener`。当消息到达时，监听器使用消息 UUID 作为键，将内容上传到 S3 桶：

```java
package com.testcontainers.demo;

import io.awspring.cloud.sqs.annotation.SqsListener;
import java.io.ByteArrayInputStream;
import java.nio.charset.StandardCharsets;
import org.springframework.stereotype.Service;

@Service
public class MessageListener {

  private final StorageService storageService;
  private final ApplicationProperties properties;

  public MessageListener(
    StorageService storageService,
    ApplicationProperties properties
  ) {
    this.storageService = storageService;
    this.properties = properties;
  }

  @SqsListener(queueNames = { "${app.queue}" })
  public void handle(Message message) {
    String bucketName = this.properties.bucket();
    String key = message.uuid().toString();
    ByteArrayInputStream is = new ByteArrayInputStream(
      message.content().getBytes(StandardCharsets.UTF_8)
    );
    this.storageService.upload(bucketName, key, is);
  }
}
```

`${app.queue}` 表达式从应用配置中读取队列名称，而不是硬编码。

## 使用 Testcontainers 编写测试

要测试该应用，你需要一个运行中的 LocalStack 实例来模拟 AWS S3 和 SQS 服务。Testcontainers 在 Docker 容器中启动 LocalStack，`@DynamicPropertySource` 将其连接到 Spring Cloud AWS。

### 配置测试容器

你可以启动一个 LocalStack 容器，并配置 Spring Cloud AWS 属性来与它通信，而不是与真实的 AWS 服务通信。你需要设置的属性包括：

```properties
spring.cloud.aws.s3.endpoint=http://localhost:4566
spring.cloud.aws.sqs.endpoint=http://localhost:4566
spring.cloud.aws.credentials.access-key=noop
spring.cloud.aws.credentials.secret-key=noop
spring.cloud.aws.region.static=us-east-1
```

为了测试，使用一个在随机可用端口上启动的临时容器，这样你就可以在 CI 中并行运行多个构建而不会发生端口冲突。

### 编写测试

创建 `MessageListenerTest.java`：

```java
package com.testcontainers.demo;

import static org.assertj.core.api.Assertions.assertThat;
import static org.awaitility.Awaitility.await;
import static org.testcontainers.containers.localstack.LocalStackContainer.Service.S3;
import static org.testcontainers.containers.localstack.LocalStackContainer.Service.SQS;

import java.io.IOException;
import java.time.Duration;
import java.util.UUID;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.DynamicPropertyRegistry;
import org.springframework.test.context.DynamicPropertySource;
import org.testcontainers.containers.localstack.LocalStackContainer;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;
import org.testcontainers.utility.DockerImageName;

@SpringBootTest
@Testcontainers
class MessageListenerTest {

  @Container
  static LocalStackContainer localStack = new LocalStackContainer(
    DockerImageName.parse("localstack/localstack:3.0")
  );

  static final String BUCKET_NAME = UUID.randomUUID().toString();
  static final String QUEUE_NAME = UUID.randomUUID().toString();

  @DynamicPropertySource
  static void overrideProperties(DynamicPropertyRegistry registry) {
    registry.add("app.bucket", () -> BUCKET_NAME);
    registry.add("app.queue", () -> QUEUE_NAME);
    registry.add(
      "spring.cloud.aws.region.static",
      () -> localStack.getRegion()
    );
    registry.add(
      "spring.cloud.aws.credentials.access-key",
      () -> localStack.getAccessKey()
    );
    registry.add(
      "spring.cloud.aws.credentials.secret-key",
      () -> localStack.getSecretKey()
    );
    registry.add(
      "spring.cloud.aws.s3.endpoint",
      () -> localStack.getEndpointOverride(S3).toString()
    );
    registry.add(
      "spring.cloud.aws.sqs.endpoint",
      () -> localStack.getEndpointOverride(SQS).toString()
    );
  }

  @BeforeAll
  static void beforeAll() throws IOException, InterruptedException {
    localStack.execInContainer("awslocal", "s3", "mb", "s3://" + BUCKET_NAME);
    localStack.execInContainer(
      "awslocal",
      "sqs",
      "create-queue",
      "--queue-name",
      QUEUE_NAME
    );
  }

  @Autowired
  StorageService storageService;

  @Autowired
  MessageSender publisher;

  @Autowired
  ApplicationProperties properties;

  @Test
  void shouldHandleMessageSuccessfully() {
    Message message = new Message(UUID.randomUUID(), "Hello World");
    publisher.publish(properties.queue(), message);

    await()
      .pollInterval(Duration.ofSeconds(2))
      .atMost(Duration.ofSeconds(10))
      .ignoreExceptions()
      .untilAsserted(() -> {
        String msg = storageService.downloadAsString(
          properties.bucket(),
          message.uuid().toString()
        );
        assertThat(msg).isEqualTo("Hello World");
      });
  }
}
```

该测试的作用是：

- `@SpringBootTest` 启动完整的 Spring 应用上下文。
- Testcontainers 的 JUnit 5 注解 `@Testcontainers` 和 `@Container` 管理 `LocalStackContainer` 实例的生命周期。
- `@DynamicPropertySource` 从容器获取动态的 S3 和 SQS 端点 URL、区域、访问密钥和秘密密钥，并将它们注册为 Spring Cloud AWS 配置属性。
- `@BeforeAll` 使用 LocalStack Docker 镜像中预装的 `awslocal` CLI 工具创建所需的 SQS 队列和 S3 桶。`localStack.execInContainer()` API 在容器内运行命令。
- `shouldHandleMessageSuccessfully()` 向 SQS 队列发布一条 `Message`。监听器接收该消息，并以 UUID 作为键将其内容存储在 S3 桶中。Awaitility 最多等待 10 秒，直到预期内容出现在桶中。

## 运行测试与后续步骤

### 运行测试

```console
$ ./mvnw test
```

或者使用 Gradle：

```console
$ ./gradlew test
```

你应该会看到 LocalStack Docker 容器启动且测试通过。测试完成后，容器会停止并自动移除。

### 小结

LocalStack 让你在本地开发和测试基于 AWS 的应用。Testcontainers LocalStack 模块通过使用在随机端口上启动、无需外部设置的临时 LocalStack 容器，使编写集成测试变得简单直接。

要了解更多关于 Testcontainers 的信息，请访问
[Testcontainers 概览](https://testcontainers.com/getting-started/)。

### 延伸阅读

- [Testcontainers LocalStack 模块](https://java.testcontainers.org/modules/localstack/)
- [Testcontainers for Java 入门](https://java.testcontainers.org/quickstart/junit_5_quickstart/)
- [Spring Cloud AWS 文档](https://docs.awspring.io/spring-cloud-aws/docs/3.0.3/reference/html/index.html)

