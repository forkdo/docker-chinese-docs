# 扩展你的 Compose 文件

Docker Compose 的 [`extends` 属性](/reference/compose-file/services.md#extends)
允许你在不同文件之间，甚至完全不同的项目之间共享通用配置。

当你有多个服务需要重用一组通用配置选项时，扩展服务非常有用。使用 `extends` 你可以将一组通用服务选项定义在一个地方，并从任何地方引用它。你可以引用另一个 Compose 文件，并选择你想要在你的应用程序中也使用的服务，同时可以根据需要覆盖一些属性。

> [!IMPORTANT]
>
> 当你使用多个 Compose 文件时，必须确保所有文件中的路径都是相对于基础 Compose 文件（即主项目文件夹中的 Compose 文件）的。这是必需的，因为扩展文件不一定是有效的 Compose 文件。扩展文件可以只包含一小部分配置。追踪服务的哪个片段相对于哪个路径是困难且令人困惑的，因此为了保持路径更容易理解，所有路径都必须相对于基础文件定义。

## `extends` 属性如何工作

### 从另一个文件扩展服务

参考以下示例：

```yaml
services:
  web:
    extends:
      file: common-services.yml
      service: webapp
```

这指示 Compose 仅重用 `common-services.yml` 文件中定义的 `webapp` 服务的属性。`webapp` 服务本身不是最终项目的一部分。

如果 `common-services.yml` 看起来像这样：

```yaml
services:
  webapp:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - "/data"
```
你会得到与在 `compose.yaml` 中直接定义 `web` 服务相同的 `build`、`ports` 和 `volumes` 配置值完全相同的结果。

要从另一个文件扩展服务并在最终项目中包含 `webapp` 服务，你需要在当前 Compose 文件中显式包含这两个服务。例如（仅用于说明）：

```yaml
services:
  web:
    build: alpine
    command: echo
    extends:
      file: common-services.yml
      service: webapp
  webapp:
    extends:
      file: common-services.yml
      service: webapp
```

或者，你可以使用 [include](include.md)。

### 在同一文件中扩展服务

如果你在同一个 Compose 文件中定义服务并从一个服务扩展到另一个服务，原始服务和扩展服务都将成为你的最终配置的一部分。例如：

```yaml 
services:
  web:
    build: alpine
    extends: webapp
  webapp:
    environment:
      - DEBUG=1
```

### 在同一文件中扩展服务并从另一个文件扩展

你可以在 `compose.yaml` 中进一步定义或重新定义本地配置：

```yaml
services:
  web:
    extends:
      file: common-services.yml
      service: webapp
    environment:
      - DEBUG=1
    cpu_shares: 5

  important_web:
    extends: web
    cpu_shares: 10
```

## 附加示例

当你有多个具有通用配置的服务时，扩展单个服务非常有用。以下示例是一个包含两个服务的 Compose 应用，一个 Web 应用和一个队列工作器。这两个服务使用相同的代码库并共享许多配置选项。

`common.yaml` 文件定义了通用配置：

```yaml
services:
  app:
    build: .
    environment:
      CONFIG_FILE_PATH: /code/config
      API_KEY: xxxyyy
    cpu_shares: 5
```

`compose.yaml` 定义了使用通用配置的具体服务：

```yaml
services:
  webapp:
    extends:
      file: common.yaml
      service: app
    command: /code/run_web_app
    ports:
      - 8080:8080
    depends_on:
      - queue
      - db

  queue_worker:
    extends:
      file: common.yaml
      service: app
    command: /code/run_worker
    depends_on:
      - queue
```

## 相对路径

当使用 `extends` 并指定指向另一个文件夹的 `file` 属性时，被扩展服务声明的相对路径会被转换，以便在扩展服务使用时仍然指向相同的文件。以下示例说明了这一点：

基础 Compose 文件：
```yaml
services:
  webapp:
    image: example
    extends:
      file: ../commons/compose.yaml
      service: base
```

`commons/compose.yaml` 文件：
```yaml
services:
  base:
    env_file: ./container.env
```

最终的服务会引用 `commons` 目录中的原始 `container.env` 文件。这可以通过 `docker compose config` 命令确认，该命令会检查实际模型：
```yaml
services:
  webapp:
    image: example
    env_file: 
      - ../commons/container.env
```

## 参考信息

- [`extends`](/reference/compose-file/services.md#extends)
