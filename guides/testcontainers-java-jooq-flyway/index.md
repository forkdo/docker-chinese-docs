# 

<!-- FILE: guides/testcontainers-java-jooq-flyway.md -->

---
title: 使用 Testcontainers 配合 jOOQ 与 Flyway
linkTitle: jOOQ 与 Flyway
description: 了解如何使用 Testcontainers 与 Flyway 从数据库生成 jOOQ 代码，并对持久化层进行测试。
keywords: testcontainers, java, testing, jooq, flyway, postgresql, spring boot, code generation
summary: |
  使用 Flyway 迁移管理、基于真实 PostgreSQL 数据库生成类型安全的 jOOQ
  代码，并使用 Testcontainers 对仓储（repository）进行测试。
aliases:
  - /guides/testcontainers-java-jooq-flyway/create-project/
  - /guides/testcontainers-java-jooq-flyway/run-tests/
  - /guides/testcontainers-java-jooq-flyway/write-tests/
params:
  tags: [testing]
  time: 25 minutes
---


<!-- Source: https://github.com/testcontainers/tc-guide-working-with-jooq-flyway-using-testcontainers -->

在本指南中，你将学习如何：

- 创建一个支持 jOOQ 的 Spring Boot 应用
- 使用 Testcontainers、Flyway 和一个 Maven 插件生成 jOOQ 代码
- 使用 jOOQ 实现基本的数据库操作
- 使用 jOOQ 的 MULTISET 特性加载复杂的对象图
- 使用 Testcontainers 测试 jOOQ 持久化层

## 先决条件

- Java 17+
- Maven
- 一个受 Testcontainers 支持的 Docker 环境

> [!NOTE]
> 如果你刚接触 Testcontainers，请访问
> [Testcontainers 概览](https://testcontainers.com/getting-started/) 了解
> Testcontainers 及其使用优势。

## 创建 Spring Boot 项目

### 搭建项目

在 [Spring Initializr](https://start.spring.io) 上创建一个 Spring Boot 项目，
构建工具选择 Maven，并添加 **JOOQ Access Layer**（JOOQ 访问层）、
**Flyway Migration**（Flyway 迁移）、**Spring Boot DevTools**、**PostgreSQL Driver**
（PostgreSQL 驱动）以及 **Testcontainers** 这几个 starter。

或者，克隆
[指南仓库](https://github.com/testcontainers/tc-guide-working-with-jooq-flyway-using-testcontainers)。

jOOQ（jOOQ Object Oriented Querying）提供了一套流式 API，用于构建类型安全的
SQL 查询。要充分享受其类型安全 DSL 带来的好处，你需要从数据库中的表、视图及其他
对象生成 Java 代码。

> [!TIP]
> 想进一步了解 jOOQ 代码生成器的帮助，请阅读
> [为什么你应该使用带代码生成的 jOOQ](https://blog.jooq.org/why-you-should-use-jooq-with-code-generation/)。

借助 jOOQ 代码生成功能构建并测试应用的典型流程如下：

1. 使用 Testcontainers 创建一个数据库实例。
2. 执行 Flyway 数据库迁移。
3. 运行 jOOQ 代码生成器，从数据库对象生成 Java 代码。
4. 运行集成测试。

[testcontainers-jooq-codegen-maven-plugin](https://github.com/testcontainers/testcontainers-jooq-codegen-maven-plugin)
会在 Maven 构建过程中自动完成上述步骤。

### 创建 Flyway 迁移脚本

示例应用包含 `users`、`posts` 和 `comments` 三张表。请按照 Flyway 的命名约定
创建第一个迁移脚本。

创建 `src/main/resources/db/migration/V1__create_tables.sql`：

```sql
create table users
(
    id         bigserial not null,
    name       varchar   not null,
    email      varchar   not null,
    created_at timestamp,
    updated_at timestamp,
    primary key (id),
    constraint user_email_unique unique (email)
);

create table posts
(
    id         bigserial                    not null,
    title      varchar                      not null,
    content    varchar                      not null,
    created_by bigint references users (id) not null,
    created_at timestamp,
    updated_at timestamp,
    primary key (id)
);

create table comments
(
    id         bigserial                    not null,
    name       varchar                      not null,
    content    varchar                      not null,
    post_id    bigint references posts (id) not null,
    created_at timestamp,
    updated_at timestamp,
    primary key (id)
);

ALTER SEQUENCE users_id_seq RESTART WITH 101;
ALTER SEQUENCE posts_id_seq RESTART WITH 101;
ALTER SEQUENCE comments_id_seq RESTART WITH 101;
```

序列值从 101 重新开始，以便你可以使用显式的主键值插入测试用的示例数据。

### 配置 jOOQ 代码生成

在 `pom.xml` 中添加 `testcontainers-jooq-codegen-maven-plugin`：

```xml
<properties>
    <testcontainers.version>2.0.4</testcontainers.version>
    <testcontainers-jooq-codegen-maven-plugin.version>0.0.4</testcontainers-jooq-codegen-maven-plugin.version>
</properties>

<build>
    <plugins>
        <plugin>
            <groupId>org.testcontainers</groupId>
            <artifactId>testcontainers-jooq-codegen-maven-plugin</artifactId>
            <version>${testcontainers-jooq-codegen-maven-plugin.version}</version>
            <dependencies>
                <dependency>
                    <groupId>org.testcontainers</groupId>
                    <artifactId>testcontainers-postgresql</artifactId>
                    <version>${testcontainers.version}</version>
                </dependency>
                <dependency>
                    <groupId>org.postgresql</groupId>
                    <artifactId>postgresql</artifactId>
                    <version>${postgresql.version}</version>
                </dependency>
            </dependencies>
            <executions>
                <execution>
                    <id>generate-jooq-sources</id>
                    <goals>
                        <goal>generate</goal>
                    </goals>
                    <phase>generate-sources</phase>
                    <configuration>
                        <database>
                            <type>POSTGRES</type>
                            <containerImage>postgres:16-alpine</containerImage>
                        </database>
                        <flyway>
                            <locations>
                                filesystem:src/main/resources/db/migration
                            </locations>
                        </flyway>
                        <jooq>
                            <generator>
                                <database>
                                    <includes>.*</includes>
                                    <excludes>flyway_schema_history</excludes>
                                    <inputSchema>public</inputSchema>
                                </database>
                                <target>
                                    <packageName>com.testcontainers.demo.jooq</packageName>
                                    <directory>target/generated-sources/jooq</directory>
                                </target>
                            </generator>
                        </jooq>
                    </configuration>
                </execution>
            </executions>
        </plugin>
    </plugins>
</build>
```

该插件配置的作用如下：

- `<configuration>/<database>` 部分将数据库类型设为 `POSTGRES`，Docker 镜像设为
  `postgres:16-alpine`。
- `<configuration>/<flyway>` 部分指向 Flyway 迁移脚本所在位置。
- `<configuration>/<jooq>` 部分配置生成代码的包名和输出目录。你可以使用官方
  `jooq-code-generator` 插件支持的任何配置选项。

当你运行 `./mvnw clean package` 时，该插件会使用 Testcontainers 启动一个
PostgreSQL 容器，执行 Flyway 迁移，并在 `target/generated-sources/jooq` 下生成
Java 代码。

### 创建模型类

创建模型类来表示不同用例的数据结构。这些 record 只包含表中部分列的值。

`User.java`：

```java
package com.testcontainers.demo.domain;

public record User(Long id, String name, String email) {}
```

`Post.java`：

```java
package com.testcontainers.demo.domain;

import java.time.LocalDateTime;
import java.util.List;

public record Post(
  Long id,
  String title,
  String content,
  User createdBy,
  List<Comment> comments,
  LocalDateTime createdAt,
  LocalDateTime updatedAt
) {}
```

`Comment.java`：

```java
package com.testcontainers.demo.domain;

import java.time.LocalDateTime;

public record Comment(
  Long id,
  String name,
  String content,
  LocalDateTime createdAt,
  LocalDateTime updatedAt
) {}
```

### 使用 jOOQ 实现仓储

创建 `UserRepository.java`，包含创建用户和按邮箱查找用户的方法：

```java
package com.testcontainers.demo.domain;

import static com.testcontainers.demo.jooq.tables.Users.USERS;
import static org.jooq.Records.mapping;

import java.time.LocalDateTime;
import java.util.Optional;
import org.jooq.DSLContext;
import org.springframework.stereotype.Repository;

@Repository
class UserRepository {

  private final DSLContext dsl;

  UserRepository(DSLContext dsl) {
    this.dsl = dsl;
  }

  public User createUser(User user) {
    return this.dsl.insertInto(USERS)
      .set(USERS.NAME, user.name())
      .set(USERS.EMAIL, user.email())
      .set(USERS.CREATED_AT, LocalDateTime.now())
      .returningResult(USERS.ID, USERS.NAME, USERS.EMAIL)
      .fetchOne(mapping(User::new));
  }

  public Optional<User> getUserByEmail(String email) {
    return this.dsl.select(USERS.ID, USERS.NAME, USERS.EMAIL)
      .from(USERS)
      .where(USERS.EMAIL.equalIgnoreCase(email))
      .fetchOptional(mapping(User::new));
  }
}
```

jOOQ 的 DSL 看起来类似于 SQL，但用 Java 编写。由于代码是从数据库 schema 生成的，
它能与数据库结构保持同步，并提供类型安全。例如，`where(USERS.EMAIL.equalIgnoreCase(email))`
期望接收一个 `String` 值。如果你传入 `123` 这类非字符串值，就会得到编译错误。

### 获取复杂的对象图

对于复杂查询，jOOQ 表现尤为出色。数据库中 `Post` 到 `User` 是多对一关系，`Post`
到 `Comment` 是一对多关系。

创建 `PostRepository.java`，使用 jOOQ 的 MULTISET 特性，通过一条查询同时加载
`Post` 及其创建者和评论：

```java
package com.testcontainers.demo.domain;

import static com.testcontainers.demo.jooq.Tables.COMMENTS;
import static com.testcontainers.demo.jooq.tables.Posts.POSTS;
import static org.jooq.Records.mapping;
import static org.jooq.impl.DSL.multiset;
import static org.jooq.impl.DSL.row;
import static org.jooq.impl.DSL.select;

import java.util.Optional;
import org.jooq.DSLContext;
import org.springframework.stereotype.Repository;

@Repository
class PostRepository {

  private final DSLContext dsl;

  PostRepository(DSLContext dsl) {
    this.dsl = dsl;
  }

  public Optional<Post> getPostById(Long id) {
    return this.dsl.select(
        POSTS.ID,
        POSTS.TITLE,
        POSTS.CONTENT,
        row(POSTS.users().ID, POSTS.users().NAME, POSTS.users().EMAIL)
          .mapping(User::new)
          .as("createdBy"),
        multiset(
          select(
            COMMENTS.ID,
            COMMENTS.NAME,
            COMMENTS.CONTENT,
            COMMENTS.CREATED_AT,
            COMMENTS.UPDATED_AT
          )
            .from(COMMENTS)
            .where(POSTS.ID.eq(COMMENTS.POST_ID))
        )
          .as("comments")
          .convertFrom(r -> r.map(mapping(Comment::new))),
        POSTS.CREATED_AT,
        POSTS.UPDATED_AT
      )
      .from(POSTS)
      .where(POSTS.ID.eq(id))
      .fetchOptional(mapping(Post::new));
  }
}
```

这里使用了 jOOQ 的
[nested records（嵌套记录）](https://www.jooq.org/doc/latest/manual/sql-building/column-expressions/nested-records/)
来表示 `Post` 到 `User` 的多对一关联，以及
[MULTISET](https://www.jooq.org/doc/latest/manual/sql-building/column-expressions/multiset-value-constructor/)
来表示 `Post` 到 `Comment` 的一对多关联。

## 使用 Testcontainers 编写测试

在编写测试之前，先创建一个 SQL 脚本来初始化测试数据，位于
`src/test/resources/test-data.sql`：

```sql
DELETE FROM comments;
DELETE FROM posts;
DELETE FROM users;

INSERT INTO users(id, name, email) VALUES
(1, 'Siva', 'siva@gmail.com'),
(2, 'Oleg', 'oleg@gmail.com');

INSERT INTO posts(id, title, content, created_by, created_at) VALUES
(1, 'Post 1 Title', 'Post 1 content', 1, CURRENT_TIMESTAMP),
(2, 'Post 2 Title', 'Post 2 content', 2, CURRENT_TIMESTAMP);

INSERT INTO comments(id, name, content, post_id, created_at) VALUES
(1, 'Ron', 'Comment 1', 1, CURRENT_TIMESTAMP),
(2, 'James', 'Comment 2', 1, CURRENT_TIMESTAMP),
(3, 'Robert', 'Comment 3', 2, CURRENT_TIMESTAMP);
```

### 使用 @JooqTest 切片进行测试

`@JooqTest` 注解只加载持久化层组件，并自动配置 jOOQ 的 `DSLContext`。使用
Testcontainers 的专用 JDBC URL 来启动一个 Postgres 容器。

创建 `UserRepositoryJooqTest.java`：

```java
package com.testcontainers.demo.domain;

import static org.assertj.core.api.Assertions.assertThat;

import org.jooq.DSLContext;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.jooq.JooqTest;
import org.springframework.test.context.jdbc.Sql;

@JooqTest(
  properties = {
    "spring.test.database.replace=none",
    "spring.datasource.url=jdbc:tc:postgresql:16-alpine:///db",
  }
)
@Sql("/test-data.sql")
class UserRepositoryJooqTest {

  @Autowired
  DSLContext dsl;

  UserRepository repository;

  @BeforeEach
  void setUp() {
    this.repository = new UserRepository(dsl);
  }

  @Test
  void shouldCreateUserSuccessfully() {
    User user = new User(null, "John", "john@gmail.com");

    User savedUser = repository.createUser(user);

    assertThat(savedUser.id()).isNotNull();
    assertThat(savedUser.name()).isEqualTo("John");
    assertThat(savedUser.email()).isEqualTo("john@gmail.com");
  }

  @Test
  void shouldGetUserByEmail() {
    User user = repository.getUserByEmail("siva@gmail.com").orElseThrow();

    assertThat(user.id()).isEqualTo(1L);
    assertThat(user.name()).isEqualTo("Siva");
    assertThat(user.email()).isEqualTo("siva@gmail.com");
  }
}
```

该测试的作用如下：

- `@JooqTest` 只加载持久化层，并自动配置 `DSLContext`。
- Testcontainers 的专用 JDBC URL（`jdbc:tc:postgresql:16-alpine:///db`）会自动
  启动一个 PostgreSQL 容器。
- 由于 `flyway-core` 在 classpath 上，Spring Boot 会在启动时执行
  `src/main/resources/db/migration` 下的 Flyway 迁移。
- `@Sql("/test-data.sql")` 会在每个测试之前加载测试数据。
- `UserRepository` 使用注入的 `DSLContext` 手动实例化。

### 使用 @SpringBootTest 进行集成测试

对于完整的集成测试，可使用 `@SpringBootTest` 配合 Spring Boot 3.1 引入的
Testcontainers `@ServiceConnection` 支持。

创建 `UserRepositoryTest.java`：

```java
package com.testcontainers.demo.domain;

import static org.assertj.core.api.Assertions.assertThat;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.testcontainers.service.connection.ServiceConnection;
import org.springframework.test.context.jdbc.Sql;
import org.testcontainers.postgresql.PostgreSQLContainer;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;

@SpringBootTest
@Sql("/test-data.sql")
@Testcontainers
class UserRepositoryTest {

  @Container
  @ServiceConnection
  static PostgreSQLContainer postgres = new PostgreSQLContainer(
    "postgres:16-alpine"
  );

  @Autowired
  UserRepository repository;

  @Test
  void shouldCreateUserSuccessfully() {
    User user = new User(null, "John", "john@gmail.com");

    User savedUser = repository.createUser(user);

    assertThat(savedUser.id()).isNotNull();
    assertThat(savedUser.name()).isEqualTo("John");
    assertThat(savedUser.email()).isEqualTo("john@gmail.com");
  }

  @Test
  void shouldGetUserByEmail() {
    User user = repository.getUserByEmail("siva@gmail.com").orElseThrow();

    assertThat(user.id()).isEqualTo(1L);
    assertThat(user.name()).isEqualTo("Siva");
    assertThat(user.email()).isEqualTo("siva@gmail.com");
  }
}
```

该测试的作用如下：

- `@SpringBootTest` 加载整个应用上下文，因此 `UserRepository` 会直接被注入。
- `@Testcontainers` 与 `@Container` 管理 PostgreSQL 容器的生命周期。
- `@ServiceConnection` 从运行中的容器自动配置数据源属性，无需再使用
  `@DynamicPropertySource`。
- `@Sql("/test-data.sql")` 初始化测试数据。

### 测试 PostRepository

对使用 Testcontainers 专用 JDBC URL 获取复杂对象图的 `PostRepository` 进行测试。

创建 `PostRepositoryTest.java`：

```java
package com.testcontainers.demo.domain;

import static org.assertj.core.api.Assertions.assertThat;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.jdbc.Sql;

@SpringBootTest(
  properties = {
    "spring.test.database.replace=none",
    "spring.datasource.url=jdbc:tc:postgresql:16-alpine:///db",
  }
)
@Sql("/test-data.sql")
class PostRepositoryTest {

  @Autowired
  PostRepository repository;

  @Test
  void shouldGetPostById() {
    Post post = repository.getPostById(1L).orElseThrow();

    assertThat(post.id()).isEqualTo(1L);
    assertThat(post.title()).isEqualTo("Post 1 Title");
    assertThat(post.content()).isEqualTo("Post 1 content");
    assertThat(post.createdBy().id()).isEqualTo(1L);
    assertThat(post.createdBy().name()).isEqualTo("Siva");
    assertThat(post.createdBy().email()).isEqualTo("siva@gmail.com");
    assertThat(post.comments()).hasSize(2);
  }
}
```

该测试验证了 `getPostById` 使用 jOOQ 的 MULTISET 特性，通过一条查询加载文章
及其创建者和评论。

## 运行测试与后续步骤

### 运行测试

```console
$ ./mvnw test
```

你应该会看到 PostgreSQL Docker 容器启动、jOOQ 代码生成完成，并且所有测试通过。
测试结束后，容器会自动停止并被移除。

### 小结

Testcontainers 库可帮助你使用 jOOQ 代码生成器从数据库生成 Java 代码，并针对与你
生产环境所用类型相同的数据库（PostgreSQL）测试持久化层，而不必使用 mock 或内存
数据库。

由于代码始终基于数据库的当前状态生成，你可以确信代码与数据库变更保持同步。
你可以放心地重构，同时仍能验证应用是否按预期工作。

想进一步了解 Testcontainers，请访问
[Testcontainers 概览](https://testcontainers.com/getting-started/)。

### 延伸阅读

- [jOOQ 文档](https://www.jooq.org/)
- [jOOQ 代码生成](https://www.jooq.org/doc/latest/manual/code-generation/)
- [Spring Boot 的 Testcontainers 支持](https://docs.spring.io/spring-boot/reference/testing/testcontainers.html)
- [用真实数据库替换 H2 进行测试](/guides/testcontainers-java-replace-h2/)

