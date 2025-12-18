---
title: 源文件规范
description: 新建 .md 文件的格式要求
keywords: 源文件, 贡献, 风格指南
weight: 30
---

## 文件名

创建新内容的 .md 文件时，请确保：
- 文件名尽可能简短
- 尽量保持文件名只包含一个或两个单词
- 使用连字符分隔单词。例如：
  - `add-seats.md` 和 `remove-seats.md`
  - `multiplatform-images` 比 `multi-platform-images` 更好

## 前置元数据（Front matter）

Markdown 文件顶部的前置元数据部分以三个连字符开始和结束，包含 YAML 内容。
支持以下键值。标题、描述和关键词是必需的。

| 键名            | 必需 | 描述                                                                                                                                                                                                    |
|-----------------|------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| title           | 是   | 页面标题。会作为 `<h1>` 级别标题添加到 HTML 输出中。                                                                                                                                                             |
| description     | 是   | 描述页面内容的一句话。会添加到 HTML 元数据中。不会在页面上渲染。                                                                                                                                                 |
| keywords        | 是   | 逗号分隔的关键词列表。会添加到 HTML 元数据中。                                                                                                                                                                   |
| aliases         | 否   | YAML 格式的页面列表，这些页面应重定向到当前页面。构建时，列表中的每个页面都会创建为一个 HTML 存根文件，包含重定向到此页面的 302 重定向。                                                                          |
| notoc           | 否   | `true` 或 `false`。如果为 `true`，则不会为此页面的 HTML 输出生成页面内目录。默认为 `false`。适用于某些没有页面内标题的着陆页。                                                                                    |
| toc_min         | 否   | 如果 `notoc` 设置为 `true`，则忽略此参数。页面内目录包含的最小标题级别。默认为 `2`，显示 `<h2>` 标题为最小级别。                                                                                                   |
| toc_max         | 否   | 如果 `notoc` 设置为 `false`，则忽略此参数。页面内目录包含的最大标题级别。默认为 `3`，显示 `<h3>` 标题。设置为与 `toc_min` 相同的值，可仅显示 `toc_min` 级别的标题。                                                |
| sitemap         | 否   | 排除搜索引擎索引此页面。设置为 `false` 时，页面会从 `sitemap.xml` 中排除，并在页面中添加 `<meta name="robots" content="noindex"/>` 头部。                                                                      |
| sidebar.reverse | 否   | 此参数用于更改该部分页面的侧边栏排序顺序。通常出现在顶部的页面（按权重或标题）将改为出现在底部，反之亦然。                                                                                                        |
| sidebar.goto    | 否   | 设置此参数可更改侧边栏条目指向的 URL。参见 [无页面侧边栏条目](#pageless-sidebar-entries)。                                                                                                                       |
| sidebar.badge   | 否   | 设置此参数可为侧边栏条目添加徽章。此参数选项包含两个字段：`badge.text` 和 `badge.color`。                                                                                                                         |

以下是一个有效的（但人为构造的）页面元数据示例。前置元数据中元数据元素的顺序不重要。

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

页面正文（关键词除外）从前置元数据之后开始。

### 文本长度

将长行拆分（最好每行最多 80 个字符）可以使对小段文本提供反馈更容易。

## 无页面侧边栏条目

如果您想在侧边栏中添加条目，但希望链接指向其他地方，可以使用 `sidebar.goto` 参数。
这在与 `build.render` 设置为 `always` 结合使用时很有用，可创建一个指向其他页面的无页面侧边栏条目。

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