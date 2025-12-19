---
description: 了解如何合并 Compose 文件
keywords: compose, docker, merge, compose file
title: 合并 Compose 文件
linkTitle: 合并
weight: 10
aliases:
- /compose/multiple-compose-files/merge/
---

Docker Compose 允许你合并和覆盖一组 Compose 文件，以创建一个复合的 Compose 文件。

默认情况下，Compose 会读取两个文件：`compose.yaml` 和一个可选的 `compose.override.yaml` 文件。按照惯例，`compose.yaml` 包含你的基础配置。覆盖文件可以包含对现有服务的配置覆盖，或者全新的服务。

如果某个服务在两个文件中都定义了，Compose 会使用下文描述的规则以及 [Compose 规范](/reference/compose-file/merge.md) 中的规则来合并配置。

## 如何合并多个 Compose 文件

要使用多个覆盖文件，或者使用不同名称的覆盖文件，你可以使用预定义的 [COMPOSE_FILE](../environment-variables/envvars.md#compose_file) 环境变量，或者使用 `-f` 选项来指定文件列表。

Compose 按照在命令行中指定的顺序合并文件。后续的文件可以合并、覆盖或添加到其前面的文件中。

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

`compose.admin.yaml` 也可能指定了同一个服务：

```yaml
webapp:
  environment:
    - DEBUG=1
```

任何匹配的字段都会覆盖前一个文件中的字段。新值会被添加到 `webapp` 服务的配置中：

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

- 路径是相对于基础文件进行评估的。当你使用多个 Compose 文件时，必须确保文件中的所有路径都是相对于基础 Compose 文件（使用 `-f` 指定的第一个 Compose 文件）的。这是必需的，因为覆盖文件不必是有效的 Compose 文件。覆盖文件可以只包含一小部分配置片段。跟踪某个服务的哪个片段相对于哪个路径是困难且令人困惑的，因此为了使路径更容易理解，所有路径都必须相对于基础文件定义。

   >[!TIP]
   >
   > 你可以使用 `docker compose config` 来检查合并后的配置，并避免与路径相关的问题。

- Compose 将原始服务的配置复制到本地服务中。如果某个配置选项在原始服务和本地服务中都定义了，则本地值会替换或扩展原始值。

   - 对于像 `image`、`command` 或 `mem_limit` 这样的单值选项，新值会替换旧值。

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

   - 对于多值选项 `ports`、`expose`、`external_links`、`dns`、`dns_search` 和 `tmpfs`，Compose 会将两组值连接起来：

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

   - 对于 `environment`、`labels`、`volumes` 和 `devices`，Compose 会“合并”条目，其中本地定义的值具有优先权。对于 `environment` 和 `labels`，环境变量或标签名称决定了使用哪个值：

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

- 使用 `-f` 是可选的。如果未提供，Compose 会在工作目录及其父目录中搜索 `compose.yaml` 和 `compose.override.yaml` 文件。你必须至少提供 `compose.yaml` 文件。如果两个文件存在于同一目录级别，Compose 会将它们组合成一个配置。

- 你可以将 `-f` 与 `-`（短横线）作为文件名一起使用，以从 `stdin` 读取配置。例如：
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
   
   当使用 `stdin` 时，配置中的所有路径都是相对于当前工作目录的。
   
- 你可以使用 `-f` 标志来指定一个不在当前目录中的 Compose 文件路径，可以通过命令行设置，也可以通过在 shell 中或环境文件中设置 [COMPOSE_FILE 环境变量](../environment-variables/envvars.md#compose_file)。

   例如，如果你正在运行 [Compose Rails 示例](https://github.com/docker/awesome-compose/tree/master/official-documentation-samples/rails/README.md)，并且在一个名为 `sandbox/rails` 的目录中有一个 `compose.yaml` 文件。你可以使用像 [docker compose pull](/reference/cli/docker/compose/pull.md) 这样的命令，通过 `-f` 标志从任何地方获取 `db` 服务的 postgres 镜像，如下所示：`docker compose -f ~/sandbox/rails/compose.yaml pull db`

   以下是完整示例：

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

使用多个文件的一个常见用例是为生产类环境（可能是生产、预发或 CI）更改开发 Compose 应用。为了支持这些差异，你可以将 Compose 配置拆分为几个不同的文件：

从一个定义服务规范配置的基础文件开始。

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

在此示例中，开发配置向主机暴露了一些端口，将我们的代码挂载为卷，并构建 web 镜像。

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

要在生产环境中使用此 Compose 应用，可以创建另一个覆盖文件，该文件可能存储在不同的 git 仓库中或由不同的团队管理。

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

要使用此生产 Compose 文件进行部署，你可以运行

```console
$ docker compose -f compose.yaml -f compose.prod.yaml up -d
```

这将使用 `compose.yaml` 和 `compose.prod.yaml` 中的配置部署所有三个服务，但不使用 `compose.override.yaml` 中的开发配置。

有关更多信息，请参阅 [在生产中使用 Compose](../production.md)。

## 限制

Docker Compose 为许多要包含在应用程序模型中的资源支持相对路径：服务镜像的构建上下文、定义环境变量的文件位置、绑定挂载卷中使用的本地目录路径。有了这样的限制，在 monorepo（单体仓库）中的代码组织可能会变得困难，因为自然的选择是为每个团队或组件设置专用文件夹，但这样 Compose 文件的相对路径就会变得无关紧要。

## 参考信息

- [合并规则](/reference/compose-file/merge.md)