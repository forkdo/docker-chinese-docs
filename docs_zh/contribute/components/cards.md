---
description: Docker 文档中使用的组件和格式示例
title: 卡片
toc_max: 3
grid:
- title: Docker Desktop
  description: Docker on your Desktop.
  icon: install_desktop
  link: /desktop/
- title: Docker Engine
  description: Vrrrrooooommm
  icon: developer_board
  link: /engine/
- title: Docker Build
  description: Clang bang
  icon: build
  link: /build/
- title: Docker Compose
  description: Figgy!
  icon: account_tree
  link: /compose/
- title: Docker Hub
  description: so much content, oh wow
  icon: hub
  link: /docker-hub/
---

可以使用 `card` 短代码在页面中添加卡片。
此短代码的参数如下：

| 参数        | 描述                                                                 |
| ----------- | -------------------------------------------------------------------- |
| title       | 卡片的标题                                                           |
| icon        | 卡片的图标 slug                                                      |
| image       | 使用自定义图像代替图标（与 icon 互斥）                                 |
| link        | （可选）单击卡片时的链接目标                                         |
| description | 描述文本，使用 Markdown 格式                                         |

> [!NOTE]
>
> 卡片的 Markdown 描述存在一个已知限制，
> 即它们不能包含指向其他 .md 文档的相对链接。
> 此类链接无法正确渲染。相反，请使用绝对链接指向您要链接的页面的 URL 路径。
>
> 例如，不要链接到 `../install/linux.md`，而是写：
> `/engine/install/linux/`。

## 示例

{{< card
  title="Get your Docker on"
  icon=favorite
  link=https://docs.docker.com/
  description="Build, share, and run your apps with Docker" >}}

## 标记

```go
{{</* card
  title="Get your Docker on"
  icon=favorite
  link=https://docs.docker.com/
  description="Build, share, and run your apps with Docker"
*/>}}
```

### 网格

还有一个内置的 `grid` 短代码，用于生成卡片网格。
在大屏幕上网格大小为 3x3，在中等屏幕上为 2x2，在小屏幕上为单列。

{{< grid >}}

`grid` 是一个与 `card` 分开的短代码，但它在底层实现中使用了相同的组件。
插入网格的标记有点不寻常。网格短代码不接受任何参数。
它只是让您指定要在页面的哪个位置显示网格。

```go
{{</* grid */>}}
```

网格的数据在页面的前言（front matter）中定义，位于 `grid` 键下，如下所示：

```yaml
# 页面的前言部分
title: some page
grid:
  - title: "Docker Engine"
    description: Vrrrrooooommm
    icon: "developer_board"
    link: "/engine/"
  - title: "Docker Build"
    description: Clang bang
    icon: "build"
    link: "/build/"
```