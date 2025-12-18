---
linkTitle: Merge
title: 合并 Compose 文件
description: 了解 Docker Compose 如何合并多个文件并解决冲突
keywords: compose, compose specification, merge, compose file reference
aliases: 
 - /compose/compose-file/13-merge/
weight: 100
---

{{% include "compose/merge.md" %}}

这些规则在下面详细说明。

## 映射（Mapping）

YAML `mapping` 通过添加缺失的条目并合并冲突的条目来进行合并。

合并以下示例 YAML 树：

```yaml
services:
  foo:
    key1: value1
    key2: value2
```

```yaml
services:
  foo:
    key2: VALUE
    key3: value3
```

结果是一个等效于以下 YAML 树的 Compose 应用模型：

```yaml
services:
  foo:
    key1: value1
    key2: VALUE
    key3: value3
```

## 序列（Sequence）

YAML `sequence` 通过将覆盖 Compose 文件中的值追加到前一个文件中来合并。

合并以下示例 YAML 树：

```yaml
services:
  foo:
    DNS:
      - 1.1.1.1
```

```yaml
services:
  foo:
    DNS: 
      - 8.8.8.8
```

结果是一个等效于以下 YAML 树的 Compose 应用模型：

```yaml
services:
  foo:
    DNS:
      - 1.1.1.1
      - 8.8.8.8
```

## 例外情况

### Shell 命令

当合并使用服务属性 [command](services.md#command)、[entrypoint](services.md#entrypoint) 和 [healthcheck: `test`](services.md#healthcheck) 的 Compose 文件时，值会被最新的 Compose 文件覆盖，而不是追加。

合并以下示例 YAML 树：

```yaml
services:
  foo:
    command: ["echo", "foo"]
```

```yaml
services:
  foo:
    command: ["echo", "bar"]
```

结果是一个等效于以下 YAML 树的 Compose 应用模型：

```yaml
services:
  foo:
    command: ["echo", "bar"]
```

### 唯一资源

适用于服务属性 [ports](services.md#ports)、[volumes](services.md#volumes)、[secrets](services.md#secrets) 和 [configs](services.md#configs)。
虽然这些类型在 Compose 文件中被建模为序列，但它们有特殊的唯一性要求：

| 属性   | 唯一键               |
|-------------|--------------------------|
| volumes     |  target                  |
| secrets     |  target                  |
| configs     |  target                  |
| ports       |  {ip, target, published, protocol}   |

合并 Compose 文件时，Compose 会追加不违反唯一性约束的新条目，并合并共享唯一键的条目。

合并以下示例 YAML 树：

```yaml
services:
  foo:
    volumes:
      - foo:/work
```

```yaml
services:
  foo:
    volumes:
      - bar:/work
```

结果是一个等效于以下 YAML 树的 Compose 应用模型：

```yaml
services:
  foo:
    volumes:
      - bar:/work
```

### 重置值

除了前面描述的机制外，覆盖 Compose 文件还可以用于从应用模型中删除元素。为此目的，可以将自定义 [YAML 标签](https://yaml.org/spec/1.2.2/#24-tags) `!reset` 设置为覆盖被覆盖 Compose 文件的值。必须提供属性的有效值，但该值将被忽略，目标属性将被设置为类型的默认值或 `null`。

为了可读性，建议显式将属性值设置为空值（`null`）或空数组 `[]`（使用 `!reset null` 或 `!reset []`），以便清楚地表明结果属性将被清除。

一个基础的 `compose.yaml` 文件：

```yaml
services:
  app:
    image: myapp
    ports:
      - "8080:80" 
    environment:
      FOO: BAR           
```

和一个 `compose.override.yaml` 文件：

```yaml
services:
  app:
    image: myapp
    ports: !reset []
    environment:
      FOO: !reset null
```

结果是：

```yaml
services:
  app:
    image: myapp
```

### 替换值

{{< summary-bar feature_name="Compose 替换文件" >}}

虽然 `!reset` 可以用于使用覆盖文件从 Compose 文件中删除声明，但 `!override` 允许你完全替换属性，绕过标准合并规则。一个典型的例子是完全替换资源定义，依赖于不同的模型但使用相同的名称。

一个基础的 `compose.yaml` 文件：

```yaml
services:
  app:
    image: myapp
    ports:
      - "8080:80"
```

要删除原始端口但暴露一个新端口，使用以下覆盖文件：

```yaml
services:
  app:
    ports: !override
      - "8443:443" 
```

这导致：

```yaml
services:
  app:
    image: myapp
    ports:
      - "8443:443" 
```

如果未使用 `!override`，则根据上面[概述的合并规则](#sequence)，`8080:80` 和 `8443:443` 都将被暴露。

## 额外资源

有关如何使用合并创建复合 Compose 文件的更多信息，请参阅 [使用多个 Compose 文件](/manuals/compose/how-tos/multiple-compose-files/_index.md)