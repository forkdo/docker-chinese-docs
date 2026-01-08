# 使用容器进行生成式 AI 开发

## 先决条件

完成 [容器化生成式 AI 应用程序](containerize.md)。

## 概述

在本节中，您将学习如何设置开发环境，以访问生成式 AI (GenAI) 应用程序所需的所有服务。这包括：

- 添加本地数据库
- 添加本地或远程 LLM 服务

> [!NOTE]
>
> 您可以在 [GenAI Stack](https://github.com/docker/genai-stack) 演示应用程序中看到更多容器化 GenAI 应用程序的示例。

## 添加本地数据库

您可以使用容器来设置本地服务，例如数据库。在本节中，您将更新 `compose.yaml` 文件以定义数据库服务。此外，您还将指定一个环境变量文件，以加载数据库连接信息，而不是每次都手动输入信息。

要运行数据库服务：

1. 在克隆的仓库目录中，将 `env.example` 文件重命名为 `.env`。
   该文件包含容器将使用的环境变量。
2. 在克隆的仓库目录中，在 IDE 或文本编辑器中打开 `compose.yaml` 文件。
3. 在 `compose.yaml` 文件中，添加以下内容：

   - 添加运行 Neo4j 数据库的指令
   - 在服务器服务下指定环境文件，以便传入连接的环境变量

   以下是更新后的 `compose.yaml` 文件。所有注释已被移除。

   ```yaml{hl_lines=["7-23"]}
   services:
     server:
       build:
         context: .
       ports:
         - 8000:8000
       env_file:
         - .env
       depends_on:
         database:
           condition: service_healthy
     database:
       image: neo4j:5.11
       ports:
         - "7474:7474"
         - "7687:7687"
       environment:
         - NEO4J_AUTH=${NEO4J_USERNAME}/${NEO4J_PASSWORD}
       healthcheck:
         test: ["CMD-SHELL", "wget --no-verbose --tries=1 --spider localhost:7474 || exit 1"]
         interval: 5s
         timeout: 3s
         retries: 5
   ```

   > [!NOTE]
   >
   > 要了解有关 Neo4j 的更多信息，请参阅 [Neo4j 官方 Docker 镜像](https://hub.docker.com/_/neo4j)。

4. 运行应用程序。在 `docker-genai-sample` 目录中，
   在终端中运行以下命令。

   ```console
   $ docker compose up --build
   ```

5. 访问应用程序。打开浏览器并访问 [http://localhost:8000](http://localhost:8000) 上的应用程序。您应该看到一个简单的 Streamlit 应用程序。请注意，向 PDF 提问会导致应用程序失败，因为 `.env` 文件中指定的 LLM 服务尚未运行。

6. 停止应用程序。在终端中，按 `ctrl`+`c` 停止应用程序。

## 添加本地或远程 LLM 服务

示例应用程序支持 [Ollama](https://ollama.ai/) 和 [OpenAI](https://openai.com/)。本指南为以下场景提供说明：

- 在容器中运行 Ollama
- 在容器外运行 Ollama
- 使用 OpenAI

虽然所有平台都可以使用上述任何场景，但性能和 GPU 支持可能会有所不同。您可以使用以下指南帮助您选择适当的选项：

- 如果您使用的是 Linux 和 Docker Engine 的原生安装，或 Windows 10/11 和 Docker Desktop，并且您有支持 CUDA 的 GPU，且系统至少有 8 GB RAM，请在容器中运行 Ollama。
- 如果您使用的是 Apple silicon Mac，请在容器外运行 Ollama。
- 如果前两个场景不适用于您，请使用 OpenAI。

为您的 LLM 服务选择以下选项之一。








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
    
      <button
        class="tab-item"
        :class="selected === '%E4%BD%BF%E7%94%A8-OpenAI' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = '%E4%BD%BF%E7%94%A8-OpenAI'"
        
      >
        使用 OpenAI
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== '%E5%9C%A8%E5%AE%B9%E5%99%A8%E4%B8%AD%E8%BF%90%E8%A1%8C-Ollama' && 'hidden'"
      >
        <p>在容器中运行 Ollama 时，您应该有一个支持 CUDA 的 GPU。虽然您可以在没有支持 GPU 的容器中运行 Ollama，但性能可能不可接受。只有 Linux 和 Windows 11 支持容器的 GPU 访问。</p>
<p>要在容器中运行 Ollama 并提供 GPU 访问：</p>
<ol>
<li>
<p>安装先决条件。</p>
<ul>
<li>对于 Linux 上的 Docker Engine，安装 <a class="link" href="https://github.com/NVIDIA/nvidia-container-toolkit" rel="noopener">NVIDIA Container Toolkit</a>。</li>
<li>对于 Windows 10/11 上的 Docker Desktop，安装最新的 <a class="link" href="https://www.nvidia.com/Download/index.aspx" rel="noopener">NVIDIA 驱动程序</a>，并确保您使用的是 
    
  
  <a class="link" href="/desktop/features/wsl/#turn-on-docker-desktop-wsl-2">WSL2 后端</a></li>
</ul>
</li>
<li>
<p>在 <code>compose.yaml</code> 中添加 Ollama 服务和卷。以下是
更新后的 <code>compose.yaml</code>：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'c2VydmljZXM6CiAgc2VydmVyOgogICAgYnVpbGQ6CiAgICAgIGNvbnRleHQ6IC4KICAgIHBvcnRzOgogICAgICAtIDgwMDA6ODAwMAogICAgZW52X2ZpbGU6CiAgICAgIC0gLmVudgogICAgZGVwZW5kc19vbjoKICAgICAgZGF0YWJhc2U6CiAgICAgICAgY29uZGl0aW9uOiBzZXJ2aWNlX2hlYWx0aHkKICBkYXRhYmFzZToKICAgIGltYWdlOiBuZW80ajo1LjExCiAgICBwb3J0czoKICAgICAgLSAiNzQ3NDo3NDc0IgogICAgICAtICI3Njg3Ojc2ODciCiAgICBlbnZpcm9ubWVudDoKICAgICAgLSBORU80Sl9BVVRIPSR7TkVPNEpfVVNFUk5BTUV9LyR7TkVPNEpfUEFTU1dPUkR9CiAgICBoZWFsdGhjaGVjazoKICAgICAgdGVzdDoKICAgICAgICBbCiAgICAgICAgICAiQ01ELVNIRUxMIiwKICAgICAgICAgICJ3Z2V0IC0tbm8tdmVyYm9zZSAtLXRyaWVzPTEgLS1zcGlkZXIgbG9jYWxob3N0Ojc0NzQgfHwgZXhpdCAxIiwKICAgICAgICBdCiAgICAgIGludGVydmFsOiA1cwogICAgICB0aW1lb3V0OiAzcwogICAgICByZXRyaWVzOiA1CiAgb2xsYW1hOgogICAgaW1hZ2U6IG9sbGFtYS9vbGxhbWE6bGF0ZXN0CiAgICBwb3J0czoKICAgICAgLSAiMTE0MzQ6MTE0MzQiCiAgICB2b2x1bWVzOgogICAgICAtIG9sbGFtYV92b2x1bWU6L3Jvb3QvLm9sbGFtYQogICAgZGVwbG95OgogICAgICByZXNvdXJjZXM6CiAgICAgICAgcmVzZXJ2YXRpb25zOgogICAgICAgICAgZGV2aWNlczoKICAgICAgICAgICAgLSBkcml2ZXI6IG52aWRpYQogICAgICAgICAgICAgIGNvdW50OiBhbGwKICAgICAgICAgICAgICBjYXBhYmlsaXRpZXM6IFtncHVdCnZvbHVtZXM6CiAgb2xsYW1hX3ZvbHVtZTo=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-yaml" data-lang="yaml"><span class="line"><span class="cl"><span class="nt">services</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">  </span><span class="nt">server</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">    </span><span class="nt">build</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">      </span><span class="nt">context</span><span class="p">:</span><span class="w"> </span><span class="l">.</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">    </span><span class="nt">ports</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">      </span>- <span class="m">8000</span><span class="p">:</span><span class="m">8000</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">    </span><span class="nt">env_file</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">      </span>- <span class="l">.env</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">    </span><span class="nt">depends_on</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">      </span><span class="nt">database</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">        </span><span class="nt">condition</span><span class="p">:</span><span class="w"> </span><span class="l">service_healthy</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">  </span><span class="nt">database</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">    </span><span class="nt">image</span><span class="p">:</span><span class="w"> </span><span class="l">neo4j:5.11</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">    </span><span class="nt">ports</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">      </span>- <span class="s2">&#34;7474:7474&#34;</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">      </span>- <span class="s2">&#34;7687:7687&#34;</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">    </span><span class="nt">environment</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">      </span>- <span class="l">NEO4J_AUTH=${NEO4J_USERNAME}/${NEO4J_PASSWORD}</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">    </span><span class="nt">healthcheck</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">      </span><span class="nt">test</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">        </span><span class="p">[</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">          </span><span class="s2">&#34;CMD-SHELL&#34;</span><span class="p">,</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">          </span><span class="s2">&#34;wget --no-verbose --tries=1 --spider localhost:7474 || exit 1&#34;</span><span class="p">,</span><span class="w">
</span></span></span><span class="line hl"><span class="cl"><span class="w">        </span><span class="p">]</span><span class="w">
</span></span></span><span class="line hl"><span class="cl"><span class="w">      </span><span class="nt">interval</span><span class="p">:</span><span class="w"> </span><span class="l">5s</span><span class="w">
</span></span></span><span class="line hl"><span class="cl"><span class="w">      </span><span class="nt">timeout</span><span class="p">:</span><span class="w"> </span><span class="l">3s</span><span class="w">
</span></span></span><span class="line hl"><span class="cl"><span class="w">      </span><span class="nt">retries</span><span class="p">:</span><span class="w"> </span><span class="m">5</span><span class="w">
</span></span></span><span class="line hl"><span class="cl"><span class="w">  </span><span class="nt">ollama</span><span class="p">:</span><span class="w">
</span></span></span><span class="line hl"><span class="cl"><span class="w">    </span><span class="nt">image</span><span class="p">:</span><span class="w"> </span><span class="l">ollama/ollama:latest</span><span class="w">
</span></span></span><span class="line hl"><span class="cl"><span class="w">    </span><span class="nt">ports</span><span class="p">:</span><span class="w">
</span></span></span><span class="line hl"><span class="cl"><span class="w">      </span>- <span class="s2">&#34;11434:11434&#34;</span><span class="w">
</span></span></span><span class="line hl"><span class="cl"><span class="w">    </span><span class="nt">volumes</span><span class="p">:</span><span class="w">
</span></span></span><span class="line hl"><span class="cl"><span class="w">      </span>- <span class="l">ollama_volume:/root/.ollama</span><span class="w">
</span></span></span><span class="line hl"><span class="cl"><span class="w">    </span><span class="nt">deploy</span><span class="p">:</span><span class="w">
</span></span></span><span class="line hl"><span class="cl"><span class="w">      </span><span class="nt">resources</span><span class="p">:</span><span class="w">
</span></span></span><span class="line hl"><span class="cl"><span class="w">        </span><span class="nt">reservations</span><span class="p">:</span><span class="w">
</span></span></span><span class="line hl"><span class="cl"><span class="w">          </span><span class="nt">devices</span><span class="p">:</span><span class="w">
</span></span></span><span class="line hl"><span class="cl"><span class="w">            </span>- <span class="nt">driver</span><span class="p">:</span><span class="w"> </span><span class="l">nvidia</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">              </span><span class="nt">count</span><span class="p">:</span><span class="w"> </span><span class="l">all</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">              </span><span class="nt">capabilities</span><span class="p">:</span><span class="w"> </span><span class="p">[</span><span class="l">gpu]</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="nt">volumes</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">  </span><span class="l">ollama_volume:</span></span></span></code></pre></div>
      
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
<p>在 <code>compose.yaml</code> 文件中添加 ollama-pull 服务。此服务使用
<code>docker/genai:ollama-pull</code> 镜像，基于 GenAI Stack 的
<a class="link" href="https://github.com/docker/genai-stack/blob/main/pull_model.Dockerfile" rel="noopener">pull_model.Dockerfile</a>。
该服务将自动为您的 Ollama 容器拉取模型。以下是 <code>compose.yaml</code> 文件的更新部分：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'c2VydmljZXM6CiAgc2VydmVyOgogICAgYnVpbGQ6CiAgICAgIGNvbnRleHQ6IC4KICAgIHBvcnRzOgogICAgICAtIDgwMDA6ODAwMAogICAgZW52X2ZpbGU6CiAgICAgIC0gLmVudgogICAgZGVwZW5kc19vbjoKICAgICAgZGF0YWJhc2U6CiAgICAgICAgY29uZGl0aW9uOiBzZXJ2aWNlX2hlYWx0aHkKICAgICAgb2xsYW1hLXB1bGw6CiAgICAgICAgY29uZGl0aW9uOiBzZXJ2aWNlX2NvbXBsZXRlZF9zdWNjZXNzZnVsbHkKICBvbGxhbWEtcHVsbDoKICAgIGltYWdlOiBkb2NrZXIvZ2VuYWk6b2xsYW1hLXB1bGwKICAgIGVudl9maWxlOgogICAgICAtIC5lbnYKICAjIC4uLg==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-yaml" data-lang="yaml"><span class="line"><span class="cl"><span class="nt">services</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">  </span><span class="nt">server</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">    </span><span class="nt">build</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">      </span><span class="nt">context</span><span class="p">:</span><span class="w"> </span><span class="l">.</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">    </span><span class="nt">ports</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">      </span>- <span class="m">8000</span><span class="p">:</span><span class="m">8000</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">    </span><span class="nt">env_file</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">      </span>- <span class="l">.env</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">    </span><span class="nt">depends_on</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">      </span><span class="nt">database</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">        </span><span class="nt">condition</span><span class="p">:</span><span class="w"> </span><span class="l">service_healthy</span><span class="w">
</span></span></span><span class="line hl"><span class="cl"><span class="w">      </span><span class="nt">ollama-pull</span><span class="p">:</span><span class="w">
</span></span></span><span class="line hl"><span class="cl"><span class="w">        </span><span class="nt">condition</span><span class="p">:</span><span class="w"> </span><span class="l">service_completed_successfully</span><span class="w">
</span></span></span><span class="line hl"><span class="cl"><span class="w">  </span><span class="nt">ollama-pull</span><span class="p">:</span><span class="w">
</span></span></span><span class="line hl"><span class="cl"><span class="w">    </span><span class="nt">image</span><span class="p">:</span><span class="w"> </span><span class="l">docker/genai:ollama-pull</span><span class="w">
</span></span></span><span class="line hl"><span class="cl"><span class="w">    </span><span class="nt">env_file</span><span class="p">:</span><span class="w">
</span></span></span><span class="line hl"><span class="cl"><span class="w">      </span>- <span class="l">.env</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">  </span><span class="c"># ...</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
</li>
</ol>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== '%E5%9C%A8%E5%AE%B9%E5%99%A8%E5%A4%96%E8%BF%90%E8%A1%8C-Ollama' && 'hidden'"
      >
        <p>要在容器外运行 Ollama：</p>
<ol>
<li><a class="link" href="https://github.com/jmorganca/ollama" rel="noopener">安装</a> 并在您的主机上运行 Ollama。</li>
<li>在 <code>.env</code> 文件中更新 <code>OLLAMA_BASE_URL</code> 值为
<code>http://host.docker.internal:11434</code>。</li>
<li>使用以下命令将模型拉取到 Ollama。
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
</ol>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== '%E4%BD%BF%E7%94%A8-OpenAI' && 'hidden'"
      >
        

  

  <blockquote
    
    class="admonition admonition-note admonition not-prose">
    <div class="admonition-header">
      <span class="admonition-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M12 8V12M12 16H12.01M7.8 21H16.2C17.8802 21 18.7202 21 19.362 20.673C19.9265 20.3854 20.3854 19.9265 20.673 19.362C21 18.7202 21 17.8802 21 16.2V7.8C21 6.11984 21 5.27976 20.673 4.63803C20.3854 4.07354 19.9265 3.6146 19.362 3.32698C18.7202 3 17.8802 3 16.2 3H7.8C6.11984 3 5.27976 3 4.63803 3.32698C4.07354 3.6146 3.6146 4.07354 3.32698 4.63803C3 5.27976 3 6.11984 3 7.8V16.2C3 17.8802 3 18.7202 3.32698 19.362C3.6146 19.9265 4.07354 20.3854 4.63803 20.673C5.27976 21 6.11984 21 7.8 21Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>

      </span>
      <span class="admonition-title">
        Important
      </span>
    </div>
    <div class="admonition-content">
      <p>使用 OpenAI 需要 <a class="link" href="https://platform.openai.com/login" rel="noopener">OpenAI 账户</a>。OpenAI 是第三方托管服务，可能会产生费用。</p>
    </div>
  </blockquote>

<ol>
<li>在 <code>.env</code> 文件中更新 <code>LLM</code> 值为
<code>gpt-3.5</code>。</li>
<li>取消注释并更新 <code>.env</code> 文件中的 <code>OPENAI_API_KEY</code> 值
为您的 <a class="link" href="https://help.openai.com/en/articles/4936850-where-do-i-find-my-api-key" rel="noopener">OpenAI API 密钥</a>。</li>
</ol>

      </div>
    
  </div>
</div>


## 运行您的 GenAI 应用程序

此时，您的 Compose 文件中包含以下服务：

- 用于主 GenAI 应用程序的服务器服务
- 用于在 Neo4j 数据库中存储向量的数据库服务
- （可选）用于运行 LLM 的 Ollama 服务
- （可选）用于自动为 Ollama 服务拉取模型的 Ollama-pull 服务

要运行所有服务，请在 `docker-genai-sample` 目录中运行以下命令：

```console
$ docker compose up --build
```

如果您的 Compose 文件包含 ollama-pull 服务，则 ollama-pull 服务可能需要几分钟才能拉取模型。ollama-pull 服务将持续更新控制台状态。拉取模型后，ollama-pull 服务容器将停止，您可以访问应用程序。

应用程序运行后，打开浏览器并访问 [http://localhost:8000](http://localhost:8000) 上的应用程序。

上传一个 PDF 文件，例如 [Docker CLI 速查表](https://docs.docker.com/get-started/docker_cheatsheet.pdf)，并询问有关 PDF 的问题。

根据您的系统和您选择的 LLM 服务，回答可能需要几分钟。如果您使用的是 Ollama 且性能不可接受，请尝试使用 OpenAI。

## 总结

在本节中，您学习了如何设置开发环境，以提供对 GenAI 应用程序所需的所有服务的访问。

相关信息：

- [Dockerfile 参考](../../../reference/dockerfile.md)
- [Compose 文件参考](/reference/compose-file/_index.md)
- [Ollama Docker 镜像](https://hub.docker.com/r/ollama/ollama)
- [Neo4j 官方 Docker 镜像](https://hub.docker.com/_/neo4j)
- [GenAI Stack 演示应用程序](https://github.com/docker/genai-stack)

## 下一步

在 [GenAI Stack 演示应用程序](https://github.com/docker/genai-stack) 中查看更多的 GenAI 应用程序示例。
