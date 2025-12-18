---
title: cagent
description: cagent 让你可以构建、编排和共享协同工作的 AI 代理团队。
weight: 60
params:
  sidebar:
    group: Open source
    badge:
      color: violet
      text: Experimental
keywords: [ai, agent, cagent]
---

{{< summary-bar feature_name="cagent" >}}

[cagent](https://github.com/docker/cagent) 是一个开源工具，用于构建专业化的 AI 代理团队。你不需要反复提示一个通用模型，而是定义具有特定角色和指令的代理，它们协同工作来解决问题。你可以从终端使用任何 LLM 提供商来运行这些代理团队。

## 为什么使用代理团队

一个代理处理复杂工作意味着频繁的上下文切换。将工作分配给专注的代理——每个代理处理它最擅长的部分。cagent 负责管理协调。

以下是一个两代理团队，用于调试问题：

```yaml
agents:
  root:
    model: openai/gpt-5-mini # 更改为你要使用的模型
    description: Bug 调查员
    instruction: |
      分析错误消息、堆栈跟踪和代码以找到 bug 的根本原因。
      解释问题所在以及为什么会发生。
      将修复实现委托给 fixer 代理。
    sub_agents: [fixer]
    toolsets:
      - type: filesystem
      - type: mcp
        ref: docker:duckduckgo

  fixer:
    model: anthropic/claude-sonnet-4-5 # 更改为你要使用的模型
    description: 修复实现者
    instruction: |
      为调查员诊断的 bug 编写修复。
      进行最小化、有针对性的更改，并添加测试以防止回归。
    toolsets:
      - type: filesystem
      - type: shell
```

root 代理负责调查和解释问题。理解问题后，它将任务交接给 `fixer` 进行实现。每个代理都专注于其专业领域。

## 安装

cagent 包含在 Docker Desktop 4.49 及更高版本中。

对于 Docker Engine 用户或自定义安装：

- **Homebrew**: `brew install cagent`
- **Winget**: `winget install Docker.Cagent`
- **预编译二进制文件**: [GitHub
  releases](https://github.com/docker/cagent/releases)
- **从源码构建**: 参见 [cagent
  仓库](https://github.com/docker/cagent?tab=readme-ov-file#build-from-source)

## 快速开始

尝试 bug 分析器团队：

1. 为你想使用的模型提供商设置 API 密钥：

   ```console
   $ export ANTHROPIC_API_KEY=<your_key>  # 用于 Claude 模型
   $ export OPENAI_API_KEY=<your_key>     # 用于 OpenAI 模型
   $ export GOOGLE_API_KEY=<your_key>     # 用于 Gemini 模型
   ```

2. 将 [示例配置](#why-agent-teams) 保存为 `debugger.yaml`。

3. 运行你的代理团队：

   ```console
   $ cagent run debugger.yaml
   ```

你会看到一个提示，可以在其中描述 bug 或粘贴错误消息。调查员分析问题，然后将任务交接给 fixer 进行实现。

## 工作原理

你与 _root 代理_ 交互，它可以将工作委托给你定义的子代理。每个代理：

- 使用自己的模型和参数
- 拥有自己的上下文（代理之间不共享知识）
- 可以访问内置工具，如待办事项列表、内存和任务委托
- 可以通过 [MCP
  服务器](/manuals/ai/mcp-catalog-and-toolkit/mcp-gateway.md) 使用外部工具

root 代理将任务委托给 `sub_agents` 下列出的代理。子代理可以有自己的子代理，以实现更深层次的层次结构。

## 配置选项

代理配置是 YAML 文件。基本结构如下：

```yaml
agents:
  root:
    model: claude-sonnet-4-0
    description: 简要角色摘要
    instruction: |
      此代理的详细说明...
    sub_agents: [helper]

  helper:
    model: gpt-5-mini
    description: 专业代理角色
    instruction: |
      helper 代理的说明...
```

你还可以配置模型设置（如上下文限制）、工具（包括 MCP 服务器）等。详见 [配置
参考](./reference/config.md)
以获取完整详细信息。

## 共享代理团队

代理配置被打包为 OCI 工件。像推送和拉取容器镜像一样推送和拉取它们：

```console
$ cagent push ./debugger.yaml myusername/debugger
$ cagent pull myusername/debugger
```

使用 Docker Hub 或任何兼容 OCI 的注册表。推送时如果仓库不存在会自动创建。

## 接下来做什么

- 阅读 [教程](./tutorial.md) 构建你的第一个编码代理
- 学习构建高效代理的 [最佳实践](./best-practices.md)
- 将 cagent 与你的 [编辑器](./integrations/acp.md) 集成，或在 MCP 客户端中将代理用作
  [工具](./integrations/mcp.md)
- 浏览 [cagent
  仓库](https://github.com/docker/cagent/tree/main/examples) 中的示例代理配置
- 使用 `cagent new` 通过 AI 生成代理团队 <!-- TODO: 链接到解释此功能的页面，可能是 CLI 参考？ -->
- 通过 [Docker MCP
  Gateway](/manuals/ai/mcp-catalog-and-toolkit/mcp-gateway.md) 将代理连接到外部工具
- 阅读完整的 [配置
  参考](https://github.com/docker/cagent?tab=readme-ov-file#-configuration-reference)
  <!-- TODO: 移动到本网站/仓库 -->