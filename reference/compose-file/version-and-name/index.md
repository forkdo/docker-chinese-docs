# 版本和名称顶级元素

## 版本顶级元素（已弃用）

> [!IMPORTANT]
>
> 顶级 `version` 属性由 Compose 规范定义，用于向后兼容。该属性仅用于提供信息，如果使用，你将收到一条关于其已弃用的警告消息。

无论 `version` 字段如何设置，Compose 始终使用最新的 schema 来验证 Compose 文件。

Compose 会验证它是否可以完全解析 Compose 文件。如果某些字段未知，通常是因为 Compose 文件是由较新版本的规范中定义的字段编写的，你将会收到一条警告消息。

## 名称顶级元素

顶级 `name` 属性由 Compose 规范定义，用作在你未显式设置项目名称时使用的项目名称。

Compose 提供了一种让你覆盖此名称的方法，并在未设置顶级 `name` 元素时设置一个默认的项目名称。

无论项目名称是由顶级 `name` 还是某些自定义机制定义的，它都会以 `COMPOSE_PROJECT_NAME` 的形式暴露出来，用于
[插值](interpolation.md) 和环境变量解析。

```yml
name: myapp

services:
  foo:
    image: busybox
    command: echo "I'm running ${COMPOSE_PROJECT_NAME}"
```

有关命名 Compose 项目的其他方式的更多信息，请参阅 [指定项目名称](/manuals/compose/how-tos/project-name.md)。
