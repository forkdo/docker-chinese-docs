# 
build:
  list: never
  publishResources: false
  render: never---
build:
  list: never
  publishResources: false
  render: never---
# 关于这些文件

此目录中的文件是存根文件，其中包含了文件
`/_includes/cli.md`，该文件会解析从
[`docker/cli`](https://github.com/docker/cli) 仓库生成的 YAML 文件。这些 YAML 文件
会被解析成输出文件，例如
</reference/cli/docker/build/>。

## 输出是如何生成的

输出文件由两个来源组成：

- **描述** 和 **用法** 部分直接来自该仓库中的 CLI 源代码。

- **扩展描述** 和 **示例** 部分是从以下文件中的内容提取到 YAML 中的：对于 Docker CLI 命令，来自 [https://github.com/docker/cli/tree/master/docs/reference/commandline](https://github.com/docker/cli/tree/master/docs/reference/commandline)；对于 Docker Compose 命令，来自 [https://github.com/docker/compose/tree/v2/docs/reference](https://github.com/docker/compose/tree/v2/docs/reference)。
  具体来说，会解析 `## Description` 和 `## Examples`
  标题下的 Markdown 内容。如需更正文本，请向相应的仓库提交修改。

## 更新 YAML 文件

生成 YAML 文件的过程仍在变动中。请联系
@thaJeztah 确认。请务必使用正确的
`docker/cli` 发布分支（例如 `19.03` 分支）来生成 YAML 文件。

生成 YAML 文件后，将
[https://github.com/docker/docs/tree/main/_data/engine-cli](https://github.com/docker/docs/tree/main/_data/engine-cli)
中的 YAML 文件替换为新生成的文件，然后提交一个 pull request。
