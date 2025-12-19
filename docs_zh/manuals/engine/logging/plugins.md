---
description: 了解日志记录驱动插件，用于扩展和自定义 Docker 的日志记录功能
title: 使用日志记录驱动插件
keywords: logging, driver, plugins, monitoring
aliases:
  - /engine/admin/logging/plugins/
  - /engine/reference/logging/plugins/
  - /config/containers/logging/plugins/
---

Docker 日志记录插件允许您扩展和自定义 Docker 的日志记录功能，超越[内置日志记录驱动程序](configure.md)的功能。日志记录服务提供商可以[实现他们自己的插件](/manuals/engine/extend/plugins_logging.md)，并使其在 Docker Hub 或私有注册表中可用。本主题展示该日志记录服务的用户如何配置 Docker 来使用该插件。

## 安装日志记录驱动插件

要安装日志记录驱动插件，请使用 `docker plugin install <org/image>`，使用插件开发者提供的信息。

您可以使用 `docker plugin ls` 列出所有已安装的插件，并且可以使用 `docker inspect` 检查特定插件。

## 将插件配置为默认日志记录驱动

安装插件后，您可以通过在 `daemon.json` 中将插件的名称设置为 `log-driver` 键的值，来将 Docker 守护进程配置为使用它作为默认值，如[日志记录概述](configure.md#configure-the-default-logging-driver)中所述。如果日志记录驱动支持附加选项，您可以将它们设置为同一文件中 `log-opts` 数组的值。

## 配置容器使用插件作为日志记录驱动

安装插件后，您可以通过在 `docker run` 中指定 `--log-driver` 标志来配置容器使用插件作为其日志记录驱动，如[日志记录概述](configure.md#configure-the-logging-driver-for-a-container)中所述。如果日志记录驱动支持附加选项，您可以使用一个或多个 `--log-opt` 标志来指定它们，选项名称作为键，选项值作为值。