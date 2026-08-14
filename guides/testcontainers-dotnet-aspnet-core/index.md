# 使用 Testcontainers 测试 ASP.NET Core Web 应用



<!-- Source: https://github.com/testcontainers/tc-guide-testing-aspnet-core -->

在本指南中，你将学习如何：

- 使用 Testcontainers for .NET 启动一个用于集成测试的 Microsoft SQL Server 容器
- 在 ASP.NET Core 测试中用类似生产的数据库提供程序替换 SQLite
- 自定义 `WebApplicationFactory` 以使用 Testcontainers 配置测试依赖
- 使用 xUnit 的 `IAsyncLifetime` 管理容器生命周期

## 先决条件

- .NET 8.0+ SDK
- 代码编辑器或 IDE（Visual Studio、VS Code、Rider）
- Testcontainers 支持的 Docker 环境。详情请参阅
  [Testcontainers .NET 系统要求](https://dotnet.testcontainers.org/supported_docker_environment/)。

> [!NOTE]
> 如果你是 Testcontainers 的新手，请访问
> [Testcontainers 概览](https://testcontainers.com/getting-started/) 以了解更多关于
> Testcontainers 及其优势的信息。

## 设置项目

### 背景

本指南基于 Microsoft 的
[ASP.NET Core 中的集成测试](https://learn.microsoft.com/en-us/aspnet/core/test/integration-tests)
文档构建。原始示例使用内存中的 SQLite 数据库作为集成测试的底层存储。你将使用
Testcontainers，用运行在 Docker 容器中的真实 Microsoft SQL Server 实例替换 SQLite。

你可以在
[dotnet/AspNetCore.Docs.Samples](https://github.com/dotnet/AspNetCore.Docs.Samples/tree/main/test/integration-tests/IntegrationTestsSample)
仓库中找到原始代码示例。

### 克隆仓库

克隆 Testcontainers 指南仓库并进入项目目录：

```console
$ git clone https://github.com/testcontainers/tc-guide-testing-aspnet-core.git
$ cd tc-guide-testing-aspnet-core
```

### 项目结构

该解决方案包含两个项目：

```text
RazorPagesProject.sln
├── src/RazorPagesProject/              # ASP.NET Core Razor Pages 应用
└── tests/RazorPagesProject.Tests/      # xUnit 集成测试
```

#### 应用项目

应用项目（`src/RazorPagesProject/RazorPagesProject.csproj`）
是一个 Razor Pages Web 应用，使用 Entity Framework Core，并以 SQLite 作为默认的数据库提供程序：

```xml
<Project Sdk="Microsoft.NET.Sdk.Web">

  <PropertyGroup>
    <TargetFramework>net9.0</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="Microsoft.EntityFrameworkCore.Sqlite" Version="7.0.0" />
    <PackageReference Include="Microsoft.AspNetCore.Diagnostics.EntityFrameworkCore" Version="7.0.0" />
    <PackageReference Include="Microsoft.AspNetCore.Identity.EntityFrameworkCore" Version="7.0.0" />
    <PackageReference Include="Microsoft.AspNetCore.Identity.UI" Version="7.0.0" />
    <PackageReference Include="Microsoft.EntityFrameworkCore.Tools" Version="7.0.0">
      <PrivateAssets>all</PrivateAssets>
      <IncludeAssets>runtime; build; native; contentfiles; analyzers; buildtransitive</IncludeAssets>
    </PackageReference>
  </ItemGroup>

</Project>
```

`ApplicationDbContext` 存储 `Message` 实体，并提供查询和管理它们的方法：

```csharp
public class ApplicationDbContext : IdentityDbContext
{
    public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
        : base(options)
    {
    }

    public virtual DbSet<Message> Messages { get; set; }

    public async virtual Task<List<Message>> GetMessagesAsync()
    {
        return await Messages
            .OrderBy(message => message.Text)
            .AsNoTracking()
            .ToListAsync();
    }

    public async virtual Task AddMessageAsync(Message message)
    {
        await Messages.AddAsync(message);
        await SaveChangesAsync();
    }

    public async virtual Task DeleteAllMessagesAsync()
    {
        foreach (Message message in Messages)
        {
            Messages.Remove(message);
        }

        await SaveChangesAsync();
    }

    public async virtual Task DeleteMessageAsync(int id)
    {
        var message = await Messages.FindAsync(id);

        if (message != null)
        {
            Messages.Remove(message);
            await SaveChangesAsync();
        }
    }

    public void Initialize()
    {
        Messages.AddRange(GetSeedingMessages());
        SaveChanges();
    }

    public static List<Message> GetSeedingMessages()
    {
        return new List<Message>()
        {
            new Message(){ Text = "You're standing on my scarf." },
            new Message(){ Text = "Would you like a jelly baby?" },
            new Message(){ Text = "To the rational mind, nothing is inexplicable; only unexplained." }
        };
    }
}
```

#### 测试项目

测试项目（`tests/RazorPagesProject.Tests/RazorPagesProject.Tests.csproj`）
包含 xUnit、ASP.NET Core 测试基础设施，以及 Testcontainers MSSQL 模块：

```xml
<Project Sdk="Microsoft.NET.Sdk.Web">

  <PropertyGroup>
    <TargetFramework>net9.0</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="AngleSharp" Version="0.17.1" />
    <PackageReference Include="Microsoft.AspNetCore.Diagnostics.EntityFrameworkCore" Version="7.0.0" />
    <PackageReference Include="Microsoft.AspNetCore.Identity.EntityFrameworkCore" Version="7.0.0" />
    <PackageReference Include="Microsoft.AspNetCore.Identity.UI" Version="7.0.0" />
    <PackageReference Include="Microsoft.AspNetCore.Mvc.Testing" Version="7.0.0" />
    <PackageReference Include="Microsoft.EntityFrameworkCore" Version="7.0.0" />
    <PackageReference Include="Microsoft.EntityFrameworkCore.Sqlite" Version="7.0.0" />
    <PackageReference Include="Microsoft.EntityFrameworkCore.SqlServer" Version="7.0.0" />
    <PackageReference Include="Microsoft.EntityFrameworkCore.Tools" Version="7.0.0">
      <PrivateAssets>all</PrivateAssets>
      <IncludeAssets>runtime; build; native; contentfiles; analyzers; buildtransitive</IncludeAssets>
    </PackageReference>

    <PackageReference Include="Microsoft.NET.Test.Sdk" Version="17.4.0" />

    <PackageReference Include="Testcontainers.MsSql" Version="3.0.0" />
    <PackageReference Include="xunit" Version="2.4.2" />
    <PackageReference Include="xunit.runner.visualstudio" Version="2.4.5">
      <PrivateAssets>all</PrivateAssets>
      <IncludeAssets>runtime; build; native; contentfiles; analyzers; buildtransitive</IncludeAssets>
    </PackageReference>
  </ItemGroup>

  <ItemGroup>
    <ProjectReference Include="..\..\src\RazorPagesProject\RazorPagesProject.csproj" />
  </ItemGroup>

  <ItemGroup>
    <Content Update="xunit.runner.json">
      <CopyToOutputDirectory>Always</CopyToOutputDirectory>
    </Content>
  </ItemGroup>

</Project>
```

关键的依赖项有：

- `Microsoft.AspNetCore.Mvc.Testing` —— 提供用于在测试中引导应用的 `WebApplicationFactory`
- `Microsoft.EntityFrameworkCore.SqlServer` —— 用于 Entity Framework Core 的 SQL Server 数据库提供程序
- `Testcontainers.MsSql` —— 用于 Microsoft SQL Server 的 Testcontainers 模块

#### 现有的基于 SQLite 的测试工厂

原始项目包含一个 `CustomWebApplicationFactory`，它将应用的数据库替换为内存中的 SQLite 实例：

```csharp
public class CustomWebApplicationFactory<TProgram>
    : WebApplicationFactory<TProgram> where TProgram : class
{
    protected override void ConfigureWebHost(IWebHostBuilder builder)
    {
        builder.ConfigureServices(services =>
        {
            var dbContextDescriptor = services.SingleOrDefault(
                d => d.ServiceType ==
                    typeof(DbContextOptions<ApplicationDbContext>));

            services.Remove(dbContextDescriptor);

            var dbConnectionDescriptor = services.SingleOrDefault(
                d => d.ServiceType ==
                    typeof(DbConnection));

            services.Remove(dbConnectionDescriptor);

            // Create open SqliteConnection so EF won't automatically close it.
            services.AddSingleton<DbConnection>(container =>
            {
                var connection = new SqliteConnection("DataSource=:memory:");
                connection.Open();

                return connection;
            });

            services.AddDbContext<ApplicationDbContext>((container, options) =>
            {
                var connection = container.GetRequiredService<DbConnection>();
                options.UseSqlite(connection);
            });
        });

        builder.UseEnvironment("Development");
    }
}
```

虽然这种方法可行，但 SQLite 与你生产中使用的数据库存在行为差异。在下一节中，你将用 Testcontainers 管理的 Microsoft SQL Server 实例替换它。

## 使用 Testcontainers 编写测试

现有的测试使用内存中的 SQLite 数据库。虽然方便，但这与生产行为并不一致。你可以用 Testcontainers 管理的真实 Microsoft SQL Server 实例替换它。

### 添加依赖

切换到测试项目目录，并添加 SQL Server Entity Framework 提供程序和 Testcontainers MSSQL 模块：

```console
$ cd tests/RazorPagesProject.Tests
$ dotnet add package Microsoft.EntityFrameworkCore.SqlServer --version 7.0.0
$ dotnet add package Testcontainers.MsSql --version 3.0.0
```

> [!NOTE]
> Testcontainers for .NET 提供了一系列遵循最佳实践配置的
> [模块](https://www.nuget.org/profiles/Testcontainers)。

### 创建测试类

在 `IntegrationTests` 目录中创建一个 `MsSqlTests.cs` 文件。该类管理 SQL Server 容器的生命周期，并包含一个嵌套的测试类。

```csharp
using System.Data.Common;
using System.Net;
using AngleSharp.Html.Dom;
using Microsoft.AspNetCore.Mvc.Testing;
using Microsoft.EntityFrameworkCore;
using RazorPagesProject.Data;
using RazorPagesProject.Tests.Helpers;
using Testcontainers.MsSql;
using Xunit;

namespace RazorPagesProject.Tests.IntegrationTests;

public sealed class MsSqlTests : IAsyncLifetime
{
    private readonly MsSqlContainer _msSqlContainer = new MsSqlBuilder().Build();

    public Task InitializeAsync()
    {
        return _msSqlContainer.StartAsync();
    }

    public Task DisposeAsync()
    {
        return _msSqlContainer.DisposeAsync().AsTask();
    }

    public sealed class IndexPageTests : IClassFixture<MsSqlTests>, IDisposable
    {
        private readonly WebApplicationFactory<Program> _webApplicationFactory;

        private readonly HttpClient _httpClient;

        public IndexPageTests(MsSqlTests fixture)
        {
            var clientOptions = new WebApplicationFactoryClientOptions();
            clientOptions.AllowAutoRedirect = false;

            _webApplicationFactory = new CustomWebApplicationFactory(fixture);
            _httpClient = _webApplicationFactory.CreateClient(clientOptions);
        }

        public void Dispose()
        {
            _webApplicationFactory.Dispose();
        }

        [Fact]
        public async Task Post_DeleteAllMessagesHandler_ReturnsRedirectToRoot()
        {
            // Arrange
            var defaultPage = await _httpClient.GetAsync("/")
                .ConfigureAwait(false);

            var document = await HtmlHelpers.GetDocumentAsync(defaultPage)
                .ConfigureAwait(false);

            // Act
            var form = (IHtmlFormElement)document.QuerySelector("form[id='messages']");
            var submitButton = (IHtmlButtonElement)document.QuerySelector("button[id='deleteAllBtn']");

            var response = await _httpClient.SendAsync(form, submitButton)
                .ConfigureAwait(false);

            // Assert
            Assert.Equal(HttpStatusCode.OK, defaultPage.StatusCode);
            Assert.Equal(HttpStatusCode.Redirect, response.StatusCode);
            Assert.Equal("/", response.Headers.Location.OriginalString);
        }

        private sealed class CustomWebApplicationFactory : WebApplicationFactory<Program>
        {
            private readonly string _connectionString;

            public CustomWebApplicationFactory(MsSqlTests fixture)
            {
                _connectionString = fixture._msSqlContainer.GetConnectionString();
            }

            protected override void ConfigureWebHost(IWebHostBuilder builder)
            {
                builder.ConfigureServices(services =>
                {
                    services.Remove(services.SingleOrDefault(service => typeof(DbContextOptions<ApplicationDbContext>) == service.ServiceType));
                    services.Remove(services.SingleOrDefault(service => typeof(DbConnection) == service.ServiceType));
                    services.AddDbContext<ApplicationDbContext>((_, option) => option.UseSqlServer(_connectionString));
                });
            }
        }
    }
}
```

### 理解测试结构

#### 使用 IAsyncLifetime 管理容器生命周期

外部的 `MsSqlTests` 类实现了 `IAsyncLifetime`。xUnit 在创建类实例后立即调用
`InitializeAsync()`，这会启动 SQL Server 容器。所有测试完成后，`DisposeAsync()` 会停止并移除容器。

```csharp
private readonly MsSqlContainer _msSqlContainer = new MsSqlBuilder().Build();
```

`MsSqlBuilder().Build()` 创建一个预配置的 Microsoft SQL Server 容器。Testcontainers 模块遵循最佳实践，因此你无需自行配置端口、密码或启动等待策略。

#### 使用 IClassFixture 的嵌套测试类

`IndexPageTests` 类嵌套在 `MsSqlTests` 内部，并实现了
`IClassFixture<MsSqlTests>`。这让测试类可以访问容器的私有字段，并在测试资源管理器中形成清晰的层次结构。

#### 自定义的 WebApplicationFactory

嵌套的 `CustomWebApplicationFactory` 从运行中的 SQL Server 容器获取连接字符串，并将其传递给 `UseSqlServer()`，而不是使用基于 SQLite 的工厂：

```csharp
private sealed class CustomWebApplicationFactory : WebApplicationFactory<Program>
{
    private readonly string _connectionString;

    public CustomWebApplicationFactory(MsSqlTests fixture)
    {
        _connectionString = fixture._msSqlContainer.GetConnectionString();
    }

    protected override void ConfigureWebHost(IWebHostBuilder builder)
    {
        builder.ConfigureServices(services =>
        {
            services.Remove(services.SingleOrDefault(service => typeof(DbContextOptions<ApplicationDbContext>) == service.ServiceType));
            services.Remove(services.SingleOrDefault(service => typeof(DbConnection) == service.ServiceType));
            services.AddDbContext<ApplicationDbContext>((_, option) => option.UseSqlServer(_connectionString));
        });
    }
}
```

该工厂：

1. 移除现有的 `DbContextOptions<ApplicationDbContext>` 注册
2. 移除现有的 `DbConnection` 注册
3. 添加一个新的 `ApplicationDbContext`，配置为使用来自 Testcontainers 管理容器的 SQL Server 连接字符串

> [!NOTE]
> Microsoft SQL Server 的 Docker 镜像与 ARM 设备（如搭载 Apple Silicon 的 Mac）不兼容。你可以使用
> [SqlEdge](https://www.nuget.org/packages/Testcontainers.SqlEdge) 模块或
> [Testcontainers Cloud](https://www.testcontainers.cloud/) 作为替代方案。

## 运行测试与后续步骤

### 运行测试

从解决方案根目录运行测试：

```console
$ dotnet test ./RazorPagesProject.sln
```

首次运行可能较慢，因为 Docker 需要拉取 Microsoft SQL Server 镜像。后续运行会使用该镜像的本地缓存。

你应该会看到 xUnit 发现并运行测试，包括 `MsSqlTests.IndexPageTests` 类。Testcontainers 启动一个 SQL Server 容器，测试针对它执行，测试完成后容器会自动停止并移除。

### 小结

通过将 SQLite 替换为 Testcontainers 管理的 Microsoft SQL Server 实例，集成测试将针对与生产中所用相同类型的数据库运行。这种方法能尽早发现特定于数据库的问题，例如 SQLite 与 SQL Server 之间在 SQL 方言、事务行为或数据类型处理上的差异。

`MsSqlTests` 类使用 `IAsyncLifetime` 管理容器生命周期，嵌套的 `CustomWebApplicationFactory` 将容器的连接字符串接入应用的服务配置。你可以将同样的模式应用于 Testcontainers 支持的任何数据库或服务。

要了解更多关于 Testcontainers 的信息，请访问
[Testcontainers 概览](https://testcontainers.com/getting-started/)。

### 延伸阅读

- [Testcontainers for .NET 文档](https://dotnet.testcontainers.org/)
- [Testcontainers for .NET 模块](https://dotnet.testcontainers.org/modules/)
- [Microsoft SQL Server 模块](https://www.nuget.org/packages/Testcontainers.MsSql)
- [ASP.NET Core 中的集成测试](https://learn.microsoft.com/en-us/aspnet/core/test/integration-tests)

