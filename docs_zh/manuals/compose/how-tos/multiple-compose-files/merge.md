---
description: Compose 文件合并的工作原理
keywords: compose, docker, merge, compose file
title: 合并 Compose 文件
linkTitle: 合并
weight: 10
aliases:
- /compose/multiple-compose-files/merge/
---

Docker Compose 允许你将一组 Compose 文件合并在一起，创建一个复合的 Compose 文件。

默认情况下，Compose 会读取两个文件：`compose.yaml` 和一个可选的 `compose.override.yaml` 文件。按照约定，`compose.yaml` 包含你的基础配置，而覆盖文件可以包含对现有服务的配置覆盖，或全新的服务。

如果一个服务在两个文件中都有定义，Compose 会根据下面描述的规则以及 [Compose 规范](/reference/compose-file/merge.md) 中的规则来合并配置。

## 如何合并多个 Compose 文件

要使用多个覆盖文件，或使用不同名称的覆盖文件，你可以使用预定义的 [COMPOSE_FILE](../environment-variables/envvars.md#compose_file) 环境变量，或使用 `-f` 选项指定文件列表。

Compose 按照命令行中指定的顺序合并文件。后续文件可以合并、覆盖或添加到前一个文件中。

例如：

```console
$ docker compose -f compose.yaml -f compose.admin.yaml run backup_db
```

`compose.yaml` 文件可能指定了一个 `webapp` 服务。

```yaml
webapp:
  image: examples/web
  ports:
    - "8000:8000"
  volumes:
    - "/data"
```

`compose.admin.yaml` 也可能指定了相同的 `webapp` 服务：

```yaml
webapp:
  environment:
    - DEBUG=1
```

任何匹配的字段都会覆盖前一个文件，新值会添加到 `webapp` 服务的配置中：

```yaml
webapp:
  image: examples/web
  ports:
    - "8000:8000"
  volumes:
    - "/data"
  environment:
    - DEBUG=1
```

## 合并规则

- 路径相对于基础文件进行评估。当你使用多个 Compose 文件时，必须确保所有文件中的路径都相对于基础 Compose 文件（使用 `-f` 指定的第一个 Compose 文件）。这是必需的，因为覆盖文件不需要是有效的 Compose 文件。覆盖文件可以只包含配置的小片段。跟踪服务的哪个片段相对于哪个路径是很困难且令人困惑的，因此为了使路径更容易理解，所有路径都必须相对于基础文件定义。

   >[!TIP]
   >
   > 你可以使用 `docker compose config` 来查看合并后的配置，避免路径相关的问题。

- Compose 将原始服务的配置复制到本地服务中。如果某个配置选项在原始服务和本地服务中都有定义，本地值会替换或扩展原始值。

   - 对于 `image`、`command` 或 `mem_limit` 等单值选项，新值会替换旧值。

      原始服务：

      ```yaml
      services:
        myservice:
          # ...
          command: python app.py
      ```

      本地服务：

      ```yaml
      services:
        myservice:
          # ...
          command: python otherapp.py
      ```

      结果：

      ```yaml
      services:
        myservice:
          # ...
          command: python otherapp.py
      ```

   - 对于 `ports`、`expose`、`external_links`、`dns`、`dns_search` 和 `tmpfs` 等多值选项，Compose 会连接两组值：

      原始服务：

      ```yaml
      services:
        myservice:
          # ...
          expose:
            - "3000"
      ```

      本地服务：

      ```yaml
      services:
        myservice:
          # ...
          expose:
            - "4000"
            - "5000"
      ```

      结果：

      ```yaml
      services:
        myservice:
          # ...
          expose:
            - "3000"
            - "4000"
            - "5000"
      ```

   - 对于 `environment`、`labels`、`volumes` 和 `devices`，Compose 会“合并”条目，本地定义的值优先。对于 `environment` 和 `labels`，环境变量或标签名称决定使用哪个值：

      原始服务：

      ```yaml
      services:
        myservice:
          # ...
          environment:
            - FOO=original
            - BAR=original
      ```

      本地服务：

      ```yaml
      services:
        myservice:
          # ...
          environment:
            - BAR=local
            - BAZ=local
      ```

      结果：

      ```yaml
      services:
        myservice:
          # ...
          environment:
            - FOO=original
            - BAR=local
            - BAZ=local
      ```

   - `volumes` 和 `devices` 的条目使用容器中的挂载路径进行合并：

      原始服务：

      ```yaml
      services:
        myservice:
          # ...
          volumes:
            - ./original:/foo
            - ./original:/bar
      ```

      本地服务：

      ```yaml
      services:
        myservice:
          # ...
          volumes:
            - ./local:/bar
            - ./local:/baz
      ```

      结果：

      ```yaml
      services:
        myservice:
          # ...
          volumes:
            - ./original:/foo
            - ./local:/bar
            - ./local:/baz
      ```

有关更多合并规则，请参阅 Compose 规范中的 [合并和覆盖](/reference/compose-file/merge.md)。

### 附加信息

- 使用 `-f` 是可选的。如果不提供，Compose 会在工作目录及其父目录中搜索 `compose.yaml` 和 `compose.override.yaml` 文件。你必须至少提供 `compose.yaml` 文件。如果两个文件在同一目录级别存在，Compose 会将它们合并为单一配置。

- 你可以使用 `-f` 与 `-`（破折号）作为文件名，从 `stdin` 读取配置。例如：

   ```console
   $ docker compose -f - <<EOF
     webapp:
       image: examples/web
       ports:
        - "8000:8000"
       volumes:
        - "/data"
       environment:
        - DEBUG=1
     EOF
   ```

   当使用 `stdin` 时，配置中的所有路径都相对于当前工作目录。

- 你可以使用 `-f` 标志指定一个不在当前目录中的 Compose 文件路径，可以通过命令行指定，也可以通过在 shell 或环境文件中设置 [COMPOSE_FILE 环境变量](../environment-variables/envvars.md#compose_file) 来实现。

   例如，如果你正在运行 [Compose Rails 示例](https://github.com/docker/awesome-compose/tree/master/official-documentation-samples/rails/README.md)，并且在名为 `sandbox/rails` 的目录中有 `compose.yaml` 文件。你可以使用类似 [docker compose pull](/reference/cli/docker/compose/pull.md) 的命令，通过使用 `-f` 标志从任何位置获取 `db` 服务的 postgres 镜像，如下所示：`docker compose -f ~/sandbox/rails/compose.yaml pull db`

   完整示例如下：

   ```console
   $ docker compose -f ~/sandbox/rails/compose.yaml pull db
   Pulling db (postgres:18)...
   18: Pulling from library/postgres
   ef0380f84d05: Pull complete
   50cf91dc1db8: Pull complete
   d3add4cd115c: Pull complete
   467830d8a616: Pull complete
   089b9db7dc57: Pull complete
   6fba0a36935c: Pull complete
   81ef0e73c953: Pull complete
   338a6c4894dc: Pull complete
   15853f32f67c: Pull complete
   044c83d92898: Pull complete
   17301519f133: Pull complete
   dcca70822752: Pull complete
   cecf11b8ccf3: Pull complete
   Digest: sha256:1364924c753d5ff7e2260cd34dc4ba05ebd40ee8193391220be0f9901d4e1651
   Status: Downloaded newer image for postgres:18
   ```

## 示例

多个文件的常见用例是将开发环境的 Compose 应用更改为生产环境（可能是生产、预发布或 CI 环境）。为了支持这些差异，你可以将 Compose 配置拆分为几个不同的文件：

从一个基础文件开始，定义服务的规范配置。

`compose.yaml`

```yaml
services:
  web:
    image: example/my_web_app:latest
    depends_on:
      - db
      - cache

  db:
    image: postgres:18

  cache:
    image: redis:latest
```

在此示例中，开发配置将一些端口暴露给主机，将代码挂载为卷，并构建 web 镜像。

`compose.override.yaml`

```yaml
services:
  web:
    build: .
    volumes:
      - '.:/code'
    ports:
      - 8883:80
    environment:
      DEBUG: 'true'

  db:
    command: '-d'
    ports:
     - 5432:5432

  cache:
    ports:
      - 6379:6379
```

当你运行 `docker compose up` 时，它会自动读取覆盖文件。

要在生产环境中使用此 Compose 应用，需要创建另一个覆盖文件，该文件可能存储在不同的 git 仓库中或由不同的团队管理。

`compose.prod.yaml`

```yaml
services:
  web:
    ports:
      - 80:80
    environment:
      PRODUCTION: 'true'

  cache:
    environment:
      TTL: '500'
```

要使用此生产 Compose 文件部署，你可以运行：

```console
$ docker compose -f compose.yaml -f compose.prod.yaml up -d
```

这会使用 `compose.yaml` 和 `compose.prod.yaml` 中的配置部署所有三个服务，但不使用 `compose.override.yaml` 中的开发配置。

有关更多信息，请参阅 [在生产环境中使用 Compose](../production.md)。

## 限制

Docker Compose 支持应用程序模型中许多资源的相对路径：服务镜像的构建上下文、定义环境变量的文件位置、用于绑定挂载卷的本地目录路径。由于这种限制，在 monorepo 中组织代码可能变得困难，因为自然的选择是按团队或组件拥有专用文件夹，但这样 Compose 文件的相对路径就变得不相关了。

## 参考信息

- [合并规则](/reference/compose-file/merge.md)