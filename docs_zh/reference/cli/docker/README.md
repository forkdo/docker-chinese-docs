---
_build:
  list: never
  publishResources: false
  render: never
---

# 关于这些文件

此目录中的文件是存根文件，它们包含文件
`/_includes/cli.md`，该文件解析从
[`docker/cli`](https://github.com/docker/cli) 仓库生成的 YAML 文件。YAML 文件
被解析为输出文件，如
</reference/cli/docker/build/>。

## 输出文件的生成方式

输出文件由两个来源组成：

- **描述**和**用法**部分直接来自
  该仓库中的 CLI 源代码。

- **扩展描述**和**示例**部分从 [https://github.com/docker/cli/tree/master/docs/reference/commandline](https://github.com/docker/cli/tree/master/docs/reference/commandline) 中的文件（Docker CLI 命令）和 [https://github.com/docker/compose/tree/v2/docs/reference](https://github.com/docker/compose/tree/v2/docs/reference) 中的文件（Docker Compose 命令）提取到 YAML 中。
  具体来说，解析的是 `## Description` 和 `## Examples` 标题下的 Markdown。请向这些仓库提交文本更正。

## 更新 YAML 文件

生成 YAML 文件的流程仍在变动中。请与
@thaJeztah 确认。务必使用正确的
`docker/cli` 发布分支（例如 `19.03` 分支）生成 YAML 文件。

生成 YAML 文件后，用新生成的文件替换
[https://github.com/docker/docs/tree/main/_data/engine-cli](https://github.com/docker/docs/tree/main/_data/engine-cli)
中的 YAML 文件。提交拉取请求。