---
description: 查找用于定义多容器应用程序的最新推荐 Docker Compose 文件格式版本。
keywords: docker compose file, docker compose yml, docker compose reference, docker
  compose cmd, docker compose user, docker compose image, yaml spec, docker compose
  syntax, yaml specification, docker compose specification
title: Compose 文件参考
toc_max: 4
toc_min: 1
grid:
- title: Version and name top-level element
  description: 理解 Compose 的 version 和 name 属性。
  icon: text_snippet
  link: /reference/compose-file/version-and-name/
- title: Services top-level element
  description: 探索 Compose 的所有 services 属性。
  icon: construction
  link: /reference/compose-file/services/
- title: Networks top-level element
  description: 查找 Compose 的所有 networks 属性。
  icon: lan
  link: /reference/compose-file/networks/
- title: Volumes top-level element
  description: 探索 Compose 的所有 volumes 属性。
  icon: database
  link: /reference/compose-file/volumes/
- title: Configs top-level element
  description: 了解 Compose 中的 configs。
  icon: settings
  link: /reference/compose-file/configs/
- title: Secrets top-level element
  description: 了解 Compose 中的 secrets。
  icon: lock
  link: /reference/compose-file/secrets/
aliases:
 - /compose/yaml/
 - /compose/compose-file/compose-file-v1/
 - /compose/compose-file/
 - /compose/reference/overview/
---

>**刚接触 Docker Compose？**
>
> 查找有关 [Docker Compose 的关键特性和使用场景](/manuals/compose/intro/features-uses.md) 的更多信息，或 [尝试快速入门指南](/manuals/compose/gettingstarted.md)。

Compose 规范是 Compose 文件格式的最新且推荐的版本。它帮助您定义 [Compose 文件](/manuals/compose/intro/compose-application-model.md)，用于配置 Docker 应用程序的服务、网络、卷等。

Compose 文件格式的旧版本 2.x 和 3.x 已合并到 Compose 规范中。它在 Docker Compose CLI 的 1.27.0 及以上版本（也称为 Compose v2）中实现。

Docker Docs 上的 Compose 规范是 Docker Compose 的实现。如果您希望实现自己的 Compose 规范版本，请参阅 [Compose 规范仓库](https://github.com/compose-spec/compose-spec)。

使用以下链接导航 Compose 规范的关键部分。

> [!TIP]
>
> 希望在 VS Code 中获得更好的 Compose 文件编辑体验？
> 查看 [Docker VS Code 扩展（Beta）](https://marketplace.visualstudio.com/items?itemName=docker.docker)，支持代码检查、代码导航和漏洞扫描功能。

{{< grid >}}