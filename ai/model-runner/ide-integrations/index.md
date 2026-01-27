# IDE 与工具集成


Docker Model Runner (DMR) 可以作为流行的 AI 编程助手和开发工具的本地后端。本指南介绍了如何配置常用工具以使用在 DMR 中运行的模型。

## 前提条件

在配置任何工具之前：

1. 在 Docker Desktop 或 Docker Engine 中[启用 Docker Model Runner](get-started.md#enable-docker-model-runner)。
2. 启用 TCP 主机访问：
   - Docker Desktop：在 Settings > AI 中启用 **host-side TCP support**，或运行：
     ```console
     $ docker desktop enable model-runner --tcp 12434
     ```
   - Docker Engine：TCP 默认在端口 12434 上启用。
3. 拉取模型：
   ```console
   $ docker model pull ai/qwen2.5-coder
   ```

## Cline (VS Code)

[Cline](https://github.com/cline/cline) 是一款用于 VS Code 的 AI 编程助手。

### 配置

1. 打开 VS Code 并转到 Cline 扩展设置。
2. 选择 **OpenAI Compatible** 作为 API 提供商。
3. 配置以下设置：

| 设置 | 值 |
|---------|-------|
| Base URL | `http://localhost:12434/engines/v1` |
| API Key | `not-needed`（或任何占位符内容） |
| Model ID | `ai/qwen2.5-coder`（或您偏好的模型） |

> [!IMPORTANT]
> 基础 URL 必须在末尾包含 `/engines/v1`。不要包含结尾斜杠。

### Cline 故障排除

如果 Cline 连接失败：

1. 验证 DMR 是否正在运行：
   ```console
   $ docker model status
   ```

2. 直接测试端点：
   ```console
   $ curl http://localhost:12434/engines/v1/models
   ```

3. 如果运行的是基于 Web 的版本，请检查 CORS 是否已配置：
   - 在 Docker Desktop Settings > AI 中，将您的源（origin）添加到 **CORS Allowed Origins**。

## Continue (VS Code / JetBrains)

[Continue](https://continue.dev) 是一款开源 AI 代码助手，适用于 VS Code 和 JetBrains IDE。

### 配置

编辑您的 Continue 配置文件 (`~/.continue/config.json`)：

```json
{
  "models": [
    {
      "title": "Docker Model Runner",
      "provider": "openai",
      "model": "ai/qwen2.5-coder",
      "apiBase": "http://localhost:12434/engines/v1",
      "apiKey": "not-needed"
    }
  ]
}
```

### 使用 Ollama 提供商

Continue 还支持 Ollama 提供商，它可以与 DMR 配合使用：

```json
{
  "models": [
    {
      "title": "Docker Model Runner (Ollama)",
      "provider": "ollama",
      "model": "ai/qwen2.5-coder",
      "apiBase": "http://localhost:12434"
    }
  ]
}
```

## Cursor

[Cursor](https://cursor.sh) 是一款 AI 驱动的代码编辑器。

### 配置

1. 打开 Cursor 设置 (Cmd/Ctrl + ,)。
2. 导航到 **Models** > **OpenAI API Key**。
3. 配置：

   | 设置 | 值 |
   |---------|-------|
   | OpenAI API Key | `not-needed` |
   | Override OpenAI Base URL | `http://localhost:12434/engines/v1` |

4. 在模型下拉菜单中，输入您的模型名称：`ai/qwen2.5-coder`

> [!NOTE]
> 某些 Cursor 功能可能需要具有特定能力（例如函数调用）的模型。使用 `ai/qwen2.5-coder` 或 `ai/llama3.2` 等能力较强的模型以获得最佳效果。

## Zed

[Zed](https://zed.dev) 是一款具有 AI 功能的高性能代码编辑器。

### 配置

编辑您的 Zed 设置 (`~/.config/zed/settings.json`)：

```json
{
  "language_models": {
    "openai": {
      "api_url": "http://localhost:12434/engines/v1",
      "available_models": [
        {
          "name": "ai/qwen2.5-coder",
          "display_name": "Qwen 2.5 Coder (DMR)",
          "max_tokens": 8192
        }
      ]
    }
  }
}
```

## Open WebUI

[Open WebUI](https://github.com/open-webui/open-webui) 为本地模型提供类似 ChatGPT 的界面。

有关详细设置说明，请参阅 [Open WebUI 集成](openwebui-integration.md)。

## Aider

[Aider](https://aider.chat) 是一款用于终端的 AI 结对编程工具。

### 配置

设置环境变量或使用命令行标志：

```bash
export OPENAI_API_BASE=http://localhost:12434/engines/v1
export OPENAI_API_KEY=not-needed

aider --model openai/ai/qwen2.5-coder
```

或者使用单条命令：

```console
$ aider --openai-api-base http://localhost:12434/engines/v1 \
        --openai-api-key not-needed \
        --model openai/ai/qwen2.5-coder
```

## LangChain

### Python

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    base_url="http://localhost:12434/engines/v1",
    api_key="not-needed",
    model="ai/qwen2.5-coder"
)

response = llm.invoke("Write a hello world function in Python")
print(response.content)
```

### JavaScript/TypeScript

```typescript
import { ChatOpenAI } from "@langchain/openai";

const model = new ChatOpenAI({
  configuration: {
    baseURL: "http://localhost:12434/engines/v1",
  },
  apiKey: "not-needed",
  modelName: "ai/qwen2.5-coder",
});

const response = await model.invoke("Write a hello world function");
console.log(response.content);
```

## LlamaIndex

```python
from llama_index.llms.openai_like import OpenAILike

llm = OpenAILike(
    api_base="http://localhost:12434/engines/v1",
    api_key="not-needed",
    model="ai/qwen2.5-coder"
)

response = llm.complete("Write a hello world function")
print(response.text)
```

## 常见问题

### “Connection refused” 错误

1. 确保 Docker Model Runner 已启用并正在运行：
   ```console
   $ docker model status
   ```

2. 验证 TCP 访问已启用：
   ```console
   $ curl http://localhost:12434/engines/v1/models
   ```

3. 检查是否有其他服务正在使用端口 12434。

### “Model not found” 错误

1. 验证模型是否已拉取：
   ```console
   $ docker model list
   ```

2. 使用包含命名空间的完整模型名称（例如 `ai/qwen2.5-coder`，而不仅仅是 `qwen2.5-coder`）。

### 响应缓慢或超时

1. 对于首次请求，模型需要加载到内存中。后续请求会更快。

2. 考虑使用较小的模型或调整上下文大小：
   ```console
   $ docker model configure --context-size 4096 ai/qwen2.5-coder
   ```

3. 检查可用的系统资源（RAM、GPU 显存）。

### CORS 错误（基于 Web 的工具）

如果使用基于浏览器的工具，请将源（origin）添加到 CORS 允许的源中：

1. Docker Desktop：Settings > AI > CORS Allowed Origins
2. 添加工具的 URL（例如 `http://localhost:3000`）

## 按用例推荐的模型

| 用例 | 推荐模型 | 备注 |
|----------|-------------------|-------|
| 代码补全 | `ai/qwen2.5-coder` | 针对编程任务进行了优化 |
| 通用助手 | `ai/llama3.2` | 能力均衡 |
| 轻量/快速 | `ai/smollm2` | 资源占用低 |
| 嵌入 (Embeddings) | `ai/all-minilm` | 用于 RAG 和语义搜索 |

## 下一步

- [API 参考](api-reference.md) - 完整的 API 文档
- [配置选项](configuration.md) - 调整模型行为
- [Open WebUI 集成](openwebui-integration.md) - 设置 Web 界面
