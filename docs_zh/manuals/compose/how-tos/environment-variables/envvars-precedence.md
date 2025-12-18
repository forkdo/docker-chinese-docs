---
title: Docker Compose 中环境变量的优先级
linkTitle: 环境变量优先级
description: 说明 Compose 中环境变量解析顺序的场景概览
keywords: compose, environment, env file
weight: 20
aliases:
- /compose/envvars-precedence/
- /compose/environment-variables/envvars-precedence/
---

当同一个环境变量在多个来源中设置时，Docker Compose 会遵循一个优先级规则来确定容器环境中该变量的值。

本文档解释了当环境变量在多个位置定义时，Docker Compose 如何确定其最终值。

优先级顺序（从高到低）如下：
1. 使用 [`docker compose run -e` 在命令行中设置](set-environment-variables.md#set-environment-variables-with-docker-compose-run---env)。
2. 使用 `environment` 或 `env_file` 属性设置，但值是从你的 [shell](variable-interpolation.md#substitute-from-the-shell) 或环境文件中插值而来（要么是默认的 [`.env` 文件](variable-interpolation.md#env-file)，要么是通过命令行中的 [`--env-file` 参数](variable-interpolation.md#substitute-with---env-file) 指定的文件）。
3. 在 Compose 文件中仅使用 [`environment` 属性](set-environment-variables.md#use-the-environment-attribute) 设置。
4. 在 Compose 文件中使用 [`env_file` 属性](set-environment-variables.md#use-the-env_file-attribute) 设置。
5. 在容器镜像的 [ENV 指令](/reference/dockerfile.md#env) 中设置。
   只有在 Docker Compose 中没有为 `environment`、`env_file` 或 `run --env` 设置任何 `ARG` 或 `ENV` 时，`Dockerfile` 中的 `ARG` 或 `ENV` 设置才会生效。

## 简单示例

在以下示例中，同一个环境变量在 `.env` 文件和 Compose 文件的 `environment` 属性中设置了不同的值：

```console
$ cat ./webapp.env
NODE_ENV=test

$ cat compose.yaml
services:
  webapp:
    image: 'webapp'
    env_file:
     - ./webapp.env
    environment:
     - NODE_ENV=production
```

使用 `environment` 属性定义的环境变量具有更高的优先级。

```console
$ docker compose run webapp env | grep NODE_ENV
NODE_ENV=production
```

## 进阶示例

下表使用 `VALUE` 环境变量（定义镜像版本）作为示例。

### 表格说明

每一列表示一个可以设置 `VALUE` 值或从中插值的上下文。

`Host OS environment` 和 `.env` 文件列仅用于说明。实际上，它们本身不会在容器中创建变量，但会与 `environment` 或 `env_file` 属性结合使用。

每一行表示 `VALUE` 被设置、插值或两者兼有的上下文组合。**Result** 列显示每种场景下 `VALUE` 的最终值。

|  # |  `docker compose run`  |  `environment` attribute  |  `env_file` attribute  |  Image `ENV` |  `Host OS` environment  |  `.env` file      |   Result  |
|:--:|:----------------:|:-------------------------------:|:----------------------:|:------------:|:-----------------------:|:-----------------:|:----------:|
|  1 |   -              |   -                             |   -                    |   -          |  `VALUE=1.4`            |  `VALUE=1.3`      | -               |
|  2 |   -              |   -                             |  `VALUE=1.6`           |  `VALUE=1.5` |  `VALUE=1.4`            |   -               |**`VALUE=1.6`**  |
|  3 |   -              |  `VALUE=1.7`                    |   -                    |  `VALUE=1.5` |  `VALUE=1.4`            |   -               |**`VALUE=1.7`**  |
|  4 |   -              |   -                             |   -                    |  `VALUE=1.5` |  `VALUE=1.4`            |  `VALUE=1.3`      |**`VALUE=1.5`**  |
|  5 |`--env VALUE=1.8` |   -                             |   -                    |  `VALUE=1.5` |  `VALUE=1.4`            |  `VALUE=1.3`      |**`VALUE=1.8`**  |
|  6 |`--env VALUE`     |   -                             |   -                    |  `VALUE=1.5` |  `VALUE=1.4`            |  `VALUE=1.3`      |**`VALUE=1.4`**  |
|  7 |`--env VALUE`     |   -                             |   -                    |  `VALUE=1.5` |   -                     |  `VALUE=1.3`      |**`VALUE=1.3`**  |
|  8 |   -              |   -                             |   `VALUE`              |  `VALUE=1.5` |  `VALUE=1.4`            |  `VALUE=1.3`      |**`VALUE=1.4`**  |
|  9 |   -              |   -                             |   `VALUE`              |  `VALUE=1.5` |   -                     |  `VALUE=1.3`      |**`VALUE=1.3`**  |
| 10 |   -              |  `VALUE`                        |   -                    |  `VALUE=1.5` |  `VALUE=1.4`            |  `VALUE=1.3`      |**`VALUE=1.4`**  |
| 11 |   -              |  `VALUE`                        |   -                    |  `VALUE=1.5` |  -                      |  `VALUE=1.3`      |**`VALUE=1.3`**  |
| 12 |`--env VALUE`     |  `VALUE=1.7`                    |   -                    |  `VALUE=1.5` |  `VALUE=1.4`            |  `VALUE=1.3`      |**`VALUE=1.4`**  |
| 13 |`--env VALUE=1.8` |  `VALUE=1.7`                    |   -                    |  `VALUE=1.5` |  `VALUE=1.4`            |  `VALUE=1.3`      |**`VALUE=1.8`**  |
| 14 |`--env VALUE=1.8` |   -                             |  `VALUE=1.6`           |  `VALUE=1.5` |  `VALUE=1.4`            |  `VALUE=1.3`      |**`VALUE=1.8`**  |
| 15 |`--env VALUE=1.8` |  `VALUE=1.7`                    |  `VALUE=1.6`           |  `VALUE=1.5` |  `VALUE=1.4`            |  `VALUE=1.3`      |**`VALUE=1.8`**  |

### 理解优先级结果

结果 1：本地环境具有优先级，但 Compose 文件未设置在容器内复制此变量，因此未设置该变量。

结果 2：Compose 文件中的 `env_file` 属性为 `VALUE` 定义了显式值，因此容器环境相应设置。

结果 3：Compose 文件中的 `environment` 属性为 `VALUE` 定义了显式值，因此容器环境相应设置。

结果 4：镜像的 `ENV` 指令声明了变量 `VALUE`，由于 Compose 文件未设置覆盖此值，因此该变量由镜像定义。

结果 5：`docker compose run` 命令的 `--env` 标志设置了显式值，并覆盖了镜像中设置的值。

结果 6：`docker compose run` 命令的 `--env` 标志设置为复制环境中的值。Host OS 值具有优先级并复制到容器环境中。

结果 7：`docker compose run` 命令的 `--env` 标志设置为复制环境中的值。从 `.env` 文件中选择的值定义容器环境。

结果 8：Compose 文件中的 `env_file` 属性设置为从本地环境复制 `VALUE`。Host OS 值具有优先级并复制到容器环境中。

结果 9：Compose 文件中的 `env_file` 属性设置为从本地环境复制 `VALUE`。从 `.env` 文件中选择的值定义容器环境。

结果 10：Compose 文件中的 `environment` 属性设置为从本地环境复制 `VALUE`。Host OS 值具有优先级并复制到容器环境中。

结果 11：Compose 文件中的 `environment` 属性设置为从本地环境复制 `VALUE`。从 `.env` 文件中选择的值定义容器环境。

结果 12：`--env` 标志比 `environment` 和 `env_file` 属性具有更高的优先级，设置为复制本地环境中的 `VALUE`。Host OS 值具有优先级并复制到容器环境中。

结果 13 到 15：`--env` 标志比 `environment` 和 `env_file` 属性具有更高的优先级，因此设置了值。

## 下一步

- [在 Compose 中设置环境变量](set-environment-variables.md)
- [在 Compose 文件中使用变量插值](variable-interpolation.md)