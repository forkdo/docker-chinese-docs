---
title: MUI 最佳实践
description: 使用 MUI 以最大化与 Docker Desktop 兼容性的指导原则
keywords: Docker, extensions, mui, theme, theming, material-ui, material
aliases: 
 - /desktop/extensions-sdk/design/mui-best-practices/
---

本文假设你正在遵循我们的推荐实践，使用我们的 [Material UI 主题](https://www.npmjs.com/package/@docker/docker-mui-theme)。
遵循以下步骤可以最大化与 Docker Desktop 的兼容性，并减少你作为扩展作者所需的工作量。这些实践应被视为对 [UI 样式概述](index.md) 中非 MUI 特定指南的补充。

## 假设主题可能随时变化

请避免通过精确的颜色、偏移和字体大小来微调你的 UI，以使其看起来尽可能美观。你今天所做的任何特殊调整都是相对于当前 MUI 主题的，当主题改变时可能会显得更糟。主题的任何部分都可能在没有警告的情况下发生变化，包括但不限于：

-  字体或字体大小
-  边框粗细或样式
-  颜色：
   -  我们的调色板成员（例如 `red-100`）可能改变其 RGB 值
   -  语义颜色（例如 `error`、`primary`、`textPrimary` 等）可能被更改为使用我们调色板中的不同成员
   -  背景颜色（例如页面或对话框的背景色）可能改变
-  间距：
   -  基础间距单位的大小（通过 `theme.spacing` 暴露）。例如，我们可能允许用户自定义 UI 的密度
   -  段落或网格项之间的默认间距

构建 UI 以使其能够抵御未来主题变化的最佳方式是：

-  尽可能少地覆盖默认样式。
-  使用语义化排版。例如，使用带有适当 `variant` 的 `Typography` 或 `Link`，而不是直接使用排版 HTML 元素（`<a>`、`<p>`、`<h1>` 等）。
-  使用预定义的尺寸。例如，在按钮上使用 `size="small"`，或在图标上使用 `fontSize="small"`，而不是以像素为单位指定尺寸。
-  优先使用语义化颜色。例如，使用 `error` 或 `primary` 而不是显式的颜色代码。
-  尽量减少 CSS 的编写。改为编写语义化标记。例如，如果你想要分隔文本段落，请在你的 `Typography` 实例上使用 `paragraph` 属性。如果你想要分隔其他内容，请使用带有默认间距的 `Stack` 或 `Grid`。
-  使用你在 Docker Desktop UI 中见过的视觉惯用法，因为这些是我们测试任何主题变化时主要考虑的内容。

## 自定义时，请集中化处理

有时你可能需要一个在我们的设计系统中不存在的 UI 组件。如果是这样，我们建议你首先与我们联系。我们可能已经在内部设计系统中有类似的东西，或者我们可能能够扩展我们的设计系统以适应你的用例。

如果你在联系我们后仍决定自行构建，请尝试以可重用的方式定义新 UI。如果你将自定义 UI 定义在一个地方，那么将来如果我们的核心主题发生变化，修改起来会更容易。你可以使用：

-  现有组件的新 `variant` — 参见 [MUI 文档](https://mui.com/material-ui/customization/theme-components/#creating-new-component-variants)
-  MUI mixin（在主题内定义的可重用样式规则的自由组合）
-  新的 [可重用组件](https://mui.com/material-ui/customization/how-to-customize/#2-reusable-component)

上述某些选项需要你扩展我们的 MUI 主题。请参阅 MUI 文档中的 [主题组合](https://mui.com/material-ui/customization/theming/#nesting-the-theme)。

## 接下来是什么？

- 查看我们的 [UI 样式指南](index.md)。
- 了解如何 [发布你的扩展](../extensions/_index.md)。