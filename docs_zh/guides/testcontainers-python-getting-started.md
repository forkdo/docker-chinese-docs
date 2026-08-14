<!-- FILE: guides/testcontainers-python-getting-started.md -->

---
title: 使用 Testcontainers for Python 入门
linkTitle: Testcontainers for Python
description: 学习如何使用 Testcontainers for Python，通过真实的 PostgreSQL 实例测试数据库交互。
keywords: testcontainers, python, testing, postgresql, integration testing, pytest
summary: |
  学习如何创建 Python 应用，并使用 Testcontainers for Python 搭配真实的 PostgreSQL 实例测试数据库交互。
aliases:
  - /guides/testcontainers-python-getting-started/create-project/
  - /guides/testcontainers-python-getting-started/run-tests/
  - /guides/testcontainers-python-getting-started/write-tests/
params:
  tags: [testing]
  time: 15 minutes
---


<!-- Source: https://github.com/testcontainers/tc-guide-getting-started-with-testcontainers-for-python -->

在本指南中，你将学习如何：

- 创建一个使用 PostgreSQL 存储客户数据的 Python 应用
- 使用 `psycopg` 与数据库交互
- 使用 `testcontainers-python` 和 `pytest` 编写集成测试
- 通过 pytest fixtures 管理容器生命周期

## 先决条件

- Python 3.10+
- pip
- 受 Testcontainers 支持的 Docker 环境

> [!NOTE]
> 如果你是 Testcontainers 的新手，请访问
> [Testcontainers 概述](https://testcontainers.com/getting-started/) 了解更多关于
> Testcontainers 及其优势的信息。

## 创建 Python 项目

### 初始化项目

首先创建一个带虚拟环境的 Python 项目：

```console
$ mkdir tc-python-demo
$ cd tc-python-demo
$ python3 -m venv venv
$ source venv/bin/activate
```

本指南使用 [psycopg3](https://www.psycopg.org/psycopg3/) 与 Postgres 数据库交互，[pytest](https://pytest.org/) 用于测试，以及
[testcontainers-python](https://testcontainers-python.readthedocs.io/) 在容器中运行 PostgreSQL 数据库。

安装依赖：

```console
$ pip install "psycopg[binary]" pytest testcontainers[postgres]
$ pip freeze > requirements.txt
```

`pip freeze` 命令会生成 `requirements.txt` 文件，以便其他人可以使用 `pip install -r requirements.txt` 安装相同的包版本。

### 创建数据库辅助函数

创建一个 `db/connection.py` 文件，包含获取数据库连接的函数：

```python
import os

import psycopg


def get_connection():
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    username = os.getenv("DB_USERNAME", "postgres")
    password = os.getenv("DB_PASSWORD", "postgres")
    database = os.getenv("DB_NAME", "postgres")
    return psycopg.connect(f"host={host} dbname={database} user={username} password={password} port={port}")
```

该函数不使用硬编码的数据库连接参数，而是使用环境变量。这样无需修改代码即可在不同环境中运行应用。

### 创建业务逻辑

创建一个 `customers/customers.py` 文件并定义 `Customer` 类：

```python
class Customer:
    def __init__(self, cust_id, name, email):
        self.id = cust_id
        self.name = name
        self.email = email

    def __str__(self):
        return f"Customer({self.id}, {self.name}, {self.email})"
```

添加 `create_table()` 函数以创建 `customers` 表：

```python
from db.connection import get_connection


def create_table():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE customers (
                    id serial PRIMARY KEY,
                    name varchar not null,
                    email varchar not null unique)
                """)
            conn.commit()
```

该函数使用 `get_connection()` 获取数据库连接并创建 `customers` 表。`with` 语句会在完成后自动关闭连接。

添加其余的 CRUD 函数：

```python
def create_customer(name, email):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO customers (name, email) VALUES (%s, %s)", (name, email))
            conn.commit()


def get_all_customers() -> list[Customer]:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM customers")
            return [Customer(cid, name, email) for cid, name, email in cur]


def get_customer_by_email(email) -> Customer:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, email FROM customers WHERE email = %s", (email,))
            (cid, name, email) = cur.fetchone()
            return Customer(cid, name, email)


def delete_all_customers():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM customers")
            conn.commit()
```

> [!NOTE]
> 为了让本指南保持简洁，每个函数都会创建一个新连接。在真实应用中，应使用连接池来复用连接。

## 使用 Testcontainers 编写测试

你将使用 Testcontainers 创建一个 PostgreSQL 容器，并将其用于所有测试。在每次测试之前，你会删除所有客户记录，以便测试在干净的数据库中运行。

### 设置 pytest fixtures

本指南使用 [pytest fixtures](https://pytest.org/en/stable/how-to/fixtures.html) 进行设置和清理逻辑。推荐的方法是使用
[finalizers](https://pytest.org/en/stable/how-to/fixtures.html#adding-finalizers-directly) 来确保即使设置失败也会执行清理：

```python
@pytest.fixture
def setup(request):
    # setup code

    def cleanup():
        # teardown code

    request.addfinalizer(cleanup)
    return some_value
```

### 创建测试文件

创建一个内容为空的 `tests/__init__.py` 文件，以启用 pytest 的
[自动发现](https://pytest.org/explanation/goodpractices.html#test-discovery) 功能。

然后创建带有 fixtures 的 `tests/test_customers.py`：

```python
import os
import pytest
from testcontainers.postgres import PostgresContainer

from customers import customers

postgres = PostgresContainer("postgres:16-alpine")


@pytest.fixture(scope="module", autouse=True)
def setup(request):
    postgres.start()

    def remove_container():
        postgres.stop()

    request.addfinalizer(remove_container)
    os.environ["DB_CONN"] = postgres.get_connection_url()
    os.environ["DB_HOST"] = postgres.get_container_host_ip()
    os.environ["DB_PORT"] = str(postgres.get_exposed_port(5432))
    os.environ["DB_USERNAME"] = postgres.username
    os.environ["DB_PASSWORD"] = postgres.password
    os.environ["DB_NAME"] = postgres.dbname
    customers.create_table()


@pytest.fixture(scope="function", autouse=True)
def setup_data():
    customers.delete_all_customers()
```

这些 fixtures 的作用是：

- `setup` fixture 的 `scope="module"`，因此它对文件中的所有测试只运行一次。它会启动一个 PostgreSQL 容器，设置包含连接信息的环境变量，并创建 `customers` 表。一个清理函数会在所有测试完成后移除容器。
- `setup_data` fixture 的 `scope="function"`，因此它会在每个测试之前运行。它会删除所有记录，为每个测试提供干净的数据库。

### 编写测试

将测试函数添加到同一个文件中：

```python
def test_get_all_customers():
    customers.create_customer("Siva", "siva@gmail.com")
    customers.create_customer("James", "james@gmail.com")
    customers_list = customers.get_all_customers()
    assert len(customers_list) == 2


def test_get_customer_by_email():
    customers.create_customer("John", "john@gmail.com")
    customer = customers.get_customer_by_email("john@gmail.com")
    assert customer.name == "John"
    assert customer.email == "john@gmail.com"
```

- `test_get_all_customers()` 插入两条客户记录，获取所有客户，并断言数量。
- `test_get_customer_by_email()` 插入一个客户，通过邮箱获取它，并断言详细信息。

由于 `setup_data` 会在每个测试前删除所有记录，测试可以按任意顺序运行。

## 运行测试及后续步骤

### 运行测试

使用 pytest 运行测试：

```console
$ pytest -v
```

你应该会看到类似以下输出：

```text
============================= test session starts ==============================
platform linux -- Python 3.13.x, pytest-9.x.x
collected 2 items

tests/test_customers.py::test_get_all_customers PASSED                   [ 50%]
tests/test_customers.py::test_get_customer_by_email PASSED               [100%]

============================== 2 passed in 1.90s ===============================
```

这些测试针对真实的 PostgreSQL 数据库运行，而不是模拟对象，因此对实现更有信心。

### 总结

Testcontainers for Python 库可帮助你使用与生产环境相同的数据库类型（Postgres）编写集成测试，而不是使用模拟对象。由于你不是使用模拟，而是与真实服务通信，因此可以自由地重构代码，同时仍能验证应用按预期工作。

除了 PostgreSQL，Testcontainers for Python 还为许多 SQL 数据库、NoSQL 数据库、消息队列等提供了模块。你可以使用 Testcontainers 运行测试所需的任何容器化依赖。

要了解更多关于 Testcontainers 的信息，请访问
[Testcontainers 概述](https://testcontainers.com/getting-started/)。

### 延伸阅读

- [testcontainers-python 文档](https://testcontainers-python.readthedocs.io/)
- [使用 Testcontainers for Go 入门](/guides/testcontainers-go-getting-started/)
- [使用 Testcontainers for Java 入门](https://testcontainers.com/guides/getting-started-with-testcontainers-for-java/)
- [使用 Testcontainers for Node.js 入门](https://testcontainers.com/guides/getting-started-with-testcontainers-for-nodejs/)
