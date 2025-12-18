---
title: Compose 中的环境变量
linkTitle: 使用环境变量
weight: 40
description: 解释如何在 Docker Compose 中设置、使用和管理环境变量。
keywords: compose, 编排, 环境, env 文件
aliases:
- /compose/environment-variables/
---

Docker Compose 中的环境变量和变量插值功能可帮助您创建可复用、灵活的配置。这使得容器化应用程序在不同环境中更易于管理和部署。

> [!TIP]
>
> 在使用环境变量之前，请先完整阅读所有信息，以便全面了解 Docker Compose 中的环境变量。

本节涵盖：

- [如何在容器环境中设置环境变量](set-environment-variables.md)。
- [容器环境中环境变量的优先级机制](envvars-precedence.md)。
- [预定义的环境变量](envvars.md)。

此外还包括：
- [插值](variable-interpolation.md) 如何用于在 Compose 文件中设置变量，以及它与容器环境的关系。
- 一些 [最佳实践](best-practices.md)。