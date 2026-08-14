<!-- FILE: guides/testcontainers-java-micronaut-kafka.md -->

---
title: 使用 Testcontainers 测试 Micronaut Kafka 监听器
linkTitle: Micronaut Kafka
description: 了解如何使用 Testcontainers 的 Kafka 与 MySQL 模块测试 Micronaut Kafka 监听器。
keywords: testcontainers, java, micronaut, testing, kafka, mysql, jpa, awaitility
summary: |
  了解如何创建一个带有 Kafka 监听器、并将数据持久化到 MySQL 的 Micronaut 应用，
  然后使用 Testcontainers 的 Kafka 与 MySQL 模块配合 Awaitility 对其进行测试。
aliases:
  - /guides/testcontainers-java-micronaut-kafka/create-project/
  - /guides/testcontainers-java-micronaut-kafka/run-tests/
  - /guides/testcontainers-java-micronaut-kafka/write-tests/
params:
  tags: [testing]
  time: 25 minutes
---


<!-- Source: https://github.com/testcontainers/tc-guide-testing-micronaut-kafka-listener -->

在本指南中，你将学习如何：

- 创建一个集成了 Kafka 的 Micronaut 应用
- 实现一个 Kafka 监听器并将数据持久化到 MySQL 数据库
- 使用 Testcontainers 与 Awaitility 测试该 Kafka 监听器

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
勾选 **kafka**、**data-jpa**、**mysql**、**awaitility**、**assertj** 以及
**testcontainers** 这些特性（feature）。

或者，克隆
[指南仓库](https://github.com/testcontainers/tc-guide-testing-micronaut-kafka-listener)。

你将使用 [Awaitility](http://www.awaitility.org/) 库来断言一个异步流程的预期结果。

`pom.xml` 中的关键依赖如下：

```xml
<parent>
    <groupId>io.micronaut.platform</groupId>
    <artifactId>micronaut-parent</artifactId>
    <version>4.1.4</version>
</parent>
<dependencies>
    <dependency>
        <groupId>io.micronaut.data</groupId>
        <artifactId>micronaut-data-hibernate-jpa</artifactId>
        <scope>compile</scope>
    </dependency>
    <dependency>
        <groupId>io.micronaut.kafka</groupId>
        <artifactId>micronaut-kafka</artifactId>
        <scope>compile</scope>
    </dependency>
    <dependency>
        <groupId>io.micronaut.serde</groupId>
        <artifactId>micronaut-serde-jackson</artifactId>
        <scope>compile</scope>
    </dependency>
    <dependency>
        <groupId>io.micronaut.sql</groupId>
        <artifactId>micronaut-jdbc-hikari</artifactId>
        <scope>compile</scope>
    </dependency>
    <dependency>
        <groupId>mysql</groupId>
        <artifactId>mysql-connector-java</artifactId>
        <scope>runtime</scope>
    </dependency>
    <dependency>
        <groupId>org.awaitility</groupId>
        <artifactId>awaitility</artifactId>
        <version>4.2.0</version>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.testcontainers</groupId>
        <artifactId>testcontainers-junit-jupiter</artifactId>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.testcontainers</groupId>
        <artifactId>testcontainers-kafka</artifactId>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.testcontainers</groupId>
        <artifactId>testcontainers-mysql</artifactId>
        <scope>test</scope>
    </dependency>
</dependencies>
```

Micronaut 的 parent POM 管理了 Testcontainers 的 BOM，因此你无需为每个
Testcontainers 模块单独指定版本。

### 创建 JPA 实体

该应用会监听一个名为 `product-price-changes` 的主题（topic）。当消息到达时，它会从
事件负载中提取产品编码和价格，并更新 MySQL 数据库中该产品的价格。

创建 `Product.java`：

```java
package com.testcontainers.demo;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import java.math.BigDecimal;

@Entity
@Table(name = "products")
public class Product {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private String code;

    @Column(nullable = false)
    private String name;

    @Column(nullable = false)
    private BigDecimal price;

    public Product() {}

    public Product(Long id, String code, String name, BigDecimal price) {
        this.id = id;
        this.code = code;
        this.name = name;
        this.price = price;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getCode() {
        return code;
    }

    public void setCode(String code) {
        this.code = code;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public BigDecimal getPrice() {
        return price;
    }

    public void setPrice(BigDecimal price) {
        this.price = price;
    }
}
```

### 创建 Micronaut Data JPA 仓储

为 `Product` 实体创建一个仓储接口，包含按编码查找产品以及更新指定产品编码价格的方法：

```java
package com.testcontainers.demo;

import io.micronaut.data.annotation.Query;
import io.micronaut.data.annotation.Repository;
import io.micronaut.data.jpa.repository.JpaRepository;
import java.math.BigDecimal;
import java.util.Optional;

@Repository
public interface ProductRepository extends JpaRepository<Product, Long> {

    Optional<Product> findByCode(String code);

    @Query("update Product p set p.price = :price where p.code = :productCode")
    void updateProductPrice(String productCode, BigDecimal price);
}
```

与 Spring Data JPA 不同，Micronaut Data 使用编译期注解处理来实现仓储方法，避免了运行时反射。

### 创建事件负载

创建一个名为 `ProductPriceChangedEvent` 的 record，表示来自 Kafka 主题的事件负载结构：

```java
package com.testcontainers.demo;

import io.micronaut.serde.annotation.Serdeable;
import java.math.BigDecimal;

@Serdeable
public record ProductPriceChangedEvent(String productCode, BigDecimal price) {}
```

`@Serdeable` 注解告诉 Micronaut Serialization 该类型可以被序列化和反序列化。

发送方与接收方约定的 JSON 格式如下：

```json
{
  "productCode": "P100",
  "price": 25.0
}
```

### 实现 Kafka 监听器

创建 `ProductPriceChangedEventHandler.java`，处理来自 `product-price-changes`
主题的消息，并更新数据库中的产品价格：

```java
package com.testcontainers.demo;

import static io.micronaut.configuration.kafka.annotation.OffsetReset.EARLIEST;

import io.micronaut.configuration.kafka.annotation.KafkaListener;
import io.micronaut.configuration.kafka.annotation.Topic;
import jakarta.inject.Singleton;
import jakarta.transaction.Transactional;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@Singleton
@Transactional
class ProductPriceChangedEventHandler {

    private static final Logger LOG = LoggerFactory.getLogger(ProductPriceChangedEventHandler.class);

    private final ProductRepository productRepository;

    ProductPriceChangedEventHandler(ProductRepository productRepository) {
        this.productRepository = productRepository;
    }

    @Topic("product-price-changes")
    @KafkaListener(offsetReset = EARLIEST, groupId = "demo")
    public void handle(ProductPriceChangedEvent event) {
        LOG.info("Received a ProductPriceChangedEvent with productCode:{}: ", event.productCode());
        productRepository.updateProductPrice(event.productCode(), event.price());
    }
}
```

要点：

- `@KafkaListener` 注解将该类标记为 Kafka 消息监听器。将 `offsetReset` 设为 `EARLIEST`
  会让监听器从分区的起始位置开始消费消息，这在测试时很有用。
- `@Topic` 注解指定要订阅的主题。
- Micronaut 会使用 Micronaut Serialization 自动对 `ProductPriceChangedEvent` 进行
  JSON 反序列化。

### 配置数据源

在 `src/main/resources/application.properties` 中添加以下属性：

```properties
micronaut.application.name=tc-guide-testing-micronaut-kafka-listener
datasources.default.db-type=mysql
datasources.default.dialect=MYSQL
jpa.default.properties.hibernate.hbm2ddl.auto=update
jpa.default.entity-scan.packages=com.testcontainers.demo
datasources.default.driver-class-name=com.mysql.cj.jdbc.Driver
```

Hibernate 的 `hbm2ddl.auto=update` 会自动创建和更新数据库 schema。在测试时，你会在
测试属性文件中将其覆盖为 `create-drop`。

创建 `src/test/resources/application-test.properties`：

```properties
jpa.default.properties.hibernate.hbm2ddl.auto=create-drop
```

## 使用 Testcontainers 编写测试

要测试 Kafka 监听器，你需要一个运行中的 Kafka broker 和一个 MySQL 数据库，外加一个
启动的 Micronaut 应用上下文。Testcontainers 会在 Docker 容器中启动这两个服务，而
`TestPropertyProvider` 接口会将它们连接到 Micronaut。

### 创建用于测试的 Kafka 客户端

首先，创建一个 `@KafkaClient` 接口，用于在测试中发布事件：

```java
package com.testcontainers.demo;

import io.micronaut.configuration.kafka.annotation.KafkaClient;
import io.micronaut.configuration.kafka.annotation.KafkaKey;
import io.micronaut.configuration.kafka.annotation.Topic;

@KafkaClient
public interface ProductPriceChangesClient {

    @Topic("product-price-changes")
    void send(@KafkaKey String productCode, ProductPriceChangedEvent event);
}
```

要点：

- `@KafkaClient` 注解将该接口指定为 Kafka 生产者。
- `@Topic` 注解指定目标主题。
- `@KafkaKey` 注解标记用作 Kafka 消息键的参数。如果不存在这样的参数，Micronaut 会以
  null 键发送记录。

### 编写测试

创建 `ProductPriceChangedEventHandlerTest.java`：

```java
package com.testcontainers.demo;

import static java.util.concurrent.TimeUnit.SECONDS;
import static org.assertj.core.api.Assertions.assertThat;
import static org.awaitility.Awaitility.await;

import io.micronaut.context.annotation.Property;
import io.micronaut.core.annotation.NonNull;
import io.micronaut.test.extensions.junit5.annotation.MicronautTest;
import io.micronaut.test.support.TestPropertyProvider;
import java.math.BigDecimal;
import java.time.Duration;
import java.util.Collections;
import java.util.Map;
import java.util.Optional;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.TestInstance;
import org.testcontainers.kafka.ConfluentKafkaContainer;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;

@MicronautTest(transactional = false)
@Property(name = "datasources.default.driver-class-name", value = "org.testcontainers.jdbc.ContainerDatabaseDriver")
@Property(name = "datasources.default.url", value = "jdbc:tc:mysql:8.0.32:///db")
@Testcontainers(disabledWithoutDocker = true)
@TestInstance(TestInstance.Lifecycle.PER_CLASS)
class ProductPriceChangedEventHandlerTest implements TestPropertyProvider {

    @Container
    static final ConfluentKafkaContainer kafka = new ConfluentKafkaContainer("confluentinc/cp-kafka:7.8.0");

    @Override
    public @NonNull Map<String, String> getProperties() {
        if (!kafka.isRunning()) {
            kafka.start();
        }
        return Collections.singletonMap("kafka.bootstrap.servers", kafka.getBootstrapServers());
    }

    @Test
    void shouldHandleProductPriceChangedEvent(
            ProductPriceChangesClient productPriceChangesClient, ProductRepository productRepository) {
        Product product = new Product(null, "P100", "Product One", BigDecimal.TEN);
        Long id = productRepository.save(product).getId();

        ProductPriceChangedEvent event = new ProductPriceChangedEvent("P100", new BigDecimal("14.50"));

        productPriceChangesClient.send(event.productCode(), event);

        await().pollInterval(Duration.ofSeconds(3)).atMost(10, SECONDS).untilAsserted(() -> {
            Optional<Product> optionalProduct = productRepository.findByCode("P100");
            assertThat(optionalProduct).isPresent();
            assertThat(optionalProduct.get().getCode()).isEqualTo("P100");
            assertThat(optionalProduct.get().getPrice()).isEqualTo(new BigDecimal("14.50"));
        });

        productRepository.deleteById(id);
    }
}
```

该测试的作用如下：

- `@MicronautTest` 初始化 Micronaut 应用上下文和嵌入式服务器。将 `transactional` 设为
  `false` 可防止每个测试方法都在一个回滚的事务中运行，这对于 Kafka 监听器在独立线程中
  处理消息是必要的。
- `@Property` 注解覆盖了数据源的驱动和 URL，使其使用 Testcontainers 的专用 JDBC URL
  （`jdbc:tc:mysql:8.0.32:///db`）。这会启动一个 MySQL 容器，并将其自动配置为数据源。
- `@Testcontainers` 与 `@Container` 管理 Kafka 容器的生命周期。`TestPropertyProvider`
  接口将 Kafka bootstrap 服务器注册到 Micronaut，使生产者和消费者都能连接到测试容器。
- `@TestInstance(TestInstance.Lifecycle.PER_CLASS)` 为所有测试方法创建一个单一的测试
  实例，这是实现 `TestPropertyProvider` 所必需的。
- 该测试先在数据库中创建一个 `Product` 记录，然后使用 `ProductPriceChangesClient`
  向 `product-price-changes` 主题发送一个 `ProductPriceChangedEvent`。
- 由于 Kafka 消息处理是异步的，测试使用 [Awaitility](http://www.awaitility.org/)
  每 3 秒轮询一次（最多 10 秒），直到数据库中的产品价格与期望值匹配。

## 运行测试与后续步骤

### 运行测试

```console
$ ./mvnw test
```

或者使用 Gradle：

```console
$ ./gradlew test
```

你应该会看到 Kafka 和 MySQL 的 Docker 容器启动，并且所有测试通过。测试结束后，容器会
自动停止并被移除。

### 小结

相比 mock 或嵌入式替代方案，使用真实的 Kafka 和 MySQL 实例进行测试，能让你对代码的正确性
更有信心。Testcontainers 库管理着容器生命周期，使你的集成测试能够针对与生产环境相同的服务
运行。

想进一步了解 Testcontainers，请访问
[Testcontainers 概览](https://testcontainers.com/getting-started/)。

### 延伸阅读

- [在 Micronaut 应用中使用 WireMock 测试 REST API 集成](/guides/testcontainers-java-micronaut-wiremock/)
- [使用 Testcontainers 测试 Spring Boot Kafka 监听器](/guides/testcontainers-java-spring-boot-kafka/)
- [在 Java Spring Boot 项目中使用 Testcontainers 入门](https://testcontainers.com/guides/testing-spring-boot-rest-api-using-testcontainers/)
- [Awaitility](http://www.awaitility.org/)
- [Testcontainers Kafka 模块](https://java.testcontainers.org/modules/kafka/)
- [Testcontainers MySQL 模块](https://java.testcontainers.org/modules/databases/mysql/)
