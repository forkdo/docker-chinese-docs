# DMR REST API

启用 Model Runner 后，将提供新的 API 端点。你可以使用这些端点以编程方式与模型交互。

### 确定基础 URL

与端点交互的基础 URL 取决于你运行 Docker 的方式：








<div
  class="tabs"
  
    x-data="{ selected: 'Docker-Desktop' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'Docker-Desktop' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Docker-Desktop'"
        
      >
        Docker Desktop
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Docker-Engine' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Docker-Engine'"
        
      >
        Docker Engine
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Docker-Desktop' && 'hidden'"
      >
        <ul>
<li>从容器内：<code>http://model-runner.docker.internal/</code></li>
<li>从主机进程：<code>http://localhost:12434/</code>（假设在默认端口 12434 上启用了 TCP 主机访问）</li>
</ul>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Docker-Engine' && 'hidden'"
      >
        <ul>
<li>从容器内：<code>http://172.17.0.1:12434/</code>（其中 <code>172.17.0.1</code> 表示主机网关地址）</li>
<li>从主机进程：<code>http://localhost:12434/</code></li>
</ul>


  

  <blockquote
    
    class="admonition admonition-note admonition not-prose">
    <div class="admonition-header">
      <span class="admonition-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M12 16V12M12 8H12.01M22 12C22 17.5228 17.5228 22 12 22C6.47715 22 2 17.5228 2 12C2 6.47715 6.47715 2 12 2C17.5228 2 22 6.47715 22 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>

      </span>
      <span class="admonition-title">
        Note
      </span>
    </div>
    <div class="admonition-content">
      <p><code>172.17.0.1</code> 接口默认情况下可能对 Compose 项目中的容器不可用。
在这种情况下，在你的 Compose 服务 YAML 中添加 <code>extra_hosts</code> 指令：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'ZXh0cmFfaG9zdHM6CiAgLSAibW9kZWwtcnVubmVyLmRvY2tlci5pbnRlcm5hbDpob3N0LWdhdGV3YXki', copying: false }"
        class="
          top-1
         absolute right-2 z-10 text-gray-300 dark:text-gray-500"
        title="copy"
        @click="window.navigator.clipboard.writeText(atob(code).replaceAll(/^[\$>]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);"
      >
        <span
          :class="{ 'group-hover:block' : !copying }"
          class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M300-200q-24 0-42-18t-18-42v-560q0-24 18-42t42-18h440q24 0 42 18t18 42v560q0 24-18 42t-42 18H300ZM180-80q-24 0-42-18t-18-42v-590q0-13 8.5-21.5T150-760q13 0 21.5 8.5T180-730v590h470q13 0 21.5 8.5T680-110q0 13-8.5 21.5T650-80H180Z"/></svg></span
        >
        <span :class="{ 'group-hover:block' : copying }" class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="m421-389-98-98q-9-9-22-9t-23 10q-9 9-9 22t9 22l122 123q9 9 21 9t21-9l239-239q10-10 10-23t-10-23q-10-9-23.5-8.5T635-603L421-389Zm59 309q-82 0-155-31.5t-127.5-86Q143-252 111.5-325T80-480q0-83 31.5-156t86-127Q252-817 325-848.5T480-880q83 0 156 31.5T763-763q54 54 85.5 127T880-480q0 82-31.5 155T763-197.5q-54 54.5-127 86T480-80Z"/></svg></span
        >
      </button>
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-yaml" data-lang="yaml"><span class="line"><span class="cl"><span class="nt">extra_hosts</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">  </span>- <span class="s2">&#34;model-runner.docker.internal:host-gateway&#34;</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>然后你可以通过 <a class="link" href="http://model-runner.docker.internal:12434/" rel="noopener">http://model-runner.docker.internal:12434/</a> 访问 Docker Model Runner API</p>
    </div>
  </blockquote>


      </div>
    
  </div>
</div>


### 可用的 DMR 端点

- 创建模型：

  ```text
  POST /models/create
  ```

- 列出模型：

  ```text
  GET /models
  ```

- 获取模型：

  ```text
  GET /models/{namespace}/{name}
  ```

- 删除本地模型：

  ```text
  DELETE /models/{namespace}/{name}
  ```

### 可用的 OpenAI 端点

DMR 支持以下 OpenAI 端点：

- [列出模型](https://platform.openai.com/docs/api-reference/models/list)：

  ```text
  GET /engines/llama.cpp/v1/models
  ```

- [检索模型](https://platform.openai.com/docs/api-reference/models/retrieve)：

  ```text
  GET /engines/llama.cpp/v1/models/{namespace}/{name}
  ```

- [列出聊天完成](https://platform.openai.com/docs/api-reference/chat/list)：

  ```text
  POST /engines/llama.cpp/v1/chat/completions
  ```

- [创建完成](https://platform.openai.com/docs/api-reference/completions/create)：

  ```text
  POST /engines/llama.cpp/v1/completions
  ```

- [创建嵌入](https://platform.openai.com/docs/api-reference/embeddings/create)：

  ```text
  POST /engines/llama.cpp/v1/embeddings
  ```

要通过 Unix 套接字（`/var/run/docker.sock`）调用这些端点，需在其路径前添加 `/exp/vDD4.40`。

> [!NOTE]
> 你可以从路径中省略 `llama.cpp`。例如：`POST /engines/v1/chat/completions`。

## REST API 示例

### 从容器内请求

要从另一个容器内使用 `curl` 调用 `chat/completions` OpenAI 端点：

```bash
#!/bin/sh

curl http://model-runner.docker.internal/engines/llama.cpp/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{
        "model": "ai/smollm2",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": "Please write 500 words about the fall of Rome."
            }
        ]
    }'

```

### 使用 TCP 从主机请求

要通过 TCP 从主机调用 `chat/completions` OpenAI 端点：

1. 从 Docker Desktop GUI 启用主机侧 TCP 支持，或通过 [Docker Desktop CLI](/manuals/desktop/features/desktop-cli.md) 启用。
   例如：`docker desktop enable model-runner --tcp <port>`。

   如果你在 Windows 上运行，还需启用 GPU 支持的推理。
   参见 [启用 Docker Model Runner](get-started.md#enable-docker-model-runner-in-docker-desktop)。

1. 按照上一节的文档使用 `localhost` 和正确的端口与其交互。

```bash
#!/bin/sh

  curl http://localhost:12434/engines/llama.cpp/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{
        "model": "ai/smollm2",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": "Please write 500 words about the fall of Rome."
            }
        ]
    }'
```

### 使用 Unix 套接字从主机请求

要通过 Docker 套接字使用 `curl` 从主机调用 `chat/completions` OpenAI 端点：

```bash
#!/bin/sh

curl --unix-socket $HOME/.docker/run/docker.sock \
    localhost/exp/vDD4.40/engines/llama.cpp/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{
        "model": "ai/smollm2",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": "Please write 500 words about the fall of Rome."
            }
        ]
    }'
```
