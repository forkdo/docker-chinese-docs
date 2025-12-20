# Docker Model Runner





  
  
  
  


  <div
    class="not-prose summary-bar"
  >
    

    

    
      <div class="flex flex-wrap gap-1">
        <span class="font-bold">Requires:</span>
        <span>Docker Engine or Docker Desktop (Windows) 4.41+ or Docker Desktop (MacOS) 4.40+</span>
        <span class="icon-svg">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M140-240q-24 0-42-18t-18-42v-480q0-24 18-42t42-18h367q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5H140v480h680v-109q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v109q0 24-18 42t-42 18H652l39 38q5 5 7 10.54 2 5.55 2 11.46v30q0 12.75-8.62 21.37Q682.75-120 670-120H290q-12.75 0-21.37-8.63Q260-137.25 260-150v-31q0-5.57 2-10.78 2-5.22 7-10.22l38-38H140Zm457-221v-349q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v349l100-99q9-8 21.1-8.5 12.1-.5 20.9 8.5 9 9 9 21t-9 21L627-346 455-518q-9-9-9-21t9-21q9-9 21-9t21 9l100 99Z"/></svg>
        </span>
      </div>
    

    
      <div class="flex flex-wrap gap-1">
        <span class="font-bold">For:</span>
        <span>See Requirements section below</span>
        
      </div>
    
  </div>



Docker Model Runner (DMR) 让使用 Docker 管理、运行和部署 AI 模型变得简单。Docker Model Runner 专为开发者设计，简化了从 Docker Hub 或任何符合 OCI 标准的注册中心拉取、运行和服务大型语言模型 (LLM) 及其他 AI 模型的流程。

通过与 Docker Desktop 和 Docker Engine 的无缝集成，您可以通过与 OpenAI 兼容的 API 提供模型服务，将 GGUF 文件打包为 OCI Artifacts，并通过命令行和图形界面与模型交互。

无论您是构建生成式 AI 应用、试验机器学习工作流，还是将 AI 集成到软件开发生命周期中，Docker Model Runner 都提供了一种一致、安全且高效的方式在本地使用 AI 模型。

## 主要特性

- [从 Docker Hub 拉取和推送模型](https://hub.docker.com/u/ai)
- 通过与 OpenAI 兼容的 API 提供模型服务，便于与现有应用集成
- 支持 llama.cpp 和 vLLM 推理引擎（vLLM 目前仅在 Linux x86_64/amd64 上支持 NVIDIA GPU）
- 将 GGUF 和 Safetensors 文件打包为 OCI Artifacts 并发布到任何容器注册中心
- 直接从命令行或 Docker Desktop GUI 运行和交互 AI 模型
- 管理本地模型并显示日志
- 显示提示和响应详情
- 支持对话上下文，实现多轮交互

## 系统要求

Docker Model Runner 支持以下平台：








<div
  class="tabs"
  
    x-data="{ selected: 'Windows' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'Windows' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Windows'"
        
      >
        Windows
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'MacOS' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'MacOS'"
        
      >
        MacOS
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Linux' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Linux'"
        
      >
        Linux
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Windows' && 'hidden'"
      >
        <p>Windows(amd64):</p>
<ul>
<li>NVIDIA GPU</li>
<li>NVIDIA 驱动 576.57+</li>
</ul>
<p>Windows(arm64):</p>
<ul>
<li>
<p>Adreno 的 OpenCL</p>
</li>
<li>
<p>Qualcomm Adreno GPU（6xx 系列及更高版本）</p>


  

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
      <p>6xx 系列可能不完全支持某些 llama.cpp 功能。</p>
    </div>
  </blockquote>

</li>
</ul>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'MacOS' && 'hidden'"
      >
        <ul>
<li>Apple Silicon</li>
</ul>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Linux' && 'hidden'"
      >
        <p>仅限 Docker Engine：</p>
<ul>
<li>支持 CPU、NVIDIA (CUDA)、AMD (ROCm) 和 Vulkan 后端</li>
<li>使用 NVIDIA GPU 时需要 NVIDIA 驱动 575.57.08+</li>
</ul>

      </div>
    
  </div>
</div>


## Docker Model Runner 工作原理

模型在首次使用时从 Docker Hub 拉取并存储在本地。它们仅在运行时收到请求时加载到内存中，并在不使用时卸载以优化资源。由于模型可能很大，初始拉取可能需要一些时间。之后，它们会缓存在本地以便更快访问。您可以使用 [与 OpenAI 兼容的 API](api-reference.md) 与模型交互。

Docker Model Runner 同时支持 [llama.cpp](https://github.com/ggerganov/llama.cpp) 和 [vLLM](https://github.com/vllm-project/vllm) 作为推理引擎，为不同的模型格式和性能要求提供了灵活性。更多详情，请参阅 [Docker Model Runner 仓库](https://github.com/docker/model-runner)。

> [!TIP]
>
> 正在使用 Testcontainers 或 Docker Compose？
> [Testcontainers for Java](https://java.testcontainers.org/modules/docker_model_runner/)
> 和 [Go](https://golang.testcontainers.org/modules/dockermodelrunner/)，以及
> [Docker Compose](/manuals/ai/compose/models-and-compose.md) 现已支持 Docker Model Runner。

## 已知问题

### `docker model` 无法识别

如果您运行 Docker Model Runner 命令时看到：

```text
docker: 'model' is not a docker command
```

这表示 Docker 找不到该插件，因为它不在预期的 CLI 插件目录中。

要解决此问题，请创建一个符号链接，以便 Docker 能够检测到它：

```console
$ ln -s /Applications/Docker.app/Contents/Resources/cli-plugins/docker-model ~/.docker/cli-plugins/docker-model
```

链接后，重新运行该命令。

## 分享反馈

感谢您试用 Docker Model Runner。要报告错误或请求功能，请 [在 GitHub 上提交 issue](https://github.com/docker/model-runner/issues)。您也可以通过 **Enable Docker Model Runner** 设置旁边的 **Give feedback** 链接提供反馈。

## 下一步

[开始使用 DMR](get-started.md)

- [DMR 入门指南](/ai/model-runner/get-started/)

- [DMR REST API](/ai/model-runner/api-reference/)

- [DMR 示例](/ai/model-runner/examples/)

