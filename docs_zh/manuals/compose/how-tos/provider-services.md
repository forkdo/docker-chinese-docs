---
title: 使用提供者服务
description: 了解如何在 Docker Compose 中使用提供者服务，将外部功能集成到应用程序中
keywords: compose, docker compose, provider, services, platform capabilities, integration, model runner, ai
weight: 112
params:
  sidebar:
    badge:
      color: green
      text: 新增
---

{{< summary-bar feature_name="Compose provider services" >}}

Docker Compose 支持提供者服务，允许集成由第三方组件管理生命周期（而非由 Compose 本身管理）的服务。  
此功能使您能够定义和使用特定于平台的服务，而无需手动设置或直接管理生命周期。

## 什么是提供者服务？

提供者服务是 Compose 中一种特殊类型的服务，它代表平台功能而非容器。  
它们允许您声明应用程序所需的特定平台功能的依赖关系。

当您在 Compose 文件中定义提供者服务时，Compose 会与平台协作，配置并置备所请求的功能，使其可供您的应用程序服务使用。

## 使用提供者服务

要在 Compose 文件中使用提供者服务，您需要：

1. 使用 `provider` 属性定义服务
2. 指定要使用的提供者 `type`（类型）
3. 配置任何特定于提供者的选项
4. 从应用程序服务声明对提供者服务的依赖关系

以下是一个基本示例：

```yaml
services:
  database:
    provider:
      type: awesomecloud
      options:
        type: mysql
        foo: bar  
  app:
    image: myapp 
    depends_on:
       - database
```

请注意 `database` 服务中的专用 `provider` 属性。  
此属性指定该服务由提供者管理，并允许您定义特定于该提供者类型的选项。

`app` 服务中的 `depends_on` 属性指定它依赖于 `database` 服务。  
这意味着 `database` 服务将在 `app` 服务之前启动，从而允许将提供者信息注入到 `app` 服务中。

## 工作原理

在执行 `docker compose up` 命令期间，Compose 会识别依赖提供者的服务，并与它们协作以置备所请求的功能。然后，提供者会用有关如何访问已置备资源的信息填充 Compose 模型。

此信息会传递给声明对提供者服务有依赖关系的服务，通常通过环境变量传递。这些变量的命名约定为：

```env
<<PROVIDER_SERVICE_NAME>>_<<VARIABLE_NAME>>
```

例如，如果您的提供者服务名为 `database`，您的应用程序服务可能会收到如下环境变量：

- `DATABASE_URL`：访问已置备资源的 URL
- `DATABASE_TOKEN`：身份验证令牌
- 其他特定于提供者的变量

然后，您的应用程序可以使用这些环境变量与已置备的资源进行交互。

## 提供者类型

提供者服务中的 `type` 字段引用以下任一项的名称：

1. Docker CLI 插件（例如 `docker-model`）
2. 用户 PATH 中可用的二进制文件
3. 要执行的二进制文件或脚本的路径

当 Compose 遇到提供者服务时，它会查找具有指定名称的插件或二进制文件来处理所请求功能的置备。

例如，如果您指定 `type: model`，Compose 将查找名为 `docker-model` 的 Docker CLI 插件或 PATH 中名为 `model` 的二进制文件。

```yaml
services:
  ai-runner:
    provider:
      type: model  # 查找 docker-model 插件或 model 二进制文件
      options:
        model: ai/example-model
```

插件或二进制文件负责：

1. 解释提供者服务中提供的选项
2. 置备所请求的功能
3. 返回有关如何访问已置备资源的信息

然后，此信息会作为环境变量传递给依赖服务。

> [!TIP]
>
> 如果您要在 Compose 中使用 AI 模型，请改用 [`models` 顶级元素](/manuals/ai/compose/models-and-compose.md)。

## 使用提供者服务的好处

在 Compose 应用程序中使用提供者服务可提供多项好处：

1. 简化配置：您无需手动配置和管理平台功能
2. 声明式方法：您可以在一个地方声明应用程序的所有依赖关系
3. 一致的工作流：您可以使用相同的 Compose 命令管理整个应用程序，包括平台功能

## 创建您自己的提供者

如果您想创建自己的提供者，以通过自定义功能扩展 Compose，可以实现一个 Compose 插件来注册提供者类型。

有关如何创建和实现您自己的提供者的详细信息，请参阅 [Compose 扩展文档](https://github.com/docker/compose/blob/main/docs/extension.md)。  
本指南解释了允许您向 Compose 添加新提供者类型的扩展机制。

## 参考

- [Docker 模型运行器文档](/manuals/ai/model-runner.md)
- [Compose 扩展文档](https://github.com/docker/compose/blob/main/docs/extension.md)