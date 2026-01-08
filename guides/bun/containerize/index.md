# 容器化 Bun 应用程序

## 先决条件

* 您拥有 [Git 客户端](https://git-scm.com/downloads)。本节中的示例使用基于命令行的 Git 客户端，但您可以使用任何客户端。

## 概述

长期以来，Node.js 一直是服务器端 JavaScript 应用程序的事实标准运行时。近年来，生态系统中出现了许多新的替代运行时，包括 [Bun 网站](https://bun.sh/)。与 Node.js 一样，Bun 是一个 JavaScript 运行时。Bun 是一个相对轻量级的运行时，旨在快速且高效。

为什么使用 Docker 开发 Bun 应用程序？拥有多种运行时可供选择固然很棒。但随着运行时数量的增加，在不同环境中一致地管理不同的运行时及其依赖项变得具有挑战性。这正是 Docker 的用武之地。按需创建和销毁容器是管理不同运行时及其依赖项的绝佳方式。此外，由于它是一个相当新的运行时，为 Bun 建立一致的开发环境可能具有挑战性。Docker 可以帮助您为 Bun 建立一致的开发环境。

## 获取示例应用程序

克隆示例应用程序以供本指南使用。打开终端，切换到您想要工作的目录，然后运行以下命令来克隆存储库：

```console
$ git clone https://github.com/dockersamples/bun-docker.git && cd bun-docker
```

现在，您的 `bun-docker` 目录中应包含以下内容。

```text
├── bun-docker/
│ ├── compose.yml
│ ├── Dockerfile
│ ├── LICENSE
│ ├── server.js
│ └── README.md
```

## 创建 Dockerfile

在创建 Dockerfile 之前，您需要选择一个基础镜像。您可以使用 [Bun Docker 官方镜像](https://hub.docker.com/r/oven/bun) 或来自 [Hardened Image 目录](https://hub.docker.com/hardened-images/catalog) 的 Docker Hardened Image (DHI)。

选择 DHI 的优势在于它提供了生产就绪、轻量级且安全的镜像。更多信息，请参阅 [Docker Hardened Images](https://docs.docker.com/dhi/)。








<div
  class="tabs"
  
    x-data="{ selected: '%E4%BD%BF%E7%94%A8-Docker-Hardened-Images' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === '%E4%BD%BF%E7%94%A8-Docker-Hardened-Images' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = '%E4%BD%BF%E7%94%A8-Docker-Hardened-Images'"
        
      >
        使用 Docker Hardened Images
      </button>
    
      <button
        class="tab-item"
        :class="selected === '%E4%BD%BF%E7%94%A8%E5%AE%98%E6%96%B9%E9%95%9C%E5%83%8F' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = '%E4%BD%BF%E7%94%A8%E5%AE%98%E6%96%B9%E9%95%9C%E5%83%8F'"
        
      >
        使用官方镜像
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== '%E4%BD%BF%E7%94%A8-Docker-Hardened-Images' && 'hidden'"
      >
        <p>Docker Hardened Images (DHIs) 可在 <a class="link" href="https://hub.docker.com/hardened-images/catalog/dhi/bun" rel="noopener">Docker Hardened Images 目录</a> 中找到。您可以直接从 <code>dhi.io</code> 注册表拉取 DHIs。</p>
<ol>
<li>
<p>登录 DHI 注册表：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBkb2NrZXIgbG9naW4gZGhpLmlv', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> docker login dhi.io
</span></span></code></pre></div>
      
    </div>
  </div>
</div>
</li>
<li>
<p>将 Bun DHI 拉取为 <code>dhi.io/bun:1</code>。此示例中的标签 (<code>1</code>) 指的是 Bun 的最新 1.x 版本。</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBkb2NrZXIgcHVsbCBkaGkuaW8vYnVuOjE=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> docker pull dhi.io/bun:1
</span></span></code></pre></div>
      
    </div>
  </div>
</div>
</li>
</ol>
<p>有关其他可用版本，请参阅 <a class="link" href="https://hub.docker.com/hardened-images/catalog/dhi/bun" rel="noopener">目录</a>。</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'IyDkvb/nlKggREhJIEJ1biDplZzlg4/kvZzkuLrln7rnoYDplZzlg48KRlJPTSBkaGkuaW8vYnVuOjEKCiMg6K6&#43;572u5a655Zmo5Lit55qE5bel5L2c55uu5b2VCldPUktESVIgL2FwcAoKIyDlsIblvZPliY3nm67lvZXnmoTlhoXlrrnlpI3liLbliLDlrrnlmajkuK3nmoQgL2FwcApDT1BZIC4gLgoKIyDmmrTpnLIgQVBJIOWwhuebkeWQrOeahOerr&#43;WPowpFWFBPU0UgMzAwMAoKIyDlnKjlrrnlmajlkK/liqjml7bov5DooYzmnI3liqHlmagKQ01EIFsiYnVuIiwgInNlcnZlci5qcyJd', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-dockerfile" data-lang="dockerfile"><span class="line"><span class="cl"><span class="c"># 使用 DHI Bun 镜像作为基础镜像</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">FROM</span><span class="w"> </span><span class="s">dhi.io/bun:1</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 设置容器中的工作目录</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">WORKDIR</span><span class="w"> </span><span class="s">/app</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 将当前目录的内容复制到容器中的 /app</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">COPY</span> . .<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 暴露 API 将监听的端口</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">EXPOSE</span><span class="w"> </span><span class="s">3000</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 在容器启动时运行服务器</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">CMD</span> <span class="p">[</span><span class="s2">&#34;bun&#34;</span><span class="p">,</span> <span class="s2">&#34;server.js&#34;</span><span class="p">]</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== '%E4%BD%BF%E7%94%A8%E5%AE%98%E6%96%B9%E9%95%9C%E5%83%8F' && 'hidden'"
      >
        <p>使用 Docker 官方镜像非常简单。在下面的 Dockerfile 中，您会注意到 <code>FROM</code> 指令使用 <code>oven/bun</code> 作为基础镜像。</p>
<p>您可以在 <a class="link" href="https://hub.docker.com/r/oven/bun" rel="noopener">Docker Hub</a> 上找到该镜像。这是由 Bun 背后的公司 Oven 创建的 Bun 的 Docker 官方镜像，并且可在 Docker Hub 上使用。</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'IyDkvb/nlKjlrpjmlrnnmoQgQnVuIOmVnOWDjwpGUk9NIG92ZW4vYnVuOmxhdGVzdAoKIyDorr7nva7lrrnlmajkuK3nmoTlt6XkvZznm67lvZUKV09SS0RJUiAvYXBwCgojIOWwhuW9k&#43;WJjeebruW9leeahOWGheWuueWkjeWItuWIsOWuueWZqOS4reeahCAvYXBwCkNPUFkgLiAuCgojIOaatOmcsiBBUEkg5bCG55uR5ZCs55qE56uv5Y&#43;jCkVYUE9TRSAzMDAwCgojIOWcqOWuueWZqOWQr&#43;WKqOaXtui/kOihjOacjeWKoeWZqApDTUQgWyJidW4iLCAic2VydmVyLmpzIl0=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-dockerfile" data-lang="dockerfile"><span class="line"><span class="cl"><span class="c"># 使用官方的 Bun 镜像</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">FROM</span><span class="w"> </span><span class="s">oven/bun:latest</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 设置容器中的工作目录</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">WORKDIR</span><span class="w"> </span><span class="s">/app</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 将当前目录的内容复制到容器中的 /app</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">COPY</span> . .<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 暴露 API 将监听的端口</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">EXPOSE</span><span class="w"> </span><span class="s">3000</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 在容器启动时运行服务器</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">CMD</span> <span class="p">[</span><span class="s2">&#34;bun&#34;</span><span class="p">,</span> <span class="s2">&#34;server.js&#34;</span><span class="p">]</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
  </div>
</div>


除了指定基础镜像之外，Dockerfile 还：

- 将容器中的工作目录设置为 `/app`。
- 将当前目录的内容复制到容器中的 `/app` 目录。
- 暴露 API 正在监听请求的端口 3000。
- 最后，在容器启动时使用命令 `bun server.js` 启动服务器。

## 运行应用程序

在 `bun-docker` 目录中，在终端中运行以下命令。

```console
$ docker compose up --build
```

打开浏览器，在 [http://localhost:3000](http://localhost:3000) 查看应用程序。您将在浏览器中看到消息 `{"Status" : "OK"}`。

在终端中，按 `ctrl`+`c` 停止应用程序。

### 在后台运行应用程序

您可以通过添加 `-d` 选项在终端后台运行应用程序。在 `bun-docker` 目录中，在终端中运行以下命令。

```console
$ docker compose up --build -d
```

打开浏览器，在 [http://localhost:3000](http://localhost:3000) 查看应用程序。

在终端中，运行以下命令停止应用程序。

```console
$ docker compose down
```

## 总结

在本节中，您学习了如何使用 Docker 容器化并运行您的 Bun 应用程序。

相关信息：

 - [Dockerfile 参考](/reference/dockerfile.md)
 - [.dockerignore 文件](/reference/dockerfile.md#dockerignore-file)
 - [Docker Compose 概述](/manuals/compose/_index.md)
 - [Compose 文件参考](/reference/compose-file/_index.md)
 - [Docker Hardened Images](/dhi/)

## 下一步

在下一节中，您将学习如何使用容器开发您的应用程序。
