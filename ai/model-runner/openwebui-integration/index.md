---
title: Open WebUI 集成
url: /ai/model-runner/openwebui-integration/
parent:
  title: Docker Model Runner
  url: /ai/model-runner/
breadcrumbs:
  - title: 手册
    url: /manuals/
  - title: Docker Model Runner
    url: /ai/model-runner/
  - title: Open WebUI 集成
    url: /ai/model-runner/openwebui-integration/
next:
  title: IDE 与工具集成
  url: /ai/model-runner/ide-integrations/
prev:
  title: 推理引擎
  url: /ai/model-runner/inference-engines/
---


[Open WebUI](https://github.com/open-webui/open-webui) 是一个开源、自托管的 Web 界面，为本地 AI 模型提供类 ChatGPT 的体验。您可以将其连接到 Docker Model Runner，为您的模型获取一个精美的聊天界面。

## 先决条件

- 已启用 Docker Model Runner 并支持 TCP 访问
- 已拉取模型（例如 `docker model pull ai/llama3.2`）

## 使用 Docker Compose 快速开始

使用 Docker Compose 是运行 Open WebUI 与 Docker Model Runner 的最简单方式。

创建一个 `compose.yaml` 文件：

```yaml
services:
  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    ports:
      - "3000:8080"
    environment:
      - OLLAMA_BASE_URL=http://host.docker.internal:12434
      - WEBUI_AUTH=false
    extra_hosts:
      - "host.docker.internal:host-gateway"
    volumes:
      - open-webui:/app/backend/data

volumes:
  open-webui:
```

启动服务：

```console
$ docker compose up -d
```

在浏览器中打开 [http://localhost:3000](http://localhost:3000)。

## 配置选项

### 环境变量

| 变量 | 描述 | 默认值 |
|----------|-------------|---------|
| `OLLAMA_BASE_URL` | Docker Model Runner 的 URL | 必需 |
| `WEBUI_AUTH` | 启用身份验证 | `true` |
| `OPENAI_API_BASE_URL` | 改用 OpenAI 兼容 API | - |
| `OPENAI_API_KEY` | API 密钥（对于 DMR 使用任意值） | - |

### 使用 OpenAI 兼容 API

如果您更喜欢使用 OpenAI 兼容 API 而不是 Ollama API：

```yaml
services:
  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    ports:
      - "3000:8080"
    environment:
      - OPENAI_API_BASE_URL=http://host.docker.internal:12434/engines/v1
      - OPENAI_API_KEY=not-needed
      - WEBUI_AUTH=false
    extra_hosts:
      - "host.docker.internal:host-gateway"
    volumes:
      - open-webui:/app/backend/data

volumes:
  open-webui:
```

## 网络配置

### Docker Desktop

在 Docker Desktop 上，`host.docker.internal` 会自动解析到主机机器。
前面的示例无需修改即可工作。

### Docker Engine (Linux)

在 Docker Engine 上，您可能需要以不同方式配置网络：

```yaml
services:
  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    network_mode: host
    environment:
      - OLLAMA_BASE_URL=http://localhost:12434
      - WEBUI_AUTH=false
    volumes:
      - open-webui:/app/backend/data

volumes:
  open-webui:
```

或者使用主机网关：

```yaml
services:
  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    ports:
      - "3000:8080"
    environment:
      - OLLAMA_BASE_URL=http://172.17.0.1:12434
      - WEBUI_AUTH=false
    volumes:
      - open-webui:/app/backend/data

volumes:
  open-webui:
```

## 使用 Open WebUI

### 选择模型

1. 打开 [http://localhost:3000](http://localhost:3000)
2. 在左上角选择模型下拉菜单
3. 从您已拉取的模型中选择（它们会以 `ai/` 前缀显示）

### 通过 UI 拉取模型

Open WebUI 可以直接拉取模型：

1. 选择模型下拉菜单
2. 输入模型名称：`ai/llama3.2`
3. 选择下载图标

### 聊天功能

Open WebUI 提供：

- 带上下文的多轮对话
- 消息编辑和重新生成
- 代码语法高亮
- Markdown 渲染
- 对话历史记录和搜索
- 导出对话

## 包含多个模型的完整示例

此示例设置了 Open WebUI 与 Docker Model Runner，并预先拉取了几个模型：

```yaml
services:
  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    ports:
      - "3000:8080"
    environment:
      - OLLAMA_BASE_URL=http://host.docker.internal:12434
      - WEBUI_AUTH=false
      - DEFAULT_MODELS=ai/llama3.2
    extra_hosts:
      - "host.docker.internal:host-gateway"
    volumes:
      - open-webui:/app/backend/data
    depends_on:
      model-setup:
        condition: service_completed_successfully

  model-setup:
    image: docker:cli
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    command: >
      sh -c "
        docker model pull ai/llama3.2 &&
        docker model pull ai/qwen2.5-coder &&
        docker model pull ai/smollm2
      "

volumes:
  open-webui:
```

## 启用身份验证

对于多用户设置或安全性，启用身份验证：

```yaml
services:
  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    ports:
      - "3000:8080"
    environment:
      - OLLAMA_BASE_URL=http://host.docker.internal:12434
      - WEBUI_AUTH=true
    extra_hosts:
      - "host.docker.internal:host-gateway"
    volumes:
      - open-webui:/app/backend/data

volumes:
  open-webui:
```

首次访问时，您将创建一个管理员账户。

## 故障排除

### 模型未出现在下拉菜单中

1. 验证 Docker Model Runner 是否可访问：
   ```console
   $ curl http://localhost:12434/api/tags
   ```

2. 检查模型是否已拉取：
   ```console
   $ docker model list
   ```

3. 验证 `OLLAMA_BASE_URL` 是否正确且可从容器访问。

### "连接被拒绝" 错误

1. 确保 Docker Model Runner 已启用 TCP 访问。

2. 在 Docker Desktop 上，验证 `host.docker.internal` 是否可解析：
   ```console
   $ docker run --rm alpine ping -c 1 host.docker.internal
   ```

3. 在 Docker Engine 上，尝试使用 `network_mode: host` 或显式主机 IP。

### 响应时间慢

1. 首次请求会将模型加载到内存中，这需要时间。

2. 后续请求会快得多。

3. 如果持续缓慢，请考虑：
   - 使用更小的模型
   - 减少上下文大小
   - 检查 GPU 加速是否正常工作

### CORS 错误

如果在不同主机上运行 Open WebUI：

1. 在 Docker Desktop 中，转到设置 > AI
2. 将 Open WebUI URL 添加到 **CORS Allowed Origins**

## 自定义

### 自定义系统提示

Open WebUI 支持为每个模型设置系统提示。在 UI 中的设置 > 模型下配置这些。

### 模型参数

在聊天界面中调整模型参数：

1. 选择模型名称旁边的设置图标
2. 调整 temperature、top-p、max tokens 等。

这些设置会传递给 Docker Model Runner。

## 在不同端口上运行

要在不同端口上运行 Open WebUI：

```yaml
services:
  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    ports:
      - "8080:8080"  # 更改第一个端口号
    # ... 其余配置
```

## 下一步

- [API 参考](api-reference.md) - 了解 Open WebUI 使用的 API
- [配置选项](configuration.md) - 调整模型行为
- [IDE 集成](ide-integrations.md) - 将其他工具连接到 DMR
