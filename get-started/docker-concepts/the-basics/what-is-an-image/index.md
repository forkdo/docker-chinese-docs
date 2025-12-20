# 什么是镜像？

<div id="youtube-player-NyvT9REqLe4" data-video-id="NyvT9REqLe4" class="youtube-video aspect-video h-fit w-full py-2">
</div>


## 解释

鉴于[容器](./what-is-a-container.md)是一个隔离的进程，那么它的文件和配置从何而来？又该如何共享这些环境？

这就是容器镜像发挥作用的地方。容器镜像是一个标准化的软件包，其中包含运行容器所需的所有文件、二进制文件、库和配置。

对于一个 [PostgreSQL](https://hub.docker.com/_/postgres) 镜像，该镜像会打包数据库二进制文件、配置文件和其他依赖项。对于一个 Python Web 应用，它会包含 Python 运行时、你的应用代码及其所有依赖项。

镜像有两个重要的原则：

1.  **镜像是不可变的**。镜像一旦创建，就无法修改。你只能创建一个新镜像，或者在现有镜像之上添加更改。
2.  **容器镜像由多个层组成**。每层代表一组文件系统的更改，包括添加、删除或修改文件。

这两个原则让你能够扩展现有的镜像或在其基础上添加内容。例如，如果你正在构建一个 Python 应用，可以从 [Python 镜像](https://hub.docker.com/_/python)开始，然后添加额外的层来安装应用的依赖项并添加你的代码。这样你就可以专注于应用本身，而不是 Python。

### 查找镜像

[Docker Hub](https://hub.docker.com) 是用于存储和分发镜像的默认全球市场。它拥有超过 100,000 个由开发者创建的镜像，你可以在本地运行。你可以直接从 Docker Desktop 搜索 Docker Hub 镜像并运行它们。

Docker Hub 提供了各种 Docker 支持和认可的镜像，称为 Docker Trusted Content（Docker 受信任内容）。这些镜像提供了完全托管的服务，或者作为你自己镜像的绝佳起点。这些包括：

- [Docker 官方镜像](https://hub.docker.com/search?badges=official) - 一组精心策划的 Docker 仓库，是大多数用户的起点，也是 Docker Hub 上最安全的镜像之一。
- [Docker 验证发布者](https://hub.docker.com/search?badges=verified_publisher) - 由 Docker 验证的商业发布者提供的高质量镜像。
- [Docker 赞助的开源项目](https://hub.docker.com/search?badges=open_source) - 由通过 Docker 开源计划获得赞助的开源项目发布和维护的镜像。

例如，[Redis](https://hub.docker.com/_/redis) 和 [Memcached](https://hub.docker.com/_/memcached) 是几个流行的、开箱即用的 Docker 官方镜像。你可以下载这些镜像，并在几秒钟内启动和运行这些服务。还有一些基础镜像，例如 [Node.js](https://hub.docker.com/_/node) Docker 镜像，你可以将其作为起点，并添加你自己的文件和配置。

## 动手尝试








<div
  class="tabs"
  
    
      x-data="{ selected: $persist('%E4%BD%BF%E7%94%A8-GUI').as('tabgroup-concept-usage') }"
    
    @tab-select.window="$event.detail.group === 'concept-usage' ? selected =
    $event.detail.name : null"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === '%E4%BD%BF%E7%94%A8-GUI' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'concept-usage', name:
          '%E4%BD%BF%E7%94%A8-GUI'})"
        
      >
        使用 GUI
      </button>
    
      <button
        class="tab-item"
        :class="selected === '%E4%BD%BF%E7%94%A8-CLI' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'concept-usage', name:
          '%E4%BD%BF%E7%94%A8-CLI'})"
        
      >
        使用 CLI
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== '%E4%BD%BF%E7%94%A8-GUI' && 'hidden'"
      >
        <p>在这个动手实践中，你将学习如何使用 Docker Desktop GUI 搜索和拉取容器镜像。</p>

<h3 class=" scroll-mt-20 flex items-center gap-2" id="搜索并下载镜像">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e6%90%9c%e7%b4%a2%e5%b9%b6%e4%b8%8b%e8%bd%bd%e9%95%9c%e5%83%8f">
    搜索并下载镜像
  </a>
</h3>

<ol>
<li>打开 Docker Desktop 仪表板，在左侧导航菜单中选择 **Images（镜像）**视图。</li>
</ol>

  
  
    








<figure
  x-data="{ zoom: false }"
  @click="zoom = ! zoom"
  class="cursor-pointer hover:opacity-90"
>
  <img
    loading="lazy"
    src="/get-started/docker-concepts/the-basics/images/click-image.webp"
    alt="Docker Desktop 仪表板的截图，显示左侧边栏中的镜像视图"
    width="1050"
    height="400"
    class="mx-auto
      border border-divider-light dark:border-divider-dark
     rounded-sm"
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
        src="/get-started/docker-concepts/the-basics/images/click-image.webp"
        alt="Docker Desktop 仪表板的截图，显示左侧边栏中的镜像视图"
      />
    </div>
  </template>
</figure>
<ol start="2">
<li>选择 **Search images to run（搜索要运行的镜像）**按钮。如果看不到该按钮，请选择屏幕顶部的<em>全局搜索栏</em>。</li>
</ol>

  
  
    








<figure
  x-data="{ zoom: false }"
  @click="zoom = ! zoom"
  class="cursor-pointer hover:opacity-90"
>
  <img
    loading="lazy"
    src="/get-started/docker-concepts/the-basics/images/search-image.webp"
    alt="Docker Desktop 仪表板的截图，显示搜索标签"
    
    
    class="mx-auto
      border border-divider-light dark:border-divider-dark
     rounded-sm"
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
        src="/get-started/docker-concepts/the-basics/images/search-image.webp"
        alt="Docker Desktop 仪表板的截图，显示搜索标签"
      />
    </div>
  </template>
</figure>
<ol start="3">
<li>在 **Search（搜索）**字段中，输入 &quot;welcome-to-docker&quot;。搜索完成后，选择 <code>docker/welcome-to-docker</code> 镜像。</li>
</ol>

  
  
    








<figure
  x-data="{ zoom: false }"
  @click="zoom = ! zoom"
  class="cursor-pointer hover:opacity-90"
>
  <img
    loading="lazy"
    src="/get-started/docker-concepts/the-basics/images/select-image.webp"
    alt="Docker Desktop 仪表板的截图，显示 docker/welcome-to-docker 镜像的搜索结果"
    width="1050"
    height="400"
    class="mx-auto
      border border-divider-light dark:border-divider-dark
     rounded-sm"
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
        src="/get-started/docker-concepts/the-basics/images/select-image.webp"
        alt="Docker Desktop 仪表板的截图，显示 docker/welcome-to-docker 镜像的搜索结果"
      />
    </div>
  </template>
</figure>
<ol start="4">
<li>选择 **Pull（拉取）**以下载镜像。</li>
</ol>

<h3 class=" scroll-mt-20 flex items-center gap-2" id="了解镜像">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e4%ba%86%e8%a7%a3%e9%95%9c%e5%83%8f">
    了解镜像
  </a>
</h3>

<p>下载镜像后，你可以通过 GUI 或 CLI 了解镜像的许多详细信息。</p>
<ol>
<li>在 Docker Desktop 仪表板中，选择 **Images（镜像）**视图。</li>
<li>选择 <strong>docker/welcome-to-docker</strong> 镜像以打开镜像的详细信息。</li>
</ol>

  
  
    








<figure
  x-data="{ zoom: false }"
  @click="zoom = ! zoom"
  class="cursor-pointer hover:opacity-90"
>
  <img
    loading="lazy"
    src="/get-started/docker-concepts/the-basics/images/pulled-image.webp"
    alt="Docker Desktop 仪表板的截图，显示镜像视图，箭头指向 docker/welcome-to-docker 镜像"
    width="1050"
    height="400"
    class="mx-auto
      border border-divider-light dark:border-divider-dark
     rounded-sm"
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
        src="/get-started/docker-concepts/the-basics/images/pulled-image.webp"
        alt="Docker Desktop 仪表板的截图，显示镜像视图，箭头指向 docker/welcome-to-docker 镜像"
      />
    </div>
  </template>
</figure>
<ol start="3">
<li>镜像详情页面会显示有关镜像层、镜像中安装的软件包和库以及任何已发现漏洞的信息。</li>
</ol>

  
  
    








<figure
  x-data="{ zoom: false }"
  @click="zoom = ! zoom"
  class="cursor-pointer hover:opacity-90"
>
  <img
    loading="lazy"
    src="/get-started/docker-concepts/the-basics/images/image-layers.webp"
    alt="docker/welcome-to-docker 镜像的镜像详情视图截图"
    width="1050"
    height="400"
    class="mx-auto
      border border-divider-light dark:border-divider-dark
     rounded-sm"
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
        src="/get-started/docker-concepts/the-basics/images/image-layers.webp"
        alt="docker/welcome-to-docker 镜像的镜像详情视图截图"
      />
    </div>
  </template>
</figure>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== '%E4%BD%BF%E7%94%A8-CLI' && 'hidden'"
      >
        <p>按照以下说明使用 CLI 搜索和拉取 Docker 镜像，并查看其层。</p>

<h3 class=" scroll-mt-20 flex items-center gap-2" id="搜索并下载镜像">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e6%90%9c%e7%b4%a2%e5%b9%b6%e4%b8%8b%e8%bd%bd%e9%95%9c%e5%83%8f">
    搜索并下载镜像
  </a>
</h3>

<ol>
<li>打开终端，使用 
    
  
  <a class="link" href="/reference/cli/docker/search/"><code>docker search</code></a> 命令搜索镜像：</li>
</ol>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'ZG9ja2VyIHNlYXJjaCBkb2NrZXIvd2VsY29tZS10by1kb2NrZXI=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="go">docker search docker/welcome-to-docker
</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>你将看到类似以下的输出：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'TkFNRSAgICAgICAgICAgICAgICAgICAgICAgREVTQ1JJUFRJT04gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgU1RBUlMgICAgIE9GRklDSUFMCmRvY2tlci93ZWxjb21lLXRvLWRvY2tlciAgIERvY2tlciBpbWFnZSBmb3IgbmV3IHVzZXJzIGdldHRpbmcgc3RhcnRlZCB34oCmICAgMjA=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="go">NAME                       DESCRIPTION                                     STARS     OFFICIAL
</span></span></span><span class="line"><span class="cl"><span class="go">docker/welcome-to-docker   Docker image for new users getting started w…   20
</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>此输出显示了 Docker Hub 上可用的相关镜像信息。</p>
<ol start="2">
<li>使用 
    
  
  <a class="link" href="/reference/cli/docker/image/pull/"><code>docker pull</code></a> 命令拉取镜像。</li>
</ol>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'ZG9ja2VyIHB1bGwgZG9ja2VyL3dlbGNvbWUtdG8tZG9ja2Vy', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="go">docker pull docker/welcome-to-docker
</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>你将看到类似以下的输出：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'VXNpbmcgZGVmYXVsdCB0YWc6IGxhdGVzdApsYXRlc3Q6IFB1bGxpbmcgZnJvbSBkb2NrZXIvd2VsY29tZS10by1kb2NrZXIKNTc5YjM0ZjBhOTViOiBEb3dubG9hZCBjb21wbGV0ZQpkMTFhNDUxZTYzOTk6IERvd25sb2FkIGNvbXBsZXRlCjFjMjIxNGY5OTM3YzogRG93bmxvYWQgY29tcGxldGUKYjQyYTJmMjg4ZjRkOiBEb3dubG9hZCBjb21wbGV0ZQo1NGIxOWUxMmM2NTU6IERvd25sb2FkIGNvbXBsZXRlCjFmYjI4ZTA3ODI0MDogRG93bmxvYWQgY29tcGxldGUKOTRiZTdlNzgwNzMxOiBEb3dubG9hZCBjb21wbGV0ZQo4OTU3OGNlNzJjMzU6IERvd25sb2FkIGNvbXBsZXRlCkRpZ2VzdDogc2hhMjU2OmVlZGFmZjQ1ZTNjNzg1MzgwODdiZGQ5ZGM3YWZhZmFjN2UxMTAwNjFiYmRkODM2YWY0MTA0YjEwZjEwYWI2OTMKU3RhdHVzOiBEb3dubG9hZGVkIG5ld2VyIGltYWdlIGZvciBkb2NrZXIvd2VsY29tZS10by1kb2NrZXI6bGF0ZXN0CmRvY2tlci5pby9kb2NrZXIvd2VsY29tZS10by1kb2NrZXI6bGF0ZXN0', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="go">Using default tag: latest
</span></span></span><span class="line"><span class="cl"><span class="go">latest: Pulling from docker/welcome-to-docker
</span></span></span><span class="line"><span class="cl"><span class="go">579b34f0a95b: Download complete
</span></span></span><span class="line"><span class="cl"><span class="go">d11a451e6399: Download complete
</span></span></span><span class="line"><span class="cl"><span class="go">1c2214f9937c: Download complete
</span></span></span><span class="line"><span class="cl"><span class="go">b42a2f288f4d: Download complete
</span></span></span><span class="line"><span class="cl"><span class="go">54b19e12c655: Download complete
</span></span></span><span class="line"><span class="cl"><span class="go">1fb28e078240: Download complete
</span></span></span><span class="line"><span class="cl"><span class="go">94be7e780731: Download complete
</span></span></span><span class="line"><span class="cl"><span class="go">89578ce72c35: Download complete
</span></span></span><span class="line"><span class="cl"><span class="go">Digest: sha256:eedaff45e3c78538087bdd9dc7afafac7e110061bbdd836af4104b10f10ab693
</span></span></span><span class="line"><span class="cl"><span class="go">Status: Downloaded newer image for docker/welcome-to-docker:latest
</span></span></span><span class="line"><span class="cl"><span class="go">docker.io/docker/welcome-to-docker:latest
</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>每一行都代表镜像的一个已下载层。请记住，每层都是一组文件系统更改，并提供镜像的功能。</p>

<h3 class=" scroll-mt-20 flex items-center gap-2" id="了解镜像">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e4%ba%86%e8%a7%a3%e9%95%9c%e5%83%8f">
    了解镜像
  </a>
</h3>

<ol>
<li>使用 
    
  
  <a class="link" href="/reference/cli/docker/image/ls/"><code>docker image ls</code></a> 命令列出你下载的镜像：</li>
</ol>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'ZG9ja2VyIGltYWdlIGxz', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="go">docker image ls
</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>你将看到类似以下的输出：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'UkVQT1NJVE9SWSAgICAgICAgICAgICAgICAgVEFHICAgICAgIElNQUdFIElEICAgICAgIENSRUFURUQgICAgICAgIFNJWkUKZG9ja2VyL3dlbGNvbWUtdG8tZG9ja2VyICAgbGF0ZXN0ICAgIGVlZGFmZjQ1ZTNjNyAgIDQgbW9udGhzIGFnbyAgIDI5LjdNQg==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="go">REPOSITORY                 TAG       IMAGE ID       CREATED        SIZE
</span></span></span><span class="line"><span class="cl"><span class="go">docker/welcome-to-docker   latest    eedaff45e3c7   4 months ago   29.7MB
</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>该命令显示当前系统上可用的 Docker 镜像列表。<code>docker/welcome-to-docker</code> 的总大小约为 29.7MB。</p>


  

<blockquote
  
  class="admonition not-prose">
  <p><strong>镜像大小</strong></p>
<p>这里显示的镜像大小反映了镜像的未压缩大小，而不是层的下载大小。</p>

  </blockquote>

<ol start="2">
<li>使用 
    
  
  <a class="link" href="/reference/cli/docker/image/history/"><code>docker image history</code></a> 命令列出镜像的层：</li>
</ol>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'ZG9ja2VyIGltYWdlIGhpc3RvcnkgZG9ja2VyL3dlbGNvbWUtdG8tZG9ja2Vy', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="go">docker image history docker/welcome-to-docker
</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>你将看到类似以下的输出：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'SU1BR0UgICAgICAgICAgQ1JFQVRFRCAgICAgICAgQ1JFQVRFRCBCWSAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgU0laRSAgICAgIENPTU1FTlQKNjQ4ZjkzYTFiYTdkICAgNCBtb250aHMgYWdvICAgQ09QWSAvYXBwL2J1aWxkIC91c3Ivc2hhcmUvbmdpbngvaHRtbCAjIGJ1aWzigKYgICAxLjZNQiAgICAgYnVpbGRraXQuZG9ja2VyZmlsZS52MAo8bWlzc2luZz4gICAgICA1IG1vbnRocyBhZ28gICAvYmluL3NoIC1jICMobm9wKSAgQ01EIFsibmdpbngiICItZyIgImRhZW1vbuKApiAgIDBCCjxtaXNzaW5nPiAgICAgIDUgbW9udGhzIGFnbyAgIC9iaW4vc2ggLWMgIyhub3ApICBTVE9QU0lHTkFMIFNJR1FVSVQgICAgICAgICAgIDBCCjxtaXNzaW5nPiAgICAgIDUgbW9udGhzIGFnbyAgIC9iaW4vc2ggLWMgIyhub3ApICBFWFBPU0UgODAgICAgICAgICAgICAgICAgICAgIDBCCjxtaXNzaW5nPiAgICAgIDUgbW9udGhzIGFnbyAgIC9iaW4vc2ggLWMgIyhub3ApICBFTlRSWVBPSU5UIFsiL2RvY2tlci1lbnRy4oCmICAgMEIKPG1pc3Npbmc&#43;ICAgICAgNSBtb250aHMgYWdvICAgL2Jpbi9zaCAtYyAjKG5vcCkgQ09QWSBmaWxlOjllM2IyYjYzZGI5ZjhmYzfigKYgICA0LjYya0IKPG1pc3Npbmc&#43;ICAgICAgNSBtb250aHMgYWdvICAgL2Jpbi9zaCAtYyAjKG5vcCkgQ09QWSBmaWxlOjU3ODQ2NjMyYWNjYzg5NzXigKYgICAzLjAya0IKPG1pc3Npbmc&#43;ICAgICAgNSBtb250aHMgYWdvICAgL2Jpbi9zaCAtYyAjKG5vcCkgQ09QWSBmaWxlOjNiMWI5OTE1YjdkZDg5OGHigKYgICAyOThCCjxtaXNzaW5nPiAgICAgIDUgbW9udGhzIGFnbyAgIC9iaW4vc2ggLWMgIyhub3ApIENPUFkgZmlsZTpjYWVjMzY4ZjVhNTRmNzBh4oCmICAgMi4xMmtCCjxtaXNzaW5nPiAgICAgIDUgbW9udGhzIGFnbyAgIC9iaW4vc2ggLWMgIyhub3ApIENPUFkgZmlsZTowMWU3NWM2ZGQwY2UzMTdk4oCmICAgMS42MmtCCjxtaXNzaW5nPiAgICAgIDUgbW9udGhzIGFnbyAgIC9iaW4vc2ggLWMgc2V0IC14ICAgICAmJiBhZGRncm91cCAtZyAxMDEgLVMg4oCmICAgOS43TUIKPG1pc3Npbmc&#43;ICAgICAgNSBtb250aHMgYWdvICAgL2Jpbi9zaCAtYyAjKG5vcCkgIEVOViBQS0dfUkVMRUFTRT0xICAgICAgICAgICAgMEIKPG1pc3Npbmc&#43;ICAgICAgNSBtb250aHMgYWdvICAgL2Jpbi9zaCAtYyAjKG5vcCkgIEVOViBOR0lOWF9WRVJTSU9OPTEuMjUuMyAgICAgMEIKPG1pc3Npbmc&#43;ICAgICAgNSBtb250aHMgYWdvICAgL2Jpbi9zaCAtYyAjKG5vcCkgIExBQkVMIG1haW50YWluZXI9TkdJTlggRG/igKYgICAwQgo8bWlzc2luZz4gICAgICA1IG1vbnRocyBhZ28gICAvYmluL3NoIC1jICMobm9wKSAgQ01EIFsiL2Jpbi9zaCJdICAgICAgICAgICAgICAwQgo8bWlzc2luZz4gICAgICA1IG1vbnRocyBhZ28gICAvYmluL3NoIC1jICMobm9wKSBBREQgZmlsZTpmZjMxMTI4Mjg5NjdlODAwNOKApiAgIDcuNjZNQg==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="go">IMAGE          CREATED        CREATED BY                                      SIZE      COMMENT
</span></span></span><span class="line"><span class="cl"><span class="go">648f93a1ba7d   4 months ago   COPY /app/build /usr/share/nginx/html # buil…   1.6MB     buildkit.dockerfile.v0
</span></span></span><span class="line"><span class="cl"><span class="go">&lt;missing&gt;      5 months ago   /bin/sh -c #(nop)  CMD [&#34;nginx&#34; &#34;-g&#34; &#34;daemon…   0B
</span></span></span><span class="line"><span class="cl"><span class="go">&lt;missing&gt;      5 months ago   /bin/sh -c #(nop)  STOPSIGNAL SIGQUIT           0B
</span></span></span><span class="line"><span class="cl"><span class="go">&lt;missing&gt;      5 months ago   /bin/sh -c #(nop)  EXPOSE 80                    0B
</span></span></span><span class="line"><span class="cl"><span class="go">&lt;missing&gt;      5 months ago   /bin/sh -c #(nop)  ENTRYPOINT [&#34;/docker-entr…   0B
</span></span></span><span class="line"><span class="cl"><span class="go">&lt;missing&gt;      5 months ago   /bin/sh -c #(nop) COPY file:9e3b2b63db9f8fc7…   4.62kB
</span></span></span><span class="line"><span class="cl"><span class="go">&lt;missing&gt;      5 months ago   /bin/sh -c #(nop) COPY file:57846632accc8975…   3.02kB
</span></span></span><span class="line"><span class="cl"><span class="go">&lt;missing&gt;      5 months ago   /bin/sh -c #(nop) COPY file:3b1b9915b7dd898a…   298B
</span></span></span><span class="line"><span class="cl"><span class="go">&lt;missing&gt;      5 months ago   /bin/sh -c #(nop) COPY file:caec368f5a54f70a…   2.12kB
</span></span></span><span class="line"><span class="cl"><span class="go">&lt;missing&gt;      5 months ago   /bin/sh -c #(nop) COPY file:01e75c6dd0ce317d…   1.62kB
</span></span></span><span class="line"><span class="cl"><span class="go">&lt;missing&gt;      5 months ago   /bin/sh -c set -x     &amp;&amp; addgroup -g 101 -S …   9.7MB
</span></span></span><span class="line"><span class="cl"><span class="go">&lt;missing&gt;      5 months ago   /bin/sh -c #(nop)  ENV PKG_RELEASE=1            0B
</span></span></span><span class="line"><span class="cl"><span class="go">&lt;missing&gt;      5 months ago   /bin/sh -c #(nop)  ENV NGINX_VERSION=1.25.3     0B
</span></span></span><span class="line"><span class="cl"><span class="go">&lt;missing&gt;      5 months ago   /bin/sh -c #(nop)  LABEL maintainer=NGINX Do…   0B
</span></span></span><span class="line"><span class="cl"><span class="go">&lt;missing&gt;      5 months ago   /bin/sh -c #(nop)  CMD [&#34;/bin/sh&#34;]              0B
</span></span></span><span class="line"><span class="cl"><span class="go">&lt;missing&gt;      5 months ago   /bin/sh -c #(nop) ADD file:ff3112828967e8004…   7.66MB
</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>此输出显示了所有层、它们的大小以及用于创建该层的命令。</p>


  

<blockquote
  
  class="admonition not-prose">
  <p><strong>查看完整命令</strong></p>
<p>如果你在命令中添加 <code>--no-trunc</code> 标志，你将看到完整的命令。请注意，由于输出是类似表格的格式，较长的命令会使输出非常难以浏览。</p>

  </blockquote>


      </div>
    
  </div>
</div>


在这个演练中，你搜索并拉取了一个 Docker 镜像。除了拉取 Docker 镜像，你还了解了 Docker 镜像的层。

## 其他资源

以下资源将帮助你进一步了解如何探索、查找和构建镜像：

- [Docker 受信任内容](/manuals/docker-hub/image-library/trusted-content.md)
- [探索 Docker Desktop 中的镜像视图](/manuals/desktop/use-desktop/images.md)
- [Docker Build 概述](/manuals/build/concepts/overview.md)
- [Docker Hub](https://hub.docker.com)

## 下一步

现在你已经了解了镜像的基础知识，是时候学习如何通过注册中心来分发镜像了。


<a class="button not-prose" href="/get-started/docker-concepts/the-basics/what-is-a-registry/">什么是注册中心？</a>

