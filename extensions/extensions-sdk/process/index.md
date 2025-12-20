# 构建和发布流程

本文档的结构与您创建扩展时需要采取的步骤相匹配。

创建 Docker 扩展主要有两个部分：

1. 构建基础
2. 发布扩展

> [!NOTE]
>
> 创建 Docker 扩展无需付费。[Docker Extension SDK](https://www.npmjs.com/package/@docker/extension-api-client) 根据 Apache 2.0 许可证授权，可免费使用。任何人都可以创建新扩展并自由分享，不受限制。
>
> 扩展的许可方式也没有任何限制，这由您在创建新扩展时自行决定。

## 第一部分：构建基础

构建过程包括：

- 安装最新版本的 Docker Desktop。
- 使用文件设置目录，包括扩展的源代码和所需的扩展特定文件。
- 创建 `Dockerfile` 以在 Docker Desktop 中构建、发布和运行您的扩展。
- 配置镜像文件系统根目录下必需的元数据文件。
- 构建并安装扩展。

如需更多灵感，请参阅 [samples 文件夹](https://github.com/docker/extensions-sdk/tree/main/samples) 中的其他示例。

> [!TIP]
>
> 在创建扩展时，请确保遵循 [设计](design/design-guidelines.md) 和 [UI 样式](design/_index.md) 指南，以确保视觉一致性并符合 [AA 级无障碍标准](https://www.w3.org/WAI/WCAG2AA-Conformance)。

## 第二部分：发布和分发您的扩展

Docker Desktop 在扩展市场 (Extensions Marketplace) 中显示已发布的扩展。扩展市场是一个精心策划的空间，开发者可以在其中发现扩展以改善他们的开发体验，并上传自己的扩展与世界分享。

如果您希望您的扩展在市场中发布，请阅读 [发布文档](extensions/publish.md)。



> 已经构建了一个扩展？
>
> 请通过 [反馈表单](https://survey.alchemer.com/s3/7184948/Publishers-Feedback-Form) 告诉我们您的使用体验。

## 下一步是什么？

如果您想开始创建 Docker 扩展，请参阅 [快速入门指南](quickstart.md)。

或者，开始阅读“第一部分：构建”部分，以获取有关扩展创建过程每个步骤的更深入信息。

关于整个构建过程的深入教程，我们推荐以下来自 DockerCon 2022 的视频演示。

<iframe width="560" height="315" src="https://www.youtube.com/embed/Yv7OG-EGJsg" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
