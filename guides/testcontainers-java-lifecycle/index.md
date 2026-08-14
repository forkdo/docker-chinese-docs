# 

<!-- FILE: guides/testcontainers-java-lifecycle.md -->

---
title: 使用 JUnit 5 管理 Testcontainers 容器生命周期
linkTitle: 容器生命周期（Java）
description: 了解如何使用 JUnit 5 回调、扩展注解以及单例容器模式来管理 Testcontainers 容器的生命周期。
keywords: testcontainers, java, testing, junit, lifecycle, singleton containers, postgresql
summary: |
  了解使用 JUnit 5 生命周期回调、扩展注解以及单例容器模式，通过不同方式
  管理 Testcontainers 容器生命周期。
aliases:
  - /guides/testcontainers-java-lifecycle/create-project/
  - /guides/testcontainers-java-lifecycle/extension-annotations/
  - /guides/testcontainers-java-lifecycle/lifecycle-callbacks/
  - /guides/testcontainers-java-lifecycle/singleton-containers/
params:
  tags: [testing]
  time: 20 minutes
---


<!-- Source: https://github.com/testcontainers/tc-guide-testcontainers-lifecycle -->

在本指南中，你将学习如何：

- 使用 JUnit 5 生命周期回调启动和停止容器
- 使用 JUnit 5 扩展注解（`@Testcontainers` 和 `@Container`）管理容器
- 使用单例容器模式在多个测试类之间共享容器
- 避免将扩展注解与单例容器混用时的常见错误配置

## 先决条件

- Java 17+
- 你偏好的 IDE
- 一个受 Testcontainers 支持的 Docker 环境

> [!NOTE]
> 如果你刚接触 Testcontainers，请访问
> [Testcontainers 概览](https://testcontainers.com/getting-started/) 了解
> Testcontainers 及其使用优势。

## 创建项目与业务逻辑

### 搭建项目

使用 Maven 创建一个 Java 项目，并添加所需依赖：

```xml
<dependencies>
    <dependency>
        <groupId>org.postgresql</groupId>
        <artifactId>postgresql</artifactId>
        <version>42.7.3</version>
    </dependency>
    <dependency>
        <groupId>ch.qos.logback</groupId>
        <artifactId>logback-classic</artifactId>
        <version>1.5.6</version>
    </dependency>
    <dependency>
        <groupId>org.junit.jupiter</groupId>
        <artifactId>junit-jupiter</artifactId>
        <version>5.10.2</version>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.testcontainers</groupId>
        <artifactId>testcontainers-junit-jupiter</artifactId>
        <version>2.0.4</version>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.testcontainers</groupId>
        <artifactId>testcontainers-postgresql</artifactId>
        <version>2.0.4</version>
        <scope>test</scope>
    </dependency>
</dependencies>
```

### 创建业务逻辑

创建一个 `Customer` record：

```java
package com.testcontainers.demo;

public record Customer(Long id, String name) {}
```

创建一个 `CustomerService` 类，包含创建、查询和删除客户的方法：

```java
package com.testcontainers.demo;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

public class CustomerService {

  private final String url;
  private final String username;
  private final String password;

  public CustomerService(String url, String username, String password) {
    this.url = url;
    this.username = username;
    this.password = password;
    createCustomersTableIfNotExists();
  }

  public void createCustomer(Customer customer) {
    try (Connection conn = this.getConnection()) {
      PreparedStatement pstmt = conn.prepareStatement(
        "insert into customers(id,name) values(?,?)"
      );
      pstmt.setLong(1, customer.id());
      pstmt.setString(2, customer.name());
      pstmt.execute();
    } catch (SQLException e) {
      throw new RuntimeException(e);
    }
  }

  public List<Customer> getAllCustomers() {
    List<Customer> customers = new ArrayList<>();
    try (Connection conn = this.getConnection()) {
      PreparedStatement pstmt = conn.prepareStatement(
        "select id,name from customers"
      );
      ResultSet rs = pstmt.executeQuery();
      while (rs.next()) {
        long id = rs.getLong("id");
        String name = rs.getString("name");
        customers.add(new Customer(id, name));
      }
    } catch (SQLException e) {
      throw new RuntimeException(e);
    }
    return customers;
  }

  public Optional<Customer> getCustomer(Long customerId) {
    try (Connection conn = this.getConnection()) {
      PreparedStatement pstmt = conn.prepareStatement(
        "select id,name from customers where id = ?"
      );
      pstmt.setLong(1, customerId);
      ResultSet rs = pstmt.executeQuery();
      if (rs.next()) {
        long id = rs.getLong("id");
        String name = rs.getString("name");
        return Optional.of(new Customer(id, name));
      }
    } catch (SQLException e) {
      throw new RuntimeException(e);
    }
    return Optional.empty();
  }

  public void deleteAllCustomers() {
    try (Connection conn = this.getConnection()) {
      PreparedStatement pstmt = conn.prepareStatement("delete from customers");
      pstmt.execute();
    } catch (SQLException e) {
      throw new RuntimeException(e);
    }
  }

  private void createCustomersTableIfNotExists() {
    try (Connection conn = this.getConnection()) {
      PreparedStatement pstmt = conn.prepareStatement(
        """
        create table if not exists customers (
            id bigint not null,
            name varchar not null,
            primary key (id)
        )
        """
      );
      pstmt.execute();
    } catch (SQLException e) {
      throw new RuntimeException(e);
    }
  }

  private Connection getConnection() {
    try {
      return DriverManager.getConnection(url, username, password);
    } catch (Exception e) {
      throw new RuntimeException(e);
    }
  }
}
```

## JUnit 5 生命周期回调

使用 Testcontainers 进行测试时，你希望在执行任何测试之前启动所需容器，并在之后移除它们。你可以使用 JUnit 5 的 `@BeforeAll` 和 `@AfterAll` 生命周期回调方法来实现：

```java
package com.testcontainers.demo;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.List;
import java.util.Optional;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.testcontainers.postgresql.PostgreSQLContainer;

class CustomerServiceWithLifeCycleCallbacksTest {

  static PostgreSQLContainer postgres = new PostgreSQLContainer(
    "postgres:16-alpine"
  );

  CustomerService customerService;

  @BeforeAll
  static void startContainers() {
    postgres.start();
  }

  @AfterAll
  static void stopContainers() {
    postgres.stop();
  }

  @BeforeEach
  void setUp() {
    customerService =
    new CustomerService(
      postgres.getJdbcUrl(),
      postgres.getUsername(),
      postgres.getPassword()
    );
    customerService.deleteAllCustomers();
  }

  @Test
  void shouldCreateCustomer() {
    customerService.createCustomer(new Customer(1L, "George"));

    Optional<Customer> customer = customerService.getCustomer(1L);
    assertTrue(customer.isPresent());
    assertEquals(1L, customer.get().id());
    assertEquals("George", customer.get().name());
  }

  @Test
  void shouldGetCustomers() {
    customerService.createCustomer(new Customer(1L, "George"));
    customerService.createCustomer(new Customer(2L, "John"));

    List<Customer> customers = customerService.getAllCustomers();
    assertEquals(2, customers.size());
  }
}
```

该代码的作用如下：

- `PostgreSQLContainer` 被声明为**静态字段**。容器在本类所有测试之前启动，并在之后停止。
- `@BeforeAll` 启动容器，`@AfterAll` 停止容器。
- `@BeforeEach` 使用容器的 JDBC 参数初始化 `CustomerService`，并删除所有行，让每个测试都拥有一个干净的数据库。

要点观察：

- 由于容器是**静态字段**，它在类的所有测试方法之间共享。你也可以将其声明为非静态字段，并使用 `@BeforeEach`/`@AfterEach` 为每个测试启动一个新容器，但不推荐这样做，因为资源消耗较大。
- 即使没有在 `@AfterAll` 中显式停止容器，Testcontainers 也会使用 [Ryuk 容器](https://github.com/testcontainers/moby-ryuk) 在 JVM 退出时自动清理容器。

## JUnit 5 扩展注解

Testcontainers 库提供了一个 JUnit 5 扩展，使用注解即可简化容器的启动和停止。要使用它，请添加 `org.testcontainers:testcontainers-junit-jupiter` 测试依赖。

```java
package com.testcontainers.demo;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.List;
import java.util.Optional;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.testcontainers.postgresql.PostgreSQLContainer;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;

@Testcontainers
class CustomerServiceWithJUnit5ExtensionTest {

  @Container
  static PostgreSQLContainer postgres = new PostgreSQLContainer(
    "postgres:16-alpine"
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
    customerService.deleteAllCustomers();
  }

  @Test
  void shouldCreateCustomer() {
    customerService.createCustomer(new Customer(1L, "George"));

    Optional<Customer> customer = customerService.getCustomer(1L);
    assertTrue(customer.isPresent());
    assertEquals(1L, customer.get().id());
    assertEquals("George", customer.get().name());
  }

  @Test
  void shouldGetCustomers() {
    customerService.createCustomer(new Customer(1L, "George"));
    customerService.createCustomer(new Customer(2L, "John"));

    List<Customer> customers = customerService.getAllCustomers();
    assertEquals(2, customers.size());
  }
}
```

类上的 `@Testcontainers` 注解和字段上的 `@Container` 注解会自动处理容器的启动和停止，无需再在 `@BeforeAll` 和 `@AfterAll` 中手动操作：

- 该扩展会找到所有带 `@Container` 注解的字段。
- **静态字段**在所有测试之前启动一次，并在所有测试之后停止。
- **实例字段**在每个测试之前启动，并在每个测试之后停止（不推荐——资源消耗较大）。

## 单例容器模式

随着测试类数量的增长，为每个类启动容器的开销会累积。单例容器模式会在公共基类中启动所有所需容器一次，并在所有集成测试中复用它们。

### 定义基类

创建一个抽象基类，在静态初始化块中启动容器：

```java
package com.testcontainers.demo;

import org.testcontainers.postgresql.PostgreSQLContainer;
import org.testcontainers.kafka.ConfluentKafkaContainer;

public abstract class AbstractIntegrationTest {

   static PostgreSQLContainer postgres = new PostgreSQLContainer(
           "postgres:16-alpine");
   static ConfluentKafkaContainer kafka = new ConfluentKafkaContainer(
           "confluentinc/cp-kafka:7.8.0");

   static {
       postgres.start();
       kafka.start();
   }
}
```

容器在类加载时启动一次，Testcontainers 会使用 [Ryuk 容器](https://github.com/testcontainers/moby-ryuk) 在 JVM 退出后移除它们。

> [!TIP]
> 与其顺序启动容器，不如使用 `Startables.deepStart(postgres, kafka).join();` 并行启动它们。

### 继承基类

每个测试类都继承自基类，并复用相同的容器：

```java
class ProductControllerTest extends AbstractIntegrationTest {

   ProductRepository productRepository;

   @BeforeEach
   void setUp() {
       productRepository = new ProductRepository(...);
       productRepository.deleteAll();
   }

   @Test
   void shouldGetAllProducts() {
       // 使用共享的 postgres 容器的测试逻辑
   }
}
```

### 避免常见的错误配置

一个常见错误是将单例容器与 `@Testcontainers` 和 `@Container` 注解混用：

```java
// 不要这样做 —— 容器会在每个测试类结束后被停止
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@Testcontainers
public abstract class AbstractIntegrationTest {

   @Container
   static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>(
           DockerImageName.parse("postgres:16-alpine"));

   @DynamicPropertySource
   static void configureProperties(DynamicPropertyRegistry registry) {
       registry.add("spring.datasource.url", postgres::getJdbcUrl);
       registry.add("spring.datasource.username", postgres::getUsername);
       registry.add("spring.datasource.password", postgres::getPassword);
   }
}
```

`@Testcontainers` 扩展会在**每个测试类**结束时停止容器。后续的测试类会复用缓存的 Spring 上下文，但容器已经被停止——从而导致连接失败。

反之，应使用静态初始化块或 `@BeforeAll` 来启动容器，且不带 `@Testcontainers` 和 `@Container` 注解。

### 小结

- 使用 **JUnit 5 生命周期回调**（`@BeforeAll`/`@AfterAll`）来显式控制容器的启动与关闭。
- 使用 **扩展注解**（`@Testcontainers`/`@Container`）来减少单个测试类中的样板代码。
- 使用 **单例容器模式**（基类中的静态初始化块）在多个测试类之间共享容器。
- 不要将单例容器与 `@Testcontainers`/`@Container` 注解混用。

### 延伸阅读

- [Testcontainers JUnit 5 快速入门](https://java.testcontainers.org/quickstart/junit_5_quickstart/)
- [Testcontainers 单例容器模式](https://java.testcontainers.org/test_framework_integration/manual_lifecycle_control/#singleton-containers)
- [使用 Testcontainers 测试 Spring Boot REST API](/guides/testcontainers-java-spring-boot-rest-api/)

