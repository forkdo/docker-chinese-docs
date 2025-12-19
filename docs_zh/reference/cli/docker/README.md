---
_build:
  list: never
  publishResources: false
  render: never
---

# 关于这些文件

此目录中的文件是存根文件，它们包含文件 `/_includes/cli.md`，该文件解析从 [`docker/cli`](https://github.com/docker/cli) 仓库生成的 YAML 文件。这些 YAML 文件会被解析成输出文件，例如 </reference/cli/docker/build/>。

## 输出如何生成

输出文件由两个来源组成：

- **描述** 和 **用法** 部分直接来自该仓库中的 CLI 源代码。

- **扩展描述** 和 **示例** 部分是从 [https://github.com/docker/cli/tree/master/docs/reference/commandline](https://github.com/docker/cli/tree/master/docs/reference/commandline)（用于 Docker CLI 命令）和 [https://github.com/docker/compose/tree/v2/docs/reference](https://github.com/docker/compose/tree/v2/docs/reference)（用于 Docker Compose 命令）中的文件提取到 YAML 中的。具体来说，会解析 `## Description` 和 `## Examples` 标题内的 Markdown。请向这些仓库提交文本更正。

## 更新 YAML 文件

生成 YAML 文件的过程仍在不断变化中。请咨询 @thaJeztah。请务必使用 `docker/cli` 的正确发布分支来生成 YAML 文件，例如 `19.03` 分支。

生成 YAML 文件后，用新生成的文件替换 [https://github.com/docker/docs/tree/main/_data/engine-cli](https://github.com/docker/docs/tree/main/_data/engine-cli) 中的 YAML 文件。然后提交拉取请求（pull request）。