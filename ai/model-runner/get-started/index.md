# DMR 入门指南

Docker Model Runner (DMR) 让您能够使用 Docker 在本地运行和管理 AI 模型。本文将向您展示如何启用 DMR、拉取和运行模型、配置模型设置以及发布自定义模型。

## 启用 Docker Model Runner

您可以使用 Docker Desktop 或 Docker Engine 启用 DMR。请根据您的设置按照以下说明操作。

### Docker Desktop

1. 在设置视图中，转到 **AI** 选项卡。
1. 选择 **启用 Docker Model Runner** 设置。
1. 如果您使用的是支持 NVIDIA GPU 的 Windows 系统，您还会看到并可以选择
   **启用 GPU 支持的推理**。
1. 可选：要启用 TCP 支持，请选择 **启用主机端 TCP 支持**。
   1. 在 **端口** 字段中，输入您要使用的端口。
   1. 如果您通过本地前端 Web 应用与 Model Runner 交互，请在
      **CORS 允许的来源** 中选择 Model Runner 应接受请求的来源。来源是指您的 Web 应用运行的 URL，例如 `http://localhost:3131`。

现在，您可以在 CLI 中使用 `docker model` 命令，并在 Docker Desktop 仪表板的 **模型** 选项卡中查看和与您的本地模型交互。

> [!重要]
>
> 对于 Docker Desktop 4.45 及更早版本，此设置位于
> **Beta 功能** 选项卡下。

### Docker Engine

1. 确保您已安装 [Docker Engine](/engine/install/)。
1. Docker Model Runner 以软件包的形式提供。要安装它，请运行：

   






<div
  class="tabs"
  
    x-data="{ selected: 'Ubuntu/Debian' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'Ubuntu/Debian' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Ubuntu/Debian'"
        
      >
        Ubuntu/Debian
      </button>
    
      <button
        class="tab-item"
        :class="selected === '%E5%9F%BA%E4%BA%8E-RPM-%E7%9A%84%E5%8F%91%E8%A1%8C%E7%89%88' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = '%E5%9F%BA%E4%BA%8E-RPM-%E7%9A%84%E5%8F%91%E8%A1%8C%E7%89%88'"
        
      >
        基于 RPM 的发行版
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Ubuntu/Debian' && 'hidden'"
      >
        <div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBzdWRvIGFwdC1nZXQgdXBkYXRlCiQgc3VkbyBhcHQtZ2V0IGluc3RhbGwgZG9ja2VyLW1vZGVsLXBsdWdpbg==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-bash" data-lang="bash"><span class="line"><span class="cl">$ sudo apt-get update
</span></span><span class="line"><span class="cl">$ sudo apt-get install docker-model-plugin</span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== '%E5%9F%BA%E4%BA%8E-RPM-%E7%9A%84%E5%8F%91%E8%A1%8C%E7%89%88' && 'hidden'"
      >
        <div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBzdWRvIGRuZiB1cGRhdGUKJCBzdWRvIGRuZiBpbnN0YWxsIGRvY2tlci1tb2RlbC1wbHVnaW4=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-bash" data-lang="bash"><span class="line"><span class="cl">$ sudo dnf update
</span></span><span class="line"><span class="cl">$ sudo dnf install docker-model-plugin</span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
  </div>
</div>


1. 测试安装：

   ```bash
   $ docker model version
   $ docker model run ai/smollm2
   ```

> [!注意]
> 对于 Docker Engine，TCP 支持默认在端口 `12434` 上启用。

### 在 Docker Engine 中更新 DMR

要在 Docker Engine 中更新 Docker Model Runner，请先使用
[`docker model uninstall-runner`](/reference/cli/docker/model/uninstall-runner/)
卸载它，然后重新安装：

```bash
docker model uninstall-runner --images && docker model install-runner
```

> [!注意]
> 使用上述命令时，本地模型会被保留。
> 要在升级期间删除模型，请在 `uninstall-runner` 命令中添加 `--models` 选项。

## 拉取模型

模型会被缓存在本地。

> [!注意]
>
> 当您使用 Docker CLI 时，也可以直接从
> [HuggingFace](https://huggingface.co/) 拉取模型。








<div
  class="tabs"
  
    
      x-data="{ selected: '%E4%BB%8E-Docker-Desktop' }"
    
    @tab-select.window="$event.detail.group === 'release' ? selected =
    $event.detail.name : null"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === '%E4%BB%8E-Docker-Desktop' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'release', name:
          '%E4%BB%8E-Docker-Desktop'})"
        
      >
        从 Docker Desktop
      </button>
    
      <button
        class="tab-item"
        :class="selected === '%E4%BB%8E-Docker-CLI' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'release', name:
          '%E4%BB%8E-Docker-CLI'})"
        
      >
        从 Docker CLI
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== '%E4%BB%8E-Docker-Desktop' && 'hidden'"
      >
        <ol>
<li>选择 <strong>模型</strong>，然后选择 <strong>Docker Hub</strong> 选项卡。</li>
<li>找到您想要的模型，然后选择 <strong>拉取</strong>。</li>
</ol>

  
  
    








<figure
  x-data="{ zoom: false }"
  @click="zoom = ! zoom"
  class="cursor-pointer hover:opacity-90"
>
  <img
    loading="lazy"
    src="/ai/model-runner/images/dmr-catalog.png"
    alt="显示 Docker Hub 视图的屏幕截图。"
    
    
    class="mx-auto rounded-sm"
  />
  
  <template x-teleport="body">
    <div
      x-show="zoom"
      @click="zoom = false"
      x-transition.opacity.duration.250ms
      class="fixed inset-0 z-20 flex items-center justify-center bg-black/100 p-6"
    >
      <button class="icon-svg fixed top-6 right-8 z-30 text-white">
        <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M480-438 270-228q-9 9-21 9t-21-9q-9-9-9-21t9-21l210-210-210-210q-9-9-9-21t9-21q9-9 21-9t21 9l210 210 210-210q9-9 21-9t21 9q9 9 9 21t-9 21L522-480l210 210q9 9 9 21t-9 21q-9 9-21 9t-21-9L480-438Z"/></svg>
      </button>
      <img
        loading="lazy"
        class="max-h-full max-w-full rounded-sm"
        src="/ai/model-runner/images/dmr-catalog.png"
        alt="显示 Docker Hub 视图的屏幕截图。"
      />
    </div>
  </template>
</figure>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== '%E4%BB%8E-Docker-CLI' && 'hidden'"
      >
        <p>使用 
  <a class="link" href="/reference/cli/docker/model/pull/"><code>docker model pull</code> 命令</a>。
例如：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
    <div class="flex w-full items-center gap-2">
      <div
        class="flex items-center gap-2.5 rounded bg-gray-100 px-2 py-0.5 dark:bg-gray-800"
      >
        <div class="font-normal text-gray-500 dark:text-gray-200">
          从 Docker Hub 拉取
        </div>
      </div>
    </div>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'ZG9ja2VyIG1vZGVsIHB1bGwgYWkvc21vbGxtMjozNjBNLVE0X0tfTQ==', copying: false }"
        class="
          -top-10
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-bash" data-lang="bash"><span class="line"><span class="cl">docker model pull ai/smollm2:360M-Q4_K_M</span></span></code></pre></div>
      
    </div>
  </div>
</div>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
    <div class="flex w-full items-center gap-2">
      <div
        class="flex items-center gap-2.5 rounded bg-gray-100 px-2 py-0.5 dark:bg-gray-800"
      >
        <div class="font-normal text-gray-500 dark:text-gray-200">
          从 HuggingFace 拉取
        </div>
      </div>
    </div>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'ZG9ja2VyIG1vZGVsIHB1bGwgaGYuY28vYmFydG93c2tpL0xsYW1hLTMuMi0xQi1JbnN0cnVjdC1HR1VG', copying: false }"
        class="
          -top-10
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-bash" data-lang="bash"><span class="line"><span class="cl">docker model pull hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF</span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
  </div>
</div>


## 运行模型








<div
  class="tabs"
  
    
      x-data="{ selected: '%E4%BB%8E-Docker-Desktop' }"
    
    @tab-select.window="$event.detail.group === 'release' ? selected =
    $event.detail.name : null"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === '%E4%BB%8E-Docker-Desktop' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'release', name:
          '%E4%BB%8E-Docker-Desktop'})"
        
      >
        从 Docker Desktop
      </button>
    
      <button
        class="tab-item"
        :class="selected === '%E4%BB%8E-Docker-CLI' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'release', name:
          '%E4%BB%8E-Docker-CLI'})"
        
      >
        从 Docker CLI
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== '%E4%BB%8E-Docker-Desktop' && 'hidden'"
      >
        <ol>
<li>选择 <strong>模型</strong>，然后选择 <strong>本地</strong> 选项卡。</li>
<li>选择播放按钮。交互式聊天屏幕将打开。</li>
</ol>

  
  
    








<figure
  x-data="{ zoom: false }"
  @click="zoom = ! zoom"
  class="cursor-pointer hover:opacity-90"
>
  <img
    loading="lazy"
    src="/ai/model-runner/images/dmr-run.png"
    alt="显示本地视图的屏幕截图。"
    
    
    class="mx-auto rounded-sm"
  />
  
  <template x-teleport="body">
    <div
      x-show="zoom"
      @click="zoom = false"
      x-transition.opacity.duration.250ms
      class="fixed inset-0 z-20 flex items-center justify-center bg-black/100 p-6"
    >
      <button class="icon-svg fixed top-6 right-8 z-30 text-white">
        <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M480-438 270-228q-9 9-21 9t-21-9q-9-9-9-21t9-21l210-210-210-210q-9-9-9-21t9-21q9-9 21-9t21 9l210 210 210-210q9-9 21-9t21 9q9 9 9 21t-9 21L522-480l210 210q9 9 9 21t-9 21q-9 9-21 9t-21-9L480-438Z"/></svg>
      </button>
      <img
        loading="lazy"
        class="max-h-full max-w-full rounded-sm"
        src="/ai/model-runner/images/dmr-run.png"
        alt="显示本地视图的屏幕截图。"
      />
    </div>
  </template>
</figure>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== '%E4%BB%8E-Docker-CLI' && 'hidden'"
      >
        <p>使用 
  <a class="link" href="/reference/cli/docker/model/run/"><code>docker model run</code> 命令</a>。</p>

      </div>
    
  </div>
</div>


## 配置模型

您可以使用 Docker Compose 配置模型，例如其最大 token 限制等。
请参阅 [模型与 Compose - 模型配置选项](../compose/models-and-compose.md#model-configuration-options)。

## 发布模型

> [!注意]
>
> 这适用于任何支持 OCI Artifacts 的容器注册表，而不仅仅是
> Docker Hub。

您可以使用新名称标记现有模型，并将其发布到不同的命名空间和存储库下：

```bash
# 使用新名称标记已拉取的模型
$ docker model tag ai/smollm2 myorg/smollm2

# 将其推送到 Docker Hub
$ docker model push myorg/smollm2
```

有关更多详细信息，请参阅 [`docker model tag`](/reference/cli/docker/model/tag)
和 [`docker model push`](/reference/cli/docker/model/push) 命令文档。

您还可以将 GGUF 格式的模型文件打包为 OCI Artifact 并发布到 Docker Hub。

```bash
# 下载 GGUF 格式的模型文件，例如从 HuggingFace
$ curl -L -o model.gguf https://huggingface.co/TheBloke/Mistral-7B-v0.1-GGUF/resolve/main/mistral-7b-v0.1.Q4_K_M.gguf

# 将其打包为 OCI Artifact 并推送到 Docker Hub
$ docker model package --gguf "$(pwd)/model.gguf" --push myorg/mistral-7b-v0.1:Q4_K_M
```

有关更多详细信息，请参阅
[`docker model package`](/reference/cli/docker/model/package/) 命令文档。

## 故障排除

### 显示日志

要排查问题，请显示日志：








<div
  class="tabs"
  
    
      x-data="{ selected: '%E4%BB%8E-Docker-Desktop' }"
    
    @tab-select.window="$event.detail.group === 'release' ? selected =
    $event.detail.name : null"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === '%E4%BB%8E-Docker-Desktop' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'release', name:
          '%E4%BB%8E-Docker-Desktop'})"
        
      >
        从 Docker Desktop
      </button>
    
      <button
        class="tab-item"
        :class="selected === '%E4%BB%8E-Docker-CLI' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'release', name:
          '%E4%BB%8E-Docker-CLI'})"
        
      >
        从 Docker CLI
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== '%E4%BB%8E-Docker-Desktop' && 'hidden'"
      >
        <p>选择 <strong>模型</strong>，然后选择 <strong>日志</strong> 选项卡。</p>

  
  
    








<figure
  x-data="{ zoom: false }"
  @click="zoom = ! zoom"
  class="cursor-pointer hover:opacity-90"
>
  <img
    loading="lazy"
    src="/ai/model-runner/images/dmr-logs.png"
    alt="显示模型视图的屏幕截图。"
    
    
    class="mx-auto rounded-sm"
  />
  
  <template x-teleport="body">
    <div
      x-show="zoom"
      @click="zoom = false"
      x-transition.opacity.duration.250ms
      class="fixed inset-0 z-20 flex items-center justify-center bg-black/100 p-6"
    >
      <button class="icon-svg fixed top-6 right-8 z-30 text-white">
        <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M480-438 270-228q-9 9-21 9t-21-9q-9-9-9-21t9-21l210-210-210-210q-9-9-9-21t9-21q9-9 21-9t21 9l210 210 210-210q9-9 21-9t21 9q9 9 9 21t-9 21L522-480l210 210q9 9 9 21t-9 21q-9 9-21 9t-21-9L480-438Z"/></svg>
      </button>
      <img
        loading="lazy"
        class="max-h-full max-w-full rounded-sm"
        src="/ai/model-runner/images/dmr-logs.png"
        alt="显示模型视图的屏幕截图。"
      />
    </div>
  </template>
</figure>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== '%E4%BB%8E-Docker-CLI' && 'hidden'"
      >
        <p>使用 
  <a class="link" href="/reference/cli/docker/model/logs/"><code>docker model logs</code> 命令</a>。</p>

      </div>
    
  </div>
</div>


### 检查请求和响应

检查请求和响应有助于诊断与模型相关的问题。
例如，您可以评估上下文使用情况，以验证您是否保持在模型的上下文窗口内，或者在开发框架时显示请求的完整正文以控制传递给模型的参数。

在 Docker Desktop 中，要检查每个模型的请求和响应：

1. 选择 **模型**，然后选择 **请求** 选项卡。此视图显示对所有模型的所有请求：
   - 请求发送的时间。
   - 模型名称和版本
   - 提示/请求
   - 上下文使用情况
   - 生成响应所花费的时间。
1. 选择一个请求以显示更多详细信息：
   - 在 **概览** 选项卡中，查看 token 使用情况、响应元数据和生成速度，以及实际的提示和响应。
   - 在 **请求** 和 **响应** 选项卡中，查看请求和响应的完整 JSON 负载。

> [!注意]
> 您还可以在选择一个模型后选择 **请求** 选项卡来显示特定模型的请求。

## 相关页面

- [以编程方式与您的模型交互](./api-reference.md)
- [模型与 Compose](../compose/models-and-compose.md)
- [Docker Model Runner CLI 参考文档](/reference/cli/docker/model)
