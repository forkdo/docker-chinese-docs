---
description: 了解如何使用 Docker Compose 的 extends 属性在文件和项目之间复用服务配置。
keywords: fig, composition, compose, docker, orchestration, documentation, docs, compose file modularization
title: 扩展你的 Compose 文件
linkTitle: 扩展
weight: 20
aliases:
- /compose/extends/
- /compose/multiple-compose-files/extends/
---

Docker Compose 的 [`extends` 属性](/reference/compose-file/services.md#extends)
让你可以在不同文件之间，甚至完全不同的项目之间共享通用配置。

如果多个服务需要复用一组通用的配置选项，那么扩展服务就非常有用。使用 `extends`，你可以将一组通用的服务选项定义在一个地方，然后在任何地方引用它。你可以引用另一个 Compose 文件，并选择你想要在自己应用中使用的服务，同时能够覆盖某些属性以满足自己的需求。

> [!IMPORTANT]
>
> 当你使用多个 Compose 文件时，必须确保所有文件中的路径都相对于基础 Compose 文件（即主项目文件夹中的 Compose 文件）。这是必需的，因为扩展文件不需要是有效的 Compose 文件。扩展文件可以只包含配置的小片段。跟踪服务的哪个片段相对于哪个路径是很困难且令人困惑的，因此为了保持路径更容易理解，所有路径都必须相对于基础文件定义。

## `extends` 属性的工作原理

### 从另一个文件扩展服务

以以下示例为例：

```yaml
services:
  web:
    extends:
      file: common-services.yml
      service: webapp
```

这指示 Compose 重用 `common-services.yml` 文件中定义的 `webapp` 服务的属性。`webapp` 服务本身不是最终项目的一部分。

如果 `common-services.yml`
如下所示：

```yaml
services:
  webapp:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - "/data"
```
你得到的结果与在 `compose.yaml` 中直接在 `web` 下定义相同的 `build`、`ports` 和 `volumes` 配置值完全相同。

要在从另一个文件扩展服务时将服务 `webapp` 包含在最终项目中，你需要在当前 Compose 文件中显式包含这两个服务。例如（仅用于说明）：

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

### 在同一文件内扩展服务

如果你在同一 Compose 文件中定义服务并从另一个服务扩展，那么原始服务和扩展的服务都将成为你最终配置的一部分。例如：

```yaml 
services:
  web:
    build: alpine
    extends: webapp
  webapp:
    environment:
      - DEBUG=1
```

### 在同一文件内和从另一个文件扩展服务

你可以进一步在 `compose.yaml` 中定义或重新定义配置：

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

## 另一个示例

扩展单个服务在你有多个服务共享许多配置选项时很有用。下面的示例是一个 Compose 应用，包含两个服务：一个 Web 应用和一个队列工作器。两个服务使用相同的代码库并共享许多配置选项。

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

当使用 `extends` 和指向另一个文件夹的 `file` 属性时，被扩展服务声明的相对路径会被转换，以便扩展服务使用时仍然指向同一个文件。以下示例说明了这一点：

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

结果服务引用了 `commons` 目录中原始的 `container.env` 文件。这可以通过 `docker compose config` 检查实际模型来确认：
```yaml
services:
  webapp:
    image: example
    env_file: 
      - ../commons/container.env
```

## 参考信息

- [`extends`](/reference/compose-file/services.md#extends)