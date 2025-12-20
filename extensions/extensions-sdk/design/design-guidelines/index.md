# Docker 扩展的设计指南

在 Docker，我们的目标是构建能够融入用户现有工作流程的工具，而不是要求他们采用新的工作流程。我们强烈建议您在创建扩展时遵循这些指南。我们将根据这些要求来审核并批准您在 Marketplace 的发布。

在创建扩展时，可以参考以下简单的检查清单：
- 是否易于上手？
- 是否易于使用？
- 需要帮助时是否易于获取？


## 与 Docker Desktop 保持一致的体验

使用 [Docker Material UI 主题](https://www.npmjs.com/package/@docker/docker-mui-theme) 和 [Docker 扩展风格指南](https://www.figma.com/file/U7pLWfEf6IQKUHLhdateBI/Docker-Design-Guidelines?node-id=1%3A28771)，确保您的扩展感觉像是 Docker Desktop 的一部分，为用户创造无缝的体验。

- 确保扩展同时支持浅色和深色主题。遵循 Docker 风格指南使用组件和样式，可确保您的扩展符合 [AA 级无障碍标准。](https://www.w3.org/WAI/WCAG2AA-Conformance)。

  ![浅色和深色模式](images/light_dark_mode.webp)

- 确保您的扩展图标在浅色和深色模式下都清晰可见。

  ![浅色和深色模式下的图标颜色](images/icon_colors.webp)

- 确保导航行为与 Docker Desktop 的其余部分保持一致。添加页眉以设置扩展的上下文。

  ![设置上下文的页眉](images/header.webp)

- 避免嵌入终端窗口。与 CLI 相比，Docker Desktop 的优势在于我们有机会向用户提供丰富的信息。请尽可能利用此界面。

  ![错误使用终端窗口](images/terminal_window_dont.webp)

  ![正确使用终端窗口](images/terminal_window_do.webp)


## 原生构建功能

- 为避免打断用户的工作流，请避免出现用户必须离开 Docker Desktop（例如导航到 CLI 或网页）才能执行某些功能的场景。相反，应构建 Docker Desktop 原生的功能。

  ![切换上下文的错误方式](images/switch_context_dont.webp)

  ![切换上下文的正确方式](images/switch_context_do.webp)


## 拆分复杂的用户流程

- 如果一个流程过于复杂或概念抽象，请将该流程分解为多个步骤，每个步骤包含一个简单的行动号召 (call-to-action)。这有助于引导新手用户使用您的扩展。

  ![复杂的流程](images/complicated_flows.webp)

- 当存在多个行动号召时，请确保使用主要按钮（填充按钮样式）和次要按钮（轮廓按钮样式）来传达每个操作的重要性。

  ![行动号召](images/cta.webp)


## 引导新用户

在创建扩展时，请确保扩展和您产品的首次用户能够理解其附加价值并轻松采用。确保在扩展内包含情境帮助。

- 确保所有必要的信息都已添加到扩展 Marketplace 以及扩展详情页。这应包括：
  - 扩展的截图。请注意，推荐的截图尺寸为 2400x1600 像素。
  - 详细的描述，涵盖扩展的用途、目标用户以及工作原理。
  - 指向必要资源（如文档）的链接。
- 如果您的扩展功能特别复杂，请在起始页添加演示或视频。这有助于首次用户快速上手。

  ![起始页](images/start_page.webp)


## 下一步是什么？

- 探索我们的[设计原则](design-principles.md)。
- 查看我们的[UI 样式指南](index.md)。
- 了解如何[发布您的扩展](../extensions/_index.md)。
