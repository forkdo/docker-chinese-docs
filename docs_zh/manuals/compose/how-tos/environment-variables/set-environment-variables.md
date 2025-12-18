---
title: 在容器环境中设置环境变量
linkTitle: 设置环境变量
weight: 10
description: 如何使用 Compose 设置、使用和管理环境变量
keywords: compose, 编排, 环境, 环境变量, 容器环境变量
aliases:
- /compose/env/
- /compose/link-env-deprecated/
- /compose/environment-variables/set-environment-variables/
---

容器的环境变量只有在服务配置中显式声明时才会被设置。使用 Compose，您可以通过 `compose.yaml` 文件以两种方式在容器中设置环境变量。

它同时支持列表和映射语法：

```yaml
services:
  webapp:
    environment:
      DEBUG: "true"
```
等同于
```yaml
services:
  webapp:
    environment:
      - DEBUG=true
```

更多使用示例，请参阅 [`environment` 属性](/reference/compose-file/services.md#environment)。

### 附加信息

- 您可以选择不设置值，而是将环境变量直接从您的 shell 传递到容器中。其工作方式与 `docker run -e VARIABLE ...` 相同：
  ```yaml
  web:
    environment:
      - DEBUG
  ```
容器中的 `DEBUG` 变量值取自运行 Compose 的 shell 中的同名变量值。注意，如果 shell 环境中未设置 `DEBUG` 变量，此处不会发出警告。

- 您还可以利用 [插值](variable-interpolation.md#interpolation-syntax) 功能。在以下示例中，结果与上面类似，但如果 `DEBUG` 变量未在 shell 环境或项目目录中的 `.env` 文件中设置，Compose 会给出警告。

  ```yaml
  web:
    environment:
      - DEBUG=${DEBUG}
  ```

## 使用 `env_file` 属性

容器的环境变量也可以通过 [`.env` 文件](variable-interpolation.md#env-file) 和 [`env_file` 属性](/reference/compose-file/services.md#env_file) 来设置。

```yaml
services:
  webapp:
    env_file: "webapp.env"
```

使用 `.env` 文件可以让您使用相同的文件供普通的 `docker run --env-file ...` 命令使用，或者在多个服务之间共享同一个 `.env` 文件，而无需复制冗长的 `environment` YAML 块。

它还可以帮助您将环境变量与主要配置文件分开，提供更有序和安全的方式来管理敏感信息，因为您不需要将 `.env` 文件放在项目目录的根目录中。

[`env_file` 属性](/reference/compose-file/services.md#env_file) 还允许您在 Compose 应用中使用多个 `.env` 文件。

在 `env_file` 属性中指定的 `.env` 文件路径相对于您的 `compose.yaml` 文件位置。

> [!IMPORTANT]
>
> `.env` 文件中的插值是 Docker Compose CLI 功能。
>
> 在运行 `docker run --env-file ...` 时不受支持。

### 附加信息

- 如果指定了多个文件，它们将按顺序求值，后面的文件可以覆盖前面文件中设置的值。
- 从 Docker Compose 2.24.0 版本开始，您可以通过 `required` 字段将 `env_file` 属性定义的 `.env` 文件设置为可选。当 `required` 设置为 `false` 且 `.env` 文件缺失时，Compose 会静默忽略该条目。
  ```yaml
  env_file:
    - path: ./default.env
      required: true # 默认值
    - path: ./override.env
      required: false
  ``` 
- 从 Docker Compose 2.30.0 版本开始，您可以使用 `format` 属性为 `env_file` 使用替代的文件格式。更多信息请参阅 [`format`](/reference/compose-file/services.md#format)。
- `.env` 文件中的值可以通过命令行使用 [`docker compose run -e`](#set-environment-variables-with-docker-compose-run---env) 覆盖。

## 使用 `docker compose run --env` 设置环境变量

类似于 `docker run --env`，您可以使用 `docker compose run --env` 或其简写形式 `docker compose run -e` 临时设置环境变量：

```console
$ docker compose run -e DEBUG=1 web python console.py
```

### 附加信息

- 您也可以通过不给变量赋值的方式从 shell 或环境文件传递变量：

  ```console
  $ docker compose run -e DEBUG web python console.py
  ```

容器中的 `DEBUG` 变量值取自运行 Compose 的 shell 中的同名变量值或环境文件中的值。

## 进一步资源

- [了解环境变量优先级](envvars-precedence.md)
- [设置或更改预定义环境变量](envvars.md)
- [探索最佳实践](best-practices.md)
- [理解插值](variable-interpolation.md)