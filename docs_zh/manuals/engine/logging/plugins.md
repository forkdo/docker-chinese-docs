---
description: 了解日志驱动插件，用于扩展和自定义 Docker 的日志功能
title: 使用日志驱动插件
keywords: 日志记录, 驱动, 插件, 监控
aliases:
  - /engine/admin/logging/plugins/
  - /engine/reference/logging/plugins/
  - /config/containers/logging/plugins/
---

Docker 日志驱动插件允许你扩展和自定义 Docker 的日志功能，超越[内置日志驱动](configure.md)的能力范围。日志服务提供商可以[实现自己的插件](/manuals/engine/extend/plugins_logging.md)并将其发布到 Docker Hub 或私有仓库。本主题展示了使用该日志服务的用户如何配置 Docker 以使用该插件。

## 安装日志驱动插件

要安装日志驱动插件，请使用 `docker plugin install <org/image>`，具体信息由插件开发者提供。

你可以使用 `docker plugin ls` 列出所有已安装的插件，并使用 `docker inspect` 检查特定插件。

## 将插件配置为默认日志驱动

安装插件后，你可以通过在 `daemon.json` 中将插件名称设置为 `log-driver` 键的值，将 Docker 守护进程配置为使用该插件作为默认驱动，详细信息请参阅[日志概述](configure.md#configure-the-default-logging-driver)。如果日志驱动支持额外选项，你可以在同一文件中将这些选项设置为 `log-opts` 数组的值。

## 配置容器使用插件作为日志驱动

安装插件后，你可以通过在 `docker run` 中指定 `--log-driver` 标志，将容器配置为使用该插件作为其日志驱动，详细信息请参阅[日志概述](configure.md#configure-the-logging-driver-for-a-container)。如果日志驱动支持额外选项，你可以使用一个或多个 `--log-opt` 标志指定它们，选项名称作为键，选项值作为值。