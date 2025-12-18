---
linkTitle: Migrate to Compose v2
Title: 从 Docker Compose v1 迁移到 v2
weight: 30
description: 从 Compose v1 迁移到 v2 的分步指导，包括语法差异、环境变量处理和 CLI 变化
keywords: 迁移 docker compose, 升级 docker compose v2, docker compose 迁移, docker compose v1 vs v2, docker compose CLI 变化, docker-compose 到 docker compose
aliases:
- /compose/compose-v2/
- /compose/cli-command-compatibility/
- /compose/migrate/
---

从 2023 年 7 月起，Compose v1 停止接收更新。它也不再包含在新版本的 Docker Desktop 中。

Compose v2 于 2020 年首次发布，已包含在所有当前受支持的 Docker Desktop 版本中。它提供了改进的 CLI 体验、使用 BuildKit 提升的构建性能，以及持续的新功能开发。

## 如何切换到 Compose v2？

最简单且推荐的方法是确保你安装了最新版本的 [Docker Desktop](/manuals/desktop/release-notes.md)，它捆绑了 Docker Engine 和包含 Compose v2 的 Docker CLI 平台。

使用 Docker Desktop，Compose v2 始终可以通过 `docker compose` 访问。

对于 Linux 上的手动安装，你可以通过以下方式获取 Compose v2：
- [使用 Docker 的仓库](/manuals/compose/install/linux.md#install-using-the-repository)（推荐）
- [手动下载并安装](/manuals/compose/install/linux.md#install-the-plugin-manually)

## Compose v1 和 Compose v2 之间有什么区别？

### `docker-compose` 与 `docker compose`

与 Compose v1 不同，Compose v2 集成到 Docker CLI 平台中，推荐的命令行语法是 `docker compose`。

Docker CLI 平台提供了一致且可预测的选项和标志集，例如 `DOCKER_HOST` 环境变量或 `--context` 命令行标志。

此更改允许你在根 `docker` 命令上使用所有共享标志。
例如，`docker --log-level=debug --tls compose up` 启用来自 Docker Engine 的调试日志，并确保连接使用 TLS。

> [!TIP]
>
> 通过将连字符（`-`）替换为空格，使用 `docker compose` 代替 `docker-compose` 来更新脚本以使用 Compose v2。

### 服务容器名称

Compose 基于项目名称、服务名称和规模/副本计数生成容器名称。

在 Compose v1 中，使用下划线（`_`）作为单词分隔符。
在 Compose v2 中，使用连字符（`-`）作为单词分隔符。

下划线在 DNS 主机名中不是有效字符。
通过使用连字符，Compose v2 确保服务容器可以通过一致、可预测的主机名通过网络访问。

例如，运行 Compose 命令 `-p myproject up --scale=1 svc` 在 Compose v1 中生成名为 `myproject_svc_1` 的容器，在 Compose v2 中生成名为 `myproject-svc-1` 的容器。

> [!TIP]
>
> 在 Compose v2 中，全局 `--compatibility` 标志或 `COMPOSE_COMPATIBILITY` 环境变量保留 Compose v1 的行为，使用下划线（`_`）作为单词分隔符以匹配 v1。
由于此选项必须为每个 Compose v2 命令指定，因此建议仅在向 Compose v2 过渡期间临时使用此选项。

### 命令行标志和子命令

Compose v2 支持几乎所有 Compose V1 标志和子命令，因此在大多数情况下，它可以作为脚本中的即插即用替代品使用。

#### v2 中不支持

以下功能在 Compose v1 中已弃用，在 Compose v2 中不支持：
* `docker-compose scale`。改用 `docker compose up --scale`。
* `docker-compose rm --all`

#### v2 中的行为差异

以下功能在 Compose v1 和 v2 之间行为不同：

|                         | Compose v1                                                       | Compose v2                                                                    |
|-------------------------|------------------------------------------------------------------|-------------------------------------------------------------------------------|
| `--compatibility`       | 已弃用。基于遗留架构版本迁移 YAML 字段。                           | 使用 `_` 作为容器名称的单词分隔符而不是 `-` 以匹配 v1。                         |
| `ps --filter KEY-VALUE` | 未记录。允许按任意服务属性过滤。                                   | 仅允许按特定属性过滤，例如 `--filter=status=running`。                         |

### 环境变量

Compose v1 中的环境变量行为未正式记录，在某些边缘情况下行为不一致。

对于 Compose v2，[环境变量](/manuals/compose/how-tos/environment-variables/_index.md) 部分涵盖了 [优先级](/manuals/compose/how-tos/environment-variables/envvars-precedence.md) 以及 [`.env` 文件插值](/manuals/compose/how-tos/environment-variables/variable-interpolation.md)，并包含许多示例，涵盖复杂情况，例如转义嵌套引号。

检查是否：
- 你的项目使用多级环境变量覆盖，例如 `.env` 文件和 `--env` CLI 标志。
- 任何 `.env` 文件值包含转义序列或嵌套引号。
- 任何 `.env` 文件值在其包含字面 `$` 符号。这在 PHP 项目中很常见。
- 任何变量值使用高级扩展语法，例如 `${VAR:?error}`。

> [!TIP]
>
> 运行 `docker compose config` 预览 Compose v2 执行插值后的配置，以验证值是否符合预期。
>
> 通常可以通过确保字面值（无插值）使用单引号，而需要应用插值的值使用双引号来保持与 Compose v1 的向后兼容性。

## 这对我的使用 Compose v1 的项目意味着什么？

对于大多数项目，切换到 Compose v2 不需要更改 Compose YAML 或你的开发工作流。

建议你适应 Compose v2 的新推荐运行方式，即使用 `docker compose` 代替 `docker-compose`。
这提供了额外的灵活性，并消除了对 `docker-compose` 兼容性别名的需求。

但是，Docker Desktop 继续支持 `docker-compose` 别名以将命令重定向到 `docker compose`，以提供便利性和改进与第三方工具和脚本的兼容性。

## 切换前还有什么需要了解的吗？

### 迁移正在运行的项目

在 v1 和 v2 中，对 Compose 项目运行 up 会根据需要重新创建服务容器。它将 Docker Engine 中的实际状态与解析的项目配置进行比较，后者包括 Compose YAML、环境变量和命令行标志。

由于 Compose v1 和 v2 [为服务容器命名的方式不同](#service-container-names)，首次使用 v2 在原本由 v1 启动的运行服务的项目上运行 `up` 会导致服务容器被重新创建并更新名称。

请注意，即使使用 `--compatibility` 标志保留 v1 命名风格，Compose 仍需要在首次使用 v2 运行 `up` 时重新创建原本由 v1 启动的服务容器，以迁移内部状态。

### 在 Docker-in-Docker 中使用 Compose v2

Compose v2 现在已包含在 [Docker Hub 上的 Docker 官方镜像](https://hub.docker.com/_/docker) 中。

此外，Docker Hub 上的 [docker/compose-bin 镜像](https://hub.docker.com/r/docker/compose-bin) 打包了最新版本的 Compose v2，用于多阶段构建。

## 如果我想使用，还能继续使用 Compose v1 吗？

可以。你仍然可以下载和安装 Compose v1 包，但如果出现问题，Docker 不会提供支持。

>[!WARNING]
>
> Compose v1 的最终版本是 2021 年 5 月 10 日发布的 1.29.2 版。这些包自那以后没有收到任何安全更新。使用风险自负。

## 额外资源

- [PyPI 上的 docker-compose v1](https://pypi.org/project/docker-compose/1.29.2/)
- [Docker Hub 上的 docker/compose v1](https://hub.docker.com/r/docker/compose)
- [GitHub 上的 docker-compose v1 源码](https://github.com/docker/compose/releases/tag/1.29.2)