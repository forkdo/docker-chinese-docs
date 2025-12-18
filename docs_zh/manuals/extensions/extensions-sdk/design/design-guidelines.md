---
title: Docker 扩展设计指南
linkTitle: 设计指南
description: Docker 扩展设计
keywords: Docker, 扩展, 设计
aliases: 
 - /desktop/extensions-sdk/design/design-guidelines/
weight: 10
---

在 Docker，我们的目标是构建能够融入用户现有工作流程的工具，而不是要求他们采用新的工作流程。我们强烈建议您在创建扩展时遵循这些指南。我们将根据这些要求审核并批准您在 Marketplace 上的发布。

创建扩展时，请遵循以下简单清单：
- 是否易于上手？
- 是否易于使用？
- 需要帮助时是否易于获取？

## 与 Docker Desktop 保持一致的体验

使用 [Docker Material UI Theme](https://www.npmjs.com/package/@docker/docker-mui-theme) 和 [Docker Extensions Styleguide](https://www.figma.com/file/U7pLWfEf6IQKUHLhdateBI/Docker-Design-Guidelines?node-id=1%3A28771) 确保您的扩展看起来像是 Docker Desktop 的一部分，为用户提供无缝体验。

- 确保扩展同时支持亮色和暗色主题。按照 Docker 样式指南使用组件和样式，确保您的扩展符合 [AA 级无障碍标准](https://www.w3.org/WAI/WCAG2AA-Conformance)。

  ![亮色和暗色模式](images/light_dark_mode.webp)

- 确保您的扩展图标在亮色和暗色模式下都清晰可见。

  ![亮色和暗色模式下的图标颜色](images/icon_colors.webp)

- 确保导航行为与 Docker Desktop 的其余部分保持一致。添加标题以设置扩展的上下文。

  ![设置上下文的标题](images/header.webp)

- 避免嵌入终端窗口。Docker Desktop 相比 CLI 的优势在于，我们有机会为用户提供丰富的信息。尽可能充分利用此界面。

  ![错误使用终端窗口](images/terminal_window_dont.webp)

  ![正确使用终端窗口](images/terminal_window_do.webp)

## 原生构建功能

- 为避免打断用户流程，避免用户需要导航到 Docker Desktop 外部（例如 CLI 或网页）才能执行某些功能的场景。相反，构建适合 Docker Desktop 的原生功能。

  ![错误的切换上下文方式](images/switch_context_dont.webp)

  ![正确的切换上下文方式](images/switch_context_do.webp)

## 分解复杂用户流程

- 如果流程过于复杂或概念过于抽象，请将流程分解为多个步骤，每个步骤只包含一个简单的行动号召。这有助于新手用户快速上手您的扩展。

  ![复杂流程](images/complicated_flows.webp)

- 当存在多个行动号召时，确保使用主要按钮（实心按钮样式）和次要按钮（轮廓按钮样式）来传达每个操作的重要性。

  ![行动号召](images/cta.webp)

## 新用户引导

创建扩展时，确保首次使用扩展和您产品的用户能够理解其价值并轻松采用。确保在扩展中包含上下文帮助。

- 确保所有必要信息都添加到扩展的 Marketplace 以及扩展详情页面。应包括：
  - 扩展的截图。请注意，推荐的截图尺寸为 2400x1600 像素。
  - 详细描述，涵盖扩展的目的、适用人群以及工作原理。
  - 相关资源链接，例如文档。
- 如果您的扩展功能特别复杂，请在起始页面添加演示或视频。这有助于快速引导首次用户。

  ![起始页面](images/start_page.webp)

## 下一步？

- 探索我们的 [设计原则](design-principles.md)。
- 查看我们的 [UI 样式指南](index.md)。
- 了解如何 [发布您的扩展](../extensions/_index.md)。