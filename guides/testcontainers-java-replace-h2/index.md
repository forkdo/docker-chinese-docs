# 

<!-- FILE: guides/testcontainers-java-replace-h2.md -->

---
title: 用真实数据库替换 H2 进行测试
linkTitle: 替换 H2 数据库
description: 了解如何使用 Testcontainers 将 H2 内存数据库替换为真实的 PostgreSQL 数据库进行测试。
keywords: testcontainers, java, testing, h2, postgresql, spring boot, spring data jpa, jdbc
summary: |
  使用 Testcontainers 的专用 JDBC URL（一行改动）将 H2 内存测试数据库替换为真实的
  PostgreSQL 实例。
aliases:
  - /guides/testcontainers-java-replace-h2/jdbc-url-approach/
  - /guides/testcontainers-java-replace-h2/junit-extension-approach/
  - /guides/testcontainers-java-replace-h2/problem-with-h2/
params:
  tags: [testing]
  time: 15 minutes
---


<!-- Source: https://github.com/testcontainers/tc-guide-replace-h2-with-real-database-for-testing -->

在本指南中，你将学习如何：

- 了解使用 H2 内存数据库进行测试的缺陷
- 使用 Testcontainers 的专用 JDBC URL 将 H2 替换为真实的 PostgreSQL 数据库
- 使用 Testcontainers 的 JUnit 5 扩展以获得对容器的更多控制
- 测试基于 Spring Data JPA 和 JdbcTemplate 的仓储

## 先决条件

- Java 17+
- Maven 或 Gradle
- 一个受 Testcontainers 支持的 Docker 环境

> [!NOTE]
> 如果你刚接触 Testcontainers，请访问
> [Testcontainers 概览](https://testcontainers.com/getting-started/) 了解
> Testcontainers 及其使用优势。

## 使用 H2 进行测试的问题

一种常见做法是在测试时使用 H2 或 HSQL 这类轻量级数据库作为内存数据库，而在生产环境中
使用 PostgreSQL、MySQL 或 Oracle。这种方式存在显著的缺陷：

- 测试数据库可能不支持生产数据库的所有特性。
- H2 与生产数据库之间的 SQL 语法可能不兼容。
- 在 H2 上通过的测试并不能保证在生产环境中也能正常工作。

### 示例：PostgreSQL 专有语法

考虑实现一个"upsert"——仅在产品不存在时才插入。在 PostgreSQL 中，你可以使用：

```sql
INSERT INTO products(id, code, name) VALUES(?,?,?) ON CONFLICT DO NOTHING;
```

该查询在 H2 中默认无法工作：

```text
Caused by: org.h2.jdbc.JdbcSQLException: Syntax error in SQL statement
"INSERT INTO products (id, code, name) VALUES (?, ?, ?) ON[*] CONFLICT DO NOTHING";
```

你可以让 H2 以 PostgreSQL 兼容模式运行，但并非所有特性都受支持。反之亦然——H2 支持的
`ROWNUM()` 在 PostgreSQL 中并不支持。

使用与生产环境不同的数据库进行测试，意味着你无法信任测试结果，必须在部署后再进行验证，
这有违自动化测试的初衷。

### 使用 H2 的 Spring Boot 测试

一个典型的基于 H2 的测试如下所示：

```java
@DataJpaTest
class ProductRepositoryTest {

   @Autowired
   ProductRepository productRepository;

   @Test
   @Sql("classpath:/sql/seed-data.sql")
   void shouldGetAllProducts() {
       List<Product> products = productRepository.findAll();
       assertEquals(2, products.size());
   }
}
```

当 H2 位于 classpath 上时，Spring Boot 会自动使用它。测试能够通过的，但它不会捕获
PostgreSQL 专有的问题。

## 使用 Testcontainers 的 JDBC URL 替换 H2

将 H2 替换为真实的 PostgreSQL 数据库只需要两个测试属性：

```java
@DataJpaTest
@TestPropertySource(properties = {
  "spring.test.database.replace=none",
  "spring.datasource.url=jdbc:tc:postgresql:16-alpine:///db"
})
class ProductRepositoryWithJdbcUrlTest {

  @Autowired
  ProductRepository productRepository;

  @Test
  @Sql("classpath:/sql/seed-data.sql")
  void shouldGetAllProducts() {
    List<Product> products = productRepository.findAll();
    assertEquals(2, products.size());
  }
}
```

就这些——两个属性，你的测试就会针对真实的 PostgreSQL 数据库运行。

### 专用 JDBC URL 的工作原理

标准的 PostgreSQL JDBC URL 如下所示：

```text
jdbc:postgresql://localhost:5432/postgres
```

Testcontainers 的专用 JDBC URL 在 `jdbc:` 之后插入 `tc:`：

```text
jdbc:tc:postgresql:///db
```

主机名、端口和数据库名都会被忽略——Testcontainers 会自动管理它们。你可以在数据库名之后
指定 Docker 镜像标签：

```text
jdbc:tc:postgresql:16-alpine:///db
```

这会基于 `postgres:16-alpine` 镜像创建一个容器。

### 使用脚本初始化数据库

传入 `TC_INITSCRIPT`，可在容器启动时运行一个 SQL 脚本：

```text
jdbc:tc:postgresql:16-alpine:///db?TC_INITSCRIPT=sql/init-db.sql
```

Testcontainers 会自动运行该脚本。对于生产应用，请改用 Flyway 或 Liquibase 之类的
数据库迁移工具。

该专用 JDBC URL 同样适用于 MySQL、MariaDB、PostGIS、YugabyteDB、CockroachDB，以及其他
具备 Testcontainers JDBC 支持的数据库。

### 测试基于 JdbcTemplate 的仓储

同样的方法适用于基于 `JdbcTemplate` 的仓储。使用 `@JdbcTest` 代替 `@DataJpaTest`：

```java
@JdbcTest
@TestPropertySource(properties = {
  "spring.test.database.replace=none",
  "spring.datasource.url=jdbc:tc:postgresql:16-alpine:///db?TC_INITSCRIPT=sql/init-db.sql"
})
class JdbcProductRepositoryTest {

  @Autowired
  private JdbcTemplate jdbcTemplate;

  private JdbcProductRepository productRepository;

  @BeforeEach
  void setUp() {
    productRepository = new JdbcProductRepository(jdbcTemplate);
  }

  @Test
  @Sql("/sql/seed-data.sql")
  void shouldGetAllProducts() {
    List<Product> products = productRepository.getAllProducts();
    assertEquals(2, products.size());
  }
}
```

## 使用 JUnit 5 扩展获得更多控制

如果专用 JDBC URL 无法满足你的需求，或者你需要对容器的创建进行更多控制（例如复制初始化
脚本），可以使用 Testcontainers 的 JUnit 5 扩展：

```java
@DataJpaTest
@TestPropertySource(properties = {
    "spring.test.database.replace=none"
})
@Testcontainers
class ProductRepositoryTest {

  @Container
  static PostgreSQLContainer postgres =
    new PostgreSQLContainer("postgres:16-alpine")
      .withCopyFileToContainer(
        MountableFile.forClasspathResource("sql/init-db.sql"),
        "/docker-entrypoint-initdb.d/init-db.sql");

  @DynamicPropertySource
  static void configureProperties(DynamicPropertyRegistry registry) {
    registry.add("spring.datasource.url", postgres::getJdbcUrl);
    registry.add("spring.datasource.username", postgres::getUsername);
    registry.add("spring.datasource.password", postgres::getPassword);
  }

  @Autowired
  ProductRepository productRepository;

  @Test
  @Sql("/sql/seed-data.sql")
  void shouldGetAllProducts() {
    List<Product> products = productRepository.findAll();
    assertEquals(2, products.size());
  }

  @Test
  @Sql("/sql/seed-data.sql")
  void shouldNotCreateAProductWithDuplicateCode() {
    Product product = new Product(3L, "p101", "Test Product");
    productRepository.createProductIfNotExists(product);
    Optional<Product> optionalProduct = productRepository.findById(
      product.getId()
    );
    assertThat(optionalProduct).isEmpty();
  }
}
```

这种方式：

- 使用 `@Testcontainers` 和 `@Container` 管理容器生命周期。
- 将 `init-db.sql` 复制到容器的初始化目录，使 PostgreSQL 在启动时运行它。
- 使用 `@DynamicPropertySource` 将容器的连接信息注册到 Spring Boot。
- 测试 PostgreSQL 专有特性（如 `ON CONFLICT DO NOTHING`），这些在 H2 中是无法工作的。

### 小结

- 使用**专用 JDBC URL**（`jdbc:tc:postgresql:...`）是从 H2 切换到真实数据库最快捷的方式——
  只需改动一个属性。
- 当你需要对容器进行更多控制（自定义初始化脚本、环境变量等）时，使用 **JUnit 5 扩展**。
- 这两种方式都适用于 Spring Data JPA（`@DataJpaTest`）和 JdbcTemplate（`@JdbcTest`）测试。

### 延伸阅读

- [Testcontainers Postgres 模块](https://java.testcontainers.org/modules/databases/postgres/)
- [Testcontainers JDBC 支持](https://java.testcontainers.org/modules/databases/jdbc/)
- [使用 Testcontainers 测试 Spring Boot REST API](/guides/testcontainers-java-spring-boot-rest-api/)

