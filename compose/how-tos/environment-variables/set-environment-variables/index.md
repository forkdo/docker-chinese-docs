# 在容器环境中设置环境变量

在服务配置中明确指定之前，容器的环境变量不会被设置。使用 Compose，您可以通过 Compose 文件以两种方式为容器设置环境变量。

>[!TIP]
>
> 请勿使用环境变量向容器传递敏感信息（如密码）。请改用 [secrets](../use-secrets.md)。

## 使用 `environment` 属性

您可以通过 `compose.yaml` 中的 [`environment` 属性](/reference/compose-file/services.md#environment) 直接在容器环境中设置环境变量。

它支持列表和映射两种语法：

```yaml
services:
  webapp:
    environment:
      DEBUG: "true"
```
等价于
```yaml
services:
  webapp:
    environment:
      - DEBUG=true
```

有关更多使用示例，请参阅 [`environment` 属性](/reference/compose-file/services.md#environment)。

### 附加信息

- 您可以选择不设置值，而是将环境变量从 shell 直接传递到容器中。其工作方式与 `docker run -e VARIABLE ...` 相同：
  ```yaml
  web:
    environment:
      - DEBUG
  ```
容器中的 `DEBUG` 变量值取自运行 Compose 的 shell 中同名变量的值。请注意，如果 shell 环境中未设置 `DEBUG` 变量，则不会发出警告。

- 您还可以利用 [插值](variable-interpolation.md#interpolation-syntax)。在以下示例中，结果与上面类似，但如果 `DEBUG` 变量未在 shell 环境或项目目录中的 `.env` 文件中设置，Compose 会发出警告。

  ```yaml
  web:
    environment:
      - DEBUG=${DEBUG}
  ```

## 使用 `env_file` 属性

还可以使用 [`.env` 文件](variable-interpolation.md#env-file) 和 [`env_file` 属性](/reference/compose-file/services.md#env_file) 来设置容器的环境变量。

```yaml
services:
  webapp:
    env_file: "webapp.env"
```

使用 `.env` 文件可让您使用相同的文件执行普通的 `docker run --env-file ...` 命令，或在多个服务之间共享同一个 `.env` 文件，而无需重复冗长的 `environment` YAML 块。

它还有助于将环境变量与主配置文件分开，提供更有序且安全的方式来管理敏感信息，因为您无需将 `.env` 文件放在项目目录的根目录中。

[`env_file` 属性](/reference/compose-file/services.md#env_file) 还允许您在 Compose 应用程序中使用多个 `.env` 文件。

在 `env_file` 属性中指定的 `.env` 文件路径是相对于 `compose.yaml` 文件的位置。

> [!IMPORTANT]
>
> `.env` 文件中的插值是 Docker Compose CLI 的一项功能。
>
> 运行 `docker run --env-file ...` 时不支持此功能。

### 附加信息

- 如果指定了多个文件，它们将按顺序求值，并且可以覆盖先前文件中设置的值。
- 从 Docker Compose 2.24.0 版本开始，您可以通过 `required` 字段将 `env_file` 属性定义的 `.env` 文件设置为可选。当 `required` 设置为 `false` 且 `.env` 文件缺失时，Compose 会静默忽略该条目。
  ```yaml
  env_file:
    - path: ./default.env
      required: true # 默认值
    - path: ./override.env
      required: false
  ```
- 从 Docker Compose 2.30.0 版本开始，您可以使用 `format` 属性为 `env_file` 使用替代文件格式。有关更多信息，请参阅 [`format`](/reference/compose-file/services.md#format)。
- 使用 [`docker compose run -e`](#set-environment-variables-with-docker-compose-run---env) 可以从命令行覆盖 `.env` 文件中的值。

## 使用 `docker compose run --env` 设置环境变量

与 `docker run --env` 类似，您可以使用 `docker compose run --env` 或其简写形式 `docker compose run -e` 临时设置环境变量：

```console
$ docker compose run -e DEBUG=1 web python console.py
```

### 附加信息

- 您也可以不赋值，从而从 shell 或环境文件中传递变量：

  ```console
  $ docker compose run -e DEBUG web python console.py
  ```

容器中的 `DEBUG` 变量值取自运行 Compose 的 shell 中同名变量的值，或来自环境文件。

## 更多资源

- [了解环境变量优先级](envvars-precedence.md)。
- [设置或更改预定义环境变量](envvars.md)
- [探索最佳实践](best-practices.md)
- [了解插值](variable-interpolation.md)
