# 

<!-- FILE: guides/testcontainers-java-wiremock.md -->

---
title: 使用 WireMock 测试 REST API 集成
linkTitle: WireMock
description: 了解如何使用 Testcontainers WireMock 模块测试 Spring Boot 应用中的 REST API 集成。
keywords: testcontainers, java, spring boot, testing, wiremock, rest api, rest assured
summary: |
  了解如何创建一个与外部 REST API 集成的 Spring Boot 应用，
  然后使用 Testcontainers 和 WireMock 测试这些集成。
aliases:
  - /guides/testcontainers-java-wiremock/create-project/
  - /guides/testcontainers-java-wiremock/run-tests/
  - /guides/testcontainers-java-wiremock/write-tests/
params:
  tags: [testing]
  time: 20 minutes
---


<!-- Source: https://github.com/testcontainers/tc-guide-testing-rest-api-integrations-using-wiremock -->

在本指南中，你将学习如何：

- 创建一个与外部 REST API 通信的 Spring Boot 应用
- 同时使用 JUnit 5 扩展和 Testcontainers WireMock 模块，通过 WireMock 测试外部 API 集成

## 先决条件

- Java 17+
- Maven 或 Gradle
- Testcontainers 支持的 Docker 环境

> [!NOTE]
> 如果你是 Testcontainers 的新手，请访问
> [Testcontainers 概览](https://testcontainers.com/getting-started/) 进一步了解
> Testcontainers 及其使用优势。

## 创建 Spring Boot 项目

### 搭建项目

从 [Spring Initializr](https://start.spring.io) 创建一个 Spring Boot 项目，
选择 **Spring Web** 和 **Testcontainers** 这两个 starter。

或者，克隆
[指南仓库](https://github.com/testcontainers/tc-guide-testing-rest-api-integrations-using-wiremock)。

生成项目后，将 **REST Assured**、**WireMock** 和
**WireMock Testcontainers 模块** 作为测试依赖添加进来。`pom.xml` 中的关键
依赖如下：

```xml
<properties>
    <java.version>17</java.version>
    <testcontainers.version>2.0.4</testcontainers.version>
    <wiremock-testcontainers.version>1.0-alpha-13</wiremock-testcontainers.version>
</properties>
<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
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
        <groupId>org.wiremock</groupId>
        <artifactId>wiremock-standalone</artifactId>
        <version>3.6.0</version>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.wiremock.integrations.testcontainers</groupId>
        <artifactId>wiremock-testcontainers-module</artifactId>
        <version>${wiremock-testcontainers.version}</version>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>io.rest-assured</groupId>
        <artifactId>rest-assured</artifactId>
        <scope>test</scope>
    </dependency>
</dependencies>
```

建议使用 Testcontainers BOM（Bill of Materials，物料清单），这样就无需为每个
Testcontainers 模块依赖重复声明版本。

本指南构建的应用用于管理视频相册。一个第三方 REST API 负责处理照片资源。
出于演示目的，应用使用公开可用的 [JSONPlaceholder](https://jsonplaceholder.typicode.com/) API
作为照片服务。

该应用暴露一个 `GET /api/albums/{albumId}` 接口，调用照片服务来获取指定相册的照片。
[WireMock](https://wiremock.org/) 是一款用于构建模拟 API 的工具。
Testcontainers 提供了一个
[WireMock 模块](https://testcontainers.com/modules/wiremock/)，可将
WireMock 作为 Docker 容器运行。

### 创建 Album 和 Photo 模型

使用 Java 记录（record）创建 `Album.java`：

```java
package com.testcontainers.demo;

import java.util.List;

public record Album(Long albumId, List<Photo> photos) {}

record Photo(Long id, String title, String url, String thumbnailUrl) {}
```

### 创建 PhotoServiceClient

创建 `PhotoServiceClient.java`，它使用 `RestTemplate` 来获取指定相册 ID 的照片：

```java
package com.testcontainers.demo;

import java.util.List;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

@Service
class PhotoServiceClient {

  private final String baseUrl;
  private final RestTemplate restTemplate;

  PhotoServiceClient(
    @Value("${photos.api.base-url}") String baseUrl,
    RestTemplateBuilder builder
  ) {
    this.baseUrl = baseUrl;
    this.restTemplate = builder.build();
  }

  List<Photo> getPhotos(Long albumId) {
    String url = baseUrl + "/albums/{albumId}/photos";
    ResponseEntity<List<Photo>> response = restTemplate.exchange(
      url,
      HttpMethod.GET,
      null,
      new ParameterizedTypeReference<>() {},
      albumId
    );
    return response.getBody();
  }
}
```

照片服务的 base URL 被外部化为一个配置属性。在 `src/main/resources/application.properties`
中添加以下内容：

```properties
photos.api.base-url=https://jsonplaceholder.typicode.com
```

### 创建 REST API 接口

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
import org.springframework.web.client.RestClientResponseException;

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
    } catch (RestClientResponseException e) {
      logger.error("Failed to get photos", e);
      return new ResponseEntity<>(e.getStatusCode());
    }
  }
}
```

该接口会调用照片服务获取指定相册 ID 的照片，并返回类似如下的响应：

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

## 使用 WireMock 和 Testcontainers 编写测试

在 HTTP 协议层面模拟外部 API 交互（而非模拟 Java 方法），可以让你验证编解码（marshalling/unmarshalling）行为并模拟网络问题。

### 使用 WireMock JUnit 5 扩展进行测试

WireMock 提供了一个 JUnit 5 扩展，可启动一个进程内（in-process）的 WireMock 服务器。
你可以使用 WireMock Java API 配置桩（stub）响应。

创建 `AlbumControllerTest.java`：

```java
package com.testcontainers.demo;

import static com.github.tomakehurst.wiremock.client.WireMock.aResponse;
import static com.github.tomakehurst.wiremock.client.WireMock.urlMatching;
import static com.github.tomakehurst.wiremock.core.WireMockConfiguration.wireMockConfig;
import static io.restassured.RestAssured.given;
import static org.hamcrest.CoreMatchers.is;
import static org.hamcrest.Matchers.hasSize;
import static org.springframework.boot.test.context.SpringBootTest.WebEnvironment.RANDOM_PORT;

import com.github.tomakehurst.wiremock.client.WireMock;
import com.github.tomakehurst.wiremock.junit5.WireMockExtension;
import io.restassured.RestAssured;
import io.restassured.http.ContentType;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.RegisterExtension;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.server.LocalServerPort;
import org.springframework.http.MediaType;
import org.springframework.test.context.DynamicPropertyRegistry;
import org.springframework.test.context.DynamicPropertySource;

@SpringBootTest(webEnvironment = RANDOM_PORT)
class AlbumControllerTest {

  @LocalServerPort
  private Integer port;

  @RegisterExtension
  static WireMockExtension wireMock = WireMockExtension
    .newInstance()
    .options(wireMockConfig().dynamicPort())
    .build();

  @DynamicPropertySource
  static void configureProperties(DynamicPropertyRegistry registry) {
    registry.add("photos.api.base-url", wireMock::baseUrl);
  }

  @BeforeEach
  void setUp() {
    RestAssured.port = port;
  }

  @Test
  void shouldGetAlbumById() {
    Long albumId = 1L;

    wireMock.stubFor(
      WireMock
        .get(urlMatching("/albums/" + albumId + "/photos"))
        .willReturn(
          aResponse()
            .withHeader("Content-Type", MediaType.APPLICATION_JSON_VALUE)
            .withBody(
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
  }

  @Test
  void shouldReturnServerErrorWhenPhotoServiceCallFailed() {
    Long albumId = 2L;
    wireMock.stubFor(
      WireMock
        .get(urlMatching("/albums/" + albumId + "/photos"))
        .willReturn(aResponse().withStatus(500))
    );

    given()
      .contentType(ContentType.JSON)
      .when()
      .get("/api/albums/{albumId}", albumId)
      .then()
      .statusCode(500);
  }
}
```

该测试的工作方式如下：

- `@SpringBootTest` 在随机端口上启动完整的应用。
- `@RegisterExtension` 创建一个 `WireMockExtension`，在动态端口上启动 WireMock。
- `@DynamicPropertySource` 覆写 `photos.api.base-url`，使其指向
  WireMock 端点，这样应用就会与 WireMock 通信，而不是真实的照片服务。
- `shouldGetAlbumById()` 为 `/albums/{albumId}/photos` 配置桩响应，
  向应用的 `/api/albums/{albumId}` 接口发送请求，并验证响应体。
- `shouldReturnServerErrorWhenPhotoServiceCallFailed()` 配置 WireMock
  返回 500 状态码，并验证应用将该状态码传递给调用方。

### 使用 JSON 映射文件配置桩

除了使用 WireMock Java API，你还可以使用 JSON 映射文件配置桩。创建
`src/test/resources/wiremock/mappings/get-album-photos.json`：

```json
{
  "mappings": [
    {
      "request": {
        "method": "GET",
        "urlPattern": "/albums/([0-9]+)/photos"
      },
      "response": {
        "status": 200,
        "headers": {
          "Content-Type": "application/json"
        },
        "bodyFileName": "album-photos-resp-200.json"
      }
    },
    {
      "request": {
        "method": "GET",
        "urlPattern": "/albums/2/photos"
      },
      "response": {
        "status": 500,
        "headers": {
          "Content-Type": "application/json"
        }
      }
    },
    {
      "request": {
        "method": "GET",
        "urlPattern": "/albums/3/photos"
      },
      "response": {
        "status": 200,
        "headers": {
          "Content-Type": "application/json"
        },
        "jsonBody": []
      }
    }
  ]
}
```

在 `src/test/resources/wiremock/__files/album-photos-resp-200.json` 创建响应体文件：

```json
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
```

初始化 WireMock 以从映射文件加载桩：

```java
@RegisterExtension
static WireMockExtension wireMockServer = WireMockExtension
  .newInstance()
  .options(
    wireMockConfig().dynamicPort().usingFilesUnderClasspath("wiremock")
  )
  .build();
```

配置好基于映射的桩后，创建 `AlbumControllerWireMockMappingTests.java`：

```java
package com.testcontainers.demo;

import static com.github.tomakehurst.wiremock.core.WireMockConfiguration.wireMockConfig;
import static io.restassured.RestAssured.given;
import static org.hamcrest.CoreMatchers.is;
import static org.hamcrest.Matchers.hasSize;
import static org.springframework.boot.test.context.SpringBootTest.WebEnvironment.RANDOM_PORT;

import com.github.tomakehurst.wiremock.junit5.WireMockExtension;
import io.restassured.RestAssured;
import io.restassured.http.ContentType;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.RegisterExtension;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.server.LocalServerPort;
import org.springframework.test.context.DynamicPropertyRegistry;
import org.springframework.test.context.DynamicPropertySource;

@SpringBootTest(webEnvironment = RANDOM_PORT)
class AlbumControllerWireMockMappingTests {

  @LocalServerPort
  private Integer port;

  @RegisterExtension
  static WireMockExtension wireMockServer = WireMockExtension
    .newInstance()
    .options(
      wireMockConfig().dynamicPort().usingFilesUnderClasspath("wiremock")
    )
    .build();

  @DynamicPropertySource
  static void configureProperties(DynamicPropertyRegistry registry) {
    registry.add("photos.api.base-url", wireMockServer::baseUrl);
  }

  @BeforeEach
  void setUp() {
    RestAssured.port = port;
  }

  @Test
  void shouldGetAlbumById() {
    Long albumId = 1L;

    given()
      .contentType(ContentType.JSON)
      .when()
      .get("/api/albums/{albumId}", albumId)
      .then()
      .statusCode(200)
      .body("albumId", is(albumId.intValue()))
      .body("photos", hasSize(2));
  }

  @Test
  void shouldReturnServerErrorWhenPhotoServiceCallFailed() {
    Long albumId = 2L;

    given()
      .contentType(ContentType.JSON)
      .when()
      .get("/api/albums/{albumId}", albumId)
      .then()
      .statusCode(500);
  }

  @Test
  void shouldReturnEmptyPhotos() {
    Long albumId = 3L;

    given()
      .contentType(ContentType.JSON)
      .when()
      .get("/api/albums/{albumId}", albumId)
      .then()
      .statusCode(200)
      .body("albumId", is(albumId.intValue()))
      .body("photos", hasSize(0));
  }
}
```

这些测试不需要内联的桩定义，因为 WireMock 会自动从 classpath 加载映射。

### 使用 Testcontainers WireMock 模块进行测试

[Testcontainers WireMock 模块](https://testcontainers.com/modules/wiremock/)
基于 [WireMock Docker](https://github.com/wiremock/wiremock-docker)，将 WireMock
作为独立的 Docker 容器来提供。当你希望测试 JVM 与模拟服务器之间完全隔离时，这种方式很有用。

在 `src/test/resources/com/testcontainers/demo/AlbumControllerTestcontainersTests/mocks-config.json`
创建模拟配置文件：

```json
{
  "mappings": [
    {
      "request": {
        "method": "GET",
        "urlPattern": "/albums/([0-9]+)/photos"
      },
      "response": {
        "status": 200,
        "headers": {
          "Content-Type": "application/json"
        },
        "bodyFileName": "album-photos-response.json"
      }
    },
    {
      "request": {
        "method": "GET",
        "urlPattern": "/albums/2/photos"
      },
      "response": {
        "status": 500,
        "headers": {
          "Content-Type": "application/json"
        }
      }
    },
    {
      "request": {
        "method": "GET",
        "urlPattern": "/albums/3/photos"
      },
      "response": {
        "status": 200,
        "headers": {
          "Content-Type": "application/json"
        },
        "jsonBody": []
      }
    }
  ]
}
```

在 `src/test/resources/com/testcontainers/demo/AlbumControllerTestcontainersTests/album-photos-response.json`
创建响应体文件：

```json
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
```

创建 `AlbumControllerTestcontainersTests.java`：

```java
package com.testcontainers.demo;

import static io.restassured.RestAssured.given;
import static org.hamcrest.CoreMatchers.is;
import static org.hamcrest.Matchers.hasSize;
import static org.springframework.boot.test.context.SpringBootTest.WebEnvironment.RANDOM_PORT;

import io.restassured.RestAssured;
import io.restassured.http.ContentType;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.server.LocalServerPort;
import org.springframework.test.context.DynamicPropertyRegistry;
import org.springframework.test.context.DynamicPropertySource;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;
import org.wiremock.integrations.testcontainers.WireMockContainer;

@SpringBootTest(webEnvironment = RANDOM_PORT)
@Testcontainers
class AlbumControllerTestcontainersTests {

  @LocalServerPort
  private Integer port;

  @Container
  static WireMockContainer wiremockServer = new WireMockContainer(
    "wiremock/wiremock:3.6.0"
  )
    .withMapping(
      "photos-by-album",
      AlbumControllerTestcontainersTests.class,
      "mocks-config.json"
    )
    .withFileFromResource(
      "album-photos-response.json",
      AlbumControllerTestcontainersTests.class,
      "album-photos-response.json"
    );

  @DynamicPropertySource
  static void configureProperties(DynamicPropertyRegistry registry) {
    registry.add("photos.api.base-url", wiremockServer::getBaseUrl);
  }

  @BeforeEach
  void setUp() {
    RestAssured.port = port;
  }

  @Test
  void shouldGetAlbumById() {
    Long albumId = 1L;

    given()
      .contentType(ContentType.JSON)
      .when()
      .get("/api/albums/{albumId}", albumId)
      .then()
      .statusCode(200)
      .body("albumId", is(albumId.intValue()))
      .body("photos", hasSize(2));
  }

  @Test
  void shouldReturnServerErrorWhenPhotoServiceCallFailed() {
    Long albumId = 2L;

    given()
      .contentType(ContentType.JSON)
      .when()
      .get("/api/albums/{albumId}", albumId)
      .then()
      .statusCode(500);
  }

  @Test
  void shouldReturnEmptyPhotos() {
    Long albumId = 3L;

    given()
      .contentType(ContentType.JSON)
      .when()
      .get("/api/albums/{albumId}", albumId)
      .then()
      .statusCode(200)
      .body("albumId", is(albumId.intValue()))
      .body("photos", hasSize(0));
  }
}
```

该测试的工作方式如下：

- `@Testcontainers` 和 `@Container` 注解使用 `wiremock/wiremock:3.6.0` Docker 镜像启动一个
  `WireMockContainer`。
- `withMapping()` 从 `mocks-config.json` 加载桩映射，
  `withFileFromResource()` 加载响应体文件。
- `@DynamicPropertySource` 覆写 `photos.api.base-url`，使其指向
  WireMock 容器的 base URL。
- 测试不包含内联桩定义，因为 WireMock 会从 JSON 配置文件加载它们。

## 运行测试及后续步骤

### 运行测试

```console
$ ./mvnw test
```

或者使用 Gradle：

```console
$ ./gradlew test
```

你应该会在控制台输出中看到 WireMock Docker 容器启动。它充当照片服务，根据配置的
期望（expectations）提供模拟响应。所有测试都应通过。

### 小结

你构建了一个与外部 REST API 集成的 Spring Boot 应用，然后使用三种不同的方法测试了该集成：

- 使用内联桩的 WireMock JUnit 5 扩展
- 使用 JSON 映射文件的 WireMock JUnit 5 扩展
- 在 Docker 容器中运行 WireMock 的 Testcontainers WireMock 模块

在 HTTP 协议层面而非模拟 Java 方法进行测试，可以让你捕获序列化问题并模拟真实的失败场景。

要了解更多关于 Testcontainers 的内容，请访问
[Testcontainers 概览](https://testcontainers.com/getting-started/)。

### 延伸阅读

- [Testcontainers WireMock 模块](https://testcontainers.com/modules/wiremock/)
- [WireMock 文档](https://wiremock.org/docs/)
- [Testcontainers JUnit 5 快速入门](https://java.testcontainers.org/quickstart/junit_5_quickstart/)

