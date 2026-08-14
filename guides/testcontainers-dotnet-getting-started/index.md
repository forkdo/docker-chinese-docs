# Testcontainers for .NET 入门



<!-- Source: https://github.com/testcontainers/tc-guide-getting-started-with-testcontainers-for-dotnet -->

在本指南中，你将学习如何：

- 创建一个包含源项目和测试项目的 .NET 解决方案
- 实现一个在 PostgreSQL 中管理客户记录的 `CustomerService`
- 使用 Testcontainers 和 xUnit 编写集成测试
- 使用 `IAsyncLifetime` 管理容器生命周期

## 先决条件

- .NET 8.0+ SDK
- Testcontainers 支持的 Docker 环境

> [!NOTE]
> 如果你是 Testcontainers 的新手，请访问
> [Testcontainers 概览](https://testcontainers.com/getting-started/) 以了解更多关于
> Testcontainers 及其优势的信息。

## 创建 .NET 项目

### 设置解决方案

创建一个包含源项目和测试项目的 .NET 解决方案：

```console
$ dotnet new sln -o TestcontainersDemo
$ cd TestcontainersDemo
$ dotnet new classlib -o CustomerService
$ dotnet sln add ./CustomerService/CustomerService.csproj
$ dotnet new xunit -o CustomerService.Tests
$ dotnet sln add ./CustomerService.Tests/CustomerService.Tests.csproj
$ dotnet add ./CustomerService.Tests/CustomerService.Tests.csproj reference ./CustomerService/CustomerService.csproj
```

向源项目添加 Npgsql 依赖：

```console
$ dotnet add ./CustomerService/CustomerService.csproj package Npgsql
```

### 实现业务逻辑

创建一个 `Customer` 记录类型：

```csharp
namespace Customers;

public readonly record struct Customer(long Id, string Name);
```

创建一个 `DbConnectionProvider` 类来管理数据库连接：

```csharp
using System.Data.Common;
using Npgsql;

namespace Customers;

public sealed class DbConnectionProvider
{
    private readonly string _connectionString;

    public DbConnectionProvider(string connectionString)
    {
        _connectionString = connectionString;
    }

    public DbConnection GetConnection()
    {
        return new NpgsqlConnection(_connectionString);
    }
}
```

创建 `CustomerService` 类：

```csharp
namespace Customers;

public sealed class CustomerService
{
    private readonly DbConnectionProvider _dbConnectionProvider;

    public CustomerService(DbConnectionProvider dbConnectionProvider)
    {
        _dbConnectionProvider = dbConnectionProvider;
        CreateCustomersTable();
    }

    public IEnumerable<Customer> GetCustomers()
    {
        IList<Customer> customers = new List<Customer>();

        using var connection = _dbConnectionProvider.GetConnection();
        using var command = connection.CreateCommand();
        command.CommandText = "SELECT id, name FROM customers";
        command.Connection?.Open();

        using var dataReader = command.ExecuteReader();
        while (dataReader.Read())
        {
            var id = dataReader.GetInt64(0);
            var name = dataReader.GetString(1);
            customers.Add(new Customer(id, name));
        }

        return customers;
    }

    public void Create(Customer customer)
    {
        using var connection = _dbConnectionProvider.GetConnection();
        using var command = connection.CreateCommand();

        var id = command.CreateParameter();
        id.ParameterName = "@id";
        id.Value = customer.Id;

        var name = command.CreateParameter();
        name.ParameterName = "@name";
        name.Value = customer.Name;

        command.CommandText = "INSERT INTO customers (id, name) VALUES(@id, @name)";
        command.Parameters.Add(id);
        command.Parameters.Add(name);
        command.Connection?.Open();
        command.ExecuteNonQuery();
    }

    private void CreateCustomersTable()
    {
        using var connection = _dbConnectionProvider.GetConnection();
        using var command = connection.CreateCommand();
        command.CommandText = "CREATE TABLE IF NOT EXISTS customers (id BIGINT NOT NULL, name VARCHAR NOT NULL, PRIMARY KEY (id))";
        command.Connection?.Open();
        command.ExecuteNonQuery();
    }
}
```

`CustomerService` 的作用如下：

- 构造函数调用 `CreateCustomersTable()` 以确保表存在。
- `GetCustomers()` 从 `customers` 表获取所有行，并将其作为 `Customer` 对象返回。
- `Create()` 向数据库插入一条客户记录。

## 使用 Testcontainers 编写测试

### 添加 Testcontainers 依赖

向测试项目添加 Testcontainers PostgreSQL 模块：

```console
$ dotnet add ./CustomerService.Tests/CustomerService.Tests.csproj package Testcontainers.PostgreSql
```

### 编写测试

在测试项目中创建 `CustomerServiceTest.cs`：

```csharp
using Testcontainers.PostgreSql;

namespace Customers.Tests;

public sealed class CustomerServiceTest : IAsyncLifetime
{
    private readonly PostgreSqlContainer _postgres = new PostgreSqlBuilder()
        .WithImage("postgres:16-alpine")
        .Build();

    public Task InitializeAsync()
    {
        return _postgres.StartAsync();
    }

    public Task DisposeAsync()
    {
        return _postgres.DisposeAsync().AsTask();
    }

    [Fact]
    public void ShouldReturnTwoCustomers()
    {
        // Given
        var customerService = new CustomerService(new DbConnectionProvider(_postgres.GetConnectionString()));

        // When
        customerService.Create(new Customer(1, "George"));
        customerService.Create(new Customer(2, "John"));
        var customers = customerService.GetCustomers();

        // Then
        Assert.Equal(2, customers.Count());
    }
}
```

该测试的作用是：

- 使用 `PostgreSqlBuilder` 并指定 `postgres:16-alpine` Docker 镜像，声明一个 `PostgreSqlContainer`。
- 实现 `IAsyncLifetime` 以管理容器生命周期：
  - `InitializeAsync()` 在测试运行前启动容器。
  - `DisposeAsync()` 在测试完成后停止并移除容器。
- `ShouldReturnTwoCustomers()` 使用来自容器的连接信息创建一个 `CustomerService`，插入两名客户，获取所有客户，并断言数量。

## 运行测试与后续步骤

### 运行测试

运行测试：

```console
$ dotnet test
```

你可以在输出中看到 Testcontainers 从 Docker Hub 拉取 Postgres Docker 镜像（如果本地尚不可用），启动容器，并运行测试。

使用 Testcontainers 编写集成测试与你从 IDE 运行的单元测试并无二致。你的团队成员可以克隆项目并运行测试，而无需在机器上安装 Postgres。

### 小结

Testcontainers for .NET 库帮助你编写使用与生产相同类型数据库（Postgres）的集成测试，而不是使用 mock。由于你没有使用 mock，而是与真实服务通信，因此你可以自由重构代码，同时仍能验证应用按预期工作。

除了 Postgres，Testcontainers 还为许多 SQL 数据库、NoSQL 数据库、消息队列等提供了专用的
[模块](https://www.nuget.org/profiles/Testcontainers)。

要了解更多关于 Testcontainers 的信息，请访问
[Testcontainers 概览](https://testcontainers.com/getting-started/)。

### 延伸阅读

- [测试 ASP.NET Core Web 应用](https://testcontainers.com/guides/testing-an-aspnet-core-web-app/)

