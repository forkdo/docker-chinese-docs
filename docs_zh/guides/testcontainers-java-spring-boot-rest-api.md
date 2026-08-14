<!-- FILE: guides/testcontainers-java-spring-boot-rest-api.md -->

---
title: 使用 Testcontainers 测试 Spring Boot REST API
linkTitle: Spring Boot REST API
description: 了解如何使用 Testcontainers 配合 PostgreSQL 和 REST Assured 测试 Spring Boot REST API。
keywords: testcontainers, java, spring boot, testing, postgresql, rest api, rest assured, jpa
summary: |
  了解如何创建一个使用 Spring Data JPA 与 PostgreSQL 的 Spring Boot REST API，
  然后使用 Testcontainers 和 REST Assured 对其进行测试。
aliases:
  - /guides/testcontainers-java-spring-boot-rest-api/create-project/
  - /guides/testcontainers-java-spring-boot-rest-api/run-tests/
  - /guides/testcontainers-java-spring-boot-rest-api/write-tests/
params:
  tags: [testing]
  time: 25 minutes
---


<!-- Source: https://github.com/testcontainers/tc-guide-testing-spring-boot-rest-api -->

在本指南中，你将学习如何：

- 创建一个带有 REST API 端点的 Spring Boot 应用
- 使用 Spring Data JPA 与 PostgreSQL 存储和检索数据
- 使用 Testcontainers 与 REST Assured 测试 REST API

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

在 [Spring Initializr](https://start.spring.io) 上创建一个 Spring Boot 项目，添加
**Spring Web**、**Spring Data JPA**、**PostgreSQL Driver** 以及 **Testcontainers** 这几个
starter。

或者，克隆
[指南仓库](https://github.com/testcontainers/tc-guide-testing-spring-boot-rest-api)。

`pom.xml` 中的关键依赖如下：

```xml
<properties>
    <java.version>17</java.version>
    <testcontainers.version>2.0.4</testcontainers.version>
</properties>
<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-data-jpa</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
    <dependency>
        <groupId>org.postgresql</groupId>
        <artifactId>postgresql</artifactId>
        <scope>runtime</scope>
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
        <artifactId>testcontainers-postgresql</artifactId>
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

### 创建 JPA 实体

创建 `Customer.java`：

```java
package com.testcontainers.demo;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name = "customers")
class Customer {

  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  private Long id;

  @Column(nullable = false)
  private String name;

  @Column(nullable = false, unique = true)
  private String email;

  public Customer() {}

  public Customer(Long id, String name, String email) {
    this.id = id;
    this.name = name;
    this.email = email;
  }

  public Long getId() {
    return id;
  }

  public void setId(Long id) {
    this.id = id;
  }

  public String getName() {
    return name;
  }

  public void setName(String name) {
    this.name = name;
  }

  public String getEmail() {
    return email;
  }

  public void setEmail(String email) {
    this.email = email;
  }
}
```

### 创建 Spring Data JPA 仓储

```java
package com.testcontainers.demo;

import org.springframework.data.jpa.repository.JpaRepository;

interface CustomerRepository extends JpaRepository<Customer, Long> {}
```

### 添加 schema 创建脚本

创建 `src/main/resources/schema.sql`：

```sql
create table if not exists customers (
    id bigserial not null,
    name varchar not null,
    email varchar not null,
    primary key (id),
    UNIQUE (email)
);
```

在 `src/main/resources/application.properties` 中启用 schema 初始化：

```properties
spring.sql.init.mode=always
```

### 创建 REST API 端点

创建 `CustomerController.java`：

```java
package com.testcontainers.demo;

import java.util.List;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
class CustomerController {

  private final CustomerRepository repo;

  CustomerController(CustomerRepository repo) {
    this.repo = repo;
  }

  @GetMapping("/api/customers")
  List<Customer> getAll() {
    return repo.findAll();
  }
}
```

## 使用 Testcontainers 编写测试

要测试 REST API，你需要一个运行中的 Postgres 数据库和一个启动的 Spring 上下文。
Testcontainers 会在 Docker 容器中启动 Postgres，而 `@DynamicPropertySource` 会将其连接到
Spring。

### 编写测试

创建 `CustomerControllerTest.java`：

```java
package com.testcontainers.demo;

import static io.restassured.RestAssured.given;
import static org.hamcrest.Matchers.hasSize;

import io.restassured.RestAssured;
import io.restassured.http.ContentType;
import java.util.List;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.server.LocalServerPort;
import org.springframework.test.context.DynamicPropertyRegistry;
import org.springframework.test.context.DynamicPropertySource;
import org.testcontainers.postgresql.PostgreSQLContainer;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
class CustomerControllerTest {

  @LocalServerPort
  private Integer port;

  static PostgreSQLContainer postgres = new PostgreSQLContainer(
    "postgres:16-alpine"
  );

  @BeforeAll
  static void beforeAll() {
    postgres.start();
  }

  @AfterAll
  static void afterAll() {
    postgres.stop();
  }

  @DynamicPropertySource
  static void configureProperties(DynamicPropertyRegistry registry) {
    registry.add("spring.datasource.url", postgres::getJdbcUrl);
    registry.add("spring.datasource.username", postgres::getUsername);
    registry.add("spring.datasource.password", postgres::getPassword);
  }

  @Autowired
  CustomerRepository customerRepository;

  @BeforeEach
  void setUp() {
    RestAssured.baseURI = "http://localhost:" + port;
    customerRepository.deleteAll();
  }

  @Test
  void shouldGetAllCustomers() {
    List<Customer> customers = List.of(
      new Customer(null, "John", "john@mail.com"),
      new Customer(null, "Dennis", "dennis@mail.com")
    );
    customerRepository.saveAll(customers);

    given()
      .contentType(ContentType.JSON)
      .when()
      .get("/api/customers")
      .then()
      .statusCode(200)
      .body(".", hasSize(2));
  }
}
```

该测试的作用如下：

- `@SpringBootTest` 在随机端口上启动完整的应用。
- `PostgreSQLContainer` 在 `@BeforeAll` 中启动，在 `@AfterAll` 中停止。
- `@DynamicPropertySource` 将容器的 JDBC URL、用户名和密码注册到 Spring，使数据源连接到
  测试容器。
- `@BeforeEach` 在每个测试之前删除所有客户记录，以防测试之间相互污染。
- `shouldGetAllCustomers()` 插入两个客户，调用 `GET /api/customers`，并验证响应包含 2 条
  记录。

## 运行测试与后续步骤

### 运行测试

```console
$ ./mvnw test
```

或者使用 Gradle：

```console
$ ./gradlew test
```

你应该会看到 Postgres 的 Docker 容器启动，并且所有测试通过。测试结束后，容器会自动停止
并被移除。

### 小结

Testcontainers 库让你能够使用与生产环境相同类型的数据库（Postgres）来编写集成测试，而不是
使用 mock 或内存数据库。由于你是基于真实服务进行测试，你可以放心地重构代码，同时仍能验证
应用是否按预期工作。

想进一步了解 Testcontainers，请访问
[Testcontainers 概览](https://testcontainers.com/getting-started/)。

### 延伸阅读

- [Testcontainers JUnit 5 快速入门](https://java.testcontainers.org/quickstart/junit_5_quickstart/)
- [Testcontainers Postgres 模块](https://java.testcontainers.org/modules/databases/postgres/)
- [Testcontainers JDBC 支持](https://java.testcontainers.org/modules/databases/jdbc/)
