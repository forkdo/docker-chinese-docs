# 什么是容器？

<div id="youtube-player-W1kWqFkiu7k" data-video-id="W1kWqFkiu7k" class="youtube-video aspect-video h-fit w-full py-2">
</div>


## 解释

假设您正在开发一个杀手级的 Web 应用程序，它包含三个主要组件：一个 React 前端、一个 Python API 和一个 PostgreSQL 数据库。如果您想在这个项目上工作，您必须安装 Node、Python 和 PostgreSQL。

您如何确保您的版本与团队中的其他开发人员相同？或者与您的 CI/CD 系统相同？或者与生产环境中使用的版本相同？

您如何确保应用程序所需的 Python（或 Node 或数据库）版本不受您机器上已安装内容的影响？您如何管理潜在的冲突？

容器应运而生！

什么是容器？简单来说，容器是您应用程序每个组件的隔离进程。每个组件——前端 React 应用、Python API 引擎和数据库——都在其自己的隔离环境中运行，与您机器上的其他一切完全隔离。

以下是它们的过人之处。容器是：

- **自包含的**。每个容器都拥有其运行所需的一切，不依赖于主机机器上的任何预安装依赖项。
- **隔离的**。由于容器在隔离状态下运行，它们对主机和其他容器的影响最小，从而提高了应用程序的安全性。
- **独立的**。每个容器都是独立管理的。删除一个容器不会影响任何其他容器。
- **可移植的**。容器可以在任何地方运行！在您的开发机器上运行的容器，在数据中心或云中的任何地方都能以相同的方式工作！

### 容器与虚拟机 (VM)

无需深入探讨，虚拟机 (VM) 是一个完整的操作系统，拥有自己的内核、硬件驱动程序、程序和应用程序。仅为了隔离单个应用程序而启动一个虚拟机，开销非常大。

容器只是一个隔离的进程，附带其运行所需的所有文件。如果您运行多个容器，它们都共享同一个内核，这使得您可以在更少的基础设施上运行更多的应用程序。

> **同时使用虚拟机和容器**
>
> 很常见的情况是，您会看到容器和虚拟机一起使用。例如，在云环境中，配置的机器通常是虚拟机。但是，与其配置一台机器来运行一个应用程序，不如在一个装有容器运行时的虚拟机上运行多个容器化应用程序，这样可以提高资源利用率并降低成本。


## 尝试一下

在本实践教程中，您将学习如何使用 Docker Desktop GUI 运行一个 Docker 容器。








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
        <p>请按照以下说明运行容器。</p>
<ol>
<li>
<p>打开 Docker Desktop 并选择顶部导航栏中的 <strong>搜索</strong> 字段。</p>
</li>
<li>
<p>在搜索输入框中指定 <code>welcome-to-docker</code>，然后选择 <strong>拉取 (Pull)</strong> 按钮。</p>

  
  
    








<figure
  x-data="{ zoom: false }"
  @click="zoom = ! zoom"
  class="cursor-pointer hover:opacity-90"
>
  <img
    loading="lazy"
    src="https://docs.docker.com/get-started/docker-concepts/the-basics/images/search-the-docker-image.webp"
    alt="Docker Desktop 仪表板的截图，显示 welcome-to-docker 镜像的搜索结果"
    width="1000"
    height="700"
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
        src="https://docs.docker.com/get-started/docker-concepts/the-basics/images/search-the-docker-image.webp"
        alt="Docker Desktop 仪表板的截图，显示 welcome-to-docker 镜像的搜索结果"
      />
    </div>
  </template>
</figure>
</li>
<li>
<p>镜像成功拉取后，选择 <strong>运行 (Run)</strong> 按钮。</p>
</li>
<li>
<p>展开 <strong>可选设置 (Optional settings)</strong>。</p>
</li>
<li>
<p>在 <strong>容器名称 (Container name)</strong> 中，指定 <code>welcome-to-docker</code>。</p>
</li>
<li>
<p>在 <strong>主机端口 (Host port)</strong> 中，指定 <code>8080</code>。</p>

  
  
    








<figure
  x-data="{ zoom: false }"
  @click="zoom = ! zoom"
  class="cursor-pointer hover:opacity-90"
>
  <img
    loading="lazy"
    src="https://docs.docker.com/get-started/docker-concepts/the-basics/images/run-a-new-container.webp"
    alt="Docker Desktop 仪表板的截图，显示容器运行对话框，容器名称为 welcome-to-docker，端口号指定为 8080"
    width="550"
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
        src="https://docs.docker.com/get-started/docker-concepts/the-basics/images/run-a-new-container.webp"
        alt="Docker Desktop 仪表板的截图，显示容器运行对话框，容器名称为 welcome-to-docker，端口号指定为 8080"
      />
    </div>
  </template>
</figure>
</li>
<li>
<p>选择 <strong>运行 (Run)</strong> 以启动您的容器。</p>
</li>
</ol>
<p>恭喜！您刚刚运行了您的第一个容器！🎉</p>

<h3 class=" scroll-mt-20 flex items-center gap-2" id="查看您的容器">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e6%9f%a5%e7%9c%8b%e6%82%a8%e7%9a%84%e5%ae%b9%e5%99%a8">
    查看您的容器
  </a>
</h3>

<p>您可以通过转到 Docker Desktop 仪表板的 <strong>容器 (Containers)</strong> 视图来查看所有容器。</p>

  
  
    








<figure
  x-data="{ zoom: false }"
  @click="zoom = ! zoom"
  class="cursor-pointer hover:opacity-90"
>
  <img
    loading="lazy"
    src="https://docs.docker.com/get-started/docker-concepts/the-basics/images/view-your-containers.webp"
    alt="Docker Desktop GUI 容器视图的截图，显示 welcome-to-docker 容器正在主机端口 8080 上运行"
    width="750"
    height="600"
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
        src="https://docs.docker.com/get-started/docker-concepts/the-basics/images/view-your-containers.webp"
        alt="Docker Desktop GUI 容器视图的截图，显示 welcome-to-docker 容器正在主机端口 8080 上运行"
      />
    </div>
  </template>
</figure>
<p>这个容器运行一个显示简单网站的 Web 服务器。在处理更复杂的项目时，您会在不同的容器中运行不同的部分。例如，您可能会为前端、后端和数据库分别运行不同的容器。</p>

<h3 class=" scroll-mt-20 flex items-center gap-2" id="访问前端">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e8%ae%bf%e9%97%ae%e5%89%8d%e7%ab%af">
    访问前端
  </a>
</h3>

<p>当您启动容器时，您将容器的一个端口暴露到了您的机器上。可以将其视为创建配置，以允许您通过容器的隔离环境进行连接。</p>
<p>对于此容器，前端可在端口 <code>8080</code> 上访问。要打开网站，请选择容器 <strong>端口 (Port(s))</strong> 列中的链接，或在浏览器中访问 <a class="link" href="http://localhost:8080" rel="noopener">http://localhost:8080</a>。</p>

  
  
    








<figure
  x-data="{ zoom: false }"
  @click="zoom = ! zoom"
  class="cursor-pointer hover:opacity-90"
>
  <img
    loading="lazy"
    src="https://docs.docker.com/get-started/docker-concepts/the-basics/images/access-the-frontend.webp"
    alt="来自正在运行的容器的登录页面截图"
    
    
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
        src="https://docs.docker.com/get-started/docker-concepts/the-basics/images/access-the-frontend.webp"
        alt="来自正在运行的容器的登录页面截图"
      />
    </div>
  </template>
</figure>

<h3 class=" scroll-mt-20 flex items-center gap-2" id="探索您的容器">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e6%8e%a2%e7%b4%a2%e6%82%a8%e7%9a%84%e5%ae%b9%e5%99%a8">
    探索您的容器
  </a>
</h3>

<p>Docker Desktop 允许您探索容器的不同方面并与之交互。请亲自尝试一下。</p>
<ol>
<li>
<p>转到 Docker Desktop 仪表板中的 <strong>容器 (Containers)</strong> 视图。</p>
</li>
<li>
<p>选择您的容器。</p>
</li>
<li>
<p>选择 <strong>文件 (Files)</strong> 标签页以探索容器的隔离文件系统。</p>

  
  
    








<figure
  x-data="{ zoom: false }"
  @click="zoom = ! zoom"
  class="cursor-pointer hover:opacity-90"
>
  <img
    loading="lazy"
    src="https://docs.docker.com/get-started/docker-concepts/the-basics/images/explore-your-container.webp"
    alt="Docker Desktop 仪表板的截图，显示正在运行的容器内的文件和目录"
    
    
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
        src="https://docs.docker.com/get-started/docker-concepts/the-basics/images/explore-your-container.webp"
        alt="Docker Desktop 仪表板的截图，显示正在运行的容器内的文件和目录"
      />
    </div>
  </template>
</figure>
</li>
</ol>

<h3 class=" scroll-mt-20 flex items-center gap-2" id="停止您的容器">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e5%81%9c%e6%ad%a2%e6%82%a8%e7%9a%84%e5%ae%b9%e5%99%a8">
    停止您的容器
  </a>
</h3>

<p><code>docker/welcome-to-docker</code> 容器会持续运行，直到您将其停止。</p>
<ol>
<li>
<p>转到 Docker Desktop 仪表板中的 <strong>容器 (Containers)</strong> 视图。</p>
</li>
<li>
<p>找到您想要停止的容器。</p>
</li>
<li>
<p>在 <strong>操作 (Actions)</strong> 列中选择 <strong>停止 (Stop)</strong> 操作。</p>

  
  
    








<figure
  x-data="{ zoom: false }"
  @click="zoom = ! zoom"
  class="cursor-pointer hover:opacity-90"
>
  <img
    loading="lazy"
    src="https://docs.docker.com/get-started/docker-concepts/the-basics/images/stop-your-container.webp"
    alt="Docker Desktop 仪表板的截图，已选择 welcome 容器并准备停止"
    
    
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
        src="https://docs.docker.com/get-started/docker-concepts/the-basics/images/stop-your-container.webp"
        alt="Docker Desktop 仪表板的截图，已选择 welcome 容器并准备停止"
      />
    </div>
  </template>
</figure>
</li>
</ol>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== '%E4%BD%BF%E7%94%A8-CLI' && 'hidden'"
      >
        <p>请按照以下说明使用 CLI 运行容器：</p>
<ol>
<li>
<p>打开您的 CLI 终端，并使用 
  <a class="link" href="/reference/cli/docker/container/run/"><code>docker run</code></a> 命令启动一个容器：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBkb2NrZXIgcnVuIC1kIC1wIDgwODA6ODAgZG9ja2VyL3dlbGNvbWUtdG8tZG9ja2Vy', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> docker run -d -p 8080:80 docker/welcome-to-docker
</span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>此命令的输出是完整的容器 ID。</p>
</li>
</ol>
<p>恭喜！您刚刚启动了您的第一个容器！🎉</p>

<h3 class=" scroll-mt-20 flex items-center gap-2" id="查看正在运行的容器">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e6%9f%a5%e7%9c%8b%e6%ad%a3%e5%9c%a8%e8%bf%90%e8%a1%8c%e7%9a%84%e5%ae%b9%e5%99%a8">
    查看正在运行的容器
  </a>
</h3>

<p>您可以使用 
  <a class="link" href="/reference/cli/docker/container/ls/"><code>docker ps</code></a> 命令来验证容器是否已启动并正在运行：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'ZG9ja2VyIHBz', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="go">docker ps
</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>您将看到类似以下的输出：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'IENPTlRBSU5FUiBJRCAgIElNQUdFICAgICAgICAgICAgICAgICAgICAgIENPTU1BTkQgICAgICAgICAgICAgICAgICBDUkVBVEVEICAgICAgICAgIFNUQVRVUyAgICAgICAgICBQT1JUUyAgICAgICAgICAgICAgICAgICAgICBOQU1FUwogYTFmN2E0YmIzYTI3ICAgZG9ja2VyL3dlbGNvbWUtdG8tZG9ja2VyICAgIi9kb2NrZXItZW50cnlwb2ludC7igKYiICAgMTEgc2Vjb25kcyBhZ28gICBVcCAxMSBzZWNvbmRzICAgMC4wLjAuMDo4MDgwLT44MC90Y3AgICAgICAgZ3JhY2lvdXNfa2VsZHlzaA==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="go"> CONTAINER ID   IMAGE                      COMMAND                  CREATED          STATUS          PORTS                      NAMES
</span></span></span><span class="line"><span class="cl"><span class="go"> a1f7a4bb3a27   docker/welcome-to-docker   &#34;/docker-entrypoint.…&#34;   11 seconds ago   Up 11 seconds   0.0.0.0:8080-&gt;80/tcp       gracious_keldysh
</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>这个容器运行一个显示简单网站的 Web 服务器。在处理更复杂的项目时，您会在不同的容器中运行不同的部分。例如，为 <code>frontend</code>、<code>backend</code> 和 <code>database</code> 分别运行不同的容器。</p>


  

  <blockquote
    
    class="admonition admonition-tip admonition not-prose">
    <div class="admonition-header">
      <span class="admonition-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<mask id="mask0_5432_1749" style="mask-type:alpha" maskUnits="userSpaceOnUse" x="4" y="1" width="17" height="22">
<path d="M9.93896 22H14.939M10.439 10H14.439M12.439 10L12.439 16M15.439 15.3264C17.8039 14.2029 19.439 11.7924 19.439 9C19.439 5.13401 16.305 2 12.439 2C8.57297 2 5.43896 5.13401 5.43896 9C5.43896 11.7924 7.07402 14.2029 9.43896 15.3264V16C9.43896 16.9319 9.43896 17.3978 9.59121 17.7654C9.79419 18.2554 10.1835 18.6448 10.6736 18.8478C11.0411 19 11.5071 19 12.439 19C13.3708 19 13.8368 19 14.2043 18.8478C14.6944 18.6448 15.0837 18.2554 15.2867 17.7654C15.439 17.3978 15.439 16.9319 15.439 16V15.3264Z" stroke="#6C7E9D" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</mask>
<g mask="url(#mask0_5432_1749)">
<rect width="24" height="24" fill="currentColor" fill-opacity="0.8"/>
</g>
</svg>

      </span>
      <span class="admonition-title">
        Tip
      </span>
    </div>
    <div class="admonition-content">
      <p><code>docker ps</code> 命令将仅显示<em>正在运行的</em>容器。要查看已停止的容器，请添加 <code>-a</code> 标志以列出所有容器：<code>docker ps -a</code></p>
    </div>
  </blockquote>


<h3 class=" scroll-mt-20 flex items-center gap-2" id="访问前端">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e8%ae%bf%e9%97%ae%e5%89%8d%e7%ab%af">
    访问前端
  </a>
</h3>

<p>当您启动容器时，您将容器的一个端口暴露到了您的机器上。可以将其视为创建配置，以允许您通过容器的隔离环境进行连接。</p>
<p>对于此容器，前端可在端口 <code>8080</code> 上访问。要打开网站，请选择容器 <strong>端口 (Port(s))</strong> 列中的链接，或在浏览器中访问 <a class="link" href="http://localhost:8080" rel="noopener">http://localhost:8080</a>。</p>

  
  
    








<figure
  x-data="{ zoom: false }"
  @click="zoom = ! zoom"
  class="cursor-pointer hover:opacity-90"
>
  <img
    loading="lazy"
    src="https://docs.docker.com/get-started/docker-concepts/the-basics/images/access-the-frontend.webp"
    alt="来自正在运行的容器的 Nginx Web 服务器登录页面截图"
    
    
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
        src="https://docs.docker.com/get-started/docker-concepts/the-basics/images/access-the-frontend.webp"
        alt="来自正在运行的容器的 Nginx Web 服务器登录页面截图"
      />
    </div>
  </template>
</figure>

<h3 class=" scroll-mt-20 flex items-center gap-2" id="停止您的容器">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e5%81%9c%e6%ad%a2%e6%82%a8%e7%9a%84%e5%ae%b9%e5%99%a8">
    停止您的容器
  </a>
</h3>

<p><code>docker/welcome-to-docker</code> 容器会持续运行，直到您将其停止。您可以使用 <code>docker stop</code> 命令来停止容器。</p>
<ol>
<li>
<p>运行 <code>docker ps</code> 以获取容器的 ID</p>
</li>
<li>
<p>将容器 ID 或名称提供给 
  <a class="link" href="/reference/cli/docker/container/stop/"><code>docker stop</code></a> 命令：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'ZG9ja2VyIHN0b3AgPHRoZS1jb250YWluZXItaWQ&#43;', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="go">docker stop &lt;the-container-id&gt;
</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
</li>
</ol>


  

  <blockquote
    
    class="admonition admonition-tip admonition not-prose">
    <div class="admonition-header">
      <span class="admonition-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<mask id="mask0_5432_1749" style="mask-type:alpha" maskUnits="userSpaceOnUse" x="4" y="1" width="17" height="22">
<path d="M9.93896 22H14.939M10.439 10H14.439M12.439 10L12.439 16M15.439 15.3264C17.8039 14.2029 19.439 11.7924 19.439 9C19.439 5.13401 16.305 2 12.439 2C8.57297 2 5.43896 5.13401 5.43896 9C5.43896 11.7924 7.07402 14.2029 9.43896 15.3264V16C9.43896 16.9319 9.43896 17.3978 9.59121 17.7654C9.79419 18.2554 10.1835 18.6448 10.6736 18.8478C11.0411 19 11.5071 19 12.439 19C13.3708 19 13.8368 19 14.2043 18.8478C14.6944 18.6448 15.0837 18.2554 15.2867 17.7654C15.439 17.3978 15.439 16.9319 15.439 16V15.3264Z" stroke="#6C7E9D" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</mask>
<g mask="url(#mask0_5432_1749)">
<rect width="24" height="24" fill="currentColor" fill-opacity="0.8"/>
</g>
</svg>

      </span>
      <span class="admonition-title">
        Tip
      </span>
    </div>
    <div class="admonition-content">
      <p>通过 ID 引用容器时，您不需要提供完整的 ID。您只需提供足够的 ID 使其唯一即可。例如，可以通过运行以下命令来停止上一个容器：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'ZG9ja2VyIHN0b3AgYTFm', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="go">docker stop a1f
</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
    </div>
  </blockquote>


      </div>
    
  </div>
</div>


## 其他资源

以下链接提供了关于容器的更多指导：

- [运行容器](/engine/containers/run/)
- [容器概述](https://www.docker.com/resources/what-container/)
- [为什么选择 Docker？](https://www.docker.com/why-docker/)

## 下一步

既然您已经了解了 Docker 容器的基础知识，是时候学习 Docker 镜像了。


<a class="button not-prose" href="https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-an-image/">什么是镜像？</a>

