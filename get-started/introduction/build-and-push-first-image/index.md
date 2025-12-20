# 构建并推送你的第一个镜像

<div id="youtube-player-7ge1s5nAa34" data-video-id="7ge1s5nAa34" class="youtube-video aspect-video h-fit w-full py-2">
</div>


## 说明

现在你已经更新了[待办事项列表应用](develop-with-containers.md)，接下来就可以为这个应用创建一个容器镜像，并将其分享到 Docker Hub 上。为此，你需要完成以下步骤：

1. 使用你的 Docker 账户登录
2. 在 Docker Hub 上创建一个镜像仓库
3. 构建容器镜像
4. 将镜像推送到 Docker Hub

在开始动手实践之前，你需要了解以下几个核心概念。

### 容器镜像

如果你是容器镜像的新手，可以将其理解为包含运行应用所需的所有内容的标准化软件包，包括文件、配置和依赖项。这些软件包可以分发给其他人共享。

### Docker Hub

要分享你的 Docker 镜像，你需要一个存储它们的地方。这就是镜像仓库的作用。虽然有很多镜像仓库可供选择，但 Docker Hub 是镜像的默认首选仓库。Docker Hub 既为你提供了存储自己镜像的空间，也让你能够找到其他人发布的镜像，可以直接运行或用作自己镜像的基础。

在[使用容器进行开发](develop-with-containers.md)中，你使用了以下来自 Docker Hub 的镜像，它们都是 [Docker 官方镜像](/manuals/docker-hub/image-library/trusted-content.md#docker-official-images)：

- [node](https://hub.docker.com/_/node) - 提供 Node 环境，用作你开发工作的基础。这个镜像也被用作最终应用镜像的基础。
- [mysql](https://hub.docker.com/_/mysql) - 提供 MySQL 数据库，用于存储待办事项列表项
- [phpmyadmin](https://hub.docker.com/_/phpmyadmin) - 提供 phpMyAdmin，一个基于 Web 的 MySQL 数据库管理界面
- [traefik](https://hub.docker.com/_/traefik) - 提供 Traefik，一个现代的 HTTP 反向代理和负载均衡器，根据路由规则将请求路由到适当的容器

浏览 [Docker 官方镜像](https://hub.docker.com/search?badges=official)、[Docker 认证发布者](https://hub.docker.com/search?badges=verified_publisher) 和 [Docker 赞助的开源软件](https://hub.docker.com/search?badges=open_source) 的完整目录，了解更多可以运行和构建的内容。

## 动手实践

在本动手指南中，你将学习如何登录 Docker Hub 并将镜像推送到 Docker Hub 仓库。

## 使用你的 Docker 账户登录

要将镜像推送到 Docker Hub，你需要使用 Docker 账户登录。

1. 打开 Docker 仪表板。

2. 点击右上角的 **登录**。

3. 如果需要，请创建一个账户，然后完成登录流程。

完成后，你应该看到 **登录** 按钮变成了你的头像。

## 创建镜像仓库

现在你已经有了账户，可以创建一个镜像仓库。就像 Git 仓库保存源代码一样，镜像仓库存储容器镜像。

1. 访问 [Docker Hub](https://hub.docker.com)。

2. 点击 **创建仓库**。

3. 在 **创建仓库** 页面，输入以下信息：

    - **仓库名称** - `getting-started-todo-app`
    - **简短描述** - 如果需要，可以输入描述
    - **可见性** - 选择 **公开**，以便其他人可以拉取你定制的待办事项应用

4. 点击 **创建** 来创建仓库。

## 构建并推送镜像

现在你已经有了仓库，就可以构建并推送你的镜像了。需要注意的是，你正在构建的镜像是基于 Node 镜像的，这意味着你不需要安装或配置 Node、yarn 等。你只需专注于让你的应用变得独特。

> **什么是镜像/Dockerfile？**
>
> 暂时不用深入了解，可以将容器镜像理解为包含运行某个进程所需的所有内容的单一软件包。在本例中，它将包含 Node 环境、后端代码和编译后的 React 代码。
>
> 任何运行使用该镜像的容器的机器，都能够运行这个应用，就像它是被构建的一样，而无需在机器上预先安装任何其他东西。
>
> `Dockerfile` 是一个基于文本的脚本，提供了构建镜像的指令集。在这个快速入门中，仓库已经包含了 Dockerfile。








<div
  class="tabs"
  
    
      x-data="{ selected: $persist('CLI').as('tabgroup-cli-or-vs-code') }"
    
    @tab-select.window="$event.detail.group === 'cli-or-vs-code' ? selected =
    $event.detail.name : null"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'CLI' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'cli-or-vs-code', name:
          'CLI'})"
        
      >
        CLI
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'VS-Code' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'cli-or-vs-code', name:
          'VS-Code'})"
        
      >
        VS Code
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'CLI' && 'hidden'"
      >
        <ol>
<li>
<p>要开始，可以将项目克隆或<a class="link" href="https://github.com/docker/getting-started-todo-app/archive/refs/heads/main.zip" rel="noopener">以 ZIP 文件的形式下载</a>到本地机器。</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBnaXQgY2xvbmUgaHR0cHM6Ly9naXRodWIuY29tL2RvY2tlci9nZXR0aW5nLXN0YXJ0ZWQtdG9kby1hcHA=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> git clone https://github.com/docker/getting-started-todo-app
</span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>克隆项目后，进入克隆创建的新目录：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBjZCBnZXR0aW5nLXN0YXJ0ZWQtdG9kby1hcHA=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> <span class="nb">cd</span> getting-started-todo-app
</span></span></code></pre></div>
      
    </div>
  </div>
</div>
</li>
<li>
<p>通过运行以下命令构建项目，将 <code>DOCKER_USERNAME</code> 替换为你的用户名。</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBkb2NrZXIgYnVpbGQgLXQgPERPQ0tFUl9VU0VSTkFNRT4vZ2V0dGluZy1zdGFydGVkLXRvZG8tYXBwIC4=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> docker build -t &lt;DOCKER_USERNAME&gt;/getting-started-todo-app .
</span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>例如，如果你的 Docker 用户名是 <code>mobydock</code>，你可以运行以下命令：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBkb2NrZXIgYnVpbGQgLXQgbW9ieWRvY2svZ2V0dGluZy1zdGFydGVkLXRvZG8tYXBwIC4=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> docker build -t mobydock/getting-started-todo-app .
</span></span></code></pre></div>
      
    </div>
  </div>
</div>
</li>
<li>
<p>要验证镜像是否已在本地存在，可以使用 <code>docker image ls</code> 命令：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBkb2NrZXIgaW1hZ2UgbHM=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> docker image ls
</span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>你会看到类似以下的输出：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'UkVQT1NJVE9SWSAgICAgICAgICAgICAgICAgICAgICAgICAgVEFHICAgICAgIElNQUdFIElEICAgICAgIENSRUFURUQgICAgICAgICAgU0laRQptb2J5ZG9jay9nZXR0aW5nLXN0YXJ0ZWQtdG9kby1hcHAgICBsYXRlc3QgICAgMTU0MzY1NmM5MjkwICAgMiBtaW51dGVzIGFnbyAgICAxLjEyR0IKLi4u', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="go">REPOSITORY                          TAG       IMAGE ID       CREATED          SIZE
</span></span></span><span class="line"><span class="cl"><span class="go">mobydock/getting-started-todo-app   latest    1543656c9290   2 minutes ago    1.12GB
</span></span></span><span class="line"><span class="cl"><span class="go">...
</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
</li>
<li>
<p>要推送镜像，请使用 <code>docker push</code> 命令。确保将 <code>DOCKER_USERNAME</code> 替换为你的用户名：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBkb2NrZXIgcHVzaCA8RE9DS0VSX1VTRVJOQU1FPi9nZXR0aW5nLXN0YXJ0ZWQtdG9kby1hcHA=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> docker push &lt;DOCKER_USERNAME&gt;/getting-started-todo-app
</span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>根据你的上传速度，这可能需要一点时间。</p>
</li>
</ol>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'VS-Code' && 'hidden'"
      >
        <ol>
<li>
<p>打开 Visual Studio Code。确保你已经从<a class="link" href="https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker" rel="noopener">扩展市场</a>安装了 <strong>VS Code 的 Docker 扩展</strong>。</p>

  
  
    








<figure
  x-data="{ zoom: false }"
  @click="zoom = ! zoom"
  class="cursor-pointer hover:opacity-90"
>
  <img
    loading="lazy"
    src="/get-started/introduction/images/install-docker-extension.webp"
    alt="VS Code 扩展市场的截图"
    
    
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
        src="/get-started/introduction/images/install-docker-extension.webp"
        alt="VS Code 扩展市场的截图"
      />
    </div>
  </template>
</figure>
</li>
<li>
<p>在 <strong>文件</strong> 菜单中，选择 <strong>打开文件夹</strong>。选择 <strong>克隆 Git 仓库</strong> 并粘贴这个 URL：<a class="link" href="https://github.com/docker/getting-started-todo-app" rel="noopener">https://github.com/docker/getting-started-todo-app</a></p>

  
  
    








<figure
  x-data="{ zoom: false }"
  @click="zoom = ! zoom"
  class="cursor-pointer hover:opacity-90"
>
  <img
    loading="lazy"
    src="/get-started/introduction/images/clone-the-repo.webp"
    alt="显示如何克隆仓库的 VS Code 截图"
    
    
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
        src="/get-started/introduction/images/clone-the-repo.webp"
        alt="显示如何克隆仓库的 VS Code 截图"
      />
    </div>
  </template>
</figure>
</li>
<li>
<p>右键点击 <code>Dockerfile</code>，选择 <strong>构建镜像...</strong> 菜单项。</p>

  
  
    








<figure
  x-data="{ zoom: false }"
  @click="zoom = ! zoom"
  class="cursor-pointer hover:opacity-90"
>
  <img
    loading="lazy"
    src="/get-started/introduction/images/build-vscode-menu-item.webp"
    alt="显示右键菜单和“构建镜像”菜单项的 VS Code 截图"
    
    
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
        src="/get-started/introduction/images/build-vscode-menu-item.webp"
        alt="显示右键菜单和“构建镜像”菜单项的 VS Code 截图"
      />
    </div>
  </template>
</figure>
</li>
<li>
<p>在出现的对话框中，输入名称 <code>DOCKER_USERNAME/getting-started-todo-app</code>，将 <code>DOCKER_USERNAME</code> 替换为你的 Docker 用户名。</p>
</li>
<li>
<p>按下 <strong>Enter</strong> 后，你会看到一个终端出现，构建过程将在其中进行。完成后，可以关闭终端。</p>
</li>
<li>
<p>通过点击左侧导航菜单中的 Docker 图标，打开 VS Code 的 Docker 扩展。</p>
</li>
<li>
<p>找到你创建的镜像。它的名称将是 <code>docker.io/DOCKER_USERNAME/getting-started-todo-app</code>。</p>
</li>
<li>
<p>展开镜像以查看镜像的标签（或不同版本）。你应该会看到一个名为 <code>latest</code> 的标签，这是镜像的默认标签。</p>
</li>
<li>
<p>右键点击 <strong>latest</strong> 项，选择 <strong>推送...</strong> 选项。</p>

  
  
    








<figure
  x-data="{ zoom: false }"
  @click="zoom = ! zoom"
  class="cursor-pointer hover:opacity-90"
>
  <img
    loading="lazy"
    src="/get-started/introduction/images/build-vscode-push-image.webp"
    alt="显示 Docker 扩展和右键菜单以推送镜像的截图"
    
    
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
        src="/get-started/introduction/images/build-vscode-push-image.webp"
        alt="显示 Docker 扩展和右键菜单以推送镜像的截图"
      />
    </div>
  </template>
</figure>
</li>
<li>
<p>按下 <strong>Enter</strong> 确认，然后观察你的镜像被推送到 Docker Hub。根据你的上传速度，这可能需要一点时间。</p>
<p>上传完成后，可以关闭终端。</p>
</li>
</ol>

      </div>
    
  </div>
</div>


## 总结

在继续之前，花点时间回顾一下这里发生的事情。在短短几分钟内，你就成功构建了一个打包你应用的容器镜像，并将其推送到了 Docker Hub。

今后，请记住以下几点：

- Docker Hub 是查找可信内容的最佳仓库。Docker 提供了一系列可信内容，包括 Docker 官方镜像、Docker 认证发布者和 Docker 赞助的开源软件，你可以直接使用或用作自己镜像的基础。

- Docker Hub 提供了一个分发你自己应用的市场。任何人都可以创建账户并分发镜像。虽然你公开分发了你创建的镜像，但私有仓库可以确保你的镜像只能被授权用户访问。

> **其他仓库的使用**
>
> 虽然 Docker Hub 是默认仓库，但仓库是通过 [开放容器倡议](https://opencontainers.org/) 实现标准化和互操作的。这使得公司和组织可以运行自己的私有仓库。通常，可信内容会从 Docker Hub 镜像（或复制）到这些私有仓库中。

## 下一步

现在你已经构建了一个镜像，是时候讨论为什么作为开发者你应该更多地了解 Docker，以及它将如何帮助你的日常任务。


<a class="button not-prose" href="/get-started/introduction/whats-next/">下一步</a>

