---
description: Compose 预定义环境变量
keywords: fig, 编排, compose, docker, 编排, cli, 参考, compose 环境配置, docker 环境变量
title: 在 Docker Compose 中配置预定义环境变量
linkTitle: 预定义环境变量
weight: 30
aliases:
- /compose/reference/envvars/
- /compose/environment-variables/envvars/
---

Docker Compose 包含多个预定义的环境变量。它也会继承常见的 Docker CLI 环境变量，例如 `DOCKER_HOST` 和 `DOCKER_CONTEXT`。详细信息请参阅 [Docker CLI 环境变量参考](/reference/cli/docker/#environment-variables)。

本页说明如何设置或更改以下预定义环境变量：

- `COMPOSE_PROJECT_NAME`
- `COMPOSE_FILE`
- `COMPOSE_PROFILES`
- `COMPOSE_CONVERT_WINDOWS_PATHS`
- `COMPOSE_PATH_SEPARATOR`
- `COMPOSE_IGNORE_ORPHANS`
- `COMPOSE_REMOVE_ORPHANS`
- `COMPOSE_PARALLEL_LIMIT`
- `COMPOSE_ANSI`
- `COMPOSE_STATUS_STDOUT`
- `COMPOSE_ENV_FILES`
- `COMPOSE_DISABLE_ENV_FILE`
- `COMPOSE_MENU`
- `COMPOSE_EXPERIMENTAL`
- `COMPOSE_PROGRESS`

## 覆盖方法

| 方法      | 描述                                  |
| ----------- | -------------------------------------------- |
| [`.env` 文件](/manuals/compose/how-tos/environment-variables/variable-interpolation.md) | 位于工作目录中。            |
| [Shell](variable-interpolation.md#substitute-from-the-shell)       | 在主机操作系统 shell 中定义。  |
| CLI         | 在运行时使用 `--env` 或 `-e` 标志传递。 |

更改或设置任何环境变量时，请注意 [环境变量优先级](envvars-precedence.md)。

## 配置详情

### 项目和文件配置

#### COMPOSE\_PROJECT\_NAME

设置项目名称。此值在启动时会与服务名称一起添加到容器名称的前缀中。

例如，如果您的项目名称是 `myapp`，并且包含两个服务 `db` 和 `web`，那么 Compose 启动的容器将分别命名为 `myapp-db-1` 和 `myapp-web-1`。

Compose 可以通过不同方式设置项目名称。每种方法的优先级（从高到低）如下：

1. `-p` 命令行标志
2. `COMPOSE_PROJECT_NAME`
3. 配置文件中的顶级 `name:` 变量（或使用 `-f` 指定的一系列配置文件中的最后一个 `name:`）
4. 包含配置文件的项目目录的 `basename`（或使用 `-f` 指定的第一个配置文件所在目录的 `basename`）
5. 如果未指定配置文件，则为当前目录的 `basename`

项目名称必须仅包含小写字母、十进制数字、连字符和下划线，并且必须以小写字母或十进制数字开头。如果项目目录或当前目录的 `basename` 违反此约束，则必须使用其他机制。

另请参阅 [命令行选项概述](/reference/cli/docker/compose/_index.md#command-options-overview-and-help) 和 [使用 `-p` 指定项目名称](/reference/cli/docker/compose/_index.md#use--p-to-specify-a-project-name)。

#### COMPOSE\_FILE

指定 Compose 文件的路径。支持指定多个 Compose 文件。

- 默认行为：如果未提供，Compose 会在当前目录中查找名为 `compose.yaml` 的文件，如果未找到，则 Compose 会递归搜索每个父目录，直到找到该名称的文件。
- 指定多个 Compose 文件时，默认路径分隔符为：
   - Mac 和 Linux：`:`（冒号）
   - Windows：`;`（分号）
   例如：

      ```console
      COMPOSE_FILE=compose.yaml:compose.prod.yaml
      ```
   路径分隔符也可以使用 [`COMPOSE_PATH_SEPARATOR`](#compose_path_separator) 自定义。

另请参阅 [命令行选项概述](/reference/cli/docker/compose/_index.md#command-options-overview-and-help) 和 [使用 `-f` 指定一个或多个 Compose 文件的名称和路径](/reference/cli/docker/compose/_index.md#use--f-to-specify-the-name-and-path-of-one-or-more-compose-files)。

#### COMPOSE\_PROFILES

指定一个或多个在运行 `docker compose up` 时启用的配置文件。

具有匹配配置文件的服务以及未定义配置文件的任何服务都会启动。

例如，使用 `COMPOSE_PROFILES=frontend` 调用 `docker compose up` 会选择具有 `frontend` 配置文件的服务以及任何未指定配置文件的服务。

如果指定多个配置文件，请使用逗号作为分隔符。

以下示例启用所有与 `frontend` 和 `debug` 配置文件匹配的服务以及未指定配置文件的服务。

```console
COMPOSE_PROFILES=frontend,debug
```

另请参阅 [使用 Compose 配置文件](../profiles.md) 和 [`--profile` 命令行选项](/reference/cli/docker/compose/_index.md#use-profiles-to-enable-optional-services)。

#### COMPOSE\_PATH\_SEPARATOR

为 `COMPOSE_FILE` 中列出的项目指定不同的路径分隔符。

- 默认为：
    - macOS 和 Linux：`:`
    - Windows：`;`

#### COMPOSE\_ENV\_FILES

指定 Compose 在未使用 `--env-file` 时应使用的环境文件。

使用多个环境文件时，请使用逗号作为分隔符。例如：

```console
COMPOSE_ENV_FILES=.env.envfile1,.env.envfile2
```

如果未设置 `COMPOSE_ENV_FILES`，并且您未在 CLI 中提供 `--env-file`，Docker Compose 使用默认行为，即在项目目录中查找 `.env` 文件。

#### COMPOSE\_DISABLE\_ENV\_FILE

允许您禁用使用默认的 `.env` 文件。

- 支持的值：
    - `true` 或 `1`，Compose 忽略 `.env` 文件
    - `false` 或 `0`，Compose 在项目目录中查找 `.env` 文件
- 默认为：`0`

### 环境处理和容器生命周期

#### COMPOSE\_CONVERT\_WINDOWS\_PATHS

启用时，Compose 在卷定义中执行从 Windows 风格到 Unix 风格的路径转换。

- 支持的值：
    - `true` 或 `1`，启用
    - `false` 或 `0`，禁用
- 默认为：`0`

#### COMPOSE\_IGNORE\_ORPHANS

启用时，Compose 不会尝试检测项目的孤立容器。

- 支持的值：
   - `true` 或 `1`，启用
   - `false` 或 `0`，禁用
- 默认为：`0`

#### COMPOSE\_REMOVE\_ORPHANS

启用时，Compose 在更新服务或堆栈时自动删除孤立容器。孤立容器是指由先前配置创建但当前 `compose.yaml` 文件中不再定义的容器。

- 支持的值：
   - `true` 或 `1`，启用自动删除孤立容器
   - `false` 或 `0`，禁用自动删除。Compose 会显示关于孤立容器的警告。
- 默认为：`0`

#### COMPOSE\_PARALLEL\_LIMIT

指定并发引擎调用的最大并行级别。

### 输出

#### COMPOSE\_ANSI

指定何时打印 ANSI 控制字符。

- 支持的值：
   - `auto`，Compose 检测是否可以使用 TTY 模式。否则，使用纯文本模式
   - `never`，使用纯文本模式
   - `always` 或 `0`，使用 TTY 模式
- 默认为：`auto`

#### COMPOSE\_STATUS\_STDOUT

启用时，Compose 将其内部状态和进度消息写入 `stdout` 而不是 `stderr`。默认值为 false，以清楚地分离 Compose 消息和容器日志之间的输出流。

- 支持的值：
   - `true` 或 `1`，启用
   - `false` 或 `0`，禁用
- 默认为：`0`

#### COMPOSE\_PROGRESS

{{< summary-bar feature_name="Compose progress" >}}

定义进度输出的类型，如果未使用 `--progress`。支持的值为 `auto`、`tty`、`plain`、`json` 和 `quiet`。默认为 `auto`。

### 用户体验

#### COMPOSE\_MENU

{{< summary-bar feature_name="Compose menu" >}}

启用时，Compose 显示一个导航菜单，您可以在其中选择在 Docker Desktop 中打开 Compose 堆栈、启用 [`watch` 模式](../file-watch.md)，或使用 [Docker Debug](/reference/cli/docker/debug.md)。

- 支持的值：
   - `true` 或 `1`，启用
   - `false` 或 `0`，禁用
- 默认为：如果您通过 Docker Desktop 获得 Docker Compose，则默认为 `1`，否则默认为 `0`

#### COMPOSE\_EXPERIMENTAL

{{< summary-bar feature_name="Compose experimental" >}}

这是一个选择退出变量。关闭时会停用实验性功能。

- 支持的值：
   - `true` 或 `1`，启用
   - `false` 或 `0`，禁用
- 默认为：`1`

## Compose V2 中不支持

以下环境变量在 Compose V2 中无效。详细信息请参阅 [迁移到 Compose V2](/manuals/compose/releases/migrate.md)。

- `COMPOSE_API_VERSION`
    默认情况下，API 版本与服务器协商。使用 `DOCKER_API_VERSION`。请参阅 [Docker CLI 环境变量参考](/reference/cli/docker/#environment-variables) 页面。
- `COMPOSE_HTTP_TIMEOUT`
- `COMPOSE_TLS_VERSION`
- `COMPOSE_FORCE_WINDOWS_HOST`
- `COMPOSE_INTERACTIVE_NO_CLI`
- `COMPOSE_DOCKER_CLI_BUILD`
    使用 `DOCKER_BUILDKIT` 在 BuildKit 和经典构建器之间选择。如果 `DOCKER_BUILDKIT=0`，则 `docker compose build` 使用经典构建器构建镜像。