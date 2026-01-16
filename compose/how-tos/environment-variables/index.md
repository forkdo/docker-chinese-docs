---
title: Compose 中的环境变量
url: /compose/how-tos/environment-variables/
parent:
  title: Docker Compose
  url: /compose/
breadcrumbs:
  - title: 手册
    url: /manuals/
  - title: Docker Compose
    url: /compose/
  - title: Compose 中的环境变量
    url: /compose/how-tos/environment-variables/
children:
  - title: 在容器环境中设置环境变量
    url: /compose/how-tos/environment-variables/set-environment-variables/
    description: 如何使用 Compose 设置、使用和管理环境变量
  - title: Docker Compose 中的环境变量优先级
    url: /compose/how-tos/environment-variables/envvars-precedence/
    description: 说明 Compose 中环境变量解析方式的场景概览
  - title: 在 Docker Compose 中配置预定义环境变量
    url: /compose/how-tos/environment-variables/envvars/
    description: 预定义环境变量的配置方法
  - title: 在 Compose 文件中使用插值设置、使用和管理变量
    url: /compose/how-tos/environment-variables/variable-interpolation/
    description: 如何在 Compose 文件中使用插值设置、使用和管理变量
  - title: Docker Compose 中处理环境变量的最佳实践
    url: /compose/how-tos/environment-variables/best-practices/
    description: 解释在 Compose 中设置、使用和管理环境变量的最佳方式
---


Docker Compose 中的环境变量和插值（interpolation）帮助您创建可重用、灵活的配置。这使得 Docker 化的应用程序更易于在不同环境之间管理和部署。

> [!TIP]
>
> 在使用环境变量之前，请先通读所有信息，以全面了解 Docker Compose 中的环境变量。

本节涵盖：

- [如何在容器环境中设置环境变量](set-environment-variables.md)。
- [容器环境中环境变量的优先级如何工作](envvars-precedence.md)。
- [预定义的环境变量](envvars.md)。

此外，本节还涵盖：
- 如何使用[插值](variable-interpolation.md)在 Compose 文件中设置变量，以及它与容器环境的关系。
- 一些[最佳实践](best-practices.md)。
