# 

<!-- FILE: guides/testcontainers-nodejs-getting-started.md -->

---
title: 使用 Testcontainers for Node.js 入门
linkTitle: Testcontainers for Node.js
description: 学习如何使用 Testcontainers for Node.js，通过真实的 PostgreSQL 实例测试数据库交互。
keywords: testcontainers, nodejs, javascript, testing, postgresql, integration testing, jest
summary: |
  学习如何创建 Node.js 应用，并使用 Testcontainers for Node.js 搭配真实的 PostgreSQL 实例测试数据库交互。
aliases:
  - /guides/testcontainers-nodejs-getting-started/create-project/
  - /guides/testcontainers-nodejs-getting-started/run-tests/
  - /guides/testcontainers-nodejs-getting-started/write-tests/
params:
  tags: [testing]
  time: 15 minutes
---


<!-- Source: https://github.com/testcontainers/tc-guide-getting-started-with-testcontainers-for-nodejs -->

在本指南中，你将学习如何：

- 创建一个 Node.js 应用，用于存储和检索 PostgreSQL 中的客户数据
- 使用 Testcontainers 和 Jest 编写集成测试
- 针对 Docker 容器中真实的 PostgreSQL 数据库运行测试

## 先决条件

- Node.js 18+
- npm
- 受 Testcontainers 支持的 Docker 环境

> [!NOTE]
> 如果你是 Testcontainers 的新手，请访问
> [Testcontainers 概述](https://testcontainers.com/getting-started/) 了解更多关于
> Testcontainers 及其优势的信息。

## 创建 Node.js 项目

### 初始化项目

创建一个新的 Node.js 项目：

```console
$ npm init -y
```

添加 `pg`、`jest` 和 `@testcontainers/postgresql` 作为依赖：

```console
$ npm install pg --save
$ npm install jest @testcontainers/postgresql --save-dev
```

### 实现客户仓储

创建 `src/customer-repository.js`，包含用于在 PostgreSQL 中管理客户的函数：

```javascript
async function createCustomerTable(client) {
  const sql =
    "CREATE TABLE IF NOT EXISTS customers (id INT NOT NULL, name VARCHAR NOT NULL, PRIMARY KEY (id))";
  await client.query(sql);
}

async function createCustomer(client, customer) {
  const sql = "INSERT INTO customers (id, name) VALUES($1, $2)";
  await client.query(sql, [customer.id, customer.name]);
}

async function getCustomers(client) {
  const sql = "SELECT * FROM customers";
  const result = await client.query(sql);
  return result.rows;
}

module.exports = { createCustomerTable, createCustomer, getCustomers };
```

该模块提供三个函数：

- `createCustomerTable()`：如果 `customers` 表不存在，则创建它。
- `createCustomer()`：插入一条客户记录。
- `getCustomers()`：获取所有客户记录。

## 使用 Testcontainers 编写测试

创建 `src/customer-repository.test.js`，包含测试代码：

```javascript
const { Client } = require("pg");
const { PostgreSqlContainer } = require("@testcontainers/postgresql");
const {
  createCustomerTable,
  createCustomer,
  getCustomers,
} = require("./customer-repository");

describe("Customer Repository", () => {
  jest.setTimeout(60000);

  let postgresContainer;
  let postgresClient;

  beforeAll(async () => {
    postgresContainer = await new PostgreSqlContainer().start();
    postgresClient = new Client({
      connectionString: postgresContainer.getConnectionUri(),
    });
    await postgresClient.connect();
    await createCustomerTable(postgresClient);
  });

  afterAll(async () => {
    await postgresClient.end();
    await postgresContainer.stop();
  });

  it("should create and return multiple customers", async () => {
    const customer1 = { id: 1, name: "John Doe" };
    const customer2 = { id: 2, name: "Jane Doe" };

    await createCustomer(postgresClient, customer1);
    await createCustomer(postgresClient, customer2);

    const customers = await getCustomers(postgresClient);
    expect(customers).toEqual([customer1, customer2]);
  });
});
```

测试的具体工作流程如下：

- `beforeAll` 代码块使用 `PostgreSqlContainer` 启动一个真实的 PostgreSQL 容器。然后创建一个连接到该容器的 `pg` 客户端，并初始化 `customers` 表。
- `afterAll` 代码块关闭客户端连接并停止容器。
- 测试插入两个客户，获取所有客户，并断言结果匹配。

测试超时设置为 60 秒，以便为首次运行（需要拉取 Docker 镜像）启动容器预留时间。

## 运行测试及后续步骤

### 运行测试

如果 `package.json` 中还没有测试脚本，请添加：

```json
{
  "scripts": {
    "test": "jest"
  }
}
```

然后运行测试：

```console
$ npm test
```

你应该会看到类似以下输出：

```text
 PASS  src/customer-repository.test.js
  Customer Repository
    ✓ should create and return multiple customers (5 ms)

Test Suites: 1 passed, 1 total
Tests:       1 passed, 1 total
```

想了解 Testcontainers 在底层做了什么——它启动了哪些容器、使用了哪些版本——可以设置 `DEBUG` 环境变量：

```console
$ DEBUG=testcontainers* npm test
```

### 总结

Testcontainers for Node.js 库可帮助你使用与生产环境相同的数据库类型（Postgres）编写集成测试，而不是使用模拟对象（mocks）。由于你不是使用模拟，而是与真实服务通信，因此可以自由地重构代码，同时仍能验证应用按预期工作。

除了 PostgreSQL，Testcontainers 还为许多 SQL 数据库、NoSQL 数据库、消息队列等提供了专用的 [模块（modules）](https://github.com/testcontainers/testcontainers-node/tree/main/packages/modules)。

要了解更多关于 Testcontainers 的信息，请访问
[Testcontainers 概述](https://testcontainers.com/getting-started/)。

### 延伸阅读

- [Testcontainers for Node.js 文档](https://node.testcontainers.org)

