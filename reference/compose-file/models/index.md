# 模型





  
  
  
  


  <div
    class="not-prose summary-bar"
  >
    

    

    
      <div class="flex flex-wrap gap-1">
        <span class="font-bold">Requires:</span>
        <span>Docker Compose <a class="link" href="https://github.com/docker/compose/releases/tag/v2.38.0" rel="noopener">2.38.0</a> and later</span>
        <span class="icon-svg">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M140-240q-24 0-42-18t-18-42v-480q0-24 18-42t42-18h367q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5H140v480h680v-109q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v109q0 24-18 42t-42 18H652l39 38q5 5 7 10.54 2 5.55 2 11.46v30q0 12.75-8.62 21.37Q682.75-120 670-120H290q-12.75 0-21.37-8.63Q260-137.25 260-150v-31q0-5.57 2-10.78 2-5.22 7-10.22l38-38H140Zm457-221v-349q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v349l100-99q9-8 21.1-8.5 12.1-.5 20.9 8.5 9 9 9 21t-9 21L627-346 455-518q-9-9-9-21t9-21q9-9 21-9t21 9l100 99Z"/></svg>
        </span>
      </div>
    

    
  </div>



顶级 `models` 部分声明了您的 Compose 应用程序所使用的 AI 模型。这些模型通常作为 OCI 工件拉取，由模型运行器执行，并作为 API 暴露，您的服务容器可以消费这些 API。

服务只有在 `services` 顶级元素中的 [`models` 属性](services.md#models) 明确授权时，才能访问模型。

## 示例

### 示例 1

```yaml
services:
  app:
    image: app
    models:
      - ai_model


models:
  ai_model:
    model: ai/model
```

在这个基本示例中：

 - app 服务使用 `ai_model`。
 - `ai_model` 被定义为 OCI 工件（`ai/model`），由模型运行器拉取并提供服务。
 - Docker Compose 将连接信息（例如 `AI_MODEL_URL`）注入到容器中。

### 示例 2

```yaml
services:
  app:
    image: app
    models:
      my_model:
        endpoint_var: MODEL_URL

models:
  my_model:
    model: ai/model
    context_size: 1024
    runtime_flags: 
      - "--a-flag"
      - "--another-flag=42"
```

在这个高级设置中：

 - 服务 app 使用长格式语法引用 `my_model`。
 - Compose 将模型运行器的 URL 作为环境变量 `MODEL_URL` 注入。

## 属性

- `model`（必需）：模型的 OCI 工件标识符。Compose 通过模型运行器拉取并运行此标识符。
- `context_size`：定义模型的最大令牌上下文大小。
- `runtime_flags`：模型启动时传递给推理引擎的原始命令行标志列表。

## 额外资源

有关使用 `model` 的更多示例和信息，请参阅 [在 Compose 中使用 AI 模型](/manuals/ai/compose/models-and-compose.md)
