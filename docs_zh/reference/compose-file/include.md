---
linkTitle: Include
title: 使用 include 模块化 Compose 文件
description: 使用 include 顶级元素引用外部 Compose 文件
keywords: compose, compose specification, include, compose file reference
aliases:
 - /compose/compose-file/14-include/
weight: 110
---

{{< summary-bar feature_name="Composefile include" >}}

你可以通过包含其他 Compose 文件来复用和模块化 Docker Compose 配置。这在以下场景中很有用：
- 你想复用其他 Compose 文件。
- 你需要将应用模型的某些部分提取到单独的 Compose 文件中，以便可以独立管理或与他人共享。
- 团队需要维护一个 Compose 文件，只包含其在较大部署中有限子域所需的资源声明。

`include` 顶级部分用于定义对另一个 Compose 应用或子域的依赖。
`include` 部分中列出的每个路径都被加载为一个独立的 Compose 应用模型，具有自己的项目目录，以解析相对路径。

一旦包含的 Compose 应用被加载，所有资源定义都会被复制到当前 Compose 应用模型中。
如果资源名称冲突，Compose 会显示警告，但不会尝试合并它们。为了强制执行这一点，`include` 在选中的 Compose 文件被解析和合并之后才进行评估，这样可以检测到 Compose 文件之间的冲突。

`include` 支持递归，因此包含自己 `include` 部分的 Compose 文件会触发其他文件也被包含进来。

从包含的 Compose 文件中拉入的任何卷、网络或其他资源都可以被当前 Compose 应用用于跨服务引用。例如：

```yaml
include:
  - my-compose-include.yaml  # 声明了 serviceB
services:
  serviceA:
    build: .
    depends_on:
      - serviceB # 直接使用 serviceB，就像在当前 Compose 文件中声明一样
```

Compose 还支持在 `include` 中使用插值变量。建议你[指定必需变量](interpolation.md)。例如：

```text
include:
  -${INCLUDE_PATH:?FOO}/compose.yaml
```

## 短语法

短语法仅定义指向其他 Compose 文件的路径。文件以其父文件夹作为项目目录加载，并可选地加载 `.env` 文件以定义插值变量的默认值。
本地项目的环境可以覆盖这些值。

```yaml
include:
  - ../commons/compose.yaml
  - ../another_domain/compose.yaml

services:
  webapp:
    depends_on:
      - included-service # 由 another_domain 定义
```

在前面的例子中，`../commons/compose.yaml` 和 `../another_domain/compose.yaml` 都被作为独立的 Compose 项目加载。
`include` 引用的 Compose 文件中的相对路径根据其自身 Compose 文件的路径解析，而不是基于本地项目的目录。
变量使用同一文件夹中的可选 `.env` 文件中的值进行插值，并被本地项目的环境覆盖。

## 长语法

长语法对子项目解析提供了更多控制：

```yaml
include:
   - path: ../commons/compose.yaml
     project_directory: ..
     env_file: ../another/.env
```

### `path`

`path` 是必需的，定义了要解析并包含到本地 Compose 模型中的 Compose 文件的位置。

`path` 可以设置为：

- 字符串：使用单个 Compose 文件时。
- 字符串列表：当多个 Compose 文件需要[合并在一起](merge.md)以定义本地应用的 Compose 模型时。

```yaml
include:
   - path:
       - ../commons/compose.yaml
       - ./commons-override.yaml
```

### `project_directory`

`project_directory` 定义了用于解析 Compose 文件中设置的相对路径的基础路径。默认为包含的 Compose 文件的目录。

### `env_file`

`env_file` 定义了在解析 Compose 文件时用于插值变量默认值的环境文件。默认为 Compose 文件所在 `project_directory` 中的 `.env` 文件。

`env_file` 可以设置为字符串或字符串列表（当需要合并多个环境文件以定义项目环境时）。

```yaml
include:
   - path: ../another/compose.yaml
     env_file:
       - ../another/.env
       - ../another/dev.env
```

本地项目的环境优先于 Compose 文件中设置的值，因此本地项目可以覆盖这些值以进行自定义。

## 附加资源

有关使用 `include` 的更多信息，请参阅 [使用多个 Compose 文件](/manuals/compose/how-tos/multiple-compose-files/_index.md)