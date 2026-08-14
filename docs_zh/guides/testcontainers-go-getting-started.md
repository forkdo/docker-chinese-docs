---
title: Testcontainers for Go 入门
linkTitle: Testcontainers for Go
description: 学习如何使用 Testcontainers for Go 通过真实的 PostgreSQL 实例测试数据库交互。
keywords: testcontainers, go, golang, testing, postgresql, integration testing
summary: |
  学习如何创建一个 Go 应用，并使用 Testcontainers for Go
  配合真实的 PostgreSQL 实例测试数据库交互。
aliases:
  - /guides/testcontainers-go-getting-started/create-project/
  - /guides/testcontainers-go-getting-started/run-tests/
  - /guides/testcontainers-go-getting-started/test-suites/
  - /guides/testcontainers-go-getting-started/write-tests/
params:
  tags: [testing]
  time: 20 minutes
---


<!-- Source: https://github.com/testcontainers/tc-guide-getting-started-with-testcontainers-for-go -->

在本指南中，你将学习如何：

- 创建一个启用了模块支持的 Go 应用
- 使用 pgx 驱动实现一个在 PostgreSQL 数据库中管理客户数据的 Repository
- 使用 testcontainers-go 编写集成测试
- 使用测试套件在多个测试之间复用容器

## 先决条件

- Go 1.25+
- 你偏好的 IDE（VS Code、GoLand）
- Testcontainers 支持的 Docker 环境。详情请参阅
  [testcontainers-go 系统要求](https://golang.testcontainers.org/system_requirements/)。

> [!NOTE]
> 如果你是 Testcontainers 的新手，请访问
> [Testcontainers 概览](https://testcontainers.com/getting-started/) 以了解更多关于
> Testcontainers 及其优势的信息。

## 创建 Go 项目

### 初始化项目

首先创建一个 Go 项目。

```console
$ mkdir testcontainers-go-demo
$ cd testcontainers-go-demo
$ go mod init github.com/testcontainers/testcontainers-go-demo
```

本指南使用 [jackc/pgx](https://github.com/jackc/pgx) PostgreSQL 驱动来与 Postgres 数据库交互，使用 testcontainers-go 的
[Postgres 模块](https://golang.testcontainers.org/modules/postgres/) 来启动一个 Postgres Docker 实例用于测试，并使用
[testify](https://github.com/stretchr/testify) 将多个测试作为套件运行并编写断言。

安装这些依赖：

```console
$ go get github.com/jackc/pgx/v5
$ go get github.com/testcontainers/testcontainers-go
$ go get github.com/testcontainers/testcontainers-go/modules/postgres
$ go get github.com/stretchr/testify
```

### 创建 Customer 结构体

在 `customer` 包中创建一个 `types.go` 文件，并定义 `Customer` 结构体来建模客户详情：

```go
package customer

type Customer struct {
	Id    int
	Name  string
	Email string
}
```

### 创建 Repository

接下来，创建 `customer/repo.go`，定义 `Repository` 结构体，并添加创建客户和按邮箱获取客户的方法：

```go
package customer

import (
	"context"
	"fmt"
	"os"

	"github.com/jackc/pgx/v5"
)

type Repository struct {
	conn *pgx.Conn
}

func NewRepository(ctx context.Context, connStr string) (*Repository, error) {
	conn, err := pgx.Connect(ctx, connStr)
	if err != nil {
		_, _ = fmt.Fprintf(os.Stderr, "Unable to connect to database: %v\n", err)
		return nil, err
	}
	return &Repository{
		conn: conn,
	}, nil
}

func (r Repository) CreateCustomer(ctx context.Context, customer Customer) (Customer, error) {
	err := r.conn.QueryRow(ctx,
		"INSERT INTO customers (name, email) VALUES ($1, $2) RETURNING id",
		customer.Name, customer.Email).Scan(&customer.Id)
	return customer, err
}

func (r Repository) GetCustomerByEmail(ctx context.Context, email string) (Customer, error) {
	var customer Customer
	query := "SELECT id, name, email FROM customers WHERE email = $1"
	err := r.conn.QueryRow(ctx, query, email).
		Scan(&customer.Id, &customer.Name, &customer.Email)
	if err != nil {
		return Customer{}, err
	}
	return customer, nil
}
```

这段代码的作用是：

- `Repository` 持有一个 `*pgx.Conn` 用于执行数据库操作。
- `NewRepository(connStr)` 接收一个数据库连接字符串并初始化一个 `Repository`。
- `CreateCustomer()` 和 `GetCustomerByEmail()` 是 `Repository` 接收者上的方法，用于插入和查询客户记录。

## 使用 Testcontainers 编写测试

你已经准备好 `Repository` 实现，但测试需要一个 PostgreSQL 数据库。你可以使用 testcontainers-go 在 Docker 容器中启动一个 Postgres 数据库，并针对该数据库运行测试。

### 设置测试数据库

在真实应用中你可能会使用数据库迁移工具，但在本指南中，使用一个脚本来初始化数据库。

创建一个 `testdata/init-db.sql` 文件来创建 `CUSTOMERS` 表并插入示例数据：

```sql
CREATE TABLE IF NOT EXISTS customers (id serial, name varchar(255), email varchar(255));

INSERT INTO customers(name, email) VALUES ('John', 'john@gmail.com');
```

### 理解 testcontainers-go API

testcontainers-go 库提供了通用的 `Container` 抽象，可以运行任何容器化服务。为了进一步简化，testcontainers-go 提供了特定于技术的模块，可减少样板代码，并提供函数式选项（functional options）模式来构造容器实例。

例如，`PostgresContainer` 提供了 `WithDatabase()`、`WithUsername()`、`WithPassword()` 等函数来设置 Postgres 容器的各种属性。

### 编写测试

创建 `customer/repo_test.go` 文件并实现测试：

```go
package customer

import (
	"context"
	"path/filepath"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
	"github.com/testcontainers/testcontainers-go"
	"github.com/testcontainers/testcontainers-go/modules/postgres"
)

func TestCustomerRepository(t *testing.T) {
	ctx := context.Background()

	ctr, err := postgres.Run(ctx,
		"postgres:16-alpine",
		postgres.WithInitScripts(filepath.Join("..", "testdata", "init-db.sql")),
		postgres.WithDatabase("test-db"),
		postgres.WithUsername("postgres"),
		postgres.WithPassword("postgres"),
		postgres.BasicWaitStrategies(),
	)
	testcontainers.CleanupContainer(t, ctr)
	require.NoError(t, err)

	connStr, err := ctr.ConnectionString(ctx, "sslmode=disable")
	require.NoError(t, err)

	customerRepo, err := NewRepository(ctx, connStr)
	require.NoError(t, err)

	c, err := customerRepo.CreateCustomer(ctx, Customer{
		Name:  "Henry",
		Email: "henry@gmail.com",
	})
	assert.NoError(t, err)
	assert.NotNil(t, c)

	customer, err := customerRepo.GetCustomerByEmail(ctx, "henry@gmail.com")
	assert.NoError(t, err)
	assert.NotNil(t, customer)
	assert.Equal(t, "Henry", customer.Name)
	assert.Equal(t, "henry@gmail.com", customer.Email)
}
```

该测试的作用是：

- 调用 `postgres.Run()`，第一个参数为 `postgres:16-alpine` Docker 镜像。这是 v0.41.0 的 API——镜像是必需的 positional 参数，而非选项。
- 使用 `WithInitScripts(...)` 配置初始化脚本，以便在数据库启动后创建 `CUSTOMERS` 表并插入示例数据。
- 使用 `postgres.BasicWaitStrategies()`，它结合了等待 Postgres 日志消息和等待端口就绪。这取代了手动的等待策略配置。
- 在 `postgres.Run()` 之后立即调用 `testcontainers.CleanupContainer(t, ctr)`。这向测试框架注册自动清理，取代了手动的 `t.Cleanup` 和 `Terminate` 模式。
- 从容器获取数据库 `ConnectionString` 并初始化一个 `Repository`。
- 创建一个邮箱为 `henry@gmail.com` 的客户，并验证该客户存在于数据库中。

## 使用测试套件复用容器

在上一节中，你看到了如何为单个测试启动一个 Postgres Docker 容器。但你通常会在单个文件中有多个测试，并且可能希望为所有这些测试复用同一个 Postgres Docker 容器。

你可以使用 [testify suite](https://pkg.go.dev/github.com/stretchr/testify/suite) 包来实现通用的测试设置和拆解动作。

### 提取容器设置

首先，将 `PostgresContainer` 创建逻辑提取到一个名为 `testhelpers/containers.go` 的独立文件中：

```go
package testhelpers

import (
	"context"
	"path/filepath"
	"testing"

	"github.com/stretchr/testify/require"
	"github.com/testcontainers/testcontainers-go"
	"github.com/testcontainers/testcontainers-go/modules/postgres"
)

type PostgresContainer struct {
	*postgres.PostgresContainer
	ConnectionString string
}

func CreatePostgresContainer(t *testing.T, ctx context.Context) *PostgresContainer {
	t.Helper()

	ctr, err := postgres.Run(ctx,
		"postgres:16-alpine",
		postgres.WithInitScripts(filepath.Join("..", "testdata", "init-db.sql")),
		postgres.WithDatabase("test-db"),
		postgres.WithUsername("postgres"),
		postgres.WithPassword("postgres"),
		postgres.BasicWaitStrategies(),
	)
	testcontainers.CleanupContainer(t, ctr)
	require.NoError(t, err)

	connStr, err := ctr.ConnectionString(ctx, "sslmode=disable")
	require.NoError(t, err)

	return &PostgresContainer{
		PostgresContainer: ctr,
		ConnectionString:  connStr,
	}
}
```

在 `containers.go` 中，`PostgresContainer` 扩展了 testcontainers-go 的 `PostgresContainer` 以提供对 `ConnectionString` 的便捷访问。`CreatePostgresContainer()` 函数接受 `*testing.T` 作为第一个参数，调用 `t.Helper()` 以便测试失败时能指向调用方，并使用 `testcontainers.CleanupContainer()` 注册自动清理。

### 编写测试套件

创建 `customer/repo_suite_test.go`，并使用 testify suite 包实现创建客户和按邮箱获取客户的测试：

```go
package customer

import (
	"context"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
	"github.com/stretchr/testify/suite"
	"github.com/testcontainers/testcontainers-go-demo/testhelpers"
)

type CustomerRepoTestSuite struct {
	suite.Suite
	pgContainer *testhelpers.PostgresContainer
	repository  *Repository
	ctx         context.Context
}

func (suite *CustomerRepoTestSuite) SetupSuite() {
	suite.ctx = context.Background()
	suite.pgContainer = testhelpers.CreatePostgresContainer(suite.T(), suite.ctx)

	repository, err := NewRepository(suite.ctx, suite.pgContainer.ConnectionString)
	require.NoError(suite.T(), err)
	suite.repository = repository
}

func (suite *CustomerRepoTestSuite) TestCreateCustomer() {
	t := suite.T()

	customer, err := suite.repository.CreateCustomer(suite.ctx, Customer{
		Name:  "Henry",
		Email: "henry@gmail.com",
	})
	require.NoError(t, err)
	assert.NotNil(t, customer.Id)
}

func (suite *CustomerRepoTestSuite) TestGetCustomerByEmail() {
	t := suite.T()

	customer, err := suite.repository.GetCustomerByEmail(suite.ctx, "john@gmail.com")
	require.NoError(t, err)
	assert.Equal(t, "John", customer.Name)
	assert.Equal(t, "john@gmail.com", customer.Email)
}

func TestCustomerRepoTestSuite(t *testing.T) {
	suite.Run(t, new(CustomerRepoTestSuite))
}
```

这段代码的作用是：

- `CustomerRepoTestSuite` 扩展了 `suite.Suite`，并包含跨多个测试共享的字段。
- `SetupSuite()` 在所有测试之前运行一次。它调用 `CreatePostgresContainer(suite.T(), ...)`，后者通过 `CleanupContainer` 自动处理清理注册，因此不需要 `TearDownSuite()`。
- `TestCreateCustomer()` 对创建操作使用 `require.NoError()`（一旦出错立即失败），对 ID 检查使用 `assert.NotNil()`。
- `TestGetCustomerByEmail()` 使用 `require.NoError()`，然后对返回值进行断言。
- `TestCustomerRepoTestSuite(t *testing.T)` 在你执行 `go test` 时运行该测试套件。

> [!TIP]
> 出于本指南的目的，这些测试不会重置数据库中的数据。
> 在实践中，在运行每个测试之前将数据库重置为已知状态是个好主意。

## 运行测试与后续步骤

### 运行测试

使用 `go test ./...` 运行所有测试。可选地添加 `-v` 标志以获得详细输出：

```console
$ go test -v ./...
```

你应该会看到两个 Postgres Docker 容器自动启动：一个用于套件及其两个测试，另一个用于最初的独立测试。所有测试都应通过。测试完成后，容器会自动停止并移除。

### 小结

Testcontainers for Go 库帮助你编写使用与生产相同类型数据库（Postgres）的集成测试，而不是使用 mock。由于你没有使用 mock，而是与真实服务通信，因此你可以自由重构代码，同时仍能验证应用按预期工作。

要了解更多关于 Testcontainers 的信息，请访问
[Testcontainers 概览](https://testcontainers.com/getting-started/)。

### 延伸阅读

- [Testcontainers for Go 文档](https://golang.testcontainers.org/)
- [Testcontainers for Go 快速入门](https://golang.testcontainers.org/quickstart/)
- [Testcontainers Postgres 模块 for Go](https://golang.testcontainers.org/modules/postgres/)
