---
linkTitle: Configs 
title: Configs 顶级元素
description: 使用 Docker Compose 中的 configs 元素来管理和共享配置数据。
keywords: compose, compose specification, configs, compose file reference
aliases: 
 - /compose/compose-file/08-configs/
weight: 50
---

{{% include "compose/configs.md" %}}

服务只有在 `services` 顶级元素中通过 [`configs`](services.md#configs) 属性显式授予时，才能访问配置项。

默认情况下，配置项：
- 由运行容器命令的用户拥有，但可以通过服务配置覆盖。
- 具有全局可读权限（mode 0444），除非服务配置覆盖了此设置。

顶级 `configs` 声明定义或引用了 Compose 应用程序中服务可访问的配置数据。配置项的来源可以是 `file`、`environment`、`content` 或 `external`。

- `file`：使用指定路径文件的内容创建配置项。
- `environment`：使用环境变量的值创建配置项内容。在 Docker Compose 版本 [2.23.1](/manuals/compose/releases/release-notes.md#2231) 中引入。
- `content`：使用内联值创建内容。在 Docker Compose 版本 [2.23.1](/manuals/compose/releases/release-notes.md#2231) 中引入。
- `external`：如果设置为 true，`external` 指定此配置项已预先创建。Compose 不会尝试创建它，如果它不存在，将发生错误。

`name`：容器引擎中配置项对象的名称。此字段可用于引用包含特殊字符的配置项。名称将按原样使用，**不会** 使用项目名称作为作用域。

## 示例 1

部署应用程序时，通过注册 `httpd.conf` 的内容作为配置数据来创建 `<project_name>_http_config`。

```yml
configs:
  http_config:
    file: ./httpd.conf
```

或者，`http_config` 可以声明为 external。Compose 查找 `http_config` 以向相关服务公开配置数据。

```yml
configs:
  http_config:
    external: true
```

## 示例 2

外部配置项查找也可以通过指定 `name` 使用不同的键。

以下示例修改了前面的示例，使用参数 `HTTP_CONFIG_KEY` 查找配置项。实际查找键在部署时通过 [变量插值](interpolation.md) 设置，但对容器暴露为硬编码 ID `http_config`。

```yml
configs:
  http_config:
    external: true
    name: "${HTTP_CONFIG_KEY}"
```

## 示例 3

部署应用程序时，通过注册内联内容作为配置数据来创建 `<project_name>_app_config`。这意味着 Compose 在创建配置项时推断变量，这允许您根据服务配置调整内容：

```yml
configs:
  app_config:
    content: |
      debug=${DEBUG}
      spring.application.admin.enabled=${DEBUG}
      spring.application.name=${COMPOSE_PROJECT_NAME}
```

## 示例 4

部署应用程序时，使用环境变量的值作为配置数据创建 `<project_name>_simple_config`。这对于不需要插值的简单配置值很有用：

```yml
configs:
  simple_config:
    environment: "SIMPLE_CONFIG_VALUE"
```

如果 `external` 设置为 `true`，除了 `name` 之外的所有其他属性都是无关紧要的。如果 Compose 检测到任何其他属性，它将拒绝该 Compose 文件作为无效文件。