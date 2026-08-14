# 

<!-- FILE: guides/testcontainers-java-mockserver.md -->

---
title: 使用 MockServer 测试 REST API 集成
linkTitle: MockServer
description: 了解如何使用 Testcontainers 的 MockServer 模块测试 Spring Boot 应用中的 REST API 集成。
keywords: testcontainers, java, spring boot, testing, mockserver, rest api, rest assured
summary: |
  了解如何创建一个与外部 REST API 集成的 Spring Boot 应用，然后使用 Testcontainers
  和 MockServer 对这些集成进行测试。
aliases:
  - /guides/testcontainers-java-mockserver/create-project/
  - /guides/testcontainers-java-mockserver/run-tests/
  - /guides/testcontainers-java-mockserver/write-tests/
params:
  tags: [testing]
  time: 20 minutes
---


<!-- Source: https://github.com/testcontainers/tc-guide-testing-rest-api-integrations-using-mockserver -->

在本指南中，你将学习如何：

- 创建一个与外部 REST API 通信的 Spring Boot 应用
- 使用 Testcontainers 的 MockServer 模块测试外部 API 集成

## 先决条件

- Java 17+
- Maven 或 Gradle
- 一个受 Testcontainers 支持的 Docker 环境

> [!NOTE]
> 如果你刚接触 Testcontainers，请访问
> [Testcontainers 概览](https://testcontainers.com/getting-started/) 了解
> Testcontainers 及其使用优势。

## 创建 Spring Boot 项目

### 搭建项目

在 [Spring Initializr](https://start.spring.io) 上创建一个 Spring Boot 项目，
添加 **Spring Web**、**Spring Reactive Web** 以及 **Testcontainers** 这几个 starter。

或者，克隆
[指南仓库](https://github.com/testcontainers/tc-guide-testing-rest-api-integrations-using-mockserver)。

生成项目后，添加 **REST Assured** 和 **MockServer** 库作为测试依赖。`pom.xml` 中的
关键依赖如下：

```xml
<properties>
    <java.version>17</java.version>
    <testcontainers.version>2.0.4</testcontainers.version>
</properties>
<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-webflux</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-test</artifactId>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.testcontainers</groupId>
        <artifactId>testcontainers-junit-jupiter</artifactId>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.testcontainers</groupId>
        <artifactId>testcontainers-mockserver</artifactId>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.mock-server</groupId>
        <artifactId>mockserver-netty</artifactId>
        <version>5.15.0</version>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>io.rest-assured</groupId>
        <artifactId>rest-assured</artifactId>
        <scope>test</scope>
    </dependency>
</dependencies>
```

建议使用 Testcontainers 的 BOM（Bill of Materials，物料清单），这样你无需为每个
Testcontainers 模块依赖重复指定版本。

本指南构建的是一个管理视频相册（album）的应用。相册中的照片资源由第三方 REST API
处理。出于演示目的，该应用使用公开可用的 [JSONPlaceholder](https://jsonplaceholder.typicode.com/)
API 作为照片服务。

该应用暴露一个 `GET /api/albums/{albumId}` 端点，它会调用照片服务以获取指定相册的
照片。[MockServer](https://www.mock-server.com/) 是一个用于 mock 基于 HTTP 的服务
的库。Testcontainers 提供了一个 [MockServer 模块](https://java.testcontainers.org/modules/mockserver/)，
能以 Docker 容器方式运行 MockServer。

### 创建 Album 和 Photo 模型

使用 Java record 创建 `Album.java`：

```java
package com.testcontainers.demo;

import java.util.List;

public record Album(Long albumId, List<Photo> photos) {}

record Photo(Long id, String title, String url, String thumbnailUrl) {}
```

### 创建 PhotoServiceClient 接口

Spring Framework 6 引入了[声明式 HTTP 客户端支持](https://docs.spring.io/spring-framework/reference/integration/rest-clients.html#rest-http-interface)。
创建一个接口，包含一个按相册 ID 获取照片的方法：

```java
package com.testcontainers.demo;

import java.util.List;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.service.annotation.GetExchange;

interface PhotoServiceClient {
  @GetExchange("/albums/{albumId}/photos")
  List<Photo> getPhotos(@PathVariable Long albumId);
}
```

### 将 PhotoServiceClient 注册为 bean

要生成 `PhotoServiceClient` 的运行时实现，需使用 `HttpServiceProxyFactory` 将其
注册为 Spring bean。该工厂需要一个 `HttpClientAdapter` 实现。Spring Boot 提供了
`WebClientAdapter` 作为 `spring-webflux` 库的一部分：

```java
package com.testcontainers.demo;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.web.reactive.function.client.support.WebClientAdapter;
import org.springframework.web.service.invoker.HttpServiceProxyFactory;

@Configuration
public class AppConfig {

  @Bean
  public PhotoServiceClient photoServiceClient(
    @Value("${photos.api.base-url}") String photosApiBaseUrl
  ) {
    WebClient client = WebClient.builder().baseUrl(photosApiBaseUrl).build();
    HttpServiceProxyFactory factory = HttpServiceProxyFactory
      .builder(WebClientAdapter.forClient(client))
      .build();
    return factory.createClient(PhotoServiceClient.class);
  }
}
```

照片服务的基础 URL 被外部化为一个配置属性。在 `src/main/resources/application.properties`
中添加以下条目：

```properties
photos.api.base-url=https://jsonplaceholder.typicode.com
```

### 创建 REST API 端点

创建 `AlbumController.java`：

```java
package com.testcontainers.demo;

import java.util.List;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.reactive.function.client.WebClientResponseException;

@RestController
@RequestMapping("/api")
class AlbumController {

  private static final Logger logger = LoggerFactory.getLogger(
    AlbumController.class
  );

  private final PhotoServiceClient photoServiceClient;

  AlbumController(PhotoServiceClient photoServiceClient) {
    this.photoServiceClient = photoServiceClient;
  }

  @GetMapping("/albums/{albumId}")
  public ResponseEntity<Album> getAlbumById(@PathVariable Long albumId) {
    try {
      List<Photo> photos = photoServiceClient.getPhotos(albumId);
      return ResponseEntity.ok(new Album(albumId, photos));
    } catch (WebClientResponseException e) {
      logger.error("Failed to get photos", e);
      return new ResponseEntity<>(e.getStatusCode());
    }
  }
}
```

该端点会针对给定的相册 ID 调用照片服务，并返回类似如下的响应：

```json
{
  "albumId": 1,
  "photos": [
    {
      "id": 51,
      "title": "non sunt voluptatem placeat consequuntur rem incidunt",
      "url": "https://via.placeholder.com/600/8e973b",
      "thumbnailUrl": "https://via.placeholder.com/150/8e973b"
    },
    {
      "id": 52,
      "title": "eveniet pariatur quia nobis reiciendis laboriosam ea",
      "url": "https://via.placeholder.com/600/121fa4",
      "thumbnailUrl": "https://via.placeholder.com/150/121fa4"
    }
  ]
}
```

## 使用 Testcontainers MockServer 编写测试

在 HTTP 协议层面（而非 mock Java 方法）来 mock 外部 API 的交互，让你可以验证序列化与
反序列化行为，并模拟网络故障。

Testcontainers 提供了一个 MockServer 模块，可在 Docker 容器内启动一个
[MockServer](https://www.mock-server.com/) 实例。然后你可以使用 `MockServerClient`
配置 mock 预期（expectation）。

### 编写测试

创建 `AlbumControllerTest.java`：

```java
package com.testcontainers.demo;

import static io.restassured.RestAssured.given;
import static org.hamcrest.CoreMatchers.is;
import static org.hamcrest.Matchers.hasSize;
import static org.mockserver.model.HttpRequest.request;
import static org.mockserver.model.HttpResponse.response;
import static org.mockserver.model.JsonBody.json;

import io.restassured.RestAssured;
import io.restassured.http.ContentType;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockserver.client.MockServerClient;
import org.mockserver.model.Header;
import org.mockserver.verify.VerificationTimes;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.server.LocalServerPort;
import org.springframework.test.context.DynamicPropertyRegistry;
import org.springframework.test.context.DynamicPropertySource;
import org.testcontainers.mockserver.MockServerContainer;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@Testcontainers
class AlbumControllerTest {

  @LocalServerPort
  private Integer port;

  @Container
  static MockServerContainer mockServerContainer =
    new MockServerContainer("mockserver/mockserver:5.15.0");

  static MockServerClient mockServerClient;

  @DynamicPropertySource
  static void overrideProperties(DynamicPropertyRegistry registry) {
    mockServerClient =
    new MockServerClient(
      mockServerContainer.getHost(),
      mockServerContainer.getServerPort()
    );
    registry.add("photos.api.base-url", mockServerContainer::getEndpoint);
  }

  @BeforeEach
  void setUp() {
    RestAssured.port = port;
    mockServerClient.reset();
  }

  @Test
  void shouldGetAlbumById() {
    Long albumId = 1L;

    mockServerClient
      .when(
        request().withMethod("GET").withPath("/albums/" + albumId + "/photos")
      )
      .respond(
        response()
          .withStatusCode(200)
          .withHeaders(
            new Header("Content-Type", "application/json; charset=utf-8")
          )
          .withBody(
            json(
              """
              [
                   {
                       "id": 1,
                       "title": "accusamus beatae ad facilis cum similique qui sunt",
                       "url": "https://via.placeholder.com/600/92c952",
                       "thumbnailUrl": "https://via.placeholder.com/150/92c952"
                   },
                   {
                       "id": 2,
                       "title": "reprehenderit est deserunt velit ipsam",
                       "url": "https://via.placeholder.com/600/771796",
                       "thumbnailUrl": "https://via.placeholder.com/150/771796"
                   }
               ]
              """
            )
          )
      );

    given()
      .contentType(ContentType.JSON)
      .when()
      .get("/api/albums/{albumId}", albumId)
      .then()
      .statusCode(200)
      .body("albumId", is(albumId.intValue()))
      .body("photos", hasSize(2));

    verifyMockServerRequest("GET", "/albums/" + albumId + "/photos", 1);
  }

  @Test
  void shouldReturn404StatusWhenAlbumNotFound() {
    Long albumId = 1L;
    mockServerClient
      .when(
        request().withMethod("GET").withPath("/albums/" + albumId + "/photos")
      )
      .respond(response().withStatusCode(404));

    given()
      .contentType(ContentType.JSON)
      .when()
      .get("/api/albums/{albumId}", albumId)
      .then()
      .statusCode(404);

    verifyMockServerRequest("GET", "/albums/" + albumId + "/photos", 1);
  }

  private void verifyMockServerRequest(String method, String path, int times) {
    mockServerClient.verify(
      request().withMethod(method).withPath(path),
      VerificationTimes.exactly(times)
    );
  }
}
```

该测试的作用如下：

- `@SpringBootTest` 在随机端口上启动完整的应用。
- `@Testcontainers` 与 `@Container` 注解启动一个 `MockServerContainer`，并创建连接到
  它的 `MockServerClient`。
- `@DynamicPropertySource` 覆盖 `photos.api.base-url`，使其指向 MockServer 端点，从而
  让应用与 MockServer 通信，而非真实的照片服务。
- `@BeforeEach` 在每个测试之前重置 `MockServerClient`，使一个测试的预期不会影响
  另一个测试。
- `shouldGetAlbumById()` 为 `/albums/{albumId}/photos` 配置一个 mock 响应，向应用的
  `/api/albums/{albumId}` 端点发送请求，并校验响应体。它还使用 `mockServerClient.verify()`
  确认预期的 API 调用确实到达了 MockServer。
- `shouldReturn404StatusWhenAlbumNotFound()` 配置 MockServer 返回 404 状态，并验证应用
  将该状态传播给调用方。

## 运行测试与后续步骤

### 运行测试

```console
$ ./mvnw test
```

或者使用 Gradle：

```console
$ ./gradlew test
```

你应该在控制台输出中看到 MockServer 的 Docker 容器启动。它充当照片服务，依据配置的
预期（expectation）返回 mock 响应。所有测试都应通过。

### 小结

你构建了一个使用声明式 HTTP 客户端与外部 REST API 集成的 Spring Boot 应用，然后使用
Testcontainers 的 MockServer 模块对该集成进行了测试。在 HTTP 协议层面而非 mock Java
方法层面进行测试，能让你发现序列化问题并模拟真实的故障场景。

想进一步了解 Testcontainers，请访问
[Testcontainers 概览](https://testcontainers.com/getting-started/)。

### 延伸阅读

- [Testcontainers MockServer 模块](https://java.testcontainers.org/modules/mockserver/)
- [MockServer 文档](https://www.mock-server.com/)
- [Testcontainers JUnit 5 快速入门](https://java.testcontainers.org/quickstart/junit_5_quickstart/)

