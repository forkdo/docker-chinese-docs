# 在 Linux 上安装 Docker Desktop

> **Docker Desktop 条款**
>
> 在大型企业（超过 250 名员工或年收入超过 1000 万美元）中商业使用 Docker Desktop 需要[付费订阅](https://www.docker.com/pricing/)。

本页包含有关一般系统要求、支持的平台以及如何安装 Docker Desktop for Linux 的说明。

> [!IMPORTANT]
>
> Linux 上的 Docker Desktop 运行一个虚拟机 (VM)，该虚拟机在启动时创建并使用自定义的 Docker 上下文 `desktop-linux`。
>
> 这意味着在安装之前部署在 Linux Docker Engine 上的镜像和容器在 Docker Desktop for Linux 中不可用。
>
> 




<div
  id="docker-desktop-与-docker-engine有什么区别"
  x-data="{ open: false }"
  class="my-6 rounded-sm border border-gray-200 bg-white py-2 dark:border-gray-700 dark:bg-gray-900"
>
  <button
    class="not-prose flex w-full justify-between px-4 py-2"
    x-on:click="open = ! open"
  >
    <div class=" flex items-center gap-2">
       Docker Desktop 与 Docker Engine：有什么区别？
    </div>
    <span :class="{ 'hidden' : !open }" class="icon-svg"
      ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M316-400q-6.75 0-10.87-4.64-4.13-4.63-4.13-10.81 0-1.55 5-10.55l158-157q3-3 7.06-5 4.07-2 8.94-2 4.88 0 8.94 2t7.06 5l158 157q2 2 3.5 4.76 1.5 2.77 1.5 5.92 0 6.32-4.12 10.82-4.13 4.5-10.88 4.5H316Z"/></svg></span
    >
    <span :class="{ 'hidden' : open }" class="icon-svg"
      ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M464-376 306-533q-2-2-3.5-4.76-1.5-2.77-1.5-5.92 0-6.32 4.13-10.82 4.12-4.5 10.87-4.5h328q6.75 0 10.88 4.64 4.12 4.63 4.12 10.81 0 1.55-5 10.55L496-376q-3 3-7.06 5t-8.94 2q-4.87 0-8.94-2-4.06-2-7.06-5Z"/></svg></span
    >
  </button>
  <div x-show="open" x-collapse class="px-4">
    

  

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
      <p>对于在大型企业（超过 250 名员工或年收入超过 1000 万美元）中通过 Docker Desktop 获取的 Docker Engine 进行商业使用，需要<a class="link" href="https://www.docker.com/pricing/" rel="noopener">付费订阅</a>。</p>
    </div>
  </blockquote>

<p>Docker Desktop for Linux 提供了一个用户友好的图形界面，简化了容器和服务的管理。它包含 Docker Engine，因为这是驱动 Docker 容器的核心技术。Docker Desktop for Linux 还附带额外的功能，如 Docker Scout 和 Docker Extensions。</p>

<h4 class=" scroll-mt-20 flex items-center gap-2" id="安装-docker-desktop-和-docker-engine">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e5%ae%89%e8%a3%85-docker-desktop-%e5%92%8c-docker-engine">
    安装 Docker Desktop 和 Docker Engine
  </a>
</h4>

<p>Docker Desktop for Linux 和 Docker Engine 可以在同一台机器上并行安装。Docker Desktop for Linux 将容器和镜像存储在虚拟机内的隔离存储位置，并提供控制以限制
    
  
  <a class="link" href="/desktop/settings-and-maintenance/settings/#resources">其资源</a>。为 Docker Desktop 使用专用的存储位置可以防止它干扰同一台机器上的 Docker Engine 安装。</p>
<p>虽然可以同时运行 Docker Desktop 和 Docker Engine，但在某些情况下同时运行两者可能会导致问题。例如，在为容器映射网络端口（<code>-p</code> / <code>--publish</code>）时，Docker Desktop 和 Docker Engine 都可能尝试保留机器上的相同端口，从而导致冲突（“端口已被占用”）。</p>
<p>我们通常建议在使用 Docker Desktop 时停止 Docker Engine，以防止 Docker Engine 消耗资源并避免上述冲突。</p>
<p>使用以下命令停止 Docker Engine 服务：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBzdWRvIHN5c3RlbWN0bCBzdG9wIGRvY2tlciBkb2NrZXIuc29ja2V0IGNvbnRhaW5lcmQ=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> sudo systemctl stop docker docker.socket containerd
</span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>根据您的安装情况，Docker Engine 可能被配置为在机器启动时自动作为系统服务启动。使用以下命令禁用 Docker Engine 服务，并防止其自动启动：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBzdWRvIHN5c3RlbWN0bCBkaXNhYmxlIGRvY2tlciBkb2NrZXIuc29ja2V0IGNvbnRhaW5lcmQ=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> sudo systemctl disable docker docker.socket containerd
</span></span></code></pre></div>
      
    </div>
  </div>
</div>

<h3 class=" scroll-mt-20 flex items-center gap-2" id="在-docker-desktop-和-docker-engine-之间切换">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e5%9c%a8-docker-desktop-%e5%92%8c-docker-engine-%e4%b9%8b%e9%97%b4%e5%88%87%e6%8d%a2">
    在 Docker Desktop 和 Docker Engine 之间切换
  </a>
</h3>

<p>Docker CLI 可用于与多个 Docker Engine 交互。例如，您可以使用相同的 Docker CLI 来控制本地 Docker Engine 和控制在云中运行的远程 Docker Engine 实例。
    
  
  <a class="link" href="/engine/manage-resources/contexts/">Docker Contexts</a> 允许您在 Docker Engine 实例之间切换。</p>
<p>安装 Docker Desktop 时，会创建一个专用的 &quot;desktop-linux&quot; 上下文以与 Docker Desktop 交互。启动时，Docker Desktop 会自动将其自身的上下文 (<code>desktop-linux</code>) 设置为当前上下文。这意味着后续的 Docker CLI 命令都针对 Docker Desktop。关闭时，Docker Desktop 会将当前上下文重置为 <code>default</code> 上下文。</p>
<p>使用 <code>docker context ls</code> 命令查看机器上可用的上下文。当前上下文用星号 (<code>*</code>) 表示。</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBkb2NrZXIgY29udGV4dCBscwpOQU1FICAgICAgICAgICAgREVTQ1JJUFRJT04gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgRE9DS0VSIEVORFBPSU5UICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIC4uLgpkZWZhdWx0ICogICAgICAgQ3VycmVudCBET0NLRVJfSE9TVCBiYXNlZCBjb25maWd1cmF0aW9uICAgdW5peDovLy92YXIvcnVuL2RvY2tlci5zb2NrICAgICAgICAgICAgICAgICAgICAgIC4uLgpkZXNrdG9wLWxpbnV4ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgdW5peDovLy9ob21lLzx1c2VyPi8uZG9ja2VyL2Rlc2t0b3AvZG9ja2VyLnNvY2sgIC4uLiAgICAgICAg', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> docker context ls
</span></span><span class="line"><span class="cl"><span class="go">NAME            DESCRIPTION                               DOCKER ENDPOINT                                  ...
</span></span></span><span class="line"><span class="cl"><span class="go">default *       Current DOCKER_HOST based configuration   unix:///var/run/docker.sock                      ...
</span></span></span><span class="line"><span class="cl"><span class="go">desktop-linux                                             unix:///home/&lt;user&gt;/.docker/desktop/docker.sock  ...        
</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>如果您在同一台机器上同时安装了 Docker Desktop 和 Docker Engine，可以运行 <code>docker context use</code> 命令在 Docker Desktop 和 Docker Engine 上下文之间切换。例如，使用 &quot;default&quot; 上下文与 Docker Engine 交互：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBkb2NrZXIgY29udGV4dCB1c2UgZGVmYXVsdApkZWZhdWx0CkN1cnJlbnQgY29udGV4dCBpcyBub3cgImRlZmF1bHQi', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> docker context use default
</span></span><span class="line"><span class="cl"><span class="go">default
</span></span></span><span class="line"><span class="cl"><span class="go">Current context is now &#34;default&#34;
</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>并使用 <code>desktop-linux</code> 上下文与 Docker Desktop 交互：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBkb2NrZXIgY29udGV4dCB1c2UgZGVza3RvcC1saW51eApkZXNrdG9wLWxpbnV4CkN1cnJlbnQgY29udGV4dCBpcyBub3cgImRlc2t0b3AtbGludXgi', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> docker context use desktop-linux
</span></span><span class="line"><span class="cl"><span class="go">desktop-linux
</span></span></span><span class="line"><span class="cl"><span class="go">Current context is now &#34;desktop-linux&#34;
</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>有关更多详细信息，请参阅 
    
  
  <a class="link" href="/engine/manage-resources/contexts/">Docker Context 文档</a>。</p>

  </div>
</div>



## 支持的平台

Docker 为以下 Linux 发行版和架构提供 `.deb` 和 `.rpm` 软件包：

| 平台                | x86_64 / amd64          |
|:------------------------|:-----------------------:|
| [Ubuntu](ubuntu.md)                         | ✅  |
| [Debian](debian.md)                         | ✅  |
| [Red Hat Enterprise Linux (RHEL)](rhel.md)  | ✅  |
| [Fedora](fedora.md)                         | ✅  |


适用于基于 [Arch](archlinux.md) 的发行版的实验性软件包可用。Docker 尚未测试或验证该安装。

Docker 支持上述发行版的当前 LTS 版本和最新版本上的 Docker Desktop。随着新版本的发布，Docker 会停止支持最旧的版本并支持最新的版本。

## 一般系统要求

要成功安装 Docker Desktop，您的 Linux 主机必须满足以下一般要求：

- 64 位内核和 CPU 对虚拟化的支持。
- KVM 虚拟化支持。请遵循 [KVM 虚拟化支持说明](#kvm-virtualization-support) 以检查 KVM 内核模块是否已启用以及如何提供对 KVM 设备的访问。
- QEMU 版本必须为 5.2 或更高。我们建议升级到最新版本。
- systemd init 系统。
- 支持 GNOME、KDE 或 MATE 桌面环境，但其他环境也可能可用。
  - 对于许多 Linux 发行版，GNOME 环境不支持托盘图标。要添加对托盘图标的支持，您需要安装 GNOME 扩展。例如，[AppIndicator](https://extensions.gnome.org/extension/615/appindicator-support/)。
- 至少 4 GB RAM。
- 启用在用户命名空间中配置 ID 映射，请参阅[文件共享](/manuals/desktop/troubleshoot-and-support/faqs/linuxfaqs.md#how-do-i-enable-file-sharing)。请注意，对于 Docker Desktop 4.35 及更高版本，不再需要此操作。
- 推荐：[初始化 `pass`](/manuals/desktop/setup/sign-in.md#credentials-management-for-linux-users) 用于凭据管理。

Docker Desktop for Linux 运行一个虚拟机 (VM)。有关原因的更多信息，请参阅 [为什么 Docker Desktop for Linux 运行虚拟机](/manuals/desktop/troubleshoot-and-support/faqs/linuxfaqs.md#why-does-docker-desktop-for-linux-run-a-vm)。

> [!NOTE]
>
> Docker 不支持在嵌套虚拟化场景中运行 Docker Desktop for Linux。我们建议您在支持的发行版上原生运行 Docker Desktop for Linux。

### KVM 虚拟化支持

Docker Desktop 运行一个需要 [KVM 支持](https://www.linux-kvm.org) 的虚拟机。

如果主机支持虚拟化，`kvm` 模块应该会自动加载。要手动加载模块，请运行：

```console
$ modprobe kvm
```

根据主机的处理器，必须加载相应的模块：

```console
$ modprobe kvm_intel  # Intel 处理器

$ modprobe kvm_amd    # AMD 处理器
```

如果上述命令失败，可以通过运行以下命令查看诊断信息：

```console
$ kvm-ok
```

要检查 KVM 模块是否已启用，请运行：

```console
$ lsmod | grep kvm
kvm_amd               167936  0
ccp                   126976  1 kvm_amd
kvm                  1089536  1 kvm_amd
irqbypass              16384  1 kvm
```

#### 设置 KVM 设备用户权限

要检查 `/dev/kvm` 的所有权，请运行：

```console
$ ls -al /dev/kvm
```

将您的用户添加到 kvm 组以访问 kvm 设备：

```console
$ sudo usermod -aG kvm $USER
```

注销并重新登录，以便重新评估您的组成员身份。

## 下一步

- 为您的特定 Linux 发行版安装 Docker Desktop for Linux：
   - [在 Ubuntu 上安装](ubuntu.md)
   - [在 Debian 上安装](debian.md)
   - [在 Red Hat Enterprise Linux (RHEL) 上安装](rhel.md)
   - [在 Fedora 上安装](fedora.md)
   - [在 Arch 上安装](archlinux.md)

- [在 Ubuntu 上安装 Docker Desktop](/desktop/setup/install/linux/ubuntu/)

- [在 Debian 上安装 Docker Desktop](/desktop/setup/install/linux/debian/)

- [在 Fedora 上安装 Docker Desktop](/desktop/setup/install/linux/fedora/)

- [在基于 Arch 的发行版上安装 Docker Desktop](/desktop/setup/install/linux/archlinux/)

- [在 RHEL 上安装 Docker Desktop](/desktop/setup/install/linux/rhel/)

