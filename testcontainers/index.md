# Testcontainers


Testcontainers 是一组开源库，提供了简单且轻量级的 API，用于通过 Docker 容器封装的真实服务来引导本地开发和测试依赖项。
使用 Testcontainers，您可以编写依赖于生产环境中使用的相同服务的测试，而无需使用模拟或内存服务。



## 快速入门

### 支持的语言

Testcontainers 为最流行的语言提供支持，Docker 赞助了以下 Testcontainers 实现的开发：

- [Go](https://golang.testcontainers.org/quickstart/)
- [Java](https://java.testcontainers.org/quickstart/junit_5_quickstart/)

其余版本由社区驱动，并由独立贡献者维护。

### 先决条件

Testcontainers 需要一个兼容 Docker API 的容器运行时。
在开发过程中，Testcontainers 会针对 Linux 上的最新 Docker 版本以及 Mac 和 Windows 上的 Docker Desktop 进行积极测试。
Testcontainers 会自动检测并使用这些 Docker 环境，无需进行任何额外配置。

可以配置 Testcontainers 以适用于其他 Docker 设置，例如远程 Docker 主机或 Docker 替代方案。
但是，这些设置不会在主开发工作流程中积极测试，因此可能无法使用所有 Testcontainers 功能，
并且可能需要额外的手动配置。

如果您对您的设置配置细节或是否支持运行基于 Testcontainers 的测试有进一步疑问，
请在 [Slack](https://slack.testcontainers.org/) 上联系 Testcontainers 团队以及 Testcontainers 社区的其他用户。

 

## 指南

探索动手实践性的 Testcontainers 指南，了解如何在不同语言和流行框架中使用 Testcontainers：

- [.NET 版 Testcontainers 入门](/guides/testcontainers-dotnet-getting-started/)
- [Go 版 Testcontainers 入门](/guides/testcontainers-go-getting-started/)
- [Java 版 Testcontainers 入门](/guides/testcontainers-java-getting-started/)
- [Node.js 版 Testcontainers 入门](/guides/testcontainers-nodejs-getting-started/)
- [Python 版 Testcontainers 入门](/guides/testcontainers-python-getting-started/)
- [使用 Testcontainers 测试 Spring Boot REST API](/guides/testcontainers-java-spring-boot-rest-api/)
- [Testcontainers 容器生命周期管理](/guides/testcontainers-java-lifecycle/)
- [用真实数据库替换 H2 进行测试](/guides/testcontainers-java-replace-h2/)
- [在容器中运行的服务配置](/guides/testcontainers-java-service-configuration/)
- [测试 ASP.NET Core Web 应用](/guides/testcontainers-dotnet-aspnet-core/)
- [测试 Spring Boot Kafka 监听器](/guides/testcontainers-java-spring-boot-kafka/)
- [使用 MockServer 测试 REST API 集成](/guides/testcontainers-java-mockserver/)
- [使用 LocalStack 测试 AWS 服务集成](/guides/testcontainers-java-aws-localstack/)
- [使用 Testcontainers 测试 Quarkus 应用](/guides/testcontainers-java-quarkus/)
- [在 Testcontainers 中使用 jOOQ 和 Flyway](/guides/testcontainers-java-jooq-flyway/)
- [使用 WireMock 测试 REST API 集成](/guides/testcontainers-java-wiremock/)
- [使用 Keycloak 和 Testcontainers 保护 Spring Boot 安全](/guides/testcontainers-java-keycloak-spring-boot/)
- [使用 WireMock 测试 Micronaut REST API](/guides/testcontainers-java-micronaut-wiremock/)
- [测试 Micronaut Kafka 监听器](/guides/testcontainers-java-micronaut-kafka/)

