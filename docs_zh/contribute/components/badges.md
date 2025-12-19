---
description: Docker 文档中使用的组件和格式示例
title: 徽章
toc_max: 3
---

### 示例

{{< badge color=blue text="蓝色徽章" >}}
{{< badge color=amber text="琥珀色徽章" >}}
{{< badge color=red text="红色徽章" >}}
{{< badge color=green text="绿色徽章" >}}
{{< badge color=violet text="紫色徽章" >}}
{{< badge color=gray text="灰色徽章" >}}

您还可以将徽章设置为链接。

[{{< badge color="blue" text="带链接的徽章" >}}](../_index.md)

### 使用指南

使用徽章来指示发布生命周期中不同阶段的新内容和产品内容：

- 紫色徽章：用于突出显示新的早期访问或实验性内容
- 蓝色徽章：用于突出显示 Beta 内容
- 绿色徽章：用于突出显示已正式发布 (GA) 的新内容或非产品相关的内容（例如指南/学习路径）
- 灰色徽章：用于突出显示已弃用的内容

最佳实践是在功能发布后最多使用此徽章 2 个月。

### 标记语法

行内徽章：

```go
{{</* badge color=amber text="琥珀色徽章" */>}}
[{{</* badge color="blue" text="带链接的徽章" */>}}](../overview.md)
```

Frontmatter 中的侧边栏徽章：

```yaml
---
title: 页面标题
params:
  sidebar:
    badge:
      color: gray
      text: 已弃用
---
```