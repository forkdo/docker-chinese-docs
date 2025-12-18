---
linkTitle: Profiles
title: 了解如何在 Docker Compose 中使用 profiles
description: 了解 profiles 的使用方法
keywords: compose, compose specification, profiles, compose file reference
aliases: 
 - /compose/compose-file/15-profiles/
weight: 120
---

通过 profiles，您可以定义一组活跃的 profiles，以便您的 Compose 应用模型能够适应不同的使用场景和环境。

[services](services.md) 顶级元素支持 `profiles` 属性，用于定义命名 profiles 的列表。
没有 `profiles` 属性的服务始终启用。

当所列出的 `profiles` 与活跃 profiles 不匹配时，Compose 会忽略该服务，除非该服务被命令显式指定。在这种情况下，其 profile 会被添加到活跃 profiles 集合中。

> [!NOTE]
>
> 所有其他顶级元素不受 `profiles` 影响，始终处于活跃状态。

对其他服务的引用（通过 `links`、`extends` 或共享资源语法 `service:xxx`）不会自动启用一个因活跃 profiles 而被忽略的组件。相反，Compose 会返回错误。

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

在上面的例子中：

- 如果在未启用任何 profile 的情况下解析 Compose 应用模型，它只包含 `web` 服务。
- 如果启用了 profile `test`，模型包含服务 `test_lib` 和 `coverage_lib`，以及始终启用的 `web` 服务。
- 如果启用了 profile `debug`，模型包含 `web` 和 `debug_lib` 服务，但不包含 `test_lib` 和 `coverage_lib`，因此模型对于 `debug_lib` 的 `depends_on` 约束是无效的。
- 如果同时启用了 `debug` 和 `test` profiles，模型包含所有服务：`web`、`test_lib`、`coverage_lib` 和 `debug_lib`。
- 如果 Compose 以 `test_lib` 作为显式服务运行，即使未启用 `test` profile，`test_lib` 和 `test` profile 也会处于活跃状态。
- 如果 Compose 以 `coverage_lib` 作为显式服务运行，服务 `coverage_lib` 和 profile `test` 处于活跃状态，且 `test_lib` 通过 `depends_on` 约束被拉入。
- 如果 Compose 以 `debug_lib` 作为显式服务运行，由于 `debug_lib` 和 `test_lib` 没有共同列出的 `profiles`，模型对于 `debug_lib` 的 `depends_on` 约束是无效的。
- 如果 Compose 以 `debug_lib` 作为显式服务运行且启用了 profile `test`，profile `debug` 会自动启用，服务 `test_lib` 作为依赖被拉入，同时启动 `debug_lib` 和 `test_lib` 服务。

了解如何在 [Docker Compose](/manuals/compose/how-tos/profiles.md) 中使用 `profiles`。