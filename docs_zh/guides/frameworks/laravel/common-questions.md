---
title: 在 Laravel 中使用 Docker 的常见问题
description: 查找有关使用 Docker Compose 设置和管理 Laravel 环境的常见问题解答，包括故障排除和最佳实践。
weight: 40
---

<!-- vale Docker.HeadingLength = NO -->

## 1. 为什么我应该为 Laravel 使用 Docker Compose？

Docker Compose 是一个强大的工具，用于管理多容器环境，特别是在开发中，因为它简单易用。使用 Docker Compose，您可以在单个配置文件（`compose.*.yaml`）中定义并连接 Laravel 所需的所有服务，例如 PHP、Nginx 和数据库。这种设置确保了开发、测试和生产环境之间的一致性，简化了新成员的加入流程，并减少了本地与服务器环境之间的差异。

虽然 Docker Compose 是开发的绝佳选择，但像 **Docker Swarm** 或 **Kubernetes** 这样的工具提供了更高级的扩展和编排功能，这对于复杂的生产部署可能更有益。

## 2. 如何使用 Docker Compose 调试我的 Laravel 应用？

要在 Docker 环境中调试您的 Laravel 应用，请使用 **Xdebug**。在开发设置中，Xdebug 安装在 `php-fpm` 容器中以启用调试功能。请确保在您的 `compose.dev.yaml` 文件中通过设置环境变量 `XDEBUG_ENABLED=true` 来启用 Xdebug，并配置您的 IDE（例如 Visual Studio Code 或 PHPStorm）以连接到远程容器进行调试。

## 3. 我可以将 Docker Compose 与 PostgreSQL 以外的数据库一起使用吗？

是的，Docker Compose 支持多种用于 Laravel 的数据库服务。虽然示例中使用了 PostgreSQL，但您可以轻松地替换为 **MySQL**、**MariaDB** 甚至 **SQLite**。更新 `compose.*.yaml` 文件以指定所需的 Docker 镜像，并调整您的 `.env` 文件以反映新的数据库配置。

## 4. 如何在开发和生产中持久化数据？

在开发和生产中，都使用 Docker 卷来持久化数据。例如，在 `compose.*.yaml` 文件中，`postgres-data-*` 卷存储 PostgreSQL 数据，确保即使容器重启，数据也能被保留。您还可以为其他需要数据持久化的服务定义命名卷。

## 5. 开发和生产环境的 Docker 配置有什么区别？

在开发环境中，Docker 配置包含简化编码和调试的工具，例如用于调试的 Xdebug，以及卷挂载以实现无需重新构建镜像的实时代码更新。

在生产环境中，配置针对性能、安全性和效率进行了优化。这种设置使用多阶段构建来保持镜像轻量，并且仅包含必要的工具、包和库。

建议在生产中使用基于 `alpine` 的镜像，以获得更小的镜像尺寸，从而提高部署速度和安全性。

此外，考虑使用 [Docker Scout](/manuals/scout/_index.md) 来检测和分析漏洞，尤其是在生产环境中。

有关在生产中使用 Docker Compose 的更多信息，请参阅[本指南](/compose/how-tos/production/)。