---
linkTitle: ACP
title: ACP 集成
description: 配置你的编辑器或 IDE 以使用 cagent 代理作为编程助手
keywords: [cagent, acp, editor, ide, neovim, zed, integration]
weight: 40
---

在编辑器中直接运行 cagent 代理，使用 Agent Client Protocol (ACP)。
你的代理将获得编辑器文件系统上下文的访问权限，可以在你工作时读取和修改文件。
编辑器处理文件操作，而 cagent 提供 AI 能力。

本指南展示如何配置 Neovim 或 Zed 来运行 cagent 代理。如果你想要将 cagent 代理作为工具暴露给 MCP 客户端（如 Claude Desktop 或 Claude Code），请参阅 [MCP 集成](./mcp.md)。

## 工作原理

当你使用 ACP 运行 cagent 时，它会成为你编辑器环境的一部分。你选择代码、高亮函数或引用文件时，代理能看到你所看到的内容。无需复制文件路径或切换到终端。

询问“解释这个函数”时，代理会读取你正在查看的文件。要求它“添加错误处理”时，它会直接在你的编辑器中编辑代码。代理使用编辑器对项目的视图，而不是直接访问外部文件系统。

与在终端中运行 cagent 的区别：文件操作通过编辑器进行，而不是代理直接访问你的文件系统。当代理需要读取或写入文件时，它会向你的编辑器请求。这确保了代理对代码的视图与你的视图保持同步——相同的当前工作目录、相同的文件、相同的状态。

## 前置条件

在配置编辑器之前，你需要：

- **已安装 cagent** - 参阅 [安装指南](../_index.md#installation)
- **代理配置** - 定义代理的 YAML 文件。参阅 [教程](../tutorial.md) 或 [示例配置](https://github.com/docker/cagent/tree/main/examples)
- **支持 ACP 的编辑器** - Neovim、Intellij、Zed 等

你的代理将使用 shell 环境中的模型提供商 API 密钥（`ANTHROPIC_API_KEY`、`OPENAI_API_KEY` 等）。在启动编辑器之前确保这些密钥已设置。

## 编辑器配置

### Zed

Zed 内置了 ACP 支持。

1. 在 `settings.json` 中将 cagent 添加到你的代理服务器：

   ```json
   {
     "agent_servers": {
       "my-cagent-team": {
         "command": "cagent",
         "args": ["acp", "agent.yml"]
       }
     }
   }
   ```

   替换：
   - `my-cagent-team` 为你想为代理使用的名称
   - `agent.yml` 为你的代理配置文件路径

   如果你有多个需要分别运行的代理文件，可以在 `agent_servers` 下创建多个条目，每个代理一个。

2. 启动一个新的外部代理线程。在下拉列表中选择你的代理。

   ![Zed 中使用 cagent 的新外部线程](../images/cagent-acp-zed.avif)

### Neovim

使用 [CodeCompanion](https://github.com/olimorris/codecompanion.nvim) 插件，它通过内置适配器原生支持 cagent：

1. 通过你的插件管理器 [安装 CodeCompanion](https://codecompanion.olimorris.dev/installation)。
2. 在你的 CodeCompanion 配置中扩展 `cagent` 适配器：

   ```lua
   require("codecompanion").setup({
     adapters = {
       acp = {
         cagent = function()
           return require("codecompanion.adapters").extend("cagent", {
             commands = {
               default = {
                 "cagent",
                 "acp",
                 "agent.yml",
               },
             },
           })
         end,
       },
     },
   })
   ```

   将 `agent.yml` 替换为你的代理配置文件路径。如果你有多个需要分别运行的代理文件，可以为每个代理创建多个命令。

3. 重启 Neovim 并启动 CodeCompanion：

   ```plaintext
   :CodeCompanion
   ```

4. 切换到 cagent 适配器（默认在 CodeCompanion 缓冲区中使用键映射 `ga`）。

参阅 [CodeCompanion ACP 文档](https://codecompanion.olimorris.dev/usage/acp-protocol) 了解 CodeCompanion 中 ACP 支持的更多信息。注意终端操作不受支持，因此通过 CodeCompanion 无法使用 [工具集](../reference/toolsets.md)（如 `shell` 或 `script_shell`）。

## 代理引用

你可以将代理配置指定为本地文件路径或 OCI 注册表引用：

```console
# 本地文件路径
$ cagent acp ./agent.yml

# OCI 注册表引用
$ cagent acp agentcatalog/pirate
$ cagent acp dockereng/myagent:v1.0.0
```

在编辑器配置中使用相同的语法：

```json
{
  "agent_servers": {
    "myagent": {
      "command": "cagent",
      "args": ["acp", "agentcatalog/pirate"]
    }
  }
}
```

注册表引用支持团队共享、版本管理和不依赖本地文件路径的简洁配置。详情参阅 [共享代理](../sharing-agents.md) 了解使用 OCI 注册表的信息。

## 测试你的设置

验证你的配置是否正常工作：

1. 使用编辑器配置的方法启动 cagent ACP 服务器
2. 通过编辑器界面发送测试提示
3. 检查代理是否响应
4. 要求代理读取文件以验证文件系统操作是否正常工作

如果代理启动但无法访问文件或执行其他操作，请检查：

- 编辑器中的工作目录是否正确设置为项目根目录
- 代理配置文件路径是绝对路径或相对于工作目录的相对路径
- 你的编辑器或插件是否正确实现了 ACP 协议功能

## 下一步

- 查看 [配置参考](../reference/config.md) 了解高级代理设置
- 探索 [工具集参考](../reference/toolsets.md) 了解可用工具
- 为你的代理添加 [用于代码库搜索的 RAG](../rag.md)
- 查看 [CLI 参考](../reference/cli.md) 了解所有 `cagent acp` 选项
- 浏览 [示例配置](https://github.com/docker/cagent/tree/main/examples) 获取灵感