---
description: Docker 文档中使用的组件和格式化示例
title: 徽章
toc_max: 3
---

### 示例

{{< badge color=blue text="blue badge" >}}
{{< badge color=amber text="amber badge" >}}
{{< badge color=red text="red badge" >}}
{{< badge color=green text="green badge" >}}
{{< badge color=violet text="violet badge" >}}
{{< badge color=gray text="gray badge" >}}

你也可以让徽章成为一个链接。

[{{< badge color="blue" text="badge with a link" >}}](../_index.md)

### 使用指南

使用徽章来标示新内容以及处于不同发布生命周期阶段的产品内容：

- 使用紫色徽章来标示新的早期访问或实验性内容
- 使用蓝色徽章来标示 Beta 版内容
- 使用绿色徽章来标示正式发布（GA）或非产品相关的内容，例如指南/学习路径
- 使用灰色徽章来标示已弃用的内容

最佳实践是，对于功能发布后的内容，此徽章的使用时间不应超过 2 个月。

### 标记语法

内联徽章：

```go
{{</* badge color=amber text="amber badge" */>}}
[{{</* badge color="blue" text="badge with a link" */>}}](../overview.md)
```

侧边栏徽章（在 frontmatter 中）：

```yaml
---
title: Page title
params:
  sidebar:
    badge:
      color: gray
      text: Deprecated
---
```