<!-- FILE: guides/testcontainers-java-quarkus.md -->

---
title: 使用 Testcontainers 测试 Quarkus 应用
linkTitle: Quarkus
description: 了解如何使用 Testcontainers 配合 PostgreSQL、Hibernate ORM with Panache 和 REST Assured 测试 Quarkus REST API。
keywords: testcontainers, java, quarkus, testing, postgresql, rest api, rest assured, panache, dev services
summary: |
  了解如何创建一个使用 Hibernate ORM with Panache 与 PostgreSQL 的 Quarkus REST API，
  然后使用 Quarkus Dev Services、Testcontainers 和 REST Assured 对其进行测试。
aliases:
  - /guides/testcontainers-java-quarkus/create-project/
  - /guides/testcontainers-java-quarkus/run-tests/
  - /guides/testcontainers-java-quarkus/write-tests/
params:
  tags: [testing]
  time: 25 minutes
---


<!-- Source: https://github.com/testcontainers/tc-guide-testcontainers-in-quarkus-applications -->

在本指南中，你将学习如何：

- 创建一个带有 REST API 端点的 Quarkus 应用
- 使用 Hibernate ORM with Panache 与 PostgreSQL 进行持久化
- 使用 Quarkus Dev Services（其底层使用 Testcontainers）测试 REST API
- 使用 `QuarkusTestResourceLifecycleManager` 测试 Dev Services 不支持的服务

## 先决条件

- Java 17+
- Maven 或 Gradle
- 一个受 Testcontainers 支持的 Docker 环境

> [!NOTE]
> 如果你刚接触 Testcontainers，请访问
> [Testcontainers 概览](https://testcontainers.com/getting-started/) 了解
> Testcontainers 及其使用优势。

## 创建 Quarkus 项目

### 搭建项目

在 [code.quarkus.io](https://code.quarkus.io/) 上创建一个 Quarkus 项目，勾选
**RESTEasy Classic**、**RESTEasy Classic Jackson**、**Hibernate Validator**、
**Hibernate ORM with Panache**、**JDBC Driver - PostgreSQL** 以及 **Flyway** 这几个
扩展（extension）。

或者，克隆
[指南仓库](https://github.com/testcontainers/tc-guide-testcontainers-in-quarkus-applications)。

`pom.xml` 中的关键依赖如下：

```xml
<properties>
    <quarkus.platform.version>3.22.3</quarkus.platform.version>
</properties>
<dependencies>
    <dependency>
        <groupId>io.quarkus</groupId>
        <artifactId>quarkus-hibernate-orm-panache</artifactId>
    </dependency>
    <dependency>
        <groupId>io.quarkus</groupId>
        <artifactId>quarkus-flyway</artifactId>
    </dependency>
    <dependency>
        <groupId>io.quarkus</groupId>
        <artifactId>quarkus-hibernate-validator</artifactId>
    </dependency>
    <dependency>
        <groupId>io.quarkus</groupId>
        <artifactId>quarkus-resteasy</artifactId>
    </dependency>
    <dependency>
        <groupId>io.quarkus</groupId>
        <artifactId>quarkus-resteasy-jackson</artifactId>
    </dependency>
    <dependency>
        <groupId>io.quarkus</groupId>
        <artifactId>quarkus-jdbc-postgresql</artifactId>
    </dependency>
    <dependency>
        <groupId>io.quarkus</groupId>
        <artifactId>quarkus-junit5</artifactId>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>io.rest-assured</groupId>
        <artifactId>rest-assured</artifactId>
        <scope>test</scope>
    </dependency>
</dependencies>
```

### 创建 JPA 实体

Hibernate ORM with Panache 支持 Active Record 模式和 Repository 模式，以简化 JPA 的
使用。本指南使用 Active Record 模式。

通过继承 `PanacheEntity` 创建 `Customer.java`。这会让实体获得内置的持久化方法，例如
`persist()`、`listAll()` 和 `findById()`。

```java
package com.testcontainers.demo;

import io.quarkus.hibernate.orm.panache.PanacheEntity;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Table;

@Entity
@Table(name = "customers")
public class Customer extends PanacheEntity {

    @Column(nullable = false)
    public String name;

    @Column(nullable = false, unique = true)
    public String email;

    public Customer() {}

    public Customer(Long id, String name, String email) {
        this.id = id;
        this.name = name;
        this.email = email;
    }
}
```

### 创建 CustomerService CDI bean

创建一个标注了 `@ApplicationScoped` 和 `@Transactional` 的 `CustomerService` 类，用于
处理持久化操作：

```java
package com.testcontainers.demo;

import jakarta.enterprise.context.ApplicationScoped;
import jakarta.transaction.Transactional;
import java.util.List;

@ApplicationScoped
@Transactional
public class CustomerService {

    public List<Customer> getAll() {
        return Customer.listAll();
    }

    public Customer create(Customer customer) {
        customer.persist();
        return customer;
    }
}
```

### 添加 Flyway 数据库迁移脚本

创建 `src/main/resources/db/migration/V1__init_database.sql`：

```sql
create sequence customers_seq start with 1 increment by 50;

create table customers
(
    id    bigint DEFAULT nextval('customers_seq') not null,
    name  varchar                                 not null,
    email varchar                                 not null,
    primary key (id)
);

insert into customers(name, email)
values ('john', 'john@mail.com'),
       ('rambo', 'rambo@mail.com');
```

在 `src/main/resources/application.properties` 中启用 Flyway 迁移：

```properties
quarkus.flyway.migrate-at-start=true
```

### 创建 REST API 端点

创建 `CustomerResource.java`，包含获取所有客户和创建客户的端点：

```java
package com.testcontainers.demo;

import jakarta.ws.rs.Consumes;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.POST;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;
import java.util.List;

@Path("/api/customers")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class CustomerResource {
    private final CustomerService customerService;

    public CustomerResource(CustomerService customerService) {
        this.customerService = customerService;
    }

    @GET
    public List<Customer> getAllCustomers() {
        return customerService.getAll();
    }

    @POST
    public Response createCustomer(Customer customer) {
        var savedCustomer = customerService.create(customer);
        return Response.status(Response.Status.CREATED).entity(savedCustomer).build();
    }
}
```

## 使用 Testcontainers 编写测试

### Quarkus Dev Services

Quarkus Dev Services 会在开发和测试模式下自动配置（provision）未显式配置的服务。当你
引入某个扩展却没有对其进行配置时，Quarkus 会在底层使用
[Testcontainers](https://www.testcontainers.org/) 启动相关服务，并将应用连接以使用该
服务。

> [!NOTE]
> Dev Services 需要
> [受支持的 Docker 环境](https://www.testcontainers.org/supported_docker_environment/)。

Quarkus Dev Services 支持大多数常用服务，如 SQL 数据库、Kafka、RabbitMQ、Redis 和
MongoDB。更多信息请参阅 [Quarkus Dev Services 指南](https://quarkus.io/guides/dev-services)。

### 编写 API 端点的测试

使用 REST Assured 测试 `GET /api/customers` 和 `POST /api/customers` 端点。在生成项目
时，`io.rest-assured:rest-assured` 库已被添加为测试依赖。

创建 `CustomerResourceTest.java` 并使用 `@QuarkusTest` 注解。这会借助 Dev Services 启动
应用以及所需的服务。由于你还没有配置数据源属性，Dev Services 会自动使用 Testcontainers
启动一个 PostgreSQL 数据库。

```java
package com.testcontainers.demo;

import static io.restassured.RestAssured.given;
import static org.hamcrest.CoreMatchers.is;
import static org.junit.jupiter.api.Assertions.assertFalse;

import io.quarkus.test.junit.QuarkusTest;
import io.restassured.common.mapper.TypeRef;
import io.restassured.http.ContentType;
import java.util.List;
import org.junit.jupiter.api.Test;

@QuarkusTest
class CustomerResourceTest {

    @Test
    void shouldGetAllCustomers() {
        List<Customer> customers = given().when()
                .get("/api/customers")
                .then()
                .statusCode(200)
                .extract()
                .as(new TypeRef<>() {});
        assertFalse(customers.isEmpty());
    }

    @Test
    void shouldCreateCustomerSuccessfully() {
        Customer customer = new Customer(null, "John", "john@gmail.com");
        given().contentType(ContentType.JSON)
                .body(customer)
                .when()
                .post("/api/customers")
                .then()
                .statusCode(201)
                .body("name", is("John"))
                .body("email", is("john@gmail.com"));
    }
}
```

该测试的作用如下：

- `@QuarkusTest` 启动启用了 Dev Services 的完整 Quarkus 应用。
- Dev Services 使用 Testcontainers 启动一个 PostgreSQL 容器，并自动配置数据源。
- `shouldGetAllCustomers()` 调用 `GET /api/customers`，并验证返回了来自 Flyway 迁移的
  种子数据。
- `shouldCreateCustomerSuccessfully()` 发送一个 `POST /api/customers` 请求，并验证响应
  包含所创建的客户数据。

### 自定义测试配置

默认情况下，Quarkus 测试实例在 8081 端口启动，并使用 `postgres:14` Docker 镜像。
通过在 `src/main/resources/application.properties` 中添加以下属性来同时自定义二者：

```properties
quarkus.http.test-port=0
quarkus.datasource.devservices.image-name=postgres:15.2-alpine
```

将 `quarkus.http.test-port=0` 设为 0 会让应用在随机可用端口上启动，避免端口冲突。
`devservices.image-name` 属性让你能将 PostgreSQL 镜像固定到与生产环境匹配的特定版本。

### 测试 Dev Services 不支持的服务

你的应用可能使用 Dev Services 开箱即不支持的服务。在这种情况下，可使用
`QuarkusTestResourceLifecycleManager` 在 Quarkus 应用启动以进行测试之前启动该服务。

例如，假设应用使用 CockroachDB。首先，添加 CockroachDB 的 Testcontainers 模块依赖：

```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>cockroachdb</artifactId>
    <scope>test</scope>
</dependency>
```

创建一个实现了 `QuarkusTestResourceLifecycleManager` 的 `CockroachDBTestResource`：

```java
package com.testcontainers.demo;

import io.quarkus.test.common.QuarkusTestResourceLifecycleManager;
import java.util.HashMap;
import java.util.Map;
import org.testcontainers.containers.CockroachContainer;

public class CockroachDBTestResource implements QuarkusTestResourceLifecycleManager {

    CockroachContainer cockroachdb;

    @Override
    public Map<String, String> start() {
        cockroachdb = new CockroachContainer("cockroachdb/cockroach:v22.2.0");
        cockroachdb.start();
        Map<String, String> conf = new HashMap<>();
        conf.put("quarkus.datasource.jdbc.url", cockroachdb.getJdbcUrl());
        conf.put("quarkus.datasource.username", cockroachdb.getUsername());
        conf.put("quarkus.datasource.password", cockroachdb.getPassword());
        return conf;
    }

    @Override
    public void stop() {
        cockroachdb.stop();
    }
}
```

在测试类中使用 `@QuarkusTestResource` 配合 `CockroachDBTestResource`：

```java
package com.testcontainers.demo;

import static io.restassured.RestAssured.given;
import static org.junit.jupiter.api.Assertions.assertFalse;

import io.quarkus.test.common.QuarkusTestResource;
import io.quarkus.test.junit.QuarkusTest;
import io.restassured.common.mapper.TypeRef;
import java.util.List;
import org.junit.jupiter.api.Test;

@QuarkusTest
@QuarkusTestResource(value = CockroachDBTestResource.class, restrictToAnnotatedClass = true)
class CockroachDBTest {

    @Test
    void shouldGetAllCustomers() {
        List<Customer> customers = given().when()
                .get("/api/customers")
                .then()
                .statusCode(200)
                .extract()
                .as(new TypeRef<>() {});
        assertFalse(customers.isEmpty());
    }
}
```

`restrictToAnnotatedClass = true` 属性确保 CockroachDB 容器只在运行这个特定测试类时
启动，而不是对所有测试都激活。

## 运行测试与后续步骤

### 运行测试

```console
$ ./mvnw test
```

或者使用 Gradle：

```console
$ ./gradlew test
```

你应该会看到 PostgreSQL 的 Docker 容器启动，并且所有测试通过。测试结束后，容器会
自动停止并被移除。

### 在本地运行应用

Quarkus Dev Services 会在开发模式下自动配置未显式配置的服务。以开发模式启动 Quarkus
应用：

```console
$ ./mvnw compile quarkus:dev
```

或者使用 Gradle：

```console
$ ./gradlew quarkusDev
```

Dev Services 会自动启动一个 PostgreSQL 容器。如果你本机已经运行了一个 PostgreSQL 数据库
并希望改用它，请在 `src/main/resources/application.properties` 中配置数据源属性：

```properties
quarkus.datasource.jdbc.url=jdbc:postgresql://localhost:5432/postgres
quarkus.datasource.username=postgres
quarkus.datasource.password=postgres
```

当这些属性被显式设置时，Dev Services 不会再配置数据库容器，而是连接到所配置的数据库。

### 小结

Quarkus Dev Services 通过在开发和测试期间使用 Testcontainers 自动配置所需服务，改善了
开发体验。本指南涵盖了：

- 使用 JAX-RS 与 Hibernate ORM with Panache 构建 REST API
- 在 Dev Services 负责数据库配置的同时，使用 REST Assured 测试 API 端点
- 针对 Dev Services 不支持的服务使用 `QuarkusTestResourceLifecycleManager`
- 借助 Dev Services 在本地运行应用

想进一步了解 Testcontainers，请访问
[Testcontainers 概览](https://testcontainers.com/getting-started/)。

### 延伸阅读

- [Quarkus Dev Services 概述](https://quarkus.io/guides/dev-services)
- [Quarkus 测试指南](https://quarkus.io/guides/getting-started-testing)
- [Testcontainers Postgres 模块](https://java.testcontainers.org/modules/databases/postgres/)
