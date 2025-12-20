# 源文件规范

## 文件名

为新内容创建新的 .md 文件时，请确保：
- 文件名尽可能简短
- 尽量将文件名控制在一个或两个单词
- 使用短横线分隔单词。例如：
  - `add-seats.md` 和 `remove-seats.md`。
  - `multiplatform-images` 优于 `multi-platform-images`。

## Front matter（元数据）

给定页面的 front matter 位于 Markdown 文件顶部，以三个连字符开始和结束。它包含 YAML 内容。支持以下键。其中 title、description 和 keywords 是必需的。

| Key             | Required | Description                                                                                                                                                                                                    |
|-----------------|----------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| title           | yes      | 页面标题。这会作为 `<h1>` 级别的标题添加到 HTML 输出中。                                                                                                                                                                                                     |
| description     | yes      | 描述页面内容的一句话。这会添加到 HTML 元数据中。它不会在页面上呈现。                                                                                                |
| keywords        | yes      | 以逗号分隔的关键词列表。这些会添加到 HTML 元数据中。                                                                                                                                      |
| aliases         | no       | 一个 YAML 列表，包含应重定向到当前页面的页面。在构建时，此处列出的每个页面都会创建为一个包含指向此页面的 302 重定向的 HTML 存根。                                        |
| notoc           | no       | `true` 或 `false`。如果为 `true`，则不会为此页面的 HTML 输出生成页面内目录。默认为 `false`。适用于一些没有页面内标题的登录页。                      |
| toc_min         | no       | 如果 `notoc` 设置为 `true`，则忽略。页面内目录中包含的最小标题级别。默认为 `2`，表示显示 `<h2>` 标题作为最小级别。                                                           |
| toc_max         | no       | 如果 `notoc` 设置为 `false`，则忽略。页面内目录中包含的最大标题级别。默认为 `3`，表示显示 `<h3>` 标题。设置为与 `toc_min` 相同，则仅显示 `toc_min` 级别的标题。  |
| sitemap         | no       | 从搜索引擎索引中排除该页面。当设置为 `false` 时，该页面将从 `sitemap.xml` 中排除，并且会在页面中添加 `<meta name="robots" content="noindex"/>` 标头。                   |
| sidebar.reverse | no       | 此参数用于部分页面，更改该部分中页面的排序顺序。通常根据权重或标题出现在顶部的页面，将出现在底部附近，反之亦然。 |
| sidebar.goto    | no       | 设置此项以更改侧边栏应指向此条目的 URL。参见[无页面侧边栏条目](#pageless-sidebar-entries)。                                                                         |
| sidebar.badge   | no       | 设置此项以为此页面的侧边栏条目添加徽章。此参数选项包含两个字段：`badge.text` 和 `badge.color`。                                                                          |

以下是一个有效（但经过构造）的页面元数据示例。front matter 中元数据元素的顺序无关紧要。

```text
---
description: 在 Ubuntu 上安装 Docker Engine 的说明
keywords: requirements, apt, installation, ubuntu, install, uninstall, upgrade, update
title: 在 Ubuntu 上安装 Docker Engine
aliases:
- /ee/docker-ee/ubuntu/
- /engine/installation/linux/docker-ce/ubuntu/
- /engine/installation/linux/docker-ee/ubuntu/
- /engine/installation/linux/ubuntu/
- /engine/installation/linux/ubuntulinux/
- /engine/installation/ubuntulinux/
- /install/linux/docker-ce/ubuntu/
- /install/linux/docker-ee/ubuntu/
- /install/linux/ubuntu/
- /installation/ubuntulinux/
toc_max: 4
---
```

## 正文

页面的正文（关键词除外）在 front matter 之后开始。

### 文本长度

拆分长行（最好最多 80 个字符）可以更容易地对小块文本提供反馈。

## 无页面侧边栏条目

如果要向侧边栏添加条目，但希望链接指向其他地方，可以使用 `sidebar.goto` 参数。
这与 `build.render` 设置为 `always` 结合使用时非常有用，后者会在侧边栏中创建一个指向其他页面的无页面条目。

```text
---
title: 虚拟侧边栏链接
build:
  render: never
sidebar:
  goto: /some/other/page/
weight: 30
---
```
