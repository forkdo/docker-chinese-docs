---
title: MUI 最佳实践
description: 使用 MUI 以最大限度地兼容 Docker Desktop 的指南
keywords: Docker, extensions, mui, theme, theming, material-ui, material
aliases: 
 - /desktop/extensions-sdk/design/mui-best-practices/
---

本文假设您正在遵循我们的推荐做法，使用我们的 [Material UI 主题](https://www.npmjs.com/package/@docker/docker-mui-theme)。
遵循以下步骤可以最大限度地兼容 Docker Desktop，并减少您作为扩展作者所需的工作量。这些内容应被视为对 [UI 样式概览](index.md) 中非 MUI 特定指南的补充。

## 假设主题随时可能发生变化

请抵制使用精确的颜色、偏移量和字体大小来微调 UI 以使其看起来尽可能吸引人的诱惑。您今天所做的任何特殊调整都是相对于当前的 MUI 主题的，当主题发生变化时，这些调整可能会显得更糟糕。主题的任何部分都可能随时更改，包括但不限于：

-  字体或字体大小
-  边框粗细或样式
-  颜色：
   -  我们的调色板成员（例如 `red-100`）可能会更改其 RGB 值
   -  语义颜色（例如 `error`、`primary`、`textPrimary` 等）可能会更改为使用我们调色板中的不同成员
   -  背景颜色（例如页面或对话框的背景颜色）可能会更改
-  间距：
   -  基本间距单位的大小（通过 `theme.spacing` 暴露。例如，我们可能允许用户自定义 UI 的密度）
   -  段落或网格项之间的默认间距

构建 UI 的最佳方式是使其能够抵御未来的主题更改，具体方法如下：

-  尽可能少地覆盖默认样式。
-  使用语义排版。例如，使用具有适当 `variant` 的 `Typography` 或 `Link`，而不是直接使用排版 HTML 元素（`<a>`、`<p>`、`<h1>` 等）。
-  使用预设尺寸。例如，在按钮上使用 `size="small"`，或在图标上使用 `fontSize="small"`，而不是以像素为单位指定尺寸。
-  优先使用语义颜色。例如，使用 `error` 或 `primary` 而不是明确的颜色代码。
-  尽可能少写 CSS。改用语义标记。例如，如果您想要分隔文本段落，请在 `Typography` 实例上使用 `paragraph` 属性。如果您想要分隔其他内容，请使用具有默认间距的 `Stack` 或 `Grid`。
-  使用您在 Docker Desktop UI 中看到的视觉习惯用法，因为这是我们测试任何主题更改的主要依据。

## 自定义时，请集中管理

有时您可能需要一个我们设计系统中不存在的 UI 元素。如果是这样，我们建议您首先联系我们。我们可能已经在内部设计系统中有了相关内容，或者我们可能能够扩展我们的设计系统以适应您的用例。

如果您在联系我们后仍决定自行构建，请尝试以可重用的方式定义新的 UI。如果您将自定义 UI 定义在单一位置，将来我们的核心主题发生变化时，将更容易进行修改。您可以使用：

-  现有组件的新 `variant` - 请参阅 [MUI 文档](https://mui.com/material-ui/customization/theme-components/#creating-new-component-variants)
-  MUI 混入（在主题内定义的可重用样式规则的自由组合）
-  新的[可重用组件](https://mui.com/material-ui/customization/how-to-customize/#2-reusable-component)

上述某些选项需要您扩展我们的 MUI 主题。请参阅 MUI 文档中的[主题组合](https://mui.com/material-ui/customization/theming/#nesting-the-theme)。

## 下一步是什么？

- 查看我们的 [UI 样式指南](index.md)。
- 了解如何[发布您的扩展](../extensions/_index.md)。