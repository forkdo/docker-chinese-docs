---
description: 了解创建扩展的过程。
title: 构建和发布流程
keyword: Docker Extensions, sdk, build, create, publish
aliases:
 - /desktop/extensions-sdk/process/
weight: 10
---

本文档的结构与您创建扩展时需要遵循的步骤相对应。

创建 Docker 扩展主要包含两个部分：

1. 构建基础
2. 发布扩展

> [!NOTE]
>
> 您无需付费即可创建 Docker 扩展。[Docker Extension SDK](https://www.npmjs.com/package/@docker/extension-api-client) 采用 Apache 2.0 许可证，可免费使用。任何人都可以创建新扩展并分享，无任何限制。
> 
> 扩展应如何许可也没有限制，这由您在创建新扩展时自行决定。

## 第一部分：构建基础

构建过程包括：

- 安装最新版本的 Docker Desktop。
- 设置包含文件的目录，包括扩展的源代码和扩展特定的必需文件。
- 创建 `Dockerfile` 以构建、发布并在 Docker Desktop 中运行您的扩展。
- 配置元数据文件，该文件需位于镜像文件系统的根目录。
- 构建并安装扩展。

如需更多灵感，请参阅 [samples 文件夹](https://github.com/docker/extensions-sdk/tree/main/samples) 中的其他示例。

> [!TIP]
>
> 在创建扩展期间，请确保遵循 [设计](design/design-guidelines.md) 和 [UI 样式](design/_index.md) 指南，以确保视觉一致性并符合 [AA 级无障碍标准](https://www.w3.org/WAI/WCAG2AA-Conformance)。

## 第二部分：发布和分发您的扩展

Docker Desktop 在扩展市场中显示已发布的扩展。扩展市场是一个经过策划的空间，开发者可以在此发现扩展以改善开发体验，也可以上传自己的扩展与全世界分享。

如果您希望扩展发布到市场中，请阅读 [发布文档](extensions/publish.md)。

{{% include "extensions-form.md" %}}

## 下一步是什么？

如果您想快速开始创建 Docker 扩展，请参阅 [快速入门指南](quickstart.md)。

或者，阅读“第一部分：构建”部分，获取扩展创建过程中每个步骤的更详细信息。

如需完整的构建流程深度教程，我们推荐以下来自 DockerCon 2022 的视频演示。

<iframe width="560" height="315" src="https://www.youtube.com/embed/Yv7OG-EGJsg" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>