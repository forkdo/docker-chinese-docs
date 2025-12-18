---
title: 使用 Provider 服务
description: 了解如何在 Docker Compose 中使用 Provider 服务，将外部功能集成到您的应用程序中
keywords: compose, docker compose, provider, services, platform capabilities, integration, model runner, ai
weight: 112
params:
  sidebar:
    badge:
      color: green
      text: 新功能
---

{{< summary-bar feature_name="Compose provider services" >}}

Docker Compose 支持 Provider 服务，允许您集成由第三方组件而非 Compose 本身管理生命周期的服务。
此功能使您能够定义和使用平台特定服务，而无需手动设置或直接生命周期管理。

## 什么是 Provider 服务？

Provider 服务是 Compose 中一种特殊类型的服务，它代表平台能力而非容器。
它们允许您声明应用程序所需的特定平台功能依赖。

当您在 Compose 文件中定义 Provider 服务时，Compose 会与平台协作，提供并配置请求的功能，使其可用于您的应用程序服务。

## 使用 Provider 服务

要在 Compose 文件中使用 Provider 服务，您需要：

1. 定义带有 `provider` 属性的服务
2. 指定要使用的 Provider 的 `type`
3. 配置 Provider 特定的选项
4. 从应用程序服务声明对 Provider 服务的依赖

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

注意 `database` 服务中的专用 `provider` 属性。
此属性指定服务由 Provider 管理，并允许您定义该 Provider 类型特定的选项。

`app` 服务中的 `depends_on` 属性指定它依赖于 `database` 服务。
这意味着 `database` 服务将在 `app` 服务之前启动，允许 Provider 信息注入到 `app` 服务中。

## 工作原理

在执行 `docker compose up` 命令期间，Compose 识别依赖 Provider 的服务，并与它们协作提供请求的功能。
然后 Provider 使用有关如何访问已提供资源的信息填充 Compose 模型。

这些信息传递给声明对 Provider 服务依赖的服务，通常通过环境变量。
这些变量的命名约定是：

```env
<<PROVIDER_SERVICE_NAME>>_<<VARIABLE_NAME>>
```

例如，如果您的 Provider 服务名为 `database`，您的应用程序服务可能会收到如下环境变量：

- `DATABASE_URL` 包含访问已提供资源的 URL
- `DATABASE_TOKEN` 包含身份验证令牌
- 其他 Provider 特定变量

您的应用程序然后可以使用这些环境变量与已提供的资源交互。

## Provider 类型

Provider 服务中的 `type` 字段引用以下之一的名称：

1. Docker CLI 插件（例如 `docker-model`）
2. 用户 PATH 中可用的二进制文件
3. 要执行的二进制文件或脚本的路径

当 Compose 遇到 Provider 服务时，它会查找具有指定名称的插件或二进制文件来处理请求功能的提供。

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

1. 解释 Provider 服务中提供的选项
2. 提供请求的功能
3. 返回有关如何访问已提供资源的信息

然后这些信息作为环境变量传递给依赖服务。

> [!TIP]
>
> 如果您在 Compose 中使用 AI 模型，请改用 [`models` 顶级元素](/manuals/ai/compose/models-and-compose.md)。

## 使用 Provider 服务的好处

在 Compose 应用程序中使用 Provider 服务有几个好处：

1. 简化配置：您无需手动配置和管理平台功能
2. 声明式方法：您可以在一个地方声明应用程序的所有依赖
3. 一致的工作流：您使用相同的 Compose 命令管理整个应用程序，包括平台功能

## 创建您自己的 Provider

如果您想创建自己的 Provider 来使用自定义功能扩展 Compose，可以实现一个注册 Provider 类型的 Compose 插件。

有关如何创建和实现您自己的 Provider 的详细信息，请参阅 [Compose Extensions 文档](https://github.com/docker/compose/blob/main/docs/extension.md)。
此指南解释了允许您向 Compose 添加新 Provider 类型的扩展机制。

## 参考

- [Docker Model Runner 文档](/manuals/ai/model-runner.md)
- [Compose Extensions 文档](https://github.com/docker/compose/blob/main/docs/extension.md)