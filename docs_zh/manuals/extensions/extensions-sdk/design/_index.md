---
title: Docker 扩展 UI 样式概述
linkTitle: 设计与 UI 样式
description: Docker 扩展设计
keywords: Docker, 扩展, 设计
aliases:
 - /desktop/extensions-sdk/design/design-overview/
 - /desktop/extensions-sdk/design/overview/
 - /desktop/extensions-sdk/design/
weight: 60
---

我们的设计系统是一套不断演进的规范，旨在确保 Docker 产品之间视觉上的一致性，并满足 [AA 级无障碍标准](https://www.w3.org/WAI/WCAG2AA-Conformance)。我们已向扩展作者开放了部分设计系统，记录了基本样式（颜色、字体）和组件。参见：[Docker 扩展样式指南](https://www.figma.com/file/U7pLWfEf6IQKUHLhdateBI/Docker-Design-Guidelines?node-id=1%3A28771)。

我们要求扩展在一定程度上与 Docker Desktop 的整体 UI 保持一致，并保留未来进一步加强这一要求的权利。

要开始设计你的 UI，请遵循以下步骤。

## 第一步：选择你的框架

### 推荐：React + MUI，使用我们的主题

Docker Desktop 的 UI 使用 React 和 [MUI](https://mui.com/)（即 Material UI）编写。这是我们唯一官方支持的扩展开发框架，也是 `init` 命令自动为你配置的框架。使用它能为作者带来显著优势：

- 你可以使用我们的 [Material UI 主题](https://www.npmjs.com/package/@docker/docker-mui-theme) 自动复制 Docker Desktop 的外观和感觉。
- 未来，我们将发布专门针对这种组合的工具和组件（例如自定义 MUI 组件，或与 Docker 交互的 React Hooks）。

阅读我们的 [MUI 最佳实践](mui-best-practices.md) 指南，了解与 Docker Desktop 配合使用的面向未来的方法。

### 不推荐：使用其他框架

你可能更喜欢使用其他框架，也许是因为你或你的团队更熟悉它，或者因为你有想要复用的现有资源。这是可能的，但强烈不建议。这意味着：

- 你需要手动复制 Docker Desktop 的外观和感觉。这需要大量努力，如果你没有足够接近我们的主题，用户会觉得你的扩展很突兀，我们可能在审核过程中要求你进行修改。
- 你的维护负担会更重。每当 Docker Desktop 的主题发生变化（可能在任何版本中发生），你都需要手动更改你的扩展以匹配它。
- 如果你的扩展是开源的，故意避免通用约定会使社区更难为它贡献代码。

## 第二步：遵循以下建议

### 遵循我们的 MUI 最佳实践（如适用）

参见我们的 [MUI 最佳实践](mui-best-practices.md) 文章。

### 仅使用调色板中的颜色

除了少数例外（例如显示你的 Logo），你应该只使用我们调色板中的颜色。这些颜色可以在我们的 [样式指南文档](https://www.figma.com/file/U7pLWfEf6IQKUHLhdateBI/Docker-Design-Guidelines?node-id=1%3A28771) 中找到，也很快将通过我们的 MUI 主题和 CSS 变量提供。

### 在明暗模式中使用对应的颜色

我们的颜色经过精心选择，使得调色板中每种变体的对应颜色应具有相同的基本特征。在亮色模式中使用 `red-300` 的任何地方，在暗色模式中也应使用 `red-300`。

## 接下来是什么？

- 查看我们的 [MUI 最佳实践](mui-best-practices.md)。
- 了解如何 [发布你的扩展](../extensions/_index.md)。