---
title: 写作清单
description: 编写文档时的实用写作清单
keywords: checklist, documentation, style guide, contribute
weight: 60
---

使用此清单，以清晰、有帮助且与 Docker 文档其余部分保持一致的方式进行沟通。

##### 使用主动语态

主动语态更具体，能消除歧义。

在主动语态中，句子的主语（客户或系统）执行动作。

使用主动语态的句子更容易阅读。主动语态明确了谁做了什么、对谁做的。此外，主动语态使句子更直接、更简洁。

助动词如 is、was 或 would 可能表明你正在使用被动语态。如果在动词后加上 "by zombies" 这个短语，句子仍然成立，那么你就是在使用被动语态。

|正确| 错误|
|:--|:--|
|Increase productivity with Docker Desktop.| Productivity can be increased (by zombies) with Docker Desktop.|
|If you remove items from a grid, charts automatically refresh to display the change. | If items are removed (by zombies) from a grid, charts automatically refresh to display the change.|

##### 编写简洁明了、直入主题的句子

编写简短、简洁的句子。简练的句子阅读更快、更容易理解。

##### 使用小标题和项目符号列表来拆分页面

这有助于快速轻松地找到所需信息。

更多信息，请参阅 [格式](style/formatting.md#headings-and-subheadings) 页面，或参阅 [组件](components/lists.md) 页面查看示例。

##### 页面标题以动词开头

例如，'Install Docker Desktop'。

##### 检查 docs.docker.com 左侧目录中的标题是否与页面上显示的标题匹配

##### 检查链接和图片是否损坏

使用相对链接链接到 GitHub 仓库中的其他页面或图片。

更多信息，请参阅 [格式](style/formatting.md#links) 页面，或参阅 [组件](components/links.md) 页面查看示例。

##### 检查可能添加的任何重定向是否生效

有关如何添加重定向的信息，请参阅 [源文件约定](file-conventions.md#front-matter)。

##### 对内容中提到的任何 UI 元素使用粗体

##### 完成最终的拼写、标点和语法检查

有关我们风格指南的更深入信息，请探索 [语法](style/grammar.md) 或 [格式](style/formatting.md) 指南。