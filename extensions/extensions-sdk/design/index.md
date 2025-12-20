# Docker 扩展的 UI 样式概览

我们的设计系统是一套持续演进的设计规范，旨在确保 Docker 系列产品间的视觉一致性，并满足 [AA 级无障碍标准](https://www.w3.org/WAI/WCAG2AA-Conformance)。我们已向扩展开发者开放了其中部分内容，包括基础样式（颜色、排版）和组件文档。请参阅：[Docker 扩展样式指南](https://www.figma.com/file/U7pLWfEf6IQKUHLhdateBI/Docker-Design-Guidelines?node-id=1%3A28771)。

我们要求扩展程序在一定程度上与 Docker Desktop 的整体 UI 保持一致，并保留在未来进一步提高此要求的权利。

要开始构建您的 UI，请按照以下步骤操作。

## 第一步：选择您的框架

### 推荐方案：React + MUI，使用我们的主题

Docker Desktop 的 UI 使用 React 和 [MUI](https://mui.com/)（基于 Material UI）编写。这是构建扩展程序唯一官方支持的框架，也是 `init` 命令自动为您配置的框架。使用该框架可为开发者带来显著优势：

- 您可以使用我们的 [Material UI 主题](https://www.npmjs.com/package/@docker/docker-mui-theme) 自动复现 Docker Desktop 的外观和风格。
- 未来，我们将发布专门针对此组合的工具和组件（例如自定义 MUI 组件，或用于与 Docker 交互的 React 钩子）。

阅读我们的 [MUI 最佳实践](mui-best-practices.md) 指南，了解面向未来的 MUI 使用方法。

### 不推荐方案：其他框架

您可能更倾向于使用其他框架，也许是因为您或您的团队更熟悉它，或者您希望复用现有资源。虽然这是可行的，但我们强烈不建议这样做。这意味着：

- 您需要手动复现 Docker Desktop 的外观和风格。这需要大量工作，如果您与我们的主题匹配不够紧密，用户会觉得您的扩展程序突兀，我们可能会在审核过程中要求您进行修改。
- 您将承担更高的维护负担。每当 Docker Desktop 的主题发生变化时（可能发生在任何版本中），您都需要手动修改扩展程序以匹配它。
- 如果您的扩展程序是开源的，刻意避免通用约定将使社区更难为其做出贡献。

## 第二步：遵循以下建议

### 遵循我们的 MUI 最佳实践（如适用）

请参阅我们的 [MUI 最佳实践](mui-best-practices.md) 文章。

### 仅使用我们调色板中的颜色

除少数例外情况（例如展示您的徽标），您应仅使用我们调色板中的颜色。这些颜色可在我们的 [样式指南文档](https://www.figma.com/file/U7pLWfEf6IQKUHLhdateBI/Docker-Design-Guidelines?node-id=1%3A28771) 中找到，不久后也将通过我们的 MUI 主题和 CSS 变量提供。

### 在浅色/深色模式下使用对应的颜色

我们的颜色选择确保调色板的每个变体中，对应颜色应具有相同的基本特征。在浅色模式下使用 `red-300` 的任何地方，在深色模式下也应使用 `red-300`。

## 接下来做什么？

- 查看我们的 [MUI 最佳实践](mui-best-practices.md)。
- 了解如何 [发布您的扩展程序](../extensions/_index.md)。

- [Docker 扩展的设计指南](https://docs.docker.com/extensions/extensions-sdk/design/design-guidelines/)

- [Docker 设计原则](https://docs.docker.com/extensions/extensions-sdk/design/design-principles/)

- [MUI 最佳实践](https://docs.docker.com/extensions/extensions-sdk/design/mui-best-practices/)

