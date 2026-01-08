---
title: 片段
description: 使用 YAML 锚点和片段复用配置
keywords: compose, compose specification, fragments, compose file reference
aliases:
- /compose/compose-file/10-fragments/
weight: 70
---

{{% include "compose/fragments.md" %}}

锚点使用 `&` 符号创建。该符号后跟一个别名。之后您可以使用 `*` 符号与该别名来引用锚点后的值。请确保 `&` 和 `*` 字符与后面的别名之间没有空格。

您可以在单个 Compose 文件中使用多个锚点和别名。

## 示例 1

```yml
volumes:
  db-data: &default-volume
    driver: default
  metrics: *default-volume
```

在上面的示例中，基于 `db-data` 卷创建了一个 `default-volume` 锚点。随后通过别名 `*default-volume` 复用它来定义 `metrics` 卷。

锚点解析发生在[变量插值](interpolation.md)之前，因此不能使用变量来设置锚点或别名。

## 示例 2

```yml
services:
  first:
    image: my-image:latest
    environment: &env
      - CONFIG_KEY
      - EXAMPLE_KEY
      - DEMO_VAR
  second:
    image: another-image:latest
    environment: *env
```

如果您有一个锚点希望在多个服务中使用，请结合[扩展](extension.md)使用，以使您的 Compose 文件更易于维护。

## 示例 3

您可能希望部分覆盖值。Compose 遵循 [YAML 合并类型](https://yaml.org/type/merge.html) 所概述的规则。

在以下示例中，`metrics` 卷规范使用别名避免重复，但覆盖了 `name` 属性：

```yml
services:
  backend:
    image: example/database
    volumes:
      - db-data
      - metrics
volumes:
  db-data: &default-volume
    driver: default
    name: "data"
  metrics:
    <<: *default-volume
    name: "metrics"
```

## 示例 4

您还可以扩展锚点以添加其他值。

```yml
services:
  first:
    image: my-image:latest
    environment: &env
      FOO: BAR
      ZOT: QUIX
  second:
    image: another-image:latest
    environment:
      <<: *env
      YET_ANOTHER: VARIABLE
```

> [!NOTE]
>
> [YAML 合并](https://yaml.org/type/merge.html) 仅适用于映射，不能用于序列。

在上面的示例中，环境变量必须使用 `FOO: BAR` 映射语法声明，而序列语法 `- FOO=BAR` 仅在未涉及片段时有效。