<!-- FILE: guides/testcontainers-java-keycloak-spring-boot.md -->

---
title: 使用 Keycloak 与 Testcontainers 保护 Spring Boot 微服务
linkTitle: Keycloak 与 Spring Boot
description: 了解如何使用 Keycloak 保护 Spring Boot 微服务，并使用 Testcontainers 的 Keycloak 模块对其进行测试。
keywords: testcontainers, java, spring boot, testing, keycloak, security, oauth2, jwt
summary: |
  了解如何使用 Spring Boot 创建 OAuth 2.0 资源服务器，使用 Keycloak 保护 API
  端点，并使用 Testcontainers 的 Keycloak 模块测试应用。
aliases:
  - /guides/testcontainers-java-keycloak-spring-boot/create-project/
  - /guides/testcontainers-java-keycloak-spring-boot/run-tests/
  - /guides/testcontainers-java-keycloak-spring-boot/write-tests/
params:
  tags: [testing]
  time: 30 minutes
---


<!-- Source: https://github.com/testcontainers/tc-guide-securing-spring-boot-microservice-using-keycloak-and-testcontainers -->

在本指南中，你将学习如何：

- 使用 Spring Boot 创建一个 OAuth 2.0 资源服务器
- 使用 Keycloak 保护 API 端点
- 使用 Testcontainers 的 Keycloak 模块测试 API
- 使用 Testcontainers 的 Keycloak 模块在本地运行应用

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
添加 **Spring Web**、**Validation**、**JDBC API**、**PostgreSQL Driver**、
**Spring Security**、**OAuth2 Resource Server** 以及 **Testcontainers** 这几个
starter。

或者，克隆
[指南仓库](https://github.com/testcontainers/tc-guide-securing-spring-boot-microservice-using-keycloak-and-testcontainers)。

生成应用后，添加
[testcontainers-keycloak](https://github.com/dasniko/testcontainers-keycloak)
社区模块和 [REST Assured](https://rest-assured.io/) 作为测试依赖。

`pom.xml` 中的关键依赖如下：

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
        <artifactId>spring-boot-starter-validation</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-jdbc</artifactId>
    </dependency>
    <dependency>
        <groupId>org.postgresql</groupId>
        <artifactId>postgresql</artifactId>
        <scope>runtime</scope>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-security</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-oauth2-resource-server</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-test</artifactId>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.springframework.security</groupId>
        <artifactId>spring-security-test</artifactId>
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
        <artifactId>testcontainers-postgresql</artifactId>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>com.github.dasniko</groupId>
        <artifactId>testcontainers-keycloak</artifactId>
        <version>3.4.0</version>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>io.rest-assured</groupId>
        <artifactId>rest-assured</artifactId>
        <scope>test</scope>
    </dependency>
</dependencies>
```

### 创建领域模型

创建一个表示领域对象的 `Product` record：

```java
package com.testcontainers.products.domain;

import jakarta.validation.constraints.NotEmpty;

public record Product(Long id, @NotEmpty String title, String description) {}
```

### 创建仓储

使用 Spring 的 `JdbcClient` 实现 `ProductRepository`，与 PostgreSQL 数据库交互：

```java
package com.testcontainers.products.domain;

import java.util.List;
import org.springframework.jdbc.core.simple.JdbcClient;
import org.springframework.jdbc.support.GeneratedKeyHolder;
import org.springframework.jdbc.support.KeyHolder;
import org.springframework.stereotype.Repository;

@Repository
public class ProductRepository {

  private final JdbcClient jdbcClient;

  public ProductRepository(JdbcClient jdbcClient) {
    this.jdbcClient = jdbcClient;
  }

  public List<Product> getAll() {
    return jdbcClient.sql("SELECT * FROM products").query(Product.class).list();
  }

  public Product create(Product product) {
    String sql =
      "INSERT INTO products(title, description) VALUES (:title,:description) RETURNING id";
    KeyHolder keyHolder = new GeneratedKeyHolder();
    jdbcClient
      .sql(sql)
      .param("title", product.title())
      .param("description", product.description())
      .update(keyHolder);
    Long id = keyHolder.getKeyAs(Long.class);
    return new Product(id, product.title(), product.description());
  }
}
```

### 添加 schema 创建脚本

创建 `src/main/resources/schema.sql` 来初始化 `products` 表：

```sql
CREATE TABLE products (
    id bigserial primary key,
    title varchar not null,
    description text
);
```

在 `src/main/resources/application.properties` 中启用 schema 初始化：

```properties
spring.sql.init.mode=always
```

对于生产应用，请改用 Flyway 或 Liquibase 之类的数据库迁移工具。

### 实现 API 端点

创建 `ProductController`，包含获取所有产品以及创建产品的端点：

```java
package com.testcontainers.products.api;

import com.testcontainers.products.domain.Product;
import com.testcontainers.products.domain.ProductRepository;
import jakarta.validation.Valid;
import java.util.List;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/products")
class ProductController {

  private final ProductRepository productRepository;

  ProductController(ProductRepository productRepository) {
    this.productRepository = productRepository;
  }

  @GetMapping
  List<Product> getAll() {
    return productRepository.getAll();
  }

  @PostMapping
  @ResponseStatus(HttpStatus.CREATED)
  Product createProduct(@RequestBody @Valid Product product) {
    return productRepository.create(product);
  }
}
```

### 配置 OAuth 2.0 安全

创建一个 `SecurityConfig` 类，使用基于 JWT 令牌的认证来保护 API 端点：

```java
package com.testcontainers.products.config;

import static org.springframework.security.config.Customizer.withDefaults;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpMethod;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configurers.CorsConfigurer;
import org.springframework.security.config.annotation.web.configurers.CsrfConfigurer;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.web.SecurityFilterChain;

@Configuration
@EnableWebSecurity
class SecurityConfig {

  @Bean
  SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
    http
      .authorizeHttpRequests(c ->
        c
          .requestMatchers(HttpMethod.GET, "/api/products")
          .permitAll()
          .requestMatchers(HttpMethod.POST, "/api/products")
          .authenticated()
          .anyRequest()
          .authenticated()
      )
      .sessionManagement(c ->
        c.sessionCreationPolicy(SessionCreationPolicy.STATELESS)
      )
      .cors(CorsConfigurer::disable)
      .csrf(CsrfConfigurer::disable)
      .oauth2ResourceServer(oauth2 -> oauth2.jwt(withDefaults()));
    return http.build();
  }
}
```

该配置：

- 允许 `GET /api/products` 免认证访问。
- 要求 `POST /api/products` 及所有其他端点通过认证。
- 使用基于 JWT 令牌的认证配置 OAuth 2.0 资源服务器。
- 由于这是一个无状态 API，因此禁用了 CORS 和 CSRF。

将 JWT 签发者 URI 添加到 `application.properties`：

```properties
spring.security.oauth2.resourceserver.jwt.issuer-uri=http://localhost:9090/realms/keycloaktcdemo
```

### 导出 Keycloak realm 配置

在编写测试之前，先导出一份 Keycloak realm 配置，以便测试环境能自动导入它。先启动一个临时的 Keycloak 实例：

```console
$ docker run -p 9090:8080 \
    -e KEYCLOAK_ADMIN=admin \
    -e KEYCLOAK_ADMIN_PASSWORD=admin \
    quay.io/keycloak/keycloak:25 start-dev
```

打开 `http://localhost:9090`，使用 `admin/admin` 登录 Admin Console。然后配置 realm：

1. 在左上角，选择 realm 下拉菜单，创建一个名为 `keycloaktcdemo` 的 realm。
2. 在 `keycloaktcdemo` realm 下，创建一个客户端，配置如下：
   - **Client ID**：`product-service`
   - **Client Authentication**：`On`
   - **Authentication flow**：仅勾选 **Service accounts roles**
3. 在 **Client details** 页面，切换到 **Credentials** 标签页，复制 **Client secret** 的值。

导出 realm 配置：

```console
$ docker ps
# 复制 keycloak 容器 id

$ docker exec -it <container-id> /bin/bash

$ /opt/keycloak/bin/kc.sh export --dir /opt/keycloak/data/import --realm keycloaktcdemo

$ exit

$ docker cp <container-id>:/opt/keycloak/data/import/keycloaktcdemo-realm.json keycloaktcdemo-realm.json
```

将导出的 `keycloaktcdemo-realm.json` 文件复制到 `src/test/resources` 目录下。

## 使用 Testcontainers 编写测试

要测试受保护的 API 端点，你需要一个运行中的 Keycloak 实例、一个 PostgreSQL 数据库，以及启动的 Spring 上下文。Testcontainers 会在 Docker 容器中启动这两个服务，并通过动态属性注册将它们连接到 Spring。

### 配置测试容器

Spring Boot 的 Testcontainers 支持允许你将容器声明为 bean。对于 Keycloak，`@ServiceConnection`
并不可用，但你可以使用 `DynamicPropertyRegistry` 来动态设置 JWT 签发者 URI。

在 `src/test/java` 下创建 `ContainersConfig.java`：

```java
package com.testcontainers.products;

import dasniko.testcontainers.keycloak.KeycloakContainer;
import org.springframework.boot.test.context.TestConfiguration;
import org.springframework.boot.testcontainers.service.connection.ServiceConnection;
import org.springframework.context.annotation.Bean;
import org.springframework.test.context.DynamicPropertyRegistry;
import org.testcontainers.postgresql.PostgreSQLContainer;

@TestConfiguration(proxyBeanMethods = false)
public class ContainersConfig {

  static String POSTGRES_IMAGE = "postgres:16-alpine";
  static String KEYCLOAK_IMAGE = "quay.io/keycloak/keycloak:25.0";
  static String realmImportFile = "/keycloaktcdemo-realm.json";
  static String realmName = "keycloaktcdemo";

  @Bean
  @ServiceConnection
  PostgreSQLContainer postgres() {
    return new PostgreSQLContainer(POSTGRES_IMAGE);
  }

  @Bean
  KeycloakContainer keycloak(DynamicPropertyRegistry registry) {
    var keycloak = new KeycloakContainer(KEYCLOAK_IMAGE)
      .withRealmImportFile(realmImportFile);
    registry.add(
      "spring.security.oauth2.resourceserver.jwt.issuer-uri",
      () -> keycloak.getAuthServerUrl() + "/realms/" + realmName
    );
    return keycloak;
  }
}
```

该配置：

- 声明了一个带 `@ServiceConnection` 的 `PostgreSQLContainer` bean，它会启动一个
  PostgreSQL 容器并自动注册数据源属性。
- 声明了一个使用 `quay.io/keycloak/keycloak:25.0` 镜像的 `KeycloakContainer` bean，
  导入 realm 配置文件，并根据 Keycloak 容器的认证服务器 URL 动态注册 JWT 签发者 URI。

### 编写测试

创建 `ProductControllerTests.java`：

```java
package com.testcontainers.products.api;

import static io.restassured.RestAssured.given;
import static io.restassured.RestAssured.when;
import static java.util.Collections.singletonList;
import static org.springframework.boot.test.context.SpringBootTest.WebEnvironment.RANDOM_PORT;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.testcontainers.products.ContainersConfig;
import io.restassured.RestAssured;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.autoconfigure.security.oauth2.resource.OAuth2ResourceServerProperties;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.server.LocalServerPort;
import org.springframework.context.annotation.Import;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestTemplate;

@SpringBootTest(webEnvironment = RANDOM_PORT)
@Import(ContainersConfig.class)
class ProductControllerTests {

  static final String GRANT_TYPE_CLIENT_CREDENTIALS = "client_credentials";
  static final String CLIENT_ID = "product-service";
  static final String CLIENT_SECRET = "jTJJqdzeCSt3DmypfHZa42vX8U9rQKZ9";

  @LocalServerPort
  private int port;

  @Autowired
  OAuth2ResourceServerProperties oAuth2ResourceServerProperties;

  @BeforeEach
  void setup() {
    RestAssured.port = port;
  }

  @Test
  void shouldGetProductsWithoutAuthToken() {
    when().get("/api/products").then().statusCode(200);
  }

  @Test
  void shouldGetUnauthorizedWhenCreateProductWithoutAuthToken() {
    given()
      .contentType("application/json")
      .body(
        """
            {
                "title": "New Product",
                "description": "Brand New Product"
            }
        """
      )
      .when()
      .post("/api/products")
      .then()
      .statusCode(401);
  }

  @Test
  void shouldCreateProductWithAuthToken() {
    String token = getToken();

    given()
      .header("Authorization", "Bearer " + token)
      .contentType("application/json")
      .body(
        """
            {
                "title": "New Product",
                "description": "Brand New Product"
            }
        """
      )
      .when()
      .post("/api/products")
      .then()
      .statusCode(201);
  }

  private String getToken() {
    RestTemplate restTemplate = new RestTemplate();
    HttpHeaders httpHeaders = new HttpHeaders();
    httpHeaders.setContentType(MediaType.APPLICATION_FORM_URLENCODED);

    MultiValueMap<String, String> map = new LinkedMultiValueMap<>();
    map.put("grant_type", singletonList(GRANT_TYPE_CLIENT_CREDENTIALS));
    map.put("client_id", singletonList(CLIENT_ID));
    map.put("client_secret", singletonList(CLIENT_SECRET));

    String authServerUrl =
      oAuth2ResourceServerProperties.getJwt().getIssuerUri() +
      "/protocol/openid-connect/token";

    var request = new HttpEntity<>(map, httpHeaders);
    KeyCloakToken token = restTemplate.postForObject(
      authServerUrl,
      request,
      KeyCloakToken.class
    );

    assert token != null;
    return token.accessToken();
  }

  record KeyCloakToken(@JsonProperty("access_token") String accessToken) {}
}
```

这些测试覆盖的内容如下：

- `shouldGetProductsWithoutAuthToken()` 在不带 `Authorization` 头的情况下调用
  `GET /api/products`。由于该端点被配置为允许免认证访问，响应状态码为 200。
- `shouldGetUnauthorizedWhenCreateProductWithoutAuthToken()` 在不带 `Authorization`
  头的情况下调用受保护的 `POST /api/products` 端点，并断言响应状态码为 401
  （未授权）。
- `shouldCreateProductWithAuthToken()` 首先使用 Client Credentials 流程获取一个
  `access_token`。然后在调用 `POST /api/products` 时，将该令牌作为 Bearer 令牌
  放入 `Authorization` 头中，并断言响应状态码为 201（已创建）。

`getToken()` 辅助方法使用在导出的 realm 中配置的客户端 ID 和客户端密钥，从
Keycloak 令牌端点请求访问令牌。

### 将 Testcontainers 用于本地开发

Spring Boot 的 Testcontainers 支持也可用于本地开发。在 `src/test/java` 下创建
`TestApplication.java`：

```java
package com.testcontainers.products;

import org.springframework.boot.SpringApplication;

public class TestApplication {

  public static void main(String[] args) {
    SpringApplication
      .from(Application::main)
      .with(ContainersConfig.class)
      .run(args);
  }
}
```

从 IDE 中运行 `TestApplication.java`，而不是主类 `Application.java`。它会启动
`ContainersConfig` 中定义的容器，并将应用配置为使用动态注册的属性，因此你无需
手动安装或配置 PostgreSQL 和 Keycloak。

## 运行测试与后续步骤

### 运行测试

```console
$ ./mvnw test
```

或者使用 Gradle：

```console
$ ./gradlew test
```

你应该会看到 Keycloak 和 PostgreSQL 的 Docker 容器启动，并导入 realm 配置，测试
全部通过。测试结束后，容器会自动停止并被移除。

### 小结

Testcontainers 的 Keycloak 模块让你能够基于真实的 Keycloak 服务器开发并测试应用，
而不是使用 mock。针对一个与你的生产环境相仿的真实 OAuth 2.0 提供方进行测试，能让你
对安全配置和基于令牌的认证流程更有信心。

想进一步了解 Testcontainers，请访问
[Testcontainers 概览](https://testcontainers.com/getting-started/)。

### 延伸阅读

- [在 Java Spring Boot 项目中使用 Testcontainers 入门](https://testcontainers.com/guides/testing-spring-boot-rest-api-using-testcontainers/)
- [Testcontainers Keycloak 模块](https://testcontainers.com/modules/keycloak/)
- [testcontainers-keycloak GitHub 仓库](https://github.com/dasniko/testcontainers-keycloak)
- [Spring Boot OAuth 2.0 资源服务器](https://docs.spring.io/spring-security/reference/servlet/oauth2/resource-server/index.html)
