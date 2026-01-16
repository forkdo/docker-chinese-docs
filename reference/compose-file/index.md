---
title: Compose 文件参考
url: /reference/compose-file/
parent:
  title: 参考文档
  url: /reference/
breadcrumbs:
  - title: 参考文档
    url: /reference/
  - title: Compose 文件参考
    url: /reference/compose-file/
children:
  - title: 版本和名称顶级元素
    url: /reference/compose-file/version-and-name/
    description: 了解何时以及是否设置版本和名称顶级元素
  - title: 在 Docker Compose 中定义服务
    url: /reference/compose-file/services/
    description: 探索服务顶级元素可以拥有的所有属性。
  - title: 在 Docker Compose 中定义和管理网络
    url: /reference/compose-file/networks/
    description: 了解如何使用 Docker Compose 中的顶层 networks 元素来配置和控制网络。
  - title: 在 Docker Compose 中定义和管理卷
    url: /reference/compose-file/volumes/
    description: 使用顶层 volumes 元素控制卷的声明方式以及在服务之间的共享方式。
  - title: Configs 顶级元素
    url: /reference/compose-file/configs/
    description: 使用 Docker Compose 中的 configs 元素管理和共享配置数据。
  - title: Secrets
    url: /reference/compose-file/secrets/
    description: 探索 secrets 顶级元素可以拥有的所有属性。
  - title: 片段
    url: /reference/compose-file/fragments/
    description: 使用 YAML 锚点和片段复用配置
  - title: 扩展
    url: /reference/compose-file/extension/
    description: 在 Docker Compose 中使用扩展定义和复用自定义片段
  - title: 插值
    url: /reference/compose-file/interpolation/
    description: 使用插值语法在 Docker Compose 文件中替换环境变量。
  - title: 合并 Compose 文件
    url: /reference/compose-file/merge/
    description: 了解 Docker Compose 如何合并多个文件并解决冲突
  - title: 使用 include 模块化 Compose 文件
    url: /reference/compose-file/include/
    description: 使用 include 顶级元素引用外部 Compose 文件
  - title: 模型
    url: /reference/compose-file/models/
    description: 了解模型顶级元素
  - title: 学习在 Docker Compose 中使用配置文件
    url: /reference/compose-file/profiles/
    description: 了解配置文件
  - title: Compose Build 规范
    url: /reference/compose-file/build/
    description: 了解 Compose Build 规范
  - title: Compose 部署规范
    url: /reference/compose-file/deploy/
    description: 了解 Compose 部署规范
  - title: Compose 开发规范
    url: /reference/compose-file/develop/
    description: 了解 Compose 开发规范
  - title: 旧版本
    url: /reference/compose-file/legacy-versions/
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


