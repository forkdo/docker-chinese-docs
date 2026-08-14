<!-- FILE: guides/testcontainers-java-spring-boot-kafka.md -->

---
title: 使用 Testcontainers 测试 Spring Boot Kafka 监听器
linkTitle: Spring Boot Kafka
description: 了解如何使用 Testcontainers 的 Kafka 与 MySQL 模块测试 Spring Boot Kafka 监听器。
keywords: testcontainers, java, spring boot, testing, kafka, mysql, jpa, awaitility
summary: |
  了解如何创建一个带有 Kafka 监听器、并将数据持久化到 MySQL 的 Spring Boot 应用，
  然后使用 Testcontainers 的 Kafka 与 MySQL 模块配合 Awaitility 对其进行测试。
aliases:
  - /guides/testcontainers-java-spring-boot-kafka/create-project/
  - /guides/testcontainers-java-spring-boot-kafka/run-tests/
  - /guides/testcontainers-java-spring-boot-kafka/write-tests/
params:
  tags: [testing]
  time: 25 minutes
---


<!-- Source: https://github.com/testcontainers/tc-guide-testing-spring-boot-kafka-listener -->

在本指南中，你将学习如何：

- 创建一个集成了 Kafka 的 Spring Boot 应用
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

## 创建 Spring Boot 项目

### 搭建项目

在 [Spring Initializr](https://start.spring.io) 上创建一个 Spring Boot 项目，添加
**Spring for Apache Kafka**、**Spring Data JPA**、**MySQL Driver** 以及
**Testcontainers** 这几个 starter。

或者，克隆
[指南仓库](https://github.com/testcontainers/tc-guide-testing-spring-boot-kafka-listener)。

生成应用后，将 Awaitility 库添加为测试依赖。稍后你会用它来断言一个异步流程的预期结果。

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
        <groupId>org.springframework.kafka</groupId>
        <artifactId>spring-kafka</artifactId>
    </dependency>
    <dependency>
        <groupId>com.mysql</groupId>
        <artifactId>mysql-connector-j</artifactId>
        <scope>runtime</scope>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-test</artifactId>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.springframework.kafka</groupId>
        <artifactId>spring-kafka-test</artifactId>
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
    <dependency>
        <groupId>org.awaitility</groupId>
        <artifactId>awaitility</artifactId>
        <scope>test</scope>
    </dependency>
</dependencies>
```

建议使用 Testcontainers 的 BOM（Bill of Materials，物料清单），这样你无需为每个
Testcontainers 模块依赖重复指定版本。

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
class Product {

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

### 创建 Spring Data JPA 仓储

为 `Product` 实体创建一个仓储接口，包含按编码查找产品以及更新指定产品编码价格的方法：

```java
package com.testcontainers.demo;

import java.math.BigDecimal;
import java.util.Optional;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

interface ProductRepository extends JpaRepository<Product, Long> {
  Optional<Product> findByCode(String code);

  @Modifying
  @Query("update Product p set p.price = :price where p.code = :productCode")
  void updateProductPrice(
    @Param("productCode") String productCode,
    @Param("price") BigDecimal price
  );
}
```

### 添加 schema 创建脚本

由于该应用不使用内存数据库，你需要创建 MySQL 表。生产环境的推荐做法是使用 Flyway 或
Liquibase 之类的迁移工具，但就本指南而言，使用 Spring Boot 内置的 schema 初始化已足够。

创建 `src/main/resources/schema.sql`：

```sql
create table products (
      id int NOT NULL AUTO_INCREMENT,
      code varchar(255) not null,
      name varchar(255) not null,
      price numeric(5,2) not null,
      PRIMARY KEY (id),
      UNIQUE (code)
);
```

在 `src/main/resources/application.properties` 中启用 schema 初始化：

```properties
spring.sql.init.mode=always
```

### 创建事件负载

创建一个名为 `ProductPriceChangedEvent` 的 record，表示来自 Kafka 主题的事件负载结构：

```java
package com.testcontainers.demo;

import java.math.BigDecimal;

record ProductPriceChangedEvent(String productCode, BigDecimal price) {}
```

发送方与接收方约定的 JSON 格式如下：

```json
{
  "productCode": "P100",
  "price": 25.0
}
```

### 实现 Kafka 监听器

创建 `ProductPriceChangedEventHandler.java`，处理来自 `product-price-changes` 主题的
消息，并更新数据库中的产品价格：

```java
package com.testcontainers.demo;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;

@Component
@Transactional
class ProductPriceChangedEventHandler {

  private static final Logger log = LoggerFactory.getLogger(
    ProductPriceChangedEventHandler.class
  );

  private final ProductRepository productRepository;

  ProductPriceChangedEventHandler(ProductRepository productRepository) {
    this.productRepository = productRepository;
  }

  @KafkaListener(topics = "product-price-changes", groupId = "demo")
  public void handle(ProductPriceChangedEvent event) {
    log.info(
      "Received a ProductPriceChangedEvent with productCode:{}: ",
      event.productCode()
    );
    productRepository.updateProductPrice(event.productCode(), event.price());
  }
}
```

`@KafkaListener` 注解指定要监听的主题名称。Spring Kafka 会依据 `application.properties`
中配置的属性处理序列化和反序列化。

### 配置 Kafka 序列化

在 `src/main/resources/application.properties` 中添加以下 Kafka 属性：

```properties
######## Kafka Configuration  #########
spring.kafka.bootstrap-servers=localhost:9092
spring.kafka.producer.key-serializer=org.apache.kafka.common.serialization.StringSerializer
spring.kafka.producer.value-serializer=org.springframework.kafka.support.serializer.JsonSerializer

spring.kafka.consumer.group-id=demo
spring.kafka.consumer.auto-offset-reset=latest
spring.kafka.consumer.key-deserializer=org.apache.kafka.common.serialization.StringDeserializer
spring.kafka.consumer.value-deserializer=org.springframework.kafka.support.serializer.JsonDeserializer
spring.kafka.consumer.properties.spring.json.trusted.packages=com.testcontainers.demo
```

`productCode` 键使用 `StringSerializer`/`StringDeserializer` 进行（反）序列化，
`ProductPriceChangedEvent` 值则使用 `JsonSerializer`/`JsonDeserializer` 进行（反）序列化。

## 使用 Testcontainers 编写测试

要测试 Kafka 监听器，你需要一个运行中的 Kafka broker 和一个 MySQL 数据库，外加一个启动
的 Spring 上下文。Testcontainers 会在 Docker 容器中启动这两个服务，而
`@DynamicPropertySource` 会将它们连接到 Spring。

### 编写测试

创建 `ProductPriceChangedEventHandlerTest.java`：

```java
package com.testcontainers.demo;

import static java.util.concurrent.TimeUnit.SECONDS;
import static org.assertj.core.api.Assertions.assertThat;
import static org.awaitility.Awaitility.await;

import java.math.BigDecimal;
import java.time.Duration;
import java.util.Optional;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.test.context.DynamicPropertyRegistry;
import org.springframework.test.context.DynamicPropertySource;
import org.springframework.test.context.TestPropertySource;
import org.testcontainers.kafka.ConfluentKafkaContainer;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;

@SpringBootTest
@TestPropertySource(
  properties = {
    "spring.kafka.consumer.auto-offset-reset=earliest",
    "spring.datasource.url=jdbc:tc:mysql:8.0.32:///db",
  }
)
@Testcontainers
class ProductPriceChangedEventHandlerTest {

  @Container
  static final ConfluentKafkaContainer kafka =
    new ConfluentKafkaContainer("confluentinc/cp-kafka:7.8.0");

  @DynamicPropertySource
  static void overrideProperties(DynamicPropertyRegistry registry) {
    registry.add("spring.kafka.bootstrap-servers", kafka::getBootstrapServers);
  }

  @Autowired
  private KafkaTemplate<String, Object> kafkaTemplate;

  @Autowired
  private ProductRepository productRepository;

  @BeforeEach
  void setUp() {
    Product product = new Product(null, "P100", "Product One", BigDecimal.TEN);
    productRepository.save(product);
  }

  @Test
  void shouldHandleProductPriceChangedEvent() {
    ProductPriceChangedEvent event = new ProductPriceChangedEvent(
      "P100",
      new BigDecimal("14.50")
    );

    kafkaTemplate.send("product-price-changes", event.productCode(), event);

    await()
      .pollInterval(Duration.ofSeconds(3))
      .atMost(10, SECONDS)
      .untilAsserted(() -> {
        Optional<Product> optionalProduct = productRepository.findByCode(
          "P100"
        );
        assertThat(optionalProduct).isPresent();
        assertThat(optionalProduct.get().getCode()).isEqualTo("P100");
        assertThat(optionalProduct.get().getPrice())
          .isEqualTo(new BigDecimal("14.50"));
      });
  }
}
```

该测试的作用如下：

- `@SpringBootTest` 启动完整的 Spring 应用上下文。
- `@TestPropertySource` 中 Testcontainers 的专用 JDBC URL（`jdbc:tc:mysql:8.0.32:///db`）
  会启动一个 MySQL 容器，并将其自动配置为数据源。
- `@Testcontainers` 与 `@Container` 管理 Kafka 容器的生命周期。`@DynamicPropertySource`
  将 Kafka bootstrap 服务器注册到 Spring，使生产者和消费者都能连接到测试容器。
- `@BeforeEach` 在每个测试之前在数据库中创建一个 `Product` 记录。
- 该测试使用 `KafkaTemplate` 向 `product-price-changes` 主题发送一个
  `ProductPriceChangedEvent`。Spring Boot 会使用 `JsonSerializer` 将对象转换为 JSON。
- 由于 Kafka 消息处理是异步的，测试使用 [Awaitility](http://www.awaitility.org/) 每 3
  秒轮询一次（最多 10 秒），直到数据库中的产品价格与期望值匹配。
- 属性 `spring.kafka.consumer.auto-offset-reset` 设为 `earliest`，这样即使消息在监听器
  就绪之前就发送到了主题，监听器也能消费到消息。该设置对运行测试很有帮助。

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

- [在 Java Spring Boot 项目中使用 Testcontainers 入门](https://testcontainers.com/guides/testing-spring-boot-rest-api-using-testcontainers/)
- [用真实数据库替换 H2 进行测试的最简方式](https://testcontainers.com/guides/replace-h2-with-real-database-for-testing/)
- [Awaitility](http://www.awaitility.org/)
- [Testcontainers Kafka 模块](https://java.testcontainers.org/modules/kafka/)
- [Testcontainers MySQL 模块](https://java.testcontainers.org/modules/databases/mysql/)
