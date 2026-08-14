# Testcontainers for Java 入门



<!-- Source: https://github.com/testcontainers/tc-guide-getting-started-with-testcontainers-for-java -->

在本指南中，你将学习如何：

- 使用 Maven 创建一个 Java 项目
- 实现一个在 PostgreSQL 中管理客户记录的 `CustomerService`
- 使用 Testcontainers 配合真实的 Postgres 数据库编写集成测试
- 运行测试并验证一切正常工作

## 先决条件

- Java 17+
- Maven 或 Gradle
- Testcontainers 支持的 Docker 环境

> [!NOTE]
> 如果你是 Testcontainers 的新手，请访问
> [Testcontainers 概览](https://testcontainers.com/getting-started/) 以了解更多关于
> Testcontainers 及其优势的信息。

## 创建 Java 项目

### 设置 Maven 项目

从你偏好的 IDE 中创建一个使用 Maven 的 Java 项目。本指南使用 Maven，但如果你愿意也可以使用 Gradle。向 `pom.xml` 添加以下依赖：

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
</dependencies>

<build>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-surefire-plugin</artifactId>
            <version>3.2.5</version>
        </plugin>
    </plugins>
</build>
```

这会添加 Postgres JDBC 驱动、用于日志记录的 logback、用于测试的 JUnit 5，以及用于支持 JUnit 5 的最新 `maven-surefire-plugin`。

### 实现业务逻辑

创建一个 `Customer` 记录：

```java
package com.testcontainers.demo;

public record Customer(Long id, String name) {}
```

创建一个 `DBConnectionProvider` 类来保存 JDBC 连接参数并提供数据库 `Connection`：

```java
package com.testcontainers.demo;

import java.sql.Connection;
import java.sql.DriverManager;

class DBConnectionProvider {

  private final String url;
  private final String username;
  private final String password;

  public DBConnectionProvider(String url, String username, String password) {
    this.url = url;
    this.username = username;
    this.password = password;
  }

  Connection getConnection() {
    try {
      return DriverManager.getConnection(url, username, password);
    } catch (Exception e) {
      throw new RuntimeException(e);
    }
  }
}
```

创建 `CustomerService` 类：

```java
package com.testcontainers.demo;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

public class CustomerService {

  private final DBConnectionProvider connectionProvider;

  public CustomerService(DBConnectionProvider connectionProvider) {
    this.connectionProvider = connectionProvider;
    createCustomersTableIfNotExists();
  }

  public void createCustomer(Customer customer) {
    try (Connection conn = this.connectionProvider.getConnection()) {
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

    try (Connection conn = this.connectionProvider.getConnection()) {
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

  private void createCustomersTableIfNotExists() {
    try (Connection conn = this.connectionProvider.getConnection()) {
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
}
```

`CustomerService` 的作用是：

- 构造函数调用 `createCustomersTableIfNotExists()` 以确保表存在。
- `createCustomer()` 向数据库插入一条客户记录。
- `getAllCustomers()` 从 `customers` 表获取所有行，并返回一个 `Customer` 对象列表。

## 使用 Testcontainers 编写测试

你已经准备好 `CustomerService` 实现，但测试需要一个 PostgreSQL 数据库。你可以使用 Testcontainers 在 Docker 容器中启动一个 Postgres 数据库，并针对它运行测试。

### 添加 Testcontainers 依赖

在 `pom.xml` 中将 Testcontainers PostgreSQL 模块添加为测试依赖：

```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>testcontainers-postgresql</artifactId>
    <version>2.0.4</version>
    <scope>test</scope>
</dependency>
```

由于该应用使用 Postgres 数据库，Testcontainers Postgres 模块提供了用于管理容器的 `PostgreSQLContainer` 类。

### 编写测试

在 `src/test/java` 下创建 `CustomerServiceTest.java`：

```java
package com.testcontainers.demo;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.List;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.testcontainers.postgresql.PostgreSQLContainer;

class CustomerServiceTest {

  static PostgreSQLContainer postgres = new PostgreSQLContainer(
    "postgres:16-alpine"
  );

  CustomerService customerService;

  @BeforeAll
  static void beforeAll() {
    postgres.start();
  }

  @AfterAll
  static void afterAll() {
    postgres.stop();
  }

  @BeforeEach
  void setUp() {
    DBConnectionProvider connectionProvider = new DBConnectionProvider(
      postgres.getJdbcUrl(),
      postgres.getUsername(),
      postgres.getPassword()
    );
    customerService = new CustomerService(connectionProvider);
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

该测试的作用是：

- 声明一个使用 `postgres:16-alpine` Docker 镜像的 `PostgreSQLContainer`。
- `@BeforeAll` 回调在任何测试方法运行之前启动 Postgres 容器。
- `@BeforeEach` 回调使用来自容器的 JDBC 连接参数创建一个 `DBConnectionProvider`，然后创建一个 `CustomerService`。`CustomerService` 构造函数会在表不存在时创建 `customers` 表。
- `shouldGetCustomers()` 插入 2 条客户记录，获取所有客户，并断言数量。
- `@AfterAll` 回调在所有测试方法完成后停止容器。

## 运行测试与后续步骤

### 运行测试

使用 Maven 运行测试：

```console
$ mvn test
```

你可以在日志中看到 Testcontainers 从 Docker Hub 拉取 Postgres Docker 镜像（如果本地尚不可用），启动容器，并运行测试。

使用 Testcontainers 编写集成测试与你从 IDE 运行的单元测试并无二致。你的团队成员可以克隆项目并运行测试，而无需在机器上安装 Postgres。

### 小结

Testcontainers for Java 库帮助你编写使用与生产相同类型数据库（Postgres）的集成测试，而不是使用 mock。由于你没有使用 mock，而是与真实服务通信，因此你可以自由重构代码，同时仍能验证应用按预期工作。

除了 Postgres，Testcontainers 还为许多 SQL 数据库、NoSQL 数据库、消息队列等提供了专用模块。你可以使用 Testcontainers 运行测试所需的任何容器化依赖。

要了解更多关于 Testcontainers 的信息，请访问
[Testcontainers 概览](https://testcontainers.com/getting-started/)。

### 延伸阅读

- [使用 JUnit 5 管理 Testcontainers 容器生命周期](https://testcontainers.com/guides/testcontainers-container-lifecycle/)
- [用真实数据库替换 H2 进行测试](https://testcontainers.com/guides/replace-h2-with-real-database-for-testing/)
- [在 Java Spring Boot 项目中开始使用 Testcontainers](https://testcontainers.com/guides/testing-spring-boot-rest-api-using-testcontainers/)

