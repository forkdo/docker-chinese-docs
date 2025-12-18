---
title: 使用 Docker 运行 Laravel 的常见问题
description: 查找关于使用 Docker Compose 设置和管理 Laravel 环境的常见问题解答，包括故障排除和最佳实践。
weight: 40
---

<!-- vale Docker.HeadingLength = NO -->

## 1. 为什么我应该对 Laravel 使用 Docker Compose？

Docker Compose 是管理多容器环境的强大工具，特别适合开发环境，因为它简单易用。使用 Docker Compose，你可以在单个配置文件（`compose.*.yaml`）中定义并连接 Laravel 所需的所有服务，例如 PHP、Nginx 和数据库。这种设置确保了开发、测试和生产环境之间的一致性，简化了团队上手流程，减少了本地环境与服务器环境之间的差异。

虽然 Docker Compose 非常适合开发，但像 **Docker Swarm** 或 **Kubernetes** 这样的工具提供了更高级的扩展和编排功能，可能更适合复杂的生产部署。

## 2. 如何使用 Docker Compose 调试 Laravel 应用？

要在 Docker 环境中调试 Laravel 应用，可以使用 **Xdebug**。在开发环境中，Xdebug 已安装在 `php-fpm` 容器中以启用调试功能。确保在 `compose.dev.yaml` 文件中通过设置环境变量 `XDEBUG_ENABLED=true` 来启用 Xdebug，并配置你的 IDE（例如 Visual Studio Code 或 PHPStorm）连接到远程容器进行调试。

## 3. 我可以使用除 PostgreSQL 以外的数据库与 Docker Compose 配合吗？

可以，Docker Compose 支持 Laravel 使用多种数据库服务。虽然示例中使用了 PostgreSQL，但你可以轻松替换为 **MySQL**、**MariaDB** 甚至 **SQLite**。只需在 `compose.*.yaml` 文件中指定所需的 Docker 镜像，并在 `.env` 文件中更新相应的数据库配置即可。

## 4. 如何在开发和生产环境中持久化数据？

在开发和生产环境中，Docker 都使用卷（volume）来持久化数据。例如，在 `compose.*.yaml` 文件中，`postgres-data-*` 卷用于存储 PostgreSQL 数据，确保即使容器重启数据也不会丢失。你也可以为其他需要持久化数据的服务定义命名卷。

## 5. 开发和生产环境的 Docker 配置有什么区别？

在开发环境中，Docker 配置包含有助于简化编码和调试的工具，例如用于调试的 Xdebug，以及支持实时代码更新的卷挂载，无需重建镜像。

在生产环境中，配置经过优化，专注于性能、安全性和效率。这种设置使用多阶段构建来保持镜像轻量化，仅包含必要的工具、包和库。

建议在生产环境中使用基于 `alpine` 的镜像，以减小镜像体积，提升部署速度并增强安全性。

此外，建议使用 [Docker Scout](/manuals/scout/_index.md) 来检测和分析漏洞，尤其是在生产环境中。

有关在生产环境中使用 Docker Compose 的更多信息，请参阅[本指南](/compose/how-tos/production/)。