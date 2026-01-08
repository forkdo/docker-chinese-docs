# cagent





  
  
  
  


  <div
    class="not-prose summary-bar"
  >
    

    
      
      <div class="flex flex-wrap gap-1">
        <span class="font-bold">Availability:</span>
        <span>
          Experimental
          
            
          
            
          
            
              <span class="icon-svg"><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M172-120q-41.78 0-59.39-39T124-230l248-280v-270h-52q-12.75 0-21.37-8.68-8.63-8.67-8.63-21.5 0-12.82 8.63-21.32 8.62-8.5 21.37-8.5h320q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5h-52v270l248 280q29 32 11.39 71T788-120H172Z"/></svg></span>
            
          
            
          
            
          
        </span>
      </div>
    

    

    
  </div>



[cagent](https://github.com/docker/cagent) 是一个开源工具，用于构建协作工作的专业化 AI 代理团队。与使用一个通用模型进行提示不同，你可以定义具有特定角色和指令的代理，它们协作解决问题。你可以使用任何 LLM 提供商从终端运行这些代理团队。

## 为什么使用代理团队

一个代理处理复杂工作意味着持续的上下文切换。将工作分配给专注的代理——每个代理处理其最擅长的部分。cagent 负责管理协调。

以下是一个调试问题的双代理团队示例：

```yaml
agents:
  root:
    model: openai/gpt-5-mini # Change to the model that you want to use
    description: Bug investigator
    instruction: |
      Analyze error messages, stack traces, and code to find bug root causes.
      Explain what's wrong and why it's happening.
      Delegate fix implementation to the fixer agent.
    sub_agents: [fixer]
    toolsets:
      - type: filesystem
      - type: mcp
        ref: docker:duckduckgo

  fixer:
    model: anthropic/claude-sonnet-4-5 # Change to the model that you want to use
    description: Fix implementer
    instruction: |
      Write fixes for bugs diagnosed by the investigator.
      Make minimal, targeted changes and add tests to prevent regression.
    toolsets:
      - type: filesystem
      - type: shell
```

根代理负责调查并解释问题。当它理解问题后，会将任务移交给 `fixer` 代理进行实现。每个代理都专注于其专业领域。

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

尝试 bug 分析团队：

1. 设置你要使用的模型提供商的 API 密钥：

   ```console
   $ export ANTHROPIC_API_KEY=<your_key>  # For Claude models
   $ export OPENAI_API_KEY=<your_key>     # For OpenAI models
   $ export GOOGLE_API_KEY=<your_key>     # For Gemini models
   ```

2. 将 [示例配置](#why-agent-teams) 保存为 `debugger.yaml`。

3. 运行你的代理团队：

   ```console
   $ cagent run debugger.yaml
   ```

你会看到一个提示，可以在其中描述 bug 或粘贴错误消息。调查代理会分析问题，然后将任务移交给修复代理进行实现。

## 工作原理

你与 _根代理_ 交互，它可以将工作委托给你定义的子代理。每个代理：

- 使用自己的模型和参数
- 拥有自己的上下文（代理之间不共享知识）
- 可以访问内置工具，如待办事项列表、内存和任务委托
- 可以通过 [MCP
  服务器](/manuals/ai/mcp-catalog-and-toolkit/mcp-gateway.md) 使用外部工具

根代理将任务委托给 `sub_agents` 下列出的代理。子代理可以有自己的子代理，以实现更深层次的层次结构。

## 配置选项

代理配置是 YAML 文件。基本结构如下：

```yaml
agents:
  root:
    model: claude-sonnet-4-0
    description: Brief role summary
    instruction: |
      Detailed instructions for this agent...
    sub_agents: [helper]

  helper:
    model: gpt-5-mini
    description: Specialist agent role
    instruction: |
      Instructions for the helper agent...
```

你还可以配置模型设置（如上下文限制）、工具（包括 MCP 服务器）等。详见 [配置
参考](./reference/config.md)
的完整详细信息。

## 分享代理团队

代理配置被打包为 OCI 工件。像推送和拉取容器镜像一样推送和拉取它们：

```console
$ cagent push ./debugger.yaml myusername/debugger
$ cagent pull myusername/debugger
```

使用 Docker Hub 或任何 OCI 兼容注册表。推送时如果仓库不存在会自动创建。

## 后续步骤

- 跟随 [教程](./tutorial.md) 构建你的第一个编码代理
- 学习构建高效代理的 [最佳实践](./best-practices.md)
- 将 cagent 与你的 [编辑器](./integrations/acp.md) 集成，或在 MCP 客户端中将代理用作
  [工具](./integrations/mcp.md)
- 浏览 [cagent
  仓库](https://github.com/docker/cagent/tree/main/examples) 中的示例代理配置
- 使用 `cagent new` 生成 AI 代理团队 <!-- TODO: link to some page
  where we explain this, probably a CLI reference? -->
- 通过 [Docker MCP
  Gateway](/manuals/ai/mcp-catalog-and-toolkit/mcp-gateway.md) 将代理连接到外部工具
- 阅读完整的 [配置
  参考](https://github.com/docker/cagent?tab=readme-ov-file#-configuration-reference)
  <!-- TODO: move to this site/repo -->

- [模型提供商](/ai/cagent/model-providers/)

- [构建编码代理](/ai/cagent/tutorial/)

- [最佳实践](/ai/cagent/best-practices/)

- [共享代理](/ai/cagent/sharing-agents/)

- [集成](/ai/cagent/integrations/)

- [RAG](/ai/cagent/rag/)

- [评估 (Evals)](/ai/cagent/evals/)

- [](/ai/cagent/local-models/)

