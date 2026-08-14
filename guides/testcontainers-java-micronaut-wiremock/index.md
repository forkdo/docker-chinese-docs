# 

<!-- FILE: guides/testcontainers-java-micronaut-wiremock.md -->

---
title: 在 Micronaut 应用中使用 WireMock 测试 REST API 集成
linkTitle: Micronaut WireMock
description: 了解如何使用 Testcontainers 的 WireMock 模块测试 Micronaut 应用中的 REST API 集成。
keywords: testcontainers, java, micronaut, testing, wiremock, rest api
summary: |
  了解如何创建一个与外部 REST API 集成的 Micronaut 应用，然后使用 WireMock
  以及 Testcontainers 的 WireMock 模块测试这些集成。
aliases:
  - /guides/testcontainers-java-micronaut-wiremock/create-project/
  - /guides/testcontainers-java-micronaut-wiremock/run-tests/
  - /guides/testcontainers-java-micronaut-wiremock/write-tests/
params:
  tags: [testing]
  time: 20 minutes
---


<!-- Source: https://github.com/testcontainers/tc-guide-testing-rest-api-integrations-in-micronaut-apps-using-wiremock -->

在本指南中，你将学习如何：

- 创建一个与外部 REST API 通信的 Micronaut 应用
- 使用 WireMock 测试外部 API 集成
- 使用 Testcontainers 的 WireMock 模块以 Docker 容器方式运行 WireMock

## 先决条件

- Java 17+
- Maven 或 Gradle
- 一个受 Testcontainers 支持的 Docker 环境

> [!NOTE]
> 如果你刚接触 Testcontainers，请访问
> [Testcontainers 概览](https://testcontainers.com/getting-started/) 了解
> Testcontainers 及其使用优势。

## 创建 Micronaut 项目

### 搭建项目

在 [Micronaut Launch](https://micronaut.io/launch) 上创建一个 Micronaut 项目，
勾选 **http-client**、**micronaut-test-rest-assured** 以及 **testcontainers**
这些特性（feature）。

或者，克隆
[指南仓库](https://github.com/testcontainers/tc-guide-testing-rest-api-integrations-in-micronaut-apps-using-wiremock)。

生成项目后，添加 **WireMock** 和 **Testcontainers WireMock** 库作为测试依赖。
`pom.xml` 中的关键依赖如下：

```xml
<parent>
    <groupId>io.micronaut.platform</groupId>
    <artifactId>micronaut-parent</artifactId>
    <version>4.1.2</version>
</parent>

<properties>
    <jdk.version>17</jdk.version>
    <micronaut.version>4.1.2</micronaut.version>
    <micronaut.runtime>netty</micronaut.runtime>
</properties>

<repositories>
    <repository>
        <id>jitpack.io</id>
        <url>https://jitpack.io</url>
    </repository>
</repositories>

<dependencies>
    <dependency>
        <groupId>io.micronaut</groupId>
        <artifactId>micronaut-http-client</artifactId>
        <scope>compile</scope>
    </dependency>
    <dependency>
        <groupId>io.micronaut</groupId>
        <artifactId>micronaut-http-server-netty</artifactId>
        <scope>compile</scope>
    </dependency>
    <dependency>
        <groupId>io.micronaut.serde</groupId>
        <artifactId>micronaut-serde-jackson</artifactId>
        <scope>compile</scope>
    </dependency>
    <dependency>
        <groupId>io.micronaut.test</groupId>
        <artifactId>micronaut-test-junit5</artifactId>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>io.micronaut.test</groupId>
        <artifactId>micronaut-test-rest-assured</artifactId>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.testcontainers</groupId>
        <artifactId>testcontainers-junit-jupiter</artifactId>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.testcontainers</groupId>
        <artifactId>testcontainers</artifactId>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.wiremock</groupId>
        <artifactId>wiremock-standalone</artifactId>
        <version>3.2.0</version>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.wiremock.integrations.testcontainers</groupId>
        <artifactId>wiremock-testcontainers-module</artifactId>
        <version>1.0-alpha-13</version>
        <scope>test</scope>
    </dependency>
</dependencies>
```

本指南构建的是一个管理视频相册（album）的应用。相册中的照片资源由第三方 REST API
处理。出于演示目的，该应用使用公开可用的 [JSONPlaceholder](https://jsonplaceholder.typicode.com/)
API 作为照片服务。

该应用暴露一个 `GET /api/albums/{albumId}` 端点，它会调用照片服务以获取指定相册的
照片。[WireMock](https://wiremock.org/) 是一个用于构建 mock API 的工具。Testcontainers
提供了一个 [WireMock 模块](https://testcontainers.com/modules/wiremock/)，能以 Docker
容器方式运行 WireMock。

### 创建 Album 和 Photo 模型

使用 Java record 创建 `Album.java`。为两个 record 都加上 `@Serdeable` 注解，以允许
序列化和反序列化：

```java
package com.testcontainers.demo;

import io.micronaut.serde.annotation.Serdeable;
import java.util.List;

@Serdeable
public record Album(Long albumId, List<Photo> photos) {}

@Serdeable
record Photo(Long id, String title, String url, String thumbnailUrl) {}
```

### 创建 PhotoServiceClient

Micronaut 提供了[声明式 HTTP 客户端](https://docs.micronaut.io/latest/guide/#httpClient)
支持。创建一个接口，包含一个按相册 ID 获取照片的方法：

```java
package com.testcontainers.demo;

import io.micronaut.http.annotation.Get;
import io.micronaut.http.annotation.PathVariable;
import io.micronaut.http.client.annotation.Client;
import java.util.List;

@Client(id = "photosapi")
interface PhotoServiceClient {

    @Get("/albums/{albumId}/photos")
    List<Photo> getPhotos(@PathVariable Long albumId);
}
```

`@Client(id = "photosapi")` 注解将该客户端绑定到一个具名配置。在
`src/main/resources/application.properties` 中添加以下属性来设置基础 URL：

```properties
micronaut.http.services.photosapi.url=https://jsonplaceholder.typicode.com
```

### 创建 REST API 端点

创建 `AlbumController.java`：

```java
package com.testcontainers.demo;

import static io.micronaut.scheduling.TaskExecutors.BLOCKING;

import io.micronaut.http.annotation.Controller;
import io.micronaut.http.annotation.Get;
import io.micronaut.http.annotation.PathVariable;
import io.micronaut.scheduling.annotation.ExecuteOn;

@Controller("/api")
class AlbumController {

    private final PhotoServiceClient photoServiceClient;

    AlbumController(PhotoServiceClient photoServiceClient) {
        this.photoServiceClient = photoServiceClient;
    }

    @ExecuteOn(BLOCKING)
    @Get("/albums/{albumId}")
    public Album getAlbumById(@PathVariable Long albumId) {
        return new Album(albumId, photoServiceClient.getPhotos(albumId));
    }
}
```

该控制器的作用如下：

- `@Controller("/api")` 将控制器映射到 `/api` 路径。
- 通过构造函数注入提供 `PhotoServiceClient` bean。
- `@ExecuteOn(BLOCKING)` 将阻塞式 I/O 卸载到独立的线程池，避免阻塞事件循环。
- `@Get("/albums/{albumId}")` 将 `getAlbumById()` 方法映射到 HTTP GET 请求。

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

## 使用 WireMock 和 Testcontainers 编写测试

在 HTTP 协议层面（而非 mock Java 方法）来 mock 外部 API 的交互，让你可以验证序列化与
反序列化行为，并模拟网络故障。

### 使用 WireMock 的 JUnit 5 扩展进行测试

第一种方式使用 WireMock 的 `WireMockExtension`，在一个动态端口上启动一个进程内
（in-process）WireMock 服务器。

创建 `AlbumControllerTest.java`：

```java
package com.testcontainers.demo;

import static com.github.tomakehurst.wiremock.client.WireMock.aResponse;
import static com.github.tomakehurst.wiremock.client.WireMock.urlMatching;
import static com.github.tomakehurst.wiremock.core.WireMockConfiguration.wireMockConfig;
import static io.restassured.RestAssured.given;
import static org.hamcrest.CoreMatchers.is;
import static org.hamcrest.Matchers.hasSize;

import com.github.tomakehurst.wiremock.client.WireMock;
import com.github.tomakehurst.wiremock.junit5.WireMockExtension;
import io.micronaut.context.ApplicationContext;
import io.micronaut.http.MediaType;
import io.micronaut.runtime.server.EmbeddedServer;
import io.restassured.RestAssured;
import io.restassured.http.ContentType;
import java.util.Collections;
import java.util.Map;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.RegisterExtension;

class AlbumControllerTest {

    @RegisterExtension
    static WireMockExtension wireMock = WireMockExtension.newInstance()
            .options(wireMockConfig().dynamicPort())
            .build();

    private Map<String, Object> getProperties() {
        return Collections.singletonMap("micronaut.http.services.photosapi.url", wireMock.baseUrl());
    }

    @Test
    void shouldGetAlbumById() {
        try (EmbeddedServer server = ApplicationContext.run(EmbeddedServer.class, getProperties())) {
            RestAssured.port = server.getPort();
            Long albumId = 1L;
            String responseJson =
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
            """;
            wireMock.stubFor(WireMock.get(urlMatching("/albums/" + albumId + "/photos"))
                    .willReturn(aResponse()
                            .withHeader("Content-Type", MediaType.APPLICATION_JSON)
                            .withBody(responseJson)));

            given().contentType(ContentType.JSON)
                    .when()
                    .get("/api/albums/{albumId}", albumId)
                    .then()
                    .statusCode(200)
                    .body("albumId", is(albumId.intValue()))
                    .body("photos", hasSize(2));
        }
    }

    @Test
    void shouldReturnServerErrorWhenPhotoServiceCallFailed() {
        try (EmbeddedServer server = ApplicationContext.run(EmbeddedServer.class, getProperties())) {
            RestAssured.port = server.getPort();
            Long albumId = 2L;
            wireMock.stubFor(WireMock.get(urlMatching("/albums/" + albumId + "/photos"))
                    .willReturn(aResponse().withStatus(500)));

            given().contentType(ContentType.JSON)
                    .when()
                    .get("/api/albums/{albumId}", albumId)
                    .then()
                    .statusCode(500);
        }
    }
}
```

该测试的作用如下：

- `WireMockExtension` 在一个动态端口上启动一个 WireMock 服务器。
- `getProperties()` 方法覆盖 `micronaut.http.services.photosapi.url`，使其指向
  WireMock 端点，从而让应用与 WireMock 而非真实的照片服务通信。
- `shouldGetAlbumById()` 为 `/albums/{albumId}/photos` 配置一个 mock 响应，向应用的
  `/api/albums/{albumId}` 端点发送请求，并校验响应体。
- `shouldReturnServerErrorWhenPhotoServiceCallFailed()` 配置 WireMock 返回 500 状态，
  并验证应用会传播该错误。

### 使用 JSON 映射文件配置桩（stub）

除了使用 WireMock 的 Java API 配置桩之外，你也可以使用基于 JSON 映射的配置。

创建 `src/test/resources/wiremock/mappings/get-album-photos.json`：

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

创建 `src/test/resources/wiremock/__files/album-photos-resp-200.json`：

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

然后初始化 WireMock，使其从这些文件中加载桩映射：

```java
@RegisterExtension
static WireMockExtension wireMock = WireMockExtension.newInstance()
     .options(
         wireMockConfig()
            .dynamicPort()
            .usingFilesUnderClasspath("wiremock")
    )
     .build();
```

有了基于映射文件的桩配置后，就可以编写不需要编程式桩的测试：

```java
@Test
void shouldGetAlbumById() {
    Long albumId = 1L;
    try (EmbeddedServer server = ApplicationContext.run(EmbeddedServer.class, getProperties())) {
        RestAssured.port = server.getPort();

        given().contentType(ContentType.JSON)
                .when()
                .get("/api/albums/{albumId}", albumId)
                .then()
                .statusCode(200)
                .body("albumId", is(albumId.intValue()))
                .body("photos", hasSize(2));
    }
}
```

### 使用 Testcontainers 的 WireMock 模块

[Testcontainers 的 WireMock 模块](https://testcontainers.com/modules/wiremock/)
基于 [WireMock Docker](https://github.com/wiremock/wiremock-docker)，在你的测试中
将 WireMock 服务器作为独立的容器提供（provision）。

创建包含桩映射的 `src/test/resources/mocks-config.json`：

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

创建 `src/test/resources/album-photos-response.json`：

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
import static org.hamcrest.Matchers.nullValue;

import io.micronaut.context.ApplicationContext;
import io.micronaut.core.annotation.NonNull;
import io.micronaut.runtime.server.EmbeddedServer;
import io.restassured.RestAssured;
import io.restassured.http.ContentType;
import java.util.Collections;
import java.util.Map;
import org.junit.jupiter.api.Test;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;
import org.wiremock.integrations.testcontainers.WireMockContainer;

@Testcontainers(disabledWithoutDocker = true)
class AlbumControllerTestcontainersTests {

    @Container
    static WireMockContainer wiremockServer = new WireMockContainer("wiremock/wiremock:2.35.0")
            .withMappingFromResource("mocks-config.json")
            .withFileFromResource("album-photos-response.json");

    @NonNull public Map<String, Object> getProperties() {
        return Collections.singletonMap("micronaut.http.services.photosapi.url", wiremockServer.getBaseUrl());
    }

    @Test
    void shouldGetAlbumById() {
        Long albumId = 1L;
        try (EmbeddedServer server = ApplicationContext.run(EmbeddedServer.class, getProperties())) {
            RestAssured.port = server.getPort();

            given().contentType(ContentType.JSON)
                    .when()
                    .get("/api/albums/{albumId}", albumId)
                    .then()
                    .statusCode(200)
                    .body("albumId", is(albumId.intValue()))
                    .body("photos", hasSize(2));
        }
    }

    @Test
    void shouldReturnServerErrorWhenPhotoServiceCallFailed() {
        Long albumId = 2L;
        try (EmbeddedServer server = ApplicationContext.run(EmbeddedServer.class, getProperties())) {
            RestAssured.port = server.getPort();
            given().contentType(ContentType.JSON)
                    .when()
                    .get("/api/albums/{albumId}", albumId)
                    .then()
                    .statusCode(500);
        }
    }

    @Test
    void shouldReturnEmptyPhotos() {
        Long albumId = 3L;
        try (EmbeddedServer server = ApplicationContext.run(EmbeddedServer.class, getProperties())) {
            RestAssured.port = server.getPort();
            given().contentType(ContentType.JSON)
                    .when()
                    .get("/api/albums/{albumId}", albumId)
                    .then()
                    .statusCode(200)
                    .body("albumId", is(albumId.intValue()))
                    .body("photos", nullValue());
        }
    }
}
```

该测试的作用如下：

- `@Testcontainers` 与 `@Container` 注解使用 `wiremock/wiremock:2.35.0` Docker 镜像
  启动一个 `WireMockContainer`。
- `withMappingFromResource("mocks-config.json")` 从 classpath 资源中加载桩映射。
- `withFileFromResource("album-photos-response.json")` 使响应体文件对 WireMock 可用。
- `getProperties()` 覆盖照片服务 URL，使其指向 WireMock 容器的基础 URL。
- `shouldGetAlbumById()` 验证应用返回了包含两个照片的预期相册。
- `shouldReturnServerErrorWhenPhotoServiceCallFailed()` 验证照片服务返回的 500 会传播
  给调用方。
- `shouldReturnEmptyPhotos()` 验证应用能处理空的照片列表。

## 运行测试与后续步骤

### 运行测试

```console
$ ./mvnw test
```

或者使用 Gradle：

```console
$ ./gradlew test
```

你应该在控制台输出中看到 WireMock 的 Docker 容器启动。它充当照片服务，依据配置的
预期（expectation）返回 mock 响应。所有测试都应通过。

### 小结

你构建了一个使用声明式 HTTP 客户端与外部 REST API 集成的 Micronaut 应用，然后使用
WireMock 和 Testcontainers 的 WireMock 模块对该集成进行了测试。在 HTTP 协议层面而非
mock Java 方法层面进行测试，能让你发现序列化问题并模拟真实的故障场景。

> [!TIP]
> Testcontainers 的 WireMock 模块同样适用于 Go 和 Python。

想进一步了解 Testcontainers，请访问
[Testcontainers 概览](https://testcontainers.com/getting-started/)。

### 延伸阅读

- [Testcontainers WireMock 模块](https://testcontainers.com/modules/wiremock/)
- [WireMock 文档](https://wiremock.org/docs/)
- [Testcontainers JUnit 5 快速入门](https://java.testcontainers.org/quickstart/junit_5_quickstart/)
- [在 Spring Boot 中使用 WireMock 测试 REST API 集成](/guides/testcontainers-java-wiremock/)

