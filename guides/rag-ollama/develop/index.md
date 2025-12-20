# 使用容器进行 RAG 开发

## 先决条件

完成 [容器化 RAG 应用](containerize.md)。

## 概述

在本节中，你将学习如何设置开发环境以访问生成式 RAG 应用所需的所有服务。这包括：

- 添加本地数据库
- 添加本地或远程 LLM 服务

> [!NOTE]
> 你可以在 [GenAI Stack](https://github.com/docker/genai-stack) 演示应用中查看更多容器化 GenAI 应用的示例。

## 添加本地数据库

你可以使用容器来设置本地服务，例如数据库。在本节中，你将探索 `docker-compose.yaml` 文件中的数据库服务。

运行数据库服务：

1. 在克隆的仓库目录中，使用 IDE 或文本编辑器打开 `docker-compose.yaml` 文件。

2. 在 `docker-compose.yaml` 文件中，你会看到以下内容：

   ```yaml
   services:
     qdrant:
       image: qdrant/qdrant
       container_name: qdrant
       ports:
         - "6333:6333"
       volumes:
         - qdrant_data:/qdrant/storage
   ```

   > [!NOTE]
   > 要了解更多关于 Qdrant 的信息，请参阅 [Qdrant 官方 Docker 镜像](https://hub.docker.com/r/qdrant/qdrant)。

3. 启动应用。在 `winy` 目录内，在终端中运行以下命令。

   ```console
   $ docker compose up --build
   ```

4. 访问应用。打开浏览器，在 [http://localhost:8501](http://localhost:8501) 查看应用。你应该会看到一个简单的 Streamlit 应用。

5. 停止应用。在终端中，按 `ctrl`+`c` 停止应用。

## 添加本地或远程 LLM 服务

示例应用支持 [Ollama](https://ollama.ai/)。本指南提供以下场景的说明：

- 在容器中运行 Ollama
- 在容器外运行 Ollama

虽然所有平台都可以使用上述任何场景，但性能和 GPU 支持可能会有所不同。你可以使用以下指南来帮助你选择合适的选项：

- 如果你使用的是 Linux 和 Docker 引擎的原生安装，或者 Windows 10/11 和 Docker Desktop，并且拥有支持 CUDA 的 GPU，且系统至少有 8 GB 内存，则在容器中运行 Ollama。
- 如果在 Linux 机器上运行 Docker Desktop，则在容器外运行 Ollama。

为你的 LLM 服务选择以下选项之一。








<div
  class="tabs"
  
    x-data="{ selected: '%E5%9C%A8%E5%AE%B9%E5%99%A8%E4%B8%AD%E8%BF%90%E8%A1%8C-Ollama' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === '%E5%9C%A8%E5%AE%B9%E5%99%A8%E4%B8%AD%E8%BF%90%E8%A1%8C-Ollama' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = '%E5%9C%A8%E5%AE%B9%E5%99%A8%E4%B8%AD%E8%BF%90%E8%A1%8C-Ollama'"
        
      >
        在容器中运行 Ollama
      </button>
    
      <button
        class="tab-item"
        :class="selected === '%E5%9C%A8%E5%AE%B9%E5%99%A8%E5%A4%96%E8%BF%90%E8%A1%8C-Ollama' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = '%E5%9C%A8%E5%AE%B9%E5%99%A8%E5%A4%96%E8%BF%90%E8%A1%8C-Ollama'"
        
      >
        在容器外运行 Ollama
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== '%E5%9C%A8%E5%AE%B9%E5%99%A8%E4%B8%AD%E8%BF%90%E8%A1%8C-Ollama' && 'hidden'"
      >
        <p>在容器中运行 Ollama 时，你应该拥有支持 CUDA 的 GPU。虽然你可以在没有支持 GPU 的情况下在容器中运行 Ollama，但性能可能无法接受。只有 Linux 和 Windows 11 支持 GPU 访问容器。</p>
<p>要在容器中运行 Ollama 并提供 GPU 访问：</p>
<ol>
<li>
<p>安装先决条件。</p>
<ul>
<li>对于 Linux 上的 Docker 引擎，安装 <a class="link" href="https://github.com/NVIDIA/nvidia-container-toolkit" rel="noopener">NVIDIA Container Toolkit</a>。</li>
<li>对于 Windows 10/11 上的 Docker Desktop，安装最新的 <a class="link" href="https://www.nvidia.com/Download/index.aspx" rel="noopener">NVIDIA 驱动程序</a>，并确保你正在使用 
    
  
  <a class="link" href="/desktop/features/wsl/#turn-on-docker-desktop-wsl-2">WSL2 后端</a>。</li>
</ul>
</li>
<li>
<p><code>docker-compose.yaml</code> 文件已经包含必要的指令。在你自己的应用中，你需要在 <code>docker-compose.yaml</code> 中添加 Ollama 服务。以下是更新后的 <code>docker-compose.yaml</code>：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'b2xsYW1hOgogIGltYWdlOiBvbGxhbWEvb2xsYW1hCiAgY29udGFpbmVyX25hbWU6IG9sbGFtYQogIHBvcnRzOgogICAgLSAiODAwMDo4MDAwIgogIGRlcGxveToKICAgIHJlc291cmNlczoKICAgICAgcmVzZXJ2YXRpb25zOgogICAgICAgIGRldmljZXM6CiAgICAgICAgICAtIGRyaXZlcjogbnZpZGlhCiAgICAgICAgICAgIGNvdW50OiAxCiAgICAgICAgICAgIGNhcGFiaWxpdGllczogW2dwdV0=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-yaml" data-lang="yaml"><span class="line"><span class="cl"><span class="nt">ollama</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">  </span><span class="nt">image</span><span class="p">:</span><span class="w"> </span><span class="l">ollama/ollama</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">  </span><span class="nt">container_name</span><span class="p">:</span><span class="w"> </span><span class="l">ollama</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">  </span><span class="nt">ports</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">    </span>- <span class="s2">&#34;8000:8000&#34;</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">  </span><span class="nt">deploy</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">    </span><span class="nt">resources</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">      </span><span class="nt">reservations</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">        </span><span class="nt">devices</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">          </span>- <span class="nt">driver</span><span class="p">:</span><span class="w"> </span><span class="l">nvidia</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">            </span><span class="nt">count</span><span class="p">:</span><span class="w"> </span><span class="m">1</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">            </span><span class="nt">capabilities</span><span class="p">:</span><span class="w"> </span><span class="p">[</span><span class="l">gpu]</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>


  

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
      <p>有关 Compose 指令的更多详细信息，请参阅 
    
  
  <a class="link" href="/compose/how-tos/gpu-support/">使用 Docker Compose 启用 GPU 访问</a>。</p>
    </div>
  </blockquote>

</li>
<li>
<p>一旦 Ollama 容器启动并运行，就可以使用 <code>tools</code> 文件夹中的 <code>download_model.sh</code> 和以下命令：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'LiAuL2Rvd25sb2FkX21vZGVsLnNoIDxtb2RlbC1uYW1lPg==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="go">. ./download_model.sh &lt;model-name&gt;
</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
</li>
</ol>
<p>拉取 Ollama 模型可能需要几分钟。</p>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== '%E5%9C%A8%E5%AE%B9%E5%99%A8%E5%A4%96%E8%BF%90%E8%A1%8C-Ollama' && 'hidden'"
      >
        <p>要在容器外运行 Ollama：</p>
<ol>
<li>
<p>在主机上<a class="link" href="https://github.com/jmorganca/ollama" rel="noopener">安装</a>并运行 Ollama。</p>
</li>
<li>
<p>使用以下命令将模型拉取到 Ollama。</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBvbGxhbWEgcHVsbCBsbGFtYTI=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> ollama pull llama2
</span></span></code></pre></div>
      
    </div>
  </div>
</div>
</li>
<li>
<p>从 <code>docker-compose.yaml</code> 中删除 <code>ollama</code> 服务，并在 <code>winy</code> 服务中正确更新连接变量：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'LSBPTExBTUE9aHR0cDovL29sbGFtYToxMTQzNAorIE9MTEFNQT08eW91ci11cmw&#43;', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-diff" data-lang="diff"><span class="line"><span class="cl"><span class="gd">- OLLAMA=http://ollama:11434
</span></span></span><span class="line"><span class="cl"><span class="gd"></span><span class="gi">+ OLLAMA=&lt;your-url&gt;
</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
</li>
</ol>

      </div>
    
  </div>
</div>


## 运行你的 RAG 应用

此时，你的 Compose 文件中包含以下服务：

- 用于主 RAG 应用的 Server 服务
- 用于在 Qdrant 数据库中存储向量的 Database 服务
- （可选）用于运行 LLM 服务的 Ollama 服务

应用运行后，打开浏览器并访问 [http://localhost:8501](http://localhost:8501)。

根据你的系统和选择的 LLM 服务，可能需要几分钟才能得到回答。

## 总结

在本节中，你学习了如何设置开发环境以提供对 GenAI 应用所需的所有服务的访问。

相关信息：

- [Dockerfile 参考](/reference/dockerfile.md)
- [Compose 文件参考](/reference/compose-file/_index.md)
- [Ollama Docker 镜像](https://hub.docker.com/r/ollama/ollama)
- [GenAI Stack 演示应用](https://github.com/docker/genai-stack)

## 下一步

在 [GenAI Stack 演示应用](https://github.com/docker/genai-stack) 中查看更多 GenAI 应用的示例。
