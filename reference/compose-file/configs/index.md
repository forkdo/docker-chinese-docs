# Configs 顶级元素



配置使服务能够调整其行为，而无需重新构建 Docker 镜像。与卷类似，配置会以文件形式挂载到容器的文件系统中。在 Linux 容器中，挂载点在容器内的默认位置为 `/<config-name>`；在 Windows 容器中，则为 `C:\<config-name>`。

只有当服务被 `services` 顶级元素中的 [`configs`](services.md#configs) 属性显式授权时，才能访问 configs。

默认情况下，config：
- 归运行容器命令的用户所有，但可以通过服务配置覆盖。
- 具有全局可读权限（模式 0444），除非服务配置覆盖了此设置。

顶级 `configs` 声明定义或引用授予 Compose 应用中服务的配置数据。config 的来源可以是 `file`、`environment`、`content` 或 `external`。

- `file`：使用指定路径下的文件内容创建 config。
- `environment`：使用环境变量的值创建 config 内容。引入于 Docker Compose 版本 [2.23.1](https://github.com/docker/compose/releases/tag/v2.23.1)。
- `content`：使用内联值创建内容。引入于 Docker Compose 版本 [2.23.1](https://github.com/docker/compose/releases/tag/v2.23.1)。
- `external`：如果设置为 true，`external` 指定此 config 已经创建。Compose 不会
  尝试创建它，如果它不存在，则会发生错误。
- `name`：要在容器引擎中查找的 config 对象的名称。此字段可用于
  引用包含特殊字符的 configs。该名称按原样使用，
  并且**不会**使用项目名称作为作用域前缀。

## 示例 1

部署应用程序时会创建 `<project_name>_http_config`，
方法是将 `httpd.conf` 的内容注册为配置数据。

```yml
configs:
  http_config:
    file: ./httpd.conf
```

或者，可以将 `http_config` 声明为 external。Compose 查找 `http_config` 以将配置数据公开给相关服务。

```yml
configs:
  http_config:
    external: true
```

## 示例 2

外部 config 查找也可以通过指定 `name` 来使用不同的键。

以下
示例修改了前一个示例，以使用参数 `HTTP_CONFIG_KEY` 查找 config。实际的查找键在部署时通过变量的 [interpolation](interpolation.md) 设置，
但以硬编码 ID `http_config` 的形式公开给容器。

```yml
configs:
  http_config:
    external: true
    name: "${HTTP_CONFIG_KEY}"
```

## 示例 3

部署应用程序时会创建 `<project_name>_app_config`，
方法是将内联内容注册为配置数据。这意味着 Compose 在创建 config 时会推断变量，允许您
根据服务配置调整内容：

```yml
configs:
  app_config:
    content: |
      debug=${DEBUG}
      spring.application.admin.enabled=${DEBUG}
      spring.application.name=${COMPOSE_PROJECT_NAME}
```

## 示例 4

部署应用程序时会创建 `<project_name>_simple_config`，
使用环境变量的值作为配置数据。这对于不需要插值的简单配置值很有用：

```yml
configs:
  simple_config:
    environment: "SIMPLE_CONFIG_VALUE"
```

如果 `external` 设置为 `true`，则除 `name` 之外的所有其他属性均无关紧要。如果 Compose 检测到任何其他属性，它将拒绝该 Compose 文件，视为无效。
