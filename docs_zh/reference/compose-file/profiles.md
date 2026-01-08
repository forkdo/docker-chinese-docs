---
linkTitle: 配置文件
title: 学习在 Docker Compose 中使用配置文件
description: 了解配置文件
keywords: compose, compose specification, profiles, compose file reference
aliases:
- /compose/compose-file/15-profiles/
weight: 120
---

通过配置文件，您可以定义一组活动的配置文件，以便针对各种用途和环境调整 Compose 应用程序模型。

[services](services.md) 顶级元素支持 `profiles` 属性，用于定义命名配置文件的列表。  
未设置 `profiles` 属性的服务始终处于启用状态。

当服务列出的 `profiles` 与活动配置文件不匹配时，Compose 将忽略该服务，除非该服务被命令显式指定。在这种情况下，其配置文件将被添加到活动配置文件的集合中。

> [!NOTE]
>
> 所有其他顶级元素不受 `profiles` 影响，始终处于活动状态。

对其他服务的引用（通过 `links`、`extends` 或共享资源语法 `service:xxx`）不会自动启用原本会被活动配置文件忽略的组件。相反，Compose 会返回错误。

## 示例说明

```yaml
services:
  web:
    image: web_image

  test_lib:
    image: test_lib_image
    profiles:
      - test

  coverage_lib:
    image: coverage_lib_image
    depends_on:
      - test_lib
    profiles:
      - test

  debug_lib:
    image: debug_lib_image
    depends_on:
      - test_lib
    profiles:
      - debug
```

在上述示例中：

- 如果未启用任何配置文件时解析 Compose 应用程序模型，则仅包含 `web` 服务。
- 如果启用了 `test` 配置文件，则模型包含 `test_lib` 和 `coverage_lib` 服务，以及始终启用的 `web` 服务。
- 如果启用了 `debug` 配置文件，则模型包含 `web` 和 `debug_lib` 服务，但不包含 `test_lib` 和 `coverage_lib`，因此该模型对于 `debug_lib` 的 `depends_on` 约束无效。
- 如果同时启用了 `debug` 和 `test` 配置文件，则模型包含所有服务：`web`、`test_lib`、`coverage_lib` 和 `debug_lib`。
- 如果 Compose 以 `test_lib` 作为显式运行的服务执行，则即使未启用 `test` 配置文件，`test_lib` 和 `test` 配置文件也会处于活动状态。
- 如果 Compose 以 `coverage_lib` 作为显式运行的服务执行，则服务 `coverage_lib` 和配置文件 `test` 处于活动状态，并且 `test_lib` 会通过 `depends_on` 约束被引入。
- 如果 Compose 以 `debug_lib` 作为显式运行的服务执行，则模型对于 `debug_lib` 的 `depends_on` 约束再次无效，因为 `debug_lib` 和 `test_lib` 没有共同的 `profiles` 列出。
- 如果 Compose 以 `debug_lib` 作为显式运行的服务执行，并且启用了 `test` 配置文件，则 `debug` 配置文件会自动启用，并且服务 `test_lib` 作为依赖项被引入，同时启动 `debug_lib` 和 `test_lib` 服务。

了解如何在 [Docker Compose](/manuals/compose/how-tos/profiles.md) 中使用 `profiles`。