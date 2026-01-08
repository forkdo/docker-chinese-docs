# 将 Deno 应用程序容器化

## 先决条件

* 你有一个 [Git 客户端](https://git-scm.com/downloads)。本节中的示例使用的是基于命令行的 Git 客户端，但你可以使用任何客户端。

## 概览

长期以来，Node.js 一直是服务端 JavaScript 应用程序的首选运行时。然而，近年来出现了新的替代运行时，包括 [Deno](https://deno.land/)。与 Node.js 类似，Deno 也是一个 JavaScript 和 TypeScript 运行时，但它采用了全新的方法，具有现代安全特性、内置标准库以及对 TypeScript 的原生支持。

为什么要使用 Docker 开发 Deno 应用程序？拥有多种运行时选择令人兴奋，但在不同环境中一致地管理多个运行时及其依赖项可能很棘手。这正是 Docker 的价值所在。使用容器按需创建和销毁环境可以简化运行时管理并确保一致性。此外，随着 Deno 的不断发展，Docker 有助于建立一个可靠且可重现的开发环境，最大限度地减少设置挑战并简化工作流程。

## 获取示例应用程序

克隆示例应用程序以配合本指南使用。打开终端，切换到你想工作的目录，然后运行以下命令克隆仓库：

```console
$ git clone https://github.com/dockersamples/docker-deno.git && cd docker-deno
```

现在你的 `deno-docker` 目录中应该包含以下内容：

```text
├── deno-docker/
│ ├── compose.yml
│ ├── Dockerfile
│ ├── LICENSE
│ ├── server.ts
│ └── README.md
```

## 了解示例应用程序

示例应用程序是一个简单的 Deno 应用程序，它使用 Oak 框架创建一个返回 JSON 响应的简单 API。该应用程序监听 8000 端口，当你在浏览器中访问该应用程序时，会返回消息 `{"Status" : "OK"}`。

```typescript
// server.ts
import { Application, Router } from "https://deno.land/x/oak@v12.0.0/mod.ts";

const app = new Application();
const router = new Router();

// 定义一个返回 JSON 的路由
router.get("/", (context) => {
  context.response.body = { Status: "OK" };
  context.response.type = "application/json";
});

app.use(router.routes());
app.use(router.allowedMethods());

console.log("Server running on http://localhost:8000");
await app.listen({ port: 8000 });
```

## 创建 Dockerfile

在创建 Dockerfile 之前，你需要选择一个基础镜像。你可以使用 [Deno Docker 官方镜像](https://hub.docker.com/r/denoland/deno) 或来自 [Hardened Image 目录](https://hub.docker.com/hardened-images/catalog) 的 Docker Hardened Image (DHI)。

选择 DHI 的优势在于它是一个生产就绪的镜像，轻量且安全。更多信息，请参阅 [Docker Hardened Images](https://docs.docker.com/dhi/)。








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
        <p>Docker Hardened Images (DHIs) 在 <a class="link" href="https://hub.docker.com/hardened-images/catalog/dhi/deno" rel="noopener">Docker Hardened Images 目录</a> 中提供 Deno 版本。你可以直接从 <code>dhi.io</code> 注册表拉取 DHIs。</p>
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
<p>拉取 Deno DHI 作为 <code>dhi.io/deno:2</code>。此示例中的标签 (<code>2</code>) 指的是 Deno 最新 2.x 版本。</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBkb2NrZXIgcHVsbCBkaGkuaW8vZGVubzoy', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> docker pull dhi.io/deno:2
</span></span></code></pre></div>
      
    </div>
  </div>
</div>
</li>
</ol>
<p>有关其他可用版本，请参阅<a class="link" href="https://hub.docker.com/hardened-images/catalog/dhi/deno" rel="noopener">目录</a>。</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'IyDkvb/nlKggREhJIERlbm8g6ZWc5YOP5L2c5Li65Z&#43;656GA6ZWc5YOPCkZST00gZGhpLmlvL2Rlbm86MgoKIyDorr7nva7lt6XkvZznm67lvZUKV09SS0RJUiAvYXBwCgojIOWwhuacjeWKoeWZqOS7o&#43;eggeWkjeWItuWIsOWuueWZqOS4rQpDT1BZIHNlcnZlci50cyAuCgojIOiuvue9ruadg&#43;mZkO&#43;8iOWPr&#43;mAie&#43;8jOS9huWHuuS6juWuieWFqOiAg&#43;iZkeaOqOiNkO&#43;8iQpVU0VSIGRlbm8KCiMg5pq06ZyyIDgwMDAg56uv5Y&#43;jCkVYUE9TRSA4MDAwCgojIOi/kOihjCBEZW5vIOacjeWKoeWZqApDTUQgWyJydW4iLCAiLS1hbGxvdy1uZXQiLCAic2VydmVyLnRzIl0=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-dockerfile" data-lang="dockerfile"><span class="line"><span class="cl"><span class="c"># 使用 DHI Deno 镜像作为基础镜像</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">FROM</span><span class="w"> </span><span class="s">dhi.io/deno:2</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 设置工作目录</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">WORKDIR</span><span class="w"> </span><span class="s">/app</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 将服务器代码复制到容器中</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">COPY</span> server.ts .<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 设置权限（可选，但出于安全考虑推荐）</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">USER</span><span class="w"> </span><span class="s">deno</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 暴露 8000 端口</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">EXPOSE</span><span class="w"> </span><span class="s">8000</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 运行 Deno 服务器</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">CMD</span> <span class="p">[</span><span class="s2">&#34;run&#34;</span><span class="p">,</span> <span class="s2">&#34;--allow-net&#34;</span><span class="p">,</span> <span class="s2">&#34;server.ts&#34;</span><span class="p">]</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== '%E4%BD%BF%E7%94%A8%E5%AE%98%E6%96%B9%E9%95%9C%E5%83%8F' && 'hidden'"
      >
        <p>使用 Docker 官方镜像很简单。在以下 Dockerfile 中，你会注意到 <code>FROM</code> 指令使用 <code>denoland/deno:latest</code> 作为基础镜像。</p>
<p>这是 Deno 的官方镜像。该镜像<a class="link" href="https://hub.docker.com/r/denoland/deno" rel="noopener">可在 Docker Hub 上获得</a>。</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'IyDkvb/nlKjlrpjmlrkgRGVubyDplZzlg48KRlJPTSBkZW5vbGFuZC9kZW5vOmxhdGVzdAoKIyDorr7nva7lt6XkvZznm67lvZUKV09SS0RJUiAvYXBwCgojIOWwhuacjeWKoeWZqOS7o&#43;eggeWkjeWItuWIsOWuueWZqOS4rQpDT1BZIHNlcnZlci50cyAuCgojIOiuvue9ruadg&#43;mZkO&#43;8iOWPr&#43;mAie&#43;8jOS9huWHuuS6juWuieWFqOiAg&#43;iZkeaOqOiNkO&#43;8iQpVU0VSIGRlbm8KCiMg5pq06ZyyIDgwMDAg56uv5Y&#43;jCkVYUE9TRSA4MDAwCgojIOi/kOihjCBEZW5vIOacjeWKoeWZqApDTUQgWyJydW4iLCAiLS1hbGxvdy1uZXQiLCAic2VydmVyLnRzIl0=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-dockerfile" data-lang="dockerfile"><span class="line"><span class="cl"><span class="c"># 使用官方 Deno 镜像</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">FROM</span><span class="w"> </span><span class="s">denoland/deno:latest</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 设置工作目录</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">WORKDIR</span><span class="w"> </span><span class="s">/app</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 将服务器代码复制到容器中</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">COPY</span> server.ts .<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 设置权限（可选，但出于安全考虑推荐）</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">USER</span><span class="w"> </span><span class="s">deno</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 暴露 8000 端口</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">EXPOSE</span><span class="w"> </span><span class="s">8000</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 运行 Deno 服务器</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">CMD</span> <span class="p">[</span><span class="s2">&#34;run&#34;</span><span class="p">,</span> <span class="s2">&#34;--allow-net&#34;</span><span class="p">,</span> <span class="s2">&#34;server.ts&#34;</span><span class="p">]</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
  </div>
</div>


除了指定基础镜像外，Dockerfile 还：

- 将容器中的工作目录设置为 `/app`。
- 将 `server.ts` 复制到容器中。
- 将用户设置为 `deno`，以非 root 用户身份运行应用程序。
- 暴露 8000 端口以允许访问应用程序的流量。
- 使用 `CMD` 指令运行 Deno 服务器。
- 使用 `--allow-net` 标志允许应用程序的网络访问。`server.ts` 文件使用 Oak 框架创建一个监听 8000 端口的简单 API。

## 运行应用程序

确保你在 `deno-docker` 目录中。在终端中运行以下命令来构建并运行应用程序。

```console
$ docker compose up --build
```

打开浏览器并访问 [http://localhost:8000](http://localhost:8000) 查看应用程序。你将在浏览器中看到消息 `{"Status" : "OK"}`。

在终端中，按 `ctrl`+`c` 停止应用程序。

### 在后台运行应用程序

你可以通过添加 `-d` 选项使应用程序在终端后台运行。在 `deno-docker` 目录中，在终端中运行以下命令。

```console
$ docker compose up --build -d
```

打开浏览器并访问 [http://localhost:8000](http://localhost:8000) 查看应用程序。

在终端中，运行以下命令停止应用程序。

```console
$ docker compose down
```

## 总结

在本节中，你学习了如何使用 Docker 容器化并运行你的 Deno 应用程序。

相关信息：

 - [Dockerfile 参考](/reference/dockerfile.md)
 - [.dockerignore 文件](/reference/dockerfile.md#dockerignore-file)
 - [Docker Compose 概览](/manuals/compose/_index.md)
 - [Compose 文件参考](/reference/compose-file/_index.md)
 - [Docker Hardened Images](/dhi/)

## 下一步

在下一节中，你将学习如何使用容器开发你的应用程序。
