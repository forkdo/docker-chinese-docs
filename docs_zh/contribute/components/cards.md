---
description: Docker 文档中使用的组件和格式示例
title: 卡片
toc_max: 3
grid:
- title: Docker Desktop
  description: 桌面上的 Docker。
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
  description: 内容超多，哇哦
  icon: hub
  link: /docker-hub/
---

可以使用 `card` 短代码在页面中添加卡片。  
此短代码的参数如下：

| 参数        | 描述                                                                 |
|-------------|----------------------------------------------------------------------|
| title       | 卡片的标题                                                           |
| icon        | 卡片的图标标识符                                                     |
| image       | 使用自定义图片替代图标（与 icon 互斥）                               |
| link        | （可选）点击卡片时跳转的链接目标                                     |
| description | 描述文本，支持 Markdown 格式                                         |

> [!NOTE]
>
> 卡片中的 Markdown 描述存在一个已知限制：  
> 不能包含指向其他 .md 文档的相对链接，这类链接将无法正确渲染。  
> 请改用目标页面的 URL 绝对路径链接。
>
> 例如，不要写成 `../install/linux.md`，而应写成：  
> `/engine/install/linux/`。

## 示例

{{< card
  title="开始使用 Docker"
  icon=favorite
  link=https://docs.docker.com/
  description="使用 Docker 构建、共享并运行您的应用" >}}

## 标记语法

```go
{{</* card
  title="开始使用 Docker"
  icon=favorite
  link=https://docs.docker.com/
  description="使用 Docker 构建、共享并运行您的应用"
*/>}}
```

### 网格布局

还提供了一个内置的 `grid` 短代码，用于生成卡片网格布局。  
在大屏幕上为 3x3 网格，中等屏幕为 2x2，小屏幕则为单列。

{{< grid >}}

`grid` 是与 `card` 独立的短代码，但底层实现的是同一组件。  
插入网格的标记语法稍显特殊：`grid` 短代码不接受任何参数，  
它的作用仅仅是定义网格在页面中的显示位置。

```go
{{</* grid */>}}
```

网格的数据在页面的 front matter 中通过 `grid` 键定义，格式如下：

```yaml
# 页面的 front matter 部分
title: 某个页面
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